from mag_tools.enums.justify_type import JustifyType

from mag_tools.format.string_format import StringFormat
import unittest


class TestStringFormat(unittest.TestCase):
    def test_pad_string(self):
        # 测试右对齐
        self.assertEqual(StringFormat.pad_string("12.123", 10), "    12.123")
        # 测试居中对齐
        self.assertEqual(StringFormat.pad_string("12.123", 10, JustifyType.CENTER), "  12.123  ")
        # 测试左对齐
        self.assertEqual(StringFormat.pad_string("12.123", 10, JustifyType.LEFT), "12.123    ")
        # 测试字符串长度大于目标长度
        self.assertEqual(StringFormat.pad_string("12.123"), "12.123")

    def test_pad_text(self):
        # 测试多个字符串右对齐
        strings = ["test1", "test2", "test3"]
        expected_output = "     test1      test2      test3"
        self.assertEqual(expected_output, StringFormat.pad_text(strings, 10)[0])
        # 测试多个字符串居中对齐
        expected_output = " test1    test2    test3  "
        self.assertEqual(expected_output, StringFormat.pad_text(strings, 8, JustifyType.CENTER)[0])
        # 测试多个字符串左对齐
        expected_output = "test1 test2 test3"
        self.assertEqual(expected_output, StringFormat.pad_text(strings, 5, JustifyType.LEFT)[0])
        # 测试pad_len不设置
        expected_output = "test1 test2"
        self.assertEqual(expected_output, StringFormat.pad_text(strings, None, JustifyType.LEFT, 2)[0])

    def test_format(self):
        print(StringFormat.format_function("{random_text(5)}"))
        print(StringFormat.format_function("{random_string(3)}"))
        print(StringFormat.format_function("{random_chinese(12)}"))
        print(StringFormat.format_function("{random_number(4)}"))
        print(StringFormat.format_function("{random_date(2024,%Y-%m-%d)}"))
        print(StringFormat.format_function("{today(%Y%m%d)}"))
        print(StringFormat.format_function("{current(%Y-%m-%d %H:%M:%S)}"))
        print(StringFormat.format_function("{random_int(20, 30)}"))


if __name__ == '__main__':
    unittest.main()
