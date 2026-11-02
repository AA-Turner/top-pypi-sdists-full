"""Bounded lookahead for sampler-selected file batches on local or managed workers."""

from collections import deque
from collections.abc import Generator, Iterable, Iterator, Mapping, Sequence
from concurrent.futures import Future, ThreadPoolExecutor
from contextlib import closing, contextmanager
from dataclasses import dataclass
from pathlib import Path

from labqoat.dataset_access.dataset_provider import DatasetProvider, DatasetReference
from labqoat.dataset_access.prefetched_batch import PrefetchedBatch


@dataclass(frozen=True, slots=True)
class DatasetPrefetch:
    """Overlap acquisition with computation while retaining only a bounded batch window."""

    provider: DatasetProvider
    reference: DatasetReference
    ahead: int = 2

    def __post_init__(self) -> None:
        """Reject unbounded or nonpositive lookahead without starting any work."""
        if not 1 <= self.ahead <= 64:
            raise ValueError("Dataset prefetch lookahead must be between 1 and 64 batches")

    @contextmanager
    def open(self, batches: Iterable[Sequence[str]]) -> Iterator[Iterator[Mapping[str, Path]]]:
        """Keep current paths valid until iteration advances; close on early exit."""
        self.provider.manifest(self.reference)
        pending: deque[Future[PrefetchedBatch]] = deque()
        try:
            with ThreadPoolExecutor(max_workers=self.ahead, thread_name_prefix="dataset-prefetch") as pool:
                selected = iter(batches)
                for _index in range(self.ahead):
                    self._submit(pool, pending, selected)
                with closing(self._iterate(pool, pending, selected)) as ready:
                    yield ready
        finally:
            self._release(pending)

    def _iterate(
        self, pool: ThreadPoolExecutor, pending: deque[Future[PrefetchedBatch]], selected: Iterator[Sequence[str]]
    ) -> Generator[Mapping[str, Path], None, None]:
        """Preserve sampler order without waiting for unrelated upcoming batches."""
        while pending:
            with closing(pending.popleft().result()) as batch:
                self._submit(pool, pending, selected)
                yield batch.files

    def _submit(
        self, pool: ThreadPoolExecutor, pending: deque[Future[PrefetchedBatch]], selected: Iterator[Sequence[str]]
    ) -> None:
        """Pull one batch from the sampler, never materializing its entire sequence."""
        paths = next(selected, None)
        if paths is not None:
            pending.append(pool.submit(PrefetchedBatch.acquire, self.provider, self.reference, tuple(paths)))

    @staticmethod
    def _release(pending: deque[Future[PrefetchedBatch]]) -> None:
        """Drop completed lookahead leases even after transfer or authored failures."""
        for future in pending:
            if future.exception() is None:
                future.result().close()
