# -*- coding: utf-8 -*-
from hand_shake.first_handshake import first_handshake
from hand_shake.second_handshake import second_handshake
from hand_shake.untie_level import untie_level_process
from hand_shake.find_level import find_level
from Utils.stringUtil import config_reader
import Utils.logUtil as logUtil



class LevelBinding:

    def __init__(self):
        pass

    def Find_Level(self):
        # 查找服务器
        return find_level()

    def Binding_New_Level(self):
        # 先执行第一次握手
        if not first_handshake():
            return False

        # 检查层级是否早已注册
        if config_reader("LEVEL", "level_entrance_room") != '':
            # 层级切入口不为空，说明层级早已绑定过
            # 说明层级地址为 DHCP 分配，第一次握手只是确定一下新地址
            return True

        # 层级切入口为空，说明层级并未注册
        if not second_handshake():
            return False

        # 完成层级的注册
        return True

    def Untie_Level(self):
        # 开始解绑程序
        if not untie_level_process():
            logUtil.LogSys().show_warning("Untie failed, unknown error")
            return False

        logUtil.LogSys().show_info("Untie success")
        return True