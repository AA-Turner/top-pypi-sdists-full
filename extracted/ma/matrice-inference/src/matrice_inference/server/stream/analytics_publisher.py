"""Analytics Publisher — re-export shim.

The implementation was relocated to the analytics SDK so that all analytics
publishing lives in one place:

    matrice_analytics.analytics.analytics_publisher

This module is kept as a thin re-export for backward compatibility: every
existing import (``from matrice_inference.server.stream.analytics_publisher
import AnalyticsPublisher``) — used by this package's own streaming pipeline
(server.py, producer_worker, async_producer_pool, stream_pipeline) and by
tests — keeps working unchanged. matrice_inference already depends on
matrice_analytics, so this adds no new dependency direction.

The publisher's public constants (``ANALYTICS_TOPIC``, ``ANALYTICS_ZONE_GLOBAL``,
``DEFAULT_AGGREGATION_INTERVAL``, ``DEFAULT_PUBLISH_INTERVAL``) are class
attributes of ``AnalyticsPublisher`` and are reached through it.
"""

from matrice_analytics.analytics.analytics_publisher import AnalyticsPublisher

__all__ = ["AnalyticsPublisher"]
