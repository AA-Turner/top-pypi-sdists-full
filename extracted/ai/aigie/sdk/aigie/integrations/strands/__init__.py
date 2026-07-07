"""Strands Agents SDK integration for Aigie (tracing-only).

``aigie.init(framework="strands")`` triggers ``@register_adapter`` via the eager
import at the bottom of this file. From then on every constructed ``Agent`` /
``Swarm`` / ``Graph`` gets an ``StrandsHookProvider`` injected and emits spans.
"""

from __future__ import annotations

from aigie.integrations.strands.adapter import StrandsAdapter
from aigie.integrations.strands.config import StrandsConfig
from aigie.integrations.strands.lifecycle import StrandsLifecycle
from aigie.integrations.strands.native_callback import StrandsHookProvider, strands_session

__all__ = [
    "StrandsAdapter",
    "StrandsConfig",
    "StrandsHookProvider",
    "StrandsLifecycle",
    "strands_session",
]
