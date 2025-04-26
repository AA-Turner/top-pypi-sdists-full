import re

class NumberValidator:
    """
    数据格式检测类。

    @description: 提供数据格式检查。
    @version: v1.3
    @date: 2016/7/10
    """
    @staticmethod
    def is_scientific_number(string: str) -> bool:
        """
        判定一个字符串是否为科学记数法

        :param string: 科学记数法表示的字符串
        :return: 是否为科学记数法
        """
        if not string:
            return False
        # 正则表达式匹配科学记数法
        regex = r"^[+-]?\d+(\.\d*)?([Ee][+-]?\d+)?$"
        return bool(re.match(regex, string))

    @staticmethod
    def is_numeric(string: str) -> bool:
        """
        判定一个字符串是否为数值（包括浮点数和整数）

        :param string: 数值字符串
        :return: 是否为数值
        """
        try:
            if string and len(string) > 0:
                float(string)
                return True
        except ValueError:
            pass
        return False
