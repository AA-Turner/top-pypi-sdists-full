"""Comprehensive tests for sage/core/tool_executor.py - 100% coverage target."""

import asyncio
import os
import tempfile
import time
from pathlib import Path

import pytest

from sage.core.tool_executor import (
    AsyncToolExecutor,
    FileEncodingHandler,
    FileModificationTracker,
    FileOperation,
    FileTransaction,
    ResourceMonitor,
    ResourceUsage,
    SafeShellExecutor,
    ScheduledTool,
    StreamingFileHandler,
    ToolCache,
    ToolChain,
    ToolPriority,
    ToolRateLimiter,
    ToolScheduler,
    cached_tool,
)

# =============================================================================
# ResourceUsage and ResourceMonitor Tests
# =============================================================================


class TestResourceUsage:
    """Tests for ResourceUsage dataclass."""

    def test_resource_usage_creation(self):
        """Test creating ResourceUsage with all fields."""
        usage = ResourceUsage(
            cpu_percent=50.0,
            memory_mb=1024.5,
            disk_read_mb=10.0,
            disk_write_mb=5.0,
            duration_seconds=1.5,
        )
        assert usage.cpu_percent == 50.0
        assert usage.memory_mb == 1024.5
        assert usage.disk_read_mb == 10.0
        assert usage.disk_write_mb == 5.0
        assert usage.duration_seconds == 1.5

    def test_resource_usage_defaults(self):
        """Test ResourceUsage with default values."""
        usage = ResourceUsage()
        assert usage.cpu_percent == 0.0
        assert usage.memory_mb == 0.0
        assert usage.disk_read_mb == 0.0
        assert usage.disk_write_mb == 0.0
        assert usage.duration_seconds == 0.0


class TestResourceMonitor:
    """Tests for ResourceMonitor class."""

    def test_init(self):
        """Test ResourceMonitor initialization."""
        monitor = ResourceMonitor()
        assert monitor._start_time is None
        assert monitor._process is None

    def test_start_and_stop(self):
        """Test starting and stopping monitoring."""
        monitor = ResourceMonitor()
        monitor.start()
        time.sleep(0.01)
        usage = monitor.stop()
        assert isinstance(usage, ResourceUsage)
        assert usage.duration_seconds > 0

    def test_stop_without_start(self):
        """Test stopping without starting."""
        monitor = ResourceMonitor()
        usage = monitor.stop()
        assert isinstance(usage, ResourceUsage)

    def test_stop_without_psutil(self):
        """Test stopping when psutil not available."""
        monitor = ResourceMonitor()
        monitor.start()
        # Manually set _process to None to simulate psutil not available
        monitor._process = None
        usage = monitor.stop()
        assert isinstance(usage, ResourceUsage)


# =============================================================================
# ToolChain Tests
# =============================================================================


class TestToolChain:
    """Tests for ToolChain class."""

    def test_init(self):
        """Test ToolChain initialization."""
        chain = ToolChain(name="test-chain")
        assert chain.name == "test-chain"
        assert chain._steps == []

    def test_add_step(self):
        """Test adding a step to the chain."""
        chain = ToolChain()

        def my_func(x):
            return x * 2

        result = chain.add("double", my_func)
        assert result is chain  # Returns self for chaining
        assert len(chain._steps) == 1

    @pytest.mark.asyncio
    async def test_execute_single_step(self):
        """Test executing a single step."""
        chain = ToolChain()

        def double(x):
            return x * 2

        chain.add("double", double)
        result, steps = await chain.execute(initial_input=5)
        assert result == 10
        assert len(steps) == 1
        assert steps[0]["step"] == "double"
        assert steps[0]["success"] is True

    @pytest.mark.asyncio
    async def test_execute_multiple_steps(self):
        """Test executing multiple steps."""
        chain = ToolChain()
        chain.add("add_one", lambda x: x + 1)
        chain.add("double", lambda x: x * 2)
        chain.add("subtract_three", lambda x: x - 3)

        result, steps = await chain.execute(initial_input=5)
        # (5 + 1) * 2 - 3 = 9
        assert result == 9
        assert len(steps) == 3

    @pytest.mark.asyncio
    async def test_execute_with_transform(self):
        """Test executing with input transform."""
        chain = ToolChain()

        def transform_input(x):
            return x * 10

        chain.add("process", lambda x: x + 1, transform_input=transform_input)

        result, _ = await chain.execute(initial_input=5)
        # transform: 5 -> 50, then add 1 -> 51
        assert result == 51

    @pytest.mark.asyncio
    async def test_execute_async_function(self):
        """Test executing async functions."""
        chain = ToolChain()

        async def async_double(x):
            await asyncio.sleep(0.01)
            return x * 2

        chain.add("async_double", async_double)
        result, _ = await chain.execute(initial_input=5)
        assert result == 10

    @pytest.mark.asyncio
    async def test_execute_with_error(self):
        """Test error handling during execution."""
        chain = ToolChain()

        def failing_func(x):
            raise ValueError("Test error")

        chain.add("fail", failing_func)

        with pytest.raises(ValueError, match="Test error"):
            await chain.execute(initial_input=5)


