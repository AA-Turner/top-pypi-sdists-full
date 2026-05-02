"""Comprehensive tests for sage/core/enterprise.py."""

from __future__ import annotations

import time
import json
import asyncio
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock

import pytest


# =============================================================================
# Tests for LogLevel Enum
# =============================================================================


class TestLogLevel:
    """Tests for LogLevel enum."""

    def test_import(self):
        """LogLevel can be imported."""
        from sage.core.enterprise import LogLevel
        assert LogLevel is not None

    def test_debug(self):
        """DEBUG value."""
        from sage.core.enterprise import LogLevel
        assert LogLevel.DEBUG.value == "debug"

    def test_info(self):
        """INFO value."""
        from sage.core.enterprise import LogLevel
        assert LogLevel.INFO.value == "info"

    def test_warning(self):
        """WARNING value."""
        from sage.core.enterprise import LogLevel
        assert LogLevel.WARNING.value == "warning"

    def test_error(self):
        """ERROR value."""
        from sage.core.enterprise import LogLevel
        assert LogLevel.ERROR.value == "error"

    def test_critical(self):
        """CRITICAL value."""
        from sage.core.enterprise import LogLevel
        assert LogLevel.CRITICAL.value == "critical"


# =============================================================================
# Tests for LogEvent Dataclass
# =============================================================================


class TestLogEvent:
    """Tests for LogEvent dataclass."""

    def test_import(self):
        """LogEvent can be imported."""
        from sage.core.enterprise import LogEvent
        assert LogEvent is not None

    def test_create(self):
        """Create LogEvent."""
        from sage.core.enterprise import LogEvent, LogLevel

        event = LogEvent(
            timestamp=time.time(),
            level=LogLevel.INFO,
            event="test.event",
            message="Test message"
        )
        assert event.level == LogLevel.INFO
        assert event.message == "Test message"

    def test_defaults(self):
        """Default values."""
        from sage.core.enterprise import LogEvent, LogLevel

        event = LogEvent(
            timestamp=time.time(),
            level=LogLevel.INFO,
            event="test",
            message="Test"
        )
        assert event.context == {}
        assert event.trace_id is None
        assert event.span_id is None
        assert event.correlation_id is None

    def test_to_json(self):
        """to_json serializes correctly."""
        from sage.core.enterprise import LogEvent, LogLevel

        event = LogEvent(
            timestamp=time.time(),
            level=LogLevel.ERROR,
            event="error.occurred",
            message="An error happened",
            context={"key": "value"}
        )
        json_str = event.to_json()
        data = json.loads(json_str)

        assert data["level"] == "error"
        assert data["event"] == "error.occurred"
        assert data["message"] == "An error happened"
        assert data["context"] == {"key": "value"}

    def test_to_ecs(self):
        """to_ecs converts to Elastic Common Schema."""
        from sage.core.enterprise import LogEvent, LogLevel

        event = LogEvent(
            timestamp=time.time(),
            level=LogLevel.INFO,
            event="user.login",
            message="User logged in",
            trace_id="trace-123",
            span_id="span-456"
        )
        ecs = event.to_ecs()

        assert ecs["log.level"] == "info"
        assert ecs["event.action"] == "user.login"
        assert ecs["trace.id"] == "trace-123"
        assert ecs["span.id"] == "span-456"


# =============================================================================
# Tests for StructuredLogger Class
# =============================================================================


