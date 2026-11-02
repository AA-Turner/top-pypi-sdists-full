"""read a captured run back: probe snapshot-show, snapshot-restore and run reproduce (rebuild the working tree)."""

from __future__ import annotations
import json
import os
import sys

from probe.sdk.capture.code.code import wire_name
import tempfile
from pathlib import Path
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
from ....shared.reads import reads
from probe.cli.cli import app
from probe.cli.commands.refs import _api, run_ref
from probe.cli.commands.runs.runs import run_app


def _materialize_record(c: Any, run_id: str, record: dict, dest: str) -> dict:
    """Reconstruct a runnable directory from a reproduction record: restore the
    captured code tree (lockfiles included — they ride in the tree), write the
    inputs-decision artifacts that carry inline content, and drop the full record
    as ``reproduce-manifest.json``.

    An inputs-decision whose content was omitted (too large to inline) is written
    as a ``.omitted`` marker naming the reason rather than skipped — a missing file
    with no note reads as "there was nothing", which is the confident-wrong answer
    the reproduce surface exists to avoid.
    """
    dest_path = Path(dest)
    dest_path.mkdir(parents=True, exist_ok=True)
    written: dict[str, Any] = {
        "dest": str(dest_path),
        "code_tree": None,
        "inputs": [],
        "manifest": None,
    }

    env_ref = (record.get("run") or {}).get("env_ref")
    if env_ref:
        result = _restore_captured_tree(c, run_id, env_ref, str(dest_path))
        written["code_tree"] = {
            "n_restored": result["n_restored"],
            "n_unavailable": result["n_unavailable"],
            "tree_matches": result["tree_matches"],
        }
    else:
        written["code_tree"] = "no execution record — code tree not captured"

    for item in record.get("inputs_decision") or []:
        artifact = item.get("artifact") or {}
        name = artifact.get("name") or "inputs-decision.json"
        target = dest_path / name
        target.parent.mkdir(parents=True, exist_ok=True)
        if item.get("content") is not None:
            target.write_text(item["content"])
            written["inputs"].append(name)
        elif item.get("content_omitted_reason"):
            marker = dest_path / f"{name}.omitted"
            marker.write_text(str(item["content_omitted_reason"]))
            written["inputs"].append(f"{name}.omitted")

    (dest_path / "reproduce-manifest.json").write_text(json.dumps(record, indent=2, sort_keys=True))
    written["manifest"] = "reproduce-manifest.json"
    return written


@run_app.command("reproduce")
def run_reproduce(
    run: str = run_ref(),
    export: str = typer.Option(
        None,
        "--export",
        help="write the record as a portable JSON bundle (a rendering, not the source of truth)",
    ),
    materialize: str = typer.Option(
        None,
        "--materialize",
        help="reconstruct a runnable directory: restore the code tree + write inputs and the manifest",
    ),
) -> None:
    """Pull the server-assembled reproduction record for a run.

    One read assembles everything reproduction needs — execution record, launch
    context, a copyable restore command, code snapshot, inputs-decision, notes,
    lockfiles, lineage edges, per-span environments, and a completeness verdict.
    It is assembled by research-os (`GET /v1/runs/{id}/reproduce`), not here: the
    backend is the one place that reads every piece together. A run captured before
    capture-core still answers with an honest degraded record, never an error.

    `--export FILE` writes the record as a portable JSON bundle — a rendering you can
    hand off, never the source of truth (that stays the run). `--materialize DIR`
    goes further: it rebuilds the captured code tree and writes the inputs, leaving a
    directory you can run.
    """
    if export and materialize:
        raise typer.BadParameter("pass --export OR --materialize, not both")
    if not (export or materialize):
        with _client() as c:
            printed = reads.run_reproduce(_api(c, pretty=sys.stdout.isatty()), run)
        _emit(printed)
        return
    with _client() as c:
        run_id, record = reads.reproduce_record(_api(c), run)
        if materialize:
            _print_json(_materialize_record(c, run_id, record, materialize))
            return
    Path(export).write_text(json.dumps(record, indent=2, sort_keys=True))
    typer.echo(f"wrote {export}")


