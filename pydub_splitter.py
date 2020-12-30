# -*-coding: UTF-8 -*-
import os
from glob import glob
from pydub import AudioSegment
from utils.time_utils import TimeUtils

"""
使用pydub截取片段
缺点：无法处理超过4G文件，速度慢
"""

time_utils = TimeUtils()
time_utils.time_start()

playlist_songs = [AudioSegment.from_mp3(mp3_file) for mp3_file in glob(os.getcwd() + r"/media/*.mp3")]

for song in playlist_songs:
    # 截取歌曲的前30秒 (切片以毫秒为单位)
    beginning_of_song = song[:30 * 1000]
    playlist = beginning_of_song
    # 结尾淡出效果
    playlist = playlist.fade_out(3000)

    # 计算时长( len(audio_segment)返回值同样是以毫秒计的 ）
    playlist_length = len(playlist) / (1000 * 60)

    # 现在保存下来!
    out_f = open("%s_minute.mp3" % playlist_length, 'wb')

    playlist.export(out_f, format='mp3')

# 记录结束时间--------------------------------------------
time_utils.time_stop()
