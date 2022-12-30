# -*- coding: utf-8 -*-
import requests
from Utils.stringUtil import config_reader, config_writter
from Utils.network import get_ip_list
import Utils.logUtil as logUtil


def second_handshake():
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
        'base_token': base_token,
        'regist_state': is_regist,
        'base_version': base_version
    }

    # 生成层级切入路径
    level_addr = 'http://' + config_reader("LEVEL_TEMP", "level_entrance_room") + ':' + config_reader("LEVEL", "level_entrance_door") + '/handshake/second'

    # 尝试切入层级 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    response = {}
    try:
        get_response = requests.post(level_addr,
                                     headers=headers,
                                     data=data,
                                     timeout=1)
        response = get_response.json()
    except Exception as e:
        # 第二次握手失败
        logUtil.LogSys().show_warning(e)
        # 清除 Level 临时信息
        config_writter("LEVEL_TEMP", "level_name", '')
        config_writter("LEVEL_TEMP", "level_entrance_room", '')
        config_writter("LEVEL_TEMP", "level_version", '')

        # 临时更改注册信息
        config_writter("DEFAULT_GROUP", "base_regist_state", '2')
        return False

    # 开始校验信息 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # 检查反馈信息中是否包含目标信息
    if 'msg' in response:
        # 有 'msg' 表明协议有误，log 记录返回信息
        logUtil.LogSys().show_info(response['msg'])
        # 清除 Level 临时信息
        config_writter("LEVEL_TEMP", "level_name", '')
        config_writter("LEVEL_TEMP", "level_entrance_room", '')
        config_writter("LEVEL_TEMP", "level_version", '')

        # 更改注册信息
        config_writter("DEFAULT_GROUP", "base_regist_state", '2')
        return False

    # 检查是否包含关键信息
    if not 'regist_state' in response:
        logUtil.LogSys().show_warning('lose key value, second handshake failed, register cancel')
        return False
    if not 'level_ip' in response:
        logUtil.LogSys().show_warning('lose key value, second handshake failed, register cancel')
        return False
    if not 'level_mac' in response:
        logUtil.LogSys().show_warning('lose key value, second handshake failed, register cancel')
        return False
    if not 'level_name' in response:
        logUtil.LogSys().show_warning('lose key value, second handshake failed, register cancel')
        return False
    if not 'level_version' in response:
        logUtil.LogSys().show_warning('lose key value, second handshake failed, register cancel')
        return False

    # 关键信息都在
    # 获取全部关键信息
    regist_state = response['regist_state']
    level_ip = response['level_ip']
    level_mac = response['level_mac']
    level_name = response['level_name']
    level_version = response['level_version']

    # 检查 Level 的注册状态
    if not regist_state == '1':
        # 如果信息不为 1 说明 Level 未将 基地 注册
        # 清除 Level 临时信息
        config_writter("LEVEL_TEMP", "level_name", '')
        config_writter("LEVEL_TEMP", "level_entrance_room", '')
        config_writter("LEVEL_TEMP", "level_version", '')

        # 更改注册信息
        config_writter("DEFAULT_GROUP", "base_regist_state", '2')

        logUtil.LogSys().show_info("Second Handshake Failed, Register Cancel")
        return False

    # Level 已将 基地 Base 注册
    # 清空层级临时信息
    config_writter("LEVEL_TEMP", "level_name", '')
    config_writter("LEVEL_TEMP", "level_entrance_room", '')
    config_writter("LEVEL_TEMP", "level_version", '')

    # 将层级信息写入正式信息
    config_writter("LEVEL", "level_name", level_name)
    config_writter("LEVEL", "level_entrance_room", level_ip)
    config_writter("LEVEL", "level_mac_addr", level_mac)
    config_writter("LEVEL", "level_version", level_version)

    logUtil.LogSys().show_warning("register finish, successful binding")

    level_data = {
        "level_name": level_name,
        "level_entrance_room": level_ip,
        "level_mac_addr": level_mac,
        "level_version": level_version
    }

    return True
