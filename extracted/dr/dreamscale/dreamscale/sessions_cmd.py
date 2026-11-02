"""dreamscale sessions — list and terminate your open sessions.

`sessions list` shows the authed user's non-terminal sessions as the standard
list table (tables); `sessions stop <id>` / `sessions stop --all` close them
(idempotent) so workers don't keep billing on zombie leases. Async inner + sync
wrapper, client close in finally.
"""

from __future__ import annotations

import asyncio
import json
from collections.abc import Callable
from typing import Any

from rich.text import Text

from dreamscale import errors, tables
from dreamscale.config import load_config
from dreamscale.control import ControlPlaneClient
from dreamscale.model_names import public_model

# A session's status as its user reads it: (label, tables kind).
STATUS_LABELS = {
    "queued": ("Queued", "active"),
    "starting": ("Starting", "active"),
    "ready": ("Ready", "ok"),
    "active": ("Running", "ok"),
    "resuming": ("Resuming", "active"),
    "closed": ("Closed", "idle"),
    "failed": ("Failed", "bad"),
}


def _format_elapsed(elapsed_s: Any) -> Text:
    """How long it has run since ready: `12m 04s`, `1h 32m`; not yet ready, a dash."""
    if elapsed_s is None:
        return tables.none()
    hours, rest = divmod(int(elapsed_s), 3600)
    minutes, seconds = divmod(rest, 60)
    return Text(f"{hours}h {minutes:02d}m" if hours else f"{minutes}m {seconds:02d}s")


def _format_table(sessions: list[dict], *, color: bool | None = None,
                  width: int | None = None) -> list[str]:
    columns = [
        tables.Column("SESSION", style="bold"),
        tables.Column("MODEL"),
        tables.Column("REGION", drop=2, style=tables.DIM),
        tables.Column("STATUS"),
        tables.Column("RUNNING", drop=1, justify="right"),
    ]
    rows = []
    for session in sessions:
        state = str(session.get("status") or "")
        label, kind = STATUS_LABELS.get(state, (state.replace("_", " ").capitalize(), "idle"))
        rows.append([session.get("session_id"), session.get("model"), session.get("region"),
                     tables.status(label, kind), _format_elapsed(session.get("elapsed_s"))])
    footer = [tables.hint(
        "Stop one: ", tables.command("dreamscale sessions stop <session>"),
        "   ·   all of them: ", tables.command("dreamscale sessions stop --all"),
    )]
    return tables.render("Sessions", f"{len(sessions)} open", columns, rows, footer=footer,
                         color=color, width=width)


async def _list_sessions(client_factory: Callable[..., Any], config) -> list[dict]:
    client = client_factory(config.control_plane_url, config.api_key)
    try:
        sessions = await client.list_sessions()
    finally:
        await client.close()
    # Display only: name each session's model as users know it (model_names).
    return [
        {**session, "model": public_model(session["model"])} if session.get("model") else session
        for session in sessions
    ]


def run_sessions(*, client_factory: Callable[..., Any] = ControlPlaneClient,
                 print_fn: Callable[[str], None] = print,
                 json_output: bool = False) -> list[dict]:
    config = load_config()
    if not config.api_key:
        raise errors.catalog("not_configured")

    sessions = asyncio.run(_list_sessions(client_factory, config))

    if json_output:
        print_fn(json.dumps(sessions, indent=2, sort_keys=True))
        return sessions

    if not sessions:
        print_fn("No open sessions.")
        return sessions
    for line in _format_table(sessions):
        print_fn(line)
    return sessions


async def _stop(client_factory: Callable[..., Any], config, *,
                session_id: str | None, stop_all: bool,
                print_fn: Callable[[str], None]) -> None:
    client = client_factory(config.control_plane_url, config.api_key)
    try:
        if stop_all:
            sessions = await client.list_sessions()
            if not sessions:
                print_fn("No open sessions.")
                return
            for session in sessions:
                sid = session["session_id"]
                await client.delete_session(sid)
                print_fn(f"Stopped {sid}")
            print_fn(f"Stopped {len(sessions)} session(s).")
        else:
            await client.delete_session(session_id)
            print_fn(f"Stopped {session_id}")
    finally:
        await client.close()


def run_stop(*, session_id: str | None = None, stop_all: bool = False,
             client_factory: Callable[..., Any] = ControlPlaneClient,
             print_fn: Callable[[str], None] = print) -> None:
    config = load_config()
    if not config.api_key:
        raise errors.catalog("not_configured")

    if not stop_all and not session_id:
        raise errors.DreamscaleError(errors.ErrorInfo(
            code="stop_needs_target",
            problem="dreamscale sessions stop needs a session id (or --all)",
            cause="no session id was given and --all was not set",
            fix="pass a session id from `dreamscale sessions list`, or use --all to stop "
            "every open session",
        ))

    asyncio.run(_stop(
        client_factory, config,
        session_id=session_id, stop_all=stop_all, print_fn=print_fn,
    ))
