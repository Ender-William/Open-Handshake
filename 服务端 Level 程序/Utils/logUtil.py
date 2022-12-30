# -*- coding: utf-8 -*-
import logging
'''
模块主要用于封装一些常用的 Log 方法

Модули в основном используются для инкапсуляции некоторых распространенных методов Log

The module is mainly used to encapsulate some common log methods

モジュールは主に一般的なLogメソッドをカプセル化するために使用されています
'''


class LogSys:

    def __init__(self):
        logging.basicConfig(format='%(asctime)s %(levelname)s %(message)s',
                            level=logging.DEBUG,)

    # Show Debug Log
    def show_debug(self, msg):
        logging.debug(msg)

    # Show Info Log
    def show_info(self, msg):
        logging.info(msg)

    # Show Warning Log
    def show_warning(self, msg):
        logging.warning(msg)

    # Show Warning Log
    def show_error(self, msg):
        logging.error(msg)

    # Show Warning Log
    def show_critical(self, msg):
        logging.critical(msg)