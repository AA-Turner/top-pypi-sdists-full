"""UX and Reliability module for SAGE.

Implements Items 201-280 from the product roadmap:
- Items 201-220: UX Improvements
- Items 221-240: Reliability & Error Handling
- Items 241-260: Advanced Features
- Items 261-280: Integration & Testing
"""

from __future__ import annotations

import hashlib
import json
import re
import time
from collections.abc import Callable, Generator
from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Any, ClassVar

# ============================================================================
# Items 201-220: UX Improvements
# ============================================================================


class ProgressPhase(Enum):
    """Item 201: Progress tracking phases."""

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
    """Item 202: Progress state tracking."""

    phase: ProgressPhase
    message: str
    current: int = 0
    total: int = 0
    sub_progress: float = 0.0  # 0.0 to 1.0
    elapsed_ms: float = 0.0
    estimated_remaining_ms: float = 0.0
    details: dict = field(default_factory=dict)


class ProgressTracker:
    """Items 201-210: Track and report progress."""

    # Item 203: Phase weights for overall progress
    PHASE_WEIGHTS: ClassVar[dict[ProgressPhase, float]] = {
        ProgressPhase.INITIALIZING: 0.05,
        ProgressPhase.ANALYZING: 0.15,
        ProgressPhase.SEARCHING: 0.15,
        ProgressPhase.READING: 0.15,
        ProgressPhase.PROCESSING: 0.20,
        ProgressPhase.GENERATING: 0.15,
        ProgressPhase.VALIDATING: 0.10,
        ProgressPhase.FINALIZING: 0.05,
    }

    def __init__(self, callback: Callable[[ProgressState], None] | None = None):
        self.callback = callback
        self.start_time = time.time()
        self.phase_times: dict[ProgressPhase, float] = {}
        self.current_state: ProgressState | None = None

    def start_phase(self, phase: ProgressPhase, message: str, total: int = 0):
        """Item 204: Start a new progress phase."""
        now = time.time()
        elapsed = (now - self.start_time) * 1000

        self.current_state = ProgressState(
            phase=phase,
            message=message,
            current=0,
            total=total,
            elapsed_ms=elapsed,
        )
        self.phase_times[phase] = now

        if self.callback:
            self.callback(self.current_state)

    def update(self, current: int, message: str | None = None, details: dict | None = None):
        """Item 205: Update progress within current phase."""
        if not self.current_state:
            return

        now = time.time()
        elapsed = (now - self.start_time) * 1000

        self.current_state.current = current
        self.current_state.elapsed_ms = elapsed

        if self.current_state.total > 0:
            self.current_state.sub_progress = current / self.current_state.total
            # Estimate remaining time
            if current > 0:
                time_per_item = elapsed / current
                remaining_items = self.current_state.total - current
                self.current_state.estimated_remaining_ms = time_per_item * remaining_items

        if message:
            self.current_state.message = message
        if details:
            self.current_state.details.update(details)

        if self.callback:
            self.callback(self.current_state)

    def complete(self, message: str = "Completed"):
        """Item 206: Mark progress as complete."""
        now = time.time()
        elapsed = (now - self.start_time) * 1000

        self.current_state = ProgressState(
            phase=ProgressPhase.COMPLETED,
            message=message,
            current=1,
            total=1,
            sub_progress=1.0,
            elapsed_ms=elapsed,
        )

        if self.callback:
            self.callback(self.current_state)

    def fail(self, error: str):
        """Item 207: Mark progress as failed."""
        now = time.time()
        elapsed = (now - self.start_time) * 1000

        self.current_state = ProgressState(
            phase=ProgressPhase.FAILED,
            message=error,
            elapsed_ms=elapsed,
        )

        if self.callback:
            self.callback(self.current_state)

    def get_overall_progress(self) -> float:
        """Item 208: Calculate overall progress percentage."""
        if not self.current_state:
            return 0.0

        if self.current_state.phase == ProgressPhase.COMPLETED:
            return 1.0

        if self.current_state.phase == ProgressPhase.FAILED:
            return 0.0

        # Sum weights of completed phases
        completed = 0.0
        phases_list = list(ProgressPhase)
        current_idx = phases_list.index(self.current_state.phase)

        for i, phase in enumerate(phases_list):
            if i < current_idx:
                completed += self.PHASE_WEIGHTS.get(phase, 0.0)
            elif i == current_idx:
                # Add partial progress for current phase
                phase_weight = self.PHASE_WEIGHTS.get(phase, 0.0)
                completed += phase_weight * self.current_state.sub_progress

        return min(completed, 1.0)


