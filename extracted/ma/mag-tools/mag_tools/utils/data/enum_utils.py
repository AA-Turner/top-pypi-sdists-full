from enum import Enum
from typing import Type


class EnumUtils:
    @staticmethod
    def get_enum_type(enum_cls: Type[Enum], variable_name: str):
        for member in enum_cls:
            if hasattr(member, variable_name):
                return type(getattr(member, variable_name))
        return None