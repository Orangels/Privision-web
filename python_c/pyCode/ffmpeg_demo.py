import subprocess as sp
import cv2
import time
import datetime
import sys
import os

video_path = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
video_path = os.path.join(video_path, 'video', 'ssd_vgg_yq-20190828.mp4')

print(video_path)

rtmpUrl = "rtmp://127.0.0.1:1935/rtmplive/room"
camera_path = "rtsp://192.168.88.29:554/user=admin&password=admin&channel=1&stream=0.sdp?real_stream"
# camera_path = video_path
cap = cv2.VideoCapture(camera_path)
# cap = cv2.VideoCapture(0)

# Get video information
fps = int(cap.get(cv2.CAP_PROP_FPS))
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))


# ffmpeg command
# command = ['ffmpeg',
#         '-y',
#         '-f', 'rawvideo',
#         '-vcodec','rawvideo',
#         '-pix_fmt', 'bgr24',
#         '-s', "{}x{}".format(width, height),
#         '-r', str(fps),
#         # '-r', str(15),
#         '-i', '-',
#         '-c:v', 'libx264',
#         '-pix_fmt', 'yuv420p',
#         '-preset', 'ultrafast',
#         '-f', 'flv',
#         rtmpUrl
#            ]


command = ['ffmpeg',
        '-y',
        '-f', 'rawvideo',
        '-vcodec','rawvideo',
        '-pix_fmt', 'bgr24',
        '-s', "{}x{}".format(width, height),
        '-r', str(fps),
        '-i', '-',
        '-c:v', 'libx264',
        '-pix_fmt', 'yuv420p',
        '-bf', '0',
        # '-g', '50',
        # '-b:v', "100k",
        # '-x264opts', "bframes=0",
        '-preset', 'ultrafast',
        # '-preset', 'superfast',
        # "-tune", "zerolatency",
        '-f', 'flv',
        rtmpUrl
           ]


print(' '.join(command))
# 管道配置
p = sp.Popen(command, stdin=sp.PIPE, stdout=sp.PIPE)
count = 0
last_frame = frame = 0
now = time.time()
# read webcamera
while(cap.isOpened()):
    last_frame = frame
    ret, frame = cap.read()
    # cv2.imwrite('./pic/{}.jpg'.format(count), frame)
    count += 1
    if not ret:
        cv2.imwrite('last_img.jpg', last_frame)
        print("Opening camera is failed")
        cap.release()
        # cap = cv2.VideoCapture(camera_path)
        # frame = last_frame
        break
    # cv2.imshow('test', frame)
    # cv2.waitKey(1)
    # process frame
    # your code
    # process frame
    # write to pipe
    p.stdin.write(frame.tostring())
    time.sleep(1/fps)
    # time.sleep(0.005)
    # print(time.time()-now)
    # now = time.time()

cap.release()
