"""
Toolcomp tool test harness.

Run it like the model would: change ACTIVE_TEST at the bottom, then run.

The output you see IS the exact string the model receives — ToolResult.output
is JSON-dumped into a single string, and ToolError is formatted via
to_agent_message(). No transformation, no extra keys.

Usage:
    python -m ai.tools.tests.test_toolcomp_tools
"""
from __future__ import annotations

import asyncio
import json
from typing import Any
from uuid import uuid4

from matrx_utils import vcprint, clear_terminal

from matrx_ai.tools.models import ToolContext, ToolResult


# ---------------------------------------------------------------------------
# Minimal ToolContext for testing (no live HTTP request / AppContext needed)
# ---------------------------------------------------------------------------

def make_ctx(tool_name: str) -> ToolContext:
    return ToolContext(call_id=str(uuid4()), tool_name=tool_name)


# ---------------------------------------------------------------------------
# Serialize exactly as the executor does
# ---------------------------------------------------------------------------

def model_sees(result: ToolResult) -> str:
    """Return the exact string that lands in the model's tool-result message."""
    if result.success:
        content = result.output
        if isinstance(content, dict):
            content = json.dumps(content)
        elif not isinstance(content, str):
            content = str(content) if content is not None else ""
        return content
    else:
        return result.error.to_agent_message() if result.error else "Unknown error"


def print_result(tool_name: str, args: dict[str, Any], result: ToolResult) -> None:
    separator = "=" * 72

    raw = model_sees(result)
    char_count = f"{len(raw):,}"

    print(f"\n{separator}")
    print(f"  TOOL: {tool_name}")
    print(f"  ARGS: {json.dumps(args, indent=2)}")
    print(f"  SUCCESS: {result.success}")
    print(f"  CHARACTERS: {char_count}")
    print(separator)
    print("\n--- EXACT MODEL OUTPUT (start) ---\n")
    # Try to pretty-print if it's pure JSON; otherwise print as-is
    # (mixed-format outputs like toolcomp_get_code are intentionally not JSON)
    try:
        parsed = json.loads(raw)
        print(json.dumps(parsed, indent=2))
    except (json.JSONDecodeError, TypeError):
        print(raw)
    print("\n--- EXACT MODEL OUTPUT (end) ---\n")


# ---------------------------------------------------------------------------
# Importers (lazy, to avoid triggering full app startup on unused tools)
# ---------------------------------------------------------------------------

async def run_tool(tool_name: str, args: dict[str, Any]) -> ToolResult:
    from matrx_ai.tools.implementations.tool_component import (
        toolcomp_create_component,
        toolcomp_get_code,
        toolcomp_get_context,
        toolcomp_get_incident_detail,
        toolcomp_get_sample_detail,
        toolcomp_list_tools,
        toolcomp_patch_code,
        toolcomp_resolve_incident,
        toolcomp_update_code,
        toolcomp_update_settings,
    )

    dispatch = {
        "toolcomp_get_context": toolcomp_get_context,
        "toolcomp_get_code": toolcomp_get_code,
        "toolcomp_update_code": toolcomp_update_code,
        "toolcomp_update_settings": toolcomp_update_settings,
        "toolcomp_get_sample_detail": toolcomp_get_sample_detail,
        "toolcomp_get_incident_detail": toolcomp_get_incident_detail,
        "toolcomp_resolve_incident": toolcomp_resolve_incident,
        "toolcomp_list_tools": toolcomp_list_tools,
        "toolcomp_create_component": toolcomp_create_component,
        "toolcomp_patch_code": toolcomp_patch_code,
    }

    fn = dispatch[tool_name]
    ctx = make_ctx(tool_name)
    return await fn(args, ctx)


# ---------------------------------------------------------------------------
# Individual test scenarios
# The variables at the top of each function are what you'd change when
# acting as the model. Everything below is identical to what the model does.
# ---------------------------------------------------------------------------

