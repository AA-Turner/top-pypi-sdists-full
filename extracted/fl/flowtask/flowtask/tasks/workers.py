"""Worker Queue Inspector.

Provides tools to inspect the status of QWorker processes and their task queues.
This module is used by the ``flowtask workers queues`` CLI command to display
a point-in-time snapshot of queued tasks and worker health.
"""
import logging
import socket
import collections
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any

from tabulate import tabulate


logger = logging.getLogger(__name__)


@dataclass
class TaskInfo:
    """Metadata for a single queued task.

    Attributes:
        task_id: Unique UUID string for the task.
        task_name: Human-readable name (e.g. ``"navigator.scraper"`` or
            ``"my_func"``).
        enqueue_timestamp: When the task was created / queued (best-effort).
        deserialization_error: Non-None when the task payload could not be
            deserialized; contains a human-readable error message.
    """

    task_id: str
    task_name: str
    enqueue_timestamp: datetime
    deserialization_error: str | None = None


@dataclass
class WorkerInfo:
    """Metadata and queue snapshot for a single QWorker process.

    Attributes:
        worker_id: Identifier string, e.g. ``"localhost:8001"``.
        host: Hostname or IP address.
        port: TCP port the worker listens on.
        pid: OS process ID, or ``None`` when not accessible.
        status: ``"running"`` | ``"unreachable"`` | ``"unknown"``.
        queue_size: Approximate number of pending tasks (point-in-time
            snapshot; may not reflect exact state).
        tasks: Individual TaskInfo objects extracted from the queue.
    """

    worker_id: str
    host: str
    port: int
    pid: int | None
    status: str
    queue_size: int
    tasks: list[TaskInfo] = field(default_factory=list)


