# -*-coding: UTF-8 -*-

# 获取video的详细信息
import os

from vedio_info import get_audio_type, get_video_rate
from vedio_splitter import get_dir_list, run_splitter, transform_video_type, audio_clip, print_screen

file_path = os.getcwd() + r'\media\temp.mp4'
dir_path = os.getcwd() + r'\media'



file_list = [file_path]

get_audio_type(file_path)
# get_video_rate(file_path)
# all_path_list = get_dir_list(dir_path, [])
# print(all_path_list)

# run_splitter(file_list, dir_path + r'\out')
# transform_video_type(file_list, dir_path + r'\out')
# audio_clip(file_list, dir_path + r'\out',time_interval=r'00:2:00')
# print_screen(file_list, dir_path + r'\out', cut_gif=True)
