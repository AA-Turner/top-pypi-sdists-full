#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see https://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Base typed system field implementation."""

from __future__ import annotations

from typing import Any, Self, overload

from invenio_records.api import Record
from invenio_records.extensions import ExtensionMixin
from invenio_records.systemfields import SystemField


class TypedSystemField[R: Record = Record, V: Any = Any](SystemField, ExtensionMixin):
    """Base class for typed system fields."""

    @overload
    def __get__(self, instance: None, owner: type[R]) -> Self: ...

    @overload
    def __get__(self, instance: R, owner: type[R]) -> V: ...

    def __get__(self, instance: R | None, owner: type[R]) -> Self | V:  # type: ignore[override]
        """Get the value of the field."""
        if instance is None:  # pragma: no cover
            return self  # pragma: no cover
        raise NotImplementedError  # pragma: no cover

    @overload
    def __set__(self, instance: None, value: Self) -> None: ...

    @overload
    def __set__(self, instance: R, value: V) -> None: ...

    def __set__(self, instance: R | None, value: V | Self) -> None:  # type: ignore[override]
        """Set the value of the field."""
        if instance is None:  # pragma: no cover
            raise ValueError("Cannot set value on class.")  # pragma: no cover
        raise NotImplementedError  # pragma: no cover
