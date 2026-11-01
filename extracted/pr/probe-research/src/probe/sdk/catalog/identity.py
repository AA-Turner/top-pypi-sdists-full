"""Work out a dataset's identity (remote pointer, or local files hashed off-thread within a budget) and its registration body."""

from __future__ import annotations
import hashlib
import math
import os
import re
import socket
import threading
import time
from dataclasses import dataclass
from typing import Any, Iterable, Mapping
from .vocab import HashMode, Identity
from probe.sdk.catalog.manifest import Manifest, ManifestFile, _hash_cache, _levels, _shown_relpath, build_manifest
from probe.sdk.catalog.refs import CatalogRefused, check_name, ref_of
from probe.sdk.catalog.server import _warn_once

#: Counts a version's `change.stats` may carry (whole numbers >= 0): the server's closed
#: list (`app.catalog.datasets.CHANGE_STAT_KEYS`), which refuses the WHOLE registration over
#: one other key, so the SDK drops it first.
CHANGE_STAT_KEYS: tuple[str, ...] = ("files", "bytes", "rows", "tokens", "removed")
#: Budget-mode hashing stops starting files after this long; the rest stay unhashed and the
#: version is `partial`. It runs on a daemon thread waited for at most this plus
#: `HASH_GRACE_SECONDS` (a stalled mount costs the call, never the job).
HASH_DEADLINE_SECONDS = 120.0
#: Same bound for `hash="full"` and hosting (`upload=True`), which read every byte: 1 hour, waited in 1 s slices (Ctrl-C interrupts).
FULL_HASH_DEADLINE_SECONDS = 3600.0
#: Wind-down allowance past the deadline (the file in progress stops at its next 1 MiB) before the call gives up.
HASH_GRACE_SECONDS = 30.0
#: Schemes a pointer may use; anything else with `://` is refused here.
_SCHEME = re.compile(r"^([A-Za-z][A-Za-z0-9+.-]*)://")


def pointer_hash(uri: str, revision: str | None = None) -> str:
    """A remote pointer's identity: ``sha256("uri\\nrevision")`` (C3)."""
    return hashlib.sha256(f"{uri}\n{revision or ''}".encode()).hexdigest()


@dataclass
class Prepared:
    """A dataset's identity, ready to register."""

    uri: str
    content_hash: str
    size_bytes: int | None
    identity: str
    meta: dict
    manifest: Manifest | None = None
    #: The local file or folder, or None for a remote uri.
    local: str | None = None
    #: The `.probe.config` level of ``local`` (`on` or `hash`).
    level: str = "on"


def _remote(path_or_uri: str) -> str | None:
    """The uri if ``path_or_uri`` is remote (`s3://`, `hf://`, `https://`), else None (local, `file://` included)."""
    match = _SCHEME.match(path_or_uri)
    if not match or match.group(1).lower() == "file":
        return None
    return path_or_uri


def prepare(
    path_or_uri: str | os.PathLike,
    *,
    hash_mode: str = HashMode.BUDGET.value,
    budget: list[int] | None = None,
    upload: bool = False,
) -> Prepared:
    """Work out what is registered: a remote pointer, or a local file/folder hashed within
    ``budget`` (every byte for ``hash_mode="full"`` or ``upload``). Raises `CatalogRefused`
    for a path a `.probe.config` excludes, a missing path, or an upload of a `hash` path."""
    from ..recording_rules import recording_rules as exclusions
    from .. import probe_config as pc
    from ..artifact.hashing import local_file_uri

    try:
        mode = HashMode(str(hash_mode))
    except ValueError:
        raise CatalogRefused(f"hash must be one of {', '.join(m.value for m in HashMode)}, not {hash_mode!r}") from None
    raw = os.fspath(path_or_uri)
    remote = _remote(raw)
    if remote is not None:
        if upload:
            raise CatalogRefused(f"{remote} is remote: Probe can only host local files (leave out upload)")
        return Prepared(
            uri=remote,
            content_hash=pointer_hash(remote),
            size_bytes=None,
            identity=Identity.POINTER.value,
            meta={"identity": Identity.POINTER.value},
        )
    local = pc.local_path_of(raw) or raw
    local = os.path.abspath(os.path.expanduser(local))
    if not os.path.exists(local):
        raise CatalogRefused(f"no such file or folder: {local}")
    is_dir = os.path.isdir(local)
    on, hash_level, _read, _off = _levels()
    verdict = exclusions.excluded(local, is_dir=is_dir)
    level = getattr(verdict, "level", on if not verdict.excluded else pc.OFF)
    if level not in (on, hash_level):
        raise CatalogRefused(
            f"`{pc.shown(local)}` is excluded by `{exclusions.source(verdict)}`, so nothing was recorded about it"
        )
    if upload and level == hash_level:
        raise CatalogRefused(
            f"`{pc.shown(local)}` is `hash` in `{exclusions.source(verdict)}`: Probe records its identity "
            "only and never uploads it (leave out upload to register it as a reference)"
        )
    full = upload or mode is HashMode.FULL
    spend = [1 << 62] if full else (budget if budget is not None else _fresh_budget())
    bound = FULL_HASH_DEADLINE_SECONDS if full else HASH_DEADLINE_SECONDS
    deadline = time.monotonic() + bound
    hashed_level = level == hash_level
    host = socket.gethostname()
    meta: dict[str, Any] = {"local_path": local, "host": host}
    content_hash = size = rows = None
    identity = Identity.BYTES.value
    got, manifest = _hash_off_thread(
        lambda: _hash_local(local, single=not is_dir, upload=upload, spend=spend, deadline=deadline,
                            hashed_level=hashed_level, full=full),
        deadline=deadline,
        what=pc.shown(local),
        bound=bound,
    )
    if got is not None:
        size, rows, content_hash = got.get("size_bytes"), got.get("rows"), got.get("content_hash")
    if manifest is not None:
        content_hash = manifest.identity()
        size = manifest.total_bytes
        rows = manifest.total_rows
        identity = Identity.PARTIAL.value if manifest.partial else Identity.BYTES.value
        meta["files"] = len(manifest.files)
        if manifest.excluded:
            meta["excluded"] = manifest.excluded
        meta["rows_complete"] = manifest.rows_complete
    if rows is not None:
        meta["rows"] = rows
    meta["identity"] = identity
    if level == hash_level:
        meta["identity_only"] = True
    return Prepared(
        uri=local_file_uri(local),
        content_hash=str(content_hash),
        size_bytes=size,
        identity=identity,
        meta=meta,
        manifest=manifest,
        local=local,
        level=level,
    )


