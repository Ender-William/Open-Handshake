from flask import jsonify
from Utils.stringUtil import check_sn, check_token, config_reader, config_writter
import Utils.logUtil as logUtil
from Utils.network import get_ip, get_mac
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
      'base_token': 'ot20pLAhCnISPNNdwWy1XYs1Owkb6env',
      'regist_state': '1',
      'base_version': '0.0.1'
    }
    
    response = requests.post('http://host:33550/handshake/second', headers=headers, data=data)

客户端在所有数据无误的情况下获得的返回数据如下：

    {
        "level_ip": "192.168.31.230",
        "level_mac": "ac-de-48-00-11-22",
        "level_name": "11",
        "level_version": "0.0.1",
        "regist_state": "1"
    }

客户端在数据有误的情况下获得的返回数据例如：

    {
        "msg": "regist request state code is wrong."
    }


"""

def second_handshake_process(req):
    # 接收请求数据 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-
    base_name = req.form['base_name']
    base_sn = req.form['base_sn']
    base_token = req.form['base_token']
    base_version = req.form['base_version']
    regist_state = req.form['regist_state']

    # 开始校验信息 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    # 判断接收信息是否为空
    if base_name.strip() == '':
        logUtil.LogSys() \
            .show_warning("handshake.second_handshake base_name is empty!")
        return usual_json.data_is_empty()
    if base_sn.strip() == '':
        logUtil.LogSys() \
            .show_warning("handshake.second_handshake base_sn is empty!")
        return usual_json.data_is_empty()
    if base_token.strip() == '':
        logUtil.LogSys() \
            .show_warning("handshake.second_handshake base_token is empty!")
        return usual_json.data_is_empty()
    if base_version.strip() == '':
        logUtil.LogSys() \
            .show_warning("handshake.second_handshake base_version is empty!")
        return usual_json.data_is_empty()
    if regist_state.strip() != '1':
        # 注册状态不为 1 时，表明基地未将层级注册，因此层级此时应当放弃握手
        # 清除掉该基地的临时信息
        logUtil.LogSys() \
            .show_warning("handshake.second_handshake cancel regist!")
        config_writter("BASE_TEMP", "base_name_temp", '')
        config_writter("BASE_TEMP", "base_sn_temp", '')
        return usual_json.regist_request_state_wrong()

    # 校验 base_name 是否一致
    if not base_name == config_reader("BASE_TEMP", "base_name_temp"):
        logUtil.LogSys() \
            .show_warning("handshake.second_handshake base_name NOT SAME or Over time!")
        # 清空基地临时信息
        config_writter("BASE_TEMP", "base_name_temp", '')
        config_writter("BASE_TEMP", "base_sn_temp", '')
        return usual_json.verify_not_pass()

    # 校验 SN 码是否符合要求
    if not check_sn(base_sn):
        logUtil.LogSys() \
            .show_warning("handshake.second_handshake SN code wrong!")
        # 清空基地临时信息
        config_writter("BASE_TEMP", "base_name_temp", '')
        config_writter("BASE_TEMP", "base_sn_temp", '')
        return usual_json.sn_code_verify_error()

    # 校验 SN 码是否一致
    if not base_sn == config_reader("BASE_TEMP", "base_sn_temp"):
        logUtil.LogSys() \
            .show_warning("handshake.second_handshake SN NOT SAME!")
        # 清空基地临时信息
        config_writter("BASE_TEMP", "base_name_temp", '')
        config_writter("BASE_TEMP", "base_sn_temp", '')
        return usual_json.verify_not_pass()

    # 校验 Token 码是否符合要求
    if not check_token(base_token):
        logUtil.LogSys() \
            .show_warning("handshake.second_handshake Token Wrong!")
        # 清空基地临时信息
        config_writter("BASE_TEMP", "base_name_temp", '')
        config_writter("BASE_TEMP", "base_sn_temp", '')
        return usual_json.verify_not_pass()

    # 信息校验通过 -~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-~-

    # 保存基地信息
    config_writter("BASE_GROUP", "base_name", base_name)
    config_writter("BASE_GROUP", "base_sn", base_sn)
    config_writter("BASE_GROUP", "base_token", base_token)
    config_writter("BASE_GROUP", "base_version", base_version)
    config_writter("BASE_GROUP", "base_regist_state", regist_state)

    # 清空基地临时信息
    config_writter("BASE_TEMP", "base_name_temp", '')
    config_writter("BASE_TEMP", "base_sn_temp", '')

    # 修改层级注册信息
    config_writter("REGISTER_GROUP", "regist_state", '1')  # regist_state 为 1 表明此层级已被注册，0 表示层级为未被注册
    config_writter("REGISTER_GROUP", "could_regist", '0')  # could_regist 为 1 表明此层级可以注册，0 标识此层级不可注册

    # 生成层级信息
    Level_Name = config_reader("DEFAULT_GROUP", "level_name")
    Level_Version = config_reader("DEFAULT_GROUP", "level_version")
    Level_Current_Entrance_Room = get_ip()
    Level_Current_Mac_Addr = get_mac()
    Regist_State = config_reader("REGISTER_GROUP", "regist_state")

    # 生成需要返回的 Json 数据
    return_msg = {
        "regist_state": Regist_State,
        "level_ip": Level_Current_Entrance_Room,
        "level_mac": Level_Current_Mac_Addr,
        "level_name": Level_Name,
        "level_version": Level_Version
    }

    logUtil.LogSys().show_info(return_msg)

    return_msg = jsonify(return_msg)

    logUtil.LogSys().show_info("handshake.second_handshake send message successful!")

    return return_msg
