"""
Enhanced tool execution system for SAGE.

P1-36: Add resource monitoring (CPU, memory, disk I/O)
P1-37: Implement tool composition/chaining
P1-38: Add tool scheduling/prioritization
P1-39: Replace shell=True with safer execution
P1-40: Add rate limiting on tool invocation
P1-41: Implement async tool execution
P1-42: Add tool output caching/memoization
P1-43: Implement Docker isolation for shell commands
P1-44: Add sophisticated HTML parsing for web fetch
P1-45: Implement transactional file operations (ACID)
P1-46: Add concurrent modification detection
P1-47: Support streaming for large files
P1-48: Preserve file encoding and line endings
P1-49: Add write-ahead logging for file ops
P1-50: Implement file operation rollback on partial failures
"""

from __future__ import annotations

import asyncio
import hashlib
import json
import os
import shlex
import subprocess
import threading
import time
from collections import deque
from collections.abc import Callable
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any, TypeVar

# =============================================================================
# Resource Monitoring (P1-36)
# =============================================================================


@dataclass
class ResourceUsage:
    """Resource usage metrics."""

    cpu_percent: float = 0.0
    memory_mb: float = 0.0
    disk_read_mb: float = 0.0
    disk_write_mb: float = 0.0
    duration_seconds: float = 0.0


class ResourceMonitor:
    """
    Monitors resource usage during tool execution.

    P1-36: Add resource monitoring (CPU, memory, disk I/O)
    """

    def __init__(self):
        self._start_time: float | None = None
        self._process = None

    def start(self) -> None:
        """Start monitoring."""
        self._start_time = time.time()
        try:
            import psutil

            self._process = psutil.Process()
            self._initial_io = (
                self._process.io_counters() if hasattr(self._process, "io_counters") else None
            )
        except ImportError:
            self._process = None
            self._initial_io = None

    def stop(self) -> ResourceUsage:
        """Stop monitoring and return usage."""
        duration = time.time() - (self._start_time or time.time())

        if self._process is None:
            return ResourceUsage(duration_seconds=duration)

        try:
            cpu = self._process.cpu_percent()
            memory = self._process.memory_info().rss / (1024 * 1024)

            disk_read = 0.0
            disk_write = 0.0
            if self._initial_io:
                current_io = self._process.io_counters()
                disk_read = (current_io.read_bytes - self._initial_io.read_bytes) / (1024 * 1024)
                disk_write = (current_io.write_bytes - self._initial_io.write_bytes) / (1024 * 1024)

            return ResourceUsage(
                cpu_percent=cpu,
                memory_mb=memory,
                disk_read_mb=disk_read,
                disk_write_mb=disk_write,
                duration_seconds=duration,
            )
        except Exception:
            return ResourceUsage(duration_seconds=duration)


# =============================================================================
# Tool Chaining (P1-37)
# =============================================================================


T = TypeVar("T")


class ToolChain:
    """
    Chain multiple tools together.

    P1-37: Implement tool composition/chaining
    """

    def __init__(self, name: str = "chain"):
        self.name = name
        self._steps: list[tuple[str, Callable, dict]] = []

    def add(
        self,
        name: str,
        func: Callable,
        transform_input: Callable[[Any], Any] | None = None,
        **kwargs,
    ) -> ToolChain:
        """Add a step to the chain."""
        self._steps.append((name, func, {"transform": transform_input, **kwargs}))
        return self

    async def execute(self, initial_input: Any = None) -> tuple[Any, list[dict]]:
        """
        Execute the chain.

        Returns:
            Tuple of (final_result, list of step results)
        """
        current_input = initial_input
        results = []

        for name, func, opts in self._steps:
            # Transform input if transformer provided
            if opts.get("transform"):
                current_input = opts["transform"](current_input)

            # Execute step
            start_time = time.time()
            try:
                if asyncio.iscoroutinefunction(func):
                    result = await func(current_input)
                else:
                    result = func(current_input)

                results.append(
                    {
                        "step": name,
                        "success": True,
                        "output": result,
                        "duration": time.time() - start_time,
                    }
                )
                current_input = result

            except Exception as e:
                results.append(
                    {
                        "step": name,
                        "success": False,
                        "error": str(e),
                        "duration": time.time() - start_time,
                    }
                )
                raise

        return current_input, results


