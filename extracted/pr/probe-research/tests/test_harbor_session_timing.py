"""Tool-call timing recovered from the agent's own transcript."""

from __future__ import annotations

import json

from probe.connectors.harbor_session_timing import (
    TOOL_TIMING_BATCHED,
    TOOL_TIMING_SOURCE_SESSION_LOG,
    agent_is_supported,
    coverage,
    parse_session_log,
    session_log_path,
)


def _write(tmp_path, events):
    path = tmp_path / "session.jsonl"
    path.write_text("\n".join(json.dumps(event) for event in events))
    return path


def _assistant(ts, *calls):
    return {
        "type": "assistant",
        "timestamp": ts,
        "message": {
            "role": "assistant",
            "content": [
                {"type": "tool_use", "id": call, "name": "Bash", "input": {}}
                for call in calls
            ],
        },
    }


def _result(ts, call):
    return {
        "type": "user",
        "timestamp": ts,
        "message": {
            "role": "user",
            "content": [{"type": "tool_result", "tool_use_id": call, "content": "ok"}],
        },
    }


def test_a_single_call_gets_its_dispatch_and_its_own_result(tmp_path):
    path = _write(
        tmp_path,
        [
            _assistant("2026-08-05T08:50:20.850Z", "toolu_1"),
            _result("2026-08-05T08:50:23.500Z", "toolu_1"),
        ],
    )
    timings = parse_session_log(path)
    assert timings["toolu_1"].started_at == "2026-08-05T08:50:20.850Z"
    assert timings["toolu_1"].ended_at == "2026-08-05T08:50:23.500Z"
    assert timings["toolu_1"].batched is False
    assert timings["toolu_1"].attributes() == {
        "timing_source": TOOL_TIMING_SOURCE_SESSION_LOG
    }


def test_a_batch_shares_one_dispatch_and_says_so(tmp_path):
    """Two calls in one assistant message start together and end apart.

    The shared start is the honest record of what happened, so it is kept and
    labelled rather than spread out to make the bars look tidy.
    """
    path = _write(
        tmp_path,
        [
            _assistant("2026-08-05T08:50:20.000Z", "toolu_a", "toolu_b"),
            _result("2026-08-05T08:50:23.000Z", "toolu_a"),
            _result("2026-08-05T08:50:27.000Z", "toolu_b"),
        ],
    )
    timings = parse_session_log(path)
    assert timings["toolu_a"].started_at == timings["toolu_b"].started_at
    assert timings["toolu_a"].ended_at != timings["toolu_b"].ended_at
    assert timings["toolu_a"].batched is True
    assert timings["toolu_a"].attributes()["dispatch"] == TOOL_TIMING_BATCHED


def test_an_aborted_call_has_no_end_rather_than_a_fabricated_one(tmp_path):
    path = _write(
        tmp_path,
        [
            _assistant("2026-08-05T08:50:20.000Z", "toolu_done", "toolu_killed"),
            _result("2026-08-05T08:50:22.000Z", "toolu_done"),
        ],
    )
    timings = parse_session_log(path)
    assert "toolu_done" in timings
    assert "toolu_killed" not in timings


def test_a_result_with_no_dispatch_is_skipped_not_anchored_to_a_nearby_stamp(tmp_path):
    path = _write(tmp_path, [_result("2026-08-05T08:50:22.000Z", "toolu_orphan")])
    assert parse_session_log(path) == {}


def test_a_backwards_result_is_refused(tmp_path):
    path = _write(
        tmp_path,
        [
            _assistant("2026-08-05T08:50:20.000Z", "toolu_1"),
            _result("2026-08-05T08:50:19.000Z", "toolu_1"),
        ],
    )
    assert parse_session_log(path) == {}


def test_a_corrupt_line_costs_one_call_not_the_whole_trial(tmp_path):
    path = tmp_path / "session.jsonl"
    path.write_text(
        "\n".join(
            [
                json.dumps(_assistant("2026-08-05T08:50:20.000Z", "toolu_1")),
                "{not json",
                json.dumps(_result("2026-08-05T08:50:22.000Z", "toolu_1")),
            ]
        )
    )
    assert "toolu_1" in parse_session_log(path)


def test_untimestamped_and_unreadable_inputs_are_empty_not_errors(tmp_path):
    assert parse_session_log(tmp_path / "missing.jsonl") == {}
    path = _write(tmp_path, [{"type": "assistant", "message": {"content": []}}])
    assert parse_session_log(path) == {}


def test_only_a_single_unambiguous_session_file_is_used(tmp_path):
    root = tmp_path / "agent" / "sessions" / "projects" / "-testbed"
    root.mkdir(parents=True)
    assert session_log_path(tmp_path) is None  # none yet

    (root / "a.jsonl").write_text("")
    assert session_log_path(tmp_path) == root / "a.jsonl"

    # A resumed or forked session leaves two, and there is no non-arbitrary
    # way to pick. Declining keeps inferred timing rather than timing the
    # trial from the wrong transcript.
    (root / "b.jsonl").write_text("")
    assert session_log_path(tmp_path) is None


def test_only_claude_code_transcripts_are_claimed():
    assert agent_is_supported({"name": "claude-code"}) is True
    assert agent_is_supported({"name": "miles-harbor-synthetic-agent"}) is False
    assert agent_is_supported({"name": "goose"}) is False
    assert agent_is_supported(None) is False
    assert agent_is_supported({}) is False


def test_coverage_reports_the_measured_fraction_not_just_a_flag(tmp_path):
    path = _write(
        tmp_path,
        [
            _assistant("2026-08-05T08:50:20.000Z", "toolu_1"),
            _result("2026-08-05T08:50:22.000Z", "toolu_1"),
        ],
    )
    timings = parse_session_log(path)
    assert coverage(timings, ["toolu_1", "toolu_2", "toolu_3"]) == {
        "tool_calls": 3,
        "measured": 1,
        "source": TOOL_TIMING_SOURCE_SESSION_LOG,
    }
