import threading
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Dict, List, Tuple

from abstra_internals.logger import AbstraLogger

if TYPE_CHECKING:
    from abstra_internals.cloud_api.http_client import HTTPClient

# A (name, sorted-tags) group accumulated within a single execution.
_GroupKey = Tuple[str, Tuple[Tuple[str, str], ...]]


class MetricsRepository(ABC):
    """Buffers `abstra.metrics.count(...)` measurements during an execution and
    ships them once, at execution end (see ExecutionController.run)."""

    @abstractmethod
    def record(
        self,
        execution_id: str,
        stage_id: str,
        name: str,
        value: float,
        tags: Dict[str, str],
    ) -> None:
        raise NotImplementedError()

    @abstractmethod
    def flush(self, execution_id: str) -> None:
        raise NotImplementedError()


class LocalMetricsRepository(MetricsRepository):
    """No-op backend. Metric dashboards are a cloud (production) feature for now,
    so local and web-editor executions don't ship measurements anywhere."""

    def record(
        self,
        execution_id: str,
        stage_id: str,
        name: str,
        value: float,
        tags: Dict[str, str],
    ) -> None:
        return

    def flush(self, execution_id: str) -> None:
        return


class ProductionMetricsRepository(MetricsRepository):
    """Production backend: buffer in-process, pre-aggregate by (name, tags), and
    POST one compact batch per execution to cloud-api.

    Pre-aggregation is what keeps this cheap: a job that calls count() inside a
    10k-row loop buffers ~1 group per distinct (name, tags), not 10k rows.
    """

    # Cardinality guard: distinct (name, tags) groups kept per execution. Extra
    # dimensions past this are dropped (protects both memory and the DB from a
    # runaway high-cardinality tag like an id).
    MAX_GROUPS_PER_EXECUTION = 1000
    # Belt-and-suspenders against executions that never reach flush() (e.g. a
    # hard kill): cap the number of un-flushed execution buckets held in memory.
    MAX_EXECUTIONS = 256

    def __init__(self, client: "HTTPClient") -> None:
        self.client = client
        self._lock = threading.Lock()
        self._buffer: Dict[str, Dict[_GroupKey, dict]] = {}

    def record(
        self,
        execution_id: str,
        stage_id: str,
        name: str,
        value: float,
        tags: Dict[str, str],
    ) -> None:
        key: _GroupKey = (name, tuple(sorted(tags.items())))
        with self._lock:
            groups = self._buffer.get(execution_id)
            if groups is None:
                if len(self._buffer) >= self.MAX_EXECUTIONS:
                    # Drop the oldest un-flushed execution (insertion order).
                    self._buffer.pop(next(iter(self._buffer)), None)
                groups = self._buffer[execution_id] = {}
            group = groups.get(key)
            if group is None:
                if len(groups) >= self.MAX_GROUPS_PER_EXECUTION:
                    return  # cardinality cap reached — silently drop new dims
                group = groups[key] = {
                    "name": name,
                    "tags": tags,
                    "stageId": stage_id,
                    "count": 0,
                    "sum": 0.0,
                }
            group["count"] += 1
            group["sum"] += value

    def flush(self, execution_id: str) -> None:
        with self._lock:
            groups = self._buffer.pop(execution_id, None)
        if not groups:
            return
        metrics: List[dict] = [
            {
                "name": g["name"],
                "tags": g["tags"],
                "count": g["count"],
                "sum": g["sum"],
                "stageId": g["stageId"],
                "executionId": execution_id,
            }
            for g in groups.values()
        ]
        try:
            # Fire-and-forget: metrics are best-effort and must never slow down
            # or fail the user's execution teardown.
            self.client.async_post("/metrics/batch", json={"metrics": metrics})
        except Exception as e:
            AbstraLogger.capture_exception(e)
