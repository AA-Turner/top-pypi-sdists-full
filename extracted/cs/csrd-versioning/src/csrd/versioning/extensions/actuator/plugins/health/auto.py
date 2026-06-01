"""Auto-detected health indicators based on ``app.state`` service connections.

When ``HealthActuatorPlugin`` has ``auto_discover=True`` (the default), it
inspects ``app.state`` on every health request and includes indicators for
any detected service connections.  This mirrors Spring Boot's auto-configuration
of health indicators for DataSource, Redis, RabbitMQ, etc.

Supported auto-detections:

=================  =============================  ================================
Indicator name     ``app.state`` key              Source package
=================  =============================  ================================
``db``             ``db_adapter``                 csrd-repository
``rabbit``         ``rabbit``                     RabbitMQ client
``kafka``          ``kafka_producer_manager`` /    Kafka client
                   ``kafka_consumer_manager``
``mongo``          ``mongo_client``               MongoDB client
``launchDarkly``   ``launchdarkly_client``         LaunchDarkly client
=================  =============================  ================================

Architecture Note
-----------------
These indicators live in the actuator package rather than alongside each
external client because:

- The indicators are thin wrappers that check one or two attributes via
  ``getattr`` with safe fallbacks.  The coupling is minimal.
- Keeping them co-located with the actuator avoids cross-package dependency
  issues.

If indicators later grow complex (queue depths, consumer lag, etc.), the
migration path to co-locating them with their source packages is clean:
move each class, swap ``_STATE_KEY_MAP`` lookup with import-based
discovery, and the plugin's public API stays unchanged.

Internal Attribute Dependencies
-------------------------------
These indicators depend on internal attributes of external packages.
If those attributes are renamed or removed, the indicators will log a
warning once per attribute and degrade gracefully (returning DOWN or
UNKNOWN).  Keep this list updated when adding new indicators.

- ``DBProtocol.fetch_one``              — csrd-repository
- ``AMQPState.connection``              — RabbitMQ (aio_pika)
- ``AbstractConnection.is_closed``      — aio_pika
- ``KafkaProducerManager._running``     — Kafka producer
- ``KafkaConsumerManager._running``     — Kafka consumer
- ``AsyncMongoClient.admin.command``    — pymongo
- ``LDClient.is_initialized()``         — launchdarkly-server-sdk
"""

import logging
from typing import Any

from fastapi import FastAPI

from .indicators import BaseHealthIndicator

logger = logging.getLogger(__name__)

# Registry populated by the @_auto class decorator.
_STATE_KEY_MAP: dict[str, tuple[tuple[str, ...], type]] = {}

# Tracks whether we've already warned about a missing attribute so we
# don't spam logs on every health request.
_WARNED: set[str] = set()


def _warn_missing(indicator: str, obj: object, attr: str) -> None:
    """Log once when an expected internal attribute is absent."""
    key = f"{indicator}.{attr}"
    if key not in _WARNED:
        _WARNED.add(key)
        logger.warning(
            "Health indicator '%s': expected attribute '%s' not found on %s. "
            "The upstream package may have changed its internals.",
            indicator,
            attr,
            type(obj).__qualname__,
        )


class AppStateHealthIndicator(BaseHealthIndicator):
    """Health indicator base for services discovered via ``app.state``.

    Extends :class:`BaseHealthIndicator` with helpers for reading
    ``app.state`` and guarding against internal attribute changes::

        class RedisHealthIndicator(AppStateHealthIndicator):
            _name = "redis"

            def _check(self) -> dict[str, Any]:
                client = self._get_state("redis_client")
                if client is None:
                    return {"status": "DOWN", "details": {"error": "State removed"}}
                ok, info = self._require_attr(client, "ping")
                if not ok:
                    return {"status": "DOWN", "details": {"error": "No ping method"}}
                info()
                return {"status": "UP"}
    """

    def __init__(self, app: FastAPI) -> None:
        self._app = app

    def _get_state(self, key: str) -> Any | None:
        """Return ``app.state.<key>`` or ``None``."""
        return getattr(self._app.state, key, None)

    def _require_attr(self, obj: object, attr: str) -> tuple[bool, Any]:
        """Return ``(True, value)`` if *obj* has *attr*, else warn and return ``(False, None)``."""
        if hasattr(obj, attr):
            return True, getattr(obj, attr)
        _warn_missing(self._name, obj, attr)
        return False, None


def _auto(name: str, *state_keys: str):
    """Register an auto-detectable indicator class."""

    def decorator(cls: type) -> type:
        cls._name = name  # type: ignore[attr-defined]
        _STATE_KEY_MAP[name] = (state_keys, cls)
        return cls

    return decorator