def identity_meta(local: str, run_id: str) -> dict:
    """What a `hash`-level path's reference row records beyond its location
    (`Run.log_artifact(reference=True)` under a `.probe.config` `hash` rule):
    ``identity_only``, plus its dataset-rule identity from the run's one hashing budget
    (a file's sha256, or its fingerprint over 1 GiB/past budget; a folder's manifest) as
    ``fingerprint`` (the key the server pins a hashless checkpoint's bytes by), with
    ``identity`` `bytes` or `partial`. Never raises: a gone/unreadable path records location only."""
    from ..capture import lineage as inputs

    meta: dict[str, Any] = {"identity_only": True}
    budget = inputs.run_hash_budget(run_id)
    before = budget[0]
    try:
        prepared = prepare(local, budget=budget)
    except Exception:  # noqa: BLE001 -- the identity is evidence, never the call's failure
        return meta
    finally:
        inputs.charge_run_hash(run_id, before - budget[0])
    meta.update(fingerprint=prepared.content_hash, identity=prepared.identity)
    if prepared.meta.get("rows") is not None:
        meta["rows"] = prepared.meta["rows"]
    return meta


def _hash_local(
    local: str, *, single: bool, upload: bool, spend: list[int], deadline: float, hashed_level: bool, full: bool
) -> tuple[dict | None, Manifest | None]:
    """The walk and hashing `prepare` waits for: ``(identity, None)`` for a fully hashed single
    file, else ``(None, manifest)``. Runs on a worker thread; its opens are Probe's own, not the run's reads."""
    if single and not upload:
        from probe.sdk.catalog.manifest import _identify  # call time: one binding, in manifest, for tests to patch

        cache = _hash_cache()
        try:
            got = _identify(local, budget=spend, deadline=deadline, hash_level=hashed_level, full=full, cache=cache)
        finally:
            cache.flush()
        if got is None:
            raise CatalogRefused(f"{local} could not be read")
        if got.get("content_hash"):
            return got, None
        # Fingerprinted/over budget/under the hash floor: a one-file partial manifest.
        manifest = Manifest(identity_only=hashed_level, partial=True)
        manifest.files.append(ManifestFile(
            relpath=_shown_relpath(os.path.basename(local)), size_bytes=int(got.get("size_bytes") or 0),
            fingerprint=got.get("fingerprint"), rows=got.get("rows"), full=local,
        ))
        return None, manifest
    manifest = build_manifest(local, budget=spend, deadline=deadline, require_full=upload, full=full)
    if not manifest.files:
        raise CatalogRefused(f"{local} holds no file Probe may record")
    if upload and manifest.identity_only:
        from .. import probe_config as pc

        raise CatalogRefused(
            f"`{pc.shown(local)}` holds files a `.probe.config` sets to `hash`: Probe records their identity "
            "only and never uploads them (leave out upload to register it as a reference)"
        )
    return None, manifest


