from flask import Flask, jsonify, request, send_file, send_from_directory, render_template
from flask_socketio import SocketIO, emit
from flask_cors import CORS

import time
from os import popen
import sys
import cv2


import os
import json
from werkzeug.routing import BaseConverter
import random
import traceback

import base64
from PIL import Image
from io import BytesIO
import redis

sub = redis.Redis('127.0.0.1', 6379)

class RegexConverter(BaseConverter):
    def __init__(self, map, *args):
        self.map = map
        self.regex = args[0]


app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mlbbmlbb@118.89.246.97/Detect_api'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mlbbmlbb@127.0.0.1/Detect_api'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:mlbbmlbb@127.0.0.1/Camera_Web'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/step_local'
app.config['MONGO_URI'] = 'mongodb://192.168.88.27:27017/step_local'

app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads/'  # 保存文件位置
app.url_map.converters['regex'] = RegexConverter

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app, resources=r'/*')


@app.route('/det_img', methods=['POST'])
def det_img():
    try:
        now = time.time()
        img = cv2.imread('2.jpg')
        imread = time.time()
        print('imread-{}'.format(imread-now))
        img_vis = det(img)
        det_time = time.time()
        print('det time--{}'.format(det_time-imread))
        cv2.imwrite('{}.jpg'.format(int(now)), img_vis)
        print(time.time() - det_time)
        dic = {}
        dic['Results'] = 200
        dic['Cause'] = 'OK'
        return jsonify(dic)
    except Exception as e:
        print('***********')
        print(e)
        traceback.print_exc()
        print('***********')
        dic = {}
        dic['Results'] = 400
        dic['Cause'] = 'error'
        return jsonify(dic)
@app.route('/generate_reports', methods=['POST'])
def generate_report():
    try:
        res = request.json
        # print(json.dumps(res))

        # imgs = res['data']['imgs']
        # for i, img, in enumerate(imgs):
        #     img = get_b64_img(img)
        #     binary_img_data = base64.b64decode(img)
        #     # file = BytesIO(binary_img_data)
        #     with open('{}.jpg'.format(i), 'wb') as f:
        #         f.write(binary_img_data)

        pwd = os.getcwd()
        return send_from_directory(pwd + '/static/word', 'report.pdf', as_attachment=True)

    except Exception as e:
        print('***********')
        print(e)
        traceback.print_exc()
        print('***********')
        dic = {}
        dic['Results'] = 400
        dic['Cause'] = 'error'
        return jsonify(dic)

@app.route('/change_mode', methods=['POST'])
def change_mode():
    try:
        res = request.json
        mode = res['data']['mode']
        print(mode)
        sub.publish('PriVision_model_checker', str(mode))
        dic = {}
        dic['Results'] = 200
        dic['Cause'] = 'OK'
        return jsonify(dic)
    except Exception as e:
        print('***********')
        print(e)
        traceback.print_exc()
        print('***********')
        dic = {}
        dic['Results'] = 400
        dic['Cause'] = 'error'
        return jsonify(dic)

@socketio.on('', namespace='/Camera_Web_ws')
def test_message(message):
    print(message)
    emit('my response', {'data': message['data']})


@socketio.on('my broadcast event', namespace='/Camera_Web_ws')
def test_message(message):
    print('my broadcast event')
    emit('my response', {'data': message['data']}, broadcast=True)


@socketio.on('connect', namespace='/Camera_Web_ws')
def test_connect():
    print('Web connected')


@socketio.on('disconnect', namespace='/Camera_Web_ws')
def test_disconnect():
    print('Web disconnected')


@socketio.on('connect', namespace='/Camera_Client_ws')
def test_connect():
    print('Client connected')


@socketio.on('disconnect', namespace='/Camera_Client_ws')
def test_disconnect():
    print('Client disconnected')

@socketio.on('new_state', namespace='/Camera_Client_ws')
def test_setimage(img):
    try:
        # print(img)
        socketio.emit('new_state', {'data': img}, namespace='/Camera_Web_ws')
    except Exception as e:
        print('***********')
        print(e)
        traceback.print_exc()
        print('***********')

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=9000, debug=True)
    socketio.run(app, host='0.0.0.0', port=7000, )
