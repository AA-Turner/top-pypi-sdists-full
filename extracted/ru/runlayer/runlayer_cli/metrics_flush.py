from __future__ import annotations

import anyio.to_thread
import httpx
import structlog

from runlayer_cli.metrics import InstallationAnalyticsEvent, InstallationMetricsClient

logger = structlog.get_logger(__name__)


async def flush_installation_events(
    *,
    client: InstallationMetricsClient,
    events: list[InstallationAnalyticsEvent],
) -> None:
    if not events:
        return

    try:
        await anyio.to_thread.run_sync(client.track_installation_events, events)
    except httpx.HTTPError:
        logger.warning(
            "install_metrics_flush_failed",
            installed=len(events),
            exc_info=True,
        )
