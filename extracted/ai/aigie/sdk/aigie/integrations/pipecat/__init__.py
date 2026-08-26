"""Pipecat voice-agent integration for Aigie (tracing-only).

``aigie.init(framework="pipecat")`` triggers ``@register_adapter`` via the eager
import at the bottom of this file. From then on every constructed
``PipelineWorker`` (and its deprecated alias ``PipelineTask``) gets a
``PipecatObserver`` injected and emits spans.
"""

from __future__ import annotations

from aigie.integrations.pipecat.adapter import PipecatAdapter
from aigie.integrations.pipecat.config import PipecatConfig
from aigie.integrations.pipecat.lifecycle import PipecatLifecycle
from aigie.integrations.pipecat.native_callback import PipecatObserver

__all__ = [
    "PipecatAdapter",
    "PipecatConfig",
    "PipecatLifecycle",
    "PipecatObserver",
]
