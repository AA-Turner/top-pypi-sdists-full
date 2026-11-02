"""discord route registration in the abstract_flask ``register_categories``
convention.

The bot's HTTP surface (bindings / resolve / outbox / channels / users /
bridges / inbox / sessions / prefs), originally built by ``_attach`` onto two
blueprints (bare ``discord`` and ``discord_api``) in ``discord_routes.py``, is
expressed here as ONE blueprint (``discord_bp``) plus a flat category dict; the
parent wires the bare-vs-/api dual mount.

Each view body is a module-level PURE FUNCTION that takes its inputs as kwargs
(filled by abstract_flask from the JSON body / form / query string — never from
``request``). Former path params (``binding_id``, ``bridge_id``, ``session_id``,
``token``) are now kwargs. The domain logic (candidate generation, defer
routing, option validation, the model-key catalog read) is unchanged — it is
imported from ``discord_routes`` where it still lives, so there is one source.
"""
from __future__ import annotations

from abstract_flask import get_bp, register_categories
from flask import abort

from hugpy_core.discord import discord_store
from hugpy_core.discord.discord_routes import (
    _SESSION_MSG_LIMIT,
    _generate_candidate,
    _known_model_keys,
    _route_bridge_reply,
    _validate_options,
)

discord_bp, logger = get_bp("discord_bp", __name__)


# ── bindings ──────────────────────────────────────────────────────────────────
def bindings_list():
    return {"bindings": discord_store.list_bindings()}


def bindings_create(model_key=None, channel_id=None, user_id=None, label=None):
    if not model_key:
        abort(400, description="model_key is required.")
    known = _known_model_keys()
    if known and model_key not in known:
        abort(404, description="Unknown model key.")
    if not channel_id and not user_id:
        abort(400, description="Provide a channel_id and/or a user_id.")
    try:
        return discord_store.add_binding(model_key=model_key, channel_id=channel_id,
                                         user_id=user_id, label=label)
    except ValueError as exc:
        abort(400, description=str(exc))


def bindings_delete(binding_id=None):
    if not discord_store.remove_binding(binding_id):
        abort(404, description="Unknown binding id.")
    return {"ok": True, "id": binding_id}


def resolve(channel_id=None, user_id=None):
    """The bot asks core which model an inbound (channel, user) should hit."""
    return {"model_key": discord_store.resolve(channel_id=channel_id, user_id=user_id)}


# ── outbox ──────────────────────────────────────────────────────────────────
def outbox_enqueue(content=None, channel_id=None, user_id=None, binding_id=None):
    if not (content or "").strip():
        abort(400, description="content is required.")
    try:
        return discord_store.enqueue_outbound(content=content, channel_id=channel_id,
                                              user_id=user_id, binding_id=binding_id)
    except ValueError as exc:
        abort(400, description=str(exc))


def outbox_drain():
    """The bot polls this and delivers each returned message to Discord."""
    return {"messages": discord_store.drain_outbound()}


# ── channel / user snapshots ──────────────────────────────────────────────────
def channels_list():
    return discord_store.get_channels()


def channels_report(channels=None):
    if not isinstance(channels, list):
        abort(400, description="channels must be a list.")
    return discord_store.set_channels(channels)


def users_list():
    return discord_store.get_users()


def users_report(users=None):
    if not isinstance(users, list):
        abort(400, description="users must be a list.")
    return discord_store.set_users(users)


# ── bridges ─────────────────────────────────────────────────────────────────
def bridges_list():
    return {"bridges": discord_store.list_bridges()}


def bridges_create(channel_id=None, model_key=None, user_id=None, binding_id=None,
                   directive=None, defer_mode=None, brain=None, keeper_target=None,
                   log_mode=None):
    if binding_id:
        match = next((b for b in discord_store.list_bindings()
                      if b.get("id") == binding_id), None)
        if not match:
            abort(404, description="Unknown binding id.")
        channel_id = channel_id or match.get("channel_id")
        user_id = user_id or match.get("user_id")
        model_key = model_key or match.get("model_key")
    if not channel_id:
        abort(400, description="Provide a binding_id or a channel_id.")
    try:
        return discord_store.add_bridge(
            channel_id=channel_id, model_key=model_key, user_id=user_id,
            directive=directive, defer_mode=defer_mode or "auto",
            brain=brain or "model", keeper_target=keeper_target,
            log_mode=log_mode or "open")
    except ValueError as exc:
        abort(400, description=str(exc))


def bridges_delete(bridge_id=None):
    if not discord_store.remove_bridge(bridge_id):
        abort(404, description="Unknown bridge id.")
    return {"ok": True, "id": bridge_id}


def bridge_messages(bridge_id=None, since=0):
    if not discord_store.get_bridge(bridge_id):
        abort(404, description="Unknown bridge id.")
    try:
        since = float(since or 0)
    except (TypeError, ValueError):
        since = 0.0
    return {"messages": discord_store.get_messages(bridge_id, since)}


