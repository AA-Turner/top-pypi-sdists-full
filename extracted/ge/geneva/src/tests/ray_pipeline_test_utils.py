# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

"""Focused helpers for Ray pipeline writer internals tests."""

from __future__ import annotations

from contextlib import contextmanager
from dataclasses import dataclass, field
from typing import TYPE_CHECKING, Any
from unittest.mock import MagicMock, patch

import attrs

from geneva.runners.ray.pipeline import (
    FragmentWriterManager,
    FragmentWriterSession,
)
from geneva.runners.ray.writer import FragmentWriteResult

if TYPE_CHECKING:
    from collections.abc import Iterator


def _attrs_default(attribute: attrs.Attribute[Any], instance: Any) -> Any:
    default = attribute.default
    if isinstance(default, attrs.Factory):
        if default.takes_self:
            return default.factory(instance)
        return default.factory()
    return default


@dataclass
class MockedRayWriterHarness:
    queues: list[MagicMock] = field(default_factory=list)
    actors: list[MagicMock] = field(default_factory=list)
    write_futures: list[object] = field(default_factory=list)
    writer: MagicMock = field(default_factory=MagicMock)
    queue_cls: MagicMock | None = field(default=None, init=False)
    # Items enqueued per queue, in submission order, across both the per-item
    # and batched paths.
    enqueued: list[list[tuple[int, Any, int]]] = field(default_factory=list, init=False)

    def __post_init__(self) -> None:
        self.writer.options.return_value.remote.side_effect = self.make_actor

    def make_queue(self, *args: Any, **kwargs: Any) -> MagicMock:
        queue = MagicMock()
        queue.actor = MagicMock()
        items: list[tuple[int, Any, int]] = []

        def _put(item: tuple[int, Any, int]) -> object:
            items.append(item)
            return object()

        def _put_batch(batch: list[tuple[int, Any, int]]) -> object:
            items.extend(batch)
            return object()

        queue.actor.put_nowait.remote = MagicMock(side_effect=_put)
        queue.actor.put_nowait_batch.remote = MagicMock(side_effect=_put_batch)
        self.queues.append(queue)
        self.enqueued.append(items)
        return queue

    def make_actor(self, *args: Any, **kwargs: Any) -> MagicMock:
        actor = MagicMock()
        write_future = object()
        actor.write.remote.return_value = write_future
        self.actors.append(actor)
        self.write_futures.append(write_future)
        return actor

    @contextmanager
    def patch(self) -> Iterator[MockedRayWriterHarness]:
        with (
            patch(
                "geneva.runners.ray.pipeline.ray.util.queue.Queue",
                side_effect=self.make_queue,
            ) as queue_cls,
            patch("geneva.runners.ray.pipeline.FragmentWriter", self.writer),
        ):
            self.queue_cls = queue_cls
            yield self

    def put_args(self, queue_index: int = 0) -> list[tuple[int, Any, int]]:
        """Effective enqueue sequence, whether sent per-item or batched."""
        return list(self.enqueued[queue_index])

    def batch_calls(self, queue_index: int = 0) -> list[list[tuple[int, Any, int]]]:
        """Each ``put_nowait_batch`` submission, for asserting the batched shape."""
        return [
            call.args[0]
            for call in self.queues[
                queue_index
            ].actor.put_nowait_batch.remote.call_args_list
        ]


def make_fragment_writer_session(
    *,
    frag_id: int = 0,
    ds_uri: str = "memory://test",
    output_columns: list[str] | None = None,
    checkpoint_store: Any | None = None,
    where: str | None = None,
    **kwargs: Any,
) -> FragmentWriterSession:
    return FragmentWriterSession(
        frag_id=frag_id,
        ds_uri=ds_uri,
        output_columns=output_columns or ["b"],
        checkpoint_store=checkpoint_store
        if checkpoint_store is not None
        else MagicMock(),
        where=where,
        **kwargs,
    )


def make_fragment_writer_manager(
    *,
    sessions: dict[int, FragmentWriterSession] | None = None,
    failed_fragments: dict[int, str] | None = None,
    commit_granularity: int = 1,
    expected_tasks: dict[int, int] | None = None,
    remaining_tasks: dict[int, int] | None = None,
    output_columns: list[str] | None = None,
    job_tracker: Any | None = None,
    **overrides: Any,
) -> FragmentWriterManager:
    manager = FragmentWriterManager.__new__(FragmentWriterManager)
    seeded = {
        "dst_read_version": 0,
        "ds_uri": "memory://test",
        "map_task": MagicMock(),
        "checkpoint_store": MagicMock(),
        "where": None,
        "job_tracker": job_tracker,
        "commit_granularity": commit_granularity,
        "expected_tasks": expected_tasks if expected_tasks is not None else {},
        "sessions": sessions if sessions is not None else {},
        "remaining_tasks": (
            remaining_tasks
            if remaining_tasks is not None
            else dict(expected_tasks or {})
        ),
        "output_columns": output_columns or ["b"],
        "failed_fragments": failed_fragments if failed_fragments is not None else {},
    }
    seeded.update(overrides)

    for attribute in attrs.fields(FragmentWriterManager):
        if attribute.name in seeded:
            value = seeded.pop(attribute.name)
        elif attribute.default is attrs.NOTHING:
            continue
        else:
            value = _attrs_default(attribute, manager)
        setattr(manager, attribute.name, value)

    for name, value in seeded.items():
        setattr(manager, name, value)

    return manager


def attach_started_writer_future(
    sess: FragmentWriterSession,
    fut: object | None = None,
) -> object:
    future = fut if fut is not None else object()
    sess.queue = MagicMock()
    sess.actor = MagicMock()
    sess.inflight[future] = sess.frag_id
    return future


def make_fragment_write_result(
    *,
    frag_id: int,
    new_file: Any | None = None,
    rows_written: int | None = None,
    checkpoint_written: bool = False,
    fragment_checkpointing_ms: int = 0,
    buffer_sort_ms: int = 0,
    align_ms: int = 0,
    write_ms: int = 0,
    queue_wait_ms: int = 0,
    checkpoint_read_ms: int = 0,
    avg_batch_num_rows: int = 0,
    avg_batch_size: int = 0,
) -> FragmentWriteResult:
    if new_file is None:
        new_file = MagicMock()
        new_file.path = f"fragment-{frag_id}.lance"
    return FragmentWriteResult(
        frag_id=frag_id,
        new_file=new_file,
        rows_written=rows_written if rows_written is not None else frag_id + 10,
        checkpoint_written=checkpoint_written,
        fragment_checkpointing_ms=fragment_checkpointing_ms,
        buffer_sort_ms=buffer_sort_ms,
        align_ms=align_ms,
        write_ms=write_ms,
        queue_wait_ms=queue_wait_ms,
        checkpoint_read_ms=checkpoint_read_ms,
        avg_batch_num_rows=avg_batch_num_rows,
        avg_batch_size=avg_batch_size,
    )
