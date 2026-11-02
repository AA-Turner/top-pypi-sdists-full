"""probe notes append/edit: change one exact piece of an entity note, a sub-note or the team note (--team)."""

from __future__ import annotations
import sys
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer

from .... import errors
from probe.cli.commands.notes.notes import notes_app


# The TEAM note is different: the server keeps two writes that compute the change
# itself under the note's row lock (`POST /v1/team-note/apply/paragraph|span`),
# so nothing is merged here. The note IS read first, for its version and text:
# that is what settles a write whose reply was lost. A session that has the
# team-note file edits it and `probe notes sync`s instead; these are for a
# caller with no file.

_TEAM_LABEL = "team note"


def _team_only(team: bool, **targets: object) -> None:
    """Refuse `--team` beside an entity flag or `--note`: one note per write."""
    if team and any(value is not None for value in targets.values()):
        raise typer.BadParameter(
            "--team writes the team note; drop --project/--experiment/--run/--note"
        )


def _team_topped_up(body: str, text: str) -> str:
    """The server's append (`app/team_notes/service.py::_topped_up`)."""
    return f"{body.rstrip()}\n\n{text.strip()}\n" if body.strip() else f"{text.strip()}\n"


def _write_team_note(
    c: Client, write: Callable[[], dict | None], expected: Callable[[str], str]
) -> dict:
    """Run a team-note write, retrying the one refusal that wrote nothing and
    says so (`retryable`: another write landed at the same instant).

    `expected(body)` is what the server stores when it applies this write to
    `body`; with the version read just before, it settles a reply that did not
    confirm the write. A credential that cannot read the note still writes, but
    such a reply is then reported as possibly landed."""
    for _ in range(_NOTE_REWRITE_ATTEMPTS):
        base: tuple[int, str] | None = None
        try:
            head = c.get_team_note()
        except (errors.ScopeError, ValueError):
            # No read scope, or a reply that was not JSON: write anyway, but a
            # reply that does not confirm the write cannot be settled.
            head = None
        if isinstance(head, dict) and _is_version(head.get("version")):
            base = (head["version"], head.get("body") or "")

        def read() -> tuple[dict, str, object]:
            row = c.get_team_note()
            if not isinstance(row, dict):
                raise ValueError("the reply was not a team note")
            return row, row.get("body") or "", row.get("version")

        def settle(why: _Unconfirmed) -> dict:
            if base is None:
                print(
                    f"error: {why.why}, and the {_TEAM_LABEL} could not be read before the "
                    "write to check against; the write may have landed. Read it (`probe "
                    "notes team`) before running this again.",
                    file=sys.stderr,
                )
                raise typer.Exit(1)
            return _settle_unconfirmed(
                read, base[0], expected(base[1]), _TEAM_LABEL, why=why, shown="probe notes team"
            )

        try:
            row = write()
        except errors.ConflictError as exc:
            if isinstance(exc.detail, dict) and exc.detail.get("retryable") is True:
                continue
            raise
        except errors.RosError as exc:
            why = _unconfirmed_reason(exc)
            if why is None:
                raise
            return settle(why)
        if not (isinstance(row, dict) and _is_version(row.get("version"))):
            return settle(_NO_VERSION_REPLY)
        return row
    print(
        "error: the team note kept changing while this wrote; nothing was written. "
        "Run it again.",
        file=sys.stderr,
    )
    raise typer.Exit(1)


def _team_payload(row: dict, **fields: object) -> dict:
    """A team-note write's JSON. `remaining` keeps its character meaning (the
    backstop now); the cap is in tokens, and its numbers ride beside it when the
    server published them (`_headroom_fields`'s keys, same rule)."""
    payload: dict[str, Any] = {"target": "team", "label": _TEAM_LABEL, **fields}
    payload["version"] = row.get("version")
    if isinstance(row.get("remaining_chars"), int):
        payload["remaining"] = row["remaining_chars"]
    for key, out in (
        ("tokens", "stored_tokens"),
        ("limit_tokens", "limit_tokens"),
        ("remaining_tokens", "remaining_tokens"),
    ):
        value = row.get(key)
        if isinstance(value, int) and not isinstance(value, bool):
            payload[out] = value
    return payload


def _refuse_edit_match(found: int, kind: str, label: str) -> None:
    """The refusal for an `--old` that does not match exactly once."""
    if found == 0:
        why = "matches nothing", "Copy it exactly from `probe notes show`"
    else:
        why = f"matches {found} places", "Add surrounding text until it matches once"
    print(
        f"error: --old {why[0]} in the {kind} note ({label}); nothing was "
        f"written. {why[1]}.",
        file=sys.stderr,
    )
    raise typer.Exit(1)


