"""Tests for per-field enum-member drift (GAP 3 of common-docs/systems/agents/agent-tools/STATE.md).

The engine canonicalises a field's allowed-value set from both sides — a code
``Literal[...]`` / ``Enum`` and the DB ``enum`` — and diffs them. Severity splits
by how the drift actually bites:

* both sides constrain but members differ  -> ERROR (the model is shown one set and
  the executor enforces another; a guaranteed model_error),
* one-sided (only one side constrains)     -> WARNING (non-breaking; tighten the code
  model to a Literal so the executor enforces what the DB advertises).
"""
from __future__ import annotations

from typing import Literal

from matrx_ai.tools.declared import DeclaredTool, ToolArgs
from matrx_ai.tools.validation.engine import Severity, validate
from matrx_ai.tools.validation.schema import canon_db_params, canon_model_params


class _EnumArgs(ToolArgs):
    name: str
    mode: Literal["summary", "tree", "digest"] = "digest"


class _OpenArgs(ToolArgs):
    name: str
    mode: str = "digest"


def _decl(name: str, model: type[ToolArgs]) -> DeclaredTool:
    def _f(args, ctx):  # pragma: no cover - placeholder body
        return None

    return DeclaredTool(
        name=name, source_kind="native", args_model=model, func=_f,
        module="tests.fake", qualname=name, executor=None,
        validate=True, deprecated=False,
    )


def _row(name: str, params: dict) -> dict:
    return {
        "name": name, "source_kind": "native",
        "description": "",
        "is_active": True, "validation_exempt": False, "executors": [],
        "parameters": params,
    }


# ── canonicalisation: enum members are captured from both shapes ─────────────
def test_canon_model_captures_literal_enum():
    p = canon_model_params(_EnumArgs)
    assert p["mode"].enum == frozenset({"summary", "tree", "digest"})
    assert p["name"].enum is None  # a plain str is not enum-constrained


def test_canon_db_captures_flat_enum():
    p = canon_db_params({"mode": {"type": "string", "enum": ["summary", "tree", "digest"]}})
    assert p["mode"].enum == frozenset({"summary", "tree", "digest"})
    p2 = canon_db_params({"mode": {"type": "string"}})
    assert p2["mode"].enum is None


# ── engine: both sides constrain ─────────────────────────────────────────────
def test_enum_members_match_no_drift():
    row = _row("git_ingest", {
        "name": {"type": "string", "required": True},
        "mode": {"type": "string", "enum": ["summary", "tree", "digest"], "default": "digest"},
    })
    report = validate({"git_ingest": _decl("git_ingest", _EnumArgs)}, [row], owner_executors={"matrx-ai-core"})
    assert report.ok, [f.message for f in report.findings]
    assert not report.warnings


def test_enum_members_differ_is_error():
    row = _row("git_ingest", {
        "name": {"type": "string", "required": True},
        "mode": {"type": "string", "enum": ["summary", "tree", "FULL"], "default": "digest"},
    })
    report = validate({"git_ingest": _decl("git_ingest", _EnumArgs)}, [row], owner_executors={"matrx-ai-core"})
    assert not report.ok
    msgs = " ".join(f.message for f in report.errors)
    assert "enum members differ" in msgs and "mode" in msgs


# ── engine: one-sided constraint is a non-blocking WARNING ───────────────────
def test_one_sided_db_enum_is_warning():
    # DB constrains, code is open str -> WARNING, verdict stays green (no errors).
    row = _row("git_ingest", {
        "name": {"type": "string", "required": True},
        "mode": {"type": "string", "enum": ["summary", "tree", "digest"], "default": "digest"},
    })
    report = validate({"git_ingest": _decl("git_ingest", _OpenArgs)}, [row], owner_executors={"matrx-ai-core"})
    assert report.ok
    assert any(f.severity is Severity.WARNING and "only one side" in f.message
               for f in report.warnings)


def test_one_sided_code_enum_is_warning():
    # Code constrains (Literal), DB is open -> WARNING, verdict stays green.
    row = _row("git_ingest", {
        "name": {"type": "string", "required": True},
        "mode": {"type": "string", "default": "digest"},
    })
    report = validate({"git_ingest": _decl("git_ingest", _EnumArgs)}, [row], owner_executors={"matrx-ai-core"})
    assert report.ok
    assert any(f.severity is Severity.WARNING and "only one side" in f.message
               for f in report.warnings)
