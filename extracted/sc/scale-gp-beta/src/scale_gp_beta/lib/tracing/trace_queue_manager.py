import time
import queue
import atexit
import logging
import threading
from typing import TYPE_CHECKING, Optional

from scale_gp_beta import SGPClient, SGPClientError

from .util import configure, is_disabled
from .trace_exporter import TraceExporter

if TYPE_CHECKING:
    import httpx

    from .span import Span
    from .trace import Trace

# configurable by env vars?
DEFAULT_MAX_QUEUE_SIZE = 4_000
DEFAULT_TRIGGER_QUEUE_SIZE = 200
DEFAULT_TRIGGER_CADENCE = 4.0
DEFAULT_MAX_BATCH_SIZE = 50
DEFAULT_RETRIES = 4

WORKER_SLEEP_SECONDS = 0.1

log: logging.Logger = logging.getLogger(__name__)


class TraceQueueManager:
    """Manage trace and spans queue
    Store spans in-memory until the threshold has been reached then flush to server.

    Optionally provide a client, if unprovided, we will attempt to create a default client.
    """

    def __init__(
        self,
        client: Optional[SGPClient] = None,
        max_queue_size: int = DEFAULT_MAX_QUEUE_SIZE,
        max_batch_size: int = DEFAULT_MAX_BATCH_SIZE,
        trigger_queue_size: int = DEFAULT_TRIGGER_QUEUE_SIZE,
        trigger_cadence: float = DEFAULT_TRIGGER_CADENCE,
        retries: int = DEFAULT_RETRIES,
        worker_enabled: Optional[bool] = None,
    ):
        self._client = client
        self.register_client(client) if client else None
        self._attempted_local_client_creation = False
        self._trigger_queue_size = trigger_queue_size
        self._trigger_cadence = trigger_cadence

        self._reset_trigger_time()

        self._exporter = TraceExporter(max_batch_size, retries)

        self._shutdown_event = threading.Event()
        self._queue: queue.Queue[Span] = queue.Queue(maxsize=max_queue_size)

        self._worker_enabled = worker_enabled if worker_enabled is not None else not is_disabled()

        if self._worker_enabled:
            self._worker = threading.Thread(daemon=True, target=self._run)
            self._worker.start()

            # ensure the thread joins on exit
            atexit.register(self.shutdown)

    def register_client(self, client: SGPClient) -> None:
        log.info("Registering client")
        self._client = client

        original_prepare_request = self._client._prepare_request

        def custom_prepare_request(request: "httpx.Request") -> None:
            original_prepare_request(request)

            # TODO: Hook logic here, we should check to see if we are in the scope of a span, if so we should inject
            # appropriate headers into the request
            # current_span = Scope.get_current_span()

        self._client._prepare_request = custom_prepare_request  # type: ignore

    def shutdown(self, timeout: Optional[float] = None) -> None:
        if not self._worker_enabled:
            log.debug("No worker to shutdown")
            return
        log.info(f"Shutting down trace queue manager, joining worker thread with timeout {timeout}")
        self._shutdown_event.set()
        self._worker.join(timeout=timeout)
        log.info("Shutdown complete")

    def report_span_start(self, span: "Span") -> None:
        # TODO: support making this optional. Current backend requires us to send span starts
        self.enqueue(span)

    def report_span_end(self, span: "Span") -> None:
        self.enqueue(span)

    def report_trace_start(self, trace: "Trace") -> None:
        pass

    def report_trace_end(self, trace: "Trace") -> None:
        pass

    def flush_queue(self) -> None:
        self._export()

    def enqueue(self, span: "Span") -> None:
        try:
            # Should this be a deep copy of span instead? Currently is a reference
            self._queue.put_nowait(span)
        except queue.Full:
            log.warning(f"Queue full, ignoring span {span.span_id}")

    def export_now(self, span: "Span") -> None:
        if self.client:
            self._exporter.export_span(self.client, span)

    @property
    def client(self) -> Optional[SGPClient]:
        """
        Use client provided client on init if available, otherwise attempt once to create a default one.
        :return: SGPClient
        """
        if self._client is not None:
            return self._client
        if self._attempted_local_client_creation:
            # Already tried and failed to create a client
            return None

        log.info("Tracing queue manager not initialized, attempting to create a default one")
        try:
            self.register_client(SGPClient())
        except SGPClientError:
            log.warning(
                f"Failed to create SGPClient for tracing queue manager {self}, ignoring traces. Please initialize with a working client."
            )
        finally:
            self._attempted_local_client_creation = True
        return self._client

    def _run(self) -> None:
        # daemon worker loop
        while not self._shutdown_event.is_set():
            current_time = time.time()
            queue_size = self._queue.qsize()

            if queue_size >= self._trigger_queue_size or current_time >= self._next_trigger_time:
                self._export()
                self._reset_trigger_time()
                continue

            time.sleep(WORKER_SLEEP_SECONDS)

        # flush all on shutdown
        self._export()

    def _export(self) -> None:
        if self.client:
            self._exporter.export(self.client, self._queue)

    def _reset_trigger_time(self) -> None:
        self._next_trigger_time = time.time() + self._trigger_cadence


_global_tracing_queue_manager: Optional[TraceQueueManager] = None
_queue_manager_lock = threading.Lock()


def init(client: Optional[SGPClient] = None, disabled: Optional[bool] = None) -> None:
    """Initialize the tracing backend

    Good practice to always include this method call with a valid client at your program entrypoint.

    Tracing will attempt to generate a default client if unprovided.

    :param client: SGPClient
    :param disabled: Set to True to disable tracing. Overrides environment variable ``DISABLE_SCALE_TRACING``
    """
    if disabled is not None:
        configure(disabled=disabled)

    global _global_tracing_queue_manager
    if _global_tracing_queue_manager is not None:
        if client is not None:
            _global_tracing_queue_manager.register_client(client)
        return

    with _queue_manager_lock:
        if _global_tracing_queue_manager is None:
            _global_tracing_queue_manager = TraceQueueManager(client)


def tracing_queue_manager() -> TraceQueueManager:
    global _global_tracing_queue_manager
    if _global_tracing_queue_manager is None:
        init(None)

    if _global_tracing_queue_manager is None:
        # should never happen... useful for linting
        raise RuntimeError("Tracing queue manager failed to initialize.")

    return _global_tracing_queue_manager
