"""Tool-result duplication guard — loud, self-documenting last-line defenses.

Two independent provider-payload guards call into here when they catch the SAME
failure class: more than one ``tool_result`` block carrying the same
``tool_use_id`` in a single request. Anthropic (and every other provider)
rejects the WHOLE request with a 400 —

    messages.N.content.M: each tool_use must have a single result.
    Found multiple `tool_result` blocks with id: toolu_...

— so a single duplicated id silently kills every future turn of a conversation
until a human notices. These guards REMOVE the duplicate so the request
survives, but they must never do it quietly: a duplicate reaching this far means
an upstream invariant already broke. Every catch SCREAMS (red banner + a durable
ERROR log that lands in ``public.app_log`` via the host root logging handler)
with enough of the story for an admin to find the source.

Root-cause reference (2026-06-22, conversation ``bcc588b6-...``): a
watchdog-timed-out ``research_web`` tool's ``cx_tool_call`` row was persisted
with ``message_id = NULL``; the conversation-rebuild synthetic-pairing path then
re-emitted a ``tool_result`` that the persisted ``role='tool'`` message already
carried. The warm ``AgentCache`` masked it for 30 min; once the TTL expired, the
cache-miss DB rebuild surfaced the duplicate and 400'd the turn.

This module imports NOTHING from the rest of the config package, so any module
(``message_config``, the provider translators, …) can import it without a cycle.
"""

from __future__ import annotations

import asyncio
import logging
from typing import Any

from matrx_utils import supervised_task, vcprint

logger = logging.getLogger("matrx_ai.tool_result_guard")

# Identity strings so a grep / log filter can find each catch site.
LAYER_SANITIZE = "MessageList.sanitize (provider-agnostic assembly guard)"
LAYER_ANTHROPIC = (
    "anthropic.translator (final provider-payload boundary, last line before the wire)"
)

NONADJACENT_TOOL_USE_ERROR_KIND = "tool_result_pairing_corruption"


async def capture_nonadjacent_tool_uses(
    *,
    layer: str,
    dropped: list[dict[str, Any]],
    context: dict[str, Any],
) -> None:
    """Create the structured repair-queue row for a destructive guard hit.

    The app-log banner is operator evidence, not durable error capture.  Keep
    the payload deliberately bounded: call ids and provider output are not
    required to identify this root class, while request/conversation identity
    is supplied as first-class capture fields when available.
    """
    from matrx_connect.streaming.error_capture import capture_error

    separated_count = sum(d.get("reason") == "separated" for d in dropped)
    exc = RuntimeError(
        "Message assembly separated tool_use from its tool_result; "
        f"guard removed {len(dropped)} call(s), separated={separated_count}"
    )
    await capture_error(
        exc,
        kind=NONADJACENT_TOOL_USE_ERROR_KIND,
        request_id=context.get("request_id"),
        user_id=context.get("user_id"),
        conversation_id=context.get("conversation_id"),
        route=context.get("route"),
        error_type="NonadjacentToolResult",
        context={
            "layer": layer,
            "dropped_count": len(dropped),
            "separated_count": separated_count,
        },
    )


def _schedule_nonadjacent_capture(
    *, layer: str, dropped: list[dict[str, Any]], context: dict[str, Any]
) -> None:
    """Schedule capture when sanitize runs inside a request event loop.

    MessageList is also used by synchronous migration utilities and unit tests;
    those have no async host sink and must not manufacture an un-awaited
    coroutine merely by exercising the pure sanitizer.
    """
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return
    supervised_task(
        capture_nonadjacent_tool_uses(layer=layer, dropped=dropped, context=context),
        kind="tool_result_pairing_capture_failed",
        name="capture_nonadjacent_tool_uses",
        context={"layer": layer},
    )
def result_block_is_empty(content: Any) -> bool:
    """True when a tool_result's content carries nothing useful.

    Used to pick the better survivor when two blocks share an id: an empty
    pointer stub should never win over a block that actually carries output.
    """
    if content is None:
        return True
    if isinstance(content, str):
        return not content.strip()
    if isinstance(content, list | dict):
        return len(content) == 0
    return False


