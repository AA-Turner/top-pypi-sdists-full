# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Unit tests for regression record comparison (counts, PKs, field values).

Covers the acceptance criteria of the record-comparison wiring: a dropped
record, a missing primary key, and a mutated field value each flip the
verdict to fail; a stream without a primary key falls back to count
comparison.
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

import pytest
from airbyte_protocol.models import (
    AirbyteMessage,
    AirbyteRecordMessage,
    ConfiguredAirbyteCatalog,
)
from airbyte_protocol.models import Type as AirbyteMessageType

from airbyte_ops_mcp.cli.cloud import _compare_read_records
from airbyte_ops_mcp.regression_tests.ci_output import (
    generate_action_test_comparison_report,
)
from airbyte_ops_mcp.regression_tests.models import (
    duplicate_stream_names,
    get_primary_keys_per_stream,
    split_records_per_stream,
)
from airbyte_ops_mcp.regression_tests.regression import (
    check_pk_uniqueness,
    comparators,
    compare_all_records,
    compare_primary_keys,
    normalize_primary_keys,
    run_record_comparisons,
    run_record_comparisons_from_files,
)
from airbyte_ops_mcp.regression_tests.regression.comparators import (
    DEGRADED_EXAMPLE_CAP,
    MAX_EXAMPLE_PKS,
    MAX_SUMMARY_BYTES,
)


def _record(stream: str, data: dict[str, Any]) -> AirbyteMessage:
    return AirbyteMessage(
        type=AirbyteMessageType.RECORD,
        record=AirbyteRecordMessage(stream=stream, data=data, emitted_at=1),
    )


def _records(stream: str, *datas: dict[str, Any]) -> dict[str, list[AirbyteMessage]]:
    return {stream: [_record(stream, data) for data in datas]}


USERS_PKS = {"users": [["id"]]}


# ---------------------------------------------------------------------------
# normalize_primary_keys
# ---------------------------------------------------------------------------


@pytest.mark.unit
@pytest.mark.parametrize(
    "raw,expected",
    [
        pytest.param(None, None, id="none"),
        pytest.param([], None, id="empty"),
        pytest.param(["id"], [["id"]], id="flat"),
        pytest.param([["id"]], [["id"]], id="nested"),
        pytest.param(
            [["location", "id"], "date"],
            [["location", "id"], ["date"]],
            id="mixed",
        ),
    ],
)
def test_normalize_primary_keys(raw: list | None, expected: list | None) -> None:
    assert normalize_primary_keys(raw) == expected


# ---------------------------------------------------------------------------
# check_pk_uniqueness
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_pk_uniqueness_passes_on_unique_pks() -> None:
    records = _records("users", {"id": 1}, {"id": 2})
    result = check_pk_uniqueness(records, USERS_PKS)
    assert result.passed


@pytest.mark.unit
def test_pk_uniqueness_fails_on_duplicate_pks() -> None:
    records = _records("users", {"id": 1}, {"id": 1}, {"id": 2})
    result = check_pk_uniqueness(records, USERS_PKS, version_label="target")
    assert not result.passed
    assert result.stream_results["users"].duplicate_pks == [(1,)]
    assert "target" in result.errors[0]


@pytest.mark.unit
def test_pk_uniqueness_skips_streams_without_pk() -> None:
    records = _records("events", {"id": 1}, {"id": 1})
    result = check_pk_uniqueness(records, {"events": None})
    assert result.passed
    assert result.warnings


@pytest.mark.unit
def test_pk_uniqueness_with_nested_composite_pk() -> None:
    records = _records(
        "readings",
        {"location": {"id": "a"}, "date": "2026-01-01"},
        {"location": {"id": "a"}, "date": "2026-01-01"},
    )
    result = check_pk_uniqueness(records, {"readings": [["location", "id"], ["date"]]})
    assert not result.passed


@pytest.mark.unit
def test_pk_uniqueness_fails_on_records_missing_pk_values() -> None:
    # An absent PK field and an explicit null are equally unusable: the
    # catalog declares a PK that is not present on the record data.
    records = _records("users", {"id": None, "name": "a"}, {"name": "b"})
    result = check_pk_uniqueness(records, USERS_PKS, version_label="control")

    assert not result.passed
    stream_result = result.stream_results["users"]
    assert stream_result.records_missing_pk == 2
    # Records without a PK are not reported as duplicates of each other.
    assert stream_result.duplicate_pks == []
    assert "missing or null primary key" in result.errors[0]
    assert "declared in the catalog" in result.errors[0]
    assert "control" in result.errors[0]


@pytest.mark.unit
def test_pk_uniqueness_partial_composite_pk_counts_as_missing() -> None:
    records = _records(
        "readings",
        {"location": {"id": "a"}, "date": None},
        {"location": {"id": "b"}, "date": "2026-01-01"},
    )
    result = check_pk_uniqueness(records, {"readings": [["location", "id"], ["date"]]})

    assert not result.passed
    assert result.stream_results["readings"].records_missing_pk == 1


@pytest.mark.unit
def test_pk_uniqueness_reports_duplicates_and_missing_together() -> None:
    records = _records("users", {"id": 1}, {"id": 1}, {"id": None})
    result = check_pk_uniqueness(records, USERS_PKS)

    stream_result = result.stream_results["users"]
    assert stream_result.duplicate_pks == [(1,)]
    assert stream_result.records_missing_pk == 1
    assert len(result.errors) == 2


# ---------------------------------------------------------------------------
# duplicate PK classification: pre-existing / new / fixed
# ---------------------------------------------------------------------------


def _with_duplicates(
    stream: str, duplicated: list[int], unique: list[int] = ()
) -> dict[str, list[AirbyteMessage]]:
    """Records where each `duplicated` id appears twice and each `unique` once."""
    ids = [i for i in duplicated for _ in range(2)] + list(unique)
    return _records(stream, *[{"id": i} for i in ids])


def _split_of(summary: Any, check: str) -> tuple[int, int, int]:
    result = getattr(summary, check).stream_results["users"]
    return (
        result.pre_existing_duplicate_pk_count,
        result.new_duplicate_pk_count,
        result.fixed_duplicate_pk_count,
    )


@pytest.mark.unit
def test_duplicate_pks_are_classified_against_the_other_version() -> None:
    control = _with_duplicates("users", [1, 2, 3], unique=[4, 5])
    target = _with_duplicates("users", [2, 3, 4, 5], unique=[1])

    summary = run_record_comparisons(control, target, USERS_PKS)

    # 2 and 3 are duplicated in both, 4 and 5 in the target only, 1 in the
    # control only; both sides carry the same split.
    assert _split_of(summary, "control_pk_uniqueness") == (2, 2, 1)
    assert _split_of(summary, "target_pk_uniqueness") == (2, 2, 1)
    control_users = summary.control_pk_uniqueness.stream_results["users"]
    target_users = summary.target_pk_uniqueness.stream_results["users"]
    assert control_users.duplicate_pk_count == 3
    assert target_users.duplicate_pk_count == 4
    # Only the target's new duplicates are errors; the rest are the
    # control's warnings, and the target's message names the shared ones.
    pre_existing = (
        "Stream users has 2 pre-existing duplicate primary key value(s), "
        "unchanged between control and target"
    )
    fixed = (
        "Stream users has 1 duplicate primary key value(s) in control fixed in target"
    )
    new = (
        "Stream users has 2 new duplicate primary key value(s) in target "
        "(not duplicated in control)"
    )
    assert summary.errors == [new]
    assert summary.warnings == [pre_existing, fixed]
    assert control_users.message == f"{pre_existing}; {fixed}"
    assert target_users.message == f"{new}; {pre_existing}"
    assert not summary.passed
    assert summary.control_pk_uniqueness.passed
    assert not summary.target_pk_uniqueness.passed


@pytest.mark.unit
def test_identical_duplicates_on_both_sides_pass_with_a_warning() -> None:
    control = _with_duplicates("users", [1, 2])
    target = _with_duplicates("users", [1, 2])

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert _split_of(summary, "target_pk_uniqueness") == (2, 0, 0)
    assert summary.passed
    assert summary.control_pk_uniqueness.passed
    assert summary.target_pk_uniqueness.passed
    assert summary.errors == []
    assert summary.warnings == [
        "Stream users has 2 pre-existing duplicate primary key value(s), "
        "unchanged between control and target"
    ]
    assert summary.control_pk_uniqueness.message == (
        "Pre-existing duplicate primary keys in control (not a regression)"
    )
    assert summary.target_pk_uniqueness.message == (
        "Pre-existing duplicate primary keys in target (not a regression)"
    )


@pytest.mark.unit
def test_a_duplicate_the_target_adds_fails() -> None:
    control = _with_duplicates("users", [1, 2], unique=[3])
    target = _with_duplicates("users", [1, 2, 3])

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert _split_of(summary, "target_pk_uniqueness") == (2, 1, 0)
    assert not summary.passed
    assert summary.control_pk_uniqueness.passed
    assert not summary.target_pk_uniqueness.passed
    assert summary.errors == [
        "Stream users has 1 new duplicate primary key value(s) in target "
        "(not duplicated in control)"
    ]
    assert summary.target_pk_uniqueness.message == (
        "Primary key integrity issues found in target"
    )


@pytest.mark.unit
def test_duplicates_only_the_control_has_pass_as_fixed() -> None:
    control = _with_duplicates("users", [1], unique=[2])
    target = _with_duplicates("users", [], unique=[1, 2, 3])

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert _split_of(summary, "control_pk_uniqueness") == (0, 0, 1)
    assert summary.passed
    assert summary.errors == []
    assert summary.warnings == [
        "Stream users has 1 duplicate primary key value(s) in control fixed in target"
    ]
    assert summary.target_pk_uniqueness.message == (
        "All primary keys unique and present in target"
    )


HOLD = {"id": 7, "event": "T1110"}
RELEASE = {"id": 7, "event": "T1111"}


@pytest.mark.unit
def test_a_control_only_duplicate_with_a_lost_record_is_not_fixed(
    tmp_path: Path,
) -> None:
    """Control `7: hold, release` + `1`, target `7: hold` + `1` + `2`. PK 7
    is no longer duplicated, but the release row is gone: the control row
    says so and points at the field values, which fail; it does not fail
    a second time."""
    control = _records("users", HOLD, RELEASE, {"id": 1})
    target = _records("users", HOLD, {"id": 1}, {"id": 2})

    in_memory = run_record_comparisons(control, target, USERS_PKS)
    from_files = run_record_comparisons_from_files(
        _write_record_files(tmp_path / "control", control),
        _write_record_files(tmp_path / "target", target),
        USERS_PKS,
    )

    assert from_files.to_dict() == in_memory.to_dict()
    for summary in (in_memory, from_files):
        assert not summary.passed
        assert summary.errors == ["Stream users has record differences"]
        assert summary.control_pk_uniqueness.passed
        assert summary.target_pk_uniqueness.passed
        for check in ("control_pk_uniqueness", "target_pk_uniqueness"):
            users = getattr(summary, check).stream_results["users"]
            assert _split_of(summary, check) == (0, 0, 0)
            assert users.lost_duplicate_pk_count == 1
            assert users.lost_duplicate_pks == [(7,)]
        lost = (
            "Stream users has 1 duplicate primary key value(s) in control not "
            "duplicated in target, with records the target dropped or changed; "
            "field values "
            "or PK presence fail on them"
        )
        assert summary.control_pk_uniqueness.warnings == [lost]
        assert "fixed in target" not in " ".join(summary.warnings)
        assert summary.control_pk_uniqueness.message == (
            "Duplicate primary keys in control with records the target dropped "
            "or changed "
            "(field values or PK presence fail on them)"
        )
        assert summary.target_pk_uniqueness.message == (
            "All primary keys unique and present in target"
        )
        assert not summary.field_comparison.passed

    payload = in_memory.to_dict()["checks"]
    for check in ("pk_uniqueness_control", "pk_uniqueness_target"):
        users = payload[check]["streams"]["users"]
        assert users["fixed_duplicate_pk_count"] == 0
        assert users["lost_duplicate_pk_count"] == 1


