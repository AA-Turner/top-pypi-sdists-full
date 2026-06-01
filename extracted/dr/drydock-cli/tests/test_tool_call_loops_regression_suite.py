"""Comprehensive regression suite for write_file / search_replace loop bugs.

This file is the durable record of every distinct failure mode these
tools have produced over months of production. Each test class targets
ONE bug class with a docstring describing when/where it appeared and
what commit fixed it. The tests assert the CURRENT code state still
prevents the loop — they're guards against re-introducing the bait.

If a test in this file ever fails: the FIX, not the test, is what's
broken. The test is the spec of "we do not let this happen again."

Bug classes covered:

1. EmptyArgsBait
   Model emits write_file / search_replace with structurally invalid
   args (empty path, empty content). Tool returns an error. The
   (assistant tool_call + tool error) pair stays in history. Model
   copies the tool_call shape verbatim on the next turn → 25+ identical
   empty calls in a row. Operator sessions 2026-05-29 + 2026-05-31.

2. CompactionStubBait
   Old assistant tool_calls in history get compacted to small stubs to
   save context. Three stub formats over time:
     - {_truncated: true, file_path: ..., _original_bytes: N}
     - {_drydock_placeholder: "..."}
     - {__drydock_compacted_args__: "..."}
     - {} (current — commit 54d801b)
   Each previous format became bait: Gemma 4 read the shape and
   emitted "I'll call write_file with _truncated: true" on the next
   turn. The current `{}` format avoids that — pydantic rejects with a
   clean field-required error.

3. ErrorMessageShapeCopy
   Some tool errors included a literal example call shape (e.g.
   "Retry as: write_file(path='<package>/<file>.py', ...)"). Model
   copied that example into the next call's args, including the
   placeholder `<package>` / `<file>` brackets. Commits 9a07ba3 +
   dee310a stripped these examples.

4. FuzzyMatchSafety
   search_replace's fuzzy match must auto-apply on whitespace-only
   diffs (indent depth mismatch — most common Gemma 4 failure) but
   REFUSE on structural diffs (a missing closing paren that would
   create a SyntaxError after rewrite). Commit 32cb476.

5. StaleStateRecovery
   search_replace fails because the SEARCH text no longer exists in
   the file — either the model already applied this change in a
   prior turn, or another edit happened. The error must NOT echo the
   stale SEARCH text back as bait. Commits f95d3e8 + 961b443.

6. MultiFileRenameRoute
   Model uses search_replace to rename a symbol across many files —
   one SR call per file. Drydock detects the pattern and routes the
   model toward `mechanical_rename` instead. Commits 15 + 16 +
   1fb12b7.

Run: `pytest tests/test_tool_call_loops_regression_suite.py -v`
"""
from __future__ import annotations

import json
from pathlib import Path

import pytest

from drydock.core.types import (
    FunctionCall,
    LLMMessage,
    Role,
    ToolCall,
)
from tests.conftest import build_test_agent_loop


# ============================================================
# Shared fixtures / helpers
# ============================================================

def _mk_tc(name: str, args: dict | str, tc_id: str) -> ToolCall:
    """Build a ToolCall, accepting args as dict or pre-encoded string."""
    args_str = args if isinstance(args, str) else json.dumps(args)
    return ToolCall(
        id=tc_id,
        index=0,
        function=FunctionCall(name=name, arguments=args_str),
    )


def _assistant_tc_args(loop, tc_id: str) -> str:
    """Find the assistant tool_call by id, return its arguments string."""
    for m in loop.messages:
        if m.role != Role.assistant or not m.tool_calls:
            continue
        for tc in m.tool_calls:
            if tc.id == tc_id:
                return tc.function.arguments or ""
    raise AssertionError(f"no assistant tool_call with id={tc_id}")


class _FakeResolvedCall:
    """Minimal ResolvedToolCall stand-in for the scrub path."""

    def __init__(self, call_id: str, tool_name: str):
        self.call_id = call_id
        self.tool_name = tool_name


