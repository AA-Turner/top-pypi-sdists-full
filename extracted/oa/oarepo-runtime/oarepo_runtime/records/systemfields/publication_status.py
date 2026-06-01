#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Record status module."""

from __future__ import annotations

from typing import TYPE_CHECKING, Self, override

from invenio_records.api import Record

from .base import TypedSystemField
from .mapping import MappingSystemFieldMixin

if TYPE_CHECKING:
    from invenio_records.dumpers import Dumper


class PublicationStatusSystemField(MappingSystemFieldMixin, TypedSystemField[Record, str]):
    """A system field to track the status of a record (either 'draft' or 'published').

    The default key for this field is 'publication_status', but it can be customized.
    """

    def __init__(self, key: str | None = "publication_status"):
        """Initialize the system field with an optional key."""
        super().__init__(key)

    @property
    def mapping(self) -> dict:
        """Return the mapping for the field in the search index."""
        return {
            self.key: {
                "type": "keyword",
            },
        }

    @override
    def post_load(self, record: Record, data: dict, loader: Dumper | None = None) -> None:
        data.pop(self.key, None)

    @override
    def post_dump(self, record: Record, data: dict, dumper: Dumper | None = None) -> None:
        if not self.attr_name:
            raise ValueError(  # pragma: no cover
                "attr_name must be set for PublicationStatusSystemField"
            )
        data[self.key] = getattr(record, self.attr_name)

    @override
    def __get__(self, instance: Record | None, owner: type[Record]) -> Self | str:  # type: ignore[override]
        """Access the attribute."""
        if instance is None:
            return self
        return "draft" if getattr(instance, "is_draft", False) else "published"
