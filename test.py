# -*- coding: utf-8 -*-
'''
File Name: test.py
Author: JackeyGao
mail: junqi.gao@shuyun.com
Created Time: 一  7/ 6 17:40:15 2015
'''

from cmdbws import Cmdbws

if __name__ == '__main__':
    c = Cmdbws("admin", "xxxxxxx")
    cls = c.get_class("config")
    print(cls.list())