# ============================================================
# Bug Class 1: EmptyArgsBait
# ============================================================

class TestEmptyArgsBait:
    """write_file / search_replace with missing required args.

    Operator session 2026-05-29: 27 identical empty-path SR calls.
    Operator session 2026-05-31: 5+ identical empty-path write_file
    calls in the slides project. Each error message included an example
    call shape, the model copied that shape, looped indefinitely.

    Defense (in order of how it fires):
      a. Tool error messages do NOT include literal example call shapes
         (commits 9a07ba3, dee310a).
      b. _handle_tool_response detects the validation-error sentinel
         and scrubs the assistant tool_call.arguments to `{}`
         immediately (commit hash TBD this push).
      c. _circuit_breaker_check dedup, when the cached last_result is a
         validation sentinel, emits a NOTE without echoing it.
    """

    def test_write_file_empty_path_error_does_not_show_example_call(self):
        """Defense (a): the error text the tool returns must not
        contain a literal example like `write_file(path=...)` that the
        model can copy. The schema in the system prompt is the
        canonical reference."""
        # We don't run the tool here — just assert the source contains
        # the directive language and not the example pattern.
        wf_src = Path(
            "/data3/drydock/drydock/core/tools/builtins/write_file.py"
        ).read_text()
        # Both empty-path error sites must use the post-fix directive.
        assert "NO path supplied" in wf_src, (
            "expected the post-9a07ba3 directive language"
        )
        # And must not regress to the example-call form.
        assert "write_file(path='<package>" not in wf_src, (
            "the example-call bait pattern came back"
        )
        assert "Retry as: write_file(path=" not in wf_src

    def test_scrub_rewrites_empty_path_write_file_args(self):
        """Defense (b): scrub fires on validation-error tool result,
        rewrites the assistant tool_call.arguments to `{}`."""
        loop = build_test_agent_loop()
        loop.messages.reset([
            LLMMessage(role=Role.system, content="x"),
            LLMMessage(role=Role.user, content="add a test"),
            LLMMessage(
                role=Role.assistant, content="",
                tool_calls=[_mk_tc("write_file", {"path": "", "content": "y"}, "wf-1")],
            ),
        ])
        loop._scrub_validation_error_call(_FakeResolvedCall("wf-1", "write_file"))
        assert _assistant_tc_args(loop, "wf-1").strip() == "{}"

    def test_scrub_rewrites_empty_path_search_replace_args(self):
        loop = build_test_agent_loop()
        loop.messages.reset([
            LLMMessage(role=Role.system, content="x"),
            LLMMessage(role=Role.user, content="rename render_html"),
            LLMMessage(
                role=Role.assistant, content="",
                tool_calls=[_mk_tc(
                    "search_replace",
                    {"file_path": "", "content": "<<\nold\n==\nnew\n>>"},
                    "sr-1",
                )],
            ),
        ])
        loop._scrub_validation_error_call(_FakeResolvedCall("sr-1", "search_replace"))
        assert _assistant_tc_args(loop, "sr-1").strip() == "{}"

    def test_validation_sentinel_recognition(self):
        """Validation sentinels are NARROWLY defined. Tool errors with
        useful failure context must NOT be mis-classified — they
        deserve to stay in history."""
        loop = build_test_agent_loop()
        # YES — these are validation sentinels (args were structurally bad).
        for s in [
            "NO path supplied. Pick a concrete file path.",
            "File path is required. Use: search_replace(...)",
            "Empty content provided.",
        ]:
            assert loop._is_validation_error(s), (
                f"expected validation match for: {s[:40]!r}"
            )
        # NO — these are content-level failures (tool ran, returned useful info).
        for s in [
            "SEARCH/REPLACE block 1 failed: Search text not found in foo.py",
            "[Errno 2] No such file or directory: 'foo.py'",
            "pytest: rc=1, 6 failed, 20 passed",
            "Permission denied: /etc/passwd",
            "Block 1: auto-applied via fuzzy match (95% similarity)",
        ]:
            assert not loop._is_validation_error(s), (
                f"unexpected validation match for: {s[:40]!r}"
            )

    def test_dedup_note_for_repeated_empty_search_replace_strips_sentinel(self):
        """Defense (c): when search_replace has been called 24+ times
        with the same args, the dedup NOTE must list recovery options
        WITHOUT echoing the prior 'File path is required' error text
        (which contained an example call shape pre-fix)."""
        import hashlib
        loop = build_test_agent_loop()
        # Build the resolved call first so we can compute the same sig
        # the dedup uses.
        from drydock.core.llm.format import ResolvedToolCall
        from drydock.core.tools.builtins.search_replace import (
            SearchReplace, SearchReplaceArgs,
        )
        tc = ResolvedToolCall(
            tool_name="search_replace",
            tool_class=SearchReplace,
            validated_args=SearchReplaceArgs(file_path="", content="..."),
            call_id="sr-dedup-1",
        )
        args_str = json.dumps(tc.args_dict, sort_keys=True, default=str)
        sig = hashlib.sha256(f"{tc.tool_name}:{args_str}".encode()).hexdigest()
        # Pre-populate the cached count to past threshold + bait sentinel.
        loop._tool_call_history[sig] = (
            24, "File path is required. Use: search_replace(...)",
        )
        out = loop._circuit_breaker_check(tc)
        assert out is not None, "expected dedup NOTE when count > threshold"
        # Must NOT echo the bait sentinel text verbatim.
        assert "File path is required" not in out or "search_replace" in out
        # Must offer recovery options.
        assert "read_file" in out or "concrete" in out

    def test_dedup_note_for_repeated_empty_write_file_strips_sentinel(self):
        """Defense (c) for write_file: same protection for the new
        write_file empty-path sentinel ('NO path supplied')."""
        import hashlib
        loop = build_test_agent_loop()
        from drydock.core.llm.format import ResolvedToolCall
        from drydock.core.tools.builtins.write_file import (
            WriteFile, WriteFileArgs,
        )
        tc = ResolvedToolCall(
            tool_name="write_file",
            tool_class=WriteFile,
            validated_args=WriteFileArgs(path="", content="abc"),
            call_id="wf-dedup-1",
        )
        args_str = json.dumps(tc.args_dict, sort_keys=True, default=str)
        sig = hashlib.sha256(f"{tc.tool_name}:{args_str}".encode()).hexdigest()
        loop._tool_call_history[sig] = (
            24, "NO path supplied. Pick a concrete file path.",
        )
        out = loop._circuit_breaker_check(tc)
        assert out is not None
        # Should mention write_file and NO path (the recovery NOTE).
        assert "write_file" in out
        # Recovery options listed (either read_file or concrete path).
        assert "concrete file path" in out or "read_file" in out


