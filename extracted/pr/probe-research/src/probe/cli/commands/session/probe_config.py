"""the .probe.config answers: probe ignore check and probe session parent."""

from __future__ import annotations
import os
import sys

import typer
from ....sdk import agent_session, session_marker
from probe.cli.commands.session.session import _probe_config_block, _resolve_agent_session, session_app


@session_app.command("parent")
def session_parent(
    value: str = typer.Argument(None, help="follow | ignore - omit to show"),
    session: str = typer.Option(None, "--session", help="session id (defaults to this one)"),
) -> None:
    """The researcher's answer about `.probe.config` files ABOVE where this
    session started: `follow` them (the default until answered) or `ignore`
    them for this session. Files at or below the launch folder always apply.

    From an agent session it runs only with `--directed`, after the researcher
    answered. Asked again when one of those files changes."""
    resolved = _resolve_agent_session(session)
    pc = session_marker.probe_config()
    if value is not None:
        word = value.strip().lower()
        if word not in (pc.FOLLOW, pc.IGNORE):
            print(f"expected follow or ignore, got {value!r}", file=sys.stderr)
            raise typer.Exit(1)
        if not session_marker.valid_session_id(resolved):
            print(f"not a session id: {resolved!r}", file=sys.stderr)
            raise typer.Exit(1)
        ok, _parents = pc.record_answer(session_marker.sessions_dir(), resolved, word)
        if not ok:
            print("could not record the answer", file=sys.stderr)
            raise typer.Exit(1)
    _print_json({"session_id": resolved, **_probe_config_block(resolved)})


ignore_app = typer.Typer(
    no_args_is_help=True, help=".probe.config: what Probe may read and record, per path (gitignore syntax)"
)


@ignore_app.command("check")
def ignore_check(
    paths: list[str] = typer.Argument(..., help="paths to test"),
) -> None:
    """Each path's `.probe.config` level (`on`, `read`, `hash`, `off`) and the
    line that set it, as this session sees it (files above its launch folder
    count unless set aside). `excluded`: Probe records nothing about it as usual
    (`read`, `hash` or `off`); `identity_only`: the SDK records its identity
    (path, hash, size, rows) and nothing else (`hash`)."""
    pc = session_marker.probe_config()
    sid = agent_session.session_id_from_env()
    rows = []
    for raw in paths:
        verdict = session_marker.excluded(raw, sid)
        set_by = verdict.rule is not None
        rows.append(
            {
                "path": pc.shown(os.path.abspath(os.path.expanduser(raw))),
                "level": getattr(verdict, "level", "off" if verdict.excluded else "on"),
                "excluded": verdict.excluded,
                "identity_only": bool(getattr(verdict, "identity_only", False)),
                "source": session_marker.verdict_source(verdict) if set_by else None,
                "at": pc.shown(verdict.at) if set_by and verdict.at else None,
            }
        )
    _print_json(rows[0] if len(rows) == 1 else rows)
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