class StreamingOutput:
    """Items 209-215: Streaming output handler."""

    # Item 209: Output chunk types
    class ChunkType(Enum):
        TEXT = auto()
        PROGRESS = auto()
        LIST_ITEM = auto()
        CODE = auto()
        ERROR = auto()
        METADATA = auto()

    @dataclass
    class OutputChunk:
        chunk_type: StreamingOutput.ChunkType
        content: str
        metadata: dict = field(default_factory=dict)

    def __init__(self):
        self.buffer: list[StreamingOutput.OutputChunk] = []
        self.item_count = 0

    def emit_text(self, text: str) -> OutputChunk:
        """Item 210: Emit text chunk."""
        chunk = self.OutputChunk(self.ChunkType.TEXT, text)
        self.buffer.append(chunk)
        return chunk

    def emit_list_item(self, number: int, title: str, description: str = "") -> OutputChunk:
        """Item 211: Emit list item chunk."""
        content = f"{number}. **{title}**"
        if description:
            content += f": {description}"

        chunk = self.OutputChunk(
            self.ChunkType.LIST_ITEM,
            content,
            {"number": number, "title": title, "description": description},
        )
        self.buffer.append(chunk)
        self.item_count += 1
        return chunk

    def emit_progress(self, message: str, current: int, total: int) -> OutputChunk:
        """Item 212: Emit progress chunk."""
        chunk = self.OutputChunk(
            self.ChunkType.PROGRESS,
            message,
            {"current": current, "total": total},
        )
        self.buffer.append(chunk)
        return chunk

    def emit_error(self, error: str) -> OutputChunk:
        """Item 213: Emit error chunk."""
        chunk = self.OutputChunk(self.ChunkType.ERROR, error)
        self.buffer.append(chunk)
        return chunk

    def stream(self) -> Generator[OutputChunk, None, None]:
        """Item 214: Stream output chunks."""
        for chunk in self.buffer:
            yield chunk

    def get_full_output(self) -> str:
        """Item 215: Get complete output as string."""
        parts: list[str] = []
        for chunk in self.buffer:
            if chunk.chunk_type in (self.ChunkType.TEXT, self.ChunkType.LIST_ITEM):
                parts.append(chunk.content)
        return "\n".join(parts)


class OutputFormatter:
    """Items 216-220: Format output for display."""

    # Item 216: Terminal width handling
    DEFAULT_WIDTH: ClassVar[int] = 80
    MIN_WIDTH: ClassVar[int] = 40
    MAX_WIDTH: ClassVar[int] = 200

    def __init__(self, width: int = DEFAULT_WIDTH):
        self.width = max(self.MIN_WIDTH, min(width, self.MAX_WIDTH))

    def format_list_item(
        self, number: int, title: str, description: str = "", indent: int = 0
    ) -> str:
        """Item 217: Format a single list item."""
        prefix = " " * indent + f"{number}. "
        title_formatted = f"**{title}**"

        if description:
            # Wrap description to width
            desc_indent = " " * len(prefix)
            desc_lines = self._wrap_text(description, self.width - len(desc_indent))
            formatted_desc = "\n".join(desc_indent + line for line in desc_lines[1:])

            if len(prefix) + len(title_formatted) + 2 + len(desc_lines[0]) <= self.width:
                return f"{prefix}{title_formatted}: {desc_lines[0]}\n{formatted_desc}".rstrip()
            else:
                return f"{prefix}{title_formatted}:\n{desc_indent}{description}"

        return f"{prefix}{title_formatted}"

    def format_table(self, headers: list[str], rows: list[list[str]]) -> str:
        """Item 218: Format data as table."""
        if not rows:
            return ""

        # Calculate column widths
        col_widths = [len(h) for h in headers]
        for row in rows:
            for i, cell in enumerate(row):
                if i < len(col_widths):
                    col_widths[i] = max(col_widths[i], len(str(cell)))

        # Limit total width
        total = sum(col_widths) + len(col_widths) * 3 + 1
        if total > self.width:
            scale = (self.width - len(col_widths) * 3 - 1) / sum(col_widths)
            col_widths = [max(5, int(w * scale)) for w in col_widths]

        # Build table
        lines: list[str] = []

        # Header
        header_line = (
            "| "
            + " | ".join(h.ljust(col_widths[i])[: col_widths[i]] for i, h in enumerate(headers))
            + " |"
        )
        lines.append(header_line)

        # Separator
        sep_line = "|" + "|".join("-" * (w + 2) for w in col_widths) + "|"
        lines.append(sep_line)

        # Rows
        for row in rows:
            row_line = (
                "| "
                + " | ".join(
                    str(cell).ljust(col_widths[i])[: col_widths[i]]
                    if i < len(row)
                    else " " * col_widths[i]
                    for i, cell in enumerate(row + [""] * (len(headers) - len(row)))
                )
                + " |"
            )
            lines.append(row_line)

        return "\n".join(lines)

    def format_progress_bar(self, progress: float, width: int = 40) -> str:
        """Item 219: Format progress bar."""
        filled = int(progress * width)
        empty = width - filled
        bar = "█" * filled + "░" * empty
        percent = int(progress * 100)
        return f"[{bar}] {percent}%"

    def format_error(self, error: str, context: str = "") -> str:
        """Item 220: Format error message."""
        lines = [f"❌ Error: {error}"]
        if context:
            lines.append(f"   Context: {context}")
        return "\n".join(lines)

    def _wrap_text(self, text: str, width: int) -> list[str]:
        """Wrap text to specified width."""
        words = text.split()
        lines: list[str] = []
        current_line: list[str] = []
        current_length = 0

        for word in words:
            if current_length + len(word) + 1 <= width or not current_line:
                current_line.append(word)
                current_length += len(word) + 1
            else:
                lines.append(" ".join(current_line))
                current_line = [word]
                current_length = len(word)

        if current_line:
            lines.append(" ".join(current_line))

        return lines if lines else [""]