async def test_list_tools():
    # ── model args ──────────────────────────────────────────────────────────
    # Flat paginated list (default mode)
    args: dict[str, Any] = {
        # ── Filters (all optional, all combinable) ──
        # "category": "research",
        # "source_kind": "matrx_ai",     # "matrx_ai" | "matrx_local"
        # "prefix": "web",              # name prefix: "web", "toolcomp", "travel", etc.
        # "tag": "scrape",
        # "has_component": True,        # True = only tools WITH a component
        # "has_component": False,       # False = tools MISSING a component
        # "is_active": True,
        # ── Pagination ──
        "limit": 10,
        "offset": 0,                    # bump to next_offset from previous result to page
    }
    # ────────────────────────────────────────────────────────────────────────
    result = await run_tool("toolcomp_list_tools", args)
    print_result("toolcomp_list_tools", args, result)
    return result


async def test_list_tools_grouped():
    # ── model args ──────────────────────────────────────────────────────────
    args: dict[str, Any] = {
        "group_by": "prefix",           # "prefix" | "category" | "source_kind"
        # Filters still apply before grouping:
        # "source_kind": "matrx_ai",
        # "has_component": False,
        # "is_active": True,
    }
    # ────────────────────────────────────────────────────────────────────────
    result = await run_tool("toolcomp_list_tools", args)
    print_result("toolcomp_list_tools [grouped]", args, result)
    return result


async def test_get_context():
    # ── model args ──────────────────────────────────────────────────────────
    tool_name = "research_web"       # change to any tool name
    # tool_id = "075194f7-3766-4ae7-a887-2234331b49c1"  # or use id directly
    args: dict[str, Any] = {
        "tool_name": tool_name,
        # "tool_id": tool_id,
    }
    # ────────────────────────────────────────────────────────────────────────
    result = await run_tool("toolcomp_get_context", args)
    print_result("toolcomp_get_context", args, result)
    return result


async def test_get_code():
    # ── model args ──────────────────────────────────────────────────────────
    # Get component_id from test_get_context first
    component_id = "69bfc2db-5497-408e-b9df-4887f30092da"
    sections = ["inline_code", "overlay_code"]   # add/remove as needed
    args: dict[str, Any] = {
        "component_id": component_id,
        "sections": sections,
    }
    # ────────────────────────────────────────────────────────────────────────
    result = await run_tool("toolcomp_get_code", args)
    print_result("toolcomp_get_code", args, result)
    return result


async def test_update_code():
    # ── model args ──────────────────────────────────────────────────────────
    component_id = "69bfc2db-5497-408e-b9df-4887f30092da"
    args: dict[str, Any] = {
        "component_id": component_id,
        "updates": {
            "inline_code": "export default function InlineResult({ data }) {\n  return <div>{JSON.stringify(data)}</div>;\n}",
            # leave overlay_code out to only update inline_code
        },
        "bump_version": True,
        "notes": "Test update from harness",
    }
    # ────────────────────────────────────────────────────────────────────────
    result = await run_tool("toolcomp_update_code", args)
    print_result("toolcomp_update_code", args, result)
    return result


async def test_patch_code():
    # ── model args ──────────────────────────────────────────────────────────
    component_id = "69bfc2db-5497-408e-b9df-4887f30092da"
    section = "inline_code"   # which code section to patch
    args: dict[str, Any] = {
        "component_id": component_id,
        "section": section,
        "patches": [
            {
                "old_string": "return <div>{JSON.stringify(data)}</div>;",
                "new_string": "return <pre>{JSON.stringify(data, null, 2)}</pre>;",
                "description": "Use pre tag for readable JSON output",
            },
            # add more patches here — they apply in order
        ],
        "bump_version": True,
        "notes": "Patch: prettier JSON display",
    }
    # ────────────────────────────────────────────────────────────────────────
    result = await run_tool("toolcomp_patch_code", args)
    print_result("toolcomp_patch_code", args, result)
    return result


async def test_update_settings():
    # ── model args ──────────────────────────────────────────────────────────
    component_id = "69bfc2db-5497-408e-b9df-4887f30092da"
    args: dict[str, Any] = {
        "component_id": component_id,
        "settings": {
            "display_name": "Research Results (Updated)",
            "keep_expanded_on_stream": True,
        },
    }
    # ────────────────────────────────────────────────────────────────────────
    result = await run_tool("toolcomp_update_settings", args)
    print_result("toolcomp_update_settings", args, result)
    return result


