"""
threatwire.handlers
====================
Ready-made alert handlers for ThreatEventBus.

Usage::

    from threatwire import ThreatEventBus
    from threatwire.handlers import SlackHandler, FileHandler, SIEMHandler

    bus = ThreatEventBus()
    bus.add_handler(SlackHandler(webhook_url="https://hooks.slack.com/...").handle)
    bus.add_handler(FileHandler("/var/log/threatwire/alerts.jsonl").handle)
"""

from __future__ import annotations

import json
import logging
import time
from pathlib import Path

from threatwire.core.models import AlertSeverity, ThreatAlert

logger = logging.getLogger(__name__)


# ---------------------------------------------------------------------------
# File handler (JSONL)
# ---------------------------------------------------------------------------

class FileHandler:
    """
    Appends one JSON line per alert to a log file.
    Rotates when the file exceeds max_bytes.
    """

    def __init__(
        self,
        path: str | Path,
        max_bytes: int = 100 * 1024 * 1024,   # 100 MB default
        min_severity: AlertSeverity = AlertSeverity.INFO,
    ) -> None:
        self.path = Path(path)
        self.max_bytes = max_bytes
        self.min_severity = min_severity
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._fh = self.path.open("a", encoding="utf-8")

    def handle(self, alert: ThreatAlert) -> None:
        if alert.severity < self.min_severity:
            return
        if self.max_bytes and self.path.stat().st_size >= self.max_bytes:
            self._rotate()
        self._fh.write(json.dumps(alert.to_dict()) + "\n")
        self._fh.flush()

    def _rotate(self) -> None:
        self._fh.close()
        rotated = self.path.with_suffix(f".{int(time.time())}.jsonl")
        self.path.rename(rotated)
        self._fh = self.path.open("a", encoding="utf-8")
        logger.info("FileHandler rotated log to %s", rotated)

    def close(self) -> None:
        self._fh.close()


# ---------------------------------------------------------------------------
# Slack handler
# ---------------------------------------------------------------------------

class SlackHandler:
    """
    Posts threat alerts to a Slack webhook.

    Usage::

        handler = SlackHandler(
            webhook_url="https://hooks.slack.com/services/...",
            min_severity="high",
            channel="#security-alerts",
        )
        bus.add_handler(handler.handle, severity="high")
    """

    SEVERITY_EMOJI = {
        AlertSeverity.INFO: ":information_source:",
        AlertSeverity.LOW: ":large_blue_circle:",
        AlertSeverity.MEDIUM: ":large_yellow_circle:",
        AlertSeverity.HIGH: ":orange_circle:",
        AlertSeverity.CRITICAL: ":red_circle:",
    }

    def __init__(
        self,
        webhook_url: str,
        min_severity: AlertSeverity = AlertSeverity.HIGH,
        channel: str | None = None,
        username: str = "threatwire",
    ) -> None:
        self.webhook_url = webhook_url
        self.min_severity = min_severity
        self.channel = channel
        self.username = username

    def handle(self, alert: ThreatAlert) -> None:
        if alert.severity < self.min_severity:
            return
        try:
            import urllib.request

            emoji = self.SEVERITY_EMOJI.get(alert.severity, ":warning:")
            payload = {
                "username": self.username,
                "text": (
                    f"{emoji} *{alert.severity.value.upper()} — {alert.rule_name}*\n"
                    f"> `{alert.src_ip}` → `{alert.dst_ip}`\n"
                    f"> Technique: {alert.technique_id or 'N/A'} | "
                    f"Confidence: {alert.confidence:.0%}\n"
                    f"> {alert.description}"
                ),
            }
            if self.channel:
                payload["channel"] = self.channel

            data = json.dumps(payload).encode("utf-8")
            req = urllib.request.Request(
                self.webhook_url,
                data=data,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=5) as resp:
                if resp.status != 200:
                    logger.warning("Slack webhook returned %d", resp.status)
        except Exception as exc:
            logger.error("SlackHandler failed: %s", exc)


# ---------------------------------------------------------------------------
# SIEM / Elastic handler
# ---------------------------------------------------------------------------

class SIEMHandler:
    """
    Ships alerts to a SIEM via HTTP (Elasticsearch _bulk API or generic HTTP endpoint).

    Usage::

        handler = SIEMHandler(
            endpoint="https://elasticsearch:9200/threatwire/_doc",
            api_key="base64encoded==",
        )
        bus.add_handler(handler.handle)
    """

    def __init__(
        self,
        endpoint: str,
        api_key: str | None = None,
        username: str | None = None,
        password: str | None = None,
        batch_size: int = 50,
        flush_interval: float = 5.0,
        min_severity: AlertSeverity = AlertSeverity.LOW,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.api_key = api_key
        self.username = username
        self.password = password
        self.batch_size = batch_size
        self.flush_interval = flush_interval
        self.min_severity = min_severity

        self._buffer: list[ThreatAlert] = []
        self._last_flush = time.time()

    def handle(self, alert: ThreatAlert) -> None:
        if alert.severity < self.min_severity:
            return
        self._buffer.append(alert)
        elapsed = time.time() - self._last_flush
        if len(self._buffer) >= self.batch_size or elapsed >= self.flush_interval:
            self.flush()

    def flush(self) -> None:
        if not self._buffer:
            return
        batch = self._buffer.copy()
        self._buffer.clear()
        self._last_flush = time.time()
        try:
            self._send_batch(batch)
        except Exception as exc:
            logger.error("SIEMHandler flush failed: %s — %d alerts lost", exc, len(batch))

    def _send_batch(self, alerts: list[ThreatAlert]) -> None:
        import base64
        import urllib.request

        # Elasticsearch _bulk format
        body_lines = []
        for alert in alerts:
            body_lines.append(json.dumps({"index": {}}))
            body_lines.append(json.dumps(alert.to_ecs()))
        body = "\n".join(body_lines) + "\n"

        headers = {"Content-Type": "application/x-ndjson"}
        if self.api_key:
            headers["Authorization"] = f"ApiKey {self.api_key}"
        elif self.username and self.password:
            creds = base64.b64encode(f"{self.username}:{self.password}".encode()).decode()
            headers["Authorization"] = f"Basic {creds}"

        req = urllib.request.Request(
            f"{self.endpoint}/_bulk",
            data=body.encode("utf-8"),
            headers=headers,
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=10) as resp:
            if resp.status not in (200, 201):
                logger.warning("SIEM endpoint returned %d", resp.status)


# ---------------------------------------------------------------------------
# Logging handler (Python stdlib)
# ---------------------------------------------------------------------------

class LoggingHandler:
    """Emits alerts via Python's standard logging at the appropriate level."""

    LEVEL_MAP = {
        AlertSeverity.INFO: logging.INFO,
        AlertSeverity.LOW: logging.INFO,
        AlertSeverity.MEDIUM: logging.WARNING,
        AlertSeverity.HIGH: logging.ERROR,
        AlertSeverity.CRITICAL: logging.CRITICAL,
    }

    def __init__(self, logger_name: str = "threatwire.alerts") -> None:
        self._log = logging.getLogger(logger_name)

    def handle(self, alert: ThreatAlert) -> None:
        level = self.LEVEL_MAP.get(alert.severity, logging.WARNING)
        self._log.log(
            level,
            "[%s] %s | %s -> %s | technique=%s confidence=%.0f%%",
            alert.severity.value.upper(),
            alert.rule_name,
            alert.src_ip,
            alert.dst_ip,
            alert.technique_id or "N/A",
            alert.confidence * 100,
        )
