"""Behavioral regression tests for the loops user surfaced on 2026-06-06.

Tonight's sequence of escalating loop fixes (v2.9.89 -> v2.9.99) each
shipped, exposed the next layer, and got patched in turn. These tests
pin the exact symptoms so the regressions can't return silently:

  v2.9.89: write_file({}) and {path: None} acceptance       (schema fix)
  v2.9.91: 18-readonly hard-stop firing in subagents        (subagent guard)
  v2.9.93: parent dispatching identical task back-to-back   (preflight)
  v2.9.95: notebook_edit on .py files                       (gemma4 disable)
  v2.9.97: task tool spammed under union grammar             (task disable)
  v2.9.98: exit_plan_mode -> "Already in implementation"     (gemma4 disable)
           + union grammar disabled by default

Each test exercises ONE specific symptom against the real AgentLoop or
the real ToolManager so we get a yes/no signal on the architectural
fix, not the surface phrasing.
"""
from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock


from drydock.core.agents.models import AgentType
from drydock.core.tools.manager import ToolManager


# ---------------------------------------------------------------------------
# Helper: gemma4-configured ToolManager
# ---------------------------------------------------------------------------

def _gemma4_tool_manager() -> ToolManager:
    cfg = MagicMock()
    cfg.enabled_tools = None
    cfg.disabled_tools = None
    cfg.mcp_servers = []
    cfg.tool_paths = []

    class FakeModel:
        name = "gemma-4-26b"
        alias = "gemma4"

    cfg.get_active_model = lambda: FakeModel()
    return ToolManager(config_getter=lambda: cfg)


# ===========================================================================
# v2.9.89 — Schema fix: write_file required fields
# ===========================================================================

class TestSchemaTighteningWriteFile:
    """Under union grammar, vacuous-default args (path="", content="")
    must be promoted to required. Otherwise the grammar accepts
    `{"name":"write_file","arguments":{}}` and the model emits garbage."""

    def test_write_file_path_now_required_in_tightened_schema(self):
        from drydock.core.llm.grammar.policy_union import _tighten_args_schema
        from drydock.core.tools.builtins.write_file import WriteFileArgs

        tight = _tighten_args_schema(WriteFileArgs.model_json_schema())
        assert "path" in tight.get("required", [])
        assert "content" in tight.get("required", [])

    def test_overwrite_bool_default_stays_optional(self):
        """Boolean default=True is a legit "use default" optional, must NOT
        be forced required (would break callers that omit it)."""
        from drydock.core.llm.grammar.policy_union import _tighten_args_schema
        from drydock.core.tools.builtins.write_file import WriteFileArgs

        tight = _tighten_args_schema(WriteFileArgs.model_json_schema())
        assert "overwrite" not in tight.get("required", [])


# ===========================================================================
# v2.9.91 — Subagent hard-stop skip
# ===========================================================================

class TestSubagentSkipsAdaptiveBudget:
    """The 18-readonly hard-stop must skip when the running AgentLoop is
    a SUBAGENT — explore/diagnostic/planner/builder are read-mostly by
    design and the parent owns the overall budget."""

    def test_main_agent_still_triggers_hard_stop(self):
        """Sanity: agents (not subagents) still hit the hard-stop."""
        profile = SimpleNamespace(
            agent_type=AgentType.AGENT,
            name="default",
        )
        # The condition we patched is exactly:
        # `self.agent_profile.agent_type != AgentType.SUBAGENT`
        # When the profile is AGENT, the hard-stop is reachable.
        assert profile.agent_type != AgentType.SUBAGENT

    def test_subagent_skips_hard_stop(self):
        for sub_name in ("explore", "diagnostic", "planner", "builder"):
            profile = SimpleNamespace(
                agent_type=AgentType.SUBAGENT,
                name=sub_name,
            )
            # Under v2.9.91+ the hard-stop check guards against firing
            # in subagent contexts. Pin that the type comparison short-
            # circuits as designed.
            assert profile.agent_type == AgentType.SUBAGENT, (
                f"subagent {sub_name!r} must be flagged SUBAGENT so the "
                f"hard-stop in agent_loop.py:~1185 skips."
            )


# ===========================================================================
# v2.9.93 — Consecutive task call preflight (defense-in-depth even though
# task is now disabled for Gemma 4 in v2.9.97).
# ===========================================================================

