"""The Redis transport for ``results-agg`` and ``incident_res``.

Normative sources: ``_contracts/07-tobe-canonical-contract.md`` §§2-3 and
``clauding/STAGE_BC_PLAN.md`` §3 (C4).  Ported from
``analytics/redis_publisher.py:113-192``, which is **correct** -- the lazy import, the
connect backoff, the Sentinel resolution and the config-over-environment precedence are all
carried over deliberately.

Four behaviours are load-bearing:

**``XADD <stream> {"data": <json>}``.**  Every consumer hedges on the field name --
be-media-server tries ``data`` then any valid-JSON field, be-analytics tries ``data`` then
``result`` then ``value`` -- which is evidence it changed at least once.  py_analytics has
always written ``data`` and :data:`~matrice_analytics.engine.contract.emit.PAYLOAD_FIELD` is
the single declaration of it.

**Lazy ``redis`` import, degrading to a logged no-op.**  Analytics is a side channel: the
detections still reach the per-camera output topic through the pipeline whether or not this
publisher can connect.  Raising here would take a whole inference worker down because a
dashboard is unreachable, so a failed publish is counted and logged, never propagated.  What
it must not do is fail *silently* -- hence :attr:`RedisStreamPublisher.stats`.

**Sentinel when available, plain host otherwise.**  On an HA deployment the plain host is a
Service fronting the master *and* its replicas, so roughly half of all writes land on a
read-only replica and fail.  With Sentinel details present, Sentinel resolves the current
master and follows failover -- the same discovery ``matrice_common.stream.redis_stream``
uses, so the whole stack agrees on where the master is.

**The passed-in config wins over the environment.**  A caller that already resolved the
topology (the inference pipeline has) must not be overridden by whatever the pod's env
happens to say.

This module imports **nothing** from ``post_processing`` (**PY-20**): the engine now loads
zero legacy modules, and a transport is the easiest place to lose that property.
"""

from __future__ import annotations

import json
import logging
import os
from collections.abc import Mapping
from typing import Any, Final

from matrice_analytics.engine.contract.emit import (
    PAYLOAD_FIELD,
    STREAM_INCIDENT_RES,
    STREAM_RESULTS_AGG,
)

__all__ = [
    "DEFAULT_SENTINEL_PORT",
    "MESSAGE_KEY_FIELD",
    "RECONNECT_BACKOFF_SECONDS",
    "RedisStreamPublisher",
    "parse_sentinel_hosts",
]

logger = logging.getLogger(__name__)


MESSAGE_KEY_FIELD: Final[str] = "_message_key"
"""Partitioning hint written beside the payload, set to the camera id.

Not part of the contract -- consumers ignore it -- but it keeps one camera's messages in
order when a consumer group shards by key, which is what makes an incident's open/close pair
arrive in the order it happened.
"""

RECONNECT_BACKOFF_SECONDS: Final[float] = 5.0
"""Minimum gap between connection attempts.

Without it, a camera at 25 fps whose Redis is down attempts 25 TCP connects a second and the
connect timeouts become the frame budget.
"""

DEFAULT_SENTINEL_PORT: Final[int] = 26379
_SOCKET_TIMEOUT: Final[int] = 5