class TestStructuredLogger:
    """Tests for StructuredLogger class."""

    def test_import(self):
        """StructuredLogger can be imported."""
        from sage.core.enterprise import StructuredLogger
        assert StructuredLogger is not None

    def test_create_default(self):
        """Create with defaults."""
        from sage.core.enterprise import StructuredLogger

        logger = StructuredLogger()
        assert logger.name == "sage"
        assert logger.console_output is True

    def test_create_custom(self, tmp_path):
        """Create with custom settings."""
        from sage.core.enterprise import StructuredLogger

        output_path = tmp_path / "logs.json"
        logger = StructuredLogger(
            name="custom",
            output_path=output_path,
            console_output=False
        )
        assert logger.name == "custom"
        assert logger.output_path == output_path
        assert logger.console_output is False

    def test_set_correlation(self):
        """Set correlation ID."""
        from sage.core.enterprise import StructuredLogger

        logger = StructuredLogger()
        logger.set_correlation("corr-123")
        assert logger._correlation_id == "corr-123"

    def test_set_trace(self):
        """Set trace ID."""
        from sage.core.enterprise import StructuredLogger

        logger = StructuredLogger()
        logger.set_trace("trace-456")
        assert logger._trace_id == "trace-456"

    def test_log(self, tmp_path, capsys):
        """Log an event."""
        from sage.core.enterprise import StructuredLogger, LogLevel

        logger = StructuredLogger(console_output=True)
        event = logger.log(LogLevel.INFO, "test.event", "Test message", key="value")

        assert event.level == LogLevel.INFO
        assert event.event == "test.event"
        assert event.message == "Test message"
        assert event.context == {"key": "value"}

        captured = capsys.readouterr()
        assert "test.event" in captured.out

    def test_log_to_file(self, tmp_path):
        """Log to file."""
        from sage.core.enterprise import StructuredLogger, LogLevel

        log_file = tmp_path / "test.log"
        logger = StructuredLogger(output_path=log_file, console_output=False)
        logger.log(LogLevel.INFO, "file.test", "Writing to file")

        assert log_file.exists()
        content = log_file.read_text()
        assert "file.test" in content

    def test_debug(self, capsys):
        """Debug shorthand."""
        from sage.core.enterprise import StructuredLogger, LogLevel

        logger = StructuredLogger(console_output=False)
        event = logger.debug("debug.event", "Debug message")
        assert event.level == LogLevel.DEBUG

    def test_info(self, capsys):
        """Info shorthand."""
        from sage.core.enterprise import StructuredLogger, LogLevel

        logger = StructuredLogger(console_output=False)
        event = logger.info("info.event", "Info message")
        assert event.level == LogLevel.INFO

    def test_warning(self, capsys):
        """Warning shorthand."""
        from sage.core.enterprise import StructuredLogger, LogLevel

        logger = StructuredLogger(console_output=False)
        event = logger.warning("warning.event", "Warning message")
        assert event.level == LogLevel.WARNING

    def test_error(self, capsys):
        """Error shorthand."""
        from sage.core.enterprise import StructuredLogger, LogLevel

        logger = StructuredLogger(console_output=False)
        event = logger.error("error.event", "Error message")
        assert event.level == LogLevel.ERROR


# =============================================================================
# Tests for AuditAction Enum
# =============================================================================


class TestAuditAction:
    """Tests for AuditAction enum."""

    def test_import(self):
        """AuditAction can be imported."""
        from sage.core.enterprise import AuditAction
        assert AuditAction is not None

    def test_all_values(self):
        """All expected values exist."""
        from sage.core.enterprise import AuditAction

        expected = [
            "create", "read", "update", "delete", "execute",
            "approve", "reject", "login", "logout"
        ]
        values = [a.value for a in AuditAction]
        for e in expected:
            assert e in values


# =============================================================================
# Tests for AuditEntry Dataclass
# =============================================================================


class TestAuditEntry:
    """Tests for AuditEntry dataclass."""

    def test_import(self):
        """AuditEntry can be imported."""
        from sage.core.enterprise import AuditEntry
        assert AuditEntry is not None

    def test_create(self):
        """Create AuditEntry."""
        from sage.core.enterprise import AuditEntry, AuditAction

        entry = AuditEntry(
            id="entry-1",
            timestamp=time.time(),
            action=AuditAction.CREATE,
            actor="user@example.com",
            resource_type="task",
            resource_id="task-123",
            details={"key": "value"}
        )
        assert entry.action == AuditAction.CREATE
        assert entry.actor == "user@example.com"

    def test_defaults(self):
        """Default values."""
        from sage.core.enterprise import AuditEntry, AuditAction

        entry = AuditEntry(
            id="e1",
            timestamp=time.time(),
            action=AuditAction.READ,
            actor="user",
            resource_type="file",
            resource_id="f1",
            details={}
        )
        assert entry.ip_address is None
        assert entry.outcome == "success"

    def test_to_dict(self):
        """to_dict serializes correctly."""
        from sage.core.enterprise import AuditEntry, AuditAction

        entry = AuditEntry(
            id="e1",
            timestamp=time.time(),
            action=AuditAction.DELETE,
            actor="admin",
            resource_type="user",
            resource_id="u1",
            details={"reason": "requested"}
        )
        data = entry.to_dict()

        assert data["id"] == "e1"
        assert data["action"] == "delete"
        assert data["actor"] == "admin"
        assert data["resource_type"] == "user"


