# -*-coding: UTF-8 -*-
import os
import fnmatch

import vedio_info

"""
视频分离音频
"""


# 获取全部文件
def dir_list(path, allfiles):
    """
    :param path: 文件的路径
    :param allfiles: 存放文件地址的列表
    :return: 返回所有的文件列表
    """
    filelists = os.listdir(path)
    for filename in filelists:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            dir_list(filepath, allfiles)
        elif fnmatch.fnmatch(filepath, '*.mp4'):  # 判断文件格式
            allfiles.append(filepath)
        elif fnmatch.fnmatch(filepath, '*.mkv', ):
            allfiles.append(filepath)

    return allfiles


def run_splitter(fileList):
    '''
    分离视频中的音频和画面视频
    :param fileList: 文件路径
    '''

    """
       ffmpeg的一些命令
       ffmpeg -i input.mp4 -vn -y -acodec copy output.aac
       ffmpeg -i input.mp4 -codec copy -bsf: h264_mp4toannexb -f h264 output.264
       ffmpeg -i input.mp4 -an -vcodec copy output.h264
       ffmpeg -i input.mkv -vcodec copy -an video.mp4 #提取MKV视频
       ffmpeg -i input.mkv -vn -acodec copy audio.ac3 #提取MKV音频
       ffmpeg -i input.mkv -vn -an -codec:s:0 srt subtitle.srt #提取MKV字幕
    """

    # 分离音频的执行命令前部分    {}{}分别为原始视频  与输出后保存的路径名
    # code_yin = 'ffmpeg -i {} -vn -y -acodec copy {}'
    # {}{}分别为原始视频  与输出后保存的文件路径名
    # code_video = 'ffmpeg -i {} -an -vcodec copy  {}'

    # MKV处理命令
    code_yin = 'ffmpeg -i {} -vn -acodec copy {}'
    code_video = 'ffmpeg -i {} -vcodec copy -an {}'

    for filename in fileList:
        # 视频名称
        input_name = filename.split('.')[0].split('\\')[-1]
        print(input_name)

        out_video_name = input_name + '_out.mp4'

        # 源文件中音频格式
        audio_type = vedio_info.get_audio_type(filename)[0]  # 音频输出格式需要和源文件内音频一致，不然会报错
        out_audio_name = input_name + '_out.' + audio_type

        # 视频流的输路径
        out_video_path = os.path.join(save_path, out_video_name)
        out_audio_path = os.path.join(save_path, out_audio_name)
        # print('输出：', out_audio_path)

        # 提取视频的指令
        code_finish_video = code_video.format(filename, out_video_path)
        # 最终执行提取音频的指令
        code_finish_audio = code_yin.format(filename, out_audio_path)

        os.system(code_finish_video)
        os.system(code_finish_audio)

    print('End #################')


def audio_clip(fileList, time_start=r'00:00:00', time_end=r'00:00:10'):
    '''
    截取视频里面的音频片段
    :param fileList:    文件路径
    :param time_start:   那个时间段开始
    :param time_end:  截取多长时间，这里是一分钟
    '''

    for filename in fileList:
        # 源文件中音频格式
        audio_type = vedio_info.get_audio_type(filename)[0]  # 音频输出格式需要和源文件内音频一致，不然会报错

        # 视频名称
        input_name = filename.split('.')[0].split('\\')[-1]
        # 输出文件路径
        out_audio_name = input_name + '_out.' + audio_type
        out_audio_path = os.path.join(save_path, out_audio_name)

        # # code = "ffmpeg -ss 00:00:00 -t 00:01:00 -i input.mp4 -c:a ac3 -strict experimental -b:a 98k output.ac3 -y"
        code = "ffmpeg -ss {} -t {} -i {} -c:a {} -strict experimental -b:a 98k {} -y"
        code_finish = code.format(time_start, time_end, filename, audio_type, out_audio_path)
        os.system(code_finish)

    print('End #################')


if __name__ == '__main__':
    global fileDir  # 全局变量
    fileDir = os.getcwd()  # 获取源文件的遍历的文件夹
    global save_path
    save_path = os.getcwd() + r'\media'  # 输出文件夹,'r'是防止字符转义
    allfile = []

    dir_list(fileDir, allfile)  # 遍历文件夹

    run_splitter(allfile)
    # audio_clip(allfile)
