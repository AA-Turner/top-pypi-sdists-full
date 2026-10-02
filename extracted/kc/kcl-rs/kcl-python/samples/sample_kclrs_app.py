#!/usr/bin/env python
# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
Sample record processor for the Rust-powered ``kcl_rs`` bindings.

Mirrors ``amazon-kinesis-client-python``'s ``samples/sample_kclpy_app.py``, but
instead of being launched by a Java MultiLangDaemon it constructs and drives the
KCL directly from Python via :class:`kcl_rs.Scheduler`.

Run against LocalStack (see the README / PORTING.md for the full setup)::

    # 1. Start LocalStack and create the stream:
    #    localstack start -d
    #    awslocal kinesis create-stream --stream-name my-stream --shard-count 1
    #
    # 2. Build + install the extension into a venv:
    #    uv venv && source .venv/bin/activate
    #    maturin develop -m kcl-python/Cargo.toml
    #
    # 3. Run this sample. There is no implicit credential fallback, so either
    #    export the standard env vars or pass --access-key-id/--secret-access-key:
    #    export AWS_ACCESS_KEY_ID=test AWS_SECRET_ACCESS_KEY=test
    #    python kcl-python/samples/sample_kclrs_app.py \
    #        --stream my-stream --app my-app --endpoint http://localhost:4566
    #    # (or: ... --endpoint http://localhost:4566 \
    #    #        --access-key-id test --secret-access-key test)

    # 4. Put some records (in another shell):
    #    awslocal kinesis put-record --stream-name my-stream \
    #        --partition-key pk --data "$(echo -n hello | base64)"
