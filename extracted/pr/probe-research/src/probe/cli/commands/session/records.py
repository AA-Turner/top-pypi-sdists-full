"""what Probe holds of a session: probe session owed/export/send/delete/undelete."""

from __future__ import annotations
import json
import os
import sys
from pathlib import Path

import typer

from .... import errors
from ....sdk import agent_session, session_marker
from probe.cli.commands.session.session import _resolve_agent_session, session_app


@session_app.command("owed", hidden=True)
def session_owed(
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
    send_back: bool = typer.Option(
        False, "--send-back", help="print what an inline agent is sent back with, and count it"
    ),
) -> None:
    """What this session still owes (notes parity N3, `owed`): a summary for a
    project or experiment it created or concluded, a note on a run it tagged
    invalid. `--send-back`: in an inline session only, the words the agent is
    sent back with at the end of its turn, each item at most twice, else
    nothing. Host-facing (the plugin's Stop hook, pi's extension), so hidden."""
    from ....shared.notes import owed

    resolved = _resolve_agent_session(session, read=True)
    if not session_marker.valid_session_id(resolved):
        print(f"error: not a session id: {resolved!r}", file=sys.stderr)
        raise typer.Exit(1)
    if send_back:
        text = owed.send_back(resolved) if session_marker.is_inline(resolved) else None
        if text:
            print(text)
        return
    _print_json({"session": resolved, "owed": [
        {k: item.get(k) for k in ("why", "kind", "ref", "by")} for item in owed.owed(resolved)
    ]})


@session_app.command("export")
def session_export(
    session_id: str = typer.Argument(..., help="the captured session's id"),
    source: str = typer.Option(
        None, "--source", help="the agent that recorded it, as its harness id (default: each in turn)"
    ),
    out: Path = typer.Option(None, "--out", "-o", help="write the ATIF JSON here instead of stdout"),
) -> None:
    """A captured session as one ATIF trajectory document (Harbor's Agent
    Trajectory Interchange Format), readable by Harbor, Phoenix and Transluce.

    Written by Probe when the session ends; a session still running has none
    yet. The trajectory never carries tool arguments or tool output.
    """
    from probe.foundation.harness_registry import get_registry

    # `source` is part of the document's identity: an unnamed one is asked of
    # each captured agent in turn, never defaulted (a default would read every
    # other agent's session as "not found").
    candidates = [source] if source else [h.id for h in get_registry().captured()]
    document = None
    with _client() as c:
        for candidate in candidates:
            try:
                document = c.export_session_trajectory(session_id, source=candidate)
                break
            except errors.NotFoundError as exc:
                if isinstance(exc.detail, dict) and exc.detail.get("error") == "trajectory_unavailable":
                    raise  # the session exists under this agent; it has no trajectory yet
    if document is None:
        raise errors.NotFoundError(
            f"no captured session {session_id} under "
            + (source or f"any known agent ({', '.join(candidates)})"),
            status=404,
        )
    if out is None:
        _print_json(document)
        return
    out.write_text(json.dumps(document, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    typer.echo(f"wrote {out} ({len(document.get('steps') or [])} steps)")


@session_app.command("send")
def session_send(
    session_id: str = typer.Argument(..., help="the session to message: one of your own, its id"),
    text: str = typer.Argument(..., help="the message, at most 2,000 characters"),
) -> None:
    """Send a message to one of your own running agent sessions.

    Its Probe daemon puts it in the agent's mailbox within about 30 s; the
    agent reads it at its next prompt or tool call (an idle Claude Code or pi
    is woken). Sent from here it reads as from one of your agent sessions,
    never as from you: only the dashboard speaks as you. A session with no
    Probe daemon (Probe off, inline, headless `-p`) cannot be reached; `state`
    then says `unreachable`.
    """
    with _client() as c:
        _print_json(c.send_session_message(session_id, text))


#: `probe session delete|undelete` from inside a coding agent's shell, or run by
#: the Probe daemon (R24).
SESSION_DELETE_FROM_AGENT = (
    "`probe session {verb}` was refused: it runs inside a coding agent's session, and only the "
    "researcher deletes or restores a captured session, from a terminal outside the agent. "
    "Nothing changed."
)


def _refuse_session_deletion_from_agent(verb: str) -> None:
    """The researcher's own command, refused before any request when a coding
    agent's session variable is set (the `INLINE_FROM_AGENT` test: however the
    call was wrapped) or the Probe daemon runs it (`PROBE_DAEMON_SESSION`).
    A speed bump, not the boundary: the server refuses the daemon's and the
    assistant's credentials, and the 7-day undo and the owner's email are what
    stand behind an agent holding the person's own key (research-os R33)."""
    if agent_session.session_id_from_env() or os.environ.get(agent_session.DAEMON_SESSION_ENV):
        print(SESSION_DELETE_FROM_AGENT.format(verb=verb), file=sys.stderr)
        raise typer.Exit(2)


@session_app.command("delete")
def session_delete(
    session_id: str = typer.Argument(..., help="the captured session's id, a lowercase UUID"),
) -> None:
    """Delete one of your captured sessions: its transcript, and what Probe
    derived from it.

    It is hidden from search at once and deleted for good after 7 days; until
    then `probe session undelete <id>` brings it back. You are emailed when you
    ask. Only your own sessions, and only from a terminal outside a coding
    agent: you type the id's first 8 characters back to confirm. Run again on a
    session already asked for, it prints where that deletion stands.
    """
    _refuse_session_deletion_from_agent("delete")
    with _client() as c:
        preview = c.delete_session(session_id, dry_run=True)
        if preview.get("state") is not None:
            # Already asked: where it stands, never a second request.
            _print_json(preview)
            return
        seen = ", ".join(
            f"{label} {preview[key]}"
            for label, key in (("first seen", "first_seen_at"), ("last seen", "last_seen_at"))
            if preview.get(key)
        )
        print(
            f"{preview.get('agent')} session {session_id}" + (f" ({seen})" if seen else "") + ".\n"
            + str(preview.get("note") or ""),
            file=sys.stderr,
        )
        confirm = session_id[:8]
        typed = typer.prompt(
            f"Type {confirm} to delete it", default="", show_default=False, err=True
        )
        if typed.strip() != confirm:
            print("not confirmed: nothing changed", file=sys.stderr)
            raise typer.Exit(1)
        _print_json(c.delete_session(session_id))


@session_app.command("undelete")
def session_undelete(
    session_id: str = typer.Argument(..., help="the session you asked to delete"),
) -> None:
    """Undo `probe session delete` while its 7 days are open: nothing was
    deleted, and the session is back in search. Refused once the deletion has
    started."""
    _refuse_session_deletion_from_agent("undelete")
    with _client() as c:
        _print_json(c.undelete_session(session_id))
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
