# arpakit

import json
from typing import Any

from arpakitlib.ar_enumeration_util import Enumeration

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


class NeedTypes(Enumeration):
    str_ = "str"
    int_ = "int"
    bool_ = "bool"
    float_ = "float"
    list_of_int = "list_of_int"
    list_of_str = "list_of_str"
    list_of_float = "list_of_float"
    json = "json"


def parse_need_type(value: Any, need_type: str, allow_none: bool = False) -> Any:
    if allow_none and value is None:
        return None

    if not allow_none and value is None:
        raise ValueError("value is None")

    NeedTypes.parse_and_validate_values(need_type)

    if need_type == NeedTypes.str_:
        res = value
    elif need_type == NeedTypes.int_:
        res = int(value)
    elif need_type == NeedTypes.bool_:
        if value.lower() in ["true", "1"]:
            res = True
        elif value.lower() in ["false", "0"]:
            res = False
        else:
            raise ValueError(f"value {value} is not bool type")
    elif need_type == NeedTypes.float_:
        res = float(value)
    elif need_type == NeedTypes.list_of_int:
        res = value.removeprefix("[").removesuffix("]")
        res = [int(num.strip()) for num in res.split(",")]
    elif need_type == NeedTypes.list_of_str:
        res = value.removeprefix("[").removesuffix("]").strip()
        if not res:
            res = []
        else:
            res = [num.strip() for num in res.split(",")]
    elif need_type == NeedTypes.list_of_float:
        res = value.removeprefix("[").removesuffix("]")
        res = [float(num.strip()) for num in res.split(",")]
    elif need_type == NeedTypes.json:
        res = json.loads(value)
    else:
        raise ValueError(f"bad need_type {need_type}")

    return res


def __example():
    print(parse_need_type(value=123, need_type="int"))
    print(parse_need_type(value="True", need_type="bool"))
    print(parse_need_type(value=123.456, need_type="float"))
    print(parse_need_type(value='[1, 2, 3]', need_type="list_of_int"))
    print(parse_need_type(value='["a", "b", "c"]', need_type="list_of_str"))
    print(parse_need_type(value='[1.1, 2.2, 3.3]', need_type="list_of_float"))
    print(parse_need_type(value='{"key": "value"}', need_type="json"))
    print(parse_need_type(value="hello world", need_type="str"))
    print(parse_need_type(value="[]", need_type=NeedTypes.list_of_str))
    print(parse_need_type(value="", need_type=NeedTypes.list_of_str))
    print(parse_need_type(value="none,asfasfas", need_type=NeedTypes.list_of_str))


if __name__ == '__main__':
    __example()
