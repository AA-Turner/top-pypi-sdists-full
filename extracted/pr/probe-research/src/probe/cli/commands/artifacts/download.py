"""probe artifact download: an artifact's bytes, or a run's best/latest checkpoint folder."""

from __future__ import annotations
import hashlib
import sys
from pathlib import Path

import typer

from .... import errors
from ....sdk.run.readback import readback as _checkpoints_sdk
from probe.cli.commands.artifacts.artifacts import artifact_app


@artifact_app.command("download")
def artifact_download(
    artifact_id: str = typer.Argument(
        None, help="artifact id (from `probe artifact list`); omit with --run and --checkpoint"
    ),
    output: str = typer.Option(
        None,
        "--output",
        "-o",
        "--to",
        metavar="PATH",
        help="write the bytes here; '-' forces stdout. Omit to write to stdout "
        "(refused at a terminal).",
    ),
    sha256: str = typer.Option(
        None,
        "--sha256",
        metavar="HEX",
        help="expected content_hash; fail (deleting a written file) if the bytes differ",
    ),
    version: int = typer.Option(
        None,
        "--version",
        metavar="N",
        help="fetch this version's bytes instead of the artifact's live content "
        "(from `probe artifact versions`)",
    ),
    run: str = typer.Option(None, "--run", help="with --checkpoint: the run whose checkpoint to fetch"),
    checkpoint: str = typer.Option(
        None,
        "--checkpoint",
        metavar="best|latest",
        help="fetch the run's best (meta.best) or latest (highest step) checkpoint into the folder -o",
    ),
    callback: str = typer.Option(
        None, "--callback", help="with --checkpoint best: the checkpoint callback whose best (Lightning)"
    ),
) -> None:
    """Download an artifact's bytes through a presigned GET.

    To a PATH it streams straight to the file -- never buffering the whole blob,
    which can be model weights -- and prints {dest, size_bytes, sha256}. To stdout it
    buffers in memory so the hash can be checked before a byte is emitted. Pass
    --sha256 to verify the round trip against the content_hash from
    `probe artifact list`; a metadata match alone never proves the blob exists.

    --version resolves a pin: it fetches that exact version's bytes, which is what a
    reproduction needs, rather than whatever the name points at today.

    A checkpoint uploaded with `checkpoints="upload"` (the Hugging Face and
    Lightning integrations) is a folder: pass its id, or `--run R --checkpoint
    best|latest`, with `-o DIR`, and every file it stored lands under DIR, each
    checked against its sha256."""
    if checkpoint is not None or run is not None or callback is not None:
        _download_run_checkpoint(artifact_id, output, sha256, version, run, checkpoint, callback)
        return
    if artifact_id is None:
        raise typer.BadParameter("pass an artifact id, or --run with --checkpoint best|latest")
    to_stdout = output is None or output == "-"
    if to_stdout and output is None and sys.stdout.isatty():
        raise typer.BadParameter(
            "refusing to write binary to a terminal; pass -o PATH, or '-o -' / a "
            "redirect to force stdout"
        )
    with _client() as c:
        try:
            if to_stdout:
                data = (
                    c.download_artifact_version(artifact_id, version)
                    if version is not None
                    else c.download_artifact(artifact_id)
                )
                digest = hashlib.sha256(data).hexdigest()
                if sha256 and digest != sha256:
                    typer.echo(
                        f"sha256 mismatch: expected {sha256}, got {digest} ({len(data)} bytes)",
                        err=True,
                    )
                    raise typer.Exit(1)
                sys.stdout.buffer.write(data)
                sys.stdout.buffer.flush()
                typer.echo(f"{artifact_id}  {len(data)} bytes  sha256={digest}", err=True)
                return
            # download_artifact*_to removes its own partial file on a mid-stream failure.
            result = (
                c.download_artifact_version_to(artifact_id, version, output)
                if version is not None
                else c.download_artifact_to(artifact_id, output)
            )
            if sha256 and result["sha256"] != sha256:
                Path(output).unlink(missing_ok=True)
                typer.echo(
                    f"sha256 mismatch: expected {sha256}, got {result['sha256']}; deleted {output}",
                    err=True,
                )
                raise typer.Exit(1)
            _print_json(result)
        except errors.RosError as exc:
            # A reference has no managed blob to download; the server 409s with the
            # pointer so we can show the path instead of the raw error. Read it from
            # where it lives (e.g. the shared volume) -- Probe stores no bytes for it.
            detail = exc.detail if isinstance(exc.detail, dict) else {}
            status = getattr(exc, "status", None)
            # A force-deleted version answers 410 WITH who/when, so a reproduction can
            # tell "deliberately destroyed" apart from "never existed". Say which.
            if status == 410 and version is not None:
                when = detail.get("deleted_at") or "(unknown time)"
                who = detail.get("deleted_by")
                typer.echo(
                    f"artifact {artifact_id} version {version} was deleted at {when}"
                    + (f" by {who}" if who else "")
                    + "\nThe version record survives; its bytes do not.",
                    err=True,
                )
                raise typer.Exit(2)
            if status != 409 or detail.get("reason") != "reference":
                raise
            # An uploaded checkpoint's index row is a reference to where it
            # was saved; its bytes are the files it lists.
            try:
                row = c.get_artifact(artifact_id)
            except errors.RosError:
                row = {}  # the reference answer above still says where it is
            listed = _checkpoints_sdk.members(row)
            if listed:
                if to_stdout or version is not None or sha256:
                    typer.echo(
                        f"artifact {artifact_id} is checkpoint {row.get('name')}, a folder of "
                        f"{len(listed)} stored files: pass -o DIR (each file is checked against its "
                        "own sha256; --version and --sha256 do not apply to a folder)",
                        err=True,
                    )
                    raise typer.Exit(2)
                _download_checkpoint_folder(c, row, output)
                return
            where = detail.get("local_path") or detail.get("uri") or "(unknown location)"
            host = detail.get("host")
            what = f"artifact {artifact_id}" + (
                f" version {version}" if version is not None else ""
            )
            typer.echo(
                f"{what} is a reference -> {where}"
                + (f" on {host}" if host else "")
                + "\nProbe stores no bytes for it; read it from that path.",
                err=True,
            )
            raise typer.Exit(2)


