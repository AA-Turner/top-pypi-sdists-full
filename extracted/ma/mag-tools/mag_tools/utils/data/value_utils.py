import re
from datetime import date, datetime, time
from typing import Any,  Optional, Union

import numpy as np


class ValueUtils:
    @staticmethod
    def to_value(text: str, data_type: Optional[type] = None) -> Optional[Any]:
        """
        将文本转换为数值
        :param text: 文本
        :param data_type: 数据类型
        """
        if text is None or not isinstance(text, str):
            return None

        text = text.strip()
        if data_type == int:
            try:
                return int(text)
            except ValueError:
                return None
        elif data_type == float:
            try:
                if text.endswith('%'):
                    return float(text[:-1]) / 100

                return float(text)
            except ValueError:
                return None
        elif data_type == bool:
            text = text.lower()
            return text in ['true', 'yes', 't', 'y', '1']
        elif data_type == list:
            return eval(text)
        elif data_type == dict:
            return eval(text)
        else:
            return text

    @staticmethod
    def to_values(text: str, data_type: Optional[type] = None, sep: str = ' ') -> list[Any]:
        if text is None or not isinstance(text, str):
            return []

        text = text.strip()
        items = text.split(sep)
        return [ValueUtils.to_value(item, data_type) for item in items]

    @staticmethod
    def to_string(value: Optional[Union[int, float, bool, str, datetime, date, time]],
                  decimal_places: int=6,
                  decimal_places_of_zero: int=1,
                  scientific: bool = False,
                  none_default: str = None) -> str:
        """
        将给定的值转换为字符串表示
        :param value: 要转换的值，支持 int, float, bool, 和 str 类型
        :param decimal_places: 指定浮点数保留的最大小数位数，默认为 6
        :param decimal_places_of_zero: 当浮点数的值为整数或接近整数时，最少保留的小数位数，默认为 1
        :param scientific: 是否强制使用科学记数法格式，默认为 False
        :param none_default: 当数据(int或float)为None时对应的缺省字符串
        :return: 转换为字符串的值，格式根据参数动态调整
        详细说明:
        1. 整数、布尔值、字符串类型: 直接转换为字符串。

        2. 根据数值范围决定是否使用科学记数法:
            - 如果值的绝对值大于等于 1e8 或 (不为零并且绝对值小于 1e-3)，默认使用科学记数法。
            - 整数类型始终不使用科学记数法，除非显式指定使用科学计数法

        3. 浮点数的常规格式:
            - 如果浮点数为整数（即小数部分全为零），按 `decimal_places_of_zero` 指定的小数位数格式化。
            - 如果浮点数有小数部分，则按 `decimal_places` 指定的小数位数格式化。
            - 格式化后的小数部分会移除多余的零，但确保至少保留 `decimal_places_of_zero` 个小数位。
        """
        if value is None:
            return none_default

        if isinstance(value, str) or isinstance(value, bool):
            return str(value)
        elif isinstance(value, datetime):
            return value.strftime('%Y-%m-%d %H:%M:%S') if value is not None else None
        elif isinstance(value, date):
            return value.strftime('%Y-%m-%d') if value is not None else None
        elif isinstance(value, time):
            return value.strftime('%H:%M:%S') if value is not None else None
        else:
            if abs(value) >= 1e8 or (value != 0 and abs(value) < 1e-3):
                scientific = True
            elif isinstance(value, int):
                scientific = False

            if scientific:
                return ValueUtils.to_scientific(value, decimal_places, decimal_places_of_zero)

            if isinstance(value, float):
                if value.is_integer():
                    return f"{value:.{decimal_places_of_zero}f}"
                else:
                    formatted_value = f"{value:.{decimal_places}f}"
                    # 确保小数位末尾的零的个数符合要求
                    if '.' in formatted_value:
                        integer_part, decimal_part = formatted_value.split('.')
                        decimal_part = decimal_part.rstrip('0')
                        if len(decimal_part) < decimal_places_of_zero:
                            decimal_part += '0' * (decimal_places_of_zero - len(decimal_part))
                        formatted_value = f"{integer_part}.{decimal_part}"
                    return formatted_value
            elif isinstance(value, bool):
                return str(value)
            elif isinstance(value, int):
                return f"{round(value)}"

    @staticmethod
    def to_native(value: Any) -> Any:
        """
        将值转换为原生类型，如果可能
        :param value: 原始值
        :return: 转换后的原生类型值
        """
        if isinstance(value, (np.integer, int)):
            return int(value)  # 转换为 Python 的 int 类型
        elif isinstance(value, (np.floating, float)):
            return float(value)  # 转换为 Python 的 float 类型
        elif isinstance(value, (np.bool_, bool)):
            return bool(value)  # 转换为 Python 的 bool 类型
        else:
            return str(value)  # 保留为字符串

    @staticmethod
    def to_scientific(value: Union[int,float], decimal_places: int = 6, decimal_places_of_zero: int = 1) -> str:
        """
        将 float 数字转换为科学计数法表示的字符串。

        参数：
        :param value: float 数字
        :param decimal_places: 小数位数，默认为 6
        :param decimal_places_of_zero: 小数部分0的个数
        :return: 科学计数法表示的字符串
        """
        if not isinstance(value, (int, float)):
            raise TypeError("value 参数必须是 int 或 float 类型。")
        if not isinstance(decimal_places, int) or decimal_places < 0:
            raise ValueError("decimal_places 必须是一个非负整数。")
        if not isinstance(decimal_places_of_zero, int) or decimal_places_of_zero < 0:
            raise ValueError("参数 decimal_places_of_zero 必须是一个非负整数。")

        if value == 0:
            return '0' if isinstance(value, int) else f"0.{'0' * decimal_places_of_zero}"
        elif value == float('inf'):
            return 'inf'

        exponent = int(f"{value:e}".split('e')[1])  # 指数部分
        coefficient = value / (10 ** exponent)      # 系数部分

        if coefficient == int(coefficient):
            formatted_coefficient = f"{int(coefficient)}.{'0' * decimal_places_of_zero}" if decimal_places_of_zero > 0 else f"{int(coefficient)}"
        else:
            formatted_coefficient = f"{coefficient:.{decimal_places}f}"

        return f"{formatted_coefficient}E{'+' if exponent >= 0 else ''}{exponent}"

    @staticmethod
    def to_chinese_number(num: int) -> str:
        units = ["", "十", "百", "千", "万", "十", "百", "千", "亿"]
        digits = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九"]

        if num == 0:
            return "零"

        result = ""
        unit_position = 0
        while num > 0:
            digit = num % 10
            if digit != 0:
                result = f"{digits[digit]}{units[unit_position]}{result}"
            elif result and result[0] != "零":
                result = "零" + result
            num //= 10
            unit_position += 1

        # 处理 "一十" 的情况
        if result.startswith("一十"):
            result = result[1:]

        return result

    @staticmethod
    def pick_numbers(text: str) -> list[Union[int, float]]:
        numbers = []

        matches = re.findall(r'[+-]?\d+(?:\.\d+)?(?:[eE][+-]?\d+)?', text)
        for match in matches:
            try:
                # 转换为 float，如果是整数则转为 int
                num = float(match)
                if num.is_integer():
                    numbers.append(int(num))
                else:
                    numbers.append(num)
            except ValueError:
                pass
        return numbers

    @staticmethod
    def pick_number(text: str) -> Optional[Union[int, float]]:
        numbers = ValueUtils.pick_numbers(text)
        return numbers[0] if len(numbers) > 0 else None

    @staticmethod
    def get_type(value: Any) -> Optional[type]:
        """
        判断输入值的数据类型

        参数:
        value: 要判断的数据

        返回:
        str: 数据类型
        """
        if isinstance(value, int):
            return int
        elif isinstance(value, float):
            return float
        elif isinstance(value, complex):
            return complex
        elif isinstance(value, bool):
            return bool
        elif isinstance(value, str):
            return str
        else:
            return None