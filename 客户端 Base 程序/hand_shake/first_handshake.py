# -*- coding: utf-8 -*-
import requests
from Utils.stringUtil import config_reader, config_writter
from Utils.network import get_ip_list
import Utils.logUtil as logUtil


def first_handshake():

    # 准备请求信息 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # 头部信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
    }

    # 准备基地信息
    base_name = config_reader("DEFAULT_GROUP", "base_name")
    base_sn = config_reader("DEFAULT_GROUP", "base_sn")
    base_token = config_reader("DEFAULT_GROUP", "base_token")
    is_regist = config_reader("DEFAULT_GROUP", "base_regist_state")
    base_version = config_reader("DEFAULT_GROUP", "base_version")

    data = {
        'base_name': base_name,
        'base_sn': base_sn,
        'is_regist': is_regist,
        'base_version': base_version
    }

    response = {}
    # 开始寻找 Level 切入点
    for ip_item in get_ip_list():
        level_addr = 'http://' + ip_item + ':' + config_reader("LEVEL", "level_entrance_door") + '/handshake/first'
        try:
            get_response = requests.post(level_addr,
                                         headers=headers,
                                         data=data,
                                         timeout=0.05)
            response = get_response.json()
            break
        except Exception as e:
            logUtil.LogSys().show_warning(e)

    # 开始校验信息 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    if 'msg' in response:
        # 有 'msg' 表明协议有误，log 记录返回信息
        logUtil.LogSys().show_info(response['msg'])
        return False
    if not 'could_regist' in response:
        # could_regist 不存在
        logUtil.LogSys().show_info("cannot register, cancel first handshake")
        return False
    if not 'token' in response:
        # 'token' 不存在
        logUtil.LogSys().show_info("token name miss, cancel first handshake")
        return False
    if not response['token'] == '':
        # 'token' 存在且不为空，说明 Level 与 Base 绑定过，但 Level 地址变了
        if response['token'] == base_token:
            config_writter("LEVEL", "level_entrance_room",response['level_ip'])
            logUtil.LogSys().show_info("Level IP Changed!")
            return True
        return False
    if not response['could_regist'] == '1':
        # 不可以注册
        logUtil.LogSys().show_info("register refuse, cancel first handshake")
        return False
    if not response['regist_state'] == '0':
        # 不可以注册
        logUtil.LogSys().show_info("level registered, cancel first handshake")
        return False

    # 完成信息校验 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    # 保存 Level 临时信息
    config_writter("LEVEL_TEMP", "level_name", response['level_name'])
    config_writter("LEVEL_TEMP", "level_entrance_room", response['level_ip'])
    config_writter("LEVEL_TEMP", "level_version", response['level_version'])

    # 临时更改注册信息
    config_writter("DEFAULT_GROUP", "base_regist_state", '1')

    return True
