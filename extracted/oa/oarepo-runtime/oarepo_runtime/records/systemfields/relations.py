#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see https://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""A relation field that allows arbitrarily nested lists of relations."""

from __future__ import annotations

from itertools import zip_longest
from typing import TYPE_CHECKING, Any, override

from invenio_records.dictutils import dict_lookup, dict_set
from invenio_records.systemfields.relations import (
    InvalidRelationValue,
    ListRelation,
    RelationListResult,
)
from invenio_records_resources.records.systemfields.relations import (
    PIDRelation,
)

if TYPE_CHECKING:
    from collections.abc import Callable, Generator

    from invenio_records.api import Record


class ArbitraryNestedListResult(RelationListResult):
    """Relation access result."""

    @override
    def __call__(self, force: bool = True):
        """Resolve the relation."""
        try:
            # not as efficient as it could be as we create the list of lists first
            # before returning the iterator, but simpler to implement
            return iter(
                _for_each_deep(
                    self._lookup_data(),
                    lambda v: self.resolve(v[self._value_key_suffix]),
                    levels=len(self.field.path_elements),
                )
            )
        except KeyError:
            return None

    def _lookup_data(self) -> Any:
        """Lookup the data from the record."""

        # recursively lookup the data following the path elements. The end of the path
        # must always be an array of objects.
        def _lookup(r: Any, paths: list[str]) -> Any:
            if not paths:
                if self.field.relation_field:
                    try:
                        return dict_lookup(r, self.field.relation_field)
                    except KeyError:  # pragma: no cover
                        return None
                return r
            try:
                level_values = dict_lookup(r, paths[0])
                if not isinstance(level_values, list):
                    raise InvalidRelationValue(  # pragma: no cover
                        f'Invalid structure, expecting list at "{paths[0]}", got {level_values}. '
                        f'Complete paths: "{self.field.path_elements}"'
                    )
                ret = [_lookup(v, paths[1:]) for v in level_values]
                return [v for v in ret if v is not None]
            except KeyError:
                return []

        return _lookup(self.record, self.field.path_elements)

    @override
    def validate(self) -> None:
        """Validate the field."""
        try:
            values = self._lookup_data()
            # not as efficient as it could be as we create the list of lists first
            # before returning, but simpler to implement
            _for_each_deep(
                values,
                self._validate_single_value,
                levels=len(self.field.path_elements),
            )
        except KeyError:  # pragma: no cover
            return

    def _validate_single_value(self, v: Any) -> None:
        """Validate a single value."""
        if isinstance(v, list):
            raise InvalidRelationValue(f"Invalid value {v}, should not be list.")
        relation_id = self._lookup_id(v)
        if not self.exists(relation_id):
            raise InvalidRelationValue(f"Invalid value {relation_id}.")
        if self.value_check:  # pragma: no cover # not testing, copied from invenio
            obj = self.resolve(v[self.field._value_key_suffix])  # noqa: SLF001 # private attr
            self._value_check(self.value_check, obj)

    @override
    def _apply_items(  # type: ignore[override]
        self,
        func: Callable,
        keys: list[str] | None = None,
        attrs: list[str] | None = None,
    ) -> list[Any] | None:
        """Iterate over the list of objects."""
        # The attributes we want to get from the related record.
        attrs = attrs or self.attrs
        keys = keys or self.keys
        try:
            # Get the list of objects we have to dereference/clean.
            values = self._lookup_data()
            return _for_each_deep(
                values,
                lambda v: func(v, keys, attrs),
                levels=len(self.field.path_elements),
            )
        except KeyError:  # pragma: no cover
            return None


