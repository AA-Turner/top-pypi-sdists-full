"""Atomic local trainer state paired with River training checkpoints."""

from __future__ import annotations

import codecs
import hashlib
import json
import math
import os
import re
import shutil
import threading
import uuid
import warnings
import weakref
from collections import OrderedDict
from dataclasses import dataclass
from itertools import chain, count
from pathlib import Path

import numpy as np

from river_client.images import ImageStore, map_images

from .batch import TrainingBatch
from .config import _integer
from .trajectory import _SPAN_ARRAYS, _Spilled, decode_state, encode_state


def identity_state(value):
    # Session handles change on recovery; content and renderer dimensions do not.
    return encode_state(
        map_images(
            value,
            lambda image: {
                "__river_image_content__": {
                    "sha256": image.sha256,
                    "byte_count": image.byte_count,
                    "width": image.width,
                    "height": image.height,
                }
            },
        )
    )


def fingerprint(value):
    return hashlib.sha256(
        json.dumps(
            identity_state(value),
            sort_keys=True,
            ensure_ascii=False,
            separators=(",", ":"),
            allow_nan=False,
        ).encode()
    ).hexdigest()


def row_order_fingerprint(rows):
    digest = hashlib.sha256()
    for row in rows:
        digest.update(
            json.dumps(
                identity_state(row),
                sort_keys=True,
                ensure_ascii=False,
                separators=(",", ":"),
                allow_nan=False,
            ).encode()
        )
        digest.update(b"\n")
    return digest.hexdigest()


def training_plan_fingerprint(rows, groups_per_step, steps, *, repeat_dataset=True):
    digest = hashlib.sha256()
    for step in range(steps):
        digest.update(f"step:{step}\n".encode())
        for i in range(groups_per_step):
            index = step * groups_per_step + i
            if not repeat_dataset and index >= len(rows):
                break
            row = rows[index % len(rows)]
            digest.update(
                json.dumps(
                    identity_state(row),
                    sort_keys=True,
                    ensure_ascii=False,
                    separators=(",", ":"),
                    allow_nan=False,
                ).encode()
            )
            digest.update(b"\n")
    return digest.hexdigest()


@dataclass(frozen=True)
class Checkpointing:
    """Store recoverable trainer and rollout state in a durable directory.

    Attributes:
        run_dir: Local or shared filesystem directory for this run's state.
        weights_every: Optimizer updates between training recovery checkpoints.
            Rolling saves stay on shared training storage until their TTL expires;
            completed runs save a final checkpoint with durable=True. For LoRA,
            the final save uses cloud storage; full-weight saves stay on shared
            storage and durable selects the default TTL only. Recovery also
            requires run_dir. Save milestones separately to retain them.
        recovery_ttl_seconds: Lifetime of each NFS recovery save, default seven days.
            Must fit the server retention cap. Resume before the base expires.
        rollout_every: Seconds between rollout-state snapshots.
        on_signal: Signals that request a final checkpoint before shutdown.
        spill_arrays: Deprecated; use ``AsyncTrainer(spill=...)``, where
            ``spill=False`` keeps span arrays in memory.
    """

    run_dir: str | Path
    weights_every: int = 20
    rollout_every: float = 60.0
    on_signal: tuple[str, ...] = ()
    recovery_ttl_seconds: int = 7 * 24 * 60 * 60
    spill_arrays: bool | None = None

    def __post_init__(self):
        _integer(self.weights_every, "weights_every", 1)
        _integer(self.recovery_ttl_seconds, "recovery_ttl_seconds", 1)
        if "://" in str(self.run_dir):
            raise ValueError(
                "run_dir must be a durable local/shared filesystem directory; River currently stores weights, not arbitrary trainer metadata"
            )
        if (
            self.weights_every < 1
            or self.rollout_every <= 0
            or not math.isfinite(self.rollout_every)
        ):
            raise ValueError("checkpoint cadences must be finite and positive")
        if any(s not in {"SIGINT", "SIGTERM"} for s in self.on_signal):
            raise ValueError("supported checkpoint signals are SIGINT and SIGTERM")
        if self.spill_arrays is not None:
            if not isinstance(self.spill_arrays, bool):
                raise ValueError("spill_arrays must be a bool")
            warnings.warn(
                "Checkpointing(spill_arrays=...) is deprecated and will be removed "
                "in a future river-client release; use AsyncTrainer(spill=...)",
                DeprecationWarning,
                stacklevel=3,
            )


