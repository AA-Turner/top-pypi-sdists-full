"""probe notes list/create/rename/delete: titled sub-notes."""

from __future__ import annotations
import sys
from pathlib import Path

import typer

from .... import errors
from probe.cli.commands.notes.notes import notes_app


@notes_app.command("list")
def notes_list(
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
) -> None:
    """List an entity's titled sub-notes: title, fullness, when. No bodies —
    `probe notes show --note <title>` reads one.

    Fullness is `stored_tokens` of `limit_tokens`, the cap a write is refused
    at; `stored_tokens` is null when the server has not counted the sub-note.
    `stored_chars` / `limit` keep their character meaning (the backstop)."""
    with _client() as c:
        kind, entity_id, label = _note_target(
            c, project=project, experiment=experiment, run=run
        )
        try:
            page = c.list_sub_notes(kind, entity_id)
        except errors.RosError as exc:
            _sub_notes_supported(exc)
            raise
    _print_json(
        {
            "target": kind,
            "label": label,
            "limit_count": page.get("limit_count"),
            "sub_notes": [
                {
                    "id": row.get("id"),
                    "title": row.get("title"),
                    "stored_tokens": row.get("tokens"),
                    "limit_tokens": row.get("limit_tokens"),
                    "stored_chars": row.get("chars"),
                    "limit": row.get("limit_chars"),
                    "updated_at": row.get("updated_at"),
                }
                for row in page.get("sub_notes", [])
            ],
        }
    )


@notes_app.command("create")
def notes_create(
    title: str = typer.Option(..., "--title", help="the new sub-note's tab label"),
    file: str = typer.Argument(
        None, help="optional starting body; omit for a titled empty tab, '-' for stdin"
    ),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
) -> None:
    """Create a titled sub-note. Duplicate titles are legal (tabs key on id)
    but a title-addressed write to a duplicated title is refused — check
    `probe notes list` first rather than collecting rename chores."""
    body = ""
    if file is not None:
        body = sys.stdin.read() if file == "-" else Path(file).read_text()
    with _client() as c:
        kind, entity_id, label = _note_target(
            c, project=project, experiment=experiment, run=run
        )
        try:
            row = _notes_write(
                kind,
                f"{label} › {title}",
                lambda: c._create_sub_note(kind, entity_id, title, body),
            )
        except errors.RosError as exc:
            _sub_notes_supported(exc)
            raise
    row = _sub_note_row_for_headroom(row)
    if body:
        _note_landed(kind, entity_id)
    print(f"created {kind} sub-note {title!r} ({label})", file=sys.stderr)
    payload = {"target": kind, "label": label, "title": title, "chars": len(body)}
    if isinstance(row, dict):
        payload["id"] = row.get("id")
    _print_json({**payload, **_headroom_fields(row)})


@notes_app.command("rename")
def notes_rename(
    note: str = typer.Option(..., "--note", help="the sub-note's current title, or id:<uuid>"),
    to: str = typer.Option(..., "--to", help="its new title"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
) -> None:
    """Rename a sub-note. Records no version — history tracks documents, not
    labels — and it is also how a duplicated title gets un-ambiguous again."""
    with _client() as c:
        kind, entity_id, label = _note_target(
            c, project=project, experiment=experiment, run=run
        )
        row = _resolve_sub_note_by_title(c, kind, entity_id, note)
        c._rename_sub_note(row["id"], to)
    print(f"renamed {kind} sub-note {note!r} -> {to!r} ({label})", file=sys.stderr)
    _print_json({"target": kind, "label": label, "id": row.get("id"), "title": to})


@notes_app.command("delete")
def notes_delete(
    note: str = typer.Option(..., "--note", help="the sub-note's title, or id:<uuid>"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation prompt"),
) -> None:
    """Permanently delete a sub-note AND its version history. Requires a
    credential with the `delete` scope, like every other delete here."""
    with _client() as c:
        kind, entity_id, label = _note_target(
            c, project=project, experiment=experiment, run=run
        )
        row = _resolve_sub_note_by_title(c, kind, entity_id, note)
        if not yes:
            if not typer.confirm(
                f"permanently delete {kind} sub-note {note!r} ({label}) and its history?"
            ):
                raise typer.Exit(1)
            # The prompt may have sat open while another session renamed or
            # removed this id; a confirm given for title X must not destroy a
            # document that is now something else. Re-read before acting.
            try:
                current = c.get_sub_note(row["id"])
            except errors.RosError as exc:
                if exc.status == 404:
                    print("error: that sub-note was deleted meanwhile", file=sys.stderr)
                    raise typer.Exit(1) from exc
                raise
            if _sub_note_id_ref(note) is None and current.get("title") != note.strip():
                print(
                    f"error: that sub-note is now titled {current.get('title')!r} — "
                    "re-run against the current title (or `--note id:...`)",
                    file=sys.stderr,
                )
                raise typer.Exit(1)
        c._delete_sub_note(row["id"])
    print(f"deleted {kind} sub-note {note!r} ({label})", file=sys.stderr)
    _print_json({"target": kind, "label": label, "id": row.get("id"), "deleted": True})
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.notes.rewrite import _notes_write  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.notes.targets import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _headroom_fields,
    _note_landed,
    _note_target,
    _resolve_sub_note_by_title,
    _sub_note_id_ref,
    _sub_note_row_for_headroom,
    _sub_notes_supported,
)
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
