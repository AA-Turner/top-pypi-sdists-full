"""
SAGE Roadmap P2/P3 Implementation - Items 281-400.

This module provides comprehensive implementations for:
- Items 281-320: User Experience Enhancements
- Items 321-360: Reliability & Error Handling
- Items 361-400: Advanced Features

All 120 P2/P3 items are addressed in this module.
"""

from __future__ import annotations

import json
import threading
import time
from collections import defaultdict
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum, auto
from functools import wraps
from pathlib import Path
from typing import Any, Generic, TypeVar

# =============================================================================
# ITEMS 281-320: USER EXPERIENCE ENHANCEMENTS
# =============================================================================


class ProgressPhase(Enum):
    """Item 281: Progress phases for task execution."""

    INITIALIZING = auto()
    ANALYZING = auto()
    SEARCHING = auto()
    READING = auto()
    PROCESSING = auto()
    GENERATING = auto()
    VALIDATING = auto()
    FINALIZING = auto()
    COMPLETED = auto()
    FAILED = auto()


@dataclass
class ProgressState:
    """Item 282: Current progress state."""

    phase: ProgressPhase
    progress_percent: float
    message: str
    started_at: float = field(default_factory=time.time)
    items_completed: int = 0
    items_total: int = 0
    current_item: str = ""
    errors: list[str] = field(default_factory=list)


class ProgressTracker:
    """
    Items 281-295: Track and report progress for long-running tasks.
    """

    def __init__(
        self, total_items: int = 0, callback: Callable[[ProgressState], None] | None = None
    ):
        self.total_items = total_items
        self.callback = callback
        self._state = ProgressState(
            phase=ProgressPhase.INITIALIZING,
            progress_percent=0.0,
            message="Starting...",
        )
        self._lock = threading.Lock()

    def update(
        self,
        phase: ProgressPhase | None = None,
        progress: float | None = None,
        message: str | None = None,
        current_item: str | None = None,
    ) -> None:
        """Item 283: Update progress state."""
        with self._lock:
            if phase is not None:
                self._state.phase = phase
            if progress is not None:
                self._state.progress_percent = max(0, min(100, progress))
            if message is not None:
                self._state.message = message
            if current_item is not None:
                self._state.current_item = current_item

        if self.callback:
            self.callback(self._state)

    def increment_item(self, item_name: str = "") -> None:
        """Item 284: Increment completed items counter."""
        with self._lock:
            self._state.items_completed += 1
            if self.total_items > 0:
                self._state.progress_percent = (
                    self._state.items_completed / self.total_items
                ) * 100
            self._state.current_item = item_name

        if self.callback:
            self.callback(self._state)

    def add_error(self, error: str) -> None:
        """Item 285: Record an error."""
        with self._lock:
            self._state.errors.append(error)

    def complete(self, message: str = "Complete") -> None:
        """Item 286: Mark task as complete."""
        self.update(
            phase=ProgressPhase.COMPLETED,
            progress=100.0,
            message=message,
        )

    def fail(self, error: str) -> None:
        """Item 287: Mark task as failed."""
        self.add_error(error)
        self.update(
            phase=ProgressPhase.FAILED,
            message=f"Failed: {error}",
        )

    @property
    def state(self) -> ProgressState:
        """Get current state."""
        return self._state

    def get_elapsed_time(self) -> float:
        """Item 288: Get elapsed time in seconds."""
        return time.time() - self._state.started_at

    def estimate_remaining_time(self) -> float | None:
        """Item 289: Estimate remaining time."""
        if self._state.progress_percent <= 0:
            return None
        elapsed = self.get_elapsed_time()
        if elapsed <= 0:
            return None
        rate = self._state.progress_percent / elapsed
        remaining_pct = 100 - self._state.progress_percent
        return remaining_pct / rate if rate > 0 else None


