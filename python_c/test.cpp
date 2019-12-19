#include <iostream>
#include "rtmpHandler.h"
#include <opencv2/highgui.hpp>

using namespace std;
using namespace cv;

class TestLib
{
public:
    void display();
    void display(int a);
};
void TestLib::display() {
    cout<<"First display"<<endl;
}

void TestLib::display(int a) {
    cout<<"Second display:"<<a<<endl;
}

static double scale(Mat m){
    int min_side = min(m.rows, m.cols);
//    if (min_side <= 256) {
//        return 1;
//    }
    double scal;
    scal = 256.0/min_side ;
    return scal;
}

extern "C" {
TestLib obj;
int num = 0;
void display() {
    obj.display();
    cout << "num " << num << endl;
    num++;
}
void display_int() {
    obj.display(2);
    cout << "num " << num << endl;
    num++;
}

//rtmpHandler ls_handler("","rtmp://192.168.88.91:1935/rtmplive/room",1920,1080,18);
rtmpHandler ls_handler ;

int initRtmp(char * outUrl_parm, int width, int height, int fps_parm){
    ls_handler = rtmpHandler("", outUrl_parm, width, height, fps_parm);
}

int rtmp(char * path){
//    cout << path << endl;
    Mat frame = imread(path, CV_LOAD_IMAGE_COLOR);
    ls_handler.pushRTMP(frame);
    return 1;
}

}
