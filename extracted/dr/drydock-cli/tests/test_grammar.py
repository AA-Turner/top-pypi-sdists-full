"""Unit tests for the GBNF grammar generation pipeline (Phase 1/2/2.5).

Covers:
  - pydantic_to_gbnf / json_schema_to_gbnf — basic compilation
  - policy.select_grammar + apply_grammar — forced-tool path
  - policy_union.build_union_gbnf — composite union grammar
  - Kill-switch env vars (DRYDOCK_GRAMMAR_DISABLE, DRYDOCK_UNION_GRAMMAR_DISABLE)
  - max_tokens bumping in both paths
"""
from __future__ import annotations

from typing import Any
from unittest.mock import MagicMock

from pydantic import BaseModel

from drydock.core.llm.grammar import json_schema_to_gbnf, pydantic_to_gbnf
from drydock.core.llm.grammar.policy import (
    GRAMMAR_MAX_TOKENS_FLOOR,
    apply_grammar,
    select_grammar,
)
from drydock.core.llm.grammar.policy_union import (
    _tighten_args_schema,
    build_union_gbnf,
    select_union_grammar,
)


# ---------------------------------------------------------------------------
# Sample Pydantic models for testing
# ---------------------------------------------------------------------------

class SimpleArgs(BaseModel):
    path: str
    content: str


class OptionalArgs(BaseModel):
    path: str
    overwrite: bool = True
    max_lines: int | None = None


# ---------------------------------------------------------------------------
# pydantic_to_gbnf
# ---------------------------------------------------------------------------

def test_pydantic_to_gbnf_returns_nonempty():
    gbnf = pydantic_to_gbnf(SimpleArgs)
    assert isinstance(gbnf, str)
    assert len(gbnf) > 50


def test_pydantic_to_gbnf_contains_root_rule():
    gbnf = pydantic_to_gbnf(SimpleArgs)
    # GBNF always starts with a root rule
    assert "root" in gbnf


def test_pydantic_to_gbnf_optional_model():
    gbnf = pydantic_to_gbnf(OptionalArgs)
    assert isinstance(gbnf, str)
    assert len(gbnf) > 50


def test_json_schema_to_gbnf_basic():
    schema = {
        "type": "object",
        "properties": {"x": {"type": "string"}},
        "required": ["x"],
    }
    gbnf = json_schema_to_gbnf(schema)
    assert isinstance(gbnf, str)
    assert len(gbnf) > 20


# ---------------------------------------------------------------------------
# policy.select_grammar — forced single-tool path
# ---------------------------------------------------------------------------

def _make_tool_manager(tool_name: str, args_model: type) -> Any:
    """Create a minimal fake tool_manager for select_grammar tests."""
    tool_cls = MagicMock()
    tool_cls._get_tool_args_results.return_value = (args_model, MagicMock())
    mgr = MagicMock()
    mgr.available_tools = {tool_name: tool_cls}
    return mgr


def _forced_tool_choice(name: str) -> dict:
    return {"type": "function", "function": {"name": name}}


def test_select_grammar_forced_tool_returns_gbnf(monkeypatch):
    monkeypatch.delenv("DRYDOCK_GRAMMAR_DISABLE", raising=False)
    mgr = _make_tool_manager("write_file", SimpleArgs)
    gbnf, forced = select_grammar(
        tool_choice=_forced_tool_choice("write_file"),
        tool_manager=mgr,
    )
    assert gbnf is not None
    assert len(gbnf) > 50
    assert forced == "write_file"


def test_select_grammar_kill_switch(monkeypatch):
    monkeypatch.setenv("DRYDOCK_GRAMMAR_DISABLE", "1")
    mgr = _make_tool_manager("write_file", SimpleArgs)
    gbnf, forced = select_grammar(
        tool_choice=_forced_tool_choice("write_file"),
        tool_manager=mgr,
    )
    assert gbnf is None
    assert forced is None