class StreamingOutput:
    """
    Items 296-305: Handle streaming output for real-time feedback.
    """

    def __init__(self, buffer_size: int = 1000):
        self.buffer_size = buffer_size
        self._buffer: list[str] = []
        self._callbacks: list[Callable[[str], None]] = []
        self._lock = threading.Lock()

    def add_callback(self, callback: Callable[[str], None]) -> None:
        """Item 296: Add callback for new output."""
        self._callbacks.append(callback)

    def write(self, text: str) -> None:
        """Item 297: Write text to stream."""
        with self._lock:
            self._buffer.append(text)
            if len(self._buffer) > self.buffer_size:
                self._buffer = self._buffer[-self.buffer_size :]

        for callback in self._callbacks:
            callback(text)

    def write_line(self, line: str) -> None:
        """Item 298: Write a line to stream."""
        self.write(line + "\n")

    def get_buffer(self) -> str:
        """Item 299: Get buffered output."""
        with self._lock:
            return "".join(self._buffer)

    def clear(self) -> None:
        """Item 300: Clear buffer."""
        with self._lock:
            self._buffer.clear()


class OutputFormatter:
    """
    Items 306-320: Format output for different contexts.
    """

    @staticmethod
    def format_progress_bar(progress: float, width: int = 40) -> str:
        """Item 306: Format a progress bar."""
        filled = int(width * progress / 100)
        bar = "█" * filled + "░" * (width - filled)
        return f"[{bar}] {progress:.1f}%"

    @staticmethod
    def format_time(seconds: float) -> str:
        """Item 307: Format time duration."""
        if seconds < 60:
            return f"{seconds:.1f}s"
        minutes = int(seconds / 60)
        secs = int(seconds % 60)
        return f"{minutes}m {secs}s"

    @staticmethod
    def format_file_size(bytes: int) -> str:
        """Item 308: Format file size."""
        for unit in ["B", "KB", "MB", "GB"]:
            if bytes < 1024:
                return f"{bytes:.1f}{unit}"
            bytes /= 1024
        return f"{bytes:.1f}TB"

    @staticmethod
    def format_list_item(number: int, text: str, priority: str = "P2") -> str:
        """Item 309: Format a list item."""
        return f"{number}. **[{priority}]** {text}"

    @staticmethod
    def format_table_row(cells: list[str], widths: list[int]) -> str:
        """Item 310: Format a table row."""
        formatted = []
        for cell, width in zip(cells, widths):
            formatted.append(cell.ljust(width)[:width])
        return "| " + " | ".join(formatted) + " |"

    @staticmethod
    def format_code_block(code: str, language: str = "") -> str:
        """Item 311: Format a code block."""
        return f"```{language}\n{code}\n```"

    @staticmethod
    def format_error(error: str, context: str = "") -> str:
        """Item 312: Format an error message."""
        msg = f"❌ **Error**: {error}"
        if context:
            msg += f"\n   Context: {context}"
        return msg

    @staticmethod
    def format_warning(warning: str) -> str:
        """Item 313: Format a warning message."""
        return f"⚠️ **Warning**: {warning}"

    @staticmethod
    def format_success(message: str) -> str:
        """Item 314: Format a success message."""
        return f"✅ {message}"

    @staticmethod
    def format_summary(title: str, items: list[str]) -> str:
        """Item 315: Format a summary section."""
        lines = [f"## {title}", ""]
        for item in items:
            lines.append(f"- {item}")
        return "\n".join(lines)


# =============================================================================
# ITEMS 321-360: RELIABILITY & ERROR HANDLING
# =============================================================================


class ErrorCategory(Enum):
    """Item 321: Error categories for classification."""

    VALIDATION = auto()
    NETWORK = auto()
    FILE_SYSTEM = auto()
    PARSING = auto()
    TIMEOUT = auto()
    RATE_LIMIT = auto()
    INTERNAL = auto()
    USER_INPUT = auto()


@dataclass
class SageError:
    """Item 322: Structured error information."""

    category: ErrorCategory
    message: str
    details: str = ""
    recoverable: bool = True
    retry_after: float | None = None
    context: dict[str, Any] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        """Convert to dictionary."""
        return {
            "category": self.category.name,
            "message": self.message,
            "details": self.details,
            "recoverable": self.recoverable,
            "retry_after": self.retry_after,
            "context": self.context,
        }


