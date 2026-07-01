from __future__ import annotations

import enum
import json
import typing as t
from dataclasses import dataclass, fields


BSDM = t.TypeVar("BSDM", bound="BaseSerDeModel")
BSDE = t.TypeVar("BSDE", bound="BaseSerDeEnum")


def _serialize_field_value(
    value: t.Optional[t.Any], field_type: t.Type, json_converter: t.Dict[str, t.Callable]
) -> t.Any:
    """
    Serialize a field value to dict-compatible format.

    Handles:
    - None values
    - Enums (BaseSerDeEnum) -> string value
    - Nested models (has to_dict method) -> recursive dict
    - Lists -> recursive list
    - Sets -> list (JSON compatible)
    - Primitives -> pass through
    """
    if value is None:
        return None

    if "to_dict" in json_converter:
        return json_converter["to_dict"](value)

    if isinstance(value, BaseSerDeEnum):
        return value.value

    if hasattr(value, "to_dict"):
        return value.to_dict()

    origin = t.get_origin(field_type)

    if origin in (list, set) or isinstance(value, (list, set)):
        return [_serialize_field_value(item, t.Any, {}) for item in value]

    return value


def _deserialize_field_value(
    value: t.Any, field_type: t.Type, json_converter: t.Dict[str, t.Callable]
) -> t.Any:
    """
    Deserialize a field value from dict to proper Python type.

    Handles:
    - None values
    - Optional types
    - Lists -> recursive list with type conversion
    - Sets -> set from list
    - Enums (BaseSerDeEnum) -> construct from string
    - Nested models (has from_dict) -> recursive from_dict
    - Primitives -> pass through
    """
    if "from_dict" in json_converter:
        return json_converter["from_dict"](value)

    if value is None:
        return None

    origin = t.get_origin(field_type)
    args = t.get_args(field_type)

    if args and type(None) in args:
        field_type = [arg for arg in args if arg is not type(None)][0]

    if hasattr(field_type, "from_dict"):
        return field_type.from_dict(value)  # ty: ignore[call-non-callable]

    if origin is list:
        return [_deserialize_field_value(item, args[0], {}) for item in value]

    if origin is set:
        return {_deserialize_field_value(item, args[0], {}) for item in value}

    try:
        if issubclass(field_type, BaseSerDeEnum):
            return field_type(value)
    except TypeError:
        pass

    return value


@dataclass
class BaseSerDeModel:
    @classmethod
    def from_json(cls: t.Type[BSDM], payload: str) -> BSDM:
        return cls.from_dict(json.loads(payload))

    def to_json(self, **kwargs: t.Any) -> str:
        return json.dumps({**kwargs, **self.to_dict()})

    @classmethod
    def from_dict(cls: t.Type[BSDM], data: dict) -> BSDM:
        """
        Convert dictionary to dataclass instance with automatic type conversion.

        Handles:
        - Enums (BaseSerDeEnum) -> construct from string
        - Sets -> construct from list
        - Nested models (BaseSerDeModel) -> recursive from_dict
        - Lists of models -> list of from_dict calls
        - Optional types -> None handling
        - Primitives -> pass through
        - Custom converters via json_converter metadata
        """
        type_hints = t.get_type_hints(cls)
        kwargs = {}

        for field in fields(cls):
            field_name = field.name
            if field_name not in data:
                continue

            field_value = data[field_name]
            field_type = type_hints.get(field_name, field.type)

            kwargs[field_name] = _deserialize_field_value(
                field_value, field_type, field.metadata.get("json_converter", {})
            )

        return cls(**kwargs)

    def to_dict(self) -> dict:
        """
        Convert dataclass instance to dictionary with automatic type conversion.

        Handles:
        - Enums (BaseSerDeEnum) -> str value
        - Sets -> list (JSON compatible)
        - Nested models (BaseSerDeModel) -> recursive dict
        - Lists of models -> list of dicts
        - Optional types -> None handling
        - Primitives -> pass through
        - Custom converters via json_converter metadata
        """
        type_hints = t.get_type_hints(type(self))
        result = {}

        for field in fields(self):
            field_name = field.name
            field_value = getattr(self, field_name)
            field_type = type_hints.get(field_name, field.type)

            result[field_name] = _serialize_field_value(
                field_value, field_type, field.metadata.get("json_converter", {})
            )

        return result

    @classmethod
    def from_proto(cls: t.Type[BSDM], proto: t.Any) -> BSDM:
        """
        Convert protobuf message to dataclass instance.

        This method is implemented by the @proto_dataclass decorator.
        If you see this error at runtime, ensure your class is decorated with:
            @proto_dataclass(proto_message_cls)
            @dataclass
            class YourModel(BaseSerDeModel): ...
        """
        raise NotImplementedError(
            f"{cls.__name__} must be decorated with @proto_dataclass. "
            f"Add @proto_dataclass(your_proto_message_cls) above @dataclass."
        )

    def to_proto(self) -> t.Any:
        """
        Convert dataclass instance to protobuf message.

        This method is implemented by the @proto_dataclass decorator.
        If you see this error at runtime, ensure your class is decorated with:
            @proto_dataclass(proto_message_cls)
            @dataclass
            class YourModel(BaseSerDeModel): ...
        """
        raise NotImplementedError(
            f"{type(self).__name__} must be decorated with @proto_dataclass. "
            f"Add @proto_dataclass(your_proto_message_cls) above @dataclass."
        )


class BaseSerDeEnum(str, enum.Enum):
    @classmethod
    def from_proto(cls: t.Type[BSDE], proto_value: int) -> BSDE:
        """
        Convert protobuf enum value to Python enum.

        This method is implemented by the @proto_enum decorator.
        If you see this error at runtime, ensure your enum is decorated with:
            @proto_enum(proto_enum_cls)
            class YourEnum(BaseSerDeEnum): ...
        """
        raise NotImplementedError(
            f"{cls.__name__} must be decorated with @proto_enum. "
            f"Add @proto_enum(your_proto_enum_cls) above the class definition."
        )

    def to_proto(self) -> int:
        """
        Convert Python enum to protobuf enum value.

        This method is implemented by the @proto_enum decorator.
        If you see this error at runtime, ensure your enum is decorated with:
            @proto_enum(proto_enum_cls)
            class YourEnum(BaseSerDeEnum): ...
        """
        raise NotImplementedError(
            f"{type(self).__name__} must be decorated with @proto_enum. "
            f"Add @proto_enum(your_proto_enum_cls) above the class definition."
        )