async def test_get_sample_detail():
    # ── model args ──────────────────────────────────────────────────────────
    # Get sample_id from test_get_context (look in the "samples" list → "id")
    sample_id = "3b0c409b-35fc-4159-914b-ba8d01807346"
    args: dict[str, Any] = {
        "sample_id": sample_id,
        "full_events": True,   # set True to see every raw streaming event
    }
    # ────────────────────────────────────────────────────────────────────────
    result = await run_tool("toolcomp_get_sample_detail", args)
    print_result("toolcomp_get_sample_detail", args, result)
    return result


async def test_get_incident_detail():
    # ── model args ──────────────────────────────────────────────────────────
    # Get incident_id from test_get_context (look in "open_incidents" → "id")
    incident_id = "fdfd51d6-dfe1-4134-9a40-54153da78741"
    args: dict[str, Any] = {
        "incident_id": incident_id,
    }
    # ────────────────────────────────────────────────────────────────────────
    result = await run_tool("toolcomp_get_incident_detail", args)
    print_result("toolcomp_get_incident_detail", args, result)
    return result


async def test_resolve_incident():
    # ── model args ──────────────────────────────────────────────────────────
    incident_id = "fdfd51d6-dfe1-4134-9a40-54153da78741"
    args: dict[str, Any] = {
        "incident_id": incident_id,
        "resolution_notes": "Fixed by patching inline_code — bad null check on data.results",
    }
    # ────────────────────────────────────────────────────────────────────────
    result = await run_tool("toolcomp_resolve_incident", args)
    print_result("toolcomp_resolve_incident", args, result)
    return result


async def test_create_component():
    # ── model args ──────────────────────────────────────────────────────────
    # Get tool_id from test_list_tools first
    tool_id = "69bfc2db-5497-408e-b9df-4887f30092da"
    args: dict[str, Any] = {
        "tool_id": tool_id,
        "display_name": "My New Component",
        "inline_code": (
            'export default function InlineResult({ data }) {\n'
            '  return (\n'
            '    <div className="p-2 text-sm">\n'
            '      <pre>{JSON.stringify(data, null, 2)}</pre>\n'
            '    </div>\n'
            '  );\n'
            '}'
        ),
        "results_label": "Results",
        "allowed_imports": ["react", "lucide-react"],
        "language": "tsx",
    }
    # ────────────────────────────────────────────────────────────────────────
    result = await run_tool("toolcomp_create_component", args)
    print_result("toolcomp_create_component", args, result)
    return result


# ---------------------------------------------------------------------------
# ACTIVE_TEST — change this to the function you want to run
# ---------------------------------------------------------------------------

TESTS = {
    "list_tools": test_list_tools,
    "get_context": test_get_context,
    "get_code": test_get_code,
    "update_code": test_update_code,
    "patch_code": test_patch_code,
    "update_settings": test_update_settings,
    "get_sample_detail": test_get_sample_detail,
    "get_incident_detail": test_get_incident_detail,
    "resolve_incident": test_resolve_incident,
    "create_component": test_create_component,
    "list_tools_grouped": test_list_tools_grouped,
}

# ── Change this flag to run a different test ───────────────────────────────
ACTIVE_TEST = "list_tools_grouped"
# ──────────────────────────────────────────────────────────────────────────


if __name__ == "__main__":
    clear_terminal()
    test_fn = TESTS.get(ACTIVE_TEST)
    if not test_fn:
        print(f"Unknown test '{ACTIVE_TEST}'. Available: {list(TESTS.keys())}")
    else:
        asyncio.run(test_fn())



f"""
My Notes:

list_tools:
 - Do we allow filters for source_kind?
 - We should have a way to list 'groups' of tools somehow, such as the ones we have here for toolcomp, and we have things like 'web' and other things like that.
 - Also, since it's limited to 30, do we have a pagination mechanism?
 
  get_context:
 - Perfect!
 
 get_code:
 - Perfect!

 update_code:
 - perfect!
 
 patch_code:
 - perfect
 
 update_settings:
 - 
 
 get_sample_detail:
 - 
 
 get_incident_detail:
 - 
 
 resolve_incident:
 - 
 
 create_component:
 - 
 
 patch_code:
 - 
 



"""