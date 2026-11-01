"""why a tool call may not run now: the lease is gone, the audit's limits, a held command's scripts or note changed."""

from __future__ import annotations
import hashlib
import os
from pathlib import Path

from probe.shared.mailbox import approvals as appr
from probe.shared.command_rules import command_rules as precheck
from probe.daemon.store.events import scrub
from probe.tap_core import secrets


NO_LEASE = "not run: this daemon no longer records this session"
#: What the team-note audit is told for a command that would need the researcher's
#: yes: the audit asks nothing (Richard 2026-10-11), so it does not run.
AUDIT_REFUSED = "not run: the team-note audit asks the researcher nothing, so a command that needs their yes does not run"
#: The team-note audit runs only `probe` reads: the daemon pulls the note before the
#: run and publishes the audit's copy after it (`audit.AuditLane`), under the
#: researcher's own credential -- a `notes sync` under the daemon's key would park
#: the researcher's note as another credential's (`team_note_file.paths`).
AUDIT_SYNC_IS_THE_DAEMONS = ("`probe notes sync` is the daemon's: it pulled the note into your copy and "
                             "publishes your copy when you end with final_result")


#: `probe` commands that read the open web, refused to the team-note audit as
#: their MCP tools are (`agent.audit_tool_refusal`): `paper find` is
#: `find_papers` from the shell and `docs` is `search_in=["docs"]`, and text from
#: outside the team must not reach an audit that publishes into every
#: teammate's instructions.
AUDIT_WEB_COMMANDS = frozenset({"paper find", "docs"})


def audit_probe_refusal(parsed: "precheck.Parsed") -> str | None:
    """None when the team-note audit may run this `probe` command; else why not."""
    if parsed.path in AUDIT_WEB_COMMANDS:
        from probe.daemon.agent.audit import AUDIT_WEB_REFUSED  # agent imports this module

        return AUDIT_WEB_REFUSED
    if parsed.owner == precheck.READ:
        return None
    if parsed.path == "notes sync":
        return f"not run: {AUDIT_SYNC_IS_THE_DAEMONS}."
    return f"{AUDIT_REFUSED} (`probe {parsed.path}` writes; the audit reads Probe only)."
#: Opens the logbook reason of an `edge remove` run without a question because
#: Probe says this researcher's daemon made the link (`_own_link`, lineage L9).
OWN_LINK_REASON = "own link (L9): "


def write_refusal(deps: Deps) -> str | None:
    """None while this process may act for the session; else the stop message
    every tool returns (A2, R11). Read fresh from disk on each call, never renewed
    here. The replay bench has no lease. Once Probe refused the daemon's key,
    every call stops."""
    if deps.reader:
        return None
    if deps.key_refused:
        reason = deps.stopped or "Probe refused the daemon's key"
    elif deps.replay is not None:
        return None
    else:
        from probe.daemon.host import lease

        reason = lease.may_write(deps.session_id)
        if reason is None:
            return None
    deps.stopped = reason
    return f"{NO_LEASE} ({reason}). Nothing is lost: whoever records next reads the chat log."


def held_refusal(deps: Deps, req: appr.Request) -> str | None:
    """What the worker checks right before it runs an action the researcher said
    yes to (G7, C1): this process may still act for the session, the held action
    is still the one they were asked about, and for the team note, the change it
    makes is still the one they were shown (the document re-read, G6). None: run it."""
    stop = write_refusal(deps)
    if stop is not None:
        return stop
    if not appr.verify_held(req):
        return f"not run: request {req.id} no longer matches what the researcher was asked - nothing was done."
    if req.policy == "team_note.edit":
        return _team_note_refusal(deps, req)
    if req.policy == "shell.unsafe_command":
        return _script_refusal(deps, req)
    return None


def _script_refusal(deps: Deps, req: appr.Request) -> str | None:
    """A held shell command runs files its words do not show: they must still be
    the files, with the text, the researcher was shown (hashed when asked)."""
    command, cwd = str(req.held.get("command") or ""), Path(req.held.get("cwd") or deps.cwd)
    now = _script_facts(deps, command, cwd)
    if isinstance(now, str):
        return f"{now.rstrip('.')} (request {req.id}); nothing was done"
    shown = [(s.get("path"), s.get("sha256")) for s in (req.facts or {}).get("scripts") or []]
    if [(s["path"], s["sha256"]) for s in now] != shown:
        return (f"not run: a script request {req.id} runs changed after the researcher was asked - nothing was "
                "done.")
    return None


