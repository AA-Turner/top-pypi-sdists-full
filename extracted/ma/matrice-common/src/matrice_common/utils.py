"""Utility functions for the Matrice package."""

import os
import sys
import json
import traceback
import subprocess
import logging
import inspect
import base64
import hashlib
from datetime import datetime, timezone
from functools import lru_cache, wraps
from typing import Any, List, Optional, Dict, Final
import threading
import time
from importlib.metadata import PackageNotFoundError, version

try:
    import sentry_sdk
    from sentry_sdk import configure_scope
    from sentry_sdk.integrations.logging import LoggingIntegration
except ImportError:
    subprocess.run(
        [sys.executable, "-m", "pip", "install", "--upgrade", "sentry-sdk"],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )
    import sentry_sdk
    from sentry_sdk import configure_scope
    from sentry_sdk.integrations.logging import LoggingIntegration

class SentryConfig:
    def __init__(
        self,
        dsn: str,
        environment: str = "dev",
        sample_rate: float = 1.0,
        debug: bool = False,
        service_name: str = "py_common",
        enable_tracing: bool = True,
    ):
        self.dsn = dsn
        self.environment = environment
        self.sample_rate = sample_rate
        self.debug = debug
        self.service_name = service_name
        self.enable_tracing = enable_tracing

class ErrorType:
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
            "createdAt": self.created_at.astimezone(timezone.utc).isoformat(timespec="milliseconds").replace("+00:00", "Z"),
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
    elif hasattr(obj, '__dict__') and not isinstance(obj, type):
        try:
            return ('__object__', obj.__class__.__name__, _make_hashable(obj.__dict__))
        except (AttributeError, TypeError):
            return ('__str__', str(obj))
    else:
        try:
            hash(obj)
            return obj
        except TypeError:
            return ('__str__', str(obj))

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
        "current_cache_size": len(_error_cache)
    }

# Log deduplication configuration on module import
logging.info(f"Error deduplication config: {get_deduplication_config()}")

def hash_error(*parts: str) -> str:
    """Generate a hash for error deduplication."""
    h = hashlib.sha256()
    for part in parts:
        h.update(part.encode('utf-8'))
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
    """Initialize and cache the Sentry client."""
    try:
        if hasattr(sentry_sdk, "_initialized") and sentry_sdk._initialized:
            logging.debug("Sentry client already initialized, returning cached instance")
            return sentry_sdk

        access_key = access_key or os.environ.get("MATRICE_ACCESS_KEY_ID")
        secret_key = secret_key or os.environ.get("MATRICE_SECRET_ACCESS_KEY")
        if not access_key or not secret_key:
            raise ValueError(
                "Access key and Secret key are required for Sentry initialization."
            )
        if rpc_client is None:
            from .rpc import RPC
            rpc_client = RPC(access_key=access_key, secret_key=secret_key)
        
        sentry_config_route = "/v1/monitoring/sentry_config"
        response = rpc_client.get(path=sentry_config_route, raise_exception=True)
        if not response or not response.get("success"):
            raise ValueError(f"Failed to fetch Sentry config: {response.get('message', 'No response')}")

        dsn_encoded = response["data"]["dsn"]
        try:
            dsn = base64.b64decode(dsn_encoded).decode("utf-8")
        except Exception:
            dsn = dsn_encoded

        sentry_config = SentryConfig(
            dsn=dsn,
            environment=os.environ.get("ENV") or "dev", 
            sample_rate=1.0,
            debug=False,
            service_name=service_name,
            enable_tracing=True,
        )
        sentry_sdk.init(
            dsn=sentry_config.dsn,
            environment=sentry_config.environment,
            traces_sample_rate=sentry_config.sample_rate,
            debug=sentry_config.debug,
            integrations=[
                LoggingIntegration(
                    level=None,  # Disable automatic logging capture
                    event_level=None  # Disable automatic event creation from logs
                )
            ],
            before_send=lambda event, hint: event
        )
        setattr(sentry_sdk, "_initialized", True)
        logging.info("Sentry client initialized successfully")
        return sentry_sdk
    except Exception as e:
        logging.error(f"Failed to initialize Sentry: {str(e)}")
        return None

@lru_cache(maxsize=1)
def _get_error_logging_producer(rpc_client=None, access_key=None, secret_key=None):
    """Get the Kafka producer for error logging, fetching config via RPC."""
    try:
        try:
            from confluent_kafka import Producer
        except ImportError:
            import subprocess, sys
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
        return Producer({
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
        })
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
    """Log error to Sentry as an exception.
    
    Note: Deduplication is now handled at the process_error_log level.
    This function should only be called after deduplication checks have passed.
    """
    try:
        sentry_client = _get_sentry_client(service_name=service_name)
        if not sentry_client:
            logging.warning("Sentry client not initialized, skipping Sentry logging")
            return
        with configure_scope() as scope:
            scope.set_tag("service", service_name)
            scope.set_tag("error_type", error_type)
            scope.set_tag("function", function_name)
            scope.set_extra("filename", filename)
            scope.set_extra("stacktrace", traceback_str or "")
            scope.set_extra("action_id", action_id or "N/A")
            scope.set_extra("session_id", session_id or "N/A")
            scope.set_extra("additional_info", additional_info or {})
            scope.set_extra("client_ip", "N/A")
            scope.set_extra("headers", {})
            if additional_info and "latency_ms" in additional_info:
                scope.set_extra("latency_ms", additional_info["latency_ms"])
            event_id = sentry_client.capture_exception(Exception(error_message))
            logging.info(f"Sentry event logged: {event_id}")
            return event_id
    except Exception as e:
        logging.error(f"Failed to send error log to Sentry: {str(e)}")


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
                value=json.dumps(error_log.to_dict()).encode('utf-8'),
                key=service_name.encode('utf-8')
            )
        # NOTE:
        
        # producer.flush()
    except Exception as e:
        logging.error(f"Failed to send error log to Kafka: {str(e)}")