# =============================================================================
# Tests for AuditLogger Class
# =============================================================================


class TestAuditLogger:
    """Tests for AuditLogger class."""

    def test_import(self):
        """AuditLogger can be imported."""
        from sage.core.enterprise import AuditLogger
        assert AuditLogger is not None

    def test_create(self):
        """Create AuditLogger."""
        from sage.core.enterprise import AuditLogger

        logger = AuditLogger()
        assert logger._entries == []

    def test_create_with_storage(self, tmp_path):
        """Create with storage path."""
        from sage.core.enterprise import AuditLogger

        logger = AuditLogger(storage_path=tmp_path / "audit")
        assert logger.storage_path == tmp_path / "audit"

    def test_log(self):
        """Log audit entry."""
        from sage.core.enterprise import AuditLogger, AuditAction

        logger = AuditLogger()
        entry = logger.log(
            action=AuditAction.CREATE,
            actor="user@test.com",
            resource_type="project",
            resource_id="proj-1",
            details={"name": "New Project"}
        )

        assert entry.action == AuditAction.CREATE
        assert entry.actor == "user@test.com"
        assert len(logger._entries) == 1

    def test_log_persist(self, tmp_path):
        """Log persists to file."""
        from sage.core.enterprise import AuditLogger, AuditAction

        storage = tmp_path / "audit"
        logger = AuditLogger(storage_path=storage)
        logger.log(
            action=AuditAction.EXECUTE,
            actor="system",
            resource_type="task",
            resource_id="t1"
        )

        audit_file = storage / "audit.jsonl"
        assert audit_file.exists()
        content = audit_file.read_text()
        assert "execute" in content

    def test_query_all(self):
        """Query all entries."""
        from sage.core.enterprise import AuditLogger, AuditAction

        logger = AuditLogger()
        logger.log(AuditAction.CREATE, "user1", "file", "f1")
        logger.log(AuditAction.READ, "user2", "file", "f2")

        results = logger.query()
        assert len(results) == 2

    def test_query_by_action(self):
        """Query by action."""
        from sage.core.enterprise import AuditLogger, AuditAction

        logger = AuditLogger()
        logger.log(AuditAction.CREATE, "user1", "file", "f1")
        logger.log(AuditAction.READ, "user2", "file", "f2")
        logger.log(AuditAction.CREATE, "user3", "file", "f3")

        results = logger.query(action=AuditAction.CREATE)
        assert len(results) == 2

    def test_query_by_actor(self):
        """Query by actor."""
        from sage.core.enterprise import AuditLogger, AuditAction

        logger = AuditLogger()
        logger.log(AuditAction.CREATE, "user1", "file", "f1")
        logger.log(AuditAction.READ, "user1", "file", "f2")
        logger.log(AuditAction.READ, "user2", "file", "f3")

        results = logger.query(actor="user1")
        assert len(results) == 2

    def test_query_by_resource_type(self):
        """Query by resource type."""
        from sage.core.enterprise import AuditLogger, AuditAction

        logger = AuditLogger()
        logger.log(AuditAction.CREATE, "user", "file", "f1")
        logger.log(AuditAction.CREATE, "user", "task", "t1")

        results = logger.query(resource_type="task")
        assert len(results) == 1

    def test_generate_compliance_report(self):
        """Generate compliance report."""
        from sage.core.enterprise import AuditLogger, AuditAction

        logger = AuditLogger()
        logger.log(AuditAction.CREATE, "user1", "file", "f1")
        logger.log(AuditAction.CREATE, "user2", "file", "f2")
        logger.log(AuditAction.DELETE, "admin", "file", "f3")

        report = logger.generate_compliance_report(period_days=30)

        assert report["total_events"] == 3
        assert report["action_breakdown"]["create"] == 2
        assert report["action_breakdown"]["delete"] == 1
        assert "generated_at" in report