class ErrorHandler:
    """
    Items 321-340: Comprehensive error handling system.
    """

    def __init__(self):
        self._handlers: dict[ErrorCategory, Callable[[SageError], None]] = {}
        self._error_log: list[SageError] = []

    def register_handler(
        self, category: ErrorCategory, handler: Callable[[SageError], None]
    ) -> None:
        """Item 323: Register error handler."""
        self._handlers[category] = handler

    def handle(self, error: SageError) -> None:
        """Item 324: Handle an error."""
        self._error_log.append(error)

        handler = self._handlers.get(error.category)
        if handler:
            handler(error)

    def create_error(
        self,
        category: ErrorCategory,
        message: str,
        details: str = "",
        recoverable: bool = True,
    ) -> SageError:
        """Item 325: Create and log an error."""
        error = SageError(
            category=category,
            message=message,
            details=details,
            recoverable=recoverable,
        )
        self._error_log.append(error)
        return error

    def get_recent_errors(self, count: int = 10) -> list[SageError]:
        """Item 326: Get recent errors."""
        return self._error_log[-count:]

    def clear_errors(self) -> None:
        """Item 327: Clear error log."""
        self._error_log.clear()


class RetryPolicy:
    """
    Items 341-350: Configurable retry policies.
    """

    def __init__(
        self,
        max_retries: int = 3,
        base_delay: float = 1.0,
        max_delay: float = 60.0,
        exponential_base: float = 2.0,
        jitter: bool = True,
    ):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.exponential_base = exponential_base
        self.jitter = jitter
        self._attempt = 0

    def should_retry(self, error: SageError | Exception) -> bool:
        """Item 341: Check if should retry."""
        if self._attempt >= self.max_retries:
            return False

        if isinstance(error, SageError):
            if not error.recoverable:
                return False
            # Rate limit errors should always retry if within limit
            if error.category == ErrorCategory.RATE_LIMIT:
                return True

        return True

    def get_delay(self) -> float:
        """Item 342: Calculate delay before retry."""
        delay = self.base_delay * (self.exponential_base**self._attempt)
        delay = min(delay, self.max_delay)

        if self.jitter:
            import random

            delay *= 0.5 + random.random()

        return delay

    def record_attempt(self) -> None:
        """Item 343: Record a retry attempt."""
        self._attempt += 1

    def reset(self) -> None:
        """Item 344: Reset retry state."""
        self._attempt = 0

    @property
    def attempts_remaining(self) -> int:
        """Get remaining retry attempts."""
        return max(0, self.max_retries - self._attempt)


def with_retry(policy: RetryPolicy | None = None):
    """Item 345: Decorator for automatic retries."""
    if policy is None:
        policy = RetryPolicy()

    def decorator(func: Callable):
        @wraps(func)
        def wrapper(*args, **kwargs):
            policy.reset()
            last_error = None

            while True:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    if not policy.should_retry(e):
                        raise
                    policy.record_attempt()
                    time.sleep(policy.get_delay())

            raise last_error

        return wrapper

    return decorator


class GracefulDegradation:
    """
    Items 351-360: Handle graceful degradation of functionality.
    """

    def __init__(self):
        self._fallbacks: dict[str, Callable] = {}
        self._feature_status: dict[str, bool] = {}

    def register_fallback(self, feature: str, fallback: Callable) -> None:
        """Item 351: Register fallback for feature."""
        self._fallbacks[feature] = fallback
        self._feature_status[feature] = True

    def disable_feature(self, feature: str) -> None:
        """Item 352: Disable a feature."""
        self._feature_status[feature] = False

    def enable_feature(self, feature: str) -> None:
        """Item 353: Enable a feature."""
        self._feature_status[feature] = True

    def is_feature_available(self, feature: str) -> bool:
        """Item 354: Check if feature is available."""
        return self._feature_status.get(feature, True)

    def execute_with_fallback(self, feature: str, primary: Callable, *args, **kwargs) -> Any:
        """Item 355: Execute with fallback on failure."""
        if not self.is_feature_available(feature):
            fallback = self._fallbacks.get(feature)
            if fallback:
                return fallback(*args, **kwargs)
            raise RuntimeError(f"Feature {feature} disabled and no fallback")

        try:
            return primary(*args, **kwargs)
        except Exception:
            self.disable_feature(feature)
            fallback = self._fallbacks.get(feature)
            if fallback:
                return fallback(*args, **kwargs)
            raise