def process_error_log(
    error: Exception,
    service_name: str = "py_common",
    default_return=None,
    raise_exception: bool = False,
    log_error: bool = True
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
    
    # Map Python exception types to ErrorType constants
    error_type_map = {
        'ValueError': ErrorType.VALUE_ERROR,
        'TypeError': ErrorType.TYPE_ERROR,
        'IndexError': ErrorType.INDEX_ERROR,
        'KeyError': ErrorType.KEY_ERROR,
        'AttributeError': ErrorType.ATTRIBUTE_ERROR,
        'ImportError': ErrorType.IMPORT_ERROR,
        'FileNotFoundError': ErrorType.FILE_NOT_FOUND,
        'PermissionError': ErrorType.PERMISSION_DENIED,
        'ConnectionError': ErrorType.CONNECTION_ERROR,
        'JSONDecodeError': ErrorType.JSON_DECODE_ERROR,
        'AssertionError': ErrorType.ASSERTION_ERROR,
        'RuntimeError': ErrorType.RUNTIME_ERROR,
        'MemoryError': ErrorType.MEMORY_ERROR,
        'OSError': ErrorType.OS_ERROR,
        'StopIteration': ErrorType.STOP_ITERATION,
        'TimeoutError': ErrorType.TIMEOUT,
    }
    
    error_class_name = type(error).__name__
    error_type = error_type_map.get(error_class_name, ErrorType.INTERNAL)

    tb = error.__traceback__
    if tb is not None:
        while tb.tb_next:
            tb = tb.tb_next
        frame = tb.tb_frame
        func_name = frame.f_code.co_name
        func_file = os.path.abspath(frame.f_code.co_filename)
        lineno = tb.tb_lineno
    else:
        # Fallback to inspect.currentframe() when no traceback
        frame = None
        func_name = "unknown_function"
        func_file = "unknown_file"
        lineno = -1

        try:
            # Walk up the call stack to find the caller (skip process_error_log frames)
            current_frame = inspect.currentframe()
            if current_frame is not None:
                # Skip current frame (process_error_log)
                caller_frame = current_frame.f_back

                # Walk up to find first frame outside utils.py
                while caller_frame is not None:
                    caller_file = os.path.abspath(caller_frame.f_code.co_filename)
                    if 'utils.py' not in caller_file:
                        func_name = caller_frame.f_code.co_name
                        func_file = caller_file
                        lineno = caller_frame.f_lineno
                        frame = caller_frame
                        break
                    caller_frame = caller_frame.f_back

                logging.debug(f"Extracted caller info from stack: {func_file}:{lineno} in {func_name}")
        except Exception as frame_error:
            logging.debug(f"Could not extract caller frame: {frame_error}")
            # Keep defaults: unknown_function, unknown_file, -1

    # Include whether info came from traceback or frame inspection
    info_source = "traceback" if tb is not None else "frame inspection"
    logging.info(f"Processing error from {func_file}:{lineno}, function '{func_name}' (via {info_source}): {str(error)}")

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

    param_str = "unavailable"
    try:
        if frame:
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
            param_str = ", ".join(params) if params else "no parameters"
        else:
            param_str = "no frame available"
    except Exception as param_error:
        logging.debug(f"Parameter extraction failed: {param_error}")
        param_str = "unable to extract parameters"

    logging.info(f"Function parameters: {param_str}")

    error_msg = f"Exception in {func_file}:{lineno}, function '{func_name}' (via {info_source}): {str(error)}"
    logging.error(error_msg)

    additional_info = {
        "parameters": param_str,
        "latency_ms": int((time.time() - start_time) * 1000),
    }

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


def log_errors(func=None, default_return=None, raise_exception=False, log_error=True, service_name: str = "py_common"):
    """Decorator to automatically log exceptions using process_error_log."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                return process_error_log(
                    error=e,
                    # func=func,
                    service_name=service_name,
                    default_return=default_return,
                    raise_exception=raise_exception,
                    log_error=log_error
                )
        return wrapper
    if func is None:
        return decorator
    return decorator(func)


def handle_response(response, success_message, failure_message):
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

def check_for_duplicate(session, service, name):
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

def get_summary(session, project_id, service_name):
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
    return handle_response(
        resp,
        success_messages.get(service_name, "Operation successful"),
        error_messages.get(service_name, "Operation failed"),
    )

def _is_package_installed(package_name):
    """Check if a package is already installed."""
    try:
        version(package_name.replace('-', '_'))
        return True
    except (ImportError, OSError, PackageNotFoundError):
        return False

@lru_cache(maxsize=64)
def _install_package(package_name):
    """Helper function to install a package using subprocess."""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", package_name],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
        logging.info("Successfully installed %s", package_name)
        return True
    except subprocess.CalledProcessError as exc:
        logging.error("Failed to install %s: %s", package_name, exc)
        return False
    except Exception as e:
        logging.error("Unexpected error installing %s: %s", package_name, str(e))
        return False

def dependencies_check(package_names):
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