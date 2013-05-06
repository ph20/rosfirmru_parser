#!/usr/bin/env python
# -*- coding: utf-8 -*-

DEBUG = False
MYSQL_DB = 'grab'
MYSQL_USER = 'grab'
MYSQL_PASS = 'grab_cHy6c3W'
INITIAL_URLS = ['http://www.rosfirm.ru/catalog']
DB_FILE = '/root/pars/rosfirm.ru/company_db.sqlite'
CACHE_DIR = '/root/pars/rosfirm.ru_cache'
LOG_DIR = '/root/pars/rosfirm.ru/log_dir'
PROXY_LIST = '/root/proxylist.txt'
GRAB_LOG = '/root/pars/rosfirm.ru/grab.log'
NETWORK_LOG = '/root/pars/rosfirm.ru/grab.network.log'
FATAL_ERROR_DUMP = '/root/pars/rosfirm.ru/fatal_errors.txt'
THREAD_NUMBER = 30

if DEBUG:
    LOG_TASKNAME = True
else:
    LOG_TASKNAME = False