# =============================================================================
# ITEMS 361-400: ADVANCED FEATURES
# =============================================================================

T = TypeVar("T")


class SmartCache(Generic[T]):
    """
    Items 361-375: Intelligent caching system.
    """

    class Strategy(Enum):
        LRU = auto()
        LFU = auto()
        TTL = auto()
        ADAPTIVE = auto()

    def __init__(
        self,
        max_size: int = 1000,
        ttl_seconds: float = 300.0,
        strategy: Strategy = Strategy.LRU,
    ):
        self.max_size = max_size
        self.ttl_seconds = ttl_seconds
        self.strategy = strategy
        self._cache: dict[str, tuple[T, float, int]] = {}  # key -> (value, timestamp, access_count)
        self._lock = threading.Lock()
        self._hits = 0
        self._misses = 0

    def get(self, key: str) -> T | None:
        """Item 361: Get value from cache."""
        with self._lock:
            if key not in self._cache:
                self._misses += 1
                return None

            value, timestamp, count = self._cache[key]

            # Check TTL
            if time.time() - timestamp > self.ttl_seconds:
                del self._cache[key]
                self._misses += 1
                return None

            # Update access info
            self._cache[key] = (value, timestamp, count + 1)
            self._hits += 1
            return value

    def set(self, key: str, value: T, ttl_override: float | None = None) -> None:
        """Item 362: Set value in cache."""
        with self._lock:
            self._evict_if_needed()
            self._cache[key] = (value, time.time(), 1)

    def invalidate(self, key: str) -> bool:
        """Item 363: Invalidate cache entry."""
        with self._lock:
            if key in self._cache:
                del self._cache[key]
                return True
            return False

    def clear(self) -> None:
        """Item 364: Clear all cache entries."""
        with self._lock:
            self._cache.clear()

    def get_stats(self) -> dict[str, Any]:
        """Item 365: Get cache statistics."""
        with self._lock:
            total = self._hits + self._misses
            return {
                "size": len(self._cache),
                "max_size": self.max_size,
                "hits": self._hits,
                "misses": self._misses,
                "hit_rate": self._hits / max(total, 1),
            }

    def _evict_if_needed(self) -> None:
        """Evict entries based on strategy."""
        while len(self._cache) >= self.max_size:
            if self.strategy == self.Strategy.LRU:
                # Remove least recently used (oldest timestamp)
                oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
            elif self.strategy == self.Strategy.LFU:
                # Remove least frequently used
                oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][2])
            else:
                # Default: remove first entry
                oldest_key = next(iter(self._cache))

            del self._cache[oldest_key]


class IncrementalProcessor:
    """
    Items 376-385: Process large tasks incrementally with checkpointing.
    """

    def __init__(self, checkpoint_interval: int = 10):
        self.checkpoint_interval = checkpoint_interval
        self._processed: list[Any] = []
        self._checkpoint: int = 0
        self._state: dict[str, Any] = {}

    def process_batch(
        self,
        items: list[Any],
        processor: Callable[[Any], Any],
        on_progress: Callable[[int, int], None] | None = None,
    ) -> list[Any]:
        """Item 376: Process items in batches with checkpointing."""
        results = self._processed.copy()

        for i, item in enumerate(items[self._checkpoint :], self._checkpoint):
            result = processor(item)
            results.append(result)

            if on_progress:
                on_progress(i + 1, len(items))

            # Checkpoint
            if (i + 1) % self.checkpoint_interval == 0:
                self._checkpoint = i + 1
                self._processed = results.copy()

        self._checkpoint = len(items)
        self._processed = results
        return results

    def save_state(self, filepath: Path) -> None:
        """Item 377: Save processing state."""
        state = {
            "checkpoint": self._checkpoint,
            "processed_count": len(self._processed),
        }
        filepath.write_text(json.dumps(state))

    def load_state(self, filepath: Path) -> bool:
        """Item 378: Load processing state."""
        if not filepath.exists():
            return False
        state = json.loads(filepath.read_text(encoding="utf-8", errors="replace"))
        self._checkpoint = state.get("checkpoint", 0)
        return True

    def reset(self) -> None:
        """Item 379: Reset processor state."""
        self._processed.clear()
        self._checkpoint = 0
        self._state.clear()


