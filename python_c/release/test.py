import ctypes
so = ctypes.cdll.LoadLibrary
lib = so("./libpython_c.so")
path = bytes('/home/user/Program/ffmpeg_demo/python_c/release/Kobe_1920_1080.jpg', 'utf8')
a = lib.rtmp(path)
print(a)
