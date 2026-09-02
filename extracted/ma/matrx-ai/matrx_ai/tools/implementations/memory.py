from __future__ import annotations

import logging
import time
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic import ValidationError

from matrx_ai.db.ownership_fields import stamp_org_id, stamp_row_owner
from matrx_ai.persistence import (
    queue_agent_memory_create,
    queue_agent_memory_delete,
    queue_agent_memory_update,
    standalone_coordinator,
)
from matrx_ai.tools._dispatch_util import format_args_error
from matrx_ai.tools.arg_models.memory_args import (
    MemoryArgs,
    MemoryForgetArgs,
    MemoryRecallArgs,
    MemorySearchArgs,
    MemoryStoreArgs,
    MemoryUpdateArgs,
)
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

logger = logging.getLogger(__name__)


class _LazyCxm:
    """Lazy proxy for the ``cxm`` manager bundle.

    Importing ``cxm`` at module scope resolves DB-backed managers, which raise
    ``DBNotConfiguredError`` when ``matrx_ai.configure()`` hasn't run yet — so a
    bare ``import ...memory`` used to touch the DB registry at IMPORT time. This
    proxy defers that resolution to first ATTRIBUTE ACCESS (call time), keeping
    the module import side-effect-free while every ``cxm.<manager>`` call site
    stays unchanged.
    """

    def __getattr__(self, name: str) -> Any:
        from matrx_ai.db import cxm as _cxm

        return getattr(_cxm, name)


cxm = _LazyCxm()

EXPIRY_MAP = {
    "short": timedelta(hours=1),
    "medium": timedelta(days=7),
    "long": None,
}


def _scope_id(ctx: ToolContext, scope: str) -> str | None:
    if scope == "project":
        return ctx.project_id
    if scope == "organization":
        return ctx.organization_id
    return None