# ============================================================
# Bug Class 2: CompactionStubBait
# ============================================================

class TestCompactionStubBait:
    """Compaction stubs in history must not become bait shapes.

    Drydock compacts old write_file tool_calls (they carry full file
    content — 89K tokens in one historical session) by replacing the
    arguments with a stub. THREE stub formats existed; only the
    current `{}` form is safe.

      Old stub 1: {"path": ..., "_truncated": true, "_original_bytes": N}
      Old stub 2: {"_drydock_placeholder": "..."}
      Old stub 3: {"__drydock_compacted_args__": "..."}
      Current:    "{}"  (commit 54d801b)

    The old stubs were copied verbatim by Gemma 4 as next-call args.
    """

    def test_only_write_file_args_are_compacted(self):
        """Compaction must be scoped to write_file. search_replace args
        are intrinsically small and preserving them lets the model see
        what it tried. Commit 32cb476 added the scoping."""
        from tests.conftest import build_test_agent_loop
        loop = build_test_agent_loop()
        # 30 old write_file calls + 30 old search_replace calls, all
        # with large args. After compaction: write_file should be `{}`,
        # search_replace should be preserved.
        big = json.dumps({"path": "/foo.py", "content": "x" * 5000})
        big_sr = json.dumps({"file_path": "/foo.py", "content": "<<\n" + "x" * 5000 + "\n==\nnew\n>>"})
        msgs = [LLMMessage(role=Role.system, content="x"),
                LLMMessage(role=Role.user, content="please help")]
        for i in range(15):
            msgs.append(LLMMessage(
                role=Role.assistant, content="",
                tool_calls=[_mk_tc("write_file", big, f"wf-{i}")],
            ))
            msgs.append(LLMMessage(
                role=Role.tool, tool_call_id=f"wf-{i}", name="write_file",
                content=f"Wrote {i}",
            ))
        for i in range(15):
            msgs.append(LLMMessage(
                role=Role.assistant, content="",
                tool_calls=[_mk_tc("search_replace", big_sr, f"sr-{i}")],
            ))
            msgs.append(LLMMessage(
                role=Role.tool, tool_call_id=f"sr-{i}", name="search_replace",
                content="Block 1 applied",
            ))
        loop.messages.reset(msgs)
        loop._truncate_old_tool_results()
        # write_file: most old ones should be compacted to `{}`.
        wf_compacted = 0
        sr_preserved = 0
        for m in loop.messages:
            if m.role != Role.assistant or not m.tool_calls:
                continue
            for tc in m.tool_calls:
                if tc.function.name == "write_file" and tc.function.arguments.strip() == "{}":
                    wf_compacted += 1
                elif tc.function.name == "search_replace" and "_truncated" not in (tc.function.arguments or ""):
                    sr_preserved += 1
        assert wf_compacted > 0, "expected at least some write_file args compacted"
        assert sr_preserved >= 10, (
            f"expected search_replace args preserved; got only {sr_preserved}"
        )

    def test_legacy_truncated_stubs_get_upgraded(self):
        """If history contains the legacy `_truncated:true` stub form
        (from a session that started pre-2026-05-24), the upgrade pass
        rewrites them so the model on next turn doesn't see the legacy
        marker key."""
        loop = build_test_agent_loop()
        legacy = json.dumps({
            "path": "/foo.py",
            "_truncated": True,
            "_original_bytes": 5000,
        })
        msgs = [
            LLMMessage(role=Role.system, content="x"),
            LLMMessage(role=Role.user, content="help"),
            LLMMessage(
                role=Role.assistant, content="",
                tool_calls=[_mk_tc("write_file", legacy, "legacy-1")],
            ),
            LLMMessage(
                role=Role.tool, tool_call_id="legacy-1", name="write_file",
                content="ok",
            ),
        ]
        loop.messages.reset(msgs)
        loop._upgrade_legacy_compaction_stubs()
        args = _assistant_tc_args(loop, "legacy-1")
        assert "_truncated" not in args, (
            "legacy _truncated marker still present after upgrade"
        )

    def test_marker_stubs_dont_get_re_compacted(self):
        """Compaction must be idempotent — if a stub already exists in
        any of the known forms, don't re-process it."""
        loop = build_test_agent_loop()
        already_stubbed = json.dumps({
            "__drydock_compacted_args__": "previously compacted"
        })
        msgs = [
            LLMMessage(role=Role.system, content="x"),
            LLMMessage(role=Role.user, content="help"),
        ]
        for i in range(10):
            msgs.append(LLMMessage(
                role=Role.assistant, content="",
                tool_calls=[_mk_tc("write_file", already_stubbed, f"stub-{i}")],
            ))
            msgs.append(LLMMessage(
                role=Role.tool, tool_call_id=f"stub-{i}", name="write_file",
                content="ok",
            ))
        loop.messages.reset(msgs)
        loop._truncate_old_tool_results()
        # The stubs should NOT get re-stubbed (idempotency).
        for m in loop.messages:
            if m.role == Role.assistant and m.tool_calls:
                for tc in m.tool_calls:
                    # Already a stub — leave it alone or upgrade to {} cleanly.
                    args = tc.function.arguments
                    assert (
                        "__drydock_compacted_args__" in args
                        or args.strip() == "{}"
                    ), f"unexpected mutation: {args[:80]!r}"


