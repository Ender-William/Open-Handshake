# -*- coding: utf-8 -*-
from flask import jsonify
from Utils.stringUtil import check_sn, config_reader, config_writter
import Utils.logUtil as logUtil
import usual_json


def untie_level_process(req):
    # 接收请求数据 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    base_name = req.form['base_name']
    base_sn = req.form['base_sn']
    base_token = req.form['base_token']
    level_name = req.form['level_name']

    # 开始校验信息 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    # 判断接收数据是否为空
    if base_name.strip() == '':
        logUtil.LogSys() \
            .show_warning("handshake.untie base_name is empty!")
        return usual_json.data_is_empty()
    if base_sn.strip() == '':
        logUtil.LogSys() \
            .show_warning("handshake.untie base_sn is empty!")
        return usual_json.data_is_empty()
    if base_token.strip() == '':
        logUtil.LogSys() \
            .show_warning("handshake.untie base_token is empty!")
        return usual_json.data_is_empty()
    if level_name.strip() == '':
        logUtil.LogSys() \
            .show_warning("handshake.untie level_name is empty!")
        return usual_json.data_is_empty()

    # 校验信息是否由目标服务器发来 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    # 准备层级数据
    config_base_name = config_reader("BASE_GROUP", "base_name")
    config_base_sn = config_reader("BASE_GROUP", "base_sn")
    config_base_token = config_reader("BASE_GROUP", "base_token")
    config_level_name = config_reader("DEFAULT_GROUP", "level_name")

    # 对比数据
    if not config_base_name == base_name:
        return usual_json.verify_not_pass()
    if not config_base_sn == base_sn:
        return usual_json.verify_not_pass()
    if not config_base_token == base_token:
        return usual_json.verify_not_pass()
    if not config_level_name == level_name:
        return usual_json.verify_not_pass()

    # 删除层级绑定数据
    config_writter("BASE_GROUP", "base_name", '')
    config_writter("BASE_GROUP", "base_sn", '')
    config_writter("BASE_GROUP", "base_token", '')
    config_writter("BASE_GROUP", "base_version", '')
    config_writter("BASE_GROUP", "base_regist_state", '')

    # 修改本层级注册信息
    config_writter("REGISTER_GROUP", "regist_state", '0')
    config_writter("REGISTER_GROUP", "could_regist", '1')

    return_msg = {
        "level_name": config_level_name,
        "del_signal": "1"
    }

    logUtil.LogSys().show_info(return_msg)

    return_msg = jsonify(return_msg)

    logUtil.LogSys().show_info("handshake.untie untie successful")

    return return_msg