class StateStore:
    """Trainer state in ``run_dir``: a small manifest plus append-only segments.

    ``trainer.json`` holds control state and is replaced atomically on every
    save. Trajectory content and journal updates are records in
    ``trainer-segment-*.bin`` files, each written by one save and never
    modified. A trajectory's spans and messages only grow between saves, so a
    save writes the turns added since the last commit, not the whole history.
    Records in segments that fall below half live bytes are copied forward
    into the new segment, and unreferenced segments are deleted after commit.

    Once a save commits, span arrays it wrote (logprobs, top-K candidates,
    sampling log masses, and token ids that no turn resends: those of runs
    before a rewrite, or of completed trajectories) are dropped from memory
    and read back from their segment when accessed. Unfinished
    trajectories that are not saved for recovery get records of their arrays
    only. Segments stay on disk while spans still reference them.
    ``spill_arrays=False`` turns this off.
    """

    def __init__(self, config: Checkpointing, *, spill_arrays=None):
        self.directory = Path(config.run_dir)
        self.directory.mkdir(parents=True, exist_ok=True)
        self.path = self.directory / "trainer.json"
        self.images = ImageStore(self.directory / "images")
        self._lock = None
        # Committed content, by object identity, that later saves extend.
        self._cursors = {}
        self._records = {}
        self._spill_cursors = {}
        # Committed trajectory cursors by span list, which journal batches share.
        self._span_cursors = {}
        self._segments = {}
        self._version = None
        self._spill = _spill_files(self.directory)
        if spill_arrays is None:
            spill_arrays = config.spill_arrays is not False
        self._spill_arrays = spill_arrays

    def __enter__(self):
        import fcntl

        self._lock = (self.directory / ".lock").open("a+")
        try:
            fcntl.flock(self._lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            self._lock.close()
            raise RuntimeError(
                "another trainer owns this checkpoint directory"
            ) from None
        return self

    def __exit__(self, exc_type, exc, tb):
        self._lock.close()
        # Spans still spilled after training reopen segments on access.
        self._spill.close()

    def capture(self):
        """Start capturing state for one save.

        Call on the thread that mutates trajectories, after the previous save
        has finished. Only content added since the last commit is copied.
        """
        return _Capture(self)

    def load(self, *, lazy_records=False):
        """Return the committed state, or None when there is none.

        With ``lazy_records``, journal records stay on disk as references;
        ``read`` returns each one's content when it is needed.
        """
        if not self.path.exists():
            return None
        state = _read_json(self.path)
        storage = state.pop("__river_arrays__", None)
        if not isinstance(storage, dict) or storage.get("version") not in (2, 3, 4):
            raise ValueError(
                "checkpoint requires binary array storage version 2, 3 or 4"
            )
        self._version = storage["version"]
        if self._version < STORAGE_VERSION:
            # Fail before the trainer loads weights or saves anything.
            _require_migration(self.directory, self._version)
        if storage["version"] == 2:
            return self._load_v2(state, storage)
        segments = {}
        try:
            for name, meta in storage["segments"].items():
                if not re.fullmatch(r"[0-9a-f]{32}", name):
                    raise ValueError("invalid checkpoint segment name")
                stream = (self.directory / _segment_file(name)).open("rb")
                segments[name] = stream
                stream.seek(0, os.SEEK_END)
                size = stream.tell()
                stream.seek(0)
                if (
                    size != meta["bytes"]
                    or hashlib.file_digest(stream, "sha256").hexdigest()
                    != meta["sha256"]
                ):
                    raise ValueError("checkpoint segment integrity verification failed")

            def read(name, offset, length):
                if (
                    name not in segments
                    or type(offset) is not int
                    or type(length) is not int
                    or offset < 0
                    or length < 0
                    or offset + length > storage["segments"][name]["bytes"]
                ):
                    raise ValueError("invalid checkpoint record bounds")
                return b"".join(_read_chunks(segments[name].fileno(), length, offset))

            name, offset, length = storage["arrays"]
            state = _unpack_arrays(decode_state(state), read(name, offset, length))
            # Later saves may reference these records without rewriting them.
            self._segments = storage["segments"]
            return _expand(state, read, {}, lazy_records)
        finally:
            for stream in segments.values():
                stream.close()

    def _load_v2(self, state, storage):
        name = storage["file"]
        if not re.fullmatch(r"trainer-arrays-[0-9a-f]{32}\.bin", name):
            raise ValueError("invalid checkpoint array filename")
        with (self.directory / name).open("rb") as stream:
            size = os.fstat(stream.fileno()).st_size
            if (
                size != storage["bytes"]
                or hashlib.file_digest(stream, "sha256").hexdigest()
                != storage["sha256"]
            ):
                raise ValueError("checkpoint array integrity verification failed")
            # Read through a bounded window rather than holding the file.
            return _unpack_v2(decode_state(state), _ArrayWindow(stream.fileno(), size))

    def read(self, value):
        """Return a lazily loaded or released journal update's content.

        An update journaled by reference returns its recipes and the states of
        the trajectories they build from, without messages.
        """
        if not isinstance(value, (_CommittedRecord, _CommittedUpdate)):
            return value
        streams = {}
        try:

            def read(name, offset, length):
                if (
                    name not in self._segments
                    or type(offset) is not int
                    or type(length) is not int
                    or offset < 0
                    or length < 0
                    or offset + length > self._segments[name]["bytes"]
                ):
                    raise ValueError("invalid checkpoint record bounds")
                if name not in streams:
                    streams[name] = (self.directory / _segment_file(name)).open("rb")
                return b"".join(_read_chunks(streams[name].fileno(), length, offset))

            if isinstance(value, _CommittedRecord):
                return _read_record(value.ref, read, {})
            cache = {}
            return {
                "optimizer": value.optimizer,
                **_read_record(value.recipes.ref, read, cache),
                "trajectories": [
                    _trajectory_state(t.fields, t.records, read, cache, messages=False)
                    for t in value.trajectories
                ],
            }
        finally:
            for stream in streams.values():
                stream.close()

    def release(self, value):
        """Return a reference for a committed journal update, else ``value``.

        The store keeps no copy of a released value; ``read`` reloads it.
        Releasing an update journaled by reference also drops its batches,
        and with them the trajectory spans they hold.
        """
        entry = self._records.get(id(value))
        if entry is None or entry[0] is not value:
            return value
        del self._records[id(value)]
        if isinstance(entry[1], _CommittedUpdate):
            return entry[1]
        return _CommittedRecord(entry[1])

    def save(self, state, *, images=None, spills=()):
        """Commit ``state``; ``spills`` come from ``capture().spill``."""
        if "__river_arrays__" in state:
            raise ValueError("checkpoint state contains reserved storage metadata")
        committed = self._committed_version()
        if committed is not None and committed < STORAGE_VERSION:
            _require_migration(self.directory, committed)
            self._preserve_version(committed)
        name = uuid.uuid4().hex
        path = self.directory / _segment_file(name)
        stream = path.open("x+b")
        try:
            with stream:
                writer = _SegmentWriter(self, name, stream, images)
                state = writer.resolve(state)
                writer.spill(spills)
                writer.compact()
                arrays = _Relative(stream)
                state = decode_state(_pack_arrays(state, arrays))
                manifest_arrays = [name, arrays.start, arrays.tell()]
                retained = self.images.copy_images(state, images)
                retained.update(writer.images())
                size = stream.tell()
                stream.flush()
                stream.seek(0)
                digest = hashlib.file_digest(stream, "sha256").hexdigest()
                os.fsync(stream.fileno())
            segments = writer.segments(name, size, digest)
            self._sync_directory()
            state = encode_state(state)
            state["__river_arrays__"] = {
                "version": STORAGE_VERSION,
                "segments": segments,
                "arrays": manifest_arrays,
            }
            temporary = self.path.with_suffix(".tmp")
            with temporary.open("w") as output:
                output.write(
                    json.dumps(
                        state,
                        ensure_ascii=False,
                        separators=(",", ":"),
                        allow_nan=False,
                    )
                )
                output.flush()
                os.fsync(output.fileno())
            os.replace(temporary, self.path)
        except BaseException:
            path.unlink(missing_ok=True)
            raise
        self._sync_directory()
        # Readers of spilled arrays resolve records under this lock.
        with self._spill.lock:
            self._cursors, self._records, self._spill_cursors = writer.commit()
            self._span_cursors = {
                id(cursor.spans): cursor for cursor in self._cursors.values()
            }
            self._segments, self._version = segments, STORAGE_VERSION
            # Only a durably committed manifest may release unreferenced files.
            files = self._spill.files
            for segment in [s for s in files if s not in segments]:
                files.pop(segment).close()
            live = {_segment_file(segment) for segment in segments}
            for stale in self.directory.iterdir():
                if (
                    re.fullmatch(
                        r"trainer-(segment|arrays)-[0-9a-f]{32}\.bin", stale.name
                    )
                    and stale.name not in live
                ):
                    stale.unlink()
        self.images.prune(retained)

    def _committed_version(self):
        if self._version is None and self.path.exists():
            storage = _read_json(self.path).get("__river_arrays__")
            self._version = (
                storage.get("version") if isinstance(storage, dict) else None
            )
            if self._version in (3, 4):
                # Spans from an earlier store on this directory may still
                # read these segments.
                if not all(
                    re.fullmatch(r"[0-9a-f]{32}", name) for name in storage["segments"]
                ):
                    raise ValueError("invalid checkpoint segment name")
                self._segments = storage["segments"]
        return self._version

    def _preserve_version(self, version):
        """Keep a resumable copy of an older version's state before replacing it.

        Files are hard-linked where possible: later versions never modify an
        existing file, they only delete ones they no longer need. Every attempt
        rebuilds the copy from the committed state, so a backup left by an
        interrupted migration is never trusted.
        """
        name = backup_directory(version)
        backup = self.directory / name
        staging = self.directory / f".{name}.tmp"
        shutil.rmtree(staging, ignore_errors=True)
        (staging / "images").mkdir(parents=True)
        sources = [
            self.path,
            *(
                self.directory.glob("trainer-arrays-*.bin")
                if version == 2
                else (self.directory / _segment_file(name) for name in self._segments)
            ),
            *(
                self.images.directory.iterdir()
                if self.images.directory.exists()
                else ()
            ),
        ]
        for source in sources:
            if not source.is_file():
                continue
            target = staging / source.relative_to(self.directory)
            try:
                os.link(source, target)
            except OSError:
                shutil.copy2(source, target)
                with target.open("rb") as copied:
                    os.fsync(copied.fileno())
        for directory in (staging / "images", staging):
            descriptor = os.open(directory, os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
        stale = self.directory / f".{name}.stale"
        shutil.rmtree(stale, ignore_errors=True)
        if backup.exists():
            os.replace(backup, stale)
        os.replace(staging, backup)
        self._sync_directory()
        shutil.rmtree(stale, ignore_errors=True)

    def _sync_directory(self):
        descriptor = os.open(self.directory, os.O_RDONLY)
        try:
            os.fsync(descriptor)
        finally:
            os.close(descriptor)


# One read transfers at most about 2 GiB on Linux; records can be larger.
_READ_CHUNK = 1 << 30


def _read_chunks(descriptor, length, offset):
    """Yield exactly ``length`` bytes from ``offset``, failing on early EOF."""
    while length:
        data = os.pread(descriptor, min(length, _READ_CHUNK), offset)
        if not data:
            raise ValueError("checkpoint segment ended before its record")
        yield data
        offset += len(data)
        length -= len(data)


# Version 4 journals updates by reference to trajectory records.
STORAGE_VERSION = 4
MIGRATE_ENV = "RIVER_RL_MIGRATE_CHECKPOINT"
# The clients that last wrote each older storage version.
_WRITTEN_BY = {2: "0.17 or older", 3: "0.18.0 to 0.19.0"}


def backup_directory(version):
    return f"checkpoint-v{version}-backup"


def _require_migration(directory, version):
    """Refuse a one-way rewrite of an older storage version unless opted in."""
    if os.environ.get(MIGRATE_ENV) == "1":
        return
    raise RuntimeError(
        f"{directory} holds a version {version} RL checkpoint written by "
        f"river-client {_WRITTEN_BY[version]}. Resuming it with this client "
        f"overwrites the run's checkpoint in storage version {STORAGE_VERSION} "
        "on the next save; older clients cannot resume it afterwards. Back up the "
        f"directory first (for example, cp -a {directory} {directory}.bak), then "
        f"set {MIGRATE_ENV}=1 to resume and migrate. The migration also keeps "
        f"the version {version} state in {directory / backup_directory(version)}."
    )


_TRAJECTORY = "__river_trajectory__"
_RECORD = "__river_record__"
# A journaled update: recipes record plus the trajectories its datums build from.
_UPDATE = "__river_update__"
_JOURNAL_TRAJECTORY = "__river_journal_trajectory__"
_RESERVED = (_TRAJECTORY, _RECORD, _UPDATE, _JOURNAL_TRAJECTORY)
# Relocate a segment's live records once less than this fraction is live.
_COMPACT_BELOW = 0.5
# Merge the smallest segments into the new one beyond this many; bounds the
# files a load opens when long-lived records keep old segments mostly live.
_MAX_SEGMENTS = 32
_SERIAL = count()
# Smaller arrays stay in memory: a reference would save little.
_SPILL_BYTES = 1024
# Read spilled arrays of one record together across gaps up to this size.
_COALESCE_GAP = 64 << 10
_OPEN_SEGMENTS = 64


def _segment_file(name):
    return f"trainer-segment-{name}.bin"


@dataclass(frozen=True)
class _Cursor:
    """A trajectory's committed content, identified by its live containers."""

    trajectory: object
    spans: list
    span_count: int
    messages: list
    message_count: int
    records: tuple
    run: int
    # Spans whose token ids are in ``records`` but still in memory, because
    # the next turn resends them: (span, holder, token locations).
    unspilled: tuple = ()


class _TrajectoryCapture:
    """A trajectory's content that is new since its committed cursor."""

    def __init__(self, trajectory, base, delta, written=(), unspilled=()):
        self.trajectory = trajectory
        self.spans, self.span_count = trajectory._spans, len(trajectory._spans)
        self.messages = trajectory.messages
        self.message_count = len(self.messages)
        self.run, self.done = trajectory.run, bool(trajectory.done)
        self.base, self.delta = base, delta
        # Token ids that ``base`` holds and memory still keeps.
        self.unspilled = unspilled
        # Spans in ``delta``; the commit spills their arrays.
        self.written = written
        self.records = None
        self.packed = None
        self.serial = next(_SERIAL)

    def current(self):
        trajectory = self.trajectory
        return (
            trajectory._spans is self.spans
            and len(self.spans) == self.span_count
            and trajectory.messages is self.messages
            and len(self.messages) == self.message_count
            # Completion lets the commit spill current-run token ids.
            and bool(trajectory.done) == self.done
        )


class _SpillCapture:
    """Arrays of an unsaved trajectory, written so memory can drop them."""

    def __init__(self, trajectory, spans):
        self.trajectory, self.spans = trajectory, trajectory._spans
        self.span_count, self.run = len(self.spans), trajectory.run
        self.written = spans
        self.payload = [_spill_state(span, span.run < self.run) for span in spans]
        self.ref = self.packed = None


class _SpillFiles:
    """Records that spilled arrays of one run directory read from.

    Shared by every store this process opens on the directory, so a reopened
    store keeps, and compacts, records that earlier trajectories still read.
    """

    def __init__(self, directory):
        self.directory = directory
        self.holders = weakref.WeakSet()
        # Readers resolve holders, and commits repoint them, under this lock.
        self.lock = threading.RLock()
        self.files = OrderedDict()

    def close(self):
        with self.lock:
            while self.files:
                self.files.popitem()[1].close()

    def read(self, holder, values):
        """Read spilled arrays of one record, coalescing nearby ones."""
        ranges = []
        for value in sorted(values, key=lambda v: v.offset):
            end = value.offset + value.nbytes
            if ranges and value.offset - ranges[-1][1] <= _COALESCE_GAP:
                ranges[-1][1] = max(ranges[-1][1], end)
            else:
                ranges.append([value.offset, end])
        with self.lock:
            name, offset = holder.ref[0], holder.ref[1]
            path = self.directory / _segment_file(name)
            try:
                stream = self.files.pop(name, None) or path.open("rb")
                self.files[name] = stream
                while len(self.files) > _OPEN_SEGMENTS:
                    self.files.popitem(last=False)[1].close()
                payloads = [
                    (
                        start,
                        b"".join(
                            _read_chunks(stream.fileno(), end - start, offset + start)
                        ),
                    )
                    for start, end in ranges
                ]
            except (OSError, ValueError) as error:
                raise RuntimeError(
                    f"cannot read spilled trajectory data from {path}; keep the "
                    "run or spill directory available while trajectories are in use"
                ) from error
        arrays = []
        for value in values:
            start, payload = next(
                (start, payload)
                for start, payload in reversed(payloads)
                if start <= value.offset
            )
            array = (
                np.frombuffer(
                    payload,
                    dtype=value.dtype,
                    count=math.prod(value.shape),
                    offset=value.offset - start,
                )
                .reshape(value.shape)
                .copy()
            )
            array.flags.writeable = False
            arrays.append(array)
        return arrays


_SPILL_FILES = weakref.WeakValueDictionary()
_SPILL_FILES_LOCK = threading.Lock()


def _spill_files(directory):
    with _SPILL_FILES_LOCK:
        key = os.path.realpath(directory)
        files = _SPILL_FILES.get(key)
        if files is None:
            files = _SPILL_FILES[key] = _SpillFiles(Path(key))
        return files


class _Holder:
    """A segment record that spilled arrays read from.

    Compaction moves records; the commit updates ``ref`` under the files'
    lock, which readers also hold while they resolve it.
    """

    __slots__ = ("files", "ref", "__weakref__")

    def __init__(self, files, ref):
        self.files, self.ref = files, ref

    def read(self, values):
        return self.files.read(self, values)


class _CommittedRecord:
    """A journal record already in a segment; ``StateStore.read`` loads it."""

    __slots__ = ("ref",)

    def __init__(self, ref):
        self.ref = ref


class _RecordCapture:
    """An immutable value written once and referenced by later saves.

    ``value`` is None for a record that is part of a larger capture.
    """

    def __init__(self, value, payload, ref):
        self.value, self.payload, self.ref = value, payload, ref
        self.records = None


class _CommittedTrajectory:
    """A journaled trajectory's committed records; ``StateStore.read`` loads it."""

    __slots__ = ("fields", "records")

    def __init__(self, fields, records):
        self.fields, self.records = fields, records


class _CommittedUpdate:
    """An update journaled by reference; ``StateStore.read`` loads it.

    ``recipes`` holds each datum's run, advantage, normalization and
    corrections; ``trajectories`` the span records they build from.
    """

    __slots__ = ("optimizer", "recipes", "trajectories")

    def __init__(self, optimizer, recipes, trajectories):
        self.optimizer, self.recipes = optimizer, recipes
        self.trajectories = trajectories


class _JournalTrajectoryCapture:
    """A trained trajectory's spans: committed records plus any new spans."""

    def __init__(
        self, fields, base, delta=None, written=(), unspilled=(), committed=None
    ):
        self.fields, self.base, self.delta = fields, base, delta
        self.written, self.unspilled, self.committed = written, unspilled, committed
        self.records = self.packed = None


class _UpdateCapture:
    def __init__(self, value, optimizer, recipes, trajectories):
        self.value, self.optimizer = value, optimizer
        self.recipes, self.trajectories = recipes, trajectories


class _Capture:
    def __init__(self, store):
        self._store = store
        self._trajectories = {}
        self.spills = []

    def trajectory(self, trajectory):
        """Return trajectory fields plus a reference to its spans and messages.

        Spans are append-only. Messages already saved are treated as
        immutable unless the list is replaced, as ``Trajectory.rewrite`` does.
        """
        capture = self._trajectories.get(id(trajectory))
        if capture is None or not capture.current():
            # A trajectory can advance between captures within one save, for
            # example while an environment snapshot is awaited.
            capture = self._store_capture(trajectory)
            self._trajectories[id(trajectory)] = capture
        fields = encode_state(
            {
                key: value
                for key, value in vars(trajectory).items()
                if key not in ("_spans", "messages")
            }
        )
        return {**fields, _TRAJECTORY: capture}

    def _store_capture(self, trajectory):
        cursor = self._store._cursors.get(id(trajectory))
        spans, messages = trajectory._spans, trajectory.messages
        if (
            cursor is None
            or cursor.trajectory is not trajectory
            or cursor.spans is not spans
            or len(spans) < cursor.span_count
        ):
            # A replaced span list (for example re-stamped policy steps)
            # rewrites the trajectory from scratch.
            base, span_start, message_start, unspilled = (), 0, 0, ()
        else:
            base, span_start = cursor.records, cursor.span_count
            message_start = (
                cursor.message_count
                if cursor.messages is messages and len(messages) >= cursor.message_count
                else 0
            )
            unspilled = cursor.unspilled
        if (
            base
            and span_start == len(spans)
            and message_start == cursor.message_count == len(messages)
        ):
            return _TrajectoryCapture(trajectory, base, None, unspilled=unspilled)
        written = spans[span_start:]
        return _TrajectoryCapture(
            trajectory,
            base,
            {
                # Spilled arrays are copied by the save, not read here.
                "spans": [span._state(read=False) for span in written],
                "messages_start": message_start,
                "messages": encode_state(messages[message_start:]),
            },
            written,
            unspilled,
        )

    def spill(self, trajectory):
        """Write a trajectory's in-memory span arrays without saving it.

        For unfinished trajectories that restore would regenerate: the arrays
        still leave memory once the save commits.
        """
        if not self._store._spill_arrays:
            return
        cursor = self._store._spill_cursors.get(id(trajectory))
        spans, run = trajectory._spans, trajectory.run
        start = (
            cursor.span_count
            if cursor is not None
            and cursor.trajectory is trajectory
            and cursor.spans is spans
            and cursor.run == run
            and len(spans) >= cursor.span_count
            else 0
        )
        self.spills.append(
            _SpillCapture(
                trajectory,
                [span for span in spans[start:] if _unspilled(span, span.run < run)],
            )
        )

    def update(self, update):
        """Reference a journal update, writing it only on its first save.

        An update whose chunks are ``TrainingBatch`` objects is journaled by
        reference: the trajectories its datums build from, which earlier saves
        usually wrote already, plus a small record of each datum's recipe.
        Other updates are written as datums.
        """
        if isinstance(update, _CommittedUpdate):
            return self._committed_update(update)
        committed = self._store._records.get(id(update))
        if committed is not None and committed[0] is update:
            if isinstance(committed[1], _CommittedUpdate):
                return self._committed_update(committed[1])
            return _RecordCapture(update, None, committed[1])
        if not isinstance(update, dict):
            return self.record(update)
        chunks = update.get("chunks")
        kind = "chunks"
        if chunks is None:
            chunks, kind = [update["data"]], "data"
        if not all(isinstance(chunk, TrainingBatch) for chunk in chunks):
            return self.record(update)
        sources, builds, trajectories, recipes, proximal = {}, {}, [], [], []
        for chunk in chunks:
            custom = {item.custom is not None for item in chunk._items}
            if len(custom) > 1:
                return self.record(update)
            items = []
            for item in chunk._items:
                if id(item.source) not in sources:
                    sources[id(item.source)] = len(trajectories)
                    trajectories.append(self._journal_trajectory(item.source))
                build = item.build
                if id(build) not in builds:
                    builds[id(build)] = (
                        len(builds),
                        {
                            "current_step": build.current_step,
                            "max_staleness": build.max_staleness,
                            "include_loss_mask": build.include_loss_mask,
                            "loss": build.loss is not None,
                        },
                    )
                row = None
                if item.proximal is not None:
                    row = len(proximal)
                    array = np.asarray(item.proximal[0])
                    if array.dtype not in (np.float32, np.float64):
                        array = array.astype(np.float64)
                    proximal.append(array)
                items.append(
                    {
                        "trajectory": sources[id(item.source)],
                        "run": item.run,
                        "advantage": float(item.advantage),
                        "denominator": float(item.denominator),
                        "length": item.length,
                        "advantaged": item.advantaged,
                        "routing_handle": item.routing_handle,
                        "recovered": item.recovered,
                        "build": builds[id(build)][0],
                        "proximal": row,
                        "max_importance_weight": None
                        if item.proximal is None
                        else float(item.proximal[1]),
                        "drop_recovery": item.drop_recovery,
                        "drop_routing": item.drop_routing,
                    }
                )
            recipes.append({"custom": True in custom, "items": items})
        payload = {
            "kind": kind,
            "chunks": recipes,
            "builds": [build for _, build in builds.values()],
            "proximal": proximal,
        }
        return _UpdateCapture(
            update,
            update["optimizer"],
            _RecordCapture(None, payload, None),
            trajectories,
        )

    def _committed_update(self, update):
        return _UpdateCapture(
            update,
            update.optimizer,
            _RecordCapture(update.recipes, None, update.recipes.ref),
            [
                _JournalTrajectoryCapture(t.fields, t.records, committed=t)
                for t in update.trajectories
            ],
        )

    def _journal_trajectory(self, source):
        """Reference a batch's trajectory, writing only spans no save holds yet.

        A batch shares its trajectory's span list, so the trajectory's last
        committed records usually cover every span. Spans are append-only and
        restamping replaces the list, so a different list is written whole.
        """
        spans = source._spans
        cursor = self._store._span_cursors.get(id(spans))
        if (
            cursor is not None
            and cursor.spans is spans
            and len(spans) >= cursor.span_count
        ):
            base, start = cursor.records, cursor.span_count
            message_start, unspilled = cursor.message_count, cursor.unspilled
        else:
            base, start, message_start, unspilled = (), 0, 0, ()
        fields = encode_state(
            {key: value for key, value in vars(source).items() if key != "_spans"}
        )
        written = spans[start:]
        if base and not written:
            return _JournalTrajectoryCapture(fields, base, unspilled=unspilled)
        return _JournalTrajectoryCapture(
            fields,
            base,
            {
                "spans": [span._state(read=False) for span in written],
                # Messages are not replayed; keep those already saved.
                "messages_start": message_start,
                "messages": [],
            },
            written,
            unspilled,
        )

    def record(self, value):
        """Reference ``value``, writing a copy of it only on its first save."""
        if isinstance(value, _CommittedRecord):
            return _RecordCapture(value, None, value.ref)
        committed = self._store._records.get(id(value))
        if committed is not None and committed[0] is value:
            return _RecordCapture(value, None, committed[1])
        # encode_state rebuilds every container; arrays and scalars are not
        # mutated once a journal update is committed.
        return _RecordCapture(value, encode_state(value), None)


class _Relative:
    """A write stream whose positions start at its creation offset."""

    def __init__(self, stream):
        self.stream, self.start = stream, stream.tell()

    def tell(self):
        return self.stream.tell() - self.start

    def write(self, data):
        return self.stream.write(data)


class _SegmentWriter:
    def __init__(self, store, name, stream, images):
        self.store, self.name, self.stream, self.source = store, name, stream, images
        self.captures = {}
        self.containers = []
        self.digests = set()

    def resolve(self, value):
        if isinstance(value, dict) and isinstance(
            value.get(_TRAJECTORY), _TrajectoryCapture
        ):
            capture = value[_TRAJECTORY]
            if capture.records is None:
                records = list(capture.base)
                if capture.delta is not None:
                    ref, packed = self.write(capture.delta)
                    records.append(ref)
                    capture.packed = packed["spans"]
                capture.records = records
                self.captures[id(capture)] = capture
                self.containers.append(records)
            fields = {k: v for k, v in value.items() if k != _TRAJECTORY}
            return {**self.resolve(fields), _TRAJECTORY: capture.records}
        if isinstance(value, _RecordCapture):
            if value.records is None:
                ref = (
                    value.ref if value.payload is None else self.write(value.payload)[0]
                )
                value.records = [ref]
                self.captures[id(value)] = value
                self.containers.append(value.records)
            return {_RECORD: value.records}
        if isinstance(value, _JournalTrajectoryCapture):
            if value.records is None:
                records = list(value.base)
                if value.delta is not None:
                    ref, packed = self.write(value.delta)
                    records.append(ref)
                    value.packed = packed["spans"]
                value.records = records
                self.captures[id(value)] = value
                self.containers.append(records)
            return {**value.fields, _JOURNAL_TRAJECTORY: value.records}
        if isinstance(value, _UpdateCapture):
            self.captures[id(value)] = value
            return {
                _UPDATE: 1,
                "optimizer": value.optimizer,
                "recipes": self.resolve(value.recipes),
                "trajectories": [self.resolve(t) for t in value.trajectories],
            }
        if isinstance(value, dict):
            if any(key in value for key in _RESERVED):
                raise ValueError("checkpoint state contains reserved record metadata")
            return {key: self.resolve(item) for key, item in value.items()}
        if isinstance(value, (list, tuple)):
            return [self.resolve(item) for item in value]
        return value

    def spill(self, captures):
        self.spills = captures
        for capture in captures:
            if capture.written:
                capture.ref, packed = self.write({"spans": capture.payload})
                capture.packed = packed["spans"]

    def write(self, payload):
        """Append one record, its arrays then its JSON; return it and its layout."""
        offset = self.stream.tell()
        arrays = _Relative(self.stream)
        packed = _pack_arrays(payload, arrays, _read_all_spilled(payload))
        text = json.dumps(
            packed, ensure_ascii=False, separators=(",", ":"), allow_nan=False
        ).encode()
        array_bytes = arrays.tell()
        self.stream.write(text)
        digests = sorted(
            self.store.images.copy_images(decode_state(packed), self.source)
        )
        return (self.name, offset, array_bytes, len(text), *digests), packed

    def compact(self):
        """Copy live records out of old segments that are mostly dead.

        Records that spilled arrays read from are live too; the commit points
        their holders at the copies.
        """
        self.held = list(self.store._spill.holders)
        self.moved = {}
        live = {}
        for ref in {
            *(ref for records in self.containers for ref in records),
            *(holder.ref for holder in self.held),
        }:
            live[ref[0]] = live.get(ref[0], 0) + ref[2] + ref[3]
        sizes = {
            name: self.store._segments[name]["bytes"]
            for name in live
            if name != self.name
        }
        sparse = {
            name for name, size in sizes.items() if live[name] < size * _COMPACT_BELOW
        }
        remaining = sorted(
            (name for name in sizes if name not in sparse), key=lambda n: live[n]
        )
        sparse.update(remaining[: max(0, len(remaining) - _MAX_SEGMENTS)])
        if not sparse:
            return
        moved = self.moved
        sources = {
            name: (self.store.directory / _segment_file(name)).open("rb")
            for name in sparse
        }
        try:
            # A copy gets a fresh checksum, so verify the committed one first.
            for name, source in sources.items():
                if (
                    hashlib.file_digest(source, "sha256").hexdigest()
                    != self.store._segments[name]["sha256"]
                ):
                    raise ValueError("checkpoint segment integrity verification failed")

            def move(ref):
                if ref not in moved:
                    name, offset, array_bytes, text_bytes, *digests = ref
                    moved[ref] = (
                        self.name,
                        self.stream.tell(),
                        array_bytes,
                        text_bytes,
                        *digests,
                    )
                    for chunk in _read_chunks(
                        sources[name].fileno(), array_bytes + text_bytes, offset
                    ):
                        self.stream.write(chunk)
                return moved[ref]

            for records in self.containers:
                for index, ref in enumerate(records):
                    if ref[0] in sparse:
                        records[index] = move(ref)
            for holder in self.held:
                if holder.ref[0] in sparse:
                    move(holder.ref)
        finally:
            for source in sources.values():
                source.close()

    def images(self):
        return {
            digest
            for records in self.containers
            for ref in records
            for digest in ref[4:]
        }

    def segments(self, name, size, digest):
        used = {
            *(ref[0] for records in self.containers for ref in records),
            *(self.moved.get(holder.ref, holder.ref)[0] for holder in self.held),
        } - {name}
        return {
            **{segment: self.store._segments[segment] for segment in sorted(used)},
            name: {"bytes": size, "sha256": digest},
        }

    def commit(self):
        """Advance cursors and spill written arrays; call under the I/O lock."""
        for holder in self.held:
            holder.ref = self.moved.get(holder.ref, holder.ref)
        spilling = self.store._spill_arrays
        cursors, records, serials, newest = {}, {}, {}, {}
        for capture in self.captures.values():
            if isinstance(capture, _RecordCapture):
                if isinstance(capture.value, _CommittedRecord):
                    # Compaction may have moved the record.
                    capture.value.ref = capture.records[0]
                elif capture.value is not None:
                    records[id(capture.value)] = (capture.value, capture.records[0])
            elif isinstance(capture, _JournalTrajectoryCapture):
                if capture.committed is not None:
                    capture.committed.records = tuple(capture.records)
                elif spilling:
                    # Trained trajectories are complete: no turn resends ids.
                    for span, holder, locations in capture.unspilled:
                        _spill_tokens(span, locations, holder)
                    if capture.packed is not None:
                        holder = self._holder(capture.records[-1])
                        for span, packed in zip(
                            capture.written, capture.packed, strict=True
                        ):
                            _spill(span, packed, holder)
                            _spill_tokens(span, _token_locations(packed), holder)
            elif isinstance(capture, _UpdateCapture):
                if not isinstance(capture.value, _CommittedUpdate):
                    records[id(capture.value)] = (
                        capture.value,
                        _CommittedUpdate(
                            capture.optimizer,
                            _CommittedRecord(capture.recipes.records[0]),
                            [
                                _CommittedTrajectory(t.fields, tuple(t.records))
                                for t in capture.trajectories
                            ],
                        ),
                    )
            elif (
                id(capture.trajectory) not in serials
                or serials[id(capture.trajectory)] < capture.serial
            ):
                # The newest capture of a trajectory becomes its cursor.
                serials[id(capture.trajectory)] = capture.serial
                newest[id(capture.trajectory)] = capture
        for key, capture in newest.items():
            unspilled = list(capture.unspilled) if spilling else []
            if spilling and capture.packed is not None:
                # A content record is the last one of its trajectory's records.
                holder = self._holder(capture.records[-1])
                for span, packed in zip(capture.written, capture.packed, strict=True):
                    _spill(span, packed, holder)
                    unspilled.append((span, holder, _token_locations(packed)))
            # Token ids leave memory once no turn resends them: in runs before
            # a rewrite, or when the trajectory is complete.
            keep = []
            for span, holder, locations in unspilled:
                if span.run < capture.run or capture.done:
                    _spill_tokens(span, locations, holder)
                elif any(
                    isinstance(tokens := span._chunks[index]["tokens"], np.ndarray)
                    and _spillable(tokens)
                    for index, _ in locations
                ):
                    keep.append((span, holder, locations))
            cursors[key] = _Cursor(
                capture.trajectory,
                capture.spans,
                capture.span_count,
                capture.messages,
                capture.message_count,
                tuple(capture.records),
                capture.run,
                tuple(keep),
            )
        spill_cursors = {}
        for capture in self.spills if spilling else ():
            if capture.packed is not None:
                holder = self._holder(capture.ref)
                for span, packed in zip(capture.written, capture.packed, strict=True):
                    _spill(span, packed, holder)
                    if span.run < capture.run:
                        _spill_tokens(span, _token_locations(packed), holder)
        for capture in self.spills:
            spill_cursors[id(capture.trajectory)] = _Cursor(
                capture.trajectory,
                capture.spans,
                capture.span_count,
                None,
                0,
                (),
                capture.run,
            )
        return cursors, records, spill_cursors

    def _holder(self, ref):
        holder = _Holder(self.store._spill, ref)
        self.store._spill.holders.add(holder)
        return holder


def _spillable(value):
    return isinstance(value, (np.ndarray, _Spilled)) and value.nbytes >= _SPILL_BYTES


def _unspilled(span, tokens):
    """Whether ``span`` holds arrays in memory that a spill would write."""
    values = span.__dict__
    return any(
        isinstance(value, np.ndarray) and _spillable(value)
        for value in (
            *(values[name] for name in _SPAN_ARRAYS),
            *(
                c["tokens"]
                for c in (span._chunks if tokens else ())
                if c["type"] == "text"
            ),
        )
    )


def _spill_state(span, tokens):
    """The in-memory arrays of ``span`` that a spill record holds."""

    def keep(value):
        return value if isinstance(value, np.ndarray) and _spillable(value) else None

    return {
        **{name: keep(span.__dict__[name]) for name in _SPAN_ARRAYS},
        "chunks": [
            {"tokens": keep(c["tokens"]) if tokens and c["type"] == "text" else None}
            for c in span._chunks
        ],
    }


def _stored(marker):
    if isinstance(marker, dict) and set(marker) == {"__river_ndarray_storage__"}:
        return marker["__river_ndarray_storage__"]
    return None


def _spill(span, packed, holder):
    """Point ``span``'s logprob-like arrays at their copies in a record."""
    values = span.__dict__
    for name in _SPAN_ARRAYS:
        location = _stored(packed.get(name))
        if location is not None and _spillable(values[name]):
            values[name] = _Spilled(holder, *location)


def _token_locations(packed):
    """Record locations of a packed span's token ids, by chunk index.

    Pending cursors keep these rather than the packed chunks, which may hold
    encoded image bytes.
    """
    return tuple(
        (index, location)
        for index, chunk in enumerate(packed["chunks"])
        if (location := _stored(chunk.get("tokens"))) is not None
    )


def _spill_tokens(span, locations, holder):
    """Point ``span``'s token ids at their copies in a record.

    Token ids already spilled to an older record move to the new copy too, so
    the older record need not stay live.
    """
    for index, location in locations:
        chunk = span._chunks[index]
        if chunk["type"] == "text" and _spillable(chunk["tokens"]):
            chunk["tokens"] = _Spilled(holder, *location)


def _expand(value, read, cache, lazy_records=False):
    """Replace record references with their content."""
    if isinstance(value, dict):
        if _TRAJECTORY in value:
            fields = {k: v for k, v in value.items() if k != _TRAJECTORY}
            return _trajectory_state(fields, value[_TRAJECTORY], read, cache)
        if _UPDATE in value:
            trajectories = [
                _CommittedTrajectory(
                    {k: v for k, v in t.items() if k != _JOURNAL_TRAJECTORY},
                    tuple(tuple(ref) for ref in t[_JOURNAL_TRAJECTORY]),
                )
                for t in value["trajectories"]
            ]
            recipes = _CommittedRecord(tuple(value["recipes"][_RECORD][0]))
            update = _CommittedUpdate(value["optimizer"], recipes, trajectories)
            if lazy_records:
                return update
            return {
                "optimizer": update.optimizer,
                **_read_record(recipes.ref, read, cache),
                "trajectories": [
                    _trajectory_state(t.fields, t.records, read, cache, messages=False)
                    for t in trajectories
                ],
            }
        if _RECORD in value:
            if lazy_records:
                # Writers use references as keys; JSON returns them as lists.
                return _CommittedRecord(tuple(value[_RECORD][0]))
            return _read_record(value[_RECORD][0], read, cache)
        return {
            key: _expand(item, read, cache, lazy_records) for key, item in value.items()
        }
    if isinstance(value, list):
        return [_expand(item, read, cache, lazy_records) for item in value]
    return value


def _trajectory_state(fields, records, read, cache, *, messages=True):
    """A ``Trajectory.state_dict`` from its fields and records, in order."""
    spans, history = [], []
    for ref in records:
        content = _read_record(ref, read, cache)
        spans.extend(content["spans"])
        if messages:
            history = [*history[: content["messages_start"]], *content["messages"]]
    return {"version": 1, **fields, "spans": spans, "messages": history}


def _read_record(ref, read, cache):
    key = tuple(ref[:4])
    if key not in cache:
        name, offset, array_bytes, text_bytes = key
        payload = read(name, offset, array_bytes + text_bytes)
        cache[key] = _unpack_arrays(
            decode_state(json.loads(payload[array_bytes:])), payload[:array_bytes]
        )
    return cache[key]


def _read_all_spilled(value):
    """Read every spilled array in ``value``, one coalesced read per record."""
    wanted = {}

    def collect(item):
        if isinstance(item, _Spilled):
            wanted.setdefault(item.holder, []).append(item)
        elif isinstance(item, dict):
            for child in item.values():
                collect(child)
        elif isinstance(item, (list, tuple)):
            for child in item:
                collect(child)

    collect(value)
    arrays = {}
    for holder, values in wanted.items():
        arrays.update(zip(map(id, values), holder.read(values), strict=True))
    return arrays


def _pack_arrays(value, stream, spilled=None):
    if isinstance(value, TrainingBatch):
        # Journal batches are built and written one datum at a time, so a
        # save never holds an update's datums at once.
        return [_pack_arrays(encode_state(datum), stream) for datum in value]
    if isinstance(value, _Spilled):
        # A rewritten span copies its spilled bytes into the new segment.
        value = spilled[id(value)] if spilled else value.read()
    if isinstance(value, np.ndarray):
        # Preserve array dtype and representation through recovery.
        if value.ndim not in (1, 2) or value.dtype.str not in {
            "<i8",
            "<i4",
            "|u1",
            "<f8",
            "<f4",
            "|b1",
        }:
            raise ValueError("unsupported checkpoint array shape or dtype")
        array = np.ascontiguousarray(value)
        offset = stream.tell()
        if array.size:
            stream.write(memoryview(array).cast("B"))
        return {
            "__river_ndarray_storage__": [offset, list(array.shape), array.dtype.str]
        }
    if isinstance(value, dict):
        if "__river_array__" in value or "__river_ndarray_storage__" in value:
            raise ValueError("checkpoint state contains reserved array metadata")
        return {key: _pack_arrays(item, stream, spilled) for key, item in value.items()}
    if isinstance(value, (list, tuple)):
        shape = len(value)
        count, items = len(value), value
        if (
            value
            and isinstance(value[0], (list, tuple))
            and value[0]
            and all(
                isinstance(row, (list, tuple)) and len(row) == len(value[0])
                for row in value
            )
        ):
            shape = [len(value), len(value[0])]
            count = math.prod(shape)
            items = chain.from_iterable(value)
        if count >= 64:
            kind = type(value[0][0] if isinstance(shape, list) else value[0])
            dtype = {int: "<i8", float: "<f8", bool: "|b1"}.get(kind)
            if dtype and all(type(item) is kind for item in items):
                try:
                    array = np.asarray(value, dtype=dtype)
                except OverflowError:
                    # Python integers outside int64 remain lossless JSON numbers.
                    return list(value)
                if kind is int:
                    lower, upper = array.min(), array.max()
                    if lower >= 0 and upper <= 255:
                        dtype = "|u1"
                    elif lower >= -(2**31) and upper < 2**31:
                        dtype = "<i4"
                    array = array.astype(dtype, copy=False)
                if kind is float and not np.isfinite(array).all():
                    raise ValueError("checkpoint arrays must contain finite values")
                offset = stream.tell()
                stream.write(array.tobytes())
                return {"__river_array__": [offset, shape, dtype]}
        return [_pack_arrays(item, stream, spilled) for item in value]
    return value


# Bytes a version 2 load reads at once; arrays are stored in load order.
_ARRAY_WINDOW = 16 << 20


class _ArrayWindow:
    """A file read with pread through one bounded window, as a payload.

    Read errors raise exceptions, unlike faults in a memory map. Arrays
    viewed from the window must be copied before the next ``view``.
    """

    def __init__(self, descriptor, size):
        self.descriptor, self.size = descriptor, size
        self.start, self.data = 0, b""

    def __len__(self):
        return self.size

    def view(self, offset, dtype, count):
        length = count * np.dtype(dtype).itemsize
        if not (
            self.start <= offset and offset + length <= self.start + len(self.data)
        ):
            self.data = b""  # release the old window before reading the next
            self.start = offset
            self.data = b"".join(
                _read_chunks(
                    self.descriptor,
                    min(max(length, _ARRAY_WINDOW), self.size - offset),
                    offset,
                )
            )
        return np.frombuffer(
            self.data, dtype=dtype, count=count, offset=offset - self.start
        )


def _unpack_arrays(value, payload, arrays=None):
    """Restore packed arrays; ``arrays`` converts list-packed ones instead of tolist."""
    if isinstance(value, dict):
        if set(value) in ({"__river_array__"}, {"__river_ndarray_storage__"}):
            marker = next(iter(value))
            offset, shape, dtype = value[marker]
            dimensions = shape if isinstance(shape, list) else [shape]
            if len(dimensions) not in {1, 2} or any(
                type(size) is not int or size < 0 for size in dimensions
            ):
                raise ValueError("invalid checkpoint array shape")
            count = math.prod(dimensions)
            if (
                dtype not in {"<i8", "<i4", "|u1", "<f8", "<f4", "|b1"}
                or type(offset) is not int
                or offset < 0
                or offset + count * np.dtype(dtype).itemsize > len(payload)
            ):
                raise ValueError("invalid checkpoint array bounds or dtype")
            array = (
                payload.view(offset, dtype, count)
                if isinstance(payload, _ArrayWindow)
                else np.frombuffer(payload, dtype=dtype, count=count, offset=offset)
            ).reshape(dimensions)
            # Every branch copies: a leaf must not pin the payload or window.
            if marker == "__river_ndarray_storage__":
                array = array.copy()
                array.flags.writeable = False
                return array
            return array.tolist() if arrays is None else arrays(array)
        return {
            key: _unpack_arrays(item, payload, arrays) for key, item in value.items()
        }
    if isinstance(value, list):
        return [_unpack_arrays(item, payload, arrays) for item in value]
    return value


def _owned(view):
    # Span normalizes dtypes and keeps read-only arrays of its own dtype.
    array = view.copy()
    array.flags.writeable = False
    return array


def _wire(view):
    # Version 2 journals held Python lists, which the client sent as int64
    # and float32 arrays; keep those wire dtypes.
    return view.astype(np.float32 if view.dtype.kind == "f" else np.int64)


def _unpack_v2(state, payload):
    """Restore version 2 state without listing token and logprob arrays.

    Version 2 stored trajectory spans and journal datums as Python lists in
    memory. They return as arrays; other packed lists, which may belong to
    user rows or environment state, return as lists.
    """

    def trajectory(value):
        if not isinstance(value, dict):
            return _unpack_arrays(value, payload)
        return {
            key: _unpack_arrays(item, payload, _owned if key == "spans" else None)
            for key, item in value.items()
        }

    def result(value):
        if not isinstance(value, dict) or not isinstance(
            value.get("trajectories"), list
        ):
            return _unpack_arrays(value, payload)
        return {
            key: [trajectory(t) for t in item]
            if key == "trajectories"
            else _unpack_arrays(item, payload)
            for key, item in value.items()
        }

    def group(value):
        if not isinstance(value, dict) or not isinstance(value.get("members"), list):
            return _unpack_arrays(value, payload)
        return {
            key: [
                {
                    k: trajectory(v) if k == "traj" else _unpack_arrays(v, payload)
                    for k, v in member.items()
                }
                if isinstance(member, dict)
                else _unpack_arrays(member, payload)
                for member in item
            ]
            if key == "members"
            else _unpack_arrays(item, payload)
            for key, item in value.items()
        }

    def update(value):
        if not isinstance(value, dict):
            return _unpack_arrays(value, payload)
        return {
            key: _unpack_arrays(
                item, payload, _wire if key in ("data", "chunks") else None
            )
            for key, item in value.items()
        }

    def engine(value):
        if not isinstance(value, dict):
            return _unpack_arrays(value, payload)
        return {
            key: [group(g) for g in item]
            if key == "groups" and isinstance(item, list)
            else [result(r) for r in item]
            if key == "outbox" and isinstance(item, list)
            else _unpack_arrays(item, payload)
            for key, item in value.items()
        }

    if not isinstance(state, dict):
        return _unpack_arrays(state, payload)
    restore = {
        "journal": lambda item: [update(u) for u in item],
        "pending": lambda item: [result(r) for r in item],
        "engine": engine,
    }
    return {
        key: restore[key](item)
        if key in restore and isinstance(item, (list, dict))
        else _unpack_arrays(item, payload)
        for key, item in state.items()
    }


_NON_ASCII = re.compile(r"[^\x00-\x7f]+")
# Read a manifest in pieces this large.
_JSON_CHUNK = 16 << 20


def _read_json(path):
    """Parse a JSON file without one document-wide string of its widest character.

    A str stores every character at the width of its widest one, so a single
    emoji makes a decoded multi-GiB manifest four bytes per character.
    Escaping non-ASCII characters, which JSON allows only inside strings,
    keeps the document one byte per character; json still builds each string
    value at its own width.
    """
    decoder = codecs.getincrementaldecoder("utf-8")()
    parts = []

    def ascii_text(text):
        if text.isascii():
            return text
        return _NON_ASCII.sub(
            lambda match: json.encoder.encode_basestring_ascii(match.group())[1:-1],
            text,
        )

    with path.open("rb") as stream:
        remaining = os.fstat(stream.fileno()).st_size
        # read(n) allocates n bytes up front; never ask for more than remains.
        while remaining and (chunk := stream.read(min(_JSON_CHUNK, remaining))):
            remaining -= len(chunk)
            parts.append(ascii_text(decoder.decode(chunk)))
    parts.append(ascii_text(decoder.decode(b"", final=True)))
    text = "".join(parts)
    del parts
    return json.loads(text)