def test_select_grammar_auto_returns_none(monkeypatch):
    monkeypatch.delenv("DRYDOCK_GRAMMAR_DISABLE", raising=False)
    mgr = _make_tool_manager("write_file", SimpleArgs)
    gbnf, forced = select_grammar(
        tool_choice="auto",
        tool_manager=mgr,
    )
    assert gbnf is None
    assert forced is None


def test_select_grammar_unknown_tool_returns_none(monkeypatch):
    monkeypatch.delenv("DRYDOCK_GRAMMAR_DISABLE", raising=False)
    mgr = MagicMock()
    mgr.available_tools = {}  # tool not registered
    gbnf, forced = select_grammar(
        tool_choice=_forced_tool_choice("nonexistent_tool"),
        tool_manager=mgr,
    )
    assert gbnf is None
    assert forced is None


# ---------------------------------------------------------------------------
# policy.apply_grammar — kwargs mutation
# ---------------------------------------------------------------------------

def test_apply_grammar_sets_grammar_in_extra_sampling():
    kwargs: dict = {}
    apply_grammar(
        complete_kwargs=kwargs,
        grammar_gbnf="root ::= \"x\"",
        forced_tool_name="write_file",
        extra_sampling=None,
    )
    assert kwargs.get("extra_sampling", {}).get("grammar") == "root ::= \"x\""


def test_apply_grammar_strips_tools_and_tool_choice():
    kwargs: dict = {
        "tools": [{"function": {"name": "write_file"}}],
        "tool_choice": {"type": "function", "function": {"name": "write_file"}},
        "max_tokens": 512,
    }
    apply_grammar(
        complete_kwargs=kwargs,
        grammar_gbnf="root ::= \"x\"",
        forced_tool_name="write_file",
        extra_sampling=None,
    )
    assert "tools" not in kwargs
    assert "tool_choice" not in kwargs


def test_apply_grammar_bumps_max_tokens_when_low():
    kwargs: dict = {"max_tokens": 256}
    apply_grammar(
        complete_kwargs=kwargs,
        grammar_gbnf="root ::= \"x\"",
        forced_tool_name="write_file",
        extra_sampling=None,
    )
    assert kwargs["max_tokens"] >= GRAMMAR_MAX_TOKENS_FLOOR


def test_apply_grammar_preserves_high_max_tokens():
    kwargs: dict = {"max_tokens": 32000}
    apply_grammar(
        complete_kwargs=kwargs,
        grammar_gbnf="root ::= \"x\"",
        forced_tool_name="write_file",
        extra_sampling=None,
    )
    assert kwargs["max_tokens"] == 32000


def test_apply_grammar_merges_existing_extra_sampling():
    kwargs: dict = {}
    existing = {"temperature": 0.5}
    apply_grammar(
        complete_kwargs=kwargs,
        grammar_gbnf="root ::= \"x\"",
        forced_tool_name="write_file",
        extra_sampling=existing,
    )
    es = kwargs.get("extra_sampling", {})
    assert es.get("temperature") == 0.5
    assert "grammar" in es


# ---------------------------------------------------------------------------
# policy_union.build_union_gbnf
# ---------------------------------------------------------------------------

def test_build_union_gbnf_two_tools():
    specs = [
        ("write_file", SimpleArgs),
        ("read_file", OptionalArgs),
    ]
    gbnf = build_union_gbnf(specs)
    assert gbnf is not None
    assert "write_file" in gbnf or "root" in gbnf  # name literal or root rule
    assert len(gbnf) > 100


def test_build_union_gbnf_single_tool():
    specs = [("write_file", SimpleArgs)]
    gbnf = build_union_gbnf(specs)
    assert gbnf is not None
    assert len(gbnf) > 50


def test_build_union_gbnf_empty_returns_none():
    assert build_union_gbnf([]) is None


# ---------------------------------------------------------------------------
# select_union_grammar — auto-mode path
# ---------------------------------------------------------------------------

def _make_available_tools(specs: list[tuple[str, type]]) -> list[Any]:
    """Build fake available_tools list for select_union_grammar."""
    tools = []
    for name, args_model in specs:
        at = MagicMock()
        at.function.name = name
        tools.append(at)
    return tools