def bridge_clear_messages(bridge_id=None):
    if not discord_store.get_bridge(bridge_id):
        abort(404, description="Unknown bridge id.")
    cleared = discord_store.clear_messages(bridge_id)
    return {"ok": True, "id": bridge_id, "cleared": cleared or 0}


def bridge_send(bridge_id=None):
    """DISABLED (legacy 2026-07-09): console->channel send was an outbound-send
    vector. Legitimate outbound flows via /keeper-reply and the scoped session
    token."""
    if not discord_store.get_bridge(bridge_id):
        abort(404, description="Unknown bridge id.")
    abort(403, description="Console->channel send is disabled (removed as an "
                           "outbound-send vector). Use a keeper or a session token.")


def inbox(channel_id=None, content=None, attachments=None, author=None):
    """The bot posts inbound channel messages here. For a bridged channel we
    record it, generate a candidate from the bridge's directive, then apply
    defer_mode: auto-send, hold for the operator, or let the model decide."""
    content = (content or "").strip()
    attachments = attachments or []
    bridge = discord_store.bridge_for_channel(channel_id) if channel_id else None
    if not bridge:
        return {"bridged": False}
    if not content and not attachments:
        return {"bridged": True, "bridge_id": bridge["id"],
                "defer_mode": bridge.get("defer_mode"), "action": "none"}

    discord_store.append_message(bridge["id"], direction="in", source="discord",
                                 content=content, author=author, attachments=attachments)

    if bridge.get("brain", "model") == "keeper":
        return {"bridged": True, "bridge_id": bridge["id"], "brain": "keeper",
                "defer_mode": bridge.get("defer_mode"), "action": "await_keeper"}

    ephemeral = bridge.get("log_mode", "open") == "none"
    try:
        candidate = _generate_candidate(bridge, current_inbound=content if ephemeral else "")
    except Exception:  # noqa: BLE001
        logger.exception("bridge candidate generation failed")
        candidate = ""
    action = _route_bridge_reply(bridge, candidate, source="model")
    return {"bridged": True, "bridge_id": bridge["id"],
            "defer_mode": bridge.get("defer_mode"), "action": action}


def bridge_keeper_reply(bridge_id=None, content=None):
    """A keeper submits a drafted reply for a keeper-brained bridge; defer_mode
    decides what happens."""
    bridge = discord_store.get_bridge(bridge_id)
    if not bridge:
        abort(404, description="Unknown bridge id.")
    content = (content or "").strip()
    if not content:
        abort(400, description="content is required.")
    action = _route_bridge_reply(bridge, content, source="keeper")
    return {"bridge_id": bridge_id, "defer_mode": bridge.get("defer_mode"), "action": action}


def bridge_approve(bridge_id=None, message_id=None):
    """Approve a pending candidate AS GENERATED and send it (editing before send
    was removed as an outbound-send vector)."""
    bridge = discord_store.get_bridge(bridge_id)
    if not bridge:
        abort(404, description="Unknown bridge id.")
    if not message_id:
        abort(400, description="message_id is required.")
    msg = discord_store.update_message(bridge_id, message_id, status="sent")
    if not msg:
        abort(404, description="Unknown message id.")
    discord_store.enqueue_outbound(content=msg["content"], channel_id=bridge.get("channel_id"),
                                   user_id=bridge.get("user_id"))
    return msg


def bridge_reject(bridge_id=None, message_id=None):
    if not discord_store.get_bridge(bridge_id):
        abort(404, description="Unknown bridge id.")
    if not message_id:
        abort(400, description="message_id is required.")
    msg = discord_store.update_message(bridge_id, message_id, status="rejected")
    if not msg:
        abort(404, description="Unknown message id.")
    return msg


# ── comms sessions: scoped bearer endpoints for terminal agents ───────────────
def sessions_mint(channel_id=None, label=None, ttl_hours=None, author=None):
    if not channel_id:
        abort(400, description="channel_id is required.")
    bridge = discord_store.bridge_for_channel(channel_id)
    if not bridge:
        bridge = discord_store.add_bridge(
            channel_id=channel_id, brain="keeper",
            keeper_target=f"session:{(label or '').strip() or 'terminal'}")
    try:
        token, session = discord_store.add_session(channel_id=channel_id, label=label or "",
                                                   ttl_hours=ttl_hours, author=author)
    except ValueError as exc:
        abort(400, description=str(exc))
    return {"token": token, "session": session, "bridge_id": bridge["id"],
            "endpoint": f"/discord/session/{token}"}


def sessions_list():
    return {"sessions": discord_store.list_sessions()}


def sessions_prune():
    return {"ok": True, "pruned": discord_store.prune_sessions()}


def sessions_revoke(session_id=None, purge=None):
    purge = str(purge or "").strip() in ("1", "true", "yes")
    if purge:
        if not discord_store.delete_session(session_id):
            abort(404, description="Unknown session id.")
        return {"ok": True, "id": session_id, "purged": True}
    if not discord_store.revoke_session(session_id):
        abort(404, description="Unknown or already-revoked session id.")
    return {"ok": True, "id": session_id}


