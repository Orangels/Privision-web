import socketio
import sys
import os
import cv2
import numpy as np
import time
import base64
from multiprocessing import Process, Queue, Pool, Manager
import subprocess as sp
import ctypes
import threading
import redis

sys.path.append('/home/user/workspace/Pet-engine')
from modules import pet_engine

sio = socketio.Client()

image_path = '/home/user/Program/ls/PriVision/static/uploads/'
url_path = '/static/uploads/'

PRIVISION_MODEL_NUM = 0

def connect():
    print("I'm connected!")


@sio.on('connect', namespace='/Camera_Client_ws')
def on_connect():
    print("I'm connected to the /chat namespace!")


def process_det_img(q, gpu_num=0):
    out_put_w = 1280

    module = pet_engine.MODULES['ObjectDet']
    det = module(cfg_list=['MODULES.OBJDET.DETECTIONS_PER_IMG', 2, 'MODULES.OBJDET.GPU_ID', gpu_num])
    # det = module(cfg_list=['MODULES.OBJDET.DETECTIONS_PER_IMG', 2])
    # det = module(cfg_file='/home/user/workspace/privision_test/test.yaml', cfg_list=['VIS.VIS_TH', 0.7,
    #                                                                                  'VIS.SHOW_BOX.COLOR_SCHEME',
    #                                                                                  'instance'])

    sio.connect('http://192.168.88.91:9000', namespaces=['/Camera_Client_ws'])
    # camera_path = "rtsp://192.168.88.29:554/user=admin&password=admin&channel=1&stream=0.sdp?real_stream"
    # cap = cv2.VideoCapture(camera_path)
    #
    # ret, frame = cap.read()
    # scale = frame.shape[0] / frame.shape[1]
    # scale = round(scale, 2)
    # print(scale)
    scale = 1.78

    while 1:
        if not q.empty():
            frame = q.get(True)
            frame = det(frame)
            frame = cv2.resize(frame, (out_put_w, int(out_put_w * scale)))
            img_code = cv2.imencode('.jpg', frame)[1]
            img_code = np.array(img_code)
            img_code = img_code.tostring()
            img_code = base64.b64encode(img_code).decode('utf-8')
            sio.emit('new_state', {'img': img_code}, namespace='/Camera_Client_ws')

            # time_name = str(round(time.time()))
            # img_tmp_path = image_path + time_name + '.jpg'
            # url_tmp_path = url_path + time_name + '.jpg'
            # cv2.imwrite(img_tmp_path, frame)
            # sio.emit('new_state', {'img': url_tmp_path}, namespace='/Camera_Client_ws')

    # sio.disconnect()


def det_rtmp_img(q, gpu_num=0):
    so = ctypes.cdll.LoadLibrary
    lib = so("/home/user/Program/ffmpeg_demo/python_c/release/libpython_c.so")
    module = pet_engine.MODULES['ObjectDet']
    det = module(cfg_list=['MODULES.OBJDET.DETECTIONS_PER_IMG', 2, 'MODULES.OBJDET.GPU_ID', gpu_num])
    # det = module(cfg_file='/home/user/workspace/privision_test/test.yaml', cfg_list=['VIS.VIS_TH', 0.7,
    #                                                                                  'VIS.SHOW_BOX.COLOR_SCHEME',
    #                                                                                  'instance'])
    lib.initRtmp(bytes('rtmp://192.168.88.91:1935/rtmplive/room', 'utf8'), 1920, 1080, 20)
    while 1:
        if not q.empty():
            frame = q.get(True)
            # frame = det(frame)
            img_name = '{}.jpg'.format(round(time.time()))
            start = time.time()
            cv2.imwrite(img_name, frame)
            # print('write cost -- {}'.format(time.time()-start))
            path = bytes(img_name, 'utf8')
            a = lib.rtmp(path)
            os.remove(img_name)


def redis_notify_checker():
    global PRIVISION_MODEL_NUM
    print('PriVision_model_checker checkers redis start work')
    try:
        sub_strict = redis.StrictRedis('127.0.0.1', 6379).pubsub()
        sub_strict.subscribe('PriVision_model_checker')
        for i in sub_strict.listen():
            if isinstance(i.get('data'), bytes):
                redis_data = i.get('data').decode()
                if redis_data == '0':
                    PRIVISION_MODEL_NUM = 0
                if redis_data == '1':
                    PRIVISION_MODEL_NUM = 1
                if redis_data == 'exit':
                    # worker退出的过程中将无法响应其他数据修改请求
                    print('monitor receive restart signal.')
                    sub_strict.unsubscribe('PriVision_model_checker')
                    break
    except Exception as e:
        print(e)
        try:
            sub_strict.unsubscribe('PriVision_model_checker')
        except Exception:
            pass


