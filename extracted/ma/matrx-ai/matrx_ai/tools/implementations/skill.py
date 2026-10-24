"""Skill tools — the unified action-dispatched ``skill`` tool.

The agent-facing entry point for the skills system. A single ``skill`` tool
dispatches on ``action`` (``list`` / ``get`` / ``search``) to the internal
helpers below, following the unified tool dispatch contract:
``async def f(args, ctx) -> ToolResult``. This replaced the legacy per-operation
skill_list / skill_get / skill_search tools (migration 0100), matching the
note/memory/task grouped-tool pattern.

A1: results land in conversation history as tool-result messages — NEVER
edited into the system prompt mid-flight.
"""

from __future__ import annotations

import time
import traceback
from typing import Any
from uuid import UUID

from pydantic import ValidationError

from matrx_ai.skills.knobs import get_outline_rows, outline_min_chars
from matrx_ai.skills.sections import (
    SkillSection,
    find_section,
    next_section,
    parse_sections,
    section_text,
)
from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models import SkillArgs
from matrx_ai.tools.models import (
    ToolContext,
    ToolError,
    ToolResult,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _err(error_type: str, message: str, suggested: str | None = None) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            error_type=error_type,
            message=message,
            suggested_action=suggested,
        ),
    )


def _parse_uuid(value: Any) -> UUID | None:
    if isinstance(value, UUID):
        return value
    if isinstance(value, str) and value:
        try:
            return UUID(value)
        except ValueError:
            return None
    return None


def _user_id_from_ctx(ctx: ToolContext) -> UUID | None:
    try:
        from matrx_connect import get_app_context

        app_ctx = get_app_context()
    except Exception:
        return None
    raw = getattr(app_ctx, "user_id", None)
    return _parse_uuid(raw)


async def _provider() -> Any:
    # Lazy import so the package boots in environments where matrx-orm
    # managers aren't wired in (e.g. matrx-ai unit tests). The provider's
    # own lazy imports fall back to direct manager imports.
    from matrx_ai.skills.providers import DbSkillProvider

    return DbSkillProvider()


def _agent_skill_config(ctx: ToolContext) -> Any:
    """Pull the active agent's SkillConfig off AppContext.metadata if present.

    The request-prep helper (``apply_unified_skills``) stores the resolved
    SkillConfig under ``metadata['skill_config']`` so tool calls can honor
    the forbidden tier without re-querying the DB. Returns None when the
    helper hasn't run (e.g. legacy routes that haven't been wired yet).
    """
    try:
        from matrx_connect import get_app_context

        app_ctx = get_app_context()
    except Exception:
        return None
    md = getattr(app_ctx, "metadata", None)
    if not isinstance(md, dict):
        return None
    return md.get("skill_config")


def _is_forbidden(skill_uuid: UUID, config: Any) -> bool:
    if config is None:
        return False
    try:
        return config.is_forbidden(skill_uuid)
    except Exception:
        return False


# ---------------------------------------------------------------------------
# skill_list
# ---------------------------------------------------------------------------