# =============================================================================
# Tests for CircuitState Enum
# =============================================================================


class TestCircuitState:
    """Tests for CircuitState enum."""

    def test_import(self):
        """CircuitState can be imported."""
        from sage.core.enterprise import CircuitState
        assert CircuitState is not None

    def test_all_values(self):
        """All expected values exist."""
        from sage.core.enterprise import CircuitState

        assert CircuitState.CLOSED.value == "closed"
        assert CircuitState.OPEN.value == "open"
        assert CircuitState.HALF_OPEN.value == "half_open"


# =============================================================================
# Tests for CircuitBreaker Class
# =============================================================================


class TestCircuitBreaker:
    """Tests for CircuitBreaker class."""

    def test_import(self):
        """CircuitBreaker can be imported."""
        from sage.core.enterprise import CircuitBreaker
        assert CircuitBreaker is not None

    def test_create(self):
        """Create CircuitBreaker."""
        from sage.core.enterprise import CircuitBreaker, CircuitState

        breaker = CircuitBreaker("test")
        assert breaker.name == "test"
        assert breaker.state == CircuitState.CLOSED

    def test_create_custom(self):
        """Create with custom settings."""
        from sage.core.enterprise import CircuitBreaker

        breaker = CircuitBreaker(
            name="custom",
            failure_threshold=10,
            recovery_timeout=120.0,
            half_open_max_calls=3
        )
        assert breaker.failure_threshold == 10
        assert breaker.recovery_timeout == 120.0
        assert breaker.half_open_max_calls == 3

    def test_allow_request_closed(self):
        """Allow request when closed."""
        from sage.core.enterprise import CircuitBreaker

        breaker = CircuitBreaker("test")
        assert breaker.allow_request() is True

    def test_allow_request_open(self):
        """Reject request when open."""
        from sage.core.enterprise import CircuitBreaker, CircuitState

        breaker = CircuitBreaker("test", failure_threshold=2)
        breaker.record_failure()
        breaker.record_failure()

        assert breaker.state == CircuitState.OPEN
        assert breaker.allow_request() is False

    def test_record_success_resets(self):
        """Record success resets failure count."""
        from sage.core.enterprise import CircuitBreaker

        breaker = CircuitBreaker("test", failure_threshold=5)
        breaker.record_failure()
        breaker.record_failure()

        breaker.record_success()
        assert breaker._failure_count == 0

    def test_record_failure_opens_circuit(self):
        """Record failure opens circuit at threshold."""
        from sage.core.enterprise import CircuitBreaker, CircuitState

        breaker = CircuitBreaker("test", failure_threshold=3)
        breaker.record_failure()
        breaker.record_failure()
        assert breaker.state == CircuitState.CLOSED

        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

    def test_half_open_transition(self):
        """Circuit transitions to half-open after timeout."""
        from sage.core.enterprise import CircuitBreaker, CircuitState

        breaker = CircuitBreaker("test", failure_threshold=1, recovery_timeout=0.1)
        breaker.record_failure()
        assert breaker.state == CircuitState.OPEN

        # Wait for recovery timeout
        time.sleep(0.15)
        assert breaker.state == CircuitState.HALF_OPEN

    def test_half_open_success_closes(self):
        """Success in half-open closes circuit."""
        from sage.core.enterprise import CircuitBreaker, CircuitState

        breaker = CircuitBreaker("test", failure_threshold=1, recovery_timeout=0.1)
        breaker.record_failure()

        time.sleep(0.15)
        assert breaker.state == CircuitState.HALF_OPEN

        breaker.record_success()
        assert breaker.state == CircuitState.CLOSED

    @pytest.mark.asyncio
    async def test_execute_success(self):
        """Execute successful function."""
        from sage.core.enterprise import CircuitBreaker

        breaker = CircuitBreaker("test")

        async def success_func():
            return "success"

        result = await breaker.execute(success_func)
        assert result == "success"

    @pytest.mark.asyncio
    async def test_execute_failure(self):
        """Execute failing function."""
        from sage.core.enterprise import CircuitBreaker

        breaker = CircuitBreaker("test", failure_threshold=1)

        async def fail_func():
            raise ValueError("Error")

        with pytest.raises(ValueError):
            await breaker.execute(fail_func)

        from sage.core.enterprise import CircuitState
        assert breaker.state == CircuitState.OPEN

    @pytest.mark.asyncio
    async def test_execute_circuit_open_raises(self):
        """Execute raises when circuit is open."""
        from sage.core.enterprise import CircuitBreaker

        breaker = CircuitBreaker("test", failure_threshold=1)
        breaker.record_failure()

        async def any_func():
            return "result"

        with pytest.raises(RuntimeError, match="open"):
            await breaker.execute(any_func)


