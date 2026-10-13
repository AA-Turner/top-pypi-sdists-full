"""How the Hugging Face and Lightning integrations record one saved checkpoint.

Two modes, chosen with ``checkpoints=`` on ``ProbeCallback`` / ``ProbeLogger``,
else ``PROBE_CHECKPOINTS`` (the only way to choose with ``report_to="probe"``,
which builds the callback itself), else ``"reference"``:

* ``"reference"`` -- one ``kind="checkpoint"`` row that records WHERE the
  checkpoint is (path, host, size); no bytes leave the machine. On a job's own
  throwaway disk (a container, a pod, CI) that location is gone with the job,
  so the first such save warns once, naming ``"upload"``.
* ``"upload"`` -- every save is its own SET, named ``<name>@step<N>``: each
  regular file of the checkpoint (the file itself, or every file under the
  folder) is uploaded as a ``kind="file"`` row named ``<set>/<path in the
  checkpoint>``, and ONE index row, ``<set>``, is the save's ``checkpoint`` row:
  a reference to where it was saved, with ``meta.members`` (the paths) and
  ``meta.upload = "requested"``.

Why an index row plus members, and never ``checkpoint`` members:

* the failed-run alert names, and the disk-space finding sizes against, the
  NEWEST ``checkpoint`` row -- a member such as ``scheduler.pt`` would win;
* ``best`` / ``last`` / ``superseded`` / ``deleted`` change after the save, and
  only a hashless reference row can be refreshed in place (the server keys it
  on run, name and uri); an uploaded row cannot be edited, so its flags would
  stay what they were at the save;
* a set per save means a folder rewritten in place (Lightning's sharded
  ``last.ckpt/``) never mixes files from two saves under one name.

The index never claims the bytes are stored: each member's own row says that
(``probe.sdk.checkpoints.is_stored``). Members go through ``run.log_artifact``,
so a file under 64 MiB is one upload and a bigger one multipart (hardlink
staged); one the upload refuses or cannot stage becomes a reference row with a
warning, as for any ``log_artifact`` call. Members are never uploaded
``strict`` (that would be synchronous, on the training thread). Queueing still
copies on the calling thread a file up to 64 MiB (into the outbox) and a bigger
one kept on another filesystem than the outbox (to stage it), and uploads
everything there when uploads are not queued at all, so a set needing more than
:data:`CROSS_DEVICE_STAGE_MAX_BYTES` of that is recorded as a location only,
with a warning naming ``PROBE_OUTBOX_DIR``; work that still takes
:data:`SLOW_SAVE_SECONDS` warns once too. Files a ``.probe.config`` excludes
are neither uploaded nor named; the index counts them (``members_excluded``)
so a restore says it is not the whole checkpoint. A file the server would
refuse to name (``_server_takes``) makes the set a location only.

A file the trainer rewrites IN PLACE (Lightning's ``last.ckpt``, a sharded
folder saved again) before its earlier save finished uploading changes the
hard-linked staged copy too: that upload is then abandoned and its file reads
as not stored, so the earlier set never downloads as a mix of two saves.

Known limits (stated, not handled): Lightning's ``AsyncCheckpointIO`` writes
after ``after_save_checkpoint`` returns, so upload mode can read a file still
being written -- do not combine them; staged hard links keep a pruned save's
bytes on disk until it is uploaded, so a save rate above upload bandwidth
grows the disk use the trainer meant to free.

What rank 0 sees is what is uploaded: a sharded checkpoint whose shards sit
on each NODE's own disk is not gathered from the other nodes. Save sharded
checkpoints to storage every node shares to upload them whole.
"""

from __future__ import annotations

import hashlib
import os
import time
import unicodedata
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from probe.sdk import ephemeral, exclusions
from probe.sdk.filetype import file_extension
from probe.sdk.checkpoints import EXCLUDED_KEY, MEMBER_OF_KEY, MEMBERS_KEY, UPLOAD_KEY, UPLOAD_REQUESTED

#: The two ways a kept checkpoint is recorded.
REFERENCE = "reference"
UPLOAD = "upload"
MODES = (REFERENCE, UPLOAD)

