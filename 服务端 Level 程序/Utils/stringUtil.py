# -*- coding: utf-8 -*-
import re
import configparser
import string
import Utils.logUtil as logUtil


def check_sn(sn):
    """
    SN总长度为32位，其中前6位为大写字母、后4位是数字、中间22位为大小写字母与数字
    :param sn: str
    :return: bool
    """
    if len(sn) != 32:
        return False
    if not re.match(r'[A-Z]{6}[A-Za-z0-9]{22}[0-9]{4}', sn):
        return False
    return True

def check_token(token):
    # 校验Token
    if len(token) != 32:
        return False
    for i in token:
        if i not in string.ascii_letters + string.digits:
            return False
    return True


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