@app.command("snapshot-show")
def snapshot_show(
    run: str = typer.Argument(...),
    pending_only: bool = typer.Option(False, "--pending-only"),
) -> None:
    """Print a run's captured code manifest, one file per line.

    `git` files are retrievable with `git cat-file blob <blob>` from the recorded
    remote; `blob` files are the ones git cannot supply, stored as the run's
    per-file capture rows ("captured") or in its `code-bytes` archive (runs captured
    before 0193, with `PROBE_CODE_STORAGE=archive`, or against a server without the
    batch doors).

    `--pending-only` means GENUINELY UNAVAILABLE, not `source == "blob"`. The
    manifest's `n_pending_upload` is a CLASSIFICATION count -- "git cannot supply
    this, someone must upload it" (sdk.snapshot.capture_manifest says so in as
    many words) -- and it is frozen into the execution record at capture, before
    the upload it is counting. Reading it as work-remaining is what made this
    command report 6 files pending on a run whose code-bytes archive held all six
    and whose restore verified every one of them. What the upload actually did is
    recorded on the `code-snapshot` artifact, so that is what this reconciles
    against.
    """
    with _client() as c:
        # One read for both: `list_run_artifacts` is UUID-typed, and the handle
        # already resolved a petname to get here.
        data = _run_handle(c, run).data
        record = c.transport.get(f"/v1/execution-records/{data['env_ref']}")
        # A run captured by an older SDK, or one whose upload genuinely failed,
        # has no code-bytes row -- and that is exactly the case where "pending"
        # is the true answer rather than a stale label.
        row = _code_bytes_row(c, str(data["id"]))
        capture = _capture_rows(c, str(data["id"]))
    # Two ways bytes can be stored. Per-file capture rows (0193) name every
    # file they hold by (path, sha256) and only a `complete` row is stored.
    # The archive names what it holds (`meta.paths`): a run whose tree drifted
    # during capture stores most files and lists the rest as unstored, so
    # "there is an archive" is not "every file is in it". An older row with no
    # `paths` key predates that accounting and holds everything (None = all).
    stored_files = {(r.get("name"), r.get("content_hash")) for r in capture}
    listed = (row.get("meta") or {}).get("paths") if row else None
    stored_paths = set(listed) if listed is not None else None
    manifest = ((record or {}).get("code") or {}).get("manifest") or {}
    entries = manifest.get("entries") or []
    print(f"base_commit {manifest.get('base_commit')}  remote {manifest.get('remote')}")
    print(f"tree_sha256 {manifest.get('tree_sha256')}")
    classified = 0
    n_stored = 0
    n_files = 0
    for e in entries:
        source = e.get("source")
        is_blob = source == "blob"
        classified += is_blob
        as_file = is_blob and ((wire_name(e.get("path") or ""), e.get("sha256")) in stored_files)
        in_archive = (
            is_blob and bool(row) and (stored_paths is None or e.get("path") in stored_paths)
        )
        stored = as_file or in_archive
        n_stored += stored
        n_files += as_file
        if pending_only and not (is_blob and not stored):
            continue
        if source == "git":
            # Legacy: manifests captured before git referencing was retired.
            ref = e.get("blob", "-")
        elif source == "reference":
            # NOT in code-bytes and not awaiting upload -- it was deliberately
            # left where it lives. Printing "code-bytes" here (which is what the
            # old else-branch did) claimed Probe held bytes it has never held.
            ref = f"offsite on {e.get('host', '?')}"
        elif source == "withheld":
            # Held a credential at capture: never uploaded, and small ones carry
            # no sha256 (it could be brute-forced back to a password).
            ref = f"withheld ({e.get('reason', 'secret')})"
        else:
            ref = "captured" if as_file else ("code-bytes" if stored else "needs-upload")
        print(f"  {source:<9} {ref:<40} {(e.get('sha256') or '')[:12]} {e.get('path')}")
    n_git = manifest.get("n_git_referenced", 0)
    n_offsite = sum(1 for e in entries if e.get("source") == "reference")
    where = (
        "as files"
        if n_files and n_files == n_stored
        else (
            f"{n_files} as files, {n_stored - n_files} in code-bytes"
            if n_files
            else "in code-bytes"
        )
    )
    summary = f"{n_stored} stored {where}, {classified - n_stored} pending upload"
    if n_offsite:
        summary += f", {n_offsite} referenced offsite"
    if n_git:
        summary += f", {n_git} git-referenced (legacy)"
    print(summary)


def _capture_rows(c: Client, run_id: str) -> list[dict]:
    """The run's complete per-file capture rows (0193); see sdk.run.readback.restore."""
    from ....sdk.run.readback.restore import capture_rows

    return capture_rows(c, run_id)


