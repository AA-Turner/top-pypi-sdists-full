"""
One-shot registration script for the toolcomp_* tool suite.

Run once:  python -m ai.tools.tests.register_toolcomp_tools
"""

from __future__ import annotations

import asyncio

TOOLS = [
    {
        "name": "toolcomp_get_context",
        "description": (
            "Fetch a complete, curated context bundle for a specific tool's UI component. "
            "Returns the tool definition (parameters, output_schema), a summary of all "
            "component code sections with lengths, condensed test samples (event timelines, "
            "argument shapes, output previews), and any open (unresolved) component incidents. "
            "Use this as the first call when working on any tool UI component. "
            "Workflow emit-to-frontend components (tool_id=NULL) have no backing tool_def row — "
            "pass tool_name + surface_name='matrx-user/workflow', or component_id from "
            "toolcomp_create_component."
        ),
        "parameters": {
            "component_id": {
                "type": "string",
                "description": (
                    "UUID of the tool_ui component row. Works for real-tool and workflow "
                    "components. Prefer after toolcomp_create_component."
                ),
            },
            "tool_name": {
                "type": "string",
                "description": (
                    "Name of the tool or workflow component ref (e.g. 'research_web'). "
                    "For workflow components, also pass surface_name='matrx-user/workflow'."
                ),
            },
            "tool_id": {
                "type": "string",
                "description": "UUID of the backing tool_def row (real-tool components only).",
            },
            "surface_name": {
                "type": "string",
                "description": (
                    "Render surface (ui_surface.name). Required to disambiguate workflow "
                    "components: use 'matrx-user/workflow'. Defaults to workflow surface when "
                    "tool_name is not a tool_def name."
                ),
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "tool": {
                    "type": "object",
                    "description": "Full tool definition including parameters and output_schema.",
                },
                "components": {
                    "type": "array",
                    "description": "List of UI component records (metadata only, no raw code).",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "display_name": {"type": "string"},
                            "has_inline_code": {"type": "boolean"},
                            "has_overlay_code": {"type": "boolean"},
                            "inline_code_length": {"type": "integer"},
                            "overlay_code_length": {"type": "integer"},
                            "is_active": {"type": "boolean"},
                            "version": {"type": ["string", "null"]},
                        },
                    },
                },
                "component_ids": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "List of component UUIDs for use with toolcomp_get_code.",
                },
                "samples": {
                    "type": "array",
                    "description": "Condensed test samples: arguments, event timeline, output preview.",
                    "items": {"type": "object"},
                },
                "open_incidents": {
                    "type": "array",
                    "description": "Unresolved component error incidents (summary only).",
                    "items": {"type": "object"},
                },
                "summary": {
                    "type": "object",
                    "properties": {
                        "tool_id": {"type": ["string", "null"]},
                        "tool_name": {"type": "string"},
                        "surface_name": {"type": ["string", "null"]},
                        "is_workflow_component": {"type": "boolean"},
                        "has_component": {"type": "boolean"},
                        "sample_count": {"type": "integer"},
                        "open_incident_count": {"type": "integer"},
                    },
                },
            },
        },
        "function_path": "matrx_ai.tools.implementations.tool_component.toolcomp_get_context",
        "category": "internal",
        "tags": ["toolcomp", "internal", "component-agent"],
        "icon": "Wrench",
        "annotations": [
            {"type": "readOnlyHint", "value": True},
        ],
    },
    {
        "name": "toolcomp_get_code",
        "description": (
            "Retrieve the full source code for a specific tool UI component. "
            "Specify which sections to return: inline_code, overlay_code, utility_code, "
            "header_extras_code, header_subtitle_code. Defaults to inline_code and overlay_code. "
            "Get the component_id from toolcomp_get_context first."
        ),
        "parameters": {
            "component_id": {
                "type": "string",
                "description": "UUID of the tool UI component.",
                "required": True,
            },
            "sections": {
                "type": "array",
                "items": {
                    "type": "string",
                    "enum": [
                        "inline_code",
                        "overlay_code",
                        "utility_code",
                        "header_extras_code",
                        "header_subtitle_code",
                    ],
                },
                "description": "Which code sections to return. Defaults to ['inline_code', 'overlay_code'].",
                "default": ["inline_code", "overlay_code"],
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "component_id": {"type": "string"},
                "tool_name": {"type": ["string", "null"]},
                "display_name": {"type": ["string", "null"]},
                "semver": {"type": ["string", "null"]},
                "version": {"type": ["integer", "null"]},
                "language": {"type": ["string", "null"]},
                "allowed_imports": {"type": ["array", "null"], "items": {"type": "string"}},
                "code": {
                    "type": "object",
                    "description": "Map of requested section name to source code string.",
                    "additionalProperties": {"type": ["string", "null"]},
                },
            },
        },
        "function_path": "matrx_ai.tools.implementations.tool_component.toolcomp_get_code",
        "category": "internal",
        "tags": ["toolcomp", "internal", "component-agent"],
        "icon": "Code",
        "annotations": [
            {"type": "readOnlyHint", "value": True},
        ],
    },
    {
        "name": "toolcomp_update_code",
        "description": (
            "Write updated source code to one or more sections of a tool UI component. "
            "Always provide the COMPLETE replacement code for each section — never partial snippets. "
            "Optionally bump the patch version automatically and add notes explaining the change."
        ),
        "parameters": {
            "component_id": {
                "type": "string",
                "description": "UUID of the tool UI component to update.",
                "required": True,
            },
            "updates": {
                "type": "object",
                "description": "Map of section name to complete replacement code. Keys must be valid code sections.",
                "required": True,
                "additionalProperties": {"type": "string"},
            },
            "bump_version": {
                "type": "boolean",
                "description": "If true, auto-increment the patch version (e.g. 1.0.2 → 1.0.3).",
                "default": False,
            },
            "notes": {
                "type": "string",
                "description": "Explain what was changed and why. Stored with the component.",
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "component_id": {"type": "string"},
                "updated_sections": {"type": "array", "items": {"type": "string"}},
                "semver": {"type": ["string", "null"]},
                "version": {"type": ["integer", "null"]},
                "updated_at": {"type": ["string", "null"]},
                "message": {"type": "string"},
            },
        },
        "function_path": "matrx_ai.tools.implementations.tool_component.toolcomp_update_code",
        "category": "internal",
        "tags": ["toolcomp", "internal", "component-agent"],
        "icon": "Code",
        "annotations": [
            {"type": "destructiveHint", "value": True},
            {"type": "idempotentHint", "value": True},
        ],
    },
    {
        "name": "toolcomp_update_settings",
        "description": (
            "Update non-code settings on a tool UI component: display_name, results_label, "
            "allowed_imports, keep_expanded_on_stream, language, is_active, or notes. "
            "Does NOT accept code fields — use toolcomp_update_code for those."
        ),
        "parameters": {
            "component_id": {
                "type": "string",
                "description": "UUID of the tool UI component.",
                "required": True,
            },
            "settings": {
                "type": "object",
                "description": "Map of setting name to new value.",
                "required": True,
                "properties": {
                    "display_name": {"type": "string"},
                    "results_label": {"type": "string"},
                    "allowed_imports": {"type": "array", "items": {"type": "string"}},
                    "keep_expanded_on_stream": {"type": "boolean"},
                    "language": {"type": "string", "enum": ["tsx", "jsx"]},
                    "is_active": {"type": "boolean"},
                    "notes": {"type": "string"},
                },
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "component_id": {"type": "string"},
                "updated_settings": {"type": "array", "items": {"type": "string"}},
                "updated_at": {"type": ["string", "null"]},
            },
        },
        "function_path": "matrx_ai.tools.implementations.tool_component.toolcomp_update_settings",
        "category": "internal",
        "tags": ["toolcomp", "internal", "component-agent"],
        "icon": "Settings",
        "annotations": [
            {"type": "idempotentHint", "value": True},
        ],
    },
    {
        "name": "toolcomp_get_sample_detail",
        "description": (
            "Get the complete data for a specific tool test sample. "
            "By default returns a condensed view: arguments, event timeline, output preview. "
            "Set full_events=true only when you need to inspect raw streaming chunks or a "
            "specific event payload in detail. Use to understand the exact data shape a component receives."
        ),
        "parameters": {
            "sample_id": {
                "type": "string",
                "description": "UUID of the tool test sample. Get it from toolcomp_get_context.",
                "required": True,
            },
            "full_events": {
                "type": "boolean",
                "description": "If true, return the complete raw_stream_events array. Warning: can be very large.",
                "default": False,
            },
            "event_offset": {
                "type": "integer",
                "description": "Zero-based raw event offset for full_events mode.",
                "default": 0,
                "minimum": 0,
            },
            "event_limit": {
                "type": "integer",
                "description": "Raw events per page for full_events mode (maximum 10).",
                "default": 10,
                "minimum": 1,
                "maximum": 10,
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "is_success": {"type": "boolean"},
                "use_for_component": {"type": "boolean"},
                "arguments_used": {"type": "object"},
                "event_timeline": {
                    "type": "array",
                    "items": {"type": "object"},
                    "description": "Condensed event sequence. Chunks are collapsed to a single marker.",
                },
                "output_schema_from_metadata": {"type": ["object", "null"]},
                "tool_result_output": {"type": "object"},
                "output_preview": {"type": ["string", "null"]},
            },
        },
        "function_path": "matrx_ai.tools.implementations.tool_component.toolcomp_get_sample_detail",
        "category": "internal",
        "tags": ["toolcomp", "internal", "component-agent"],
        "icon": "FlaskConical",
        "annotations": [
            {"type": "readOnlyHint", "value": True},
        ],
    },
    {
        "name": "toolcomp_get_incident_detail",
        "description": (
            "Get full details for a specific tool UI component incident (error report). "
            "Includes the complete error stack trace and the tool_update_snapshot — "
            "the exact data the component received when it crashed. "
            "Use to diagnose component errors and reproduce bugs."
        ),
        "parameters": {
            "incident_id": {
                "type": "string",
                "description": "UUID of the incident. Get it from the open_incidents in toolcomp_get_context.",
                "required": True,
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "incident_id": {"type": "string"},
                "tool_name": {"type": ["string", "null"]},
                "component_type": {"type": ["string", "null"]},
                "error_type": {"type": ["string", "null"]},
                "error_message": {"type": ["string", "null"]},
                "error_stack": {"type": ["string", "null"]},
                "tool_update_snapshot": {
                    "type": ["object", "null"],
                    "description": "Exact data that caused the crash.",
                },
                "resolved": {"type": "boolean"},
                "created_at": {"type": ["string", "null"]},
            },
        },
        "function_path": "matrx_ai.tools.implementations.tool_component.toolcomp_get_incident_detail",
        "category": "internal",
        "tags": ["toolcomp", "internal", "component-agent"],
        "icon": "AlertTriangle",
        "annotations": [
            {"type": "readOnlyHint", "value": True},
        ],
    },
    {
        "name": "toolcomp_resolve_incident",
        "description": (
            "Mark a tool UI component incident as resolved. "
            "Call this after deploying a fix so the incident no longer appears "
            "in the open incidents list. Optionally add resolution notes."
        ),
        "parameters": {
            "incident_id": {
                "type": "string",
                "description": "UUID of the incident to resolve.",
                "required": True,
            },
            "resolution_notes": {
                "type": "string",
                "description": "Optional explanation of how the issue was fixed.",
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "incident_id": {"type": "string"},
                "resolved": {"type": "boolean"},
                "resolved_at": {"type": "string"},
                "resolution_notes": {"type": ["string", "null"]},
            },
        },
        "function_path": "matrx_ai.tools.implementations.tool_component.toolcomp_resolve_incident",
        "category": "internal",
        "tags": ["toolcomp", "internal", "component-agent"],
        "icon": "CheckCircle",
        "annotations": [
            {"type": "idempotentHint", "value": True},
        ],
    },
    {
        "name": "toolcomp_list_tools",
        "description": (
            "List and discover available tools. Supports flat paginated listing and grouped views. "
            "group_by='prefix' groups tools by name prefix (e.g. 'web' for web_search/web_read, "
            "'toolcomp' for all toolcomp_* tools) — best for seeing what tool families exist. "
            "group_by='category' groups by category field. "
            "group_by='source_kind' groups by source_kind (native, mcp_discovered, "
            "admin_authored, agent_authored). "
            "Filters: category, source_kind, prefix (name prefix like 'web' or 'toolcomp'), "
            "tag, has_component (true=only with UI component, false=only without), is_active. "
            "Pagination: use limit (default 30, max 100) and offset; response includes has_more and next_offset."
        ),
        "parameters": {
            "group_by": {
                "type": "string",
                "enum": ["prefix", "category", "source_kind"],
                "description": "Return tools grouped by this dimension instead of a flat list.",
            },
            "category": {
                "type": "string",
                "description": "Filter by category (e.g. 'research', 'web', 'internal', 'memory').",
            },
            "source_kind": {
                "type": "string",
                "enum": ["native", "mcp_discovered", "admin_authored", "agent_authored"],
                "description": "Filter by source_kind.",
            },
            "prefix": {
                "type": "string",
                "description": "Filter to tools whose name starts with this prefix (e.g. 'web', 'toolcomp', 'travel').",
            },
            "tag": {
                "type": "string",
                "description": "Filter to tools that include this tag.",
            },
            "has_component": {
                "type": "boolean",
                "description": "true = only tools with a UI component; false = only tools missing one.",
            },
            "is_active": {
                "type": "boolean",
                "description": "Filter by active status. Omit to return all.",
            },
            "limit": {
                "type": "integer",
                "description": "Max results per page (default 30, max 100). Ignored in group_by mode.",
                "default": 30,
            },
            "offset": {
                "type": "integer",
                "description": "Number of results to skip for pagination (default 0).",
                "default": 0,
            },
        },
        "output_schema": {
            "type": "object",
            "description": "Flat mode: total_matching, offset, limit, returned, has_more, next_offset, tools[]. Grouped mode: group_by, total_tools, group_count, groups{key: {count, tools[]}}.",
            "properties": {
                "total_matching": {"type": "integer"},
                "has_more": {"type": "boolean"},
                "next_offset": {"type": ["integer", "null"]},
                "tools": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "id": {"type": "string"},
                            "name": {"type": "string"},
                            "description": {"type": "string"},
                            "category": {"type": ["string", "null"]},
                            "tags": {"type": ["array", "null"], "items": {"type": "string"}},
                            "is_active": {"type": "boolean"},
                            "source_kind": {"type": ["string", "null"]},
                        },
                    },
                },
                "groups": {
                    "type": "object",
                    "description": "Present only in group_by mode.",
                    "additionalProperties": {
                        "type": "object",
                        "properties": {
                            "count": {"type": "integer"},
                            "tools": {"type": "array"},
                        },
                    },
                },
            },
        },
        "function_path": "matrx_ai.tools.implementations.tool_component.toolcomp_list_tools",
        "category": "internal",
        "tags": ["toolcomp", "internal", "component-agent"],
        "icon": "List",
        "annotations": [
            {"type": "readOnlyHint", "value": True},
        ],
    },
    {
        "name": "toolcomp_create_component",
        "description": (
            "Create a new tool UI render component. For a real tool's component, pass "
            "tool_id (tool_name is derived) on the default chat surface. For a workflow "
            "'emit to frontend' component, pass an explicit tool_name (no tool_id — these "
            "have no backing tool_def row) and surface_name='matrx-user/workflow'; a "
            "workflow node references the component by that tool_name. display_name and "
            "inline_code are always required; overlay_code is recommended for rich output. "
            "Components are unique per (tool_name, surface_name). Fails safely if one "
            "already exists — use toolcomp_update_code instead."
        ),
        "parameters": {
            "tool_id": {
                "type": "string",
                "description": (
                    "UUID of the backing tool_def row. Omit for a workflow render "
                    "component (it has no backing tool; tool_id is stored NULL)."
                ),
            },
            "tool_name": {
                "type": "string",
                "description": (
                    "Component name. Required when tool_id is omitted (e.g. a workflow "
                    "render component referenced by name). When tool_id is given, the name "
                    "is derived from the tool and this must be omitted or match."
                ),
            },
            "display_name": {
                "type": "string",
                "description": "Human-readable name for the component (e.g. 'Research Results').",
                "required": True,
            },
            "inline_code": {
                "type": "string",
                "description": "Complete TSX source code for the inline (collapsed) view.",
                "required": True,
            },
            "overlay_code": {
                "type": "string",
                "description": "Complete TSX source code for the overlay (expanded) view.",
            },
            "surface_name": {
                "type": "string",
                "default": "matrx-default/default",
                "description": (
                    "Render surface (ui_surface.name) the component is attached to. "
                    "Defaults to the chat/default surface. Use 'matrx-user/workflow' for a "
                    "workflow emit-to-frontend component."
                ),
            },
            "results_label": {
                "type": "string",
                "description": "Short label shown above the results (e.g. 'Research Report').",
            },
            "allowed_imports": {
                "type": "array",
                "items": {"type": "string"},
                "description": "NPM packages the component is allowed to import.",
                "default": ["react", "lucide-react"],
            },
            "language": {
                "type": "string",
                "enum": ["tsx", "jsx"],
                "default": "tsx",
            },
            "notes": {
                "type": "string",
                "description": "Implementation notes or context about this component.",
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "component_id": {"type": "string"},
                "tool_id": {"type": ["string", "null"]},
                "tool_name": {"type": "string"},
                "surface_name": {"type": "string"},
                "display_name": {"type": "string"},
                "created_at": {"type": "string"},
                "message": {"type": "string"},
            },
        },
        "function_path": "matrx_ai.tools.implementations.tool_component.toolcomp_create_component",
        "category": "internal",
        "tags": ["toolcomp", "internal", "component-agent"],
        "icon": "PlusCircle",
        "annotations": [
            {"type": "destructiveHint", "value": False},
        ],
    },
    {
        "name": "toolcomp_patch_code",
        "description": (
            "Apply one or more targeted string replacements to a tool UI component's code "
            "without rewriting the entire section. Each patch specifies an old_string to find "
            "and a new_string to replace it with. Patches apply in order, each on the result "
            "of the previous. "
            "Matching uses three rounds of decreasing strictness: "
            "(1) exact character match, "
            "(2) whitespace-normalized (any whitespace sequence matches any other), "
            "(3) quote+whitespace normalized (smart quotes and backticks treated as equivalent). "
            "If any patch fails all three rounds, the entire operation is aborted and nothing is saved."
        ),
        "parameters": {
            "component_id": {
                "type": "string",
                "description": "UUID of the tool UI component to patch.",
                "required": True,
            },
            "section": {
                "type": "string",
                "enum": [
                    "inline_code",
                    "overlay_code",
                    "utility_code",
                    "header_extras_code",
                    "header_subtitle_code",
                ],
                "description": "Which code section to patch.",
                "default": "inline_code",
            },
            "patches": {
                "type": "array",
                "description": "Ordered list of string replacement operations.",
                "required": True,
                "items": {
                    "type": "object",
                    "properties": {
                        "old_string": {
                            "type": "string",
                            "description": "The exact substring to find and replace. Must be unique enough to identify the target location unambiguously.",
                        },
                        "new_string": {
                            "type": "string",
                            "description": "The string to replace old_string with.",
                        },
                        "description": {
                            "type": "string",
                            "description": "Human-readable label for this patch, shown in the result.",
                        },
                    },
                },
            },
            "bump_version": {
                "type": "boolean",
                "description": "If true, auto-increment the patch version after a successful patch.",
                "default": False,
            },
            "notes": {
                "type": "string",
                "description": "Explain what was changed and why.",
            },
        },
        "output_schema": {
            "type": "object",
            "properties": {
                "component_id": {"type": "string"},
                "section": {"type": "string"},
                "patches_applied": {"type": "integer"},
                "patch_results": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "index": {"type": "integer"},
                            "description": {"type": "string"},
                            "status": {"type": "string", "enum": ["applied"]},
                            "match_round": {
                                "type": "string",
                                "enum": ["exact", "whitespace_normalized", "quote_normalized"],
                                "description": "Which matching round found the string.",
                            },
                        },
                    },
                },
                "semver": {"type": ["string", "null"]},
                "version": {"type": ["integer", "null"]},
                "updated_at": {"type": ["string", "null"]},
                "message": {"type": "string"},
            },
        },
        "function_path": "matrx_ai.tools.implementations.tool_component.toolcomp_patch_code",
        "category": "internal",
        "tags": ["toolcomp", "internal", "component-agent"],
        "icon": "Scissors",
        "annotations": [
            {"type": "destructiveHint", "value": True},
            {"type": "idempotentHint", "value": False},
        ],
    },
]


async def register_all() -> None:
    from matrx_ai._ext import get_ext

    get_async_supabase_client = get_ext("get_async_supabase_client")

    client = get_async_supabase_client()

    for tool in TOOLS:
        existing = (
            await client.schema("tool")
            .table("definition")
            .select("id, name")
            .eq("name", tool["name"])
            .execute()
        )
        if existing.data:
            print(f"  [SKIP]   {tool['name']} — already registered (id={existing.data[0]['id']})")
            continue

        payload = {
            "name": tool["name"],
            "description": tool["description"],
            "parameters": tool["parameters"],
            "output_schema": tool["output_schema"],
            "source_kind": "native",
            "category": tool["category"],
            "tags": tool["tags"],
            "icon": tool["icon"],
            "is_active": True,
            "annotations": tool.get("annotations", []),
        }

        res = await client.schema("tool").table("definition").insert(payload).execute()
        if res.data:
            print(f"  [OK]     {tool['name']} — registered (id={res.data[0]['id']})")
        else:
            print(f"  [ERROR]  {tool['name']} — insert returned no data")


if __name__ == "__main__":
    asyncio.run(register_all())
