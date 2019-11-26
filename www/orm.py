#!/usr/bin/env python
# -*- coding:utf-8 -*-
# @Title    : ''
# @Time     : 2019/11/26 14:21
# @Author   : wangguoqing27
# @Describe :
# @File     : .py
import logging; logging.basicConfig(level=logging.INFO)

class Model(dict, metaclass=ModelMetaclass):

    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"'Model' object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self,key,None)

    def getVlaueOrDefault(self,key):
        value = getattr(self,key,None)
        if value is None:
            field = self.__mappings__[key]
            if field.default is not None
                value = field.default() if callable(field.default) else field.default
                logging.debug('useing default value for %s: %s' % (key,str(value)))
                setattr(self, key, value)
        return value

class Field(object):
    def __init__(self, name, colume_type, primary_key, default):
        self.name = name
        self.colume_type = colume_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s:%s>' % (self.__class__.__name__, self.colume_type, self.primary_key, self.default)
