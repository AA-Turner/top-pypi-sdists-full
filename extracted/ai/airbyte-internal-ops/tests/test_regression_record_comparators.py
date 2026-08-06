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
def test_duplicate_pk_in_control_fails() -> None:
    control = _records("users", {"id": 1, "name": "a"}, {"id": 1, "name": "a"})
    target = _records("users", {"id": 1, "name": "a"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert not summary.passed
    assert summary.control_pk_uniqueness is not None
    assert not summary.control_pk_uniqueness.passed


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
    assert "(1 missing PK)" in content
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
    """A duplicated PK keeps its FIRST record in the by-PK lookup, so the
    example shown does not depend on emission order (the run still fails
    via the uniqueness check either way)."""
    control = _records("users", {"id": 1, "name": "first"}, {"id": 1, "name": "second"})
    target = _records("users", {"id": 1, "name": "first"})

    summary = run_record_comparisons(control, target, USERS_PKS)

    assert summary.field_comparison is not None
    assert summary.field_comparison.passed
    assert summary.control_pk_uniqueness is not None
    assert not summary.control_pk_uniqueness.passed


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
