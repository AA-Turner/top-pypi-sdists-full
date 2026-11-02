"""count one run's ops that may hold its close, here and in the outbox's other queues."""

from __future__ import annotations

import json
import os
from pathlib import Path


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

    def _scan(self, directory: Path) -> list[Path]:
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
        out: list[Path] = []
        for name in names:
            key = (where, name)
            mine = self._mine.get(key)
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
            if mine:
                out.append(directory / name)
        return out

    def _older_attempts(self, op: dict) -> bool:
        if self._min_epoch is None:
            return False
        epoch = _write_epoch_of(op)
        return epoch is not None and epoch < self._min_epoch

    def pending(self) -> list[Path]:
        return [path for queue in self._queues for path in self._scan(queue.ops_dir)]

    def failed(self) -> list[Path]:
        return [path for queue in self._queues for path in self._scan(queue.failed_dir)]


class RunOpsMixin:
    """Part of Journal: its methods run with `self` the Journal; fold_parts() copies them into Journal."""

    def run_ops(self, run_ref: str) -> "RunOps":
        """A counter of ONE run's blocking ops that parses each op file once."""
        return RunOps(self, run_ref)

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
