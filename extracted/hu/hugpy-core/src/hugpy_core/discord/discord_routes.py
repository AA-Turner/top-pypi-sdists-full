# The Discord bot's HTTP surface, LIFTED from legacy central (read-only reference):
#   hugpy_server/app/routes/discord_routes.py  (bindings/resolve/outbox/channels/
#       users/bridges/inbox/sessions) and comms_routes.py:431 (/discord/prefs).
# The bot (hugpy_discord) 404'd on every one of these since legacy central went off
# 2026-10-03; core now serves them. State is the core DB (discord_store), not a JSON
# file. Candidate generation goes through core's own /v1/chat/completions so every
# reply is a call_log row (intent 'discord-bridge') — not legacy's in-process
# execute_prompt.
#
# DROPPED (dependencies absent in core): the MEMBER bot-link routes
#   POST/GET/DELETE /discord/bot-links — they need legacy api_keys (create/list/
#   revoke_api_key), auth_common (require_member_strict, caller_username),
#   operator_auth, and agent_routes._install_public_base, none of which exist in
#   core. The hugpy bot never calls them; the console's bridge UI does not need them.
# Auth: core runs open-auth (/auth/config=open, LAN/WG-only at nginx), so the
#   operator/member gates legacy wrapped around some of these are NOT re-applied —
#   this mirrors every other core route (none carry an auth decorator).
"""hugpy_core /discord/*: the bot's bindings/outbox/bridges/sessions surface."""
from __future__ import annotations

import json
import logging
import os


from hugpy_core.discord import discord_store
from flask import abort  # _validate_options aborts with 400; the import was missing

logger = logging.getLogger("hugpy_core")


# Discord hard-caps a message at 2000 chars; refuse instead of a silent later fail.
_SESSION_MSG_LIMIT = 1900


# ── candidate generation (the bridge's "brain") ───────────────────────────────
def _strip_think(text: str):
    try:
        from hugpy_resources.imports.functions.thinking import strip_think
        return strip_think(text)
    except Exception:  # noqa: BLE001 — stdlib fallback, same regex semantics
        import re
        rx = re.compile(r"<think>(.*?)(?:</think>|\Z)", re.DOTALL | re.IGNORECASE)
        if not text:
            return "", ""
        reasoning = "\n".join(m.group(1).strip() for m in rx.finditer(text))
        return rx.sub("", text).strip(), reasoning.strip()


def _with_no_think(user_text: str) -> str:
    try:
        from hugpy_resources.imports.functions.thinking import with_no_think
        return with_no_think(user_text)
    except Exception:  # noqa: BLE001
        directive = "/no_think"
        if not user_text:
            return directive
        return user_text if directive in user_text else f"{user_text}\n\n{directive}"


def _relay_chat(model_key: str, messages: list) -> str:
    """Core's own /v1/chat/completions, so the reply is a call_log row
    (metadata.intent 'discord-bridge'). Returns the assistant content ('' on any
    non-2xx / malformed body so the caller falls back to manual operation)."""
    from hugpy_core.relay.internal import chat
    try:
        payload, status = chat({"model": model_key, "messages": messages,
                                "metadata": {"intent": "discord-bridge"}}, caller="discord")
        if status >= 400:
            logger.warning("discord bridge relay failed: %s", payload.get("error"))
            return ""
    except Exception as exc:
        logger.warning("discord bridge relay failed: %s", exc)
        return ""
    try:
        return (payload["choices"][0]["message"]["content"] or "").strip()
    except (KeyError, IndexError, TypeError):
        logger.warning("discord bridge relay returned no content: %r", payload)
        return ""


_DIRECTIVE_DECIDE = (
    "\n\nWhen you have drafted your reply: if the guidance above indicates you "
    "should let the operator review it before it is sent (e.g. uncertainty, or a "
    "sensitive / out-of-scope topic), begin the reply with 'DEFER: '. Otherwise "
    "reply normally.")