def _make_tool_manager_multi(specs: list[tuple[str, type]]) -> Any:
    mgr = MagicMock()
    registry = {}
    for name, args_model in specs:
        tc = MagicMock()
        tc._get_tool_args_results.return_value = (args_model, MagicMock())
        registry[name] = tc
    mgr.available_tools = registry
    return mgr


def test_select_union_grammar_auto_off_by_default(monkeypatch):
    """v2.9.98: union grammar is OFF by default — must be explicitly
    enabled via DRYDOCK_UNION_GRAMMAR_ENABLE=1. The 72-tool union let the
    model pick whichever branch had the simplest schema and iterate
    through them mechanically (task, exit_plan_mode, notebook_edit, …).
    Forced-tool grammar (policy.py) is unaffected.
    """
    monkeypatch.delenv("DRYDOCK_GRAMMAR_DISABLE", raising=False)
    monkeypatch.delenv("DRYDOCK_UNION_GRAMMAR_DISABLE", raising=False)
    monkeypatch.delenv("DRYDOCK_UNION_GRAMMAR_ENABLE", raising=False)
    specs = [("write_file", SimpleArgs), ("read_file", OptionalArgs)]
    at = _make_available_tools(specs)
    mgr = _make_tool_manager_multi(specs)
    gbnf = select_union_grammar(
        tool_choice="auto",
        available_tools=at,
        tool_manager=mgr,
    )
    assert gbnf is None  # off by default


def test_select_union_grammar_auto_when_enabled(monkeypatch):
    """When DRYDOCK_UNION_GRAMMAR_ENABLE=1, the union grammar engages."""
    monkeypatch.delenv("DRYDOCK_GRAMMAR_DISABLE", raising=False)
    monkeypatch.delenv("DRYDOCK_UNION_GRAMMAR_DISABLE", raising=False)
    monkeypatch.setenv("DRYDOCK_UNION_GRAMMAR_ENABLE", "1")
    specs = [("write_file", SimpleArgs), ("read_file", OptionalArgs)]
    at = _make_available_tools(specs)
    mgr = _make_tool_manager_multi(specs)
    gbnf = select_union_grammar(
        tool_choice="auto",
        available_tools=at,
        tool_manager=mgr,
    )
    assert gbnf is not None
    assert len(gbnf) > 100


def test_select_union_grammar_forced_tool_skips(monkeypatch):
    monkeypatch.delenv("DRYDOCK_GRAMMAR_DISABLE", raising=False)
    monkeypatch.delenv("DRYDOCK_UNION_GRAMMAR_DISABLE", raising=False)
    specs = [("write_file", SimpleArgs)]
    at = _make_available_tools(specs)
    mgr = _make_tool_manager_multi(specs)
    gbnf = select_union_grammar(
        tool_choice=_forced_tool_choice("write_file"),
        available_tools=at,
        tool_manager=mgr,
    )
    assert gbnf is None  # forced single tool → not auto-mode


def test_select_union_grammar_kill_switch(monkeypatch):
    monkeypatch.setenv("DRYDOCK_UNION_GRAMMAR_DISABLE", "1")
    specs = [("write_file", SimpleArgs)]
    at = _make_available_tools(specs)
    mgr = _make_tool_manager_multi(specs)
    gbnf = select_union_grammar(
        tool_choice="auto",
        available_tools=at,
        tool_manager=mgr,
    )
    assert gbnf is None


def test_select_union_grammar_global_kill_switch(monkeypatch):
    monkeypatch.setenv("DRYDOCK_GRAMMAR_DISABLE", "1")
    monkeypatch.delenv("DRYDOCK_UNION_GRAMMAR_DISABLE", raising=False)
    specs = [("write_file", SimpleArgs)]
    at = _make_available_tools(specs)
    mgr = _make_tool_manager_multi(specs)
    gbnf = select_union_grammar(
        tool_choice="auto",
        available_tools=at,
        tool_manager=mgr,
    )
    assert gbnf is None


