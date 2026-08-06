from __future__ import annotations

import enum
import typing as t
from dataclasses import Field, dataclass, fields

from google.protobuf.message import Message
from typing_extensions import dataclass_transform


@dataclass
class FieldInfo:
    name: str
    field_type: t.Type
    proto_converter: t.Dict[str, t.Dict[str, t.Callable]]

    @property
    def from_proto_converter(self) -> t.Callable | None:
        return getattr(self.field_type, "from_proto", self.proto_converter.get("from_proto"))  # ty: ignore[invalid-return-type]

    @property
    def to_proto_converter(self) -> t.Callable | None:
        return getattr(self.field_type, "to_proto", self.proto_converter.get("to_proto"))  # ty: ignore[invalid-return-type]

    @property
    def is_optional(self) -> bool:
        args = t.get_args(self.field_type)
        return args is not None and type(None) in args

    @property
    def inner_types(self) -> t.Tuple[t.Type, ...]:
        return t.get_args(self.field_type)

    @property
    def outer_type(self) -> t.Type | None:
        return t.get_origin(self.field_type)

    def create_inner_field_info(self) -> FieldInfo:
        return FieldInfo(
            name=self.name,
            field_type=next(x for x in self.inner_types if x is not type(None)),
            proto_converter={},
        )

    @classmethod
    def from_field(cls, field: Field, type_hints: t.Dict[str, t.Type]) -> FieldInfo:
        field_type = type_hints.get(field.name, field.type)
        assert field_type is not None, f"Field {field} has no type"
        proto_converter = field.metadata.get("proto_converter", {})
        return cls(
            name=field.name,
            field_type=field_type,  # type: ignore
            proto_converter=proto_converter,
        )


@dataclass_transform()
def proto_dataclass(proto_cls: t.Type, **dataclass_kwargs: t.Any) -> t.Callable[[t.Type], t.Type]:
    """
    Decorator that auto-generates from_proto() and to_proto() methods for dataclasses.

    Automatically applies @dataclass internally.

    Args:
        proto_cls: The protobuf message class corresponding to this dataclass
        **dataclass_kwargs: Optional kwargs passed to @dataclass (frozen, kw_only, slots, etc.)

    Usage:
        @proto_dataclass(shared_pb2.QueryDependency)
        class QueryDependency(BaseSerdeModel):
            name: str
            query: str

        # With dataclass kwargs:
        @proto_dataclass(shared_pb2.QueryDependency, frozen=True)
        class QueryDependency(BaseSerdeModel):
            name: str
            query: str

    The decorator analyzes the dataclass fields and their type annotations to generate
    appropriate conversion logic for:
    - Primitives (str, int, bool, float)
    - Optional types (t.Optional[T])
    - Collections (t.List[T], t.Dict[K,V], t.Set[T])
    - Nested models (other BaseSerdeModel subclasses)
    - Enums (BaseCommonEnum subclasses)
    - Custom converters via field metadata
    """

    def decorator(cls: t.Type) -> t.Type:
        # Apply @dataclass if not already applied
        # Check if __dataclass_fields__ is in the class's own __dict__, not inherited
        if "__dataclass_fields__" not in cls.__dict__:
            cls = dataclass(cls, **dataclass_kwargs)

        field_infos = _get_class_field_infos(cls)

        # Generate and attach from_proto method
        cls.from_proto = _create_from_proto_method(field_infos)  # ty: ignore[invalid-assignment]

        # Generate and attach to_proto method
        cls.to_proto = _create_to_proto_method(field_infos, proto_cls)  # ty: ignore[invalid-assignment]

        return cls

    return decorator


def _get_class_field_infos(cls: t.Type) -> t.List[FieldInfo]:
    """Helper to get dataclass fields and their type hints."""
    type_hints = t.get_type_hints(cls, localns={cls.__name__: cls})
    return [FieldInfo.from_field(f, type_hints) for f in fields(cls)]


def _create_from_proto_method(field_infos: t.List[FieldInfo]) -> t.Any:
    def from_proto_func(cls: t.Type, proto: t.Any) -> t.Any:
        kwargs = {
            field_info.name: _convert_from_proto_field(proto, field_info)
            for field_info in field_infos
        }
        return cls(**kwargs)

    return classmethod(from_proto_func)


