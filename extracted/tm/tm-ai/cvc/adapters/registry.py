"""
cvc.adapters.registry — Universal adapter registry.

Discovers every BaseAdapter subclass in cvc.adapters.* and exposes a uniform
surface so the gateway, agent loop, and dashboard can reason about brains
without knowing provider-specifics.

The registry is the single source-of-truth for "which brain can do what,
right now, from this machine."
"""

from __future__ import annotations

import importlib
import inspect
import logging
import pkgutil
import time
from pathlib import Path
from typing import Any

from cvc.adapters.base import BaseAdapter
from cvc.adapters.capabilities import (
    Capability,
    CapabilityReport,
    get_static_capabilities,
)

logger = logging.getLogger("cvc.adapters.registry")


# Display name map — keep here, not in adapter classes, so adapter files
# stay provider-specific and this file stays product-facing.
_DISPLAY_NAMES: dict[str, str] = {
    "openai": "OpenAI",
    "anthropic": "Anthropic",
    "google": "Google AI",
    "vertex": "Google Vertex",
    "copilot": "GitHub Copilot",
    "github": "GitHub Models",
    "ollama": "Ollama (local)",
    "lmstudio": "LM Studio (local)",
    "minimax": "MiniMax",
    "nvidia": "NVIDIA NIM",
    "telegram_gateway": "Telegram Gateway",
    "telegram_handler": "Telegram Handler",
    "telegram_streamer": "Telegram Streamer",
}


class AdapterRegistry:
    """Discovers and tracks every adapter CVC ships with."""

    def __init__(self) -> None:
        self._classes: dict[str, type[BaseAdapter]] = {}
        self._reports: dict[str, CapabilityReport] = {}
        self._discovered = False

    # ── discovery ──────────────────────────────────────────────────────

    def discover(self) -> list[str]:
        """Walk cvc.adapters.* and import every BaseAdapter subclass.

        Returns the list of adapter ids discovered.
        """
        if self._discovered:
            return list(self._classes.keys())

        import cvc.adapters as pkg
        for mod_info in pkgutil.iter_modules(pkg.__path__):
            module_name = mod_info.name
            # skip base + capabilities + registry itself
            if module_name in ("base", "capabilities", "registry", "__init__"):
                continue
            try:
                mod = importlib.import_module(f"cvc.adapters.{module_name}")
            except Exception as exc:  # noqa: BLE001
                logger.debug("Could not import cvc.adapters.%s: %s", module_name, exc)
                continue

            for _, obj in inspect.getmembers(mod, inspect.isclass):
                if obj is BaseAdapter:
                    continue
                if not issubclass(obj, BaseAdapter):
                    continue
                if obj.__module__ != mod.__name__:
                    continue
                # derive adapter id from module name
                adapter_id = module_name
                if adapter_id in self._classes:
                    continue
                self._classes[adapter_id] = obj
                self._reports[adapter_id] = CapabilityReport(
                    adapter_id=adapter_id,
                    display_name=_DISPLAY_NAMES.get(adapter_id, adapter_id.title()),
                    capabilities=[c.value for c in get_static_capabilities(adapter_id)],
                    healthy=False,
                    last_check=0.0,
                    supports_streaming=Capability.STREAMING.value
                        in [c.value for c in get_static_capabilities(adapter_id)],
                    supports_tools=Capability.FUNCTION_CALLING.value
                        in [c.value for c in get_static_capabilities(adapter_id)],
                    supports_vision=Capability.VISION.value
                        in [c.value for c in get_static_capabilities(adapter_id)],
                    supports_local=Capability.LOCAL.value
                        in [c.value for c in get_static_capabilities(adapter_id)],
                )

        self._discovered = True
        logger.info("Discovered %d adapters: %s",
                    len(self._classes), ", ".join(sorted(self._classes.keys())))
        return list(self._classes.keys())

    # ── public surface ────────────────────────────────────────────────

    def list_adapters(self) -> list[str]:
        return self.discover()

    def get_report(self, adapter_id: str) -> CapabilityReport | None:
        self.discover()
        return self._reports.get(adapter_id)

    def list_reports(self) -> list[CapabilityReport]:
        self.discover()
        return [self._reports[k] for k in sorted(self._reports.keys())]

    def get_class(self, adapter_id: str) -> type[BaseAdapter] | None:
        self.discover()
        return self._classes.get(adapter_id)

    def record_health(self, adapter_id: str, healthy: bool, error: str = "") -> None:
        """Update the live health flag after a probe."""
        self.discover()
        report = self._reports.get(adapter_id)
        if not report:
            return
        report.healthy = healthy
        report.last_error = error
        report.last_check = time.time()

    def negotiate(self, required: set[Capability]) -> CapabilityReport | None:
        """Return the first healthy adapter that supports all required capabilities."""
        self.discover()
        caps_strings = {c.value for c in required}
        for report in self.list_reports():
            if not report.healthy:
                continue
            if caps_strings.issubset(set(report.capabilities)):
                return report
        return None

    def snapshot(self) -> dict[str, Any]:
        """A serializable snapshot for the dashboard."""
        self.discover()
        return {
            "adapters": [r.to_dict() for r in self.list_reports()],
            "total": len(self._classes),
            "healthy": sum(1 for r in self._reports.values() if r.healthy),
            "discovered_at": time.time(),
        }


# Module-level singleton — one registry per process.
_REGISTRY = AdapterRegistry()


def get_registry() -> AdapterRegistry:
    return _REGISTRY