@notes_app.command("append")
def notes_append(
    text: str = typer.Option(..., "--text", help="the paragraph to add, as literal text"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    note: str = typer.Option(None, "--note", help="a titled SUB-NOTE (title, or id:<uuid>)"),
    team: bool = typer.Option(False, "--team", help="the TEAM note instead of an entity's"),
) -> None:
    """Add a paragraph to the end of a note: an entity's, one sub-note, or the team note.

    The text is taken literally (no @file, no stdin). It lands after a blank
    line, and anything a teammate wrote meanwhile is kept.
    """
    if not text.strip():
        raise typer.BadParameter("--text is empty")
    _team_only(team, project=project, experiment=experiment, run=run, note=note)
    if team:
        stored = _stored_form("text", text)
        with _client() as c:
            row = _write_team_note(
                c,
                lambda: c.append_team_note(text),
                lambda body: _team_topped_up(body, stored),
            )
        print(f"appended to the {_TEAM_LABEL}", file=sys.stderr)
        _print_json(_team_payload(row, chars=len(text)))
        return
    from ....sdk.reads.notes_cap import append_to_document

    def change(document: str) -> tuple[str, str, str]:
        joined = append_to_document(document, text)
        return joined[: len(joined) - len(text)], text, ""

    with _client() as c:
        kind, entity_id, sub_id, label = _note_carrier(
            c, project=project, experiment=experiment, run=run, note=note
        )
        row = _rewrite_note(c, kind, entity_id, sub_id, label, change, appending=True)
    _note_landed(kind, entity_id)
    print(f"appended to {kind} note ({label})", file=sys.stderr)
    payload: dict[str, Any] = {"target": kind, "label": label}
    if note is not None:
        payload["note"] = note
    payload.update({"chars": len(text), "version": row.get("notes_version")})
    _print_json({**payload, **_headroom_fields(row)})
    _report_notes_headroom(row, kind, label)


@notes_app.command("edit")
def notes_edit(
    old: str = typer.Option(..., "--old", help="the exact text to replace; must match once"),
    new: str = typer.Option(..., "--new", help="what replaces it ('' deletes it)"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    note: str = typer.Option(None, "--note", help="a titled SUB-NOTE (title, or id:<uuid>)"),
    team: bool = typer.Option(False, "--team", help="the TEAM note instead of an entity's"),
) -> None:
    """Replace one exact piece of a note: an entity's, one sub-note, or the team note.

    `--old` must appear exactly once, character for character; otherwise
    nothing is written and the command fails. Both values are literal text
    (no @file, no stdin).
    """
    if not old:
        raise typer.BadParameter("--old is empty")
    _team_only(team, project=project, experiment=experiment, run=run, note=note)
    _refuse_scrubbed_old(old)
    if team:
        stored_new = _stored_form("new_text", new)
        with _client() as c:
            try:
                row = _write_team_note(
                    c,
                    lambda: c.edit_team_note(old, new),
                    lambda body: body.replace(old, stored_new, 1),
                )
            except errors.ConflictError as exc:
                found = exc.detail.get("match_count") if isinstance(exc.detail, dict) else None
                if not isinstance(found, int):
                    raise
                _refuse_edit_match(found, "team", _TEAM_LABEL)
        print(f"edited the {_TEAM_LABEL}", file=sys.stderr)
        _print_json(_team_payload(row, removed=len(old), added=len(new)))
        return
    from ....sdk.reads.notes_cap import edit_match_count

    with _client() as c:
        kind, entity_id, sub_id, label = _note_carrier(
            c, project=project, experiment=experiment, run=run, note=note
        )

        def change(document: str) -> tuple[str, str, str]:
            found = edit_match_count(document, old)
            if found != 1:
                _refuse_edit_match(found, kind, label)
            at = document.index(old)
            return document[:at], new, document[at + len(old) :]

        row = _rewrite_note(c, kind, entity_id, sub_id, label, change, appending=False)
    if new:
        _note_landed(kind, entity_id)
    print(f"edited {kind} note ({label})", file=sys.stderr)
    payload: dict[str, Any] = {"target": kind, "label": label}
    if note is not None:
        payload["note"] = note
    payload.update(
        {"removed": len(old), "added": len(new), "version": row.get("notes_version")}
    )
    _print_json({**payload, **_headroom_fields(row)})
    # An edit is also how a note is compacted, so this line going quiet is how a
    # caller sees that a compaction worked.
    _report_notes_headroom(row, kind, label)
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.notes.rewrite import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _NOTE_REWRITE_ATTEMPTS,
    _NO_VERSION_REPLY,
    _Unconfirmed,
    _is_version,
    _note_carrier,
    _refuse_scrubbed_old,
    _rewrite_note,
    _settle_unconfirmed,
    _stored_form,
    _unconfirmed_reason,
)
from probe.cli.commands.notes.targets import _headroom_fields, _note_landed, _report_notes_headroom  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
