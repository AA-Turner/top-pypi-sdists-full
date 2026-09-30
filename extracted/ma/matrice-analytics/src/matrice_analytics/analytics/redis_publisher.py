"""Direct Redis publisher for the new analytics flow.

The new flow publishes two streams, matching the validated fire-detection
harness exactly:

    XADD incident_res MAXLEN ~ N  {"data": json.dumps(payload), "_message_key": camera_id}
    XADD results-agg  MAXLEN ~ N  {"data": json.dumps(payload), "_message_key": camera_id}

Both are shared keys no consumer trims, so every XADD carries an approximate
``MAXLEN`` (``stream_maxlen`` in the config, else ``MATRICE_ANALYTICS_STREAM_MAXLEN``,
else ``DEFAULT_STREAM_MAXLEN``). Unbounded, they grow until Redis evicts the
whole key together with its consumer groups.

Publishing happens from inside the SDK (in the worker process), the same way
the LPR use-case already talks to its server and the harness publishes — so the
inference pipeline needs no publisher wiring. ``redis`` is imported lazily and a
single client is reused per process; if redis is unavailable or unconfigured,
publishing degrades to a logged no-op (detections still reach the per-camera
output topic through the normal pipeline path).

Connection config comes from the caller's override dict first, then the
environment (``REDIS_HOST``/``REDIS_PORT``/``REDIS_PASSWORD``/``REDIS_USERNAME``,
plus ``REDIS_SENTINEL_HOSTS``/``REDIS_SENTINEL_PORT``/``REDIS_MASTER_NAME``).

On an HA deployment the plain host is a Service that fronts the master AND its
replicas, so writes land on a read-only replica roughly half the time. When
Sentinel details are available they are used instead: Sentinel resolves the
current master and follows failover. The passed-in config always wins over the
environment, so a caller that already resolved the topology (the inference
pipeline does) does not depend on the pod's env being set.
"""

import json
import logging
import os
import time
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

INCIDENT_STREAM = "incident_res"
AGG_STREAM = "results-agg"

_RECONNECT_BACKOFF_SEC = 5.0
_DEFAULT_SENTINEL_PORT = 26379

# Approximate cap per stream, sized to the consumer-lag budget: how far a stalled
# reader may fall behind before the oldest entries are trimmed. Same cap as the
# LPR sighting stream and engine.publish.redis_stream.DEFAULT_STREAM_MAXLEN.
DEFAULT_STREAM_MAXLEN = 100_000
STREAM_MAXLEN_ENV = "MATRICE_ANALYTICS_STREAM_MAXLEN"


def _resolve_stream_maxlen(raw: Any) -> int:
    """A positive stream cap; anything unusable falls back to the default.

    No value switches the cap off -- an unbounded stream is the failure it exists
    to prevent.
    """
    if raw is None or raw == "":
        return DEFAULT_STREAM_MAXLEN
    try:
        value = int(raw)
    except (TypeError, ValueError):
        logger.warning(
            "Ignoring non-integer stream maxlen %r; using %d", raw, DEFAULT_STREAM_MAXLEN
        )
        return DEFAULT_STREAM_MAXLEN
    if value <= 0:
        logger.warning(
            "Ignoring non-positive stream maxlen %d; using %d", value, DEFAULT_STREAM_MAXLEN
        )
        return DEFAULT_STREAM_MAXLEN
    return value


def _parse_sentinel_hosts(raw: Any, default_port: int) -> List[Tuple[str, int]]:
    """Normalize sentinel hosts into the ``[(host, port), …]`` redis-py wants.

    Accepts what each source actually provides: a list of ``(host, port)``
    pairs, a list of ``"host"`` or ``"host:port"`` strings, or the
    comma-separated string form used by the ``REDIS_SENTINEL_HOSTS`` env var
    that the k8s scheduler injects.
    """
    if not raw:
        return []
    items = raw.split(",") if isinstance(raw, str) else list(raw)

    hosts: List[Tuple[str, int]] = []
    for item in items:
        if isinstance(item, (list, tuple)) and len(item) == 2:
            host, port = item[0], item[1]
        elif isinstance(item, str):
            host, _, port_str = item.strip().partition(":")
            port = port_str or default_port
        else:
            logger.warning("Ignoring unrecognised sentinel host entry: %r", item)
            continue
        host = str(host).strip()
        if not host:
            continue
        try:
            hosts.append((host, int(port)))
        except (TypeError, ValueError):
            logger.warning("Ignoring sentinel host %r with a non-integer port %r", host, port)
    return hosts


