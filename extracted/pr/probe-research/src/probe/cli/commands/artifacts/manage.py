"""probe artifact set/move/list/tree/versions/pin-impact/version-add/delete/gc-uploads."""

from __future__ import annotations

import typer
# The option enums only, from `_generated.enums` rather than `probe.models`: that
# seam builds every wire model, ~0.5 s that every command paid at startup -- the
# wizard, the hooks and the status line included -- whether or not it sent one.
# `tests/test_cli_startup_imports.py` holds the CLI to this.
from ....generated.enums import AnchorLevel
from ....sdk.artifact.anchors import Anchor
from ....sdk.reads.notes_cap import FILE_NOTES_REMOVED
from .. import ref_syntax as refs
from probe.cli.commands.artifacts.artifacts import artifact_app


@artifact_app.command("set", hidden=True)
def artifact_set(
    artifact_id: str = typer.Argument(None, metavar="{artifact}", help="artifact id"),
    notes: str = typer.Option(None, "--notes", help="removed: files no longer carry notes"),
) -> None:
    """Removed: a file's one-line note. Files no longer carry notes, and `--notes`
    was this command's only option, so it is kept only to say so.

    Say what a file is, and where it lives, in its run's notes (`probe notes
    append --run RUN --text ...`). Nothing is sent and it exits 1."""
    typer.echo(
        f"error: `probe artifact set` was removed: {FILE_NOTES_REMOVED} "
        "(`probe notes append --run RUN --text ...`)",
        err=True,
    )
    raise typer.Exit(1)


@artifact_app.command("move")
def artifact_move(
    artifact_id: str = typer.Argument(
        ..., help="artifact id — artifacts have no slug, so this is a UUID"
    ),
    to: AnchorLevel = typer.Option(
        ...,
        "--to",
        help="the level to move it to: run | experiment | project",
    ),
    target: str = typer.Option(
        None,
        "--target",
        metavar="REF",
        help="the entity at --to to land on: a slug, id:<uuid>, or a run petname. "
        "Omit to PROMOTE up this artifact's own chain, where the target follows "
        "from where it already hangs",
    ),
) -> None:
    """Move an artifact to another level, keeping its id.

    Promote up (``--to`` above where it hangs now) needs no ``--target``: the
    destination follows from the artifact's own run -> experiment -> project
    chain. Demoting down needs ``--target``, because a project has many
    experiments and only the caller knows which. A lateral move — one project to
    another — is the same call with ``--to project --target OTHER``.

    WHAT THIS COMMAND DOES NOT DO is decide which of those the server allows.
    The rules live in one place, server-side, and they are moving: lateral is
    landing on the backend now. A client-side copy of them would either reject a
    move the server has just started accepting, or invent a reason of its own for
    one it refuses. So the level and the target go straight through, and a 422 or
    409 is printed exactly as the server worded it.
    """
    with _client() as c:
        target_id = None
        if target is not None:
            if to is AnchorLevel.run:
                target_id = refs.resolve_run(c, target).id
            else:
                target_id = refs.resolve(c, to.value, target).id
        _print_json(c.move_artifact(artifact_id, level=to.value, target_id=target_id))


@artifact_app.command("list")
def artifact_list(
    run: str = typer.Argument(None, help="run id — omit when using an anchor flag"),
    kind: str = typer.Option(None, "--kind", help="run anchor only"),
    step_from: int = typer.Option(None, "--step-from", help="run anchor only"),
    step_to: int = typer.Option(None, "--step-to", help="run anchor only"),
    project: str = typer.Option(None, "--project"),
    experiment: str = typer.Option(None, "--experiment"),
    workspace: str = typer.Option(None, "--workspace"),
    shared: bool = typer.Option(False, "--shared"),
) -> None:
    """List artifacts under an anchor. Run listing is server-filtered by step window."""
    anchor, anchor_id = _pick_anchor(
        run=run, project=project, experiment=experiment, workspace=workspace, shared=shared
    )
    with _client() as c:
        if anchor is Anchor.RUN:
            _print_json(
                c.list_run_artifacts(
                    # UUID-typed route, same as `span list` -- and the run anchor is
                    # the one anchor whose ref is normally typed as a petname.
                    _ref(c, "run", anchor_id).id,
                    kind=kind,
                    step_from=step_from,
                    step_to=step_to,
                )
            )
            return
        if kind or step_from is not None or step_to is not None:
            raise typer.BadParameter(
                f"--kind/--step-from/--step-to are run-only filters; "
                f"the {anchor.value} listing does not accept them"
            )
        _print_json(c.list_anchored(anchor, _anchor_id_for(c, anchor, anchor_id)))


