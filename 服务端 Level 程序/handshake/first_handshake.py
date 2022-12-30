# -*- coding: utf-8 -*-
from flask import jsonify
from Utils.stringUtil import check_sn, config_reader, config_writter
import Utils.logUtil as logUtil
from Utils.network import get_ip
import usual_json

"""
客户端 Python 程序样例：

    import requests
    
    headers = {
        'User-Agent': 'Apipost client Runtime/+https://www.apipost.cn/',
    }
    
    data = {
      'base_name': 'MEG',
      'base_sn': 'XKVFQA2XQA2xKVFQA2XKVFQA21234567',
      'is_regist': '2',
      'base_version': '0.0.1'
    }
    
    response = requests.post('http://host:33550/handshake/first', headers=headers, data=data)

客户端在所有数据无误的情况下获得的返回数据如下：

    {
        "could_regist": "1",
        "level_ip": "192.168.31.230",
        "level_name": "11",
        "level_version": "0.0.1",
        "regist_state": "0",
        "token": ""
    }

客户端在数据有误的情况下获得的返回数据例如：

    {
        "msg": "regist request state code is wrong."
    }

"""


def first_handshake_process(req):
    """
    第一次握手校验
    :param req: request 请求
    :return: Json 报文
    """
    # 接收请求数据 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    base_name = req.form['base_name']
    base_sn = req.form['base_sn']
    is_regist = req.form['is_regist']
    base_version = req.form['base_version']

    # 开始校验信息 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    # 判断接收数据是否为空
    if base_name.strip() == '':
        logUtil.LogSys() \
            .show_warning("handshake.first_handshake base_name is empty!")
        return usual_json.data_is_empty()
    if base_sn.strip() == '':
        logUtil.LogSys() \
            .show_warning("handshake.first_handshake base_sn is empty!")
        return usual_json.data_is_empty()
    if is_regist != '2':
        logUtil.LogSys() \
            .show_warning("handshake.first_handshake is_regist code wrong!")
        return usual_json.regist_request_state_wrong()
    if base_version.strip() == '':
        logUtil.LogSys() \
            .show_warning("handshake.first_handshake base_version is empty!")
        return usual_json.data_is_empty()

    # 校验 SN 码是否符合要求
    if not check_sn(base_sn):
        logUtil.LogSys() \
            .show_warning("handshake.first_handshake SN code wrong!")
        return usual_json.sn_code_verify_error()

    # 校验版本是否匹配
    Level_Version = config_reader("DEFAULT_GROUP", "level_version")
    if not base_version == Level_Version:
        logUtil.LogSys() \
            .show_warning("handshake.first_handshake Version ERROR")
        return usual_json.version_error(Level_Version, base_version)

    # 信息校验通过 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    # 保存基地临时信息
    config_writter("BASE_TEMP", "base_name_temp", base_name)
    config_writter("BASE_TEMP", "base_sn_temp", base_sn)

    # 返回层级信息
    Level_Name = config_reader("DEFAULT_GROUP", "level_name")
    Level_Current_Entrance_Room = get_ip()
    Level_Version = config_reader("DEFAULT_GROUP", "level_version")

    Regist_State = config_reader("REGISTER_GROUP", "regist_state")
    Could_Regist = config_reader("REGISTER_GROUP", "could_regist")

    Base_Token = config_reader("BASE_GROUP", "base_token")

    # 生成需要返回的 Json 数据
    return_msg = {
        "level_name": Level_Name,
        "level_version": Level_Version,
        "level_ip": Level_Current_Entrance_Room,
        "regist_state": Regist_State,
        "could_regist": Could_Regist,
        "token": Base_Token
    }

    logUtil.LogSys().show_info(return_msg)

    return_msg = jsonify(return_msg)

    logUtil.LogSys().show_info("handshake.first_handshake send message successful!")

    return return_msg