class AnalyticsRedisPublisher:
    """Lazy, per-process Redis publisher for incident_res + results-agg."""

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        config = config or {}
        self.host = config.get("host") or os.environ.get("REDIS_HOST", "localhost")
        self.port = int(config.get("port") or os.environ.get("REDIS_PORT", "6379"))
        self.password = config.get("password") or os.environ.get("REDIS_PASSWORD")
        self.username = config.get("username") or os.environ.get("REDIS_USERNAME")
        self.db = int(config.get("db") or os.environ.get("REDIS_DB", "0"))
        sentinel_port = int(
            config.get("sentinel_port")
            or os.environ.get("REDIS_SENTINEL_PORT", _DEFAULT_SENTINEL_PORT)
        )
        self.sentinel_hosts = _parse_sentinel_hosts(
            config.get("sentinel_hosts") or os.environ.get("REDIS_SENTINEL_HOSTS"),
            sentinel_port,
        )
        self.master_name = config.get("master_name") or os.environ.get("REDIS_MASTER_NAME")
        self.stream_maxlen = _resolve_stream_maxlen(
            config.get("stream_maxlen") or os.environ.get(STREAM_MAXLEN_ENV)
        )
        self._trim_rejected = False
        self._client = config.get("redis_client")  # injectable for tests
        self._injected = self._client is not None
        self._last_connect_attempt = 0.0
        self._import_failed = False
        self.stats = {"incidents": 0, "aggregations": 0, "errors": 0, "dropped": 0, "untrimmed": 0}

    # ------------------------------------------------------------------
    # Connection
    # ------------------------------------------------------------------

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        if self._import_failed:
            return None
        now = time.time()
        if now - self._last_connect_attempt < _RECONNECT_BACKOFF_SEC:
            return None
        self._last_connect_attempt = now
        try:
            import redis  # lazy: only needed when the new flow is active
        except Exception as e:  # noqa: BLE001 - any import failure disables publishing, logged
            self._import_failed = True
            logger.warning("redis not importable (%s) — analytics publishing disabled", e)
            return None
        try:
            if self.sentinel_hosts and self.master_name:
                client = self._connect_via_sentinel()
            else:
                client = redis.Redis(
                    host=self.host,
                    port=self.port,
                    password=self.password,
                    username=self.username,
                    db=self.db,
                    decode_responses=False,
                    socket_connect_timeout=5,
                    socket_timeout=5,
                )
            client.ping()
            self._client = client
            self._trim_rejected = False
            logger.info("AnalyticsRedisPublisher connected to redis %s", self._target_description())
        except Exception as e:  # noqa: BLE001 - connect failure is logged and retried after backoff
            logger.warning(
                "AnalyticsRedisPublisher redis connect failed (%s): %s",
                self._target_description(),
                e,
            )
            self._client = None
        return self._client

    def _connect_via_sentinel(self) -> Any:
        """Resolve the current master through Sentinel.

        Mirrors ``matrice_common.stream.redis_stream.RedisUtils`` so the whole
        stack discovers the master the same way. Sentinel owns the resulting
        connection pool and re-resolves after a failover, which a fixed host
        cannot do.
        """
        from redis.sentinel import Sentinel

        sentinel_kwargs: Dict[str, Any] = {"socket_timeout": 5}
        if self.password:
            sentinel_kwargs["password"] = self.password
        sentinel = Sentinel(self.sentinel_hosts, **sentinel_kwargs)

        master_kwargs: Dict[str, Any] = {
            "db": self.db,
            "socket_timeout": 5,
            "decode_responses": False,
            "retry_on_timeout": True,
            "health_check_interval": 30,
        }
        if self.password:
            master_kwargs["password"] = self.password
        if self.username:
            master_kwargs["username"] = self.username
        return sentinel.master_for(self.master_name, **master_kwargs)

    def _target_description(self) -> str:
        """How the connection target reads in a log line."""
        if self.sentinel_hosts and self.master_name:
            hosts = ",".join(f"{h}:{p}" for h, p in self.sentinel_hosts)
            return f"sentinel[{hosts}] master={self.master_name}"
        return f"{self.host}:{self.port}"

    # ------------------------------------------------------------------
    # Publishing
    # ------------------------------------------------------------------

    def _xadd(self, stream: str, camera_id: str, payload: Dict[str, Any]) -> bool:
        if not isinstance(payload, dict):
            self.stats["dropped"] += 1
            return False
        client = self._get_client()
        if client is None:
            self.stats["errors"] += 1
            return False
        try:
            self._trimmed_xadd(
                client,
                stream,
                {"data": json.dumps(payload, default=str), "_message_key": camera_id},
            )
            return True
        except Exception as e:  # noqa: BLE001 - a failed XADD is counted and logged, never raised
            self.stats["errors"] += 1
            logger.warning("AnalyticsRedisPublisher XADD to %s failed: %s", stream, e)
            if not self._injected:
                self._client = None  # force reconnect on next publish (with backoff)
            return False

    def _trimmed_xadd(self, client: Any, stream: str, fields: Dict[str, str]) -> None:
        """XADD with ``MAXLEN ~ stream_maxlen``; raises what the client raises.

        A client that rejects the trim keywords (an injected duck-typed wrapper --
        redis-py accepts them) still gets the write, but the stream is then
        unbounded, so that is warned once and counted in ``stats["untrimmed"]``.
        """
        if not self._trim_rejected:
            try:
                client.xadd(stream, fields, maxlen=self.stream_maxlen, approximate=True)
                return
            except TypeError as e:
                self._trim_rejected = True
                logger.warning(
                    "AnalyticsRedisPublisher: client %s rejected XADD MAXLEN (%s); "
                    "%s is written untrimmed",
                    type(client).__name__,
                    e,
                    stream,
                )
        client.xadd(stream, fields)
        self.stats["untrimmed"] += 1

    def publish_incident(self, camera_id: str, payload: Dict[str, Any]) -> bool:
        ok = self._xadd(INCIDENT_STREAM, camera_id, payload)
        if ok:
            self.stats["incidents"] += 1
        return ok

    def publish_aggregation(self, camera_id: str, payload: Dict[str, Any]) -> bool:
        ok = self._xadd(AGG_STREAM, camera_id, payload)
        if ok:
            self.stats["aggregations"] += 1
        return ok
