"""DirectoryTreeSource: walk a folder that is not a git repository (bounded entries, tagged caches, secret dirs)."""

from __future__ import annotations
import hashlib
import os
from typing import Any
from ....recording_rules import recording_rules as _ignore
from ... import owndirs as _owndirs
from probe.sdk.capture.code.code import (
    SKIP_GENERATED_DIRS,
    SKIP_SECRET_DIRS,
    SnapshotError,
    SnapshotTooLarge,
    _Ignored,
    _include_entries,
    _is_lockfile,
    _posix,
    _skip_reason,
    is_tagged_cache_dir,
    tree_digest,
)


# Refuse rather than silently ship a partial archive. Raise it with
# `--max-upload-mb` when a repo genuinely needs to.
DEFAULT_MAX_UPLOAD_BYTES = 256 * 1024 * 1024


#: Above this, an included file is RECORDED rather than uploaded. A base
#: checkpoint or a dataset shard is an input whose identity matters and whose
#: bytes are already sitting on a shared volume; copying tens of GB per run to
#: re-store what is already there is not reproducibility, it is duplication.
DEFAULT_REFERENCE_OVER_BYTES = 100 * 1024 * 1024

#: File ceiling for a NON-GIT capture. Git bounds its own walk by what is
#: tracked; a bare directory has nothing to bound it, so the walk is whatever
#: happens to sit under the cwd -- and `probe run start` runs in whatever
#: directory a person's shell is parked in.
#:
#: Measured 2026-08-10 in ~/Documents/GitHub (a directory of ~245 checkouts):
#: 276,507 entries, 54.6s of walking and sha256, every one classified pending
#: upload -- and then a 256MB upload cap to fail against at the END. The run
#: itself was created in well under a second; the whole stall was this.
#:
#: A ceiling, not a truncation: a manifest missing files it never mentions is
#: the thing `skipped` exists to prevent, and half a tree reproduces nothing.
#: Overflow raises SnapshotTooLarge, which the auto-snapshot hook turns into a
#: warning -- capture is never a gate (maintainer decision 2026-08-06), so the
#: run survives uncaptured rather than the command hanging.
#:
#: 20k is well above a real project (this repo is ~1.5k files) and well below
#: a directory that is really somebody's whole workspace.
DEFAULT_MAX_DIRECTORY_ENTRIES = 20_000
#: Every directory a walk prunes (`inputs` and `outputs` read this union).
SKIP_DIRS = SKIP_GENERATED_DIRS | SKIP_SECRET_DIRS


