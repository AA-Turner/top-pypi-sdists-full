"""``dictionary`` — agent-callable handler for the Custom Dictionary system.

One multi-action tool (the house pattern) that lets a dictionary-assistant agent
read and write terminology + pronunciation entries at any of the four owner
levels (user / organization / scope_type / scope), discover what the user can
attach to, resolve a merged dictionary, and mine the user's recent conversations
and notes for candidate terms.

All authorization lives in the DB: the tool calls the ``dict_*_for(p_user_id,…)``
inner functions over the matrx-orm connection (this process has no ``auth.uid()``),
passing the authenticated ``ctx.user_id``. Those functions enforce org membership
and personal-dictionary privacy and raise on violations.
"""

from __future__ import annotations

import json
import logging
import time
from typing import Any

from matrx_ai.tools.arg_models.dictionary_args import DictionaryArgs
from matrx_ai.tools.models import ToolContext, ToolError, ToolResult

logger = logging.getLogger(__name__)


def _database_name() -> str:
    from matrx_orm.core.config import get_all_database_project_names

    names = get_all_database_project_names()
    return names[0] if names else "matrx"


def _json(value: Any) -> Any:
    if isinstance(value, str):
        try:
            return json.loads(value)
        except (json.JSONDecodeError, TypeError):
            return value
    return value


def _rows(rows: Any) -> list[dict[str, Any]]:
    """Normalize asyncpg records to fully JSON-native dicts.

    ``SELECT *`` returns native ``datetime`` / ``uuid.UUID`` columns; those are
    not JSON-serializable and break the tool-result handoff. The json round-trip
    with ``default=str`` coerces every non-native leaf (datetime → ISO string,
    UUID → str) so the tool output honours the JSON-native contract.
    """
    return [json.loads(json.dumps(dict(r), default=str)) for r in rows]


def _err(ctx: ToolContext, started: float, etype: str, msg: str) -> ToolResult:
    return ToolResult(
        success=False,
        error=ToolError(error_type=etype, message=msg),
        started_at=started,
        completed_at=time.time(),
        tool_name="dictionary",
        call_id=ctx.call_id,
    )


def _ok(ctx: ToolContext, started: float, output: Any) -> ToolResult:
    return ToolResult(
        success=True,
        output=output,
        started_at=started,
        completed_at=time.time(),
        tool_name="dictionary",
        call_id=ctx.call_id,
    )


def _owner_id(action: Any, user_id: str) -> str:
    """Resolve owner_id, defaulting the user level to the calling user."""
    level = getattr(action, "level", None)
    oid = (getattr(action, "owner_id", "") or "").strip()
    if level == "user" and not oid:
        return user_id
    return oid


async def dictionary(args: dict[str, Any], ctx: ToolContext) -> ToolResult:
    started = time.time()
    try:
        parsed = DictionaryArgs(**args).root
    except Exception as exc:  # noqa: BLE001 — surfaced as a clean tool error
        return _err(ctx, started, "invalid_arguments", f"dictionary: {exc}")

    user_id = ctx.user_id
    if not user_id:
        return _err(ctx, started, "auth_required", "dictionary requires an authenticated user.")

    action = parsed.action
    database = _database_name()

    try:
        from matrx_orm import ArrayArg, call_function

        if action == "list_owners":
            r = await call_function(database, "public", "dict_list_owners_for", user_id)
            return _ok(ctx, started, _json(r))

        if action == "resolve":
            r = await call_function(
                database,
                "public",
                "dict_resolve_for",
                user_id,
                parsed.include_personal,
                parsed.all,
                # uuid[] params — a bare list binds ::jsonb in call_function
                # and raises UndefinedFunctionError; ArrayArg binds natively.
                ArrayArg([str(x) for x in parsed.organization_ids]),
                ArrayArg([str(x) for x in parsed.scope_type_ids]),
                ArrayArg([str(x) for x in parsed.scope_ids]),
            )
            return _ok(ctx, started, _json(r))

        if action == "list_entries":
            oid = _owner_id(parsed, user_id)
            rows = await call_function(
                database, "public", "dict_list_entries_for", user_id, parsed.level, oid, mode="rows"
            )
            return _ok(ctx, started, {"entries": _rows(rows)})

        if action == "upsert_entries":
            oid = _owner_id(parsed, user_id)
            rows = await call_function(
                database,
                "public",
                "dict_upsert_entries_for",
                user_id,
                parsed.level,
                oid,
                json.dumps(parsed.entries),
                mode="rows",
            )
            return _ok(ctx, started, {"entries": _rows(rows), "count": len(rows)})

        if action == "delete_entries":
            oid = _owner_id(parsed, user_id)
            n = await call_function(
                database,
                "public",
                "dict_delete_entries_for",
                user_id,
                parsed.level,
                oid,
                ArrayArg([str(x) for x in parsed.ids]),
            )
            return _ok(ctx, started, {"deleted": int(n or 0)})

        if action == "get_settings":
            oid = _owner_id(parsed, user_id)
            r = await call_function(
                database, "public", "dict_get_settings_for", user_id, parsed.level, oid
            )
            return _ok(ctx, started, _json(r))

        if action == "set_settings":
            oid = _owner_id(parsed, user_id)
            r = await call_function(
                database,
                "public",
                "dict_set_settings_for",
                user_id,
                parsed.level,
                oid,
                parsed.max_inline_chars,
            )
            return _ok(ctx, started, _json(r))

        if action == "fetch_user_content":
            return _ok(ctx, started, await _fetch_user_content(user_id, parsed))

    except Exception as exc:  # noqa: BLE001
        # DB-raised auth violations (42501) and everything else land here.
        msg = str(exc)
        etype = (
            "permission_denied"
            if "outside your organizations" in msg or "another user" in msg
            else "db_error"
        )
        logger.warning("[dictionary] %s failed: %s", action, msg)
        return _err(ctx, started, etype, msg)

    return _err(ctx, started, "invalid_arguments", f"dictionary: unknown action {action!r}")


