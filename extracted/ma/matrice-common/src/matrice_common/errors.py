"""Error types, deduplication, logging, and the log_errors decorator.

Split out of ``utils.py``; re-exported from ``matrice_common.utils`` for
backward compatibility.

NOTE: ``send_error_log`` resolves ``_get_error_logging_producer`` through the
``matrice_common.utils`` module namespace so that the historical patch target
``matrice_common.utils._get_error_logging_producer`` stays effective after the
split. The ``from .rpc import RPC`` import inside ``_get_error_logging_producer``
is kept lazy to avoid a circular import.
"""

import atexit
import base64
import hashlib
import inspect
import json
import logging
import os
import threading
import time
import traceback
from datetime import datetime, timezone
from functools import lru_cache, wraps
from types import FrameType
from typing import Any, Dict, Final, List, Optional, Tuple

from .logging_config import _SENSITIVE_NAME_RE, redact_url, scrub_message

logger = logging.getLogger(__name__)

# Sentry SDK disabled — all Sentry calls are no-ops.
# To re-enable, restore the sentry_sdk imports and remove the stubs below.
sentry_sdk = None
configure_scope = None
LoggingIntegration = None


def _utils():
    """Lazily resolve the ``matrice_common.utils`` shim module.

    Used so that test patches against ``matrice_common.utils.<name>`` are
    honored by the functions that now live here.
    """
    import matrice_common.utils as _u

    return _u


class SentryConfig:
    """Configuration for Sentry error reporting."""

    def __init__(
        self,
        dsn: str,
        environment: str = "dev",
        sample_rate: float = 1.0,
        debug: bool = False,
        service_name: str = "py_common",
        enable_tracing: bool = True,
    ) -> None:
        self.dsn = dsn
        self.environment = environment
        self.sample_rate = sample_rate
        self.debug = debug
        self.service_name = service_name
        self.enable_tracing = enable_tracing


class ErrorType:
    """Constants for error type classification in error logging."""

    NOT_FOUND: Final = "NotFound"
    PRECONDITION_FAILED: Final = "PreconditionFailed"
    VALIDATION_ERROR: Final = "ValidationError"
    UNAUTHORIZED: Final = "Unauthorized"
    UNAUTHENTICATED: Final = "Unauthenticated"
    INTERNAL: Final = "Internal"
    UNKNOWN: Final = "Unknown"
    TIMEOUT: Final = "Timeout"
    VALUE_ERROR: Final = "ValueError"
    TYPE_ERROR: Final = "TypeError"
    INDEX_ERROR: Final = "IndexError"
    KEY_ERROR: Final = "KeyError"
    ATTRIBUTE_ERROR: Final = "AttributeError"
    IMPORT_ERROR: Final = "ImportError"
    FILE_NOT_FOUND: Final = "FileNotFound"
    PERMISSION_DENIED: Final = "PermissionDenied"
    CONNECTION_ERROR: Final = "ConnectionError"
    JSON_DECODE_ERROR: Final = "JSONDecodeError"
    ASSERTION_ERROR: Final = "AssertionError"
    RUNTIME_ERROR: Final = "RuntimeError"
    MEMORY_ERROR: Final = "MemoryError"
    OS_ERROR: Final = "OSError"
    STOP_ITERATION: Final = "StopIteration"


ERROR_TYPE_TO_MESSAGE = {
    ErrorType.NOT_FOUND: "The requested resource was not found.",
    ErrorType.PRECONDITION_FAILED: "A precondition for this request was not met.",
    ErrorType.VALIDATION_ERROR: "Some input values are invalid. Please check your request.",
    ErrorType.UNAUTHORIZED: "You do not have permission to perform this action.",
    ErrorType.UNAUTHENTICATED: "Authentication is required to access this resource.",
    ErrorType.INTERNAL: "An internal server error occurred. Please try again later.",
    ErrorType.UNKNOWN: "An unknown error occurred.",
    ErrorType.TIMEOUT: "The operation timed out. Please try again.",
    ErrorType.VALUE_ERROR: "An invalid value was provided.",
    ErrorType.TYPE_ERROR: "An operation was applied to an object of inappropriate type.",
    ErrorType.INDEX_ERROR: "An index is out of range.",
    ErrorType.KEY_ERROR: "A required key was not found in the dictionary.",
    ErrorType.ATTRIBUTE_ERROR: "The requested attribute is missing or invalid.",
    ErrorType.IMPORT_ERROR: "There was an issue importing a module or object.",
    ErrorType.FILE_NOT_FOUND: "The specified file could not be found.",
    ErrorType.PERMISSION_DENIED: "You do not have permission to access this file or resource.",
    ErrorType.CONNECTION_ERROR: "A connection error occurred. Check your network or endpoint.",
    ErrorType.JSON_DECODE_ERROR: "Failed to decode the JSON data. The format might be incorrect.",
    ErrorType.ASSERTION_ERROR: "An assertion failed during execution.",
    ErrorType.RUNTIME_ERROR: "A runtime error occurred.",
    ErrorType.MEMORY_ERROR: "The system ran out of memory while processing the request.",
    ErrorType.OS_ERROR: "An operating system-level error occurred.",
    ErrorType.STOP_ITERATION: "No further items in iterator.",
}


