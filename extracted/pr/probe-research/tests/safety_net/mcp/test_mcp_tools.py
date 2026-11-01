"""The MCP server's surface beyond its tools: name, instructions, prompts, resources, retired names.

Every listed tool's name, description and input schema is already pinned byte for byte by
tests/test_mcp_threading.py::test_tool_schemas_match_the_pre_offload_baseline (fixture
tests/fixtures/mcp_tool_schemas.json), and the 2,048-char budget by
tests/test_mcp_description_budget.py: the net runs both rather than copy them.
"""

from __future__ import annotations

import inspect

import anyio
import pytest
from mcp.server.fastmcp.exceptions import ToolError

from probe.mcp.server import create_server

#: Tool names agents were taught before a rename: each must keep answering with its successor,
#: never `Unknown tool` (a session's tool list is a snapshot from before the rename). Kept forever.
RETIRED_TOOLS = (
    "browse_research",
    "get_entity",
    "read_metrics",
    "get_metrics_grouped",
    "get_run_coordinates",
    "export_metric_points",
    "search_knowledge",
)


@pytest.fixture(scope="module")
def server():
    return create_server(object())  # a fixed service: listing and refusals never call it


def _dump(items) -> list[dict]:
    return sorted((item.model_dump(mode="json", exclude_none=True) for item in items), key=lambda d: d.get("name", ""))


def test_mcp_server_surface_is_unchanged(server, baseline):
    surface = {
        "name": server.name,
        "instructions": inspect.cleandoc(server.instructions or ""),
        "tools": sorted(tool.name for tool in anyio.run(server.list_tools)),
        "prompts": _dump(anyio.run(server.list_prompts)),
        "resources": _dump(anyio.run(server.list_resources)),
        "resource_templates": _dump(anyio.run(server.list_resource_templates)),
    }
    baseline("mcp_server", surface)


def _refusal(server, name: str) -> str:
    async def call() -> str:
        try:
            await server.call_tool(name, {})
        except ToolError as exc:
            return str(exc)
        return "(no refusal: the call ran)"

    return anyio.run(call)


def test_retired_tool_names_still_point_to_their_successors(server, baseline):
    answers = {name: _refusal(server, name) for name in RETIRED_TOOLS}
    unknown = sorted(name for name, text in answers.items() if text.startswith("Unknown tool"))
    assert not unknown, f"retired names now answer `Unknown tool` (their successor hint is gone): {unknown}"
    baseline("mcp_retired_tools", answers)
