from __future__ import annotations

import logging
import re
import time
import uuid
from datetime import UTC, datetime, timedelta
from typing import Any

from pydantic import ValidationError

from matrx_ai.db.ownership_fields import stamp_org_id, stamp_row_owner
from matrx_ai.persistence import (
    queue_agent_memory_create,
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


def _is_live(row: Any) -> bool:
    return getattr(row, "deleted_at", None) is None


async def _live_memories(**filters: Any) -> list[Any]:
    # forget ARCHIVES (deleted_at) — every read sees live memories only.
    return [m for m in await cxm.agent_memory.filter_agent_memories(**filters) if _is_live(m)]


def _loose(key: Any) -> str:
    """A key with spaces, underscores, hyphens and dots all alike and case ignored — how a person or model retypes one."""
    return re.sub(r"[\s_.\-]+", "_", str(key or "")).strip("_").lower()


class _KeyMatch:
    """The ONE answer to "which memory does this key name?": ``rows`` (exact stored key first, else the single
    loose match) or ``ambiguous`` (the stored keys when several match loosely)."""

    def __init__(self, rows: list[Any], ambiguous: list[str]) -> None:
        self.rows = rows
        self.ambiguous = ambiguous


async def _resolve_key(key: str, **filters: Any) -> _KeyMatch:
    """Every action that takes a key (recall, update, forget, store) resolves it here (2026-11-17: a retyped
    key returned not_found; store made a duplicate). Two loose matches are ambiguous, never a guess about
    what to change or archive: the caller says so and lists the stored keys."""
    exact = await _live_memories(key=key, **filters)
    if exact:
        return _KeyMatch(exact, [])
    wanted = _loose(key)
    loose = [m for m in await _live_memories(**filters) if _loose(getattr(m, "key", "")) == wanted]
    if len(loose) == 1:
        return _KeyMatch(loose, [])
    return _KeyMatch([], sorted(str(getattr(m, "key", "")) for m in loose))


def _bad_key_result(tool: str, key: str, started_at: float, ctx: ToolContext) -> ToolResult | None:
    """A key made only of separators names nothing; refuse it rather than match a stored "_"."""
    if _loose(key):
        return None
    return ToolResult(
        success=False,
        error=ToolError(
            refusal=True,
            error_type="invalid_key",
            message=f"Memory key {key!r} has no letters or digits. Use a key such as 'preferred_airline'.",
        ),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool,
        call_id=ctx.call_id,
    )


def _key_note(typed: str, stored: str) -> dict[str, str]:
    """Said whenever the stored key differs from the one typed (the stored key is the one to use next time)."""
    if typed == stored:
        return {}
    return {"typed_key": typed, "note": f"'{typed}' matched the stored key '{stored}'; use '{stored}' from now on."}


def _ambiguous_key_result(tool: str, key: str, keys: list[str], started_at: float, ctx: ToolContext) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(
            refusal=True,
            error_type="ambiguous_key",
            message=(
                f"Memory key '{key}' matches more than one stored memory: {', '.join(repr(k) for k in keys)}. "
                "Nothing was changed. Call again with one of these exact keys."
            ),
        ),
        started_at=started_at,
        completed_at=time.time(),
        tool_name=tool,
        call_id=ctx.call_id,
    )