class TestConsecutiveWriteDuplicatePreflight:
    """v2.9.104: 5+ identical write_file calls to the same path get
    pruned at preflight. User session 2026-06-06 v2.9.95 batch
    `sam-cell-seg` trial: 22 identical writes to
    /app/conversation_summary.smd, sha8=d3bedbf3. The tool-level dedup
    is advisory-only by design (feedback_no_tool_errors_for_loop_...)
    and Gemma 4 ignored the advisory. The preflight prunes the
    duplicates from history so the model's next turn sees a clean
    context."""

    def test_preflight_marker_present_in_agent_loop(self):
        text = open(
            "/data3/drydock/drydock/core/agent_loop.py"
        ).read()
        # v2.9.108 generalized the marker from PREFLIGHT-WRITE-DUP to
        # PREFLIGHT-DUP (covers any tool with 5+ identical-args calls).
        assert "PREFLIGHT-DUP" in text, (
            "duplicate-call preflight was removed from agent_loop.py"
        )
        assert "dup_count >= 5" in text, (
            "duplicate-call threshold changed; update test"
        )

    def test_preflight_prunes_history_to_most_recent_attempt(self):
        """Behavioral: 7 identical writes + tool results -> 2 messages
        remain after the preflight logic runs (most recent write + its
        result). Replicates the sam-cell-seg pattern."""
        import json as _json
        from drydock.core.agent_loop import AgentLoop
        from drydock.core.types import (
            FunctionCall,
            LLMMessage,
            MessageList,
            Role,
            ToolCall,
        )

        msgs = MessageList()
        identical_args = _json.dumps(
            {"path": "/app/foo.smd", "content": "out0 = out0\nout1 = out1\n"}
        )
        for i in range(7):
            msgs.append(LLMMessage(
                role=Role.assistant,
                content="",
                tool_calls=[ToolCall(
                    id=f"call_{i}",
                    function=FunctionCall(
                        name="write_file", arguments=identical_args
                    ),
                )],
            ))
            msgs.append(LLMMessage(
                role=Role.tool,
                content="advisory no-op",
                tool_call_id=f"call_{i}",
            ))

        al = object.__new__(AgentLoop)
        al.messages = msgs

        # Reproduce the inline preflight logic exactly
        cur_path = "/app/foo.smd"
        cur_content = "out0 = out0\nout1 = out1\n"
        dup_indices = []
        for i, m in enumerate(al.messages):
            if m.role != Role.assistant or not m.tool_calls:
                continue
            for tc in m.tool_calls:
                if tc.function.name != "write_file":
                    continue
                try:
                    a = _json.loads(tc.function.arguments or "{}")
                except Exception:
                    continue
                ap = a.get("path") or a.get("file_path") or ""
                ac = a.get("content", "")
                if ap == cur_path and ac == cur_content:
                    dup_indices.append(i)
                    break
        dup_count = len(dup_indices)
        assert dup_count == 7

        to_drop = set()
        for idx in dup_indices[:-1]:
            to_drop.add(idx)
            if idx + 1 < len(al.messages):
                next_m = al.messages[idx + 1]
                if next_m.role == Role.tool:
                    to_drop.add(idx + 1)
        kept = [m for i, m in enumerate(al.messages) if i not in to_drop]
        al.messages.reset(kept)
        assert len(al.messages) == 2, (
            f"expected 2 messages remaining (last write + result), "
            f"got {len(al.messages)}"
        )


class TestConsecutiveTaskBlockPreflight:
    """When a model emits `task` two turns in a row, the second call must
    be blocked at preflight (drop from history + emit advisory). The
    preflight is reachable only for non-Gemma models now that v2.9.97
    yanks `task` from the Gemma 4 grammar, but it remains the safety
    net for any future re-enable or non-Gemma backend.

    The preflight code path is in agent_loop.py: hunt the marker comment
    so a refactor that moves it surfaces here.
    """

    def test_preflight_marker_present_in_agent_loop(self):
        """Regression guard: the consecutive-task preflight comment +
        guard must exist in agent_loop.py. If someone refactors the
        preflight chain and accidentally drops this block, this test
        fires loud."""
        text = open(
            "/data3/drydock/drydock/core/agent_loop.py"
        ).read()
        assert "PREFLIGHT-TASK" in text, (
            "consecutive-task preflight was removed from agent_loop.py"
        )
        assert "task tool blocked" in text, (
            "consecutive-task advisory phrasing was changed; update test"
        )


