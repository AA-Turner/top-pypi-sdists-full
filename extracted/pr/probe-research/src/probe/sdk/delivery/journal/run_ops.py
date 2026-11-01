"""count one run's ops that may hold its close, here and in the outbox's other queues."""

from __future__ import annotations
import json
import os
from pathlib import Path


class RunOps:
    """One run's ops that may hold its close, counted from directory LISTINGS.

    `Run.finish()` asks "what of mine is still queued / dead-lettered?" after every pass of its
    deadline loop. ``journal.pending()`` parsed the WHOLE machine-wide queue each time (every
    run's ops, every 0.25 s): most of the loop's cost at a 20k-op backlog (plan 1.9 side note).
    Op files are immutable in the two fields asked about (``run_ref``, ``blocking``) while in
    one directory, so each ``(directory, name)`` is parsed once and remembered; later calls cost
    one ``listdir``. ``blocking`` flips only on the move INTO ``failed/``: a new
    ``(directory, name)`` key, parsed fresh.

    Same selection as `Run._queued_ops`: ``run_ref`` matches and ``blocking`` is not False (a
    best-effort diagnostic never holds a close).
    """

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
from probe.sdk.delivery.journal.journal import Journal  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.delivery.ops.ops import _write_epoch_of  # noqa: E402 -- pieces need each other; the front door loads this one first