def _hash_off_thread(work: Any, *, deadline: float, what: str, bound: float) -> Any:
    """``work()`` on a daemon thread, waited in 1 s slices (Ctrl-C interrupts) until
    ``deadline`` plus `HASH_GRACE_SECONDS`, as `inputs.reference_hash`: a stalled mount
    costs this call, never the training thread. Raises what ``work`` raised."""
    from ..capture import lineage as inputs

    box: dict[str, Any] = {}

    def run() -> None:
        with inputs.internal():
            try:
                box["result"] = work()
            except BaseException as exc:  # noqa: BLE001 - handed to the caller
                box["error"] = exc

    worker = threading.Thread(target=run, name="probe-dataset-hash", daemon=True)
    worker.start()
    give_up = deadline + HASH_GRACE_SECONDS
    while worker.is_alive():
        left = give_up - time.monotonic()
        if left <= 0:
            raise CatalogRefused(
                f"hashing `{what}` did not finish within {bound:g}s (a stalled mount?); nothing was recorded"
            )
        worker.join(min(1.0, left))
    if "error" in box:
        raise box["error"]
    return box["result"]


def _fresh_budget() -> list[int]:
    from ..capture import lineage as inputs

    return [inputs.RUN_HASH_BUDGET_BYTES]


def run_file_spec(run_id: str, name: str, prepared: Prepared) -> dict:
    """`run_file` in `POST /v1/catalog/datasets`: the producing run's file."""
    return {
        "run_id": run_id,
        "name": name,
        "uri": prepared.uri,
        "content_hash": prepared.content_hash,
        "size_bytes": prepared.size_bytes,
        "identity": prepared.identity,
        "meta": dict(prepared.meta),
    }


def reference_spec(prepared: Prepared) -> dict:
    """`reference` in `POST /v1/catalog/datasets`: a pointer no run produced."""
    return {
        "uri": prepared.uri,
        "content_hash": prepared.content_hash,
        "size_bytes": prepared.size_bytes,
        "identity": prepared.identity,
    }


def _stat_count(value: Any) -> int | None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return None
    if isinstance(value, float) and (not math.isfinite(value) or value != int(value)):
        return None
    return int(value) if value >= 0 else None


def change_stats(stats: Mapping[str, Any]) -> dict[str, int]:
    """The `stats` the server takes: `CHANGE_STAT_KEYS` with whole counts >= 0. Others are
    dropped with one warning per key (the server would refuse the whole registration)."""
    kept: dict[str, int] = {}
    for key, value in stats.items():
        count = _stat_count(value)
        if key in CHANGE_STAT_KEYS and count is not None:
            kept[key] = count
            continue
        why = (
            f"`{key}` is not a stat Probe keeps (it keeps {', '.join(CHANGE_STAT_KEYS)})"
            if key not in CHANGE_STAT_KEYS
            else f"stats[{key!r}] must be a whole number >= 0, not {value!r}"
        )
        _warn_once(
            f"log_dataset:stats:{key}",
            f"probe: log_dataset: {why}; it was left out and the dataset is recorded without it. "
            "Put other numbers in `note`.",
        )
    return kept


def registration_body(
    name: str,
    *,
    run_file: dict | None = None,
    reference: dict | None = None,
    hosted: dict | None = None,
    note: str | None = None,
    stats: Mapping[str, Any] | None = None,
    sources: Iterable[Any] = (),
    publish: bool = False,
    description: str | None = None,
    composition: list[dict] | None = None,
) -> dict:
    """The `POST /v1/catalog/datasets` body: exactly one of ``run_file``,
    ``reference`` or ``hosted``."""
    given = [k for k, v in (("run_file", run_file), ("reference", reference), ("hosted", hosted)) if v]
    if len(given) != 1:
        raise CatalogRefused("a registration names exactly one of run_file, reference or hosted")
    body: dict[str, Any] = {"name": check_name(name), given[0]: run_file or reference or hosted}
    if reference:
        from probe.sdk.catalog.catalog import _refuse_credential  # call time: catalog imports this module

        _refuse_credential(reference.get("uri"))
    change: dict[str, Any] = {}
    if note is not None:
        change["note"] = str(note)
    if stats:
        if not isinstance(stats, Mapping):
            raise CatalogRefused("stats must be a mapping of counts, e.g. {'rows': 98796, 'removed': 1204}")
        kept = change_stats(stats)
        if kept:
            change["stats"] = kept
    if change:
        body["change"] = change
    refs = []
    for item in sources or ():
        ref = ref_of(item)
        if not ref:
            raise CatalogRefused(f"source {item!r} has no ref (was it registered?)")
        refs.append(ref)
    if refs:
        body["sources"] = refs
    if publish:
        body["publish"] = True
    if description:
        body["description"] = description
    if composition:
        body["composition"] = composition
    return body