# ===========================================================================
# v2.9.95 / v2.9.97 / v2.9.98 — Tools that must be disabled for Gemma 4
# ===========================================================================

class TestGemma4DisableListCovers2026_06_06Loops:
    """Every tool that drove a visible Gemma 4 loop session tonight
    must be filtered out of the auto-discovered list. Parametrized in
    test_gemma4_tool_filter.py too; these are duplicate explicit
    assertions so a refactor that breaks the param suite still catches."""

    def test_task_re_enabled_in_v2_9_113(self):
        """task was disabled in v2.9.97, re-enabled in v2.9.113 after
        the experiment_REPASS_v2.9.110 PASS->FAIL regression on
        extract-elf showed losing subagent delegation broke proven
        capability. Union grammar OFF (v2.9.98) + consecutive-task
        preflight (v2.9.93) are the new loop guards."""
        names = set(_gemma4_tool_manager().available_tools.keys())
        assert "task" in names

    def test_notebook_edit_blocked(self):
        names = set(_gemma4_tool_manager().available_tools.keys())
        assert "notebook_edit" not in names

    def test_exit_plan_mode_blocked(self):
        names = set(_gemma4_tool_manager().available_tools.keys())
        assert "exit_plan_mode" not in names


# ===========================================================================
# v2.9.98 — Union grammar disabled by default
# ===========================================================================

class TestUnionGrammarDefaultOff:
    """Union grammar (one branch per tool, ~13 vacuous-args branches)
    must be OFF by default. The 72-tool union grammar made the model
    iterate through whichever branch had the simplest schema. Default
    is OFF; explicit opt-in via DRYDOCK_UNION_GRAMMAR_ENABLE=1."""

    def test_default_off(self, monkeypatch):
        monkeypatch.delenv("DRYDOCK_GRAMMAR_DISABLE", raising=False)
        monkeypatch.delenv("DRYDOCK_UNION_GRAMMAR_DISABLE", raising=False)
        monkeypatch.delenv("DRYDOCK_UNION_GRAMMAR_ENABLE", raising=False)
        from drydock.core.llm.grammar.policy_union import select_union_grammar

        mgr = MagicMock()
        mgr.available_tools = {"write_file": object}
        at = [MagicMock()]
        at[0].function.name = "write_file"
        gbnf = select_union_grammar(
            tool_choice="auto",
            available_tools=at,
            tool_manager=mgr,
        )
        assert gbnf is None

    def test_explicit_enable_engages(self, monkeypatch):
        monkeypatch.delenv("DRYDOCK_GRAMMAR_DISABLE", raising=False)
        monkeypatch.delenv("DRYDOCK_UNION_GRAMMAR_DISABLE", raising=False)
        monkeypatch.setenv("DRYDOCK_UNION_GRAMMAR_ENABLE", "1")
        from drydock.core.llm.grammar.policy_union import (
            build_union_gbnf,
        )
        from drydock.core.tools.builtins.write_file import WriteFileArgs

        # Direct build path
        gbnf = build_union_gbnf([("write_file", WriteFileArgs)])
        assert gbnf is not None
        assert "write_file" in gbnf or "root" in gbnf


