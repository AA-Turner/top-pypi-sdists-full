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
from typing import TYPE_CHECKING

from flask import current_app
from invenio_records.systemfields.relations import MultiRelationsField
from invenio_vocabularies.records.systemfields.relations import CustomFieldsRelation

from oarepo_runtime.records.mapping import prefixed_index, update_record_index

if TYPE_CHECKING:
    from collections.abc import Iterable

    from invenio_records.api import RecordBase


def update_record_system_fields_mapping_relation_field(
    record_class: type[RecordBase],
) -> None:
    """Update mapping for system fields in the record class.

    :param record_class: The record class which index mapping should be updated.
    :raise search.RequestError: If there is an error while updating the mapping.
    """
    index = getattr(record_class, "index", None)
    if not index:
        return

    for field_name, fld in get_mapping_relation_fields(record_class):
        custom_fields = current_app.config.get(fld._fields_var, [])  # noqa: SLF001

        props: dict[str, dict] = {}
        mapping = {field_name: {"type": "object", "properties": props}}
        for cf in custom_fields:
            # get mapping
            props[cf.name] = cf.mapping

        # upload mapping
        if props:
            update_record_index(prefixed_index(index), {}, mapping, None)


def get_mapping_relation_fields(
    record_class: type[RecordBase],
) -> Iterable[tuple[str, CustomFieldsRelation]]:
    """Get all mapping fields from the record class."""
    for _, relation_fields in inspect.getmembers(record_class, lambda x: isinstance(x, MultiRelationsField)):
        yield from (
            (field_name, relation_field)
            for field_name, relation_field in relation_fields._original_fields.items()  # noqa: SLF001
            if isinstance(relation_field, CustomFieldsRelation)
        )