# ============================================================================
# Items 221-240: Reliability & Error Handling
# ============================================================================


class ErrorCategory(Enum):
    """Item 221: Error categories."""

    NETWORK = auto()
    FILE_IO = auto()
    PARSE = auto()
    VALIDATION = auto()
    TIMEOUT = auto()
    RESOURCE = auto()
    PERMISSION = auto()
    CONFIGURATION = auto()
    INTERNAL = auto()
    USER_INPUT = auto()


@dataclass
class SageError:
    """Item 222: Structured error representation."""

    category: ErrorCategory
    message: str
    code: str
    recoverable: bool = True
    context: dict = field(default_factory=dict)
    suggestions: list[str] = field(default_factory=list)
    original_exception: Exception | None = None


class ErrorHandler:
    """Items 221-230: Handle errors gracefully."""

    # Item 223: Error recovery strategies
    class RecoveryStrategy(Enum):
        RETRY = auto()
        SKIP = auto()
        FALLBACK = auto()
        ABORT = auto()
        ASK_USER = auto()

    # Item 224: Error patterns and their strategies
    ERROR_STRATEGIES: ClassVar[dict[ErrorCategory, ErrorHandler.RecoveryStrategy]] = {
        ErrorCategory.NETWORK: RecoveryStrategy.RETRY,
        ErrorCategory.FILE_IO: RecoveryStrategy.FALLBACK,
        ErrorCategory.PARSE: RecoveryStrategy.SKIP,
        ErrorCategory.VALIDATION: RecoveryStrategy.ASK_USER,
        ErrorCategory.TIMEOUT: RecoveryStrategy.RETRY,
        ErrorCategory.RESOURCE: RecoveryStrategy.FALLBACK,
        ErrorCategory.PERMISSION: RecoveryStrategy.ASK_USER,
        ErrorCategory.CONFIGURATION: RecoveryStrategy.ABORT,
        ErrorCategory.INTERNAL: RecoveryStrategy.ABORT,
        ErrorCategory.USER_INPUT: RecoveryStrategy.ASK_USER,
    }

    # Item 225: Max retry attempts
    MAX_RETRIES: ClassVar[int] = 3
    RETRY_DELAY_MS: ClassVar[int] = 1000

    def __init__(self):
        self.errors: list[SageError] = []
        self.retry_counts: dict[str, int] = {}

    def handle(self, error: SageError) -> RecoveryStrategy:
        """Item 226: Handle an error and determine strategy."""
        self.errors.append(error)

        # Get base strategy
        strategy = self.ERROR_STRATEGIES.get(error.category, self.RecoveryStrategy.ABORT)

        # Check retry limits
        if strategy == self.RecoveryStrategy.RETRY:
            error_key = f"{error.category.name}:{error.code}"
            current_retries = self.retry_counts.get(error_key, 0)

            if current_retries >= self.MAX_RETRIES:
                strategy = self.RecoveryStrategy.FALLBACK
            else:
                self.retry_counts[error_key] = current_retries + 1

        # Non-recoverable errors always abort
        if not error.recoverable:
            strategy = self.RecoveryStrategy.ABORT

        return strategy

    def format_for_user(self, error: SageError) -> str:
        """Item 227: Format error for user display."""
        lines = [f"Error: {error.message}"]

        if error.suggestions:
            lines.append("\nSuggestions:")
            for suggestion in error.suggestions:
                lines.append(f"  • {suggestion}")

        if error.context:
            lines.append("\nDetails:")
            for key, value in error.context.items():
                lines.append(f"  {key}: {value}")

        return "\n".join(lines)

    def get_error_summary(self) -> dict:
        """Item 228: Get summary of errors encountered."""
        by_category: dict[str, int] = {}
        recoverable_count = 0

        for error in self.errors:
            cat = error.category.name
            by_category[cat] = by_category.get(cat, 0) + 1
            if error.recoverable:
                recoverable_count += 1

        return {
            "total_errors": len(self.errors),
            "recoverable": recoverable_count,
            "unrecoverable": len(self.errors) - recoverable_count,
            "by_category": by_category,
            "retry_exhausted": sum(1 for c in self.retry_counts.values() if c >= self.MAX_RETRIES),
        }