class ErrorLog:
    def __init__(
        self,
        service_name: str,
        stack_trace: str,
        error_type: str,
        description: str,
        file_name: str,
        function_name: str,
        hash: str,
        action_record_id: Optional[str] = None,
        created_at: Optional[datetime] = None,
        is_resolved: bool = False,
        more_info: Optional[Any] = None,
        sentryIssueLink: Optional[str] = None,
    ):
        self.action_record_id = action_record_id
        self.service_name = service_name
        self.created_at = created_at or datetime.now(timezone.utc)
        self.stack_trace = stack_trace
        self.error_type = error_type
        self.description = description
        self.file_name = file_name
        self.function_name = function_name
        self.hash = hash
        self.is_resolved = is_resolved
        self.more_info = more_info
        self.sentryIssueLink = sentryIssueLink

    def to_dict(self) -> dict:
        return {
            "actionRecordId": self.action_record_id,
            "serviceName": self.service_name,
            "createdAt": self.created_at.astimezone(timezone.utc)
            .isoformat(timespec="milliseconds")
            .replace("+00:00", "Z"),
            "stackTrace": self.stack_trace,
            "errorType": self.error_type,
            "description": self.description,
            "fileName": self.file_name,
            "functionName": self.function_name,
            "hash": self.hash,
            "isResolved": self.is_resolved,
            "moreInfo": self.more_info,
            "sentryIssueLink": self.sentryIssueLink,
        }


class AppError(Exception):
    def __init__(
        self,
        error_type: str,
        error: Exception,
        service_name: str,
        details: Optional[List[Any]] = None,
        action_id: Optional[str] = None,
        session_id: Optional[str] = None,
    ):
        self.error_type = error_type
        self.error = error
        self.service_name = service_name
        self.details = details or []
        self.action_id = action_id or os.environ.get("MATRICE_ACTION_ID")
        self.session_id = session_id or os.environ.get("MATRICE_SESSION_ID") or None
        self.message = ERROR_TYPE_TO_MESSAGE.get(error_type, "An unknown error occurred.")
        super().__init__(self.message)

    def append(self, *details: Any) -> "AppError":
        self.details.extend(details)
        return self

    def generate_hash(self) -> str:
        error_class = type(self.error).__name__
        # NOTE : Decide on the fields to include in the hash
        error_str = f"{self.error_type}{error_class}{self.service_name}"
        return hashlib.sha256(error_str.encode()).hexdigest()


def _make_hashable(obj):
    """Recursively convert unhashable types to hashable ones."""
    if isinstance(obj, (list, tuple)):
        return tuple(_make_hashable(e) for e in obj)
    elif isinstance(obj, dict):
        return tuple(sorted((k, _make_hashable(v)) for k, v in obj.items()))
    elif isinstance(obj, set):
        return tuple(sorted(_make_hashable(e) for e in obj))
    elif hasattr(obj, "__dict__") and not isinstance(obj, type):
        try:
            return ("__object__", obj.__class__.__name__, _make_hashable(obj.__dict__))
        except (AttributeError, TypeError):
            return ("__str__", str(obj))
    else:
        try:
            hash(obj)
            return obj
        except TypeError:
            return ("__str__", str(obj))


