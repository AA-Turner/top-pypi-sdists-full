# SPDX-License-Identifier: PROPRIETARY
# SPDX-FileCopyrightText: Copyright The Geneva Authors

from __future__ import annotations

from collections import deque
from typing import TYPE_CHECKING, Any

import attrs
import pyarrow as pa

from geneva.apply.task import ReadTask

if TYPE_CHECKING:
    from collections.abc import Iterator


@attrs.define
class AdaptiveCheckpointSizer:
    """Track and adjust checkpoint batch size based on observed durations."""

    max_size: int
    min_size: int = attrs.field(default=1)
    target_seconds: float = attrs.field(default=10.0)
    initial_size: int | None = attrs.field(default=None)
    _current_size: int = attrs.field(init=False, repr=False)

    def __attrs_post_init__(self) -> None:
        max_size = int(self.max_size)
        min_size = int(self.min_size)
        if min_size <= 0:
            min_size = 1
        if max_size < min_size:
            max_size = min_size
        self.max_size = max_size
        self.min_size = min_size
        initial = min_size if self.initial_size is None else int(self.initial_size)
        if initial < min_size:
            initial = min_size
        elif initial > max_size:
            initial = max_size
        self._current_size = initial

    @property
    def current_size(self) -> int:
        return self._current_size

    def record(self, *, duration_seconds: float, rows: int) -> None:
        """Update size from observed batch duration and row count.

        This implementation is intentionally simple and can be extended to use
        additional signals (e.g. EMA
        smoothing by recording the last N durations and rows)
        without changing the calling contract.
        """
        if duration_seconds <= 0 or rows <= 0:
            return

        desired = int(round((rows / duration_seconds) * self.target_seconds))
        if desired < self.min_size:
            desired = self.min_size
        elif desired > self.max_size:
            desired = self.max_size

        self._current_size = desired


@attrs.define
class BatchSizeTracker:
    """Queue of sizes used for each emitted batch."""

    _sizes: deque[int] = attrs.field(factory=deque, init=False)

    def record(self, size: int) -> None:
        self._sizes.append(int(size))

    def pop(self) -> int | None:
        if not self._sizes:
            return None
        return self._sizes.popleft()


@attrs.define
class AdaptiveReadTask(ReadTask):
    """ReadTask wrapper that slices max-size batches into adaptive checkpoints.

    ReadTasks are planned with a task size that effectively caps the maximum
    checkpoint size (`max_checkpoint_size`). This wrapper reads batches at that
    max size and then slices them into smaller `adaptive_checkpoint_size`
    batches based on the adaptive sizer. The max size also bounds the largest
    in-memory batch produced by `ReadTask.to_batches`, so it directly caps peak
    memory usage. The goal is to start with small checkpoints (faster
    proof-of-life and frequent progress) and grow them as timings arrive, while
    never exceeding the max size to avoid memory/OOM risk.
    """

    inner: ReadTask = attrs.field()
    sizer: AdaptiveCheckpointSizer = attrs.field()
    size_tracker: BatchSizeTracker | None = attrs.field(default=None)

    def to_batches(
        self,
        *,
        batch_size: int | None = None,
    ) -> Iterator[pa.RecordBatch | list[dict]]:
        max_size = self.sizer.max_size
        if max_size <= 0:
            max_size = self.sizer.max_size

        # The inner scan's ``batch_size`` sets how many rows Lance
        # materializes per read, not the consumer batch shape — the loop
        # below re-slices each inner batch to the sizer's
        # ``current_size``. Scan at least ``max_size`` so one inner batch
        # can always fill a full consumer slice, and honor a larger
        # caller hint when there is one.
        scan_size = max(int(batch_size or 0), max_size)
        if scan_size <= 0:
            scan_size = max(1, max_size)

        for batch in self.inner.to_batches(batch_size=scan_size):
            if isinstance(batch, pa.RecordBatch):
                total = batch.num_rows
                offset = 0
                while offset < total:
                    size = min(self.sizer.current_size, max_size, total - offset)
                    if size <= 0:
                        size = 1
                    if self.size_tracker is not None:
                        self.size_tracker.record(size)
                    yield batch.slice(offset, size)
                    offset += size
            else:
                total = len(batch)
                offset = 0
                while offset < total:
                    size = min(self.sizer.current_size, max_size, total - offset)
                    if size <= 0:
                        size = 1
                    if self.size_tracker is not None:
                        self.size_tracker.record(size)
                    yield batch[offset : offset + size]
                    offset += size

    def checkpoint_key(self) -> str:
        return self.inner.checkpoint_key()

    def dest_frag_id(self) -> int:
        return self.inner.dest_frag_id()

    def dest_offset(self) -> int:
        return self.inner.dest_offset()

    def num_rows(self) -> int:
        return self.inner.num_rows()

    def table_uri(self) -> str:
        return self.inner.table_uri()

    def __getattr__(self, item: str) -> Any:
        return getattr(self.inner, item)
