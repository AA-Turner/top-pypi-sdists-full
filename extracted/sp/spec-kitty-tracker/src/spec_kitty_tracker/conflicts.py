from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import StrEnum
from typing import Any

from spec_kitty_tracker.policy import FieldOwner


class ConflictStrategy(StrEnum):
    EXTERNAL_WINS = "external_wins"
    LOCAL_WINS = "local_wins"
    NEWER_TIMESTAMP = "newer_timestamp"
    MANUAL_REVIEW = "manual_review"


@dataclass(frozen=True, slots=True)
class ConflictRecord:
    field_name: str
    local_value: Any
    external_value: Any
    resolved_value: Any
    strategy: ConflictStrategy
    manual_review_required: bool = False


@dataclass(frozen=True, slots=True)
class FieldResolution:
    value: Any
    conflict: ConflictRecord | None


def _prefer_newer(
    local_value: Any,
    external_value: Any,
    local_updated_at: datetime | None,
    external_updated_at: datetime | None,
) -> Any:
    if local_updated_at is None and external_updated_at is None:
        return external_value
    if local_updated_at is None:
        return external_value
    if external_updated_at is None:
        return local_value
    if external_updated_at >= local_updated_at:
        return external_value
    return local_value


def resolve_field(
    *,
    field_name: str,
    owner: FieldOwner,
    local_value: Any,
    external_value: Any,
    local_updated_at: datetime | None,
    external_updated_at: datetime | None,
    strategy: ConflictStrategy,
) -> FieldResolution:
    if local_value == external_value:
        return FieldResolution(value=local_value, conflict=None)

    if owner is FieldOwner.LOCAL:
        return FieldResolution(value=local_value, conflict=None)

    if owner is FieldOwner.EXTERNAL:
        return FieldResolution(value=external_value, conflict=None)

    manual_review_required = False
    if strategy is ConflictStrategy.EXTERNAL_WINS:
        resolved = external_value
    elif strategy is ConflictStrategy.LOCAL_WINS:
        resolved = local_value
    elif strategy is ConflictStrategy.NEWER_TIMESTAMP:
        resolved = _prefer_newer(
            local_value,
            external_value,
            local_updated_at,
            external_updated_at,
        )
    else:
        resolved = local_value
        manual_review_required = True

    conflict = ConflictRecord(
        field_name=field_name,
        local_value=local_value,
        external_value=external_value,
        resolved_value=resolved,
        strategy=strategy,
        manual_review_required=manual_review_required,
    )
    return FieldResolution(value=resolved, conflict=conflict)
