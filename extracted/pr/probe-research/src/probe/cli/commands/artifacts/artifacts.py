"""probe artifact add: record a file against a run, project, experiment, workspace or Shared (direct, queued, multipart or a manifest)."""

from __future__ import annotations
from enum import Enum
from typing import Optional

import typer

from probe.cli.commands.commands import register_group
from ....sdk.artifact.anchors import Anchor
from ....sdk.artifact.kinds import (
    DEFAULT_ARTIFACT_KIND,
    USER_ARTIFACT_KINDS)
from ....sdk.artifact.filetype import artifact_kind_for
from ....sdk.artifact.hashing import reference_fields
from probe.cli.commands.artifacts.manifest import _MANIFEST_REFERENCE_OVER_BYTES, _artifact_add_manifest
from probe.cli.connection import _UNDELIVERED, _client, _resolve_write_mode, write_mode_opt


class AssetMode(str, Enum):
    readonly = "readonly"
    copy = "copy"


# -- artifacts --------------------------------------------------------------
artifact_app = typer.Typer(no_args_is_help=True, help="artifacts")


@artifact_app.command("add")
def artifact_add(
    run: str = typer.Argument(None, help="run id — omit when using an anchor flag"),
    path: str = typer.Argument(None, help="local file to upload"),
    uri: str = typer.Option(None, "--uri", help="record a reference to an existing object"),
    name: str = typer.Option(
        None,
        "--name",
        help="the file's relative path (defaults to its basename). The file's "
        "extension is kept whatever you pass — say what the file IS in its run's notes",
    ),
    kind: str = typer.Option(
        None,
        "--kind",
        help="run anchor only; one of "
        + ", ".join(f"`{k.value}`" for k in USER_ARTIFACT_KINDS)
        + ". Any other word is filed as `other` and kept as its label (a synonym such "
        "as `benchmark` or `script` is filed as its kind, labelled the same way). "
        "Default: `checkpoint` for ckpt, safetensors, pt or pth, else `other`",
    ),
    step: int = typer.Option(None, "--step", help="run anchor only"),
    span: str = typer.Option(None, "--span", help="associate with a run span UUID"),
    content_type: str = typer.Option(None, "--content-type"),
    meta: list[str] = typer.Option(None, "--meta", metavar="k=v", help="run anchor only"),
    # HIDDEN AND IGNORED: files no longer carry notes. Kept so a script or an
    # agent on an older skill still uploads its file; it is told once, on stderr.
    notes: str = typer.Option(None, "--notes", hidden=True),
    project: str = typer.Option(None, "--project", help="anchor to a project slug (or id:<uuid>)"),
    experiment: str = typer.Option(
        None, "--experiment", help="anchor to an experiment slug (or id:<uuid>)"
    ),
    workspace: str = typer.Option(
        None,
        "--workspace",
        help="anchor to a workspace slug (or id:<uuid>) — a file, not an artifact",
    ),
    shared: bool = typer.Option(False, "--shared", help="put it in the team Shared folder"),
    write_mode: Optional[bool] = write_mode_opt(),
    reference: bool = typer.Option(
        False,
        "--reference",
        help="record the file's PATH as a reference (file://) instead of uploading its "
        "bytes — for large files on a shared volume the agent resolves locally",
    ),
    hash_content: bool = typer.Option(
        False,
        "--hash",
        help="also fingerprint a --reference (reads the whole file; enables dedup)",
    ),
    allow_missing: bool = typer.Option(
        False,
        "--allow-missing",
        help="record a --reference even if the path is not visible from this host",
    ),
    from_manifest: str = typer.Option(
        None,
        "--from-manifest",
        metavar="FILE",
        help="bulk import: one JSON object per line, each the row form of these "
        "flags. ONE process, one anchor resolution, N files queued",
    ),
    reference_over: int = typer.Option(
        _MANIFEST_REFERENCE_OVER_BYTES,
        "--reference-over",
        metavar="BYTES",
        help="--from-manifest only: at or over this size a row is RECORDED as a "
        "reference instead of uploaded",
    ),
) -> None:
    """Record an artifact against a run, project, experiment, workspace, or Shared.

    With a path and no --uri/--reference the real upload runs (fingerprint -> presign ->
    PUT -> confirm). With --reference the file's PATH is recorded (file://, bytes NOT
    uploaded) — for a 16GB checkpoint or a shared-volume file an agent resolves locally.
    With --uri it records a reference to an object already in a bucket. References are
    run/project/experiment only — a workspace/Shared file *is* its bytes.

    CODE IS THE EXCEPTION: --kind code (or a word filed as code, such as script or
    source, and the code_bytes / code_snapshot kinds the snapshot writes) is
    always uploaded, never referenced.
    Passing --reference with one of those uploads the bytes and says so; if they
    are not readable from this host it is an error rather than a pointer. A script
    is small, and a pointer to it stops resolving the moment the box or the
    checkout goes away.

    --from-manifest FILE imports many files in one go. Each line is a JSON object
    whose keys are these flags: "path", "name", "uri", "kind", "step", "span",
    "content_type", "meta", "reference", "hash", "allow_missing", and an anchor
    ("run"/"project"/"experiment"/"workspace"/"shared"). A row without an
    anchor uses the one on the command line. Every distinct anchor is resolved
    ONCE. Rows are queued to the outbox and delivered by the drainer, whether or
    not --async is set — that is the point of the verb. A bad row is reported
    with its line number and does not stop the rest; the summary is JSON on
    stdout and the exit code is non-zero if anything failed.

    Say what a file IS, and where it lives, in its run's notes (`probe notes
    append --run RUN --text ...`). Files no longer carry notes: `--notes` (and a
    manifest row's "notes") is ignored, with a warning.
    """
    if notes is not None:
        _warn_file_notes_ignored("--notes")
    if from_manifest is not None:
        if run is not None or path is not None:
            raise typer.BadParameter(
                "--from-manifest takes its rows from the file; drop the positional arguments"
            )
        if write_mode is not None:
            # Refuse rather than ignore: --sync is what someone reaches for when
            # they need the write to have LANDED, and this path always queues.
            raise typer.BadParameter(
                "--from-manifest always queues to the outbox; --async/--sync do not "
                "apply. Use `probe outbox status` to confirm delivery"
            )
        if name is not None or uri is not None or reference:
            raise typer.BadParameter(
                "--name/--uri/--reference are per-ROW in a manifest, not flags. Set "
                "them on the JSON objects instead"
            )
        default_anchor = None
        if project or experiment or workspace or shared:
            default_anchor = _pick_anchor(
                run=None,
                project=project,
                experiment=experiment,
                workspace=workspace,
                shared=shared,
            )
        _artifact_add_manifest(
            from_manifest,
            default_anchor=default_anchor,
            reference_over=reference_over,
        )
        return

    anchored = project or experiment or workspace or shared
    if anchored:
        # With an anchor flag there is no RUN, so the single positional is the path.
        # Shifting here (rather than guessing from the value) keeps `add ./f.bin` and
        # `add RUN ./f.bin` both unambiguous.
        if path is not None:
            # Two positionals means the caller passed RUN *and* an anchor flag. Catch
            # it here: after the shift below `run` is always None, so _pick_anchor's
            # two-anchor check can no longer see the RUN and the id would be silently
            # reinterpreted as a file path (an unhandled FileNotFoundError).
            raise typer.BadParameter(
                "an artifact anchors to exactly one thing; got RUN and an anchor flag. "
                "Drop the RUN argument, or drop the flag."
            )
        path, run = run, None

    anchor, anchor_id = _pick_anchor(
        run=run, project=project, experiment=experiment, workspace=workspace, shared=shared
    )
    if kind is None:
        # The SDK's default, so one .pt is a `checkpoint` whichever door it came in by.
        # Only a run artifact has a kind; every other anchor takes the default.
        if anchor is Anchor.RUN:
            kind = artifact_kind_for(name or "", path or uri)
        else:
            kind = DEFAULT_ARTIFACT_KIND.value

    resolved = _validate_artifact_row(
        anchor,
        path=path,
        uri=uri,
        name=name,
        reference=reference,
        hash_content=hash_content,
        allow_missing=allow_missing,
        kind=kind,
        step=step,
        span=span,
        meta=meta,
    )

    was_reference = reference
    reference = _reference_after_code_check(
        kind, reference=reference, path=path, allow_missing=allow_missing
    )
    if was_reference and not reference:
        # Say it out loud on the single-file path: the caller typed --reference
        # and is getting an upload, and a behaviour change nobody is told about
        # is how the next person concludes the flag is broken.
        typer.echo(
            f"--kind {kind} is stored, not referenced: uploading {path} instead of "
            "recording its path.",
            err=True,
        )

    if anchor is not Anchor.RUN and path and not reference and uri is None:
        # 0333 (bigger-uploads plan D5): a file over 64 MiB for a project,
        # experiment, workspace or Shared goes in parts, queued -- the single
        # PUT below cannot take it, and the Probe daemon's call to this command
        # times out at 180 s. A run's goes through `_artifact_enqueue`.
        if _artifact_add_anchored_multipart(
            anchor,
            anchor_id,
            resolved,
            path,
            content_type=content_type,
            write_mode=write_mode,
        ):
            return

    # QUEUE ONLY WHERE A BARRIER EXISTS. `run end` is the one command that
    # verifies delivery, and it drains by run_ref -- so a project-, experiment-,
    # workspace- or shared-anchored upload has no command in anyone's workflow
    # that would force it out. Those anchors keep failing loudly at the moment of
    # the write instead of queueing into a window nothing closes.
    #
    # An explicit --async still opts any anchor in: this changes the DEFAULT, and
    # `probe --async artifact add --project ...` worked yesterday.
    #
    # Costs almost nothing: `_artifact_add_manifest` returned above, so the
    # 200k-file bulk path is already always-queued and untouched either way. What
    # stays synchronous is the single-file non-run add, which is rare by nature.
    effective_mode = _resolve_write_mode(write_mode)
    if effective_mode is None and anchor is not Anchor.RUN:
        effective_mode = False
    if (
        effective_mode is None
        and _goes_in_parts(anchor, path, uri=uri, reference=reference)
        and _queue_is_deliverable()
    ):
        # A run file over 64 MiB is QUEUED in parts unless --sync says otherwise,
        # even under PROBE_ASYNC=0: the Probe daemon sets that to see each write
        # land, and a multi-gigabyte transfer cannot land inside its 180 s call.
        # The op is durable and the outbox worker resumes it. The run is read
        # FIRST, so a wrong id still fails now instead of in the outbox, where
        # nothing tells the caller (the daemon's L14 rule).
        with _client() as c:
            c.get_run(anchor_id)
        effective_mode = True
    # Build a client here ONLY when queueing is actually on the table. A client
    # opened just to be asked "are you async?" and then closed is wasteful in
    # production and wrong under test, where `Client` is monkeypatched to one
    # shared object: closing it closed the very client the synchronous path
    # below then tried to use ("Cannot send a request, as the client has been
    # closed"). `_sync` never reaches this at all.
    with _queue_client_if_possible(effective_mode) as queue_client:
        # An explicit --async is a COMMAND, so it does not get second-guessed by
        # reading the client back; `_async_client` has already refused if nothing
        # could drain the journal. Only the unforced case asks what was resolved.
        if queue_client is not None and (effective_mode is True or queue_client.async_writes):
            if anchor in _SLUG_ANCHORS:
                # Only reachable via an explicit --async now that _SLUG_ANCHORS
                # (project/experiment/workspace) no longer take the default.
                #
                # A queued write must not carry a raw slug into the journal: the
                # drainer POSTs it minutes later, an unresolved slug becomes a 422
                # nobody is watching, and an id/slug collision files the upload
                # against the wrong project with no operator present. Sync and
                # async have to agree on what a ref means.
                #
                # One bounded indexed lookup, and free offline -- _anchor_id_for
                # passes an unresolvable ref straight through rather than gating.
                with _client() as c:
                    anchor_id = _anchor_id_for(c, anchor, anchor_id)
            if _artifact_add_async(
                queue_client,
                anchor,
                anchor_id,
                resolved,
                path=path,
                uri=uri,
                reference=reference,
                hash_content=hash_content,
                allow_missing=allow_missing,
                kind=kind,
                step=step,
                span=span,
                content_type=content_type,
                meta=_kv_pairs(meta) if meta else None,
            ):
                return
            # Nothing was queued -- staging was refused, or the outbox could not
            # be written. Fall through and upload synchronously: this process is
            # now the only writer, which is exactly why the enqueue side had to
            # leave no op behind.

    # Every path that reaches the server DIRECTLY passes through here: --sync, a
    # credential-degraded session, a non-run anchor, and the fallback above.
    # Order against anything already queued for this same name before writing.
    _drain_colliding_uploads(anchor, anchor_id, resolved)

    if anchor is Anchor.RUN:
        with _client() as c:
            row = _run_handle(c, anchor_id).log_artifact(
                resolved,
                path=path,
                uri=uri,
                reference=reference,
                hash_content=hash_content,
                allow_missing=allow_missing,
                kind=kind,
                step_index=step,
                span_id=span,
                content_type=content_type,
                meta=_kv_pairs(meta) if meta else None,
            )
        upload = (row.get("meta") or {}) if isinstance(row, dict) else {}
        if upload.get("upload") == "failed":
            # The SDK does not raise for a refused or failed upload: it records
            # a pointer and carries on, which is right in a training loop and a
            # lie at a prompt. `(delivered)` and exit 0 read as "the bytes are
            # stored" to every script and agent that runs this command.
            typer.echo(
                f"error: not uploaded ({upload.get('upload_error') or 'the upload failed'}); "
                "a pointer was recorded",
                err=True,
            )
            raise typer.Exit(1)
        word = _UNDELIVERED.word()
        print(f"artifact {resolved!r} recorded on {anchor_id} ({word})")
        # A run file over 64 MiB sent in parts comes back through here (sync)
        # or `_artifact_add_async` (queued); every other anchor takes no kind.
        _say_where_the_kind_went(kind)
        return
    with _client() as c:
        anchor_id = _anchor_id_for(c, anchor, anchor_id)
        if reference:
            fields = reference_fields(path, hash_content=hash_content, allow_missing=allow_missing)
            body = {"name": resolved, "is_reference": True, **fields}
            if content_type:
                body["content_type"] = content_type
            _print_json(c.create_anchored_reference(anchor, anchor_id, body))
        elif uri is not None:
            body = {"name": resolved, "uri": uri, "is_reference": True}
            if content_type:
                body["content_type"] = content_type
            _print_json(c.create_anchored_reference(anchor, anchor_id, body))
        else:
            if not path:
                raise typer.BadParameter("needs a file path (--reference, or --uri)")
            _print_json(
                c.upload_file(
                    anchor,
                    anchor_id,
                    resolved,
                    path,
                    content_type=content_type,
                )
            )
from probe.cli.commands.artifacts.anchors import _SLUG_ANCHORS, _anchor_id_for, _pick_anchor  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.artifacts.enqueue import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _artifact_add_async,
    _drain_colliding_uploads,
    _queue_client_if_possible,
    _queue_is_deliverable,
)

#: `probe artifact --help` order (artifacts, manage and download register them).
ARTIFACT_GROUP = register_group(
    artifact_app,
    (
        "add", "set", "move", "list", "tree", "download", "versions", "pin-impact", "version-add",
        "delete", "gc-uploads",
    ),
)
from probe.cli.commands.artifacts.multipart import _artifact_add_anchored_multipart, _goes_in_parts  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.artifacts.row_checks import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _reference_after_code_check,
    _say_where_the_kind_went,
    _validate_artifact_row,
)
from probe.cli.commands.flag_values import _kv_pairs, _warn_file_notes_ignored  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.run_handle import _run_handle  # noqa: E402 -- pieces need each other; the front door loads this one first
