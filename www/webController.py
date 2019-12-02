#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Title    : ''
# @Time     : 2019/12/2 20:29
# @Author   : wangguoqing27
# @Describe :
# @File     : .py

import logging;logging.basicConfig(level=logging.INFO)

import asyncio
import functools
import inspect
from urllib import request
from urllib.parse import parse_qs

from aiohttp.web_routedef import get

def get(path):
    '''
    Define decorator @get('/path')
    :param path:
    :return:
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'GET'
        wrapper.__route__ = path
        return wrapper
    return decorator

def post(path):
    '''
    Define decorator @post('/path')
    :param path:
    :return:
    '''
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kw):
            return func(*args, **kw)
        wrapper.__method__ = 'POST'
        wrapper.__route__ = path
        return wrapper
    return decorator

class RequestHandler(object):

    def __init__(self, app, fn):
        self._app = app
        self._func = fn

    @asyncio.coroutine
    def __call__(self, *args, **kw):
        kw = ... # 获取参数
        r = yield from self._func(**kw)
        return r

def add_route(app,fn):
    method = getattr(fn, '__method__', None)
    path = getattr(fn, '__route__', None)
    if path is None or method is None:
        raise ValueError('@get or @post not defined in %s.' % str(fn))
    if not asyncio.iscoroutinefunction(fn) and not inspect.isgeneratorfunction(fn):
        fn = asyncio.coroutine(fn)
        logging.info('add route %s %s => %S(%s)' % (method, path, fn.__name__,
                                                   ', '.join(inspect.signature(fn).parameters.keys())))
        app.route.add_route(method, path, RequestHandler(app, fn))

def add_routes(app, moudel_name):
    n = moudel_name.rfind('.')
    if n == (-1):
        mod = __import__(moudel_name, globals(), locals())
    else:
        name = moudel_name[n + 1]
        mod = getattr(__import__(moudel_name[:n], globals(), locals(), [name]), name)

    for attr in dir(mod):
        if attr.startswith('_'):
            continue
        fn = getattr(mod, attr)
        if callable(fn):
            method = getattr(fn, '__method__', None)
            path = getattr(fn, '__route__', None)
            if method and path:
                add_route(app, fn)

@asyncio.coroutine
def handle_url_xxx(request):
    pass
url_param = request.match_info['key']
query_param = parse_qs(request.query_string)

@get('/blog/{id}')
def get_blog(id):
    pass

@get('/api/comments')
def api_comments(*, page='1'):
    ##pass
    return {
        '__template__': 'index.html',
        'data': '...'
    }