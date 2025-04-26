import unittest

from mag_tools.utils.data.string_utils import StringUtils

class TestStringStringUtils(unittest.TestCase):

    def test_get_before_keyword(self):
        self.assertEqual(StringUtils.pick_head("hello world", "world"), "hello ")
        self.assertEqual(StringUtils.pick_head("hello world", " "), "hello")
        self.assertEqual(StringUtils.pick_head("hello world", "hello"), "")

    def test_get_after_keyword(self):
        self.assertEqual(StringUtils.pick_tail("hello world", "hello"), " world")
        self.assertIsNone(StringUtils.pick_tail("hello world", "world"))
        self.assertIsNone(StringUtils.pick_tail("hello world", "notfound"))

    def test_split_by_keyword(self):
        _input_strings = [
            "{打开工区}",
            "打开工区",
            "GridControl{T}",
            "打开工区(AAA)",
            "打开工区[AAA]BBB",
            "打开工区'AAA'BBB",
            '打开工区"AAA"BBB',
        ]

        _keywords = ['{}', '{}', '()', '[]', "''", '""']

        for _input_string, _keyword in zip(_input_strings, _keywords):
            _name, _function, _remainder = StringUtils.split_by_keyword(_input_string, _keyword)
            print(f"Input: {_input_string} -> Name: {_name}, Function: {_function}, Remainder: {_remainder}")

    def test_split_name_id(self):
        self.assertEqual(StringUtils.split_name_id("名称(标识)"), ("名称", "标识"))
        self.assertEqual(StringUtils.split_name_id("名称（标识）"), ("名称", "标识"))
        self.assertEqual(StringUtils.split_name_id("名称标识"), ("名称标识", None))

    def test_parse_function(self):
        self.assertEqual(StringUtils.parse_function("test(arg1, arg2)"), ("test", ["arg1", "arg2"]))
        self.assertEqual(StringUtils.parse_function("test()"), ("test", []))
        with self.assertRaises(ValueError):
            StringUtils.parse_function("test")

    def test_parse_strings_to_map(self):
        # 测试用例 1：使用空格作为分隔符
        strs = [
            "key1 value1",
            "key2 value2",
            "key3 value3"
        ]
        expected_output = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }
        result = StringUtils.parse_strings_to_map(strs)
        self.assertEqual(result, expected_output)

        # 测试用例 2：使用逗号作为分隔符
        strs = [
            "key1,value1",
            "key2,value2",
            "key3,value3"
        ]
        expected_output = {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }
        result = StringUtils.parse_strings_to_map(strs, delimiter=',')
        self.assertEqual(result, expected_output)

        # 测试用例 3：字符串中没有分隔符
        strs = [
            "key1 value1",
            "key2value2",  # 没有空格
            "key3 value3"
        ]
        with self.assertRaises(ValueError):
            StringUtils.parse_strings_to_map(strs)

        # 测试用例 4：字符串中有多个分隔符
        strs = [
            "key1 value1",
            "key2  value2",  # 多个空格
            "key3 value3"
        ]
        expected_output = {
            "key1": "value1",
            "key2": " value2",
            "key3": "value3"
        }
        result = StringUtils.parse_strings_to_map(strs)
        self.assertEqual(result, expected_output)

    def test_underline2hump(self):
        self.assertEqual(StringUtils.underline2hump('family_address'), 'familyAddress')
        self.assertEqual(StringUtils.underline2hump('my_variable_name'), 'myVariableName')
        self.assertEqual(StringUtils.underline2hump('test_case'), 'testCase')
        self.assertEqual(StringUtils.underline2hump('example_string'), 'exampleString')

    def test_hump2underline(self):
        self.assertEqual(StringUtils.hump2underline('familyAddress'), 'family_address')
        self.assertEqual(StringUtils.hump2underline('myVariableName'), 'my_variable_name')
        self.assertEqual(StringUtils.hump2underline('testCase'), 'test_case')
        self.assertEqual(StringUtils.hump2underline('exampleString'), 'example_string')

if __name__ == '__main__':
    unittest.main()