@pytest.mark.unit
def test_a_pure_collapse_stays_fixed_next_to_a_lost_one() -> None:
    """PK 7 collapses two identical rows (fixed); PK 8 drops a distinct row
    (lost). Each is counted on its own, exactly."""
    control = _records(
        "users", HOLD, HOLD, {"id": 8, "event": "a"}, {"id": 8, "event": "b"}
    )
    target = _records("users", HOLD, {"id": 8, "event": "a"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    users = summary.control_pk_uniqueness.stream_results["users"]
    assert (users.fixed_duplicate_pk_count, users.lost_duplicate_pk_count) == (1, 1)
    assert users.lost_duplicate_pks == [(8,)]
    assert summary.control_pk_uniqueness.message == (
        "Duplicate primary keys in control fixed in target (not a regression); "
        "others with records the target dropped or changed (field values or PK "
        "presence fail "
        "on them)"
    )
    assert not summary.passed

    # A collapse alone is still "fixed", and passes.
    summary = run_record_comparisons(
        _records("users", HOLD, HOLD), _records("users", HOLD), USERS_PKS
    )
    users = summary.control_pk_uniqueness.stream_results["users"]
    assert (users.fixed_duplicate_pk_count, users.lost_duplicate_pk_count) == (1, 0)
    assert summary.passed


@pytest.mark.unit
def test_a_duplicate_the_target_dropped_entirely_or_changed_has_lost_records() -> None:
    # Dropped: PK presence fails on it.
    summary = run_record_comparisons(
        _records("users", HOLD, HOLD, {"id": 1}),
        _records("users", {"id": 1}),
        USERS_PKS,
    )
    users = summary.control_pk_uniqueness.stream_results["users"]
    assert (users.fixed_duplicate_pk_count, users.lost_duplicate_pk_count) == (0, 1)
    assert not summary.pk_presence.passed

    # Changed: the one target record equals neither control row.
    summary = run_record_comparisons(
        _records("users", HOLD, HOLD), _records("users", RELEASE), USERS_PKS
    )
    users = summary.control_pk_uniqueness.stream_results["users"]
    assert (users.fixed_duplicate_pk_count, users.lost_duplicate_pk_count) == (0, 1)
    assert not summary.field_comparison.passed

    # Pre-existing next to lost: both named on the control's message.
    summary = run_record_comparisons(
        _records("users", HOLD, RELEASE, {"id": 1}, {"id": 1}),
        _records("users", HOLD, {"id": 1}, {"id": 1}),
        USERS_PKS,
    )
    assert summary.control_pk_uniqueness.message == (
        "Pre-existing duplicate primary keys in control (not a regression); "
        "others with records the target dropped or changed (field values or PK "
        "presence fail "
        "on them)"
    )


@pytest.mark.unit
def test_the_pk_integrity_message_names_what_the_control_duplicates_are(
    tmp_path: Path,
) -> None:
    """Derived from the split: pre-existing only, fixed only, or both. The
    target never emits the fixed ones, so its row does not mention them."""
    cases = {
        "pre_existing": (
            _with_duplicates("users", [1]),
            _with_duplicates("users", [1]),
            "Pre-existing duplicate primary keys in control (not a regression)",
            "Pre-existing duplicate primary keys in target (not a regression)",
        ),
        "fixed": (
            _with_duplicates("users", [1], unique=[2]),
            _with_duplicates("users", [], unique=[1, 2]),
            "Duplicate primary keys in control fixed in target (not a regression)",
            "All primary keys unique and present in target",
        ),
        "both": (
            _with_duplicates("users", [1, 2]),
            _with_duplicates("users", [1], unique=[2]),
            "Pre-existing duplicate primary keys in control, and others fixed in "
            "target (not a regression)",
            "Pre-existing duplicate primary keys in target (not a regression)",
        ),
    }
    for case, (control, target, control_message, target_message) in cases.items():
        in_memory = run_record_comparisons(control, target, USERS_PKS)
        from_files = run_record_comparisons_from_files(
            _write_record_files(tmp_path / case / "control", control),
            _write_record_files(tmp_path / case / "target", target),
            USERS_PKS,
        )
        for summary in (in_memory, from_files):
            assert summary.passed, case
            assert summary.control_pk_uniqueness.message == control_message, case
            assert summary.target_pk_uniqueness.message == target_message, case


@pytest.mark.unit
def test_a_version_checked_alone_fails_on_every_duplicate() -> None:
    result = check_pk_uniqueness(_with_duplicates("users", [1, 2]), USERS_PKS)

    assert not result.passed
    assert result.errors == ["Stream users has 2 duplicate primary key value(s)"]
    assert result.warnings == []


@pytest.mark.unit
def test_records_missing_pk_still_fail_next_to_pre_existing_duplicates() -> None:
    control = _records("users", {"id": 1}, {"id": 1}, {"id": None})
    target = _records("users", {"id": 1}, {"id": 1}, {"id": None})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert not summary.control_pk_uniqueness.passed
    assert not summary.target_pk_uniqueness.passed
    assert all("missing or null primary key" in error for error in summary.errors)
    assert len(summary.errors) == 2


@pytest.mark.unit
def test_duplicate_pk_split_is_serialized_on_both_sides() -> None:
    control = _with_duplicates("users", [1, 2, 3, 6])
    target = _with_duplicates("users", [2, 3, 4, 5], unique=[1])

    payload = run_record_comparisons(control, target, USERS_PKS).to_dict()

    checks = payload["checks"]
    for check in ("pk_uniqueness_control", "pk_uniqueness_target"):
        users = checks[check]["streams"]["users"]
        assert users["pre_existing_duplicate_pk_count"] == 2
        assert users["new_duplicate_pk_count"] == 2
        assert users["fixed_duplicate_pk_count"] == 1
        # 6 is duplicated in the control and gone from the target: not fixed.
        assert users["lost_duplicate_pk_count"] == 1
        assert {
            "passed",
            "duplicate_pk_count",
            "duplicate_pk_examples",
            "records_missing_pk",
        } <= set(users)
    assert (
        checks["pk_uniqueness_control"]["streams"]["users"]["duplicate_pk_count"] == 4
    )
    assert checks["pk_uniqueness_target"]["streams"]["users"]["duplicate_pk_count"] == 4


@pytest.mark.unit
def test_duplicate_pk_split_is_exact_past_the_example_cap(monkeypatch) -> None:
    monkeypatch.setattr(comparators, "MAX_EXAMPLE_PKS", 3)
    control = _with_duplicates("users", list(range(10)))
    target = _with_duplicates("users", list(range(5, 15)), unique=list(range(5)))

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert _split_of(summary, "target_pk_uniqueness") == (5, 5, 5)
    target_users = summary.target_pk_uniqueness.stream_results["users"]
    assert target_users.duplicate_pk_count == 10
    assert len(target_users.duplicate_pks) == 3


@pytest.mark.unit
def test_single_version_check_has_no_split() -> None:
    result = check_pk_uniqueness(_with_duplicates("users", [1]), USERS_PKS)

    assert not result.passed
    users = result.stream_results["users"]
    assert (
        users.pre_existing_duplicate_pk_count,
        users.new_duplicate_pk_count,
        users.fixed_duplicate_pk_count,
    ) == (0, 0, 0)
    assert "duplicated in both versions" not in result.errors[0]


@pytest.mark.unit
def test_duplicate_pk_split_survives_summary_degradation() -> None:
    control = _with_duplicates("users", list(range(DEGRADED_EXAMPLE_CAP + 10)))
    target = _with_duplicates("users", list(range(DEGRADED_EXAMPLE_CAP + 20)))
    payload = run_record_comparisons(control, target, USERS_PKS).to_dict()

    assert comparators._degrade_example_lists(payload) is not None
    users = payload["checks"]["pk_uniqueness_target"]["streams"]["users"]
    assert len(users["duplicate_pk_examples"]) == DEGRADED_EXAMPLE_CAP
    assert users["duplicate_pk_count"] == DEGRADED_EXAMPLE_CAP + 20
    assert users["pre_existing_duplicate_pk_count"] == DEGRADED_EXAMPLE_CAP + 10
    assert users["new_duplicate_pk_count"] == 10
    assert users["fixed_duplicate_pk_count"] == 0

    assert comparators._degrade_to_verdict_only(payload) is not None
    assert payload["checks"]["pk_uniqueness_target"]["passed"] is False


@pytest.mark.unit
def test_run_record_comparisons_from_files_classifies_duplicates(
    tmp_path: Path,
) -> None:
    control = _with_duplicates("users", [1, 2, 3], unique=[4])
    target = _with_duplicates("users", [2, 3, 4], unique=[1])
    control_files = _write_record_files(tmp_path / "control", control)
    target_files = _write_record_files(tmp_path / "target", target)

    from_files = run_record_comparisons_from_files(
        control_files, target_files, USERS_PKS
    )
    in_memory = run_record_comparisons(control, target, USERS_PKS)

    assert from_files.to_dict() == in_memory.to_dict()
    assert _split_of(from_files, "control_pk_uniqueness") == (2, 1, 1)
    assert _split_of(from_files, "target_pk_uniqueness") == (2, 1, 1)
    assert from_files.control_pk_uniqueness.passed
    assert from_files.control_pk_uniqueness.message == (
        "Pre-existing duplicate primary keys in control, and others fixed in "
        "target (not a regression)"
    )
    assert not from_files.target_pk_uniqueness.passed


@pytest.mark.unit
def test_run_record_comparisons_from_files_passes_on_shared_duplicates(
    tmp_path: Path,
) -> None:
    control = _with_duplicates("users", [1, 2])
    control_files = _write_record_files(tmp_path / "control", control)
    target_files = _write_record_files(tmp_path / "target", control)

    summary = run_record_comparisons_from_files(control_files, target_files, USERS_PKS)

    assert summary.passed
    assert summary.errors == []
    assert summary.warnings == [
        "Stream users has 2 pre-existing duplicate primary key value(s), "
        "unchanged between control and target"
    ]
    assert summary.target_pk_uniqueness.message == (
        "Pre-existing duplicate primary keys in target (not a regression)"
    )


# ---------------------------------------------------------------------------
# compare_all_records directional mode
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_directional_field_comparison_allows_extra_target_records() -> None:
    control = _records("users", {"id": 1, "name": "a"})
    target = _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"})

    strict = compare_all_records(control, target, USERS_PKS)
    directional = compare_all_records(control, target, USERS_PKS, directional=True)

    assert not strict.passed
    assert directional.passed


@pytest.mark.unit
def test_directional_field_comparison_fails_on_value_diff() -> None:
    control = _records("users", {"id": 1, "name": "a"})
    target = _records("users", {"id": 1, "name": "CHANGED"})

    result = compare_all_records(control, target, USERS_PKS, directional=True)
    assert not result.passed


# ---------------------------------------------------------------------------
# run_record_comparisons — acceptance criteria
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_identical_output_passes() -> None:
    control = _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"})
    target = _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed
    assert not summary.errors


@pytest.mark.unit
def test_dropped_record_fails() -> None:
    control = _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"})
    target = _records("users", {"id": 1, "name": "a"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert not summary.count_comparison.passed
    assert summary.pk_presence is not None
    assert not summary.pk_presence.passed


@pytest.mark.unit
def test_missing_pk_fails_even_when_counts_match() -> None:
    control = _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"})
    target = _records("users", {"id": 1, "name": "a"}, {"id": 3, "name": "c"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert summary.count_comparison.passed
    assert summary.pk_presence is not None
    assert not summary.pk_presence.passed
    assert summary.pk_presence.stream_results["users"].missing_pks == [(2,)]


@pytest.mark.unit
def test_pk_value_type_change_fails_and_message_explains_it() -> None:
    # PKs are matched by exact value and type: 123 and "123" are different
    # PK values, so a type change fails (it is a breaking change for
    # destinations) and the error must mention that possibility — every
    # control PK reads as "missing" even though the records are all there.
    control = _records("users", {"id": 123, "name": "a"})
    target = _records("users", {"id": "123", "name": "a"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert summary.pk_presence is not None
    assert not summary.pk_presence.passed
    assert any("PK value type changed" in error for error in summary.errors)


@pytest.mark.unit
def test_mutated_field_value_fails() -> None:
    control = _records("users", {"id": 1, "name": "a"})
    target = _records("users", {"id": 1, "name": "MUTATED"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert summary.count_comparison.passed
    assert summary.pk_presence is not None and summary.pk_presence.passed
    assert summary.field_comparison is not None
    assert not summary.field_comparison.passed


@pytest.mark.unit
def test_duplicate_pk_in_target_fails() -> None:
    control = _records("users", {"id": 1, "name": "a"})
    target = _records("users", {"id": 1, "name": "a"}, {"id": 1, "name": "a"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert summary.target_pk_uniqueness is not None
    assert not summary.target_pk_uniqueness.passed
    assert summary.control_pk_uniqueness is not None
    assert summary.control_pk_uniqueness.passed

    target_check = summary.to_dict()["checks"]["pk_uniqueness_target"]
    assert target_check["streams"]["users"]["duplicate_pk_examples"] == [
        {"pk": [1], "count": 2}
    ]


@pytest.mark.unit
def test_missing_pk_examples_are_capped_but_count_is_full() -> None:
    total = MAX_EXAMPLE_PKS + 100
    control = _records("users", *[{"id": i} for i in range(total)])
    target = _records("users", *[{"id": i} for i in range(total, 2 * total)])

    summary = run_record_comparisons(control, target, USERS_PKS)

    users = summary.to_dict()["checks"]["pk_presence"]["streams"]["users"]
    assert users["missing_pk_count"] == total
    assert len(users["missing_pk_examples"]) == MAX_EXAMPLE_PKS


@pytest.mark.unit
def test_duplicate_pk_examples_under_cap_are_listed_in_full() -> None:
    duplicated = [{"id": i} for i in range(15)] * 2
    control = _records("users", {"id": 0})
    target = _records("users", *duplicated)

    summary = run_record_comparisons(control, target, USERS_PKS)

    users = summary.to_dict()["checks"]["pk_uniqueness_target"]["streams"]["users"]
    assert users["duplicate_pk_count"] == 15
    assert len(users["duplicate_pk_examples"]) == 15
    # Every example says how many records shared the PK value.
    assert all(example["count"] == 2 for example in users["duplicate_pk_examples"])


@pytest.mark.unit
def test_duplicate_pk_in_control_warns_as_fixed() -> None:
    control = _records("users", {"id": 1, "name": "a"}, {"id": 1, "name": "a"})
    target = _records("users", {"id": 1, "name": "a"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    # The control's duplicate is a warning the target fixed, and the record
    # it no longer emits is within the duplicate rows the count allows for.
    assert summary.passed
    assert summary.errors == []
    assert summary.control_pk_uniqueness is not None
    assert summary.control_pk_uniqueness.passed
    assert summary.control_pk_uniqueness.warnings == [
        "Stream users has 1 duplicate primary key value(s) in control fixed in target"
    ]
    assert summary.count_comparison.passed
    assert summary.count_comparison.errors == []
    assert summary.count_comparison.warnings == [
        "Stream users has 1 fewer record in target, within the duplicate rows the "
        "target dropped (1 in control, 0 in target); field values check that the "
        "dropped rows were copies"
    ]
    assert summary.count_comparison.message == (
        "Record counts match once duplicate rows are left out"
    )


# ---------------------------------------------------------------------------
# record counts: a shortfall of duplicate rows the target dropped warns
# ---------------------------------------------------------------------------


def _ids(*counts: tuple[int, int]) -> list[dict[str, Any]]:
    """`(id, n)` pairs as n identical records per id."""
    return [{"id": pk, "n": "same"} for pk, n in counts for _ in range(n)]


@pytest.mark.unit
def test_a_shortfall_of_dropped_duplicate_rows_warns_on_record_counts() -> None:
    # Control: id 1 x4 and id 2 x3 (5 duplicate rows). Target: x2 each
    # (2 duplicate rows). 3 fewer records, within the 3 duplicate rows dropped.
    control = _records("users", *_ids((1, 4), (2, 3), (3, 1)))
    target = _records("users", *_ids((1, 2), (2, 2), (3, 1)))

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed
    users = summary.count_comparison.stream_results["users"]
    assert users.passed
    assert (users.control_count, users.target_count) == (8, 5)
    message = (
        "Stream users has 3 fewer records in target, within the duplicate rows "
        "the target dropped (5 in control, 2 in target); field values check that "
        "the dropped rows were copies"
    )
    assert users.message == message
    assert message in summary.warnings
    assert summary.errors == []
    assert (
        summary.control_pk_uniqueness.stream_results["users"].duplicate_row_count == 5
    )
    assert summary.target_pk_uniqueness.stream_results["users"].duplicate_row_count == 2

    payload = summary.to_dict()["checks"]
    assert payload["record_counts"]["passed"] is True
    assert (
        payload["pk_uniqueness_control"]["streams"]["users"]["duplicate_row_count"] == 5
    )
    assert (
        payload["pk_uniqueness_target"]["streams"]["users"]["duplicate_row_count"] == 2
    )


@pytest.mark.unit
def test_a_shortfall_beyond_the_dropped_duplicate_rows_still_fails() -> None:
    control = _records("users", *_ids((1, 2), (2, 1)))
    target = _records("users", *_ids((1, 1)))

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert not summary.count_comparison.passed
    assert summary.count_comparison.message == "Record count mismatch"
    assert summary.count_comparison.errors == [
        "Stream users has 2 fewer records in target (1 vs 3)"
    ]


@pytest.mark.unit
def test_new_duplicate_rows_in_the_target_count_against_the_allowance() -> None:
    # The target collapses id 1 (-2 rows) but duplicates id 2 (+1 row):
    # 1 duplicate row fewer net, against a shortfall of 1.
    control = _records("users", *_ids((1, 3), (2, 1), (3, 1)))
    target = _records("users", *_ids((1, 1), (2, 2), (3, 1)))

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.count_comparison.passed
    assert summary.count_comparison.warnings == [
        "Stream users has 1 fewer record in target, within the duplicate rows the "
        "target dropped (2 in control, 1 in target); field values check that the "
        "dropped rows were copies"
    ]
    # The new duplicate still fails on its own check.
    assert not summary.target_pk_uniqueness.passed
    assert not summary.passed


@pytest.mark.unit
def test_a_stream_without_pk_gets_no_duplicate_row_allowance() -> None:
    control = _records("events", {"id": 1}, {"id": 1})
    target = _records("events", {"id": 1})

    summary = run_record_comparisons(control, target, {"events": None})

    assert not summary.passed
    assert not summary.count_comparison.passed


@pytest.mark.unit
def test_the_duplicate_row_allowance_is_the_same_from_files(tmp_path: Path) -> None:
    control = {
        **_records("users", *_ids((1, 4), (2, 3), (3, 1))),
        **_records("orders", *[{"order_id": 1, "v": "a"}] * 2),
        **_records("events", {"type": "x"}, {"type": "y"}),
    }
    target = {
        **_records("users", *_ids((1, 2), (2, 2), (3, 1))),
        **_records("orders", {"order_id": 1, "v": "a"}),
        **_records("events", {"type": "x"}),
    }
    pks = {"users": [["id"]], "orders": [["order_id"]], "events": None}

    in_memory = run_record_comparisons(control, target, pks)
    from_files = run_record_comparisons_from_files(
        _write_record_files(tmp_path / "control", control),
        _write_record_files(tmp_path / "target", target),
        pks,
    )

    in_memory_payload = in_memory.to_dict()
    from_files_payload = from_files.to_dict()
    assert from_files_payload["checks"] == in_memory_payload["checks"]
    assert sorted(from_files_payload["errors"]) == sorted(in_memory_payload["errors"])
    assert sorted(from_files_payload["warnings"]) == sorted(
        in_memory_payload["warnings"]
    )
    # The no-PK stream still fails its count; the two PK streams warn.
    assert from_files.passed is in_memory.passed is False
    assert from_files.count_comparison.failed_streams == ["events"]
    assert from_files.count_comparison.message == "Record count mismatch"
    for summary in (in_memory, from_files):
        counts = summary.count_comparison.stream_results
        assert counts["users"].passed and counts["orders"].passed
        assert any("(5 in control, 2 in target)" in w for w in summary.warnings)
        assert any("(1 in control, 0 in target)" in w for w in summary.warnings)

    # Without the failing no-PK stream, both paths pass with the same message.
    del control["events"], target["events"]
    in_memory = run_record_comparisons(control, target, pks)
    from_files = run_record_comparisons_from_files(
        _write_record_files(tmp_path / "control2", control),
        _write_record_files(tmp_path / "target2", target),
        pks,
    )
    assert in_memory.passed and from_files.passed
    assert in_memory.count_comparison.message == from_files.count_comparison.message
    assert from_files.count_comparison.message == (
        "Record counts match once duplicate rows are left out"
    )


@pytest.mark.unit
def test_record_missing_pk_value_fails_even_when_pre_existing() -> None:
    # A missing PK value fails the run even when both versions show it: the
    # declared PK cannot be trusted regardless of which version introduced it.
    control = _records("users", {"id": None, "name": "a"})
    target = _records("users", {"id": None, "name": "a"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert summary.control_pk_uniqueness is not None
    assert not summary.control_pk_uniqueness.passed
    assert summary.target_pk_uniqueness is not None
    assert not summary.target_pk_uniqueness.passed
    assert any("missing or null primary key" in e for e in summary.errors)


@pytest.mark.unit
def test_records_missing_pk_are_excluded_from_matching_not_collapsed() -> None:
    # Mixed stream: records with valid PKs still get the real comparisons
    # (the id=1 mutation is caught), records without a PK value don't
    # collide with each other in the presence check or the by-PK matching.
    control = _records(
        "users",
        {"id": 1, "name": "a"},
        {"id": None, "name": "x"},
        {"id": None, "name": "y"},
    )
    target = _records(
        "users",
        {"id": 1, "name": "MUTATED"},
        {"id": None, "name": "x"},
        {"id": None, "name": "y"},
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert summary.field_comparison is not None
    assert not summary.field_comparison.passed
    users_diff = summary.field_comparison.stream_results["users"].record_diff
    assert users_diff is not None
    assert len(users_diff.records_with_value_diff) == 1
    # The missing-PK records are not reported as duplicates or as missing
    # from the target; they surface through the dedicated error only.
    assert summary.pk_presence is not None
    assert summary.pk_presence.passed
    assert summary.control_pk_uniqueness is not None
    assert summary.control_pk_uniqueness.stream_results["users"].duplicate_pks == []

    payload = summary.to_dict()
    for check in ("pk_uniqueness_control", "pk_uniqueness_target"):
        assert payload["checks"][check]["streams"]["users"]["records_missing_pk"] == 2


@pytest.mark.unit
def test_stream_without_pk_falls_back_to_count_comparison() -> None:
    # Mutated values and extra records must NOT fail a stream without a PK;
    # only a drop in record count does.
    control = _records("events", {"type": "x"}, {"type": "y"})
    target = _records("events", {"type": "MUTATED"}, {"type": "y"}, {"type": "z"})

    summary = run_record_comparisons(control, target, {"events": None})

    assert summary.passed
    assert summary.streams_without_pk == ["events"]
    assert summary.field_comparison is None
    assert any("no primary key" in w for w in summary.warnings)


@pytest.mark.unit
def test_stream_without_pk_fails_on_fewer_records() -> None:
    control = _records("events", {"type": "x"}, {"type": "y"})
    target = _records("events", {"type": "x"})

    summary = run_record_comparisons(control, target, {"events": None})

    assert not summary.passed
    assert not summary.count_comparison.passed


@pytest.mark.unit
def test_extra_target_records_pass_directionally() -> None:
    control = _records("users", {"id": 1, "name": "a"})
    target = _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed


@pytest.mark.unit
def test_mixed_pk_and_no_pk_streams() -> None:
    control = {
        **_records("users", {"id": 1, "name": "a"}),
        **_records("events", {"type": "x"}),
    }
    target = {
        **_records("users", {"id": 1, "name": "MUTATED"}),
        **_records("events", {"type": "y"}),
    }

    summary = run_record_comparisons(
        control, target, {"users": [["id"]], "events": None}
    )

    # The users mutation fails; the events mutation is ignored (no PK).
    assert not summary.passed
    assert summary.field_comparison is not None
    assert set(summary.field_comparison.stream_results) == {"users"}


@pytest.mark.unit
def test_flat_pk_format_is_normalized() -> None:
    control = _records("users", {"id": 1, "name": "a"})
    target = _records("users", {"id": 1, "name": "MUTATED"})

    summary = run_record_comparisons(control, target, {"users": ["id"]})

    assert not summary.passed


@pytest.mark.unit
def test_summary_to_dict_is_json_serializable() -> None:
    control = _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"})
    target = _records("users", {"id": 1, "name": "MUTATED"})

    summary = run_record_comparisons(control, target, USERS_PKS)
    payload = summary.to_dict()

    serialized = json.dumps(payload)
    assert serialized
    assert payload["passed"] is False
    checks = payload["checks"]
    assert not checks["record_counts"]["passed"]
    assert not checks["pk_presence"]["passed"]
    assert not checks["field_values"]["passed"]
    assert checks["pk_presence"]["streams"]["users"]["missing_pk_count"] == 1
    assert checks["pk_presence"]["streams"]["users"]["missing_pk_examples"] == [[2]]


@pytest.mark.unit
def test_value_diff_examples_are_capped_but_counts_are_full() -> None:
    control = _records("users", *[{"id": i, "name": f"a{i}"} for i in range(1, 9)])
    target = _records("users", *[{"id": i, "name": f"b{i}"} for i in range(1, 9)])

    summary = run_record_comparisons(control, target, USERS_PKS)

    users = summary.to_dict()["checks"]["field_values"]["streams"]["users"]
    assert users["records_with_value_diff"] == 8
    assert len(users["value_diff_examples"]) == 5


@pytest.mark.unit
def test_records_only_in_control_examples_are_capped() -> None:
    control = _records("users", *[{"id": i} for i in range(1, 10)])
    target = _records("users", {"id": 1})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.field_comparison is not None
    diff = summary.field_comparison.stream_results["users"].record_diff
    assert diff is not None
    assert diff.records_only_in_control_count == 8
    assert len(diff.records_only_in_control) == 5
    assert diff.has_diff


def _users_value_diff_example(summary) -> dict[str, Any]:
    streams = summary.to_dict()["checks"]["field_values"]["streams"]
    return streams["users"]["value_diff_examples"][0]


@pytest.mark.unit
def test_small_value_diff_is_embedded_intact() -> None:
    control = _records("users", {"id": 1, "name": "a"})
    target = _records("users", {"id": 1, "name": "b"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    example = _users_value_diff_example(summary)
    assert "values_changed" in example["diff"]
    assert "truncated" not in json.dumps(example["diff"])


@pytest.mark.unit
def test_large_diff_values_are_embedded_whole_in_the_summary() -> None:
    """No size cap on a kept example's diff: the full values ride along.

    The examples are bounded in number (`MAX_EXAMPLE_DIFFS`), not in size.
    If GITHUB_OUTPUT ever overflows on a connector with huge field values,
    add a cap then, on the JSON path only.
    """
    control = _records("users", {"id": 1, "blob": "x" * 5000})
    target = _records("users", {"id": 1, "blob": "y" * 5000})

    summary = run_record_comparisons(control, target, USERS_PKS)

    example = _users_value_diff_example(summary)
    diff = example["diff"]
    assert diff["values_changed"]["root['data']['blob']"]["old_value"] == "x" * 5000
    assert diff["values_changed"]["root['data']['blob']"]["new_value"] == "y" * 5000
    assert "truncated" not in diff


@pytest.mark.unit
def test_a_wide_diff_is_embedded_whole_in_the_summary() -> None:
    control = _records("users", {"id": 1, **{f"f{i}": "a" * 150 for i in range(20)}})
    target = _records("users", {"id": 1, **{f"f{i}": "b" * 150 for i in range(20)}})

    summary = run_record_comparisons(control, target, USERS_PKS)

    example = _users_value_diff_example(summary)
    assert example["pk"] == [1]
    changed = example["diff"]["values_changed"]
    assert len(changed) == 20
    assert all(len(entry["new_value"]) == 150 for entry in changed.values())


# ---------------------------------------------------------------------------
# to_dict global size budget (GITHUB_OUTPUT caps a step's outputs at ~1MiB)
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_summary_under_budget_is_not_degraded() -> None:
    control = _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"})
    target = _records("users", {"id": 1, "name": "MUTATED"})

    payload = run_record_comparisons(control, target, USERS_PKS).to_dict()

    assert not any("truncated" in warning for warning in payload["warnings"])
    example = payload["checks"]["field_values"]["streams"]["users"][
        "value_diff_examples"
    ][0]
    assert "values_changed" in example["diff"]


@pytest.mark.unit
def test_oversized_diffs_degrade_to_placeholders() -> None:
    # A single value-diff whose old+new values alone exceed the budget:
    # the whole-diff embedding must give way, but pk and counts survive
    # so the record stays findable in the per-stream artifact files.
    blob_size = MAX_SUMMARY_BYTES
    control = _records("users", {"id": 1, "blob": "x" * blob_size})
    target = _records("users", {"id": 1, "blob": "y" * blob_size})

    payload = run_record_comparisons(control, target, USERS_PKS).to_dict()

    assert len(json.dumps(payload, separators=(",", ":"))) <= MAX_SUMMARY_BYTES
    example = payload["checks"]["field_values"]["streams"]["users"][
        "value_diff_examples"
    ][0]
    assert example["pk"] == [1]
    assert example["diff"]["truncated"] is True
    assert example["diff"]["changed_sections"] == ["values_changed"]
    assert (
        payload["checks"]["field_values"]["streams"]["users"]["records_with_value_diff"]
        == 1
    )
    assert any("truncated to fit GITHUB_OUTPUT" in w for w in payload["warnings"])


@pytest.mark.unit
def test_oversized_pk_example_lists_degrade_to_capped_lists() -> None:
    # The stage in isolation: example lists shrink to the cap, the exact
    # counts survive untouched.
    total = DEGRADED_EXAMPLE_CAP + 50
    control = _records("users", *[{"id": i} for i in range(total)])
    target = _records("users", *[{"id": i} for i in range(total, 2 * total)])
    payload = run_record_comparisons(control, target, USERS_PKS).to_dict()

    note = comparators._degrade_example_lists(payload)

    assert note is not None and "PK example lists capped" in note
    users = payload["checks"]["pk_presence"]["streams"]["users"]
    assert users["missing_pk_count"] == total
    assert len(users["missing_pk_examples"]) == DEGRADED_EXAMPLE_CAP


@pytest.mark.unit
def test_oversized_passing_catalog_drops_passing_stream_entries() -> None:
    # A huge catalog outgrows the budget on per-stream metadata alone --
    # every stream gets an entry per check even when everything passes.
    # Failing streams' entries must survive the drop.
    control = {
        **_records("healthy", {"id": 1}),
        **_records("broken", {"id": 1}, {"id": 2}),
    }
    target = {
        **_records("healthy", {"id": 1}),
        **_records("broken", {"id": 1}),
    }
    payload = run_record_comparisons(
        control, target, {"healthy": [["id"]], "broken": [["id"]]}
    ).to_dict()

    note = comparators._degrade_passing_stream_entries(payload)

    assert note is not None and "passing streams omitted" in note
    counts = payload["checks"]["record_counts"]
    assert set(counts["streams"]) == {"broken"}
    assert counts["streams"]["broken"]["control_count"] == 2
    assert counts["passing_streams_omitted"] == 1
    # The verdict layer is untouched: the summary still fails on "broken".
    assert payload["passed"] is False


@pytest.mark.unit
def test_oversized_message_lists_are_capped() -> None:
    streams = {f"s{i:03d}": [_record(f"s{i:03d}", {"id": 1})] for i in range(120)}
    empty_target: dict[str, list[AirbyteMessage]] = {}
    payload = run_record_comparisons(
        streams, empty_target, {name: [["id"]] for name in streams}
    ).to_dict()

    note = comparators._degrade_message_lists(payload)

    assert note is not None
    assert len(payload["errors"]) == DEGRADED_EXAMPLE_CAP + 1
    assert "more (see run artifacts)" in payload["errors"][-1]


@pytest.mark.unit
def test_many_failing_streams_cannot_outgrow_the_floor(monkeypatch) -> None:
    """Nothing before the terminal stages bounds the number of FAILING
    streams; a wide source dropping records across many tables must still
    serialize under the floor, with the drop recorded."""
    monkeypatch.setattr(comparators, "MAX_SUMMARY_BYTES", 20_000)
    streams = {f"s{i:04d}": [_record(f"s{i:04d}", {"id": 1})] for i in range(300)}
    empty_target: dict[str, list[AirbyteMessage]] = {}

    payload = run_record_comparisons(
        streams, empty_target, {name: [["id"]] for name in streams}
    ).to_dict()

    assert len(json.dumps(payload).encode()) <= 20_000
    assert payload["passed"] is False
    assert any(
        "per-stream detail capped" in w or "verdicts only" in w
        for w in payload["warnings"]
    )


@pytest.mark.unit
def test_pathological_payloads_degrade_to_verdicts_only(monkeypatch) -> None:
    """The floor is a guarantee, not a hope: content the other stages cannot
    shrink (huge scalar PK values) falls back to verdicts and counts."""
    monkeypatch.setattr(comparators, "MAX_SUMMARY_BYTES", 5_000)
    control = _records("users", *[{"id": f"pk-{i}-" + "x" * 500} for i in range(40)])
    target = _records("users", {"id": "only-this-one"})

    payload = run_record_comparisons(control, target, USERS_PKS).to_dict()

    assert len(json.dumps(payload).encode()) <= 5_000
    assert payload["passed"] is False
    assert any("verdicts only" in w for w in payload["warnings"])
    # The verdict survives even when every per-stream payload is gone.
    assert payload["checks"]["pk_presence"]["passed"] is False


# ---------------------------------------------------------------------------
# file-based (memory-bounded) comparison
# ---------------------------------------------------------------------------


def _write_record_files(
    base_dir: Path,
    records: dict[str, list[AirbyteMessage]],
) -> dict[str, Path]:
    base_dir.mkdir(parents=True, exist_ok=True)
    paths: dict[str, Path] = {}
    for stream, messages in records.items():
        path = base_dir / f"{stream}.jsonl"
        path.write_text("".join(m.model_dump_json() + "\n" for m in messages))
        paths[stream] = path
    return paths


@pytest.mark.unit
def test_run_record_comparisons_from_files_matches_in_memory(tmp_path: Path) -> None:
    # Mixed scenario: a mutated record and a dropped PK on a PK stream, a
    # count regression on a no-PK stream, and a stream missing entirely
    # from the target.
    control = {
        **_records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"}),
        **_records("events", {"type": "x"}, {"type": "y"}),
        **_records("orders", {"order_id": 7}),
    }
    target = {
        **_records("users", {"id": 1, "name": "MUTATED"}),
        **_records("events", {"type": "x"}),
    }
    pks = {"users": [["id"]], "events": None, "orders": [["order_id"]]}

    in_memory = run_record_comparisons(control, target, pks)
    from_files = run_record_comparisons_from_files(
        _write_record_files(tmp_path / "control", control),
        _write_record_files(tmp_path / "target", target),
        pks,
    )

    in_memory_payload = in_memory.to_dict()
    from_files_payload = from_files.to_dict()
    assert from_files_payload["passed"] == in_memory_payload["passed"] is False
    assert from_files_payload["checks"] == in_memory_payload["checks"]
    assert from_files_payload["streams_without_pk"] == ["events"]
    assert sorted(from_files_payload["errors"]) == sorted(in_memory_payload["errors"])
    assert sorted(from_files_payload["warnings"]) == sorted(
        in_memory_payload["warnings"]
    )


@pytest.mark.unit
def test_run_record_comparisons_from_files_passes_on_identical_output(
    tmp_path: Path,
) -> None:
    records = _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"})

    summary = run_record_comparisons_from_files(
        _write_record_files(tmp_path / "control", records),
        _write_record_files(tmp_path / "target", records),
        USERS_PKS,
    )

    assert summary.passed
    assert not summary.errors


@pytest.mark.unit
def test_run_record_comparisons_from_files_empty_runs(tmp_path: Path) -> None:
    summary = run_record_comparisons_from_files({}, {}, USERS_PKS)

    assert summary.passed
    assert summary.to_dict()["checks"]["record_counts"]["passed"]


# ---------------------------------------------------------------------------
# models helpers
# ---------------------------------------------------------------------------


def _configured_catalog(streams: list[dict[str, Any]]) -> ConfiguredAirbyteCatalog:
    return ConfiguredAirbyteCatalog.model_validate({"streams": streams})


@pytest.mark.unit
def test_get_primary_keys_per_stream_prefers_source_defined() -> None:
    catalog = _configured_catalog(
        [
            {
                "stream": {
                    "name": "users",
                    "json_schema": {},
                    "supported_sync_modes": ["full_refresh"],
                    "source_defined_primary_key": [["id"]],
                },
                "sync_mode": "full_refresh",
                "destination_sync_mode": "append",
                "primary_key": [["configured_id"]],
            },
            {
                "stream": {
                    "name": "orders",
                    "json_schema": {},
                    "supported_sync_modes": ["full_refresh"],
                },
                "sync_mode": "full_refresh",
                "destination_sync_mode": "append",
                "primary_key": [["order_id"]],
            },
            {
                "stream": {
                    "name": "events",
                    "json_schema": {},
                    "supported_sync_modes": ["full_refresh"],
                },
                "sync_mode": "full_refresh",
                "destination_sync_mode": "append",
            },
        ]
    )

    assert get_primary_keys_per_stream(catalog) == {
        "users": [["id"]],
        "orders": [["order_id"]],
        "events": None,
    }


@pytest.mark.unit
def test_split_records_per_stream(tmp_path: Path) -> None:
    stdout = tmp_path / "stdout.log"
    lines = [
        "plain log line that is not json",
        _record("users", {"id": 1}).model_dump_json(),
        json.dumps({"type": "LOG", "log": {"level": "INFO", "message": "hi"}}),
        _record("users", {"id": 2}).model_dump_json(),
        _record("orders", {"order_id": 7}).model_dump_json(),
        "",
    ]
    stdout.write_text("\n".join(lines))

    record_files = split_records_per_stream(stdout)

    assert set(record_files) == {"users", "orders"}
    assert all(
        path.parent == tmp_path / "records_per_stream" for path in record_files.values()
    )
    users_lines = record_files["users"].read_text().splitlines()
    assert [json.loads(line)["record"]["data"]["id"] for line in users_lines] == [1, 2]
    assert len(record_files["orders"].read_text().splitlines()) == 1


@pytest.mark.unit
def test_split_records_per_stream_sanitizes_colliding_names(tmp_path: Path) -> None:
    stdout = tmp_path / "stdout.log"
    stdout.write_text(
        "\n".join(
            [
                _record("a/b", {"id": 1}).model_dump_json(),
                _record("a_b", {"id": 2}).model_dump_json(),
            ]
        )
    )

    record_files = split_records_per_stream(stdout)

    assert set(record_files) == {"a/b", "a_b"}
    # Both stream names sanitize to "a_b"; the files must not collide.
    assert record_files["a/b"] != record_files["a_b"]
    for stream, path in record_files.items():
        line = json.loads(path.read_text().splitlines()[0])
        assert line["record"]["stream"] == stream


@pytest.mark.unit
def test_split_records_per_stream_bounds_open_file_handles(
    tmp_path: Path, monkeypatch
) -> None:
    # More streams than the handle cap, interleaved so streams are written,
    # evicted, and written again: eviction + append-mode reopen must lose
    # nothing and keep every stream's records in order.
    monkeypatch.setattr(
        "airbyte_ops_mcp.regression_tests.models.MAX_OPEN_RECORD_FILES", 2
    )
    streams = ["a", "b", "c", "a", "b", "c", "a"]
    stdout = tmp_path / "stdout.log"
    stdout.write_text(
        "\n".join(
            _record(stream, {"id": index}).model_dump_json()
            for index, stream in enumerate(streams)
        )
    )

    record_files = split_records_per_stream(stdout)

    assert set(record_files) == {"a", "b", "c"}
    for stream in ("a", "b", "c"):
        ids = [
            json.loads(line)["record"]["data"]["id"]
            for line in record_files[stream].read_text().splitlines()
        ]
        assert ids == [i for i, s in enumerate(streams) if s == stream]


# ---------------------------------------------------------------------------
# report rendering
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_report_includes_record_comparison_section(tmp_path: Path) -> None:
    control = _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"})
    target = _records("users", {"id": 1, "name": "a"})
    summary = run_record_comparisons(control, target, USERS_PKS)

    report_path = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={
            "success": True,
            "exit_code": 0,
            "record_counts_per_stream": {"users": 1},
        },
        control_result={
            "success": True,
            "exit_code": 0,
            "record_counts_per_stream": {"users": 2},
        },
        output_dir=tmp_path,
        record_comparison=summary.to_dict(),
    )

    content = report_path.read_text()
    assert "### Record Comparison" in content
    assert "**Status:** ❌ FAILED" in content
    assert "REGRESSION DETECTED" in content
    assert "| users |" in content


@pytest.mark.unit
def test_report_record_comparison_pass(tmp_path: Path) -> None:
    control = _records("users", {"id": 1, "name": "a"})
    target = _records("users", {"id": 1, "name": "a"})
    summary = run_record_comparisons(control, target, USERS_PKS)

    report_path = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": True, "exit_code": 0},
        control_result={"success": True, "exit_code": 0},
        output_dir=tmp_path,
        record_comparison=summary.to_dict(),
    )

    content = report_path.read_text()
    assert "### Record Comparison" in content
    assert "**Status:** ✅ PASSED" in content
    assert "Both versions succeeded (no regression)" in content


@pytest.mark.unit
def test_report_marks_pre_existing_duplicates_as_a_warning(tmp_path: Path) -> None:
    control = _with_duplicates("users", [1, 2], unique=[3])
    summary = run_record_comparisons(control, control, USERS_PKS)

    report_path = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": True, "exit_code": 0},
        control_result={"success": True, "exit_code": 0},
        output_dir=tmp_path,
        record_comparison=summary.to_dict(),
    )

    content = report_path.read_text()
    assert "**Status:** ✅ PASSED" in content
    assert "Both versions succeeded (no regression)" in content
    assert (
        "| users | 5 → 5 ✅ | 0 ✅ | 2 (pre-existing) ⚠️ | 2 (pre-existing) ⚠️ "
        "| 0 ✅ | ⚠️ |"
    ) in content
    assert "#### Comparison Errors" not in content
    assert (
        "- ⚠️ Stream users has 2 pre-existing duplicate primary key value(s), "
        "unchanged between control and target"
    ) in content


@pytest.mark.unit
def test_report_marks_new_duplicates_as_a_failure(tmp_path: Path) -> None:
    control = _with_duplicates("users", [1], unique=[2, 3])
    target = _with_duplicates("users", [1, 2, 3])
    summary = run_record_comparisons(control, target, USERS_PKS)

    report_path = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": True, "exit_code": 0},
        control_result={"success": True, "exit_code": 0},
        output_dir=tmp_path,
        record_comparison=summary.to_dict(),
    )

    content = report_path.read_text()
    assert "**Status:** ❌ FAILED" in content
    assert "REGRESSION DETECTED" in content
    assert (
        "| users | 4 → 6 ✅ | 0 ✅ | 1 (pre-existing) ⚠️ "
        "| 3 (1 pre-existing, 2 new) ❌ | 0 ✅ | ❌ |"
    ) in content
    assert (
        "- ❌ Stream users has 2 new duplicate primary key value(s) in target "
        "(not duplicated in control)"
    ) in content


@pytest.mark.unit
def test_report_cells_name_the_one_category_a_side_has(tmp_path: Path) -> None:
    control = _with_duplicates("users", [1], unique=[2, 3])
    target = _with_duplicates("users", [2, 3], unique=[1])
    summary = run_record_comparisons(control, target, USERS_PKS)

    report_path = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": True, "exit_code": 0},
        control_result={"success": True, "exit_code": 0},
        output_dir=tmp_path,
        record_comparison=summary.to_dict(),
    )

    content = report_path.read_text()
    assert "| 1 fixed in target ⚠️ | 2 new ❌ | 0 ✅ | ❌ |" in content


@pytest.mark.unit
def test_report_marks_dropped_duplicate_rows_as_a_count_warning(
    tmp_path: Path,
) -> None:
    control = _with_duplicates("users", [1], unique=[2])
    target = _with_duplicates("users", [], unique=[1, 2])
    summary = run_record_comparisons(control, target, USERS_PKS)

    report_path = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": True, "exit_code": 0},
        control_result={"success": True, "exit_code": 0},
        output_dir=tmp_path,
        record_comparison=summary.to_dict(),
    )

    content = report_path.read_text()
    assert "**Status:** ✅ PASSED" in content
    assert "| users | 3 → 2 ⚠️ | 0 ✅ | 1 fixed in target ⚠️ | 0 ✅ | 0 ✅ | ⚠️ |" in (
        content
    )
    assert (
        "- ⚠️ Stream users has 1 fewer record in target, within the duplicate "
        "rows the target dropped (1 in control, 0 in target); field values check "
        "that the dropped rows were copies"
    ) in content
    assert "#### Comparison Errors" not in content


@pytest.mark.unit
def test_report_names_a_duplicate_with_lost_records_on_the_control_cell(
    tmp_path: Path,
) -> None:
    control = _records("users", HOLD, RELEASE, {"id": 1})
    target = _records("users", HOLD, {"id": 1}, {"id": 2})
    summary = run_record_comparisons(control, target, USERS_PKS)

    report_path = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": True, "exit_code": 0},
        control_result={"success": True, "exit_code": 0},
        output_dir=tmp_path,
        record_comparison=summary.to_dict(),
    )

    content = report_path.read_text()
    assert "**Status:** ❌ FAILED" in content
    assert (
        "| users | 3 → 3 ✅ | 0 ✅ | 1 with dropped or changed records ⚠️ | 0 ✅ "
        "| 1 ❌ | ❌ |"
    ) in content
    assert "fixed in target" not in content


@pytest.mark.unit
def test_report_marks_added_copies_as_a_value_diff_warning(tmp_path: Path) -> None:
    rows = [{"id": 7, "event": "A"}, {"id": 7, "event": "B"}]
    summary = run_record_comparisons(
        _records("users", *rows), _records("users", *(rows * 50)), USERS_PKS
    )

    report_path = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": True, "exit_code": 0},
        control_result={"success": True, "exit_code": 0},
        output_dir=tmp_path,
        record_comparison=summary.to_dict(),
    )

    content = report_path.read_text()
    assert "**Status:** ✅ PASSED" in content
    assert (
        "| users | 2 → 100 ✅ | 0 ✅ | 1 (pre-existing) ⚠️ | 1 (pre-existing) ⚠️ "
        "| 0, 98 added copies ⚠️ | ⚠️ |"
    ) in content
    assert (
        "- ⚠️ Stream users: 1 duplicated PK value(s) emit 98 more identical copies "
        "in target than in control"
    ) in content


@pytest.mark.unit
def test_report_names_one_added_copy_in_the_singular(tmp_path: Path) -> None:
    a, b = {"id": 7, "c": "A"}, {"id": 7, "c": "B"}
    summary = run_record_comparisons(
        _records("users", a, a, b), _records("users", a, b, b), USERS_PKS
    )

    report_path = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": True, "exit_code": 0},
        control_result={"success": True, "exit_code": 0},
        output_dir=tmp_path,
        record_comparison=summary.to_dict(),
    )

    assert "| 0, 1 added copy ⚠️ | ⚠️ |" in report_path.read_text()


@pytest.mark.unit
def test_report_shows_records_missing_pk(tmp_path: Path) -> None:
    control = _records("users", {"id": 1, "name": "a"}, {"id": None, "name": "x"})
    target = _records("users", {"id": 1, "name": "a"}, {"id": None, "name": "x"})
    summary = run_record_comparisons(control, target, USERS_PKS)

    report_path = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": True, "exit_code": 0},
        control_result={"success": True, "exit_code": 0},
        output_dir=tmp_path,
        record_comparison=summary.to_dict(),
    )

    content = report_path.read_text()
    assert "**Status:** ❌ FAILED" in content
    # The status closes the cell, after the missing-PK count it judges.
    assert "| 0, 1 missing PK ❌ | 0, 1 missing PK ❌ |" in content
    assert "missing or null primary key" in content


# ---------------------------------------------------------------------------
# CLI wiring (_compare_read_records)
# ---------------------------------------------------------------------------


def _write_stdout_file(path: Path, records: dict[str, list[AirbyteMessage]]) -> Path:
    """Write a fake connector stdout: log noise plus the record messages."""
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = ["starting read, this line is not an Airbyte message"]
    for messages in records.values():
        lines.extend(message.model_dump_json() for message in messages)
    path.write_text("\n".join(lines) + "\n")
    return path


def _users_catalog_file(tmp_path: Path) -> Path:
    catalog = _configured_catalog(
        [
            {
                "stream": {
                    "name": "users",
                    "json_schema": {},
                    "supported_sync_modes": ["full_refresh"],
                    "source_defined_primary_key": [["id"]],
                },
                "sync_mode": "full_refresh",
                "destination_sync_mode": "append",
            }
        ]
    )
    catalog_file = tmp_path / "configured_catalog.json"
    catalog_file.write_text(catalog.model_dump_json())
    return catalog_file


@pytest.mark.unit
def test_compare_read_records_skips_without_catalog(tmp_path: Path) -> None:
    results = {"stdout_file": str(tmp_path / "stdout.log")}

    for catalog_file in (None, tmp_path / "does-not-exist.json"):
        summary, skip_reason = _compare_read_records(
            target_result=results, control_result=results, catalog_file=catalog_file
        )
        assert summary is None
        # The reason travels back so the caller can surface the skip as a
        # diagnostic check instead of a silent stdout warning.
        assert skip_reason is not None and "no configured catalog" in skip_reason


@pytest.mark.unit
def test_compare_read_records_skips_on_unparseable_catalog(tmp_path: Path) -> None:
    catalog_file = tmp_path / "configured_catalog.json"
    catalog_file.write_text("{not valid json")
    results = {"stdout_file": str(tmp_path / "stdout.log")}

    summary, skip_reason = _compare_read_records(
        target_result=results, control_result=results, catalog_file=catalog_file
    )

    assert summary is None
    assert skip_reason is not None and "could not be parsed" in skip_reason


@pytest.mark.unit
def test_compare_read_records_passes_on_identical_output(tmp_path: Path) -> None:
    catalog_file = _users_catalog_file(tmp_path)
    records = _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"})
    control_stdout = _write_stdout_file(tmp_path / "control" / "stdout.log", records)
    target_stdout = _write_stdout_file(tmp_path / "target" / "stdout.log", records)

    summary, _skip_reason = _compare_read_records(
        target_result={"stdout_file": str(target_stdout)},
        control_result={"stdout_file": str(control_stdout)},
        catalog_file=catalog_file,
    )

    assert summary is not None
    assert summary.passed
    assert not summary.errors
    # The per-stream record files land next to each run's stdout.
    assert (tmp_path / "control" / "records_per_stream" / "users.jsonl").exists()
    assert (tmp_path / "target" / "records_per_stream" / "users.jsonl").exists()


@pytest.mark.unit
def test_compare_read_records_detects_regression(tmp_path: Path) -> None:
    catalog_file = _users_catalog_file(tmp_path)
    control_stdout = _write_stdout_file(
        tmp_path / "control" / "stdout.log",
        _records("users", {"id": 1, "name": "a"}, {"id": 2, "name": "b"}),
    )
    target_stdout = _write_stdout_file(
        tmp_path / "target" / "stdout.log",
        _records("users", {"id": 1, "name": "MUTATED"}),
    )

    summary, _skip_reason = _compare_read_records(
        target_result={"stdout_file": str(target_stdout)},
        control_result={"stdout_file": str(control_stdout)},
        catalog_file=catalog_file,
    )

    assert summary is not None
    assert not summary.passed
    assert summary.errors
    payload = summary.to_dict()
    # The source-defined PK from the configured catalog drives the checks.
    assert not payload["checks"]["pk_presence"]["passed"]
    assert not payload["checks"]["field_values"]["passed"]


@pytest.mark.unit
def test_compare_read_records_survives_comparison_errors(
    tmp_path: Path, monkeypatch
) -> None:
    """An unexpected comparison error fails the verdict, never the whole run.

    By the time the comparison runs, both (expensive, live-API) runs have
    completed -- a crash here would destroy the run's outputs and reports,
    so the comparison degrades to a FAILED summary carrying the error.
    """
    catalog_file = _users_catalog_file(tmp_path)
    records = _records("users", {"id": 1, "name": "a"})
    control_stdout = _write_stdout_file(tmp_path / "control" / "stdout.log", records)
    target_stdout = _write_stdout_file(tmp_path / "target" / "stdout.log", records)

    def explode(*args: Any, **kwargs: Any) -> dict[str, Path]:
        raise OSError("Too many open files")

    monkeypatch.setattr("airbyte_ops_mcp.cli.cloud.split_records_per_stream", explode)

    summary, _skip_reason = _compare_read_records(
        target_result={"stdout_file": str(target_stdout)},
        control_result={"stdout_file": str(control_stdout)},
        catalog_file=catalog_file,
    )

    assert summary is not None
    assert not summary.passed
    assert any("Record comparison errored" in error for error in summary.errors)
    assert any("Too many open files" in error for error in summary.errors)
    # The degraded summary must survive every downstream consumer: the
    # JSON GitHub output and both report surfaces.
    payload = summary.to_dict()
    assert json.dumps(payload)
    assert payload["passed"] is False
    # Errored is distinct from failed: the CLI treats it as inconclusive
    # (fails the run, does not claim a regression).
    assert summary.errored is True
    assert payload["errored"] is True


def test_missing_pk_record_examples_are_capped_but_count_is_full() -> None:
    """Full copies of the first few offending records ride along for the report."""
    records = _records(
        "users",
        {"id": 1, "n": "ok"},
        *({"n": f"no-pk-{i}"} for i in range(8)),
    )

    result = check_pk_uniqueness(records, USERS_PKS)

    stream_result = result.stream_results["users"]
    assert stream_result.records_missing_pk == 8
    assert len(stream_result.records_missing_pk_examples) == 5
    assert stream_result.records_missing_pk_examples[0]["data"] == {"n": "no-pk-0"}
    # Records that do carry their PK are not swept into the examples.
    assert not any(
        example["data"].get("id") == 1
        for example in stream_result.records_missing_pk_examples
    )


# ---------------------------------------------------------------------------
# review follow-ups: single-parse splitting, bounded PK components,
# deterministic duplicate examples, markdown-safe stream names
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_split_records_per_stream_skips_malformed_record_lines(tmp_path: Path) -> None:
    """The splitter routes on a plain JSON parse; junk shapes must not crash it."""
    stdout = tmp_path / "stdout.log"
    stdout.write_text(
        "\n".join(
            [
                json.dumps({"type": "RECORD", "record": "not-an-object"}),
                json.dumps({"type": "RECORD", "record": {"no_stream": True}}),
                json.dumps({"type": "RECORD", "record": {"stream": 42}}),
                json.dumps({"type": "RECORD"}),
                _record("users", {"id": 1}).model_dump_json(),
            ]
        )
    )

    record_files = split_records_per_stream(stdout)

    assert set(record_files) == {"users"}
    assert len(record_files["users"].read_text().splitlines()) == 1


@pytest.mark.unit
def test_protocol_invalid_record_lines_reach_the_file_but_not_the_comparison(
    tmp_path: Path,
) -> None:
    """Splitting validates shape only; the reader does the one full protocol
    validation per record. A RECORD-typed line that fails it stays in the
    per-stream artifact (an honest copy of the connector output) and is
    dropped from the comparison."""
    invalid = json.dumps({"type": "RECORD", "record": {"stream": "users"}})
    stdout = tmp_path / "stdout.log"
    stdout.write_text(
        "\n".join([invalid, _record("users", {"id": 1}).model_dump_json()])
    )

    record_files = split_records_per_stream(stdout)

    assert len(record_files["users"].read_text().splitlines()) == 2
    summary = run_record_comparisons_from_files(record_files, record_files, USERS_PKS)
    assert summary.passed
    counts = summary.to_dict()["checks"]["record_counts"]["streams"]["users"]
    assert counts["control_count"] == 1


@pytest.mark.unit
def test_oversized_pk_components_are_bounded_but_stay_distinct() -> None:
    """Truncation alone would merge two distinct oversized PKs; the digest
    suffix keeps equality exact while the component stays bounded."""
    prefix = ["x" * 600]
    distinct = _records(
        "users",
        {"id": [*prefix, "a"], "n": "1"},
        {"id": [*prefix, "b"], "n": "2"},
    )

    result = check_pk_uniqueness(distinct, USERS_PKS)

    assert result.passed

    duplicated = _records("users", {"id": [*prefix, "a"]}, {"id": [*prefix, "a"]})
    result = check_pk_uniqueness(duplicated, USERS_PKS)
    assert not result.passed
    (dup_pk,) = result.stream_results["users"].duplicate_pks
    assert "…sha256:" in dup_pk[0]
    assert len(dup_pk[0]) < comparators.MAX_PK_COMPONENT_CHARS + 30


@pytest.mark.unit
def test_duplicate_pk_field_diff_example_is_deterministic() -> None:
    """A duplicated PK's records are matched as a multiset, so the example
    names the record the target dropped, whatever the emission order."""
    control = _records("users", {"id": 1, "name": "first"}, {"id": 1, "name": "second"})
    target = _records("users", {"id": 1, "name": "second"})

    for control_order in (control, {"users": control["users"][::-1]}):
        summary = run_record_comparisons(control_order, target, USERS_PKS)

        assert summary.field_comparison is not None
        assert not summary.field_comparison.passed
        (example,) = _users_record_diff(summary).records_with_value_diff
        assert [r["data"]["name"] for r in example["control"]] == ["first"]
        assert example["target"] == []
        assert summary.control_pk_uniqueness is not None
        assert summary.control_pk_uniqueness.passed
        assert not summary.passed


@pytest.mark.unit
def test_report_escapes_pipes_in_stream_names(tmp_path: Path) -> None:
    records = _records("a|b", {"id": 1})
    summary = run_record_comparisons(records, records, {"a|b": [["id"]]})

    report_path = generate_action_test_comparison_report(
        target_image="airbyte/source-test:2.0.0",
        control_image="airbyte/source-test:1.0.0",
        command="read",
        target_result={"success": True, "exit_code": 0},
        control_result={"success": True, "exit_code": 0},
        output_dir=tmp_path,
        record_comparison=summary.to_dict(),
    )

    row = next(
        line for line in report_path.read_text().splitlines() if line.startswith("| a")
    )
    assert "a\\|b" in row
    # Eight unescaped pipes delimit the table's seven columns.
    assert len(re.findall(r"(?<!\\)\|", row)) == 8


def test_missing_and_extra_pks_are_deterministically_ordered() -> None:
    """Set differences vary per process under hash randomization; the lists
    must come back in one fixed order so a capped report shows the same
    subset on every re-run. Sorted by repr because PK tuples mix types."""
    control = _records("users", {"id": 3}, {"id": 1}, {"id": "x"}, {"id": 2})
    target = _records("users", {"id": 9}, {"id": 8})

    result = compare_primary_keys(control, target, USERS_PKS)

    stream_result = result.stream_results["users"]
    assert stream_result.missing_pks == sorted(stream_result.missing_pks, key=repr)
    assert stream_result.missing_pks == [("x",), (1,), (2,), (3,)]
    assert stream_result.extra_pks == [(8,), (9,)]


def test_records_differing_only_in_excluded_fields_match() -> None:
    """The equality fast path must strip the excluded paths before comparing,
    or an emitted_at difference (which every real pair has) would defeat it
    and send every identical record through DeepDiff anyway."""
    control = {
        "users": [
            AirbyteMessage(
                type=AirbyteMessageType.RECORD,
                record=AirbyteRecordMessage(
                    stream="users", data={"id": 1, "n": "a"}, emitted_at=1
                ),
            )
        ]
    }
    target = {
        "users": [
            AirbyteMessage(
                type=AirbyteMessageType.RECORD,
                record=AirbyteRecordMessage(
                    stream="users", data={"id": 1, "n": "a"}, emitted_at=2
                ),
            )
        ]
    }

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed
    assert summary.field_comparison is not None
    diff = summary.field_comparison.stream_results["users"].record_diff
    assert diff is not None and not diff.has_diff


def test_value_diff_examples_are_selected_deterministically() -> None:
    """More diffs than the example cap: the kept examples must be the same
    ones on every run (sorted PK order), not whatever set iteration yields."""
    control = _records("users", *({"id": i, "v": "a"} for i in range(20)))
    target = _records("users", *({"id": i, "v": "b"} for i in range(20)))

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.field_comparison is not None
    diff = summary.field_comparison.stream_results["users"].record_diff
    assert diff is not None
    kept = [example["pk"] for example in diff.records_with_value_diff]
    assert kept == sorted(kept, key=repr)
    assert diff.records_with_value_diff_count == 20


# ---------------------------------------------------------------------------
# duplicated PKs: the two versions' records for one PK are compared as
# multisets, not first record against first record
# ---------------------------------------------------------------------------


def _users_record_diff(summary: Any) -> Any:
    assert summary.field_comparison is not None
    diff = summary.field_comparison.stream_results["users"].record_diff
    assert diff is not None
    return diff


@pytest.mark.unit
def test_duplicate_pk_rows_in_swapped_order_are_not_a_value_diff() -> None:
    """The PayPal shape: a hold (T1110) and a release (T1111) row per
    transaction id, emitted in the other order by the target."""
    control = _records(
        "users",
        {"id": 1, "code": "T1111", "updated": "2026-10-02"},
        {"id": 1, "code": "T1110", "updated": "2026-10-01"},
        {"id": 2, "code": "T1111", "updated": "2026-10-04"},
        {"id": 2, "code": "T1110", "updated": "2026-10-03"},
    )
    target = _records(
        "users",
        {"id": 1, "code": "T1110", "updated": "2026-10-01"},
        {"id": 2, "code": "T1110", "updated": "2026-10-03"},
        {"id": 1, "code": "T1111", "updated": "2026-10-02"},
        {"id": 2, "code": "T1111", "updated": "2026-10-04"},
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed
    assert summary.errors == []
    diff = _users_record_diff(summary)
    assert not diff.has_diff
    assert _split_of(summary, "target_pk_uniqueness") == (2, 0, 0)


@pytest.mark.unit
def test_duplicate_pk_rows_differing_only_in_emitted_at_match() -> None:
    control = {
        "users": [
            AirbyteMessage(
                type=AirbyteMessageType.RECORD,
                record=AirbyteRecordMessage(
                    stream="users", data={"id": 1, "code": code}, emitted_at=1
                ),
            )
            for code in ("T1110", "T1111")
        ]
    }
    target = {
        "users": [
            AirbyteMessage(
                type=AirbyteMessageType.RECORD,
                record=AirbyteRecordMessage(
                    stream="users", data={"id": 1, "code": code}, emitted_at=99
                ),
            )
            for code in ("T1111", "T1110")
        ]
    }

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed
    assert not _users_record_diff(summary).has_diff


@pytest.mark.unit
def test_a_duplicate_pk_group_whose_rows_differ_is_one_value_diff() -> None:
    control = _records(
        "users",
        {"id": 1, "code": "T1110", "amount": 5},
        {"id": 1, "code": "T1111", "amount": 5},
        {"id": 2, "code": "T1110", "amount": 7},
        {"id": 2, "code": "T1111", "amount": 7},
    )
    target = _records(
        "users",
        {"id": 1, "code": "T1111", "amount": 5},
        {"id": 1, "code": "T1110", "amount": 500},
        {"id": 2, "code": "T1110", "amount": 7},
        {"id": 2, "code": "T1111", "amount": 7},
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    diff = _users_record_diff(summary)
    # Counted per PK, as for single records: one PK differs, not two rows.
    assert diff.records_with_value_diff_count == 1
    (example,) = diff.records_with_value_diff
    assert example["pk"] == (1,)
    # The example shows each side's unmatched records; the matching T1111
    # rows are not in it.
    assert [r["data"] for r in example["control"]] == [
        {"id": 1, "code": "T1110", "amount": 5}
    ]
    assert [r["data"] for r in example["target"]] == [
        {"id": 1, "code": "T1110", "amount": 500}
    ]
    assert "values_changed" in example["diff"]
    assert not summary.field_comparison.passed

    payload = summary.to_dict()
    users = payload["checks"]["field_values"]["streams"]["users"]
    assert users["records_with_value_diff"] == 1
    assert users["value_diff_examples"][0]["pk"] == [1]
    assert users["value_diff_examples"][0]["diff"]
    json.dumps(payload)


@pytest.mark.unit
def test_every_differing_duplicate_pk_group_counts_once() -> None:
    control = _records(
        "users", *({"id": i, "code": c, "v": "a"} for i in (1, 2) for c in ("x", "y"))
    )
    target = _records(
        "users", *({"id": i, "code": c, "v": "b"} for i in (1, 2) for c in ("x", "y"))
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    diff = _users_record_diff(summary)
    assert diff.records_with_value_diff_count == 2
    assert [example["pk"] for example in diff.records_with_value_diff] == [(1,), (2,)]
    assert all(len(example["control"]) == 2 for example in diff.records_with_value_diff)


@pytest.mark.unit
def test_a_record_lost_inside_a_duplicated_pk_fails_next_to_a_new_pk() -> None:
    """The control emits PK 7 as a T1110 and a T1111 row; the target emits
    PK 7 once and a new PK 8. Counts match and every control PK is present,
    so only the group rule can catch the dropped T1111 row."""
    control = _records("users", {"id": 7, "code": "T1110"}, {"id": 7, "code": "T1111"})
    target = _records("users", {"id": 7, "code": "T1110"}, {"id": 8, "code": "T1110"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert summary.count_comparison.passed
    assert summary.pk_presence is not None and summary.pk_presence.passed
    assert summary.control_pk_uniqueness.passed
    # Not "fixed": the target dropped a record of the duplicated PK.
    assert _split_of(summary, "control_pk_uniqueness") == (0, 0, 0)
    assert (
        summary.control_pk_uniqueness.stream_results["users"].lost_duplicate_pk_count
        == 1
    )
    assert not summary.field_comparison.passed
    diff = _users_record_diff(summary)
    assert diff.records_with_value_diff_count == 1
    (example,) = diff.records_with_value_diff
    assert example["pk"] == (7,)
    assert [r["data"] for r in example["control"]] == [{"id": 7, "code": "T1111"}]
    assert example["target"] == []
    assert example["note"] == "the target no longer emits 1 record of this PK"
    assert "iterable_item_removed" in example["diff"]

    (json_example,) = summary.to_dict()["checks"]["field_values"]["streams"]["users"][
        "value_diff_examples"
    ]
    assert json_example["note"] == "the target no longer emits 1 record of this PK"
    assert list(json_example["diff"]["iterable_item_removed"]) == ["root[0]"]


@pytest.mark.unit
def test_a_distinct_record_lost_from_a_group_of_three_fails() -> None:
    control = _records(
        "users", {"id": 7, "c": "a"}, {"id": 7, "c": "b"}, {"id": 7, "c": "c"}
    )
    target = _records("users", {"id": 7, "c": "b"}, {"id": 7, "c": "a"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    # The shortfall is within the duplicate rows dropped (2 in control, 1 in
    # target), so the count only warns, and says no more than that; the field
    # values are what catch that the dropped row was not a copy.
    assert summary.count_comparison.passed
    assert summary.count_comparison.warnings == [
        "Stream users has 1 fewer record in target, within the duplicate rows the "
        "target dropped (2 in control, 1 in target); field values check that the "
        "dropped rows were copies"
    ]
    assert not summary.field_comparison.passed
    assert summary.errors == ["Stream users has record differences"]
    (example,) = _users_record_diff(summary).records_with_value_diff
    assert [r["data"]["c"] for r in example["control"]] == ["c"]
    assert example["target"] == []
    assert example["note"] == "the target no longer emits 1 record of this PK"


@pytest.mark.unit
def test_identical_copies_collapsed_by_the_target_pass_at_field_level() -> None:
    control = _records("users", {"id": 7, "c": "a"}, {"id": 7, "c": "a"})
    target = _records("users", {"id": 7, "c": "a"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.field_comparison.passed
    assert not _users_record_diff(summary).has_diff
    assert _split_of(summary, "control_pk_uniqueness") == (0, 0, 1)


@pytest.mark.unit
def test_a_lost_record_is_reported_next_to_collapsed_copies() -> None:
    """Collapsed copies pass; a distinct record dropped with them does not,
    and only the lost one is listed."""
    control = _records(
        "users",
        {"id": 7, "c": "a"},
        {"id": 7, "c": "a"},
        {"id": 7, "c": "a"},
        {"id": 7, "c": "b"},
    )
    target = _records("users", {"id": 7, "c": "a"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    (example,) = _users_record_diff(summary).records_with_value_diff
    assert [r["data"]["c"] for r in example["control"]] == ["b"]
    assert example["note"] == "the target no longer emits 1 record of this PK"


ADDED_COPIES_WARNING = (
    "Stream users: 1 duplicated PK value(s) emit {copies} more identical "
    "{noun} in target than in control"
)


@pytest.mark.unit
def test_identical_copies_added_under_a_duplicated_pk_warn(tmp_path: Path) -> None:
    """Control `7: A, B`, target `(A, B) x 50`: offset pagination on a live
    read can repeat rows, so 98 extra identical copies warn and pass."""
    rows = [{"id": 7, "event": "A"}, {"id": 7, "event": "B"}]
    control = _records("users", *rows)
    target = _records("users", *(rows * 50))

    in_memory = run_record_comparisons(control, target, USERS_PKS)
    from_files = run_record_comparisons_from_files(
        _write_record_files(tmp_path / "control", control),
        _write_record_files(tmp_path / "target", target),
        USERS_PKS,
    )

    assert from_files.to_dict() == in_memory.to_dict()
    warning = ADDED_COPIES_WARNING.format(copies=98, noun="copies")
    for summary in (in_memory, from_files):
        assert summary.passed
        assert summary.errors == []
        assert summary.field_comparison.passed
        assert summary.field_comparison.warnings == [warning]
        assert summary.field_comparison.message == (
            "All records match, apart from identical copies the target added"
        )
        diff = _users_record_diff(summary)
        assert not diff.has_diff
        assert (diff.added_copy_count, diff.added_copy_pk_count) == (98, 1)
        assert diff.added_copy_pks == {(7,): 98}
        assert summary.field_comparison.stream_results["users"].message == warning
    users = in_memory.to_dict()["checks"]["field_values"]["streams"]["users"]
    assert (users["added_copy_count"], users["added_copy_pk_count"]) == (98, 1)
    assert users["records_with_value_diff"] == 0


@pytest.mark.unit
def test_more_exact_copies_in_the_target_warn_as_added_copies() -> None:
    control = _records("users", *[{"id": 7, "c": "a"}] * 2)
    target = _records("users", *[{"id": 7, "c": "a"}] * 4)

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed
    assert summary.count_comparison.passed
    # Duplicated in both versions: PK integrity calls it pre-existing.
    assert summary.target_pk_uniqueness.passed
    assert _split_of(summary, "target_pk_uniqueness") == (1, 0, 0)
    assert summary.field_comparison.passed
    assert summary.field_comparison.warnings == [
        ADDED_COPIES_WARNING.format(copies=2, noun="copies")
    ]
    assert _users_record_diff(summary).records_with_value_diff == []


@pytest.mark.unit
def test_a_new_record_emitted_twice_under_a_duplicated_pk_is_one_added_copy() -> None:
    """The first of two new equal records is an added record; the second is
    a copy of it, and warns."""
    control = _records("users", {"id": 7, "c": "a"}, {"id": 7, "c": "b"})
    target = _records(
        "users",
        {"id": 7, "c": "a"},
        {"id": 7, "c": "b"},
        {"id": 7, "c": "new"},
        {"id": 7, "c": "new"},
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed
    assert _users_record_diff(summary).added_copy_count == 1
    assert summary.field_comparison.warnings == [
        ADDED_COPIES_WARNING.format(copies=1, noun="copy")
    ]


@pytest.mark.unit
def test_a_whole_float_counts_as_a_copy_of_the_int_it_equals() -> None:
    """`1` and `1.0` are one value in the matching key, as in the pairing."""
    control = _records("users", *[{"id": 7, "v": 1.0}] * 2)
    target = _records(
        "users", {"id": 7, "v": 1.0}, {"id": 7, "v": 1.0}, {"id": 7, "v": 1}
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed
    assert _users_record_diff(summary).added_copy_count == 1


@pytest.mark.unit
def test_a_lost_record_next_to_added_copies_still_fails() -> None:
    # Same PK: B is gone and A is repeated, so both sides have leftovers.
    control = _records("users", {"id": 7, "c": "A"}, {"id": 7, "c": "B"})
    target = _records("users", *[{"id": 7, "c": "A"}] * 3)

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    (example,) = _users_record_diff(summary).records_with_value_diff
    assert [r["data"]["c"] for r in example["control"]] == ["B"]

    # Other PKs of the stream: PK 7 only warns, PK 8's lost row fails it.
    control = _records(
        "users",
        {"id": 7, "c": "A"},
        {"id": 7, "c": "B"},
        {"id": 8, "c": "x"},
        {"id": 8, "c": "y"},
    )
    target = _records(
        "users",
        *([{"id": 7, "c": "A"}, {"id": 7, "c": "B"}] * 2),
        {"id": 8, "c": "x"},
        {"id": 8, "c": "x"},
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert not summary.field_comparison.passed
    diff = _users_record_diff(summary)
    assert [example["pk"] for example in diff.records_with_value_diff] == [(8,)]
    assert diff.added_copy_pks == {(7,): 2}
    assert summary.field_comparison.warnings == [
        ADDED_COPIES_WARNING.format(copies=2, noun="copies")
    ]
    assert summary.field_comparison.stream_results["users"].message == (
        "Stream users has record differences; "
        + ADDED_COPIES_WARNING.format(copies=2, noun="copies")
    )


@pytest.mark.unit
def test_the_canonical_form_agrees_with_the_single_pair_comparison() -> None:
    """Whole floats and bools key as the ints they equal, and list order is
    ignored, at any depth, as `==` and DeepDiff's `ignore_order` do; other
    values keep their own key."""

    def key(value: Any) -> str:
        return comparators._canonical_record({"v": value}, ["emitted_at"])

    assert key(1) == key(1.0) == key(True)
    assert key(0) == key(0.0) == key(False) == key(-0.0)
    assert key({"n": [1, {"m": True}]}) == key({"n": [{"m": 1}, 1.0]})
    assert key([1, 2]) == key([2, 1])
    assert key([[3, 1], {"a": [2, 1]}]) == key([{"a": [1, 2]}, [1, 3]])
    assert key([1, "1", None, {"a": 1}]) == key([{"a": 1}, None, "1", 1])
    assert key(1.5) != key(1)
    assert key("1") != key(1)
    assert key(None) != key(0)
    # Repetition still counts; `_record_group_diff` judges such leftovers.
    assert key([1, 1, 2]) != key([1, 2])


def _tagged(seq: int, tags: list[int], **fields: Any) -> dict[str, Any]:
    return {"id": 7, "seq": seq, "tags": tags, **fields}


@pytest.mark.unit
def test_a_change_past_the_example_cap_is_not_hidden_by_list_order() -> None:
    """30 records a side under one PK; every target record reverses a nested
    list, and record 9 also changes a value. List order is not a difference,
    so only record 9 is left over, and it fails."""
    control = _records(
        "users", *(_tagged(i, [i, i + 1000], amount=1) for i in range(30))
    )
    target = _records(
        "users",
        *(_tagged(i, [i + 1000, i], amount=2 if i == 9 else 1) for i in range(30)),
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert not summary.field_comparison.passed
    (example,) = _users_record_diff(summary).records_with_value_diff
    assert [r["data"]["seq"] for r in example["control"]] == [9]
    assert [r["data"]["seq"] for r in example["target"]] == [9]
    assert "values_changed" in example["diff"]
    assert "note" not in example


@pytest.mark.unit
def test_a_group_differing_only_in_list_order_passes() -> None:
    control = _records("users", *(_tagged(i, [i, i + 1000]) for i in range(30)))
    target = _records("users", *(_tagged(i, [i + 1000, i]) for i in range(30)))

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed
    assert not _users_record_diff(summary).has_diff


@pytest.mark.unit
def test_a_capped_group_fails_closed_when_the_shown_records_diff_empty() -> None:
    """25 records a side differ only in a repeated list item, which DeepDiff
    ignores: the keys say they do not match, and past the cap the empty diff
    of the shown ones cannot clear the group."""
    control = _records("users", *(_tagged(i, [1, 1]) for i in range(25)))
    target = _records("users", *(_tagged(i, [1]) for i in range(25)))

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.field_comparison.passed
    (example,) = _users_record_diff(summary).records_with_value_diff
    assert example["diff"] == {}
    cap = comparators.MAX_GROUP_EXAMPLE_RECORDS
    assert example["note"] == (
        f"25 control and 25 target records of this PK do not match (first {cap} "
        "of each shown); the shown ones differ only in repeated list items, "
        "which the diff ignores, so the difference may be past them"
    )

    # Under the cap the diff covers every leftover, and repetition alone
    # passes, as it does for a single pair.
    control = _records("users", *(_tagged(i, [1, 1]) for i in range(3)))
    target = _records("users", *(_tagged(i, [1]) for i in range(3)))
    assert run_record_comparisons(control, target, USERS_PKS).field_comparison.passed
    assert run_record_comparisons(
        _records("users", _tagged(0, [1, 1])),
        _records("users", _tagged(0, [1])),
        USERS_PKS,
    ).field_comparison.passed


@pytest.mark.unit
def test_a_collapse_with_a_reordered_nested_list_is_fixed() -> None:
    """The control emits one record twice; the target emits it once with a
    nested list in another order. That is a collapse: "fixed", and green."""
    record = {"id": 7, "meta": {"tags": ["b", "a"], "n": [3, 1, 2]}}
    reordered = {"id": 7, "meta": {"tags": ["a", "b"], "n": [1, 2, 3]}}

    summary = run_record_comparisons(
        _records("users", record, record), _records("users", reordered), USERS_PKS
    )

    assert summary.passed
    users = summary.control_pk_uniqueness.stream_results["users"]
    assert (users.fixed_duplicate_pk_count, users.lost_duplicate_pk_count) == (1, 0)
    assert summary.control_pk_uniqueness.message == (
        "Duplicate primary keys in control fixed in target (not a regression)"
    )


@pytest.mark.unit
def test_whole_floats_and_bools_match_their_ints_inside_a_group() -> None:
    """The group path matches what the single-pair path's `==` matches: `1`,
    `1.0` and `True` are one value, nested too, whatever the emission order."""
    control = _records(
        "users",
        {"id": 7, "v": 1, "flag": True, "meta": {"n": [1, 2]}},
        {"id": 7, "v": 2, "flag": False, "meta": {"n": [3]}},
    )
    target = _records(
        "users",
        {"id": 7, "v": 2.0, "flag": 0, "meta": {"n": [3.0]}},
        {"id": 7, "v": 1.0, "flag": 1, "meta": {"n": [1.0, 2]}},
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed
    assert not _users_record_diff(summary).has_diff

    # And a real change next to them is still found.
    target = _records(
        "users",
        {"id": 7, "v": 2.0, "flag": 0, "meta": {"n": [3.5]}},
        {"id": 7, "v": 1.0, "flag": 1, "meta": {"n": [1.0, 2]}},
    )
    summary = run_record_comparisons(control, target, USERS_PKS)
    (example,) = _users_record_diff(summary).records_with_value_diff
    assert [r["data"]["meta"] for r in example["control"]] == [{"n": [3]}]
    assert [r["data"]["meta"] for r in example["target"]] == [{"n": [3.5]}]


@pytest.mark.unit
def test_a_group_example_is_capped_and_its_note_keeps_the_full_counts() -> None:
    cap = comparators.MAX_GROUP_EXAMPLE_RECORDS
    control = _records("users", *({"id": 7, "seq": i} for i in range(1_235)))
    target = _records("users", {"id": 7, "seq": 0})

    summary = run_record_comparisons(control, target, USERS_PKS)

    (example,) = _users_record_diff(summary).records_with_value_diff
    assert len(example["control"]) == cap
    assert example["target"] == []
    assert len(example["diff"]["iterable_item_removed"]) == cap
    assert example["note"] == (
        f"the target no longer emits 1,234 records of this PK (first {cap} shown)"
    )
    users = summary.to_dict()["checks"]["field_values"]["streams"]["users"]
    assert users["value_diff_examples"][0]["note"] == example["note"]

    # Both sides left over: each side is capped, and the note counts both.
    control = _records("users", *({"id": 7, "seq": i} for i in range(30)))
    target = _records("users", *({"id": 7, "seq": i, "new": 1} for i in range(25)))

    summary = run_record_comparisons(control, target, USERS_PKS)

    (example,) = _users_record_diff(summary).records_with_value_diff
    assert (len(example["control"]), len(example["target"])) == (cap, cap)
    assert example["note"] == (
        "30 control and 25 target records of this PK do not match "
        f"(first {cap} of each shown)"
    )


@pytest.mark.unit
def test_a_distinct_record_added_to_a_pre_existing_duplicate_passes() -> None:
    control = _records("users", {"id": 7, "c": "a"}, {"id": 7, "c": "b"})
    target = _records(
        "users", {"id": 7, "c": "b"}, {"id": 7, "c": "c"}, {"id": 7, "c": "a"}
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.passed
    assert summary.field_comparison.passed
    assert not _users_record_diff(summary).has_diff
    assert summary.errors == []


@pytest.mark.unit
def test_a_single_record_pk_the_target_duplicates_fails_only_on_pk_integrity() -> None:
    control = _records("users", {"id": 7, "c": "a"})
    target = _records("users", {"id": 7, "c": "a"}, {"id": 7, "c": "a"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert summary.field_comparison.passed
    assert not _users_record_diff(summary).has_diff
    assert not summary.target_pk_uniqueness.passed
    assert summary.errors == [
        "Stream users has 1 new duplicate primary key value(s) in target "
        "(not duplicated in control)"
    ]


@pytest.mark.unit
def test_unmatched_records_on_both_sides_of_a_duplicated_pk_still_fail() -> None:
    control = _records(
        "users", {"id": 1, "c": "a"}, {"id": 1, "c": "b"}, {"id": 1, "c": "c"}
    )
    target = _records("users", {"id": 1, "c": "a"}, {"id": 1, "c": "CHANGED"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.field_comparison.passed
    diff = _users_record_diff(summary)
    assert diff.records_with_value_diff_count == 1
    (example,) = diff.records_with_value_diff
    assert sorted(r["data"]["c"] for r in example["control"]) == ["b", "c"]
    assert [r["data"]["c"] for r in example["target"]] == ["CHANGED"]
    # A changed record has both sides to show; no note is needed.
    assert "note" not in example
    users = summary.to_dict()["checks"]["field_values"]["streams"]["users"]
    assert "note" not in users["value_diff_examples"][0]


@pytest.mark.unit
def test_a_both_sides_example_leaves_out_the_controls_collapsed_copies() -> None:
    """Control {a, a, b} against target {a, b'}: the second `a` is a collapsed
    copy, not part of the change, so only `b` is shown against `b'`."""
    control = _records(
        "users", {"id": 1, "c": "a"}, {"id": 1, "c": "a"}, {"id": 1, "c": "b"}
    )
    target = _records("users", {"id": 1, "c": "a"}, {"id": 1, "c": "b-CHANGED"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.field_comparison.passed
    (example,) = _users_record_diff(summary).records_with_value_diff
    assert [r["data"]["c"] for r in example["control"]] == ["b"]
    assert [r["data"]["c"] for r in example["target"]] == ["b-CHANGED"]
    assert list(example["diff"]) == ["values_changed"]
    assert "note" not in example


@pytest.mark.unit
def test_a_collapsed_copy_next_to_an_added_copy_is_a_repeat_not_a_change() -> None:
    """Control {A, A, B} against target {A, B, B}: one copy of A collapsed and
    one copy of B added, as an offset-pagination repeat that moved to another
    row. Nothing was lost or changed, so it passes and warns."""
    a, b = {"id": 7, "c": "A"}, {"id": 7, "c": "B"}

    summary = run_record_comparisons(
        _records("users", a, a, b), _records("users", a, b, b), USERS_PKS
    )

    assert summary.passed
    assert summary.field_comparison.passed
    diff = _users_record_diff(summary)
    assert not diff.has_diff
    assert (diff.added_copy_count, diff.added_copy_pks) == (1, {(7,): 1})
    assert summary.field_comparison.warnings == [
        ADDED_COPIES_WARNING.format(copies=1, noun="copy")
    ]


@pytest.mark.unit
def test_a_both_sides_example_keeps_the_control_leftovers_when_all_are_copies() -> None:
    """Control {a, a} against target {a, x}: the leftover `a` is a copy, but
    with nothing lost there is nothing else to show against `x`. Still a
    difference, as before."""
    control = _records("users", {"id": 1, "c": "a"}, {"id": 1, "c": "a"})
    target = _records("users", {"id": 1, "c": "a"}, {"id": 1, "c": "x"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.field_comparison.passed
    (example,) = _users_record_diff(summary).records_with_value_diff
    assert [r["data"]["c"] for r in example["control"]] == ["a"]
    assert [r["data"]["c"] for r in example["target"]] == ["x"]


@pytest.mark.unit
def test_duplicate_pk_group_example_is_deterministic() -> None:
    """The unmatched records are listed in a sorted order, not emission order."""
    control = _records(
        "users", {"id": 1, "c": "z"}, {"id": 1, "c": "y"}, {"id": 1, "c": "x"}
    )
    target = _records(
        "users", {"id": 1, "c": "q"}, {"id": 1, "c": "p"}, {"id": 1, "c": "r"}
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    (example,) = _users_record_diff(summary).records_with_value_diff
    assert [r["data"]["c"] for r in example["control"]] == ["x", "y", "z"]
    assert [r["data"]["c"] for r in example["target"]] == ["p", "q", "r"]


@pytest.mark.unit
def test_a_single_record_pk_next_to_a_duplicated_one_is_compared_as_before() -> None:
    control = _records(
        "users", {"id": 1, "c": "a"}, {"id": 1, "c": "b"}, {"id": 2, "c": "one"}
    )
    target = _records(
        "users", {"id": 1, "c": "b"}, {"id": 1, "c": "a"}, {"id": 2, "c": "MUTATED"}
    )

    summary = run_record_comparisons(control, target, USERS_PKS)

    diff = _users_record_diff(summary)
    assert diff.records_with_value_diff_count == 1
    (example,) = diff.records_with_value_diff
    assert example["pk"] == (2,)
    assert example["control"]["data"] == {"id": 2, "c": "one"}
    assert example["target"]["data"] == {"id": 2, "c": "MUTATED"}


# ---------------------------------------------------------------------------
# composite and nested PKs: the duplicate split and the group matching key on
# the whole PK tuple, whatever its shape
# ---------------------------------------------------------------------------

COMPOSITE_PKS = {"balances": [["account"], ["day"]]}
NESTED_PKS = {"readings": [["location", "id"], ["day"]]}


def _balance(account: str, day: str, **fields: Any) -> dict[str, Any]:
    return {"account": account, "day": day, **fields}


def _reading(location: str, day: str, **fields: Any) -> dict[str, Any]:
    return {"location": {"id": location, "zone": "z1"}, "day": day, **fields}


def _stream_split(summary: Any, check: str, stream: str) -> tuple[int, int, int]:
    result = getattr(summary, check).stream_results[stream]
    return (
        result.pre_existing_duplicate_pk_count,
        result.new_duplicate_pk_count,
        result.fixed_duplicate_pk_count,
    )


@pytest.mark.unit
@pytest.mark.parametrize(
    "stream,pks,row",
    [
        pytest.param("balances", COMPOSITE_PKS, _balance, id="composite"),
        pytest.param("readings", NESTED_PKS, _reading, id="nested"),
    ],
)
def test_duplicate_split_keys_on_the_whole_pk(stream, pks, row) -> None:
    # (a, d1) is duplicated in both versions, (a, d2) in the control only,
    # (b, d1) in the target only. Sharing one component is not a duplicate.
    control = _records(
        stream,
        *[row("a", "d1")] * 2,
        *[row("a", "d2")] * 2,
        row("b", "d1"),
        row("b", "d2"),
    )
    target = _records(
        stream,
        *[row("a", "d1")] * 2,
        row("a", "d2"),
        *[row("b", "d1")] * 2,
        row("b", "d2"),
    )

    summary = run_record_comparisons(control, target, pks)

    for check in ("control_pk_uniqueness", "target_pk_uniqueness"):
        assert _stream_split(summary, check, stream) == (1, 1, 1)
    control_result = summary.control_pk_uniqueness.stream_results[stream]
    target_result = summary.target_pk_uniqueness.stream_results[stream]
    assert sorted(control_result.duplicate_pks) == [("a", "d1"), ("a", "d2")]
    assert sorted(target_result.duplicate_pks) == [("a", "d1"), ("b", "d1")]
    assert control_result.duplicate_row_count == 2
    assert target_result.duplicate_row_count == 2
    # Only the new (b, d1) fails; the collapsed (a, d2) copy is no diff.
    assert summary.errors == [
        f"Stream {stream} has 1 new duplicate primary key value(s) in target "
        "(not duplicated in control)"
    ]
    assert summary.field_comparison.passed
    examples = summary.to_dict()["checks"]["pk_uniqueness_target"]["streams"][stream][
        "duplicate_pk_examples"
    ]
    assert {"pk": ["b", "d1"], "count": 2} in examples


@pytest.mark.unit
@pytest.mark.parametrize(
    "stream,pks,row",
    [
        pytest.param("balances", COMPOSITE_PKS, _balance, id="composite"),
        pytest.param("readings", NESTED_PKS, _reading, id="nested"),
    ],
)
def test_duplicate_pk_groups_match_as_multisets_under_any_pk_shape(
    stream, pks, row
) -> None:
    control = _records(
        stream,
        row("a", "d1", code="T1110"),
        row("a", "d1", code="T1111"),
        row("a", "d2", code="T1110"),
        row("a", "d2", code="T1111"),
    )
    swapped = _records(
        stream,
        row("a", "d1", code="T1111"),
        row("a", "d2", code="T1111"),
        row("a", "d1", code="T1110"),
        row("a", "d2", code="T1110"),
    )

    summary = run_record_comparisons(control, swapped, pks)

    assert summary.passed
    assert not summary.field_comparison.stream_results[stream].record_diff.has_diff

    # The target drops (a, d2)'s T1111 row and emits a new (b, d1) instead:
    # counts match, every control PK is present, and the lost row fails.
    lossy = _records(
        stream,
        row("a", "d1", code="T1111"),
        row("a", "d1", code="T1110"),
        row("a", "d2", code="T1110"),
        row("b", "d1", code="T1110"),
    )

    summary = run_record_comparisons(control, lossy, pks)

    assert not summary.passed
    assert summary.count_comparison.passed
    assert summary.pk_presence.passed
    record_diff = summary.field_comparison.stream_results[stream].record_diff
    assert record_diff.records_with_value_diff_count == 1
    (example,) = record_diff.records_with_value_diff
    assert example["pk"] == ("a", "d2")
    assert [r["data"] for r in example["control"]] == [row("a", "d2", code="T1111")]
    assert example["target"] == []
    assert example["note"] == "the target no longer emits 1 record of this PK"


# ---------------------------------------------------------------------------
# namespaces: the pipeline keys streams by name, so a name that repeats
# across namespaces must degrade to count-only, never to phantom failures
# ---------------------------------------------------------------------------


def _two_namespace_catalog_file(tmp_path: Path) -> Path:
    """`public.users` and `reporting.users`: the routine database-source case."""
    streams = [
        {
            "stream": {
                "name": "users",
                "namespace": namespace,
                "json_schema": {},
                "supported_sync_modes": ["full_refresh"],
                "source_defined_primary_key": [["id"]],
            },
            "sync_mode": "full_refresh",
            "destination_sync_mode": "append",
        }
        for namespace in ("public", "reporting")
    ]
    catalog_file = tmp_path / "configured_catalog.json"
    catalog_file.write_text(_configured_catalog(streams).model_dump_json())
    return catalog_file


def _namespaced_record(namespace: str, data: dict[str, Any]) -> AirbyteMessage:
    return AirbyteMessage(
        type=AirbyteMessageType.RECORD,
        record=AirbyteRecordMessage(
            stream="users", namespace=namespace, data=data, emitted_at=1
        ),
    )


def test_duplicate_stream_names_degrade_to_no_pk() -> None:
    """A name shared by two namespaces maps to None (count comparison only):
    applying either stream's PK to the merged records would report phantom
    duplicates on a run where nothing changed."""
    catalog = _configured_catalog(
        [
            {
                "stream": {
                    "name": "users",
                    "namespace": namespace,
                    "json_schema": {},
                    "supported_sync_modes": ["full_refresh"],
                    "source_defined_primary_key": [["id"]],
                },
                "sync_mode": "full_refresh",
                "destination_sync_mode": "append",
            }
            for namespace in ("public", "reporting")
        ]
        + [
            {
                "stream": {
                    "name": "orders",
                    "json_schema": {},
                    "supported_sync_modes": ["full_refresh"],
                    "source_defined_primary_key": [["id"]],
                },
                "sync_mode": "full_refresh",
                "destination_sync_mode": "append",
            }
        ]
    )

    assert duplicate_stream_names(catalog) == ["users"]
    primary_keys = get_primary_keys_per_stream(catalog)
    assert primary_keys["users"] is None
    # A unique name keeps its PK untouched.
    assert primary_keys["orders"] == [["id"]]


def test_identical_namespaced_output_passes_with_a_warning(tmp_path: Path) -> None:
    """The reviewer's repro: same table in two schemas, identical output on
    both sides, nothing changed — this must pass (count-only), not report
    phantom duplicate PKs and block a release."""
    catalog_file = _two_namespace_catalog_file(tmp_path)
    records = {
        "users": [
            _namespaced_record("public", {"id": 1, "n": "a"}),
            _namespaced_record("public", {"id": 2, "n": "b"}),
            _namespaced_record("reporting", {"id": 1, "n": "a"}),
            _namespaced_record("reporting", {"id": 3, "n": "c"}),
        ]
    }
    control_stdout = _write_stdout_file(tmp_path / "control" / "stdout.log", records)
    target_stdout = _write_stdout_file(tmp_path / "target" / "stdout.log", records)

    summary, skip_reason = _compare_read_records(
        target_result={"stdout_file": str(control_stdout)},
        control_result={"stdout_file": str(target_stdout)},
        catalog_file=catalog_file,
    )

    assert skip_reason is None
    assert summary is not None
    assert summary.passed
    assert not summary.errors
    assert "users" in summary.streams_without_pk
    # The degradation is loud: the summary says why the PK checks are off.
    assert any("more than one namespace" in warning for warning in summary.warnings)


def test_dropped_namespaced_records_still_fail_by_count(tmp_path: Path) -> None:
    """Count-only is a degradation, not a free pass: dropping one namespace's
    records still fails the merged count comparison."""
    catalog_file = _two_namespace_catalog_file(tmp_path)
    control = {
        "users": [
            _namespaced_record("public", {"id": 1, "n": "a"}),
            _namespaced_record("reporting", {"id": 1, "n": "a"}),
        ]
    }
    target = {"users": [_namespaced_record("public", {"id": 1, "n": "a"})]}
    control_stdout = _write_stdout_file(tmp_path / "control" / "stdout.log", control)
    target_stdout = _write_stdout_file(tmp_path / "target" / "stdout.log", target)

    summary, _skip_reason = _compare_read_records(
        target_result={"stdout_file": str(target_stdout)},
        control_result={"stdout_file": str(control_stdout)},
        catalog_file=catalog_file,
    )

    assert summary is not None
    assert not summary.passed
    assert any("fewer records" in error for error in summary.errors)


def test_in_memory_pk_lists_are_capped_but_counts_stay_exact() -> None:
    """The merged summary of a failing run keeps every stream's result alive
    through report generation; uncapped PK lists would break the
    "peak memory is the largest single stream" bound exactly on the runs
    that drop the most records."""
    total = MAX_EXAMPLE_PKS + 25
    control = _records("users", *[{"id": i} for i in range(total)])
    target = _records("users", {"id": -1})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.pk_presence is not None
    result = summary.pk_presence.stream_results["users"]
    assert result.missing_pk_count == total
    assert len(result.missing_pks) == MAX_EXAMPLE_PKS
    assert result.extra_pk_count == 1
    # The report and JSON surfaces state the exact totals, not the cap.
    payload = summary.to_dict()
    users = payload["checks"]["pk_presence"]["streams"]["users"]
    assert users["missing_pk_count"] == total


# ---------------------------------------------------------------------------
# DeepDiff private-variable handling
#
# DeepDiff drops every key beginning with `__` unless `ignore_private_variables`
# is False. A connector's own `__`-prefixed field is data it emitted, not a
# Python private, so on the default a record differing only in such a field
# compares equal and the difference is never counted.
# ---------------------------------------------------------------------------


@pytest.mark.unit
def test_a_dunder_field_value_diff_is_counted_on_a_pk_matched_stream() -> None:
    """Records matched by PK, differing only in a `__`-prefixed field.

    The fast path uses plain equality so this pair does reach DeepDiff; on the
    default it would come back empty and the stream would pass.
    """
    control = _records("users", {"id": 1, "__v": 1})
    target = _records("users", {"id": 1, "__v": 2})

    result = compare_all_records(control, target, USERS_PKS, directional=True)

    assert not result.passed
    assert result.stream_results["users"].record_diff.records_with_value_diff


@pytest.mark.unit
def test_a_dunder_field_value_diff_is_counted_on_a_stream_without_a_pk() -> None:
    """The no-PK path compares whole record lists order-independently."""
    control = _records("events", {"name": "a", "__typename": "Old"})
    target = _records("events", {"name": "a", "__typename": "New"})

    result = compare_all_records(control, target, {"events": None}, directional=True)

    assert not result.passed
    assert result.stream_results["events"].record_diff.records_with_value_diff


@pytest.mark.unit
def test_an_added_dunder_field_is_counted() -> None:
    """Not only a changed value: a `__`-prefixed field appearing is a diff too."""
    control = _records("users", {"id": 1})
    target = _records("users", {"id": 1, "__typename": "User"})

    result = compare_all_records(control, target, USERS_PKS, directional=True)

    assert not result.passed
    # The pair is PK-matched, so an added field lands in the value-diff tally
    # rather than in the one-sided lists. Asserted so the failure has to come
    # from the added `__typename` and not from the records failing to match up.
    assert result.stream_results["users"].record_diff.records_with_value_diff
