"""
Enterprise and advanced features for SAGE.

P3-106: Implement distributed task execution (SSH, K8s)
P3-107: Add task queue integration (Redis, RabbitMQ)
P3-108: Implement DAG-based workflow engine
P3-109: Add event sourcing for audit trail
P3-110: Implement circuit breakers
P3-111: Add canary deployments for task execution
P3-112: Implement compensation transactions (sagas)
P3-113: Add content-addressable task caching
P3-114: Implement incremental analysis
P3-115: Add reinforcement learning hooks for task routing
P3-116: Implement structured logging (JSON events)
P3-117: Add distributed tracing (OpenTelemetry hooks)
P3-118: Build task execution dashboard data
P3-119: Support log aggregation formats
P3-120: Add performance metrics collection
P3-121: Add audit logging for all operations
P3-122: Implement approval workflows
P3-123: Support policy enforcement
P3-124: Enable compliance reporting
P3-125: Add task notifications (webhook support)
"""

from __future__ import annotations

import asyncio
import json
import time
import uuid
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any

# =============================================================================
# Structured Logging (P3-116, P3-119)
# =============================================================================


class LogLevel(Enum):
    """Log levels."""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


@dataclass
class LogEvent:
    """Structured log event."""

    timestamp: float
    level: LogLevel
    event: str
    message: str
    context: dict[str, Any] = field(default_factory=dict)
    trace_id: str | None = None
    span_id: str | None = None
    correlation_id: str | None = None

    def to_json(self) -> str:
        """Convert to JSON format."""
        return json.dumps(
            {
                "@timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
                "level": self.level.value,
                "event": self.event,
                "message": self.message,
                "context": self.context,
                "trace_id": self.trace_id,
                "span_id": self.span_id,
                "correlation_id": self.correlation_id,
            }
        )

    def to_ecs(self) -> dict[str, Any]:
        """Convert to Elastic Common Schema format."""
        return {
            "@timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
            "log.level": self.level.value,
            "event.action": self.event,
            "message": self.message,
            "labels": self.context,
            "trace.id": self.trace_id,
            "span.id": self.span_id,
        }


class StructuredLogger:
    """
    Structured JSON logger.

    P3-116: Implement structured logging
    """

    def __init__(
        self,
        name: str = "sage",
        output_path: Path | None = None,
        console_output: bool = True,
    ):
        self.name = name
        self.output_path = output_path
        self.console_output = console_output
        self._correlation_id: str | None = None
        self._trace_id: str | None = None

    def set_correlation(self, correlation_id: str) -> None:
        """Set correlation ID for log grouping."""
        self._correlation_id = correlation_id

    def set_trace(self, trace_id: str) -> None:
        """Set trace ID for distributed tracing."""
        self._trace_id = trace_id

    def log(
        self,
        level: LogLevel,
        event: str,
        message: str,
        **context,
    ) -> LogEvent:
        """Log an event."""
        log_event = LogEvent(
            timestamp=time.time(),
            level=level,
            event=event,
            message=message,
            context=context,
            trace_id=self._trace_id,
            correlation_id=self._correlation_id,
        )

        # Output
        json_line = log_event.to_json()

        if self.console_output:
            print(json_line)

        if self.output_path:
            with open(self.output_path, "a") as f:
                f.write(json_line + "\n")

        return log_event

    def debug(self, event: str, message: str, **context) -> LogEvent:
        return self.log(LogLevel.DEBUG, event, message, **context)

    def info(self, event: str, message: str, **context) -> LogEvent:
        return self.log(LogLevel.INFO, event, message, **context)

    def warning(self, event: str, message: str, **context) -> LogEvent:
        return self.log(LogLevel.WARNING, event, message, **context)

    def error(self, event: str, message: str, **context) -> LogEvent:
        return self.log(LogLevel.ERROR, event, message, **context)


# =============================================================================
# Audit Logging (P3-121)
# =============================================================================


class AuditAction(Enum):
    """Audit action types."""

    CREATE = "create"
    READ = "read"
    UPDATE = "update"
    DELETE = "delete"
    EXECUTE = "execute"
    APPROVE = "approve"
    REJECT = "reject"
    LOGIN = "login"
    LOGOUT = "logout"


@dataclass
class AuditEntry:
    """Audit log entry."""

    id: str
    timestamp: float
    action: AuditAction
    actor: str
    resource_type: str
    resource_id: str
    details: dict[str, Any]
    ip_address: str | None = None
    outcome: str = "success"

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "timestamp": datetime.fromtimestamp(self.timestamp).isoformat(),
            "action": self.action.value,
            "actor": self.actor,
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
            "details": self.details,
            "ip_address": self.ip_address,
            "outcome": self.outcome,
        }