def parse_sentinel_hosts(raw: Any, default_port: int = DEFAULT_SENTINEL_PORT) -> list[tuple[str, int]]:
    """Normalise Sentinel hosts into the ``[(host, port), ...]`` redis-py wants.

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
    if not raw:
        return []
    items = raw.split(",") if isinstance(raw, str) else list(raw)

    hosts: list[tuple[str, int]] = []
    for item in items:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            host, port = item[0], item[1]
        elif isinstance(item, str):
            host, _, port_text = item.strip().partition(":")
            port = port_text or default_port
        else:
            logger.warning("ignoring unrecognised sentinel host entry: %r", item)
            continue
        host = str(host).strip()
        if not host:
            continue
        try:
            hosts.append((host, int(port)))
        except (TypeError, ValueError):
            logger.warning("ignoring sentinel host %r with a non-integer port %r", host, port)
    return hosts


class RedisStreamPublisher:
    """A :class:`~matrice_analytics.engine.contract.emit.Publisher` backed by Redis streams.

    Implements the whole protocol -- ``publish(stream, payload)`` -- and nothing else.  The
    payload is already built and validated by
    :mod:`matrice_analytics.engine.contract.emit`; this class knows about transport and
    counts what it could not deliver.

    One client per instance, created on first use and re-created after a failure (behind
    :data:`RECONNECT_BACKOFF_SECONDS`).

    Example:
        >>> publisher = RedisStreamPublisher({"host": "redis", "port": 6379})  # doctest: +SKIP
        >>> publisher.publish("results-agg", payload)                          # doctest: +SKIP
        >>> publisher.stats["published"]                                       # doctest: +SKIP
        1
    """

    __slots__ = (
        "_client",
        "_clock",
        "_db",
        "_host",
        "_import_failed",
        "_injected",
        "_last_attempt",
        "_master_name",
        "_password",
        "_port",
        "_sentinel_hosts",
        "_username",
        "stats",
    )

    def __init__(
        self,
        config: Mapping[str, Any] | None = None,
        *,
        clock: Any = None,
    ) -> None:
        """Resolve the connection target from ``config``, then the environment.

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
        settings = dict(config or {})
        self._host: str = str(settings.get("host") or os.environ.get("REDIS_HOST", "localhost"))
        self._port: int = int(settings.get("port") or os.environ.get("REDIS_PORT", "6379"))
        self._password: str | None = settings.get("password") or os.environ.get("REDIS_PASSWORD")
        self._username: str | None = settings.get("username") or os.environ.get("REDIS_USERNAME")
        self._db: int = int(settings.get("db") or os.environ.get("REDIS_DB", "0"))
        sentinel_port = int(
            settings.get("sentinel_port")
            or os.environ.get("REDIS_SENTINEL_PORT", DEFAULT_SENTINEL_PORT)
        )
        self._sentinel_hosts = parse_sentinel_hosts(
            settings.get("sentinel_hosts") or os.environ.get("REDIS_SENTINEL_HOSTS"),
            sentinel_port,
        )
        self._master_name: str | None = settings.get("master_name") or os.environ.get(
            "REDIS_MASTER_NAME"
        )

        self._client: Any = settings.get("redis_client")
        self._injected: bool = self._client is not None
        self._import_failed = False
        self._last_attempt = 0.0
        if clock is None:
            from matrice_analytics.engine.primitives.base import WallClock  # noqa: PLC0415

            clock = WallClock()
        self._clock = clock

        self.stats: dict[str, int] = {
            "published": 0,
            STREAM_RESULTS_AGG: 0,
            STREAM_INCIDENT_RES: 0,
            "errors": 0,
            "dropped": 0,
        }
        """Delivery counters.  ``errors`` counts failed publishes, ``dropped`` malformed ones.

        The whole reason a degraded publisher is acceptable: "analytics is quiet" and "analytics
        cannot reach Redis" must be distinguishable *from inside the process*.
        """

    # -- the Publisher protocol ---------------------------------------------

    def publish(self, stream: str, payload: dict[str, Any]) -> None:
        """``XADD stream {"data": <json>, "_message_key": <camera_id>}``.

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
        if not isinstance(payload, Mapping):
            self.stats["dropped"] += 1
            logger.warning(
                "refusing to publish a %s to %r: the payload must be the dict built by "
                "contract.emit.to_payload()",
                type(payload).__name__,
                stream,
            )
            return

        client = self._connect()
        if client is None:
            self.stats["errors"] += 1
            return

        try:
            body = json.dumps(payload, default=str)
        except (TypeError, ValueError) as exc:
            # Unreachable for a payload that came through to_payload() (mode="json"), which is
            # the only supported input -- but a JSON error here would otherwise surface as a
            # transport failure and send someone to look at Redis.
            self.stats["dropped"] += 1
            logger.error("payload for %r is not JSON-serialisable: %s", stream, exc)
            return

        fields = {PAYLOAD_FIELD: body}
        camera_id = payload.get("camera_id")
        if isinstance(camera_id, str) and camera_id:
            fields[MESSAGE_KEY_FIELD] = camera_id

        try:
            client.xadd(stream, fields)
        except Exception as exc:  # noqa: BLE001 - transport failures must not propagate
            self.stats["errors"] += 1
            logger.warning("XADD to %s failed: %s", stream, exc)
            if not self._injected:
                # Force a reconnect on the next publish, behind the backoff. An injected
                # client belongs to the caller and is never discarded.
                self._client = None
            return

        self.stats["published"] += 1
        if stream in self.stats:
            self.stats[stream] += 1
        logger.debug("published to %s (%d bytes)", stream, len(body))

    # -- connection ---------------------------------------------------------

    @property
    def target(self) -> str:
        """How the connection target reads in a log line."""
        if self._sentinel_hosts and self._master_name:
            hosts = ",".join(f"{host}:{port}" for host, port in self._sentinel_hosts)
            return f"sentinel[{hosts}] master={self._master_name}"
        return f"{self._host}:{self._port}"

    @property
    def uses_sentinel(self) -> bool:
        """Whether this publisher will resolve the master through Sentinel."""
        return bool(self._sentinel_hosts and self._master_name)

    @property
    def is_connected(self) -> bool:
        """Whether a client is currently held.  Does not attempt a connection."""
        return self._client is not None

    def _connect(self) -> Any:
        """The client, connecting on first use and after a failure.

        Returns ``None`` -- never raises -- when ``redis`` is not installed or the server is
        unreachable.  The import is lazy because the engine must stay importable in an
        environment with no Redis at all (a test, a CLI validating a manifest), and
        ``_import_failed`` makes that a one-time cost rather than a per-frame ``ImportError``.
        """
        if self._client is not None:
            return self._client
        if self._import_failed:
            return None
        now = float(self._clock.now())
        if now - self._last_attempt < RECONNECT_BACKOFF_SECONDS:
            return None
        self._last_attempt = now

        try:
            import redis  # noqa: PLC0415 - lazy on purpose; see the docstring
        except Exception as exc:  # noqa: BLE001 - any import failure degrades the same way
            self._import_failed = True
            logger.warning(
                "redis is not importable (%s) -- analytics publishing is disabled for this "
                "process. Detections still reach the per-camera output topic; results-agg and "
                "incident_res do not.",
                exc,
            )
            return None

        try:
            client = (
                self._connect_via_sentinel()
                if self.uses_sentinel
                else redis.Redis(
                    host=self._host,
                    port=self._port,
                    password=self._password,
                    username=self._username,
                    db=self._db,
                    decode_responses=False,
                    socket_connect_timeout=_SOCKET_TIMEOUT,
                    socket_timeout=_SOCKET_TIMEOUT,
                )
            )
            client.ping()
        except Exception as exc:  # noqa: BLE001 - unreachable Redis is not fatal
            logger.warning("redis connect failed (%s): %s", self.target, exc)
            self._client = None
            return None

        self._client = client
        logger.info("analytics publisher connected to redis %s", self.target)
        return client

    def _connect_via_sentinel(self) -> Any:
        """Resolve the current master through Sentinel.

        Sentinel owns the resulting connection pool and re-resolves after a failover, which a
        fixed host cannot do -- and on an HA deployment a fixed host is a Service fronting the
        replicas too, so half the writes hit a read-only node.
        """
        from redis.sentinel import Sentinel  # noqa: PLC0415 - lazy with the parent import

        sentinel_kwargs: dict[str, Any] = {"socket_timeout": _SOCKET_TIMEOUT}
        if self._password:
            sentinel_kwargs["password"] = self._password
        sentinel = Sentinel(self._sentinel_hosts, **sentinel_kwargs)

        master_kwargs: dict[str, Any] = {
            "db": self._db,
            "socket_timeout": _SOCKET_TIMEOUT,
            "decode_responses": False,
            "retry_on_timeout": True,
            "health_check_interval": 30,
        }
        if self._password:
            master_kwargs["password"] = self._password
        if self._username:
            master_kwargs["username"] = self._username
        return sentinel.master_for(self._master_name, **master_kwargs)

    def close(self) -> None:
        """Drop the client.  An injected one is released, never closed.

        Closing a caller-supplied client would be a surprise: the caller may be using it for
        something else.
        """
        client = self._client
        self._client = None
        if client is not None and not self._injected:
            closer = getattr(client, "close", None)
            if callable(closer):
                try:
                    closer()
                except Exception as exc:  # noqa: BLE001 - closing must not raise either
                    logger.debug("closing the redis client raised: %s", exc)

    def __repr__(self) -> str:
        return (
            f"RedisStreamPublisher(target={self.target!r}, connected={self.is_connected}, "
            f"published={self.stats['published']}, errors={self.stats['errors']})"
        )
