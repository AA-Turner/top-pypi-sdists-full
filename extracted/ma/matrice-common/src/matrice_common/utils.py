"""Utility functions for the Matrice package."""

import base64
import hashlib
import inspect
import json
import logging
import os
import subprocess
import sys
import threading
import time
import traceback
from datetime import datetime, timezone
from functools import lru_cache, wraps
from importlib.metadata import PackageNotFoundError, version
from typing import Any, Dict, Final, List, Optional, Tuple, Union

logger = logging.getLogger(__name__)

# Sentry SDK disabled — all Sentry calls are no-ops.
# To re-enable, restore the sentry_sdk imports and remove the stubs below.
sentry_sdk = None
configure_scope = None
LoggingIntegration = None


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
_DEDUPLICATION_ENABLED = True


def get_deduplication_config() -> dict:
    """Get the current deduplication configuration."""
    return {
        "enabled": _DEDUPLICATION_ENABLED,
        "ttl_seconds": _ERROR_CACHE_TTL,
        "max_cache_size": _ERROR_CACHE_MAX,
        "current_cache_size": len(_error_cache),
    }


# Log deduplication configuration on module import
logging.info(f"Error deduplication config: {get_deduplication_config()}")


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
    with _error_cache_lock:
        # Proactive cache cleanup: remove stale entries on every call if needed
        if len(_error_cache) > _ERROR_CACHE_MAX * 0.8:  # Start cleanup at 80% capacity
            stale_keys = [k for k, t in _error_cache.items() if now - t > _ERROR_CACHE_TTL]
            for k in stale_keys:
                del _error_cache[k]
            if stale_keys:
                logging.debug(f"Cleaned up {len(stale_keys)} stale error cache entries")

        # Atomic check and update: prevents race condition where multiple threads
        # could pass the check before any of them updates the cache
        if hash_str in _error_cache:
            time_since_last_log = now - _error_cache[hash_str]
            if time_since_last_log <= _ERROR_CACHE_TTL:
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
        try:
            from confluent_kafka import Producer
        except ImportError:
            import subprocess
            import sys

            logging.warning("confluent-kafka not found. Installing automatically...")
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", "confluent-kafka"],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
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
        producer = _get_error_logging_producer()
        if producer:
            producer.produce(
                topic="error_logs",
                value=json.dumps(error_log.to_dict()).encode("utf-8"),
                key=service_name.encode("utf-8"),
            )
        # NOTE:

        # producer.flush()
    except Exception as e:
        logging.error(f"Failed to send error log to Kafka: {str(e)}")


def _extract_error_location(error: Exception) -> Tuple:
    """Extract file, function, line number and frame from an exception.

    Returns:
        Tuple of (frame, func_name, func_file, lineno, info_source)
    """
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
    """Extract function parameter string from a frame object."""
    if not frame:
        return "no frame available"
    try:
        arg_info = inspect.getargvalues(frame)
        params = []
        for name in arg_info.args:
            value = arg_info.locals.get(name, "<not found>")
            val_repr = repr(value)
            if len(val_repr) > 120:
                val_repr = val_repr[:117] + "..."
            params.append(f"{name}={val_repr}")
        if arg_info.varargs:
            params.append(f"*{arg_info.varargs}={arg_info.locals.get(arg_info.varargs)}")
        if arg_info.keywords:
            params.append(f"**{arg_info.keywords}={arg_info.locals.get(arg_info.keywords)}")
        return ", ".join(params) if params else "no parameters"
    except Exception as param_error:
        logging.debug(f"Parameter extraction failed: {param_error}")
        return "unable to extract parameters"


