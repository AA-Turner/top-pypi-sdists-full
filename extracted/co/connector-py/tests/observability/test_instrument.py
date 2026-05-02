from typing import Any, TypeAlias
from unittest.mock import MagicMock, patch

import pytest
import pytest_cases
from connector.observability.instrument import Instrument, initialize
from datadog.dogstatsd.base import DogStatsd

OpName: TypeAlias = tuple[str, str]
CallArgs: TypeAlias = dict[str, Any]
StatKey: TypeAlias = str
Case: TypeAlias = tuple[
    Instrument,
    OpName,
    CallArgs,
    CallArgs,
    StatKey,
]


def case_incr_default_rates() -> Case:
    instrument = Instrument.some.key.with_default_rate()
    operation_name = ("incr", "increment")
    call_args = {}
    expected_call_args = {
        "value": 1,
        "tags": [],
        "sample_rate": 1,
    }
    expected_stat_key = "some.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_incr_override_default_rates() -> Case:
    instrument = Instrument.some.key.with_default_rate(
        counter=0.25,
        gauge=0.50,
        timer=0.75,
    )
    operation_name = ("incr", "increment")
    call_args = {}
    expected_call_args = {
        "value": 1,
        "tags": [],
        "sample_rate": 0.25,
    }
    expected_stat_key = "some.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_incr_default_args() -> Case:
    instrument = Instrument.some.tags(connector="connector_id").key
    operation_name = ("incr", "increment")
    call_args = {}
    expected_call_args = {
        "value": 1,
        "tags": ["connector:connector_id"],
        "sample_rate": 1,
    }
    expected_stat_key = "some.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_incr_provide_args() -> Case:
    instrument = Instrument.some.stats.key
    operation_name = ("incr", "increment")
    call_args = {
        "count": 28,
        "rate": 0.7,
    }
    expected_call_args = {
        "value": 28,
        "tags": [],
        "sample_rate": 0.7,
    }
    expected_stat_key = "some.stats.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_decr_override_default_rates() -> Case:
    instrument = Instrument.some.key.with_default_rate(
        counter=0.25,
        gauge=0.50,
        timer=0.75,
    )
    operation_name = ("decr", "decrement")
    call_args = {}
    expected_call_args = {
        "value": 1,
        "tags": [],
        "sample_rate": 0.25,
    }
    expected_stat_key = "some.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_decr_default_args() -> Case:
    instrument = Instrument.some.stats.key
    operation_name = ("decr", "decrement")
    call_args = {}
    expected_call_args = {
        "value": 1,
        "tags": [],
        "sample_rate": 1,
    }
    expected_stat_key = "some.stats.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_decr_provide_args() -> Case:
    instrument = Instrument.some.stats.key
    operation_name = ("decr", "decrement")
    call_args = {
        "count": 28,
        "rate": 0.7,
    }
    expected_call_args = {
        "value": 28,
        "tags": [],
        "sample_rate": 0.7,
    }
    expected_stat_key = "some.stats.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_gauge_override_default_rates() -> Case:
    instrument = Instrument.some.key.with_default_rate(
        counter=0.25,
        gauge=0.50,
        timer=0.75,
    )
    operation_name = ("gauge", "gauge")
    call_args = {
        "value": 42,
    }
    expected_call_args = {
        "value": 42,
        "tags": [],
        "sample_rate": 0.50,
    }
    expected_stat_key = "some.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_gauge_default_args() -> Case:
    instrument = Instrument.some.stats.key
    operation_name = ("gauge", "gauge")
    call_args = {
        "value": 42,
    }
    expected_call_args = {
        "value": 42,
        "tags": [],
        "sample_rate": 1,
    }
    expected_stat_key = "some.stats.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_gauge_provide_args() -> Case:
    instrument = Instrument.some.stats.key
    operation_name = ("gauge", "gauge")
    call_args = {
        "value": 42,
        "rate": 0.01,
    }
    expected_call_args = {
        "value": 42,
        "tags": [],
        "sample_rate": 0.01,
    }
    expected_stat_key = "some.stats.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_timing_override_default_rates() -> Case:
    instrument = Instrument.some.key.with_default_rate(
        counter=0.25,
        gauge=0.50,
        timer=0.75,
    )
    operation_name = ("timing", "timing")
    call_args = {
        "delta": 42,
    }
    expected_call_args = {
        "value": 42,
        "tags": [],
        "sample_rate": 0.75,
    }
    expected_stat_key = "some.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_timing_default_args() -> Case:
    instrument = Instrument.some.stats.key
    operation_name = ("timing", "timing")
    call_args = {
        "delta": 42,
    }
    expected_call_args = {
        "value": 42,
        "tags": [],
        "sample_rate": 1,
    }
    expected_stat_key = "some.stats.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_timing_provide_args() -> Case:
    instrument = Instrument.some.stats.key
    operation_name = ("timing", "timing")
    call_args = {
        "delta": 42,
        "rate": 0.4,
    }
    expected_call_args = {
        "value": 42,
        "tags": [],
        "sample_rate": 0.4,
    }
    expected_stat_key = "some.stats.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_timer_override_default_rates() -> Case:
    instrument = Instrument.some.key.with_default_rate(
        counter=0.25,
        gauge=0.50,
        timer=0.75,
    )
    operation_name = ("timer", "timed")
    call_args = {}
    expected_call_args = {
        "sample_rate": 0.75,
        "tags": [],
    }
    expected_stat_key = "some.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_timer_default_args() -> Case:
    instrument = Instrument.some.stats.key
    operation_name = ("timer", "timed")
    call_args = {}
    expected_call_args = {
        "sample_rate": 1,
        "tags": [],
    }
    expected_stat_key = "some.stats.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_timer_provide_args() -> Case:
    instrument = Instrument.some.stats.key
    operation_name = ("timer", "timed")
    call_args = {
        "rate": 0.4,
    }
    expected_call_args = {
        "sample_rate": 0.4,
        "tags": [],
    }
    expected_stat_key = "some.stats.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_distribution_override_default_rates() -> Case:
    instrument = Instrument.some.key.with_default_rate(
        counter=0.25,
        gauge=0.50,
        timer=0.75,
        distribution=0.85,
    )
    operation_name = ("distribution", "distribution")
    call_args = {
        "value": 42,
    }
    expected_call_args = {
        "value": 42,
        "sample_rate": 0.85,
        "tags": [],
    }
    expected_stat_key = "some.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_distribution_default_args() -> Case:
    instrument = Instrument.some.stats.key
    operation_name = ("distribution", "distribution")
    call_args = {
        "value": 42,
    }
    expected_call_args = {
        "value": 42,
        "sample_rate": 1,
        "tags": [],
    }
    expected_stat_key = "some.stats.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