def dedupe_tool_result_dicts(
    content: list[Any],
) -> tuple[list[Any], list[dict[str, Any]]]:
    """Remove duplicate ``tool_result`` blocks (same ``tool_use_id``) from a
    provider-shaped content list.

    Keeps the first occurrence of each id, but upgrades to a later block if the
    one already kept was empty and the later one is not — so a real result never
    loses to an empty stub. Returns ``(deduped_content, duplicates_report)`` where
    each report entry is ``{tool_use_id, name, count, dropped}``.
    """
    first_index: dict[str, int] = {}
    counts: dict[str, int] = {}
    names: dict[str, str] = {}
    out: list[Any] = []

    for block in content:
        if isinstance(block, dict) and block.get("type") == "tool_result":
            tid = block.get("tool_use_id") or block.get("call_id")
            if tid:
                counts[tid] = counts.get(tid, 0) + 1
                if not names.get(tid):
                    names[tid] = block.get("name") or ""
                if tid in first_index:
                    kept = out[first_index[tid]]
                    if result_block_is_empty(
                        kept.get("content")
                    ) and not result_block_is_empty(block.get("content")):
                        out[first_index[tid]] = block
                    continue  # drop this duplicate
                first_index[tid] = len(out)
        out.append(block)

    duplicates = [
        {"tool_use_id": tid, "name": names.get(tid) or None, "count": c, "dropped": c - 1}
        for tid, c in counts.items()
        if c > 1
    ]
    return out, duplicates


def _current_context() -> dict[str, Any]:
    """Best-effort request identity for the durable log. Never raises."""
    try:
        from matrx_connect import get_app_context  # optional dep, lazy

        ctx = get_app_context()
    except Exception:
        return {}
    if ctx is None:
        return {}

    out: dict[str, Any] = {}
    for attr in ("user_id", "request_id", "route", "auth_type"):
        val = getattr(ctx, attr, None)
        if val is not None:
            out[attr] = str(val)
    meta = getattr(ctx, "metadata", None)
    if isinstance(meta, dict):
        conv = meta.get("conversation_id")
        if conv:
            out["conversation_id"] = str(conv)
    return out


def report_tool_result_duplicates(
    *,
    layer: str,
    duplicates: list[dict[str, Any]],
    total_tool_results: int,
) -> None:
    """Scream about duplicate tool_result blocks we just removed.

    Loud red banner (terminal) + a durable ERROR record (``public.app_log`` via
    the host's root logging handler). The banner tells the whole story so an
    admin can chase the source without reverse-engineering it from a 400.
    """
    if not duplicates:
        return

    ctx = _current_context()
    ids = ", ".join(str(d.get("tool_use_id")) for d in duplicates)

    lines = [
        "",
        "████████████████████████████████████████████████████████████████████████████",
        "██  DUPLICATE tool_result BLOCKS CAUGHT AND REMOVED — THIS IS NOT NORMAL   ██",
        "████████████████████████████████████████████████████████████████████████████",
        f"WHO I AM      : {layer}",
        "                A last-line provider-payload guard inside matrx-ai. I exist",
        "                only to stop a malformed request from reaching the provider.",
        f"WHAT I GOT    : {total_tool_results} tool_result block(s) in this request; "
        f"{len(duplicates)} tool_use_id(s)",
        "                appeared MORE THAN ONCE:",
    ]
    for d in duplicates:
        lines.append(
            f"                  • id={d.get('tool_use_id')}  "
            f"name={d.get('name') or '?'}  "
            f"seen {d.get('count')}x  →  kept 1, dropped {d.get('dropped')}"
        )
    lines += [
        "WHAT'S WRONG  : Every provider requires EXACTLY ONE tool_result per tool_use.",
        "                Two blocks with the same id 400 the WHOLE request",
        "                ('each tool_use must have a single result') — which then kills",
        "                every future turn of the conversation until someone fixes it.",
        "WHERE TO LOOK : 1) cx_tool_call rows with message_id=NULL for these call_ids —",
        "                   a tool that finalized (often error_type='watchdog_timeout')",
        "                   AFTER its role='tool' pointer message was already written.",
        "                2) conversation_rebuild.py synthetic-pairing path re-emitting a",
        "                   result the persisted role='tool' message already carries.",
        "                3) A stale-cache vs DB-rebuild mix: a warm AgentCache entry",
        "                   (30-min TTL) expiring and forcing a cache-miss rebuild.",
        f"CONTEXT       : {ctx or 'no app context available'}",
        "VERDICT       : I removed the duplicate so THIS request survives — but I will",
        "                not save you twice. Fix the source above.",
        "████████████████████████████████████████████████████████████████████████████",
        "",
    ]
    vcprint("\n".join(lines), color="red")

    logger.error(
        "Duplicate tool_result blocks removed at %s (ids: %s) — upstream invariant broke; "
        "see banner for where to look.",
        layer,
        ids,
        extra={
            "event": "duplicate_tool_result_blocks",
            "layer": layer,
            "duplicate_ids": [d.get("tool_use_id") for d in duplicates],
            "duplicate_detail": duplicates,
            "total_tool_results": total_tool_results,
            **{f"ctx_{k}": v for k, v in ctx.items()},
        },
    )