async def memory_store(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started_at = time.time()
    parsed = MemoryStoreArgs(**args)
    if bad := _bad_key_result("memory_store", parsed.key, started_at, ctx):
        return bad

    try:
        expires_delta = EXPIRY_MAP.get(parsed.memory_type)
        expires_at = (datetime.now(UTC) + expires_delta).isoformat() if expires_delta else None

        filters: dict[str, Any] = {"created_by": ctx.user_id, "scope": parsed.scope}
        scope_id = _scope_id(ctx, parsed.scope)
        if scope_id:
            filters["scope_id"] = scope_id

        match = await _resolve_key(parsed.key, **filters)
        if match.ambiguous:
            return _ambiguous_key_result("memory_store", parsed.key, match.ambiguous, started_at, ctx)
        existing = match.rows
        # A key that loosely names a live memory updates THAT memory under its stored key (no duplicate).
        stored_key = str(existing[0].key) if existing else parsed.key
        # A forgotten memory keeps its row (archived) and the key stays unique
        # per (created_by, scope, scope_id, key) — storing the key again
        # REVIVES that row instead of colliding with it.
        archived = (
            []
            if existing
            # include-archived: storing a forgotten key revives its archived row (names deleted_at → reads archived)
            else [
                m
                for m in await cxm.agent_memory.filter_agent_memories(key=parsed.key, deleted_at__isnull=False, **filters)
                if not _is_live(m)
            ]
        )

        data: dict[str, Any] = {
            "memory_type": parsed.memory_type,
            "scope": parsed.scope,
            "scope_id": scope_id,
            "key": stored_key,
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
        elif archived:
            queue_agent_memory_update(archived[0].id, **data, deleted_at=None)
        else:
            # CxAgentMemory.id has no DB-side UUID default, so the insert must
            # carry an explicit primary key — otherwise the ORM Session refuses
            # to queue the op ("Cannot queue ... without a primary key value").
            data["id"] = str(uuid.uuid4())
            data["created_at"] = datetime.now(UTC).isoformat()
            data["access_count"] = 0
            queue_agent_memory_create(**data)

        result = ToolResult(
            success=True,
            output={
                "stored": True,
                "key": stored_key,
                "type": parsed.memory_type,
                **({"updated_existing": True} if existing else {}),
                **({"merged_into_existing": True, **_key_note(parsed.key, stored_key)} if existing and stored_key != parsed.key else {}),
            },
            started_at=started_at,
            completed_at=time.time(),
            tool_name="memory_store",
            call_id=ctx.call_id,
        )
        if not existing:
            return result  # a new memory: nothing was replaced
        # store UPSERTS by key: an existing memory's text was replaced, so the
        # card shows what it said before (verifier round 2, proved live).
        from matrx_ai.tools.surface_write import attach_surface_write

        return attach_surface_write(
            result,
            before=str(getattr(existing[0], "content", "") or ""),
            after=str(parsed.content or ""),
            target_type="memory",
            target_id=str(existing[0].id),
            target_label=f"Memory · {stored_key}",
            mode="overwrite",
            content_format="markdown",
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
    if parsed.key and (bad := _bad_key_result("memory_recall", parsed.key, started_at, ctx)):
        return bad

    try:
        filters: dict[str, Any] = {"created_by": ctx.user_id, "scope": parsed.scope}
        if parsed.memory_type:
            filters["memory_type"] = parsed.memory_type
        scope_id = _scope_id(ctx, parsed.scope)
        if scope_id:
            filters["scope_id"] = scope_id

        if parsed.key:
            match = await _resolve_key(parsed.key, **filters)
            if match.ambiguous:
                return _ambiguous_key_result("memory_recall", parsed.key, match.ambiguous, started_at, ctx)
            items = match.rows
        else:
            items = await _live_memories(**filters)

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

        # ToolContext exposes request identity through the ambient AppContext.
        # Detached tasks deliberately do not retain that ContextVar, so capture
        # the identity while the tool invocation is still inside its request.
        memory_owner_id = ctx.user_id

        async def _bump_access(
            mem_id: str, new_count: int, *, user_id: str
        ) -> None:
            try:
                async with standalone_coordinator(
                    reason="agent_memory_access_count",
                    user_id=user_id,
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
                _bump_access(
                    item.id,
                    (item.access_count or 0) + 1,
                    user_id=memory_owner_id,
                ),
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

        all_items = await _live_memories(**filters)

        query_lower = parsed.query.lower()
        matched = [
            item
            for item in all_items
            if query_lower in (item.content or "").lower()
            or query_lower in (item.key or "").lower()
            or (_loose(parsed.query) and _loose(parsed.query) in _loose(item.key))
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
    if bad := _bad_key_result("memory_update", parsed.key, started_at, ctx):
        return bad

    try:
        filters: dict[str, Any] = {
            "created_by": ctx.user_id,
            "scope": parsed.scope,
        }
        scope_id = _scope_id(ctx, parsed.scope)
        if scope_id:
            filters["scope_id"] = scope_id

        match = await _resolve_key(parsed.key, **filters)
        if match.ambiguous:
            return _ambiguous_key_result("memory_update", parsed.key, match.ambiguous, started_at, ctx)
        existing = match.rows

        if not existing:
            return ToolResult(
                success=False,
                error=ToolError(
                    refusal=True,
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
        stored_key = str(existing[0].key)

        from matrx_ai.tools.surface_write import attach_surface_write

        return attach_surface_write(
            ToolResult(
                success=True,
                output={"updated": 1, "key": stored_key, **_key_note(parsed.key, stored_key)},
                started_at=started_at,
                completed_at=time.time(),
                tool_name="memory_update",
                call_id=ctx.call_id,
            ),
            before=str(getattr(existing[0], "content", "") or ""),
            after=str(parsed.content or ""),
            target_type="memory",
            target_id=str(existing[0].id),
            target_label=f"Memory · {stored_key}",
            mode="overwrite",
            content_format="markdown",
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
    if bad := _bad_key_result("memory_forget", parsed.key, started_at, ctx):
        return bad

    try:
        filters: dict[str, Any] = {
            "created_by": ctx.user_id,
            "scope": parsed.scope,
        }
        scope_id = _scope_id(ctx, parsed.scope)
        if scope_id:
            filters["scope_id"] = scope_id

        match = await _resolve_key(parsed.key, **filters)
        if match.ambiguous:
            return _ambiguous_key_result("memory_forget", parsed.key, match.ambiguous, started_at, ctx)
        existing = match.rows

        if not existing:
            return ToolResult(
                success=False,
                error=ToolError(
                    refusal=True,
                    error_type="not_found",
                    message=f"Memory with key '{parsed.key}' not found. Nothing was forgotten.",
                ),
                started_at=started_at,
                completed_at=time.time(),
                tool_name="memory_forget",
                call_id=ctx.call_id,
            )
        stored_key = str(existing[0].key)
        deleted = 0
        now = datetime.now(UTC).isoformat()
        for item in existing:
            # Archive, never remove: the row keeps deleted_at and every read skips it.
            if queue_agent_memory_update(item.id, deleted_at=now, updated_at=now):
                deleted += 1

        return ToolResult(
            success=True,
            output={"deleted": deleted, "archived": deleted, "key": stored_key, **_key_note(parsed.key, stored_key)},
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


#: Actions that SAVE (the person's memory changes); the rest only read it.
_WRITING_ACTIONS = frozenset({"store", "update", "forget"})


def person_memory_refusal(action: str) -> str | None:
    """Why this turn may not use the memory tool, else ``None`` (CGU-10, ``config/person_context.py``).

    A confidential chat never reads or writes memory; a temporary chat never SAVES one, and reads only
    when the person opted in for the turn. The words are what the model reads back."""
    from matrx_ai.config.person_context import person_context_decision
    from matrx_ai.context.app_context import try_get_app_context

    app = try_get_app_context()
    if app is None:
        return None
    if getattr(app, "sealed_conversation_id", None):
        return "This is a confidential chat: memory is not read or saved here."
    if not getattr(app, "store", True):
        if action in _WRITING_ACTIONS:
            return "This is a temporary chat: nothing is saved to memory from it."
        allowed, _why = person_context_decision(app)
        if not allowed:
            return "This is a temporary chat and the person did not turn memory on for it."
    return None


def _memory_stamp(result: ToolResult, started_at: float, ctx: ToolContext) -> ToolResult:
    result.tool_name = "memory"
    result.call_id = ctx.call_id
    if not result.started_at:
        result.started_at = started_at
    if not result.completed_at:
        result.completed_at = time.time()
    return result


def _memory_validation_error(message: str, started_at: float, ctx: ToolContext, *, exc: BaseException | None = None) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError.declared("validation", message, exc=exc),
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
        return _memory_validation_error(format_args_error(exc), started_at, ctx, exc=exc)

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

    refusal = person_memory_refusal(action)
    if refusal:
        return _memory_stamp(
            ToolResult(success=False, error=ToolError.declared("person_memory_off", refusal), started_at=started_at),
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