def cacheable(f):
    """Wraps a function to make its args hashable before caching."""

    @lru_cache(maxsize=128)
    def wrapped(*args_hashable, **kwargs_hashable):
        try:
            return f(*args_hashable, **kwargs_hashable)
        except Exception as e:
            logging.warning(f"Error in cacheable function {f.__name__}: {str(e)}")
            raise

    @wraps(f)
    def wrapper(*args, **kwargs):
        try:
            hashable_args = tuple(_make_hashable(arg) for arg in args)
            hashable_kwargs = {k: _make_hashable(v) for k, v in kwargs.items()}
            return wrapped(*hashable_args, **hashable_kwargs)
        except Exception as e:
            logging.warning(f"Caching failed for {f.__name__}, using original function: {str(e)}")
            return f(*args, **kwargs)

    return wrapper


# In-memory cache for error deduplication
# NOTE: Configurable via environment variables
_error_cache: Dict[str, float] = {}
_error_cache_lock = threading.Lock()
# Default: 24 hours TTL, configurable via MATRICE_ERROR_CACHE_TTL_SECONDS
_ERROR_CACHE_TTL = int(os.environ.get("MATRICE_ERROR_CACHE_TTL_SECONDS", 24 * 60 * 60))
# Default: 1000 max cache size, configurable via MATRICE_ERROR_CACHE_MAX_SIZE
_ERROR_CACHE_MAX = int(os.environ.get("MATRICE_ERROR_CACHE_MAX_SIZE", 1000))
# Enable/disable deduplication via environment variable (default: enabled)
_DEDUPLICATION_ENABLED = os.environ.get("MATRICE_ERROR_DEDUPLICATION_ENABLED", "true").strip().lower() not in (
    "0",
    "false",
    "no",
    "off",
)


def get_deduplication_config() -> dict:
    """Get the current deduplication configuration."""
    return {
        "enabled": _DEDUPLICATION_ENABLED,
        "ttl_seconds": _ERROR_CACHE_TTL,
        "max_cache_size": _ERROR_CACHE_MAX,
        "current_cache_size": len(_error_cache),
    }


# NOTE: the deduplication config is intentionally NOT logged at import time.
# The stdlib root convenience functions (logging.info/warning/...) call
# logging.basicConfig() when the root logger has no handlers, which would
# attach a root StreamHandler at `import matrice_common` and permanently
# disable the package's own logging_config.configure_logging(). Callers that
# want this config can call get_deduplication_config() and log it themselves.
logger.debug("Error deduplication config: %s", get_deduplication_config())


def hash_error(*parts: str) -> str:
    """Generate a hash for error deduplication."""
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode("utf-8"))
    return h.hexdigest()


def generate_error_dedup_key(error_type: str, filename: str, function_name: str, service_name: str) -> str:
    """Generate a consistent deduplication key based on error location and type, not message content.

    This ensures the same error from the same location is not logged multiple times,
    regardless of slight variations in error messages.
    """
    return hash_error(error_type, filename, function_name, service_name)


def seen_error(hash_str: str) -> bool:
    """Check if an error has been seen recently, and update cache.

    This function is thread-safe and atomically checks and updates the cache
    to prevent race conditions where multiple threads might log the same error.
    """
    now = time.time()
    # Resolve config thresholds through the matrice_common.utils namespace so
    # that test monkeypatches against matrice_common.utils._ERROR_CACHE_TTL /
    # _ERROR_CACHE_MAX remain effective after the utils.py split.
    _u = _utils()
    _ttl = _u._ERROR_CACHE_TTL
    _max = _u._ERROR_CACHE_MAX
    with _error_cache_lock:
        # Proactive cache cleanup: remove stale entries on every call if needed
        if len(_error_cache) > _max * 0.8:  # Start cleanup at 80% capacity
            stale_keys = [k for k, t in _error_cache.items() if now - t > _ttl]
            for k in stale_keys:
                del _error_cache[k]
            if stale_keys:
                logging.debug(f"Cleaned up {len(stale_keys)} stale error cache entries")

        # Atomic check and update: prevents race condition where multiple threads
        # could pass the check before any of them updates the cache
        if hash_str in _error_cache:
            time_since_last_log = now - _error_cache[hash_str]
            if time_since_last_log <= _ttl:
                # Error was seen recently, skip logging
                return True
            else:
                # Error cache entry is stale, update and allow logging
                _error_cache[hash_str] = now
                return False
        else:
            # First time seeing this error, add to cache and allow logging
            _error_cache[hash_str] = now
            return False


