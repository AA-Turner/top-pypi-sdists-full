# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the final-state extraction and comparison.

The state a `read` leaves behind is what the next incremental sync resumes from,
so the rule is two-tiered on purpose: the *shape* of a state blob is a contract
and any change to it fails, while a scalar that moved under an unchanged shape
is reported and does not gate -- the two versions call the live API in separate
runs, so a timestamp cursor advances between them on its own.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from airbyte_ops_mcp.regression_tests.models import (
    LEGACY_STATE_KEY,
    SHARED_STATE_KEY,
    Command,
    ConnectorUnderTest,
    ExecutionResult,
    TargetOrControl,
)
from airbyte_ops_mcp.regression_tests.regression import compare_final_states

pytestmark = pytest.mark.unit


def _ids(states: dict[str, Any]) -> dict[tuple[str | None, str], Any]:
    """Name-keyed fixtures as the identity-keyed dict the comparison consumes.

    Extraction keys on `(namespace, name)` so two streams that render the same
    label stay two streams; a fixture with no namespaces says so once here rather
    than at every literal.
    """
    return {(None, name): state for name, state in states.items()}


# ---------------------------------------------------------------------------
# helpers
#
# The fixtures are the JSON a connector writes to stdout, not `AirbyteMessage`
# objects round-tripped through `model_dump_json`: this version of
# `airbyte_protocol` treats the `global` alias as validation-only, so a dumped
# GLOBAL message says `global_` and parses back with no global state at all.
# What the extraction has to read is the wire format, so that is what it gets.
# ---------------------------------------------------------------------------


def _stream_state(
    name: str,
    state: dict[str, Any] | None,
    namespace: str | None = None,
    **extra: Any,
) -> dict[str, Any]:
    """A STREAM state message for one stream."""
    descriptor: dict[str, Any] = {"name": name}
    if namespace is not None:
        descriptor["namespace"] = namespace

    return {
        "type": "STATE",
        "state": {
            "type": "STREAM",
            "stream": {"stream_descriptor": descriptor, "stream_state": state},
            **extra,
        },
    }


