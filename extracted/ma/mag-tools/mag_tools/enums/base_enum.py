from enum import Enum
from typing import Optional, Union


class BaseEnum(Enum):
    def __init__(self, code: Union[str, int], desc: Optional[str] = None):
        self._code = code
        self._desc = desc

    @classmethod
    def of_name(cls, name: str, default_value=None) :
        return getattr(cls, name, default_value)

    @classmethod
    def of_code(cls, code: Optional[Union[str, int]], default_value=None):
        """
        根据代码获取枚举
        :param code: 代码
        :param default_value: 缺省值
        :return: 枚举
        """
        if code is not None:
            for _enum in cls:
                if str(_enum.code).upper() == str(code).upper():
                    return _enum
        return default_value

    @classmethod
    def of_desc(cls, desc: str, default_value=None):
        for _enum in cls:
            if _enum.desc == desc:
                return _enum
        return default_value

    @property
    def code(self):
        return self._code

    @property
    def desc(self):
        return self._desc

    @classmethod
    def names(cls):
        return [enum_member.name for enum_member in cls]

    @classmethod
    def codes(cls):
        return [enum_member.code for enum_member in cls]

    def __str__(self):
        return f"{self.name}[code={self.code}, desc={self.desc}]"

    @classmethod
    def of(cls, enum_type: type, value: str):
        if issubclass(enum_type, Enum):
            if value is not None and hasattr(enum_type, 'of_code'):
                enum_value = enum_type.of_code(value)
                if enum_value is None and hasattr(enum_type, 'of_name'):
                    enum_value = enum_type.of_name(value)

                return enum_value
        return None