"""A DB rename must never orphan a live tool.

Live incident 2026-10-06: the `tool.definition` row `picklist` was renamed `pick_list` before the
deployed server's code knew the new name, so the server registered `picklist`, the row said
`pick_list`, and every agent lost the tool until the next deploy.

The rule (TOOL_RENAMES.md): code that accepts BOTH names ships first, then the DB rename, then the
old name is removed in a later change. This file holds the code half of that rule: a tool declared
with `aliases=` resolves, and passes the drift gate, whichever of its names the DB row carries.
"""

from __future__ import annotations

import pytest

from matrx_ai.tools import declared
from matrx_ai.tools.declared import NoArgs, ToolDeclarationError, tool
from matrx_ai.tools.validation.engine import FindingKind, validate


def _row(name: str) -> dict:
    return {
        "name": name,
        "source_kind": "native",
        "parameters": {},
        "description": "fixture",
        "is_active": True,
        "validation_exempt": False,
        "executors": ["matrx-ai-core"],
    }


@pytest.fixture
def renamed_tool():
    saved = (dict(declared._REGISTRY), dict(declared._ALIAS_INDEX))

    @tool(name="rename_new", source_kind="native", args=NoArgs, executor="matrx-ai-core",
          aliases=("rename_old",))
    async def rename_new(args, ctx):  # noqa: ARG001
        return None

    yield rename_new
    declared._REGISTRY.clear()
    declared._REGISTRY.update(saved[0])
    declared._ALIAS_INDEX.clear()
    declared._ALIAS_INDEX.update(saved[1])


def test_the_runtime_lookup_answers_to_either_name(renamed_tool):
    assert declared.get_effective_declared("rename_new").name == "rename_new"
    assert declared.get_effective_declared("rename_old").name == "rename_new"
    assert declared.get_declared_tool("rename_old").name == "rename_new"
    assert declared.code_name_for("rename_old") == "rename_new"
    assert declared.get_effective_declared("rename_unrelated") is None


@pytest.mark.parametrize("db_name", ["rename_new", "rename_old"])
def test_the_drift_gate_passes_whichever_name_the_db_row_carries(renamed_tool, db_name):
    report = validate(declared.declared_tools(), [_row(db_name)], owner_executors={"matrx-ai-core"})
    bad = [f for f in report.findings if f.tool_name in {"rename_new", "rename_old"}]
    assert bad == [], bad


def test_a_db_row_under_neither_name_is_still_caught(renamed_tool):
    report = validate(declared.declared_tools(), [_row("rename_other")], owner_executors={"matrx-ai-core"})
    kinds = {(f.kind, f.tool_name) for f in report.findings}
    assert (FindingKind.MISSING_IN_DB, "rename_new") in kinds
    assert (FindingKind.MISSING_IN_CODE, "rename_other") in kinds


def test_an_alias_that_is_already_a_tool_name_is_refused(renamed_tool):
    with pytest.raises(ToolDeclarationError):
        @tool(name="rename_third", source_kind="native", args=NoArgs, aliases=("rename_new",))
        async def rename_third(args, ctx):  # noqa: ARG001
            return None


def test_pick_list_answers_to_its_old_name():
    import matrx_ai.tools._generated_declarations  # noqa: F401 - registers every tool

    assert declared.get_effective_declared("picklist").name == "pick_list"
    assert declared.get_effective_declared("pick_list").name == "pick_list"