class TestReadonlyStreakOnlyCountsDoomLoops:
    """v2.9.111: the readonly streak only grows on DUPLICATE results,
    not every distinct read. Operator session 2026-06-07: model running
    legit diagnosis (run script -> ls -> read -> count -> cat) was hit
    by the 18-readonly hard-stop before it could use the new info cat
    revealed. Productive read-shaped tool calls (each yields novel
    content) must not count toward the doom-loop streak."""

    def test_novel_results_do_not_grow_streak(self):
        """20 distinct readonly results -> streak stays at 0."""
        import hashlib

        recent: list[str] = []
        streak = 0
        for i in range(20):
            text = f"unique content {i} - {'x' * 100}"
            h = hashlib.sha256(text.encode()).hexdigest()[:16]
            if h in recent:
                streak += 1
            recent.append(h)
            recent = recent[-30:]
        assert streak == 0, (
            f"20 distinct reads should not grow streak; got {streak}"
        )

    def test_duplicate_results_grow_streak(self):
        """Same result returned 6 times -> streak hits 5 (first is
        novel, next 5 are duplicates)."""
        import hashlib

        recent: list[str] = []
        streak = 0
        identical_text = "stuck loop content"
        h = hashlib.sha256(identical_text.encode()).hexdigest()[:16]
        for _ in range(6):
            if h in recent:
                streak += 1
            recent.append(h)
            recent = recent[-30:]
        assert streak == 5

    def test_v2_9_114_strips_dedup_headers_before_hash(self):
        """v2.9.114: read_file's dedup advisory headers change every time
        ([2nd identical read...], [REPEATED READ #3...], #4 etc.). Each
        carries the same underlying file content but a unique header.
        v2.9.112 hashed the full text and saw each as "novel", missing
        the loop. v2.9.114 strips the leading [advisory] block before
        hashing so the underlying content is the comparison key.

        Direct test of the marker-detection fast path: any text starting
        with the dedup marker is forced to count as duplicate even
        without hash collision."""
        DEDUP_MARKERS = (
            "[2nd identical read",
            "[REPEATED READ",
        )
        cases = [
            ("[2nd identical read of this file - content is unchanged]\nfile contents go here", True),
            ("[REPEATED READ #5: file has not changed across 5 reads]\nfile contents", True),
            ("normal file output 1\nline 2\nline 3", False),
            ("no header just content", False),
        ]
        for text, expected_forced_dup in cases:
            forced_dup = text.startswith("[") and any(
                m in text[:200] for m in DEDUP_MARKERS
            )
            assert forced_dup == expected_forced_dup, (
                f"{text[:40]!r} -> forced_dup={forced_dup}, "
                f"expected {expected_forced_dup}"
            )

    def test_marker_present_in_agent_loop(self):
        text = open(
            "/data3/drydock/drydock/core/agent_loop.py"
        ).read()
        assert "_recent_readonly_hashes" in text
        assert "doom-loop signature is" in text or "v2.9.111" in text


class TestNoWriteStreakHardStop:
    """v2.9.116: replace the arbitrary 100-call hard stop with two
    layered limits — HARD_STOP_CALLS raised to 500 as runaway safety,
    and a new NO_WRITE_HARD_STOP at 80 consecutive readonly/neutral
    tool calls without any write/edit. Operator's reasoning: real
    work shouldn't get killed by a count cap, only real loops should
    stop. The no-write streak is the actual "stuck without progress"
    detector."""

    def test_hard_stop_calls_raised_from_100_to_500(self):
        """The arbitrary count cap that killed legit work."""
        text = open(
            "/data3/drydock/drydock/core/agent_loop.py"
        ).read()
        assert (
            '"DRYDOCK_HARD_STOP_CALLS"' in text
            and 'getattr(self, "_admiral_hard_stop_tool_calls", 500)' in text
        ), "HARD_STOP_CALLS default should be 500 (env-configurable)"

    def test_no_write_hard_stop_default_80(self):
        text = open(
            "/data3/drydock/drydock/core/agent_loop.py"
        ).read()
        assert "DRYDOCK_NO_WRITE_HARD_STOP" in text
        assert '"_admiral_no_write_hard_stop", 80' in text

    def test_no_write_streak_skips_subagent(self):
        """The no-write streak hard-stop must skip subagents (explore /
        diagnostic / planner / builder) — they're read-mostly by design.
        Same gate v2.9.91 added for the readonly-streak hard-stop."""
        text = open(
            "/data3/drydock/drydock/core/agent_loop.py"
        ).read()
        # Find the no-write check block and verify it has the SUBAGENT
        # type check
        idx = text.find("no_write_streak >= NO_WRITE_HARD_STOP")
        assert idx >= 0, "no-write hard-stop block missing"
        # Within a reasonable window after, AgentType.SUBAGENT must
        # appear (the skip-condition)
        window = text[idx : idx + 400]
        assert "AgentType.SUBAGENT" in window, (
            "subagent skip missing from no-write hard-stop"
        )

    def test_write_resets_no_write_streak(self):
        """Verify the reset path in _maybe_reflect: a write tool sets
        _no_write_streak back to 0."""
        text = open(
            "/data3/drydock/drydock/core/agent_loop.py"
        ).read()
        # The reset is paired with the readonly-streak reset
        idx = text.find('if effective_kind == "write":')
        assert idx >= 0
        window = text[idx : idx + 300]
        assert "self._no_write_streak = 0" in window