"""
from __future__ import annotations

import argparse
import sys

from kcl_rs import RecordProcessorBase, Scheduler, CheckpointError


class SampleRecordProcessor(RecordProcessorBase):
    """A RecordProcessor that logs each record and checkpoints periodically."""

    CHECKPOINT_RETRIES = 5

    def __init__(self) -> None:
        self._shard_id = None

    def log(self, message: str) -> None:
        sys.stderr.write(message + "\n")
        sys.stderr.flush()

    def initialize(self, initialize_input) -> None:
        self._shard_id = initialize_input.shard_id
        self.log(
            f"Initializing shard {initialize_input.shard_id} "
            f"at sequence {initialize_input.sequence_number}"
        )

    def checkpoint(self, checkpointer, sequence_number=None, sub_sequence_number=None) -> None:
        """Checkpoint with retries on retryable exceptions (mirrors amazon_kclpy)."""
        for n in range(self.CHECKPOINT_RETRIES):
            try:
                checkpointer.checkpoint(sequence_number, sub_sequence_number)
                return
            except CheckpointError as e:
                # e.value is the Java-style exception name (as in amazon_kclpy).
                value = e.value
                if value == "ShutdownException":
                    self.log("Encountered shutdown exception, skipping checkpoint")
                    return
                elif value == "ThrottlingException":
                    if n == self.CHECKPOINT_RETRIES - 1:
                        self.log(f"Failed to checkpoint after {n} attempts, giving up.")
                        return
                    self.log("Throttled while checkpointing, retrying.")
                elif value == "InvalidStateException":
                    self.log("KCL reported an invalid state while checkpointing.")
                else:
                    self.log(f"Error while checkpointing: {e}")

    def process_records(self, process_records_input) -> None:
        try:
            for record in process_records_input.records:
                data = record.binary_data
                seq = record.sequence_number
                key = record.partition_key
                self.log(
                    f"Record (shard={self._shard_id}, partition_key={key}, "
                    f"sequence={seq}, data_size={len(data)})"
                )
            # Checkpoint at the latest record in this batch.
            self.checkpoint(process_records_input.checkpointer)
        except Exception as e:  # noqa: BLE001 - mirror amazon_kclpy's broad catch
            self.log(f"Encountered an exception while processing records: {e}")

    def lease_lost(self, lease_lost_input) -> None:
        self.log(f"Lease lost for shard {self._shard_id}")

    def shard_ended(self, shard_ended_input) -> None:
        self.log(f"Shard {self._shard_id} ended; checkpointing.")
        self.checkpoint(shard_ended_input.checkpointer)

    def shutdown_requested(self, shutdown_requested_input) -> None:
        self.log("Shutdown requested; checkpointing.")
        self.checkpoint(shutdown_requested_input.checkpointer)


def main() -> None:
    parser = argparse.ArgumentParser(description="kcl_rs sample app")
    parser.add_argument("--stream", required=True, help="Kinesis stream name")
    parser.add_argument("--app", required=True, help="KCL application name")
    parser.add_argument("--region", default="us-east-1", help="AWS region")
    parser.add_argument(
        "--endpoint", default=None,
        help="Override endpoint URL (e.g. http://localhost:4566 for LocalStack)",
    )
    parser.add_argument(
        "--initial-position", default="TRIM_HORIZON",
        choices=["LATEST", "TRIM_HORIZON", "AT_TIMESTAMP"],
    )
    parser.add_argument(
        "--timestamp", default=None, type=float,
        help="Epoch seconds to start from; required with --initial-position AT_TIMESTAMP",
    )
    parser.add_argument("--worker-id", default=None, help="Unique worker id")
    parser.add_argument(
        "--access-key-id", default=None,
        help="Explicit AWS access key id (must be given with --secret-access-key); "
             "otherwise the standard credential chain (env vars, profile, IMDS, ...) is used",
    )
    parser.add_argument(
        "--secret-access-key", default=None,
        help="Explicit AWS secret access key (must be given with --access-key-id)",
    )
    parser.add_argument(
        "--session-token", default=None,
        help="Explicit AWS session token (requires --access-key-id and --secret-access-key)",
    )
    parser.add_argument(
        "--retrieval-mode", default="FANOUT", type=str.upper,
        choices=["FANOUT", "POLLING"],
        help="Retrieval mode: FANOUT (default, EFO SubscribeToShard) or "
             "POLLING (classic GetRecords)",
    )
    parser.add_argument(
        "--max-records", default=None, type=int,
        help="Polling-only: max records per GetRecords call (default 10000, max 10000); "
             "requires --retrieval-mode POLLING",
    )
    parser.add_argument(
        "--idle-time-between-reads-millis", default=None, type=int,
        help="Polling-only: delay between GetRecords calls in ms (default 1500, "
             "clamped up to a 200ms floor); requires --retrieval-mode POLLING",
    )
    args = parser.parse_args()

    if args.initial_position == "AT_TIMESTAMP" and args.timestamp is None:
        parser.error("--timestamp is required when --initial-position is AT_TIMESTAMP")

    scheduler = Scheduler(
        stream_name=args.stream,
        application_name=args.app,
        # The factory: the RecordProcessor class itself is callable and returns a
        # fresh instance per shard.
        record_processor_factory=SampleRecordProcessor,
        worker_identifier=args.worker_id,
        region=args.region,
        endpoint_url=args.endpoint,
        initial_position=args.initial_position,
        timestamp=args.timestamp,   # only consulted for AT_TIMESTAMP
        access_key_id=args.access_key_id,
        secret_access_key=args.secret_access_key,
        session_token=args.session_token,
        retrieval_mode=args.retrieval_mode,
        max_records=args.max_records,
        idle_time_between_reads_millis=args.idle_time_between_reads_millis,
    )

    sys.stderr.write(f"Starting KCL for stream={args.stream} app={args.app}\n")
    # run() blocks until shutdown. Ctrl-C (KeyboardInterrupt) triggers a
    # graceful shutdown inside run() and is then re-raised here. (Calling
    # scheduler.shutdown() from another thread also works.)
    try:
        scheduler.run()
    except KeyboardInterrupt:
        sys.stderr.write("\nInterrupted; scheduler stopped.\n")
    else:
        sys.stderr.write("Scheduler stopped.\n")


if __name__ == "__main__":
    main()