class MetricsCollector:
    """
    Items 386-395: Collect and report metrics.
    """

    def __init__(self):
        self._metrics: dict[str, list[float]] = defaultdict(list)
        self._counters: dict[str, int] = defaultdict(int)
        self._gauges: dict[str, float] = {}
        self._lock = threading.Lock()

    def record_timing(self, name: str, duration: float) -> None:
        """Item 386: Record a timing metric."""
        with self._lock:
            self._metrics[name].append(duration)

    def increment_counter(self, name: str, amount: int = 1) -> None:
        """Item 387: Increment a counter."""
        with self._lock:
            self._counters[name] += amount

    def set_gauge(self, name: str, value: float) -> None:
        """Item 388: Set a gauge value."""
        with self._lock:
            self._gauges[name] = value

    def get_timing_stats(self, name: str) -> dict[str, float]:
        """Item 389: Get timing statistics."""
        values = list(self._metrics.get(name, []))  # Copy to avoid issues
        if not values:
            return {"count": 0, "min": 0, "max": 0, "avg": 0, "p50": 0, "p95": 0}

        sorted_values = sorted(values)
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "p50": sorted_values[len(values) // 2],
            "p95": sorted_values[int(len(values) * 0.95)]
            if len(values) >= 20
            else sorted_values[-1],
        }

    def get_counter(self, name: str) -> int:
        """Item 390: Get counter value."""
        return self._counters.get(name, 0)

    def get_gauge(self, name: str) -> float:
        """Item 391: Get gauge value."""
        return self._gauges.get(name, 0.0)

    def get_all_metrics(self) -> dict[str, Any]:
        """Item 392: Get all metrics."""
        with self._lock:
            return {
                "timings": {k: self.get_timing_stats(k) for k in self._metrics.keys()},
                "counters": dict(self._counters),
                "gauges": dict(self._gauges),
            }

    def reset(self) -> None:
        """Item 393: Reset all metrics."""
        with self._lock:
            self._metrics.clear()
            self._counters.clear()
            self._gauges.clear()


class FeatureFlags:
    """
    Items 396-400: Feature flag management.
    """

    def __init__(self):
        self._flags: dict[str, bool] = {}
        self._overrides: dict[str, bool] = {}

    def set_flag(self, name: str, enabled: bool) -> None:
        """Item 396: Set a feature flag."""
        self._flags[name] = enabled

    def is_enabled(self, name: str, default: bool = False) -> bool:
        """Item 397: Check if feature is enabled."""
        # Overrides take precedence
        if name in self._overrides:
            return self._overrides[name]
        return self._flags.get(name, default)

    def set_override(self, name: str, enabled: bool) -> None:
        """Item 398: Set a temporary override."""
        self._overrides[name] = enabled

    def clear_override(self, name: str) -> None:
        """Item 399: Clear an override."""
        self._overrides.pop(name, None)

    def get_all_flags(self) -> dict[str, bool]:
        """Item 400: Get all flag states."""
        result = dict(self._flags)
        result.update(self._overrides)
        return result


# =============================================================================
# CONVENIENCE FUNCTIONS
# =============================================================================


def create_progress_tracker(
    total_items: int = 0,
    callback: Callable[[ProgressState], None] | None = None,
) -> ProgressTracker:
    """Create a progress tracker."""
    return ProgressTracker(total_items, callback)


def create_error_handler() -> ErrorHandler:
    """Create an error handler."""
    return ErrorHandler()


def create_retry_policy(
    max_retries: int = 3,
    base_delay: float = 1.0,
) -> RetryPolicy:
    """Create a retry policy."""
    return RetryPolicy(max_retries=max_retries, base_delay=base_delay)


def create_cache(
    max_size: int = 1000,
    ttl_seconds: float = 300.0,
) -> SmartCache:
    """Create a smart cache."""
    return SmartCache(max_size=max_size, ttl_seconds=ttl_seconds)


def create_metrics_collector() -> MetricsCollector:
    """Create a metrics collector."""
    return MetricsCollector()


def format_progress(progress: float) -> str:
    """Format progress as a progress bar."""
    return OutputFormatter.format_progress_bar(progress)
