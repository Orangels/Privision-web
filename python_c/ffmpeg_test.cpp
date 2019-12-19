//
//  main.cpp
//  ffmpeg_test_xcode
//
//  Created by Orangels on 2019/10/21.
//  Copyright © 2019年 Orangels. All rights reserved.
//

#include <iostream>
#include <opencv2/highgui.hpp>
extern "C"
{
#include <libswscale/swscale.h>
#include <libavcodec/avcodec.h>
#include <libavformat/avformat.h>
}

int main(int argc, const char * argv[]) {
    // insert code here...
    std::cout << "avcodec_configuration:\n";
    std::cout <<avcodec_configuration();
    return 0;
}
