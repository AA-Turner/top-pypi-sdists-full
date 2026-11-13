"""count one run's ops that may hold its close, here and in the outbox's other queues."""

from __future__ import annotations

import json
import os
from pathlib import Path
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Callable


class RunOps:
    """One run's ops that may hold its close (``run_ref`` matches, ``blocking`` not False), counted
    from directory listings: each op file is parsed once, then one ``listdir`` per call (plan 1.9)."""

    def __init__(
        self,
        journal: "Journal",
        run_ref: str,
        *,
        blocking_only: bool = True,
        queues: "list[Journal] | None" = None,
        min_epoch: int | None = None,
    ):
        self._journal = journal
        self._run_ref = run_ref
        #: False counts every op of the run, blocking or not: "is anything of this run still
        #: queued" (plan 1.5's direct send), not "what holds its close".
        self._blocking_only = blocking_only
        #: The queues counted: this journal alone, or (`Journal.run_ops_elsewhere`)
        #: the other queues of its outbox.
        self._queues = [journal] if queues is None else list(queues)
        #: Leave out ops stamped with an older write epoch: the server refuses
        #: them as a superseded attempt's, so nothing waits for them.
        self._min_epoch = min_epoch
        self._mine: dict[tuple[str, str], bool] = {}
        #: Of the files that are mine: (final, a past epoch's) by `discards.is_final_letter`.
        self._finality: dict[tuple[str, str], tuple[bool, bool]] = {}
        #: A dead letter's ``st_mtime_ns`` when it was read: `probe outbox retry` keeps its name, so
        #: one refused again may carry another error (and finality) under the same name.
        self._stamps: dict[tuple[str, str], int] = {}

    def _scan(
        self, directory: Path, *, keep: "Callable[[tuple[str, str]], bool] | None" = None, should_recheck: bool = False
    ) -> list[Path]:
        """This run's op files in ``directory``; ``keep(key)`` narrows them (`_is_refused`, `_is_set_aside`).
        ``should_recheck`` (a dead-letter folder): a file whose mtime moved since it was read is read again."""
        try:
            names = sorted(n for n in os.listdir(directory) if n.endswith(".json"))
        except FileNotFoundError:
            return []
        # Forget files that left this directory so a long-lived handle does not remember every
        # op the run ever queued (review of #2054).
        present = set(names)
        where = str(directory)
        for key in [k for k in self._mine if k[0] == where and k[1] not in present]:
            del self._mine[key]
            self._finality.pop(key, None)
            self._stamps.pop(key, None)
        out: list[Path] = []
        for name in names:
            key = (where, name)
            mine = self._mine.get(key)
            stamp = None
            if should_recheck:
                try:
                    stamp = os.stat(directory / name).st_mtime_ns
                except OSError:
                    continue  # retried or moved between the listing and the stat
                if mine is not None and self._stamps.get(key) != stamp:
                    mine = None
                    self._finality.pop(key, None)
            if mine is None:
                try:
                    op = json.loads((directory / name).read_text())
                except FileNotFoundError:
                    continue  # delivered (or moved) between the listing and the read
                except (OSError, ValueError):
                    continue  # corrupt: quarantine's business; not cached, re-read later
                mine = bool(
                    isinstance(op, dict)
                    and op.get("run_ref") == self._run_ref
                    and (op.get("blocking", True) or not self._blocking_only)
                    and not self._older_attempts(op)
                )
                self._mine[key] = mine
                if stamp is not None:
                    self._stamps[key] = stamp
                if mine:
                    error = str(op.get("last_error") or "")
                    self._finality[key] = (is_final_letter(op, error), is_stale_epoch_letter(error))
            if mine and (keep is None or keep(key)):
                out.append(directory / name)
        return out

    def _is_refused(self, key: tuple[str, str]) -> bool:
        return not self._finality.get(key, (False, False))[0]

    def _is_set_aside(self, key: tuple[str, str]) -> bool:
        final, stale = self._finality.get(key, (False, False))
        # A past epoch's refusal with no epoch to judge by may be any earlier attempt's: not this one's.
        return final and not (stale and self._min_epoch is None)

    def _older_attempts(self, op: dict) -> bool:
        if self._min_epoch is None:
            return False
        epoch = _write_epoch_of(op)
        return epoch is not None and epoch < self._min_epoch

    def pending(self) -> list[Path]:
        return [path for queue in self._queues for path in self._scan(queue.ops_dir)]

    def failed(self) -> list[Path]:
        """Every dead letter of the run, final or not."""
        return [path for queue in self._queues for path in self._scan(queue.failed_dir, should_recheck=True)]

    def get_refused(self) -> list[Path]:
        """Dead letters a retry may still deliver (`probe outbox retry`): `failed` but the final ones."""
        return [
            path for queue in self._queues
            for path in self._scan(queue.failed_dir, keep=self._is_refused, should_recheck=True)
        ]

    def set_aside(self) -> list[Path]:
        """Writes the server refuses for good (`discards.is_final_letter`): dead letters, and the ones
        set aside in discarded/ instead (each discard folder once: a credential queue's is its
        root's). They never landed, and nothing retries them."""
        letters = [path for queue in self._queues for path in self._scan(
            queue.failed_dir, keep=self._is_set_aside, should_recheck=True
        )]
        discards = dict.fromkeys(queue._discard_dir() for queue in self._queues)
        return letters + [path for folder in discards for path in self._scan(folder, keep=self._is_set_aside)]


class RunOpsMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

    def run_ops(self, run_ref: str, *, min_epoch: int | None = None) -> "RunOps":
        """A counter of ONE run's blocking ops that parses each op file once. ``min_epoch`` leaves
        out an older attempt's."""
        return RunOps(self, run_ref, min_epoch=min_epoch)

    def own_namespaces(self) -> "list[Journal]":
        """`namespaces` without the credential queues under a root: what the
        root's own worker serves."""
        return [
            queue
            for queue in self.namespaces()
            if queue.dir == self.dir or queue.dir == self.dir / DELIVERY_NAMESPACE
        ]

    def other_queues(self) -> "list[Journal]":
        """`outbox_queues` minus this queue and its own receipt namespace."""
        mine = {self.dir, self.dir / DELIVERY_NAMESPACE}
        return [queue for queue in self.outbox_queues() if queue.dir not in mine]

    def run_ops_elsewhere(self, run_ref: str, *, min_epoch: int | None = None) -> "RunOps":
        """ONE run's blocking ops in the outbox's OTHER queues: writes of the
        same run queued under another credential (#2035), which this queue's
        order cannot see and a close queued here could overtake. ``min_epoch``
        leaves out an older attempt's (round 5)."""
        return RunOps(self, run_ref, queues=self.other_queues(), min_epoch=min_epoch)

from probe.sdk.delivery.journal.journal import Journal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _write_epoch_of  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import DELIVERY_NAMESPACE  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.journal.failures.discards import is_final_letter, is_stale_epoch_letter  # noqa: E402 -- pieces need each other; the front door loads this one first
