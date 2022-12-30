# -*- coding: utf-8 -*-
from flask import Flask, request, jsonify
from Utils.network import get_ip
from Utils.stringUtil import config_reader
from handshake.first_handshake import first_handshake_process
from handshake.second_handshake import second_handshake_process
from handshake.untie_level import untie_level_process

app = Flask(__name__)
app.config['host'] = config_reader("DEFAULT_GROUP", "level_entrance_room")
app.config['port'] = config_reader("DEFAULT_GROUP", "level_entrance_door")


@app.route('/data', methods=['POST'])
def get_data():

    return jsonify({ "data": get_ip(),})

@app.route('/handshake/first', methods=['POST'])
def first_handshake():
    data = request
    result = first_handshake_process(data)
    return result

@app.route('/handshake/second', methods=['POST'])
def second_handshake():
    data = request
    result = second_handshake_process(data)
    return result

@app.route('/handshake/untie', methods=['POST'])
def untie_level():
    data = request
    result = untie_level_process(data)
    return result

if __name__ == '__main__':
    app.run(host=app.config['host'], port=app.config["port"])

