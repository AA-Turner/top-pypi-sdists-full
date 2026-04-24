#  IBM Confidential
#  PID 5900-BAF
#  Copyright StreamSets Inc., an IBM Company 2025

"""HTTPError Retry logic."""

# fmt: off
import copy
import functools
import inspect
import logging
import random
import threading
import time
from contextlib import contextmanager
from dataclasses import dataclass
from typing import Any, Callable, Dict, Iterator, Optional, Set

import requests

# fmt: on

logger = logging.getLogger(__name__)

# Configuration limits and constants
MAX_ATTEMPTS_LIMIT = 50
MAX_TIME_LIMIT = 3600.0  # 1 hour
MAX_INIT_DELAY = 300.0  # 5 minutes
MAX_EXP_FACTOR = 10.0
MAX_DELAY = 60.0  # Maximum delay between retries
JITTER_FACTOR = 0.25  # ±25% randomness in delays


@dataclass
class RetrySettings:
    """Configuration for retry behavior."""

    max_attempts: int = 3
    max_time: Optional[float] = None
    init_delay: float = 1.0
    exp_factor: float = 2.0
    jitter: bool = True

    def __post_init__(self):
        """Validate retry settings values."""
        if not isinstance(self.max_attempts, int) or self.max_attempts < 1:
            raise ValueError(f"max_attempts must be a positive integer, got: {self.max_attempts}")
        if self.max_attempts > MAX_ATTEMPTS_LIMIT:
            raise ValueError(f"max_attempts cannot exceed {MAX_ATTEMPTS_LIMIT}, got: {self.max_attempts}")

        if self.max_time is not None:
            if not isinstance(self.max_time, (int, float)) or self.max_time <= 0:
                raise ValueError(f"max_time must be a positive number, got: {self.max_time}")
            if self.max_time > MAX_TIME_LIMIT:
                raise ValueError(f"max_time cannot exceed {MAX_TIME_LIMIT} seconds, got: {self.max_time}")

        if not isinstance(self.init_delay, (int, float)) or self.init_delay < 0:
            raise ValueError(f"init_delay must be a non-negative number, got: {self.init_delay}")
        if self.init_delay > MAX_INIT_DELAY:
            raise ValueError(f"init_delay cannot exceed {MAX_INIT_DELAY} seconds, got: {self.init_delay}")

        if not isinstance(self.exp_factor, (int, float)) or self.exp_factor < 1.0:
            raise ValueError(f"exp_factor must be >= 1.0, got: {self.exp_factor}")
        if self.exp_factor > MAX_EXP_FACTOR:
            raise ValueError(f"exp_factor cannot exceed {MAX_EXP_FACTOR}, got: {self.exp_factor}")


# Default retry configuration
DEFAULT_RETRY_SETTINGS = RetrySettings()

DEFAULT_STATUS_CONFIGS = {
    429: RetrySettings(max_attempts=10, init_delay=1.0, exp_factor=1.5),
}

DEFAULT_RETRYABLE_STATUS_CODES = {429, 500, 502, 503, 504}


def _locked(func):
    """Decorator to automatically acquire class lock."""

    @functools.wraps(func)
    def wrapper(cls, *args, **kwargs):
        with cls._lock:
            return func(cls, *args, **kwargs)

    return wrapper


class RetryConfigMeta(type):
    """Metaclass for RetryConfig, needed to create __repr__ for RetryConfig."""

    def __repr__(cls):
        """Get class attributes, excluding private/dunder attributes"""
        attr_names = getattr(cls, '_repr_attrs', [])

        attrs = []
        for key in attr_names:
            if hasattr(cls, key):
                value = getattr(cls, key)
                attrs.append(f"{key}={repr(value)}")
        return f"{cls.__name__}({', '.join(attrs)})"


