# -*- coding: utf-8 -*-
import configparser
import Utils.logUtil as logUtil


def config_reader(group_name, item_name):
    """
    读取 ./config.ini 文件
    :param group_name: section
    :param item_name: options
    :return: msg
    """
    config = configparser.ConfigParser()
    config.read("./config.ini", encoding="utf-8")
    msg = config.get(group_name, item_name)
    return msg


def config_writter(group_name, item_name, msg):
    try:
        config = configparser.ConfigParser()
        config.read("./config.ini", encoding="utf-8")
        config.set(group_name, item_name, msg)

        # 保存配置
        config.write(open("./config.ini", "w"))

        # 记录
        logUtil.LogSys() \
            .show_warning("Utils.stringUtil.config_writter config change save!")

    except:
        logUtil.LogSys() \
            .show_warning("Utils.stringUtil.config_writter config file not exist!")
