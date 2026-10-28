"""Note edits never sent, found and sent before an uninstall (clean-uninstall U-T5, D1 = A).

An agent edits the team note, an entity's note or a summary as a local file
(`team_note_file`, `notes_file`, `probe summary`) and the hooks send it at the
next Stop. An edit that was never sent is the researcher's unsent work, as a
queued write is: the uninstall tries to send it (bounded, in the drain step)
and counts what is still unsent with the outbox, so the D1 rule applies to it
(asked, saved to the backup file, or `--discard-unsent`), never deleted
silently.

    team note   `<state>/team-note/probe-team-note.md` that differs from the
                base copy of the credential that wrote it (its `.owner`
                stamp), and every parked copy (`*.unsynced-<stamp>`, one per
                copy: its `.owner`/`.base`/`.meta` sidecars are not copies):
                text a switched credential set aside, by definition never sent
    notes       `<state>/notes/<kind>/<uuid>/note.md` and `.../sub/<id>.md`
                that differ from their `.base`
    summaries   `<state>/summaries/<kind>/<uuid>/<session>.md|.html` that
                differ from their `.base` (counted apart, as drafts, and never
                sent here: a draft belongs to the session that checked it out,
                so only --discard-unsent or the backup file gets past one)

Sending reuses the commands' own pushes (`team_note_file.push`,
`notes_file.push`), with this machine's credential, inside the caller's deadline.
"""

from __future__ import annotations

import contextlib
from dataclasses import dataclass
from pathlib import Path

TEAM_NOTE = "team note"
NOTE = "note"
SUB_NOTE = "sub-note"
SUMMARY = "summary"
#: The entity kinds a note is filed under (`notes_file.paths_for`).
NOTE_KINDS = ("project", "experiment", "run")


@dataclass(frozen=True)
class Edit:
    kind: str
    path: Path
    #: (entity kind, entity id, sub-note id or None) for a note; None otherwise.
    target: tuple | None = None


def _text(path: Path) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        return None
    except (OSError, UnicodeDecodeError):
        return "\0unreadable"  # unknown is never "clean"


def _differs(document: Path, base: Path) -> bool:
    text = _text(document)
    if text is None or not text.strip():
        return False
    return text != (_text(base) or "")


def _team_note(root: Path) -> list[Edit]:
    from probe.cli import team_note_file

    folder = root / "team-note"
    document = folder / team_note_file.DOCUMENT_NAME
    out = []
    stamp = (_text(document.with_name(document.name + ".owner")) or "").strip()
    if document.is_file() and stamp and _differs(document, folder / stamp / "base.md"):
        out.append(Edit(TEAM_NOTE, document))
    with contextlib.suppress(OSError):
        for parked in sorted(folder.glob(f"{team_note_file.DOCUMENT_NAME}.unsynced-*")):
            # One per parked edit: its `.owner`, `.base` and `.meta` travel with it.
            if parked.name.endswith(team_note_file.PARKED_SIDECARS):
                continue
            if parked.is_file() and (_text(parked) or "").strip():
                out.append(Edit(TEAM_NOTE, parked))
    return out


def _notes(root: Path) -> list[Edit]:
    out = []
    for kind in NOTE_KINDS:
        with contextlib.suppress(OSError):
            for entity in sorted((root / "notes" / kind).iterdir()):
                if not entity.is_dir():
                    continue
                note = entity / "note.md"
                if _differs(note, entity / "note.base"):
                    out.append(Edit(NOTE, note, (kind, entity.name, None)))
                with contextlib.suppress(OSError):
                    for sub in sorted((entity / "sub").glob("*.md")):
                        if _differs(sub, sub.with_suffix(".base")):
                            out.append(Edit(SUB_NOTE, sub, (kind, entity.name, sub.stem)))
    return out


def _summaries(root: Path) -> list[Edit]:
    out = []
    with contextlib.suppress(OSError):
        for draft in sorted((root / "summaries").rglob("*")):
            if draft.suffix in (".md", ".html") and draft.is_file() and _differs(draft, draft.with_suffix(".base")):
                out.append(Edit(SUMMARY, draft))
    return out


def unsynced() -> list[Edit]:
    """Every note edit on this computer the server has not got."""
    from probe.cli import uninstall_plan

    out: list[Edit] = []
    for root in uninstall_plan.state_roots():
        out += _team_note(root) + _notes(root) + _summaries(root)
    return out


def send(deadline: float, lines: list[str]) -> None:
    """Push the team note and every entity note with unsent edits, within
    `deadline` (`time.monotonic()`). What could not be sent stays for the D1
    rule; nothing here deletes or overwrites an edit."""
    import time

    edits = [e for e in unsynced() if e.kind in (TEAM_NOTE, NOTE, SUB_NOTE)]
    if not edits or time.monotonic() >= deadline:
        return
    from probe.cli import team_note_file
    from probe.sdk.config import resolve
    from probe.sdk.transport import deadline_scope

    settings = resolve()
    if not settings.token:
        return
    from probe.cli.main import _client

    sent = 0
    try:
        with deadline_scope(deadline), _client() as client:
            for edit in edits:
                if time.monotonic() >= deadline:
                    break
                with contextlib.suppress(Exception):
                    if edit.kind == TEAM_NOTE and edit.path.name == team_note_file.DOCUMENT_NAME:
                        report = team_note_file.push(client, team_note_file.paths_for(settings))
                    elif edit.kind in (NOTE, SUB_NOTE):
                        report = _push_note(client, settings, edit)
                    else:
                        continue  # a parked copy is another credential's: never sent with this one
                    sent += bool(report.pushed)
    except Exception as exc:  # noqa: BLE001 - what is left is counted, never lost
        lines.append(f"! could not send note edits: {type(exc).__name__}")
    if sent:
        lines.append(f"Sent {sent} note edit(s).")


def _push_note(client, settings, edit: Edit):
    from probe.cli import notes_file
    from probe.cli.main import _entity_notes_row

    kind, entity_id, sub_id = edit.target
    if sub_id is not None:
        where = notes_file.paths_for(settings, kind, entity_id, sub_id)

        def send_text(text, base_version, op_key):
            row = client._replace_sub_note(sub_id, text, base_version=base_version, op_key=op_key)  # noqa: SLF001
            return (row or {}).get("notes_version", 0)

        def fetch():
            row = client.get_sub_note(sub_id)
            return row.get("body") or "", row.get("notes_version") or 0
    else:
        where = notes_file.paths_for(settings, kind, entity_id)

        def send_text(text, base_version, op_key):
            row = client._replace_notes(kind, entity_id, text, base_version=base_version, op_key=op_key)  # noqa: SLF001
            return (row or {}).get("notes_version", 0)

        def fetch():
            row = _entity_notes_row(client, kind, entity_id)
            return row.get("notes") or "", row.get("notes_version") or 0

    return notes_file.push(where, send=send_text, fetch=fetch, label=f"{kind} note")
