import json
from dataclasses import asdict, is_dataclass
from datetime import date, datetime
from decimal import Decimal
from enum import Enum
from typing import Any, Optional, Type, TypeVar, get_origin

from anytree import Node

from mag_tools.enums.base_enum import BaseEnum
from mag_tools.bean.easy_map import EasyMap
from mag_tools.bean.easy_map import K, V
from mag_tools.bean.results import Results
from mag_tools.jsonparser.json_encoder import JsonEncoder
from mag_tools.enums.service_status import ServiceStatus
from mag_tools.utils.data.map_utils import MapUtils
from mag_tools.utils.data.value_utils import ValueUtils
from mag_tools.utils.common.class_utils import ClassUtils

T = TypeVar('T')
E = TypeVar('E')

class JsonParser:
    @staticmethod
    def to_string(json_src: str) -> str:
        return json.loads(json_src)

    @staticmethod
    def to_decimal(json_src: str) -> Optional[Decimal]:
        if not json_src:
            return None
        return Decimal(json.loads(json_src))

    @staticmethod
    def to_float(json_src: str) -> Optional[float]:
        if not json_src:
            return None
        return float(json.loads(json_src))

    @staticmethod
    def to_int(json_src: str) -> Optional[int]:
        if not json_src:
            return None
        return int(json.loads(json_src))

    @staticmethod
    def to_datetime(json_src: str) -> Optional[datetime]:
        if not json_src:
            return None
        return datetime.strptime(json.loads(json_src), '%Y-%m-%dT%H:%M:%S.%fZ')

    @staticmethod
    def to_bool(json_src: str) -> bool:
        json_str = JsonParser.to_string(json_src).lower()
        return json_str in ("y", "yes", "true", "t", "1")

    @staticmethod
    def to_enum(json_src: str, enum_type: Optional[Type[E]]) -> Optional[E]:
        if not json_src or not issubclass(enum_type, Enum):
            return None
        enum_str = JsonParser.to_string(json_src)
        for member in enum_type:
            if member.name == enum_str or member.value == enum_str:
                return member
        return None

    @staticmethod
    def to_bean(json_src: str, clazz: Optional[Type[T]]) -> Optional[T]:
        if not json_src or not clazz:
            return None
        if not isinstance(json_src, str):
            json_src = JsonParser.from_bean(json_src)

        bean = json.loads(json_src, object_hook=lambda d: clazz(**d))
        for attr_name, attr_type in clazz.__annotations__.items():
            attr_type = ClassUtils.get_origin_type(attr_type)

            if get_origin(attr_type) == tuple:
                attr_value = getattr(bean, attr_name, None)
                if isinstance(attr_value, list):  # 如果是 list，转换为 tuple
                    setattr(bean, attr_name, tuple(attr_value))
            elif issubclass(attr_type, Enum):
                attr_value = getattr(bean, attr_name, None)
                enum_value = BaseEnum.of(attr_type, attr_value)
                setattr(bean, attr_name, enum_value)
        return bean

    @staticmethod
    def to_results(json_src: str, clazz: Optional[Type[T]]) -> Results[T]:
        if not json_src or not clazz:
            return Results()

        try:
            results_map = json.loads(json_src)
            results_map = MapUtils.keys_to_underline(results_map)

            data = list()
            for item in results_map.get('data', []):
                if clazz == bool:
                    data.append(bool(item))
                elif clazz == int:
                    data.append(int(item))
                elif clazz == float:
                    data.append(float(item))
                elif clazz == str:
                    data.append(str(item))
                elif clazz == datetime:
                    data.append(datetime.fromisoformat(item))
                else:
                    data.append(clazz(**item))

            result = Results(
                code=ServiceStatus.of_code(results_map.get('code')) if results_map.get('code') else None,
                message=results_map.get('message'),
                data=data,
                total_count=results_map.get('total_count'),
                timestamp=datetime.fromisoformat(results_map.get('timestamp')) if results_map.get('timestamp') else datetime.now()
            )
            return result
        except (json.JSONDecodeError, TypeError) as e:
            return Results.fail(str(e))

    @staticmethod
    def to_list(json_src: str, clazz: Optional[Type[T]]) -> list[T]:
        if not json_src or not clazz:
            return []
        return json.loads(json_src, object_hook=lambda d: clazz(**d))

    @staticmethod
    def to_tuple(json_src: str, clazz: Optional[Type[T]]) -> tuple[T] | None:
        if not json_src or not clazz:
            return tuple()
        list_ = json.loads(json_src, object_hook=lambda d: clazz(**d))
        return tuple(list_) if list_ else None

    @staticmethod
    def to_map(json_src: str, key_cls: Optional[Type[K]], value_cls: Optional[Type[V]]) -> dict[K, V]:
        if not json_src or not key_cls or not value_cls:
            return {}

        data_map = json.loads(json_src)
        return {
            ValueUtils.to_value(str(key), key_cls): ValueUtils.to_value(str(value), value_cls) if not isinstance(
                value, dict) else value_cls(
                **value) for key, value in data_map.items()
        }

    @staticmethod
    def to_easy_map(json_src: str, value_cls: Optional[Type[V]]) -> EasyMap[str, V]:
        return EasyMap(JsonParser.to_map(json_src, str, value_cls))


    @staticmethod
    def to_tree(json_src: str, clazz: Optional[Type[T]]) -> Node:
        if not json_src or not clazz:
            return Node("root")

        data = json.loads(json_src)

        def create_node(data_, parent=None):
            if isinstance(data_, dict):
                name = data_.get('name', 'root')
                data_object = clazz(**data_) if clazz != str else name
                node = Node(name, parent=parent, data=data_object)
                for child_data in data_.get('children', []):
                    create_node(child_data, parent=node)
            else:
                node = Node(str(data_), parent=parent)
            return node

        tree = create_node(data)
        return tree

    @staticmethod
    def from_bean(obj: Any) -> str:
        if isinstance(obj, (int, float, bool, str)):
            return json.dumps(obj) if obj else "null"
        elif isinstance(obj, (datetime, date)):
            return obj.isoformat() if obj else "null"
        elif isinstance(obj, list):
            obj = [asdict(o) if is_dataclass(o) else o for o in obj]
            return json.dumps(obj, cls=JsonEncoder) if obj else "[]"
        elif isinstance(obj, tuple):
            obj = list(obj)
            return json.dumps(obj, cls=JsonEncoder) if obj else "[]"
        elif isinstance(obj, dict):
            obj = {k: asdict(v) if is_dataclass(v) else v for k, v in obj.items()}
            return json.dumps(obj, cls=JsonEncoder) if obj else "{}"
        elif hasattr(obj, 'to_dict'):
            return json.dumps(obj.to_dict(), cls=JsonEncoder) if obj else None
        else:
            return json.dumps(obj, cls=JsonEncoder) if obj else "null"

    @staticmethod
    def from_results(obj: Results) -> str:
        json_str = JsonParser.from_bean(obj)
        results_map = json.loads(json_str)
        results_map = MapUtils.keys_to_hump(results_map)
        return json.dumps(results_map, cls=JsonEncoder) if results_map else "null"

    @staticmethod
    def to_json_by_type(obj: Any) -> Optional[str]:
        if obj is None:
            return None
        return json.dumps(obj, default=lambda o: o.__dict__, sort_keys=True, indent=4)