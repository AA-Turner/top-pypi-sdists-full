"""rows about local files: team-note sync and its parked copies, old snapshot refs, interrupted imports, dropped install extras."""

from __future__ import annotations
import json
import os



def _team_note_rows() -> list[str]:
    """Whether the team note is actually syncing on this machine.

    THE FAILURE THIS EXISTS FOR IS SILENT. The sync runs from session hooks, and
    hooks do not always run: Codex skips a hook whose hash changed until the
    researcher re-approves it, an MDM policy can disable non-managed hooks
    outright, and a plugin that was never installed has none. In every one of
    those cases the file simply stops syncing -- edits accumulate locally, the
    document the team reads never changes, and nothing anywhere reports it. The
    dirty flag below is the only place that turns that into something a person
    can see.
    """
    from ....sdk.settings.settings import resolve
    from ....shared.notes import team_note as team_note_file

    try:
        where = team_note_file.paths_for(resolve())
        document = where.document.read_text(encoding="utf-8") if where.document.exists() else None
        base = where.base.read_text(encoding="utf-8") if where.base.exists() else None
        meta = json.loads(where.meta.read_text(encoding="utf-8")) if where.meta.exists() else {}
    except (OSError, UnicodeDecodeError, ValueError):
        return ["Team note", _row("Local file", "unreadable")]

    rows = ["Team note", _row("Local file", str(where.document))]
    if document is None:
        rows.append(_row("State", "not seeded yet -- runs at the next session start"))
        rows.extend(_parked_rows(where))
        return rows
    rows.append(_row("Synced version", str(meta.get("version", "unknown"))))
    if base is not None and document != base:
        rows.append(
            _row(
                "Unsynced edits",
                "YES -- this file has local changes the team has not seen. "
                "`probe notes sync` sends them; if this persists, your session "
                "hooks are not running (`/hooks` on Codex re-approves them).",
            )
        )
    else:
        rows.append(_row("Unsynced edits", "none"))
    rows.extend(_parked_rows(where))
    return rows


def _snapshot_ref_rows(cwd: str | None = None) -> list[str]:
    """Old code-snapshot refs in the repo doctor runs in (plan 2.6).

    The once-per-repo capture notice can be missed (a script's stderr goes to a
    log nobody reads), so the count is also here, where someone looks when
    things are wrong. Nothing outside a git repo; never deletes (D10).
    """
    import os

    from ....sdk.capture import code as _snapshot

    try:
        here = cwd or os.getcwd()
        in_repo, reason = _snapshot._repo_check(here)
        if not in_repo:
            return ["Code capture", _row("Old snapshot refs", f"unknown ({reason})")] if reason else []
        refs = _snapshot.old_snapshot_refs(here)
    except Exception:  # noqa: BLE001 - a diagnostic must never crash
        return []
    if not refs:
        return ["Code capture", _row("Old snapshot refs", "none in this repo")]
    return [
        "Code capture",
        _row(
            "Old snapshot refs",
            f"{len(refs)} in this repo (refs/probe/snapshots/*, from earlier Probe "
            "versions; `git push --mirror` publishes them). Review with "
            "`probe snapshot-prune-refs --dry-run`.",
        ),
    ]


def _parked_rows(where) -> list[str]:
    """PARKED COPIES ARE TEXT NOBODY IS SENDING.

    The sync parks a leftover per-harness document, or one written under another
    credential, rather than deleting it -- so this is the one place a person can
    find out it is there and whose it is (the session-start hook tells the model;
    a headless machine has no such channel).

    Reported EVEN WHEN THE DOCUMENT IS ABSENT, which is the case that matters
    most: parking the only copy leaves no document at all, and a "not seeded
    yet" row with nothing after it reads as "nothing here" over text that is
    sitting on disk unsent.
    """
    from ....shared.notes import team_note as team_note_file

    try:
        parked = team_note_file.parked_copies(where)
    except Exception:  # noqa: BLE001 - a diagnostic must never be the thing that fails
        return []
    rows = []
    for path, owner, kind in parked:
        if owner is None:
            whose = (
                "no owner stamp -- unknown; read it before folding anything in, and check "
                "it is your team's"
            )
        elif owner != where.owner:
            whose = "a DIFFERENT credential -- another team's note; do not fold it in"
        elif kind == "legacy":
            whose = (
                "a leftover per-agent copy: read it, fold anything still true into the file "
                "above, then delete it. It is never sent on its own"
            )
        else:
            whose = "your own unsent work: it is taken back automatically on your next sync"
        rows.append(_row("Parked copy", f"{path} ({whose})"))
    return rows

def _interrupted_import_rows() -> list[str]:
    """Name any import this machine stopped part-way through.

    There is no boot service for background imports on purpose, so a machine
    that restarts mid-import leaves a job that is complete in every way except
    that nothing is running it. Its journals are intact and one menu entry
    resumes it -- but only for someone who already knows to look. This is a
    read of state that is already on disk, in the one command people run when
    they suspect something is wrong.
    """
    try:
        from ...imports import jobs as import_jobs

        stalled = [
            job for job in import_jobs.list_jobs()
            if job.get("state") == import_jobs.State.INTERRUPTED
        ]
    except Exception:  # noqa: BLE001 -- diagnostics must never fail the report
        return []
    if not stalled:
        return []
    label = "import" if len(stalled) == 1 else "imports"
    return [_row(
        "Unfinished work",
        f"{len(stalled)} {label} stopped part-way. Resume: `probe wizard --action imports`",
    )]


def _dropped_with_rows() -> list[str]:
    """The packages added beside the CLI (`uv tool install --with`) that an
    update had to leave out, and the exact command that adds them back
    (`updater.dropped_with_command`). Nothing when there are none."""
    try:
        from probe.cli.install import updater

        found = updater.dropped_with_command()
    except Exception:  # noqa: BLE001 -- a diagnostic line, never a failed doctor
        return []
    if not found:
        return []
    missing, command = found
    return [
        _row("Left out", f"{', '.join(missing)} (would not install beside the last update)"),
        _row("Add back", command),
    ]
from probe.shared.harness.diagnosis import _row  # noqa: E402 -- pieces need each other; the front door loads this one first