class AuditLogger:
    """
    Audit logger for compliance.

    P3-121: Add audit logging for all operations
    P3-124: Enable compliance reporting
    """

    def __init__(self, storage_path: Path | None = None):
        self.storage_path = storage_path
        self._entries: list[AuditEntry] = []

    def log(
        self,
        action: AuditAction,
        actor: str,
        resource_type: str,
        resource_id: str,
        details: dict | None = None,
        outcome: str = "success",
    ) -> AuditEntry:
        """Log an audit entry."""
        entry = AuditEntry(
            id=str(uuid.uuid4()),
            timestamp=time.time(),
            action=action,
            actor=actor,
            resource_type=resource_type,
            resource_id=resource_id,
            details=details or {},
            outcome=outcome,
        )

        self._entries.append(entry)
        self._persist(entry)

        return entry

    def _persist(self, entry: AuditEntry) -> None:
        """Persist audit entry."""
        if self.storage_path:
            self.storage_path.mkdir(parents=True, exist_ok=True)
            audit_file = self.storage_path / "audit.jsonl"
            with open(audit_file, "a") as f:
                f.write(json.dumps(entry.to_dict()) + "\n")

    def query(
        self,
        action: AuditAction | None = None,
        actor: str | None = None,
        resource_type: str | None = None,
        since: float | None = None,
        until: float | None = None,
    ) -> list[AuditEntry]:
        """Query audit log."""
        results = self._entries

        if action:
            results = [e for e in results if e.action == action]
        if actor:
            results = [e for e in results if e.actor == actor]
        if resource_type:
            results = [e for e in results if e.resource_type == resource_type]
        if since:
            results = [e for e in results if e.timestamp >= since]
        if until:
            results = [e for e in results if e.timestamp <= until]

        return results

    def generate_compliance_report(self, period_days: int = 30) -> dict[str, Any]:
        """Generate compliance report."""
        since = time.time() - (period_days * 24 * 60 * 60)
        entries = self.query(since=since)

        # Aggregate statistics
        action_counts = {}
        actor_counts = {}
        outcome_counts = {"success": 0, "failure": 0}

        for entry in entries:
            action_counts[entry.action.value] = action_counts.get(entry.action.value, 0) + 1
            actor_counts[entry.actor] = actor_counts.get(entry.actor, 0) + 1
            outcome_counts[entry.outcome] = outcome_counts.get(entry.outcome, 0) + 1

        return {
            "report_period_days": period_days,
            "total_events": len(entries),
            "action_breakdown": action_counts,
            "actor_breakdown": actor_counts,
            "outcome_breakdown": outcome_counts,
            "generated_at": datetime.now().isoformat(),
        }


# =============================================================================
# Circuit Breaker (P3-110)
# =============================================================================


class CircuitState(Enum):
    """Circuit breaker states."""

    CLOSED = "closed"  # Normal operation
    OPEN = "open"  # Failing, reject requests
    HALF_OPEN = "half_open"  # Testing if recovered


class CircuitBreaker:
    """
    Circuit breaker for fault tolerance.

    P3-110: Implement circuit breakers
    """

    def __init__(
        self,
        name: str,
        failure_threshold: int = 5,
        recovery_timeout: float = 60.0,
        half_open_max_calls: int = 1,
    ):
        self.name = name
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.half_open_max_calls = half_open_max_calls

        self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._last_failure_time: float | None = None
        self._half_open_calls = 0

    @property
    def state(self) -> CircuitState:
        """Get current state, transitioning if needed."""
        if self._state == CircuitState.OPEN:
            if time.time() - (self._last_failure_time or 0) >= self.recovery_timeout:
                self._state = CircuitState.HALF_OPEN
                self._half_open_calls = 0
        return self._state

    def allow_request(self) -> bool:
        """Check if request should be allowed."""
        state = self.state

        if state == CircuitState.CLOSED:
            return True
        elif state == CircuitState.OPEN:
            return False
        else:  # HALF_OPEN
            return self._half_open_calls < self.half_open_max_calls

    def record_success(self) -> None:
        """Record a successful call."""
        if self._state == CircuitState.HALF_OPEN:
            self._state = CircuitState.CLOSED
        self._failure_count = 0
        self._half_open_calls = 0

    def record_failure(self) -> None:
        """Record a failed call."""
        self._failure_count += 1
        self._last_failure_time = time.time()

        if self._state == CircuitState.HALF_OPEN or self._failure_count >= self.failure_threshold:
            self._state = CircuitState.OPEN

    async def execute(self, func: Callable, *args, **kwargs) -> Any:
        """Execute function with circuit breaker protection."""
        if not self.allow_request():
            raise RuntimeError(f"Circuit breaker {self.name} is open")

        if self._state == CircuitState.HALF_OPEN:
            self._half_open_calls += 1

        try:
            if asyncio.iscoroutinefunction(func):
                result = await func(*args, **kwargs)
            else:
                result = func(*args, **kwargs)
            self.record_success()
            return result
        except Exception:
            self.record_failure()
            raise