# =============================================================================
# ToolScheduler Tests
# =============================================================================


class TestToolPriority:
    """Tests for ToolPriority enum."""

    def test_priority_values(self):
        """Test priority enum values."""
        assert ToolPriority.CRITICAL.value == 0
        assert ToolPriority.HIGH.value == 1
        assert ToolPriority.NORMAL.value == 2
        assert ToolPriority.LOW.value == 3
        assert ToolPriority.BACKGROUND.value == 4


class TestScheduledTool:
    """Tests for ScheduledTool dataclass."""

    def test_creation(self):
        """Test creating a ScheduledTool."""

        def my_func():
            pass

        tool = ScheduledTool(
            id="test-id",
            name="test_tool",
            func=my_func,
            args=(1, 2),
            kwargs={"key": "value"},
            priority=ToolPriority.HIGH,
        )
        assert tool.id == "test-id"
        assert tool.name == "test_tool"
        assert tool.priority == ToolPriority.HIGH

    def test_comparison_by_priority(self):
        """Test ScheduledTool comparison by priority."""

        def dummy():
            pass

        low = ScheduledTool("1", "low", dummy, (), {}, ToolPriority.LOW)
        high = ScheduledTool("2", "high", dummy, (), {}, ToolPriority.HIGH)
        critical = ScheduledTool("3", "critical", dummy, (), {}, ToolPriority.CRITICAL)

        assert critical < high < low

    def test_comparison_by_deadline(self):
        """Test ScheduledTool comparison by deadline."""

        def dummy():
            pass

        early = ScheduledTool("1", "early", dummy, (), {}, deadline=time.time() + 10)
        late = ScheduledTool("2", "late", dummy, (), {}, deadline=time.time() + 100)

        assert early < late

    def test_comparison_by_creation(self):
        """Test ScheduledTool comparison by creation time."""

        def dummy():
            pass

        first = ScheduledTool("1", "first", dummy, (), {})
        time.sleep(0.01)
        second = ScheduledTool("2", "second", dummy, (), {})

        assert first < second


class TestToolScheduler:
    """Tests for ToolScheduler class."""

    def test_init(self):
        """Test ToolScheduler initialization."""
        scheduler = ToolScheduler(max_concurrent=5)
        assert scheduler.max_concurrent == 5
        assert scheduler._queue == []

    def test_schedule(self):
        """Test scheduling a tool."""
        scheduler = ToolScheduler()

        def my_func():
            pass

        tool_id = scheduler.schedule("test", my_func, 1, 2, key="value")
        assert len(tool_id) == 8
        assert len(scheduler._queue) == 1

    def test_get_next(self):
        """Test getting next tool to execute."""
        scheduler = ToolScheduler()

        def my_func():
            pass

        scheduler.schedule("test", my_func)
        tool = scheduler.get_next()
        assert tool is not None
        assert tool.name == "test"
        assert tool.id in scheduler._running

    def test_get_next_empty_queue(self):
        """Test getting next when queue is empty."""
        scheduler = ToolScheduler()
        tool = scheduler.get_next()
        assert tool is None

    def test_get_next_max_concurrent(self):
        """Test getting next when at max concurrent."""
        scheduler = ToolScheduler(max_concurrent=1)

        def my_func():
            pass

        scheduler.schedule("test1", my_func)
        scheduler.schedule("test2", my_func)

        tool1 = scheduler.get_next()
        tool2 = scheduler.get_next()

        assert tool1 is not None
        assert tool2 is None  # At max concurrent

    def test_complete(self):
        """Test completing a tool."""
        scheduler = ToolScheduler()

        def my_func():
            pass

        scheduler.schedule("test", my_func)
        tool = scheduler.get_next()
        scheduler.complete(tool.id)
        assert tool.id not in scheduler._running

    @pytest.mark.asyncio
    async def test_process_queue(self):
        """Test processing all scheduled tools."""
        scheduler = ToolScheduler()
        results = []

        def append_result(n):
            results.append(n)
            return n

        scheduler.schedule("task1", append_result, 1)
        scheduler.schedule("task2", append_result, 2)

        queue_results = await scheduler.process_queue()
        assert len(queue_results) == 2
        assert 1 in results
        assert 2 in results


