#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Selectors for extracting values from records based on specified paths."""

from __future__ import annotations

from typing import Any, Protocol


class Selector(Protocol):
    """Protocol for selectors that extract values from records."""

    def select(self, record: dict) -> list[Any]:  # noqa: ARG002
        """Select values from the record based on the selector's logic."""
        return []


class PathSelector(Selector):
    """Selector that extracts values from records based on specified paths."""

    def __init__(self, *paths: str) -> None:
        """Initialize the PathSelector with given paths."""
        self.paths = [x.split(".") for x in paths]

    def select(self, record: dict) -> list[Any]:
        """Select values from the record based on the specified paths."""
        ret = []
        for path in self.paths:
            ret.extend(list(getter(record, path)))
        return ret


def getter(data: list | dict, path: list) -> Any:
    """Recursively get values from data based on the provided path."""
    if len(path) == 0:
        if isinstance(data, list):
            yield from data
        else:
            yield data
    elif isinstance(data, dict):
        if path[0] in data:
            yield from getter(data[path[0]], path[1:])
    elif isinstance(data, list):
        for item in data:
            yield from getter(item, path)