def report_nonadjacent_tool_uses(
    *,
    layer: str,
    dropped: list[dict[str, Any]],
) -> None:
    """Scream about tool_use blocks removed because their tool_result was NOT in
    the immediately-following message.

    Every provider requires an assistant's tool_results in the VERY NEXT message,
    so a tool_use that loses adjacency has to go or the whole request 400s. But
    adjacency is lost for one of TWO different reasons, and each entry in
    ``dropped`` carries its ``reason``:

    * ``separated``  — ONE call, ONE result, WRONG ORDER: a producer put another
      message (typically the assistant's own text) between them. Nothing is
      duplicated, so nothing survives the drop — the call AND its result are
      erased from the model's history and never reach ``cx_message``. This is
      the 2026-08-11 incident (the OpenAI translator emitting the text message
      after the tool calls), and it wore the "duplicate" label below for months,
      which is why 251 of these alarms went unread.
    * ``duplicated`` — the MIRROR of the duplicate-tool_result bug: the SAME id
      was re-emitted in a later assistant turn that IS adjacently paired, i.e.
      one assistant message absorbed tool_uses belonging to OTHER turns. The
      adjacently-paired copy survives; only the stray copy is dropped.
    """
    if not dropped:
        return

    ctx = _current_context()
    ids = ", ".join(str(d.get("tool_use_id")) for d in dropped)
    separated = [d for d in dropped if d.get("reason") == "separated"]

    headline = (
        "SEPARATED tool_use/tool_result — THE CALL IS BEING ERASED"
        if separated
        else "NON-ADJACENT / DUPLICATE tool_use BLOCKS REMOVED — THIS IS NOT NORMAL"
    )
    bar = "█" * (len(headline) + 8)

    lines = [
        "",
        bar,
        f"██  {headline}  ██",
        bar,
        f"WHO I AM      : {layer}",
        "                A last-line provider-payload guard inside matrx-ai — the",
        "                MIRROR of the duplicate-tool_result guard.",
        f"WHAT I GOT    : {len(dropped)} tool_use block(s) whose tool_result was NOT in the",
        "                immediately-following message (the provider's hard rule:",
        "                'tool_use ids were found without tool_result blocks'):",
    ]
    for d in dropped:
        detail = (
            "its result comes LATER and nothing duplicates it — WRONG ORDER"
            if d.get("reason") == "separated"
            else "its result is paired with a LATER assistant turn"
        )
        lines.append(
            f"                  • id={d.get('tool_use_id')}  name={d.get('name') or '?'}  "
            f"({detail})"
        )

    if separated:
        lines += [
            "WHAT'S WRONG  : A producer emitted a message BETWEEN a tool_use and its",
            "                tool_result. There is no duplicate and no surviving copy —",
            "                this tool call and its result are deleted from the model's",
            "                history AND never written to cx_message. The user watches",
            "                the tool card stream, then loses it on reload. DATA LOSS.",
            "WHERE TO LOOK : 1) the provider translator that built this turn's messages —",
            "                   tool_use blocks MUST be the LAST assistant-side content",
            "                   before the role='tool' results (see the ordering note in",
            "                   OpenAITranslator._build_unified_messages).",
            "                2) anything appending to config.messages after a tool_use.",
            "                3) fork/edit/retry paths that re-stitch the message graph.",
        ]
    else:
        lines += [
            "WHAT'S WRONG  : ONE assistant message carries MORE tool_use blocks than the",
            "                next role='tool' message has results, and the extras are",
            "                duplicated in later assistant turns that ARE adjacently paired",
            "                — i.e. an assistant message absorbed tool_uses from other turns.",
            "WHERE TO LOOK : 1) cx_message: an assistant row whose content has N tool_use",
            "                   blocks while the next role='tool' row has < N results, the",
            "                   surplus ids re-appearing as tool_use in later assistant rows.",
            "                2) the orchestrator/persist path for PARALLEL tool calls that",
            "                   complete at staggered times (results land in separate",
            "                   role='tool' messages), and any fork/edit/retry that re-stitched",
            "                   the message graph.",
            "                3) conversation_rebuild.py grouping / synthesis.",
        ]

    lines += [
        f"CONTEXT       : {ctx or 'no app context available'}",
        "VERDICT       : I dropped what could not be adjacently paired so THIS request",
        "                survives — fix the source above so the graph stops getting",
        "                corrupted.",
        bar,
        "",
    ]
    vcprint("\n".join(lines), color="red")

    logger.error(
        "%s tool_use blocks removed at %s (ids: %s) — corrupted message graph; "
        "see banner for where to look.",
        "SEPARATED (call erased)" if separated else "Non-adjacent/duplicate",
        layer,
        ids,
        extra={
            "event": "nonadjacent_tool_use_blocks",
            "layer": layer,
            "separated_count": len(separated),
            "dropped_ids": [d.get("tool_use_id") for d in dropped],
            "dropped_detail": dropped,
            **{f"ctx_{k}": v for k, v in ctx.items()},
        },
    )
    _schedule_nonadjacent_capture(layer=layer, dropped=dropped, context=ctx)
