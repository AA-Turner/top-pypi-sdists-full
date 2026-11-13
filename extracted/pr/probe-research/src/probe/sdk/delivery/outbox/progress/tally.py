"""Count one worker's queues per run from the folders themselves (R10): queued (ops, multipart,
waiting for a scan), held, refused, discarded (set aside: refused for good). "Delivered" is none
of these left."""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any

#: Dead-letter folders: `probe outbox retry` keeps a letter's name, so one retried and refused
#: again may be the same name with another error (and finality): re-read when its mtime moved.
_LETTER_FOLDERS = frozenset({"failed", "multipart/failed"})

#: Folder (under a queue) -> the count it feeds.
_FOLDERS = (
    ("ops", "pending"),
    ("multipart/ops", "pending"),
    ("held", "held"),
    ("multipart/held", "held"),
    ("failed", "failed"),
    ("multipart/failed", "failed"),
    ("discarded", "discarded"),
)


@dataclass
class RunCount:
    """One run's writes in the folders, at the moment of the count."""

    #: Writes that hold the run's result: blocking ones and multipart uploads (the user's files).
    pending: int = 0
    pending_bytes: int = 0
    held: int = 0
    #: Refused writes that hold the run's result (``blocking`` not False) and a retry may still
    #: deliver, as the close counts them (`REFUSED`).
    failed: int = 0
    discarded: int = 0
    #: Writes that hold the run's result and the server refuses for good (`discards.is_final_letter`:
    #: a past epoch, the run in the trash), dead-lettered or in discarded/ (`SET_ASIDE`). A past
    #: epoch's only when the run's current epoch is known (``min_epochs``): else it may be any
    #: earlier attempt's, and discarded/ is never pruned.
    set_aside: int = 0
    #: Every dead letter of the run, blocking or not, final or not: what `probe outbox status` shows.
    dead_letters: int = 0
    #: Best-effort writes still in line (`held.is_best_effort`): waited for, never a reason to raise;
    #: one set aside after a failure is not counted at all.
    best_effort: int = 0


@dataclass(frozen=True)
class _OpFacts:
    run_ref: str | None
    size: int
    blocking: bool
    lane: Any = None
    best_effort: bool = False
    epoch: int | None = None
    is_final: bool = False
    is_stale_epoch: bool = False


