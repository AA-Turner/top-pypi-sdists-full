"""Hand the run the main process opened to the job's other processes, never through a collective: the main process
sets the run's id on the job's own key-value store (torch.distributed's default process group store, which every
process of the job already reaches) under a key naming the attempt and the tracker, and the others poll it from
their sender's thread. It needs no shared filesystem and no agreeing clocks, and two jobs sharing an `output_dir` never meet: each
job has its own store. With no process group, a file per job and tracker under `output_dir/.probe/` stands in."""

from __future__ import annotations

import hashlib
import itertools
import json
import os
import sys
import tempfile
import time
from collections.abc import Callable
from dataclasses import dataclass, field
from typing import Any

from ..run_key import KEY_FOLDER

KEY_PREFIX = "probe/trl/run-id/"
RUN_ID_FILE = "run-id"
#: What the main process leaves when it has no run: the others stop waiting and train unrecorded.
NO_RUN = ""
#: How long another process's sender waits for the main process's run id before that process trains unrecorded.
WAIT_SECONDS = 120.0
POLL_SECONDS = 0.5
#: A file written more than this before this process started is an earlier job's (clocks of one job's hosts).
CLOCK_SLACK_SECONDS = 5.0
#: When /proc cannot say when this process started: when this module was imported (before the job's `train()`).
_IMPORTED_AT = time.time()
#: Trackers this process made, in order: every process of a job makes the same ones in the same order.
_TRACKER_COUNT = itertools.count()
#: torchrun's attempt number: its store outlives `--max-restarts`, while each attempt counts trackers from 0 again.
RESTART_ENV = "TORCHELASTIC_RESTART_COUNT"
DIGEST_CHARS = 12


def find_store() -> Any:
    """The job's default process group store, or None (one process, or no torch.distributed group)."""
    distributed = sys.modules.get("torch.distributed")  # never imports torch: a group needs it imported already
    if distributed is None:
        return None
    try:
        if not (distributed.is_available() and distributed.is_initialized()):
            return None
        return distributed.distributed_c10d._get_default_store()
    except Exception:  # noqa: BLE001 -- a torch without it: the file stands in
        return None


@dataclass(frozen=True)
class Handoff:
    """Where one tracker's run id goes. ``name``: the tracker's place among the trackers this process made, and a
    digest of its trainer's class (`make`; never `output_dir`, which a process may build itself): the same on every
    process of the job. A process whose count drifted waits on a name no other trainer's main process writes, unless
    the trainer at its drifted place is of the same class (two GRPO trainers, one tracked on only some processes).
    ``restart``: torchrun's attempt (`TORCHELASTIC_RESTART_COUNT`), so an attempt never reads the run id an earlier
    one left on the store it keeps. ``store``: the job's store; None looks it up when the id is saved or waited for
    (`find_store`)."""

    name: str
    output_dir: str | None = None
    store: Any = field(default=None, compare=False)
    restart: str = field(default_factory=lambda: os.environ.get(RESTART_ENV, "0"))

    @classmethod
    def make(cls, output_dir: str | None, trainer: Any = None) -> Handoff:
        """The next tracker's handoff: call once per tracker, as every process makes them."""
        cls_name = f"{type(trainer).__module__}.{type(trainer).__qualname__}" if trainer is not None else ""
        digest = hashlib.sha256(cls_name.encode()).hexdigest()[:DIGEST_CHARS]  # never output_dir: a path built per
        # process (a timestamp) would differ between ranks and leave the others waiting on a key nobody writes
        return cls(name=f"{next(_TRACKER_COUNT)}-{digest}", output_dir=output_dir)

    @property
    def key(self) -> str:
        return f"{KEY_PREFIX}{self.restart}/{self.name}"

    @property
    def path(self) -> str | None:
        """The fallback file, named by the job (torchrun's `MASTER_ADDR` and `MASTER_PORT`) and the tracker."""
        if not self.output_dir:
            return None
        address, port = os.environ.get("MASTER_ADDR"), os.environ.get("MASTER_PORT")
        job = f"{address}-{port}.".replace(os.sep, "_") if address and port else ""
        return os.path.join(str(self.output_dir), KEY_FOLDER, f"{RUN_ID_FILE}.{job}{self.name}")

    def save(self, run_id: str | None) -> None:
        """The main process: leave ``run_id`` (or that it has none). Raises (an OSError, a store's error)."""
        store = self._get_store()
        if store is not None:
            store.set(self.key, run_id or NO_RUN)
        else:
            save_file(self.path, run_id)

    def load(self, *, since: float) -> str | None:
        """The run id, `NO_RUN` when the main process has none, None when it left nothing yet. A file written before
        ``since`` (epoch seconds, this process's start) is an earlier job's."""
        store = self._get_store()
        if store is None:
            return load_file(self.path, since=since)
        try:
            if not store.check([self.key]):
                return None
            return store.get(self.key).decode("utf-8")
        except Exception:  # noqa: BLE001 -- a store read that failed: read again next poll
            return None

    def wait(self, *, timeout: float = WAIT_SECONDS, should_stop: Callable[[], bool] = lambda: False) -> str | None:
        """Poll for the main process's run id (a sender's background thread only); None when it has no run, after
        ``timeout``, or once ``should_stop`` (this process finished first)."""
        since = get_process_start()
        deadline = time.monotonic() + timeout
        while True:
            run_id = self.load(since=since)
            if run_id is not None:
                return run_id or None
            if should_stop() or time.monotonic() >= deadline:
                return None
            time.sleep(POLL_SECONDS)

    def _get_store(self) -> Any:
        return self.store if self.store is not None else find_store()


def save_file(path: str | None, run_id: str | None) -> None:
    """Write ``run_id`` (or `NO_RUN`) whole: a temp file, then a rename. Raises OSError."""
    if path is None:
        return
    folder = os.path.dirname(path)
    os.makedirs(folder, exist_ok=True)
    handle, temp = tempfile.mkstemp(prefix=f".{RUN_ID_FILE}.", dir=folder)
    try:
        with os.fdopen(handle, "w", encoding="utf-8") as file:
            json.dump({"run_id": run_id or NO_RUN, "written_at": time.time()}, file)
        os.replace(temp, path)
    except OSError:
        if os.path.exists(temp):
            os.unlink(temp)
        raise


def load_file(path: str | None, *, since: float) -> str | None:
    """The run id (or `NO_RUN`) written at or after ``since``; None when there is none yet."""
    if path is None:
        return None
    try:
        with open(path, encoding="utf-8") as file:
            found = json.load(file)
    except (OSError, ValueError):
        return None
    if not isinstance(found, dict) or not isinstance(found.get("run_id"), str):
        return None
    written_at = found.get("written_at")
    if not isinstance(written_at, (int, float)) or written_at < since - CLOCK_SLACK_SECONDS:
        return None  # an earlier job's
    return found["run_id"]


def get_process_start() -> float:
    """When this process started (Linux `/proc`), else when this module was imported."""
    try:
        with open("/proc/self/stat", encoding="ascii") as file:
            ticks = int(file.read().rsplit(")", 1)[1].split()[19])  # field 22, `starttime`
        with open("/proc/stat", encoding="ascii") as file:
            boot = next(int(line.split()[1]) for line in file if line.startswith("btime "))
        return boot + ticks / os.sysconf("SC_CLK_TCK")
    except (OSError, ValueError, IndexError, StopIteration):
        return _IMPORTED_AT
