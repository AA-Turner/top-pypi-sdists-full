"""`_telemetry_core.AGENT_DETECT_ENV` must mirror `agent_session.AGENTS`.

The table is duplicated for the same hard reason the whole file is duplicated: the
plugin hook runs under the system python3 with no `probe` package importable, so it
cannot import `agent_session`. Duplication is fine; SILENT DRIFT is not — a new agent
added to `AGENTS` and forgotten here would be attributed as "no agent", which is
exactly the misattribution the detection replaced.

Order matters as much as membership: both sides are first-match-wins, so a table that
agreed on membership but not order would resolve a process carrying two agents'
markers differently on each side.
"""

from __future__ import annotations

import pytest

from probe.sdk import _telemetry_core as core
from probe.sdk import agent_session


def test_the_tables_agree_on_labels_and_order() -> None:
    assert [label for label, _ in core.AGENT_DETECT_ENV] == [
        spec.label for spec in agent_session.AGENTS
    ]


def test_the_tables_agree_on_every_detection_marker() -> None:
    assert {label: markers for label, markers in core.AGENT_DETECT_ENV} == {
        spec.label: spec.detect_env for spec in agent_session.AGENTS
    }


@pytest.mark.parametrize("spec", agent_session.AGENTS, ids=lambda s: s.label)
def test_each_agent_resolves_to_the_same_label_on_both_sides(spec) -> None:
    for marker in spec.detect_env:
        env = {marker: "1"}
        assert core.detect_agent_label(env) == spec.label
        detected = agent_session.detect_agent(env)
        assert detected is not None and detected.label == spec.label


def test_no_agent_is_none_not_a_placeholder() -> None:
    # The bug this replaced: an unset PROBE_AGENT defaulted to "claude_code", so
    # every Cursor and unpaired-Codex user landed in the Claude Code bucket.
    assert core.detect_agent_label({}) is None
    assert agent_session.detect_agent({}) is None


def test_probe_agent_override_wins_over_detection() -> None:
    env = {"CLAUDECODE": "1", "PROBE_AGENT": "harness"}
    assert core.detect_agent_label(env) == "harness"


def test_a_blank_override_falls_through_to_detection() -> None:
    env = {"CLAUDECODE": "1", "PROBE_AGENT": "   "}
    assert core.detect_agent_label(env) == "claude_code"


def test_cursor_is_labelled_cursor_not_claude_code() -> None:
    # The headline regression: Cursor is detectable but uncaptured, so
    # resolve_agent_session() returns None for it while the LABEL is still cursor.
    env = {"CURSOR_TRACE_ID": "abc"}
    assert core.detect_agent_label(env) == "cursor"
    assert agent_session.resolve_agent_session(env) is None
