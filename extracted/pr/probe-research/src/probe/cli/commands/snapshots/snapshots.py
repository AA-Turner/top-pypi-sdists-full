"""probe snapshot and snapshot-prune-refs: capture a run's code and environment; prune old snapshot refs."""

from __future__ import annotations
import os
import sys
import uuid
from typing import Optional

import typer
from pydantic import ValidationError
from ....sdk.errors import NotFoundError
from ....sdk.capture.code.environment import UNRESOLVED_FALLBACK as _UNRESOLVED_FALLBACK
from .. import ref_syntax as refs
from probe.cli.cli import app


@app.command()
def snapshot(
    run: str = typer.Argument(...),
    cwd: str = typer.Option(None, "--cwd"),
    venv: str = typer.Option(
        None, "--venv", help="virtualenv to record; auto-detected from --cwd otherwise"
    ),
    no_env: bool = typer.Option(False, "--no-env"),
    no_gpu: bool = typer.Option(False, "--no-gpu"),
    no_upload: bool = typer.Option(
        False, "--no-upload", help="do NOT store the bytes git cannot supply"
    ),
    max_upload_mb: int = typer.Option(
        256, "--max-upload-mb", help="refuse (never truncate) above this size"
    ),
    include: list[str] = typer.Option(
        None,
        "--include",
        metavar="GLOB",
        help="also capture paths git ignores (datasets, checkpoints, out-of-tree configs)",
    ),
    reference_over_mb: int = typer.Option(
        100,
        "--reference-over-mb",
        help="above this, record where a file lives instead of copying it",
    ),
) -> None:
    """Non-disruptive code + env capture.

    Every captured file has its BYTES stored as an artifact row on the run (one per
    file, deduped by content; `PROBE_CODE_STORAGE=archive` stores one `code-bytes`
    archive instead), because a sha256 verifies a file you already have rather
    than producing one you do not.
    Files a pushed remote could supply are uploaded too: git referencing is retired,
    since a pointer that outlives its remote is indistinguishable from a live one.
    `--no-upload` skips the upload, and the run is then not reproducible from the
    record alone.

    The exception is size. Above `--reference-over-mb` a file's path, host and
    sha256 are recorded instead of copied — a base checkpoint is not duplicated
    into every run of a sweep. The commit and remote are still recorded, as
    provenance no byte depends on.

    The dependency set comes from the PROJECT's virtualenv, not this CLI's. `probe`
    is normally a uv-tool install with its own interpreter, so recording the
    packages of the process you are reading this from would describe typer and rich
    rather than torch and transformers.
    """
    with _client() as c:
        snap = _run_handle(c, run).snapshot(
            cwd=cwd,
            include_env=not no_env,
            include_gpu=not no_gpu,
            venv=venv,
            # The CLI is never the process that runs the code.
            detect_venv=True,
            upload=not no_upload,
            max_upload_bytes=max_upload_mb * 1024 * 1024,
            include=list(include) if include else None,
            reference_over_bytes=reference_over_mb * 1024 * 1024,
        )
    m = snap["manifest"]
    callback = snap.get("code_bytes") or {}
    g = snap.get("git")
    if g:
        # Provenance only: read, never written (no shadow ref since plan 2.6).
        head = (g.get("head") or "")[:12] or "no commits yet"
        dirty = ", uncommitted changes" if g.get("dirty") else ""
        print(f"snapshot of {g.get('branch') or 'detached HEAD'} @ {head}{dirty}")
    else:
        print(f"snapshot (no git repo) — {len(m['entries'])} files")
    if snap.get("git_error"):
        print(f"      git unreadable ({snap['git_error']}); captured as a plain directory")
    skipped = m.get("skipped") or []
    if skipped:
        # A COUNT, never a path or a value -- naming it `secrets` made CodeQL
        # read the printed integer as the credential itself, and it read that
        # way to humans too. Printed with or without git: a skip inside a repo
        # (a withheld config, a tracked `.env`) is no less a gap in the record.
        n_credential_shaped = sum(1 for s in skipped if s["reason"] == "secret")
        n_content = sum(1 for s in skipped if s.get("found_in") == "content")
        n_slow = sum(1 for s in skipped if s.get("found_in") == "scan_time")
        note = f", {n_credential_shaped} credential-shaped" if n_credential_shaped else ""
        if n_content:
            note += f", {n_content} withheld for their content"
        if n_slow:
            note += f", {n_slow} withheld: scan ran out of time"
        print(f"      skipped {len(skipped)} paths (excluded by policy{note})")
    base = m["base_commit"][:12] if m["base_commit"] else "no pushed base"
    # The count that used to lead this line was `n_git_referenced` -- files
    # NOT captured, printed as if they were. It is structurally 0 now, so say
    # what is in the record instead, and keep the commit as the provenance it is.
    print(f"code: {len(m['entries'])} files, provenance {base}")
    if callback.get("uploaded") and callback.get("storage") == "artifacts":
        print(
            f"      {callback['n_files']} stored as files ({callback.get('n_uploaded', 0)} uploaded, "
            f"{callback.get('n_deduped', 0)} already held)"
        )
        if callback.get("pending_upload"):
            names = ", ".join(f"{u['path']} ({u['reason']})" for u in callback.get("unstored") or [])
            print(f"      {callback['pending_upload']} NOT stored: {names}")
    elif callback.get("uploaded"):
        print(
            f"      {callback['n_files']} uploaded ({callback['size_bytes'] / 1e6:.2f} MB, "
            f"{callback['archive_sha256'][:12]})"
        )
        if callback.get("pending_upload"):
            names = ", ".join(callback.get("drifted") or [])
            print(
                f"      {callback['pending_upload']} NOT stored (changed or vanished during "
                f"capture): {names}"
            )
    elif callback.get("pending_upload"):
        print(
            f"      {callback['pending_upload']} NOT stored ({callback.get('reason')}) — "
            "this run is not reproducible from the record alone"
        )
    for e in m.get("entries") or []:
        if e.get("source") == "reference":
            print(
                f"      referenced (too large to copy): {e['path']}  "
                f"{e['size'] / 1e6:.0f} MB on {e.get('host')}"
            )
    deps = snap.get("deps") or {}
    prov = snap.get("env_provenance") or {}
    if deps.get("packages") is not None:
        source = prov.get("venv") or prov.get("python_executable")
        print(
            f"env: {deps['package_count']} packages, python {deps['python']}"
            f" ({prov.get('resolved_via')}: {source})"
        )
    elif prov.get("resolved_via") == _UNRESOLVED_FALLBACK:
        # Loud, because the alternative to a wrong dependency list is an ABSENT
        # one, and absence that prints nothing is how a run reaches the record
        # looking captured. Says what to do, not just what happened.
        print(
            "env: NOT captured — no virtualenv found for this project, and this "
            f"CLI's own interpreter ({prov.get('python_executable')}) is outside "
            "it. Recording its packages would describe the CLI, not the "
            "experiment. Pass --venv PATH, or activate the environment the code "
            "runs in, then re-run `probe snapshot`.",
            file=sys.stderr,
        )