async def memory_store(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = MemoryStoreArgs(**args)

    try:
        expires_delta = EXPIRY_MAP.get(parsed.memory_type)
        expires_at = (datetime.now(UTC) + expires_delta).isoformat() if expires_delta else None

        filters = {
            "created_by": ctx.user_id,
            "scope": parsed.scope,
            "key": parsed.key,
        }
        scope_id = _scope_id(ctx, parsed.scope)
        if scope_id:
            filters["scope_id"] = scope_id

        existing = await cxm.agent_memory.filter_agent_memories(**filters)

        data: dict[str, Any] = {
            "memory_type": parsed.memory_type,
            "scope": parsed.scope,
            "scope_id": scope_id,
            "key": parsed.key,
            "content": parsed.content,
            "importance": parsed.importance,
            "expires_at": expires_at,
            "updated_at": datetime.now(UTC).isoformat(),
        }
        stamp_row_owner(data, ctx.user_id)
        # Default row attribution to the request's active org (same contract as
        # conversation_gate / queue_helpers) rather than falling through to the
        # DB backstop's personal-org default. For scope="organization", the row's
        # organization_id must match the semantic target org (scope_id) — never
        # split-brained between "what this memory is about" and "who owns the row".
        if parsed.scope == "organization" and scope_id:
            data["organization_id"] = scope_id
        else:
            stamp_org_id(data, ctx.organization_id)

        if existing:
            queue_agent_memory_update(existing[0].id, **data)
        else:
            # CxAgentMemory.id has no DB-side UUID default, so the insert must
            # carry an explicit primary key — otherwise the ORM Session refuses
            # to queue the op ("Cannot queue ... without a primary key value").
            data["id"] = str(uuid.uuid4())
            data["created_at"] = datetime.now(UTC).isoformat()
            data["access_count"] = 0
            queue_agent_memory_create(**data)

        return ToolResult(
            success=True,
            output={"stored": True, "key": parsed.key, "type": parsed.memory_type},
            started_at=started_at,
            completed_at=time.time(),
            tool_name="memory_store",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="database", message=f"Memory store failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="memory_store",
            call_id=ctx.call_id,
        )


async def memory_recall(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = MemoryRecallArgs(**args)

    try:
        filters: dict[str, Any] = {"created_by": ctx.user_id, "scope": parsed.scope}
        if parsed.key:
            filters["key"] = parsed.key
        if parsed.memory_type:
            filters["memory_type"] = parsed.memory_type
        scope_id = _scope_id(ctx, parsed.scope)
        if scope_id:
            filters["scope_id"] = scope_id

        items = await cxm.agent_memory.filter_agent_memories(**filters)

        # Sort by importance desc, then recency, and apply limit
        items_sorted = sorted(
            items,
            key=lambda m: (-(m.importance or 0), m.updated_at or ""),
            reverse=False,
        )
        limited = items_sorted[: parsed.limit] if parsed.limit else items_sorted

        memories = [item.to_dict() for item in limited]

        # Fire-and-forget: bump access counts. Each detached task owns an
        # isolated Coordinator because detached tasks deliberately inherit no
        # request lane or write owner.

        async def _bump_access(mem_id: str, new_count: int) -> None:
            try:
                async with standalone_coordinator(
                    reason="agent_memory_access_count",
                    user_id=getattr(ctx, "user_id", None),
                ):
                    queue_agent_memory_update(
                        mem_id,
                        access_count=new_count,
                        last_accessed_at=datetime.now(UTC).isoformat(),
                    )
            except Exception as exc:
                from matrx_connect.streaming.error_capture import capture_error

                await capture_error(
                    exc,
                    kind="agent_memory_persistence_failed",
                    route="memory_recall/access_count",
                    error_type=type(exc).__name__,
                    payload={"memory_id": mem_id, "new_count": new_count},
                )

        from matrx_utils import detached_task
        for item in limited:
            detached_task(
                _bump_access(item.id, (item.access_count or 0) + 1),
                name=f"memory_access_count:{item.id}",
            )

        return ToolResult(
            success=True,
            output={"memories": memories, "count": len(memories)},
            started_at=started_at,
            completed_at=time.time(),
            tool_name="memory_recall",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="database", message=f"Memory recall failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="memory_recall",
            call_id=ctx.call_id,
        )


async def memory_search(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = MemorySearchArgs(**args)

    try:
        # Load all memories for this user/scope and do in-process substring search.
        # A proper full-text search (pg_trgm / vector) can replace this later.
        filters: dict[str, Any] = {"created_by": ctx.user_id, "scope": parsed.scope}
        if parsed.memory_type:
            filters["memory_type"] = parsed.memory_type
        scope_id = _scope_id(ctx, parsed.scope)
        if scope_id:
            filters["scope_id"] = scope_id

        all_items = await cxm.agent_memory.filter_agent_memories(**filters)

        query_lower = parsed.query.lower()
        matched = [
            item
            for item in all_items
            if query_lower in (item.content or "").lower()
            or query_lower in (item.key or "").lower()
        ]

        limited = matched[: parsed.limit] if parsed.limit else matched
        results = [item.to_dict() for item in limited]

        return ToolResult(
            success=True,
            output={"results": results, "count": len(results)},
            started_at=started_at,
            completed_at=time.time(),
            tool_name="memory_search",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="database", message=f"Memory search failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="memory_search",
            call_id=ctx.call_id,
        )


async def memory_update(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = MemoryUpdateArgs(**args)

    try:
        filters: dict[str, Any] = {
            "created_by": ctx.user_id,
            "scope": parsed.scope,
            "key": parsed.key,
        }
        scope_id = _scope_id(ctx, parsed.scope)
        if scope_id:
            filters["scope_id"] = scope_id

        existing = await cxm.agent_memory.filter_agent_memories(**filters)

        if not existing:
            return ToolResult(
                success=False,
                error=ToolError(
                    error_type="not_found",
                    message=f"Memory with key '{parsed.key}' not found.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="memory_update",
                call_id=ctx.call_id,
            )

        update_data: dict[str, Any] = {
            "content": parsed.content,
            "updated_at": datetime.now(UTC).isoformat(),
        }
        if parsed.importance is not None:
            update_data["importance"] = parsed.importance

        queue_agent_memory_update(existing[0].id, **update_data)

        return ToolResult(
            success=True,
            output={"updated": 1, "key": parsed.key},
            started_at=started_at,
            completed_at=time.time(),
            tool_name="memory_update",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="database", message=f"Memory update failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="memory_update",
            call_id=ctx.call_id,
        )


async def memory_forget(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = MemoryForgetArgs(**args)

    try:
        filters: dict[str, Any] = {
            "created_by": ctx.user_id,
            "scope": parsed.scope,
            "key": parsed.key,
        }
        scope_id = _scope_id(ctx, parsed.scope)
        if scope_id:
            filters["scope_id"] = scope_id

        existing = await cxm.agent_memory.filter_agent_memories(**filters)

        deleted = 0
        for item in existing:
            if queue_agent_memory_delete(item.id):
                deleted += 1

        return ToolResult(
            success=True,
            output={"deleted": deleted, "key": parsed.key},
            started_at=started_at,
            completed_at=time.time(),
            tool_name="memory_forget",
            call_id=ctx.call_id,
        )
    except Exception as exc:
        return ToolResult(
            success=False,
            error=ToolError.from_exception(
                exc,error_type="database", message=f"Memory forget failed: {exc}"),
            started_at=started_at,
            completed_at=time.time(),
            tool_name="memory_forget",
            call_id=ctx.call_id,
        )


# ---------------------------------------------------------------------------
# memory — unified action dispatcher
# ---------------------------------------------------------------------------

# Valid `memory` actions are enforced by the MemoryArgs discriminated union
# (arg_models/memory_args.py) + tool_def.parameters."$variants" — the source of truth.


def _memory_stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "memory"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _memory_validation_error(message: str, started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type="validation", message=message),
        started_at=started_at,
        completed_at=time.time(),
        tool_name="memory",
        call_id=ctx.call_id,
    )


async def memory(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    # The executor already validated `args` against MemoryArgs (the discriminated
    # union) before dispatch; re-derive the typed variant so the body is bound to
    # the per-action contract the drift gate proves against the DB.
    try:
        parsed = MemoryArgs.model_validate(args).root
    except ValidationError as exc:
        return _memory_validation_error(format_args_error(exc), started_at, ctx)

    action = parsed.action
    # exclude_unset: pass only the keys the caller actually sent (so worker
    # partial-update semantics are unchanged — no materialised defaults leak in).
    inner_args = parsed.model_dump(exclude={"action"}, exclude_unset=True)

    # store does not accept scope=conversation — it has no durable home.
    if action == "store" and inner_args.get("scope") == "conversation":
        return _memory_validation_error(
            "scope='conversation' is not valid for store. Use 'user', 'project', or 'organization'.",
            started_at,
            ctx,
        )

    impl = {
        "recall": memory_recall,
        "search": memory_search,
        "store": memory_store,
        "update": memory_update,
        "forget": memory_forget,
    }[action]

    return _memory_stamp(await impl(inner_args, ctx), started_at, ctx)
