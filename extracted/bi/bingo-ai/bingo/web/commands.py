"""Web port of the classic Bingo slash-command palette.

The terminal exposed 19 `/commands`. The web IDE keeps the full set: pure-UI
commands return an ``action`` for the client to run locally; informational and
engine-backed commands are handled here against the live WebSession so the
pentest engine, history, and config stay authoritative (never model prose).

Security: credential commands never echo secret values — creds are referenced
by index/host only, never printed.
"""
from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .session import WebSession

# name -> ("action" for client, or None to run server-side here)
_CLIENT_ACTIONS = {
    "/clear": "clear",
    "/help": "help",
    "/history": "history",
    "/export": "export",
    "/retry": "retry",
    "/model": "settings",
    "/lang": "settings",
    "/config": "settings",
    "/quit": "quit",
    "/exit": "quit",
}


def dispatch_command(session: "WebSession", name: str, arg: str) -> dict:
    if name in _CLIENT_ACTIONS:
        return {"ok": True, "action": _CLIENT_ACTIONS[name]}

    handler = _SERVER.get(name)
    if handler is None:
        return {"ok": False, "text": f"Unknown command: {name}"}
    return handler(session, arg)


# ── server-side handlers ──────────────────────────────────────────
def _cmd_session(session: "WebSession", arg: str) -> dict:
    if arg == "clear":
        session.history.clear()
        return {"ok": True, "action": "clear",
                "text": "Session history cleared."}
    turns = len(session.history.context(limit=10000))
    tgt = session.target_hint()
    return {"ok": True, "text": f"Session: {turns} turns"
            + (f" · target {tgt}" if tgt else "")}


def _cmd_hint(session: "WebSession", arg: str) -> dict:
    if not arg:
        return {"ok": False, "text": "Usage: /hint <text>"}
    if not session.pentest_running:
        return {"ok": False,
                "text": "No pentest running. Start one in PENTEST mode first."}
    session.pentest_hint(arg)
    return {"ok": True, "text": f"Hint injected: {arg}"}


def _cmd_stop(session: "WebSession", arg: str) -> dict:
    session.pentest_stop()
    return {"ok": True, "text": "Stop requested."}


def _cmd_report(session: "WebSession", arg: str) -> dict:
    return session.build_report(arg)


def _cmd_crack(session: "WebSession", arg: str) -> dict:
    return session.crack_hash(arg)


def _cmd_cred(session: "WebSession", arg: str) -> dict:
    return session.manage_creds(arg)


def _cmd_login(session: "WebSession", arg: str) -> dict:
    return session.register_login(arg)


def _cmd_load(session: "WebSession", arg: str) -> dict:
    return session.load_session_file(arg)


_SERVER = {
    "/session": _cmd_session,
    "/hint": _cmd_hint,
    "/stop": _cmd_stop,
    "/report": _cmd_report,
    "/crack": _cmd_crack,
    "/cred": _cmd_cred,
    "/login": _cmd_login,
    "/load": _cmd_load,
}
