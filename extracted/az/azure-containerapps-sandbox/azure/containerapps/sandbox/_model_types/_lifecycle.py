"""Lifecycle policy models — shared between requests and responses."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal


@dataclass
class AutoSuspendPolicy:
    """Auto-suspend configuration for sandbox lifecycle."""

    enabled: bool = False
    interval: int | None = None
    mode: Literal["Memory", "Disk"] | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> AutoSuspendPolicy | None:
        if not d:
            return None
        return cls(
            enabled=d.get("enabled", False),
            interval=d.get("interval", d.get("idleTimeoutInSeconds", d.get("idleTimeoutSeconds"))),
            mode=d.get("mode"),
        )

    def _to_dict(self) -> dict:
        d: dict = {"enabled": self.enabled}
        if self.interval is not None:
            d["interval"] = self.interval
        if self.mode is not None:
            d["mode"] = self.mode
        return d


@dataclass
class AutoDeletePolicy:
    """Auto-delete configuration for sandbox lifecycle."""

    enabled: bool = False
    delete_interval_seconds: int | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> AutoDeletePolicy | None:
        if not d:
            return None
        return cls(
            enabled=d.get("enabled", False),
            delete_interval_seconds=d.get("deleteIntervalInSeconds", d.get("idleTimeoutInSeconds")),
        )

    def _to_dict(self) -> dict:
        d: dict = {"enabled": self.enabled}
        if self.delete_interval_seconds is not None:
            d["deleteIntervalInSeconds"] = self.delete_interval_seconds
        return d


@dataclass
class LifecyclePolicy:
    """Lifecycle policy for a sandbox — used for both input and output."""

    auto_suspend: AutoSuspendPolicy | None = None
    auto_delete: AutoDeletePolicy | None = None

    @classmethod
    def _from_dict(cls, d: dict | None) -> LifecyclePolicy | None:
        if not d:
            return None
        return cls(
            auto_suspend=AutoSuspendPolicy._from_dict(d.get("autoSuspend") or d.get("autoSuspendPolicy")),
            auto_delete=AutoDeletePolicy._from_dict(d.get("autoDelete") or d.get("autoDeletePolicy")),
        )

    def _to_dict(self) -> dict:
        d: dict = {}
        if self.auto_suspend is not None:
            d["autoSuspendPolicy"] = self.auto_suspend._to_dict()
        if self.auto_delete is not None:
            d["autoDeletePolicy"] = self.auto_delete._to_dict()
        return d