class RetryPolicy:
    """Items 229-235: Retry logic with backoff."""

    def __init__(
        self,
        max_retries: int = 3,
        initial_delay_ms: int = 100,
        max_delay_ms: int = 10000,
        backoff_multiplier: float = 2.0,
    ):
        self.max_retries = max_retries
        self.initial_delay_ms = initial_delay_ms
        self.max_delay_ms = max_delay_ms
        self.backoff_multiplier = backoff_multiplier

    def get_delay(self, attempt: int) -> int:
        """Item 230: Calculate delay for retry attempt."""
        delay = self.initial_delay_ms * (self.backoff_multiplier**attempt)
        return min(int(delay), self.max_delay_ms)

    def should_retry(self, attempt: int, error: SageError) -> bool:
        """Item 231: Determine if retry should be attempted."""
        if attempt >= self.max_retries:
            return False

        if not error.recoverable:
            return False

        # Only retry certain categories
        retryable = {
            ErrorCategory.NETWORK,
            ErrorCategory.TIMEOUT,
            ErrorCategory.RESOURCE,
        }
        return error.category in retryable

    def execute_with_retry(
        self,
        func: Callable[[], Any],
        error_handler: ErrorHandler,
    ) -> tuple[Any, list[SageError]]:
        """Item 232: Execute function with retry logic."""
        errors: list[SageError] = []

        for attempt in range(self.max_retries + 1):
            try:
                result = func()
                return result, errors
            except Exception as e:
                error = SageError(
                    category=self._classify_exception(e),
                    message=str(e),
                    code=type(e).__name__,
                    original_exception=e,
                )
                errors.append(error)

                if not self.should_retry(attempt, error):
                    raise

                delay = self.get_delay(attempt)
                time.sleep(delay / 1000)

        # Should not reach here
        return None, errors

    def _classify_exception(self, e: Exception) -> ErrorCategory:
        """Item 233: Classify exception into error category."""
        type_name = type(e).__name__.lower()

        if "timeout" in type_name or "timed out" in str(e).lower():
            return ErrorCategory.TIMEOUT
        if "connect" in type_name or "network" in type_name:
            return ErrorCategory.NETWORK
        if "permission" in type_name or "access denied" in str(e).lower():
            return ErrorCategory.PERMISSION
        if "file" in type_name or "io" in type_name:
            return ErrorCategory.FILE_IO
        if "parse" in type_name or "json" in type_name or "syntax" in type_name:
            return ErrorCategory.PARSE
        if "valid" in type_name:
            return ErrorCategory.VALIDATION
        if "memory" in type_name or "resource" in type_name:
            return ErrorCategory.RESOURCE

        return ErrorCategory.INTERNAL