@artifact_app.command("tree")
def artifact_tree(
    run: str = typer.Argument(..., help="run id or petname"),
    prefix: str = typer.Option("", "--prefix", help="folder path; empty is the root"),
    limit: int | None = typer.Option(
        None, "--limit", help="files/folders per level (server max 1000); `truncated` says if cut"
    ),
) -> None:
    """One folder level of a run's artifacts: the files at that path plus each
    child folder with its file count. What the explorer fetches on expand, so a
    run with thousands of captured files costs one small answer per folder."""
    with _client() as c:
        _print_json(c.list_run_artifact_tree(_ref(c, "run", run).id, prefix=prefix, limit=limit))


@artifact_app.command("versions")
def artifact_versions(
    artifact_id: str = typer.Argument(..., help="artifact id (from `probe artifact list`)"),
) -> None:
    """List an artifact's version chain.

    An artifact is a named thing in a container; this is the content history behind
    that name. `origin` says how each version got its bytes: `uploaded` (pushed
    directly) or `pinned` (promoted zero-copy from another artifact). Immutability is
    a property of the version, not the artifact -- renaming or moving the artifact
    never breaks a pin."""
    with _client() as c:
        _print_json(c.list_artifact_versions(artifact_id))


@artifact_app.command("pin-impact")
def artifact_pin_impact(
    artifact_id: str = typer.Argument(..., help="artifact id (from `probe artifact list`)"),
) -> None:
    """Show which projects and experiments pin this artifact's versions.

    Run this before deleting anything: it reports the actual work that would break,
    not a count. `pinned: false` means nothing published depends on it."""
    with _client() as c:
        _print_json(c.artifact_pin_impact(artifact_id))


@artifact_app.command("version-add")
def artifact_version_add(
    artifact_id: str = typer.Argument(..., help="the artifact to append a version to"),
    from_artifact: str = typer.Option(
        None,
        "--from-artifact",
        metavar="ID",
        help="promote another artifact's content ZERO-COPY: pins its hash, uri and "
        "size; the stored object is shared, never re-uploaded",
    ),
    uri: str = typer.Option(
        None, "--uri", help="name the pointer directly instead of promoting an artifact"
    ),
    sha256: str = typer.Option(None, "--sha256", metavar="HEX", help="content_hash for --uri"),
    size_bytes: int = typer.Option(None, "--size-bytes"),
    content_type: str = typer.Option(None, "--content-type"),
    label: str = typer.Option(
        None, "--label", help="an alternate selector for this version (e.g. 'prod')"
    ),
) -> None:
    """Append the next version of an artifact.

    Exactly one source: --from-artifact (zero-copy promotion) or --uri. Appending
    content identical to the artifact's current live content is a no-op that returns
    the existing version, so this is safe to retry."""
    if bool(from_artifact) == bool(uri):
        raise typer.BadParameter("pass exactly one of --from-artifact or --uri")
    with _client() as c:
        _print_json(
            c.create_artifact_version(
                artifact_id,
                from_artifact_id=from_artifact,
                uri=uri,
                content_hash=sha256,
                size_bytes=size_bytes,
                content_type=content_type,
                label=label,
            )
        )


@artifact_app.command("delete")
def artifact_delete(
    artifact_id: str = typer.Argument(..., help="artifact id (no by-name index; ids only)"),
    yes: bool = typer.Option(False, "--yes", help="skip the confirmation prompt"),
) -> None:
    """PERMANENTLY delete an artifact. Irreversible."""
    _confirmed_delete(
        "artifact",
        artifact_id,
        yes=yes,
        cascade="its stored bytes and version history go with it",
    )


@artifact_app.command("gc-uploads")
def artifact_gc_uploads(
    older_than: str = typer.Option(
        ...,
        "--older-than",
        metavar="TIMESTAMP",
        help="sweep uploads started before this; must carry a timezone, e.g. 2026-07-01T00:00:00Z",
    ),
) -> None:
    """Sweep abandoned (never-confirmed) uploads. Confirmed artifacts are untouched."""
    with _client() as c:
        _print_json(c.gc_uploads(older_than))
from probe.cli.commands.artifacts.anchors import _anchor_id_for, _pick_anchor  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.delete import _confirmed_delete  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import _ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
