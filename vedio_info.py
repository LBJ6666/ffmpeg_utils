# -*-coding: UTF-8 -*-
import json
from subprocess import PIPE

from ffmpy import FFprobe

'''
获取视频信息
'''


def get_audio_type(video_path, out_type='audio'):
    """
    接受视频路径, 读取视频中的音频格式

    :param video_path: 视频路径
    :param out_type: audio:音频,video:视频,subtitle:字幕
    :return: 输出视频中的格式
    """
    print(video_path)
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

    # 一般第一个是视频格式：h264,rv40
    # MP4：h264; mkv：h264，hevc ; rmvb：rv40; avi：mpeg4
    # 后面的是音频格式：ac3,acc，pcm_s16le
    # MP4:ac3,acc; mkv:flac,ac3,ttf,otf; rmvb:ac3; mav:pcm_s16le;
    # 如果有字幕，后面会显示字幕如：subrip，ass，hdmv_pgs_subtitle
    media_videos = []
    media_audios = []
    media_subtitles = []
    for index, stream in enumerate(video_streams):
        # print('视频流信息:', stream)
        if stream.get('codec_type') == 'video':
            media_videos.append(stream.get('codec_name'))
        elif stream.get('codec_type') == 'audio':
            media_audios.append(stream.get('codec_name'))
        elif stream.get('codec_type') == 'subtitle':
            media_subtitles.append(stream.get('codec_name'))

    print('视频格式:', media_videos)
    print('音频格式:', media_audios)
    print('字幕格式:', media_subtitles)

    if out_type == 'video':
        return media_videos
    elif out_type == 'subtitle':
        return media_subtitles
    else:
        return media_audios


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
