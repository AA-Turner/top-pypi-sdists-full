"""
Alerting system for threshold-based notifications and monitoring.

Provides configurable alerts based on metrics, error rates, latency,
cost, and custom conditions with multiple notification channels.
"""

from __future__ import annotations

import asyncio
import json
from abc import ABC, abstractmethod
from collections.abc import Callable
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from enum import Enum
from typing import Any
from uuid import uuid4


class AlertSeverity(Enum):
    """Severity levels for alerts."""

    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class AlertStatus(Enum):
    """Status of an alert."""

    OK = "ok"
    TRIGGERED = "triggered"
    ACKNOWLEDGED = "acknowledged"
    RESOLVED = "resolved"
    MUTED = "muted"


class MetricType(Enum):
    """Types of metrics that can trigger alerts."""

    LATENCY_P50 = "latency_p50"
    LATENCY_P90 = "latency_p90"
    LATENCY_P99 = "latency_p99"
    LATENCY_AVG = "latency_avg"
    LATENCY_MAX = "latency_max"
    ERROR_RATE = "error_rate"
    SUCCESS_RATE = "success_rate"
    TOKENS_PER_REQUEST = "tokens_per_request"
    COST_PER_REQUEST = "cost_per_request"
    COST_TOTAL = "cost_total"
    REQUEST_COUNT = "request_count"
    THROUGHPUT = "throughput"
    HALLUCINATION_RATE = "hallucination_rate"
    TOXICITY_RATE = "toxicity_rate"
    QUALITY_SCORE = "quality_score"
    CUSTOM = "custom"


class ComparisonOperator(Enum):
    """Comparison operators for alert conditions."""

    GREATER_THAN = "gt"
    GREATER_THAN_OR_EQUAL = "gte"
    LESS_THAN = "lt"
    LESS_THAN_OR_EQUAL = "lte"
    EQUAL = "eq"
    NOT_EQUAL = "neq"
    CHANGE_PERCENT = "change_pct"
    ANOMALY = "anomaly"


class AggregationWindow(Enum):
    """Time windows for metric aggregation."""

    MINUTE_1 = "1m"
    MINUTE_5 = "5m"
    MINUTE_15 = "15m"
    HOUR_1 = "1h"
    HOUR_4 = "4h"
    DAY_1 = "1d"


@dataclass
class AlertCondition:
    """Condition that triggers an alert."""

    metric: MetricType
    operator: ComparisonOperator
    threshold: float
    window: AggregationWindow = AggregationWindow.MINUTE_5

    # For percentage change comparisons
    baseline_window: AggregationWindow | None = None

    # For anomaly detection
    anomaly_std_dev: float = 3.0

    # Custom metric function
    custom_fn: Callable[[dict[str, Any]], float] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "metric": self.metric.value,
            "operator": self.operator.value,
            "threshold": self.threshold,
            "window": self.window.value,
            "baseline_window": self.baseline_window.value if self.baseline_window else None,
            "anomaly_std_dev": self.anomaly_std_dev,
        }


@dataclass
class AlertRule:
    """A rule that defines when and how to alert."""

    id: str
    name: str
    description: str | None
    conditions: list[AlertCondition]
    severity: AlertSeverity

    # Targeting
    tags: list[str] = field(default_factory=list)
    trace_filters: dict[str, Any] = field(default_factory=dict)

    # Behavior
    enabled: bool = True
    muted_until: datetime | None = None
    cooldown_minutes: int = 5  # Minimum time between alerts

    # Notification
    notification_channels: list[str] = field(default_factory=list)
    notification_message: str | None = None

    # Metadata
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    created_by: str | None = None

    # State
    last_triggered: datetime | None = None
    trigger_count: int = 0

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "conditions": [c.to_dict() for c in self.conditions],
            "severity": self.severity.value,
            "tags": self.tags,
            "trace_filters": self.trace_filters,
            "enabled": self.enabled,
            "muted_until": self.muted_until.isoformat() if self.muted_until else None,
            "cooldown_minutes": self.cooldown_minutes,
            "notification_channels": self.notification_channels,
            "notification_message": self.notification_message,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
            "created_by": self.created_by,
            "last_triggered": self.last_triggered.isoformat() if self.last_triggered else None,
            "trigger_count": self.trigger_count,
        }