# =============================================================================
# Tests for MetricType Enum
# =============================================================================


class TestMetricType:
    """Tests for MetricType enum."""

    def test_import(self):
        """MetricType can be imported."""
        from sage.core.enterprise import MetricType
        assert MetricType is not None

    def test_all_values(self):
        """All expected values exist."""
        from sage.core.enterprise import MetricType

        assert MetricType.COUNTER.value == "counter"
        assert MetricType.GAUGE.value == "gauge"
        assert MetricType.HISTOGRAM.value == "histogram"
        assert MetricType.TIMER.value == "timer"


# =============================================================================
# Tests for Metric Dataclass
# =============================================================================


class TestMetric:
    """Tests for Metric dataclass."""

    def test_import(self):
        """Metric can be imported."""
        from sage.core.enterprise import Metric
        assert Metric is not None

    def test_create(self):
        """Create Metric."""
        from sage.core.enterprise import Metric, MetricType

        metric = Metric(
            name="requests",
            type=MetricType.COUNTER,
            value=100,
            timestamp=time.time()
        )
        assert metric.name == "requests"
        assert metric.type == MetricType.COUNTER
        assert metric.value == 100

    def test_defaults(self):
        """Default values."""
        from sage.core.enterprise import Metric, MetricType

        metric = Metric(
            name="test",
            type=MetricType.GAUGE,
            value=50,
            timestamp=time.time()
        )
        assert metric.tags == {}


# =============================================================================
# Tests for MetricsCollector Class
# =============================================================================