@lru_cache(maxsize=1)
def _get_sentry_client(rpc_client=None, access_key=None, secret_key=None, service_name: str = "py_common"):
    """Sentry is disabled — always returns None."""
    return None


@lru_cache(maxsize=1)
def _get_error_logging_producer(rpc_client=None, access_key=None, secret_key=None):
    """Get the Kafka producer for error logging, fetching config via RPC."""
    try:
        # SECURITY (supply-chain): do NOT pip install at runtime from inside the
        # error-logging path. confluent-kafka is baked into the service image;
        # if it is genuinely missing we degrade to "Kafka error logging disabled"
        # (handled by the outer `except ImportError` below) rather than pulling an
        # unpinned package from whatever index the environment points at.
        from confluent_kafka import Producer

        access_key = access_key or os.environ.get("MATRICE_ACCESS_KEY_ID")
        secret_key = secret_key or os.environ.get("MATRICE_SECRET_ACCESS_KEY")
        if not access_key or not secret_key:
            raise ValueError(
                "Access key and Secret key are required. "
                "Set them as environment variables MATRICE_ACCESS_KEY_ID and MATRICE_SECRET_ACCESS_KEY or pass them explicitly."
            )
        try:
            if rpc_client is None:
                from .rpc import RPC

                rpc_client = RPC(access_key=access_key, secret_key=secret_key)
        except ImportError:
            raise ImportError("RPC client is not available. Check for cyclic import.")

        path = "/v1/actions/get_kafka_info"
        response = rpc_client.get(path=path, raise_exception=True)
        if not response or not response.get("success"):
            raise ValueError(f"Failed to fetch Kafka config: {response.get('message', 'No response')}")
        encoded_ip = response["data"]["ip"]
        encoded_port = response["data"]["port"]
        ip = base64.b64decode(encoded_ip).decode("utf-8")
        port = base64.b64decode(encoded_port).decode("utf-8")
        bootstrap_servers = f"{ip}:{port}"
        return Producer(
            {
                "bootstrap.servers": bootstrap_servers,
                "acks": "all",
                "retries": 3,
                "retry.backoff.ms": 1000,
                "request.timeout.ms": 30000,
                "max.in.flight.requests.per.connection": 5,
                "linger.ms": 10,
                "batch.size": 4096,
                "queue.buffering.max.ms": 50,
                "log_level": 0,
            }
        )
    except ImportError:
        logging.warning("KafkaUtils not available, error logging to Kafka disabled")
        return None


def send_sentry_log(
    filename: str,
    function_name: str,
    error_message: str,
    traceback_str: Optional[str] = None,
    additional_info: Optional[dict] = None,
    error_type: str = ErrorType.INTERNAL,
    service_name: str = "py_common",
    action_id: Optional[str] = None,
    session_id: Optional[str] = None,
):
    """Sentry is disabled — this is a no-op stub."""
    return None


def send_error_log(
    filename: str,
    function_name: str,
    error_message: str,
    traceback_str: Optional[str] = None,
    additional_info: Optional[dict] = None,
    error_type: str = ErrorType.INTERNAL,
    service_name: str = "py_common",
    action_id: Optional[str] = None,
    session_id: Optional[str] = None,
    access_key: Optional[str] = None,
    secret_key: Optional[str] = None,
    sentryIssueLink: Optional[str] = None,
):
    """Log error to the backend system, sending to Kafka.

    Note: Deduplication is now handled at the process_error_log level.
    This function should only be called after deduplication checks have passed.
    """
    if traceback_str is None:
        traceback_str = traceback.format_exc().rstrip()
    more_info = {}
    if additional_info and isinstance(additional_info, dict):
        more_info.update(additional_info)
    secret_key = secret_key or os.environ.get("MATRICE_SECRET_ACCESS_KEY")
    if not secret_key:
        raise ValueError("Secret key is required for RPC authentication")

    access_key = access_key or os.environ.get("MATRICE_ACCESS_KEY_ID")
    if not access_key:
        raise ValueError("Access key is required for RPC authentication")

    action_id = action_id or os.environ.get("MATRICE_ACTION_ID")
    session_id = session_id or os.environ.get("MATRICE_SESSION_ID") or None

    if action_id:
        more_info["actionId"] = action_id
    if session_id:
        more_info["sessionId"] = session_id

    error_hash = hash_error(error_type, filename, function_name, service_name)

    error_log = ErrorLog(
        service_name=service_name,
        stack_trace=traceback_str,
        error_type=error_type,
        description=error_message,
        file_name=filename,
        function_name=function_name,
        hash=error_hash,
        sentryIssueLink=sentryIssueLink,
        action_record_id=action_id,
        more_info=more_info,
    )
    try:
        producer = _utils()._get_error_logging_producer()
        if producer:
            producer.produce(
                topic="error_logs",
                value=json.dumps(error_log.to_dict()).encode("utf-8"),
                key=service_name.encode("utf-8"),
            )
            # Track the live producer so a best-effort atexit flush can drain
            # buffered records. We deliberately do NOT flush per-message (it
            # would serialize the hot path); short-lived/crashing processes are
            # covered by the atexit hook below.
            global _active_error_producer
            _active_error_producer = producer
    except Exception as e:
        logging.exception(f"Failed to send error log to Kafka: {str(e)}")