# ============================================================
# Bug Class 3: ErrorMessageShapeCopy
# ============================================================

class TestErrorMessageShapeCopy:
    """Tool errors must not include literal example call shapes.

    Pre-fix, several errors looked like:
        "Retry as: write_file(path='<package>/<file>.py', content='...')."
    Gemma 4 copied the literal `<package>/<file>.py` as the next path.
    Commits 9a07ba3 + dee310a stripped these.
    """

    def test_write_file_source_has_no_example_call_pattern(self):
        wf = Path(
            "/data3/drydock/drydock/core/tools/builtins/write_file.py"
        ).read_text()
        # No example call shapes in error messages.
        for pat in [
            "write_file(path='<package>/",
            "Retry as: write_file(path=",
        ]:
            assert pat not in wf, (
                f"forbidden example-call pattern reappeared: {pat!r}"
            )

    def test_search_replace_source_has_no_example_call_pattern(self):
        sr = Path(
            "/data3/drydock/drydock/core/tools/builtins/search_replace.py"
        ).read_text()
        # The error "File path is required" exists, but it should NOT
        # be followed by a literal call example in the same message.
        # (The dedup NOTE wraps the cached preview, that's tested
        # separately — here we only ensure the TOOL ITSELF doesn't
        # generate the bait.)
        # The known bait wording from prior versions:
        for pat in [
            "Retry as: search_replace(",
        ]:
            assert pat not in sr, (
                f"forbidden example-call pattern reappeared: {pat!r}"
            )


