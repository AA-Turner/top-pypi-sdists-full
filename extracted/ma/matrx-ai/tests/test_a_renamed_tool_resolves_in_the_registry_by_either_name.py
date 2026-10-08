"""Live 2026-10-07: `tool.definition` row `dataset` was renamed `table`; the registry keys by the DB
row name and ignored the code's `aliases=("dataset",)`, so a request naming the other spelling got
"Some tools configured for this request are not registered" on /chat. The registry must answer to
both names, whichever one the DB row carries."""

from __future__ import annotations

import pytest

from matrx_ai.tools import declared
from matrx_ai.tools.declared import NoArgs, tool
from matrx_ai.tools.registry import ToolRegistry


@pytest.fixture
def renamed():
    saved = (dict(declared._REGISTRY), dict(declared._ALIAS_INDEX))

    @tool(name="rn_new", source_kind="native", args=NoArgs, executor="matrx-ai-core", aliases=("rn_old",))
    async def rn_new(args, ctx):  # noqa: ARG001
        return None

    yield
    declared._REGISTRY.clear()
    declared._REGISTRY.update(saved[0])
    declared._ALIAS_INDEX.clear()
    declared._ALIAS_INDEX.update(saved[1])


@pytest.mark.parametrize("db_name,asked", [("rn_new", "rn_old"), ("rn_old", "rn_new"), ("rn_new", "rn_new")])
def test_either_spelling_resolves_to_the_registered_row(renamed, db_name, asked):
    reg = ToolRegistry()
    reg._tools[db_name] = object()  # type: ignore[assignment]
    assert reg._resolve_tool_name(asked) == db_name


def test_an_unrelated_name_still_misses(renamed):
    reg = ToolRegistry()
    reg._tools["rn_new"] = object()  # type: ignore[assignment]
    assert reg._resolve_tool_name("rn_other") is None
