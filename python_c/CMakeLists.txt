cmake_minimum_required(VERSION 3.9.4)
project(python_c)

set(CMAKE_CXX_STANDARD 11)
include_directories(/usr/local/include /usr/include
#        ${OpenCV_INCLUDE_DIRS}
        /home/user/Program/ffmpeg_demo/ffmpeg_rtmp_demo/include
        /usr/include/python3.6m
		)

find_package(OpenCV REQUIRED)
find_package(pybind11 REQUIRED)

#add_subdirectory(pybind11)

#add_executable(python_c main.cpp)
add_library(python_c SHARED test.cpp rtmpHandler.cpp rtmpHandler.h)
#pybind11_add_module(python_c py_c_11.cpp)

target_link_libraries(python_c
#		PRIVATE
        /usr/local/lib/libopencv_core.so.3.4
        /usr/local/lib/libopencv_highgui.so.3.4
        /usr/local/lib/libopencv_imgproc.so.3.4
        /usr/local/lib/libopencv_imgcodecs.so.3.4
        /usr/local/lib/libopencv_video.so.3.4
        /usr/local/lib/libopencv_shape.so.3.4
        /usr/local/lib/libopencv_features2d.so
#        ${OpenCV_LIBS}
        /usr/local/ffmpeg/lib/libavcodec.so
        /usr/local/ffmpeg/lib/libavdevice.so
        /usr/local/ffmpeg/lib/libavfilter.so
        /usr/local/ffmpeg/lib/libavformat.so
        /usr/local/ffmpeg/lib/libavutil.so
        /usr/local/ffmpeg/lib/libpostproc.so
        /usr/local/ffmpeg/lib/libswresample.so
        /usr/local/ffmpeg/lib/libswscale.so
        )