def _code_bytes_row(c: Client, run_id: str) -> dict | None:
    """The run's uploaded `code-bytes` archive, or None if its bytes never landed.

    Same read `_restore_captured_tree` does before it can rebuild anything, and
    the same normalisation: `list_run_artifacts` answers a bare list on some
    routes and a paged object on others.
    """
    rows = c.list_run_artifacts(run_id, kind="code_bytes") or []
    rows = rows.get("items", rows) if isinstance(rows, dict) else rows
    # A fail-open upload failure leaves a REFERENCE row pointing at a tmp file
    # the SDK deleted; that is a pointer, not stored bytes.
    rows = [r for r in rows if not r.get("is_reference")]
    return rows[0] if rows else None


def _restore_captured_tree(
    c: Any, run_id: str, env_ref: str, dest: str, *, verify_only: bool = False
) -> dict:
    """Rebuild a run's captured working tree into ``dest`` from its execution
    record's code manifest plus the run's per-file capture rows and/or its uploaded ``code-bytes`` archive.

    Shared by ``snapshot-restore`` and ``run reproduce --materialize`` so both fetch,
    verify, and write bytes exactly one way — every file is checked against the
    sha256 the manifest recorded, and a mismatch is reported UNAVAILABLE rather than
    written. Lockfiles ride in the tree here; they are not written from the reproduce
    record's `lockfiles` list, which carries path+sha256 for VISIBILITY, not bytes.
    Returns the ``restore_snapshot`` result dict.
    """
    from ....sdk.run.readback.restore import restore_snapshot

    record = c.transport.get(f"/v1/execution-records/{env_ref}")
    manifest = ((record or {}).get("code") or {}).get("manifest") or {}

    # Per-file capture rows (0193) AND the code-bytes archive, whichever the
    # run holds: a file is taken from the rows first, then from the archive, so
    # a run snapshotted under both storages (the default flip, a partial
    # capture re-run as an archive) restores every byte Probe has.
    from ....sdk.run.readback.restore import capture_blob_fetch

    rows = _capture_rows(c, run_id)
    blob_fetch = (
        capture_blob_fetch(c, rows, warn=lambda m: print(m, file=sys.stderr)) if rows else None
    )

    archive = None
    temp = None
    row = _code_bytes_row(c, run_id)
    if row:
        temp = tempfile.NamedTemporaryFile(prefix="probe-code-", suffix=".tar.gz", delete=False)
        temp.close()
        try:
            c.download_artifact_to(row["id"], temp.name)
            archive = temp.name
        except Exception as exc:  # noqa: BLE001 -- reported per file by restore_snapshot
            print(f"warning: could not download code-bytes: {exc}", file=sys.stderr)

    try:
        return restore_snapshot(
            manifest, dest, archive_path=archive, blob_fetch=blob_fetch, verify_only=verify_only
        )
    finally:
        if temp is not None:
            try:
                os.unlink(temp.name)
            except OSError:
                pass


@app.command("snapshot-restore")
def snapshot_restore(
    run: str = typer.Argument(...),
    dest: str = typer.Argument(None, help="directory to rebuild into; omit with --verify-only"),
    verify_only: bool = typer.Option(
        False, "--verify-only", help="resolve and hash everything, write nothing"
    ),
) -> None:
    """Rebuild a run's captured working tree, or say exactly what is missing.

    Files git can supply are fetched from the recorded remote; the rest come from
    the run's per-file capture rows, then from its `code-bytes` archive when one
    exists. Every file is verified against the sha256
    the manifest recorded — a mismatch is reported UNAVAILABLE and never written,
    so this cannot hand back a tree that only looks right.

    Exits non-zero if any file could not be produced.
    """
    if not verify_only and not dest:
        raise typer.BadParameter("DEST is required unless --verify-only is passed")

    with _client() as c:
        handle = _run_handle(c, run)
        env_ref = handle.data.get("env_ref")
        if not env_ref:
            print(f"error: run {run} has no execution record to restore", file=sys.stderr)
            raise typer.Exit(1)
        result = _restore_captured_tree(c, handle.id, env_ref, dest or ".", verify_only=verify_only)

    for f in result["files"]:
        if f["status"] == "unavailable":
            print(f"  MISSING {f['path']}  ({f['reason']})")
    for r in result.get("referenced") or []:
        print(f"  OFF-PLATFORM {r['path']}  -> {r['uri']} on {r['host']}")
    verb = "verified" if verify_only else "restored"
    ref = (
        f", {result['n_referenced']} referenced off-platform" if result.get("n_referenced") else ""
    )
    print(f"{result['n_restored']} {verb}, {result['n_unavailable']} unavailable{ref}")
    print(f"tree_sha256 {result['tree_sha256']} matches={result['tree_matches']}")
    if result["n_unavailable"]:
        raise typer.Exit(1)
from probe.cli.commands.json_print import _emit, _print_json  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.run_handle import _run_handle  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