@dataclass
class AlertEvent:
    """An individual alert event/incident."""

    id: str
    rule_id: str
    rule_name: str
    severity: AlertSeverity
    status: AlertStatus

    # Trigger details
    triggered_at: datetime
    condition_values: dict[str, float]
    threshold_values: dict[str, float]

    # Context
    trace_ids: list[str] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)

    # Resolution
    acknowledged_at: datetime | None = None
    acknowledged_by: str | None = None
    resolved_at: datetime | None = None
    resolved_by: str | None = None
    resolution_notes: str | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "rule_id": self.rule_id,
            "rule_name": self.rule_name,
            "severity": self.severity.value,
            "status": self.status.value,
            "triggered_at": self.triggered_at.isoformat(),
            "condition_values": self.condition_values,
            "threshold_values": self.threshold_values,
            "trace_ids": self.trace_ids,
            "metadata": self.metadata,
            "acknowledged_at": self.acknowledged_at.isoformat() if self.acknowledged_at else None,
            "acknowledged_by": self.acknowledged_by,
            "resolved_at": self.resolved_at.isoformat() if self.resolved_at else None,
            "resolved_by": self.resolved_by,
            "resolution_notes": self.resolution_notes,
        }


# ============================================================================
# Notification Channels
# ============================================================================


class NotificationChannel(ABC):
    """Base class for notification channels."""

    @abstractmethod
    async def send(self, event: AlertEvent, message: str) -> bool:
        """Send a notification for an alert event."""
        pass

    @property
    @abstractmethod
    def channel_type(self) -> str:
        """Get the channel type identifier."""
        pass


class SlackChannel(NotificationChannel):
    """Slack notification channel."""

    def __init__(
        self,
        webhook_url: str,
        channel: str | None = None,
        username: str = "Aigie Alerts",
    ):
        self.webhook_url = webhook_url
        self.channel = channel
        self.username = username

    @property
    def channel_type(self) -> str:
        return "slack"

    async def send(self, event: AlertEvent, message: str) -> bool:
        """Send Slack notification."""
        # Build Slack message payload
        color_map = {
            AlertSeverity.INFO: "#36a64f",
            AlertSeverity.WARNING: "#ff9500",
            AlertSeverity.ERROR: "#ff4444",
            AlertSeverity.CRITICAL: "#8b0000",
        }

        payload = {
            "username": self.username,
            "attachments": [
                {
                    "color": color_map.get(event.severity, "#808080"),
                    "title": f"🚨 {event.rule_name}",
                    "text": message,
                    "fields": [
                        {"title": "Severity", "value": event.severity.value, "short": True},
                        {"title": "Status", "value": event.status.value, "short": True},
                    ],
                    "ts": int(event.triggered_at.timestamp()),
                }
            ],
        }

        if self.channel:
            payload["channel"] = self.channel

        # In production, would use aiohttp to POST to webhook_url
        # For now, just log
        print(f"[Slack] Would send to {self.webhook_url}: {json.dumps(payload)}")
        return True


class EmailChannel(NotificationChannel):
    """Email notification channel."""

    def __init__(
        self,
        smtp_host: str,
        smtp_port: int,
        from_email: str,
        to_emails: list[str],
        username: str | None = None,
        password: str | None = None,
        use_tls: bool = True,
    ):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.from_email = from_email
        self.to_emails = to_emails
        self.username = username
        self.password = password
        self.use_tls = use_tls

    @property
    def channel_type(self) -> str:
        return "email"

    async def send(self, event: AlertEvent, message: str) -> bool:
        """Send email notification."""
        subject = f"[{event.severity.value.upper()}] {event.rule_name}"

        # In production, would use aiosmtplib to send email
        print(f"[Email] Would send to {self.to_emails}: {subject}")
        return True


class WebhookChannel(NotificationChannel):
    """Generic webhook notification channel."""

    def __init__(
        self,
        url: str,
        headers: dict[str, str] | None = None,
        method: str = "POST",
    ):
        self.url = url
        self.headers = headers or {"Content-Type": "application/json"}
        self.method = method

    @property
    def channel_type(self) -> str:
        return "webhook"

    async def send(self, event: AlertEvent, message: str) -> bool:
        """Send webhook notification."""
        payload = {
            "event": event.to_dict(),
            "message": message,
            "timestamp": datetime.utcnow().isoformat(),
        }

        # In production, would use aiohttp to send request
        print(f"[Webhook] Would {self.method} to {self.url}: {json.dumps(payload)}")
        return True


