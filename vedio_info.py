# -*-coding: UTF-8 -*-
import json
from subprocess import PIPE

from ffmpy import FFprobe

'''
获取视频信息
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
    video_streams = json.loads(res[0]).get('streams')
    video_format = json.loads(res[0]).get('format')
    # print("视频流信息：", video_streams)
    # print("视频格式信息：", video_format)

    # 一般第一个是视频格式：h264
    # 后面的是音频格式：ac3,acc
    # 如果有字幕，后面会显示字幕如：subrip，ass
    video_audios = []
    for index, stream in enumerate(video_streams):
        print('视频流信息:', stream)
        if stream.get('codec_type') == 'video':
            continue
        video_audios.append(stream.get('codec_name'))

    print('音频格式:', video_audios)
    return video_audios


def get_video_rate(video_path):
    """
    传入视频路径, 读取视频信息
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

    video_streams = json.loads(res[0]).get('streams')
    frame_rate = ''
    for index, stream in enumerate(video_streams):
        # 解析视频流信息
        if stream.get('codec_type') == 'video':
            print('视频流信息:', stream)
            # 获取视频实际帧率, 计算取整
            frame_rate = round(eval(stream.get('r_frame_rate')))
            print('码率:', frame_rate)
            break

    # 返回码率
    return frame_rate
