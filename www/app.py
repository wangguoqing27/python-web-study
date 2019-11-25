#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Title    : ''
# @Time     : 2019/11/25 14:46
# @Author   : wangguoqing27
# @Describe :
# @File     : .py
import logging; logging.basicConfig(level=logging.INFO)

import asyncio, os, json, time,aiomysql
from datetime import datetime

from aiohttp import web

def index(request):
    return web.Response(body=b'<hl>Awesome</hl>',content_type='text/html')

@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET','/',index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('server started at http://127.0.0.1:9000...')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()

@asyncio.coroutine
def create_pool(pool, **kw):
    '''
    连接数据源
    :param pool:
    :param kw:
    :return:
    '''
    logging.info('create database create database connection pool ...')
    global __pool
    __pool = yield from aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['user'],
        password=kw['password'],
        db=kw['db'],
        charset=kw.get('charset','utf8'),
        autocommint=kw.get('autocommit',True),
        maxsize=kw.get('maxsize',10),
        minsize=kw.get('minsize',1),
        loop=loop
    )

@asyncio.coroutine
def select(sql,args,size=None):
    '''
    SQL语句的占位符是?，而MySQL的占位符是%s，select()函数在内部自动替换。注意要始终坚持使用带参数的SQL，
    而不是自己拼接SQL字符串，这样可以防止SQL注入攻击。
    注意到yield from将调用一个子协程（也就是在一个协程中调用另一个协程）并直接获得子协程的返回结果。
    如果传入size参数，就通过fetchmany()获取最多指定数量的记录，否则，通过fetchall()获取所有记录。
    :param sql:
    :param args: 传参
    :param size: 获取多少条数据
    :return:
    '''
    logging.log(sql, args)
    global __pool
    with (yield from __pool) as conn:
        cur = yield from conn.cursor(aiomysql.DictCursor)
        yield from cur.execute(sql.replace('?','%s'),args or ())
        if size:
            rs = yield from cur.fetchmany(size)
        else:
            rs = yield from cur.fetchall()
        yield from cur.close()
        logging.info('rows returned: %s' % len(rs))
        return rs