def _download_run_checkpoint(artifact_id, output, sha256, version, run, which, callback) -> None:
    """`probe artifact download --run R --checkpoint best|latest -o DIR`."""
    if artifact_id is not None:
        raise typer.BadParameter("pass an artifact id or --run with --checkpoint, not both")
    if run is None or which is None:
        raise typer.BadParameter("--run and --checkpoint go together (and --callback needs both)")
    if which not in _checkpoints_sdk.WHICH:
        raise typer.BadParameter(f"--checkpoint must be one of {', '.join(_checkpoints_sdk.WHICH)}")
    if version is not None or sha256:
        raise typer.BadParameter("--version and --sha256 take an artifact id, not --checkpoint")
    if output is None or output == "-":
        raise typer.BadParameter("a checkpoint is a folder: pass -o DIR")
    with _client() as c:
        run_id = _ref(c, "run", run).id
        try:
            row, rows = _checkpoints_sdk.find(c, run_id, which, callback=callback)
        except _checkpoints_sdk.AmbiguousCheckpoint as exc:
            typer.echo(f"{exc}; pass --callback with one of them", err=True)
            raise typer.Exit(2) from None
        if row is None:
            typer.echo(
                f"run {run} has no {which} checkpoint that can still be fetched "
                "(none recorded, none marked best, or every one is gone)",
                err=True,
            )
            raise typer.Exit(1)
        _download_checkpoint_folder(c, row, output, rows=rows)


def _download_checkpoint_folder(c, row: dict, output: str, *, rows: list[dict] | None = None) -> None:
    try:
        result = _checkpoints_sdk.download(c, row, output, rows=rows)
    except (_checkpoints_sdk.CheckpointNotStored, ValueError) as exc:
        typer.echo(str(exc), err=True)
        raise typer.Exit(2) from None
    except OSError as exc:  # not empty, a mount point, no permission, disk full
        typer.echo(f"could not restore checkpoint {row.get('name')} into {output}: {exc}", err=True)
        raise typer.Exit(2) from None
    if result.get("excluded"):
        typer.echo(
            f"note: {result['excluded']} file(s) of this checkpoint were excluded by .probe.config "
            "and were never uploaded; they are not in the restored folder",
            err=True,
        )
    if result.get("redacted"):
        typer.echo(
            "note: these files had a credential masked when stored, so they differ from the "
            f"originals: {', '.join(result['redacted'])}",
            err=True,
        )
    _print_json(result)
from probe.cli.commands.json_print import _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.refs import _ref  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