class QueueTally:
    """Per-run counts over the queues one worker serves (its own namespaces). Names are listed on
    every count; an op file is parsed once, the first time its name is seen (plan 1.9's rule), or in
    a dead-letter folder again when its mtime moved (`_LETTER_FOLDERS`)."""

    def __init__(self, journal: Any) -> None:
        self._journal = journal
        self._facts: dict[tuple[str, str], _OpFacts] = {}
        #: A dead letter's ``st_mtime_ns`` when its facts were read.
        self._stamps: dict[tuple[str, str], int] = {}
        #: A run's pinned context (from its first op seen), for the stall report's credential.
        self.contexts: dict[str, dict] = {}

    def count(self, min_epochs: dict | None = None) -> tuple[dict[str | None, RunCount], int]:
        """(run_ref -> its counts, writes queued in all), refreshed from disk. ``min_epochs``:
        run -> its current write epoch; an older attempt's writes are left out (the server refuses
        them as superseded, so nothing waits for them: `RunOps` ``min_epoch``)."""
        counts: dict[str | None, RunCount] = {}
        queued = 0
        for queue in self._journal.own_namespaces():
            base = Path(queue.dir)
            lanes_held = held_lanes(base)
            for relative, field_name in _FOLDERS:
                for facts in self._read_folder(base / relative, should_recheck=relative in _LETTER_FOLDERS):
                    if field_name == "failed":
                        counts.setdefault(facts.run_ref, RunCount()).dead_letters += 1
                        if not facts.blocking:
                            continue
                    if _is_superseded(facts, min_epochs):
                        continue
                    if field_name in ("failed", "discarded") and facts.is_final:
                        if facts.blocking and (not facts.is_stale_epoch or _has_floor(facts, min_epochs)):
                            counts.setdefault(facts.run_ref, RunCount()).set_aside += 1
                        if field_name == "failed":
                            continue
                    if facts.best_effort and field_name in ("pending", "held"):
                        # Waited for while in line; once set aside after a failure, never.
                        if field_name == "pending":
                            counts.setdefault(facts.run_ref, RunCount()).best_effort += 1
                            queued += 1
                        continue
                    if field_name == "pending" and facts.lane in lanes_held:
                        # Its run's lane is held after a stall: waiting an hour, not in line.
                        run = counts.setdefault(facts.run_ref, RunCount())
                        run.held += 1
                        continue
                    run = counts.setdefault(facts.run_ref, RunCount())
                    setattr(run, field_name, getattr(run, field_name) + 1)
                    if field_name == "pending":
                        run.pending_bytes += facts.size
                        queued += 1
            if not getattr(queue, "receipt_enabled", False):
                queued += self._count_waiting(queue, counts)
        for ref in [ref for ref in self.contexts if ref not in counts]:
            del self.contexts[ref]
        return counts, queued

    def _read_folder(self, folder: Path, *, should_recheck: bool = False) -> list[_OpFacts]:
        """The facts of each op file in ``folder``; ``should_recheck``: a file whose mtime moved since it was
        read is read again."""
        try:
            names = [n for n in os.listdir(folder) if n.endswith(".json")]
        except OSError:
            names = []
        where = str(folder)
        present = set(names)
        for key in [k for k in self._facts if k[0] == where and k[1] not in present]:
            del self._facts[key]
            self._stamps.pop(key, None)
        out: list[_OpFacts] = []
        for name in names:
            key = (where, name)
            facts = self._facts.get(key)
            stamp = None
            if should_recheck:
                try:
                    stamp = os.stat(folder / name).st_mtime_ns
                except OSError:
                    continue  # gone meanwhile
                if facts is not None and self._stamps.get(key) != stamp:
                    facts = None
            if facts is None:
                facts = self._parse(folder / name)
                if facts is None:
                    continue  # gone meanwhile, or torn: read again next time
                self._facts[key] = facts
                if stamp is not None:
                    self._stamps[key] = stamp
            out.append(facts)
        return out

    def _parse(self, path: Path) -> _OpFacts | None:
        try:
            op = json.loads(path.read_text())
        except (OSError, ValueError):
            return None
        if not isinstance(op, dict):
            return None
        ref = op.get("run_ref")
        if ref is not None and not isinstance(ref, str):
            ref = None
        if ref is not None and ref not in self.contexts and isinstance(op.get("context"), dict):
            self.contexts[ref] = op["context"]
        error = str(op.get("last_error") or "")
        return _OpFacts(
            ref, _size_of(op), op.get("blocking", True) is not False, _lane_of(op), is_best_effort(op),
            _write_epoch_of(op), is_final_letter(op, error), is_stale_epoch_letter(error),
        )

    @staticmethod
    def _count_waiting(queue: Any, counts: dict) -> int:
        """Uploads still waiting for their credential scan: queued too, sizes unknown."""
        waiting = 0
        try:
            items = list(queue._waiting_items())
        except Exception:  # noqa: BLE001 -- the waiting room is the drain's to repair
            return 0
        for item in items:
            ref = item[2] if len(item) > 2 and isinstance(item[2], str) else None
            counts.setdefault(ref, RunCount()).pending += 1
            waiting += 1
        return waiting


def _has_floor(facts: _OpFacts, min_epochs: dict | None) -> bool:
    return (min_epochs or {}).get(facts.run_ref) is not None


def _is_superseded(facts: _OpFacts, min_epochs: dict | None) -> bool:
    floor = (min_epochs or {}).get(facts.run_ref)
    return floor is not None and facts.epoch is not None and facts.epoch < floor


def _size_of(op: dict) -> int:
    try:
        return max(0, int((op.get("upload") or {}).get("size_bytes") or 0))
    except (TypeError, ValueError, AttributeError):
        return 0


from probe.sdk.delivery.ops.ops import _write_epoch_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _lane_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.failures.discards import is_final_letter, is_stale_epoch_letter  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.outbox.held import held_lanes, is_best_effort  # noqa: E402 -- pieces need each other; the front door loads this one first
