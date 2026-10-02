# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
``kcl_rs`` — Python bindings for the Rust port of the Amazon Kinesis
Client Library.

The public surface mirrors ``amazon_kclpy``:

* :class:`RecordProcessorBase` — subclass this and implement ``initialize``,
  ``process_records``, ``lease_lost``, ``shard_ended``, ``shutdown_requested``.
* The ``*Input`` message types and :class:`Record` passed to those callbacks.
* :class:`Checkpointer` / :class:`CheckpointError` for recording progress.
* :class:`Scheduler` — the control surface: construct it with the stream/app
  identity and a record-processor factory, then ``start()`` (background) or
  ``run()`` (blocking), and ``shutdown()`` to stop.

Runtime / GIL model: the Rust KCL runs on its own tokio runtime, on background
threads, without holding the GIL. Callbacks acquire the GIL only transiently.

Example::

    from kcl_rs import Scheduler, RecordProcessorBase

    class MyProcessor(RecordProcessorBase):
        def initialize(self, i): ...
        def process_records(self, p):
            for r in p.records:
                handle(r.binary_data)
            p.checkpointer.checkpoint()
        def lease_lost(self, l): ...
        def shard_ended(self, s): s.checkpointer.checkpoint()
        def shutdown_requested(self, s): s.checkpointer.checkpoint()

    scheduler = Scheduler(
        stream_name="my-stream",
        application_name="my-app",
        record_processor_factory=MyProcessor,   # a callable returning a processor
        region="us-east-1",
        endpoint_url="http://localhost:4566",   # LocalStack
        access_key_id="test", secret_access_key="test",   # or export the env vars
        initial_position="TRIM_HORIZON",
    )
    scheduler.run()   # blocks until shutdown() is called (e.g. from a signal)

Initial position:
    ``initial_position`` accepts ``"LATEST"`` (default), ``"TRIM_HORIZON"``, or
    ``"AT_TIMESTAMP"``. For ``"AT_TIMESTAMP"`` also pass a ``timestamp`` — either
    epoch seconds (``int``/``float``) or a ``datetime.datetime`` (naive datetimes
    are treated as UTC)::

        Scheduler(..., initial_position="AT_TIMESTAMP",
                  timestamp=datetime(2024, 1, 1, tzinfo=timezone.utc))

Multi-stream:
    Instead of ``stream_name``, pass ``stream_identifiers`` — a list of serialized
    multi-stream identifiers ``"accountId:streamName:creationEpoch"`` — to consume
    several streams with one worker::

        Scheduler(
            stream_identifiers=[
                "123456789012:orders:1700000000",
                "123456789012:events:1700000001",
            ],
            application_name="my-app",
            record_processor_factory=MyProcessor,
        )

Retrieval mode:
    ``retrieval_mode`` selects fan-out (default) or classic polling retrieval;
    ``max_records``/``idle_time_between_reads_millis`` are polling-only knobs::

        Scheduler(..., retrieval_mode="POLLING", max_records=500)

Prepared (two-phase) checkpoints:
    ``checkpointer.prepare_checkpoint(sequence_number=None, sub_sequence_number=None)``
    durably records a *pending* checkpoint and returns a :class:`PreparedCheckpointer`
    whose ``.checkpoint()`` commits it — enabling idempotent side effects across
    failover.
"""

# Re-export the native classes from the compiled Rust extension.
from kcl_rs._native import (  # noqa: F401
    CheckpointError,
    Checkpointer,
    InitializeInput,
    LeaseLostInput,
    PreparedCheckpointer,
    ProcessRecordsInput,
    Record,
    Scheduler,
    ShardEndedInput,
    ShutdownRequestedInput,
)

# The pure-Python abstract base users subclass.
from kcl_rs.processor import RecordProcessorBase  # noqa: F401

__all__ = [
    "CheckpointError",
    "Checkpointer",
    "InitializeInput",
    "LeaseLostInput",
    "PreparedCheckpointer",
    "ProcessRecordsInput",
    "Record",
    "RecordProcessorBase",
    "Scheduler",
    "ShardEndedInput",
    "ShutdownRequestedInput",
]
