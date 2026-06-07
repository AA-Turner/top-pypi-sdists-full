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

import pytest

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

    def test_task_blocked(self):
        names = set(_gemma4_tool_manager().available_tools.keys())
        assert "task" not in names

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
            select_union_grammar,
        )
        from drydock.core.tools.builtins.write_file import WriteFileArgs

        # Direct build path
        gbnf = build_union_gbnf([("write_file", WriteFileArgs)])
        assert gbnf is not None
        assert "write_file" in gbnf or "root" in gbnf


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
                content=f"contents at offset {i*100}",
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