def _generate_candidate(bridge: dict, current_inbound: str = "") -> str:
    """A model reply from the bridge's directive + the sent transcript. '' on any
    failure. current_inbound carries the turn for a no-logs bridge (whose transcript
    is never stored); logged bridges already have it in the transcript."""
    model_key = bridge.get("model_key")
    if not model_key:
        return ""
    directive = (bridge.get("directive")
                 or "You are relaying a Discord channel on the operator's behalf. Reply concisely.")
    if bridge.get("defer_mode") == "directive":
        directive = directive + _DIRECTIVE_DECIDE
    msgs = [{"role": "system", "content": directive}]
    for m in discord_store.get_messages(bridge["id"]):
        if m.get("status") != "sent":
            continue  # pending/rejected are not part of the real conversation
        role = "user" if m.get("direction") == "in" else "assistant"
        msgs.append({"role": role, "content": m.get("content") or ""})
    if current_inbound:
        msgs.append({"role": "user", "content": current_inbound})
    if len(msgs) > 13:                       # system + last 12 turns
        msgs = [msgs[0]] + msgs[-12:]
    # NO-THINK: the reply is parsed (the DEFER gate reads candidate.upper()) and
    # then transmitted verbatim to a live channel; a <think> prelude would defeat
    # the gate and leak reasoning. Strip it; nobody is watching tokens here.
    if len(msgs) > 1 and msgs[-1]["role"] == "user":
        msgs[-1] = {**msgs[-1], "content": _with_no_think(msgs[-1]["content"])}
    candidate, reasoning = _strip_think(_relay_chat(model_key, msgs))
    if reasoning and not candidate:
        logger.warning("bridge %s: model returned only reasoning, no candidate", bridge.get("id"))
    return candidate


def _route_bridge_reply(bridge: dict, candidate: str, *, source: str) -> str:
    """Apply a bridge's defer_mode to an outbound reply: hold it (pending) or send
    it (enqueue to Discord). Returns 'none' | 'pending' | 'sent'."""
    candidate = (candidate or "").strip()
    if not candidate:
        return "none"
    mode = bridge.get("defer_mode", "auto")
    defer = (mode == "defer")
    if mode == "directive" and candidate.upper().startswith("DEFER"):
        defer = True
        candidate = candidate.split(":", 1)[1].strip() if ":" in candidate else candidate
    if not candidate:
        return "none"
    if defer:
        discord_store.append_message(bridge["id"], direction="out", source=source,
                                     content=candidate, status="pending")
        return "pending"
    discord_store.append_message(bridge["id"], direction="out", source=source,
                                 content=candidate, status="sent")
    discord_store.enqueue_outbound(content=candidate, channel_id=bridge.get("channel_id"),
                                   user_id=bridge.get("user_id"))
    return "sent"


def _known_model_keys() -> set:
    """The model keys core knows about (its /models catalog). Empty when no worker
    is online / central is unreadable — in which case binding create does NOT 404
    (core's model source is discovery, not a static manifest)."""
    try:
        from hugpy_core.web.routes import catalog_rows
        return {r.get("model_key") for r in catalog_rows() if r.get("model_key")}
    except Exception:  # noqa: BLE001
        return set()


def _validate_options(raw):
    """None when absent; else a normalised list of 1..5 stripped label strings
    (Discord caps a button row at 5). Aborts 400 on any violation."""
    if raw is None:
        return None
    if not isinstance(raw, list):
        abort(400, description="options must be a list of strings.")
    if not raw:
        abort(400, description="options must be a non-empty list (omit it for a plain message).")
    if len(raw) > 5:
        abort(400, description="at most 5 options.")
    clean = []
    for opt in raw:
        if not isinstance(opt, str):
            abort(400, description="each option must be a string.")
        label = opt.strip()
        if not label:
            abort(400, description="options must not be empty.")
        if len(label) > 80:
            abort(400, description="each option must be at most 80 chars.")
        clean.append(label)
    return clean
