from datetime import datetime, timedelta, timezone

from spec_kitty_tracker.conflicts import ConflictStrategy, resolve_field
from spec_kitty_tracker.policy import FieldOwner


def test_resolve_field_external_owner() -> None:
    resolution = resolve_field(
        field_name="status",
        owner=FieldOwner.EXTERNAL,
        local_value="todo",
        external_value="done",
        local_updated_at=None,
        external_updated_at=None,
        strategy=ConflictStrategy.LOCAL_WINS,
    )
    assert resolution.value == "done"
    assert resolution.conflict is None


def test_resolve_field_newer_timestamp() -> None:
    now = datetime.now(timezone.utc)
    resolution = resolve_field(
        field_name="title",
        owner=FieldOwner.SHARED,
        local_value="old",
        external_value="new",
        local_updated_at=now,
        external_updated_at=now + timedelta(minutes=1),
        strategy=ConflictStrategy.NEWER_TIMESTAMP,
    )
    assert resolution.value == "new"
    assert resolution.conflict is not None
    assert resolution.conflict.manual_review_required is False


def test_resolve_field_manual_review() -> None:
    now = datetime.now(timezone.utc)
    resolution = resolve_field(
        field_name="body",
        owner=FieldOwner.SHARED,
        local_value="local",
        external_value="external",
        local_updated_at=now,
        external_updated_at=now,
        strategy=ConflictStrategy.MANUAL_REVIEW,
    )
    assert resolution.value == "local"
    assert resolution.conflict is not None
    assert resolution.conflict.manual_review_required is True