class ArbitraryNestedListRelation(ListRelation):
    """Arbitrary nested relation list type.

    self.path_elements contain the segments of the path that are within lists.
    For example:
    - For paths like "a.b.c", path = [], relation_field="a.b.c"
    - For paths like "a.b.0.c", path = ["a.b"], relation_field="c"
    - For paths like "a.0.b.1.c", path = ["a", "b"], relation_field="c"
    - For paths like "a.1", path = ["a"], relation_field=None

    ids and values are stored as lists that can contain other lists arbitrarily nested.
    The total depth of nesting is given by the length of self.path_elements + 1 if self.relation_field is not None
    or length of self.path_elements if self.relation_field is None.
    """

    result_cls = ArbitraryNestedListResult

    def __init__(
        self,
        *args: Any,
        array_paths: list[str] | None = None,
        relation_field: str | None = None,
        **kwargs: Any,
    ):
        """Initialize the relation."""
        if not array_paths:
            raise ValueError("array_paths are required for ArbitraryNestedListRelation.")
        self.path_elements = array_paths
        super().__init__(*args, relation_field=relation_field, **kwargs)

    @override
    def exists_many(self, ids: Any) -> bool:  # type: ignore[override]
        """Return True if all ids exists."""

        # ids is a list that might recursively contain lists that contain ids
        def flatten(nested_list: Any) -> Generator[Any]:
            for item in nested_list:
                if isinstance(item, (list, tuple)):
                    yield from flatten(item)
                else:
                    yield item

        return all(self.exists(i) for i in flatten(ids))

    @override
    def parse_value(self, value: list[Any] | tuple[Any]) -> list[Any]:  # type: ignore[override]
        """Parse a record (or ID) to the ID to be stored."""
        return _for_each_deep(value, self._parse_single_value, levels=len(self.path_elements))

    def _parse_single_value(self, value: Any) -> Any:
        """Parse a single value using the parent class method.

        Note: we are skipping the list's parse_value here and calling
        the next one after ListRelation in mro chain. That might be, for example,
        PIDRelation.parse_value
        """
        if self.relation_field:
            try:
                return super(ListRelation, self).parse_value(dict_lookup(value, self.relation_field))
            except KeyError:  # pragma: no cover
                return None
        else:
            return super(ListRelation, self).parse_value(value)

    @override
    def set_value(
        self,
        record: Record,
        value: list[Any] | tuple[Any],
    ) -> None:  # type: ignore[override]
        """Set the relation value."""
        store_values = self.parse_value(value)

        if not self.exists_many(store_values):
            raise InvalidRelationValue(f'One of the values "{store_values}" is invalid.')

        total_depth = len(self.path_elements)

        for path_indices, path_value in _deep_enumerate(store_values, total_depth):
            r: Any = record
            self._set_value_at_path(r, path_indices, {self._value_key_suffix: path_value})

    def _set_value_at_path(self, r: Any, path_indices: list[int], path_value: Any) -> None:
        """Set the value at the given path indices."""
        pe = [
            *self.path_elements,
        ]
        if self.relation_field:
            pe.append(self.relation_field)

        # pe might be 1 longer than path_indices, that's why we use zip_longest
        zipped = list(zip_longest(pe, path_indices, fillvalue=None))
        for idx, (subpath, index) in enumerate(zipped[:-1]):
            if not subpath:
                raise InvalidRelationValue(  # pragma: no cover
                    f"Invalid structure, missing key at index {idx} in [{self.path_elements}, {path_indices}]."
                )
            if index is None:
                raise InvalidRelationValue(  # pragma: no cover
                    f"Invalid structure, missing index at {subpath} in [{self.path_elements}, {path_indices}]."
                )
            r = self._set_default_value_at_path(r, subpath, index, path_indices)

        last_path, last_index = zipped[-1]
        if last_path is None:  # pragma: no cover
            raise InvalidRelationValue("Implementation error.")
        if last_index is None:
            # we have a relation_field at the end, so set it directly
            dict_set(r, last_path, path_value)
        else:
            # no relation_field at the end, so we set the whole object at the index
            try:
                val = dict_lookup(r, last_path)
            except KeyError:
                val = []
                dict_set(r, last_path, val)
            if last_index < len(val):
                val[last_index] = path_value
            elif last_index == len(val):
                val.append(path_value)
            else:
                raise InvalidRelationValue(  # pragma: no cover # just sanity check
                    f"Invalid structure, missing index {last_index} "
                    f"at {last_path} in [{self.path_elements}, {path_indices}]."
                )

    def _set_default_value_at_path(self, r: Any, subpath: str, index: int, path_indices: list[int]) -> Any:
        """Set default value of [] at the given path if missing."""
        # look up the subpath and create it if missing
        try:
            val = dict_lookup(r, subpath)
        except KeyError:
            dict_set(r, subpath, [])
            val = dict_lookup(r, subpath)
        if not isinstance(val, list):
            raise InvalidRelationValue(  # pragma: no cover
                f"Invalid structure, expecting list at {subpath} in [{self.path_elements}, {path_indices}]."
            )

        # now we have the array - if the index is within array, return the value at the index
        if index < len(val):
            return val[index]

        # if the index is exactly at the end of the array, we can append a new default value,
        # which is always an empty dict
        if index == len(val):
            # append new default value which is always empty dict
            r = {}
            val.append(r)
            return r

        # we can not skip indices, so if that would happen, raise error
        raise InvalidRelationValue(  # pragma: no cover
            f"Invalid structure, missing index {index} at {subpath} in [{self.path_elements}, {path_indices}]."
        )


def _deep_enumerate(nested_list: Any, max_depth: int, depth: int = 0) -> Generator[tuple[list[int], Any]]:
    """Enumerate all non-list items in a nested list structure."""
    for index, item in enumerate(nested_list):
        current_path = [index]
        if depth < max_depth - 1 and isinstance(item, (list, tuple)):
            for sub_path, sub_item in _deep_enumerate(item, max_depth, depth + 1):
                yield current_path + sub_path, sub_item
        else:
            yield current_path, item


def _for_each_deep(nested_list: Any, func: Any, levels: int) -> list[Any]:
    """Apply a function to each non-list item in a nested list structure."""
    result = []
    for item in nested_list:
        if isinstance(item, (list, tuple)) and levels > 1:
            result.append(_for_each_deep(item, func, levels=levels - 1))
        else:
            result.append(func(item))
    return result


class PIDArbitraryNestedListRelation(ArbitraryNestedListRelation, PIDRelation):  # type: ignore[override, misc]
    """PID list relation type."""