#: Chooses the mode when the constructor did not.
ENV = "PROBE_CHECKPOINTS"

#: A checkpoint with more files than this is recorded as a location only, with
#: a warning: each member is one upload and one row.
MAX_MEMBERS = 1000

#: Folder entries (files and folders) the walk looks at before it gives up: it
#: runs on the training thread.
MAX_WALK_ENTRIES = 20_000

#: Staging (or uploading) a set for longer than this on the training thread is
#: worth one warning.
SLOW_SAVE_SECONDS = 10.0

#: A set needing more than this copied or sent on the training thread to queue
#: it (`_foreground_bytes`) is recorded as a location only, with a warning: the
#: work holds rank 0's training thread, and a distributed job's other ranks time
#: out waiting for it (HF's default ``ddp_timeout`` is 1800 s).
CROSS_DEVICE_STAGE_MAX_BYTES = 2 * 1024**3

Warn = Callable[[str, str], None]


def resolve_mode(passed: str | None, warn: Warn) -> str:
    """The mode: ``passed`` (a wrong value raises, as a wrong argument does),
    else ``PROBE_CHECKPOINTS`` (a wrong value warns once and means
    ``"reference"``: an environment variable must never fail the job), else
    ``"reference"``."""
    if passed is not None:
        if passed not in MODES:
            raise ValueError(f"checkpoints must be one of {MODES}, not {passed!r}")
        return passed
    value = (os.environ.get(ENV) or "").strip().lower()
    if not value:
        return REFERENCE
    if value not in MODES:
        warn(
            "checkpoints_env",
            f"probe: {ENV}={value!r} is not one of {', '.join(MODES)}; checkpoints are "
            "recorded as their location only.",
        )
        return REFERENCE
    return value


def set_name(name: str, step: int | None, *, salt: str = "") -> str:
    """The name of one save's set: ``<name>@step<N>``, the step before a file
    extension (``last@step8.ckpt``) so the name keeps it -- the SDK would
    otherwise put the extension back after the step (`name_with_extension`).
    ``salt`` (``~a1b2c3``) tells apart two paths with one basename saved at one
    step (two Lightning callbacks' ``last.ckpt``)."""
    tag = (f"@step{step}" if step is not None else "") + (f"~{salt}" if salt else "")
    extension = file_extension(name)
    if extension:
        return f"{name[: -len(extension) - 1]}{tag}.{extension}"
    return f"{name}{tag}"


def _unique_set_name(name: str, step: int | None, local: str, taken: dict[str, str]) -> str:
    """The set's name, unique in this run: members are found by name, so two
    sets sharing one would share (and overwrite) members."""
    if step is None:
        # No step to tell two saves of one path apart (a custom Lightning
        # callback): every save is its own set all the same.
        return set_name(name, None, salt=hashlib.sha256(f"{local}:{time.time_ns()}".encode()).hexdigest()[:8])
    index = set_name(name, step)
    if taken.get(index, local) != local:
        index = set_name(name, step, salt=hashlib.sha256(local.encode()).hexdigest()[:6])
    taken[index] = local
    return index


@dataclass
class Inventory:
    """What one checkpoint holds, as far as Probe may record it."""

    #: (path in the checkpoint, NFC as the server stores names; full path)
    files: list[tuple[str, str]] = field(default_factory=list)
    #: Paths left out for a reason other than ``.probe.config``: a link (it can
    #: point anywhere), a non-regular file, an unreadable folder, two names that
    #: are one after NFC. Any of these makes the set incomplete.
    skipped: list[str] = field(default_factory=list)
    #: More than MAX_MEMBERS files, or MAX_WALK_ENTRIES entries looked at.
    too_many: bool = False
    #: Files a `.probe.config` excludes: counted (never named) on the index, so
    #: a restore says it is not the whole checkpoint.
    excluded: int = 0