def _global_state(
    streams: dict[str, dict[str, Any]],
    shared: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """A GLOBAL state message covering several streams at once."""
    global_state: dict[str, Any] = {
        "stream_states": [
            {"stream_descriptor": {"name": name}, "stream_state": state}
            for name, state in streams.items()
        ]
    }
    if shared is not None:
        global_state["shared_state"] = shared

    return {"type": "STATE", "state": {"type": "GLOBAL", "global": global_state}}


def _legacy_state(data: dict[str, Any]) -> dict[str, Any]:
    """A LEGACY state message, which carries no stream identity."""
    return {"type": "STATE", "state": {"type": "LEGACY", "data": data}}


def _result(tmp_path: Path, *messages: dict[str, Any]) -> ExecutionResult:
    """A finished `read` whose stdout is exactly these messages."""
    tmp_path.mkdir(parents=True, exist_ok=True)
    stdout = tmp_path / "stdout.jsonl"
    stdout.write_text("\n".join(json.dumps(message) for message in messages))

    return ExecutionResult(
        connector_under_test=ConnectorUnderTest(
            image_name="airbyte/source-test:1.0.0",
            target_or_control=TargetOrControl.TARGET,
        ),
        command=Command.READ,
        stdout_file_path=stdout,
        stderr_file_path=tmp_path / "stderr.log",
        success=True,
        exit_code=0,
    )


# ---------------------------------------------------------------------------
# get_final_state_per_stream
# ---------------------------------------------------------------------------


def test_the_last_state_per_stream_is_the_one_kept(tmp_path):
    """Earlier states are checkpoints the connector has already moved past.

    Keeping the first, or merging them, would compare a position neither version
    would actually resume from.
    """
    result = _result(
        tmp_path,
        _stream_state("users", {"updated_at": "2024-01-01"}),
        _stream_state("orders", {"updated_at": "2024-01-05"}),
        _stream_state("users", {"updated_at": "2024-01-09"}),
    )

    assert result.get_final_state_per_stream() == _ids(
        {
            "users": {"updated_at": "2024-01-09"},
            "orders": {"updated_at": "2024-01-05"},
        }
    )


def test_a_global_state_is_unpacked_into_one_entry_per_stream(tmp_path):
    """A GLOBAL message holds every stream's cursor plus a shared blob.

    Compared whole, one stream's advanced cursor would mask another's dropped
    key: the diff would just say "the global state changed".
    """
    result = _result(
        tmp_path,
        _global_state(
            {"users": {"lsn": 100}, "orders": {"lsn": 100}},
            shared={"replication_slot": "airbyte_slot"},
        ),
    )

    assert result.get_final_state_per_stream() == {
        (None, "users"): {"lsn": 100},
        (None, "orders"): {"lsn": 100},
        SHARED_STATE_KEY: {"replication_slot": "airbyte_slot"},
    }


def test_a_legacy_state_is_compared_whole_rather_than_dropped(tmp_path):
    """The protocol gives a LEGACY blob no stream identity, but it is still state.

    Skipping it would let the comparison report "state unchanged" over the only
    thing the connector will resume from.
    """
    result = _result(tmp_path, _legacy_state({"users": {"updated_at": "2024-01-01"}}))

    assert result.get_final_state_per_stream() == {
        LEGACY_STATE_KEY: {"users": {"updated_at": "2024-01-01"}}
    }


def test_the_same_stream_name_in_two_namespaces_does_not_shadow_itself(tmp_path):
    """`public.users` and `reporting.users` are two streams with two cursors."""
    result = _result(
        tmp_path,
        _stream_state("users", {"id": 1}, namespace="public"),
        _stream_state("users", {"id": 2}, namespace="reporting"),
    )

    assert result.get_final_state_per_stream() == {
        ("public", "users"): {"id": 1},
        ("reporting", "users"): {"id": 2},
    }


def test_record_counts_beside_the_state_are_not_part_of_it(tmp_path):
    """`sourceStats.recordCount` differs between two runs of the same version.

    Comparing it here would fail every incremental read for a reason the record
    counts table already reports properly.
    """
    result = _result(
        tmp_path,
        _stream_state(
            "users",
            {"updated_at": "2024-01-01"},
            sourceStats={"recordCount": 42.0},
        ),
    )

    assert result.get_final_state_per_stream() == _ids(
        {"users": {"updated_at": "2024-01-01"}}
    )


def test_a_run_that_emitted_no_state_yields_nothing_rather_than_failing(tmp_path):
    """Emitting nothing is a legitimate empty, not a broken extraction.

    Note this is *not* the full-refresh case: the Python CDK emits a terminal
    sentinel state per stream even for a plain full refresh. This is a connector
    that predates that, or one that stopped before its first checkpoint.
    """
    assert _result(tmp_path).get_final_state_per_stream() == {}


# ---------------------------------------------------------------------------
# compare_final_states
# ---------------------------------------------------------------------------


def test_identical_states_pass():
    states = {"users": {"updated_at": "2024-01-01"}, "orders": {"id": 7}}

    result = compare_final_states(_ids(states), _ids(states))

    assert result.passed is True
    assert result.errors == []
    assert result.warnings == []
    assert result.value_only is False
    assert result.message == "Final state unchanged across 2 streams"


def test_an_advanced_cursor_warns_instead_of_failing():
    """Both sides hit the live API separately, so a timestamp moves on its own.

    Failing on this would redden every incremental read, which is how a check
    stops being read at all. It is still reported.
    """
    result = compare_final_states(
        _ids({"users": {"updated_at": "2024-01-01T00:00:00Z"}}),
        _ids({"users": {"updated_at": "2024-01-01T00:05:00Z"}}),
    )

    assert result.passed is False
    assert result.value_only is True
    assert result.errors == []
    assert result.warnings == ["State for users changed value"]
    assert result.message == "Final state: 1 stream whose state changed value"


@pytest.mark.parametrize(
    "control,target",
    [
        pytest.param(
            {"updated_at": "2024-01-01", "page": 3},
            {"updated_at": "2024-01-01"},
            id="key-removed",
        ),
        pytest.param(
            {"updated_at": "2024-01-01"},
            {"updated_at": "2024-01-01", "page": 3},
            id="key-added",
        ),
        pytest.param(
            {"updated_at": "2024-01-01"},
            {"updated_at": 1704067200},
            id="type-changed",
        ),
        pytest.param(
            {"cursor_path": ["updated_at"]},
            {"cursor_path": ["updated_at", "id"]},
            id="cursor-path-grew",
        ),
    ],
)
def test_a_change_to_the_shape_of_a_state_fails(control, target):
    """The shape is a contract with the connector's own next run.

    A renamed, retyped or dropped cursor key means the next sync resumes from
    somewhere else -- or from the beginning -- and it exits 0 while doing it.
    """
    result = compare_final_states(_ids({"users": control}), _ids({"users": target}))

    assert result.passed is False
    assert result.value_only is False
    assert result.errors == ["State for users changed shape"]
    assert result.warnings == []


@pytest.mark.parametrize(
    "control,target,side",
    [
        pytest.param({"users": {"id": 1}}, {}, "target", id="missing-on-target"),
        pytest.param({}, {"users": {"id": 1}}, "control", id="missing-on-control"),
    ],
)
def test_a_stream_with_state_on_only_one_side_fails(control, target, side):
    """One side has nothing to resume from, or resumes from something new."""
    result = compare_final_states(_ids(control), _ids(target))

    assert result.passed is False
    assert result.value_only is False
    assert result.errors == [f"State for users is missing on the {side}"]


def test_a_structural_change_outranks_a_moved_cursor_in_the_summary():
    """Summaries truncate, so the finding that gates has to come first."""
    result = compare_final_states(
        _ids(
            {
                "advanced": {"updated_at": "2024-01-01"},
                "dropped": {"updated_at": "2024-01-01"},
                "restructured": {"updated_at": "2024-01-01", "page": 1},
            }
        ),
        _ids(
            {
                "advanced": {"updated_at": "2024-06-01"},
                "restructured": {"updated_at": "2024-01-01"},
            }
        ),
    )

    assert result.passed is False
    assert result.value_only is False
    assert result.errors == [
        "State for dropped is missing on the target",
        "State for restructured changed shape",
    ]
    assert result.warnings == ["State for advanced changed value"]
    assert result.message == (
        "Final state: 1 stream with state on one side only, "
        "1 stream whose state changed shape, 1 stream whose state changed value"
    )


@pytest.mark.parametrize(
    "control,target",
    [
        pytest.param({}, {}, id="both-empty"),
        pytest.param(None, None, id="both-uncollected"),
    ],
)
def test_no_state_on_either_side_is_inconclusive_not_a_pass(control, target):
    """Emitting no state at all cannot hard-fail, but must not go green either.

    A connector predating the CDK's terminal full-refresh sentinel, or one that
    stopped before its first checkpoint, has nothing here through no fault of the
    target version -- so this cannot hard-fail the way a `discover` with no
    catalog does. A green row over something never looked at is how a state
    regression ships, so it is not a pass either.
    """
    result = compare_final_states(control, target)

    assert result.passed is False
    # Reported as a warning: nothing was compared, and nothing was found wrong.
    # Not `value_only` -- that classifies differences, and there were none.
    assert result.inconclusive is True
    assert result.value_only is False
    assert result.message == "Neither version emitted any state; nothing was compared"


def test_a_stream_state_that_became_null_is_a_structural_change():
    """A cursor that vanished is not a cursor that moved."""
    result = compare_final_states(_ids({"users": {"id": 1}}), _ids({"users": None}))

    assert result.passed is False
    assert result.value_only is False
    assert result.errors == ["State for users changed shape"]


def test_the_diff_survives_the_trip_into_the_run_payload():
    """The diff is written to `GITHUB_OUTPUT`, so DeepDiff's own types cannot ship."""
    result = compare_final_states(
        _ids({"users": {"updated_at": "2024-01-01", "page": 1}}),
        _ids({"users": {"updated_at": "2024-01-01"}}),
    )

    diff = result.stream_results["users"].schema_diff
    assert diff is not None
    assert "page" in json.dumps(diff)


def test_the_extracted_states_are_what_the_comparison_consumes(tmp_path):
    """Extraction and comparison have to agree on the labels, end to end."""
    control = _result(
        tmp_path / "control",
        _stream_state("users", {"updated_at": "2024-01-01"}),
    )
    target = _result(
        tmp_path / "target",
        _stream_state("users", {"cursor": "2024-01-01"}),
    )

    result = compare_final_states(
        control.get_final_state_per_stream(),
        target.get_final_state_per_stream(),
    )

    assert result.passed is False
    assert result.errors == ["State for users changed shape"]


def test_a_cursor_key_that_was_null_and_then_dropped_is_a_structural_change(tmp_path):
    """A `null` inside a state blob is data, not an unset protocol optional.

    The blob is an `AirbyteStateBlob`, so normalising it with `exclude_none=True`
    would strip `"cursor": null` on the way in and report the two sides as
    identical -- a green "Final state unchanged" over exactly the dropped key
    this check exists to catch.
    """
    control = _result(
        tmp_path / "control",
        _stream_state("users", {"cursor": None, "page": 1}),
    )
    target = _result(tmp_path / "target", _stream_state("users", {"page": 1}))

    assert control.get_final_state_per_stream() == _ids(
        {"users": {"cursor": None, "page": 1}}
    )

    result = compare_final_states(
        control.get_final_state_per_stream(),
        target.get_final_state_per_stream(),
    )

    assert result.passed is False
    assert result.value_only is False
    assert result.errors == ["State for users changed shape"]


def test_a_null_shared_state_key_is_kept_too(tmp_path):
    """The shared blob of a GLOBAL state is normalised the same way."""
    result = _result(
        tmp_path,
        _global_state({"users": {"lsn": 100}}, shared={"lsn": None, "slot": "s"}),
    )

    assert result.get_final_state_per_stream()[SHARED_STATE_KEY] == {
        "lsn": None,
        "slot": "s",
    }


def test_two_streams_that_render_the_same_label_stay_two_streams(tmp_path):
    """A stream literally named `public.users` beside `users` in `public`.

    Keyed by the label these would collapse, and the last one emitted would take
    the other's state with it -- a regression in the shadowed stream would be
    invisible. The catalog comparison qualifies the same collision.
    """
    extracted = _result(
        tmp_path,
        _stream_state("public.users", {"cursor": "A"}),
        _stream_state("users", {"cursor": "B"}, namespace="public"),
    ).get_final_state_per_stream()

    assert extracted == {
        (None, "public.users"): {"cursor": "A"},
        ("public", "users"): {"cursor": "B"},
    }

    result = compare_final_states(extracted, extracted)

    assert result.passed is True
    # Two results, under qualified labels, rather than one that swallowed the
    # other. `(2)` goes to the namespaced stream: identities sort before labels.
    assert sorted(result.stream_results) == ["public.users", "public.users (2)"]


def test_a_shared_label_is_derived_from_identity_not_emission_order(tmp_path):
    """Both sides must agree which stream a qualified label refers to.

    Labelling in emission order would let the same label mean stream A on the
    control and stream B on the target, and the diff would compare two unrelated
    cursors.
    """
    control = _result(
        tmp_path / "control",
        _stream_state("public.users", {"cursor": "A"}),
        _stream_state("users", {"cursor": "B"}, namespace="public"),
    )
    target = _result(
        tmp_path / "target",
        # The other way round on the wire.
        _stream_state("users", {"cursor": "B"}, namespace="public"),
        _stream_state("public.users", {"cursor": "A"}),
    )

    result = compare_final_states(
        control.get_final_state_per_stream(),
        target.get_final_state_per_stream(),
    )

    assert result.passed is True
    assert result.errors == []


def test_a_stream_named_like_the_shared_state_is_not_merged_into_it(tmp_path):
    """A connector that names a stream `(shared)` must not absorb the shared blob.

    The sentinel keys on the empty namespace, which `_stream_id` can never
    produce, so the two stay distinct entries and the comparison qualifies the
    label they share.
    """
    extracted = _result(
        tmp_path,
        _global_state({"(shared)": {"cursor": "A"}}, shared={"slot": "s"}),
    ).get_final_state_per_stream()

    assert extracted == {
        (None, "(shared)"): {"cursor": "A"},
        SHARED_STATE_KEY: {"slot": "s"},
    }
    # The sentinel is not the stream's own identity, which is what would have
    # let one overwrite the other.
    assert SHARED_STATE_KEY != (None, "(shared)")

    result = compare_final_states(extracted, extracted)

    assert result.passed is True
    assert sorted(result.stream_results) == ["(shared)", "(shared) (2)"]


# The terminal state the Python CDK emits for a full-refresh stream: the whole
# blob is one `__`-prefixed sentinel, which is why DeepDiff's default of
# ignoring private variables would hide this comparison entirely.
_NO_CURSOR_STATE = {"__ab_no_cursor_state_message": True}
_RFR_COMPLETE_STATE = {"__ab_full_refresh_sync_complete": True}


def test_a_full_refresh_stream_does_emit_state_and_it_is_compared(tmp_path):
    """A full-refresh read is not the "no state" case.

    `FullRefreshCheckpointReader` emits a terminal sentinel per stream, so
    extraction finds state and the comparison has something to do. Treating this
    as inconclusive would have been wrong about the common case.
    """
    extracted = _result(
        tmp_path, _stream_state("users", dict(_NO_CURSOR_STATE))
    ).get_final_state_per_stream()

    assert extracted == _ids({"users": _NO_CURSOR_STATE})

    result = compare_final_states(extracted, extracted)

    assert result.passed is True
    assert result.inconclusive is False
    assert result.message == "Final state unchanged across 1 stream"


def test_a_sentinel_only_state_is_not_invisible_to_the_diff():
    """DeepDiff ignores `__`-prefixed keys unless told otherwise.

    On the default, both of these normalise to `{}` and the check reports
    "Final state unchanged" over a swap that changes what the next sync resumes
    from -- the same silent green this comparison exists to prevent.
    """
    result = compare_final_states(
        _ids({"users": dict(_NO_CURSOR_STATE)}),
        _ids({"users": dict(_RFR_COMPLETE_STATE)}),
    )

    assert result.passed is False
    assert result.value_only is False
    assert result.errors == ["State for users changed shape"]


def test_a_changed_value_under_a_private_key_is_seen_too():
    """Not just added and removed keys: the value under one has to be compared."""
    result = compare_final_states(
        _ids({"users": {"__ab_full_refresh_sync_complete": True}}),
        _ids({"users": {"__ab_full_refresh_sync_complete": False}}),
    )

    assert result.passed is False
    assert result.warnings == ["State for users changed value"]
    assert result.value_only is True


def test_a_substream_rfr_partition_that_completed_on_one_side_only_fails():
    """Substream RFR nests the sentinel per partition, under `states[].cursor`.

    A partition complete on one side and not the other is a different resume
    point, and on DeepDiff's default the two cursors would both read as `{}`.
    """
    result = compare_final_states(
        _ids({"users": {"states": [{"partition": {"id": 1}, "cursor": {}}]}}),
        _ids(
            {
                "users": {
                    "states": [
                        {"partition": {"id": 1}, "cursor": dict(_RFR_COMPLETE_STATE)}
                    ]
                }
            }
        ),
    )

    assert result.passed is False
    assert result.value_only is False
    assert result.errors == ["State for users changed shape"]


def test_only_a_read_collects_final_states(tmp_path):
    """`None` and `{}` have to stay distinguishable on `ComparableOutputs`.

    `get_final_state_per_stream` returns `{}` for anything that emitted no state,
    including a `spec` run that never could -- so collecting it unconditionally
    would make "this command emits no state" indistinguishable from "this read
    resumed from nothing", which is a finding.
    """
    from airbyte_ops_mcp.regression_tests.models import ComparableOutputs

    messages = [_stream_state("users", {"updated_at": "2024-01-01"})]

    read = _result(tmp_path / "read", *messages)
    assert ComparableOutputs.from_execution_result(read).final_states == _ids(
        {"users": {"updated_at": "2024-01-01"}}
    )

    spec_run = _result(tmp_path / "spec", *messages)
    spec_run.command = Command.SPEC
    assert ComparableOutputs.from_execution_result(spec_run).final_states is None

    empty_read = _result(tmp_path / "empty")
    assert ComparableOutputs.from_execution_result(empty_read).final_states == {}


def test_the_catalog_and_state_tables_agree_on_a_collision_label():
    """One report's two tables must not point at each other's stream.

    Both comparisons qualify a label collision, and they have to resolve it the
    same way or a reader following `z.a` from the catalog table to the state
    table lands on the sibling stream. `z.a` beside `a` in namespace `z` is the
    case where a name-first tie-break diverges from a namespace-first one, since
    `"a" < "z.a"` while `"" < "z"`.
    """
    from airbyte_ops_mcp.regression_tests.regression import compare_catalog_schemas

    schema = {"type": "object", "properties": {"x": {"type": "string"}}}
    retyped = {"type": "object", "properties": {"x": {"type": "integer"}}}

    # Only the namespaced stream ("z", "a") differs, on both surfaces.
    catalog = compare_catalog_schemas(
        {
            "streams": [
                {"name": "z.a", "json_schema": schema},
                {"name": "a", "namespace": "z", "json_schema": schema},
            ]
        },
        {
            "streams": [
                {"name": "z.a", "json_schema": schema},
                {"name": "a", "namespace": "z", "json_schema": retyped},
            ]
        },
    )
    state = compare_final_states(
        {(None, "z.a"): {"c": 1}, ("z", "a"): {"c": 1}},
        {(None, "z.a"): {"c": 1}, ("z", "a"): {"c": 1, "extra": 2}},
    )

    assert catalog.failed_streams == state.failed_streams == ["z.a (2)"]
    assert list(catalog.stream_results) == list(state.stream_results)


def test_a_reordered_list_in_a_state_blob_warns_instead_of_failing():
    """A reorder is visible but does not gate, and that is on purpose.

    DeepDiff encodes a pure reorder of same-shaped elements as `values_changed`,
    so the classifier calls it value-only. A substream's partition list can come
    back in a different order from two live-API runs, and failing on that would
    redden those runs the way failing on a moved cursor would. Pinned because it
    would otherwise be an accident of DeepDiff's encoding rather than a decision.
    """
    result = compare_final_states(
        _ids({"users": {"cursor_path": ["updated_at", "id"]}}),
        _ids({"users": {"cursor_path": ["id", "updated_at"]}}),
    )

    assert result.passed is False
    assert result.value_only is True
    assert result.errors == []
    assert result.warnings == ["State for users changed value"]


def test_a_list_that_grew_still_fails():
    """The contrast to a reorder: a new element changes the shape, so it gates."""
    result = compare_final_states(
        _ids({"users": {"cursor_path": ["updated_at"]}}),
        _ids({"users": {"cursor_path": ["updated_at", "id"]}}),
    )

    assert result.passed is False
    assert result.value_only is False
    assert result.errors == ["State for users changed shape"]


def test_a_legacy_to_per_stream_state_migration_fails_once_per_key(tmp_path):
    """The CDK-migration signature, and the error list scales with the streams.

    A connector moving off `LEGACY` state onto per-stream `STREAM` state has
    `(legacy)` on the control and one entry per stream on the target, so *every*
    key is one-sided: one error for the legacy blob plus one per stream, not a
    fixed pair. It gates, which is intended -- the state contract really did
    change and a human should look at it -- but the count is what tells a
    reviewer this is a wholesale migration rather than one stream regressing.
    """
    control = _result(
        tmp_path / "control",
        _legacy_state({"users": {"c": 1}, "orders": {"c": 2}}),
    ).get_final_state_per_stream()
    target = _result(
        tmp_path / "target",
        _stream_state("users", {"c": 1}),
        _stream_state("orders", {"c": 2}),
        _stream_state("events", {"c": 3}),
    ).get_final_state_per_stream()

    result = compare_final_states(control, target)

    assert result.passed is False
    assert result.value_only is False
    assert result.inconclusive is False
    # One per one-sided key: the legacy blob, then each stream the target grew.
    assert result.errors == [
        "State for (legacy) is missing on the target",
        "State for events is missing on the control",
        "State for orders is missing on the control",
        "State for users is missing on the control",
    ]
    assert result.message == "Final state: 4 streams with state on one side only"
