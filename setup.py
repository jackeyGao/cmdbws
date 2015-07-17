# -*- coding: utf-8 -*-
'''
File Name: setup.py
Author: JackeyGao
mail: junqi.gao@shuyun.com
Created Time: 四  5/14 17:04:52 2015
'''
import os
import sys
from setuptools import setup
from cmdbuild import VERSION

if sys.argv[-1] == 'publish':
    os.system('python setup.py sdist upload -r internal')
    sys.exit()

def long_description():
    with open("README.md") as f:
        content = f.read()
    return content

setup(
    name = 'cmdbws',
    version = VERSION,
    install_requires = ['requests'],
    py_modules = ['cmdbuild'],
    author = 'JackeyGao',
    author_email = 'junqi.gao@shuyun.com',
    url = 'http://git.yunat.com/projects/OPS/repos/cmws/browse',
    description = 'A client of cmdbuild rest web service',
    long_description = long_description(),
    classifiers = [
        'Development Status :: 4 - Beta',
        'Topic :: Internet',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python 2.6',
        'Programming Language :: Python 2.7',
    ],
)
