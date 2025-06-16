from dataclasses import dataclass, field, asdict, fields
from typing import Optional


@dataclass
class InternalBaseInterface:
    def __post_init__(self):
        # 初始化 __explicitly_set_fields__ 集合
        self.__explicitly_set_fields__ = set()

        for f in fields(self):
            value = getattr(self, f.name)
            if f.name in self.__explicitly_set_fields__ or value is not f.default:
                self.__explicitly_set_fields__.add(f.name)

    def __init__(self, **kwargs):
        # 初始化 __explicitly_set_fields__ 集合
        self.__explicitly_set_fields__ = set()

        for f in fields(self):
            if f.name in kwargs:
                value = kwargs[f.name]
                setattr(self, f.name, value)
                self.__explicitly_set_fields__.add(f.name)

    def to_dict(self, exclude_unset: bool = False, exclude_defaults: bool = False, exclude_none: bool = False):
        # 將 dataclass 轉換為字典
        data = asdict(self)

        if exclude_unset:
            # 過濾掉那些未被明確設置的欄位
            data = {k: v for k, v in data.items() if k in self.__explicitly_set_fields__ or v is not None}

        if exclude_defaults:
            # 過濾掉那些設置為預設值的欄位
            data = {k: v for k, v in data.items() if v != self.__dataclass_fields__[k].default}

        if exclude_none:
            # 過濾掉那些值為 None 的欄位
            data = {k: v for k, v in data.items() if v is not None}

        return data