@_auto("rabbit", "rabbit")
class RabbitHealthIndicator(AppStateHealthIndicator):
    """RabbitMQ connection health via ``app.state.rabbit``.

    Depends on: ``AMQPState.connection``, ``AbstractConnection.is_closed``.
    """

    def _check(self) -> dict[str, Any]:
        rabbit = self._get_state("rabbit")
        if rabbit is None:
            return {"status": "DOWN", "details": {"error": "State removed"}}

        ok, connection = self._require_attr(rabbit, "connection")
        if not ok:
            return {"status": "DOWN", "details": {"error": "No connection attribute"}}

        ok, is_closed = self._require_attr(connection, "is_closed")
        if not ok:
            return {
                "status": "DOWN",
                "details": {"error": "Cannot determine connection state"},
            }

        if is_closed:
            return {"status": "DOWN", "details": {"error": "Connection closed"}}
        return {"status": "UP"}


@_auto("kafka", "kafka_producer_manager", "kafka_consumer_manager")
class KafkaHealthIndicator(AppStateHealthIndicator):
    """Kafka producer/consumer health via ``app.state.kafka_*_manager``.

    Depends on: ``KafkaProducerManager._running``, ``KafkaConsumerManager._running``
    (private attributes — may change without notice).
    """

    def _check(self) -> dict[str, Any]:
        components: dict[str, dict[str, Any]] = {}
        statuses: list[str] = []

        for role, state_key in (
            ("producer", "kafka_producer_manager"),
            ("consumer", "kafka_consumer_manager"),
        ):
            manager = self._get_state(state_key)
            if manager is None:
                continue
            ok, running = self._require_attr(manager, "_running")
            if not ok:
                running = False
            status = "UP" if running else "DOWN"
            components[role] = {"status": status}
            statuses.append(status)

        if not components:
            return {"status": "UNKNOWN"}

        overall = "DOWN" if "DOWN" in statuses else "UP"
        return {"status": overall, "components": components}


@_auto("mongo", "mongo_client")
class MongoHealthIndicator(AppStateHealthIndicator):
    """MongoDB connection health via ``app.state.mongo_client``.

    Depends on: ``AsyncMongoClient.admin.command`` (public pymongo API).
    """

    async def _check(self) -> dict[str, Any]:  # type: ignore[override]
        client = self._get_state("mongo_client")
        if client is None:
            return {"status": "DOWN", "details": {"error": "State removed"}}
        result = await client.admin.command("ping")
        return {"status": "UP", "details": result}


@_auto("launchDarkly", "launchdarkly_client")
class LaunchDarklyHealthIndicator(AppStateHealthIndicator):
    """LaunchDarkly SDK health via ``app.state.launchdarkly_client``.

    Depends on: ``LDClient.is_initialized()`` (public SDK API).
    """

    def _check(self) -> dict[str, Any]:
        client = self._get_state("launchdarkly_client")
        if client is None:
            return {"status": "DOWN", "details": {"error": "State removed"}}

        ok, is_initialized = self._require_attr(client, "is_initialized")
        if not ok:
            return {
                "status": "UNKNOWN",
                "details": {"error": "Cannot determine SDK state"},
            }

        if is_initialized():
            return {"status": "UP"}
        return {"status": "DOWN", "details": {"error": "Client not initialized"}}


@_auto("db", "db_adapter")
class DatabaseHealthIndicator(AppStateHealthIndicator):
    """Database connection health via ``app.state.db_adapter``.

    Runs ``SELECT 1`` through the csrd-repository adapter to verify the
    database connection is alive.  Works with SQLite, PostgreSQL, and
    MariaDB adapters — the query is portable across all three.

    Depends on: ``DBProtocol.fetch_one`` (public csrd-repository API).
    """

    async def _check(self) -> dict[str, Any]:  # type: ignore[override]
        adapter = self._get_state("db_adapter")
        if adapter is None:
            return {"status": "DOWN", "details": {"error": "State removed"}}

        ok, fetch_one = self._require_attr(adapter, "fetch_one")
        if not ok:
            return {"status": "DOWN", "details": {"error": "No fetch_one method"}}

        try:
            await fetch_one("SELECT 1")
        except Exception as exc:
            return {"status": "DOWN", "details": {"error": str(exc)}}
        return {"status": "UP", "details": {"database": type(adapter).__name__}}


def discover_indicators(app: FastAPI) -> dict[str, Any]:
    """Inspect ``app.state`` and return indicators for detected services.

    Only returns indicators for services whose state keys are present,
    meaning the corresponding lifespan has been configured.
    """
    found: dict[str, Any] = {}
    for name, (state_keys, cls) in _STATE_KEY_MAP.items():
        for key in state_keys:
            if hasattr(app.state, key):
                found[name] = cls(app)
                logger.debug(
                    "Auto-detected '%s' health indicator via app.state.%s",
                    name,
                    key,
                )
                break
    return found
