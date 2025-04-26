import unittest

from mag_tools.utils.data.value_utils import ValueUtils


class TestValueUtils(unittest.TestCase):
    def test_to_value(self):
        print(ValueUtils.to_value('12.50', float))

        # 测试整数转换
        self.assertEqual(ValueUtils.to_value("123", int), 123)
        # 测试浮点数转换
        self.assertEqual(ValueUtils.to_value("123.45", float), 123.45)
        self.assertEqual(ValueUtils.to_value("1.12000E+03", float), 1120)
        # 测试布尔值转换
        self.assertTrue(ValueUtils.to_value("true", bool))
        self.assertFalse(ValueUtils.to_value("false", bool))
        # 测试列表转换
        self.assertEqual(ValueUtils.to_value("[1, 2, 3]", list), [1, 2, 3])
        # 测试字典转换
        self.assertEqual(ValueUtils.to_value("{'key': 'value'}", dict), {'key': 'value'})
        # 测试默认类型转换
        self.assertEqual(ValueUtils.to_value("text"), "text")

    def test_to_values(self):
        str_ = '1.00000E+01 3.00000E+02 7.00000E+02 1.00000E+03 2.00000E+03'
        print(ValueUtils.to_values(str_, float))

        str_ = '1 1 1 1 1.93199E+03 1.36585E+03 6.77031E+02 7.15261E+02 8.62436E+02'
        print(ValueUtils.to_values(str_, float))

        str_ = '12, 23,123,321,12'
        print(ValueUtils.to_values(str_, int, ','))

    def test_number_to_scientific(self):
        print(ValueUtils.to_scientific(123.50, 3, 2))

        # 测试0
        self.assertEqual("0", ValueUtils.to_scientific(0, 5, 2))
        self.assertEqual("0.000", ValueUtils.to_scientific(0.0, 5,3))

        # 测试默认小数位数
        self.assertEqual("1.000E+9", ValueUtils.to_scientific(1000000000.0, decimal_places=5, decimal_places_of_zero=3))
        self.assertEqual("1.230000E-4", ValueUtils.to_scientific(0.000123))

        # 测试指定小数位数
        self.assertEqual("1.00E+9", ValueUtils.to_scientific(1000000000.0, 5, 2))
        self.assertEqual("1.230E-4", ValueUtils.to_scientific(0.000123, 3))

        # 测试负数
        self.assertEqual("-1.0E+9", ValueUtils.to_scientific(-1000000000.0))
        self.assertEqual("-1.230000E-4", ValueUtils.to_scientific(-0.000123))

        # 测试小数位数不足时补零
        self.assertEqual("1.23000E+0", ValueUtils.to_scientific(1.23, 5))
        self.assertEqual("1.00000E+0", ValueUtils.to_scientific(1.0, 5, 5))

    def test_to_string(self):
        print(ValueUtils.to_string(None, 6, 3, False, 'NA'))
        print(ValueUtils.to_string(125000, 6, 3))

        # 测试浮点数格式化
        self.assertEqual(ValueUtils.to_string(123.456, 2), "123.46")
        self.assertEqual("9110", ValueUtils.to_string(9110.0, 5, 0))
        # 测试科学计数法格式化
        self.assertEqual("1.230000E+3", ValueUtils.to_string(1.23e3, 6, 1,True))
        # 测试整数格式化
        self.assertEqual(ValueUtils.to_string(123), "123")

    def test_to_chinese_number(self):
        self.assertEqual(ValueUtils.to_chinese_number(0), "零")
        self.assertEqual(ValueUtils.to_chinese_number(10), "十")
        self.assertEqual(ValueUtils.to_chinese_number(110), "一百一十")
        self.assertEqual(ValueUtils.to_chinese_number(1234), "一千二百三十四")
        self.assertEqual(ValueUtils.to_chinese_number(10001), "一万零一")