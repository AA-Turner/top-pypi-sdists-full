import threading
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any, Protocol, Set

from chalk.clogging import chalk_logger


class CancellableQuery(Protocol):
    def cancel(self) -> None:
        ...


class QueryRegistry:
    """
    Thread-safe, extensible registry for tracking and cancelling active queries across multiple backends.
    Stores CancellableQuery objects.
    """

    def __init__(self):
        super().__init__()
        self._lock = threading.Lock()
        self._is_shutting_down = False
        self._active_queries: Set[CancellableQuery] = set()

    def register_query(self, query: CancellableQuery) -> None:
        """
        Register a new query. Returns the unique registry ID, used for unregistering, or None if shutting down.
        """
        with self._lock:
            if not self._is_shutting_down:
                self._active_queries.add(query)

    def unregister_query(self, query: CancellableQuery) -> None:
        """
        Unregister a query. Done on completion of query.
        """
        with self._lock:
            if query in self._active_queries:
                self._active_queries.remove(query)

    def cancel_all_queries(self) -> None:
        """
        Cancel all registered queries. Sets is_shutting_down to True and blocks new registrations.
        """
        with self._lock:
            self._is_shutting_down = True
            queries = list(self._active_queries)
            self._active_queries.clear()

        if not queries:
            return

        def cancel_query(query: CancellableQuery):
            try:
                query.cancel()
            except Exception as e:
                chalk_logger.exception(f"Failed to cancel query {query}: {e}")

        with ThreadPoolExecutor(max_workers=min(len(queries), 10)) as executor:
            futures = [executor.submit(cancel_query, query) for query in queries]
            for future in as_completed(futures):
                try:
                    future.result()
                except Exception:
                    # Exception already logged
                    pass

    def is_shutting_down(self) -> bool:
        """
        Whether the query registry is shutting down.
        """
        with self._lock:
            return self._is_shutting_down

    def get_active_queries(self) -> list[CancellableQuery]:
        """
        Get all active queries.
        """
        with self._lock:
            return list(self._active_queries)

    def get_num_active_queries(self) -> int:
        """
        Get the number of active queries.
        """
        with self._lock:
            return len(self._active_queries)


QUERY_REGISTRY = QueryRegistry()


def _prevent_duplicate_construction(*args: Any, **kwargs: Any):
    raise RuntimeError(
        "The QueryRegistry class is a singleton. Please use chalk.sql._internal.query_registry.QUERY_REGISTRY"
    )


QueryRegistry.__new__ = _prevent_duplicate_construction
