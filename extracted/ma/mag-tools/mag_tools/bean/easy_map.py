import json
from dataclasses import asdict, is_dataclass
from enum import Enum
from typing import Any,  Type, TypeVar, Optional
from datetime import datetime, date
from decimal import Decimal

from mag_tools.jsonparser.json_encoder import JsonEncoder
from mag_tools.enums.base_enum import BaseEnum
from mag_tools.utils.data.map_utils import MapUtils

K = TypeVar('K')
V = TypeVar('V')


class EasyMap(dict[K, V]):
    """
    Map简化操作类

    @author xlcao
    @version 2.2
    @copyright Copyright (c) 2015
    """

    def __init__(self, map_: Optional[dict[K, V]] = None) -> None:
        super().__init__(map_ if map_ else {})

    def add(self, key: K, value: V):
        """
        添加键值及对应的数值

        :param key: 键值
        :param value: 数值
        :return: self
        """
        if value is not None:
            self[key] = value
        return self

    def get_string(self, key: Any) -> Optional[str]:
        """
        从Map中取字符串

        :param key: 键值
        :return: 字符串
        """
        return str(self.get(key)) if self.get(key) is not None else None

    def get_byte(self, key: Any) -> Optional[bytes]:
        """
        从Map中取字节

        :param key: 键值
        :return: 字节
        """
        value = self.get_string(key)
        return bytes(value, 'utf-8') if value else None

    def get_int(self, key: Any) -> Optional[int]:
        """
        从Map中取整数

        :param key: 键值
        :return: 整数
        """
        value = self.get_string(key)
        try:
            return int(value) if value else None
        except ValueError:
            return None

    def get_float(self, key: Any) -> Optional[float]:
        """
        从Map中取Double

        :param key: 键值
        :return: Double
        """
        value = self.get_string(key)
        try:
            return float(value) if value else None
        except ValueError:
            return None

    def get_decimal(self, key: Any) -> Optional[Decimal]:
        """
        从Map中取BigDecimal

        :param key: 键值
        :return: BigDecimal
        """
        value = self.get_string(key)
        try:
            return Decimal(value) if value else None
        except ValueError:
            return None

    def get_date(self, key: Any) -> Optional[date]:
        """
        从Map中取日期

        :param key: 键值
        :return: 日期
        """
        value = self.get_string(key)
        try:
            return datetime.strptime(value, '%Y-%m-%d').date() if value else None
        except ValueError:
            return None

    def get_datetime(self, key: Any) -> Optional[datetime]:
        """
        从Map中取日期时间

        :param key: 键值
        :return: 日期时间
        """
        value = self.get_string(key)
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S') if value else None
        except ValueError:
            return None

    def get_time(self, key: Any) -> Optional[datetime.time]:
        """
        从Map中取时间

        :param key: 键值
        :return: 时间
        """
        value = self.get_string(key)
        try:
            return datetime.strptime(value, '%H:%M:%S').time() if value else None
        except ValueError:
            return None

    def get_bool(self, key: Any) -> bool:
        """
        从Map中取布尔值

        :param key: 键值
        :return: 布尔值
        """
        value = self.get_string(key)
        return value.lower() in ('y', 'yes', 't', 'true', '1') if value else False

    def get_enum(self, key: Any, enum_type: Type[Enum]) -> Optional[V]:
        """
        从Map中取枚举

        :param key: 键值
        :param enum_type: 枚举类型
        :return: 枚举值
        """
        try:
            code = self.get_string(key)
            if code:
                if issubclass(enum_type, BaseEnum):
                    return enum_type.of_code(code) or enum_type[code]
                else:
                    return enum_type[code]
        except KeyError:
            return None

    def get_string_by_json(self, key: Any) -> Optional[str]:
        """
        从Map中取字符串（JSON）

        :param key: 键值
        :return: 字符串
        """
        return json.dumps(self.get(key))

    def get_int_by_json(self, key: Any) -> Optional[int]:
        """
        从Map中取整数（JSON）

        :param key: 键值
        :return: 整数
        """
        value = self.get_string_by_json(key)
        try:
            return int(value) if value else None
        except ValueError:
            return None

    def get_float_by_json(self, key: Any) -> Optional[float]:
        """
        从Map中取float（JSON）

        :param key: 键值
        :return: float
        """
        value = self.get_string_by_json(key)
        try:
            return float(value) if value else None
        except ValueError:
            return None

    def get_decimal_by_json(self, key: Any) -> Optional[Decimal]:
        """
        从Map中取Decimal（JSON）

        :param key: 键值
        :return: Decimal
        """
        value = self.get_string_by_json(key)
        try:
            return Decimal(value) if value else None
        except ValueError:
            return None

    def get_date_by_json(self, key: Any) -> Optional[date]:
        """
        从Map中取日期（JSON）

        :param key: 键值
        :return: 日期
        """
        value = self.get_string_by_json(key)
        try:
            return datetime.strptime(value, '%Y-%m-%d').date() if value else None
        except ValueError:
            return None

    def get_datetime_by_json(self, key: Any) -> Optional[datetime]:
        """
        从Map中取日期时间（JSON）

        :param key: 键值
        :return: 日期时间
        """
        value = self.get_string_by_json(key)
        try:
            return datetime.strptime(value, '%Y-%m-%d %H:%M:%S') if value else None
        except ValueError:
            return None

    def get_time_by_json(self, key: Any) -> Optional[datetime.time]:
        """
        从Map中取时间（JSON）

        :param key: 键值
        :return: 时间
        """
        value = self.get_string_by_json(key)
        try:
            return datetime.strptime(value, '%H:%M:%S').time() if value else None
        except ValueError:
            return None

    def get_bool_by_json(self, key: Any) -> bool:
        """
        从Map中取布尔值（JSON）

        :param key: 键值
        :return: 布尔值
        """
        value = self.get_string_by_json(key)
        return value.lower() in ('y', 'yes', 't', 'true', '1') if value else False

    def get_enum_by_json(self, key: Any, enum_type: Type[V]) -> Optional[V]:
        """
        从Map中取枚举（JSON）

        :param key: 键值
        :param enum_type: 枚举类型
        :return: 枚举值
        """
        try:
            code = self.get_string_by_json(key)
            if code:
                if issubclass(enum_type, BaseEnum):
                    return enum_type.of_code(code) or enum_type[code]
                else:
                    return enum_type[code]
        except KeyError:
            return None

    def put(self, key: K, value: V) -> V:
        """
        添加键值及对应的数值

        :param key: 键值
        :param value: 数值
        :return: 数值
        """
        return super().__setitem__(key, value)

    def to_map(self) -> dict[K, V]:
        """
        转为Map

        :return: Map
        """
        return dict(self)

    def keys_to_hump(self) -> dict[str, Any]:
        """
        将键值转为驼峰格式，包括为对象的成员变量中的变量
        """
        obj = {k: asdict(v) if is_dataclass(v) else v for k, v in self.items()}
        json_str = json.dumps(obj, cls=JsonEncoder) if obj else "{}"

        new_map = json.loads(json_str)
        return MapUtils.keys_to_hump(new_map)

    def get_by_json(self, key: Any, clazz: Type[V]) -> Optional[V]:
        """
        从Map中取对象（JSON）

        :param key: 键值
        :param clazz: 类类型
        :return: 对象
        """
        value = self.get(key)
        return json.loads(value, object_hook=clazz) if value else None