# =============================================================================
# SafeShellExecutor Tests
# =============================================================================


class TestSafeShellExecutor:
    """Tests for SafeShellExecutor class."""

    @pytest.fixture
    def temp_dir(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            yield Path(tmpdir)

    def test_init(self, temp_dir):
        """Test SafeShellExecutor initialization."""
        executor = SafeShellExecutor(temp_dir)
        assert executor.cwd == temp_dir
        assert executor.timeout == 60

    def test_is_safe_allowed_command(self, temp_dir):
        """Test checking allowed commands."""
        executor = SafeShellExecutor(temp_dir)
        is_safe, reason = executor.is_safe("ls -la")
        assert is_safe is True
        assert reason is None

    def test_is_safe_blocked_pattern_rm_rf(self, temp_dir):
        """Test blocking dangerous rm commands."""
        executor = SafeShellExecutor(temp_dir)
        is_safe, reason = executor.is_safe("rm -rf /")
        assert is_safe is False
        assert "Blocked pattern" in reason

    def test_is_safe_blocked_pattern_sudo(self, temp_dir):
        """Test blocking sudo commands."""
        executor = SafeShellExecutor(temp_dir)
        is_safe, reason = executor.is_safe("sudo rm file")
        assert is_safe is False

    def test_is_safe_blocked_pattern_pipe_sh(self, temp_dir):
        """Test blocking pipe to shell."""
        executor = SafeShellExecutor(temp_dir)
        is_safe, reason = executor.is_safe("echo test | sh")
        assert is_safe is False

    def test_is_safe_not_in_allowlist(self, temp_dir):
        """Test rejecting commands not in allowlist."""
        executor = SafeShellExecutor(temp_dir)
        is_safe, reason = executor.is_safe("dangerous_command")
        assert is_safe is False
        assert "not in allowlist" in reason

    def test_is_safe_empty_command(self, temp_dir):
        """Test handling empty commands."""
        executor = SafeShellExecutor(temp_dir)
        is_safe, reason = executor.is_safe("")
        assert is_safe is False

    def test_execute_allowed_command(self, temp_dir):
        """Test executing allowed command."""
        executor = SafeShellExecutor(temp_dir)
        code, stdout, stderr = executor.execute("echo hello")
        assert code == 0
        assert "hello" in stdout

    def test_execute_blocked_command(self, temp_dir):
        """Test executing blocked command."""
        executor = SafeShellExecutor(temp_dir)
        code, stdout, stderr = executor.execute("rm -rf /")
        assert code == -1
        assert "blocked" in stderr.lower()

    def test_execute_with_env(self, temp_dir):
        """Test executing with environment variables."""
        executor = SafeShellExecutor(temp_dir)
        code, stdout, stderr = executor.execute("echo $TEST_VAR", env={"TEST_VAR": "hello"})
        # Note: without shell=True, env vars won't expand this way
        # but the command should still run


# =============================================================================
# ToolRateLimiter Tests
# =============================================================================


class TestToolRateLimiter:
    """Tests for ToolRateLimiter class."""

    def test_init(self):
        """Test ToolRateLimiter initialization."""
        limiter = ToolRateLimiter(max_per_second=5.0, max_per_minute=50.0, burst_size=10)
        assert limiter.max_per_second == 5.0
        assert limiter.max_per_minute == 50.0
        assert limiter.burst_size == 10

    def test_acquire_within_limit(self):
        """Test acquiring when within limits."""
        limiter = ToolRateLimiter(burst_size=5)
        for _ in range(5):
            assert limiter.acquire(timeout=0.1)

    def test_acquire_timeout(self):
        """Test acquire timeout."""
        limiter = ToolRateLimiter(max_per_second=0.1, burst_size=1)
        assert limiter.acquire(timeout=0.01)
        # Second acquire should timeout quickly
        assert not limiter.acquire(timeout=0.05)

    def test_get_stats(self):
        """Test getting rate limiter stats."""
        limiter = ToolRateLimiter(burst_size=10)
        limiter.acquire(timeout=0.01)

        stats = limiter.get_stats()
        assert "tokens_available" in stats
        assert "burst_size" in stats
        assert stats["burst_size"] == 10


# =============================================================================
# AsyncToolExecutor Tests
# =============================================================================


class TestAsyncToolExecutor:
    """Tests for AsyncToolExecutor class."""

    def test_init(self):
        """Test AsyncToolExecutor initialization."""
        executor = AsyncToolExecutor(max_concurrent=5)
        assert executor.max_concurrent == 5

    @pytest.mark.asyncio
    async def test_execute_sync_function(self):
        """Test executing a sync function."""
        executor = AsyncToolExecutor()

        def my_func(x):
            return x * 2

        result = await executor.execute("test", my_func, 5)
        assert result == 10

    @pytest.mark.asyncio
    async def test_execute_async_function(self):
        """Test executing an async function."""
        executor = AsyncToolExecutor()

        async def async_func(x):
            await asyncio.sleep(0.01)
            return x * 2

        result = await executor.execute("test", async_func, 5)
        assert result == 10

    @pytest.mark.asyncio
    async def test_execute_many(self):
        """Test executing many tasks concurrently."""
        executor = AsyncToolExecutor(max_concurrent=3)

        def double(x):
            return x * 2

        tasks = [
            ("task1", double, (1,), {}),
            ("task2", double, (2,), {}),
            ("task3", double, (3,), {}),
        ]

        results = await executor.execute_many(tasks)
        assert len(results) == 3
        assert all(r["success"] for r in results)

    @pytest.mark.asyncio
    async def test_execute_with_rate_limiter(self):
        """Test execution with rate limiter."""
        limiter = ToolRateLimiter(burst_size=1, max_per_second=0.1)
        executor = AsyncToolExecutor(rate_limiter=limiter)

        async def my_func():
            return "ok"

        result = await executor.execute("test", my_func)
        assert result == "ok"


# =============================================================================
# ToolCache Tests
# =============================================================================


class TestToolCache:
    """Tests for ToolCache class."""

    def test_init(self):
        """Test ToolCache initialization."""
        cache = ToolCache(max_entries=100, ttl_seconds=300)
        assert cache.max_entries == 100
        assert cache.ttl_seconds == 300

    def test_get_miss(self):
        """Test cache miss."""
        cache = ToolCache()
        found, value = cache.get("func", (), {})
        assert found is False
        assert value is None

    def test_set_and_get(self):
        """Test setting and getting cached values."""
        cache = ToolCache()
        cache.set("func", (1, 2), {"key": "value"}, "result")
        found, value = cache.get("func", (1, 2), {"key": "value"})
        assert found is True
        assert value == "result"

    def test_ttl_expiry(self):
        """Test TTL expiration."""
        cache = ToolCache(ttl_seconds=0)  # Immediate expiry
        cache.set("func", (), {}, "result")
        time.sleep(0.01)
        found, _ = cache.get("func", (), {})
        assert found is False

    def test_max_entries_eviction(self):
        """Test eviction when at max entries."""
        cache = ToolCache(max_entries=2)
        cache.set("func1", (), {}, "result1")
        cache.set("func2", (), {}, "result2")
        cache.set("func3", (), {}, "result3")

        # One entry should be evicted
        assert len(cache._cache) == 2

    def test_invalidate_all(self):
        """Test invalidating all entries."""
        cache = ToolCache()
        cache.set("func1", (), {}, "r1")
        cache.set("func2", (), {}, "r2")

        count = cache.invalidate()
        assert count == 2
        assert len(cache._cache) == 0


class TestCachedToolDecorator:
    """Tests for cached_tool decorator."""

    @pytest.mark.asyncio
    async def test_caching_sync_function(self):
        """Test caching a sync function."""
        cache = ToolCache()
        call_count = [0]

        @cached_tool(cache)
        def expensive_func(x):
            call_count[0] += 1
            return x * 2

        result1 = await expensive_func(5)
        result2 = await expensive_func(5)

        assert result1 == 10
        assert result2 == 10
        assert call_count[0] == 1

    @pytest.mark.asyncio
    async def test_caching_async_function(self):
        """Test caching an async function."""
        cache = ToolCache()
        call_count = [0]

        @cached_tool(cache)
        async def async_expensive_func(x):
            call_count[0] += 1
            return x * 2

        result1 = await async_expensive_func(5)
        result2 = await async_expensive_func(5)

        assert result1 == 10
        assert result2 == 10
        assert call_count[0] == 1


# =============================================================================
# FileOperation and FileTransaction Tests
# =============================================================================


class TestFileOperation:
    """Tests for FileOperation dataclass."""

    def test_creation(self):
        """Test creating a FileOperation."""
        op = FileOperation(
            op_type="write",
            path=Path("/tmp/test.txt"),
            content="hello",
        )
        assert op.op_type == "write"
        assert op.path == Path("/tmp/test.txt")
        assert op.content == "hello"


class TestFileTransaction:
    """Tests for FileTransaction class."""

    def test_init(self):
        """Test FileTransaction initialization."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tx = FileTransaction(Path(tmpdir))
            assert tx.base_dir == Path(tmpdir)
            assert tx._operations == []

    def test_write_new_file(self):
        """Test writing a new file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tx = FileTransaction(Path(tmpdir))
            file_path = Path(tmpdir) / "test.txt"

            tx.write(file_path, "hello world")
            assert len(tx._operations) == 1

    def test_write_existing_file(self):
        """Test writing to existing file stores original."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            file_path.write_text("original")

            tx = FileTransaction(Path(tmpdir))
            tx.write(file_path, "modified")

            assert tx._operations[0].original_content == "original"

    def test_delete_file(self):
        """Test deleting a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            file_path.write_text("content")

            tx = FileTransaction(Path(tmpdir))
            tx.delete(file_path)

            assert tx._operations[0].op_type == "delete"

    def test_rename_file(self):
        """Test renaming a file."""
        with tempfile.TemporaryDirectory() as tmpdir:
            old_path = Path(tmpdir) / "old.txt"
            new_path = Path(tmpdir) / "new.txt"
            old_path.write_text("content")

            tx = FileTransaction(Path(tmpdir))
            tx.rename(old_path, new_path)

            assert tx._operations[0].op_type == "rename"

    def test_commit(self):
        """Test committing transaction."""
        with tempfile.TemporaryDirectory() as tmpdir:
            tx = FileTransaction(Path(tmpdir))
            file_path = Path(tmpdir) / "test.txt"

            tx.write(file_path, "hello")
            tx.commit()

            assert file_path.exists()
            assert file_path.read_text() == "hello"

    def test_rollback(self):
        """Test rolling back transaction."""
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            file_path.write_text("original")

            tx = FileTransaction(Path(tmpdir))
            tx.write(file_path, "modified")
            tx.commit()
            tx.rollback()

            assert file_path.read_text() == "original"


# =============================================================================
# FileEncodingHandler Tests
# =============================================================================


class TestFileEncodingHandler:
    """Tests for FileEncodingHandler class."""

    def test_detect_encoding_utf8(self):
        """Test detecting UTF-8 encoding."""
        handler = FileEncodingHandler()
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("Hello, world!")
            f.flush()
            try:
                encoding = handler.detect_encoding(Path(f.name))
                assert encoding.lower() in ["utf-8", "ascii"]
            finally:
                os.unlink(f.name)

    def test_detect_line_ending_unix(self):
        """Test detecting Unix line endings."""
        handler = FileEncodingHandler()
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
            f.write(b"line1\nline2\n")
            f.flush()
            try:
                ending = handler.detect_line_ending(Path(f.name))
                assert ending == "\n"
            finally:
                os.unlink(f.name)

    def test_detect_line_ending_windows(self):
        """Test detecting Windows line endings."""
        handler = FileEncodingHandler()
        with tempfile.NamedTemporaryFile(mode="wb", suffix=".txt", delete=False) as f:
            f.write(b"line1\r\nline2\r\n")
            f.flush()
            try:
                ending = handler.detect_line_ending(Path(f.name))
                assert ending == "\r\n"
            finally:
                os.unlink(f.name)

    def test_read_file(self):
        """Test reading file with encoding info."""
        handler = FileEncodingHandler()
        with tempfile.NamedTemporaryFile(
            mode="w", suffix=".txt", delete=False, encoding="utf-8"
        ) as f:
            f.write("Hello world")
            f.flush()
            try:
                content, encoding, line_ending = handler.read_file(Path(f.name))
                assert content == "Hello world"
            finally:
                os.unlink(f.name)

    def test_write_file(self):
        """Test writing file."""
        handler = FileEncodingHandler()
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            handler.write_file(file_path, "Hello world", "utf-8", "\n")
            assert file_path.read_text() == "Hello world"


# =============================================================================
# FileModificationTracker Tests
# =============================================================================


class TestFileModificationTracker:
    """Tests for FileModificationTracker class."""

    def test_init(self):
        """Test FileModificationTracker initialization."""
        tracker = FileModificationTracker()
        assert tracker._tracked == {}

    def test_track_existing_file(self):
        """Test tracking an existing file."""
        tracker = FileModificationTracker()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("content")
            f.flush()
            try:
                tracker.track(Path(f.name))
                assert str(Path(f.name)) in tracker._tracked
            finally:
                os.unlink(f.name)

    def test_track_nonexistent_file(self):
        """Test tracking a nonexistent file."""
        tracker = FileModificationTracker()
        tracker.track(Path("/nonexistent/file.txt"))
        assert tracker._tracked["/nonexistent/file.txt"] == (0, "")

    def test_has_changed_untracked(self):
        """Test has_changed for untracked file."""
        tracker = FileModificationTracker()
        assert tracker.has_changed(Path("/some/file.txt")) is False

    def test_has_changed_unchanged(self):
        """Test has_changed for unchanged file."""
        tracker = FileModificationTracker()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("content")
            f.flush()
            try:
                tracker.track(Path(f.name))
                assert tracker.has_changed(Path(f.name)) is False
            finally:
                os.unlink(f.name)

    def test_has_changed_modified(self):
        """Test has_changed for modified file."""
        tracker = FileModificationTracker()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("original")
            f.flush()
            tracker.track(Path(f.name))

            time.sleep(0.01)
            Path(f.name).write_text("modified")

            try:
                assert tracker.has_changed(Path(f.name)) is True
            finally:
                os.unlink(f.name)


# =============================================================================
# StreamingFileHandler Tests
# =============================================================================


class TestStreamingFileHandler:
    """Tests for StreamingFileHandler class."""

    def test_init(self):
        """Test StreamingFileHandler initialization."""
        handler = StreamingFileHandler(chunk_size=1024)
        assert handler.chunk_size == 1024

    def test_read_lines(self):
        """Test reading lines from a file."""
        handler = StreamingFileHandler()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("line1\nline2\nline3\n")
            f.flush()
            try:
                lines = list(handler.read_lines(Path(f.name)))
                assert len(lines) == 3
                assert lines[0] == (0, "line1\n")
            finally:
                os.unlink(f.name)

    def test_read_lines_with_start(self):
        """Test reading lines from offset."""
        handler = StreamingFileHandler()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("line1\nline2\nline3\n")
            f.flush()
            try:
                lines = list(handler.read_lines(Path(f.name), start_line=1))
                assert len(lines) == 2
                assert lines[0] == (1, "line2\n")
            finally:
                os.unlink(f.name)

    def test_read_chunks(self):
        """Test reading file in chunks."""
        handler = StreamingFileHandler(chunk_size=10)
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("a" * 25)
            f.flush()
            try:
                chunks = list(handler.read_chunks(Path(f.name)))
                assert len(chunks) == 3
            finally:
                os.unlink(f.name)

    def test_write_chunks(self):
        """Test writing file from chunks."""
        handler = StreamingFileHandler()
        with tempfile.TemporaryDirectory() as tmpdir:
            file_path = Path(tmpdir) / "test.txt"
            chunks = ["chunk1", "chunk2", "chunk3"]

            total = handler.write_chunks(file_path, iter(chunks))
            assert file_path.read_text() == "chunk1chunk2chunk3"

    def test_get_file_info(self):
        """Test getting file information."""
        handler = StreamingFileHandler()
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            f.write("content")
            f.flush()
            try:
                info = handler.get_file_info(Path(f.name))
                assert "path" in info
                assert "size_bytes" in info
                assert info["size_bytes"] == 7
            finally:
                os.unlink(f.name)