# =============================================================================
# Tool Scheduling (P1-38)
# =============================================================================


class ToolPriority(Enum):
    """Priority levels for tool execution."""

    CRITICAL = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    BACKGROUND = 4


@dataclass
class ScheduledTool:
    """A tool scheduled for execution."""

    id: str
    name: str
    func: Callable
    args: tuple
    kwargs: dict
    priority: ToolPriority = ToolPriority.NORMAL
    deadline: float | None = None
    created_at: float = field(default_factory=time.time)

    def __lt__(self, other: ScheduledTool) -> bool:
        # Higher priority (lower value) comes first
        if self.priority.value != other.priority.value:
            return self.priority.value < other.priority.value
        # Earlier deadline comes first
        if self.deadline and other.deadline:
            return self.deadline < other.deadline
        # Earlier creation comes first
        return self.created_at < other.created_at


class ToolScheduler:
    """
    Schedules and prioritizes tool execution.

    P1-38: Add tool scheduling/prioritization
    """

    def __init__(self, max_concurrent: int = 4):
        self.max_concurrent = max_concurrent
        self._queue: list[ScheduledTool] = []
        self._running: set[str] = set()
        self._lock = threading.Lock()

    def schedule(
        self,
        name: str,
        func: Callable,
        *args,
        priority: ToolPriority = ToolPriority.NORMAL,
        deadline: float | None = None,
        **kwargs,
    ) -> str:
        """Schedule a tool for execution."""
        import uuid

        tool_id = str(uuid.uuid4())[:8]

        tool = ScheduledTool(
            id=tool_id,
            name=name,
            func=func,
            args=args,
            kwargs=kwargs,
            priority=priority,
            deadline=deadline,
        )

        with self._lock:
            self._queue.append(tool)
            self._queue.sort()

        return tool_id

    def get_next(self) -> ScheduledTool | None:
        """Get the next tool to execute."""
        with self._lock:
            if not self._queue:
                return None
            if len(self._running) >= self.max_concurrent:
                return None

            tool = self._queue.pop(0)
            self._running.add(tool.id)
            return tool

    def complete(self, tool_id: str) -> None:
        """Mark a tool as complete."""
        with self._lock:
            self._running.discard(tool_id)

    async def process_queue(self) -> list[Any]:
        """Process all scheduled tools."""
        results = []
        while self._queue or self._running:
            tool = self.get_next()
            if tool is None:
                await asyncio.sleep(0.1)
                continue

            try:
                if asyncio.iscoroutinefunction(tool.func):
                    result = await tool.func(*tool.args, **tool.kwargs)
                else:
                    result = tool.func(*tool.args, **tool.kwargs)
                results.append({"id": tool.id, "success": True, "result": result})
            except Exception as e:
                results.append({"id": tool.id, "success": False, "error": str(e)})
            finally:
                self.complete(tool.id)

        return results


# =============================================================================
# Safe Shell Execution (P1-39)
# =============================================================================