def case_distribution_provide_args() -> Case:
    instrument = Instrument.some.stats.key
    operation_name = ("distribution", "distribution")
    call_args = {
        "value": 42,
        "rate": 0.4,
    }
    expected_call_args = {
        "value": 42,
        "sample_rate": 0.4,
        "tags": [],
    }
    expected_stat_key = "some.stats.key"
    return (
        instrument,
        operation_name,
        call_args,
        expected_call_args,
        expected_stat_key,
    )


class TestInstrumentMeta:
    """Test the InstrumentMeta metaclass functionality."""

    def test_metaclass_getattr_creates_instrument(self):
        """Test that accessing attributes on the class creates Instrument instances."""
        # Test accessing a single node
        instrument = Instrument.some_node
        assert isinstance(instrument, Instrument)
        assert instrument._nodes == ["some_node"]

    def test_metaclass_getattr_with_multiple_nodes(self):
        """Test that accessing nested attributes creates proper Instrument instances."""
        # This should work through the metaclass
        instrument = Instrument.ics.do_something
        assert isinstance(instrument, Instrument)
        assert instrument._nodes == ["ics", "do_something"]


class TestInstrument:
    """Test the Instrument class functionality."""

    @pytest.fixture
    def mock_stats_client(self):
        """Mock the StatsClient for testing."""
        with patch(
            "connector.observability.instrument.statsd",
            spec=DogStatsd,
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_datadog(self):
        """Mock datadog for testing."""
        with patch(
            "connector.observability.instrument.datadog",
        ) as mock:
            yield mock

    @pytest.fixture
    def mock_logging(self):
        """Mock the logging for testing."""
        with patch(
            "connector.observability.instrument.logging",
        ) as mock:
            yield mock

    @pytest.fixture
    def instrument(self):
        """Create a test Instrument instance."""
        return Instrument(["test", "metric"])

    @pytest_cases.parametrize_with_cases(
        [
            "instrument",
            "operation_name",
            "call_args",
            "expected_call_args",
            "expected_stat_key",
        ],
        cases=[
            ".",
        ],
    )
    def test_instrument(
        self,
        instrument: Instrument,
        operation_name: tuple[str, str],
        call_args: dict[str, Any],
        expected_call_args: dict[str, Any],
        expected_stat_key: str,
        mock_stats_client: MagicMock,
    ) -> None:
        assert instrument._stat_key == expected_stat_key
        instrument_op_name, statsd_op_name = operation_name
        operation = getattr(instrument, instrument_op_name)
        operation(**call_args)

        statsd_op: MagicMock = getattr(
            mock_stats_client,
            statsd_op_name,
        )
        statsd_op.assert_called_once_with(
            metric=instrument._stat_key,
            **expected_call_args,
        )

    def test_instrument_timer(
        self,
        mock_stats_client: MagicMock,
    ) -> None:
        timer = Instrument.some_timed_value.timer()
        mock_stats_client.timed.assert_called_once_with(
            metric="some_timed_value",
            tags=[],
            sample_rate=1,
        )
        assert timer == mock_stats_client.timed()

    def test_initialization_failure(
        self,
        mock_datadog: MagicMock,
        mock_logging: MagicMock,
    ) -> None:
        """Assert that initialization failure does not result in an exception."""
        mock_datadog.initialize.side_effect = (Exception("woof"),)
        initialize()
        mock_logging.getLogger().exception.assert_called_once_with(
            "Failed to initialize datadog.", exc_info=True
        )
