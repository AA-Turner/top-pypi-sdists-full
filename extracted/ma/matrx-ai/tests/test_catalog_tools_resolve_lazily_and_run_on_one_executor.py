"""Catalog Tools (source_kind='catalog'): typed CATALOG, never preloaded, one executor.

CONTRACT §4 (common-docs/projects/third-party-services/CONTRACT.md):
  - a catalog row types as ``ToolType.CATALOG`` with ``function_path = catalog:<id>``;
  - no ``ui:*`` keyword reaches a provider tool schema;
  - the lazy resolver pins every definition a request uses on that request, and a
    lazily resolved Tool answers ``registry.get`` but never ``list_tools``;
  - dispatch goes to the ONE host-injected catalog executor, after the declared
    schema check;
  - the drift engine never owns a catalog row.
"""

from __future__ import annotations

import json
import uuid
from typing import Any

import pytest
from matrx_connect.context.app_context import AppContext, set_app_context

from matrx_ai.tools import catalog_seam
from matrx_ai.tools.agent_projection import PROJECTED_AGENT_TOOLS_KEY
from matrx_ai.tools.models import ToolContext, ToolDefinition, ToolResult, ToolType
from matrx_ai.tools.registry import ToolRegistry
from matrx_ai.tools.validation.engine import DbTool, is_owned


def _catalog_row(name: str = "seo_domain_authority") -> dict[str, Any]:
    return {
        "id": str(uuid.uuid4()),
        "name": name,
        "description": "Domain Authority for one domain.",
        "source_kind": "catalog",
        "parameters": {
            "type": "object",
            "properties": {
                "domain": {
                    "type": "string",
                    "title": "Domain",
                    "ui:primary": True,
                    "ui:detect": "domain",
                    "ui:example": "example.com",
                },
                "include_subdomains": {"type": "boolean", "default": True, "ui:advanced": True},
            },
            "required": ["domain"],
        },
        "annotations": {"screen_callable": True},
        "side_effect_class": "paid_read",
        "is_active": True,
    }


@pytest.fixture(autouse=True)
def _clean_seams():
    catalog_seam.configure_catalog_executor(None)
    catalog_seam.configure_lazy_tool_resolver(None)
    yield
    catalog_seam.configure_catalog_executor(None)
    catalog_seam.configure_lazy_tool_resolver(None)


def test_a_catalog_row_types_catalog_with_a_synthesised_path():
    row = _catalog_row()
    tool_def = ToolRegistry._row_to_definition(row)
    assert tool_def.tool_type == ToolType.CATALOG
    assert tool_def.function_path == f"catalog:{row['id']}"
    assert tool_def.required_params == ["domain"]


@pytest.mark.parametrize("provider", ["anthropic", "openai", "google"])
def test_no_ui_keyword_reaches_a_provider_schema(provider: str):
    tool_def = ToolRegistry._row_to_definition(_catalog_row())
    wire = json.dumps(tool_def.get_provider_format(provider))
    assert "ui:" not in wire
    assert "domain" in wire


def test_strip_ui_keywords_is_recursive():
    schema = {"a": {"ui:x": 1, "b": [{"ui:y": 2, "c": 3}]}, "ui:z": 4}
    assert catalog_seam.strip_ui_keywords(schema) == {"a": {"b": [{"c": 3}]}}


@pytest.mark.asyncio
async def test_lazy_resolve_pins_to_the_request_and_never_lists():
    row = _catalog_row("seo_domain_authority_lazy")
    calls: list[list[str]] = []

    async def resolver(names: list[str]) -> list[ToolDefinition]:
        calls.append(list(names))
        return [ToolRegistry._row_to_definition(row)] if row["name"] in names else []

    async def window() -> float:
        return 60.0

    catalog_seam.configure_lazy_tool_resolver(resolver, cache_seconds=window)
    ctx = AppContext(emitter=None, user_id="u-1", request_id="r-1")
    set_app_context(ctx)

    resolved = await catalog_seam.resolve_lazy_tools([row["name"], "no_such_tool_anywhere"], ctx=ctx)
    assert [d.name for d in resolved] == [row["name"]]
    assert row["name"] in ctx.metadata[PROJECTED_AGENT_TOOLS_KEY]

    registry = ToolRegistry.get_instance()
    assert registry.get(row["name"]) is not None
    assert registry.get(row["id"]) is not None
    assert row["name"] not in {t.name for t in registry.list_tools(active_only=False)}
    assert row["name"] not in registry.list_tool_names()

    # Second request inside the TTL: served from the process cache, still pinned.
    ctx2 = AppContext(emitter=None, user_id="u-1", request_id="r-2")
    await catalog_seam.resolve_lazy_tools([row["name"]], ctx=ctx2)
    assert len(calls) == 1
    assert row["name"] in ctx2.metadata[PROJECTED_AGENT_TOOLS_KEY]

    # Eviction never removes a definition a live request holds.
    catalog_seam.clear_lazy_cache()
    assert registry.get(row["name"]) is None
    assert row["name"] in ctx2.metadata[PROJECTED_AGENT_TOOLS_KEY]


@pytest.mark.asyncio
async def test_dispatch_runs_the_one_catalog_executor_after_the_schema_check():
    from matrx_ai.tools.executor import ToolExecutor
    from matrx_ai.tools.guardrails import GuardrailEngine
    from matrx_ai.tools.lifecycle import ToolLifecycleManager
    from matrx_ai.tools.logger import ToolExecutionLogger

    seen: list[tuple[str, dict[str, Any]]] = []

    async def run(tool_def: ToolDefinition, args: dict[str, Any], ctx: ToolContext) -> ToolResult:
        seen.append((tool_def.name, args))
        return ToolResult(success=True, output={"authority": 42}, tool_name=ctx.tool_name, call_id=ctx.call_id)

    tool_def = ToolRegistry._row_to_definition(_catalog_row())
    executor = ToolExecutor(
        registry=ToolRegistry(),
        guardrails=GuardrailEngine(),
        execution_logger=ToolExecutionLogger(),
        lifecycle=ToolLifecycleManager.get_instance(),
    )
    ctx = ToolContext(call_id="c-1", tool_name=tool_def.name, iteration=1)

    unconfigured = await executor._dispatch(tool_def, {"domain": "moz.com"}, ctx, stream=None)
    assert unconfigured.success is False and unconfigured.error.error_type == "configuration"

    catalog_seam.configure_catalog_executor(run)
    bad = await executor._dispatch(tool_def, {"include_subdomains": True}, ctx, stream=None)
    assert bad.success is False and bad.error.error_type == "validation"
    assert seen == []

    ok = await executor._dispatch(tool_def, {"domain": "moz.com"}, ctx, stream=None)
    assert ok.success is True and ok.output == {"authority": 42}
    assert seen == [(tool_def.name, {"domain": "moz.com"})]


def test_the_drift_engine_never_owns_a_catalog_row():
    row = DbTool(
        name="seo_domain_authority",
        source_kind="catalog",
        parameters={},
        description="",
        is_active=True,
        validation_exempt=False,
        executors=(),
    )
    assert is_owned(row, {"matrx-ai-core", "aidream"}) is False
