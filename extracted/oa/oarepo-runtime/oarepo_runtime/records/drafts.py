#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Record drafts."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from invenio_drafts_resources.records.api import Record
    from invenio_records.api import Record as RecordBase

from oarepo_runtime.proxies import current_runtime


def has_draft(record: RecordBase) -> bool:
    """Check if record has draft."""
    return get_draft(record) is not None


def get_draft(record: RecordBase) -> RecordBase | None:
    """Get the draft of a published record, if it exists.

    A record can have a draft if:

    - it has a parent record (so, for vocabulary records, this will always be False)
    - if it has a has_draft attribute (that means, it is a published record)
    - the has_draft is True meaning that the record has a draft ('edit metadata' button)
    - if the record has a parent and the parent has a draft (edited 'new version' of the record)
    """
    if getattr(record, "is_draft", False):
        return record
    if not hasattr(record, "parent") or not hasattr(record, "has_draft"):
        return None

    record_service = current_runtime.get_record_service_for_record(record)

    try:
        parent = getattr(record, "parent", None)
        if parent is None:
            return None  # pragma: no cover  # just a safety check, parent should be there
        draft_cls: Record | None = getattr(record_service.config, "draft_cls", None)
        if draft_cls is None:
            return None  # pragma: no cover  # just a safety check, draft_cls should be there

        return next(draft_cls.get_records_by_parent(parent, with_deleted=False))
    except StopIteration:
        # no draft found
        return None
