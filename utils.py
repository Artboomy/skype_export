#! python3
# -*- coding: utf-8 -*-
# Logger initialization

import logging
import logging.handlers
import re
import os
import datetime as dt


def get_cur_time_filename():
    now = dt.datetime.today().timetuple()
    now = '{0}_{1}_{2}_{3}_{4}_{5}'.format(str(now.tm_year), str(now.tm_mon), str(now.tm_mday), str(now.tm_hour),
                                           str(now.tm_min), str(now.tm_sec))
    return now


def logger_init(log_name_obj=None, prefix=None):
    re_check = re.compile(u'[.]log')
    if log_name_obj is None:
        log_name_obj = get_cur_time_filename()

    if not re.search(re_check, log_name_obj):
        log_name_obj += '.log'

    if prefix is not None:
        log_name_obj = prefix + log_name_obj

    dir_name = str(os.path.dirname(os.path.abspath(__file__)))
    if not os.path.exists(dir_name + '/logs/'):
        os.makedirs(dir_name + '/logs/')

    log_name = dir_name + '/logs/{0}'.format(log_name_obj)
    logging.basicConfig(format=u'%(levelname)s [%(asctime)s] : %(message)s', filename=log_name, level=logging.INFO)
    try:
        my_logger_obj = logging.getLogger('{0} logger'.format(log_name_obj))
        return my_logger_obj
    except Exception as e:
        print('Logger init failure. Details: ', e)


def list_db():
    path = os.getenv('APPDATA') + '\Skype'
    return find_all('main.db', path)


# http://stackoverflow.com/questions/1724693/find-a-file-in-python
def find_all(name, path):
    result = []
    for root, dirs, files in os.walk(path):
        if name in files:
            result.append(os.path.join(root, name))
    return result
