"""Auto-generated stub for module: utils."""
from typing import Any, Dict, List, Optional, Tuple, Union

from .rpc import RPC

# Constants
ERROR_TYPE_TO_MESSAGE: Dict[Any, Any]
LoggingIntegration: None
configure_scope: None
logger: Any
sentry_sdk: None

# Functions
def cacheable(f: Any) -> Any:
    """
    Wraps a function to make its args hashable before caching.
    """
    ...
def check_for_duplicate(session: Any, service: str, name: str) -> Tuple[Any, Optional[str], str]:
    """
    Check if an item with the given name already exists for the specified service.
    """
    ...
def dependencies_check(package_names: Union[List[str], str]) -> None:
    """
    Check and install required dependencies.
    """
    ...
def extract_service_from_path(path: str) -> str:
    """
    Helper: Extracts 'actions' from '/v1/actions/get_kafka_info'.
    """
    ...
def generate_error_dedup_key(error_type: str, filename: str, function_name: str, service_name: str) -> str:
    """
    Generate a consistent deduplication key based on error location and type, not message content.
    
        This ensures the same error from the same location is not logged multiple times,
        regardless of slight variations in error messages.
    """
    ...
def get_deduplication_config() -> dict:
    """
    Get the current deduplication configuration.
    """
    ...
def get_summary(session: Any, project_id: str, service_name: str) -> Tuple[Any, Optional[str]]:
    """
    Fetch a summary of the specified service in the project.
    """
    ...
def handle_response(response: Optional[Dict[str, Any]], success_message: str, failure_message: str) -> Tuple[Any, Optional[str], str]:
    """
    Handle API response and return appropriate result.
    """
    ...
def hash_error(*parts: Any) -> str:
    """
    Generate a hash for error deduplication.
    """
    ...
def log_errors(func: Any = None, default_return: Any = None, raise_exception: Any = False, log_error: Any = True, service_name: str = 'py_common') -> Any:
    """
    Decorator to automatically log exceptions with dynamic path-based service detection.
    """
    ...
def process_error_log(error: Any, service_name: str = 'py_common', default_return: Any = None, raise_exception: bool = False, log_error: bool = True) -> Any:
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
    ...
def seen_error(hash_str: str) -> bool:
    """
    Check if an error has been seen recently, and update cache.
    
        This function is thread-safe and atomically checks and updates the cache
        to prevent race conditions where multiple threads might log the same error.
    """
    ...
def send_error_log(filename: str, function_name: str, error_message: str, traceback_str: Optional[str] = None, additional_info: Optional[dict] = None, error_type: str = ErrorType.INTERNAL, service_name: str = 'py_common', action_id: Optional[str] = None, session_id: Optional[str] = None, access_key: Optional[str] = None, secret_key: Optional[str] = None, sentryIssueLink: Optional[str] = None) -> Any:
    """
    Log error to the backend system, sending to Kafka.
    
        Note: Deduplication is now handled at the process_error_log level.
        This function should only be called after deduplication checks have passed.
    """
    ...
def send_sentry_log(filename: str, function_name: str, error_message: str, traceback_str: Optional[str] = None, additional_info: Optional[dict] = None, error_type: str = ErrorType.INTERNAL, service_name: str = 'py_common', action_id: Optional[str] = None, session_id: Optional[str] = None) -> Any:
    """
    Sentry is disabled — this is a no-op stub.
    """
    ...

# Classes
class AppError(Exception):
    def __init__(self: Any, error_type: str, error: Any, service_name: str, details: Optional[List[Any]] = None, action_id: Optional[str] = None, session_id: Optional[str] = None) -> None: ...

    def append(self: Any, *details: Any) -> 'Any': ...

    def generate_hash(self: Any) -> str: ...

class BenchmarkMetrics:
    # Accumulates per-stage timing samples with zero overhead when disabled.
    #
    #     When enabled=False, all methods return immediately with no allocations.
    #     When enabled=True, tracks sum/count/min/max/samples per named stage.
    #
    #     Usage::
    #
    #         bm = BenchmarkMetrics(enabled=True)
    #         t = bm.start()
    #         # ... do work ...
    #         bm.record("stage_name", t)
    #
    #         # Periodic reporting:
    #         print(bm.get_breakdown_str("My Title", interval_seconds=5.0, total_items=100))
    #         bm.reset()

    def __init__(self: Any, enabled: bool = False) -> None: ...

    def get_breakdown_str(self: Any, title: str = 'BENCHMARK METRICS', interval_seconds: float = 0.0, total_items: int = 0, item_label: str = 'frames') -> str:
        """
        Format a multi-line log string with per-stage breakdown.
        
                Args:
                    title: Header line for the metrics block.
                    interval_seconds: Wall-clock seconds for the reporting interval.
                        Used to compute throughput (items/sec) per stage.
                    total_items: Total items processed in the interval (e.g. frames, batches).
                    item_label: Label for the items (e.g. "frames", "batches").
        """
        ...

    def record(self: Any, stage_name: str, start_time: float) -> float:
        """
        Record elapsed time since start_time for the named stage.
                Returns elapsed seconds. No-op if disabled.
        """
        ...

    def record_value(self: Any, stage_name: str, value_seconds: float) -> Any:
        """
        Record a pre-computed value in seconds.
        """
        ...

    def reset(self: Any) -> Any:
        """
        Reset all accumulators for the next reporting interval.
        """
        ...

    def start(self: Any) -> float:
        """
        Return current time if enabled, else 0.0.
        """
        ...

class ErrorLog:
    def __init__(self: Any, service_name: str, stack_trace: str, error_type: str, description: str, file_name: str, function_name: str, hash: str, action_record_id: Optional[str] = None, created_at: Optional[Any] = None, is_resolved: bool = False, more_info: Optional[Any] = None, sentryIssueLink: Optional[str] = None) -> None: ...

    def to_dict(self: Any) -> dict: ...

class ErrorType:
    # Constants for error type classification in error logging.

    INTERNAL: object = ...
class SentryConfig:
    # Configuration for Sentry error reporting.

    def __init__(self: Any, dsn: str, environment: str = 'dev', sample_rate: float = 1.0, debug: bool = False, service_name: str = 'py_common', enable_tracing: bool = True) -> None: ...