class RetryConfig(metaclass=RetryConfigMeta):
    """Global retry configuration - class-only interface.

    Available Operations:
        enable()  - Enable retries (previous config or defaults)
        disable() - Disable all retries temporarily
        reset()   - Reset to factory defaults

        set()     - Replace entire configuration
        add()     - Add status codes or configurations
        remove()  - Remove status codes or configurations

        show()                 - Display current configuration
        get_current_config()   - Get current configuration as dict
    """

    _repr_attrs = ['default', 'retryable_status_codes', 'status_configs']

    default = DEFAULT_RETRY_SETTINGS
    status_configs = DEFAULT_STATUS_CONFIGS.copy()
    retryable_status_codes = DEFAULT_RETRYABLE_STATUS_CODES.copy()
    _last_config = None
    _lock = threading.Lock()

    def __init__(self):
        raise RuntimeError("RetryConfig should not be instantiated. Use class methods directly.")

    @classmethod
    @_locked
    def enable(cls, use_defaults: bool = False) -> None:
        """Enable retries.

        Args:
            use_defaults: If True, use default configuration,
                          If False use previous enabled configuration
        """
        if use_defaults or cls._last_config is None:
            cls.default = DEFAULT_RETRY_SETTINGS
            cls.status_configs = DEFAULT_STATUS_CONFIGS.copy()
            cls.retryable_status_codes = DEFAULT_RETRYABLE_STATUS_CODES.copy()
        else:
            cls.default = cls._last_config['default']
            cls.status_configs = cls._last_config['status_configs']
            cls.retryable_status_codes = cls._last_config['retryable_status_codes']
            logger.debug("Restored last configuration.")

    @classmethod
    @_locked
    def disable(cls) -> None:
        """Disable all retries, saves current configuration for later restore via enable()."""
        cls._save_current_config()
        cls.default = RetrySettings(max_attempts=1)
        cls.status_configs = {}
        cls.retryable_status_codes = set()

    @classmethod
    @_locked
    def reset(cls) -> None:
        """Reset to default configuration."""
        cls.default = DEFAULT_RETRY_SETTINGS
        cls.status_configs = DEFAULT_STATUS_CONFIGS.copy()
        cls.retryable_status_codes = DEFAULT_RETRYABLE_STATUS_CODES.copy()

    @classmethod
    @_locked
    def set(
        cls,
        default: Optional[RetrySettings] = None,
        status_configs: Optional[Dict[int, RetrySettings]] = None,
        retryable_status_codes: Optional[Set[int]] = None,
    ) -> None:
        """
        Replace current configuration (overwrites existing settings).

        Args:
            default: New default retry settings (replaces current default)
            status_configs: New status-specific configurations (replaces all existing configs)
            retryable_status_codes: New set of retryable status codes (replaces existing set)

        Warning:
            This method REPLACES configurations, not adds to them.
            Use add() to add to existing configuration without removing others.

        Example:
            # Replace default settings
            >>> RetryConfig.set(default=RetrySettings(max_attempts=10))

            # Replace ALL status-specific configs (removes previous ones)
            >>> RetryConfig.set(
            ...     status_configs={
            ...         429: RetrySettings(max_attempts=20),
            ...         500: RetrySettings(max_attempts=5)
            ...     }
            ... )

            # Replace ALL retryable status codes (removes previous ones)
            >>> RetryConfig.set(retryable_status_codes={429, 500, 503})

            # Replace everything at once
            >>> RetryConfig.set(
            ...     default=RetrySettings(max_attempts=5),
            ...     status_configs={429: RetrySettings(max_attempts=15)},
            ...     retryable_status_codes={429, 500, 502, 503, 504}
            ... )
        """
        if default is not None:
            cls.default = default
        if status_configs is not None:
            cls.status_configs = status_configs
        if retryable_status_codes is not None:
            cls._validate_status_codes(retryable_status_codes)
            cls.retryable_status_codes = retryable_status_codes

    @classmethod
    @_locked
    def add(
        cls,
        status_configs: Optional[Dict[int, RetrySettings]] = None,
        retryable_status_codes: Optional[Set[int]] = None,
    ) -> None:
        """
        Add status codes and/or configurations to existing retry settings.

        Args:
            status_configs: Additional status-specific retry configurations to add/update
            retryable_status_codes: Additional status codes to mark as retryable

        Example:
            # Add new retryable status codes
            >>> RetryConfig.add(retryable_status_codes={404, 405})

            # Add specific configuration for a status code
            >>> RetryConfig.add(
            ...     status_configs={
            ...         404: RetrySettings(max_attempts=5, init_delay=2.0)
            ...     }
            ... )
        """
        if status_configs is not None:
            if not isinstance(status_configs, dict):
                raise ValueError("status_configs must be a dictionary")
            for code in status_configs.keys():
                if not isinstance(code, int) or not (300 <= code <= 599):
                    raise ValueError(f"Invalid HTTP status code: {code}")
            cls.status_configs.update(status_configs)

        if retryable_status_codes is not None:
            cls._validate_status_codes(retryable_status_codes)
            cls.retryable_status_codes.update(retryable_status_codes)

    @classmethod
    @_locked
    def remove(
        cls,
        status_configs: Optional[Set[int]] = None,
        retryable_status_codes: Optional[Set[int]] = None,
    ) -> None:
        """
        Remove status codes and/or configurations from retry settings.

        Args:
            status_configs: Set of status codes to remove from status-specific configurations
            retryable_status_codes: Set of status codes to remove from retryable list

        Example:
            # Remove status codes from retryable list
            >>> RetryConfig.remove(retryable_status_codes={404, 405})

            # Remove specific configuration (will fall back to default)
            >>> RetryConfig.remove(status_configs={429})

        Note:
            - Removing from status_configs makes that code use default settings
            - Removing from retryable_status_codes makes that code non-retryable
              (unless it's still in status_configs)
        """
        if status_configs is not None:
            if not isinstance(status_configs, set):
                raise ValueError("status_configs must be a set of status codes")
            for code in status_configs:
                cls.status_configs.pop(code, None)

        if retryable_status_codes is not None:
            cls._validate_status_codes(retryable_status_codes)
            cls.retryable_status_codes.difference_update(retryable_status_codes)

    @classmethod
    def show(cls) -> None:
        """Display current retry configuration in human-readable format.

        Example:
            >>> RetryConfig.show()
            ======================================================================
            RETRY CONFIGURATION
            STATUS: RETRIES ENABLED
            ======================================================================

            Default Settings:
            Applied to status codes: [500, 502, 503, 504]
              Max Attempts:    3
              Max Time:        None (max allowed: 3600s)
              Initial Delay:   1.0s
              Exp Factor:      2.0x
              Jitter:          Enabled
            ...
        """
        print(cls._get_display_string())

    @classmethod
    def get_current_config(cls) -> Dict[str, Any]:
        """Get current configuration as a dictionary."""
        return {
            'default': cls.default,
            'status_configs': cls.status_configs.copy(),
            'retryable_status_codes': cls.retryable_status_codes.copy(),
        }

    @classmethod
    def get_settings_for_status(cls, status_code: int) -> RetrySettings:
        """Get retry settings for a specific HTTP status code."""
        return cls.status_configs.get(status_code, cls.default)

    @classmethod
    def is_retryable_status(cls, status_code: int) -> bool:
        """Check if status code should be retried."""
        return status_code in cls.status_configs or status_code in cls.retryable_status_codes

    @staticmethod
    def _validate_status_codes(codes: Set[int]):
        """Validate HTTP status codes."""
        if not isinstance(codes, set):
            raise ValueError("retryable_status_codes must be a set")
        for code in codes:
            if not isinstance(code, int) or not (100 <= code <= 599):
                raise ValueError(f"Invalid HTTP status code: {code}")

    @classmethod
    def _save_current_config(cls):
        """Save current configuration for later restore."""
        cls._last_config = {
            'default': copy.deepcopy(cls.default),
            'status_configs': copy.deepcopy(cls.status_configs),
            'retryable_status_codes': cls.retryable_status_codes.copy(),
        }

    @classmethod
    def _get_display_string(cls) -> str:
        """
        Internal method to generate display string.
        """
        lines = ["=" * 70, "RETRY CONFIGURATION"]

        # Check if retries are disabled
        retries_disabled = cls.default.max_attempts == 1 and not cls.status_configs and not cls.retryable_status_codes

        if retries_disabled:
            lines.append("STATUS: RETRIES DISABLED")
            lines.append("=" * 70)
            lines.append("")
            lines.append("All HTTP request retries are currently disabled.")
            lines.append("")
            lines.append("To enable retries, use:")
            lines.append("  RetryConfig.enable()")
            lines.append("=" * 70)
            return "\n".join(lines)

        # Retries are enabled - show full configuration
        lines.append("STATUS: RETRIES ENABLED")
        lines.append("=" * 70)

        # Calculate which status codes use default settings
        all_retryable = sorted(set(cls.status_configs.keys()) | cls.retryable_status_codes)
        codes_using_default = sorted([code for code in all_retryable if code not in cls.status_configs])

        # Default settings
        lines.append("")
        lines.append("Default Settings:")
        if codes_using_default:
            lines.append(f"Applied to status codes: {codes_using_default}")
        else:
            lines.append("Applied to status codes: None (all codes have specific settings)")
        lines.append(f"  Max Attempts:    {cls.default.max_attempts}")  # noqa: E241

        # Show max_time with limit info
        if cls.default.max_time is None:
            max_time_display = f"None (max allowed: {MAX_TIME_LIMIT}s)"
        else:
            max_time_display = f"{cls.default.max_time}s (max allowed: {MAX_TIME_LIMIT}s)"
        lines.append(f"  Max Time:        {max_time_display}")  # noqa: E241

        lines.append(f"  Initial Delay:   {cls.default.init_delay}s")  # noqa: E241
        lines.append(f"  Exp Factor:      {cls.default.exp_factor}x")  # noqa: E241
        lines.append(f"  Jitter:          {'Enabled' if cls.default.jitter else 'Disabled'}")  # noqa: E241

        # Status-specific configs
        if cls.status_configs:
            lines.append("")
            lines.append("Status-Specific Settings:")
            for status_code in sorted(cls.status_configs.keys()):
                config = cls.status_configs[status_code]
                lines.append(f"  HTTP {status_code}: ")
                lines.append(f"    Max Attempts:  {config.max_attempts}")  # noqa: E241

                # Show max_time with limit info for each config
                if config.max_time is None:
                    config_max_time = f"None (max allowed: {MAX_TIME_LIMIT}s)"
                else:
                    config_max_time = f"{config.max_time}s (max allowed: {MAX_TIME_LIMIT}s)"
                lines.append(f"    Max Time:      {config_max_time}")  # noqa: E241

                lines.append(f"    Initial Delay: {config.init_delay}s")  # noqa: E241
                lines.append(f"    Exp Factor:    {config.exp_factor}x")  # noqa: E241
                lines.append(f"    Jitter:        {'Enabled' if config.jitter else 'Disabled'}")  # noqa: E241
        else:
            lines.append("")
            lines.append("Status-Specific Settings:")
            lines.append("  None configured")
        lines.append("=" * 70)

        return "\n".join(lines)


