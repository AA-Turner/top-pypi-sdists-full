#!/usr/bin/env python3
# -*- coding:utf-8 -*-

from __future__ import annotations

import sys
from datetime import datetime
from typing import Any, TypeVar, cast, get_args, get_origin, overload

from pendingai.exceptions import TypeValidationError

if sys.version_info.minor < 10:
    from typing import Union as Union
else:
    from types import UnionType as Union  # type: ignore


T = TypeVar("T")


# Additional implicit standard type category casting, validation on some
# types requires unique recursive logic such as annotated mapping and
# sequence types.


T_standard = TypeVar("T_standard", str, int, float, complex, bool, bytes, bytearray)
T_sequence = TypeVar("T_sequence", list, tuple, set, frozenset)
T_datetime = TypeVar("T_datetime", str, float, int, datetime)
T_mapping = TypeVar("T_mapping", bound=dict)


def _cast_value(dtype: type[Any], instance: Any) -> Any:
    if isinstance(instance, dtype):
        return instance
    try:
        return dtype(instance)
    except Exception as e:
        raise TypeValidationError(instance, dtype) from e


def _cast_standard(dtype: type[T_standard], instance: T_standard) -> Any:
    return _cast_value(dtype, instance)


def _cast_sequence(
    dtype: type[T_sequence], instance: T_sequence, v_annotation: Any = None
) -> Any:
    instance = _cast_value(dtype, instance)
    instance = dtype(
        [validate(v_annotation, v) if v_annotation else v for v in instance]
    )
    return instance


def _cast_mapping(
    dtype: type[T_mapping],
    instance: T_mapping,
    k_annotation: Any = None,
    v_annotation: Any = None,
) -> Any:
    instance = _cast_value(dtype, instance)
    instance = dtype(
        {
            validate(k_annotation, k) if k_annotation else k: validate(v_annotation, v)
            if v_annotation
            else v
            for k, v in instance.items()
        }
    )
    return instance


def _cast_datetime(_: type[T_datetime], instance: T_datetime) -> Any:
    if isinstance(instance, str):
        return datetime.fromisoformat(instance.replace("Z", "+00:00"))
    elif isinstance(instance, (int, float)):
        return datetime.fromtimestamp(instance)
    raise TypeError(
        "Cannot implicitly convert datetime from type '%s'." % type(instance).__name__
    )


@overload
def validate(dtype: None, instance: None) -> None: ...
@overload
def validate(dtype: type[T], instance: Any) -> T: ...


def validate(dtype: type[T] | None, instance: Any) -> T | None:
    """
    Validate an object against a data type with strict implicit type-
    casting and validation.

    Args:
        dtype (type[T] | None): The validation type for the an instance
            to be validated against. The type variable supported generic
            annotations and recursive type-validation from implicit
            standard Python types.
        instance (Any): An object instance to validate.

    Raises:
        TypeValidationError: Instance type did not match the required
            validation type. For example, validation of a `None` typed
            instance raises `TypeValidationError` when the instance is
            not `None`. A `Union` validation type may fail implicit type
            validation on all annotations raising `TypeValidationError`.
        TypeError: A mismatch of annotations to standard Python types
            cannot be processed as expected. For example, iterable types
            in Python can have a single annotated type like `list[int]`
            but cannot be annotated with more values. A dictionary can
            only have a key-value mapping such as `dict[str, int]`.
        TypeError: The provided validation type is not supported.

    Returns:
        T: The validated object instance. On success, the data structure
            is implicitly casted to the `typ` argument data type.
    """
    origin_type: Any = get_origin(dtype)
    annotations: tuple[Any, ...] = get_args(dtype)
    dt_validate: type[T] = cast(type[T], dtype if not origin_type else origin_type)

    # Captured type variables which may be aliased, treated the same as
    # an instance of type Any but cannot be used in issubclass.
    if isinstance(dtype, TypeVar):
        return instance

    # None-type validation should return None as the only valid value,
    # if a non-None value is given, an InvalidTypeError is raised.
    if dtype is None or (not origin_type and issubclass(dtype, None.__class__)):
        if instance is not None:
            raise TypeValidationError(instance, None)
        return None  # type: ignore[return-type]

    # Validation of an Any-typed or already valid-typed instance is not
    # required and returns the instance immediately, this requires for
    # there to be no generic type annotations.
    if dt_validate is Any or (not origin_type and isinstance(instance, dtype)):
        return instance  # type: ignore[return-type]

    if dt_validate is Union:
        # Union type handling requires specific logic and at least one
        # type annotation. First iterate over types to see if a standard
        # instance exists, otherwise attempt an implicit cast on each.
        if len(annotations) == 0:
            raise TypeError("Unsupported annotation for a union, needs at least 1 type.")
        for annotation in [annot for annot in annotations if not get_origin(annot)]:
            if isinstance(instance, annotation):
                return instance
        for annotation in annotations:
            try:
                return validate(annotation, instance)
            except Exception:
                pass
        raise TypeValidationError(instance, dtype)

    elif issubclass(dt_validate, (list, tuple, set, frozenset)):
        # Sequence type handling requires an item type annotation or
        # no annotation to perform a simple implicit validation or cast.
        if len(annotations) == 1:
            return _cast_sequence(dt_validate, instance, annotations[0])  # type: ignore
        elif len(annotations) == 0:
            return _cast_sequence(dt_validate, instance)  # type: ignore
        raise TypeError("Unsupported annotation for a sequence, only 1 allowed type.")

    elif issubclass(dt_validate, (dict,)):
        # Mapping type handling requires a key, value pair annotation or
        # no annotation to perform a simple implicit validation or cast.
        if len(annotations) == 2:
            return _cast_mapping(dt_validate, instance, annotations[0], annotations[1])
        elif len(annotations) == 0:
            return _cast_mapping(dt_validate, instance)
        raise TypeError("Unsupported annotation for a mapping, only 2 allowed types.")

    elif issubclass(dt_validate, (datetime,)):
        # Datetime type handling will only accept datetime instances,
        # castable ISO 8601 formatted strings, or numeric POSIX time-
        # stamps to perform an implicit cast.
        return _cast_datetime(dt_validate, instance)

    elif issubclass(dt_validate, (str, int, float, complex, bool, bytes, bytearray)):
        # Standard type handling only allows for direct instance casts
        # using the type constructor for implicit type conversion.
        return _cast_standard(dt_validate, instance)  # type: ignore

    # Any unhandled type-check is treated as an unsupported type and so
    # is a TypeError is raised for a user to handle individually.
    raise TypeError(f"Unsupported validation type: '{dtype.__name__}'.")
