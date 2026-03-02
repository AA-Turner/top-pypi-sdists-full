"""Auto-generated stub for module: utils."""
from typing import Any, Dict, List, Optional

from .rpc import RPC
from .rpc import RPC

# Constants
ERROR_TYPE_TO_MESSAGE: Dict[Any, Any]

# Functions
def cacheable(f: Any) -> Any:
    """
    Wraps a function to make its args hashable before caching.
    """
    ...
def check_for_duplicate(session: Any, service: Any, name: Any) -> Any:
    """
    Check if an item with the given name already exists for the specified service.
    """
    ...
def dependencies_check(package_names: Any) -> Any:
    """
    Check and install required dependencies.
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
def get_summary(session: Any, project_id: Any, service_name: Any) -> Any:
    """
    Fetch a summary of the specified service in the project.
    """
    ...
def handle_response(response: Any, success_message: Any, failure_message: Any) -> Any:
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
    Decorator to automatically log exceptions using process_error_log.
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
    Log error to Sentry as an exception.
    
        Note: Deduplication is now handled at the process_error_log level.
        This function should only be called after deduplication checks have passed.
    """
    ...

# Classes
class AppError(Exception):
    def __init__(self: Any, error_type: str, error: Any, service_name: str, details: Optional[List[Any]] = None, action_id: Optional[str] = None, session_id: Optional[str] = None) -> None: ...

    def append(self: Any, *details: Any) -> 'Any': ...

    def generate_hash(self: Any) -> str: ...

class ErrorLog:
    def __init__(self: Any, service_name: str, stack_trace: str, error_type: str, description: str, file_name: str, function_name: str, hash: str, action_record_id: Optional[str] = None, created_at: Optional[Any] = None, is_resolved: bool = False, more_info: Optional[Any] = None, sentryIssueLink: Optional[str] = None) -> None: ...

    def to_dict(self: Any) -> dict: ...

class ErrorType:
    INTERNAL: object = ...
class SentryConfig:
    def __init__(self: Any, dsn: str, environment: str = 'dev', sample_rate: float = 1.0, debug: bool = False, service_name: str = 'py_common', enable_tracing: bool = True) -> None: ...