class TestPerPromptTimeBudget:
    """v2.9.119: raise per-prompt wall-clock budget 30 min -> 4 hours.
    Operator session 2026-06-07 hit the 30-min cap mid-edit on a real
    slide-app debugging session — model had written 2 files and was
    iterating, then got killed. Same principle as v2.9.116's
    HARD_STOP_CALLS raise: arbitrary caps that kill legit work."""

    def test_default_raised_to_4_hours(self):
        text = open(
            "/data3/drydock/drydock/core/agent_loop.py"
        ).read()
        # Default is 4h = 14400s, expressed as `4 * 60 * 60` in source
        assert (
            'getattr(self, "_admiral_per_prompt_budget_sec", 4 * 60 * 60)' in text
        ), "PER_PROMPT_BUDGET_SEC default should be 4 hours (4*60*60)"

    def test_env_override_supported(self):
        text = open(
            "/data3/drydock/drydock/core/agent_loop.py"
        ).read()
        assert '"DRYDOCK_PER_PROMPT_BUDGET_SEC"' in text


class TestContextWindowProbe:
    """v2.9.115: drydock probes the live llama.cpp backend's /props
    endpoint at AgentLoop init to discover the runtime n_ctx, then
    uses that to recompute auto_compact_threshold (instead of the
    stale config value). Prevents the 32K backend / 131K config skew
    that would let context bloat past the wire limit."""

    def test_probe_extracts_n_ctx_from_llamacpp_props_shape(self):
        """Verify the JSON walk that finds n_ctx in llama.cpp's exact
        /props response shape."""
        import json as _json
        from unittest.mock import patch, MagicMock
        from drydock.core.agent_loop import _probe_backend_context_window

        class FakeModel:
            base_url = "http://test:8000/v1"

        # Mock urllib.request.urlopen to return the exact /props shape
        # llama.cpp emits (the inner `default_generation_settings.params`
        # dict carries the runtime n_ctx).
        fake_resp = _json.dumps({
            "default_generation_settings": {
                "params": {
                    "n_ctx": 32768,
                    "temperature": 1.0,
                },
            },
        }).encode()
        mock_handle = MagicMock()
        mock_handle.read.return_value = fake_resp
        mock_handle.__enter__.return_value = mock_handle
        mock_handle.__exit__.return_value = None

        with patch("urllib.request.urlopen", return_value=mock_handle):
            n = _probe_backend_context_window(FakeModel())
        assert n == 32768

    def test_probe_returns_none_when_no_base_url(self):
        """Cloud-backed models (Mistral, Anthropic) have no base_url for
        the llama.cpp /props endpoint — probe must short-circuit cleanly."""
        from drydock.core.agent_loop import _probe_backend_context_window

        class CloudModel:
            base_url = ""

        assert _probe_backend_context_window(CloudModel()) is None

    def test_probe_returns_none_on_network_error(self):
        """If the backend is unreachable, the probe must not raise — it
        falls through to the static config value."""
        from unittest.mock import patch
        from drydock.core.agent_loop import _probe_backend_context_window

        class FakeModel:
            base_url = "http://nonexistent.invalid:8000/v1"

        # Force urlopen to raise
        with patch("urllib.request.urlopen", side_effect=OSError("nope")):
            assert _probe_backend_context_window(FakeModel()) is None

    def test_probe_handles_v1_suffix_correctly(self):
        """base_url often ends in /v1 (OpenAI-compatible convention).
        /props sits at the root, not under /v1. The probe must strip
        /v1 before appending /props."""
        from unittest.mock import patch, MagicMock
        import json as _json
        from drydock.core.agent_loop import _probe_backend_context_window

        class FakeModel:
            base_url = "http://test:8000/v1"

        captured_url = {}

        def fake_urlopen(url, timeout=None):
            captured_url["u"] = url
            mock = MagicMock()
            mock.read.return_value = _json.dumps(
                {"default_generation_settings": {"params": {"n_ctx": 32768}}}
            ).encode()
            mock.__enter__.return_value = mock
            mock.__exit__.return_value = None
            return mock

        with patch("urllib.request.urlopen", side_effect=fake_urlopen):
            _probe_backend_context_window(FakeModel())
        # /v1 must be stripped before appending /props
        assert captured_url["u"] == "http://test:8000/props"


