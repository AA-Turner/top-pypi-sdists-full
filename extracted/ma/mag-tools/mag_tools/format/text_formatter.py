from dataclasses import dataclass, field
from datetime import date, datetime, time
from typing import Any,  Optional

import numpy as np

from mag_tools.bean.array import Array
from mag_tools.enums.justify_type import JustifyType
from mag_tools.utils.data.value_utils import ValueUtils
from mag_tools.format.string_format import StringFormat


@dataclass
class TextFormatter:
    """
    文本拼接的格式，用于将多个字符串拼接为一个文本时使用
    """
    number_per_line: Optional[int] = field(default=None, metadata={"description": "每行显示的数据个数"})
    justify_type: Optional[JustifyType] = field(default=JustifyType.LEFT, metadata={"description": "对齐方式"})
    at_header: Optional[str] = field(default='', metadata={"description": "句首添加的字符串"})
    at_end: Optional[str] = field(default='', metadata={"description": "句尾添加的字符串"})
    decimal_places: Optional[int] = field(default=2, metadata={"description": "小数位数"})
    decimal_places_of_zero: Optional[int] = field(default=1, metadata={"description": "小数为0时的小数位数"})
    pad_length: Optional[int] = field(default=None, metadata={"description": "字段显示长度，为 None 保持字段原长度"})
    pad_char: Optional[str] = field(default=' ', metadata={"description": "填充占位符"})
    scientific: bool = field(default=False, metadata={"description": "是否使用科学计数法"})
    none_default: str = field(default=None, metadata={'description': 'int或float字段为None时的缺省值'})
    group_by_layer: bool = field(default=True, metadata={'description': "对3D数组分层展示，对2D数组分行展示"})
    merge_duplicate: bool = field(default=False, metadata={'description': '是否合并重复的数据'})

    def array_1d_to_lines(self, array_1d: list[Any]) -> list[str]:
        """
        将一维数组转换为多行文本表示,相邻的重复数据采用 m*A的方法
        :param array_1d: 一维数组，包含任意类型的数值
        :return: 多行文本表示的数组
        """
        result = self.__merge_array_1d(array_1d)
        max_length = len(max((s for s in result if isinstance(s, str)), key=len, default=""))
        return self.__to_lines(result, max_length)

    def array_2d_to_lines(self, array_2d: list[list[Any]]) -> list[str]:
        """
        将二维数组平铺为一维，然后生成数值块,相邻的重复数据采用 m*A的方法
        :param array_2d: 二维数组
        :return: 数值块，由多行构成，每行由 "数值" 或 "数值个数*数值"构成
        """
        if self.group_by_layer:
            new_array_2d = []
            # 遍历每一行后添加到列表中
            num_rows = np.array(array_2d).shape[0]  # 行数
            for i in range(num_rows):
                new_array_2d.append(self.__merge_array_1d(array_2d[i]))

            array_1d_sum = self.__to_blocks(new_array_2d)
        else:
            # 将其展平为一维数组后添加到列表中
            layer = np.array(array_2d).flatten()
            array_1d_sum = self.array_1d_to_lines(layer.tolist())
        return array_1d_sum

    def array_3d_to_lines(self, array_3d: list[list[list[Any]]]) -> list[str]:
        """
        将三维数组按层平铺为二维，然后生成数值块,相邻的重复数据采用 m*A的方法
        :param array_3d: 三维数组
        :return: 数值块，由多行构成，每行由 "数值" 或 "数值个数*数值"构成
        """
        #分层展示
        if self.group_by_layer:
            new_array_2d = []
            # 遍历每一层并将其展平为一维数组后添加到列表中
            num_layers = np.array(array_3d).shape[0]  # 层数
            for i in range(num_layers):
                array_1d = np.array(array_3d[i]).flatten().tolist()
                new_array_2d.append(self.__merge_array_1d(array_1d))

            array_1d_sum = self.__to_blocks(new_array_2d)
        #所有数据合并一个块后展示
        else:
            array_1d = np.array(array_3d).flatten()
            array_1d_sum = self.array_1d_to_lines(array_1d.tolist())

        return array_1d_sum

    def arrays_to_lines(self, arrays: list[Array]) -> list[str]:
        self.pad_length = 0
        blocks = []
        for array_ in arrays:
            items = [array_.array_name, array_.unit_name]
            items.extend(array_.data)
            blocks.append(items)

        return self.__to_blocks(blocks)

    def __merge_array_1d(self, array_1d: list[Any]) -> list[Any]:
        """
        合并一维数组,相邻的重复数据采用 m*A的方法
        :param array_1d: 一维数组，包含任意类型的数值
        """
        if array_1d is None:
            return []

        result = []

        #需要合并重复数据
        if self.merge_duplicate:
            count = 1
            current_value = array_1d[0]

            for i in range(1, len(array_1d)):
                if array_1d[i] == current_value:
                    count += 1
                else:
                    current_text = ValueUtils.to_string(current_value, self.decimal_places,
                                                        self.decimal_places_of_zero, self.scientific)
                    if current_text is None:
                        current_text = self.none_default

                    txt = f"{count}*{current_text}" if count > 1 else f"{current_text}"
                    result.append(txt)

                    current_value = array_1d[i]
                    count = 1

            # 处理最后一组数据
            current_text = ValueUtils.to_string(current_value, self.decimal_places,
                                                self.decimal_places_of_zero, self.scientific)
            if current_text is None:
                current_text = self.none_default
            txt = f"{count}*{current_text}" if count > 1 else f"{current_text}"
            result.append(txt)
        else:
            for v in array_1d:
                result.append(ValueUtils.to_string(v, self.decimal_places, self.decimal_places_of_zero, self.scientific, self.none_default))

        return result

    def __to_lines(self, values: list[Any], max_len: int) -> list[str]:
        """
        将数值数组转为按指定格式的字符串
        :param values: 数值数组
        :param max_len: 字段显示的最大长度,为None时则按格式中定义的长度
        """
        padding_length = max(self.pad_length, max_len) if self.pad_length is not None else None

        lines = list()
        for value in values:
            if isinstance(value, int) or isinstance(value, float):
                value_str = ValueUtils.to_string(value=value,
                                                 decimal_places=self.decimal_places,
                                                 decimal_places_of_zero=self.decimal_places_of_zero,
                                                 scientific=self.scientific,
                                                 none_default=self.none_default)
            elif isinstance(value, date):
                value_str = value.strftime('%Y-%m-%d')
            elif isinstance(value, time):
                value_str = value.strftime('%H:%M:%S')
            elif isinstance(value, datetime):
                value_str = value.strftime('%Y-%m-%d %H:%M:%S')
            else:
                value_str = str(value)

            lines.append(value_str if value_str is not None else self.none_default)

        return StringFormat.pad_text(strings=lines,
                                     padding_length=padding_length,
                                     justify=self.justify_type,
                                     number_per_line=self.number_per_line,
                                     at_header=self.at_header,
                                     at_end=self.at_end,
                                     pad_char=self.pad_char)

    def __to_blocks(self, values: list[list[Any]]) -> list[str]:
        max_len = max(len(str(item)) for sublist in values for item in sublist)

        lines = []
        for value in values:
            lines.extend(self.__to_lines(value, max_len))
        return lines