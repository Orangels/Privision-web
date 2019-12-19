//
// Created by Orangels on 2019-10-24.
//

#ifndef FFMPEG_RTMP_RTMPHANDLER_H
#define FFMPEG_RTMP_RTMPHANDLER_H
#include <iostream>
#include <opencv2/highgui.hpp>

extern "C"
{
#include <libswscale/swscale.h>
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
#include <libavutil/time.h>
#include <libavutil/opt.h>
}
//#pragma comment(lib, "swscale.lib")
//#pragma comment(lib, "avcodec.lib")
//#pragma comment(lib, "avutil.lib")
//#pragma comment(lib, "avformat.lib")
//#pragma comment(lib,"opencv_world300.lib")
using namespace std;


class rtmpHandler {
    public :
        char * inUrl;
        char * outUrl;
        int inWidth;
        int inHeight;
        int fps;


        rtmpHandler();
        rtmpHandler(char * inUrl_parm, char * outUrl_parm, int width, int height, int fps_parm);
        void pushRTMP(cv::Mat frame);

    private:
        //像素格式转换上下文
        SwsContext *vsc = NULL;

        //输出的数据结构
        AVFrame *yuv = NULL;

        //编码器上下文
        AVCodecContext *vc = NULL;

        //rtmp flv 封装器
        AVFormatContext *ic = NULL;

        //编码器
        AVCodec *codec;
        //视频流
        AVStream *vs;
        AVPacket pack;
        int vpts = 0;

};


#endif //FFMPEG_RTMP_RTMPHANDLER_H
