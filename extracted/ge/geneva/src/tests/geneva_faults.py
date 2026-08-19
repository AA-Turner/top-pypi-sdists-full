# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""External fault-injection library for geneva's durable writes.

Lives outside the production ``geneva`` package, which exposes only the injection
points (``get_X``/``set_X``/``using_X`` per durable-write surface); this module supplies
the ``Flaky*`` implementations a test installs through them. Two install paths: an
in-process test calls ``set_X`` / ``using_X`` directly; a cross-process (real-Ray)
deployment runs ``install_all_from_env()`` in each worker -- e.g. from a
``sitecustomize`` bootstrap on the worker image, which this library does not itself
provide -- to install the ``Flaky*`` named by the propagated ``GENEVA_FAULT_*`` env
vars. Both work because production reads the injected global late, so a fault installed
before the first write takes effect. ``install_all_from_env`` and the spec parsers are
covered by ``test_geneva_faults_env_install``.
"""

from __future__ import annotations

import logging
import os
from collections.abc import Callable
from typing import TYPE_CHECKING, Any

import lance
import ray
import ray.exceptions  # noqa: F401 -- ray.exceptions.RayError used below

from geneva.checkpoint import CheckpointStore, set_checkpoint_store_wrap
from geneva.committer import Committer, LanceCommitter, set_committer
from geneva.field_metadata_writer import (
    FieldMetadataWriter,
    LanceFieldMetadataWriter,
    set_field_metadata_writer,
)
from geneva.fragment_writer import (
    FragmentFileWriter,
    RealFragmentFileWriter,
    set_fragment_file_writer,
)
from geneva.table_writer import LanceTableWriter, TableWriter, set_table_writer

if TYPE_CHECKING:
    from collections.abc import Collection, Iterator

    import pyarrow as pa

_LOG = logging.getLogger(__name__)


class InjectedFaultError(RuntimeError):
    """Models a worker dying at a durability boundary.

    A dedicated type so a test can tell an injected death from a real failure. Not in
    the ActorPool's ``_ACTOR_LOSS_ERRORS``, so it drives the driver-side commit/write
    failure path, not the actor-death path.
    """


# --- committer --------------------------------------------------------------

# Selects which commits a fault counts (e.g. only ``Append`` operations).
OpMatcher = Callable[[Any], bool]


def by_op_name(*names: str) -> OpMatcher:
    """Match commits whose operation class name is one of ``names``."""
    wanted = frozenset(names)
    return lambda op: type(op).__name__ in wanted


class FlakyCommitter:
    """Committer that faults selected commits, for worker-death tests.

    Counts commits matching ``match`` (all if None), 1-based. By matched index:
    ``raise_at`` raises ``InjectedFaultError``; ``drop_at`` skips the commit but returns
    the dataset at its pre-commit version (a lost commit reported as success);
    ``raise_after`` lands the commit then raises (the at-least-once-retry case);
    ``conflict_at`` raises a retryable-conflict-shaped ``OSError`` WITHOUT committing
    (a concurrent writer won the version -- the caller's conflict-retry loop should
    refetch the version and retry); ``conflict_after`` lands the commit then raises the
    same conflict-shaped error (a lost ack -- a conflict-retry loop that cannot tell
    the retry from the original will re-apply an already-landed commit).
    """

    # Substring-matches geneva's retryable-conflict classifier, like lance's own error.
    _CONFLICT_MSG = (
        "Retryable commit conflict for version {v}: this transaction was preempted "
        "by an injected concurrent transaction. Please retry."
    )

    def __init__(
        self,
        inner: Committer | None = None,
        *,
        drop_at: Collection[int] = (),
        raise_at: Collection[int] = (),
        raise_after: Collection[int] = (),
        conflict_at: Collection[int] = (),
        conflict_after: Collection[int] = (),
        match: OpMatcher | None = None,
    ) -> None:
        self.inner: Committer = inner or LanceCommitter()
        self.drop_at = frozenset(drop_at)
        self.raise_at = frozenset(raise_at)
        self.raise_after = frozenset(raise_after)
        self.conflict_at = frozenset(conflict_at)
        self.conflict_after = frozenset(conflict_after)
        self.match = match
        self.calls = 0
        self.dropped: list[int] = []
        self.raised: list[int] = []
        self.raised_after: list[int] = []
        self.conflicted: list[int] = []
        self.conflicted_after: list[int] = []

    def commit(
        self,
        dataset_or_uri: Any,
        operation: Any,
        *,
        read_version: int | None = None,
        storage_options: dict[str, str] | None = None,
        namespace_client: Any = None,
        table_id: list[str] | None = None,
    ) -> lance.LanceDataset:
        if self.match is None or self.match(operation):
            self.calls += 1
            n = self.calls
            if n in self.raise_at:
                self.raised.append(n)
                raise InjectedFaultError(
                    f"injected worker death at commit #{n} ({type(operation).__name__})"
                )
            if n in self.drop_at:
                self.dropped.append(n)
                return self._unchanged(dataset_or_uri, read_version, storage_options)
            if n in self.raise_after:
                self.inner.commit(
                    dataset_or_uri,
                    operation,
                    read_version=read_version,
                    storage_options=storage_options,
                    namespace_client=namespace_client,
                    table_id=table_id,
                )
                self.raised_after.append(n)
                raise InjectedFaultError(
                    f"injected worker death AFTER commit #{n} landed "
                    f"({type(operation).__name__})"
                )
            if n in self.conflict_at:
                self.conflicted.append(n)
                raise OSError(self._CONFLICT_MSG.format(v=read_version or 0))
            if n in self.conflict_after:
                self.inner.commit(
                    dataset_or_uri,
                    operation,
                    read_version=read_version,
                    storage_options=storage_options,
                    namespace_client=namespace_client,
                    table_id=table_id,
                )
                self.conflicted_after.append(n)
                raise OSError(self._CONFLICT_MSG.format(v=read_version or 0))
        return self.inner.commit(
            dataset_or_uri,
            operation,
            read_version=read_version,
            storage_options=storage_options,
            namespace_client=namespace_client,
            table_id=table_id,
        )

    @staticmethod
    def _unchanged(
        dataset_or_uri: Any,
        read_version: int | None,
        storage_options: dict[str, str] | None,
    ) -> lance.LanceDataset:
        # Reopen at the pre-commit version so callers see the unchanged dataset.
        uri = getattr(dataset_or_uri, "uri", dataset_or_uri)
        kw: dict[str, Any] = {}
        if storage_options is not None:
            kw["storage_options"] = storage_options
        if read_version is not None:
            kw["version"] = read_version
        return lance.dataset(uri, **kw)


class InterleavingCommitter:
    """Committer that runs a callback BEFORE selected commits, then delegates.

    Deterministically simulates a concurrent writer winning the race: the callback
    (e.g. an append to the same table) commits between the job's read of the table
    version and the job's own commit, so the delegated commit sees a bumped version
    and geneva's conflict handling must resolve it for real -- no synthetic error
    text involved. ``at`` selects which matched commits (1-based) get the interleave.
    """

    def __init__(
        self,
        interleave: Callable[[], None],
        *,
        inner: Committer | None = None,
        at: Collection[int] = (1,),
        match: OpMatcher | None = None,
    ) -> None:
        self.inner: Committer = inner or LanceCommitter()
        self.interleave = interleave
        self.at = frozenset(at)
        self.match = match
        self.calls = 0
        self.fired: list[int] = []

    def commit(
        self,
        dataset_or_uri: Any,
        operation: Any,
        *,
        read_version: int | None = None,
        storage_options: dict[str, str] | None = None,
        namespace_client: Any = None,
        table_id: list[str] | None = None,
    ) -> lance.LanceDataset:
        if self.match is None or self.match(operation):
            self.calls += 1
            if self.calls in self.at:
                self.fired.append(self.calls)
                self.interleave()
        return self.inner.commit(
            dataset_or_uri,
            operation,
            read_version=read_version,
            storage_options=storage_options,
            namespace_client=namespace_client,
            table_id=table_id,
        )


_COMMITTER_FAULT_ENV = "GENEVA_FAULT_COMMITTER"


def _parse_committer_fault(spec: str) -> FlakyCommitter:
    """Parse ``OpName:mode:occ[,occ...]`` (e.g. ``DataReplacement:drop:1``); ``mode`` is
    drop/raise/raise_after, occurrences 1-based. Raises ``ValueError`` if malformed."""
    parts = spec.split(":")
    if len(parts) != 3:
        raise ValueError(f"expected 'OpName:mode:occ', got {spec!r}")
    op_name, mode, occ_csv = (p.strip() for p in parts)
    if not op_name:
        raise ValueError("empty op name")
    if mode not in ("drop", "raise", "raise_after"):
        raise ValueError(f"bad mode {mode!r} (want drop/raise/raise_after)")
    occs = frozenset(int(x) for x in occ_csv.split(",") if x.strip())
    if not occs:
        raise ValueError(f"no occurrences in {occ_csv!r}")
    return FlakyCommitter(
        match=by_op_name(op_name),
        drop_at=occs if mode == "drop" else (),
        raise_at=occs if mode == "raise" else (),
        raise_after=occs if mode == "raise_after" else (),
    )


def install_committer_fault_from_env() -> FlakyCommitter | None:
    """Install a ``FlakyCommitter`` from ``GENEVA_FAULT_COMMITTER`` (no-op if unset;
    malformed spec logged and ignored)."""
    spec = os.environ.get(_COMMITTER_FAULT_ENV, "").strip()
    if not spec:
        return None
    try:
        committer = _parse_committer_fault(spec)
    except ValueError as e:
        _LOG.warning("ignoring malformed %s=%r: %s", _COMMITTER_FAULT_ENV, spec, e)
        return None
    set_committer(committer)
    _LOG.warning("INSTALLED committer fault from %s=%r", _COMMITTER_FAULT_ENV, spec)
    return committer


# --- table writer -----------------------------------------------------------

# Selects which lancedb table a write targets (e.g. only ``geneva_jobs``).
TableMatcher = Callable[[Any], bool]


def by_table_name(*substrings: str) -> TableMatcher:
    """Match writes whose table identity (``uri`` or ``name``) contains a substring."""
    subs = tuple(substrings)

    def _match(ltbl: Any) -> bool:
        ident = str(getattr(ltbl, "uri", None) or getattr(ltbl, "name", None) or "")
        return any(sub in ident for sub in subs)

    return _match


class FlakyTableWriter:
    """Table writer that faults selected lancedb writes, for worker-death tests.

    Counts writes whose op is in ``ops`` (all of add/update/delete if None), 1-based.
    By counted index: ``raise_at`` raises ``InjectedFaultError``; ``drop_at`` skips the
    write returning ``None`` (a lost write reported as success); ``raise_after`` lands
    the write then raises. ``table_match`` (optional) narrows to a specific table.
    """

    def __init__(
        self,
        inner: TableWriter | None = None,
        *,
        ops: Collection[str] | None = None,
        drop_at: Collection[int] = (),
        raise_at: Collection[int] = (),
        raise_after: Collection[int] = (),
        table_match: TableMatcher | None = None,
    ) -> None:
        self.inner: TableWriter = inner or LanceTableWriter()
        self.ops = frozenset(ops) if ops is not None else None
        self.drop_at = frozenset(drop_at)
        self.raise_at = frozenset(raise_at)
        self.raise_after = frozenset(raise_after)
        self.table_match = table_match
        self.calls = 0
        self.dropped: list[tuple[str, int]] = []
        self.raised: list[tuple[str, int]] = []
        self.raised_after: list[tuple[str, int]] = []

    def add(self, ltbl: Any, *args: Any, **kwargs: Any) -> Any:
        return self._maybe("add", ltbl, *args, **kwargs)

    def update(self, ltbl: Any, *args: Any, **kwargs: Any) -> Any:
        return self._maybe("update", ltbl, *args, **kwargs)

    def delete(self, ltbl: Any, *args: Any, **kwargs: Any) -> Any:
        return self._maybe("delete", ltbl, *args, **kwargs)

    def _maybe(self, op: str, ltbl: Any, *args: Any, **kwargs: Any) -> Any:
        op_matches = self.ops is None or op in self.ops
        table_matches = self.table_match is None or self.table_match(ltbl)
        if op_matches and table_matches:
            self.calls += 1
            n = self.calls
            if n in self.raise_at:
                self.raised.append((op, n))
                raise InjectedFaultError(f"injected worker death at {op} write #{n}")
            if n in self.drop_at:
                self.dropped.append((op, n))
                return None
            if n in self.raise_after:
                getattr(self.inner, op)(ltbl, *args, **kwargs)
                self.raised_after.append((op, n))
                raise InjectedFaultError(
                    f"injected worker death AFTER {op} write #{n} landed"
                )
        return getattr(self.inner, op)(ltbl, *args, **kwargs)


_TABLE_WRITER_FAULT_ENV = "GENEVA_FAULT_TABLE_WRITER"


def _parse_table_writer_fault(spec: str) -> FlakyTableWriter:
    """Parse ``op:mode:occ[,occ...]`` (e.g. ``delete:drop:1``); ``op`` is
    add/update/delete, ``mode`` is drop/raise/raise_after, occurrences 1-based.
    Raises ``ValueError`` if malformed."""
    parts = spec.split(":")
    if len(parts) != 3:
        raise ValueError(f"expected 'op:mode:occ', got {spec!r}")
    op, mode, occ_csv = (p.strip() for p in parts)
    if op not in ("add", "update", "delete"):
        raise ValueError(f"bad op {op!r} (want add/update/delete)")
    if mode not in ("drop", "raise", "raise_after"):
        raise ValueError(f"bad mode {mode!r} (want drop/raise/raise_after)")
    occs = frozenset(int(x) for x in occ_csv.split(",") if x.strip())
    if not occs:
        raise ValueError(f"no occurrences in {occ_csv!r}")
    return FlakyTableWriter(
        ops={op},
        drop_at=occs if mode == "drop" else (),
        raise_at=occs if mode == "raise" else (),
        raise_after=occs if mode == "raise_after" else (),
    )


def install_table_writer_fault_from_env() -> FlakyTableWriter | None:
    """Install a ``FlakyTableWriter`` from ``GENEVA_FAULT_TABLE_WRITER`` (no-op if
    unset; malformed spec logged and ignored)."""
    spec = os.environ.get(_TABLE_WRITER_FAULT_ENV, "").strip()
    if not spec:
        return None
    try:
        writer = _parse_table_writer_fault(spec)
    except ValueError as e:
        _LOG.warning("ignoring malformed %s=%r: %s", _TABLE_WRITER_FAULT_ENV, spec, e)
        return None
    set_table_writer(writer)
    _LOG.warning(
        "INSTALLED table-writer fault from %s=%r", _TABLE_WRITER_FAULT_ENV, spec
    )
    return writer


# --- fragment-file writer ---------------------------------------------------


def _drop_tail_rows(batches: Any, n_drop: int) -> Iterator[Any]:
    """Yield ``batches`` with the last ``n_drop`` rows removed (a short write).

    Buffers the stream to learn the total row count, then drops whole/partial trailing
    batches to remove exactly ``n_drop`` rows (or all rows if fewer).
    """
    bufs = list(batches)
    total = sum(b.num_rows for b in bufs)
    keep = max(0, total - n_drop)
    seen = 0
    out = []
    for b in bufs:
        if seen >= keep:
            break
        take = min(b.num_rows, keep - seen)
        out.append(b.slice(0, take))
        seen += take
    return iter(out)


class FlakyFragmentFileWriter:
    """Fails or truncates selected fragment-data-file writes, modelling writer faults.

    Counts ``write`` calls 1-based. By counted index: ``raise_at`` raises a
    ``ray.exceptions.RayError`` before the file is written (the driver's
    graceful-degradation path swallows it to a WARNING and reports success with the
    fragment missing); ``short_at`` writes the fragment with its last ``short_rows``
    rows dropped (a partial write, to probe whether the short file is validated against
    the row count).
    """

    def __init__(
        self,
        inner: FragmentFileWriter | None = None,
        *,
        raise_at: Collection[int] = (),
        short_at: Collection[int] = (),
        short_rows: int = 1,
    ) -> None:
        self.inner: FragmentFileWriter = inner or RealFragmentFileWriter()
        self.raise_at = frozenset(raise_at)
        self.short_at = frozenset(short_at)
        self.short_rows = short_rows
        self.calls = 0
        self.raised: list[int] = []
        self.shorted: list[int] = []

    def write(self, fn: Callable[..., Any], /, *args: Any, **kwargs: Any) -> Any:
        self.calls += 1
        n = self.calls
        if n in self.raise_at:
            self.raised.append(n)
            raise ray.exceptions.RayError(
                f"injected fragment-writer death #{n} (graceful-degradation test)"
            )
        if n in self.short_at:
            # args == (uri, batches, ...); truncate the batch iterator's tail rows.
            self.shorted.append(n)
            uri, batches, *rest = args
            short = _drop_tail_rows(batches, self.short_rows)
            return self.inner.write(fn, uri, short, *rest, **kwargs)
        return self.inner.write(fn, *args, **kwargs)


_FRAGMENT_WRITER_FAULT_ENV = "GENEVA_FAULT_FRAGMENT_WRITER"


def _parse_fragment_writer_fault(spec: str) -> FlakyFragmentFileWriter:
    """Parse ``mode:occ[,occ...][:rows]`` where ``mode`` is ``raise`` or ``short``
    (truncate the fragment's last ``rows`` rows, default 1). E.g. ``raise:1``,
    ``short:1,2:3``. Raises ``ValueError`` on a malformed spec."""
    parts = spec.split(":")
    if len(parts) not in (2, 3):
        raise ValueError(f"expected 'mode:occ[:rows]', got {spec!r}")
    mode, occ_csv = parts[0].strip(), parts[1].strip()
    if mode not in ("raise", "short"):
        raise ValueError(f"bad mode {mode!r} (want raise/short)")
    occs = frozenset(int(x) for x in occ_csv.split(",") if x.strip())
    if not occs:
        raise ValueError(f"no occurrences in {occ_csv!r}")
    short_rows = int(parts[2]) if len(parts) == 3 else 1
    if mode == "short":
        return FlakyFragmentFileWriter(short_at=occs, short_rows=short_rows)
    return FlakyFragmentFileWriter(raise_at=occs)


def install_fragment_writer_fault_from_env() -> FlakyFragmentFileWriter | None:
    """Install a ``FlakyFragmentFileWriter`` from ``GENEVA_FAULT_FRAGMENT_WRITER``
    (no-op if unset; malformed spec logged and ignored)."""
    spec = os.environ.get(_FRAGMENT_WRITER_FAULT_ENV, "").strip()
    if not spec:
        return None
    try:
        writer = _parse_fragment_writer_fault(spec)
    except ValueError as e:
        _LOG.warning(
            "ignoring malformed %s=%r: %s", _FRAGMENT_WRITER_FAULT_ENV, spec, e
        )
        return None
    set_fragment_file_writer(writer)
    _LOG.warning(
        "INSTALLED fragment-writer fault from %s=%r", _FRAGMENT_WRITER_FAULT_ENV, spec
    )
    return writer


# --- field-metadata writer --------------------------------------------------


class FlakyFieldMetadataWriter:
    """Field-metadata writer that faults selected watermark writes, for tests.

    Counts ``update`` calls 1-based. By counted index: ``raise_at`` raises
    ``InjectedFaultError``; ``drop_at`` skips the write (watermark not advanced);
    ``raise_after`` lands the write then raises.
    """

    def __init__(
        self,
        inner: FieldMetadataWriter | None = None,
        *,
        drop_at: Collection[int] = (),
        raise_at: Collection[int] = (),
        raise_after: Collection[int] = (),
    ) -> None:
        self.inner: FieldMetadataWriter = inner or LanceFieldMetadataWriter()
        self.drop_at = frozenset(drop_at)
        self.raise_at = frozenset(raise_at)
        self.raise_after = frozenset(raise_after)
        self.calls = 0
        self.dropped: list[int] = []
        self.raised: list[int] = []
        self.raised_after: list[int] = []

    def update(self, ltbl: Any, *updates: Any) -> Any:
        self.calls += 1
        n = self.calls
        if n in self.raise_at:
            self.raised.append(n)
            raise InjectedFaultError(
                f"injected worker death at field-metadata write #{n}"
            )
        if n in self.drop_at:
            self.dropped.append(n)
            return None
        if n in self.raise_after:
            self.inner.update(ltbl, *updates)
            self.raised_after.append(n)
            raise InjectedFaultError(
                f"injected worker death AFTER field-metadata write #{n} landed"
            )
        return self.inner.update(ltbl, *updates)


_FIELD_METADATA_FAULT_ENV = "GENEVA_FAULT_FIELD_METADATA"


def _parse_field_metadata_fault(spec: str) -> FlakyFieldMetadataWriter:
    """Parse ``mode:occ[,occ...]`` (e.g. ``drop:1``); one op (the watermark write), so
    no op name. ``mode`` is drop/raise/raise_after, occurrences 1-based. Raises
    ``ValueError`` if malformed."""
    parts = spec.split(":")
    if len(parts) != 2:
        raise ValueError(f"expected 'mode:occ', got {spec!r}")
    mode, occ_csv = (p.strip() for p in parts)
    if mode not in ("drop", "raise", "raise_after"):
        raise ValueError(f"bad mode {mode!r} (want drop/raise/raise_after)")
    occs = frozenset(int(x) for x in occ_csv.split(",") if x.strip())
    if not occs:
        raise ValueError(f"no occurrences in {occ_csv!r}")
    return FlakyFieldMetadataWriter(
        drop_at=occs if mode == "drop" else (),
        raise_at=occs if mode == "raise" else (),
        raise_after=occs if mode == "raise_after" else (),
    )


def install_field_metadata_fault_from_env() -> FlakyFieldMetadataWriter | None:
    """Install a ``FlakyFieldMetadataWriter`` from ``GENEVA_FAULT_FIELD_METADATA``
    (no-op if unset; malformed spec logged and ignored)."""
    spec = os.environ.get(_FIELD_METADATA_FAULT_ENV, "").strip()
    if not spec:
        return None
    try:
        writer = _parse_field_metadata_fault(spec)
    except ValueError as e:
        _LOG.warning("ignoring malformed %s=%r: %s", _FIELD_METADATA_FAULT_ENV, spec, e)
        return None
    set_field_metadata_writer(writer)
    _LOG.warning(
        "INSTALLED field-metadata fault from %s=%r", _FIELD_METADATA_FAULT_ENV, spec
    )
    return writer


# --- checkpoint store -------------------------------------------------------


class CheckpointFaultPolicy:
    """Shared fault state for a process's wrapped checkpoint stores.

    Shared across every store the wrapper produces, so occurrence counts are
    per-process. ``ops`` selects operations to fault (``set`` = ``__setitem__``,
    ``delete``, ``purge``, ``list`` = ``list_keys``, ``mismatch`` = the
    ``has_*_mismatch`` reprocess probes); ``key_match`` (optional substring) narrows
    by key.

    The read-side ops model a real path, not a storage anomaly: the hierarchical
    store's identity sidecar write is best-effort (a swallowed ``OSError``) and a
    missing sidecar is negatively cached for the process, so a whole checkpoint
    directory can genuinely become invisible -- LISTs return nothing and the mismatch
    probes report "no reprocess needed" over data that does mismatch.
    """

    def __init__(
        self,
        *,
        ops: Collection[str] | None = None,
        drop_at: Collection[int] = (),
        raise_at: Collection[int] = (),
        short_at: Collection[int] = (),
        short_rows: int = 1,
        key_match: str | None = None,
    ) -> None:
        self.ops = frozenset(ops) if ops is not None else None
        self.drop_at = frozenset(drop_at)
        self.raise_at = frozenset(raise_at)
        # ``short_at`` (set op only) stores a batch truncated by ``short_rows`` rows.
        self.short_at = frozenset(short_at)
        self.short_rows = short_rows
        self.key_match = key_match
        self.calls = 0
        self.dropped: list[tuple[str, str]] = []
        self.raised: list[tuple[str, str]] = []
        self.shorted: list[tuple[str, str]] = []

    def decide(self, op: str, key: str) -> str | None:
        """Return ``"raise"`` / ``"drop"`` / ``"short"`` for a matched op, else None."""
        if self.ops is not None and op not in self.ops:
            return None
        if self.key_match is not None and self.key_match not in key:
            return None
        self.calls += 1
        n = self.calls
        if n in self.raise_at:
            self.raised.append((op, key))
            return "raise"
        if n in self.drop_at:
            self.dropped.append((op, key))
            return "drop"
        if n in self.short_at:
            self.shorted.append((op, key))
            return "short"
        return None


class FlakyCheckpointStore(CheckpointStore):
    """Checkpoint store that faults selected mutations, for worker-death tests.

    Wraps a real store and consults a shared :class:`CheckpointFaultPolicy` on each
    mutation: ``raise_at`` raises, ``drop_at`` skips it returning as if it succeeded,
    ``short_at`` (set only) writes a truncated batch. Reads and non-faulted calls
    delegate to the inner store.
    """

    def __init__(self, inner: CheckpointStore, policy: CheckpointFaultPolicy) -> None:
        self._inner = inner
        self._policy = policy

    # --- faulted mutations ---
    def __setitem__(self, key: str, value: pa.RecordBatch) -> None:
        decision = self._policy.decide("set", key)
        if decision == "raise":
            raise InjectedFaultError(f"injected worker death at checkpoint set {key!r}")
        if decision == "drop":
            return
        if decision == "short":
            # Store a partial batch with the last ``short_rows`` rows dropped.
            keep = max(0, value.num_rows - self._policy.short_rows)
            self._inner[key] = value.slice(0, keep)
            return
        self._inner[key] = value

    def delete(self, key: str) -> None:
        decision = self._policy.decide("delete", key)
        if decision == "raise":
            raise InjectedFaultError(
                f"injected worker death at checkpoint delete {key!r}"
            )
        if decision == "drop":
            return
        self._inner.delete(key)

    def purge(self, key: str) -> None:
        decision = self._policy.decide("purge", key)
        if decision == "raise":
            raise InjectedFaultError(
                f"injected worker death at checkpoint purge {key!r}"
            )
        if decision == "drop":
            return
        self._inner.purge(key)

    def purge_many(self, keys: list[str]) -> None:
        # Decide once for the batch, keyed on the first key.
        decision = self._policy.decide("purge", keys[0] if keys else "")
        if decision == "raise":
            raise InjectedFaultError("injected worker death at checkpoint purge_many")
        if decision == "drop":
            return
        self._inner.purge_many(keys)

    # --- faulted reads (the invisible-directory path; see the policy docstring) ---
    def list_keys(self, prefix: str = "") -> Iterator[str]:
        decision = self._policy.decide("list", prefix)
        if decision == "raise":
            raise InjectedFaultError(
                f"injected failure at checkpoint list_keys {prefix!r}"
            )
        if decision == "drop":
            return iter(())  # the directory is invisible (lost identity sidecar)
        return self._inner.list_keys(prefix)

    def has_udf_version_mismatch(self, column: str, current_udf_version: str) -> bool:
        decision = self._policy.decide("mismatch", column)
        if decision == "raise":
            raise InjectedFaultError(
                f"injected failure at udf-version mismatch probe for {column!r}"
            )
        if decision == "drop":
            return False  # an empty LIST reports no mismatch: no reprocess happens
        return self._inner.has_udf_version_mismatch(column, current_udf_version)

    # --- delegated reads / structure (preserve inner behavior) ---
    def __contains__(self, item: str) -> bool:
        return item in self._inner

    def __getitem__(self, item: str) -> pa.RecordBatch:
        return self._inner[item]

    def read_range(self, key: str, start: int, num_rows: int) -> pa.RecordBatch:
        # Keep GEN-780 writer recovery on the inner store's true bounded-read
        # path; the base-class fallback would materialize the whole checkpoint.
        return self._inner.read_range(key, start, num_rows)

    def uri(self) -> str:
        return self._inner.uri()

    def delete_prefix(self, prefix: str) -> int:
        return self._inner.delete_prefix(prefix)

    def has_srcfiles_hash_mismatch(
        self, column: str, current_srcfiles_hash: str
    ) -> bool:
        decision = self._policy.decide("mismatch", column)
        if decision == "raise":
            raise InjectedFaultError(
                f"injected failure at srcfiles mismatch probe for {column!r}"
            )
        if decision == "drop":
            return False  # an empty LIST reports no mismatch: no reprocess happens
        return self._inner.has_srcfiles_hash_mismatch(column, current_srcfiles_hash)


def flaky_checkpoint_wrap(
    policy: CheckpointFaultPolicy,
) -> Callable[[CheckpointStore], CheckpointStore]:
    """Wrapper that wraps every created store in a :class:`FlakyCheckpointStore`
    sharing ``policy``."""

    def _wrap(store: CheckpointStore) -> CheckpointStore:
        # Never double-wrap (from_uri and make() can both run for one store).
        if isinstance(store, FlakyCheckpointStore):
            return store
        return FlakyCheckpointStore(store, policy)

    return _wrap


_CHECKPOINT_FAULT_ENV = "GENEVA_FAULT_CHECKPOINT"


def _parse_checkpoint_fault(spec: str) -> CheckpointFaultPolicy:
    """Parse ``op:mode:occ[,occ...]`` (e.g. ``set:drop:1``); op is set/delete/purge,
    mode is drop/raise/short (short applies to set only)."""
    parts = spec.split(":")
    if len(parts) != 3:
        raise ValueError(f"expected 'op:mode:occ', got {spec!r}")
    op, mode, occ_csv = (p.strip() for p in parts)
    if op not in ("set", "delete", "purge"):
        raise ValueError(f"bad op {op!r} (want set/delete/purge)")
    if mode not in ("drop", "raise", "short"):
        raise ValueError(f"bad mode {mode!r} (want drop/raise/short)")
    if mode == "short" and op != "set":
        raise ValueError(f"mode 'short' only applies to op 'set', got {op!r}")
    occs = frozenset(int(x) for x in occ_csv.split(",") if x.strip())
    if not occs:
        raise ValueError(f"no occurrences in {occ_csv!r}")
    return CheckpointFaultPolicy(
        ops={op},
        drop_at=occs if mode == "drop" else (),
        raise_at=occs if mode == "raise" else (),
        short_at=occs if mode == "short" else (),
    )


def install_checkpoint_fault_from_env() -> CheckpointFaultPolicy | None:
    """Install a checkpoint fault from ``GENEVA_FAULT_CHECKPOINT`` if set. No-op when
    unset; a malformed spec is logged and ignored (never break a normal import)."""
    spec = os.environ.get(_CHECKPOINT_FAULT_ENV, "").strip()
    if not spec:
        return None
    try:
        policy = _parse_checkpoint_fault(spec)
    except ValueError as e:
        _LOG.warning("ignoring malformed %s=%r: %s", _CHECKPOINT_FAULT_ENV, spec, e)
        return None
    set_checkpoint_store_wrap(flaky_checkpoint_wrap(policy))
    _LOG.warning("INSTALLED checkpoint fault from %s=%r", _CHECKPOINT_FAULT_ENV, spec)
    return policy


# --- the cross-process entry point -----------------------------------------------


def install_all_from_env() -> None:
    """Install every ``GENEVA_FAULT_*`` fault set in the environment.

    The cross-process bootstrap: a real-Ray worker runs it (from a ``sitecustomize`` in
    the worker image) before its first task. Each installer is a no-op when its env var
    is unset, so calling them all is safe.
    """
    install_committer_fault_from_env()
    install_table_writer_fault_from_env()
    install_fragment_writer_fault_from_env()
    install_field_metadata_fault_from_env()
    install_checkpoint_fault_from_env()