def test_select_union_grammar_empty_tools_returns_none(monkeypatch):
    monkeypatch.delenv("DRYDOCK_GRAMMAR_DISABLE", raising=False)
    monkeypatch.delenv("DRYDOCK_UNION_GRAMMAR_DISABLE", raising=False)
    mgr = MagicMock()
    mgr.available_tools = {}
    gbnf = select_union_grammar(
        tool_choice="auto",
        available_tools=[],
        tool_manager=mgr,
    )
    assert gbnf is None


# ---------------------------------------------------------------------------
# Regression: vacuous-default fields must become grammar-required.
# v2.9.87 batch had 18 write_file calls with path=None and identical
# 428-char `out0 = out0\nout1 = out1\n...` garbage content because the
# pydantic schema (path: str = Field(default="")) marked path as
# non-required, the grammar accepted the empty default, and the model
# committed to whatever fit. The tightener strips those defaults.
# ---------------------------------------------------------------------------

def test_tighten_args_schema_forces_empty_string_defaults_required():
    schema = {
        "properties": {
            "path": {"type": "string", "default": ""},
            "content": {"type": "string", "default": ""},
            "overwrite": {"type": "boolean", "default": True},
        },
    }
    out = _tighten_args_schema(schema)
    assert set(out["required"]) == {"path", "content"}
    assert "default" not in out["properties"]["path"]
    assert "default" not in out["properties"]["content"]
    # legit boolean default left alone
    assert out["properties"]["overwrite"]["default"] is True


def test_tighten_args_schema_preserves_nullable_optionals():
    # ReadFileArgs.limit pattern: Optional[int] = None → type allows null,
    # default=null is a legit "no limit" — must NOT be forced required.
    schema = {
        "properties": {
            "path": {"type": "string"},
            "limit": {
                "anyOf": [{"type": "integer"}, {"type": "null"}],
                "default": None,
            },
        },
        "required": ["path"],
    }
    out = _tighten_args_schema(schema)
    assert out["required"] == ["path"]
    assert out["properties"]["limit"]["default"] is None


def test_tighten_args_schema_real_write_file_args():
    """End-to-end with the actual production WriteFileArgs."""
    from drydock.core.tools.builtins.write_file import WriteFileArgs
    raw = WriteFileArgs.model_json_schema()
    # baseline: pydantic leaves it open
    assert "required" not in raw or "path" not in raw.get("required", [])
    tight = _tighten_args_schema(raw)
    assert "path" in tight["required"]
    assert "content" in tight["required"]
    # overwrite stays optional
    assert "overwrite" not in tight["required"]


def test_union_grammar_requires_write_file_path_after_tightener():
    """The grammar string itself must include the required-fields markers
    for write_file's path. We assert by checking that the GBNF doesn't
    contain a permissive write_file branch that lets path be omitted."""
    from drydock.core.tools.builtins.write_file import WriteFileArgs
    gbnf = build_union_gbnf([("write_file", WriteFileArgs)])
    assert gbnf is not None
    # Tool name + path appear as GBNF string constants (\"-escaped).
    assert '\\"write_file\\"' in gbnf
    assert '\\"path\\"' in gbnf
    assert '\\"content\\"' in gbnf
    # The smoking gun for the bug would be an args body rule that allows
    # `{}` (no required keys). After the tightener, the args body opens
    # with `path-kv "," space content-kv` — path and content are
    # unconditional, overwrite is wrapped in `( ... )?`. Verify the args
    # rule doesn't degenerate to `"{" space "}"`.
    args_rule_line = next(
        (ln for ln in gbnf.splitlines() if "-arguments ::=" in ln),
        "",
    )
    assert args_rule_line, "expected an arguments rule in GBNF"
    assert "path-kv" in args_rule_line  # path is in the args body
    assert "content-kv" in args_rule_line  # content is in the args body
    # overwrite (optional) should appear wrapped in `( ... )?`
    assert "overwrite-kv )" in args_rule_line and "?" in args_rule_line