# Best-effort flush of any buffered error-log records at interpreter exit so
# short-lived processes (batch jobs, crashing workers) don't drop their final
# error records. Bounded timeout so exit is never blocked indefinitely.
_active_error_producer: Any = None


@atexit.register
def _flush_error_logging_producer() -> None:
    producer = _active_error_producer
    if producer is None:
        return
    try:
        producer.flush(5)
    except Exception as e:  # noqa: BLE001 - best-effort, exit path must not raise
        logger.debug("Error-log producer flush at exit failed: %s", e)


def _extract_error_location(error: Exception) -> Tuple:
    """Extract file, function, line number and frame from an exception.

    Returns:
        Tuple of (frame, func_name, func_file, lineno, info_source)
    """
    frame: Optional[FrameType]
    tb = error.__traceback__
    if tb is not None:
        while tb.tb_next:
            tb = tb.tb_next
        frame = tb.tb_frame
        func_name = frame.f_code.co_name
        func_file = os.path.abspath(frame.f_code.co_filename)
        lineno = tb.tb_lineno
        return frame, func_name, func_file, lineno, "traceback"

    # Fallback to inspect.currentframe() when no traceback
    frame = None
    func_name = "unknown_function"
    func_file = "unknown_file"
    lineno = -1

    try:
        current_frame = inspect.currentframe()
        if current_frame is not None:
            caller_frame = current_frame.f_back
            # Walk up two levels: _extract_error_location -> process_error_log -> caller
            if caller_frame is not None:
                caller_frame = caller_frame.f_back
            while caller_frame is not None:
                caller_file = os.path.abspath(caller_frame.f_code.co_filename)
                if "utils.py" not in caller_file:
                    func_name = caller_frame.f_code.co_name
                    func_file = caller_file
                    lineno = caller_frame.f_lineno
                    frame = caller_frame
                    break
                caller_frame = caller_frame.f_back
            logging.debug(f"Extracted caller info from stack: {func_file}:{lineno} in {func_name}")
    except Exception as frame_error:
        logging.debug(f"Could not extract caller frame: {frame_error}")

    return frame, func_name, func_file, lineno, "frame inspection"


def _extract_function_params(frame) -> str:
    """Extract function parameter string from a frame object.

    SECURITY: parameters whose name looks like a credential (access_key,
    secret_key, token, password, key, ...) are redacted so the auth/session
    constructors on the failure path cannot serialize the root credentials
    into the error log or the Kafka error_logs topic.
    """
    if not frame:
        return "no frame available"
    try:
        arg_info = inspect.getargvalues(frame)
        params = []
        for name in arg_info.args:
            if _SENSITIVE_NAME_RE.search(str(name)):
                params.append(f"{name}=<redacted>")
                continue
            value = arg_info.locals.get(name, "<not found>")
            val_repr = scrub_message(repr(value))
            if len(val_repr) > 120:
                val_repr = val_repr[:117] + "..."
            params.append(f"{name}={val_repr}")
        if arg_info.varargs:
            params.append(f"*{arg_info.varargs}={scrub_message(str(arg_info.locals.get(arg_info.varargs)))}")
        if arg_info.keywords:
            params.append(f"**{arg_info.keywords}={scrub_message(str(arg_info.locals.get(arg_info.keywords)))}")
        return ", ".join(params) if params else "no parameters"
    except Exception as param_error:
        logging.debug(f"Parameter extraction failed: {param_error}")
        return "unable to extract parameters"