def _extract_http_context(frame) -> Optional[Dict[str, str]]:
    """Extract HTTP request context from frame locals for debugging."""
    if not frame:
        return None
    try:
        locals_dict = frame.f_locals
        http_context = {}
        for key in ("method", "request_url", "payload", "data", "curl_cmd"):
            if key in locals_dict and locals_dict[key]:
                val_str = str(locals_dict[key])
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

    # ========== DEDUPLICATION CHECK (MOVED TO TOP LEVEL) ==========
    # Check deduplication ONCE here, before any logging happens
    if log_error and _DEDUPLICATION_ENABLED:
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
            sentry_event_id = send_sentry_log(
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
            logging.error(f"Failed to log error to Sentry: {str(sentry_error)}")

        sentry_link = (
            f"https://sentry.io/organizations/matrice-ai-inc/issues/?query={sentry_event_id}"
            if sentry_event_id
            else None
        )

        # ========== LOG TO KAFKA ==========
        try:
            send_error_log(
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
            logging.error(f"Failed to log error to Kafka: {str(logging_error)}")

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
                    # func=func,
                    service_name=final_service_name,
                    default_return=default_return,
                    raise_exception=raise_exception,
                    log_error=log_error,
                )

        return wrapper

    if func is None:
        return decorator
    return decorator(func)


def handle_response(
    response: Optional[Dict[str, Any]],
    success_message: str,
    failure_message: str,
) -> Tuple[Any, Optional[str], str]:
    """Handle API response and return appropriate result."""
    if response and response.get("success"):
        result = response.get("data")
        error = None
        message = success_message
    else:
        result = None
        error = response.get("message") if response else "No response received"
        message = failure_message
    return result, error, message


def check_for_duplicate(session: Any, service: str, name: str) -> Tuple[Any, Optional[str], str]:
    """Check if an item with the given name already exists for the specified service."""
    service_config = {
        "dataset": {
            "path": f"/v1/dataset/check_for_duplicate?datasetName={name}",
            "item_name": "Dataset",
        },
        "annotation": {
            "path": f"/v1/annotations/check_for_duplicate?annotationName={name}",
            "item_name": "Annotation",
        },
        "model_export": {
            "path": f"/v1/model/model_export/check_for_duplicate?modelExportName={name}",
            "item_name": "Model export",
        },
        "model": {
            "path": f"/v1/model/model_train/check_for_duplicate?modelTrainName={name}",
            "item_name": "Model Train",
        },
        "projects": {
            "path": f"/v1/project/check_for_duplicate?name={name}",
            "item_name": "Project",
        },
        "deployment": {
            "path": f"/v1/inference/check_for_duplicate?deploymentName={name}",
            "item_name": "Deployment",
        },
    }
    if service not in service_config:
        return (
            None,
            f"Invalid service: {service}",
            "Service not supported",
        )
    config = service_config[service]
    resp = session.rpc.get(path=config["path"])
    if resp and resp.get("success"):
        if resp.get("data") == "true":
            return handle_response(
                resp,
                f"{config['item_name']} with this name already exists",
                f"Could not check for this {service} name",
            )
        return handle_response(
            resp,
            f"{config['item_name']} with this name does not exist",
            f"Could not check for this {service} name",
        )
    return handle_response(
        resp,
        "",
        f"Could not check for this {service} name",
    )


def get_summary(session: Any, project_id: str, service_name: str) -> Tuple[Any, Optional[str]]:
    """Fetch a summary of the specified service in the project."""
    service_paths = {
        "annotations": "/v1/annotations/summary",
        "models": "/v1/model/summary",
        "exports": "/v1/model/summaryExported",
        "deployments": "/v1/inference/summary",
    }
    success_messages = {
        "annotations": "Annotation summary fetched successfully",
        "models": "Model summary fetched successfully",
        "exports": "Model Export Summary fetched successfully",
        "deployments": "Deployment summary fetched successfully",
    }
    error_messages = {
        "annotations": "Could not fetch annotation summary",
        "models": "Could not fetch models summary",
        "exports": "Could not fetch models export summary",
        "deployments": "An error occurred while trying to fetch deployment summary.",
    }
    if service_name not in service_paths:
        return (
            None,
            f"Invalid service name: {service_name}",
        )
    path = f"{service_paths[service_name]}?projectId={project_id}"
    resp = session.rpc.get(path=path)
    result, error, _message = handle_response(
        resp,
        success_messages.get(service_name, "Operation successful"),
        error_messages.get(service_name, "Operation failed"),
    )
    return result, error


# Names this interpreter has already successfully installed — short-circuits
# in-process repeat calls without touching the cross-process lock.
_INSTALLED_THIS_PROCESS: set = set()


def _acquire_install_lock():
    """Acquire an exclusive cross-process file lock for pip install.

    Returns the fd holding the lock, or None if locking is unavailable
    (Windows / no fcntl / lockfile-create failure). Callers must pair a
    non-None return with `_release_install_lock(fd)` in a finally.

    Why: multiple sibling Python interpreters sharing one venv can race
    inside pip's wheel installer when each runs `dependencies_check` at
    import time, corrupting site-packages (.dist-info, .pth). The lock is
    keyed to the venv root (`sys.prefix`) so independent venvs stay
    independent.
    """
    lock_dir = os.path.join(sys.prefix, "var", "lock")
    try:
        os.makedirs(lock_dir, exist_ok=True)
    except OSError:
        lock_dir = os.path.join(os.path.expanduser("~"), ".cache", "matrice")
        try:
            os.makedirs(lock_dir, exist_ok=True)
        except OSError as exc:
            logging.warning(
                "Could not create install lock dir at %s (%s); running pip without cross-process serialization",
                lock_dir,
                exc,
            )
            return None
    lock_path = os.path.join(lock_dir, "matrice_deps.lock")

    try:
        import fcntl  # POSIX-only
    except ImportError:
        logging.debug("fcntl unavailable; running pip install without cross-process lock")
        return None

    fd = None
    try:
        fd = os.open(lock_path, os.O_CREAT | os.O_RDWR, 0o600)
        fcntl.flock(fd, fcntl.LOCK_EX)
        return fd
    except OSError as exc:
        if fd is not None:
            try:
                os.close(fd)
            except OSError:
                pass
        logging.warning(
            "Could not acquire install lock at %s (%s); running pip without cross-process serialization",
            lock_path,
            exc,
        )
        return None


def _release_install_lock(fd):
    """Release a lock acquired by `_acquire_install_lock` and close its fd."""
    if fd is None:
        return
    try:
        import fcntl

        fcntl.flock(fd, fcntl.LOCK_UN)
    except (ImportError, OSError):
        pass
    finally:
        try:
            os.close(fd)
        except OSError:
            pass


def _is_package_installed(package_name):
    """Check if a package is already installed."""
    try:
        version(package_name.replace("-", "_"))
        return True
    except (ImportError, OSError, PackageNotFoundError):
        return False


def _install_package(package_name):
    """Install a package via `pip install --upgrade`, serialized cross-process.

    Holds an exclusive venv-keyed file lock for the duration of the pip
    subprocess so sibling interpreters cannot race inside the wheel
    installer. Re-checks installed state inside the critical section so
    a sibling that just finished installing the same package
    short-circuits this caller.
    """
    if package_name in _INSTALLED_THIS_PROCESS:
        return True
    lock_fd = _acquire_install_lock()
    try:
        if _is_package_installed(package_name):
            _INSTALLED_THIS_PROCESS.add(package_name)
            return True
        try:
            subprocess.run(
                [sys.executable, "-m", "pip", "install", "--upgrade", package_name],
                check=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
            logging.info("Successfully installed %s", package_name)
            _INSTALLED_THIS_PROCESS.add(package_name)
            return True
        except subprocess.CalledProcessError as exc:
            logging.error("Failed to install %s: %s", package_name, exc)
            return False
        except Exception as e:
            logging.error("Unexpected error installing %s: %s", package_name, str(e))
            return False
    finally:
        _release_install_lock(lock_fd)


def dependencies_check(package_names: Union[List[str], str]) -> None:
    """Check and install required dependencies."""
    if not isinstance(package_names, list):
        package_names = [package_names]
    success = True
    for package_name in package_names:
        if _is_package_installed(package_name):
            logging.debug(f"Package {package_name} is already installed, skipping installation")
            continue
        if not _install_package(package_name):
            success = False
    return success


# =============================================================================
# Benchmark Metrics Utility
# =============================================================================


class BenchmarkMetrics:
    """Accumulates per-stage timing samples with zero overhead when disabled.

    When enabled=False, all methods return immediately with no allocations.
    When enabled=True, tracks sum/count/min/max/samples per named stage.

    Usage::

        bm = BenchmarkMetrics(enabled=True)
        t = bm.start()
        # ... do work ...
        bm.record("stage_name", t)

        # Periodic reporting:
        print(bm.get_breakdown_str("My Title", interval_seconds=5.0, total_items=100))
        bm.reset()
    """

    __slots__ = ("enabled", "_stages", "_order")

    def __init__(self, enabled: bool = False):
        self.enabled = enabled
        self._stages: Dict[str, List[float]] = {}
        self._order: List[str] = []  # preserves insertion order for display

    def start(self) -> float:
        """Return current time if enabled, else 0.0."""
        if not self.enabled:
            return 0.0
        return time.perf_counter()

    def record(self, stage_name: str, start_time: float) -> float:
        """Record elapsed time since start_time for the named stage.
        Returns elapsed seconds. No-op if disabled."""
        if not self.enabled:
            return 0.0
        elapsed = time.perf_counter() - start_time
        self._accumulate(stage_name, elapsed)
        return elapsed

    def record_value(self, stage_name: str, value_seconds: float):
        """Record a pre-computed value in seconds."""
        if not self.enabled:
            return
        self._accumulate(stage_name, value_seconds)

    def _accumulate(self, name: str, value: float):
        if name not in self._stages:
            self._stages[name] = []
            self._order.append(name)
        self._stages[name].append(value)

    def _percentile(self, sorted_samples: List[float], p: float) -> float:
        """Compute percentile from sorted samples."""
        n = len(sorted_samples)
        if n == 0:
            return 0.0
        idx = p / 100.0 * (n - 1)
        lo = int(idx)
        hi = min(lo + 1, n - 1)
        frac = idx - lo
        return sorted_samples[lo] * (1 - frac) + sorted_samples[hi] * frac

    def get_breakdown_str(
        self,
        title: str = "BENCHMARK METRICS",
        interval_seconds: float = 0.0,
        total_items: int = 0,
        item_label: str = "frames",
    ) -> str:
        """Format a multi-line log string with per-stage breakdown.

        Args:
            title: Header line for the metrics block.
            interval_seconds: Wall-clock seconds for the reporting interval.
                Used to compute throughput (items/sec) per stage.
            total_items: Total items processed in the interval (e.g. frames, batches).
            item_label: Label for the items (e.g. "frames", "batches").
        """
        if not self._stages:
            return ""

        lines = [
            f"\n{'=' * 70}",
            f"{title}",
            f"{'=' * 70}",
        ]

        # Throughput summary if caller provides interval info
        if interval_seconds > 0 and total_items > 0:
            throughput = total_items / interval_seconds
            lines.append(
                f"  THROUGHPUT: {total_items:,} {item_label} in {interval_seconds:.1f}s "
                f"= {throughput:,.1f} {item_label}/sec"
            )
            lines.append("")

        lines.append("  STAGE LATENCIES:")

        # Compute total time across all stages for % breakdown
        stage_avgs: Dict[str, float] = {}
        total_avg = 0.0
        for name in self._order:
            samples = self._stages[name]
            avg = sum(samples) / len(samples) if samples else 0.0
            stage_avgs[name] = avg
            total_avg += avg

        max_name_len = max(len(n) for n in self._order) if self._order else 10

        for name in self._order:
            samples = self._stages[name]
            if not samples:
                continue
            n = len(samples)
            avg = sum(samples) / n
            mn = min(samples)
            mx = max(samples)
            sorted_s = sorted(samples)
            p50 = self._percentile(sorted_s, 50)
            p95 = self._percentile(sorted_s, 95)
            p99 = self._percentile(sorted_s, 99)
            pct = (avg / total_avg * 100) if total_avg > 0 else 0

            # Compute per-stage throughput: how many items/sec this stage alone could sustain
            stage_throughput_str = ""
            if avg > 0:
                max_throughput = 1.0 / avg
                stage_throughput_str = f"  max={max_throughput:,.0f}/s"

            lines.append(
                f"  {name:<{max_name_len}}  "
                f"avg={avg * 1000:7.2f}ms  "
                f"p50={p50 * 1000:7.2f}  p95={p95 * 1000:7.2f}  p99={p99 * 1000:7.2f}  "
                f"({pct:5.1f}%){stage_throughput_str}  n={n}"
            )

        if total_avg > 0:
            total_max_throughput = 1.0 / total_avg
            lines.append(
                f"  {'TOTAL':<{max_name_len}}  "
                f"avg={total_avg * 1000:7.2f}ms  "
                f"max={total_max_throughput:,.0f}/s (serial bottleneck)"
            )

        lines.append(f"{'=' * 70}")
        return "\n".join(lines)

    def reset(self):
        """Reset all accumulators for the next reporting interval."""
        self._stages.clear()
        self._order.clear()