class HTTPRetryError(Exception):
    """Exception raised when max retries are exceeded."""

    def __init__(
        self,
        message: str,
        last_exception: Optional[Exception] = None,
        last_response: Optional[Any] = None,
        attempts_made: int = 0,
        total_time: float = 0.0,
    ):
        self.last_exception = last_exception
        self.last_response = last_response
        self.attempts_made = attempts_made
        self.total_time = total_time
        super().__init__(message)


# Thread-local storage for retry overrides
_local = threading.local()


def get_current_retry_override() -> Optional[Dict[str, Any]]:
    """Get current retry override for this thread."""
    return getattr(_local, 'retry_override', None)


@contextmanager
def retry_on_http_error(
    settings: Optional[RetrySettings] = None,
    only_status_codes: Optional[Set[int]] = None,
    skip_status_codes: Optional[Set[int]] = None,
) -> Iterator[None]:
    """
    Context manager for temporary retry override with error filtering.

    Args:
        settings: Retry settings to use
        only_status_codes: If specified, ONLY retry these status codes
        skip_status_codes: If specified, retry ALL status codes EXCEPT these

    Logic:
        - only_status_codes={429} = retry ONLY 429
        - skip_status_codes={500} = retry ALL 4xx and 5xx status codes EXCEPT 500
        - No parameters = retry ALL 4xx and 5xx status codes

    Examples:
        # Retry ONLY rate limiting errors
        with retry_on_http_error(RetrySettings(max_attempts=10), only_status_codes={429}):
            sch.delete_job(job)  # Only retries on 429

        # Retry everything except 500 errors
        with retry_on_http_error(RetrySettings(max_attempts=5), skip_status_codes={500}):
            sch.delete_job(job)  # Retries all errors except 500

        # Retry everything (all 4xx and 5xx)
        with retry_on_http_error(RetrySettings(max_attempts=20)):
            sch.delete_job(job)  # Retries ALL 4xx and 5xx status codes
    """
    if only_status_codes is not None and skip_status_codes is not None:
        raise ValueError("Cannot specify both only_status_codes and skip_status_codes.")

    settings = settings or RetrySettings()
    previous_override = get_current_retry_override()

    # Create enhanced override with filtering
    override_data = {
        'settings': settings,
        'only_status_codes': only_status_codes,
        'skip_status_codes': skip_status_codes,
    }
    _local.retry_override = override_data

    try:
        yield
    finally:
        if previous_override is None:
            if hasattr(_local, 'retry_override'):
                delattr(_local, 'retry_override')
        else:
            _local.retry_override = previous_override


