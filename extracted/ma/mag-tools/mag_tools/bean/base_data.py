from dataclasses import MISSING, dataclass, fields
from typing import Any,   Optional, Union

import random

from mag_tools.format.text_formatter import TextFormatter
from mag_tools.enums.justify_type import JustifyType


@dataclass
class BaseData:
    """
    Bean的基类
    """
    _formatter = TextFormatter(
        number_per_line=None,
        justify_type=JustifyType.LEFT,
        at_header='',
        at_end='',
        decimal_places=6,
        decimal_places_of_zero=1,
        pad_length=None,
        pad_char=' ',
        scientific=False,
        none_default='NA'
    )

    def __repr__(self):
        field_dict = {k: v for k, v in self.__dict__.items() if not k.startswith('_')}
        field_str = ', '.join(f"{k}={v}" for k, v in field_dict.items())
        return f"{self.__class__.__name__}({field_str})"

    def __str__(self):
        excluded_attributes = {}
        attributes = [
            f"{attr}={repr(getattr(self, attr))}"
            for attr in vars(self)
            if getattr(self, attr) is not None and attr not in excluded_attributes
        ]
        return f"{self.__class__.__name__}({', '.join(attributes)})"

    def __getitem__(self, item):
        if hasattr(self, item):
            return getattr(self, item)
        raise KeyError(f"{item} not found in {self.__class__.__name__}")

    @classmethod
    def get_default_value(cls, field_name: str) -> Any:
        """
        获取字段的缺省值
        """
        for f in fields(cls):   # type: ignore
            if f.name == field_name:
                return f.default if f.default is not MISSING else None
        raise ValueError(f"Field '{field_name}' not found in {cls.__name__}")

    @classmethod
    def get_metadata(cls, field_name: str, prop_name: str) -> Any:
        """
        获取字段的metadata属性
        """
        for f in fields(cls):  # type: ignore
            if f.name == field_name:
                return f.metadata.get(prop_name) if f.metadata is not MISSING else None
        raise ValueError(f"Field '{field_name}.{prop_name}' not found in {cls.__name__}")

    @property
    def to_map(self) -> dict[str, Any]:
        return {
            k: repr(v) for k, v in self.__dict__.items()
            if not (k.startswith('__') and k.endswith('__')) and k not in {'_text_format', '_data_formats'}
        }

    def set_random_value(self, field_name: str, max_value: Union[float,int] = None, min_value: Union[float,int] = 0) -> Any:
        """
        为指定字段随机生成值并设置到实例属性中。

        :param field_name: 数据类中的字段名
        :param max_value: 最大值（可选）
        :param min_value: 最小值（默认为0）
        """
        for f in fields(self):  # type: ignore
            # 处理 int 和 float 类型
            if f.name == field_name and issubclass(f.type, (int, float)):
                min_ = min_value if min_value else f.metadata.get('min', min_value) if f.metadata is not MISSING else min_value
                max_ = max_value if max_value else f.metadata.get('max', max_value) if f.metadata is not MISSING else max_value

                if min_ is None or max_ is None or min_ > max_:
                    raise ValueError("min_value 和 max_value 必须提供有效范围。")

                value = random.randint(min_, max_) if f.type == int else random.uniform(min_, max_)
                setattr(self, field_name, value)
                return value
        raise ValueError(f"Field '{field_name}' not found in {self.__name__}")

    def set_random_array(self, field_name: str, size: int, max_value: Union[float,int] = None, min_value: Union[float,int] = 0) -> Any:
        """
        为指定字段随机生成值并设置到实例属性中。

        :param field_name: 数据类中的字段名
        :param max_value: 最大值（可选）
        :param min_value: 最小值（默认为0）
        :param size: 数组的长度
        """
        for f in fields(self):  # type: ignore
            # 处理 list[int] 和 list[float] 类型
            if f.name == field_name and f.type in (list[int], list[float], list[int], list[float]):
                min_ = min_value if min_value else f.metadata.get('min', min_value) if f.metadata is not MISSING else min_value
                max_ = max_value if max_value else f.metadata.get('max', max_value) if f.metadata is not MISSING else max_value

                if min_ is None or max_ is None or min_ > max_:
                    raise ValueError("min_value 和 max_value 必须提供有效范围。")

                # 生成随机列表
                value = [
                    random.randint(min_, max_) if f.type == list[int] else random.uniform(min_, max_)
                    for _ in range(size)
                ]
                setattr(self, field_name, value)
                return value
        raise ValueError(f"Field '{field_name}' not found in {self.__name__}")

    def set_random_array_3d(
        self,
        field_name: str,
        shape: list[int],
        max_value: Union[int, float] = None,
        min_value: Union[int, float] = 0) -> Any:
        """
        为指定字段生成嵌套随机数组并设置到实例属性中。

        :param field_name: 数据类中的字段名
        :param shape: 数组的形状，例如 [2, 3, 4] 表示 2x3x4 的三维数组
        :param max_value: 最大值（可选）
        :param min_value: 最小值（默认为 0）
        """
        for f in fields(self):   # type: ignore
            if f.name == field_name and f.type in (list[list[list[int]]],
                                                   list[list[list[float]]],
                                                   list[list[list[Optional[int]]]],
                                                   list[list[list[Optional[float]]]],
                                                   list[list[list[int]]],
                                                   list[list[list[float]]],
                                                   list[list[list[Optional[int]]]],
                                                   list[list[list[Optional[float]]]]):
                min_ = min_value if min_value else f.metadata.get('min', min_value) if f.metadata is not MISSING else min_value
                max_ = max_value if max_value else f.metadata.get('max', max_value) if f.metadata is not MISSING else max_value

                if min_ is None or max_ is None or min_ > max_:
                    raise ValueError("min_value 和 max_value 必须提供有效范围。")

                # 递归生成嵌套数组
                def generate_nested_array(current_shape: list[int]) -> Any:
                    if len(current_shape) == 1:  # 最后一维生成随机值
                        return [
                            random.randint(min_, max_)
                            if f.type in [list[list[list[int]]], list[list[list[Optional[int]]]], list[list[list[int]]], list[list[list[Optional[int]]]]]
                            else random.uniform(min_, max_)
                            for _ in range(current_shape[0])
                        ]
                    return [
                        generate_nested_array(current_shape[1:])
                        for _ in range(current_shape[0])
                    ]

                # 生成随机嵌套数组
                value = generate_nested_array(shape)
                setattr(self, field_name, value)
                return value

        raise ValueError(f"Field '{field_name}' not found in {self.__class__.__name__}")
