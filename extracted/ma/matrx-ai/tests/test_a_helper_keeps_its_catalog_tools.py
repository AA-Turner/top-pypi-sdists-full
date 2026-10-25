"""A stored catalog tool id survives the direct-execution edge (PB-08 defect 57).

Ledgerline Ideas Desk declares ``current_time_in_zone`` — a catalog Tool
(``source_kind='catalog'``), which is never preloaded into the registry. Run as
a helper through ``agent`` (``Agent.execute``, the direct-execution edge), its
stored id went straight to ``drop_retired_tool_ids``, which calls every id the
registry cannot resolve "retired": the tool was dropped ("Stored tool id(s) name
no active tool", live 2026-10-19 02:36:22Z), the request carried no tools, and
Haiku wrote its time call as plain text (conversation 95c1083f…).

The edge must ask the lazy resolver first, map the id by the resolved
definition (the process cache may hold nothing), pin it on the request, and only
then drop what is truly retired.
"""

from __future__ import annotations

import ast
from matrx_utils.source_guard import stable_source
import uuid

import pytest
from matrx_connect.context.app_context import AppContext

from matrx_ai.agents import definition as definition_module
from matrx_ai.tools import catalog_seam
from matrx_ai.tools.agent_projection import PROJECTED_AGENT_TOOLS_KEY
from matrx_ai.tools.registry import ToolRegistry

CATALOG_ID = str(uuid.uuid4())
LIVE_ID = str(uuid.uuid4())
RETIRED_ID = str(uuid.uuid4())


def _catalog_def():
    return ToolRegistry._row_to_definition(
        {
            "id": CATALOG_ID,
            "name": "current_time_in_zone",
            "description": "Current time in one IANA zone.",
            "source_kind": "catalog",
            "parameters": {
                "type": "object",
                "properties": {"zone": {"type": "string"}},
                "required": ["zone"],
            },
            "is_active": True,
        }
    )


@pytest.fixture
def registry(monkeypatch: pytest.MonkeyPatch) -> ToolRegistry:
    fresh = ToolRegistry()
    fresh.ensure_registered("web", description="unified web tool", tool_id=LIVE_ID)
    fresh._loaded = True
    monkeypatch.setattr(ToolRegistry, "get_instance", classmethod(lambda cls: fresh))

    async def resolver(keys: list[str]):
        return [_catalog_def()] if CATALOG_ID in keys or "current_time_in_zone" in keys else []

    # No cache window: the live process may hold nothing in the lazy cache.
    catalog_seam.configure_lazy_tool_resolver(resolver)
    yield fresh
    catalog_seam.configure_lazy_tool_resolver(None)


async def test_a_stored_catalog_id_resolves_to_its_name_and_is_pinned(registry) -> None:
    from matrx_ai.tools.merge import resolve_stored_tools

    ctx = AppContext(emitter=None, user_id="u-1", request_id="r-1")
    kept, retired = await resolve_stored_tools([CATALOG_ID, LIVE_ID, RETIRED_ID], ctx=ctx)
    assert kept == ["current_time_in_zone", "web"], kept
    assert retired == [RETIRED_ID]
    assert "current_time_in_zone" in (ctx.metadata or {}).get(PROJECTED_AGENT_TOOLS_KEY, {})


def test_the_direct_execution_edge_resolves_catalog_tools_before_dropping() -> None:
    """``Agent.execute`` must use the one resolver, never the bare drop."""
    source = stable_source(definition_module)
    tree = ast.parse(source)
    bare_drops: list[int] = []
    resolves = False
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func
            name = fn.id if isinstance(fn, ast.Name) else getattr(fn, "attr", None)
            if name == "drop_retired_tool_ids":
                bare_drops.append(node.lineno)
            if name == "resolve_stored_tools":
                resolves = True
    assert not bare_drops, (
        f"definition.py calls drop_retired_tool_ids directly at lines {bare_drops}: a "
        "catalog tool the helper declares is dropped as 'retired' before it is resolved"
    )
    assert resolves, "definition.py never calls resolve_stored_tools"
