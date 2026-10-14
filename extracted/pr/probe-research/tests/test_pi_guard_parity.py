"""pi's guard refuses what Claude Code's refuses, in the same words.

pi has no hooks, so `plugins/probe-research-pi/src/guard.ts` (a `tool_call`
handler) and `core/probeCommands.ts` (the shell parse) carry ports of
`session_marker.touches_approvals` / `daemon_profile_allows` and of
`tracking_guard._probe_invocations`. A refusal that reads differently, a list
that lost a word or a parse that splits a line differently would tell pi's
agent something Claude Code's is not told, so every copied constant is pinned
here, and the shared fixture (`fixtures/pi_probe_commands.json`, which the pi
package's vitest runs through the port) is re-derived from the Python.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

from probe.sdk import session_marker
from tests.ts_source import ts_raw, ts_set, ts_string

AGENT = Path(__file__).resolve().parents[1]
HOOKS = AGENT / "plugins" / "probe-research" / "hooks"
PI_SRC = AGENT / "plugins" / "probe-research-pi" / "src"
GUARD = PI_SRC / "guard.ts"
COMMANDS = PI_SRC / "core" / "probeCommands.ts"
PROFILE = PI_SRC / "profile.ts"
FIXTURE = AGENT / "tests" / "fixtures" / "pi_probe_commands.json"


def _guard():
    sys.path.insert(0, str(HOOKS))
    try:
        spec = importlib.util.spec_from_file_location("_tracking_guard_pi_parity", HOOKS / "tracking_guard.py")
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    finally:
        sys.path.remove(str(HOOKS))


def test_the_refusals_read_word_for_word():
    assert ts_string(GUARD, "DENY_REASON_APPROVALS") == session_marker.DENY_REASON_APPROVALS
    assert ts_string(GUARD, "DAEMON_PROFILE_DENY") == session_marker.DAEMON_PROFILE_DENY
    assert ts_string(GUARD, "DIRECTED_RETRY") == session_marker.DIRECTED_RETRY
    assert ts_string(GUARD, "WRITER_RETRY") == session_marker.WRITER_RETRY
    assert ts_string(GUARD, "DAEMON_PROFILE_DENY_WRITE") == session_marker.DAEMON_PROFILE_DENY_WRITE


def test_the_question_folder_is_found_the_same_way():
    assert ts_string(PI_SRC / "core" / "paths.ts", "APPROVALS_DIRNAME") == session_marker.APPROVALS_DIRNAME
    assert ts_raw(GUARD, "APPROVALS_TEXT_SOURCE") == session_marker._APPROVALS_TEXT.pattern
    assert session_marker._APPROVALS_TEXT.flags & re.IGNORECASE == 0
    # The Python guards file-writing tools by name; pi's are `write` and `edit`,
    # both naming their file in `path` (checked against pi's own types in
    # guard.test.ts). A new Python entry needs a pi spelling, or a reason not to.
    assert set(session_marker._FILE_WRITE_TOOLS) == {"Write", "Edit", "MultiEdit", "NotebookEdit"}


def test_the_daemon_profile_allows_the_same_commands():
    assert ts_set(COMMANDS, "DAEMON_PROFILE_ALLOWED") == session_marker.DAEMON_PROFILE_ALLOWED
    assert ts_set(COMMANDS, "DAEMON_AGENT_WRITES") == session_marker.DAEMON_AGENT_WRITES


def test_an_inline_session_is_read_the_same_way():
    # `sessionIsInline` ports `session_marker.is_inline`: `full` plus a marker
    # naming one of these, beside the state file.
    assert ts_set(GUARD, "INLINE_FROM") == set(session_marker.INLINE_FROM)
    assert ts_string(GUARD, "INLINE_SUFFIX") == session_marker.INLINE_SUFFIX


def test_the_inline_agent_is_refused_the_same_switch_in_the_same_words():
    assert ts_set(COMMANDS, "RESEARCHER_SWITCH") == session_marker.RESEARCHER_SWITCH
    assert ts_string(GUARD, "INLINE_SWITCH_DENY") == session_marker.INLINE_SWITCH_DENY
    assert ts_string(GUARD, "RESEARCHER_SWITCH_DENY") == session_marker.RESEARCHER_SWITCH_DENY


def test_the_classifier_knows_the_same_words():
    for name in (
        "TOP_LEVEL_WRITES",
        "WRITE_GROUPS",
        "SUBGROUPS",
        "READ_VERBS",
        "REMOVAL_VERBS",
        "UNGATED_COMMANDS",
        "DIRECTED_ONLY",
        "ROOT_VALUE_OPTIONS",
        "READ_GROUPS",
    ):
        assert ts_set(COMMANDS, name) == getattr(session_marker, name), name
    assert ts_set(COMMANDS, "READ_UNLESS_FLAGS_COMMANDS") == set(session_marker.READ_UNLESS_FLAGS)
    # pi keeps one flag set for every READ_UNLESS_FLAGS command: a command with
    # flags of its own fails here until the port grows a table.
    flags = ts_set(COMMANDS, "READ_UNLESS_FLAGS_WRITE_FLAGS")
    assert session_marker.READ_UNLESS_FLAGS == {command: flags for command in session_marker.READ_UNLESS_FLAGS}
    assert set(ts_string(COMMANDS, "SHELL_EXPANSION_CHARS")) == session_marker._SHELL_EXPANSION_CHARS
    assert set(ts_string(COMMANDS, "GLOB_CHARS")) == session_marker._GLOB_CHARS
    assert ts_string(COMMANDS, "HELP_FLAG") == session_marker.HELP_FLAG
    assert ts_string(COMMANDS, "DIRECTED_FLAG") == session_marker.DIRECTED_FLAG


def test_the_shell_parse_uses_the_same_tables():
    guard = _guard()
    assert ts_string(COMMANDS, "OPERATOR_CHARS") == guard._OPERATOR_CHARS
    assert ts_set(COMMANDS, "SEPARATOR_CHARS") == set(guard._SEPARATOR_CHARS)
    assert ts_set(COMMANDS, "REDIRECTIONS") == guard._REDIRECTIONS
    assert ts_set(COMMANDS, "WORD_BOUNDARY") == set(guard._WORD_BOUNDARY)
    assert ts_raw(COMMANDS, "HEREDOC_DELIMITER_SOURCE") == guard._HEREDOC_DELIMITER.pattern
    assert ts_raw(COMMANDS, "ENV_ASSIGNMENT_SOURCE") == guard._ENV_ASSIGNMENT.pattern
    assert ts_set(COMMANDS, "WRAPPERS") == guard._WRAPPERS
    assert ts_set(COMMANDS, "WRAPPER_VALUE_OPTS") == guard._WRAPPER_VALUE_OPTS
    assert ts_set(COMMANDS, "SHELLS") == guard._SHELLS
    assert ts_raw(COMMANDS, "PYTHONS_SOURCE") == guard._PYTHONS.pattern
    assert ts_set(COMMANDS, "PROBE_MODULES") == guard._PROBE_MODULES


def test_a_probe_mcp_tool_is_recognised_the_same_way():
    guard = _guard()
    assert ts_string(PROFILE, "PROBE_MCP_TOOL_SOURCE") == guard._PROBE_MCP_RE.pattern
    assert guard._PROBE_MCP_RE.flags & re.IGNORECASE
    assert 'new RegExp(PROBE_MCP_TOOL_SOURCE, "i")' in PROFILE.read_text(encoding="utf-8")


def test_the_shared_fixture_is_what_the_python_guard_answers():
    """The pi package's vitest runs these same cases through `probeCommands.ts`."""
    guard = _guard()
    cases = json.loads(FIXTURE.read_text(encoding="utf-8"))["cases"]
    assert len(cases) > 50
    for case in cases:
        command = case["command"]
        invocations = [list(args) for args in guard._probe_invocations(command)]
        refused = write = None
        for args in invocations:
            if guard._asks_help(args):
                continue
            allowed, matched = session_marker.daemon_profile_allows(args)
            if not allowed:
                refused = matched
                write = session_marker.classify_probe_args(args)[0] == "write"
                break
        assert (invocations, refused, write) == (case["invocations"], case["refused"], case["write"]), command


def test_the_inline_notice_reads_word_for_word():
    # pi tells its agent in the approved words, and both sides write one file.
    source = PI_SRC / "inlineNotice.ts"
    assert ts_string(source, "INLINE_NOTICE") == session_marker.INLINE_NOTICE
    assert ts_string(source, "INLINE_READS") == session_marker.INLINE_READS
    assert ts_string(source, "INLINE_READS_OLD_CLI") == session_marker.INLINE_READS_OLD_CLI
    # The same CLI floor for the read bridge (`probe mcp tools|call`) on both sides.
    floor = re.search(r'^INLINE_BRIDGE_MIN_CLI = "([^"]+)"$', (HOOKS / "version_check.py").read_text(), re.M)
    assert floor and ts_string(source, "INLINE_BRIDGE_MIN_CLI") == floor.group(1)
    assert ts_string(source, "INLINE_SHOWN_SUFFIX") == session_marker.INLINE_SHOWN_SUFFIX
