# -*- coding: utf-8 -*-
from flask import jsonify


def data_is_empty():
    return jsonify({'msg':'data is empty, you are not BASE or something wrong.'})

def regist_request_state_wrong():
    return jsonify({'msg':'regist request state code is wrong.'})

def sn_code_verify_error():
    return jsonify({'msg': 'sn code verify is not pass'})

def version_error(Level, Base):
    return jsonify({'msg':'Version ERROR, Lavel is ' + Level + ' and Base is ' + Base})

def verify_not_pass():
    return jsonify({'msg':'verify not pass'})


