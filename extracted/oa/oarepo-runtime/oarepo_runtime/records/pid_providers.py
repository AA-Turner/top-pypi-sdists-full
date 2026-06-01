#
# Copyright (c) 2025 CESNET z.s.p.o.
#
# This file is a part of oarepo-runtime (see http://github.com/oarepo/oarepo-runtime).
#
# oarepo-runtime is free software; you can redistribute it and/or modify it
# under the terms of the MIT License; see LICENSE file for more details.
#
"""PID providers."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, Self, cast

from invenio_pidstore.models import PersistentIdentifier, PIDStatus

if TYPE_CHECKING:
    from invenio_pidstore.providers.recordid_v2 import RecordIdProviderV2
else:
    RecordIdProviderV2 = object


class UniversalPIDMixin(RecordIdProviderV2):
    """Mixin class to handle creation and management of universal PIDs for records."""

    unpid_pid_type = "recid"
    """Setting this to recid so that RDM can use it."""
    unpid_default_status = PIDStatus.REGISTERED

    @classmethod
    def create(  # type: ignore[override] # as pid type and value are given
        cls,
        object_type: str | None = None,
        object_uuid: str | None = None,
        options: dict | None = None,
        **kwargs: Any,
    ) -> Self:
        """Create PID for a given object and store it."""
        pid = cast(
            "Self",
            super().create(
                object_type=object_type,
                object_uuid=object_uuid,
                options=options,
                **kwargs,
            ),
        )
        if pid.pid.pid_value is None:
            raise ValueError("PID value cannot be None.")  # pragma: no cover

        PersistentIdentifier.create(
            cls.unpid_pid_type,
            cast("str", pid.pid.pid_value),
            pid_provider=None,
            object_type=object_type,
            object_uuid=object_uuid,
            status=cls.unpid_default_status,
        )
        return pid
