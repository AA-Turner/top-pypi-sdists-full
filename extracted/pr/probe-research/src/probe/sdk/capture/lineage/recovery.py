"""send (or drop) the spools that dead processes and offline runs left behind, and clear their bindings and folders."""

from __future__ import annotations

import contextlib
import json
import os
import re
import shutil
import time
from pathlib import Path
from typing import Any
from ...recording_rules import ignore as _ignore
#: A dead run's spools are recovered only after they sat this long unchanged.
ORPHAN_AGE_S = 600.0


#: An offline run's id (`offline.LOCAL_PREFIX`): no server knows it yet.
OFFLINE_PREFIX = "local:"


class _OfflineQueue:
    """An offline run's own queue, as the client a recovery delivers to: its
    leftovers join the run's other writes, and ``probe sync`` checks the
    server's features and rewrites ``local:<key>`` when it delivers them."""

    def __init__(self, directory: str) -> None:
        from ...delivery.journal.journal import Journal

        self.journal = Journal(directory)

    @staticmethod
    def supports_feature(name: str) -> bool:
        return name in (FEATURE, OUTPUTS_FEATURE)


def _offline_queue(owner: dict) -> "_OfflineQueue | None":
    directory = owner.get("offline_dir")
    if not isinstance(directory, str) or not os.path.isdir(directory):
        return None
    try:
        return _OfflineQueue(directory)
    except Exception:  # noqa: BLE001
        return None


def recover_orphans(client: Any, *, now: float | None = None, late_only: bool = False) -> int:
    """Send the read and write lists of processes on this host that ended
    without closing their run -- and the hashes a closed run's close ran out
    of time for (`_resend_late`, F7). Returns how many runs had lists queued.

    A spool is an orphan when it is this host's, its process is gone, it sat
    unchanged for ORPHAN_AGE_S, and its run is not one this process records --
    and only for a run of this client's server and credential: another
    tenant's run would dead-letter here with its reads lost. An OFFLINE run's
    leftovers (``local:<key>``, which no server knows) go into its own queue
    for ``probe sync``, never to this client's server; with its queue gone
    they are dropped. ``late_only``: only the late hashes (a later run of
    this process, `start_recovery`)."""
    sent = 0
    now = time.time() if now is None else now
    _clear_dead_bindings()
    root = state_dir()
    if not root.is_dir():
        return 0
    takes_reads = _server_takes(client, FEATURE)
    takes_writes = _server_takes(client, OUTPUTS_FEATURE)
    takes_late = _server_takes(client, OBSERVATIONS_FEATURE)
    reachable = takes_reads is not None and takes_writes is not None
    url, token = _client_url(client), _token_id(client)
    host, me = _host(), os.getpid()
    with internal():
        candidates = [p for p in root.iterdir() if p.is_dir()]
    for directory in candidates:
        run_id = _folder_run(directory.name)
        if run_folder(run_id) != directory.name or run_id in _active:
            continue  # (a folder no run's `run_folder` names is not a run's)
        if not _sdk_owned(directory):
            continue  # the Probe daemon's mailbox shares this folder (#3616)
        offline = run_id.startswith(OFFLINE_PREFIX)
        if not offline and not reachable:
            continue
        try:
            owner = json.loads((directory / "owner.json").read_text())
        except (OSError, ValueError):
            owner = {}
        if not isinstance(owner, dict):
            continue
        if not offline:
            if owner.get("base_url") and url and owner["base_url"] != url:
                continue
            if owner.get("token_id") and token and owner["token_id"] != token:
                continue
        noted = owner.get("writes") is True
        # Late hashes first: a closed run's, complete when written.
        if _late_files(directory):
            late_to = _offline_queue(owner) if offline else client
            if late_to is None or (not offline and takes_late is False):
                for late in _late_files(directory):  # nothing will ever replace those rows
                    with internal(), contextlib.suppress(OSError):
                        late.unlink()
            elif offline or takes_late:
                late_reads = True if offline else bool(takes_reads)
                late_writes = noted and (True if offline else bool(takes_writes))
                if _resend_late(run_id, late_to, reads=late_reads, writes=late_writes):
                    sent += 1
        if late_only:
            continue
        # A live process of the run on this host (the owner, a rank, a probe
        # exec launcher waiting on its child) may still write or send these.
        if _live_here(directory):
            continue
        spools = _collectable_spools(run_id)
        if any(_spool_owner(s) == (host, me) for s in spools):
            continue
        try:
            if any(now - s.stat().st_mtime < ORPHAN_AGE_S for s in spools):
                continue
        except OSError:
            continue
        if not spools:
            _clear_dead_folder(directory, now)
            continue
        if offline:
            target: Any = _offline_queue(owner)
            reads_ok = target is not None
            writes_ok = reads_ok and noted
        else:
            target, reads_ok, writes_ok = client, bool(takes_reads), bool(takes_writes) and noted
        if _recover_one(run_id, spools, owner, target, reads=reads_ok, writes=writes_ok):
            sent += 1
    return sent


#: A file only a run's recorder writes in its folder: ``owner.json``, a
#: ``<host>.<pid>`` spool, live marker or writes sidecar (`_host` never holds a
#: dot), a close marker (`_mark_closed`), or a late-hash file (`_keep_late`),
#: claimed (`_resend_late`) or not.
_RUN_FILE = re.compile(
    r"owner\.json|[\w-]+\.\d+\.(?:jsonl|live|wf\.json)|closed\.[\w-]+\.\d+\.json"
    r"|late\.[\w-]+\.\d+\.json(?:\.\d+\.claimed)?"
)


