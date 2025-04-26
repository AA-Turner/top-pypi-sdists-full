import re
from datetime import date, datetime, time, timedelta
from typing import  Optional, Union

from dateutil import parser

from mag_tools.utils.data.value_utils import ValueUtils


class DateUtils:
    @staticmethod
    def to_string(dt: Union[datetime, date, time], pattern: str) -> str:
        return dt.strftime(pattern) if dt is not None else None

    """
    日期时间的工具类
    """
    @staticmethod
    def float_to_datetime(timestamp: float) -> datetime:
        """
        将浮点数转换为日期时间对象

        :param timestamp: 浮点数，表示自 Unix 纪元以来的秒数
        :return: 日期时间对象
        """
        return datetime(1970, 1, 1) + timedelta(seconds=timestamp)

    @staticmethod
    def to_datetime(date_time_str: str) -> Optional[datetime]:
        date_time_formats = [
            "%Y-%m-%d %H:%M:%S",
            "%Y/%m/%d %H:%M:%S",
            "%Y.%m.%d %H:%M:%S",
            "%Y年%m月%d日 %H时%M分%S秒",
            "%Y年%m月%d日%H时%M分%S秒",
            "%Y-%m-%d",
            "%Y/%m/%d",
            "%Y.%m.%d",
            "%H:%M:%S",
            "%Y年%m月%d日",
            "%H时%M分%S秒",
            "%Y-%m-%d %H:%M",
            "%Y-%m-%d %H:%M:%S.%f",
            "%Y%m%d%H%M%S",
            "%Y%m%d%H%M%S%f",
            "%Y%m%d",
            "%a, %d %b %Y %H:%M:%S %Z",
            "%a %b %d %H:%M:%S %Z %Y",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S.%fZ",
            "%Y-%m-%dT%H:%M:%S%z",
            "%Y-%m-%dT%H:%M:%S.%f%z"
        ]

        for fmt in date_time_formats:
            try:
                return datetime.strptime(date_time_str, fmt)
            except ValueError:
                continue

        try:
            return parser.parse(date_time_str)
        except ValueError:
            return None

    @staticmethod
    def pick_datetimes(text: str) -> list[Union[datetime, date, time]]:
        """
        从字符串中提取日期、时间和日期时间。

        参数：
        :param text: 包含日期或时间的字符串
        :return: 包含日期、时间和日期时间的字典
        """
        datetime_pattern = r'(?:\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}(?:[日T\s])?)?(?:\d{1,2}[:时]\d{1,2}[:分]?(?:\d{1,2}(?:[秒])?)?)?'

        # 转换为对象
        results = []
        # 匹配日期时间
        for match in re.finditer(datetime_pattern, text):
            full_match = match.group(0)  # 获取完整匹配项
            dt = DateUtils.to_datetime(full_match)
            if dt is not None:
                if DateUtils.datetime_type(full_match) == datetime:
                    results.append(dt)
                elif DateUtils.datetime_type(full_match) == date:
                    results.append(dt.date())
                elif DateUtils.datetime_type(full_match) == time:
                    results.append(dt.time())
        return results

    @staticmethod
    def pick_datetime(text: str) -> Optional[datetime]:
        results = DateUtils.pick_datetimes(text)
        if not results:
            time_value = ValueUtils.to_value(text, float)
            if time_value is not None:
                return DateUtils.float_to_datetime(time_value)
        else:
            return results[0] if len(results) > 0 else None

    @staticmethod
    def datetime_type(text: str) -> Optional[type]:
        """
        从字符串中提取日期、时间和日期时间。

        参数：
        :param text: 包含日期或时间的字符串
        :return: 包含日期、时间和日期时间的字典
        """
        datetime_pattern = r'\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}(?:[日T\s])?[\s]?\d{1,2}[:时]\d{1,2}[:分](?:\d{1,2}[秒]?)?'
        date_pattern =     r'\d{4}[-/.年]\d{1,2}[-/.月]\d{1,2}(?:[日T\s])?'
        time_pattern = r'\d{1,2}[:时]\d{1,2}[:分]?(?:\d{1,2}(?:[秒])?)?'

        if re.match(datetime_pattern, text):
            return datetime
            # 判断日期
        elif re.match(date_pattern, text):
            return date
            # 判断时间
        elif re.match(time_pattern, text):
            return time
        else:
            return None