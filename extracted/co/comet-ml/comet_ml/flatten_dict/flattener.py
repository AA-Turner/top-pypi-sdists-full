# -*- coding: utf-8 -*-
# *******************************************************
#   ____                     _               _
#  / ___|___  _ __ ___   ___| |_   _ __ ___ | |
# | |   / _ \| '_ ` _ \ / _ \ __| | '_ ` _ \| |
# | |__| (_) | | | | | |  __/ |_ _| | | | | | |
#  \____\___/|_| |_| |_|\___|\__(_)_| |_| |_|_|
#
#  Sign up for free at https://www.comet.com
#  Copyright (C) 2015-2023 Comet ML INC
#  This source code is licensed under the MIT license.
# *******************************************************
from collections.abc import Mapping
from typing import Any, Dict, Optional

from comet_ml.flatten_dict.key_reducer import make_reducer

PARAMETERS_DELIMITER = "|"
PARAMETERS_MAX_DEPTH = 10
METRICS_DELIMITER = "/"
METRICS_MAX_DEPTH = 1000


class FlattenDictionaryOpResult:
    def __init__(
        self, d: Dict[str, Any], max_depth_limit_reached: bool, max_depth: int
    ):
        self.flattened = d
        self.max_depth_limit_reached = max_depth_limit_reached
        self.max_depth = max_depth

    def has_nested_dictionary(self):
        return self.max_depth > 1


class _FlattenFrame:
    """One level of the traversal in FlattenDictionaryOp._flatten."""

    __slots__ = ("mapping", "items", "depth", "parent_key", "flat_key", "has_items")

    def __init__(
        self,
        mapping: Mapping,
        depth: int,
        parent_key: Optional[str],
        flat_key: Optional[str],
    ):
        self.mapping = mapping
        self.items = iter(mapping.items())
        self.depth = depth
        self.parent_key = parent_key
        # the key this mapping itself would be stored under, None for the outermost one
        self.flat_key = flat_key
        # whether the mapping yielded any item at all, nested or scalar
        self.has_items = False


class FlattenDictionaryOp:
    def __init__(
        self,
        separator: str,
        max_depth_limit: int = 10,
    ):
        self.flattened_dict = dict()
        self.reducer = make_reducer(separator)
        self.max_depth_limit = max_depth_limit
        self.max_depth_reached = False
        self.max_depth = 0

    def flatten(
        self, d: Dict[str, Any], parent_key: Optional[str] = None
    ) -> FlattenDictionaryOpResult:
        self._flatten(d, depth=1, parent_key=parent_key)

        return FlattenDictionaryOpResult(
            d=self.flattened_dict,
            max_depth_limit_reached=self.max_depth_reached,
            max_depth=self.max_depth,
        )

    def _flatten(
        self,
        d: Mapping,
        depth: int,
        parent_key: Optional[str],
    ) -> bool:
        """Flattens ``d`` depth-first, using an explicit stack rather than recursion.

        ``max_depth_limit`` is as high as 1000 for metrics, which is at CPython's default
        recursion limit, so recursing once per level raised RecursionError instead of
        reporting that the limit was reached."""
        root = _FlattenFrame(
            mapping=d, depth=depth, parent_key=parent_key, flat_key=None
        )
        stack = [root]

        while stack:
            frame = stack[-1]

            try:
                key, value = next(frame.items)
            except StopIteration:
                self.max_depth = max(self.max_depth, frame.depth)
                stack.pop()
                # an empty mapping is not a node, so it is stored as a plain value, the
                # same way the recursive version stored it when _flatten returned False
                if not frame.has_items and frame.flat_key is not None:
                    self._store(frame.flat_key, frame.mapping)
                continue

            frame.has_items = True
            flat_key = self.reducer(frame.parent_key, key)

            if isinstance(value, Mapping):
                if frame.depth < self.max_depth_limit:
                    stack.append(
                        _FlattenFrame(
                            mapping=value,
                            depth=frame.depth + 1,
                            parent_key=flat_key,
                            flat_key=flat_key,
                        )
                    )
                    continue
                else:
                    self.max_depth_reached = True

            self._store(flat_key, value)

        return root.has_items

    def _store(self, flat_key: str, value: Any) -> None:
        if flat_key in self.flattened_dict:
            raise ValueError("duplicated key '{}'".format(flat_key))
        self.flattened_dict[flat_key] = value


def flatten_dict(
    d: Dict[str, Any],
    separator: str,
    max_depth: int = 10,
    parent_key: Optional[str] = None,
) -> FlattenDictionaryOpResult:
    if not isinstance(d, Mapping):
        raise ValueError("argument type %s is not a Mapping" % type(d))

    if max_depth < 1:
        raise ValueError("max_depth should not be less than 1.")

    flatten_op = FlattenDictionaryOp(separator=separator, max_depth_limit=max_depth)
    return flatten_op.flatten(d, parent_key=parent_key)
