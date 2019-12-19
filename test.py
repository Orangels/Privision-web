import sys
import time
import cv2
sys.path.append('/home/user/workspace/Pet-engine')
from modules import pet_engine


if __name__ == '__main__':
    print(pet_engine.MODULES.keys())
    module = pet_engine.MODULES['ObjectDet']
    # det = module(cfg_list=['MODULES.OBJDET.DETECTIONS_PER_IMG', 2])
    det = module(cfg_file='/home/user/workspace/privision_test/test.yaml', cfg_list=['VIS.VIS_TH', 0.7,
    'VIS.SHOW_BOX.COLOR_SCHEME', 'instance'])
    # det = module()

    camera_path = "rtsp://192.168.88.29:554/user=admin&password=admin&channel=1&stream=0.sdp?real_stream"
    # camera_path = '/home/user/Program/ffmpeg_demo/video/ssd_vgg_yq-20190828.mp4'
    cap = cv2.VideoCapture(camera_path)
    last_frame = frame = 0
    num = 0
    while (cap.isOpened()):
        ret, frame = cap.read()
        start = time.time()
        img_vis = det(frame)
        print('total time -- {}'.format(time.time()-start))
        print('***********')
    # img = cv2.imread('2.jpg')
    # img_vis = det(img)
    # cv2.imwrite('222.jpg', img_vis)