class GracefulDegradation:
    """Items 234-240: Graceful degradation strategies."""

    @dataclass
    class FallbackOption:
        name: str
        description: str
        quality_loss: float  # 0.0 to 1.0
        func: Callable[[], Any]

    def __init__(self):
        self.fallbacks: dict[str, list[GracefulDegradation.FallbackOption]] = {}
        self.degradation_log: list[dict] = []

    def register_fallback(self, operation: str, fallback: FallbackOption):
        """Item 235: Register fallback option."""
        if operation not in self.fallbacks:
            self.fallbacks[operation] = []
        self.fallbacks[operation].append(fallback)
        # Keep sorted by quality loss (prefer less degradation)
        self.fallbacks[operation].sort(key=lambda f: f.quality_loss)

    def execute_with_fallback(
        self, operation: str, primary: Callable[[], Any]
    ) -> tuple[Any, float]:
        """Item 236: Execute with fallback on failure."""
        # Try primary
        try:
            result = primary()
            return result, 0.0  # No quality loss
        except Exception as primary_error:
            self.degradation_log.append(
                {
                    "operation": operation,
                    "primary_failed": True,
                    "error": str(primary_error),
                }
            )

        # Try fallbacks
        fallbacks = self.fallbacks.get(operation, [])
        for fallback in fallbacks:
            try:
                result = fallback.func()
                self.degradation_log.append(
                    {
                        "operation": operation,
                        "fallback_used": fallback.name,
                        "quality_loss": fallback.quality_loss,
                    }
                )
                return result, fallback.quality_loss
            except Exception:
                continue

        # All failed
        self.degradation_log.append(
            {
                "operation": operation,
                "all_failed": True,
            }
        )
        raise RuntimeError(f"All fallbacks failed for operation: {operation}")

    def get_degradation_report(self) -> dict:
        """Item 237: Get report on degradation events."""
        total_ops = len(self.degradation_log)
        degraded = sum(1 for log in self.degradation_log if log.get("fallback_used"))
        failed = sum(1 for log in self.degradation_log if log.get("all_failed"))

        return {
            "total_operations": total_ops,
            "degraded_operations": degraded,
            "failed_operations": failed,
            "success_rate": (total_ops - failed) / total_ops if total_ops > 0 else 1.0,
            "degradation_rate": degraded / total_ops if total_ops > 0 else 0.0,
        }


# ============================================================================
# Items 241-260: Advanced Features
# ============================================================================


class CacheStrategy(Enum):
    """Item 241: Cache strategies."""

    LRU = auto()  # Least Recently Used
    LFU = auto()  # Least Frequently Used
    TTL = auto()  # Time To Live
    ADAPTIVE = auto()  # Adaptive based on access patterns


@dataclass
class CacheEntry:
    """Item 242: Cache entry with metadata."""

    key: str
    value: Any
    created_at: float
    accessed_at: float
    access_count: int = 1
    size_bytes: int = 0
    ttl_seconds: float = 3600.0


class SmartCache:
    """Items 241-250: Intelligent caching system."""

    # Item 243: Default cache limits
    DEFAULT_MAX_SIZE_MB: ClassVar[int] = 100
    DEFAULT_MAX_ENTRIES: ClassVar[int] = 1000
    DEFAULT_TTL_SECONDS: ClassVar[float] = 3600.0

    def __init__(
        self,
        strategy: CacheStrategy = CacheStrategy.LRU,
        max_size_mb: int = DEFAULT_MAX_SIZE_MB,
        max_entries: int = DEFAULT_MAX_ENTRIES,
    ):
        self.strategy = strategy
        self.max_size_bytes = max_size_mb * 1024 * 1024
        self.max_entries = max_entries
        self.entries: dict[str, CacheEntry] = {}
        self.total_size_bytes = 0
        self.hits = 0
        self.misses = 0

    def get(self, key: str) -> Any | None:
        """Item 244: Get from cache."""
        entry = self.entries.get(key)

        if entry is None:
            self.misses += 1
            return None

        # Check TTL
        if self.strategy == CacheStrategy.TTL:
            if time.time() - entry.created_at > entry.ttl_seconds:
                self._remove(key)
                self.misses += 1
                return None

        # Update access info
        entry.accessed_at = time.time()
        entry.access_count += 1
        self.hits += 1

        return entry.value

    def set(self, key: str, value: Any, ttl_seconds: float | None = None):
        """Item 245: Set in cache."""
        # Calculate size
        size = len(json.dumps(value, default=str)) if value else 0

        # Evict if necessary
        while (
            self.total_size_bytes + size > self.max_size_bytes
            or len(self.entries) >= self.max_entries
        ):
            if not self._evict_one():
                break

        # Remove existing if present
        if key in self.entries:
            self._remove(key)

        # Add new entry
        now = time.time()
        entry = CacheEntry(
            key=key,
            value=value,
            created_at=now,
            accessed_at=now,
            size_bytes=size,
            ttl_seconds=ttl_seconds or self.DEFAULT_TTL_SECONDS,
        )
        self.entries[key] = entry
        self.total_size_bytes += size

    def _remove(self, key: str):
        """Remove entry from cache."""
        if key in self.entries:
            self.total_size_bytes -= self.entries[key].size_bytes
            del self.entries[key]

    def _evict_one(self) -> bool:
        """Item 246: Evict one entry based on strategy."""
        if not self.entries:
            return False

        if self.strategy == CacheStrategy.LRU:
            # Evict least recently accessed
            oldest_key = min(self.entries.keys(), key=lambda k: self.entries[k].accessed_at)
            self._remove(oldest_key)

        elif self.strategy == CacheStrategy.LFU:
            # Evict least frequently accessed
            least_key = min(self.entries.keys(), key=lambda k: self.entries[k].access_count)
            self._remove(least_key)

        elif self.strategy == CacheStrategy.TTL:
            # Evict oldest
            oldest_key = min(self.entries.keys(), key=lambda k: self.entries[k].created_at)
            self._remove(oldest_key)

        elif self.strategy == CacheStrategy.ADAPTIVE:
            # Score based on recency and frequency
            def score(k: str) -> float:
                e = self.entries[k]
                recency = time.time() - e.accessed_at
                return e.access_count / (recency + 1)

            lowest_key = min(self.entries.keys(), key=score)
            self._remove(lowest_key)

        return True

    def clear(self):
        """Item 247: Clear cache."""
        self.entries.clear()
        self.total_size_bytes = 0

    def get_stats(self) -> dict:
        """Item 248: Get cache statistics."""
        total_accesses = self.hits + self.misses
        return {
            "entries": len(self.entries),
            "size_bytes": self.total_size_bytes,
            "size_mb": self.total_size_bytes / (1024 * 1024),
            "hits": self.hits,
            "misses": self.misses,
            "hit_rate": self.hits / total_accesses if total_accesses > 0 else 0.0,
        }

    def make_key(self, *args, **kwargs) -> str:
        """Item 249: Generate cache key from arguments."""
        key_parts = [str(a) for a in args]
        key_parts.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
        key_str = "|".join(key_parts)
        return hashlib.md5(key_str.encode()).hexdigest()


