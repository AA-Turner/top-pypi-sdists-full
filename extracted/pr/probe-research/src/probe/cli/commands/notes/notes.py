"""probe notes show/find/checkout/push/write: read a note, or check it out as a file and push it back."""

from __future__ import annotations
import sys
import uuid
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from probe import analytics as probe_telemetry
    from ....sdk.client.client import Client
else:
    #: The SDK client class: a module global so the CLI package can monkeypatch
    #: it in tests, and None until then. The SDK client imports every wire model,
    #: so a command imports it when it builds one (`_client_class`), not at start.
    Client = None

import typer

from probe.cli.commands.commands import register_group
from ....sdk.settings.settings import resolve
from ....shared.reads import reads


# -- the project's notes file -------------------------------------------------
# One markdown file per project, read and written as text. This replaced a
# structured `probe note` command group whose kind vocabulary
# (intent/decision/observation/...), supersession and authority field were never
# validated or grouped by anything server-side -- eight kinds bought one list filter.
# Prose is what people write; a fixed filename is the only thing that needed inventing.
notes_app = typer.Typer(
    no_args_is_help=True,
    help="notes on a project, experiment or run (free-text markdown), main note and titled sub-notes",
)

#: `probe notes --help` order (notes, sub_notes, edit, fullness and team_note register them).
NOTES_GROUP = register_group(
    notes_app,
    (
        "show", "find", "checkout", "push", "write", "list", "create", "append", "edit", "rename",
        "delete", "status", "team", "audit-advisory", "sync",
    ),
)


def _notes_project(client: Client, project: str | None) -> tuple[str, str]:
    """(project_id, label) for a notes read/write (`reads.notes_project`)."""
    return reads.notes_project(_api(client), project)


#: The whole entity row a note lives on (`reads.entity_notes_row`).
_entity_notes_row = reads.entity_notes_row


@notes_app.command("show")
def notes_show(
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    note: str = typer.Option(
        None, "--note", help="print this titled SUB-NOTE instead (title, or id:<uuid>)"
    ),
) -> None:
    """Print an entity's notes — the main note, or one titled sub-note.

    Empty output means none were ever written. Historically project-only; the
    carrier flags arrived with sub-notes (0146) because a sub-note is reached
    through its entity and a reader should not need a different verb per kind.
    """
    with _client() as c:
        kind, entity_id, label = _note_target(
            c, project=project, experiment=experiment, run=run
        )
        if note is not None:
            found = _resolve_sub_note_by_title(c, kind, entity_id, note)
            document = c.get_sub_note(found["id"])
            text = document.get("body") or None
            label = f"{label} › {note}"
        else:
            document = _entity_notes_row(c, kind, entity_id)
            text = document.get("notes")
    if text is None or text == "":
        print(f"{label} has no notes yet", file=sys.stderr)
        return
    sys.stdout.write(text if text.endswith("\n") else text + "\n")
    # STDERR, beside the document rather than inside it: stdout is the note and
    # a script pipes it. Same channel and same reasoning as the write-path
    # headroom line, which this is the READ half of.

    # A SUB-NOTE spells the headroom `remaining_tokens`/`limit_tokens` while
    # the shared reader is written against the entity spelling, so an unadapted
    # sub-note read is silently advisory-free. `_sub_note_row_for_headroom`
    # exists for exactly this and is a no-op on an entity row.
    from ....sdk.reads.notes_cap import read_advisory

    document = _sub_note_row_for_headroom(document)
    advisory = read_advisory(document, version=document.get("notes_version"))
    if advisory is not None:
        print(f"{label}: {advisory}", file=sys.stderr)


