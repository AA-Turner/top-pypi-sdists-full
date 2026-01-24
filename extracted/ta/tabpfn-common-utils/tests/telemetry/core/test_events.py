import pytest
import sys
from datetime import datetime, timezone

from tabpfn_common_utils.telemetry.core.events import (
    BaseTelemetryEvent,
    DatasetEvent,
    FitEvent,
    PingEvent,
    PredictEvent,
    _get_py_version,
    _utc_now,
    _uuid4,
)


class TestUtilityFunctions:
    """Test utility functions in events.py"""

    def test_uuid4_generation(self):
        """Test that _uuid4 generates valid UUID strings"""
        uuid1 = _uuid4()
        uuid2 = _uuid4()

        # Should be different UUIDs
        assert uuid1 != uuid2

        # Should be valid UUID format (36 characters with hyphens)
        assert len(uuid1) == 36
        assert uuid1.count("-") == 4

        # Should be strings
        assert isinstance(uuid1, str)
        assert isinstance(uuid2, str)

    def test_utc_now(self):
        """Test that _utc_now returns current UTC datetime"""
        now = _utc_now()

        # Should be a datetime object
        assert isinstance(now, datetime)

        # Should be timezone aware (UTC)
        assert now.tzinfo == timezone.utc

        # Should be recent (within last minute)
        current_time = datetime.now(timezone.utc)
        time_diff = abs((current_time - now).total_seconds())
        assert time_diff < 60

    def test_get_py_version(self):
        """Test that _get_py_version returns correct Python version"""
        version = _get_py_version()

        # Should be a string
        assert isinstance(version, str)

        # Should be in format "major.minor"
        parts = version.split(".")
        assert len(parts) == 2
        assert parts[0].isdigit()
        assert parts[1].isdigit()


class TestBaseTelemetryEvent:
    """Test BaseTelemetryEvent class"""

    def test_base_event_initialization(self):
        """Test that BaseTelemetryEvent initializes with correct values"""

        # Create a concrete implementation for testing
        class TestEvent(BaseTelemetryEvent):
            @property
            def name(self) -> str:
                return "test_event"

        event = TestEvent()

        # Check that all fields are initialized
        assert isinstance(event.python_version, str)
        assert isinstance(event.tabpfn_version, str)
        assert isinstance(event.timestamp, datetime)

        # Check that python_version matches current version
        version_info = sys.version_info
        expected_py_version = f"{version_info.major}.{version_info.minor}"
        assert event.python_version == expected_py_version

        # Check that timestamp is recent and timezone aware
        assert event.timestamp.tzinfo == timezone.utc
        current_time = datetime.now(timezone.utc)
        time_diff = abs((current_time - event.timestamp).total_seconds())
        assert time_diff < 60

    def test_base_event_source_property(self):
        """Test that source property returns 'sdk'"""

        class TestEvent(BaseTelemetryEvent):
            @property
            def name(self) -> str:
                return "test_event"

        event = TestEvent()
        assert event.source == "sdk"

    def test_base_event_name_property_not_implemented(self):
        """Test that name property raises NotImplementedError"""
        event = BaseTelemetryEvent()

        with pytest.raises(NotImplementedError):
            _ = event.name

    def test_base_event_properties_excludes_name(self):
        """Test that properties method excludes 'name' from the returned dict"""

        class TestEvent(BaseTelemetryEvent):
            @property
            def name(self) -> str:
                return "test_event"

        event = TestEvent()
        props = event.properties

        # Should not contain 'name' key
        assert "name" not in props

        # Should contain other fields
        assert "python_version" in props
        assert "tabpfn_version" in props