@contextmanager
def no_retry_on_http_error() -> Iterator[None]:
    """Context manager to disable retry for the current thread."""
    with retry_on_http_error(RetrySettings(max_attempts=1)):
        yield


def _calculate_delay(attempt: int, settings: RetrySettings) -> float:
    """Calculate delay with exponential backoff and optional jitter."""
    delay = settings.init_delay * (settings.exp_factor**attempt)
    delay = min(delay, MAX_DELAY)  # Cap maximum delay
    if settings.jitter:
        jitter_range = delay * JITTER_FACTOR
        jitter_offset = random.uniform(-jitter_range, jitter_range)
        delay += jitter_offset
    return max(0, delay)


def _is_retryable_exception(exception: Exception) -> bool:
    """Check if an exception should trigger a retry (only non-HTTP exceptions)."""

    # Don't retry HTTP errors - they should be handled by status code logic
    if isinstance(exception, requests.exceptions.HTTPError):
        return False

    # Only retry connection/network level exceptions
    retryable_exceptions = (
        requests.exceptions.ConnectionError,
        requests.exceptions.Timeout,
        requests.exceptions.ConnectTimeout,
        requests.exceptions.ReadTimeout,
    )
    return isinstance(exception, retryable_exceptions)


def _get_status_code_from_exception(exception: Exception) -> Optional[int]:
    """Extract status code from HTTP exception if available."""
    try:
        return exception.response.status_code
    except AttributeError:
        return None