class TestMetricsCollector:
    """Tests for MetricsCollector class."""

    def test_import(self):
        """MetricsCollector can be imported."""
        from sage.core.enterprise import MetricsCollector
        assert MetricsCollector is not None

    def test_create(self):
        """Create MetricsCollector."""
        from sage.core.enterprise import MetricsCollector

        collector = MetricsCollector()
        assert collector._metrics == []
        assert collector._counters == {}

    def test_increment(self):
        """Increment counter."""
        from sage.core.enterprise import MetricsCollector

        collector = MetricsCollector()
        collector.increment("requests")
        collector.increment("requests")
        collector.increment("requests", 5)

        assert collector._counters["requests:"] == 7

    def test_increment_with_tags(self):
        """Increment with tags."""
        from sage.core.enterprise import MetricsCollector

        collector = MetricsCollector()
        collector.increment("requests", method="GET")
        collector.increment("requests", method="POST")
        collector.increment("requests", method="GET")

        assert collector._counters["requests:method=GET"] == 2
        assert collector._counters["requests:method=POST"] == 1

    def test_gauge(self):
        """Set gauge value."""
        from sage.core.enterprise import MetricsCollector

        collector = MetricsCollector()
        collector.gauge("memory_mb", 512)
        collector.gauge("memory_mb", 600)

        assert collector._gauges["memory_mb:"] == 600

    def test_histogram(self):
        """Record histogram values."""
        from sage.core.enterprise import MetricsCollector

        collector = MetricsCollector()
        collector.histogram("latency_ms", 100)
        collector.histogram("latency_ms", 150)
        collector.histogram("latency_ms", 200)

        assert len(collector._histograms["latency_ms:"]) == 3

    def test_timer(self):
        """Timer context manager."""
        from sage.core.enterprise import MetricsCollector

        collector = MetricsCollector()

        with collector.timer("operation_time"):
            time.sleep(0.05)

        assert len(collector._histograms["operation_time:"]) == 1
        assert collector._histograms["operation_time:"][0] >= 0.05

    def test_get_stats(self):
        """Get statistics for metric."""
        from sage.core.enterprise import MetricsCollector

        collector = MetricsCollector()
        collector.histogram("values", 10)
        collector.histogram("values", 20)
        collector.histogram("values", 30)

        stats = collector.get_stats("values")

        assert stats["count"] == 3
        assert stats["min"] == 10
        assert stats["max"] == 30
        assert stats["avg"] == 20
        assert stats["sum"] == 60

    def test_get_stats_empty(self):
        """Get stats for unknown metric."""
        from sage.core.enterprise import MetricsCollector

        collector = MetricsCollector()
        stats = collector.get_stats("unknown")
        assert stats == {}

    def test_export_prometheus(self):
        """Export in Prometheus format."""
        from sage.core.enterprise import MetricsCollector

        collector = MetricsCollector()
        collector.increment("requests")
        collector.gauge("active_connections", 10)

        output = collector.export_prometheus()

        assert "TYPE requests counter" in output
        assert "TYPE active_connections gauge" in output


# =============================================================================
# Tests for NotificationType Enum
# =============================================================================


class TestNotificationType:
    """Tests for NotificationType enum."""

    def test_import(self):
        """NotificationType can be imported."""
        from sage.core.enterprise import NotificationType
        assert NotificationType is not None

    def test_all_values(self):
        """All expected values exist."""
        from sage.core.enterprise import NotificationType

        expected = [
            "task.started", "task.completed", "task.failed",
            "approval.required", "system.error"
        ]
        values = [n.value for n in NotificationType]
        for e in expected:
            assert e in values


# =============================================================================
# Tests for Notification Dataclass
# =============================================================================


class TestNotification:
    """Tests for Notification dataclass."""

    def test_import(self):
        """Notification can be imported."""
        from sage.core.enterprise import Notification
        assert Notification is not None

    def test_create(self):
        """Create Notification."""
        from sage.core.enterprise import Notification, NotificationType

        notif = Notification(
            id="n1",
            type=NotificationType.TASK_COMPLETED,
            title="Task Done",
            message="Your task has completed successfully"
        )
        assert notif.type == NotificationType.TASK_COMPLETED
        assert notif.title == "Task Done"

    def test_defaults(self):
        """Default values."""
        from sage.core.enterprise import Notification, NotificationType

        notif = Notification(
            id="n1",
            type=NotificationType.TASK_STARTED,
            title="Started",
            message="Task started"
        )
        assert notif.data == {}
        assert notif.priority == 1
        assert notif.timestamp > 0


# =============================================================================
# Tests for WebhookChannel Class
# =============================================================================


class TestWebhookChannel:
    """Tests for WebhookChannel class."""

    def test_import(self):
        """WebhookChannel can be imported."""
        from sage.core.enterprise import WebhookChannel
        assert WebhookChannel is not None

    def test_create(self):
        """Create WebhookChannel."""
        from sage.core.enterprise import WebhookChannel

        channel = WebhookChannel("https://hooks.example.com/notify")
        assert channel.url == "https://hooks.example.com/notify"
        assert channel.headers == {}

    def test_create_with_headers(self):
        """Create with custom headers."""
        from sage.core.enterprise import WebhookChannel

        headers = {"Authorization": "Bearer token123"}
        channel = WebhookChannel("https://hooks.example.com", headers=headers)
        assert channel.headers == headers
