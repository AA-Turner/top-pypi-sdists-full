from __future__ import annotations

import json
import re
import traceback
from datetime import UTC
from typing import Any

from matrx_ai.db._registry import get_model as get_db_model
from matrx_ai.tools.kinds.tool_components import (
    ToolComponentCode,
    ToolComponentContext,
    ToolComponentCreateResult,
    ToolComponentIncidentDetail,
    ToolComponentIncidentResolution,
    ToolComponentListing,
    ToolComponentPatchResult,
    ToolComponentSample,
    ToolComponentUpdateResult,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

# ── Render surfaces (ui_surface.name) ──────────────────────────────────────
# tool_ui.surface_name is NOT NULL (FK → ui_surface.name) with no DB default,
# so every insert MUST set it explicitly. These are the two surfaces this
# authoring tool targets. CAPS constants, never env vars — changing a surface
# is a code push, not a silent per-environment flip.
#
# DEFAULT_RENDER_SURFACE — the chat/default surface a component lands on when
#   the caller doesn't say otherwise (back-compat: real-tool components).
# WORKFLOW_RENDER_SURFACE — the workflow "emit to frontend" render surface. A
#   workflow node references a component purely by its tool_name string on this
#   surface (NodeEmittedEvent.component_ref + .surface in matrx-graph). Such a
#   component has NO backing tool_def row, so tool_id is NULL.
DEFAULT_RENDER_SURFACE = "matrx-default/default"
WORKFLOW_RENDER_SURFACE = "matrx-user/workflow"


async def _get_tools_manager():
    from matrx_ai.tools.tool_def_db import tool_def_manager_instance

    return tool_def_manager_instance


def _row_dict(instance: Any, fields: tuple[str, ...] | None = None) -> dict[str, Any]:
    """Model instance -> plain dict, PostgREST-compatible shape (ISO-8601
    datetimes, string UUIDs) so downstream code (which expects the old
    ``response.data`` row shape) is unaffected by the ORM conversion."""
    from datetime import datetime
    from uuid import UUID as _UUID

    names = fields if fields is not None else tuple(instance._fields.keys())
    out: dict[str, Any] = {}
    for name in names:
        value = getattr(instance, name, None)
        if isinstance(value, datetime):
            out[name] = value.isoformat()
        elif isinstance(value, _UUID):
            out[name] = str(value)
        else:
            out[name] = value
    return out


# ── Versioning: two distinct columns, one of them DB-owned ─────────────────
# tool_ui carries TWO version columns and they are NOT interchangeable:
#
#   • version (INTEGER, default 1) — the authoritative revision counter,
#     FULLY managed by DB triggers. `trg_tool_ui_set_initial_version` forces it
#     to 1 on insert; `trg_tool_ui_snapshot_version` snapshots the prior row
#     into tool_ui_version and sets version := next snapshot number on EVERY
#     meaningful update. The application MUST NEVER write it — doing so is
#     redundant when a real field changed (the trigger overwrites it) and
#     CORRUPTS the counter in the no-other-change edge case (the trigger early-
#     returns and persists whatever the app passed).
#
#   • semver (TEXT, default '1.0.0') — the human-facing version label. It is the
#     value the frontend renders and the value tool_ui_incident.component_version
#     records. It is NOT trigger-managed, so a manual "bump the version" only
#     means anything when applied to THIS column.
#
# So `bump_version` advances semver (the dotted string), never the integer.
def _bump_semver_patch(semver: str | None) -> str:
    """Increment the trailing numeric segment of a dotted semver string."""
    base = (semver or "1.0.0").strip() or "1.0.0"
    parts = base.split(".")
    try:
        parts[-1] = str(int(parts[-1]) + 1)
        return ".".join(parts)
    except ValueError:
        # Non-numeric tail (e.g. '1.0.0-beta') — append a fresh patch segment.
        return base + ".1"


def _extract_sample_shape(sample: dict) -> dict:
    """
    Reduce a raw tool test sample to what the component agent actually needs:
    - The arguments used (so agent knows what data shape to expect)
    - A concise event timeline (type + message, no giant text blobs)
    - Whether the sample succeeded
    - The final output schema from metadata
    """
    final_payload = sample.get("final_payload") or {}
    output = final_payload.get("output") or {}
    full_result = output.get("full_result") or {}
    metadata = final_payload.get("metadata") or {}

    events = sample.get("raw_stream_events") or []
    timeline = []
    for ev in events:
        event_type = ev.get("event", "")
        data = ev.get("data") or {}

        if event_type == "chunk":
            if not timeline or timeline[-1].get("event") != "chunk":
                timeline.append({"event": "chunk", "note": "(streaming text)"})
            continue

        if event_type == "heartbeat":
            continue

        entry: dict[str, Any] = {"event": event_type}
        if event_type == "status_update":
            entry["status"] = data.get("status")
            entry["message"] = data.get("user_message") or data.get("system_message")
        elif event_type == "tool_event":
            entry["tool_event"] = data.get("event")
            entry["message"] = data.get("message")
            entry["tool_name"] = data.get("tool_name")
        elif event_type == "completion":
            entry["status"] = data.get("status")
        elif event_type == "data":
            inner = data.get("event")
            if inner:
                entry["inner_event"] = inner
        elif event_type == "end":
            entry["reason"] = data.get("reason")

        timeline.append(entry)

    raw_output = full_result.get("output", "")
    if raw_output:
        preview_text = str(raw_output)
        # Cut at a word boundary near 900 chars rather than mid-character
        if len(preview_text) > 900:
            cut = preview_text.rfind(" ", 700, 900)
            preview_text = preview_text[: cut if cut != -1 else 900] + "…"
    else:
        preview_text = None

    return {
        "id": sample.get("id"),
        "is_success": sample.get("is_success"),
        "use_for_component": sample.get("use_for_component"),
        "arguments_used": sample.get("arguments"),
        "event_timeline": timeline,
        # output_schema intentionally omitted — already in tool.output_schema
        "execution_stats": {
            "duration_ms": full_result.get("duration_ms"),
        },
        "output_preview": preview_text,
        "admin_comments": sample.get("admin_comments"),
    }


def _dedup_incidents(incidents: list[dict]) -> list[dict]:
    """
    Collapse incidents with identical signatures into a single entry.

    Two incidents are considered the same if they share:
      - error_type
      - error_message (exact)
      - first 300 chars of error_stack (catches same exception from same call site
        even when the minified bundle name changes between deploys)

    The oldest incident ID is kept as the canonical ID.
    All occurrence timestamps are collected into `occurrences`.
    """
    groups: dict[str, dict] = {}

    for inc in incidents:
        stack = (inc.get("error_stack") or "")[:300]
        key = (
            inc.get("error_type") or "",
            inc.get("error_message") or "",
            stack,
        )

        if key not in groups:
            groups[key] = {
                "id": inc.get("id"),
                "component_type": inc.get("component_type"),
                "error_type": inc.get("error_type"),
                "error_message": inc.get("error_message"),
                "error_stack_preview": stack or None,
                "component_version": inc.get("component_version"),
                "resolved": inc.get("resolved"),
                "resolution_notes": inc.get("resolution_notes"),
                "occurrences": [],
                "tool_update_snapshot_keys": (
                    list(inc["tool_update_snapshot"].keys())
                    if isinstance(inc.get("tool_update_snapshot"), dict)
                    else None
                ),
            }

        ts = inc.get("created_at")
        if ts:
            groups[key]["occurrences"].append(ts)

    result = []
    for group in groups.values():
        occs = sorted(group["occurrences"])
        group["first_seen"] = occs[0] if occs else None
        group["last_seen"] = occs[-1] if occs else None
        group["occurrence_count"] = len(occs)
        del group["occurrences"]
        result.append(group)

    # Sort by most recent first
    result.sort(key=lambda g: g.get("last_seen") or "", reverse=True)
    return result


_TOOL_DEF_FIELDS = (
    "id, name, description, parameters, output_schema, annotations, "
    "source_kind, managed_by_server_id, category, tags, icon, is_active"
)


def _workflow_component_tool_stub(tool_name: str, surface_name: str) -> dict[str, Any]:
    return {
        "id": None,
        "name": tool_name,
        "description": "Workflow emit-to-frontend component (no backing tool_def row).",
        "parameters": {},
        "output_schema": None,
        "annotations": None,
        "source_kind": "workflow_component",
        "managed_by_server_id": None,
        "category": None,
        "tags": None,
        "icon": None,
        "is_active": True,
        "surface_name": surface_name,
        "is_workflow_component": True,
    }


def _summarize_components(components: list[dict]) -> list[dict]:
    summaries: list[dict] = []
    for comp in components:
        summaries.append(
            {
                "id": comp.get("id"),
                "tool_name": comp.get("tool_name"),
                "surface_name": comp.get("surface_name"),
                "display_name": comp.get("display_name"),
                "results_label": comp.get("results_label"),
                "language": comp.get("language"),
                "semver": comp.get("semver"),
                "version": comp.get("version"),
                "is_active": comp.get("is_active"),
                "keep_expanded_on_stream": comp.get("keep_expanded_on_stream"),
                "allowed_imports": comp.get("allowed_imports"),
                "notes": comp.get("notes"),
                "has_inline_code": bool(comp.get("inline_code")),
                "has_overlay_code": bool(comp.get("overlay_code")),
                "has_utility_code": bool(comp.get("utility_code")),
                "has_header_extras_code": bool(comp.get("header_extras_code")),
                "has_header_subtitle_code": bool(comp.get("header_subtitle_code")),
                "inline_code_length": len(comp.get("inline_code") or ""),
                "overlay_code_length": len(comp.get("overlay_code") or ""),
                "created_at": comp.get("created_at"),
                "updated_at": comp.get("updated_at"),
            }
        )
    return summaries


_TOOL_DEF_FIELD_TUPLE = tuple(f.strip() for f in _TOOL_DEF_FIELDS.split(","))


async def _fetch_tool_def(tool_id: str) -> dict[str, Any] | None:
    ToolDefinition = get_db_model("ToolDefinition")
    row = await ToolDefinition.get_or_none(id=tool_id)
    return _row_dict(row, _TOOL_DEF_FIELD_TUPLE) if row else None


async def _fetch_components_by_tool_id(
    tool_id: str,
    *,
    surface_name: str | None = None,
) -> list[dict]:
    ToolUi = get_db_model("ToolUi")
    filters: dict[str, Any] = {"tool_id": tool_id}
    if surface_name:
        filters["surface_name"] = surface_name
    rows = await ToolUi.filter(**filters).all()
    return [_row_dict(r) for r in rows]


async def _fetch_components_by_name_surface(
    tool_name: str,
    surface_name: str,
) -> list[dict]:
    ToolUi = get_db_model("ToolUi")
    rows = await ToolUi.filter(tool_name=tool_name, surface_name=surface_name).all()
    return [_row_dict(r) for r in rows]


async def toolcomp_get_context(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Primary context-fetching tool for the tool component agent.

    Returns a focused, curated bundle of everything the agent needs to
    understand and work on a specific tool's UI component:

    - Tool metadata (name, description, parameters, output_schema)
    - Current component code (inline_code, overlay_code, settings)
    - Condensed sample data (event timelines, arguments, output previews)
    - Open incidents (errors the component has thrown in production)

    Use this as the first call when working on any tool component.
    """
    from matrx_ai.tools._generated_declarations import ToolcompGetContextArgs

    ToolcompGetContextArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    component_id = (args.get("component_id") or "").strip() or None
    tool_name = (args.get("tool_name") or "").strip() or None
    tool_id = (args.get("tool_id") or "").strip() or None
    surface_name = (args.get("surface_name") or "").strip() or None

    if not component_id and not tool_name and not tool_id:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="Provide component_id, tool_name, or tool_id.",
                suggested_action=(
                    "Real-tool components: tool_name or tool_id. Workflow components "
                    f"(tool_id=NULL): tool_name + surface_name='{WORKFLOW_RENDER_SURFACE}', "
                    "or component_id from toolcomp_create_component."
                ),
            ),
        )

    try:
        ToolUi = get_db_model("ToolUi")
        ToolDefinition = get_db_model("ToolDefinition")
        ToolTestSample = get_db_model("ToolTestSample")
        ToolUiIncident = get_db_model("ToolUiIncident")

        tool: dict[str, Any] | None = None
        components: list[dict] = []
        resolved_tool_name: str | None = None
        is_workflow_component = False

        if component_id:
            comp_row = await ToolUi.get_or_none(id=component_id)
            if not comp_row:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="not_found",
                        message=f"No component found with id '{component_id}'.",
                    ),
                )
            components = [_row_dict(comp_row)]
            comp = components[0]
            resolved_tool_name = comp.get("tool_name")
            surface_name = surface_name or comp.get("surface_name")
            tool_id = comp.get("tool_id")
            if tool_id:
                tool = await _fetch_tool_def(tool_id)
            if tool is None:
                is_workflow_component = True
                tool = _workflow_component_tool_stub(
                    resolved_tool_name or "",
                    surface_name or WORKFLOW_RENDER_SURFACE,
                )

        elif tool_id:
            tool = await _fetch_tool_def(tool_id)
            if not tool:
                return ToolResult(
                    success=False,
                    error=ToolError(error_type="not_found", message=f"Tool '{tool_id}' not found."),
                )
            resolved_tool_name = tool["name"]
            components = await _fetch_components_by_tool_id(tool_id, surface_name=surface_name)

        elif tool_name and surface_name:
            components = await _fetch_components_by_name_surface(tool_name, surface_name)
            if not components:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="not_found",
                        message=(
                            f"No component found for tool_name '{tool_name}' "
                            f"on surface '{surface_name}'."
                        ),
                        suggested_action=(
                            "Check tool_name and surface_name, or pass component_id "
                            "from toolcomp_create_component."
                        ),
                    ),
                )
            resolved_tool_name = tool_name
            tool_id = components[0].get("tool_id")
            if tool_id:
                tool = await _fetch_tool_def(tool_id)
            if tool is None:
                is_workflow_component = True
                tool = _workflow_component_tool_stub(tool_name, surface_name)

        elif tool_name:
            def_row = await ToolDefinition.get_or_none(name=tool_name)
            if def_row:
                tool_id = str(def_row.id)
                tool = await _fetch_tool_def(tool_id)
                resolved_tool_name = tool["name"] if tool else tool_name
                components = await _fetch_components_by_tool_id(tool_id)
            else:
                wf_surface = WORKFLOW_RENDER_SURFACE
                components = await _fetch_components_by_name_surface(tool_name, wf_surface)
                if not components:
                    return ToolResult(
                        success=False,
                        error=ToolError(
                            error_type="not_found",
                            message=f"No tool or workflow component found with name '{tool_name}'.",
                            suggested_action=(
                                "For a real tool, check the name with toolcomp_list_tools. "
                                f"For a workflow component, pass surface_name='{WORKFLOW_RENDER_SURFACE}'."
                            ),
                        ),
                    )
                resolved_tool_name = tool_name
                is_workflow_component = True
                tool = _workflow_component_tool_stub(tool_name, wf_surface)
                surface_name = wf_surface

        if tool is None or resolved_tool_name is None:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="execution",
                    message="Failed to resolve tool/component context.",
                ),
            )

        if tool_id and not is_workflow_component:
            sample_rows = (
                await ToolTestSample.filter(tool_id=tool_id).order_by("-created_at").limit(3).all()
            )
            raw_samples = [_row_dict(r) for r in sample_rows]
        else:
            raw_samples = []
        samples = [_extract_sample_shape(s) for s in raw_samples]
        has_reference_sample = any(s.get("use_for_component") for s in raw_samples)

        incident_rows = (
            await ToolUiIncident.filter(tool_name=resolved_tool_name, resolved=False)
            .order_by("-created_at")
            .limit(50)
            .all()
        )
        raw_incidents = [_row_dict(r) for r in incident_rows]
        incidents = _dedup_incidents(raw_incidents)
        component_summaries = _summarize_components(components)

        total_raw_incidents = len(raw_incidents)
        deduped_incident_count = len(incidents)

        return ToolResult(
            success=True,
            output=ToolComponentContext(
                tool=tool,
                components=component_summaries,
                component_ids=[c["id"] for c in component_summaries],
                samples=samples,
                open_incidents=incidents,
                summary={
                    "tool_id": tool_id,
                    "tool_name": resolved_tool_name,
                    "surface_name": surface_name
                    or (
                        component_summaries[0].get("surface_name") if component_summaries else None
                    ),
                    "is_workflow_component": is_workflow_component,
                    "has_component": len(component_summaries) > 0,
                    "sample_count": len(samples),
                    "has_reference_sample": has_reference_sample,
                    "open_incident_types": deduped_incident_count,
                    "open_incident_total_occurrences": total_raw_incidents,
                },
            ),
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=str(e),
                traceback=traceback.format_exc(),
                is_retryable=True,
            ),
        )


async def toolcomp_get_code(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Retrieve the full source code for a specific tool UI component.

    Use this when you need to read the actual component code before editing it.
    Specify which code sections to return: inline_code, overlay_code,
    utility_code, header_extras_code, or header_subtitle_code.
    Defaults to inline_code and overlay_code.

    Output format: JSON metadata block followed by each code section as a
    labeled fenced code block. Use the section labels (e.g. [inline_code])
    to identify which block to reference when calling toolcomp_patch_code
    or toolcomp_update_code.
    """
    from matrx_ai.tools._generated_declarations import ToolcompGetCodeArgs

    ToolcompGetCodeArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    component_id = args.get("component_id", "").strip()
    sections = args.get("sections") or ["inline_code", "overlay_code"]

    if not component_id:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="component_id is required.",
                suggested_action="Get the component_id from toolcomp_get_context first.",
            ),
        )

    valid_sections = {
        "inline_code",
        "overlay_code",
        "utility_code",
        "header_extras_code",
        "header_subtitle_code",
    }
    invalid = [s for s in sections if s not in valid_sections]
    if invalid:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=f"Invalid sections: {invalid}. Valid: {sorted(valid_sections)}",
            ),
        )

    try:
        ToolUi = get_db_model("ToolUi")
        fields = (
            "id",
            "tool_name",
            "display_name",
            "semver",
            "version",
            "language",
            "allowed_imports",
            *sections,
        )
        comp_row = await ToolUi.get_or_none(id=component_id)

        if not comp_row:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found", message=f"Component '{component_id}' not found."
                ),
            )

        comp = _row_dict(comp_row, fields)
        lang = comp.get("language") or "tsx"

        # Build the metadata block (no code here — just facts the model needs
        # to correctly call patch/update tools)
        section_lengths = {s: len(comp.get(s) or "") for s in sections}
        metadata = {
            "component_id": comp["id"],
            "tool_name": comp.get("tool_name"),
            "display_name": comp.get("display_name"),
            "semver": comp.get("semver"),  # human-facing version label (what the FE renders)
            "version": comp.get(
                "version"
            ),  # DB-managed integer revision (matches tool_ui_version snapshots)
            "language": lang,
            "allowed_imports": comp.get("allowed_imports"),
            "sections_returned": sections,
            "section_lengths": section_lengths,
        }

        # Emit metadata as compact JSON, then each code section as a raw
        # fenced block so the model reads actual code, not JSON-escaped strings.
        parts: list[str] = [json.dumps(metadata, indent=2)]

        for section in sections:
            code = comp.get(section) or ""
            parts.append(f"\n\n[{section}]\n```{lang}\n{code}\n```")

        output_str = "".join(parts)

        # Structured kind on ``output`` (what is stored / rendered / typed);
        # the deliberate fenced-block text still reaches the MODEL untouched
        # via provider_content (see ToolResult.to_tool_result_content).
        return ToolResult(
            success=True,
            output=ToolComponentCode(
                **metadata,
                sections={s: comp.get(s) or "" for s in sections},
            ),
            provider_content=output_str,
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def toolcomp_update_code(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Write updated code to a specific section of a tool UI component.

    Always provide the COMPLETE replacement code for the section — never partial.
    You can update multiple sections in a single call.
    Optionally bump the human-facing semver and add notes explaining what changed.
    (The integer revision auto-increments in the DB on every save regardless.)
    """
    from matrx_ai.tools._generated_declarations import ToolcompUpdateCodeArgs

    ToolcompUpdateCodeArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    component_id = args.get("component_id", "").strip()
    updates = args.get("updates") or {}
    notes = args.get("notes", "").strip() or None
    bump_version = args.get("bump_version", False)

    if not component_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="component_id is required."),
        )

    valid_code_fields = {
        "inline_code",
        "overlay_code",
        "utility_code",
        "header_extras_code",
        "header_subtitle_code",
    }
    invalid = [k for k in updates if k not in valid_code_fields]
    if invalid:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=f"Invalid update keys: {invalid}. Only code sections are allowed: {sorted(valid_code_fields)}",
                suggested_action="To update settings (version, notes, etc.) use toolcomp_update_settings.",
            ),
        )

    if not updates:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation", message="No code sections provided in updates."
            ),
        )

    try:
        ToolUi = get_db_model("ToolUi")
        code_sections = list(updates.keys())  # capture before folding in semver/notes

        # bump_version advances the human-facing semver (TEXT). The integer
        # `version` is DB-trigger-managed and must never be written here.
        if bump_version:
            cur = await ToolUi.get_or_none(id=component_id)
            if cur:
                updates["semver"] = _bump_semver_patch(cur.semver)

        if notes is not None:
            updates["notes"] = notes

        # update_where(...) is a single UPDATE statement (no RETURNING) — the
        # `version`/`updated_at` columns are DB-trigger-managed, so re-fetch
        # the row afterward to read back the trigger's computed values rather
        # than trusting a stale in-memory instance.
        rows_affected = await ToolUi.update_where({"id": component_id}, **updates)
        if not rows_affected:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="execution", message="Update returned no data. Check component_id."
                ),
            )
        updated_row = await ToolUi.get_or_none(id=component_id)

        updated = _row_dict(updated_row, ("semver", "version", "updated_at")) if updated_row else {}
        return ToolResult(
            success=True,
            output=ToolComponentUpdateResult(
                component_id=component_id,
                updated_sections=code_sections,
                semver=updated.get("semver"),  # human-facing version label
                version=updated.get("version"),  # DB-managed integer revision (auto-bumped)
                updated_at=updated.get("updated_at"),
                message=f"Successfully updated {len(code_sections)} section(s) on component {component_id}.",
            ),
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def toolcomp_update_settings(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Update non-code settings on a tool UI component.

    Use this to change display_name, results_label, allowed_imports,
    keep_expanded_on_stream, language, is_active, or notes.
    Does NOT accept code fields — use toolcomp_update_code for code.
    """
    from matrx_ai.tools._generated_declarations import ToolcompUpdateSettingsArgs

    ToolcompUpdateSettingsArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    component_id = args.get("component_id", "").strip()
    settings = args.get("settings") or {}

    if not component_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="component_id is required."),
        )

    valid_settings = {
        "display_name",
        "results_label",
        "allowed_imports",
        "keep_expanded_on_stream",
        "language",
        "is_active",
        "notes",
    }
    code_fields = {
        "inline_code",
        "overlay_code",
        "utility_code",
        "header_extras_code",
        "header_subtitle_code",
    }
    rejected_code = [k for k in settings if k in code_fields]
    invalid = [k for k in settings if k not in valid_settings and k not in code_fields]

    if rejected_code:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=f"Code fields not allowed here: {rejected_code}. Use toolcomp_update_code instead.",
            ),
        )

    if invalid:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=f"Unknown settings keys: {invalid}. Valid: {sorted(valid_settings)}",
            ),
        )

    if not settings:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="No settings provided."),
        )

    try:
        ToolUi = get_db_model("ToolUi")
        rows_affected = await ToolUi.update_where({"id": component_id}, **settings)

        if not rows_affected:
            return ToolResult(
                success=False,
                error=ToolError(error_type="execution", message="Update returned no data."),
            )
        updated_row = await ToolUi.get_or_none(id=component_id)

        updated = _row_dict(updated_row, ("updated_at",)) if updated_row else {}
        return ToolResult(
            success=True,
            output=ToolComponentUpdateResult(
                component_id=component_id,
                updated_settings=list(settings.keys()),
                updated_at=updated.get("updated_at"),
            ),
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def toolcomp_get_sample_detail(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Retrieve the complete raw stream events for a specific test sample.

    By default this still condenses the data — only request full_events=true
    if you genuinely need to inspect individual streaming chunks or a
    specific event payload in detail.

    Useful for understanding exactly what data the component will receive
    during a real tool execution stream.
    """
    from matrx_ai.tools._generated_declarations import ToolcompGetSampleDetailArgs

    ToolcompGetSampleDetailArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    sample_id = args.get("sample_id", "").strip()
    full_events = args.get("full_events", False)
    event_offset = max(int(args.get("event_offset", 0)), 0)
    event_limit = min(max(int(args.get("event_limit", 10)), 1), 10)

    if not sample_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="sample_id is required."),
        )

    try:
        ToolTestSample = get_db_model("ToolTestSample")
        sample_row = await ToolTestSample.get_or_none(id=sample_id)

        if not sample_row:
            return ToolResult(
                success=False,
                error=ToolError(error_type="not_found", message=f"Sample '{sample_id}' not found."),
            )

        sample = _row_dict(sample_row)

        if full_events:
            from matrx_ai.tools.output_caps import cap_text

            def _bounded_json(value: Any, *, limit: int) -> Any:
                serialized = json.dumps(value, default=str, ensure_ascii=False)
                if len(serialized) <= limit:
                    return value
                preview, info = cap_text(serialized, limit=limit)
                return {
                    "preview": preview,
                    "total_chars": info.total_chars,
                    "shown_chars": info.shown_chars,
                    "truncated": True,
                }

            raw_events = sample.get("raw_stream_events")
            events = raw_events if isinstance(raw_events, list) else []
            page = events[event_offset : event_offset + event_limit]
            return ToolResult(
                success=True,
                output=ToolComponentSample(
                    sample_id=sample_id,
                    arguments=_bounded_json(sample.get("arguments"), limit=4_000),
                    is_success=sample.get("is_success"),
                    raw_stream_events={
                        "events": [_bounded_json(event, limit=2_500) for event in page],
                        "event_offset": event_offset,
                        "event_limit": event_limit,
                        "total_events": len(events),
                        "returned_events": len(page),
                        "has_more_events": event_offset + len(page) < len(events),
                        "next_event_offset": (
                            event_offset + len(page)
                            if event_offset + len(page) < len(events)
                            else None
                        ),
                    },
                    final_payload=_bounded_json(sample.get("final_payload"), limit=8_000),
                    admin_comments=cap_text(sample.get("admin_comments"), limit=2_000)[0],
                ),
                output_self_capped=True,
            )

        return ToolResult(
            success=True,
            output=ToolComponentSample(**_extract_sample_shape(sample)),
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def toolcomp_get_incident_detail(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Retrieve full details for a specific tool UI component incident (error report).

    Includes the complete error stack trace and the tool_update_snapshot —
    the exact data the component received when it crashed.

    Use this to diagnose component errors and reproduce bugs.
    """
    from matrx_ai.tools._generated_declarations import ToolcompGetIncidentDetailArgs

    ToolcompGetIncidentDetailArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    incident_id = args.get("incident_id", "").strip()

    if not incident_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="incident_id is required."),
        )

    try:
        ToolUiIncident = get_db_model("ToolUiIncident")
        incident_row = await ToolUiIncident.get_or_none(id=incident_id)

        if not incident_row:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found", message=f"Incident '{incident_id}' not found."
                ),
            )

        incident = _row_dict(incident_row)
        return ToolResult(
            success=True,
            output=ToolComponentIncidentDetail(
                incident_id=incident_id,
                tool_name=incident.get("tool_name"),
                component_id=incident.get("component_id"),
                component_type=incident.get("component_type"),
                component_version=incident.get("component_version"),
                error_type=incident.get("error_type"),
                error_message=incident.get("error_message"),
                error_stack=incident.get("error_stack"),
                browser_info=incident.get("browser_info"),
                session_id=incident.get("session_id"),
                tool_update_snapshot=incident.get("tool_update_snapshot"),
                resolved=incident.get("resolved"),
                resolution_notes=incident.get("resolution_notes"),
                created_at=incident.get("created_at"),
            ),
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def toolcomp_resolve_incident(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Mark a tool UI component incident as resolved.

    Call this after deploying a fix so the incident no longer appears
    in the open incidents list returned by toolcomp_get_context.
    """
    from matrx_ai.tools._generated_declarations import ToolcompResolveIncidentArgs

    ToolcompResolveIncidentArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    incident_id = args.get("incident_id", "").strip()
    resolution_notes = args.get("resolution_notes", "").strip()

    if not incident_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="incident_id is required."),
        )

    try:
        from datetime import datetime

        ToolUiIncident = get_db_model("ToolUiIncident")
        resolved_at = datetime.now(UTC)
        updates: dict[str, Any] = {
            "resolved": True,
            "resolved_at": resolved_at,
            "resolved_by": ctx.user_id,
        }
        if resolution_notes:
            updates["resolution_notes"] = resolution_notes

        rows_affected = await ToolUiIncident.update_where({"id": incident_id}, **updates)

        if not rows_affected:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found", message=f"Incident '{incident_id}' not found."
                ),
            )

        updates["resolved_at"] = resolved_at.isoformat()
        return ToolResult(
            success=True,
            output=ToolComponentIncidentResolution(
                incident_id=incident_id,
                resolved=True,
                resolved_at=updates["resolved_at"],
                resolution_notes=resolution_notes or None,
            ),
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def toolcomp_list_tools(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    List and discover available tools.

    Modes:
    - Default: flat paginated list with optional filters.
    - group_by="prefix": groups tools by their name prefix (e.g. "web" groups
      web_search, web_read, research_web). Best way to see what tool families exist.
    - group_by="category": groups by the category field.
    - group_by="source_kind": groups by source_kind (native, mcp_discovered,
      admin_authored, agent_authored).

    Filters (all combinable):
    - category: exact match on the category field
    - source_kind: exact match on source_kind (one of "native",
      "mcp_discovered", "admin_authored", "agent_authored")
    - prefix: filter to tools whose name starts with this prefix (e.g. "web", "toolcomp")
    - tag: filter to tools that include this tag
    - has_component: true = only tools with a UI component; false = only those without
    - is_active: filter by active status (default: no filter, returns all)

    Pagination:
    - limit: max results per page (default 30, max 100)
    - offset: skip this many results (default 0)
    - Returns has_more and next_offset when more results exist.
    """
    from matrx_ai.tools._generated_declarations import ToolcompListToolsArgs

    ToolcompListToolsArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    category = args.get("category", "").strip() or None
    source_kind = args.get("source_kind", "").strip() or None
    prefix = args.get("prefix", "").strip() or None
    tag = args.get("tag", "").strip() or None
    has_component = args.get("has_component")
    is_active = args.get("is_active")
    group_by = args.get("group_by", "").strip() or None
    limit = min(int(args.get("limit", 30)), 100)
    offset = max(int(args.get("offset", 0)), 0)

    if group_by and group_by not in ("prefix", "category", "source_kind"):
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=f"Invalid group_by '{group_by}'. Valid values: 'prefix', 'category', 'source_kind'.",
            ),
        )

    try:
        ToolDefinition = get_db_model("ToolDefinition")
        ToolUi = get_db_model("ToolUi")

        # Fetch the full filtered set from DB (we'll paginate in Python after
        # applying Python-side filters like tag and has_component).
        # Fetch up to 500 so pagination math is accurate.
        list_fields = ("id", "name", "description", "category", "tags", "is_active", "source_kind")
        filters: dict[str, Any] = {}
        if category:
            filters["category"] = category
        if source_kind:
            filters["source_kind"] = source_kind
        if is_active is not None:
            filters["is_active"] = is_active

        query = ToolDefinition.filter(**filters)
        if prefix:
            from matrx_orm import F, Like

            # case-insensitive prefix match — same shape as the PostgREST ilike() this replaces.
            query = query.filter(
                Like(F("name"), f"{prefix}_%", case_insensitive=True)
            )

        tool_rows = await query.order_by("name").limit(500).all()
        tools = [_row_dict(t, list_fields) for t in tool_rows]

        # Python-side filters (tag requires scanning the array, has_component
        # requires a second table lookup)
        if tag:
            tools = [t for t in tools if tag in (t.get("tags") or [])]

        if has_component is not None:
            comp_rows = await ToolUi.filter().all()
            tool_ids_with_comp = {str(c.tool_id) for c in comp_rows if c.tool_id is not None}
            if has_component:
                tools = [t for t in tools if t["id"] in tool_ids_with_comp]
            else:
                tools = [t for t in tools if t["id"] not in tool_ids_with_comp]

        total_matching = len(tools)

        def _tool_row(t: dict) -> dict:
            return {
                "id": t["id"],
                "name": t["name"],
                "description": (t.get("description") or "")[:120],
                "category": t.get("category"),
                "tags": t.get("tags"),
                "is_active": t.get("is_active"),
                "source_kind": t.get("source_kind"),
            }

        # ── Grouped mode ────────────────────────────────────────────────────
        if group_by:
            groups: dict[str, list[dict]] = {}
            for t in tools:
                if group_by == "prefix":
                    key = t["name"].split("_")[0] if "_" in t["name"] else t["name"]
                elif group_by == "category":
                    key = t.get("category") or "uncategorized"
                else:  # source_kind
                    key = t.get("source_kind") or "unknown"

                groups.setdefault(key, []).append(_tool_row(t))

            sorted_groups = sorted(groups.items())
            return ToolResult(
                success=True,
                output=ToolComponentListing(
                    group_by=group_by,
                    total_tools=total_matching,
                    group_count=len(sorted_groups),
                    groups={
                        key: {
                            "count": len(rows),
                            "tools": rows,
                        }
                        for key, rows in sorted_groups
                    },
                ),
            )

        # ── Flat paginated mode ──────────────────────────────────────────────
        page = tools[offset : offset + limit]
        has_more = (offset + limit) < total_matching
        next_offset = offset + limit if has_more else None

        return ToolResult(
            success=True,
            output=ToolComponentListing(
                total_matching=total_matching,
                offset=offset,
                limit=limit,
                returned=len(page),
                has_more=has_more,
                next_offset=next_offset,
                tools=[_tool_row(t) for t in page],
            ),
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


async def toolcomp_create_component(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Create a new tool UI render component.

    Two shapes, one path:
    - Real-tool component (chat/default surface): provide tool_id, display_name,
      and inline_code. tool_name is derived from the tool_def row.
    - Workflow "emit to frontend" component: provide an explicit tool_name (no
      tool_id — these have no backing tool_def row) and set
      surface_name="matrx-user/workflow". A workflow node references the
      component by this tool_name string.

    surface_name defaults to the chat/default surface, so existing callers are
    unaffected. overlay_code is optional but recommended for rich output.
    Components are unique per (tool_name, surface_name).

    After creating, use toolcomp_update_code to update individual sections.
    """
    from matrx_ai.tools._generated_declarations import ToolcompCreateComponentArgs

    ToolcompCreateComponentArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    tool_id = args.get("tool_id", "").strip() or None
    tool_name = args.get("tool_name", "").strip() or None
    display_name = args.get("display_name", "").strip()
    inline_code = args.get("inline_code", "").strip()
    overlay_code = args.get("overlay_code", "").strip() or None
    results_label = args.get("results_label", "").strip() or None
    allowed_imports = args.get("allowed_imports") or ["react", "lucide-react"]
    language = args.get("language", "tsx")
    surface_name = args.get("surface_name", "").strip() or DEFAULT_RENDER_SURFACE
    notes = args.get("notes", "").strip() or None

    if not display_name or not inline_code:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message="display_name and inline_code are required.",
            ),
        )

    if not tool_id and not tool_name:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=(
                    "Provide tool_id (a real tool_def row — tool_name is derived) "
                    "or an explicit tool_name (e.g. a workflow render component, "
                    f"surface_name='{WORKFLOW_RENDER_SURFACE}')."
                ),
                suggested_action=(
                    "For a tool's UI component pass tool_id. For a workflow "
                    "emit-to-frontend component pass tool_name + surface_name="
                    f"'{WORKFLOW_RENDER_SURFACE}'."
                ),
            ),
        )

    try:
        ToolDefinition = get_db_model("ToolDefinition")
        ToolUi = get_db_model("ToolUi")

        # tool_id present → it must exist; tool_name is derived from it. If the
        # caller ALSO passed tool_name, the two must agree (no silent override).
        if tool_id:
            def_row = await ToolDefinition.get_or_none(id=tool_id)
            if not def_row:
                return ToolResult(
                    success=False,
                    error=ToolError(error_type="not_found", message=f"Tool '{tool_id}' not found."),
                )
            derived_name = def_row.name
            if tool_name and tool_name != derived_name:
                return ToolResult(
                    success=False,
                    error=ToolError(
                        error_type="validation",
                        message=(
                            f"tool_name '{tool_name}' does not match the name of "
                            f"tool_id {tool_id} ('{derived_name}'). Omit tool_name "
                            "when passing tool_id — it is derived from the tool."
                        ),
                    ),
                )
            tool_name = derived_name

        # Uniqueness is (tool_name, surface_name) in the DB — check that exact key
        # (works for both real-tool rows and tool_id=NULL workflow rows).
        existing_rows = (
            await ToolUi.filter(tool_name=tool_name, surface_name=surface_name).limit(1).all()
        )
        if existing_rows:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=(
                        f"A component already exists for tool_name '{tool_name}' on "
                        f"surface '{surface_name}' (id: {existing_rows[0].id}). "
                        "Use toolcomp_update_code to modify it."
                    ),
                    suggested_action="Use toolcomp_update_code with the existing component_id.",
                ),
            )

        # tool_ui.organization_id is NOT NULL (2026 schema-reorg) and — unlike
        # the chat.* tables — has no backstop trigger, so an unstamped insert
        # fails at the DB. The writer receives an EXPLICIT org (the request's
        # active org); a fallback to personal/system here is forbidden by the
        # db-rules contract, so a request with no org is refused by name.
        if not ctx.organization_id:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=(
                        "This request carries no active organization, and "
                        "tool_ui rows require an explicit organization_id."
                    ),
                    suggested_action="Retry from a session with an active organization.",
                ),
            )

        payload: dict[str, Any] = {
            "organization_id": ctx.organization_id,
            "tool_id": tool_id,  # NULL for workflow components — column is nullable
            "tool_name": tool_name,
            "display_name": display_name,
            "inline_code": inline_code,
            "allowed_imports": allowed_imports,
            "language": language,
            "surface_name": surface_name,  # NOT NULL, no DB default — always set
            "is_active": True,
            "keep_expanded_on_stream": False,
        }
        if overlay_code:
            payload["overlay_code"] = overlay_code
        if results_label:
            payload["results_label"] = results_label
        if notes:
            payload["notes"] = notes

        created_row = await ToolUi.create_item(**payload)
        created = _row_dict(created_row, ("id", "created_at"))

        return ToolResult(
            success=True,
            output=ToolComponentCreateResult(
                component_id=created.get("id"),
                tool_id=tool_id,
                tool_name=tool_name,
                surface_name=surface_name,
                display_name=display_name,
                created_at=created.get("created_at"),
                message=f"Component created for '{tool_name}' on surface '{surface_name}'.",
            ),
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )


# ---------------------------------------------------------------------------
# String-replacement matching — three rounds of decreasing strictness
# ---------------------------------------------------------------------------


def _normalize_whitespace(s: str) -> str:
    """Collapse all whitespace runs to a single space and strip."""
    return re.sub(r"\s+", " ", s).strip()


def _normalize_quotes(s: str) -> str:
    """Normalize smart quotes, backtick strings, and mixed quote styles."""
    s = s.replace("\u2018", "'").replace("\u2019", "'")
    s = s.replace("\u201c", '"').replace("\u201d", '"')
    s = s.replace("`", "'")
    return s


def _apply_patch(code: str, old_str: str, new_str: str) -> tuple[str, str]:
    """
    Apply a single old→new replacement using three rounds of matching:

    Round 1 — Exact literal match.
    Round 2 — Whitespace-normalized: any whitespace sequence matches any other.
    Round 3 — Quote + whitespace normalized: additionally treats smart quotes,
               backticks, and standard quotes as interchangeable.

    Returns (patched_code, round_applied).
    Raises ValueError if no round matches.
    """
    # Round 1: exact
    if old_str in code:
        return code.replace(old_str, new_str, 1), "exact"

    # Round 2: whitespace-normalized regex
    # Build a pattern from old_str where whitespace sequences become \s+
    escaped = re.escape(old_str)
    ws_pattern = re.sub(r"(\\ |\\\t|\\\n|\\\r)+", r"\\s+", escaped)
    match = re.search(ws_pattern, code)
    if match:
        return code[: match.start()] + new_str + code[match.end() :], "whitespace_normalized"

    # Round 3: quote + whitespace normalized
    quote_chars = r"""['"` \u2018\u2019\u201c\u201d]"""
    parts: list[str] = []
    i = 0
    while i < len(old_str):
        ch = old_str[i]
        if ch in "'\"`\u2018\u2019\u201c\u201d":
            parts.append(quote_chars)
        elif ch in " \t\n\r":
            # consume any following whitespace chars too
            parts.append(r"\s+")
            while i + 1 < len(old_str) and old_str[i + 1] in " \t\n\r":
                i += 1
        else:
            parts.append(re.escape(ch))
        i += 1

    combined = "".join(parts)
    match = re.search(combined, code)
    if match:
        return code[: match.start()] + new_str + code[match.end() :], "quote_normalized"

    raise ValueError(f"No match found in any round.\nold_string preview: {old_str[:200]!r}")


async def toolcomp_patch_code(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """
    Apply one or more targeted string replacements to a tool UI component's
    code without rewriting the whole section.

    Each patch specifies an old_string to find and a new_string to replace it
    with. Patches are applied in order — each one operates on the result of
    the previous patch.

    Matching uses three rounds of decreasing strictness:
    - Round 1: exact character match
    - Round 2: whitespace-normalized (any whitespace sequence equals any other)
    - Round 3: quote + whitespace normalized (smart quotes, backticks treated
      as equivalent to standard ASCII quotes)

    If any patch fails all three rounds, the ENTIRE operation is aborted and
    NO changes are written — all patches succeed or none are applied.
    """
    from matrx_ai.tools._generated_declarations import ToolcompPatchCodeArgs

    ToolcompPatchCodeArgs.model_validate(
        args
    )  # enforce the declared arg contract (common-docs/systems/agents/agent-tools/HANDOFF.md)
    component_id = args.get("component_id", "").strip()
    section = args.get("section", "inline_code").strip()
    patches = args.get("patches") or []
    notes = args.get("notes", "").strip() or None
    bump_version = args.get("bump_version", False)

    valid_sections = {
        "inline_code",
        "overlay_code",
        "utility_code",
        "header_extras_code",
        "header_subtitle_code",
    }

    if not component_id:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="component_id is required."),
        )

    if section not in valid_sections:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="validation",
                message=f"Invalid section '{section}'. Valid: {sorted(valid_sections)}",
            ),
        )

    if not patches:
        return ToolResult(
            success=False,
            error=ToolError(error_type="validation", message="patches list is empty."),
        )

    for i, p in enumerate(patches):
        if "old_string" not in p or "new_string" not in p:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"Patch {i} is missing 'old_string' or 'new_string'.",
                ),
            )

    try:
        ToolUi = get_db_model("ToolUi")
        comp_row = await ToolUi.get_or_none(id=component_id)

        if not comp_row:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found", message=f"Component '{component_id}' not found."
                ),
            )

        comp = _row_dict(comp_row, ("id", section, "semver"))
        code = comp.get(section) or ""

        if not code:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="validation",
                    message=f"Section '{section}' is empty. Nothing to patch.",
                    suggested_action="Use toolcomp_update_code to write the initial code first.",
                ),
            )

        patch_results: list[dict[str, Any]] = []
        working_code = code

        for i, patch in enumerate(patches):
            old_str = patch["old_string"]
            new_str = patch["new_string"]
            description = patch.get("description", f"patch {i + 1}")

            try:
                working_code, round_used = _apply_patch(working_code, old_str, new_str)
                patch_results.append(
                    {
                        "index": i,
                        "description": description,
                        "status": "applied",
                        "match_round": round_used,
                    }
                )
            except ValueError as ve:
                return ToolResult(
                    success=False,
                    error=ToolError.from_exception(
                        ve,
                        error_type="patch_no_match",
                        message=f"Patch {i} ('{description}') failed: {ve}",
                        suggested_action=(
                            "Fetch the current code with toolcomp_get_code and verify your "
                            "old_string exactly matches a contiguous substring. "
                            "Avoid including surrounding indentation that may differ."
                        ),
                    ),
                    output={
                        "patches_applied_before_failure": len(patch_results),
                        "failed_patch_index": i,
                        "failed_patch_description": description,
                        "old_string_preview": old_str[:300],
                        "patch_results_so_far": patch_results,
                    },
                )

        update_payload: dict[str, Any] = {section: working_code}

        # bump_version advances the human-facing semver (TEXT). The integer
        # `version` is DB-trigger-managed and must never be written here.
        if bump_version:
            update_payload["semver"] = _bump_semver_patch(comp.get("semver"))

        if notes:
            update_payload["notes"] = notes

        await ToolUi.update_where({"id": component_id}, **update_payload)
        updated_row = await ToolUi.get_or_none(id=component_id)
        updated = _row_dict(updated_row, ("semver", "version", "updated_at")) if updated_row else {}

        return ToolResult(
            success=True,
            output=ToolComponentPatchResult(
                component_id=component_id,
                section=section,
                patches_applied=len(patches),
                patch_results=patch_results,
                semver=updated.get("semver"),  # human-facing version label
                version=updated.get("version"),  # DB-managed integer revision (auto-bumped)
                updated_at=updated.get("updated_at"),
                message=f"Applied {len(patches)} patch(es) to '{section}'.",
            ),
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution", message=str(e), traceback=traceback.format_exc()
            ),
        )
