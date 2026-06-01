#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""Update mappings for all record classes in the service registry."""

from __future__ import annotations

from typing import TYPE_CHECKING

from invenio_records_resources.services.records import (
    RecordService,
    RecordServiceConfig,
)

from oarepo_runtime import current_runtime
from oarepo_runtime.records.mapping import update_record_system_fields_mapping

if TYPE_CHECKING:
    from invenio_records_resources.services.base import Service


def update_all_records_mappings() -> None:
    """Update all mappings for the registered record classes."""
    service: Service
    for service in current_runtime.services.values():
        if not isinstance(service, RecordService):
            continue

        config: RecordServiceConfig = service.config

        record_class = getattr(config, "record_cls", None)
        if record_class:
            update_record_system_fields_mapping(record_class)

        draft_class = getattr(config, "draft_cls", None)
        if draft_class:
            update_record_system_fields_mapping(draft_class)