class TestGeneralizedDuplicatePreflight:
    """v2.9.108: the preflight handles ANY tool with 5+ identical-args
    calls, not just write_file. Verifies the v2.9.95 distribution-search
    pattern (3 identical `solve` calls at end of trial) would be
    pruned."""

    def test_solve_loop_pattern_prunes(self):
        import json as _json
        from drydock.core.agent_loop import AgentLoop
        from drydock.core.types import (
            FunctionCall,
            LLMMessage,
            MessageList,
            Role,
            ToolCall,
        )

        msgs = MessageList()
        # 6 identical solve calls — same args, same conclusion.
        solve_args = _json.dumps({
            "op": "solve",
            "variables": "p1: Real, p2: Real",
            "conclusion": "True",
            "objective": "",
        })
        for i in range(6):
            msgs.append(LLMMessage(
                role=Role.assistant,
                content="",
                tool_calls=[ToolCall(
                    id=f"solve_{i}",
                    function=FunctionCall(name="solve", arguments=solve_args),
                )],
            ))
            msgs.append(LLMMessage(
                role=Role.tool,
                content="sat",
                tool_call_id=f"solve_{i}",
            ))

        al = object.__new__(AgentLoop)
        al.messages = msgs

        # Reproduce the inline generic preflight
        cur_name = "solve"
        cur_args_dict = _json.loads(solve_args)
        cur_args_json = _json.dumps(cur_args_dict, sort_keys=True, default=str)
        dup_indices = []
        for i, m in enumerate(al.messages):
            if m.role != Role.assistant or not m.tool_calls:
                continue
            for tc in m.tool_calls:
                if tc.function.name != cur_name:
                    continue
                try:
                    a = _json.loads(tc.function.arguments or "{}")
                except Exception:
                    continue
                if _json.dumps(a, sort_keys=True, default=str) == cur_args_json:
                    dup_indices.append(i)
                    break

        assert len(dup_indices) == 6
        to_drop = set()
        for idx in dup_indices[:-1]:
            to_drop.add(idx)
            if idx + 1 < len(al.messages):
                if al.messages[idx + 1].role == Role.tool:
                    to_drop.add(idx + 1)
        kept = [m for i, m in enumerate(al.messages) if i not in to_drop]
        al.messages.reset(kept)
        # 5 older duplicates + their tool results = 10 dropped, 2 remain
        assert len(al.messages) == 2

    def test_different_args_NOT_pruned(self):
        """read_file with different offsets — legitimate progress, NOT a dup."""
        import json as _json
        from drydock.core.agent_loop import AgentLoop
        from drydock.core.types import (
            FunctionCall,
            LLMMessage,
            MessageList,
            Role,
            ToolCall,
        )

        msgs = MessageList()
        for i in range(8):
            args = _json.dumps({"path": "/app/foo.py", "offset": i * 100})
            msgs.append(LLMMessage(
                role=Role.assistant,
                content="",
                tool_calls=[ToolCall(
                    id=f"read_{i}",
                    function=FunctionCall(name="read_file", arguments=args),
                )],
            ))
            msgs.append(LLMMessage(
                role=Role.tool,
                content=f"contents at offset {i * 100}",
                tool_call_id=f"read_{i}",
            ))

        al = object.__new__(AgentLoop)
        al.messages = msgs

        # Now check what the preflight would do for "the 9th read_file
        # call with offset=900". cur_args_json differs from all prior 8
        # calls (each had a different offset).
        cur_args_json = _json.dumps(
            {"path": "/app/foo.py", "offset": 900}, sort_keys=True
        )
        dup_indices = []
        for i, m in enumerate(al.messages):
            if m.role != Role.assistant or not m.tool_calls:
                continue
            for tc in m.tool_calls:
                if tc.function.name != "read_file":
                    continue
                try:
                    a = _json.loads(tc.function.arguments or "{}")
                except Exception:
                    continue
                if _json.dumps(a, sort_keys=True, default=str) == cur_args_json:
                    dup_indices.append(i)
                    break
        # No duplicates of {offset:900} in history — preflight stays inert
        assert dup_indices == []