class PagerDutyChannel(NotificationChannel):
    """PagerDuty notification channel."""

    def __init__(self, routing_key: str, service_name: str = "Aigie"):
        self.routing_key = routing_key
        self.service_name = service_name

    @property
    def channel_type(self) -> str:
        return "pagerduty"

    async def send(self, event: AlertEvent, message: str) -> bool:
        """Send PagerDuty notification."""
        severity_map = {
            AlertSeverity.INFO: "info",
            AlertSeverity.WARNING: "warning",
            AlertSeverity.ERROR: "error",
            AlertSeverity.CRITICAL: "critical",
        }

        payload = {
            "routing_key": self.routing_key,
            "event_action": "trigger",
            "dedup_key": event.id,
            "payload": {
                "summary": f"{event.rule_name}: {message}",
                "severity": severity_map.get(event.severity, "info"),
                "source": self.service_name,
                "timestamp": event.triggered_at.isoformat(),
            },
        }

        print(f"[PagerDuty] Would trigger: {json.dumps(payload)}")
        return True


# ============================================================================
# Alert Manager
# ============================================================================


class AlertManager:
    """
    Manages alert rules, evaluates conditions, and sends notifications.

    Usage:
        manager = AlertManager(client)

        # Create an alert rule
        rule = manager.create_rule(
            name="High Latency Alert",
            conditions=[
                AlertCondition(
                    metric=MetricType.LATENCY_P99,
                    operator=ComparisonOperator.GREATER_THAN,
                    threshold=5000,  # 5 seconds
                    window=AggregationWindow.MINUTE_5,
                )
            ],
            severity=AlertSeverity.WARNING,
        )

        # Add notification channels
        manager.add_channel("slack", SlackChannel(webhook_url="https://..."))

        # Update rule to use channel
        manager.update_rule(rule.id, notification_channels=["slack"])

        # Start monitoring
        await manager.start()
    """

    def __init__(self, client: Any | None = None):
        self._client = client
        self._rules: dict[str, AlertRule] = {}
        self._channels: dict[str, NotificationChannel] = {}
        self._events: list[AlertEvent] = []
        self._running = False
        self._check_interval = 60  # seconds

        # Metric collection (would be populated by actual data)
        self._metrics_buffer: list[dict[str, Any]] = []

    # =========================================================================
    # Rule Management
    # =========================================================================

    def create_rule(
        self,
        name: str,
        conditions: list[AlertCondition],
        severity: AlertSeverity = AlertSeverity.WARNING,
        description: str | None = None,
        tags: list[str] | None = None,
        trace_filters: dict[str, Any] | None = None,
        notification_channels: list[str] | None = None,
        notification_message: str | None = None,
        cooldown_minutes: int = 5,
        enabled: bool = True,
    ) -> AlertRule:
        """Create a new alert rule."""
        rule = AlertRule(
            id=str(uuid4()),
            name=name,
            description=description,
            conditions=conditions,
            severity=severity,
            tags=tags or [],
            trace_filters=trace_filters or {},
            notification_channels=notification_channels or [],
            notification_message=notification_message,
            cooldown_minutes=cooldown_minutes,
            enabled=enabled,
        )
        self._rules[rule.id] = rule
        return rule

    def get_rule(self, rule_id: str) -> AlertRule | None:
        """Get a rule by ID."""
        return self._rules.get(rule_id)

    def list_rules(
        self,
        enabled_only: bool = False,
        severity: AlertSeverity | None = None,
        tags: list[str] | None = None,
    ) -> list[AlertRule]:
        """List alert rules with optional filtering."""
        rules = list(self._rules.values())

        if enabled_only:
            rules = [r for r in rules if r.enabled]

        if severity:
            rules = [r for r in rules if r.severity == severity]

        if tags:
            rules = [r for r in rules if any(t in r.tags for t in tags)]

        return rules

    def update_rule(
        self,
        rule_id: str,
        name: str | None = None,
        description: str | None = None,
        conditions: list[AlertCondition] | None = None,
        severity: AlertSeverity | None = None,
        enabled: bool | None = None,
        notification_channels: list[str] | None = None,
        notification_message: str | None = None,
        cooldown_minutes: int | None = None,
    ) -> AlertRule | None:
        """Update an existing rule."""
        rule = self._rules.get(rule_id)
        if not rule:
            return None

        if name is not None:
            rule.name = name
        if description is not None:
            rule.description = description
        if conditions is not None:
            rule.conditions = conditions
        if severity is not None:
            rule.severity = severity
        if enabled is not None:
            rule.enabled = enabled
        if notification_channels is not None:
            rule.notification_channels = notification_channels
        if notification_message is not None:
            rule.notification_message = notification_message
        if cooldown_minutes is not None:
            rule.cooldown_minutes = cooldown_minutes

        rule.updated_at = datetime.utcnow()
        return rule

    def delete_rule(self, rule_id: str) -> bool:
        """Delete a rule."""
        if rule_id in self._rules:
            del self._rules[rule_id]
            return True
        return False

    def mute_rule(self, rule_id: str, duration_minutes: int) -> bool:
        """Mute a rule for a duration."""
        rule = self._rules.get(rule_id)
        if rule:
            rule.muted_until = datetime.utcnow() + timedelta(minutes=duration_minutes)
            return True
        return False

    def unmute_rule(self, rule_id: str) -> bool:
        """Unmute a rule."""
        rule = self._rules.get(rule_id)
        if rule:
            rule.muted_until = None
            return True
        return False

    # =========================================================================
    # Channel Management
    # =========================================================================

    def add_channel(self, name: str, channel: NotificationChannel) -> None:
        """Add a notification channel."""
        self._channels[name] = channel

    def remove_channel(self, name: str) -> bool:
        """Remove a notification channel."""
        if name in self._channels:
            del self._channels[name]
            return True
        return False

    def list_channels(self) -> dict[str, str]:
        """List all channels with their types."""
        return {name: ch.channel_type for name, ch in self._channels.items()}

    # =========================================================================
    # Event Management
    # =========================================================================

    def get_events(
        self,
        rule_id: str | None = None,
        status: AlertStatus | None = None,
        severity: AlertSeverity | None = None,
        since: datetime | None = None,
        limit: int = 100,
    ) -> list[AlertEvent]:
        """Get alert events with optional filtering."""
        events = self._events

        if rule_id:
            events = [e for e in events if e.rule_id == rule_id]

        if status:
            events = [e for e in events if e.status == status]

        if severity:
            events = [e for e in events if e.severity == severity]

        if since:
            events = [e for e in events if e.triggered_at >= since]

        return events[-limit:]

    def acknowledge_event(
        self,
        event_id: str,
        acknowledged_by: str,
    ) -> bool:
        """Acknowledge an alert event."""
        for event in self._events:
            if event.id == event_id:
                event.status = AlertStatus.ACKNOWLEDGED
                event.acknowledged_at = datetime.utcnow()
                event.acknowledged_by = acknowledged_by
                return True
        return False

    def resolve_event(
        self,
        event_id: str,
        resolved_by: str,
        notes: str | None = None,
    ) -> bool:
        """Resolve an alert event."""
        for event in self._events:
            if event.id == event_id:
                event.status = AlertStatus.RESOLVED
                event.resolved_at = datetime.utcnow()
                event.resolved_by = resolved_by
                event.resolution_notes = notes
                return True
        return False

    # =========================================================================
    # Metric Collection
    # =========================================================================

    def record_metric(
        self,
        trace_id: str,
        latency_ms: float,
        tokens: int,
        cost_usd: float,
        success: bool,
        tags: list[str] | None = None,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """Record a metric data point."""
        self._metrics_buffer.append(
            {
                "trace_id": trace_id,
                "timestamp": datetime.utcnow(),
                "latency_ms": latency_ms,
                "tokens": tokens,
                "cost_usd": cost_usd,
                "success": success,
                "tags": tags or [],
                "metadata": metadata or {},
            }
        )

        # Keep buffer size manageable
        if len(self._metrics_buffer) > 10000:
            self._metrics_buffer = self._metrics_buffer[-5000:]

    def _get_aggregated_metrics(
        self,
        window: AggregationWindow,
        tags: list[str] | None = None,
    ) -> dict[str, float]:
        """Get aggregated metrics for a time window."""
        window_seconds = {
            AggregationWindow.MINUTE_1: 60,
            AggregationWindow.MINUTE_5: 300,
            AggregationWindow.MINUTE_15: 900,
            AggregationWindow.HOUR_1: 3600,
            AggregationWindow.HOUR_4: 14400,
            AggregationWindow.DAY_1: 86400,
        }

        cutoff = datetime.utcnow() - timedelta(seconds=window_seconds.get(window, 300))

        # Filter metrics
        metrics = [m for m in self._metrics_buffer if m["timestamp"] >= cutoff]

        if tags:
            metrics = [m for m in metrics if any(t in m["tags"] for t in tags)]

        if not metrics:
            return {}

        # Calculate aggregates
        latencies = sorted([m["latency_ms"] for m in metrics])
        n = len(latencies)

        success_count = sum(1 for m in metrics if m["success"])
        total_tokens = sum(m["tokens"] for m in metrics)
        total_cost = sum(m["cost_usd"] for m in metrics)

        return {
            MetricType.LATENCY_AVG.value: sum(latencies) / n,
            MetricType.LATENCY_P50.value: latencies[n // 2],
            MetricType.LATENCY_P90.value: latencies[int(n * 0.9)],
            MetricType.LATENCY_P99.value: latencies[int(n * 0.99)],
            MetricType.LATENCY_MAX.value: max(latencies),
            MetricType.ERROR_RATE.value: 1 - (success_count / n),
            MetricType.SUCCESS_RATE.value: success_count / n,
            MetricType.TOKENS_PER_REQUEST.value: total_tokens / n,
            MetricType.COST_PER_REQUEST.value: total_cost / n,
            MetricType.COST_TOTAL.value: total_cost,
            MetricType.REQUEST_COUNT.value: n,
            MetricType.THROUGHPUT.value: n / window_seconds.get(window, 300),
        }

    # =========================================================================
    # Alert Evaluation
    # =========================================================================

    def _evaluate_condition(
        self,
        condition: AlertCondition,
        metrics: dict[str, float],
    ) -> tuple[bool, float, float]:
        """Evaluate a single condition. Returns (triggered, actual_value, threshold)."""
        metric_key = condition.metric.value
        actual = metrics.get(metric_key, 0.0)
        threshold = condition.threshold

        operators = {
            ComparisonOperator.GREATER_THAN: lambda a, t: a > t,
            ComparisonOperator.GREATER_THAN_OR_EQUAL: lambda a, t: a >= t,
            ComparisonOperator.LESS_THAN: lambda a, t: a < t,
            ComparisonOperator.LESS_THAN_OR_EQUAL: lambda a, t: a <= t,
            ComparisonOperator.EQUAL: lambda a, t: a == t,
            ComparisonOperator.NOT_EQUAL: lambda a, t: a != t,
        }

        op_fn = operators.get(condition.operator)
        if op_fn:
            triggered = op_fn(actual, threshold)
            return triggered, actual, threshold

        # Handle special operators
        if condition.operator == ComparisonOperator.CHANGE_PERCENT:
            if condition.baseline_window:
                baseline_metrics = self._get_aggregated_metrics(condition.baseline_window)
                baseline_value = baseline_metrics.get(metric_key, 0.0)
                if baseline_value > 0:
                    change_pct = ((actual - baseline_value) / baseline_value) * 100
                    return abs(change_pct) > threshold, change_pct, threshold

        return False, actual, threshold

    def _evaluate_rule(self, rule: AlertRule) -> AlertEvent | None:
        """Evaluate a rule and create an event if triggered."""
        # Check if rule is muted
        if rule.muted_until and datetime.utcnow() < rule.muted_until:
            return None

        # Check cooldown
        if rule.last_triggered:
            cooldown_end = rule.last_triggered + timedelta(minutes=rule.cooldown_minutes)
            if datetime.utcnow() < cooldown_end:
                return None

        # Get metrics for each condition's window
        all_triggered = True
        condition_values: dict[str, float] = {}
        threshold_values: dict[str, float] = {}

        for i, condition in enumerate(rule.conditions):
            metrics = self._get_aggregated_metrics(condition.window, rule.tags)
            triggered, actual, threshold = self._evaluate_condition(condition, metrics)

            condition_values[f"condition_{i}_{condition.metric.value}"] = actual
            threshold_values[f"condition_{i}_{condition.metric.value}"] = threshold

            if not triggered:
                all_triggered = False
                break

        if all_triggered:
            # Create alert event
            event = AlertEvent(
                id=str(uuid4()),
                rule_id=rule.id,
                rule_name=rule.name,
                severity=rule.severity,
                status=AlertStatus.TRIGGERED,
                triggered_at=datetime.utcnow(),
                condition_values=condition_values,
                threshold_values=threshold_values,
            )

            # Update rule state
            rule.last_triggered = datetime.utcnow()
            rule.trigger_count += 1

            self._events.append(event)
            return event

        return None

    async def _send_notifications(self, event: AlertEvent, rule: AlertRule) -> None:
        """Send notifications for an alert event."""
        message = rule.notification_message or (
            f"Alert triggered: {rule.name}\n"
            f"Severity: {event.severity.value}\n"
            f"Values: {event.condition_values}"
        )

        for channel_name in rule.notification_channels:
            channel = self._channels.get(channel_name)
            if channel:
                try:
                    await channel.send(event, message)
                except Exception as e:
                    print(f"Failed to send to channel {channel_name}: {e}")

    async def check_alerts(self) -> list[AlertEvent]:
        """Check all enabled rules and return triggered events."""
        triggered_events = []

        for rule in self._rules.values():
            if not rule.enabled:
                continue

            event = self._evaluate_rule(rule)
            if event:
                triggered_events.append(event)
                await self._send_notifications(event, rule)

        return triggered_events

    # =========================================================================
    # Monitoring Loop
    # =========================================================================

    async def start(self, check_interval: int = 60) -> None:
        """Start the alert monitoring loop."""
        self._running = True
        self._check_interval = check_interval

        while self._running:
            try:
                await self.check_alerts()
            except Exception as e:
                print(f"Error checking alerts: {e}")

            await asyncio.sleep(self._check_interval)

    def stop(self) -> None:
        """Stop the alert monitoring loop."""
        self._running = False

    # =========================================================================
    # Convenience Methods
    # =========================================================================

    def create_latency_alert(
        self,
        name: str,
        threshold_ms: float,
        percentile: str = "p99",
        severity: AlertSeverity = AlertSeverity.WARNING,
    ) -> AlertRule:
        """Create a latency alert rule."""
        metric_map = {
            "p50": MetricType.LATENCY_P50,
            "p90": MetricType.LATENCY_P90,
            "p99": MetricType.LATENCY_P99,
            "avg": MetricType.LATENCY_AVG,
            "max": MetricType.LATENCY_MAX,
        }

        return self.create_rule(
            name=name,
            conditions=[
                AlertCondition(
                    metric=metric_map.get(percentile, MetricType.LATENCY_P99),
                    operator=ComparisonOperator.GREATER_THAN,
                    threshold=threshold_ms,
                )
            ],
            severity=severity,
            description=f"Alert when {percentile} latency exceeds {threshold_ms}ms",
        )

    def create_error_rate_alert(
        self,
        name: str,
        threshold_percent: float,
        severity: AlertSeverity = AlertSeverity.ERROR,
    ) -> AlertRule:
        """Create an error rate alert rule."""
        return self.create_rule(
            name=name,
            conditions=[
                AlertCondition(
                    metric=MetricType.ERROR_RATE,
                    operator=ComparisonOperator.GREATER_THAN,
                    threshold=threshold_percent / 100,
                )
            ],
            severity=severity,
            description=f"Alert when error rate exceeds {threshold_percent}%",
        )

    def create_cost_alert(
        self,
        name: str,
        threshold_usd: float,
        window: AggregationWindow = AggregationWindow.HOUR_1,
        severity: AlertSeverity = AlertSeverity.WARNING,
    ) -> AlertRule:
        """Create a cost alert rule."""
        return self.create_rule(
            name=name,
            conditions=[
                AlertCondition(
                    metric=MetricType.COST_TOTAL,
                    operator=ComparisonOperator.GREATER_THAN,
                    threshold=threshold_usd,
                    window=window,
                )
            ],
            severity=severity,
            description=f"Alert when total cost exceeds ${threshold_usd} in {window.value}",
        )


# Convenience function
def create_alert_manager(client: Any | None = None) -> AlertManager:
    """Create a new alert manager."""
    return AlertManager(client)
