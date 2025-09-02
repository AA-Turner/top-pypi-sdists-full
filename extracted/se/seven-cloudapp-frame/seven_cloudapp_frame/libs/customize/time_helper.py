# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2021-07-15 11:54:54
@LastEditTime: 2025-02-21 15:22:25
@LastEditors: HuangJianYi
:description: 时间帮助类
"""
from seven_framework import *
import datetime



class TimeExHelper:
    """
    :description: 时间帮助类
    """

    @classmethod
    def get_now_int(self, hours=0, minutes=0, fmt='%Y%m%d%H%M%S'):
        """
        :description: 获取整形的时间 格式为yyyyMMddHHmmss，如2009年12月27日9点10分10秒表示为20091227091010
        :param hours: 需要增加的小时数
        :param hours: 需要增加的分钟数
        :param fmt: 时间格式
        :return:
        :last_editors: HuangJianYi
        """
        now_date = (datetime.datetime.now() + datetime.timedelta(minutes=minutes, hours=hours))
        return int(now_date.strftime(fmt))

    @classmethod
    def get_now_hour_int(self, hours=0):
        """
        :description: 获取整形的小时2020050612
        :param hours: 需要增加的小时数
        :return: int（2020050612）
        :last_editors: HuangJianYi
        """
        return self.get_now_int(hours=hours, fmt='%Y%m%d%H')

    @classmethod
    def get_now_day_int(self, hours=0):
        """
        :description: 获取整形的天20200506
        :param hours: 需要增加的小时数
        :return: int（20200506）
        :last_editors: HuangJianYi
        """
        return self.get_now_int(hours=hours, fmt='%Y%m%d')

    @classmethod
    def get_now_month_int(self, hours=0):
        """
        :description: 获取整形的月202005
        :param hours: 需要增加的小时数
        :return: int（202005）
        :last_editors: HuangJianYi
        """
        return self.get_now_int(hours=hours,fmt='%Y%m')

    @classmethod
    def get_date_list(self, start_date, end_date):
        """
        :description: 两个日期之间的日期列表
        :param start_date：开始日期
        :param end_date：结束日期
        :return: list
        :last_editors: HuangJianYi
        """
        if not start_date or not end_date:
            return []
        if ":" not in start_date:
            start_date+=" 00:00:00"
        if ":" not in end_date:
            end_date += " 00:00:00"
        datestart = datetime.datetime.strptime(start_date, '%Y-%m-%d %H:%M:%S')
        dateend = datetime.datetime.strptime(end_date, '%Y-%m-%d %H:%M:%S')

        date_list = []

        while datestart < dateend:
            date_list.append(datestart.strftime('%Y-%m-%d'))
            datestart += datetime.timedelta(days=1)
        return date_list
    
    @classmethod
    def get_week_day_list(self, fmt='%Y%m%d'):
        """
        :description: 获取本周日期列表
        :param fmt: 时间格式
        :return list
        :last_editors: HuangJianYi
        """
        week_day_list = []
        now_datetime = TimeHelper.get_now_datetime()
        for i in range(7):
            cur_day = int((now_datetime + datetime.timedelta(days=i - now_datetime.weekday())).date().strftime(fmt))
            week_day_list.append(cur_day)
        return week_day_list

    @classmethod
    def convert_custom_date(self, dt):
        """
        :description: 转换自定义文本时间
        :param dt: datetime格式时间或时间字符串
        :return: str
        :last_editors: HuangJianYi
        """
        now_timestamp = TimeHelper.get_now_timestamp()
        difference_seconds = TimeHelper.difference_seconds(now_timestamp, dt)
        if difference_seconds <= 1:
            return "刚刚"
        elif difference_seconds < 60:
            return  str(difference_seconds) + "秒前"
        elif difference_seconds >= 60 and difference_seconds < 3600:
            return str(int(difference_seconds / 60)) + "分钟前"
        elif difference_seconds >= 3600 and difference_seconds < 24 * 3600:
            return str(int(difference_seconds / 3600)) + "小时前"
        else:
            return str(int(difference_seconds / (24 * 3600))) + "天前"

    @classmethod
    def convert_bj_to_rfc(self, time_str=None):
        """
        :description: 北京时间转换成RFC 3339时间格式
        :param time_str: datetime格式时间
        :return: RFC 3339时间格式字符串
        :last_editors: HuangJianYi
        """
        import pytz
        if not time_str:
            time_str = TimeHelper.get_now_datetime()
        # 设置所需时区（例如：东八区）
        target_timezone = pytz.timezone('Asia/Shanghai')
        # 转换为目标时区的时间
        target_time = time_str.astimezone(target_timezone)
        # 格式化为指定的时间格式
        formatted_time = target_time.strftime('%Y-%m-%dT%H:%M:%S.%f%z')
        return formatted_time
    
    @classmethod
    def convert_bj_to_utc(self, time_str, fmt='%Y-%m-%d %H:%M:%S'):
        """
        :description: 北京时间转UTC时间
        :param time_str: 北京时间字符串
        :param fmt: 时间格式
        :return: utc时间，比北京时间少8小时
        :last_editors: HuangJianYi
        """
        import pytz
        # 将字符串转换为datetime对象，并设置为北京时区
        beijing_tz = pytz.timezone('Asia/Shanghai')
        bj_dt = datetime.strptime(time_str, fmt)
        bj_dt = beijing_tz.localize(bj_dt)
        # 转换为UTC时间
        utc_dt = bj_dt.astimezone(pytz.utc)
        return utc_dt.strftime(fmt)
    
    @classmethod
    def convert_utc_to_bj(self, time_str, fmt='%Y-%m-%d %H:%M:%S'):
        """
        :description: UTC时间转北京时间
        :param time_str: utc时间字符串
        :param fmt: 时间格式
        :return:  北京时间
        :last_editors: HuangJianYi
        """
        import pytz
        # 将字符串转换为datetime对象，并设置为UTC时区
        utc_tz = pytz.UTC
        utc_dt = datetime.strptime(time_str, fmt)
        utc_dt = utc_tz.localize(utc_dt)
        # 转换为北京时间
        beijing_tz = pytz.timezone('Asia/Shanghai')
        bj_dt = utc_dt.astimezone(beijing_tz)
        return bj_dt.strftime(fmt)

    @classmethod
    def get_format_date(self, dt):
        """
        :description: 将时间字符串格式化为日期 + "00:00:00" 的格式
        :param dt: utc时间字符串
        :return:  格式化后的字符串，格式为 "YYYY-MM-DD 00:00:00"。
        :last_editors: HuangJianYi
        """
        try:
            if isinstance(dt, str):
                # 将输入字符串解析为 datetime 对象
                dt = datetime.datetime.strptime(dt, "%Y-%m-%d %H:%M:%S")
            # 将时间部分设置为 00:00:00
            dt = dt.replace(hour=0, minute=0, second=0)
            # 格式化为字符串
            format_time = dt.strftime("%Y-%m-%d %H:%M:%S")
            return format_time
        except ValueError as e:
            # 如果输入格式不正确，抛出异常
            raise ValueError(f"输入的时间字符串格式不正确")
    
