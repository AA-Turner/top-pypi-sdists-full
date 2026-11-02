"""parse the op folder once, quarantine what does not parse, sweep stale temps, and requeue or list dead letters."""

from __future__ import annotations

import errno
import json
import os
from pathlib import Path
import time

from probe.foundation.durable.durable import SYNC_NONE, file_lock, fsync_directory, now_iso, write_text_atomic

#: Dead letters status.json remembers (plan 1.7), and how much of each error.
_RECENT_DEAD_LETTERS = 32
#: Op-file bytes whose parsed ops a journal keeps between drain passes (`Journal._scan_ops`):
#: about 4,300 one-point `log()` writes. Parsed, an op takes 4-7x its file size; uncapped,
#: 20k queued one-point ops held 58 MB in a long-lived exporter on the training node, with
#: this cap 12.4 MB (5,000 twenty-point ops: 8.2 MB). Ops past it are parsed again each pass.
SCAN_CACHE_MAX_BYTES = 2 * 1024 * 1024


#: A dead letter's read failing with one of these is this process's state (no file handle
#: left, a signal), not the file's: it is not counted torn.
_READ_LATER_ERRNOS = frozenset({errno.EMFILE, errno.ENFILE, errno.EINTR, errno.EAGAIN, errno.ENOMEM})


class FailuresMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

    def quarantine_corrupt(self) -> int:
        """Move unparseable op files to failed/ so they stay VISIBLE. Silently skipping them
        (codex) let status count files the drain never saw: the worker exited 'empty' while the
        banner re-kicked it forever. Quarantined files keep their names: they count as failed in
        status.json while the (parse-skipping) readers ignore them. The queue is parsed OUTSIDE the
        append lock (plan 1.9); only the corrupt files are re-checked under it
        (`quarantine_paths`).
        """
        ops, corrupt = self._scan_ops()
        return self.quarantine_paths(corrupt, known=op_meta(ops))

    def _scan_ops(
        self, stamps: dict | None = None
    ) -> tuple[list[tuple[Path, dict]], list[Path]]:
        """ONE parse of ``ops/``, taken outside every lock: the ops in FIFO order and the paths
        that did not parse (for `quarantine_paths`). Op files appear by atomic rename, so one that
        does not parse is corrupt, not half-written. One vanished between listing and read was
        delivered or moved by someone else and is skipped. ``stamps`` gets each parsed op's
        (inode, size, mtime): how a pass that let go of the drain lock tells an op another drain
        changed (#3618).
        """
        if not self.ops_dir.exists():
            return [], []
        ops: list[tuple[Path, dict]] = []
        corrupt: list[Path] = []
        # Plan 1.6 review: a worker delivering one run while another sits in backoff re-scanned
        # the parked run's ops every pass; at 20k parked ops that held a core for the whole
        # outage. An op file unchanged since the last pass (same inode, size, mtime) and not
        # attempted by the drain (`_scan_forget`) is not parsed again. Only the first
        # `SCAN_CACHE_MAX_BYTES` of op files are kept: the cache outlives the pass and unbounded
        # held 58 MB at 20k ops.
        cache = self.__dict__.setdefault("_scan_cache", {})
        seen: dict = {}
        kept = 0
        for name in sorted(n for n in os.listdir(self.ops_dir) if n.endswith(".json")):
            path = self.ops_dir / name
            try:
                stat = os.stat(path)
                stamp = (stat.st_ino, stat.st_size, stat.st_mtime_ns)
                cached = cache.get(name)
                if cached is not None and cached[0] == stamp:
                    op = cached[1]
                else:
                    op = json.loads(path.read_text())
                if kept + stat.st_size <= SCAN_CACHE_MAX_BYTES:
                    seen[name] = (stamp, op)
                    kept += stat.st_size
                if stamps is not None:
                    stamps[name] = stamp
                ops.append((path, op))
            except FileNotFoundError:
                continue
            except (OSError, json.JSONDecodeError, ValueError):
                corrupt.append(path)
        self._scan_cache = seen
        return ops, corrupt

    def _scan_forget(self, name: str) -> None:
        """The drain is about to attempt this op (it may change it in memory): the next pass reads
        it from disk again."""
        cache = self.__dict__.get("_scan_cache")
        if cache is not None:
            cache.pop(name, None)

    def quarantine_paths(self, paths: list[Path], *, known: dict | None = None) -> int:
        """Move the given op files to failed/ if they STILL do not parse, re-checking only them
        under the append lock. ``known`` (from `op_meta`) lets the status recount skip re-parsing
        the rest."""
        if not paths:
            return 0
        moved = 0
        torn: list[dict] = []
        with file_lock(self.append_lock):
            for path in paths:
                try:
                    json.loads(path.read_text())
                    continue  # parses now: not ours to move
                except FileNotFoundError:
                    continue
                except (OSError, json.JSONDecodeError, ValueError):
                    os.replace(path, self.failed_dir / path.name)
                    moved += 1
                    # What a power cut leaves of an op `log()` had not yet fsynced (plan T6): no
                    # run id survives in it, so it is counted, never attributed to a run.
                    torn.append(
                        {
                            "run_ref": None,
                            "op_id": path.name.rsplit("-", 1)[-1][: -len(".json")],
                            "error": "torn: an empty or unparseable op file (a power cut?)",
                            "status": None,
                            "reason": "torn",
                        }
                    )
            if moved:
                fsync_directory(self.failed_dir)
                fsync_directory(self.ops_dir)
                self._write_status_locked(known=known, torn_delta=moved, new_dead_letters=torn)
        return moved

    def read_failed(self) -> tuple[list[tuple[Path, dict]], int]:
        """The dead letters in failed/ (as `failed()`) and how many files there are torn (empty,
        unparseable or unreadable for good: what a power cut leaves, plan T6, and what
        `quarantine_paths` moves here as torn), in one pass over a folder nothing caps. Counted
        from the files, not status.json's `torn` tally, which an older SDK's status rewrite
        drops (review of #3785, I11)."""
        try:
            names = sorted(name for name in os.listdir(self.failed_dir) if name.endswith(".json"))
        except OSError:
            return [], 0
        letters: list[tuple[Path, dict]] = []
        torn = 0
        for name in names:
            path = self.failed_dir / name
            try:
                letters.append((path, json.loads(path.read_text())))
            except FileNotFoundError:
                continue  # gone meanwhile
            except OSError as exc:
                if exc.errno not in _READ_LATER_ERRNOS:
                    torn += 1  # unreadable for good (EACCES, EIO): as `quarantine_paths` counted it
            except ValueError:
                torn += 1
        return letters, torn

    def sweep_stale_temps(self, *, older_than: float = 3600.0) -> int:
        """Remove ``.<name>.<uuid>.tmp`` siblings `write_text_atomic` left when a writer was killed
        mid-write, once older than an hour (a live write lasts milliseconds). Blob staging has its
        own sweep in `gc_blobs`. Never raises."""
        removed = 0
        cutoff = time.time() - older_than
        for directory in (self.ops_dir, self.failed_dir, self.dir):
            try:
                names = [n for n in os.listdir(directory) if n.startswith(".") and n.endswith(".tmp")]
            except OSError:
                continue
            for name in names:
                try:
                    path = directory / name
                    if path.stat().st_mtime < cutoff:
                        path.unlink()
                        removed += 1
                except OSError:
                    continue
        return removed

    def clear_auth_block(self) -> None:
        """Forget a recorded auth block (after re-login / explicit retry) so the wake-on-enqueue
        drainer spawns again (codex: nothing cleared it, so delivery stayed stopped forever after
        one 401)."""
        for child in self.namespaces()[1:]:
            child.clear_auth_block()
        self.write_status(auth_blocked_since=None, refused_fingerprints={}, held=0, close_held=0, held_at=None)
        try:  # a worker sleeping on held runs looks again now (outbox_worker._wake_stamp)
            write_text_atomic(self.dir / ".wake", now_iso() + "\n", mode=0o600)
        except OSError:
            pass

    def retry_failed(
        self, op_id: str | None = None, *, run_ref: str | None = None
    ) -> int:
        """Requeue dead letters (one op, one run's, or all). Files keep their names, so a retried
        op re-enters at its original FIFO position."""
        children_moved = sum(
            child.retry_failed(op_id, run_ref=run_ref) for child in self.namespaces()[1:]
        )
        moved = 0
        with file_lock(self.append_lock):
            for path, op in self._read_dir(self.failed_dir):
                if op_id is not None and op.get("op_id") != op_id:
                    continue
                if run_ref is not None and op.get("run_ref") != run_ref:
                    continue
                if "first_failed_at" in op:
                    # A human asked for another try: the transient budget's clock restarts, or an op
                    # dead-lettered by the budget would be dead-lettered again by its first failure.
                    op.pop("first_failed_at", None)
                    write_text_atomic(path, json.dumps(op, indent=2) + "\n", mode=0o600)
                os.replace(path, self.ops_dir / path.name)
                moved += 1
            if moved:
                fsync_directory(self.ops_dir)
                fsync_directory(self.failed_dir)
                self._write_status_locked()
                self._record_dead_letters()
        return moved + children_moved

    @property
    def dead_letters_file(self) -> Path:
        return self.dir / "dead_letters.json"

    def recent_dead_letters(self) -> list[dict]:
        """The last `_RECENT_DEAD_LETTERS` dead letters (`{run_ref, op_id, error, status}`, errors
        redacted at the source) for a training process to say so while it runs (plan 1.7). Their
        own file, written only by the drain and the dead-letter commands: in status.json every
        append re-read and rewrote them (review of #2055: 15 KB, 179 -> 511 us)."""
        try:
            records = json.loads(self.dead_letters_file.read_text())
        except (OSError, ValueError):
            return []
        return [r for r in records if isinstance(r, dict)] if isinstance(records, list) else []

    def _record_dead_letters(self, new: list[dict] | None = None) -> None:
        """Append ``new`` and forget entries whose op is no longer a dead letter (retried or
        discarded). Under the append lock."""
        try:
            present = {
                name for name in os.listdir(self.failed_dir) if name.endswith(".json")
            } if self.failed_dir.exists() else set()
        except OSError:
            present = None
        kept = self.recent_dead_letters() + list(new or [])
        if present is not None:
            # A record names its op, not its file: keep those whose op id still names a file in
            # failed/ (the name ends in "-<op_id>.json").
            ids = {name.rsplit("-", 1)[-1][: -len(".json")] for name in present}
            kept = [r for r in kept if str(r.get("op_id")) in ids]
        kept = kept[-_RECENT_DEAD_LETTERS:]
        try:
            if kept:
                write_text_atomic(
                    self.dead_letters_file,
                    json.dumps(kept, separators=(",", ":")) + "\n",
                    mode=0o600,
                    sync=SYNC_NONE,
                )
            else:
                self.dead_letters_file.unlink(missing_ok=True)
        except OSError:
            pass
from probe.sdk.delivery.ops.ops import op_meta  # noqa: E402 -- pieces need each other; the front door loads this one first