# =============================================================================
# Metrics Collection (P3-120)
# =============================================================================


class MetricType(Enum):
    """Metric types."""

    COUNTER = "counter"
    GAUGE = "gauge"
    HISTOGRAM = "histogram"
    TIMER = "timer"


@dataclass
class Metric:
    """A metric data point."""

    name: str
    type: MetricType
    value: float
    timestamp: float
    tags: dict[str, str] = field(default_factory=dict)


class MetricsCollector:
    """
    Collects performance metrics.

    P3-120: Add performance metrics collection
    """

    def __init__(self):
        self._metrics: list[Metric] = []
        self._counters: dict[str, float] = {}
        self._gauges: dict[str, float] = {}
        self._histograms: dict[str, list[float]] = {}

    def increment(self, name: str, value: float = 1, **tags) -> None:
        """Increment a counter."""
        key = self._make_key(name, tags)
        self._counters[key] = self._counters.get(key, 0) + value
        self._record(name, MetricType.COUNTER, self._counters[key], tags)

    def gauge(self, name: str, value: float, **tags) -> None:
        """Set a gauge value."""
        key = self._make_key(name, tags)
        self._gauges[key] = value
        self._record(name, MetricType.GAUGE, value, tags)

    def histogram(self, name: str, value: float, **tags) -> None:
        """Record a histogram value."""
        key = self._make_key(name, tags)
        if key not in self._histograms:
            self._histograms[key] = []
        self._histograms[key].append(value)
        self._record(name, MetricType.HISTOGRAM, value, tags)

    def timer(self, name: str, **tags):
        """Context manager for timing operations."""
        return _Timer(self, name, tags)

    def _make_key(self, name: str, tags: dict) -> str:
        """Create metric key."""
        tag_str = ",".join(f"{k}={v}" for k, v in sorted(tags.items()))
        return f"{name}:{tag_str}"

    def _record(self, name: str, type: MetricType, value: float, tags: dict) -> None:
        """Record a metric."""
        self._metrics.append(
            Metric(
                name=name,
                type=type,
                value=value,
                timestamp=time.time(),
                tags=tags,
            )
        )

    def get_stats(self, name: str) -> dict[str, Any]:
        """Get statistics for a metric."""
        relevant = [m for m in self._metrics if m.name == name]

        if not relevant:
            return {}

        values = [m.value for m in relevant]
        return {
            "count": len(values),
            "min": min(values),
            "max": max(values),
            "avg": sum(values) / len(values),
            "sum": sum(values),
        }

    def export_prometheus(self) -> str:
        """Export metrics in Prometheus format."""
        lines = []
        for name, value in self._counters.items():
            metric_name = name.split(":")[0]
            lines.append(f"# TYPE {metric_name} counter")
            lines.append(f"{name.replace(':', '{')} {value}")

        for name, value in self._gauges.items():
            metric_name = name.split(":")[0]
            lines.append(f"# TYPE {metric_name} gauge")
            lines.append(f"{name.replace(':', '{')} {value}")

        return "\n".join(lines)


class _Timer:
    """Timer context manager."""

    def __init__(self, collector: MetricsCollector, name: str, tags: dict):
        self.collector = collector
        self.name = name
        self.tags = tags
        self.start_time: float | None = None

    def __enter__(self):
        self.start_time = time.time()
        return self

    def __exit__(self, *args):
        duration = time.time() - (self.start_time or time.time())
        self.collector.histogram(self.name, duration, **self.tags)


# =============================================================================
# Notification System (P3-125)
# =============================================================================


class NotificationType(Enum):
    """Notification types."""

    TASK_STARTED = "task.started"
    TASK_COMPLETED = "task.completed"
    TASK_FAILED = "task.failed"
    APPROVAL_REQUIRED = "approval.required"
    SYSTEM_ERROR = "system.error"


