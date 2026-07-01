"""
cvc.security.sentinel — guard against surprise network egress.

The CVC soul should ONLY talk to the brain(s) the owner explicitly
configured. If anything else tries to reach the network — telemetry,
auto-update pings, hidden analytics — this module blocks it and
records the attempt in the audit log.

How it works:
  - The gateway installs an outbound hook (via httpx event hooks or by
    wrapping the underlying transport) that asks the sentinel before
    allowing any non-loopback request.
  - The sentinel compares the destination against the brain allowlist.
  - If allowed: log NETWORK_BRAIN_CALL in the audit log and pass.
  - If blocked: log NETWORK_BLOCKED and raise OutboundBlocked.

This is the "Apple privacy nutrition label" idea applied at runtime —
the owner can prove, not just claim, that nothing left the machine.
"""

from __future__ import annotations

import logging
import threading
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

logger = logging.getLogger("cvc.security.sentinel")


class OutboundBlocked(RuntimeError):
    """Raised when an outbound call is rejected by the sentinel."""

    def __init__(self, url: str, reason: str) -> None:
        super().__init__(f"blocked outbound to {url}: {reason}")
        self.url = url
        self.reason = reason


@dataclass
class SentinelConfig:
    """Configuration for the network sentinel."""

    allowed_brains: list[str] = field(default_factory=list)
    # hosts the owner has explicitly approved (besides brain providers)
    allowed_hosts: list[str] = field(default_factory=list)
    # hosts always blocked (defence-in-depth — useful for telemetry domains)
    blocked_hosts: list[str] = field(
        default_factory=lambda: [
            "telemetry.openai.com",
            "api.mixpanel.com",
            "api.segment.io",
            "www.google-analytics.com",
            "stats.amplitude.com",
            "cdn.segment.com",
        ]
    )
    # when True, calls to loopback (127.0.0.1, localhost) always allowed
    allow_loopback: bool = True
    # when True, even unknown hosts pass (permissive mode for dev)
    permissive: bool = False


class NetworkSentinel:
    """Single-process gatekeeper for outbound network calls."""

    def __init__(
        self,
        config: SentinelConfig | None = None,
        audit_log: Any | None = None,
    ) -> None:
        self.config = config or SentinelConfig()
        self.audit_log = audit_log
        self._lock = threading.Lock()
        self._allowed_count = 0
        self._blocked_count = 0

    # ── public surface ────────────────────────────────────────────────

    def configure(self, **kwargs: Any) -> None:
        for k, v in kwargs.items():
            if hasattr(self.config, k):
                setattr(self.config, k, v)

    def stats(self) -> dict[str, Any]:
        return {
            "allowed": self._allowed_count,
            "blocked": self._blocked_count,
            "allowed_brains": list(self.config.allowed_brains),
            "allowed_hosts": list(self.config.allowed_hosts),
            "blocked_hosts": list(self.config.blocked_hosts),
            "permissive": self.config.permissive,
        }

    def check(self, url: str, *, allow_loopback_override: bool | None = None) -> bool:
        """
        Returns True if the URL may be called, False if blocked.
        Does NOT raise — use assert_safe() when you want blocking behavior.
        """
        allow_lb = (
            self.config.allow_loopback
            if allow_loopback_override is None
            else allow_loopback_override
        )
        host = urlparse(url).hostname or ""

        # Blocklist wins first
        for bad in self.config.blocked_hosts:
            if host == bad or host.endswith("." + bad):
                return False

        if allow_lb and host in ("localhost", "127.0.0.1", "::1", "0.0.0.0"):
            return True

        if self.config.permissive:
            return True

        if host in self.config.allowed_hosts:
            return True
        for brain in self.config.allowed_brains:
            if host == brain or host.endswith("." + brain):
                return True
        return False

    def assert_safe(self, url: str) -> None:
        """Raise OutboundBlocked if URL is not on the allowlist."""
        allowed = self.check(url)
        with self._lock:
            if allowed:
                self._allowed_count += 1
            else:
                self._blocked_count += 1
        if not allowed:
            reason = "host not in brain allowlist"
            if self.audit_log is not None:
                try:
                    self.audit_log.append(
                        "network.blocked",
                        actor="sentinel",
                        target=url,
                        detail={"reason": reason},
                    )
                except Exception as exc:  # noqa: BLE001
                    logger.debug("audit append failed: %s", exc)
            raise OutboundBlocked(url, reason)
        if self.audit_log is not None:
            try:
                self.audit_log.append(
                    "network.brain.call",
                    actor="sentinel",
                    target=url,
                    detail={},
                )
            except Exception as exc:  # noqa: BLE001
                logger.debug("audit append failed: %s", exc)

    # ── factory ───────────────────────────────────────────────────────

    @classmethod
    def from_vault(cls, vault_dir: Path) -> "NetworkSentinel":
        """Load a sentinel config from a vault dir, if present."""
        config_path = vault_dir / "sentinel.json"
        if config_path.exists():
            import json

            data = json.loads(config_path.read_text(encoding="utf-8"))
            cfg = SentinelConfig(**data)
        else:
            cfg = SentinelConfig()
        audit = None
        try:
            from cvc.security.audit import AuditLog

            audit = AuditLog(vault_dir / "audit.log")
        except Exception:
            audit = None
        return cls(config=cfg, audit_log=audit)


# Module-level singleton — one sentinel per process.
_SENTINEL: NetworkSentinel | None = None


def get_sentinel() -> NetworkSentinel:
    global _SENTINEL
    if _SENTINEL is None:
        _SENTINEL = NetworkSentinel()
    return _SENTINEL