class TestDatasetEvent:
    """Test DatasetEvent class"""

    def test_dataset_event_initialization(self):
        """Test DatasetEvent initialization with required parameters"""
        event = DatasetEvent(task="classification", role="train")

        # Check required fields
        assert event.task == "classification"
        assert event.role == "train"
        assert event.name == "dataset"

        # Check default values
        assert event.num_rows == 0
        assert event.num_columns == 0

    def test_dataset_event_with_custom_values(self):
        """Test DatasetEvent with custom values"""
        event = DatasetEvent(
            task="regression", role="test", num_rows=100, num_columns=10
        )

        assert event.task == "regression"
        assert event.role == "test"
        assert event.num_rows == 100
        assert event.num_columns == 10
        assert event.name == "dataset"

    def test_dataset_event_inherits_base_properties(self):
        """Test that DatasetEvent inherits base telemetry properties"""
        event = DatasetEvent(task="classification", role="train")

        # Check inherited properties
        assert isinstance(event.python_version, str)
        assert isinstance(event.tabpfn_version, str)
        assert isinstance(event.timestamp, datetime)
        assert event.source == "sdk"

    def test_dataset_event_properties_method(self):
        """Test DatasetEvent properties method"""
        event = DatasetEvent(
            task="classification", role="train", num_rows=50, num_columns=5
        )

        props = event.properties

        # Should not contain 'name'
        assert "name" not in props

        # Should contain all other fields
        assert props["task"] == "classification"
        assert props["role"] == "train"
        assert props["num_rows"] == 50
        assert props["num_columns"] == 5
        assert "python_version" in props
        assert "tabpfn_version" in props

    def test_dataset_event_task_validation(self):
        """Test that DatasetEvent validates task parameter"""
        # Valid tasks should work
        event1 = DatasetEvent(task="classification", role="train")
        event2 = DatasetEvent(task="regression", role="train")

        assert event1.task == "classification"
        assert event2.task == "regression"

    def test_dataset_event_role_validation(self):
        """Test that DatasetEvent validates role parameter"""
        # Valid roles should work
        event1 = DatasetEvent(task="classification", role="train")
        event2 = DatasetEvent(task="classification", role="test")

        assert event1.role == "train"
        assert event2.role == "test"


class TestFitEvent:
    """Test FitEvent class"""

    def test_fit_event_initialization(self):
        """Test FitEvent initialization"""
        event = FitEvent(task="classification")

        assert event.task == "classification"
        assert event.name == "fit_called"
        assert event.num_rows == 0
        assert event.num_columns == 0
        assert event.duration_ms == -1

    def test_fit_event_with_custom_values(self):
        """Test FitEvent with custom values"""
        event = FitEvent(
            task="regression", num_rows=200, num_columns=15, duration_ms=1500
        )

        assert event.task == "regression"
        assert event.num_rows == 200
        assert event.num_columns == 15
        assert event.duration_ms == 1500

    def test_fit_event_inherits_base_properties(self):
        """Test that FitEvent inherits base telemetry properties"""
        event = FitEvent(task="classification")

        assert isinstance(event.python_version, str)
        assert isinstance(event.tabpfn_version, str)
        assert isinstance(event.timestamp, datetime)
        assert event.source == "sdk"

    def test_fit_event_properties_method(self):
        """Test FitEvent properties method"""
        event = FitEvent(
            task="classification", num_rows=75, num_columns=8, duration_ms=2000
        )

        props = event.properties

        assert "name" not in props
        assert props["task"] == "classification"
        assert props["num_rows"] == 75
        assert props["num_columns"] == 8
        assert props["duration_ms"] == 2000
        assert "python_version" in props
        assert "tabpfn_version" in props