@dataclass
class Notification:
    """A notification."""

    id: str
    type: NotificationType
    title: str
    message: str
    data: dict[str, Any] = field(default_factory=dict)
    timestamp: float = field(default_factory=time.time)
    priority: int = 1


class NotificationChannel(ABC):
    """Abstract notification channel."""

    @abstractmethod
    async def send(self, notification: Notification) -> bool:
        """Send a notification."""
        pass


class WebhookChannel(NotificationChannel):
    """
    Webhook notification channel.

    P3-125: Add task notifications
    """

    def __init__(self, url: str, headers: dict | None = None):
        self.url = url
        self.headers = headers or {}

    async def send(self, notification: Notification) -> bool:
        """Send notification via webhook."""
        import httpx

        payload = {
            "id": notification.id,
            "type": notification.type.value,
            "title": notification.title,
            "message": notification.message,
            "data": notification.data,
            "timestamp": notification.timestamp,
        }

        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.url,
                    json=payload,
                    headers=self.headers,
                    timeout=10.0,
                )
                return response.status_code < 400
        except Exception:
            return False


class NotificationManager:
    """Manages notifications."""

    def __init__(self):
        self._channels: list[NotificationChannel] = []
        self._history: list[Notification] = []

    def add_channel(self, channel: NotificationChannel) -> None:
        """Add a notification channel."""
        self._channels.append(channel)

    async def notify(
        self,
        type: NotificationType,
        title: str,
        message: str,
        data: dict | None = None,
    ) -> Notification:
        """Send a notification."""
        notification = Notification(
            id=str(uuid.uuid4()),
            type=type,
            title=title,
            message=message,
            data=data or {},
        )

        self._history.append(notification)

        # Send to all channels
        for channel in self._channels:
            try:
                await channel.send(notification)
            except Exception:
                pass

        return notification


# =============================================================================
# Policy Enforcement (P3-123)
# =============================================================================


@dataclass
class Policy:
    """A policy rule."""

    id: str
    name: str
    description: str
    condition: str  # Python expression
    action: str  # "allow", "deny", "audit"
    severity: int = 1


class PolicyEngine:
    """
    Policy enforcement engine.

    P3-123: Support policy enforcement
    """

    def __init__(self):
        self._policies: dict[str, Policy] = {}

    def add_policy(self, policy: Policy) -> None:
        """Add a policy."""
        self._policies[policy.id] = policy

    def evaluate(self, context: dict[str, Any]) -> list[tuple[Policy, bool, str]]:
        """
        Evaluate all policies against context.

        Returns list of (policy, passed, action) tuples.
        """
        results = []

        for policy in self._policies.values():
            try:
                # Safely evaluate condition
                passed = bool(eval(policy.condition, {"__builtins__": {}}, context))
                results.append((policy, passed, policy.action if not passed else "allow"))
            except Exception:
                results.append((policy, False, "error"))

        return results

    def enforce(self, context: dict[str, Any]) -> tuple[bool, list[str]]:
        """
        Enforce policies.

        Returns (allowed, list of violations).
        """
        results = self.evaluate(context)
        violations = []

        for policy, passed, action in results:
            if not passed and action == "deny":
                violations.append(f"{policy.name}: {policy.description}")

        return len(violations) == 0, violations


# =============================================================================
# Approval Workflow (P3-122)
# =============================================================================


class ApprovalStatus(Enum):
    """Approval statuses."""

    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"
    EXPIRED = "expired"


@dataclass
class ApprovalRequest:
    """An approval request."""

    id: str
    title: str
    description: str
    requester: str
    approvers: list[str]
    status: ApprovalStatus = ApprovalStatus.PENDING
    created_at: float = field(default_factory=time.time)
    expires_at: float | None = None
    approved_by: str | None = None
    rejected_by: str | None = None
    comments: list[str] = field(default_factory=list)