class WorkerQueueInspector:
    """Inspect QWorker processes and their task queues.

    Connects to the configured QClient worker list, checks process health
    via TCP and ``psutil``, and extracts queue metadata when the workers are
    accessible in-process (e.g. from an embedded scheduler context).

    Args:
        worker_list: Explicit list of ``(host, port)`` tuples.  When
            ``None`` the flowtask configuration values
            ``WORKER_LIST`` / ``WORKER_HIGH_LIST`` are used (falling back
            to QClient auto-discovery).

    Example::

        inspector = WorkerQueueInspector()
        mp_workers = inspector.inspect_multiprocessing_queues()
        asyncio_tasks = inspector.inspect_asyncio_queues()
        print(inspector.format_output(mp_workers, asyncio_tasks))
    """

    # TCP connection timeout in seconds for reachability checks.
    _TCP_TIMEOUT: float = 2.0

    def __init__(self, worker_list: list | None = None) -> None:
        self.logger = logging.getLogger(__name__)
        self._worker_list = worker_list
        self._qclient = self._create_qclient()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _create_qclient(self) -> Any:
        """Instantiate a QClient using flowtask configuration.

        Returns:
            A QClient instance, or ``None`` when the qw library is not
            importable or the client cannot be created.
        """
        try:
            from qw.client import QClient  # noqa: PLC0415 (deferred import)
            if self._worker_list:
                client = QClient(worker_list=self._worker_list)
            else:
                try:
                    from flowtask.conf import WORKER_LIST  # noqa: PLC0415
                except ImportError:
                    WORKER_LIST = None
                client = QClient(worker_list=WORKER_LIST)
            self.logger.debug(
                "QClient created with %d workers",
                len(getattr(client, "_workers", []))
            )
            return client
        except Exception as exc:  # pylint: disable=broad-except
            self.logger.warning("Could not create QClient: %s", exc)
            return None

    def _is_reachable(self, host: str, port: int) -> bool:
        """Check whether a TCP endpoint is reachable.

        Args:
            host: Hostname or IP address.
            port: TCP port number.

        Returns:
            ``True`` when a connection can be established within
            :attr:`_TCP_TIMEOUT` seconds.
        """
        try:
            with socket.create_connection((host, port), timeout=self._TCP_TIMEOUT):
                return True
        except OSError:
            return False

    def _get_pid_for_port(self, host: str, port: int) -> int | None:
        """Find the PID of the process listening on *host*:*port*.

        Uses ``psutil`` to iterate over network connections. Returns
        ``None`` when ``psutil`` is unavailable or no matching process
        is found.

        Args:
            host: Hostname or IP (``"0.0.0.0"`` / ``"localhost"``
                variants are normalised to ``"0.0.0.0"``).
            port: TCP port number.

        Returns:
            Integer PID, or ``None``.
        """
        try:
            import psutil  # noqa: PLC0415
        except ImportError:
            self.logger.debug("psutil not available; PID lookup skipped")
            return None

        try:
            for conn in psutil.net_connections(kind="tcp"):
                if conn.laddr.port == port and conn.status == "LISTEN":
                    return conn.pid
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass
        except Exception as exc:  # pylint: disable=broad-except
            self.logger.debug("psutil error during PID lookup: %s", exc)
        return None

    def _get_process_status(self, pid: int | None) -> str:
        """Return a human-readable process status string.

        Args:
            pid: Process ID, or ``None``.

        Returns:
            ``"running"``, ``"sleeping"``, ``"unknown"``, or another
            status string from ``psutil.Process.status()``.
        """
        if pid is None:
            return "unknown"
        try:
            import psutil  # noqa: PLC0415
            proc = psutil.Process(pid)
            return proc.status()
        except Exception:  # pylint: disable=broad-except
            return "unknown"

    @staticmethod
    def _extract_task_name(wrapper: Any) -> str:
        """Extract a human-readable task name from a queue wrapper.

        Args:
            wrapper: A ``TaskWrapper``, ``FuncWrapper``, or any other
                queue wrapper object.

        Returns:
            A string such as ``"navigator.scraper"`` (TaskWrapper),
            ``"my_func"`` (FuncWrapper), or ``"<unknown>"`` as fallback.
        """
        try:
            # TaskWrapper has .program and .task
            if hasattr(wrapper, "program") and hasattr(wrapper, "task"):
                return f"{wrapper.program}.{wrapper.task}"
        except Exception:  # pylint: disable=broad-except
            pass
        try:
            # FuncWrapper has .func (callable)
            if hasattr(wrapper, "func") and callable(wrapper.func):
                return getattr(wrapper.func, "__name__", str(wrapper.func))
        except Exception:  # pylint: disable=broad-except
            pass
        try:
            return str(wrapper)
        except Exception:  # pylint: disable=broad-except
            return "<unknown>"

    @staticmethod
    def _extract_task_id(wrapper: Any) -> str:
        """Extract the unique task identifier from a queue wrapper.

        Args:
            wrapper: Any object with an ``id`` or ``_id`` attribute.

        Returns:
            String representation of the task UUID, or ``"<no-id>"``.
        """
        try:
            return str(wrapper.id)
        except Exception:  # pylint: disable=broad-except
            pass
        try:
            return str(wrapper._id)  # noqa: SLF001
        except Exception:  # pylint: disable=broad-except
            return "<no-id>"

    @staticmethod
    def _extract_enqueue_timestamp(wrapper: Any) -> datetime:
        """Extract or estimate the enqueue timestamp from a wrapper.

        ``QueueWrapper`` objects are created with a UUID v1 ``_id`` whose
        first 60 bits encode a 100-ns timestamp.  We decode that to recover
        the approximate enqueue time.

        Args:
            wrapper: Any queue wrapper object.

        Returns:
            A ``datetime`` object (UTC), falling back to
            ``datetime.utcnow()`` when extraction fails.
        """
        try:
            import uuid  # noqa: PLC0415
            raw_id = getattr(wrapper, "_id", None) or getattr(wrapper, "id", None)
            if isinstance(raw_id, uuid.UUID) and raw_id.version == 1:
                # UUID v1 timestamp is 100-ns intervals since Oct 1582
                # Python's uuid library exposes .time in those 100-ns ticks.
                ts_ns100 = raw_id.time
                # Convert to Unix timestamp:
                # 0x01b21dd213814000 is the offset between RFC4122 epoch and Unix epoch
                unix_ts = (ts_ns100 - 0x01B21DD213814000) / 1e7
                return datetime.utcfromtimestamp(unix_ts)
        except Exception:  # pylint: disable=broad-except
            pass
        return datetime.utcnow()

    def _inspect_asyncio_queue_object(
        self, queue: Any
    ) -> list[TaskInfo]:
        """Extract TaskInfo objects from an ``asyncio.Queue`` instance.

        Accesses the internal ``_queue`` deque (implementation detail of
        CPython's ``asyncio.Queue``).  Handles deserialization failures
        per item — a bad payload shows an error but does not block others.

        Args:
            queue: An ``asyncio.Queue`` instance.

        Returns:
            List of :class:`TaskInfo` objects.
        """
        tasks: list[TaskInfo] = []
        try:
            # CPython stores items in queue._queue (collections.deque)
            internal: collections.deque = getattr(queue, "_queue", None)
            if internal is None:
                self.logger.debug("asyncio.Queue has no _queue attribute")
                return tasks
            for item in list(internal):
                try:
                    task_id = self._extract_task_id(item)
                    task_name = self._extract_task_name(item)
                    ts = self._extract_enqueue_timestamp(item)
                    tasks.append(TaskInfo(
                        task_id=task_id,
                        task_name=task_name,
                        enqueue_timestamp=ts,
                    ))
                except Exception as item_exc:  # pylint: disable=broad-except
                    self.logger.debug(
                        "Could not extract metadata for queue item: %s", item_exc
                    )
                    tasks.append(TaskInfo(
                        task_id="<unknown>",
                        task_name="<unknown>",
                        enqueue_timestamp=datetime.utcnow(),
                        deserialization_error=str(item_exc),
                    ))
        except Exception as exc:  # pylint: disable=broad-except
            self.logger.warning("Error inspecting asyncio.Queue: %s", exc)
        return tasks

    # ------------------------------------------------------------------
    # Public interface
    # ------------------------------------------------------------------

    def inspect_multiprocessing_queues(self) -> list[WorkerInfo]:
        """Inspect all configured multiprocessing (QWorker) workers.

        For each ``(host, port)`` in the QClient worker list:

        1. Attempt a TCP connection to determine reachability.
        2. Use ``psutil`` to find the listening process PID and status.
        3. Return a :class:`WorkerInfo` with the collected metadata.

        Workers that cannot be reached are marked as ``"unreachable"``
        and processing continues to the next worker — the method never
        raises an exception.

        Returns:
            List of :class:`WorkerInfo` objects, one per configured worker.
            An empty list is returned when no workers are configured or
            the QClient could not be created.
        """
        results: list[WorkerInfo] = []

        if self._qclient is None:
            self.logger.warning(
                "QClient not available; skipping multiprocessing queue inspection"
            )
            return results

        workers: list[tuple[str, int]] = []
        try:
            workers = list(getattr(self._qclient, "_workers", []))
        except Exception as exc:  # pylint: disable=broad-except
            self.logger.warning("Could not read QClient._workers: %s", exc)
            return results

        self.logger.debug("Inspecting %d workers", len(workers))

        for host, port in workers:
            worker_id = f"{host}:{port}"
            self.logger.debug("Checking worker %s", worker_id)
            try:
                reachable = self._is_reachable(host, port)
                if not reachable:
                    results.append(WorkerInfo(
                        worker_id=worker_id,
                        host=host,
                        port=port,
                        pid=None,
                        status="unreachable",
                        queue_size=0,
                    ))
                    self.logger.info("Worker %s is unreachable", worker_id)
                    continue

                pid = self._get_pid_for_port(host, port)
                status = self._get_process_status(pid) if pid else "running"

                results.append(WorkerInfo(
                    worker_id=worker_id,
                    host=host,
                    port=port,
                    pid=pid,
                    status=status,
                    queue_size=0,  # queue contents not accessible cross-process
                    tasks=[],
                ))
            except Exception as worker_exc:  # pylint: disable=broad-except
                self.logger.warning(
                    "Error inspecting worker %s: %s", worker_id, worker_exc
                )
                results.append(WorkerInfo(
                    worker_id=worker_id,
                    host=host,
                    port=port,
                    pid=None,
                    status="unknown",
                    queue_size=0,
                ))

        return results

    def inspect_asyncio_queues(self) -> list[TaskInfo]:
        """Inspect asyncio task queues accessible from the current process.

        Attempts to access the flowtask scheduler's QueueManager queues if
        the scheduler is running in the current Python process.  Returns
        an empty list when the scheduler is unavailable — never raises.

        Returns:
            List of :class:`TaskInfo` objects representing tasks currently
            in the scheduler's asyncio queue, or an empty list.
        """
        tasks: list[TaskInfo] = []
        try:
            # Try to reach the scheduler that may be running in this process.
            # This is relevant when WorkerQueueInspector is invoked from within
            # a running flowtask scheduler instance.
            from flowtask.scheduler.scheduler import NavScheduler  # noqa: PLC0415
            scheduler = NavScheduler.__new__(NavScheduler)
            if hasattr(scheduler, "qworker") and scheduler.qworker is not None:
                qclient = scheduler.qworker
                # If qclient exposes a QueueManager via .queue attribute (rare),
                # inspect it.
                queue_mgr = getattr(qclient, "_queue_manager", None)
                if queue_mgr is not None:
                    q = getattr(queue_mgr, "queue", None)
                    if q is not None:
                        tasks.extend(self._inspect_asyncio_queue_object(q))
        except Exception as exc:  # pylint: disable=broad-except
            self.logger.debug(
                "Scheduler asyncio queue not accessible (expected in CLI context): %s",
                exc,
            )

        if not tasks:
            # Alternative: if a QueueManager was passed directly (testing / embedded use)
            self.logger.debug("No asyncio queue tasks found (scheduler not running)")

        return tasks

    def inject_asyncio_queue(self, queue: Any) -> list[TaskInfo]:
        """Inspect a directly supplied asyncio.Queue.

        Allows callers (e.g. tests or embedded usage) to pass a queue
        object for inspection without needing a running scheduler.

        Args:
            queue: An ``asyncio.Queue`` instance.

        Returns:
            List of :class:`TaskInfo` extracted from the queue.
        """
        return self._inspect_asyncio_queue_object(queue)

    def format_output(
        self,
        multiprocessing_workers: list[WorkerInfo],
        asyncio_tasks: list[TaskInfo],
    ) -> str:
        """Render inspection results as human-readable console tables.

        Produces two sections:

        * **Multiprocessing Workers** — one row per worker with its ID,
          host, port, PID, status, and approximate queue depth.
        * **Asyncio Queue Tasks** — one row per task with ID, name, and
          enqueue timestamp (oldest first).

        Args:
            multiprocessing_workers: Output of
                :meth:`inspect_multiprocessing_queues`.
            asyncio_tasks: Output of :meth:`inspect_asyncio_queues`.

        Returns:
            A formatted string ready for ``print()``.
        """
        lines: list[str] = []

        # ── Section 1: Multiprocessing workers ────────────────────────
        lines.append("\n=== Multiprocessing Workers ===\n")
        if not multiprocessing_workers:
            lines.append("  No workers configured or QClient unavailable.\n")
        else:
            worker_rows = [
                [
                    w.worker_id,
                    w.host,
                    w.port,
                    w.pid if w.pid is not None else "N/A",
                    w.status,
                    f"~{w.queue_size}" if w.queue_size >= 0 else "N/A",
                ]
                for w in multiprocessing_workers
            ]
            lines.append(
                tabulate(
                    worker_rows,
                    headers=["Worker ID", "Host", "Port", "PID", "Status", "Queue Size"],
                    tablefmt="grid",
                )
            )
            lines.append("")

            # Sub-section: tasks per worker (if any)
            for w in multiprocessing_workers:
                if w.tasks:
                    lines.append(f"\n  Tasks for worker {w.worker_id}:\n")
                    sorted_tasks = sorted(w.tasks, key=lambda t: t.enqueue_timestamp)
                    task_rows = [
                        [
                            t.task_id[:16] + "…" if len(t.task_id) > 17 else t.task_id,
                            t.task_name,
                            t.enqueue_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                            t.deserialization_error or "",
                        ]
                        for t in sorted_tasks
                    ]
                    lines.append(
                        tabulate(
                            task_rows,
                            headers=["Task ID", "Task Name", "Queued Since", "Error"],
                            tablefmt="grid",
                        )
                    )
                    lines.append("")

        # ── Section 2: Asyncio queue ───────────────────────────────────
        lines.append("\n=== Asyncio Queue Tasks ===\n")
        if not asyncio_tasks:
            lines.append("  No asyncio queue tasks found (scheduler not running).\n")
        else:
            sorted_async = sorted(asyncio_tasks, key=lambda t: t.enqueue_timestamp)
            async_rows = [
                [
                    t.task_id[:16] + "…" if len(t.task_id) > 17 else t.task_id,
                    t.task_name,
                    t.enqueue_timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                    t.deserialization_error or "",
                ]
                for t in sorted_async
            ]
            lines.append(
                tabulate(
                    async_rows,
                    headers=["Task ID", "Task Name", "Queued Since", "Error"],
                    tablefmt="grid",
                )
            )
            lines.append("")

        return "\n".join(lines)
