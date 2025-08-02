# arpakit

from typing import Any

_ARPAKIT_LIB_MODULE_VERSION = "3.0"


def combine_dicts(*dicts: dict) -> dict[Any, Any]:
    res = {}
    for dict_ in dicts:
        res.update(dict_)
    return res


def replace_dict_key(*, dict_: dict, old_key: Any, new_key: Any) -> dict[Any, Any]:
    if old_key in dict_:
        dict_[new_key] = dict_.pop(old_key)
    return dict_


def __example():
    pass


if __name__ == '__main__':
    __example()
