
import re
from typing import   Optional

import unicodedata


class StringUtils:
    """
    字符串处理工具类
    """
    @staticmethod
    def pick_head(s: str, keyword: str) -> Optional[str]:
        return s.split(keyword)[0] if s else None

    @staticmethod
    def pick_tail(s: str, keyword: str) -> Optional[str]:
        if s is None or keyword not in s:
            return None

        return s.split(keyword, 1)[1]

    @staticmethod
    def split_by_keyword(input_string: str, keyword: str = '{}'):
        result = None, None, None
        if input_string:
            first, end = keyword[0], keyword[1]
            if first not in input_string or end not in input_string:
                return input_string, None, None
            else:
                pattern = rf'^(.*?)(\{first}(.*?)\{end})(.*)$'
                match = re.match(pattern, input_string)
                if match:
                    result1 = match.group(1) if match.group(1) else None # 第一个捕获组
                    result2 = match.group(3) if match.group(3) else None  # 第三个捕获组
                    result3 = match.group(4) if match.group(4) else None  # 第四个捕获组
                    result = result1, result2, result3
                else:
                    raise ValueError("输入字符串格式不正确")
        return result

    @staticmethod
    def split_name_id(text: str) -> {str, str}:
        """
        将 名称(标识)字符串分为{名称, 标识}
        :param text: 名称(标识)字符串
        :return: {名称, 标识}
        """
        match = re.match(r"(.+)[(（](.+)[)）]", text)
        if match:
            _name = match.group(1)
            _id = match.group(2)
            return _name, _id
        else:
            return text, None

    @staticmethod
    def parse_function(function_name: str) -> tuple:
        """
        解析字符串，将其分解为方法名和参数
        :param function_name: 字符串，格式如：test(arg1, arg2)
        :return: 方法名和参数列表
        """
        pattern = r'(\w+)\((.*)\)'
        match = re.match(pattern, function_name)

        if not match:
            raise ValueError("字符串格式不正确")

        method_name = match.group(1)
        args = match.group(2).split(',') if match.group(2) else []

        # 去除参数两端的空格
        args = [arg.strip() for arg in args]

        return method_name, args



    @staticmethod
    def parse_strings_to_map(strs: list[str], delimiter: str = ' ') -> dict[str, str]:
        """
        将字符串数组解析为字典。

        参数：
        :param strs: 字符串数组
        :param delimiter: 分隔符，默认为空格
        :return: 字典
        """
        data_map = {}
        for _str in strs:
            if delimiter in _str:
                key, value = _str.split(delimiter, maxsplit=1)
                data_map[key] = value
            else:
                raise ValueError(f"字符串 '{_str}' 中没有分隔符 '{delimiter}'，无法解析为键值对")
        return data_map

    @staticmethod
    def get_print_width(s: str, chines_width: float = 1.67) -> int:
        width = 0
        for char in s:
            if unicodedata.east_asian_width(char) in ('F', 'W'):
                width += chines_width
            else:
                width += 1
        return int(width)

    @staticmethod
    def remove_between_keywords(text: str, keyword_begin: str, keyword_end: str) -> str:
        # 使用正则表达式去除keyword_begin和keyword_end之间的内容，包括这两个关键词
        pattern = re.escape(keyword_begin) + '.*?' + re.escape(keyword_end)
        return re.sub(pattern, '', text, flags=re.DOTALL)



    @staticmethod
    def underline2hump(string: str) -> str:
        """
        将用"_"拼接的字符串转换为驼峰格式，首字母小写。

        :param string: String 参数
        """
        # 首字母小写
        string = StringUtils.lower_first_letter(string)
        return re.sub(r'_([a-z])', lambda x: x.group(1).upper(), string)

    @staticmethod
    def hump2underline(s: str) -> str:
        """
        将驼峰格式参数变换为"_"连接的格式。
        """
        s = StringUtils.lower_first_letter(s)
        hump_pattern = re.compile(r'([A-Z])')
        return hump_pattern.sub(r'_\1', s).lower()

    @staticmethod
    def lower_first_letter(string: str) -> str:
        """
        将字符串的首字母转换为小写

        :param string: 输入字符串
        :return: 首字母小写的字符串
        """
        return string[0].lower() + string[1:] if string else ""

    @staticmethod
    def upper_first_letter(string: str) -> str:
        """
        将字符串的首字母转换为小写

        :param string: 输入字符串
        :return: 首字母小写的字符串
        """
        return string[0].upper() + string[1:] if string else ""

    @staticmethod
    def last_word(s: str) -> str:
        """
        获取字段串末尾的关键词，空格分隔

        :param s: 原字符串
        :return: 末尾的关键词
        """
        tokens = s.split()
        return tokens[-1] if tokens else ""