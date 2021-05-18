# -*-coding: UTF-8 -*-

# 获取video的详细信息
import os

from vedio_info import get_audio_type, get_video_rate

file_path = os.getcwd() + r'\media\temp.mp4'

get_audio_type(file_path)
# get_video_rate(file_path)