def det_rtmp_py(q, gpu_num=0):
    global PRIVISION_MODEL_NUM
    module_num_tmp = PRIVISION_MODEL_NUM
    d_checker = threading.Thread(name='redis_notify_checker', target=redis_notify_checker)
    d_checker.start()

    rtmpUrl = "rtmp://192.168.88.91:1935/rtmplive/room"
    command_0 = ['ffmpeg',
               '-y',
               '-f', 'rawvideo',
               '-vcodec', 'rawvideo',
               '-pix_fmt', 'bgr24',
               '-s', "{}x{}".format(1920, 1080),
               # '-r', str(12),
               '-r', str(13),
               '-i', '-',
               '-c:v', 'libx264',
               '-pix_fmt', 'yuv420p',
               # '-bf', '0',
               # '-g', '50',
               # '-b:v', "100k",
               # '-x264opts', "bframes=0",
               # '-preset', 'ultrafast',
               '-preset', 'superfast',
               # "-tune", "zerolatency",
               '-f', 'flv',
               rtmpUrl
               ]
    command_1 = ['ffmpeg',
                 '-y',
                 '-f', 'rawvideo',
                 '-vcodec', 'rawvideo',
                 '-pix_fmt', 'bgr24',
                 '-s', "{}x{}".format(1920, 1080),
                 # '-r', str(12),
                 '-r', str(10),
                 '-i', '-',
                 '-c:v', 'libx264',
                 '-pix_fmt', 'yuv420p',
                 # '-bf', '0',
                 # '-g', '50',
                 # '-b:v', "100k",
                 # '-x264opts', "bframes=0",
                 # '-preset', 'ultrafast',
                 '-preset', 'superfast',
                 # "-tune", "zerolatency",
                 '-f', 'flv',
                 rtmpUrl
                 ]

    print(' '.join(command_0))
    # 管道配置
    p = sp.Popen(command_0, stdin=sp.PIPE, stdout=sp.PIPE)
    module = pet_engine.MODULES['ObjectDet']
    det = module(cfg_file='/home/user/Program/ls/PriVision/test.yaml', cfg_list=['VIS.VIS_TH', 0.7,
                                                                                     'VIS.SHOW_BOX.COLOR_SCHEME',
                                                                                     'instance'])
    # det = module(cfg_list=['MODULES.OBJDET.DETECTIONS_PER_IMG', 2, 'MODULES.OBJDET.GPU_ID', 1])

    while 1:
        if module_num_tmp != PRIVISION_MODEL_NUM:
            module_num_tmp = PRIVISION_MODEL_NUM
            # p.terminate()
            p.kill()
            print(module_num_tmp)
            if module_num_tmp == 0:
                p = sp.Popen(command_0, stdin=sp.PIPE, stdout=sp.PIPE)
                del det
                det = module(cfg_file='/home/user/Program/ls/PriVision/test.yaml', cfg_list=['VIS.VIS_TH', 0.7,
                                                                                'VIS.SHOW_BOX.COLOR_SCHEME',
                                                                                                 'instance'])
                # det = det_0
                print('*****')
                print('change mode 0')
                print('*****')
            if module_num_tmp == 1:
                p = sp.Popen(command_1, stdin=sp.PIPE, stdout=sp.PIPE)
                del det
                det = module(cfg_file='/home/user/Program/ls/PriVision/segmentation_0.yaml', cfg_list=['MODULES.OBJDET.DETECTIONS_PER_IMG', 2, 'MODULES.OBJDET.GPU_ID', 1])
                # det = det_1
                print('*****')
                print('change mode 1')
                print('*****')

        if not q.empty():
            # time.sleep(1)
            # print(det.gpu_id)
            # print(id(det))
            frame = q.get(True)
            frame = det(frame)
            # cv2.imwrite('{}.jpg'.format(det.gpu_id), frame)
            p.stdin.write(frame.tostring())


def get_img(q):
    camera_path = "rtsp://192.168.88.29:554/user=admin&password=admin&channel=1&stream=0.sdp?real_stream"
    cap = cv2.VideoCapture(camera_path)

    while (cap.isOpened()):
        ret, frame = cap.read()
        if q.empty():
            q.put(frame)


def get_jump_img(q):
    camera_path = "rtsp://192.168.88.29:554/user=admin&password=admin&channel=1&stream=0.sdp?real_stream"
    cap = cv2.VideoCapture(camera_path)
    num = 0
    while (cap.isOpened()):

        if num == 100000:
            num = 0

        ret, frame = cap.read()
        if num % 2 == 0:
            q.put(frame)
        num += 1


if __name__ == '__main__':

    q_1 = Queue()

    # pw_1 = Process(target=process_det_img, args=(q_1, 0))
    pw_1 = Process(target=det_rtmp_py, args=(q_1, 0))
    pr = Process(target=get_img, args=(q_1, ))

    pw_1.start()
    time.sleep(5)
    pr.start()

    pw_1.join()
    pr.join()