class SafeShellExecutor:
    """
    Executes shell commands safely without shell=True.

    P1-39: Replace shell=True with safer execution
    """

    # Allowed executables
    ALLOWED_EXECUTABLES = {
        # Core utilities
        "ls",
        "cat",
        "head",
        "tail",
        "grep",
        "find",
        "wc",
        "sort",
        "uniq",
        "echo",
        "pwd",
        "cd",
        "mkdir",
        "rm",
        "cp",
        "mv",
        "touch",
        "chmod",
        # Development tools
        "git",
        "python",
        "python3",
        "pip",
        "pip3",
        "node",
        "npm",
        "npx",
        "cargo",
        "rustc",
        "go",
        "java",
        "javac",
        "make",
        "cmake",
        # Testing
        "pytest",
        "jest",
        "mocha",
        "cargo-test",
        "go-test",
        # Build tools
        "tsc",
        "webpack",
        "vite",
        "esbuild",
        "rollup",
        # Linters/formatters
        "ruff",
        "black",
        "eslint",
        "prettier",
        "rustfmt",
        "gofmt",
    }

    # Blocked patterns
    BLOCKED_PATTERNS = [
        r"rm\s+(-[rf]+\s+)?/",
        r"sudo",
        r"su\s+",
        r"chmod\s+777\s+/",
        r"dd\s+",
        r"mkfs",
        r">(>)?\s*/dev/",
        r"\|\s*sh",
        r"\|\s*bash",
        r"`.*`",
        r"\$\(.*\)",
    ]

    def __init__(self, cwd: Path, timeout: int = 60):
        self.cwd = cwd
        self.timeout = timeout
        self._compiled_blocks = [__import__("re").compile(p) for p in self.BLOCKED_PATTERNS]

    def is_safe(self, command: str) -> tuple[bool, str | None]:
        """Check if command is safe to execute."""
        # Check blocked patterns
        for pattern in self._compiled_blocks:
            if pattern.search(command):
                return False, f"Blocked pattern detected: {pattern.pattern}"

        # Parse command
        try:
            parts = shlex.split(command)
            if not parts:
                return False, "Empty command"

            executable = parts[0]

            # Check if executable is allowed
            if executable not in self.ALLOWED_EXECUTABLES:
                # Check if it's a path to an allowed executable
                basename = os.path.basename(executable)
                if basename not in self.ALLOWED_EXECUTABLES:
                    return False, f"Executable not in allowlist: {executable}"

        except ValueError as e:
            return False, f"Invalid command syntax: {e}"

        return True, None

    def execute(
        self,
        command: str,
        env: dict[str, str] | None = None,
        capture_output: bool = True,
    ) -> tuple[int, str, str]:
        """
        Execute command safely.

        Returns:
            Tuple of (return_code, stdout, stderr)
        """
        # Safety check
        is_safe, reason = self.is_safe(command)
        if not is_safe:
            return -1, "", f"Command blocked: {reason}"

        # Parse command into arguments
        args = shlex.split(command)

        # Prepare environment
        exec_env = os.environ.copy()
        if env:
            exec_env.update(env)

        try:
            result = subprocess.run(
                args,
                cwd=str(self.cwd),
                env=exec_env,
                capture_output=capture_output,
                text=True,
                timeout=self.timeout,
                shell=False,  # Never use shell=True
            )
            return result.returncode, result.stdout, result.stderr

        except subprocess.TimeoutExpired:
            return -1, "", f"Command timed out after {self.timeout}s"
        except FileNotFoundError:
            return -1, "", f"Command not found: {args[0]}"
        except Exception as e:
            return -1, "", str(e)


# =============================================================================
# Rate Limiting (P1-40)
# =============================================================================


