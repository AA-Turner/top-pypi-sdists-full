"""Auto-generated stub for module: utils."""
from typing import Any, Dict, Optional, Tuple

from .errors import _DEDUPLICATION_ENABLED, _ERROR_CACHE_MAX, _ERROR_CACHE_TTL, _ERROR_TYPE_MAP, ERROR_TYPE_TO_MESSAGE, AppError, ErrorLog, ErrorType, LoggingIntegration, SentryConfig, _error_cache, _error_cache_lock, _extract_error_location, _extract_function_params, _extract_http_context, _get_error_logging_producer, _get_sentry_client, _make_hashable, cacheable, configure_scope, extract_service_from_path, generate_error_dedup_key, get_deduplication_config, hash_error, log_errors, process_error_log, seen_error, send_error_log, send_sentry_log, sentry_sdk
from .metrics import BenchmarkMetrics
from .packaging import _INSTALLED_THIS_PROCESS, _acquire_install_lock, _install_package, _is_package_installed, _release_install_lock, dependencies_check

# Constants
logger: Any

# Functions
def check_for_duplicate(session: Any, service: str, name: str) -> Tuple[Any, Optional[str], str]:
    """
    Check if an item with the given name already exists for the specified service.
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
