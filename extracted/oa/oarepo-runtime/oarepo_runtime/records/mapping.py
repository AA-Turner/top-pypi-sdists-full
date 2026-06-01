#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Module to update the mapping of system fields in a record class."""

from __future__ import annotations

import inspect
from collections.abc import Iterable
from typing import TYPE_CHECKING, Any

from invenio_search import current_search_client
from invenio_search.engine import dsl
from invenio_search.utils import build_alias_name

from oarepo_runtime.records.systemfields.mapping import MappingSystemFieldMixin

if TYPE_CHECKING:
    from collections.abc import Iterable

    from invenio_records.api import RecordBase


def prefixed_index(index: dsl.Index) -> dsl.Index:
    """Return a prefixed index for the given index."""
    return dsl.Index(
        build_alias_name(
            index._name,  # noqa: SLF001
        ),
        using=current_search_client,  # pyright: ignore[reportArgumentType]
    )


def update_record_system_fields_mapping(record_class: type[RecordBase]) -> None:
    """Update mapping for system fields in the record class.

    :param record_class: The record class which index mapping should be updated.
    :raise search.RequestError: If there is an error while updating the mapping.
    """
    index = getattr(record_class, "index", None)
    if not index:
        return

    for fld in get_mapping_fields(record_class):
        # get mapping
        mapping = fld.mapping
        settings = fld.mapping_settings
        dynamic_templates = fld.dynamic_templates

        # upload mapping
        update_record_index(prefixed_index(index), settings, mapping, dynamic_templates)


def update_record_index(
    record_index: dsl.Index,
    settings: dict,
    mapping: dict,
    dynamic_templates: list | None = None,
) -> None:
    """Update the index mapping for the given record index."""
    if settings:
        record_index.close()
        record_index.put_settings(body=settings)
        record_index.open()

    body: dict[str, Any] = {}
    if mapping:
        body["properties"] = mapping
    if dynamic_templates:
        body["dynamic_templates"] = dynamic_templates
    if body:
        record_index.put_mapping(body=body)


def get_mapping_fields(
    record_class: type[RecordBase],
) -> Iterable[MappingSystemFieldMixin]:
    """Get all mapping fields from the record class."""
    return (attr for _, attr in inspect.getmembers(record_class, lambda x: isinstance(x, MappingSystemFieldMixin)))