def _create_to_proto_method(
    field_infos: t.List[FieldInfo],
    proto_cls: t.Type,
) -> t.Callable:
    def to_proto_func(self: t.Any) -> t.Any:
        kwargs = {}
        for field in field_infos:
            self_value = getattr(self, field.name)

            # Convert the field value
            proto_value = _convert_to_proto_field(self_value, field)
            if proto_value is not None:
                kwargs[field.name] = proto_value

        return proto_cls(**kwargs)

    return to_proto_func


def _convert_from_proto_field(proto: Message, field: FieldInfo) -> t.Any:
    """Execute the conversion logic for a single field from proto to dataclass."""
    proto_value = getattr(proto, field.name)

    if field.from_proto_converter:
        return field.from_proto_converter(proto_value)

    if field.is_optional:
        if not proto.HasField(field.name):
            return None
        return _convert_from_proto_field(proto, field.create_inner_field_info())

    outer_type = field.outer_type
    inner_types = field.inner_types

    if outer_type is list:
        return [_value_from_proto(inner_types[0], x) for x in proto_value]

    if outer_type is set:
        return {_value_from_proto(inner_types[0], x) for x in proto_value}

    if outer_type is dict:
        return {
            _value_from_proto(inner_types[0], key): _value_from_proto(inner_types[1], value)
            for key, value in proto_value.items()
        }

    return proto_value


def _convert_to_proto_field(value: t.Any, field: FieldInfo) -> t.Any:
    if value is None:
        return None

    if field.to_proto_converter:
        return field.to_proto_converter(value)

    if field.is_optional:
        return _convert_to_proto_field(value, field.create_inner_field_info())

    outer_type = field.outer_type
    if outer_type in (list, set):
        return [_value_to_proto(x) for x in value]

    if outer_type is dict:
        return {_value_to_proto(key): _value_to_proto(item) for key, item in value.items()}

    return value


def _value_from_proto(field_type: t.Any, value: t.Any) -> t.Any:
    return field_type.from_proto(value) if hasattr(field_type, "from_proto") else value


def _value_to_proto(value: t.Any) -> t.Any:
    return value.to_proto() if hasattr(value, "to_proto") else value


def proto_enum(proto_enum_cls: t.Type) -> t.Callable[[t.Type[enum.Enum]], t.Type[enum.Enum]]:
    """
    Decorator that auto-generates from_proto() and to_proto() methods for enums.

    Introspects both Python enum and proto enum to build bidirectional mappings,
    eliminating manual mapping dictionaries.

    Args:
        proto_enum_cls: The protobuf enum class corresponding to this enum.
                       Example: shared_pb2.ModelExecutionType

    Usage:
        @proto_enum(shared_pb2.ModelExecutionType)
        class ModelExecutionType(BaseCommonEnum):
            FULL = "FULL"
            APPEND = "APPEND"
            # ... other values - no from_proto/to_proto needed!

    The decorator:
    - Validates that Python enum names match proto enum names
    - Builds bidirectional int <-> enum mappings
    - Generates from_proto() classmethod and to_proto() instance method
    - Handles errors with informative messages
    """

    def decorator(enum_cls: t.Type[enum.Enum]) -> t.Type[enum.Enum]:
        # Build bidirectional mappings
        from_proto_map, to_proto_map = _build_enum_mappings(enum_cls, proto_enum_cls)

        # Generate and attach from_proto method
        from_proto_method = _create_enum_from_proto_method(proto_enum_cls, from_proto_map)
        enum_cls.from_proto = from_proto_method  # ty: ignore[unresolved-attribute]

        # Generate and attach to_proto method
        to_proto_method = _generate_enum_to_proto_method(to_proto_map)
        enum_cls.to_proto = to_proto_method  # ty: ignore[unresolved-attribute]

        return enum_cls

    return decorator


