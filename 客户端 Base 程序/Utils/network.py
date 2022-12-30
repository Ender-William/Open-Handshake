# -*- coding: utf-8 -*-
import socket
import uuid
from psutil import net_if_addrs
import Utils.logUtil as logUtil

"""
需要注意，此模块只兼容 Linux 系统或 Windows 系统，
苹果公司 OS X 或 macOS 系统由于苹果隐私政策不兼容
"""

# Get IP Address
def get_ip():
    '''
    Get Level IP
    :return: ip
    '''
    ip = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    ip.connect(("8.8.8.8", 33550))
    ip = ip.getsockname()[0]
    log_msg = 'Utils.logUtil.get_ip IP IS: ' + ip
    logUtil.LogSys().show_info(log_msg)
    return ip


# Get MAC Address
def get_mac():
    '''
    Get Level MAC ADDRESS
    :return: MAC ADDRESS
    '''
    # 获取mac地址
    addr_num = hex(uuid.getnode())[2:]
    mac = "-".join(addr_num[i: i + 2] for i in range(0, len(addr_num), 2))
    log_msg = 'Utils.logUtil.get_mac MAC IS: ' + mac
    logUtil.LogSys().show_info(log_msg)
    return mac


def get_ip_list():
    '''
    Get IP List
    :return: Ip List
    '''
    current_ip = get_ip()
    ip_split_list = current_ip.split(".")
    ip_front_part = ip_split_list[0] + '.' + ip_split_list[1] + '.' + ip_split_list[2] + '.'
    ip_list = []
    flag = 1
    for last in range(255):
        temp = ip_front_part + str(flag)
        ip_list.append(temp)
        flag = flag + 1
    logUtil.LogSys().show_info(ip_list)
    return ip_list
