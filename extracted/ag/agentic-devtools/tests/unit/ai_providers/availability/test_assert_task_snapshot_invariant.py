import pytest

from agentic_devtools.ai_providers.availability import assert_task_snapshot_invariant
from agentic_devtools.ai_providers.errors import ProviderError


def test_assert_task_snapshot_invariant_allows_zero_delta() -> None:
    result = assert_task_snapshot_invariant(
        {"tasks": [{"id": "task-1"}, {"id": "task-2"}]},
        {"task_ids": ["task-1", "task-2"]},
    )

    assert result["task_count_delta"] == 0
    assert result["task_ids_before"] == ["task-1", "task-2"]
    assert result["task_ids_after"] == ["task-1", "task-2"]

    assert assert_task_snapshot_invariant({"id": "task-1"}, {"id": "task-1"}) == {
        "task_count_delta": 0,
        "task_ids_before": ["task-1"],
        "task_ids_after": ["task-1"],
        "new_task_ids": [],
    }
    assert assert_task_snapshot_invariant({"tasks": ["task-1"]}, {"tasks": ["task-1"]}) == {
        "task_count_delta": 0,
        "task_ids_before": ["task-1"],
        "task_ids_after": ["task-1"],
        "new_task_ids": [],
    }
    assert assert_task_snapshot_invariant({}, {}) == {
        "task_count_delta": 0,
        "task_ids_before": [],
        "task_ids_after": [],
        "new_task_ids": [],
    }
    assert assert_task_snapshot_invariant("task-1", "task-1") == {
        "task_count_delta": 0,
        "task_ids_before": ["task-1"],
        "task_ids_after": ["task-1"],
        "new_task_ids": [],
    }


def test_assert_task_snapshot_invariant_rejects_new_task_id() -> None:
    with pytest.raises(ProviderError, match="Task snapshot invariant violated"):
        assert_task_snapshot_invariant(
            {"tasks": [{"id": "task-1"}]},
            {"tasks": [{"id": "task-1"}, {"id": "task-2"}]},
        )


def test_assert_task_snapshot_invariant_rejects_invalid_payload() -> None:
    with pytest.raises(ProviderError, match="Snapshot payload must be a mapping or sequence of task ids"):
        assert_task_snapshot_invariant(123, 456)  # type: ignore[arg-type]


def test_assert_task_snapshot_invariant_rejects_duplicate_task_ids() -> None:
    with pytest.raises(ProviderError, match="duplicate task id 'task-1'"):
        assert_task_snapshot_invariant(
            {"tasks": ["task-1"]},
            {"tasks": ["task-1", "task-1"]},
        )

    with pytest.raises(ProviderError, match="duplicate task id 'task-1'"):
        assert_task_snapshot_invariant(
            {"task_ids": ["task-1", "task-1"]},
            {"task_ids": ["task-1"]},
        )


@pytest.mark.parametrize(
    ("before_payload", "after_payload", "error"),
    [
        ({"id": 123}, {"id": 123}, "Snapshot task id must be a non-empty string"),
        ({"id": ""}, {"id": ""}, "Snapshot task id must be a non-empty string"),
        ({"tasks": [{"id": "task-1"}]}, {"tasks": [{"name": "task-1"}]}, "must contain a non-empty string 'id'"),
        ({"tasks": ["task-1"]}, {"tasks": [123]}, "must be task-id strings or mappings"),
        ({"tasks": ["task-1"]}, {"tasks": [""]}, "must be non-empty task-id strings"),
        ({"tasks": [{"id": "task-1"}]}, {"tasks": [{"id": ""}]}, "must contain a non-empty string 'id'"),
        ({"tasks": None}, {"tasks": None}, "'tasks' key is present but null"),
        ({"task_ids": None}, {"task_ids": None}, "'task_ids' key is present but null"),
        ({"tasks": [{"id": "task-1"}, {"id": "task-1"}]}, {}, "duplicate task id 'task-1'"),
        # Non-empty mappings with no recognised task key must be rejected; silently
        # treating them as empty would let error payloads like {"error": "unauthorized"}
        # produce equal pre/post snapshots and pass the invariant without real data.
        ({"error": "unauthorized"}, {"error": "unauthorized"}, "Snapshot mapping must contain"),
        ({"message": "rate limited"}, {"message": "rate limited"}, "Snapshot mapping must contain"),
        # Empty top-level string must be rejected so malformed snapshots are never
        # certified as zero-delta without a real task ID having been observed.
        ("", "", "Snapshot task id string must be non-empty"),
    ],
)
def test_assert_task_snapshot_invariant_rejects_malformed_task_entries(
    before_payload: object,
    after_payload: object,
    error: str,
) -> None:
    with pytest.raises(ProviderError, match=error):
        assert_task_snapshot_invariant(before_payload, after_payload)
