"""Stub file for engine.verify directory."""
from typing import Any

# Constants
BAD_REQUEST: str = ...  # From worker
CONFIRMED: str = ...  # From worker
DROPPED: str = ...  # From worker
REJECTED: str = ...  # From worker
UNAVAILABLE: str = ...  # From worker
UNVERIFIABLE: str = ...  # From worker
logger: Any = ...  # From worker

# Functions
# From http
def post_json(url: str, body: dict[str, Any], timeout_s: float) -> Any:
    """
    ``POST`` ``body`` as JSON to ``url`` and return what came back; never raises.
    
        Args:
            url: An ``http://`` or ``https://`` URL.  The scheme is validated by the caller when
                the worker is built (``WorkerSettings.from_env``); this function trusts it.
            body: A JSON-serialisable request body.
            timeout_s: Socket timeout for connect and for each read.
    
        Returns:
            The reply; see :class:`HttpReply`.
    
        Raises:
            TypeError: ``body`` is not JSON-serialisable -- a caller bug, raised rather than
                folded so it is not mistaken for a network failure and retried.
    """
    ...

# From worker
def build_worker(settings: Any) -> Any | Any:
    """
    A new, unshared worker for ``settings``.  Prefer :func:`worker_for`.
    """
    ...

# From worker
def close_all_workers(timeout_s: float = 5.0) -> None:
    """
    Close and forget every worker :func:`worker_for` built.  Safe to call repeatedly.
    """
    ...

# From worker
def request_body(job: Any) -> dict[str, Any]:
    """
    The exact §2 wire body: ``{camera_id, rtp_timestamp, timestamp_ms, query, frames, vote}``.
    """
    ...

# From worker
def worker_for() -> Any:
    """
    The process-wide worker for the current ``(mode, endpoint)``; built on first call.
    
        The environment is read here, not at import, so importing the engine starts nothing.
        A worker that was closed is replaced on the next call.
    """
    ...

# Classes
# From http
class HttpReply:
    # What one request produced.
    #
    #     Attributes:
    #         code: The HTTP status, or ``None`` when no response arrived (transport error or
    #             timeout).
    #         payload: The decoded JSON body, or ``None`` when there was none or it did not parse.
    #         message: A short human-readable description for logs and ``Verdict.reason``: the
    #             error envelope's ``message`` (plus ``trackingCode``) for a non-2xx, the exception
    #             text for a transport failure, empty for a well-formed 200.

    ...

# From worker
class LiveVerificationWorker:
    # ``live`` mode: one daemon thread POSTing jobs to the VSS verify endpoint in order.
    #
    #     Args:
    #         settings: Parsed §2 environment.
    #         backoff_s: Retry steps; the last one repeats.  Overridable so tests can run the real
    #             retry loop in milliseconds -- production always uses the §2 table.

    def __init__(self: Any, settings: Any) -> None: ...

    def close(self: Any, timeout_s: float = 5.0) -> None:
        """
        Stop the thread and join it for up to ``timeout_s``.
        
                Queued jobs get ``unavailable``.  A request already on the wire cannot be
                interrupted (``urllib`` has no cancel); if it outlasts ``timeout_s`` the daemon
                thread is abandoned, logged, and dies with the process.
        """
        ...

    def closed(self: Any) -> bool: ...

    def submit(self: Any, mailbox: str, job: Any) -> bool: ...

    def take(self: Any, mailbox: str, frame_ts: float) -> Any | None: ...


# From worker
class ScheduledVerificationWorker:
    # ``stub`` and ``off`` modes: no thread, no I/O, fully deterministic.
    #
    #     Each submit schedules ``verdict`` for its mailbox, visible once the caller's stream clock
    #     reaches ``job.frame_ts + delay_s``.  ``delay_s=None`` (``off``) makes it visible on the
    #     very next :meth:`take`, whatever the clock.  A mailbox re-submitting a job equal on
    #     ``(camera_id, timestamp_ms, query)`` to one it is still waiting on gets one verdict, as
    #     in live mode.

    def __init__(self: Any, verdict: Any, delay_s: float | None) -> None: ...

    def close(self: Any, timeout_s: float = 5.0) -> None: ...

    def closed(self: Any) -> bool: ...

    def submit(self: Any, mailbox: str, job: Any) -> bool: ...

    def take(self: Any, mailbox: str, frame_ts: float) -> Any | None: ...


# From worker
class Verdict:
    # The outcome delivered to a mailbox; ``status`` is one of :data:`STATUSES`.

    ...

# From worker
class VerificationWorker:
    # What the ``verification`` primitive codes against (§2).

    def close(self: Any, timeout_s: float = 5.0) -> None:
        """
        Stop accepting jobs; a live worker also stops and joins its thread.
        """
        ...

    def submit(self: Any, mailbox: str, job: Any) -> bool:
        """
        Queue ``job`` for ``mailbox``; never blocks.  ``False`` only once closed.
        """
        ...

    def take(self: Any, mailbox: str, frame_ts: float) -> Any | None:
        """
        Pop the next verdict for ``mailbox`` if one has arrived; never blocks.
        """
        ...


# From worker
class VerifyJob:
    # One verification request, as the primitive builds it (§2).

    ...

# From worker
class WorkerSettings:
    # The seven §2 environment variables, parsed and bounded.
    #
    #     Read once, when a worker is built -- never from the manifest: the endpoint is
    #     deployment-specific and app folders are immutable.

    def from_env(cls: Any, environ: Any[str, str] | None = None) -> Any:
        """
        Parse the environment; a bad value is logged at ERROR and its default used.
        
                Falling back rather than raising is deliberate: :func:`worker_for` is called lazily
                from the frame loop on the first candidate, so a typo in a deployment variable
                would otherwise crash the pipeline at the moment an alert is being raised.
        """
        ...


from . import http, worker