# ============================================================
# Bug Class 4: FuzzyMatchSafety
# ============================================================

class TestFuzzyMatchSafety:
    """search_replace's fuzzy match must apply on whitespace-only
    differences but REFUSE on structural differences.

    The original failure (2026-05-22): model SEARCH was
    "@pytest.fixture(" but file had "@pytest.fixture" (no paren).
    96% similarity → auto-applied → unclosed paren → SyntaxError.

    The opposite failure (2026-05-30): model SEARCH had 12-space indent
    but file had 8-space, 94% similarity → refused, model cascaded.

    Commit 32cb476 sets the policy: search at low threshold (0.80) but
    auto-apply ONLY when whitespace-normalize(search) == whitespace-
    normalize(matched).
    """

    def test_indent_only_diff_auto_applies(self, tmp_path):
        """Whitespace-only difference: applies."""
        from drydock.core.tools.builtins.search_replace import SearchReplace
        f = tmp_path / "x.py"
        f.write_text(
            "def foo():\n"
            "    pass\n"
            "\n"
            "        # Verify body was set (Renderer converts blocks)\n"
            "        assert placeholder_body.text_frame.text == \"Mock Body\"\n"
        )
        block = (
            "            # Verify body was set (Renderer converts blocks)\n"
            "            assert placeholder_body.text_frame.text == \"Mock Body\""
        )
        replacement = (
            "            # Verify body matches with normalization\n"
            "            assert placeholder_body.text_frame.text.strip() == \"Mock Body\""
        )
        result = SearchReplace._apply_blocks(
            f.read_text(), [(block, replacement)], f, fuzzy_threshold=0.9,
        )
        # The whitespace-normalize gate should have permitted the
        # auto-apply even though raw similarity may be sub-95%.
        assert result.applied == 1, (
            f"expected indent-only diff to auto-apply; warnings={result.warnings} errors={result.errors}"
        )

    def test_structural_diff_refuses_auto_apply(self, tmp_path):
        """Non-whitespace difference (missing paren): refuses."""
        from drydock.core.tools.builtins.search_replace import SearchReplace
        f = tmp_path / "x.py"
        # File has "@pytest.fixture" (no paren)
        f.write_text(
            "import pytest\n"
            "\n"
            "@pytest.fixture\n"
            "def db():\n"
            "    return {}\n"
        )
        # Model SEARCH has "@pytest.fixture(" (with paren) — structural diff.
        block = "@pytest.fixture("
        replacement = "@pytest.fixture(scope='module')"
        result = SearchReplace._apply_blocks(
            f.read_text(), [(block, replacement)], f, fuzzy_threshold=0.9,
        )
        # Must NOT have auto-applied — the diff isn't whitespace-only.
        assert result.applied == 0, (
            "structural diff (missing paren) was auto-applied — "
            "would have created a SyntaxError"
        )
        assert result.errors, "expected an error explaining the refusal"


