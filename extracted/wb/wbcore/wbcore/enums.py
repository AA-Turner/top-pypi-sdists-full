from enum import Enum
from typing import Union


class RequestType(Enum):
    GET = "get"
    POST = "post"
    DELETE = "delete"
    PATCH = "patch"
    PUT = "put"
    OPTIONS = "options"
    HEAD = "head"


class WidgetType(Enum):
    LIST = "list"
    INSTANCE = "instance"
    CHART = "chart"
    SELECT = "select"
    HTML = "html"


class Operator(Enum):
    EQUAL = "=="
    UNEQUAL = "!="
    GREATER = ">"
    GREATER_EQUAL = ">="
    LESS = "<"
    LESS_EQUAL = "<="
    EXISTS = "∃"


class Unit(Enum):
    FRACTION = "fr"
    REM = "rem"
    PIXEL = "px"

    def __call__(self, _value):
        return (float(_value), self.value)

    def unit(self, _value: Union[float, str, int]):
        assert isinstance(_value, (float, str, int)), "_value needs to be one of str, float or int"

        return f"{float(_value)}{self.value}"


class AuthType(Enum):
    NONE = "NONE"
    JWT = "JWT"
