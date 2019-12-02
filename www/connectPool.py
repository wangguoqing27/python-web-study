#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Title    : ''
# @Time     : 2019/11/25 18:46
# @Author   : wangguoqing27
# @Describe :
# @File     : .py
import logging;logging.basicConfig(level=logging.INFO)
import www.orm as orm
import www.app as app
from www.User import User, Blog, Comment

def test():
    yield from app.create_pool(user='awesome', password='123456', database='awesome')
    u = User(name='Test', email='test@example.com', passwd='1234567890', image='about:blank')

    yield from u.save()

for x in test():
    pass