def _snapshot_ref_verdicts(refs: list[tuple[str, str]]) -> dict[str, str | None]:
    """ref -> None when its run's code is stored on Probe (safe to delete), else
    why the ref is kept.

    A shadow commit may be the only copy of a dirty tree whose upload failed
    (D10). The run's `code_snapshot` row records how many files never reached
    Probe (`meta.n_pending_upload`, what SURVIVED the upload), so only a row
    that says 0 lets its ref go. No row, a row without the count, a ref name
    that is not a run id, or a run this account cannot see all keep the ref: an
    unknown is not a zero.
    """
    import uuid

    from ....sdk.errors import NotFoundError, ScopeError, ValidationError
    from ....sdk.capture.code.snapshot_refs import SNAPSHOT_REFS_PREFIX

    verdicts: dict[str, str | None] = {}
    ids: dict[str, str] = {}
    for ref, _sha in refs:
        run_id = ref[len(SNAPSHOT_REFS_PREFIX) :]
        try:
            ids[ref] = str(uuid.UUID(run_id))
        except ValueError:
            verdicts[ref] = "not a run id, so its upload cannot be checked"
    if not ids:
        return verdicts
    try:
        c = _client()
    except Exception as exc:  # noqa: BLE001 -- no credentials is an answer, not a crash
        return verdicts | {ref: f"could not check its upload ({type(exc).__name__})" for ref in ids}
    stop: str | None = None
    with c:
        for ref, run_id in ids.items():
            if stop:
                verdicts[ref] = stop
                continue
            try:
                rows = c.list_run_artifacts(run_id, kind="code_snapshot") or []
            except (NotFoundError, ScopeError, ValidationError):
                verdicts[ref] = "run not found under this account, so its upload cannot be checked"
                continue
            except Exception as exc:  # noqa: BLE001 -- offline, auth, 5xx: stop asking
                stop = f"could not check its upload ({type(exc).__name__})"
                verdicts[ref] = stop
                continue
            rows = rows.get("items", rows) if isinstance(rows, dict) else rows
            counts = [(r.get("meta") or {}).get("n_pending_upload") for r in rows]
            ints = [n for n in counts if isinstance(n, int) and not isinstance(n, bool)]
            if not rows:
                verdicts[ref] = "no code-snapshot record on Probe: its upload may never have landed"
            elif any(n > 0 for n in ints):
                verdicts[ref] = f"{max(ints)} file(s) of its code never reached Probe"
            elif len(ints) != len(counts):
                verdicts[ref] = "its code-snapshot record predates upload accounting"
            else:
                verdicts[ref] = None
    return verdicts


