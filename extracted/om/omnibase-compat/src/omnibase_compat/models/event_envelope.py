# SPDX-FileCopyrightText: 2025 OmniNode.ai Inc.
# SPDX-License-Identifier: MIT
# COMPAT_MIGRATION_TARGET: omnibase_core.models.event_envelope
# COMPAT_REMOVAL_DATE: 2026-10-01

import uuid
from typing import Any

from pydantic import BaseModel, Field


class EventEnvelopeV1Minimal(BaseModel, frozen=True):
    """Minimal shared transport envelope for cross-repo event compatibility.

    Intentionally narrow. Does not include timestamp, source, trace_id,
    correlation_id, or category. Add those in a versioned successor or
    additive minor release once real usage patterns are established.
    """

    event_id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    event_type: str
    payload: dict[str, Any] = Field(default_factory=dict)
    # string-version-ok: wire schema guard; compat has zero runtime deps, ModelSemVer unavailable
    schema_version: str = "1.0"
    data_provenance: str | None = Field(
        default=None,
        description=(
            "Data provenance label. Expected values: "
            '"demo_seeded", "demo_projected_shortcut", "measured", "estimated", "unknown". '
            "Uses str (not enum) because omnibase_compat has zero upstream runtime deps."
        ),
    )