def _session_or_404(token: str) -> dict:
    s = discord_store.session_by_token(token)
    if not s:
        abort(404)  # bad, revoked, expired — indistinguishable, no oracle
    return s


def session_info(token=None):
    s = _session_or_404(token)
    chans = (discord_store.get_channels() or {}).get("channels") or []
    name = next((c.get("name") for c in chans if str(c.get("id")) == str(s["channel_id"])), None)
    return {
        "channel_id": s["channel_id"], "channel": name, "label": s.get("label") or "",
        "bridged": bool(discord_store.bridge_for_channel(s["channel_id"])),
        "usage": {
            "poll": "GET …/messages?since=<ts float from last message> → {\"messages\":[…]}",
            "send": f"POST …/send {{\"content\":\"…\"}} (≤{_SESSION_MSG_LIMIT} chars) → bot delivers within ~8s",
        },
    }


def session_messages(token=None, since=0):
    s = _session_or_404(token)
    bridge = discord_store.bridge_for_channel(s["channel_id"])
    if not bridge:
        return {"messages": [], "warning": "channel bridge removed — inbound relay is off"}
    try:
        since = float(since or 0)
    except (TypeError, ValueError):
        since = 0.0
    return {"messages": discord_store.get_messages(bridge["id"], since)}


def session_send(token=None, content=None, options=None, author=None):
    s = _session_or_404(token)
    content = (content or "").strip()
    if not content:
        abort(400, description="content is required.")
    if len(content) > _SESSION_MSG_LIMIT:
        abort(413, description=f"content exceeds {_SESSION_MSG_LIMIT} chars — split it.")
    options = _validate_options(options)
    author = (author or s.get("author") or s.get("label") or "session").strip()
    bridge = discord_store.bridge_for_channel(s["channel_id"])
    msg = None
    if bridge:
        kwargs = {"direction": "out", "source": "session", "content": content, "author": author}
        if options is not None:
            kwargs["options"] = options
        msg = discord_store.append_message(bridge["id"], **kwargs)
    discord_store.enqueue_outbound(content=content, channel_id=s["channel_id"], options=options)
    return {"ok": True, "message": msg}


# ── per-user prefs (Discord /model) ───────────────────────────────────────────
def prefs_set(user_id=None, model_key=None):
    """Bot M2M pref write: a user's default model, so the console sees and can
    override it."""
    user_id = str(user_id or "")
    if not user_id:
        abort(400, description="user_id required")
    value = discord_store.set_pref(user_id, {"model": model_key})
    return {"user_id": user_id, "value": value}


ALL_CATEGORIES = {
    "discord": {
        # single-verb-per-URL routes keep their original URL
        "resolve": resolve,       # GET  /discord/resolve
        "inbox": inbox,           # POST /discord/inbox
        "prefs": prefs_set,       # POST /discord/prefs
        "outbox": {
            "": outbox_enqueue,   # POST /discord/outbox
            "drain": outbox_drain,  # POST /discord/outbox/drain
        },
        # resource groups: a shared URL distinguished only by verb (GET list /
        # POST create|report) or a path-param tail collapses to one route_name
        # per action
        "bindings": {
            "list": bindings_list,      # was GET    /discord/bindings
            "create": bindings_create,  # was POST   /discord/bindings
            "delete": bindings_delete,  # was DELETE /discord/bindings/<binding_id>
        },
        "bridges": {
            "list": bridges_list,                   # was GET    /discord/bridges
            "create": bridges_create,               # was POST   /discord/bridges
            "delete": bridges_delete,               # was DELETE /discord/bridges/<bridge_id>
            "approve": bridge_approve,              # was POST   /discord/bridges/<bridge_id>/approve
            "keeper-reply": bridge_keeper_reply,    # was POST   /discord/bridges/<bridge_id>/keeper-reply
            "reject": bridge_reject,                # was POST   /discord/bridges/<bridge_id>/reject
            "send": bridge_send,                    # was POST   /discord/bridges/<bridge_id>/send
            "messages": bridge_messages,            # was GET    /discord/bridges/<bridge_id>/messages
            "messages_clear": bridge_clear_messages,  # was DELETE /discord/bridges/<bridge_id>/messages
        },
        "channels": {
            "list": channels_list,      # was GET  /discord/channels
            "report": channels_report,  # was POST /discord/channels
        },
        "users": {
            "list": users_list,      # was GET  /discord/users
            "report": users_report,  # was POST /discord/users
        },
        "sessions": {
            "list": sessions_list,      # was GET    /discord/sessions
            "mint": sessions_mint,      # was POST   /discord/sessions
            "prune": sessions_prune,    # was POST   /discord/sessions/prune
            "revoke": sessions_revoke,  # was DELETE /discord/sessions/<session_id>
        },
        "session": {
            "info": session_info,          # was GET  /discord/session/<token>
            "messages": session_messages,  # was GET  /discord/session/<token>/messages
            "send": session_send,          # was POST /discord/session/<token>/send
        },
    },
}

register_categories(discord_bp, ALL_CATEGORIES)
