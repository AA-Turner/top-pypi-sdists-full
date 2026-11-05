"""Span arrays of completed trajectories kept on disk instead of in memory."""

from __future__ import annotations

import atexit
import os
import shutil
import threading
import uuid
import weakref
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from .checkpoint import (
    Checkpointing,
    _Holder,
    _segment_file,
    _spill_state,
    _SpillFiles,
)
from .trajectory import _SPAN_ARRAYS, _Spilled


@dataclass(frozen=True)
class Spill:
    """Keep span arrays of completed trajectories on disk, not in memory.

    Logprobs, top-K candidates, sampling log masses and token ids leave
    memory and are read back when training or other code accesses them.

    Attributes:
        directory: Where to write them when the trainer has no
            ``Checkpointing``. The trainer uses a locked subdirectory of its
            own, without fsync, deletes each file once no trajectory
            references it, and removes the subdirectory at process exit;
            leftovers of a process that crashed are removed by the next one.
            With ``Checkpointing``, arrays are kept in the run directory's
            checkpoint segments instead, so leave this unset.
    """

    directory: str | Path | None = None

    def __post_init__(self):
        if self.directory is not None and "://" in str(self.directory):
            raise ValueError(
                "Spill.directory must be a local or shared filesystem path"
            )


def resolve_spill(spill, checkpoint: Checkpointing | None):
    """Return (spill checkpoint segments, scratch directory or None)."""
    if spill is not None and not isinstance(spill, (bool, Spill)):
        raise TypeError("spill must be rl.Spill, a bool, or None")
    legacy = None if checkpoint is None else checkpoint.spill_arrays
    if legacy is not None and spill is not None:
        raise ValueError(
            "set either AsyncTrainer(spill=...) or the deprecated "
            "Checkpointing.spill_arrays, not both"
        )
    if spill is None:
        spill = legacy if legacy is not None else checkpoint is not None
    if spill is False:
        return False, None
    directory = spill.directory if isinstance(spill, Spill) else None
    if checkpoint is not None:
        if directory is not None and os.path.realpath(directory) != os.path.realpath(
            checkpoint.run_dir
        ):
            raise ValueError(
                "with Checkpointing, spilled arrays live in its run_dir; "
                "omit Spill.directory"
            )
        return True, None
    if directory is None:
        raise ValueError(
            "spilling without Checkpointing needs a directory: rl.Spill(directory)"
        )
    return False, Path(directory)


class ScratchSpill:
    """Span arrays of completed trajectories in unsynced scratch files.

    One file per ``spill`` call. A file is deleted once every span reading
    from it is gone; deletion runs on the next ``spill`` call or at exit,
    never from a garbage-collection callback.
    """

    def __init__(self, root):
        import fcntl

        root = Path(root)
        root.mkdir(parents=True, exist_ok=True)
        # Cleanup and creation hold the root's lock, so no process removes a
        # directory between its creation and its owner locking it. Locks are
        # opened writable: flock on NFS takes an exclusive byte-range lock.
        with (root / ".river-spill.lock").open("a+") as root_lock:
            fcntl.flock(root_lock, fcntl.LOCK_EX)
            _remove_orphans(root)
            self.directory = root / f"river-spill-{os.getpid()}-{uuid.uuid4().hex[:12]}"
            self.directory.mkdir()
            self._lock = (self.directory / ".lock").open("a+")
            fcntl.flock(self._lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        self.files = _SpillFiles(self.directory)
        # A forked child inherits this object and its exit handler; only the
        # creating process may write to or remove the directory.
        self._owner = os.getpid()
        self._dead = []
        self._closed = False
        self._write_lock = threading.Lock()
        atexit.register(self.close)

    def spill(self, trajectories):
        """Write the trajectories' span arrays and drop them from memory.

        Call only for completed trajectories, which gain no further spans.
        """
        with self._write_lock:
            if self._closed or os.getpid() != self._owner:
                return
            self._delete_dead()
            written, offset = [], 0
            name = uuid.uuid4().hex
            path = self.directory / _segment_file(name)
            with path.open("xb") as stream:
                for trajectory in trajectories:
                    for span in trajectory._spans:
                        state = _spill_state(span, True)
                        values = [(name_, state[name_]) for name_ in _SPAN_ARRAYS] + [
                            (index, chunk["tokens"])
                            for index, chunk in enumerate(state["chunks"])
                        ]
                        for key, value in values:
                            if value is None:
                                continue
                            array = np.ascontiguousarray(value)
                            stream.write(memoryview(array).cast("B"))
                            written.append((span, key, value, offset))
                            offset += array.nbytes
            if not written:
                path.unlink()
                return
            holder = _Holder(self.files, (name, 0))
            weakref.finalize(holder, self._dead.append, name)
            with self.files.lock:
                for span, key, value, start in written:
                    spilled = _Spilled(holder, start, value.shape, value.dtype)
                    if isinstance(key, str):
                        if span.__dict__[key] is value:
                            span.__dict__[key] = spilled
                    elif span._chunks[key]["tokens"] is value:
                        span._chunks[key]["tokens"] = spilled

    def _delete_dead(self):
        while self._dead:
            name = self._dead.pop()
            with self.files.lock:
                stream = self.files.files.pop(name, None)
                if stream is not None:
                    stream.close()
            (self.directory / _segment_file(name)).unlink(missing_ok=True)

    def close(self):
        if os.getpid() != self._owner:
            return
        with self._write_lock:
            if self._closed:
                return
            self._closed = True
            self.files.close()
            shutil.rmtree(self.directory, ignore_errors=True)
            self._lock.close()


def _remove_orphans(root):
    """Remove scratch directories whose process no longer holds their lock.

    Call with the root's lock held.
    """
    import fcntl

    for directory in root.glob("river-spill-*"):
        try:
            # "r+" never creates the file: an owner's close() removes its
            # directory without the root lock, so it may vanish here.
            lock = (directory / ".lock").open("r+")
        except OSError:
            continue
        with lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except OSError:
                # Held by a live process, or not lockable here: keep it.
                continue
            shutil.rmtree(directory, ignore_errors=True)


_SCRATCH = {}
_SCRATCH_LOCK = threading.Lock()


def _after_fork_in_child():
    # A child's trainers get their own directory; the parent's stays its own.
    global _SCRATCH_LOCK
    _SCRATCH.clear()
    _SCRATCH_LOCK = threading.Lock()


if hasattr(os, "register_at_fork"):
    os.register_at_fork(after_in_child=_after_fork_in_child)


def scratch_spill(root):
    """The process's scratch spill under ``root``, shared by its trainers."""
    with _SCRATCH_LOCK:
        key = os.path.realpath(root)
        spill = _SCRATCH.get(key)
        if spill is None or spill._closed or spill._owner != os.getpid():
            spill = _SCRATCH[key] = ScratchSpill(key)
        return spill