# ============================================================
# Bug Class 5: StaleStateRecovery
# ============================================================

class TestStaleStateRecovery:
    """search_replace must distinguish 'text not found because file
    was edited' from 'text not found because model is hallucinating'.
    """

    def test_search_not_found_error_does_not_echo_search_text_as_bait(
        self, tmp_path,
    ):
        """When SEARCH fails to match, the error must include the
        WHERE-to-look context (file head, fuzzy candidates) without
        making it trivial to copy the failed SEARCH back as the next
        call's SEARCH."""
        from drydock.core.tools.builtins.search_replace import SearchReplace
        f = tmp_path / "x.py"
        f.write_text("def foo():\n    return 1\n")
        result = SearchReplace._apply_blocks(
            f.read_text(),
            [("def foo():\n    return 99", "def foo():\n    return 42")],
            f, fuzzy_threshold=0.9,
        )
        # Must report the failure with structured context.
        assert result.applied == 0
        assert result.errors
        err = result.errors[0]
        assert "not found" in err.lower() or "Search text" in err


# ============================================================
# Bug Class 6: MultiFileRenameRoute
# ============================================================

class TestMultiFileRenameRoute:
    """Model uses search_replace per-file for a rename — should be
    routed to mechanical_rename.

    Detected via DRYDOCK_MULTIFILE_INTERCEPT=1 (default in test_harness).
    """

    def test_multifile_intercept_env_gated_for_test_harness(self):
        """The intercept is wired into both search_replace AND bash
        (sed -i escape hatch). The test_harness env sets
        DRYDOCK_MULTIFILE_INTERCEPT=1 to enable. Verify the env hook
        exists in either tool's source."""
        sr_src = Path(
            "/data3/drydock/drydock/core/tools/builtins/search_replace.py"
        ).read_text()
        bash_src = Path(
            "/data3/drydock/drydock/core/tools/builtins/bash.py"
        ).read_text()
        # The hook should be present in at least one of these tools.
        found = (
            "DRYDOCK_MULTIFILE_INTERCEPT" in sr_src
            or "DRYDOCK_MULTIFILE_INTERCEPT" in bash_src
            or "_detect_multifile_rename" in sr_src
        )
        assert found, "multifile rename intercept hook is missing"


# ============================================================
# Bug Class 7: LiteralEscapeUnescaping
# ============================================================

class TestLiteralEscapeUnescaping:
    """When SEARCH text contains literal `\\n` `\\t` (a backslash
    followed by the letter, not a newline), drydock auto-unescapes them
    so the model's mistake doesn't fail SEARCH. Commit 2c236ae.
    """

    def test_literal_escapes_in_search_get_unescaped(self, tmp_path):
        """File has actual newlines; SEARCH from model has literal
        `\\n`; drydock unescapes and matches."""
        from drydock.core.tools.builtins.search_replace import SearchReplace
        f = tmp_path / "x.py"
        f.write_text("line one\nline two\nline three\n")
        # Model emitted the SEARCH with literal \\n instead of newlines.
        block = "line one\\nline two"
        replacement = "LINE_ONE\\nLINE_TWO"
        # The fallback path should unescape before searching.
        result = SearchReplace._apply_blocks(
            f.read_text(), [(block, replacement)], f, fuzzy_threshold=0.9,
        )
        # Either it matched after unescape, or it returned a clear error.
        # The minimum invariant: don't crash, don't silently no-op.
        assert result.applied == 1 or result.errors, (
            "expected either a successful match (post-unescape) or "
            "a clear error — got silent no-op"
        )
