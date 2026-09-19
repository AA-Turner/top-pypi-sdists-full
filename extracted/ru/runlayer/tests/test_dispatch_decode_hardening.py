"""Hook payload decoding survives deeply nested JSON (ISS-01 follow-up).

The raw stdin payload and a JSON-encoded ``tool_input`` (Codex
PermissionRequest) both caught only ``JSONDecodeError``; a nested-array
document raised ``RecursionError`` as a traceback. Posture is fail-open on
purpose: undecodable stdin decodes to ``{}`` and the hook exits 0 with no
event name, exactly as malformed JSON always has. Changing that posture is a
separate decision, not this fix.
"""

from __future__ import annotations

from io import StringIO

import pytest

from runlayer_cli.hook import dispatch as hook_dispatch
from runlayer_cli.hook import hook_io
from tests.hostile_inputs import DEEP_NESTING


@pytest.mark.parametrize(
    "value",
    [DEEP_NESTING, "not-valid-json{", "null", "[1, 2]", '"text"'],
    ids=["deep-nesting", "malformed", "null", "array", "string"],
)
def test_coerce_tool_input_returns_empty_dict_for_undecodable_or_non_object(value):
    assert hook_dispatch._coerce_tool_input(value) == {}


def test_coerce_tool_input_keeps_decoded_object():
    assert hook_dispatch._coerce_tool_input('{"command": "ls"}') == {"command": "ls"}


@pytest.mark.parametrize(
    "stdin_text",
    [DEEP_NESTING, "{not json", "null", "[1, 2]"],
    ids=["deep-nesting", "malformed", "null", "array"],
)
def test_run_hook_undecodable_stdin_fails_open_without_traceback(
    monkeypatch, stdin_text
):
    monkeypatch.setattr(
        hook_dispatch, "_resolve_mode", lambda: hook_dispatch.AIWatchMode.ENFORCE
    )
    monkeypatch.setattr(hook_dispatch, "_resolve_metadata_only", lambda: False)
    stdout = StringIO()
    stderr = StringIO()
    with hook_io.scoped(
        hook_io.HookIO(
            argv=["/usr/local/bin/aiwatch", "hook", "--client", "claude_code"],
            stdin_text=stdin_text,
            stdout=stdout,
            stderr=stderr,
            env={},
        )
    ):
        with pytest.raises(SystemExit) as exc:
            hook_dispatch.run_hook()

    assert exc.value.code == 0
    assert stdout.getvalue() == ""
    assert stderr.getvalue() == ""
