import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_DIR = os.path.join(BASE_DIR, 'video', 'ssd_vgg_yq-20190828.mp4')
print(BASE_DIR)