@app.command("snapshot-prune-refs")
def snapshot_prune_refs(
    cwd: str = typer.Option(".", "--cwd", help="a directory inside the repository"),
    dry_run: bool = typer.Option(False, "--dry-run", help="list the refs and what would happen; delete nothing"),
    bundle: Optional[str] = typer.Option(  # noqa: UP007
        None,
        "--bundle",
        help="back every ref up to this git bundle (outside the repo) first, then delete them all",
    ),
    force: bool = typer.Option(
        False, "--force", help="also delete refs whose run's upload is unfinished or could not be checked"
    ),
) -> None:
    """Delete the `refs/probe/snapshots/*` refs earlier Probe versions wrote.

    Each is a shadow commit of the working tree at a run's start, untracked files
    included (a `.env` among them), and `git push --mirror` publishes them. Probe
    no longer writes them (plan 2.6) and never deletes them on its own (D10).

    One may be the only copy of a dirty tree whose upload failed, so by default
    a ref is deleted only when its run's code-snapshot record on Probe says every
    file was stored; the rest are kept and listed with the reason. `--bundle
    FILE` backs every ref up first and then deletes them all; `--force` deletes
    them all as they are. Every line prints `<ref> <sha>`: `git update-ref <ref>
    <sha>` restores one until git's gc removes the objects, and `git fetch FILE
    'refs/probe/snapshots/*:refs/probe/snapshots/*'` restores from a bundle.
    """
    from ....sdk.capture.code.code import SnapshotError
    from ....sdk.capture.code.git import _repo_check
    from ....sdk.capture.code.snapshot_refs import (
        bundle_snapshot_refs,
        old_snapshot_refs,
        prune_snapshot_refs)

    in_repo, reason = _repo_check(cwd)
    if not in_repo:
        # git's own reason (no git binary, "dubious ownership"), not a guess.
        print(
            f"error: {reason or os.path.abspath(cwd) + ' is not inside a git repository'}",
            file=sys.stderr,
        )
        raise typer.Exit(1)
    refs = old_snapshot_refs(cwd)
    if not refs:
        print("no refs/probe/snapshots/* refs in this repository")
        return
    # A bundle is the backup, so with one every ref may go unchecked.
    verdicts = {} if (force or bundle) else _snapshot_ref_verdicts(refs)
    doomed = [(ref, sha) for ref, sha in refs if verdicts.get(ref) is None]
    kept = [(ref, sha, verdicts[ref]) for ref, sha in refs if verdicts.get(ref) is not None]
    go, stay = ("would delete", "would keep") if dry_run else ("deleted", "kept")
    if not dry_run:
        try:
            if bundle:
                bundle_snapshot_refs(cwd, [ref for ref, _ in refs], bundle)
                print(
                    f"backed up {len(refs)} ref(s) to {bundle}; restore with "
                    f"git fetch {bundle} 'refs/probe/snapshots/*:refs/probe/snapshots/*'"
                )
            prune_snapshot_refs(cwd, doomed)
        except SnapshotError as exc:
            print(f"error: {exc}", file=sys.stderr)
            raise typer.Exit(1) from exc
    for ref, sha in doomed:
        print(f"{go} {ref} {sha}")
    for ref, sha, why in kept:
        print(f"{stay} {ref} {sha}  ({why})")
    summary = f"{go} {len(doomed)} ref(s)"
    if kept:
        summary += (
            f"; {stay} {len(kept)} whose code may exist nowhere else. `--bundle FILE` "
            "backs them up and deletes them; `--force` deletes them as they are"
        )
    print(summary + (" (dry run; nothing changed)" if dry_run else ""))
    if doomed and not dry_run:
        print(
            "Undo one with `git update-ref <ref> <sha>` (each line above) until git's gc "
            "removes the objects, which for old refs can be the next automatic gc."
        )
    if kept and not dry_run:
        raise typer.Exit(1)
from probe.cli.commands.run_handle import _run_handle  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.commands.runs.reads import bundle  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.cli.connection import _client  # noqa: E402 -- pieces need each other; the front door loads this one first
