"""Safe compile-time config validation diagnostics.

Invalid drafts are returned to the author as field-level validation issues.
This module emits one structured warning with identity and error-type metadata,
without logging authored values or schema payloads.
"""

from __future__ import annotations

import logging
from typing import Any

from pydantic import BaseModel, ValidationError


logger = logging.getLogger(__name__)


# --- THE INPUT-NOT-CONFIG HINT (W68, 2026-09-12) --------------------------
# A node's INPUTS and its CONFIG are two different objects on ``data``, and a
# closed config schema answers a misplaced input with nothing but "Extra
# inputs are not permitted". The Masterwork Conductor read that literally and
# DELETED ``model`` / ``user_input`` / ``system_instruction`` / ``tools`` /
# ``max_iterations`` from an ``ai.chat.manual`` node one key at a time
# until the node had no inputs at all — the save then passed and the run died
# at step 1 with missing_input on ``model`` (workflow 805c1a98). The rejection
# must say WHERE the key belongs, at the one place every caller reads.
def config_extra_is_input_hint(
    *,
    key: str,
    spec_type: str,
    input_schema: type[BaseModel] | None,
    config_schema: type[BaseModel] | None,
) -> str | None:
    """Sentence to append when a rejected config key is really an INPUT.

    Returns None when the key is not a declared field of the node's
    ``input_schema`` (an ordinary typo — the existing message stands)."""
    if input_schema is None or not key:
        return None
    if key not in input_schema.model_fields:
        return None
    hint = (
        f"'{key}' is an INPUT of {spec_type}, not config — put it under "
        f"data.inputs (or wire an edge that supplies it). Deleting it makes "
        f"the save pass and the run fail at this step."
    )
    if config_schema is not None:
        try:
            accepted = sorted((config_schema.model_json_schema().get("properties") or {}).keys())
        except Exception:  # noqa: BLE001 — a schema that won't render adds no hint
            accepted = []
        if accepted:
            hint += f" Accepted config keys for {spec_type}: {', '.join(accepted)}."
        else:
            hint += f" {spec_type} accepts no config keys at all."
    return hint


def scream_node_config_rejected(
    *,
    node_id: str,
    spec_type: str,
    config_schema: type[BaseModel],
    raw_config: dict[str, Any],
    node_data: dict[str, Any],
    validation_error: ValidationError,
    input_schema: type[BaseModel] | None = None,
) -> None:
    # An incomplete draft is an expected authoring state: save returns the
    # per-field validation issue and publish/run refuse it. Emit one safe,
    # queryable warning rather than five ERROR records containing the authored
    # payload or schema. The raw arguments remain in this boundary's signature
    # so callers and validation behavior stay unchanged, but are never logged.
    _ = config_schema, raw_config, node_data, input_schema
    field_errors = [
        {
            "field": ".".join(str(part) for part in error.get("loc") or ()) or "<root>",
            "error_type": str(error.get("type") or "unknown"),
        }
        for error in validation_error.errors()
    ]
    logger.warning(
        "workflow_config_invalid",
        extra={
            "event": "workflow_config_invalid",
            "node_id": node_id,
            "spec_type": spec_type,
            "field_errors": field_errors,
        },
    )
