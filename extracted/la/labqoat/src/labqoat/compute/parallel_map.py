"""Bounded lazy dispatch with ordered or completion-ordered result delivery."""

from collections.abc import Callable, Generator, Iterable, Iterator
from concurrent.futures import FIRST_COMPLETED, Future, ThreadPoolExecutor, wait
from typing import Generic, TypeVar

T = TypeVar("T")
R = TypeVar("R")


class ParallelMap(Generic[T, R]):
    """Keep at most the configured number of input operations in flight."""

    def __init__(self, operation: Callable[[T], R], limit: int, ordered: bool) -> None:
        """Validate dispatch bounds without consuming inputs or starting threads."""
        if type(limit) is not int or not 1 <= limit <= 256:
            raise ValueError("max_in_flight must be an integer between 1 and 256")
        self.operation = operation
        self.limit = limit
        self.ordered = ordered

    def iterate(self, inputs: Iterable[T]) -> Generator[R, None, None]:
        """Consume inputs only as output delivery frees space in the bounded window."""
        source = iter(inputs)
        executor = ThreadPoolExecutor(max_workers=self.limit, thread_name_prefix="labqoat-map")
        pending: dict[Future[R], None] = {}
        try:
            self._fill(source, executor, pending)
            while pending:
                future = self._next(pending)
                del pending[future]
                yield future.result()
                self._fill(source, executor, pending)
        finally:
            executor.shutdown(wait=False, cancel_futures=True)

    def _fill(self, source: Iterator[T], executor: ThreadPoolExecutor, pending: dict[Future[R], None]) -> None:
        """Apply backpressure to generators even when remote operations complete quickly."""
        while len(pending) < self.limit:
            try:
                item = next(source)
            except StopIteration:
                return
            pending[executor.submit(self.operation, item)] = None

    def _next(self, pending: dict[Future[R], None]) -> Future[R]:
        """Preserve input order or release the next completed operation."""
        if self.ordered:
            return next(iter(pending))
        completed, _remaining = wait(pending, return_when=FIRST_COMPLETED)
        return next(iter(completed))
