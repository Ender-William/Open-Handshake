# -*- coding: utf-8 -*-
import requests
from Utils.stringUtil import config_reader, config_writter
import Utils.logUtil as logUtil


def untie_level_process():
    # 准备请求信息 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # 头部信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
    }

    # 准备基地信息
    config_base_name = config_reader("DEFAULT_GROUP", "base_name")
    config_base_sn = config_reader("DEFAULT_GROUP", "base_sn")
    config_base_token = config_reader("DEFAULT_GROUP", "base_token")
    config_is_regist = config_reader("DEFAULT_GROUP", "base_regist_state")
    config_base_version = config_reader("DEFAULT_GROUP", "base_version")

    config_level_name = config_reader("LEVEL", "level_name")
    config_level_entrance_room = config_reader("LEVEL", "level_entrance_room")
    config_level_entrance_door = config_reader("LEVEL", "level_entrance_door")

    data = {
        'base_name': config_base_name,
        'base_sn': config_base_sn,
        'base_token': config_base_token,
        'level_name': config_level_name,
    }

    # 生成层级切入路径
    level_addr = 'http://' + config_level_entrance_room + ':' + config_level_entrance_door + '/handshake/untie'

    # 尝试切入层级 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    response = {}
    try:
        get_response = requests.post(level_addr,
                                     headers=headers,
                                     data=data,
                                     timeout=1)
        response = get_response.json()
    except Exception as e:
        # 联机删除失败
        logUtil.LogSys().show_warning("Request Error")
        logUtil.LogSys().show_warning(e)
        return False

    # 检查反馈信息中是否包含目标信息
    if 'msg' in response:
        # 有 'msg' 表明协议有误，log 记录返回信息
        logUtil.LogSys().show_info(response['msg'])
        return False

    # 检查是否包含关键信息
    if not 'level_name' in response:
        logUtil.LogSys().show_warning('lose key value, second handshake failed, register cancel')
        return False
    if not 'del_signal' in response:
        logUtil.LogSys().show_warning('lose key value, second handshake failed, register cancel')
        return False

    # 获取全部关键信息
    level_name = response['level_name']
    del_signal = response['del_signal']

    if not level_name == config_level_name:
        return False
    if not del_signal == '1':
        return False

    # 完成解绑，清除所有本地信息
    config_writter("LEVEL", "level_name", "")
    config_writter("LEVEL", "level_entrance_room", "")
    config_writter("LEVEL", "level_version", "")
    config_writter("LEVEL", "level_mac_addr", "")

    # 恢复注册信息
    config_writter("DEFAULT_GROUP", "base_regist_state", "2")

    return True