async def skill_list(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    try:
        category: str | None = args.get("category")
        limit_raw = args.get("limit", 50)
        try:
            limit = int(limit_raw)
        except (TypeError, ValueError):
            limit = 50
        if limit <= 0:
            limit = 50
        if limit > 200:
            limit = 200

        provider = await _provider()
        user_id = _user_id_from_ctx(ctx)
        config = _agent_skill_config(ctx)

        if not category:
            overview = await provider.category_overview(user_id=user_id)
            return ToolResult(
                success=True,
                output={
                    "categories": [
                        {"category_key": k, "description": d, "active_count": c}
                        for k, d, c in overview
                    ],
                    "total_active": sum(c for _, _, c in overview),
                    "hint": (
                        "Call skill(action='list', category=<category_key>) to see "
                        "skill hints within a category, or skill(action='search', "
                        "query=...) to query."
                    ),
                },
            )

        hints = await provider.list_hints(user_id=user_id, category_key=category, limit=limit)
        visible = [h for h in hints if not _is_forbidden(h.id, config)]
        return ToolResult(
            success=True,
            output={
                "category": category,
                "count": len(visible),
                "hints": [h.model_dump(mode="json") for h in visible],
            },
        )

    except Exception as e:
        return _err(
            "execution",
            f"skill_list failed: {e}",
        )


# ---------------------------------------------------------------------------
# skill_get
# ---------------------------------------------------------------------------

_VALID_GET_MODES = frozenset({"auto", "full", "page"})
# Page size = agents.context.skill_outline_min_chars; outline rows = agents.context.skill_get_outline_rows
# (a 137k-char reference has hundreds of headings). Both knobs: matrx_ai.skills.knobs.


def _outline_fields(sections: list[SkillSection]) -> dict[str, Any]:
    max_rows = get_outline_rows()
    rows = [s.outline_entry() for s in sections[:max_rows]]
    return {
        "outline": rows,
        "outline_truncated": len(sections) > max_rows,
        "section_count": len(sections),
    }


def _read_section(
    body: str, sections: list[SkillSection], section: SkillSection, offset: int, chars: int
) -> dict[str, Any]:
    """One section's text (incl. subsections), paged by offset/chars when it is huge."""
    text = section_text(body, section)
    piece = text[offset : offset + chars]
    has_more = (offset + chars) < len(text)
    following = next_section(sections, section)
    return {
        "section": section.outline_entry(),
        "body": piece,
        "offset": offset,
        "chars_returned": len(piece),
        "has_more": has_more,
        "next_offset": offset + chars if has_more else None,
        "next_section_id": following.id if following else None,
    }


def _section_result(
    body: Any, common: dict[str, Any], handle: str, offset: int, chars: int
) -> ToolResult:
    sections = parse_sections(body.body)
    found = find_section(sections, handle)
    if found is None:
        known = ", ".join(f"{s.number} {s.id}" for s in sections[:40]) or "none (no headings)"
        return _err(
            "not_found",
            f"Section {handle!r} not found in skill {body.skill_id!r}.",
            f"Pass a section number or id from the outline. Sections: {known}",
        )
    return ToolResult(
        success=True,
        output={
            **common,
            **_outline_fields(sections),
            **_read_section(body.body, sections, found, offset, chars),
            "mode": "section",
            "total_chars": len(body.body),
        },
        output_kind="skill_tool_result",
    )


async def _set_result(
    body: Any, common: dict[str, Any], provider: Any, user_id: UUID | None, config: Any
) -> ToolResult:
    """A skill SET reads as its member list — each member is then read by its own id."""
    members: list[dict[str, Any]] = []
    skipped = 0  # members that are forbidden, deleted or not readable by this person
    for member_id in body.set_members:
        if _is_forbidden(member_id, config):
            skipped += 1
            continue
        member = await provider.get_by_id(member_id, user_id=user_id)
        if member is None:
            skipped += 1
            continue
        members.append(
            {
                "id": str(member.id),
                "skill_id": member.skill_id,
                "label": member.label,
                "description": member.description,
                "skill_type": member.skill_type,
                "total_chars": len(member.body),
            }
        )
    return ToolResult(
        success=True,
        output={
            **common,
            "mode": "set",
            "body": body.body,
            "members": members,
            "count": len(members),
            "skipped": skipped,
            "hint": "A skill set. Read a member with skill(action='get', skill_id=<member skill_id>).",
        },
        output_kind="skill_tool_result",
    )


async def skill_get(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    try:
        raw_id = args.get("skill_id") or args.get("id")
        if not raw_id:
            return _err(
                "validation",
                "skill_id is required.",
                "Pass either the UUID or the human-readable skill_id business key.",
            )

        skill_uuid = _parse_uuid(raw_id)

        provider = await _provider()
        user_id = _user_id_from_ctx(ctx)
        config = _agent_skill_config(ctx)

        # Look up by UUID first; if that fails, try resolving by business key.
        body = None
        if skill_uuid is not None:
            body = await provider.get_by_id(skill_uuid, user_id=user_id)
        if body is None and isinstance(raw_id, str):
            # Fallback: look up by skill_id (the human key) via the manager.
            try:
                from matrx_ai.db._registry import get_instance

                mgr = get_instance("skl_definitions_manager")
                matches = await mgr.filter_items(skill_id=raw_id, is_active=True)
                if matches:
                    body = await provider.get_by_id(UUID(str(matches[0].id)), user_id=user_id)
            except Exception:
                pass

        if body is None:
            return _err(
                "not_found",
                f"Skill {raw_id!r} not found or not visible to this user.",
                "Use skill(action='list') or skill(action='search') to find a skill_id you can read.",
            )

        if _is_forbidden(body.id, config):
            return _err(
                "forbidden",
                f"Skill {body.skill_id!r} is on the forbidden list for this agent.",
                "The agent's configuration explicitly hides this skill.",
            )

        mode: str = args.get("mode") or "auto"
        if mode not in _VALID_GET_MODES:
            return _err(
                "validation",
                f"Invalid mode {mode!r}. Use one of {sorted(_VALID_GET_MODES)}.",
            )

        offset = max(0, int(args.get("offset", 0) or 0))
        default_page = outline_min_chars()
        chars = int(args.get("chars", default_page) or default_page)
        if chars <= 0:
            chars = default_page

        common: dict[str, Any] = {
            "id": str(body.id),
            "skill_id": body.skill_id,
            "label": body.label,
            "description": body.description,
            "skill_type": body.skill_type,
            "category_path": body.category_path,
            "version": body.version,
            "allowed_tools": [str(u) for u in body.allowed_tools],
            "disable_auto_invocation": body.disable_auto_invocation,
            "trigger_patterns": body.trigger_patterns,
            "not_runnable": body.not_runnable,
        }

        if body.is_set:
            return await _set_result(body, common, provider, user_id, config)

        section_arg = args.get("section")
        if isinstance(section_arg, str) and section_arg.strip():
            return _section_result(body, common, section_arg, offset, chars)

        total = len(body.body)
        # Outline-by-default is for REFERENCE documents only: a procedure, task or convention
        # skill is read whole (a truncated procedure is acted on as if complete).
        if mode == "full" or (mode == "auto" and (total <= chars or body.skill_type != "reference")):
            return ToolResult(
                success=True,
                output={**common, "mode": "full", "body": body.body, "total_chars": total},
            )

        if mode == "auto":
            sections = parse_sections(body.body)
            if len(sections) >= 2:
                # A long document: its map plus the opening section (paged when huge).
                out = _read_section(body.body, sections, sections[0], 0, chars)
                return ToolResult(
                    success=True,
                    output={
                        **common,
                        **_outline_fields(sections),
                        **out,
                        "mode": "outline",
                        "total_chars": total,
                        "hint": (
                            "Long document: the outline lists every section. Read one with "
                            "skill(action='get', skill_id=..., section=<number or id>)."
                        ),
                    },
                    output_kind="skill_tool_result",
                )
            # No headings to navigate by — fall through to plain paging.

        slice_text = body.body[offset : offset + chars]
        has_more = (offset + chars) < total
        return ToolResult(
            success=True,
            output={
                **common,
                "mode": "page",
                "body": slice_text,
                "offset": offset,
                "chars_returned": len(slice_text),
                "total_chars": total,
                "has_more": has_more,
                "next_offset": offset + chars if has_more else None,
            },
        )

    except Exception as e:
        return ToolResult(
            success=False,
            error=ToolError(
                error_type="execution",
                message=f"skill_get failed: {e}",
                traceback=traceback.format_exc(),
                is_retryable=False,
            ),
        )


# ---------------------------------------------------------------------------
# skill_search
# ---------------------------------------------------------------------------


async def skill_search(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    try:
        query = (args.get("query") or "").strip()
        if not query:
            return _err(
                "validation",
                "query is required.",
                "Pass a non-empty keyword string. Searches name, description, body.",
            )

        category: str | None = args.get("category")
        limit_raw = args.get("limit", 10)
        try:
            limit = int(limit_raw)
        except (TypeError, ValueError):
            limit = 10
        if limit <= 0:
            limit = 10
        if limit > 50:
            limit = 50

        provider = await _provider()
        user_id = _user_id_from_ctx(ctx)
        config = _agent_skill_config(ctx)

        hints = await provider.search(
            query, category_key=category, user_id=user_id, limit=limit * 2
        )
        visible = [h for h in hints if not _is_forbidden(h.id, config)][:limit]

        return ToolResult(
            success=True,
            output={
                "query": query,
                "category": category,
                "count": len(visible),
                "hints": [h.model_dump(mode="json") for h in visible],
            },
        )

    except Exception as e:
        return _err("execution", f"skill_search failed: {e}")


# ---------------------------------------------------------------------------
# skill — the unified action-dispatched tool (list | get | search)
# ---------------------------------------------------------------------------


def _skill_stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "skill"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _skill_validation_error(message: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="validation", message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="skill",
        call_id=ctx.call_id,
    )


async def skill(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    """Unified skill-library tool. Dispatches on ``action``:

    - ``list``   → browse the category overview, or hints within a category
    - ``get``    → read one skill by id: a short body whole; a long document as its outline
      + first section; ``section=`` for exactly one section; modes full / page; a set → members
    - ``search`` → keyword search across skills
    """
    started_at = time.time()
    try:
        parsed = SkillArgs.model_validate(args).root
    except ValidationError as exc:
        return _skill_validation_error(format_args_error(exc), started_at, ctx)

    action = parsed.action
    inner_args = parsed.model_dump(exclude={"action"}, exclude_unset=True)

    impl = {
        "list": skill_list,
        "get": skill_get,
        "search": skill_search,
    }[action]

    from matrx_ai.tools.kind_stamp import stamp_result_kind
    from matrx_ai.tools.kinds.workbench import SkillToolResult

    return stamp_result_kind(
        _skill_stamp(await impl(inner_args, ctx), started_at, ctx), SkillToolResult
    )