def _should_retry_status(
    status_code: int,
    effective_settings: Optional[RetrySettings],
    effective_only_codes: Optional[Set[int]],
    effective_skip_codes: Optional[Set[int]],
) -> bool:
    """Check if this status code should be retried based on filters and config."""

    # Never retry successful status codes (2xx)
    if 200 <= status_code < 300:
        return False

    actual_retry_settings = effective_settings or RetryConfig.get_settings_for_status(status_code)

    # If max_attempts is 1, retries are disabled
    if actual_retry_settings.max_attempts == 1:
        return False

    # Context manager overrides
    if effective_only_codes is not None:
        return status_code in effective_only_codes
    if effective_skip_codes is not None:
        return status_code not in effective_skip_codes

    if effective_settings:
        return status_code >= 400

    # No override: Use global config
    return RetryConfig.is_retryable_status(status_code)


# Module-level constant for frame skipping
_SKIP_FRAME_NAMES = frozenset(
    {
        'wrapper',
        'decorator',
        '_request',
        '_get',
        '_post',
        '_put',
        '_delete',
        '_patch',
        '_head',
        'make_request',
        'send_request',
    }
)


def _extract_caller_context(func_name: str) -> str:
    """
    Walk up the call stack to find the actual user-facing function.

    Skips internal helpers like _request, _get, wrapper, etc.
    This gives us meaningful context like "ControlHub.create_pipeline"
    instead of just "_request" or "APIClient._post".
    Args:
        func_name: Name of the decorated function (fallback)
    Returns:
        "ClassName.method_name" or just "method_name"
    """
    try:
        frame = inspect.currentframe()
        try:
            while frame is not None:
                frame_name = frame.f_code.co_name
                if frame_name not in _SKIP_FRAME_NAMES and not frame_name.startswith('_'):
                    if 'self' in frame.f_locals:
                        obj = frame.f_locals['self']
                        class_name = obj.__class__.__name__
                        return f"{class_name}.{frame_name}"
                    return frame_name
                frame = frame.f_back
            return func_name
        finally:
            del frame  # Delete frame reference to avoid reference cycles.
    except Exception:
        return func_name  # If anything goes wrong, just return the decorated function name


def _resolve_retry_settings(status_code: int, effective_settings: Optional[RetrySettings]) -> RetrySettings:
    """
    Resolve retry settings from context override or global config.

    Args:
        status_code: HTTP status code
        effective_settings: Context manager override (if any)

    Returns:
        Retry settings to use (from override or status-specific config)
    """
    if effective_settings:
        return effective_settings
    return RetryConfig.get_settings_for_status(status_code)


def _build_error_description(status_code: Optional[int], exception_type: Optional[str] = None) -> str:
    """Build human-readable error description"""
    if status_code:
        return f"HTTP {status_code}" + (f" ({exception_type})" if exception_type else "")
    return f"Connection error ({exception_type or 'unknown'})"