def capture_directory_manifest(
    cwd: str | None = None,
    *,
    include: list[str] | None = None,
    reference_over_bytes: int = DEFAULT_REFERENCE_OVER_BYTES,
    max_entries: int = DEFAULT_MAX_DIRECTORY_ENTRIES,
    scan: bool = True,
    scan_budget_bytes: int | None = DEFAULT_MAX_UPLOAD_BYTES,
    ignore: _ignore.IgnoreRules | None = None,
) -> dict[str, Any]:
    """Manifest for a directory that is NOT a git repository.

    Same shape and the same :func:`_classify_by_size` rule as
    :func:`capture_manifest`; the differences are WHICH files get walked (the
    filtered walk below rather than ``ls-files``) and that ``base_commit`` and
    ``remote`` are None because there is no repo to take them from.

    The walk is size-gated like everything else: a file over
    ``reference_over_bytes`` is recorded as a file-path reference rather than
    swept into the archive, where it would push the whole snapshot past the
    upload ceiling and lose the other files with it.

    The exclusions are the whole design. Git gave the classifier `.gitignore` for
    free; a bare directory has nothing, so the defaults have to be conservative in
    the one direction that matters. ``SKIP_DIRS`` drops what a lockfile rebuilds,
    and ``SKIP_SECRETS`` drops credential-shaped files -- auto-uploading a working
    directory must not be how a `.env` leaves the machine. The SDK's own folders
    (its outbox, its state, its ``$TMPDIR`` stand-ins: `probe.sdk.capture.owndirs`) are
    skipped too, when the tree holds one: a job started in ``$TMPDIR`` used to
    take its own queue files as its code.

    Everything skipped is REPORTED in ``skipped``, because once a filter exists,
    absence from the manifest stops being informative on its own: a reader has to
    be able to tell "not an input" from "excluded by policy".

    ``max_entries`` bounds the walk (see ``DEFAULT_MAX_DIRECTORY_ENTRIES``) and is
    checked DURING it, not after: the cost being bounded is the walk itself, so a
    ceiling enforced on the finished manifest would refuse a tree only after
    paying the minute it took to build it.

    A name is not the only way a credential arrives: a `config.yaml` holding an
    HF token has an innocent name. With ``scan`` (the default) every file that
    could be uploaded is content-scanned (:class:`_ContentGate`, bounded by
    ``scan_budget_bytes``; None = unbounded) and WITHHELD when it holds one: kept
    in ``entries`` as ``source: "withheld"``, never uploaded, and reported.
    """
    cwd = os.path.abspath(cwd or os.getcwd())
    if not os.path.isdir(cwd):
        raise SnapshotError(f"{cwd} is not a directory")

    entries: list[dict[str, Any]] = []
    skipped: list[dict[str, Any]] = []
    gate = _ContentGate(scan=scan, budget=scan_budget_bytes)

    def _guard() -> None:
        if len(entries) <= max_entries:
            return
        raise SnapshotTooLarge(
            f"{cwd} holds more than {max_entries:,} capturable files and is not a "
            "git repository, so every one of them would be hashed and uploaded. "
            "That is a workspace, not a project: start the run from the project "
            "directory, or pass max_entries= to raise the ceiling deliberately."
        )

    ignored = _Ignored(ignore, cwd)
    # The SDK's own folders (its outbox, its state, its $TMPDIR stand-ins)
    # when this tree holds one: a job started in $TMPDIR swept its own queue.
    own = _owndirs.current().within(os.path.realpath(cwd))
    for root, dirnames, filenames in os.walk(cwd):
        for name in sorted(dirnames):
            if name in SKIP_DIRS:
                skipped.append(
                    {
                        "path": _posix(os.path.relpath(os.path.join(root, name), cwd)),
                        "reason": "secret" if name in SKIP_SECRET_DIRS else "generated",
                    }
                )
        kept = []
        for d in sorted(dirnames):
            if d in SKIP_DIRS:
                continue
            rel_dir = _posix(os.path.relpath(os.path.join(root, d), cwd))
            if own is not None and own.top(rel_dir) is not None:
                skipped.append({"path": rel_dir, "reason": _owndirs.REASON})
                continue
            if is_tagged_cache_dir(os.path.join(root, d)):
                skipped.append({"path": rel_dir, "reason": "generated"})
                continue
            if not ignored.directory(rel_dir):
                kept.append(d)
        dirnames[:] = kept

        for name in sorted(filenames):
            full = os.path.join(root, name)
            rel = _posix(os.path.relpath(full, cwd))
            if own is not None and own.top(rel) is not None:
                skipped.append({"path": rel, "reason": _owndirs.REASON})
                continue
            reason = _skip_reason(name)
            if reason is not None:
                skipped.append({"path": rel, "reason": reason})
                continue
            if ignored.path(rel):
                continue
            if os.path.islink(full):
                target = os.readlink(full)
                entries.append({
                    "path": rel,
                    "mode": "120000",
                    "sha256": hashlib.sha256(target.encode()).hexdigest(),
                    "size": len(target.encode()),
                    "source": "blob",
                    "symlink_target": target,
                })
                _guard()
                continue
            if not os.path.isfile(full):
                continue
            # Counted BEFORE the hash: reading the file is the cost the ceiling
            # exists to stop paying.
            entries.append({"path": rel})
            _guard()
            entries[-1] = gate.entry(full, rel, reference_over_bytes=reference_over_bytes)

    if include:
        entries.extend(
            _include_entries(
                cwd,
                include,
                # Already decided -- captured, withheld, or skipped and reported --
                # so an include that names one again neither re-adds nor re-reports it.
                # A `.probeignore` exclusion is not in this set: an explicit include wins.
                {e["path"] for e in entries} | {s["path"] for s in skipped},
                reference_over_bytes=reference_over_bytes,
                gate=gate,
                skipped=skipped,
                own=own,
            )
        )
    skipped.extend(ignored.report(entries))
    skipped.extend(gate.skipped)
    # The walk above already includes lockfiles -- they are not in any SKIP
    # filter -- so only the identity tag is new here, matching capture_manifest.
    for e in entries:
        if "/" not in e["path"] and _is_lockfile(e["path"]):
            e["lockfile"] = True
    entries.sort(key=lambda e: e["path"])

    return {
        "entries": entries,
        "tree_sha256": tree_digest(entries),
        "base_commit": None,
        "remote": None,
        "n_git_referenced": 0,
        "n_pending_upload": sum(1 for e in entries if e["source"] == "blob"),
        "n_referenced_offsite": sum(1 for e in entries if e["source"] == "reference"),
        "n_withheld": sum(1 for e in entries if e["source"] == "withheld"),
        "vcs": None,
        "skipped": skipped,
        **({"n_probeignore": ignored.count} if ignored.count else {}),
    }
from probe.sdk.capture.code.content_gate import _ContentGate  # noqa: E402 -- pieces need each other; the front door loads this one first