def _sdk_owned(directory: Path) -> bool:
    """Whether ``directory`` holds a `_RUN_FILE`. The Probe daemon's mailbox
    lives beside the run folders (``asks``, ``requests``, ``messages``,
    ``hints``: `probe.daemon.mailbox.root`) under names a run id could take,
    and holds none: recovery took its folders for dead runs' and deleted
    them, open ``probe ask --writer`` requests included (#3616). A run folder
    without one is not left behind either: `discard` removes it whole."""
    try:
        with internal(), os.scandir(directory) as entries:
            return any(_RUN_FILE.fullmatch(entry.name) for entry in entries)
    except OSError:
        return False


def _recover_one(
    run_id: str, spools: list[Path], owner: dict, target: Any, *, reads: bool, writes: bool
) -> bool:
    """Send (or, when nothing takes them, drop) one dead run's leftover spools
    to ``target``. True when lists were queued."""
    if not reads and not writes:
        _consumed[run_id] = spools
        discard(run_id)
        return False
    try:
        got = collect_all(
            run_id,
            wait_s=FINISH_WAIT_S,
            ignore=_ignore.from_record(owner.get("ignore")),
            reads=reads,
            writes=writes,
            recovered=True,
        )
        got.inputs_coverage["recovered"] = True
        got.outputs_coverage["recovered"] = True
        _deliver(
            target,
            run_id,
            got,
            reads=reads,
            writes=writes,
            observations=_server_takes(target, OBSERVATIONS_FEATURE) is True,
        )
        return True
    except Exception:  # noqa: BLE001
        _consumed.pop(run_id, None)
        return False


def recover_offline(run_id: str, queue_dir: str | os.PathLike) -> bool:
    """``probe sync``'s half: move an offline run's own leftover spools (its
    process died before its close queued them) into its queue at
    ``queue_dir``, now, so this sync delivers them. Only spools of this host's
    ENDED processes, and only when no live process of the run is here (an
    offline run still recording keeps its own); no orphan age is waited out,
    since the queue's owner is the one asking. The hashes its close ran out
    of time for are queued too (F7). True when lists were queued."""
    if not str(run_id).startswith(OFFLINE_PREFIX):
        return False
    directory = run_dir(run_id)
    try:
        if not directory.is_dir() or run_id in _active:
            return False
        owner = _read_owner(run_id)
        queued = bool(
            _late_files(directory)
            and _resend_late(
                run_id, _OfflineQueue(os.fspath(queue_dir)), reads=True, writes=owner.get("writes") is True
            )
        )
        if _live_here(directory):
            return queued
        spools = _collectable_spools(run_id)
        if not spools:
            return queued
        return queued | _recover_one(
            run_id,
            spools,
            owner,
            _OfflineQueue(os.fspath(queue_dir)),
            reads=True,
            writes=owner.get("writes") is True,
        )
    except Exception:  # noqa: BLE001 -- lineage never stops a sync
        return False


def _clear_dead_bindings() -> None:
    """Remove the binding files (F5) of this host's owners that ended
    without unbinding (their lock is free): no worker follows them."""
    host, me = _host(), os.getpid()
    with internal():
        for lock in (state_dir().parent / "bind").glob(f"{host}.*.lock"):
            parts = lock.name.split(".")
            try:
                pid = int(parts[1])
            except (IndexError, ValueError):
                continue
            if pid == me:
                # Never this process's own: on NFS flock is a POSIX lock, which
                # its own request never conflicts with and which closing ANY
                # handle to the file drops -- the probe would release the lock
                # it tests, and find this process "dead".
                continue
            if _owner_alive(str(lock), pid):
                continue
            for path in (lock.with_suffix(".json"), lock):
                with contextlib.suppress(OSError):
                    path.unlink()


def _clear_dead_folder(directory: Path, now: float) -> None:
    """A run folder with no spool left: remove it once no process may still
    write its first -- no live marker, and older than ORPHAN_AGE_S."""
    if any(directory.glob("*.jsonl")) or _late_files(directory) or _live_elsewhere(directory):
        return
    try:
        age = now - directory.stat().st_mtime
    except OSError:
        return
    if age < ORPHAN_AGE_S:
        return
    with internal():
        _drop_markers(directory)
        shutil.rmtree(directory, ignore_errors=True)
from probe.sdk.capture.lineage.finishing import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    FEATURE,
    OBSERVATIONS_FEATURE,
    OUTPUTS_FEATURE,
    _consumed,
    _deliver,
    _late_files,
    _read_owner,
    _server_takes,
    discard,
)
from probe.sdk.capture.lineage.lineage import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    FINISH_WAIT_S,
    _active,
    _client_url,
    _owner_alive,
    _resend_late,
    _token_id,
    collect_all,
)
from probe.sdk.capture.lineage.spool.reader import _collectable_spools  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.lineage.spool.spool import (  # noqa: E402 -- pieces need each other; the front door loads this one first
    _drop_markers,
    _folder_run,
    _host,
    _live_elsewhere,
    _live_here,
    _spool_owner,
    internal,
    run_dir,
    run_folder,
    state_dir,
)
