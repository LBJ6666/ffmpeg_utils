# -*-coding: UTF-8 -*-
import os
import fnmatch

import vedio_info

"""
视频分离音频
"""


# 获取全部文件
def get_dir_list(path, allfiles):
    """
    获取全部文件

    :param path: 文件的路径
    :param allfiles: 存放文件地址的列表
    :return: 返回所有的文件列表
    """
    filelists = os.listdir(path)
    for filename in filelists:
        filepath = os.path.join(path, filename)
        if os.path.isdir(filepath):
            get_dir_list(filepath, allfiles)
        elif fnmatch.fnmatch(filepath, '*.mp4'):  # 判断文件格式
            allfiles.append(filepath)
        elif fnmatch.fnmatch(filepath, '*.mkv', ):
            allfiles.append(filepath)
        elif fnmatch.fnmatch(filepath, '*.rmvb', ):
            allfiles.append(filepath)
        elif fnmatch.fnmatch(filepath, '*.avi', ):
            allfiles.append(filepath)

    return allfiles


# 分离视频中的音频和画面视频
def run_splitter(fileList, save_path):
    '''
    分离视频中的音频和画面视频

    :param fileList: 文件路径
    :param save_path:    输出保存的路径
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

    code_audio = 'ffmpeg -i {} -acodec copy -vn {}'  # 分离音频流（不处理视频）
    # code_video = 'ffmpeg -i {} -vcodec copy -an {}'  # 分离视频流（不处理音频）
    code_video = 'ffmpeg -i {} -vcodec copy -an -f mp4 {}'  # 输出为MP4格式（不处理音频）

    for filename in fileList:
        # 视频名称
        input_name = filename.split('.')[0].split('\\')[-1]
        # 后缀名称
        suffix_name = filename.split('.')[-1]

        # 源文件中的格式
        audio_type = vedio_info.get_audio_type(filename, 'audio')[0]
        vedio_type = vedio_info.get_audio_type(filename, 'video')[0]
        print('视频名称:', input_name, '\n后缀：', suffix_name, '\n音频格式：', audio_type, '\n视频格式：', vedio_type)

        # out_video_name = input_name + '_out.' + suffix_name  # 视频保存为原文件格式
        out_video_name = input_name + '_out.mp4'  # 视频保存为MP4格式
        out_audio_name = input_name + '_out.' + audio_type  # 音频保存为原来音频格式

        # 视频流的输路径
        out_video_path = os.path.join(save_path, out_video_name)
        out_audio_path = os.path.join(save_path, out_audio_name)

        # 提取视频的指令
        code_finish_video = code_video.format(filename, out_video_path)
        # 最终执行提取音频的指令
        code_finish_audio = code_audio.format(filename, out_audio_path)
        # 执行命令
        # os.system(code_finish_video)
        os.system(code_finish_audio)

    print('End #################')


# 转换视频的格式类型
def transform_video_type(fileList, save_path, out_format='mp4'):
    '''
    转换视频的格式类型

    :param fileList: 文件路径
    :param save_path: 输出保存的路径
    :param out_format: 输出的格式，默认为MP4
    '''

    for filename in fileList:
        # 原视频名称
        input_name = filename.split('.')[0].split('\\')[-1]
        out_video_name = input_name + '_out.' + out_format
        # 输出文件地址
        out_video_path = os.path.join(save_path, out_video_name)
        print('输出地址：', out_video_path)

        code_video = 'ffmpeg -i {} -vcodec copy -f  {} {}'  # 输出为指定格式
        code_finish_video = code_video.format(filename, out_format, out_video_path)
        os.system(code_finish_video)
    print('End #################')


# 截取视频里面的音频片段
def audio_clip(fileList, save_path, time_start=r'00:10:00', time_interval=r'00:10:00'):
    '''
    截取视频里面的音频片段

    :param fileList:    文件路径
    :param save_path:    输出保存的路径
    :param time_start:   那个时间段开始
    :param time_interval:  截取多长时间，这里是十分钟
    '''

    for filename in fileList:
        # 源文件中音频格式
        audio_type = vedio_info.get_audio_type(filename)[0]

        # 视频名称
        input_name = filename.split('.')[0].split('\\')[-1]
        # 输出文件路径
        out_audio_name = input_name + '_out.' + audio_type
        out_audio_path = os.path.join(save_path, out_audio_name)

        # # code = "ffmpeg -ss 00:00:00 -t 00:01:00 -i input.mp4 -c:a ac3 -strict experimental -b:a 98k output.ac3 -y"
        # -ss position 搜索到指定的时间 ,[-]hh:mm:ss[.xxx]的格式也支持
        # -t duration 设置纪录时间,hh:mm:ss[.xxx]格式的记录时间也支持
        # -c:a ：设置音频编码器
        code = "ffmpeg -ss {} -t {} -i {} -c:a {} -strict experimental -b:a 98k {} -y"
        code_finish = code.format(time_start, time_interval, filename, audio_type, out_audio_path)
        os.system(code_finish)

    print('End #################')


# 截图或GIF
def print_screen(file_list, save_path, time_start=r'00:10:00', img_width='1080', img_height='900', cut_gif=False,
                 gif_time='5'):
    '''
    截图或GIF

    :param file_list:  文件列表
    :param save_path:  保存的路径
    :param time_start:   截取的开始时间
    :param img_width:  图片的宽度
    :param img_height:  图片的高度
    :param cut_gif:  是否截取GIF图
    :param gif_time:  gif时长
    '''

    for file_name in file_list:
        print(file_name)
        # 视频名称
        input_name = file_name.split('.')[0].split('\\')[-1]
        # 输出文件路径
        if cut_gif:
            out_audio_name = input_name + '_out.gif'
        else:
            out_audio_name = input_name + '_out.jpg'
        out_audio_path = os.path.join(save_path, out_audio_name)

        # -s 设定画面的宽与高
        # code = ' ffmpeg -i input.mp4 -ss 00:10:00 -t 10 -s 320x240 -pix_fmt rgb24 output.gif'
        # code = 'ffmpeg –i input.mp4 -y -f image2 -ss 00:10:00 -t 0.001 -s 350x240 output.jpg'
        img_size = img_width + 'x' + img_height
        # 截取图片
        code = 'ffmpeg -i {} -y -f image2 -ss {} -t 0.001 -s {} {}'
        # 截取GIF图
        code_gif = 'ffmpeg -i {} -ss {} -t {} -s {} -pix_fmt rgb24 {}'
        if cut_gif:
            # 截取GIF
            code_finish = code_gif.format(file_name, time_start, gif_time, img_size, out_audio_path)
        else:
            # 截取图片
            code_finish = code.format(file_name, time_start, img_size, out_audio_path)

        os.system(code_finish)

    print('End #################')


if __name__ == '__main__':
    global fileDir  # 全局变量
    fileDir = os.getcwd()  # 获取源文件的遍历的文件夹
    global save_path
    save_path = os.getcwd() + r'\media'  # 输出文件夹,'r'是防止字符转义
    allfile = []

    get_dir_list(fileDir, allfile)  # 遍历文件夹

    run_splitter(allfile, save_path)
    # audio_clip(allfile,save_path)
