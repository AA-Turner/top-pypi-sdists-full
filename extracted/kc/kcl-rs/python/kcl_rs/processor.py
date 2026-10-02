# Copyright 2024 Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: Apache-2.0
"""
The v3 ``RecordProcessorBase`` abstract base class users subclass.

Mirrors ``amazon_kclpy.v3.processor.RecordProcessorBase``: each ``RecordProcessor``
processes a single shard through a lifecycle of ``initialize`` -> zero or more
``process_records`` -> one of ``lease_lost`` / ``shard_ended`` /
``shutdown_requested``.

Unlike ``amazon_kclpy`` (which spoke to a Java MultiLangDaemon over stdin/stdout),
these callbacks are invoked *directly* from the native Rust KCL: the Rust runtime
acquires the Python GIL only for the duration of each call. The input objects
(``InitializeInput``, ``ProcessRecordsInput``, ``LeaseLostInput``,
``ShardEndedInput``, ``ShutdownRequestedInput``) and the ``Checkpointer`` are the
native ``#[pyclass]`` types from ``kcl_rs._native``.
"""
from __future__ import annotations

import abc
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from kcl_rs._native import (
        InitializeInput,
        LeaseLostInput,
        ProcessRecordsInput,
        ShardEndedInput,
        ShutdownRequestedInput,
    )


class RecordProcessorBase(abc.ABC):
    """
    Base class for implementing a record processor. Each RecordProcessor processes
    a single shard in a stream.

    Subclass this and implement the five lifecycle methods. Pass a factory that
    returns fresh instances (e.g. the class itself, or an object with a
    ``shard_record_processor()`` method) to :class:`kcl_rs.Scheduler`.
    """

    #: Interface version. v3 mirrors amazon_kclpy's v3 RecordProcessorBase.
    version: int = 3

    @abc.abstractmethod
    def initialize(self, initialize_input: InitializeInput) -> None:
        """
        Called once before any records are delivered to this processor.

        :param kcl_rs.InitializeInput initialize_input: carries ``shard_id``,
            ``sequence_number`` (the last checkpoint, or ``None`` on a fresh shard)
            and ``sub_sequence_number``.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def process_records(self, process_records_input: ProcessRecordsInput) -> None:
        """
        Called whenever a batch of records is received.

        :param kcl_rs.ProcessRecordsInput process_records_input: carries the
            ``records`` (list of :class:`kcl_rs.Record`),
            ``millis_behind_latest`` and a ``checkpointer``
            (:class:`kcl_rs.Checkpointer`).
        """
        raise NotImplementedError

    @abc.abstractmethod
    def lease_lost(self, lease_lost_input: LeaseLostInput) -> None:
        """
        Called when the lease for this shard has been lost. After this returns the
        record processor is shut down; checkpointing is no longer possible.

        :param kcl_rs.LeaseLostInput lease_lost_input: currently empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def shard_ended(self, shard_ended_input: ShardEndedInput) -> None:
        """
        Called when the shard has been completely processed. You **must** call
        ``shard_ended_input.checkpointer.checkpoint()`` before returning, or the
        child shards will never make progress.

        :param kcl_rs.ShardEndedInput shard_ended_input: carries a
            ``checkpointer``.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def shutdown_requested(self, shutdown_requested_input: ShutdownRequestedInput) -> None:
        """
        Called when the scheduler is shutting down, while the lease is still held
        (so a final checkpoint is possible).

        :param kcl_rs.ShutdownRequestedInput shutdown_requested_input: carries
            a ``checkpointer``.
        """
        raise NotImplementedError
