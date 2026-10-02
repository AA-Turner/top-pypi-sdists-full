# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""Type stubs for the compiled ``kcl_rs._native`` extension module.

The classes below are implemented in Rust (PyO3); this stub describes their
Python-visible surface. Instances of every class except :class:`Scheduler` are
created by the runtime and handed to your callbacks — they cannot be usefully
constructed from Python.

Importing this module installs a default ``tracing`` subscriber (``WARN`` and
above, written to stderr, overridable via the ``RUST_LOG`` env var, e.g.
``RUST_LOG=kcl=debug``) so that core log output — most importantly retrieval
and lifecycle failure diagnostics — is visible by default instead of being
silently dropped. It never overrides an existing global subscriber.
"""

from collections.abc import Sequence
from datetime import datetime
from typing import Callable, Literal, Protocol, Union, final

__all__ = [
    "InitializeInput",
    "ProcessRecordsInput",
    "LeaseLostInput",
    "ShardEndedInput",
    "ShutdownRequestedInput",
    "Record",
    "Checkpointer",
    "PreparedCheckpointer",
    "CheckpointError",
    "Scheduler",
]

class _ShardRecordProcessor(Protocol):
    """Structural type of a record processor (see ``RecordProcessorBase``).

    Any object with the five lifecycle methods qualifies; subclassing
    :class:`kcl_rs.RecordProcessorBase` is the usual way to get one.
    """

    def initialize(self, initialize_input: InitializeInput) -> None: ...
    def process_records(self, process_records_input: ProcessRecordsInput) -> None: ...
    def lease_lost(self, lease_lost_input: LeaseLostInput) -> None: ...
    def shard_ended(self, shard_ended_input: ShardEndedInput) -> None: ...
    def shutdown_requested(
        self, shutdown_requested_input: ShutdownRequestedInput
    ) -> None: ...

class _ShardRecordProcessorFactory(Protocol):
    """An object with a ``shard_record_processor()`` factory method."""

    def shard_record_processor(self) -> _ShardRecordProcessor: ...

_RecordProcessorFactory = Union[
    Callable[[], _ShardRecordProcessor],
    _ShardRecordProcessorFactory,
]

class CheckpointError(Exception):
    """Raised when a checkpoint operation fails.

    The exception's :attr:`value` attribute (and ``str(e)``) is the Java-style
    error name, e.g. ``"ShutdownException"``, ``"ThrottlingException"``,
    ``"InvalidStateException"``, ``"KinesisClientLibDependencyException"``.
    Mirrors ``amazon_kclpy.kcl.CheckpointError``, so retry logic like
    ``if e.value == "ThrottlingException"`` keeps working.
    """

    value: str

@final
class Record:
    """A single Kinesis data record delivered to ``process_records``.

    Mirrors ``amazon_kclpy.messages.Record``. Unlike the multilang-daemon
    variant (which delivered base64 text), :attr:`data` is already the raw
    decoded ``bytes`` — :attr:`data` and :attr:`binary_data` are equivalent.
    """

    @property
    def sequence_number(self) -> str | None:
        """The sequence number of this record."""

    @property
    def sub_sequence_number(self) -> int:
        """The sub-sequence number (0 unless this is a de-aggregated KPL record)."""

    @property
    def approximate_arrival_timestamp(self) -> datetime | None:
        """The approximate server-side arrival timestamp (UTC), or ``None``."""

    @property
    def timestamp_millis(self) -> int | None:
        """Approximate arrival time in milliseconds since the Unix epoch, or ``None``."""

    @property
    def partition_key(self) -> str | None:
        """The partition key of this record."""

    @property
    def data(self) -> bytes:
        """The raw record payload."""

    @property
    def binary_data(self) -> bytes:
        """Alias for :attr:`data` — the raw decoded payload."""

@final
class Checkpointer:
    """Records progress for a shard; handed to ``process_records`` /
    ``shard_ended`` / ``shutdown_requested`` callbacks.

    Mirrors ``amazon_kclpy.kcl.Checkpointer``. All methods run the synchronous
    Rust checkpointer with the GIL released.
    """

    def checkpoint(
        self,
        sequence_number: str | None = None,
        sub_sequence_number: int | None = None,
    ) -> None:
        """Checkpoint the record processor's progress.

        With no arguments, checkpoints at the last record delivered to this
        processor; with ``sequence_number`` (and optionally
        ``sub_sequence_number``) checkpoints at that exact position.

        :raises CheckpointError: on failure; ``e.value`` is the Java-style
            exception name (e.g. ``"ShutdownException"``,
            ``"ThrottlingException"``).
        """

    def prepare_checkpoint(
        self,
        sequence_number: str | None = None,
        sub_sequence_number: int | None = None,
    ) -> PreparedCheckpointer:
        """Durably record a *pending* (two-phase) checkpoint.

        The returned :class:`PreparedCheckpointer`'s
        :meth:`~PreparedCheckpointer.checkpoint` commits it — enabling
        idempotent side effects across failover. Argument handling matches
        :meth:`checkpoint`.

        :raises CheckpointError: on failure; ``e.value`` is the Java-style
            exception name.
        """

@final
class PreparedCheckpointer:
    """A pending two-phase checkpoint returned by
    :meth:`Checkpointer.prepare_checkpoint`.

    Mirrors the Java KCL's ``IPreparedCheckpointer``.
    """

    def checkpoint(self) -> None:
        """Commit the pending checkpoint.

        :raises CheckpointError: on failure; ``e.value`` is the Java-style
            exception name.
        """

    @property
    def pending_checkpoint(self) -> tuple[str, int]:
        """The pending position as ``(sequence_number, sub_sequence_number)``."""

@final
class InitializeInput:
    """Parameters to ``RecordProcessorBase.initialize``.

    Mirrors ``amazon_kclpy.messages.InitializeInput``.
    """

    @property
    def shard_id(self) -> str | None:
        """The shard this processor is assigned to."""

    @property
    def sequence_number(self) -> str | None:
        """The last checkpointed sequence number, or ``None`` on a fresh shard."""

    @property
    def sub_sequence_number(self) -> int | None:
        """The last checkpointed sub-sequence number, or ``None``."""

@final
class ProcessRecordsInput:
    """Parameters to ``RecordProcessorBase.process_records``.

    Mirrors ``amazon_kclpy.messages.ProcessRecordsInput``.
    """

    @property
    def records(self) -> list[Record]:
        """The batch of records to process."""

    @property
    def millis_behind_latest(self) -> int | None:
        """How far behind the tip of the stream this batch was, in milliseconds."""

    @property
    def checkpointer(self) -> Checkpointer:
        """Checkpointer for recording progress through this shard."""

@final
class LeaseLostInput:
    """Parameters to ``RecordProcessorBase.lease_lost`` (currently empty).

    Mirrors ``amazon_kclpy.messages.LeaseLostInput``.
    """

@final
class ShardEndedInput:
    """Parameters to ``RecordProcessorBase.shard_ended``.

    Mirrors ``amazon_kclpy.messages.ShardEndedInput``.
    """

    @property
    def checkpointer(self) -> Checkpointer:
        """Checkpointer that **must** be invoked to complete the shard."""

@final
class ShutdownRequestedInput:
    """Parameters to ``RecordProcessorBase.shutdown_requested``.

    Mirrors ``amazon_kclpy.messages.ShutdownRequestedInput``.
    """

    @property
    def checkpointer(self) -> Checkpointer:
        """Checkpointer for a final checkpoint before shutdown."""

@final
class Scheduler:
    """The Python control surface for the Rust KCL.

    Construct it with the stream/application/worker identity and a
    record-processor factory, then call :meth:`start` (background) or
    :meth:`run` (blocking), and :meth:`shutdown` to stop.

    The Rust KCL runs on its own tokio runtime on background threads with the
    GIL released; record-processor callbacks re-acquire the GIL only for the
    duration of each call. Construction does no network I/O.
    """

    def __new__(
        cls,
        stream_name: str | None = None,
        application_name: str = ...,
        record_processor_factory: _RecordProcessorFactory | None = None,
        worker_identifier: str | None = None,
        region: str | None = None,
        endpoint_url: str | None = None,
        initial_position: Literal["LATEST", "TRIM_HORIZON", "AT_TIMESTAMP"] = ...,
        timestamp: float | datetime | None = None,
        stream_identifiers: Sequence[str] | None = None,
        access_key_id: str | None = None,
        secret_access_key: str | None = None,
        session_token: str | None = None,
        retrieval_mode: Literal["FANOUT", "POLLING"] = ...,
        max_records: int | None = None,
        idle_time_between_reads_millis: int | None = None,
        shard_sync_interval_millis: int | None = None,
    ) -> Scheduler:
        """Capture configuration; no network I/O, no runtime started.

        :param stream_name: the Kinesis stream to consume (single-stream mode).
            Mutually exclusive with ``stream_identifiers``; exactly one of the
            two must be provided.
        :param application_name: the KCL application name (also the default
            lease-table name and CloudWatch namespace). Required.
        :param record_processor_factory: a callable returning a fresh record
            processor per shard (e.g. a ``RecordProcessorBase`` subclass
            itself), or an object with a ``shard_record_processor()`` method.
            Required.
        :param worker_identifier: unique id for this worker (default: generated).
        :param region: AWS region, e.g. ``"us-east-1"``.
        :param endpoint_url: override endpoint, e.g. ``"http://localhost:4566"``
            for LocalStack.
        :param initial_position: where to start on a shard with no checkpoint:
            ``"LATEST"`` (default), ``"TRIM_HORIZON"``, or ``"AT_TIMESTAMP"``
            (which requires ``timestamp``).
        :param timestamp: only for ``initial_position="AT_TIMESTAMP"``: epoch
            seconds (``int``/``float``) or a ``datetime`` (naive values are
            interpreted as UTC).
        :param stream_identifiers: multi-stream mode: serialized identifiers of
            the form ``"accountId:streamName:creationEpoch"``.
        :param access_key_id: explicit static credential; overrides the default
            credential chain. Must be given with ``secret_access_key``.
        :param secret_access_key: explicit static credential; must be given with
            ``access_key_id``.
        :param session_token: explicit session token; requires both
            ``access_key_id`` and ``secret_access_key``. When no explicit
            credentials are given, the standard AWS credential chain (env vars,
            profile, IMDS, …) is used.
        :param retrieval_mode: ``"FANOUT"`` (default) or ``"POLLING"``,
            case-insensitive. Fan-out subscribes via ``SubscribeToShard`` (EFO);
            polling uses classic ``GetRecords``. Unlike the Java multilang
            daemon's ``RetrievalMode``, there is no ``"DEFAULT"`` auto-detect
            variant.
        :param max_records: polling-only; caps records per ``GetRecords`` call
            (default 10000, and the max — larger values raise ``ValueError``).
            Requires ``retrieval_mode="POLLING"``.
        :param idle_time_between_reads_millis: polling-only; delay between
            ``GetRecords`` calls (default 1500ms; clamped up to a 200ms floor).
            Requires ``retrieval_mode="POLLING"``.
        :param shard_sync_interval_millis: interval between periodic shard syncs
            (default 60000ms). Applies to both retrieval modes.
        :raises ValueError: on missing/conflicting arguments, a bad
            ``timestamp``, an unrecognized ``retrieval_mode``, ``max_records``/
            ``idle_time_between_reads_millis`` without ``retrieval_mode="POLLING"``,
            or ``max_records`` above 10000.
        """

    def start(self) -> None:
        """Start the scheduler in the background and return immediately.

        Builds the tokio runtime, AWS clients and the core scheduler (GIL
        released), then runs the KCL on its own threads. Call :meth:`shutdown`
        to stop.

        :raises RuntimeError: if already started, or if the build fails.
        """

    def run(self) -> None:
        """Build and drive the scheduler, blocking until shutdown.

        Blocks the calling Python thread until :meth:`shutdown` is called (from
        another thread) or a signal arrives. Ctrl-C (``KeyboardInterrupt``)
        triggers a graceful shutdown and is then re-raised.

        :raises RuntimeError: if already started, if the build fails, or if the
            scheduler run loop crashed.
        """

    def shutdown(self) -> None:
        """Initiate a graceful shutdown and block until the scheduler stops.

        Works for both :meth:`start` and :meth:`run` launches and may be called
        from any thread. A no-op if the scheduler was never started.

        :raises RuntimeError: if the run loop had crashed.
        """