def _extract_http_context(frame) -> Optional[Dict[str, str]]:
    """Extract HTTP request context from frame locals for debugging.

    SECURITY: values are scrubbed of credential-shaped substrings
    (Bearer/accessKey/secretKey/refreshToken/password) and URLs have their
    query string + userinfo stripped, since payload/data/curl_cmd can carry
    secrets and this context is shipped to the Kafka error_logs topic.
    """
    if not frame:
        return None
    try:
        locals_dict = frame.f_locals
        http_context = {}
        for key in ("method", "request_url", "payload", "data", "curl_cmd"):
            if key in locals_dict and locals_dict[key]:
                val_str = str(locals_dict[key])
                if key == "request_url":
                    val_str = redact_url(val_str)
                else:
                    val_str = scrub_message(val_str)
                if len(val_str) > 2000:
                    val_str = val_str[:2000] + "..."
                http_context[key] = val_str
        return http_context if http_context else None
    except Exception:
        return None


# Map Python exception types to ErrorType constants
_ERROR_TYPE_MAP: Dict[str, str] = {
    "ValueError": ErrorType.VALUE_ERROR,
    "TypeError": ErrorType.TYPE_ERROR,
    "IndexError": ErrorType.INDEX_ERROR,
    "KeyError": ErrorType.KEY_ERROR,
    "AttributeError": ErrorType.ATTRIBUTE_ERROR,
    "ImportError": ErrorType.IMPORT_ERROR,
    "FileNotFoundError": ErrorType.FILE_NOT_FOUND,
    "PermissionError": ErrorType.PERMISSION_DENIED,
    "ConnectionError": ErrorType.CONNECTION_ERROR,
    "JSONDecodeError": ErrorType.JSON_DECODE_ERROR,
    "AssertionError": ErrorType.ASSERTION_ERROR,
    "RuntimeError": ErrorType.RUNTIME_ERROR,
    "MemoryError": ErrorType.MEMORY_ERROR,
    "OSError": ErrorType.OS_ERROR,
    "StopIteration": ErrorType.STOP_ITERATION,
    "TimeoutError": ErrorType.TIMEOUT,
}


