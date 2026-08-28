"""Transport for the two outbound Redis streams.

``clauding/STAGE_BC_PLAN.md`` §3 (C4).  The contract module deliberately stops at a validated
dict and a two-line :class:`~matrice_analytics.engine.contract.emit.Publisher` protocol; this
package is the only place that knows about a socket.

:class:`~matrice_analytics.engine.publish.redis_stream.RedisStreamPublisher` is the
implementation.  It imports ``redis`` lazily and degrades to a logged no-op, so the engine
stays importable -- and a manifest stays validatable -- in an environment with no Redis.

Nothing here imports ``post_processing`` (**PY-20**).
"""

from __future__ import annotations

from matrice_analytics.engine.publish.redis_stream import (
    DEFAULT_SENTINEL_PORT,
    MESSAGE_KEY_FIELD,
    RECONNECT_BACKOFF_SECONDS,
    RedisStreamPublisher,
    parse_sentinel_hosts,
)

__all__ = [
    "DEFAULT_SENTINEL_PORT",
    "MESSAGE_KEY_FIELD",
    "RECONNECT_BACKOFF_SECONDS",
    "RedisStreamPublisher",
    "parse_sentinel_hosts",
]