def inventory(local: str) -> Inventory:
    """The checkpoint's regular files, sorted. A file is its own one member (a
    LINK to one -- Lightning's ``save_last="link"`` -- is followed: the path is
    the checkpoint the trainer named). Inside a folder links are never followed
    and make the set incomplete. What a researcher's ``.probe.config``
    excludes is not a member and is not named; an excluded folder is not
    walked. The walk stops after :data:`MAX_WALK_ENTRIES` entries: it runs on
    the training thread."""
    check = exclusions.checker(hot=True)
    if os.path.isfile(local):
        real = os.path.realpath(local)
        if check.check(local, is_dir=False).excluded or check.check(real, is_dir=False).excluded:
            return Inventory(excluded=1)
        rel = _nfc(os.path.basename(local))
        return Inventory(files=[(rel, real)], skipped=[] if _server_takes(rel) else [rel])
    found = Inventory()
    errors: list[OSError] = []
    seen = 0
    for root, dirs, leaves in os.walk(local, followlinks=False, onerror=errors.append):
        seen += len(dirs) + len(leaves)
        if seen > MAX_WALK_ENTRIES:
            return Inventory(files=found.files, skipped=found.skipped, too_many=True)
        kept_dirs = []
        for d in sorted(dirs):
            full = os.path.join(root, d)
            if check.check(full, is_dir=True).excluded:
                found.excluded += 1  # the folder counts once: what is inside it is not looked at
                continue
            if os.path.islink(full):
                found.skipped.append(_rel(full, local))
                continue
            kept_dirs.append(d)
        dirs[:] = kept_dirs
        for leaf in sorted(leaves):
            full = os.path.join(root, leaf)
            if check.check(full, is_dir=False).excluded:
                found.excluded += 1
                continue
            rel = _rel(full, local)
            if os.path.islink(full) or not os.path.isfile(full) or not _server_takes(rel):
                found.skipped.append(rel)
                continue
            found.files.append((rel, full))
            if len(found.files) > MAX_MEMBERS:
                return Inventory(files=found.files, skipped=found.skipped, too_many=True)
    found.skipped.extend(_rel(e.filename or local, local) for e in errors)
    names = [rel for rel, _full in found.files]
    found.skipped.extend(sorted({rel for rel in names if names.count(rel) > 1}))
    return found


def _server_takes(rel: str) -> bool:
    """Whether the server would take ``rel`` inside a set's name: its rules
    (``app/artifacts/schemas.py`` ``validate_artifact_name``) refuse a control,
    format or surrogate character, a backslash, a segment padded with
    whitespace or over 255 bytes. A file it refuses could never come back."""
    if "\\" in rel or any(unicodedata.category(c) in ("Cc", "Cf", "Cs") for c in rel):
        return False
    return all(seg and seg == seg.strip() and len(seg.encode("utf-8")) <= 255 for seg in rel.split("/"))


def _rel(full: str, local: str) -> str:
    return _nfc(os.path.relpath(full, local).replace(os.sep, "/"))


def _nfc(name: str) -> str:
    return unicodedata.normalize("NFC", name)


def _foreground_bytes(run: Any, files: list[tuple[str, str]]) -> int:
    """Bytes of ``files`` that queueing them would COPY or UPLOAD on this, the
    training, thread: everything when uploads are not queued (``PROBE_ASYNC=0``,
    ``PROBE_ASYNC_UPLOADS=0``, a client with no outbox); otherwise a file up to
    the multipart threshold (copied into the outbox) and a bigger one kept on
    another filesystem than the outbox (copied to stage). A bigger one on the
    outbox's filesystem stages by hard link, at no cost."""
    from probe.sdk import multipart

    client = getattr(run, "_client", None)
    queued = bool(getattr(client, "async_writes", False)) and (
        (os.environ.get("PROBE_ASYNC_UPLOADS") or "").strip().lower() not in ("0", "false", "no", "off")
    )
    try:
        outbox = os.stat(client.journal.dir).st_dev if queued else None
    except Exception:  # noqa: BLE001 -- no outbox: every upload runs in the foreground
        outbox, queued = None, False
    threshold = multipart.threshold_bytes()
    total = 0
    for _rel, full in files:
        try:
            info = os.stat(full)
        except OSError:
            continue
        if not queued or info.st_size <= threshold or info.st_dev != outbox:
            total += info.st_size
    return total