def process_error_log(
    error: Exception,
    service_name: str = "py_common",
    default_return=None,
    raise_exception: bool = False,
    log_error: bool = True,
):
    """
    Enhanced reusable error logging handler.
    Automatically extracts file, function, and parameter info
    from the traceback of a caught exception.

    Deduplication Behavior:
    - Errors are deduplicated based on: error_type, filename, function_name, and service_name
    - Deduplication check happens ONCE at the process_error_log level (not in individual logging functions)
    - Deduplication is ALWAYS enforced - if an error was logged before (within TTL), it will not be logged again
    - Deduplication is controlled by environment variables:
        * MATRICE_ERROR_DEDUPLICATION_ENABLED (default: true)
        * MATRICE_ERROR_CACHE_TTL_SECONDS (default: 86400 = 24 hours)
        * MATRICE_ERROR_CACHE_MAX_SIZE (default: 1000)
    - Same errors will be logged again after the TTL expires
    """

    start_time = time.time()
    traceback_str = traceback.format_exc().rstrip()

    error_class_name = type(error).__name__
    error_type = _ERROR_TYPE_MAP.get(error_class_name, ErrorType.INTERNAL)

    frame, func_name, func_file, lineno, info_source = _extract_error_location(error)

    logging.info(
        f"Processing error from {func_file}:{lineno}, function '{func_name}' (via {info_source}): {str(error)}"
    )

    # Resolve patch-sensitive collaborators through the matrice_common.utils
    # namespace so test patches (conftest disables dedup + stubs the loggers
    # on matrice_common.utils) remain effective after the utils.py split.
    _u = _utils()

    # ========== DEDUPLICATION CHECK (MOVED TO TOP LEVEL) ==========
    # Check deduplication ONCE here, before any logging happens
    if log_error and _u._DEDUPLICATION_ENABLED:
        dup_key = generate_error_dedup_key(error_type, func_file, func_name, service_name)
        if seen_error(dup_key):
            logging.debug(f"Skipping duplicate error log (all loggers): {dup_key}")
            # Still return or raise as requested, but skip all logging
            if raise_exception:
                raise AppError(
                    error_type=error_type,
                    error=error,
                    service_name=service_name,
                    details=[],
                    action_id=os.environ.get("MATRICE_ACTION_ID"),
                    session_id=os.environ.get("MATRICE_SESSION_ID") or None,
                )
            return default_return

    param_str = _extract_function_params(frame)
    logging.info(f"Function parameters: {param_str}")

    error_msg = f"Exception in {func_file}:{lineno}, function '{func_name}' (via {info_source}): {str(error)}"
    logging.error(error_msg)

    additional_info: Dict[str, Any] = {
        "parameters": param_str,
        "latency_ms": int((time.time() - start_time) * 1000),
    }

    http_context = _extract_http_context(frame)
    if http_context:
        additional_info["http_request_context"] = http_context

    if log_error:
        # Deduplication was already checked at the top level
        # Both loggers will run since deduplication passed

        # ========== LOG TO SENTRY ==========
        sentry_event_id = None
        try:
            sentry_event_id = _u.send_sentry_log(
                filename=func_file,
                function_name=func_name,
                error_message=error_msg,
                traceback_str=traceback_str,
                additional_info=additional_info,
                error_type=error_type,
                service_name=service_name,
                action_id=os.environ.get("MATRICE_ACTION_ID"),
                session_id=os.environ.get("MATRICE_SESSION_ID") or None,
            )
        except Exception as sentry_error:
            logging.exception(f"Failed to log error to Sentry: {str(sentry_error)}")

        sentry_link = (
            f"https://sentry.io/organizations/matrice-ai-inc/issues/?query={sentry_event_id}"
            if sentry_event_id
            else None
        )

        # ========== LOG TO KAFKA ==========
        try:
            _u.send_error_log(
                filename=func_file,
                function_name=func_name,
                error_message=error_msg,
                traceback_str=traceback_str,
                additional_info=additional_info,
                error_type=error_type,
                service_name=service_name,
                action_id=os.environ.get("MATRICE_ACTION_ID"),
                session_id=os.environ.get("MATRICE_SESSION_ID") or None,
                sentryIssueLink=sentry_link,
            )
        except Exception as logging_error:
            logging.exception(f"Failed to log error to Kafka: {str(logging_error)}")

    if raise_exception:
        raise AppError(
            error_type=error_type,
            error=error,
            service_name=service_name,
            details=[param_str],
            action_id=os.environ.get("MATRICE_ACTION_ID"),
            session_id=os.environ.get("MATRICE_SESSION_ID") or None,
        )
    return default_return


def extract_service_from_path(path: str) -> str:
    """Helper: Extracts 'actions' from '/v1/actions/get_kafka_info'."""
    # If path is empty or not a string, return empty string for safe fallback
    if not path or not isinstance(path, str):
        return ""

    # Split the path and remove empty strings
    parts = [p for p in path.split("/") if p]

    if len(parts) >= 2:
        return parts[1]  # e.g., ['v1', 'actions', 'get_kafka_info'] -> 'actions'
    # safety fall back for short paths that might just be '/actions' or 'actions'
    elif len(parts) == 1:
        return parts[0]

    return ""  # Return "" so 'path_service or ENV' works perfectly


def log_errors(func=None, default_return=None, raise_exception=False, log_error=True, service_name: str = "py_common"):
    """Decorator to automatically log exceptions with dynamic path-based service detection."""

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                final_service_name = service_name

                # 1. FIND THE PATH
                path = kwargs.get("path", "")

                # If kwargs didn't have it, look in args[2] (common position for path in RPC calls)
                if not path:
                    # Look in 3rd position (e.g., self.send_request("GET", path))
                    if len(args) > 2 and isinstance(args[2], str) and "/" in args[2]:
                        path = args[2]
                    else:
                        path = ""  # Explicitly set to empty string if logic fails

                # 2. EXTRACT THE NAME AND OVERRIDE
                path_service = extract_service_from_path(path)

                if not path_service:
                    logging.warning(f"Could not detect service name from path '{path}' in function {func.__name__}")

                # Using the default one with a safe check if any ENV exist
                final_service_name = path_service or os.environ.get("SERVICE_NAME", service_name)

                # 4. SEND TO LOGGER
                return process_error_log(
                    error=e,
                    service_name=final_service_name,
                    default_return=default_return,
                    raise_exception=raise_exception,
                    log_error=log_error,
                )

        return wrapper

    if func is None:
        return decorator
    return decorator(func)