class IncrementalProcessor:
    """Items 251-260: Incremental processing for large tasks."""

    @dataclass
    class ProcessingState:
        """Item 251: Processing state for resumption."""

        task_id: str
        total_items: int
        processed_items: int
        current_position: int
        checkpoints: list[int]
        results: list[Any]
        started_at: float
        last_checkpoint_at: float
        metadata: dict = field(default_factory=dict)

    def __init__(self, checkpoint_interval: int = 10):
        self.checkpoint_interval = checkpoint_interval
        self.states: dict[str, IncrementalProcessor.ProcessingState] = {}

    def start_task(self, task_id: str, total_items: int) -> ProcessingState:
        """Item 252: Start new incremental task."""
        now = time.time()
        state = self.ProcessingState(
            task_id=task_id,
            total_items=total_items,
            processed_items=0,
            current_position=0,
            checkpoints=[],
            results=[],
            started_at=now,
            last_checkpoint_at=now,
        )
        self.states[task_id] = state
        return state

    def checkpoint(self, task_id: str) -> bool:
        """Item 253: Create checkpoint."""
        state = self.states.get(task_id)
        if not state:
            return False

        state.checkpoints.append(state.processed_items)
        state.last_checkpoint_at = time.time()
        return True

    def resume_from_checkpoint(self, task_id: str) -> ProcessingState | None:
        """Item 254: Resume from last checkpoint."""
        state = self.states.get(task_id)
        if not state or not state.checkpoints:
            return None

        # Restore to last checkpoint
        last_checkpoint = state.checkpoints[-1]
        state.current_position = last_checkpoint
        state.results = state.results[:last_checkpoint]
        return state

    def process_item(
        self,
        task_id: str,
        item: Any,
        processor: Callable[[Any], Any],
    ) -> Any | None:
        """Item 255: Process single item with tracking."""
        state = self.states.get(task_id)
        if not state:
            return None

        try:
            result = processor(item)
            state.results.append(result)
            state.processed_items += 1
            state.current_position += 1

            # Auto-checkpoint
            if state.processed_items % self.checkpoint_interval == 0:
                self.checkpoint(task_id)

            return result
        except Exception as e:
            state.metadata["last_error"] = str(e)
            return None

    def get_progress(self, task_id: str) -> dict:
        """Item 256: Get processing progress."""
        state = self.states.get(task_id)
        if not state:
            return {"error": "Task not found"}

        elapsed = time.time() - state.started_at
        rate = state.processed_items / elapsed if elapsed > 0 else 0
        remaining = state.total_items - state.processed_items

        return {
            "task_id": task_id,
            "total": state.total_items,
            "processed": state.processed_items,
            "remaining": remaining,
            "progress": state.processed_items / state.total_items if state.total_items > 0 else 0,
            "elapsed_seconds": elapsed,
            "items_per_second": rate,
            "estimated_remaining_seconds": remaining / rate if rate > 0 else 0,
            "checkpoints": len(state.checkpoints),
        }

    def complete_task(self, task_id: str) -> list[Any]:
        """Item 257: Complete task and return results."""
        state = self.states.get(task_id)
        if not state:
            return []

        results = state.results.copy()
        del self.states[task_id]
        return results


# ============================================================================
# Items 261-280: Integration & Testing
# ============================================================================