class ApprovalWorkflow:
    """
    Approval workflow manager.

    P3-122: Implement approval workflows
    """

    def __init__(self, audit_logger: AuditLogger | None = None):
        self._requests: dict[str, ApprovalRequest] = {}
        self.audit_logger = audit_logger

    def create_request(
        self,
        title: str,
        description: str,
        requester: str,
        approvers: list[str],
        expires_in: float | None = None,
    ) -> ApprovalRequest:
        """Create an approval request."""
        request = ApprovalRequest(
            id=str(uuid.uuid4()),
            title=title,
            description=description,
            requester=requester,
            approvers=approvers,
            expires_at=time.time() + expires_in if expires_in else None,
        )

        self._requests[request.id] = request

        if self.audit_logger:
            self.audit_logger.log(
                AuditAction.CREATE,
                requester,
                "approval_request",
                request.id,
                {"title": title, "approvers": approvers},
            )

        return request

    def approve(self, request_id: str, approver: str, comment: str | None = None) -> bool:
        """Approve a request."""
        request = self._requests.get(request_id)
        if not request or request.status != ApprovalStatus.PENDING:
            return False

        if approver not in request.approvers:
            return False

        request.status = ApprovalStatus.APPROVED
        request.approved_by = approver
        if comment:
            request.comments.append(f"[{approver}] {comment}")

        if self.audit_logger:
            self.audit_logger.log(
                AuditAction.APPROVE,
                approver,
                "approval_request",
                request_id,
            )

        return True

    def reject(self, request_id: str, rejector: str, reason: str) -> bool:
        """Reject a request."""
        request = self._requests.get(request_id)
        if not request or request.status != ApprovalStatus.PENDING:
            return False

        if rejector not in request.approvers:
            return False

        request.status = ApprovalStatus.REJECTED
        request.rejected_by = rejector
        request.comments.append(f"[{rejector}] Rejected: {reason}")

        if self.audit_logger:
            self.audit_logger.log(
                AuditAction.REJECT,
                rejector,
                "approval_request",
                request_id,
                {"reason": reason},
            )

        return True

    def get_pending_for_approver(self, approver: str) -> list[ApprovalRequest]:
        """Get pending requests for an approver."""
        return [
            r
            for r in self._requests.values()
            if r.status == ApprovalStatus.PENDING and approver in r.approvers
        ]


# =============================================================================
# DAG Workflow Engine (P3-108)
# =============================================================================


@dataclass
class DAGNode:
    """A node in a DAG workflow."""

    id: str
    name: str
    handler: Callable | None = None
    dependencies: list[str] = field(default_factory=list)
    config: dict[str, Any] = field(default_factory=dict)


class DAGWorkflowEngine:
    """
    DAG-based workflow engine.

    P3-108: Implement DAG-based workflow engine
    """

    def __init__(self):
        self._nodes: dict[str, DAGNode] = {}
        self._results: dict[str, Any] = {}

    def add_node(self, node: DAGNode) -> None:
        """Add a node to the DAG."""
        self._nodes[node.id] = node

    def validate(self) -> tuple[bool, list[str]]:
        """Validate the DAG (check for cycles)."""
        # Topological sort to detect cycles
        visited = set()
        path = set()
        errors = []

        def visit(node_id: str) -> bool:
            if node_id in path:
                errors.append(f"Cycle detected involving {node_id}")
                return False
            if node_id in visited:
                return True

            path.add(node_id)
            node = self._nodes.get(node_id)
            if node:
                for dep in node.dependencies:
                    if dep not in self._nodes:
                        errors.append(f"Missing dependency: {dep}")
                        return False
                    if not visit(dep):
                        return False

            path.remove(node_id)
            visited.add(node_id)
            return True

        for node_id in self._nodes:
            if not visit(node_id):
                break

        return len(errors) == 0, errors

    def get_execution_order(self) -> list[str]:
        """Get topologically sorted execution order."""
        visited = set()
        order = []

        def visit(node_id: str):
            if node_id in visited:
                return
            visited.add(node_id)

            node = self._nodes.get(node_id)
            if node:
                for dep in node.dependencies:
                    visit(dep)

            order.append(node_id)

        for node_id in self._nodes:
            visit(node_id)

        return order

    async def execute(self) -> dict[str, Any]:
        """Execute the DAG workflow."""
        valid, errors = self.validate()
        if not valid:
            raise ValueError(f"Invalid DAG: {errors}")

        order = self.get_execution_order()

        for node_id in order:
            node = self._nodes[node_id]

            # Get dependency results
            dep_results = {dep: self._results[dep] for dep in node.dependencies}

            # Execute node
            if node.handler:
                try:
                    if asyncio.iscoroutinefunction(node.handler):
                        result = await node.handler(dep_results, node.config)
                    else:
                        result = node.handler(dep_results, node.config)
                    self._results[node_id] = result
                except Exception as e:
                    self._results[node_id] = {"error": str(e)}
            else:
                self._results[node_id] = None

        return self._results
