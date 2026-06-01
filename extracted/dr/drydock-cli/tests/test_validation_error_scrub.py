"""Regression test: validation-error tool calls get their args scrubbed
from history so the model doesn't copy the bait shape.

This is the fix the prior months of patches missed. The model copies
the assistant's tool_call.arguments from history when constructing the
next call. When the call had empty/invalid args AND failed with a
deterministic error, leaving those args in history is pure bait. The
scrub rewrites the arguments to `{}` so the call SHAPE remains in
history (for ordering / audit) but the empty-arg payload is gone.

If this test ever starts failing, do NOT roll back the scrub — instead
extend _VALIDATION_ERROR_PATTERNS to cover whatever new sentinel was
introduced. The cost of a false-negative scrub (leaving a bait shape
in history) is months of recurring loops; the cost of a false-positive
scrub (clean tool error context lost) is one extra LLM turn.
"""
from __future__ import annotations

import json

import pytest

from drydock.core.types import (
    FunctionCall,
    LLMMessage,
    Role,
    ToolCall,
)
from tests.conftest import build_test_agent_loop


def _make_tc(name: str, arguments: str, tc_id: str = "tc_a") -> ToolCall:
    return ToolCall(
        id=tc_id,
        index=0,
        function=FunctionCall(name=name, arguments=arguments),
    )


def _seed_history_with_failed_call(
    loop, tool_name: str, args_str: str, tc_id: str = "tc_a"
) -> None:
    """Plant an assistant message containing a tool_call + a tool result
    message paired with it. The args_str is what the model emitted;
    after scrubbing it should become '{}'."""
    loop.messages.reset([
        LLMMessage(role=Role.system, content="be helpful"),
        LLMMessage(role=Role.user, content="please help"),
        LLMMessage(
            role=Role.assistant,
            content="",
            tool_calls=[_make_tc(tool_name, args_str, tc_id)],
        ),
    ])


def _assistant_args(loop, tc_id: str) -> str:
    for m in loop.messages:
        if m.role != Role.assistant or not m.tool_calls:
            continue
        for tc in m.tool_calls:
            if tc.id == tc_id:
                return tc.function.arguments or ""
    raise AssertionError(f"no assistant message with tool_call id={tc_id}")


class _FakeResolvedToolCall:
    """Minimal stand-in for ResolvedToolCall — _handle_tool_response
    only reads tool_call_id / id from it for the scrub path."""

    def __init__(self, tc_id: str, tool_name: str = "write_file"):
        self.tool_call_id = tc_id
        self.id = tc_id
        self.tool_name = tool_name
        self.args_dict = {}


class TestValidationErrorScrub:
    def test_write_file_empty_path_is_scrubbed(self):
        loop = build_test_agent_loop()
        _seed_history_with_failed_call(
            loop, "write_file",
            json.dumps({"path": "", "content": "x = 1\n"}),
            tc_id="tc_wf_1",
        )
        # Sanity: bait is present pre-scrub.
        assert "x = 1" in _assistant_args(loop, "tc_wf_1")

        loop._scrub_validation_error_call(
            _FakeResolvedToolCall("tc_wf_1", "write_file")
        )

        # Post-scrub: args are empty {} — no bait shape remains.
        scrubbed = _assistant_args(loop, "tc_wf_1").strip()
        assert scrubbed == "{}", (
            f"expected scrubbed args == '{{}}', got {scrubbed!r}"
        )

    def test_search_replace_empty_path_is_scrubbed(self):
        loop = build_test_agent_loop()
        _seed_history_with_failed_call(
            loop, "search_replace",
            json.dumps({"file_path": "", "content": "<<<<\nold\n====\nnew\n>>>>"}),
            tc_id="tc_sr_1",
        )
        loop._scrub_validation_error_call(
            _FakeResolvedToolCall("tc_sr_1", "search_replace")
        )
        assert _assistant_args(loop, "tc_sr_1").strip() == "{}"

    def test_already_scrubbed_call_is_idempotent(self):
        loop = build_test_agent_loop()
        _seed_history_with_failed_call(
            loop, "write_file", "{}", tc_id="tc_wf_2",
        )
        loop._scrub_validation_error_call(
            _FakeResolvedToolCall("tc_wf_2", "write_file")
        )
        # Still {}, no exception.
        assert _assistant_args(loop, "tc_wf_2").strip() == "{}"

    def test_is_validation_error_matches_sentinels(self):
        loop = build_test_agent_loop()
        assert loop._is_validation_error(
            "NO path supplied. Pick a concrete file path under the "
            "current project, then re-emit with that path."
        )
        assert loop._is_validation_error(
            "File path is required. Use: search_replace(file_path=..."
        )
        assert loop._is_validation_error("Empty content provided.")
        # MUST NOT match useful failure context — those are kept.
        assert not loop._is_validation_error(
            "SEARCH/REPLACE block 1 failed: Search text not found"
        )
        assert not loop._is_validation_error(
            "[Errno 2] No such file or directory: 'foo.py'"
        )
        assert not loop._is_validation_error("pytest: rc=1, 6 failed")

    def test_unknown_tc_id_no_op(self):
        loop = build_test_agent_loop()
        _seed_history_with_failed_call(
            loop, "write_file",
            json.dumps({"path": "", "content": "stuff"}),
            tc_id="tc_real",
        )
        # Scrub a non-matching id — no-op, original args preserved.
        loop._scrub_validation_error_call(
            _FakeResolvedToolCall("tc_missing", "write_file")
        )
        assert "stuff" in _assistant_args(loop, "tc_real")

    def test_call_id_attribute_works(self):
        """ResolvedToolCall uses `call_id`, not `tool_call_id` or `id`.
        Regression guard: don't reintroduce the attribute-name bug."""
        loop = build_test_agent_loop()
        _seed_history_with_failed_call(
            loop, "write_file",
            json.dumps({"path": "", "content": "x"}),
            tc_id="tc_call_id_form",
        )
        # Build a stand-in that only exposes `call_id` (the canonical
        # attribute on the real ResolvedToolCall Pydantic class).
        class _CallIdOnly:
            def __init__(self, cid):
                self.call_id = cid
                self.tool_name = "write_file"
        loop._scrub_validation_error_call(_CallIdOnly("tc_call_id_form"))
        assert _assistant_args(loop, "tc_call_id_form").strip() == "{}"