def _build_enum_mappings(
    python_enum_cls: t.Type[enum.Enum],
    proto_enum_cls: t.Type,
) -> tuple[t.Dict[int, enum.Enum], t.Dict[enum.Enum, int]]:
    """
    Build bidirectional mappings between Python enum and proto enum.

    Returns:
        Tuple of (from_proto_map, to_proto_map):
        - from_proto_map: {proto_int_value: python_enum_instance}
        - to_proto_map: {python_enum_instance: proto_int_value}

    Raises:
        ValueError: If Python enum has values not in proto enum, or vice versa
    """
    from_proto_map = {}
    to_proto_map = {}

    # Get proto enum names and their integer values
    # proto_enum_cls.items() returns [('FULL', 1), ('APPEND', 2), ...]
    proto_enum_items = dict(proto_enum_cls.items())  # ty: ignore[unresolved-attribute]

    # Track which proto enum values have been mapped
    mapped_proto_names = set()

    # Iterate through Python enum members
    for python_enum_member in python_enum_cls:
        python_name = python_enum_member.name

        if python_name == "_UNSUPPORTED":
            continue

        # Validate that Python enum name exists in proto enum
        if python_name not in proto_enum_items:
            proto_enum_name = getattr(proto_enum_cls, "_enum_type", proto_enum_cls).name  # ty: ignore[unresolved-attribute]
            raise ValueError(
                f"Python enum {python_enum_cls.__name__}.{python_name} "
                f"does not have a corresponding proto enum value in {proto_enum_name}. "
                f"Available proto enum names: {sorted(proto_enum_items.keys())}"
            )

        # Get proto integer value for this name
        proto_int_value = proto_enum_items[python_name]

        # Track that we've mapped this proto name
        mapped_proto_names.add(python_name)

        # Build bidirectional mappings
        from_proto_map[proto_int_value] = python_enum_member
        to_proto_map[python_enum_member] = proto_int_value

    # Validate that all proto enum values are mapped (Proto → Python)
    unmapped_proto_names = set(proto_enum_items.keys()) - mapped_proto_names
    if unmapped_proto_names:
        proto_enum_name = getattr(proto_enum_cls, "_enum_type", proto_enum_cls).name  # ty: ignore[unresolved-attribute]
        raise ValueError(
            f"Proto enum {proto_enum_name} has values not defined in Python enum {python_enum_cls.__name__}: "
            f"{sorted(unmapped_proto_names)}. "
            f"All proto enum values must have corresponding Python enum members."
        )

    return from_proto_map, to_proto_map


def _create_enum_from_proto_method(
    proto_enum_cls: t.Type,
    from_proto_map: t.Dict[int, enum.Enum],
) -> t.Any:
    """
    Generate from_proto classmethod using closures.

    Returns:
        A classmethod that converts proto int values to Python enum instances
    """

    def from_proto_func(cls_inner: t.Type[enum.Enum], proto_value: int) -> enum.Enum:
        """Convert protobuf enum value to Python enum instance."""
        try:
            return from_proto_map[proto_value]
        except KeyError as e:
            if hasattr(cls_inner, "_UNSUPPORTED"):
                return cls_inner._UNSUPPORTED  # ty: ignore[invalid-return-type]  # noqa: SLF001
            valid_values = sorted(from_proto_map.keys())
            proto_enum_name = getattr(proto_enum_cls, "_enum_type", proto_enum_cls).name  # ty: ignore[unresolved-attribute]
            raise ValueError(
                f"Invalid proto enum value {proto_value} for {proto_enum_name}. "
                f"Valid values: {valid_values}"
            ) from e

    return classmethod(from_proto_func)


def _generate_enum_to_proto_method(
    to_proto_map: t.Dict[enum.Enum, int],
) -> t.Callable:
    """
    Generate to_proto instance method using closures.

    Returns:
        An instance method that converts Python enum to proto int value
    """

    def to_proto_func(self: enum.Enum) -> int:
        """Convert Python enum instance to protobuf enum value."""
        try:
            return to_proto_map[self]
        except KeyError as e:
            raise ValueError(
                f"Invalid enum instance {self} for conversion to proto. "
                f"This indicates a bug in the proto_enum decorator."
            ) from e

    return to_proto_func