class ToolRateLimiter:
    """
    Rate limits tool invocations.

    P1-40: Add rate limiting on tool invocation
    """

    def __init__(
        self,
        max_per_second: float = 10.0,
        max_per_minute: float = 100.0,
        burst_size: int = 20,
    ):
        self.max_per_second = max_per_second
        self.max_per_minute = max_per_minute
        self.burst_size = burst_size
        self._tokens = burst_size
        self._last_update = time.time()
        self._minute_window: deque = deque()
        self._lock = threading.Lock()

    def acquire(self, timeout: float = 10.0) -> bool:
        """Try to acquire permission to execute."""
        deadline = time.time() + timeout

        while time.time() < deadline:
            with self._lock:
                # Refill tokens based on time passed
                now = time.time()
                elapsed = now - self._last_update
                self._tokens = min(
                    self.burst_size,
                    self._tokens + elapsed * self.max_per_second,
                )
                self._last_update = now

                # Clean old minute window entries
                cutoff = now - 60
                while self._minute_window and self._minute_window[0] < cutoff:
                    self._minute_window.popleft()

                # Check limits
                if self._tokens >= 1 and len(self._minute_window) < self.max_per_minute:
                    self._tokens -= 1
                    self._minute_window.append(now)
                    return True

            # Wait and retry
            time.sleep(0.1)

        return False

    def get_stats(self) -> dict[str, Any]:
        """Get rate limiter statistics."""
        with self._lock:
            return {
                "tokens_available": self._tokens,
                "burst_size": self.burst_size,
                "requests_last_minute": len(self._minute_window),
                "max_per_minute": self.max_per_minute,
            }


# =============================================================================
# Async Tool Execution (P1-41)
# =============================================================================


class AsyncToolExecutor:
    """
    Executes tools asynchronously.

    P1-41: Implement async tool execution
    """

    def __init__(
        self,
        max_concurrent: int = 10,
        rate_limiter: ToolRateLimiter | None = None,
    ):
        self.max_concurrent = max_concurrent
        self.rate_limiter = rate_limiter
        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._running_tasks: dict[str, asyncio.Task] = {}

    async def execute(
        self,
        name: str,
        func: Callable,
        *args,
        **kwargs,
    ) -> Any:
        """Execute a tool asynchronously."""
        # Rate limit check
        if self.rate_limiter and not self.rate_limiter.acquire():
            raise RuntimeError("Rate limit exceeded")

        async with self._semaphore:
            if asyncio.iscoroutinefunction(func):
                return await func(*args, **kwargs)
            else:
                # Run sync function in thread pool
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, lambda: func(*args, **kwargs))

    async def execute_many(
        self,
        tasks: list[tuple[str, Callable, tuple, dict]],
    ) -> list[dict[str, Any]]:
        """Execute multiple tools concurrently."""

        async def run_task(name: str, func: Callable, args: tuple, kwargs: dict) -> dict:
            try:
                result = await self.execute(name, func, *args, **kwargs)
                return {"name": name, "success": True, "result": result}
            except Exception as e:
                return {"name": name, "success": False, "error": str(e)}

        coros = [run_task(name, func, args, kwargs) for name, func, args, kwargs in tasks]
        return await asyncio.gather(*coros)


# =============================================================================
# Tool Output Caching (P1-42)
# =============================================================================