class TestRepoBugReplication:
    """Replicate the operator's observed bug: a bad tool_call sits in
    history, the model copies its args verbatim, the loop never breaks.

    Without the scrub, a backend that pattern-matches on the most
    recent tool_call shape would re-emit the same empty args
    indefinitely (the actual Gemma 4 failure mode observed
    2026-05-31). With the scrub, the bait shape is gone — the
    backend looking at history sees `{}` and has nothing to copy.

    These tests don't run a real LLM (slow + flaky). They simulate
    the copy-bait behavior with a small deterministic FakeBackend
    that returns whatever args it sees in the most recent assistant
    tool_call. The before/after assertion shows the scrub breaks the
    cycle.
    """

    def _seed_failed_history(self, loop, tool_name, args_str, tc_id):
        """Plant: user → assistant tool_call(bad args) → tool error.

        Mirrors what drydock has in messages.jsonl after the model
        emitted a malformed call and the tool error came back."""
        from drydock.core.types import LLMMessage, Role
        loop.messages.reset([
            LLMMessage(role=Role.system, content="be helpful"),
            LLMMessage(role=Role.user, content="add a test"),
            LLMMessage(
                role=Role.assistant, content="",
                tool_calls=[_make_tc(tool_name, args_str, tc_id)],
            ),
            LLMMessage(
                role=Role.tool, tool_call_id=tc_id,
                name=tool_name,
                content=(
                    "NO path supplied. Pick a concrete file path "
                    "under the current project, then re-emit with "
                    "that path and the full file content."
                ),
            ),
        ])

    def _read_most_recent_tool_call_args(self, loop, tool_name):
        """What a copy-bait backend would see when constructing the
        next call: the args of the most recent assistant tool_call
        for this tool."""
        for m in reversed(list(loop.messages)):
            if m.role != Role.assistant or not m.tool_calls:
                continue
            for tc in m.tool_calls:
                if tc.function and tc.function.name == tool_name:
                    return tc.function.arguments or ""
        return None

    def test_without_scrub_bait_is_visible(self):
        """Without the scrub, the bad args remain in history and would
        be visible to a copy-bait backend on the next turn."""
        loop = build_test_agent_loop()
        bad = json.dumps({"path": "", "content": "import os\n"})
        self._seed_failed_history(loop, "write_file", bad, "tc_x")
        visible = self._read_most_recent_tool_call_args(loop, "write_file")
        assert "import os" in (visible or ""), (
            "pre-scrub: backend should see the bait args"
        )

    def test_scrub_removes_bait_from_history(self):
        """The scrub: backend on next turn sees `{}` — no shape to
        copy. Bait class is closed."""
        loop = build_test_agent_loop()
        bad = json.dumps({"path": "", "content": "import os\n"})
        self._seed_failed_history(loop, "write_file", bad, "tc_y")
        # Apply the scrub.
        loop._scrub_validation_error_call(
            _FakeResolvedToolCall("tc_y", "write_file")
        )
        visible = self._read_most_recent_tool_call_args(loop, "write_file")
        assert (visible or "").strip() == "{}", (
            f"post-scrub: backend should see {{}}, got {visible!r}"
        )
        # Tool result was already non-baity (the "NO path supplied"
        # directive replaced the prior bait that included a literal
        # example call shape).

    def test_full_handle_tool_response_path_scrubs_args(self):
        """End-to-end through _handle_tool_response (not just the
        scrub helper in isolation). This is the production code
        path: drydock runs the tool, the tool returns a validation
        error, _handle_tool_response gets called, the scrub fires.

        If THIS test passes, the bug we've been chasing for months is
        actually closed at the integration level — not just at the
        helper level."""
        from drydock.core.types import LLMMessage, Role
        from drydock.core.llm.format import ResolvedToolCall
        from drydock.core.tools.builtins.write_file import (
            WriteFile, WriteFileArgs,
        )

        loop = build_test_agent_loop()
        # Plant: assistant emitted an empty-path write_file call.
        # (The tool will be invoked elsewhere; we're testing what
        # happens AFTER the tool returns the validation-sentinel
        # error text — i.e. _handle_tool_response is the next call.)
        loop.messages.reset([
            LLMMessage(role=Role.system, content="x"),
            LLMMessage(role=Role.user, content="add a test"),
            LLMMessage(
                role=Role.assistant, content="",
                tool_calls=[_make_tc(
                    "write_file",
                    json.dumps({"path": "", "content": "import os\n"}),
                    "tc_integration",
                )],
            ),
        ])
        # Build the ResolvedToolCall the tool would have produced.
        # Pydantic schema permits empty path here because the
        # tool itself validates and emits the sentinel error.
        rtc = ResolvedToolCall(
            tool_name="write_file",
            tool_class=WriteFile,
            validated_args=WriteFileArgs(path="", content="import os\n"),
            call_id="tc_integration",
        )
        # Mimic what the agent loop does next: call
        # _handle_tool_response with the failure status + the
        # canonical validation-sentinel error text.
        loop._handle_tool_response(
            rtc,
            text=(
                "NO path supplied. Pick a concrete file path under "
                "the current project, then re-emit with that path "
                "and the full file content."
            ),
            status="failure",
        )

        # The assistant's failed tool_call.arguments must now be {}.
        # If this assertion ever fails: the bait is back in history,
        # the bug is re-introduced, the fix is gone.
        scrubbed = _assistant_args(loop, "tc_integration").strip()
        assert scrubbed == "{}", (
            f"INTEGRATION: scrub failed to fire via "
            f"_handle_tool_response. args={scrubbed!r}"
        )

    def test_write_file_empty_path_production_path_e2e(self):
        """The MOST IMPORTANT test in this file. The bug recurred in the
        operator's 9-min loop AFTER v2.9.14 shipped scrub-tests-passing.
        Reason: prior tests planted bait in history and called the
        scrub helper. They never drove write_file's actual run()
        generator with empty path AND captured the same text the
        dispatcher would synthesize. This test does that, end-to-end.

        If THIS test ever regresses, the operator-visible loop will be
        back. The unit-level scrub helper passing means nothing if the
        actual sentinel text in production doesn't match the patterns
        in _VALIDATION_ERROR_PATTERNS."""
        import asyncio
        from drydock.core.types import LLMMessage, Role
        from drydock.core.llm.format import ResolvedToolCall
        from drydock.core.tools.base import BaseToolState
        from drydock.core.tools.builtins.write_file import (
            WriteFile, WriteFileArgs, WriteFileConfig, WriteFileResult,
        )

        async def _drain():
            args = WriteFileArgs(path="", content="x = 1\n")
            config = WriteFileConfig()
            state = BaseToolState()
            tool = WriteFile(config=config, state=state)
            results = []
            async for item in tool.run(args):
                if isinstance(item, WriteFileResult):
                    results.append(item)
            return results

        results = asyncio.run(_drain())
        assert len(results) == 1, (
            f"empty-path write_file must yield exactly one result, got {len(results)}"
        )
        result = results[0]
        # Mirror the dispatcher's serialization (agent_loop.py:2527):
        result_dict = result.model_dump()
        production_text = "\n".join(f"{k}: {v}" for k, v in result_dict.items())

        # 1. Result fields the TUI uses to render:
        assert result.path == "(missing)", (
            f"path field must be '(missing)' for TUI failure-display "
            f"detection, got {result.path!r}"
        )
        assert result.bytes_written == 0, "bytes_written must be 0"

        # 2. The serialized production text must trigger sentinel match:
        loop = build_test_agent_loop()
        assert loop._is_validation_error(production_text), (
            f"PRODUCTION REGRESSION: write_file's empty-path serialized "
            f"text no longer matches any _VALIDATION_ERROR_PATTERNS. "
            f"The scrub will not fire. text={production_text[:200]!r}"
        )

        # 3. End-to-end through _handle_tool_response WITH status="success"
        #    (the production status for yielded WriteFileResult):
        loop.messages.reset([
            LLMMessage(role=Role.system, content="x"),
            LLMMessage(role=Role.user, content="add a test"),
            LLMMessage(
                role=Role.assistant, content="",
                tool_calls=[_make_tc(
                    "write_file",
                    json.dumps({"path": "", "content": "x = 1\n"}),
                    "tc_e2e",
                )],
            ),
        ])
        rtc = ResolvedToolCall(
            tool_name="write_file",
            tool_class=WriteFile,
            validated_args=WriteFileArgs(path="", content="x = 1\n"),
            call_id="tc_e2e",
        )
        loop._handle_tool_response(rtc, text=production_text, status="success")

        scrubbed = _assistant_args(loop, "tc_e2e").strip()
        assert scrubbed == "{}", (
            f"E2E REGRESSION: operator's 9-min loop is back. The "
            f"actual write_file empty-path text + status='success' "
            f"path did NOT scrub args. args={scrubbed!r}"
        )

    def test_scrub_fires_on_success_status_with_sentinel(self):
        """Operator session 2026-05-31 PM hit a 9+ minute loop showing
        ✓ Created (missing) repeatedly. Root cause: write_file's
        empty-path branch returns a WriteFileResult (yielded, not
        raised), so the dispatcher records status="success" even
        though the result content is the validation sentinel. The
        scrub originally only fired on status="failure", so this
        bait sat in history unscrubbed across every loop iteration.

        Fix (2026-05-31 PM hotfix): scrub fires whenever the result
        text contains a validation sentinel, regardless of dispatcher
        status. This test asserts that behavior at the integration
        level — if it ever fails, the bug is back."""
        from drydock.core.types import LLMMessage, Role
        from drydock.core.llm.format import ResolvedToolCall
        from drydock.core.tools.builtins.write_file import (
            WriteFile, WriteFileArgs,
        )

        loop = build_test_agent_loop()
        loop.messages.reset([
            LLMMessage(role=Role.system, content="x"),
            LLMMessage(role=Role.user, content="add a test"),
            LLMMessage(
                role=Role.assistant, content="",
                tool_calls=[_make_tc(
                    "write_file",
                    json.dumps({"path": "", "content": "import os\n"}),
                    "tc_success_path",
                )],
            ),
        ])
        rtc = ResolvedToolCall(
            tool_name="write_file",
            tool_class=WriteFile,
            validated_args=WriteFileArgs(path="", content="import os\n"),
            call_id="tc_success_path",
        )
        # KEY DIFFERENCE: status="success" — this is what the dispatcher
        # passes when write_file yields a WriteFileResult (the
        # empty-path branch). Pre-hotfix this skipped the scrub.
        loop._handle_tool_response(
            rtc,
            text=(
                "NO path supplied. Pick a concrete file path under "
                "the current project, then re-emit with that path "
                "and the full file content."
            ),
            status="success",
        )

        scrubbed = _assistant_args(loop, "tc_success_path").strip()
        assert scrubbed == "{}", (
            f"REGRESSION: scrub did NOT fire on status='success' + "
            f"validation sentinel. The operator's 9-minute "
            f"✓ Created (missing) loop is back. args={scrubbed!r}"
        )

    def test_repeated_failures_each_get_scrubbed(self):
        """Operator session 2026-05-31 cycled 5+ identical empty-path
        calls. With the scrub firing on EACH failure, every successive
        assistant tool_call lands clean."""
        from drydock.core.types import LLMMessage, Role
        loop = build_test_agent_loop()
        # Plant a chain: 3 failed attempts, each with bad args.
        msgs = [
            LLMMessage(role=Role.system, content="be helpful"),
            LLMMessage(role=Role.user, content="add a test"),
        ]
        for i in range(3):
            tc_id = f"tc_chain_{i}"
            msgs.extend([
                LLMMessage(
                    role=Role.assistant, content="",
                    tool_calls=[_make_tc(
                        "write_file",
                        json.dumps({"path": "", "content": f"v{i}\n"}),
                        tc_id,
                    )],
                ),
                LLMMessage(
                    role=Role.tool, tool_call_id=tc_id, name="write_file",
                    content="NO path supplied. Pick a concrete file path.",
                ),
            ])
        loop.messages.reset(msgs)

        # Scrub each one in turn (what _handle_tool_response does
        # immediately after each failed call lands).
        for i in range(3):
            loop._scrub_validation_error_call(
                _FakeResolvedToolCall(f"tc_chain_{i}", "write_file")
            )

        # Every assistant tool_call in history is now empty-args.
        bait_count = 0
        for m in loop.messages:
            if m.role != Role.assistant or not m.tool_calls:
                continue
            for tc in m.tool_calls:
                args = (tc.function.arguments or "").strip()
                if args and args != "{}":
                    bait_count += 1
        assert bait_count == 0, (
            f"expected 0 baity calls in history after scrub-all; "
            f"found {bait_count}"
        )
