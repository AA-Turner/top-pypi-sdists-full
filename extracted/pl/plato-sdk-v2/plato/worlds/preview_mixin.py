"""Preview mode mixin for Plato worlds.

Extracted from BaseWorld to keep base.py focused on the core reset/step loop.
"""

from __future__ import annotations

import asyncio
import json
from typing import Any


class PreviewMixin:
    """Mixin providing preview loop and timeout helpers for BaseWorld."""

    async def _run_preview_loop(self, tracer: Any) -> None:
        """Execute the preview entrypoint after restoring runtime state."""
        await self._init_world(tracer)

        with tracer.start_as_current_span("preview") as preview_span:
            preview_span.set_attribute("plato.phase", "preview")
            preview_span.set_attribute("plato.world.name", self.name)
            preview_span.set_attribute("plato.preview.timeout_seconds", self.config.preview.timeout_seconds)
            obs = await self.preview()
            obs_data = obs.model_dump()
            preview_span.set_attribute("plato.preview.observation", json.dumps(obs_data, default=str))
            preview_url = (
                obs_data.get("data", {}).get("preview_url") if isinstance(obs_data.get("data"), dict) else None
            )
            if preview_url:
                preview_span.set_attribute("plato.preview.url", preview_url)

        self._final_result = obs_data
        self.logger.info("Preview loop complete, proceeding to finalize")

    async def wait_for_preview_timeout(self) -> int:
        """Keep the preview session alive until the configured timeout elapses.

        Call this at the end of your preview() implementation to idle.
        """
        timeout_seconds = self.config.preview.timeout_seconds
        elapsed = 0
        interval = 60
        self.logger.info("Preview mode active — %d seconds remaining", timeout_seconds)
        while elapsed < timeout_seconds:
            wait = min(interval, timeout_seconds - elapsed)
            await asyncio.sleep(wait)
            elapsed += wait
            remaining = timeout_seconds - elapsed
            if remaining > 0:
                self.logger.info("Preview: %d seconds remaining", remaining)
        self.logger.info("Preview timeout reached, shutting down")
        return timeout_seconds
