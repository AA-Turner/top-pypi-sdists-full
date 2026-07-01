"""
Channel bootstrap for CVC.

This module is the single entry point for the gateway + daemon to wire
the channel stack together:

  1. Build a fresh :class:`ChannelRegistry`.
  2. Register every available adapter class. Importing is lazy — if a
     channel's SDK isn't installed, we skip that adapter with a log
     line and continue. CVC stays importable on any machine.
  3. Optionally start the configured channels.

The dashboard, the CLI, and the FastAPI gateway all import
:func:`get_registry` (a process-wide singleton). They get back a
working :class:`ChannelRegistry` populated with every available
adapter class but with no channels running until :func:`start_all` is
called with the live config dict.
"""

from __future__ import annotations

import logging
from typing import Any, Dict, List, Optional

from .channels.base import BaseChannelAdapter, ChannelStatus
from .channels.registry import ChannelRegistry
from .cvc_bindings import (
    make_echo_agent_runner,
    make_logging_commit_hook,
)


logger = logging.getLogger(__name__)


_REGISTRY: Optional[ChannelRegistry] = None


def get_registry() -> ChannelRegistry:
    """Return the process-wide :class:`ChannelRegistry`, building it on
    first call. Idempotent — calling twice returns the same instance."""
    global _REGISTRY
    if _REGISTRY is not None:
        return _REGISTRY
    reg = ChannelRegistry()
    _install_default_handlers(reg)
    _register_builtin_adapters(reg)
    _REGISTRY = reg
    return reg


def reset_registry() -> None:
    """Drop the singleton (used by tests and the dashboard's reload action)."""
    global _REGISTRY
    _REGISTRY = None


def _install_default_handlers(reg: ChannelRegistry) -> None:
    """Plug in the fallback commit hook + echo agent runner.

    The real gateway replaces these with concrete implementations that
    touch the CVC engine + chat pipeline; until it does, channels
    still work but commit hashes are synthetic and agent replies are
    echoes of the inbound. That makes the dashboard non-empty during
    early bootstrap.
    """
    reg.set_commit_hook(make_logging_commit_hook())
    reg.set_agent_runner(make_echo_agent_runner())


def _register_builtin_adapters(reg: ChannelRegistry) -> None:
    """Lazy-import every adapter module so a missing SDK doesn't break CVC."""
    for module_name, class_name, registry_name in _BUILTIN_ADAPTERS:
        try:
            module = __import__(module_name, fromlist=[class_name])
            cls = getattr(module, class_name)
            reg.register(registry_name, cls({}))
        except Exception as exc:  # noqa: BLE001
            logger.debug("bootstrap: %s not available (%s)", registry_name, exc)


# (module_path, class_name, registry_name) tuples. Order matters for
# the dashboard listing — keep this in priority order (Telegram first).
_BUILTIN_ADAPTERS: List[tuple] = [
    ("cvc.integrations.channels.telegram", "TelegramAdapter", "telegram"),
    ("cvc.integrations.channels.discord", "DiscordAdapter", "discord"),
    ("cvc.integrations.channels.slack", "SlackAdapter", "slack"),
    ("cvc.integrations.channels.whatsapp", "WhatsAppAdapter", "whatsapp"),
    ("cvc.integrations.channels.matrix", "MatrixAdapter", "matrix"),
    ("cvc.integrations.channels.email", "EmailAdapter", "email"),
    ("cvc.integrations.channels.webhook", "WebhookAdapter", "webhook"),
]


def available_adapters() -> List[Dict[str, Any]]:
    """Return a description of every adapter that successfully imported.

    Used by the dashboard to render the "Available Channels" panel and
    by the CLI's ``cvc channels list`` command.
    """
    reg = get_registry()
    out: List[Dict[str, Any]] = []
    for name in reg.list_names():
        adapter = reg.get(name)
        if adapter is None:
            continue
        status: ChannelStatus = adapter.status()
        out.append({
            "name": name,
            "capabilities": [c.value for c in status.capabilities],
            "enabled": status.enabled,
            "healthy": status.healthy,
            "info": status.info,
            "config_keys": status.config_keys,
            "last_error": status.last_error,
        })
    return out


async def start_all(configs: Dict[str, Dict[str, Any]]) -> None:
    """Start every adapter whose config has ``enabled=True``."""
    reg = get_registry()
    await reg.start_all(configs)


async def stop_all() -> None:
    """Stop every running adapter."""
    reg = get_registry()
    await reg.stop_all()
