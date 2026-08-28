"""Stub file for engine.publish directory."""
from typing import Any

# Constants
logger: Any = ...  # From redis_stream

# Functions
# From redis_stream
def parse_sentinel_hosts(raw: Any, default_port: int = DEFAULT_SENTINEL_PORT) -> list[tuple[str, int]]:
    """
    Normalise Sentinel hosts into the ``[(host, port), ...]`` redis-py wants.
    
        Accepts what each source actually provides: a list of ``(host, port)`` pairs, a list of
        ``"host"`` or ``"host:port"`` strings, or the comma-separated string the k8s scheduler
        injects as ``REDIS_SENTINEL_HOSTS``.
    
        Args:
            raw: Any of the above, or ``None``.
            default_port: Port for entries that name only a host.
    
        Returns:
            The parsed pairs.  An unusable entry is skipped **with a warning** rather than
            raising: one malformed host in a list of three must not cost the other two, but a
            silently ignored host is how an HA deployment ends up writing to one Sentinel.
    """
    ...

# Classes
# From redis_stream
class RedisStreamPublisher:
    # A :class:`~matrice_analytics.engine.contract.emit.Publisher` backed by Redis streams.
    #
    #     Implements the whole protocol -- ``publish(stream, payload)`` -- and nothing else.  The
    #     payload is already built and validated by
    #     :mod:`matrice_analytics.engine.contract.emit`; this class knows about transport and
    #     counts what it could not deliver.
    #
    #     One client per instance, created on first use and re-created after a failure (behind
    #     :data:`RECONNECT_BACKOFF_SECONDS`).
    #
    #     Example:
    #         >>> publisher = RedisStreamPublisher({"host": "redis", "port": 6379})  # doctest: +SKIP
    #         >>> publisher.publish("results-agg", payload)                          # doctest: +SKIP
    #         >>> publisher.stats["published"]                                       # doctest: +SKIP
    #         1

    def __init__(self: Any, config: Any[str, Any] | None = None) -> None:
        """
        Resolve the connection target from ``config``, then the environment.
        
                Args:
                    config: Overrides, in precedence over the environment.  Recognised keys:
                        ``host``, ``port``, ``password``, ``username``, ``db``, ``sentinel_hosts``,
                        ``sentinel_port``, ``master_name``, and ``redis_client`` -- an already-built
                        client, which is how a test drives this class without a Redis.
                    clock: Anything with ``now() -> float``, used only for the reconnect backoff.
                        Defaults to :class:`~matrice_analytics.engine.primitives.base.WallClock`,
                        which is correct here and nowhere else: a backoff is a real-time property of
                        the network, not of the stream being replayed (**PY-13** is about *windowing*,
                        and windowing must never use a wall clock).
        
                Environment read when a key is absent: ``REDIS_HOST``, ``REDIS_PORT``,
                ``REDIS_PASSWORD``, ``REDIS_USERNAME``, ``REDIS_DB``, ``REDIS_SENTINEL_HOSTS``,
                ``REDIS_SENTINEL_PORT``, ``REDIS_MASTER_NAME``.
        """
        ...

    def close(self: Any) -> None:
        """
        Drop the client.  An injected one is released, never closed.
        
                Closing a caller-supplied client would be a surprise: the caller may be using it for
                something else.
        """
        ...

    def is_connected(self: Any) -> bool:
        """
        Whether a client is currently held.  Does not attempt a connection.
        """
        ...

    def publish(self: Any, stream: str, payload: dict[str, Any]) -> None:
        """
        ``XADD stream {"data": <json>, "_message_key": <camera_id>}``.
        
                Args:
                    stream: :data:`~matrice_analytics.engine.contract.emit.STREAM_RESULTS_AGG` or
                        :data:`~matrice_analytics.engine.contract.emit.STREAM_INCIDENT_RES`.
                    payload: A validated wire dict from
                        :func:`~matrice_analytics.engine.contract.emit.to_payload`.  **Not mutated** --
                        the protocol requires that, and the caller may still be holding it.
        
                Never raises.  A transport failure is counted in :attr:`stats` and logged: analytics is
                a side channel, and taking an inference worker down because a dashboard is unreachable
                is a worse failure than a missing minute of metrics.
        """
        ...

    def target(self: Any) -> str:
        """
        How the connection target reads in a log line.
        """
        ...

    def uses_sentinel(self: Any) -> bool:
        """
        Whether this publisher will resolve the master through Sentinel.
        """
        ...


from . import redis_stream