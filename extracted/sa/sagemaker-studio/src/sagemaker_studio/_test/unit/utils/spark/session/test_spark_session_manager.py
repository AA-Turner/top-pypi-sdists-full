"""
Unit tests for SparkSessionManager.

This module tests the abstract base class for Spark session providers.
"""

import sys
import types
from abc import ABC
from unittest.mock import Mock

import pytest
from botocore.config import Config

# Snapshot `sys.modules` so the stand-ins installed below can be taken back out.
_modules_before = dict(sys.modules)

# Mock PySpark and gRPC modules before importing our code
pyspark_modules = [
    "pyspark",
    "pyspark.sql",
    "pyspark.sql.session",
    "pyspark.sql.connect",
    "pyspark.sql.connect.session",
    "pyspark.sql.connect.client",
    "grpc",
]

for module_name in pyspark_modules:
    if module_name not in sys.modules:
        mock_module = Mock()
        if module_name == "grpc":
            # Mock gRPC specific classes and functions
            mock_module.insecure_channel = Mock()
            mock_module.secure_channel = Mock()
            mock_module.UnaryUnaryClientInterceptor = Mock()
        sys.modules[module_name] = mock_module

from sagemaker_studio.utils.spark.session.spark_session_manager import (  # noqa: E402
    SparkSessionManager,
)

# Put `sys.modules` back as this module found it. The stand-ins above are needed
# only for the import that just happened; pytest imports every test module during
# COLLECTION, so one left installed here stays installed for the rest of the
# session and silently changes what every later test imports.
_stand_in_names = {
    _name
    for _name, _module in sys.modules.items()
    if not isinstance(_module, types.ModuleType) and _module is not _modules_before.get(_name)
}
for _name in list(sys.modules):
    if _name in _modules_before:
        if sys.modules[_name] is not _modules_before[_name]:
            sys.modules[_name] = _modules_before[_name]
    elif _name in _stand_in_names or any(
        _name.startswith(_root + ".") for _root in _stand_in_names
    ):
        # A stand-in, or something imported UNDER one. A real submodule reached
        # through a mocked parent is registered without the parent ever gaining the
        # attribute, so a later import of it fails ("cannot import name ...").
        # Drop both kinds so the next importer builds a clean one.
        del sys.modules[_name]


class TestSparkSessionManager:
    """Test cases for SparkSessionManager abstract base class."""

    def test_is_abstract_base_class(self):
        """Test that SparkSessionManager is an abstract base class."""
        assert issubclass(SparkSessionManager, ABC)

    def test_cannot_instantiate_directly(self):
        """Test that SparkSessionManager cannot be instantiated directly."""
        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            SparkSessionManager()

    def test_create_method_is_abstract(self):
        """Test that create method is abstract."""
        # Check that create is in the abstract methods
        assert "create" in SparkSessionManager.__abstractmethods__

    def test_stop_method_is_abstract(self):
        """Test that stop method is abstract."""
        # Check that stop is in the abstract methods
        assert "stop" in SparkSessionManager.__abstractmethods__

    def test_concrete_implementation_can_be_instantiated(self):
        """Test that concrete implementations can be instantiated."""

        class ConcreteSparkSessionManager(SparkSessionManager):
            def create(self):
                return "mock_session"

            def stop(self):
                pass

            def get_session_id(self):
                return "session_id"

        # Should be able to instantiate concrete implementation
        manager = ConcreteSparkSessionManager()
        assert isinstance(manager, SparkSessionManager)
        assert manager.create() == "mock_session"
        assert manager.get_session_id() == "session_id"
        manager.stop()  # Should not raise

    def test_partial_implementation_cannot_be_instantiated(self):
        """Test that partial implementations cannot be instantiated."""

        class PartialSparkSessionManager(SparkSessionManager):
            def create(self):
                return "mock_session"

            # Missing stop method implementation

        with pytest.raises(TypeError, match="Can't instantiate abstract class"):
            PartialSparkSessionManager()

    def test_interface_contract(self):
        """Test that the interface contract is properly defined."""

        class TestSparkSessionManager(SparkSessionManager):
            def create(self):
                return "test_session"

            def stop(self):
                return "stopped"

            def get_session_id(self):
                return "session_id"

        manager = TestSparkSessionManager()

        # Test that methods can be called and return expected types
        session = manager.create()
        assert session == "test_session"

        result = manager.stop()
        assert result == "stopped"

        result = manager.get_session_id()
        assert result == "session_id"

    def test_set_user_spark_conf(self):
        """Test that set_user_spark_conf stores user configs."""

        class ConcreteManager(SparkSessionManager):
            def create(self):
                pass

            def stop(self):
                pass

            def get_session_id(self):
                pass

        manager = ConcreteManager()
        assert manager._user_spark_conf is None

        manager.set_user_spark_conf({"spark.key": "val"})
        assert manager._user_spark_conf == {"spark.key": "val"}

    def test_set_user_spark_conf_to_none(self):
        """Test that set_user_spark_conf can clear user configs."""

        class ConcreteManager(SparkSessionManager):
            def create(self):
                pass

            def stop(self):
                pass

            def get_session_id(self):
                pass

        manager = ConcreteManager()
        manager.set_user_spark_conf({"spark.key": "val"})
        manager.set_user_spark_conf(None)
        assert manager._user_spark_conf is None

    def test_user_spark_conf_default_is_none(self):
        """Test that _user_spark_conf defaults to None on all instances."""

        class ConcreteManager(SparkSessionManager):
            def create(self):
                pass

            def stop(self):
                pass

            def get_session_id(self):
                pass

        mgr1 = ConcreteManager()
        mgr2 = ConcreteManager()
        mgr1.set_user_spark_conf({"spark.a": "1"})
        assert mgr2._user_spark_conf is None

    def test_client_retry_config_defaults(self):
        """_client_retry_config() returns adaptive retries with max_attempts=5."""
        cfg = SparkSessionManager._client_retry_config()
        assert isinstance(cfg, Config)
        assert cfg.retries == {"max_attempts": 5, "mode": "adaptive"}

    def test_client_retry_config_merges_and_preserves_base(self):
        """When given a base Config, retry settings are applied while base settings persist."""
        base = Config(read_timeout=99, connect_timeout=7)
        merged = SparkSessionManager._client_retry_config(base)

        # Retry policy applied
        assert merged.retries == {"max_attempts": 5, "mode": "adaptive"}
        # Pre-existing (e.g. endpoint/service-model) settings preserved
        assert merged.read_timeout == 99
        assert merged.connect_timeout == 7
        # Base config is not mutated in place
        assert base.retries is None

    def test_client_retry_config_available_to_subclasses(self):
        """Concrete managers inherit the shared retry-config helper."""

        class ConcreteManager(SparkSessionManager):
            def create(self):
                pass

            def stop(self):
                pass

            def get_session_id(self):
                pass

        assert ConcreteManager()._client_retry_config().retries["mode"] == "adaptive"
