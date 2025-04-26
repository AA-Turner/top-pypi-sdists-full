import unittest
from datetime import datetime, date, time
from dateutil.tz import tzoffset

from mag_tools.utils.data.date_utils import DateUtils


class TestDateUtils(unittest.TestCase):
    def test_float_to_datetime(self):
        # 测试 Unix 时间戳转换
        self.assertEqual(
            DateUtils.float_to_datetime(0),
            datetime(1970, 1, 1)
        )
        self.assertEqual(
            DateUtils.float_to_datetime(86400),
            datetime(1970, 1, 2)
        )

    def test_to_datetime(self):
        # 测试不同格式的日期时间解析
        self.assertEqual(
            DateUtils.to_datetime("2025-03-10 14:30:00"),
            datetime(2025, 3, 10, 14, 30)
        )
        self.assertEqual(
            DateUtils.to_datetime("2025/03/10"),
            datetime(2025, 3, 10)
        )
        self.assertEqual(
            DateUtils.to_datetime("2025-03-10T14:30:00+0800"),
            datetime(2025, 3, 10, 14, 30, tzinfo=tzoffset(None, 28800))
        )
        self.assertIsNone(
            DateUtils.to_datetime("invalid format")
        )

    def test_pick_datetime(self):
        # 测试从文本中提取日期、时间和日期时间
        text = "会议时间是2025-03-10 16:30:45，截止日期是2025/03/15，#2025-05-05 05:05:05提醒设置在15:45。"
        expected_results = [
            datetime(2025, 3, 10, 16, 30, 45),
            date(2025, 3, 15),
            datetime(2025, 5, 5, 5, 5, 5),
            time(15, 45),
        ]
        self.assertEqual(DateUtils.pick_datetimes(text), expected_results)

        text = "这是一个空字符串，没有日期或时间。"
        self.assertEqual(DateUtils.pick_datetimes(text), [])

    def test_datetime_type(self):
        str_1 = '2025-03-10 16:30:45'
        str_2 = '2025-03-10'
        str_3 = '16:30:45'
        str_4 = '2025/3/10 16:30:45'
        str_5 = '2025/03/10'
        str_6 = '16:30'
        str_7 = '2025年03月10日 16时30分45秒'
        str_8 = '2025年03月10日'
        str_9 = '16时30分45秒'

        self.assertEqual(DateUtils.datetime_type(str_1), datetime)
        self.assertEqual(DateUtils.datetime_type(str_2), date)
        self.assertEqual(DateUtils.datetime_type(str_3), time)
        self.assertEqual(DateUtils.datetime_type(str_4), datetime)
        self.assertEqual(DateUtils.datetime_type(str_5), date)
        self.assertEqual(DateUtils.datetime_type(str_6), time)
        self.assertEqual(DateUtils.datetime_type(str_7), datetime)
        self.assertEqual(DateUtils.datetime_type(str_8), date)
        self.assertEqual(DateUtils.datetime_type(str_9), time)

if __name__ == "__main__":
    unittest.main()