def _raise_if_max_retries_exceeded(
    attempt: int,
    retry_settings: RetrySettings,
    start_time: float,
    context: str,
    status_code: Optional[int] = None,
    exception: Optional[Exception] = None,
    response: Optional[Any] = None,
) -> None:
    """
    Raise HTTPRetryError if max retries or max time exceeded.
    Does nothing if retries should continue.

    Special case: If max_attempts == 1, no retries are configured, so we return early.
    """
    elapsed_time = time.time() - start_time

    # If max_attempts is 1, retries are disabled - caller will handle the error
    if retry_settings.max_attempts == 1:
        return

    error_desc = _build_error_description(status_code, type(exception).__name__ if exception else None)

    if attempt >= retry_settings.max_attempts - 1:
        logger.warning(f"[{context}] Max retries ({retry_settings.max_attempts}) exceeded for {error_desc}")
        raise HTTPRetryError(
            message=f"Max retries ({retry_settings.max_attempts}) exceeded for {error_desc}",
            last_exception=exception,
            last_response=response,
            attempts_made=attempt + 1,
            total_time=elapsed_time,
        ) from exception

    if retry_settings.max_time and elapsed_time >= retry_settings.max_time:
        logger.warning(f"[{context}] Max retry time ({retry_settings.max_time}s) exceeded for {error_desc}")
        raise HTTPRetryError(
            message=f"Max retry time ({retry_settings.max_time}s) exceeded for {error_desc}",
            last_exception=exception,
            last_response=response,
            attempts_made=attempt + 1,
            total_time=elapsed_time,
        ) from exception


def _log_and_sleep(
    attempt: int,
    retry_settings: RetrySettings,
    context: str,
    status_code: Optional[int] = None,
    exception_type: Optional[str] = None,
):
    """Log retry attempt and sleep."""
    delay = _calculate_delay(attempt, retry_settings)

    error_desc = _build_error_description(status_code, exception_type)

    logger.info(
        f"[{context}] {error_desc}, retrying in {delay: .1f}s " f"(attempt {attempt + 1}/{retry_settings.max_attempts})"
    )

    time.sleep(delay)


def http_retry() -> Callable:
    """
    Decorator for HTTP retry logic with jitter and exponential backoff.
    Uses global RetryConfig settings or context manager overrides.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(self, *args, **kwargs):
            start_time = time.time()
            context = _extract_caller_context(func.__name__)
            override_data = get_current_retry_override()

            # Determine effective settings
            if override_data is not None:
                effective_settings = override_data['settings']
                effective_only_codes = override_data.get('only_status_codes')
                effective_skip_codes = override_data.get('skip_status_codes')
                loop_max_attempts = effective_settings.max_attempts
            else:
                effective_settings = None
                effective_only_codes = None
                effective_skip_codes = None
                loop_max_attempts = max(
                    RetryConfig.default.max_attempts,
                    max((s.max_attempts for s in RetryConfig.status_configs.values()), default=0),
                )

            # Main retry loop
            for attempt in range(loop_max_attempts):
                try:
                    response = func(self, *args, **kwargs)

                    if not hasattr(response, 'status_code'):
                        return response

                    if not _should_retry_status(
                        response.status_code, effective_settings, effective_only_codes, effective_skip_codes
                    ):
                        return response

                    retry_settings = _resolve_retry_settings(response.status_code, effective_settings)
                    _raise_if_max_retries_exceeded(
                        attempt,
                        retry_settings,
                        start_time,
                        context,
                        status_code=response.status_code,
                        response=response,
                    )

                    _log_and_sleep(attempt, retry_settings, context, status_code=response.status_code)
                    continue

                except requests.exceptions.RequestException as e:
                    # Handle exceptions raised by raise_for_status() in APIClient implementation.
                    # This catches both HTTPError (4xx/5xx converted to exceptions) and
                    # connection errors (ConnectionError, Timeout, etc.)

                    status_code = _get_status_code_from_exception(e)

                    if status_code:
                        if not _should_retry_status(
                            status_code, effective_settings, effective_only_codes, effective_skip_codes
                        ):
                            logger.debug(f"[{context}] HTTP {status_code} is not retryable")
                            raise

                        retry_settings = _resolve_retry_settings(status_code, effective_settings)
                    # Connection/network exception

                    elif _is_retryable_exception(e):
                        retry_settings = effective_settings or RetryConfig.default

                    else:
                        logger.debug(f"[{context}] Exception {type(e).__name__} is not retryable")
                        raise

                    # Execute retry with determined settings
                    _raise_if_max_retries_exceeded(
                        attempt, retry_settings, start_time, context, status_code=status_code, exception=e
                    )
                    exception_type = type(e).__name__
                    _log_and_sleep(
                        attempt, retry_settings, context, status_code=status_code, exception_type=exception_type
                    )
                    continue

            raise RuntimeError("Internal error: retry loop completed unexpectedly")

        return wrapper

    return decorator