@notes_app.command("find")
def notes_find(
    words: list[str] = typer.Argument(..., help="words to look for (any of them, case-insensitive)"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    note: str = typer.Option(
        None, "--note", help="look in this titled SUB-NOTE instead (title, or id:<uuid>)"
    ),
) -> None:
    """Print the paragraphs of an entity's note that mention any of WORDS.

    Each one verbatim under its section heading, with its line numbers, those
    mentioning more of the words first: what an edit quotes as its old text,
    without reading the whole note. Reads the current version, like `show`.
    """
    with _client() as c:
        printed = reads.notes_find(
            _api(c, pretty=sys.stdout.isatty()), list(words), project=project, experiment=experiment,
            run=run, note=note,
        )
    _emit(printed)


@notes_app.command("checkout")
def notes_checkout(
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    note: str = typer.Option(None, "--note", help="a titled SUB-NOTE (title, or id:<uuid>)"),
    steal: bool = typer.Option(
        False, "--steal", help="take the file even though it has unpushed edits"
    ),
) -> None:
    """Pull an entity's note to a file you can edit with ordinary tools.

    Prints the path. Edit that file the way you edit any markdown -- exact-match
    edits, not a re-typed document -- then `probe notes push`.

    The file lives in the state directory at 0600, not the working directory: a
    note keeps customer and commercial facts verbatim and a work tree is one
    `git add -A` from committing them. `push` finds it from the same
    `--run`/`--project` flag, so there is no path to remember.
    """
    from ....shared.notes import notes as notes_file
    from ....sdk.settings.settings import resolve

    with _client() as c:
        kind, entity_id, label = _note_target(
            c, project=project, experiment=experiment, run=run
        )
        if note is not None:
            found = _resolve_sub_note_by_title(c, kind, entity_id, note)
            row = c.get_sub_note(found["id"])
            body, version = row.get("body") or "", row.get("notes_version") or 0
            where = notes_file.paths_for(
                resolve(base_url=_conn.base_url), kind, entity_id, found["id"]
            )
            label = f"{label} \u203a {note}"
        else:
            row = _entity_notes_row(c, kind, entity_id)
            body, version = row.get("notes") or "", row.get("notes_version") or 0
            where = notes_file.paths_for(resolve(base_url=_conn.base_url), kind, entity_id)

    refusal = notes_file.claim(where, steal=steal)
    if refusal is not None:
        print(refusal, file=sys.stderr)
        raise typer.Exit(2)
    report = notes_file.checkout(where, body=body, version=version)
    print(f"checked out {kind} note ({label}) v{version}", file=sys.stderr)
    payload = {"target": kind, "label": label, "path": str(where.document), "version": version}
    if note is not None:
        # The title a script asked for, echoed back: a caller addressing a
        # sub-note needs to know WHICH document it got, and `label` glues the
        # entity and title together for humans rather than for `jq`.
        payload["note"] = note
    _print_json({**payload, **_headroom_fields(_sub_note_row_for_headroom(row))})
    # THE ADVISORY RIDES THE READ, which is the only point it can change what you
    # do. On the push it would arrive after the editing work was already done.
    # Through the SHARED reporter, so checkout says "warning:" exactly the way
    # every other notes surface does -- a second spelling of the same signal is
    # a second thing to grep for.
    _report_notes_headroom(_sub_note_row_for_headroom(row), kind, label)
    # The path is in the JSON above and on stderr below. It must NOT also go to
    # stdout as a bare line: `_print_json` exists so `probe notes checkout | jq`
    # works, and trailing text breaks exactly that.
    print(str(report.detail), file=sys.stderr)


@notes_app.command("push")
def notes_push(
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
    experiment: str = typer.Option(None, "--experiment", help="experiment slug or id"),
    run: str = typer.Option(None, "--run", help="run slug or id"),
    note: str = typer.Option(None, "--note", help="a titled SUB-NOTE (title, or id:<uuid>)"),
    force: bool = typer.Option(
        False, "--force", help="replace the server's document without merging"
    ),
) -> None:
    """Send the checked-out file back, merging if the note moved meanwhile.

    Exit 2 means a conflict was written into the file, or there was nothing safe
    to send: resolve the markers and push again. `--force` skips the merge and
    replaces whatever is on the server -- an operator escape hatch, never a step
    in a routine, because it deletes anything written since you checked out.
    """
    from ....shared.notes import notes as notes_file
    from ....sdk.settings.settings import resolve

    with _client() as c:
        kind, entity_id, label = _note_target(
            c, project=project, experiment=experiment, run=run
        )
        settings = resolve(base_url=_conn.base_url)
        if note is not None:
            found = _resolve_sub_note_by_title(c, kind, entity_id, note)
            sub_id = found["id"]
            where = notes_file.paths_for(settings, kind, entity_id, sub_id)
            label = f"{label} \u203a {note}"

            def send(text, base_version, op_key):
                row = c._replace_sub_note(sub_id, text, base_version=base_version, op_key=op_key)
                return (row or {}).get("notes_version", 0)

            def fetch():
                row = c.get_sub_note(sub_id)
                return row.get("body") or "", row.get("notes_version") or 0
        else:
            where = notes_file.paths_for(settings, kind, entity_id)

            def send(text, base_version, op_key):
                row = c._replace_notes(
                    kind, entity_id, text, base_version=base_version, op_key=op_key
                )
                return (row or {}).get("notes_version", 0)

            def fetch():
                row = _entity_notes_row(c, kind, entity_id)
                return row.get("notes") or "", row.get("notes_version") or 0

        report = notes_file.push(where, send=send, fetch=fetch, label=f"{kind} note", force=force)

    _print_json(
        {
            "target": kind,
            "label": label,
            "pushed": report.pushed,
            "merged": report.merged,
            "conflicted": report.conflicted,
            "version": report.version,
            "detail": report.detail,
        }
    )
    if report.detail:
        print(f"{label}: {report.detail}", file=sys.stderr)
    if report.pushed:
        _note_landed(kind, entity_id)
        print(f"pushed {kind} note ({label}) v{report.version}", file=sys.stderr)
        return
    # Exit 2 means SOMEONE HAS TO LOOK, matching `notes sync`, which exits 2 only
    # on a conflict. Nothing-to-do ("no local edits", "nothing checked out") is a
    # clean 0: a hook that treats a no-op as a failure is worse than useless. A
    # clean local merge is also 0 -- it succeeded, and its own detail says to push
    # again.
    raise typer.Exit(2 if report.conflicted else 0)


@notes_app.command("write")
def notes_write(
    file: str = typer.Argument(None, help="file to upload; omit or '-' to read stdin"),
    project: str = typer.Option(None, "--project", help="project slug (or id:<uuid>)"),
) -> None:
    """Replace the project's whole notes document.

    `--append` is gone with the span verbs (0.388.0.0). It sent `notes_append`,
    which the server now refuses -- a flag that always fails is worse than no
    flag. To ADD to a document without overwriting anyone, use the file model:
    `probe notes checkout` then `probe notes push`, which merges.

    This door replaces, and it carries no version, so it forces. Use it for a
    document you are authoring outright, not for adding a paragraph to one
    somebody else is also writing.
    """
    text = sys.stdin.read() if file in (None, "-") else Path(file).read_text()
    with _client() as c:
        project_id, label = _notes_project(c, project)
        # The replace verb, so the response carries the headroom this command
        # used to print only from the deleted `notes append`. It forces because
        # this door has no version in hand -- checkout/push is the one that merges.
        row = c._replace_notes(
            "project", project_id, text, base_version=None, op_key=uuid.uuid4().hex
        )
        stored = text
    print(f"wrote notes on project {label}", file=sys.stderr)
    # The stored length, not the document. Echoing the whole thing back on stdout
    # made `notes write` unpipeable and buried the one fact a caller wants, which is
    # that the server holds what was sent -- `notes show` is how you read it.
    _print_json({"project": label, "chars": len(stored), **_headroom_fields(row)})
    # A write door that cannot say the document is filling up makes fullness
    # invisible on the door people actually use.
    _report_notes_headroom(row, "project", label)
from probe.cli.commands.json_print import _emit, _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.notes.targets import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _headroom_fields,
    _note_landed,
    _note_target,
    _report_notes_headroom,
    _resolve_sub_note_by_title,
    _sub_note_row_for_headroom,
)
from probe.cli.commands.refs import _api  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client, _conn  # noqa: E402 -- pieces need each other; the front door loads this one first