# Registered in matrx_ai/tools/_generated_declarations.py via _reg(...) — the
# authoritative declaration list the tool-drift gate validates against. The
# function stays un-decorated here (the `memory`/`sql`/`web` pattern).


def _extract_text_blocks(content: Any) -> str | None:
    """Join every ``type == "text"`` block's ``text`` field, space-separated."""
    blocks = _json(content)
    if not isinstance(blocks, list):
        return None
    parts = [
        b.get("text") for b in blocks if isinstance(b, dict) and b.get("type") == "text" and b.get("text")
    ]
    return " ".join(parts) if parts else None


async def _fetch_user_content(user_id: str, parsed: Any) -> dict[str, Any]:
    """Recent notes + conversation text for the agent to mine candidate terms."""
    from matrx_orm import Q

    from matrx_ai.db._registry import get_model

    out: dict[str, Any] = {}
    limit = parsed.limit
    if parsed.source in ("notes", "both"):
        # workbench.notes columns are created_by/deleted_at — the old raw SQL's
        # user_id/is_deleted never existed post schema-reorg and 500'd live.
        Notes = get_model("Notes")
        note_rows = await (
            Notes.filter(created_by=user_id, deleted_at__isnull=True)
            .order_by("-updated_at")
            .limit(limit)
            .values("label", "content")
        )
        out["notes"] = [
            {
                "label": r["label"],
                "content": r["content"][:4000] if r["content"] is not None else None,
            }
            for r in note_rows
        ]
    if parsed.source in ("conversations", "both"):
        # Mine recent USER-typed text. chat.message.content (jsonb blocks) is
        # the source of truth: user_content is NULL for user-role rows BY
        # DESIGN (it's the agent-template display override). chat.conversation
        # has NO user_id column — it's created_by (the OLD raw SQL's c.user_id
        # never existed post schema-reorg and would have 500'd live).
        Conversation = get_model("Conversation")
        Message = get_model("Message")
        conv_rows = await (
            Conversation.filter(created_by=user_id, deleted_at__isnull=True)
            .order_by("-updated_at")
            .limit(limit)
            .values("id", "title", "keywords")
        )
        conversations: list[dict[str, Any]] = []
        for c in conv_rows:
            # Last 6 visible, non-deleted USER messages for this conversation —
            # is_visible_to_user IS NULL is treated as visible (coalesce(...,true)
            # in the original raw SQL).
            msg_rows = await (
                Message.filter(
                    conversation_id=c["id"], role="user", deleted_at__isnull=True
                )
                .filter(Q(is_visible_to_user=True) | Q(is_visible_to_user__isnull=True))
                .order_by("-position")
                .limit(6)
                .values("content")
            )
            texts = [
                t[:500]
                for t in (_extract_text_blocks(m["content"]) for m in msg_rows)
                if t
            ]
            conversations.append(
                {
                    "title": c["title"],
                    "keywords": c["keywords"],
                    "recent_user_text": " / ".join(texts) if texts else None,
                }
            )
        out["conversations"] = conversations
    return out
