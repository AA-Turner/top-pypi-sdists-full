"""Tests for CIPlatformProvider new scheduler-related methods."""

import pytest

from tests.unit.cli.ci.provider.test_ciplatformprovider import _ConcreteProvider


class TestDispatchWorkflowDefault:
    """Tests that the default dispatch_workflow raises NotImplementedError."""

    def test_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement dispatch_workflow"):
            provider.dispatch_workflow("test.yml", {"key": "value"})


class TestGetVariableDefault:
    """Tests that the default get_variable raises NotImplementedError."""

    def test_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_variable"):
            provider.get_variable("MY_VAR")


class TestSetVariableDefault:
    """Tests that the default set_variable raises NotImplementedError."""

    def test_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement set_variable"):
            provider.set_variable("MY_VAR", "my_value")


class TestValidateVariableTokenDefault:
    """Tests that the default validate_variable_token raises NotImplementedError."""

    def test_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement validate_variable_token"):
            provider.validate_variable_token()


class TestGetRecentDispatchHistoryDefault:
    """Tests that the default get_recent_dispatch_history raises NotImplementedError."""

    def test_raises_not_implemented(self) -> None:
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement get_recent_dispatch_history"):
            provider.get_recent_dispatch_history("ai-pr-loop.yml")
