#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Title    : ''
# @Time     : 2019/11/26 13:48
# @Author   : wangguoqing27
# @Describe :
# @File     : .py
from  sqlalchemy.orm import

class User(Model):
    __table__ = 'users'

    id = IntegerField(primary_key=True)
    name = StringField()
