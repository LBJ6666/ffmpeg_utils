# -*-coding: UTF-8 -*-
import json
from subprocess import PIPE

from ffmpy import FFprobe

'''
    # 提取视频信息的指令
    strCmd = 'ffprobe -v quiet -print_format json -show_format -show_streams -i "' + filename + '"'
       # 资料：https://blog.csdn.net/JosephThatwho/article/details/105116397
'''


def get_audio_type(video_path):
    """
    接受视频路径, 读取视频中的音频格式
    :param video_path: 视频路径
    :return: 音频格式
    """

    # 构建FFmpeg命令行
    ff = FFprobe(
        global_options='-of json -show_format -show_streams',  # 显示格式化命令
        inputs={video_path: None},
    )

    res = ff.run(stdout=PIPE, stderr=PIPE)
    video_stream = res[0]
    # print("视频信息：", json.loads(video_stream))

    # 第一个是视频格式：h264
    # 第二个音频格式：ac3,acc
    # 如果有字幕，后面会显示字幕如：subrip，ass
    video_detail = json.loads(video_stream).get('streams')[1]
    audio_type = video_detail.get("codec_name")
    # print('音频格式：', audio_type)
    return audio_type


def get_video_rate(video_path):
    """
    接受视频路径, 读取视频信息
    :param video_path: 视频路径
    :return: 视频帧率
    """
    # 构建FFmpeg命令行
    ff = FFprobe(
        global_options='-of json -show_streams -select_streams v',
        inputs={video_path: None},
    )

    # ffmpeg默认输出到终端, 但我们需要在进程中获取媒体文件的信息
    # 所以将命令行的输出重定向到管道, 传递给当前进程
    res = ff.run(stdout=PIPE, stderr=PIPE)
    video_stream = res[0]
    # 解析视频流信息
    video_detail = json.loads(video_stream).get('streams')[0]

    # 获取视频实际帧率, 计算取整
    frame_rate = round(eval(video_detail.get('r_frame_rate')))

    # 返回码率
    return frame_rate
