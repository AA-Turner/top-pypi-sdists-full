"""L2 lifecycle bridge for the Claude Agent SDK integration.

Subclasses :class:`MonkeyPatchLifecycle`; declares the entry points to
patch via :func:`patch_targets`. Per-entry-point wrapper bodies live
in the ``_patches/`` subpackage as ``*_patch_target()`` factories.
"""

from __future__ import annotations

import logging
from typing import Any

from aigie.tracing.monkey_patch_lifecycle import MonkeyPatchLifecycle, PatchTarget

from ._patches import (
    client_aexit_patch_target,
    client_connect_patch_target,
    client_query_patch_target,
    client_receive_patch_target,
    query_patch_target,
)

logger = logging.getLogger(__name__)


class ClaudeAgentSDKLifecycle(MonkeyPatchLifecycle):
    """Install/uninstall the Claude Agent SDK monkey-patches."""

    framework_type = "claude_agent_sdk"

    def __init__(
        self,
        emitter: Any = None,
        adapter: Any = None,
        *,
        config: Any = None,
    ) -> None:
        super().__init__()
        self._emitter = emitter
        self._adapter = adapter
        self._config = config

    def patch_targets(self) -> list[PatchTarget]:
        return [
            query_patch_target(),
            client_query_patch_target(),
            client_connect_patch_target(),
            client_aexit_patch_target(),
            client_receive_patch_target(),
        ]


# Module-level singleton used by ``IntegrationInfo.patch_function`` and the
# test conftest. A shared instance is required so that an ``install``
# performed by one entry point can be reversed by a later ``uninstall``
# without losing the originals registry.
_singleton: ClaudeAgentSDKLifecycle | None = None


def _get_singleton() -> ClaudeAgentSDKLifecycle:
    global _singleton
    if _singleton is None:
        _singleton = ClaudeAgentSDKLifecycle()
    return _singleton


def install_claude_agent_sdk_patches() -> None:
    """Module-level entry point for ``IntegrationInfo.patch_function``."""
    _get_singleton().install()


def uninstall_claude_agent_sdk_patches() -> None:
    """Module-level uninstaller used by the test conftest."""
    _get_singleton().uninstall()


__all__ = [
    "ClaudeAgentSDKLifecycle",
    "install_claude_agent_sdk_patches",
    "uninstall_claude_agent_sdk_patches",
]