class MetricsCollector:
    """Items 261-270: Collect and report metrics."""

    @dataclass
    class Metric:
        name: str
        value: float
        unit: str
        timestamp: float
        tags: dict = field(default_factory=dict)

    def __init__(self):
        self.metrics: list[MetricsCollector.Metric] = []
        self.counters: dict[str, int] = {}
        self.gauges: dict[str, float] = {}
        self.timers: dict[str, list[float]] = {}

    def increment(self, name: str, value: int = 1, tags: dict | None = None):
        """Item 262: Increment counter."""
        self.counters[name] = self.counters.get(name, 0) + value
        self._record(name, self.counters[name], "count", tags)

    def gauge(self, name: str, value: float, tags: dict | None = None):
        """Item 263: Set gauge value."""
        self.gauges[name] = value
        self._record(name, value, "value", tags)

    def timer(self, name: str, duration_ms: float, tags: dict | None = None):
        """Item 264: Record timer value."""
        if name not in self.timers:
            self.timers[name] = []
        self.timers[name].append(duration_ms)
        self._record(name, duration_ms, "ms", tags)

    def _record(self, name: str, value: float, unit: str, tags: dict | None = None):
        """Record metric."""
        self.metrics.append(
            self.Metric(
                name=name,
                value=value,
                unit=unit,
                timestamp=time.time(),
                tags=tags or {},
            )
        )

    def get_summary(self) -> dict:
        """Item 265: Get metrics summary."""
        timer_stats = {}
        for name, values in self.timers.items():
            if values:
                timer_stats[name] = {
                    "count": len(values),
                    "min": min(values),
                    "max": max(values),
                    "avg": sum(values) / len(values),
                    "total": sum(values),
                }

        return {
            "counters": self.counters.copy(),
            "gauges": self.gauges.copy(),
            "timers": timer_stats,
            "total_metrics": len(self.metrics),
        }


class QualityAssurance:
    """Items 271-280: Quality assurance checks."""

    # Item 271: Quality thresholds
    QUALITY_THRESHOLDS: ClassVar[dict[str, float]] = {
        "min_list_items": 0.9,  # Must have 90% of requested items
        "min_actionable": 0.7,  # 70% of items must be actionable
        "min_unique": 0.95,  # 95% must be unique
        "max_error_rate": 0.05,  # Max 5% error rate
        "min_relevance": 0.6,  # Min 60% relevance score
    }

    @dataclass
    class QualityResult:
        passed: bool
        score: float
        checks: dict
        issues: list[str]
        suggestions: list[str]

    def assess_list_output(
        self,
        items: list[Any],
        requested_count: int,
        context: str = "",
    ) -> QualityResult:
        """Item 272: Assess list output quality."""
        checks: dict[str, bool] = {}
        issues: list[str] = []
        suggestions: list[str] = []

        # Check quantity
        quantity_ratio = len(items) / requested_count if requested_count > 0 else 1.0
        checks["quantity"] = quantity_ratio >= self.QUALITY_THRESHOLDS["min_list_items"]
        if not checks["quantity"]:
            issues.append(f"Only {len(items)} of {requested_count} items generated")
            suggestions.append("Continue generating to meet quantity requirement")

        # Check uniqueness
        unique_items = set()
        for item in items:
            item_key = str(item).lower().strip()
            unique_items.add(item_key)

        uniqueness = len(unique_items) / len(items) if items else 1.0
        checks["uniqueness"] = uniqueness >= self.QUALITY_THRESHOLDS["min_unique"]
        if not checks["uniqueness"]:
            issues.append(f"Duplicate items detected ({len(items) - len(unique_items)} duplicates)")
            suggestions.append("Remove duplicate items and generate replacements")

        # Calculate overall score
        score = sum(1 for v in checks.values() if v) / len(checks)
        passed = all(checks.values())

        return self.QualityResult(
            passed=passed,
            score=score,
            checks=checks,
            issues=issues,
            suggestions=suggestions,
        )

    def assess_response_quality(
        self,
        response: str,
        request_type: str,
        expected_format: str,
    ) -> QualityResult:
        """Item 273: Assess general response quality."""
        checks: dict[str, bool] = {}
        issues: list[str] = []
        suggestions: list[str] = []

        # Check not empty
        checks["not_empty"] = len(response.strip()) > 0
        if not checks["not_empty"]:
            issues.append("Response is empty")

        # Check format compliance
        if expected_format == "list":
            has_list = bool(re.search(r"^\d+\.", response, re.MULTILINE))
            checks["format"] = has_list
            if not checks["format"]:
                issues.append("Response should be numbered list format")

        elif expected_format == "text":
            # Should NOT have code blocks for text responses
            has_code = "```" in response or "FILE:" in response
            checks["format"] = not has_code
            if not checks["format"]:
                issues.append("Text response should not contain code blocks")

        # Check response length
        min_length = 100 if request_type != "simple" else 20
        checks["length"] = len(response) >= min_length
        if not checks["length"]:
            issues.append(f"Response too short (min {min_length} characters)")

        score = sum(1 for v in checks.values() if v) / len(checks)
        passed = all(checks.values())

        return self.QualityResult(
            passed=passed,
            score=score,
            checks=checks,
            issues=issues,
            suggestions=suggestions,
        )

    def validate_no_code(self, response: str) -> QualityResult:
        """Item 274: Validate response contains no code for analysis requests."""
        checks: dict[str, bool] = {}
        issues: list[str] = []

        # Check for code patterns
        code_patterns = [
            (r"^FILE:\s*\S+", "FILE: blocks"),
            (r"```[\w]*\n", "Markdown code blocks"),
            (r"^\s{4,}\S", "Indented code blocks"),
            (r"^(def|class|function|import|from|const|let|var)\s+", "Code definitions"),
        ]

        for pattern, description in code_patterns:
            has_pattern = bool(re.search(pattern, response, re.MULTILINE))
            check_name = description.lower().replace(" ", "_")
            checks[check_name] = not has_pattern
            if not checks[check_name]:
                issues.append(f"Found {description} in response")

        passed = all(checks.values())
        score = sum(1 for v in checks.values() if v) / len(checks) if checks else 1.0

        return self.QualityResult(
            passed=passed,
            score=score,
            checks=checks,
            issues=issues,
            suggestions=["Remove all code from analysis response"] if issues else [],
        )


