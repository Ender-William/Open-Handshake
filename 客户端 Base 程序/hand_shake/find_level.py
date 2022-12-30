# -*- coding: utf-8 -*-
import requests
from Utils.stringUtil import config_reader, config_writter
from Utils.network import get_ip_list, get_ip
import Utils.logUtil as logUtil

def find_level():
    # 准备请求信息 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # 头部信息
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"
    }

    # 生成层级切入路径
    level_addr = 'http://' + config_reader("LEVEL_TEMP", "level_entrance_room") + ':' + config_reader("LEVEL", "level_entrance_door") + '/data'

    # 尝试切入层级 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    response = {}

    # 开始寻找 Level 切入点
    for ip_item in get_ip_list():
        level_addr = 'http://' + ip_item + ':' + config_reader("LEVEL", "level_entrance_door") + '/data'
        try:
            get_response = requests.post(level_addr,
                                         headers=headers,
                                         timeout=0.05)
            response = get_response.json()
            break
        except Exception as e:
            logUtil.LogSys().show_warning(e)

    return response['data']