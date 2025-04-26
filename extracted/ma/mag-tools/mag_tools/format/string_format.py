import random
from datetime import date, datetime
from typing import  Optional

from mag_tools.enums.justify_type import JustifyType
from mag_tools.utils.data.list_utils import ListUtils
from mag_tools.utils.data.random_generator import RandomGenerator
from mag_tools.utils.data.string_utils import StringUtils


class StringFormat:
    @staticmethod
    def pad_string(string: str, padding_length: Optional[int] = None, justify: JustifyType = JustifyType.RIGHT, pad_char: Optional[str] = None) -> str:
        """
        将字符串用空格补充到指定长度，空格添加在字符串前。
        参数：
        :param justify: 对齐方式，空格补齐
        :param string: 原始数值或字符串
        :param padding_length: 目标长度
        :param pad_char: 分隔符号，为None则缺省为空格
        :return: 补充空格后的字符串
        """
        if string is None:
            raise ValueError('字符串不是能为空')

        pad_char = pad_char if pad_char else ' '
        pad_len = max(len(string), padding_length) if padding_length is not None else len(string)

        padding_size = pad_len - len(string) #要填充的占位符个数
        if justify == JustifyType.RIGHT:
            return f"{pad_char * padding_size}{string}"
        elif justify == JustifyType.CENTER:
            left_padding = pad_char * (padding_size // 2)
            right_padding = pad_char * (padding_size - padding_size // 2)
            return  f'{left_padding}{string}{right_padding}'
        else:
            return f"{string}{pad_char * padding_size}"

    @staticmethod
    def pad_text(strings: list[str],
                 padding_length: Optional[int] = None,
                 justify: JustifyType = JustifyType.RIGHT,
                 number_per_line: Optional[int] = None,
                 at_header: Optional[str] = None,
                 at_end: Optional[str] = None,
                 pad_char: Optional[str] = None) -> list[str]:
        """
        将字符串数组按指定格式拼接为文本
        :param strings: 字符串数组
        :param padding_length: 填写后长度，为None则为原字段长度
        :param justify: 对齐方式
        :param number_per_line: 每行字段个数，为None表示不限定
        :param at_header: 文本首的填充内容
        :param at_end: 文本尾的填充内容
        :param pad_char: 分隔符号
        """
        if number_per_line is None:
            number_per_line = len(strings)
        at_header = at_header if at_header else ''
        at_end = at_end if at_end else ''
        pad_char = pad_char if pad_char else ' '

        max_length = max(len(str(s)) for s in strings)
        padding_length = max(padding_length, max_length) if padding_length is not None else None

        items = [StringFormat.pad_string(s, padding_length, justify) for s in strings]
        blocks = ListUtils.split(items, number_per_line)
        lines = [f'{at_header}{pad_char.join(block)}{at_end}' for block in blocks]
        return lines

    @staticmethod
    def format_function(template: Optional[str]) -> Optional[str]:
        """
        格式化字符串，处理{}中的特定函数，如果不是函数，则直接返回
        """
        if template is None or not all(c in template for c in '()'):
            return template

        while '{' in template and '}' in template:
            start = template.index('{')
            end = template.index('}', start)
            expression = template[start + 1:end]

            # 解析函数名和参数
            func_name, args = StringUtils.parse_function(expression)

            # 调用相应的函数
            if func_name == 'random_text':
                result = RandomGenerator.ascii_letters(int(args[0]))
            elif func_name == 'random_string':
                result = RandomGenerator.string(int(args[0]))
            elif func_name == 'random_chinese':
                length = int(args[0]) if args[0] else random.randint(1, 100)
                result = RandomGenerator.chinese_string(length)
            elif func_name == 'random_number':
                result = RandomGenerator.number_string(int(args[0]))
            elif func_name == 'random_int':
                min_value = int(args[0] if len(args) >= 2 else 1)
                max_value = int(args[1] if len(args) >= 2 else args[0])

                result = str(random.randint(min_value, max_value))
            elif func_name == 'random_date':
                year = int(args[0]) if len(args) > 0 else date.today().year
                fmt = args[1] if len(args) > 1 else "%Y%m%d"
                result = RandomGenerator.date(year).strftime(fmt)
            elif func_name == 'today':
                fmt = args[0] if len(args) > 0 else "%Y%m%d"
                result = date.today().strftime(fmt)
            elif func_name == 'current':
                fmt = args[0] if len(args) > 0 else "%Y-%m-%d %H:%M:%S"
                result = datetime.now().strftime(fmt)
            else:
                raise ValueError(f"未知的函数: {func_name}")

            # 替换模板中的表达式
            template = template[:start] + result + template[end + 1:]

        return template