def warn_if_throwaway(local: str, warn: Warn) -> None:
    """A location-only checkpoint on storage that is gone with the job: say so
    once, naming the mode that keeps it."""
    try:
        where = ephemeral.describe(local)
    except Exception:  # noqa: BLE001 -- a mount table we cannot read is no reason to warn
        return
    if where.get("durable", True):
        return
    fstype = where.get("fstype")
    warn(
        "checkpoint_throwaway",
        f"probe: checkpoint {local} is on this job's own disk ({fstype or where.get('reason')}), "
        "which is gone when the job ends; Probe records only where it is. Pass "
        f'checkpoints="{UPLOAD}" (or set {ENV}={UPLOAD}) to store its files, or save '
        "checkpoints to a bucket or a mounted volume.",
    )


def upload_set(
    run: Any,
    local: str,
    *,
    name: str,
    step: int | None,
    meta: dict[str, Any],
    size: int | None,
    strict: bool | None,
    warn: Warn,
    taken: dict[str, str] | None = None,
) -> tuple[str, dict[str, Any]]:
    """Upload one save's files and write its index row. Returns the index row's
    name and the meta it was written with (what a later refresh re-sends).
    ``taken`` is the caller's set names in this run -> their path.

    A set that would be incomplete or too costly -- past :data:`MAX_MEMBERS`
    files, holding a file Probe would leave out, needing a cross-disk copy
    over :data:`CROSS_DEVICE_STAGE_MAX_BYTES`, or with no files -- is written
    as a location only, with a warning, and carries no ``members``: an index
    lists every file of the checkpoint or none."""
    index = _unique_set_name(name, step, local, {} if taken is None else taken)
    found = inventory(local)
    files = found.files
    index_meta = dict(meta)
    copied = _foreground_bytes(run, files) if files and not (found.too_many or found.skipped) else 0
    if found.too_many:
        warn(
            "checkpoint_members",
            f"probe: checkpoint {local} has more than {MAX_MEMBERS} files; Probe records only where it is.",
        )
    elif found.skipped:
        warn(
            "checkpoint_incomplete",
            f"probe: checkpoint {local} holds files Probe does not upload (links, files it cannot "
            f"read, names that collide): {', '.join(found.skipped[:3])}"
            + (", ..." if len(found.skipped) > 3 else "")
            + "; so that a download is never a partial checkpoint, Probe records only where it is.",
        )
    elif not files:
        warn("checkpoint_members", f"probe: checkpoint {local} has no files Probe may record; Probe records only where it is.")
    elif copied > CROSS_DEVICE_STAGE_MAX_BYTES:
        warn(
            "checkpoint_cross_device",
            f"probe: queueing checkpoint {os.path.basename(local)} for upload would copy or send "
            f"{copied / 1024**3:.1f} GB on the training thread (its files are small, on another disk "
            "than Probe's outbox, or uploads are not queued); Probe records only where it is. Set "
            "PROBE_OUTBOX_DIR to a folder on the checkpoint's disk to upload it (big files then "
            "stage by hard link).",
        )
    else:
        started = time.monotonic()
        for rel, full in files:
            # Never strict: a strict upload runs synchronously, on the training
            # thread, for a file that can be many GB. `strict` still decides
            # whether a failure of the checkpoint ROW raises (below).
            run.log_artifact(
                f"{index}/{rel}",
                path=full,
                kind="file",
                step_index=step,
                meta={MEMBER_OF_KEY: index},
                strict=False,
            )
        index_meta[MEMBERS_KEY] = [rel for rel, _full in files]
        index_meta[UPLOAD_KEY] = UPLOAD_REQUESTED
        if found.excluded:
            index_meta[EXCLUDED_KEY] = found.excluded
        took = time.monotonic() - started
        if took >= SLOW_SAVE_SECONDS:
            warn(
                "checkpoint_slow",
                f"probe: queueing checkpoint {os.path.basename(local)} for upload held training "
                f"for {took:.0f}s, most likely copying it to another disk to stage it. Set "
                "PROBE_OUTBOX_DIR to a folder on the checkpoint's own disk to stage by hard link.",
            )
    run.log_artifact(
        index,
        path=local,
        kind="checkpoint",
        reference=True,
        allow_missing=True,
        size_bytes=size,
        step_index=step,
        meta=dict(index_meta),
        strict=strict,
    )
    return index, index_meta
