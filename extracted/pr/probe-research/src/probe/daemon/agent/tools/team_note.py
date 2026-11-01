"""hold a team-note write or `notes sync` as a question, with the whole diff."""

from __future__ import annotations
import difflib
import hashlib
import os
from pathlib import Path
from typing import Any

from probe.shared.mailbox import approvals as appr
from probe.shared.command_rules import command_rules as precheck
from probe.daemon.store.events import scrub


# ---------------------------------------------------------------------------
# The team note (D6): every change to it is shown to the researcher first.
# ---------------------------------------------------------------------------


def _team_note_paths(deps: Deps) -> tuple[Path, Path]:
    """The team note's document and the base copy it was last synced from, for
    the daemon's own credential (the CLI keys the base by backend + credential)."""
    from probe.shared.notes import team_note as team_note_file
    from probe.sdk.settings.settings import DEFAULT_BASE_URL

    # The same key `probe notes sync` computes from its resolved settings.
    origin = (deps.probe_env.get("PROBE_BASE_URL") or DEFAULT_BASE_URL).rstrip("/")
    paths = team_note_file.paths(origin=origin, identity=deps.probe_env.get("PROBE_TOKEN", ""))
    return paths.document, paths.base


def _in_team_note(target: str) -> bool:
    from probe.daemon.session.session import note_dirs

    folder = note_dirs()[-1]
    real = os.path.realpath(str(folder))
    return os.path.realpath(target).startswith(real.rstrip(os.sep) + os.sep)


def _read(path: Path | str) -> str | None:
    try:
        return Path(path).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return None


def _diff(before: str, after: str, name: str) -> str:
    """The whole change, never cut (G3): a yes publishes all of it, so all of it is
    shown (a long one only in `probe approvals`, `approvals._render_team_note`)."""
    return "\n".join(difflib.unified_diff(before.splitlines(), after.splitlines(), f"{name} (now)",
                                         f"{name} (after)", n=1, lineterm=""))


def _sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def _team_note_write_facts(verdict: Any) -> dict:
    """What a heredoc into the team note changes, from the file as it is NOW."""
    current = _read(verdict.note_target) or ""
    new = current + (verdict.note_body or "") if verdict.note_append else (verdict.note_body or "")
    return {"what": "an edit of this machine's copy, which the next sync publishes", "path": verdict.note_target,
            "diff": _diff(current, new, Path(verdict.note_target).name), "text_sha": _sha(new),
            "before_sha": _sha(current)}


def _team_note_sync_facts(deps: Deps) -> dict | None:
    """What `notes sync` would publish, from the document and its base as they are
    NOW; None when there is nothing to publish."""
    document, base = _team_note_paths(deps)
    text = _read(document)
    before = _read(base) or ""
    if text is None or text == before:
        return None
    return {"what": "publishing this machine's copy", "path": os.path.realpath(document),
            "diff": _diff(before, text, document.name), "text_sha": _sha(text), "before_sha": _sha(before)}


async def _hold_team_note_write(deps: Deps, command: str, verdict: Any, why: str) -> str:
    """A heredoc into the team note: the session hooks publish that file on their
    own, so the WRITE is the change, and it waits for the researcher's yes."""
    facts = _team_note_write_facts(verdict)
    facts["reason"] = why
    held = {"kind": "shell", "command": command, "cwd": str(deps.cwd), "op_id": _op_id(deps, shell_argv(command))}
    req = _hold(deps, policy="team_note.edit", facts=facts, held=held)
    if req.state == appr.DENIED:
        return _already_no(req)
    if req.state == appr.APPROVED:
        result = await _run_shell_write(deps, command, held["op_id"], head="team note", request=req.id)
        if result.exit_code != 0 and deps.stopped is None:
            deps.lost_writes += 1
        return f"[{appr.AUTO} · {_shell_status(result)}]\n{scrub(result.output)}"
    deps.store.log_write(bite=deps.bite_id, op_id=held["op_id"], argv=shell_argv(command), head="team note",
                         status="held", reason="a team note change waits for the researcher", request=req.id)
    return (f"held for the researcher (request {req.id}) - the team note reaches every teammate's agent. It is "
            "written if they say yes - then run `probe notes sync`.")


async def _maybe_hold_team_note_sync(deps: Deps, parsed: precheck.Parsed, op_id: str, why: str) -> str | None:
    """`probe notes sync` publishes the local team note. A local change nobody has
    said yes to is held (shown as the diff against what was last synced); a change
    the researcher already approved as a write goes ahead."""
    if parsed.params.get("pull_only"):
        return None
    facts = _team_note_sync_facts(deps)
    if facts is None:
        return None
    facts["reason"] = why
    fingerprint = appr.POLICIES["team_note.edit"].fingerprint(facts)
    if any(r.policy == "team_note.edit" and r.fingerprint == fingerprint
           for r in deps.board.all(session_id=deps.session_id, state=appr.APPROVED)):
        return None
    held = {"kind": "probe", "argv": parsed.argv, "op_id": op_id, "cwd": str(deps.cwd)}
    req = _hold(deps, policy="team_note.edit", facts=facts, held=held)
    if req.state == appr.DENIED:
        return _already_no(req)
    if req.state == appr.APPROVED:
        return None
    deps.store.log_write(bite=deps.bite_id, op_id=op_id, argv=["probe", *parsed.argv], head=parsed.path,
                         status="held", reason="a team note change waits for the researcher", request=req.id)
    return f"held for the researcher (request {req.id}) - publishing the team note. It runs if they say yes."
from probe.daemon.agent.tools.bash.bash import _run_shell_write, _shell_status  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.probe_cli.process import _op_id  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.daemon.agent.tools.tools import Deps, _already_no, _hold, shell_argv  # noqa: E402 -- pieces need each other; the front door loads this one first