#: A script that is not text, or bigger than this, is never asked about: the
#: question could not show it whole.
SCRIPT_BYTES = 4 * appr.SCRIPT_CHARS
_WRITES_NOTES_TAIL = " The daemon never runs what it can write."


def _script_facts(deps: Deps, command: str, cwd: Path) -> list[dict] | str:
    """What a held shell command runs besides its own words (`shell.held_scripts`):
    `[{"path", "sha256", "text"}]`, `sha256` None for a file that does not exist
    (yet). A refusal, as the tool's answer, when it runs a file in the notes
    folders, cannot be read, or runs a script the question could not show whole."""
    from probe.daemon import shell as sh

    inside = sh.names_writable(command, cwd=cwd, home=deps.home, folders=deps.write_dirs)
    if inside is not None:
        return f"not run: the command names {inside}, in the folders the daemon writes notes into.{_WRITES_NOTES_TAIL}"
    found = sh.held_scripts(command, cwd=cwd, home=deps.home)
    if found is None:
        return "not run: the daemon could not read which files the command runs (its quoting)."
    out: list[dict] = []
    total = 0
    for path in found:
        entry: dict = {"path": path, "sha256": None}
        if os.path.isfile(path):
            try:
                with open(path, "rb") as handle:
                    data = handle.read(SCRIPT_BYTES + 1)
            except OSError:
                return (f"not run: the command runs {path}, which the daemon can't show the researcher whole (it "
                        "can't be read).")
            try:
                text = data.decode("utf-8")
            except UnicodeDecodeError:
                text = "\0"
            total += len(text)
            if len(data) > SCRIPT_BYTES or "\0" in text or total > appr.SCRIPT_CHARS:
                return (f"not run: the command runs {path}, which the daemon can't show the researcher whole (it "
                        f"isn't text, or is longer than the {appr.SCRIPT_CHARS} characters a question shows).")
            if scrub(text) != text:
                return (f"not run: the command runs {path}, which the daemon can't show the researcher whole (it "
                        "looks like it contains a credential).")
            entry.update(sha256=hashlib.sha256(data).hexdigest(), text=text)
        out.append(entry)
    return out


def _team_note_refusal(deps: Deps, req: appr.Request) -> str | None:
    """Recompute what the held team-note change does NOW: the same text, from the
    same document, and still no credential in it. Anything else: refused, so the
    worker voids the yes."""
    changed = f"not run: the team note changed after the researcher was asked (request {req.id}) - nothing was done."
    held, facts = req.held or {}, req.facts or {}
    if held.get("kind") == "shell":
        verdict = _classify(deps, str(held.get("command") or ""), Path(held.get("cwd") or deps.cwd))
        if not (verdict.safe and verdict.note_target and _in_team_note(verdict.note_target)):
            return f"not run: request {req.id} is no longer a team note change - nothing was done."
        now, text = _team_note_write_facts(verdict), verdict.note_body or ""
    elif held.get("kind") == "probe":
        now = _team_note_sync_facts(deps)
        if now is None:
            return changed
        text = _read(_team_note_paths(deps)[0]) or ""
    else:
        return f"not run: request {req.id} is no longer a team note change - nothing was done."
    if any(now.get(k) != facts.get(k) for k in ("path", "text_sha", "before_sha", "diff")):
        return changed
    found = secrets.scan(text)
    if found:
        return (f"not run: the team note change of request {req.id} now looks like it contains a credential "
                f"({found[0].rule}) - nothing was done.")
    return None
from probe.daemon.agent.tools.probe_cli.config import _classify  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.team_note import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _in_team_note,
    _read,
    _team_note_paths,
    _team_note_sync_facts,
    _team_note_write_facts,
)
from probe.daemon.agent.tools.tools import Deps  # noqa: E402 -- pieces need each other; the front door loads this one first