class TestPredictEvent:
    """Test PredictEvent class"""

    def test_predict_event_initialization(self):
        """Test PredictEvent initialization"""
        event = PredictEvent(task="classification")

        assert event.task == "classification"
        assert event.name == "predict_called"
        assert event.num_rows == 0
        assert event.num_columns == 0
        assert event.duration_ms == -1

    def test_predict_event_with_custom_values(self):
        """Test PredictEvent with custom values"""
        event = PredictEvent(
            task="regression", num_rows=300, num_columns=20, duration_ms=800
        )

        assert event.task == "regression"
        assert event.num_rows == 300
        assert event.num_columns == 20
        assert event.duration_ms == 800

    def test_predict_event_inherits_base_properties(self):
        """Test that PredictEvent inherits base telemetry properties"""
        event = PredictEvent(task="classification")

        assert isinstance(event.python_version, str)
        assert isinstance(event.tabpfn_version, str)
        assert isinstance(event.timestamp, datetime)
        assert event.source == "sdk"

    def test_predict_event_properties_method(self):
        """Test PredictEvent properties method"""
        event = PredictEvent(
            task="regression", num_rows=150, num_columns=12, duration_ms=1200
        )

        props = event.properties

        assert "name" not in props
        assert props["task"] == "regression"
        assert props["num_rows"] == 150
        assert props["num_columns"] == 12
        assert props["duration_ms"] == 1200
        assert "python_version" in props
        assert "tabpfn_version" in props


class TestPingEvent:
    """Test PingEvent class"""

    def test_ping_event_initialization(self):
        """Test PingEvent initialization"""
        event = PingEvent()

        assert event.name == "ping"

    def test_ping_event_inherits_base_properties(self):
        """Test that PingEvent inherits base telemetry properties"""
        event = PingEvent()

        assert isinstance(event.python_version, str)
        assert isinstance(event.tabpfn_version, str)
        assert isinstance(event.timestamp, datetime)
        assert event.source == "sdk"

    def test_ping_event_properties_method(self):
        """Test PingEvent properties method"""
        event = PingEvent()

        props = event.properties

        # Should not contain 'name'
        assert "name" not in props
        assert "frequency" in props

        # Should contain base properties
        assert "python_version" in props
        assert "tabpfn_version" in props
        assert "runtime_environment" in props

        # Should be minimal - only base properties
        assert len(props) == 8

    def test_ping_event_minimal_structure(self):
        """Test that PingEvent has minimal structure (no additional fields)"""
        event = PingEvent()

        # Should only have base properties and name
        expected_attrs = {
            "python_version",
            "tabpfn_version",
            "source",
            "name",
            "properties",
            "extension",
            "frequency",
            "runtime_kernel",
            "runtime_environment",
            "platform_os",
        }
        for property in event.properties:
            assert property in expected_attrs


class TestEventIntegration:
    """Integration tests for all event types"""

    def test_all_events_have_consistent_structure(self):
        """Test that all events have consistent base structure"""
        events = [
            DatasetEvent(task="classification", role="train"),
            FitEvent(task="classification"),
            PredictEvent(task="classification"),
            PingEvent(),
        ]

        for event in events:
            # All should have base properties
            assert hasattr(event, "python_version")
            assert hasattr(event, "tabpfn_version")
            assert hasattr(event, "source")
            assert hasattr(event, "name")
            assert hasattr(event, "properties")

            # All should have consistent types
            assert isinstance(event.python_version, str)
            assert isinstance(event.tabpfn_version, str)
            assert isinstance(event.timestamp, datetime)
            assert isinstance(event.source, str)
            assert isinstance(event.name, str)
            assert isinstance(event.properties, dict)

            # Properties should not include 'name'
            assert "name" not in event.properties

    def test_events_serialization_compatibility(self):
        """Test that events can be properly serialized"""
        from dataclasses import asdict

        events = [
            DatasetEvent(
                task="classification", role="train", num_rows=100, num_columns=10
            ),
            FitEvent(task="regression", num_rows=200, num_columns=15, duration_ms=1500),
            PredictEvent(
                task="classification", num_rows=50, num_columns=5, duration_ms=800
            ),
            PingEvent(),
        ]

        for event in events:
            # Should be able to convert to dict
            event_dict = asdict(event)

            # Should contain all expected fields
            assert "python_version" in event_dict
            assert "tabpfn_version" in event_dict

            # Should be able to access properties
            props = event.properties
            assert isinstance(props, dict)
            assert len(props) > 0
