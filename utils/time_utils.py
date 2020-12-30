# -*-coding: UTF-8 -*-
import datetime
import time


class TimeUtils(object):
    '''
    查看运行时间工具类
    '''

    def __init__(self):
        self.start_time = None
        self.end_time = None

    def time_start(self):
        # 记录一下开始训练的时间----------------------------------
        self.start_time = time.time()
        # 格式化成2016-03-20 11:45:39形式
        print("开始时间：", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))

    def time_stop(self):
        # 记录结束时间--------------------------------------------
        self.end_time = time.time()
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        # 计算出训练了多久
        run_tiem = (datetime.datetime.fromtimestamp(self.end_time) -
                    datetime.datetime.fromtimestamp(self.start_time)).seconds
        print("经过了：", str(datetime.timedelta(seconds=run_tiem)))