class TestFramework:
    """Items 275-280: Testing framework for SAGE components."""

    @dataclass
    class TestCase:
        name: str
        description: str
        input_data: Any
        expected_output: Any
        validator: Callable[[Any, Any], bool]
        tags: list[str] = field(default_factory=list)

    @dataclass
    class TestResult:
        test_name: str
        passed: bool
        actual_output: Any
        error: str | None = None
        execution_time_ms: float = 0.0

    def __init__(self):
        self.test_cases: list[TestFramework.TestCase] = []
        self.results: list[TestFramework.TestResult] = []

    def add_test(self, test: TestCase):
        """Item 276: Add test case."""
        self.test_cases.append(test)

    def run_test(
        self,
        test: TestCase,
        func: Callable[[Any], Any],
    ) -> TestResult:
        """Item 277: Run single test."""
        start = time.time()
        try:
            actual = func(test.input_data)
            passed = test.validator(actual, test.expected_output)
            execution_time = (time.time() - start) * 1000

            result = self.TestResult(
                test_name=test.name,
                passed=passed,
                actual_output=actual,
                execution_time_ms=execution_time,
            )
        except Exception as e:
            execution_time = (time.time() - start) * 1000
            result = self.TestResult(
                test_name=test.name,
                passed=False,
                actual_output=None,
                error=str(e),
                execution_time_ms=execution_time,
            )

        self.results.append(result)
        return result

    def run_all(self, func: Callable[[Any], Any]) -> dict:
        """Item 278: Run all tests."""
        self.results = []
        for test in self.test_cases:
            self.run_test(test, func)

        return self.get_summary()

    def get_summary(self) -> dict:
        """Item 279: Get test summary."""
        passed = sum(1 for r in self.results if r.passed)
        failed = len(self.results) - passed
        total_time = sum(r.execution_time_ms for r in self.results)

        return {
            "total": len(self.results),
            "passed": passed,
            "failed": failed,
            "pass_rate": passed / len(self.results) if self.results else 0,
            "total_time_ms": total_time,
            "avg_time_ms": total_time / len(self.results) if self.results else 0,
            "failures": [
                {"name": r.test_name, "error": r.error} for r in self.results if not r.passed
            ],
        }

    def generate_report(self) -> str:
        """Item 280: Generate test report."""
        summary = self.get_summary()
        lines = [
            "=" * 60,
            "SAGE Test Report",
            "=" * 60,
            f"Total Tests: {summary['total']}",
            f"Passed: {summary['passed']} ({summary['pass_rate'] * 100:.1f}%)",
            f"Failed: {summary['failed']}",
            f"Total Time: {summary['total_time_ms']:.2f}ms",
            "",
        ]

        if summary["failures"]:
            lines.append("Failures:")
            for failure in summary["failures"]:
                lines.append(f"  - {failure['name']}: {failure['error']}")
            lines.append("")

        lines.append("=" * 60)
        return "\n".join(lines)
