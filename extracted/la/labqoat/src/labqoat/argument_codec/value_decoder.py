"""Typed reconstruction of authored workflow values."""

from __future__ import annotations

import types
from collections.abc import Mapping
from dataclasses import fields, is_dataclass
from datetime import datetime
from enum import Enum
from typing import Annotated, Any, Literal, Union, cast, get_args, get_origin, get_type_hints
from uuid import UUID

from labqoat.argument_codec.value_encoder import ValueEncoder
from labqoat.json_document import JsonDocument
from labqoat.references import DatasetRef, ResourceId, Sha256
from labqoat.schemas.schema_record import SchemaRecord


class ValueDecoder:
    """Decode dataclasses and references while rejecting lossy conversions."""

    @staticmethod
    def decode(value: object, target: object) -> object:
        """Dispatch scalar, annotated, union, container, and dataclass types."""
        origin = get_origin(target)
        arguments = get_args(target)
        if origin is DatasetRef:
            return ValueDecoder.dataset(value, arguments[0])
        if origin is Annotated:
            return ValueDecoder.decode(value, arguments[0])
        if origin in (Union, types.UnionType):
            return ValueDecoder.union(value, arguments)
        if origin is Literal:
            if value not in arguments:
                raise ValueError("Value does not match a literal")
            return value
        if origin in (list, tuple, dict, Mapping):
            return ValueDecoder.container(value, origin, arguments)
        return ValueDecoder.concrete(value, origin or target)

    @staticmethod
    def dataset(value: object, record_type: object) -> DatasetRef[object]:
        """Restore generated row bindings from an explicit runtime type and retained schema identity."""
        reference = cast(DatasetRef[object], ValueDecoder.concrete(value, DatasetRef))
        if isinstance(record_type, type) and issubclass(record_type, SchemaRecord):
            return reference.bind(record_type)
        return reference

    @staticmethod
    def concrete(value: object, target: object) -> object:
        """Restore identity strings and concrete authored data classes."""
        if target in (ResourceId, Sha256, DatasetRef) and isinstance(value, str):
            reference_type = cast("type[ResourceId | Sha256 | DatasetRef[object]]", target)
            return reference_type.parse(value)
        if target is datetime and isinstance(value, str):
            return datetime.fromisoformat(value)
        if target is UUID and isinstance(value, str):
            return UUID(value)
        if isinstance(target, type) and issubclass(target, SchemaRecord):
            return target.from_dict(JsonDocument.expect_dict(value))
        if isinstance(target, type) and is_dataclass(target):
            return ValueDecoder.dataclass(value, target)
        if isinstance(target, type) and issubclass(target, Enum):
            return target(value)
        return ValueDecoder.scalar(value, target)

    @staticmethod
    def dataclass(value: object, target: type[object]) -> object:
        """Validate field names and reconstruct typed fields with defaults."""
        if not isinstance(value, Mapping):
            raise ValueError(f"Expected an object for {target.__name__}, got {ValueDecoder.described(value)}")
        hints = get_type_hints(target, include_extras=True)
        declared = {item.name for item in fields(cast("type", target)) if item.init}
        if unknown := sorted(set(value) - declared):
            raise ValueError(f"Unknown fields for {target.__name__}: {', '.join(map(str, unknown))}")
        decoded = {name: ValueDecoder.decode(item, hints[name]) for name, item in value.items()}
        return target(**decoded)

    @staticmethod
    def described(value: object) -> str:
        """Name a rejected value briefly enough for one error line."""
        text = repr(value)
        return f"{type(value).__name__} {text if len(text) <= 80 else text[:77] + '...'}"

    @staticmethod
    def union(value: object, targets: tuple[object, ...]) -> object:
        """Select the first losslessly matching union member."""
        for target in targets:
            try:
                return ValueDecoder.decode(value, target)
            except (TypeError, ValueError):
                continue
        raise ValueError("Value does not match any declared union member")

    @staticmethod
    def container(value: object, origin: object, arguments: tuple[object, ...]) -> object:
        """Restore recursively typed JSON collections."""
        if origin in (dict, Mapping):
            if not isinstance(value, Mapping):
                raise ValueError("Expected an object")
            key_type, value_type = arguments or (str, object)
            return {
                ValueDecoder.decode(key, key_type): ValueDecoder.decode(item, value_type) for key, item in value.items()
            }
        if not isinstance(value, list | tuple):
            raise ValueError("Expected an array")
        if origin is tuple and arguments and arguments[-1] is not Ellipsis:
            if len(value) != len(arguments):
                raise ValueError("Tuple length does not match the declaration")
            return tuple(ValueDecoder.decode(item, kind) for item, kind in zip(value, arguments, strict=True))
        item_type = arguments[0] if arguments else object
        values = [ValueDecoder.decode(item, item_type) for item in value]
        return tuple(values) if origin is tuple else values

    @staticmethod
    def scalar(value: object, target: object) -> object:
        """Require exact primitive types, allowing integer-to-float widening."""
        if target is Any or target is object:
            return ValueEncoder.encode(value)
        if target is float and type(value) in (int, float):
            return ValueEncoder.scalar(float(cast("int | float", value)))
        if target is type(None) and value is None:
            return None
        if target in (str, int, bool, list, dict, tuple) and type(value) is target:
            return value
        raise ValueError(f"Value does not match {target}")
