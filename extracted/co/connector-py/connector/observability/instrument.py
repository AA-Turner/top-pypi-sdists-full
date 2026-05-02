import logging
import re
from functools import cached_property
from typing import TypedDict, cast

import datadog
from datadog.dogstatsd.base import statsd
from datadog.dogstatsd.context import TimedContextManagerDecorator
from typing_extensions import Self

__all__ = ["Instrument"]


def initialize():
    """Attempts to initialize our observability instrumentation."""
    logger = logging.getLogger(__name__)

    # NOTE: This is used to intiliaze the datadog stats agent for stats collection.
    # For some reason, mypy does not detect that the initialize method exists
    # in datadog.
    try:
        datadog.initialize()  # type: ignore[attr-defined]
    except Exception:
        logger.exception("Failed to initialize datadog.", exc_info=True)


# NOTE: Initialize our observability instrumentation. This should be called once
# during application startup.
initialize()


class DefaultRate(TypedDict, total=False):
    """Used to specify default rates for sampling stat emission."""

    counter: float
    gauge: float
    timer: float
    distribution: float


class InstrumentMeta(type):
    def __getattr__(cls, node: str) -> "Instrument":
        return Instrument([node])


Milliseconds = int


# NOTE: We could track non-uniform tagged metrics and log when one is encountered.
class Instrument(metaclass=InstrumentMeta):
    """An observability instrument for collecting metrics.

    Usage:
    ```python
    class ObserveMe:
        def do_something(self) -> None:
            # Increments the "ics.do_something" stat by 1
            Instrument.ics.do_something.incr(1)

        def set_value(self, value: int) -> None:
            # Sets the gauge's current value
            Instrument.ics.value.gauge(1)

        # Captures the amount of time this method takes
        @Instrument.ics.sync.timer()
        def sync(self) -> None:
            requests.get("example.com/endpoint")

    ```
    """

    def __init__(
        self,
        nodes: list[str],
        tags: dict[str, str] | None = None,
        default_rates: DefaultRate | None = None,
    ) -> None:
        self._nodes = nodes
        self._tags = tags or dict()
        self._default_rates: DefaultRate = default_rates or {}

    def __getattr__(self, node: str) -> "Instrument":
        """Allows dot-chaining instrument nodes to build an instrument."""
        return Instrument(
            nodes=self._nodes + [node],
            tags=self._tags,
            default_rates=self._default_rates,
        )

    def with_default_rate(
        self,
        counter: float | None = None,
        gauge: float | None = None,
        timer: float | None = None,
        distribution: float | None = None,
    ) -> Self:
        """Override the default rates used for this instrument on different data types."""
        if counter is not None:
            self._default_rates["counter"] = counter

        if gauge is not None:
            self._default_rates["gauge"] = gauge

        if timer is not None:
            self._default_rates["timer"] = timer

        if distribution is not None:
            self._default_rates["distribution"] = distribution

        return self

    def tags(self, **tags: str) -> "Instrument":
        """A special method to add tags to the instrument.

        Tags are a way of adding dimensions to telemetries so they can be filtered,
        aggregated, and compared in visualizations.

        WARNING
        *******
        When using tags, they must be consistent across a given metric name,
        otherwise DataDog will create a new metric. This causes rollup reporting errors
        in addition to increasing usage costs.

        Example:
        ```python
        def get_connector(connector_id: str) -> Connector | None:
            instrument = Instrument.integrations.connector.tags(
                connector=connector_id,
            ).fetch
            # Count the total number of calls
            instrument.calls.incr()
            try:
                # get the connector
                connector = ...
            except Exception as exc:
                # Count the total number of errors
                instrument.errors.tags(
                    error_code=exc.__class__.__name__,
                ).incr()
                return None

            return connector
        ```
        """
        self._tags.update(tags)
        return self

    @property
    def _stat_key(self) -> str:
        return ".".join(self._sanitize(node) for node in self._nodes)

    @property
    def _stat_tags(self) -> list[str]:
        return [f"{tag}:{value}" for tag, value in self._tags.items()]

    @cached_property
    def _counter_rate(self) -> float:
        return self._default_rates.get("counter", 1.0)

    @cached_property
    def _gauge_rate(self) -> float:
        return self._default_rates.get("gauge", 1.0)

    @cached_property
    def _timer_rate(self) -> float:
        return self._default_rates.get("timer", 1.0)

    @cached_property
    def _distribution_rate(self) -> float:
        return self._default_rates.get("distribution", 1.0)

    @staticmethod
    def _sanitize(node: str) -> str:
        """Sanitizes a node to a format allowed by statsd."""
        if not node:
            return "_"

        return re.sub(r"[^a-z0-9_]", "_", node.lower())

    def incr(self, count: int = 1, rate: float | None = None) -> None:
        """Increment a stat by `count`."""
        rate = cast(int, rate if rate is not None else self._counter_rate)
        statsd.increment(
            metric=self._stat_key,
            value=count,
            tags=self._stat_tags,
            sample_rate=rate,
        )

    def decr(self, count: int = 1, rate: float | None = None) -> None:
        """Decrement a stat by `count`."""
        rate = cast(int, rate if rate is not None else self._counter_rate)
        statsd.decrement(
            metric=self._stat_key,
            value=count,
            tags=self._stat_tags,
            sample_rate=rate,
        )

    def gauge(self, value: int, rate: float | None = None) -> None:
        """Set a gauge value."""
        rate = cast(int, rate if rate is not None else self._gauge_rate)
        statsd.gauge(
            metric=self._stat_key,
            value=value,
            tags=self._stat_tags,
            sample_rate=rate,
        )

    def timing(self, delta: Milliseconds, rate: float | None = None) -> None:
        """Capture the amount of time some action takes.

        Args:
            delta: The amount of time the action took in ms.
            rate: The rate at which this stat should be recorded.
        """
        rate = cast(int, rate if rate is not None else self._timer_rate)
        statsd.timing(
            metric=self._stat_key,
            value=delta,
            tags=self._stat_tags,
            sample_rate=rate,
        )

    def timer(self, rate: float | None = None) -> TimedContextManagerDecorator:
        """A thread-safe decorator or context manager which reports the
        amount of time some inner action takes.

        Args:
            rate: The rate at which to sample the data.
        """
        rate = cast(int, rate if rate is not None else self._timer_rate)
        return statsd.timed(
            metric=self._stat_key,
            tags=self._stat_tags,
            sample_rate=rate,
        )

    def distribution(self, value: float, rate: float | None = None) -> None:
        """Send a global distribution value, optionally setting a sample rate.

        Args:
            rate: The rate at which to sample the distribution data.
        """
        rate = cast(int, rate if rate is not None else self._distribution_rate)
        statsd.distribution(
            metric=self._stat_key,
            value=value,
            tags=self._stat_tags,
            sample_rate=rate,
        )