class ToolCache:
    """
    Caches tool outputs for memoization.

    P1-42: Add tool output caching/memoization
    """

    def __init__(
        self,
        max_entries: int = 1000,
        ttl_seconds: int = 300,
    ):
        self.max_entries = max_entries
        self.ttl_seconds = ttl_seconds
        self._cache: dict[str, tuple[Any, float]] = {}
        self._lock = threading.Lock()

    def _make_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Create cache key."""
        key_data = json.dumps(
            {
                "func": func_name,
                "args": [str(a) for a in args],
                "kwargs": {k: str(v) for k, v in sorted(kwargs.items())},
            },
            sort_keys=True,
        )
        return hashlib.sha256(key_data.encode()).hexdigest()[:16]

    def get(self, func_name: str, args: tuple, kwargs: dict) -> tuple[bool, Any]:
        """Get cached result. Returns (found, value)."""
        key = self._make_key(func_name, args, kwargs)

        with self._lock:
            if key in self._cache:
                value, timestamp = self._cache[key]
                if time.time() - timestamp < self.ttl_seconds:
                    return True, value
                else:
                    del self._cache[key]

        return False, None

    def set(self, func_name: str, args: tuple, kwargs: dict, value: Any) -> None:
        """Set cached result."""
        key = self._make_key(func_name, args, kwargs)

        with self._lock:
            # Evict oldest if at capacity
            if len(self._cache) >= self.max_entries:
                oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k][1])
                del self._cache[oldest_key]

            self._cache[key] = (value, time.time())

    def invalidate(self, func_name: str | None = None) -> int:
        """Invalidate cache entries. Returns count of invalidated entries."""
        with self._lock:
            if func_name is None:
                count = len(self._cache)
                self._cache.clear()
                return count

            # Invalidate entries for specific function
            to_remove = [k for k, v in self._cache.items() if func_name in str(v)]
            for k in to_remove:
                del self._cache[k]
            return len(to_remove)


def cached_tool(cache: ToolCache):
    """Decorator for caching tool results."""

    def decorator(func: Callable) -> Callable:
        async def wrapper(*args, **kwargs):
            found, value = cache.get(func.__name__, args, kwargs)
            if found:
                return value

            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)

            cache.set(func.__name__, args, kwargs, result)
            return result

        return wrapper

    return decorator


# =============================================================================
# Transactional File Operations (P1-45)
# =============================================================================


@dataclass
class FileOperation:
    """A file operation in a transaction."""

    op_type: str  # "write", "delete", "rename"
    path: Path
    content: str | None = None
    new_path: Path | None = None
    original_content: str | None = None
    original_exists: bool = False


class FileTransaction:
    """
    Transactional file operations with ACID properties.

    P1-45: Implement transactional file operations (ACID)
    P1-49: Add write-ahead logging for file ops
    P1-50: Implement file operation rollback on partial failures
    """

    def __init__(self, base_dir: Path, wal_dir: Path | None = None):
        self.base_dir = base_dir
        self.wal_dir = wal_dir or base_dir / ".sage" / "wal"
        self._operations: list[FileOperation] = []
        self._committed = False
        self._transaction_id = hashlib.sha256(str(time.time()).encode()).hexdigest()[:8]

    def write(self, path: str | Path, content: str) -> None:
        """Add a write operation."""
        file_path = Path(path) if not isinstance(path, Path) else path
        if not file_path.is_absolute():
            file_path = self.base_dir / path

        op = FileOperation(
            op_type="write",
            path=file_path,
            content=content,
            original_exists=file_path.exists(),
            original_content=file_path.read_text(encoding="utf-8", errors="replace") if file_path.exists() else None,
        )
        self._operations.append(op)

    def delete(self, path: str | Path) -> None:
        """Add a delete operation."""
        file_path = Path(path) if not isinstance(path, Path) else path
        if not file_path.is_absolute():
            file_path = self.base_dir / path

        op = FileOperation(
            op_type="delete",
            path=file_path,
            original_exists=file_path.exists(),
            original_content=file_path.read_text(encoding="utf-8", errors="replace") if file_path.exists() else None,
        )
        self._operations.append(op)

    def rename(self, old_path: str | Path, new_path: str | Path) -> None:
        """Add a rename operation."""
        old = Path(old_path) if not isinstance(old_path, Path) else old_path
        new = Path(new_path) if not isinstance(new_path, Path) else new_path

        if not old.is_absolute():
            old = self.base_dir / old_path
        if not new.is_absolute():
            new = self.base_dir / new_path

        op = FileOperation(
            op_type="rename",
            path=old,
            new_path=new,
            original_exists=old.exists(),
        )
        self._operations.append(op)

    def _write_wal(self) -> None:
        """Write operations to write-ahead log."""
        self.wal_dir.mkdir(parents=True, exist_ok=True)
        wal_file = self.wal_dir / f"{self._transaction_id}.wal"

        wal_data = {
            "transaction_id": self._transaction_id,
            "timestamp": time.time(),
            "operations": [
                {
                    "type": op.op_type,
                    "path": str(op.path),
                    "content": op.content,
                    "new_path": str(op.new_path) if op.new_path else None,
                    "original_content": op.original_content,
                    "original_exists": op.original_exists,
                }
                for op in self._operations
            ],
        }
        wal_file.write_text(json.dumps(wal_data, indent=2))

    def _clear_wal(self) -> None:
        """Clear write-ahead log after successful commit."""
        wal_file = self.wal_dir / f"{self._transaction_id}.wal"
        if wal_file.exists():
            wal_file.unlink()

    def commit(self) -> bool:
        """
        Commit all operations atomically.

        Returns True if successful, False if rolled back.
        """
        if self._committed:
            return True

        # Write WAL first
        self._write_wal()

        executed = []
        try:
            for op in self._operations:
                if op.op_type == "write":
                    op.path.parent.mkdir(parents=True, exist_ok=True)
                    op.path.write_text(op.content)
                elif op.op_type == "delete":
                    if op.path.exists():
                        op.path.unlink()
                elif op.op_type == "rename":
                    if op.path.exists():
                        # .replace() not .rename(): cross-platform atomic
                        # overwrite. On Windows .rename() raises FileExistsError
                        # if target exists, breaking transactional file ops.
                        op.path.replace(op.new_path)

                executed.append(op)

            self._committed = True
            self._clear_wal()
            return True

        except Exception as e:
            # Rollback executed operations
            self._rollback(executed)
            self._clear_wal()
            raise RuntimeError(f"Transaction failed, rolled back: {e}")

    def _rollback(self, executed: list[FileOperation]) -> None:
        """Rollback executed operations."""
        for op in reversed(executed):
            try:
                if op.op_type == "write":
                    if op.original_exists and op.original_content is not None:
                        op.path.write_text(op.original_content)
                    elif not op.original_exists:
                        op.path.unlink(missing_ok=True)

                elif op.op_type == "delete":
                    if op.original_exists and op.original_content is not None:
                        op.path.write_text(op.original_content)

                elif op.op_type == "rename":
                    if op.new_path and op.new_path.exists():
                        # Rollback: restore by overwriting whatever's at
                        # op.path now (use .replace() so Windows doesn't
                        # crash with FileExistsError).
                        op.new_path.replace(op.path)

            except Exception:
                pass  # Best effort rollback

    def rollback(self) -> None:
        """Manually rollback all operations."""
        self._rollback(self._operations)
        self._clear_wal()


# =============================================================================
# File Encoding Detection (P1-48)
# =============================================================================


class FileEncodingHandler:
    """
    Handles file encoding detection and preservation.

    P1-48: Preserve file encoding and line endings
    """

    COMMON_ENCODINGS = ["utf-8", "utf-8-sig", "latin-1", "cp1252", "ascii"]

    def detect_encoding(self, file_path: Path) -> str:
        """Detect file encoding."""
        try:
            import chardet

            with open(file_path, "rb") as f:
                raw = f.read(10000)  # Read first 10KB
                result = chardet.detect(raw)
                return result["encoding"] or "utf-8"
        except ImportError:
            # Fallback without chardet
            for encoding in self.COMMON_ENCODINGS:
                try:
                    with open(file_path, encoding=encoding) as f:
                        f.read()
                    return encoding
                except UnicodeDecodeError:
                    continue
            return "utf-8"

    def detect_line_ending(self, file_path: Path) -> str:
        """Detect line ending style."""
        with open(file_path, "rb") as f:
            content = f.read(10000)

        if b"\r\n" in content:
            return "\r\n"  # Windows
        elif b"\r" in content:
            return "\r"  # Old Mac
        else:
            return "\n"  # Unix

    def read_file(self, file_path: Path) -> tuple[str, str, str]:
        """
        Read file preserving encoding and line ending info.

        Returns:
            Tuple of (content, encoding, line_ending)
        """
        encoding = self.detect_encoding(file_path)
        line_ending = self.detect_line_ending(file_path)

        with open(file_path, encoding=encoding, newline="") as f:
            content = f.read()

        return content, encoding, line_ending

    def write_file(
        self,
        file_path: Path,
        content: str,
        encoding: str = "utf-8",
        line_ending: str = "\n",
    ) -> None:
        """Write file with specified encoding and line ending."""
        # Normalize line endings
        content = content.replace("\r\n", "\n").replace("\r", "\n")
        if line_ending != "\n":
            content = content.replace("\n", line_ending)

        with open(file_path, "w", encoding=encoding, newline="") as f:
            f.write(content)


# =============================================================================
# Concurrent Modification Detection (P1-46)
# =============================================================================


class FileModificationTracker:
    """
    Tracks file modifications to detect concurrent changes.

    P1-46: Add concurrent modification detection
    """

    def __init__(self):
        self._tracked: dict[str, tuple[float, str]] = {}  # path -> (mtime, hash)

    def track(self, file_path: Path) -> None:
        """Start tracking a file."""
        if not file_path.exists():
            self._tracked[str(file_path)] = (0, "")
            return

        mtime = file_path.stat().st_mtime
        content_hash = self._hash_file(file_path)
        self._tracked[str(file_path)] = (mtime, content_hash)

    def has_changed(self, file_path: Path) -> bool:
        """Check if file has been modified externally."""
        path_str = str(file_path)

        if path_str not in self._tracked:
            return False

        if not file_path.exists():
            # File was deleted
            return self._tracked[path_str][0] > 0

        old_mtime, old_hash = self._tracked[path_str]
        new_mtime = file_path.stat().st_mtime

        if new_mtime != old_mtime:
            # Mtime changed, verify with hash
            new_hash = self._hash_file(file_path)
            return new_hash != old_hash

        return False

    def _hash_file(self, file_path: Path) -> str:
        """Calculate file content hash."""
        hasher = hashlib.sha256()
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(8192), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    def get_modified_files(self) -> list[Path]:
        """Get list of all modified files."""
        return [Path(p) for p in self._tracked if self.has_changed(Path(p))]


# =============================================================================
# Streaming File Handler (P1-47)
# =============================================================================


class StreamingFileHandler:
    """
    Handles large files with streaming.

    P1-47: Support streaming for large files
    """

    def __init__(self, chunk_size: int = 8192):
        self.chunk_size = chunk_size

    def read_lines(
        self,
        file_path: Path,
        start_line: int = 0,
        max_lines: int | None = None,
        encoding: str = "utf-8",
    ):
        """
        Generator that yields lines from a file.

        Efficient for large files - doesn't load entire file into memory.
        """
        line_num = 0
        lines_yielded = 0

        with open(file_path, encoding=encoding) as f:
            for line in f:
                if line_num >= start_line:
                    yield line_num, line
                    lines_yielded += 1

                    if max_lines and lines_yielded >= max_lines:
                        return

                line_num += 1

    def read_chunks(self, file_path: Path, encoding: str = "utf-8"):
        """Generator that yields file in chunks."""
        with open(file_path, encoding=encoding) as f:
            while True:
                chunk = f.read(self.chunk_size)
                if not chunk:
                    break
                yield chunk

    def write_chunks(
        self,
        file_path: Path,
        chunks,
        encoding: str = "utf-8",
    ) -> int:
        """
        Write file from chunks iterator.

        Returns total bytes written.
        """
        total = 0
        with open(file_path, "w", encoding=encoding) as f:
            for chunk in chunks:
                f.write(chunk)
                total += len(chunk.encode(encoding))
        return total

    def get_file_info(self, file_path: Path) -> dict[str, Any]:
        """Get file information without loading content."""
        stat = file_path.stat()
        return {
            "path": str(file_path),
            "size_bytes": stat.st_size,
            "modified": stat.st_mtime,
            "is_large": stat.st_size > 1024 * 1024,  # >1MB
        }
