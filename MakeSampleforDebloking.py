'''
这个脚本用来将一个YUV序列按照一个码率编码，并将编码的视频解码后
以png格式都保存到./out/compressed路径;
还将编码输入的每一帧YUV转换为png格式保存到./out/src路径中。
可用于生成去block效应的训练样本。
示例：
python make.py --input ParkScene_1920x1080_24.yuv --output-dir br500 --br 500
依赖：
ffmpeg,x264
'''

import argparse
import os

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', type=str, required=True)
    parser.add_argument('--output-dir', type=str, required=True)
    #parser.add_argument('--crf', type=int, default=24)
    parser.add_argument('--br', type=int, required=True)

    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.mkdir(args.output_dir)

    cmd = 'x264 ' + '--bitrate ' + str(args.br) + ' ' + args.input + ' -o tmp.m4v'
    print(cmd)
    os.system(cmd)
    cmd = 'ffmpeg -i tmp.m4v decode.yuv' 
    print(cmd)
    os.system(cmd)

    input_yuv_dir = args.output_dir + '/src'
    if not os.path.exists(input_yuv_dir):
        os.mkdir(input_yuv_dir)
    
    compressed_yuv_dir = args.output_dir + '/compressed'
    if not os.path.exists(compressed_yuv_dir):
        os.mkdir(compressed_yuv_dir)
    
    cmd = 'ffmpeg -s ' + str(1920) + 'x' + str(1080) + ' -i ' + args.input + ' ' +input_yuv_dir + '/%03d.png'
    print(cmd)
    os.system(cmd)

    cmd = 'ffmpeg -s ' + str(1920) + 'x' + str(1080) + ' -i ' + 'decode.yuv ' + compressed_yuv_dir + '/%03d.png'
    print(cmd)
    os.system(cmd)
    os.remove('tmp.m4v')
    os.remove('decode.yuv')

