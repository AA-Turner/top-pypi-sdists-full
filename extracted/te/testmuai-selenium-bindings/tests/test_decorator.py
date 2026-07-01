"""Test @testmu_selenium.test decorator."""
import pytest
import logging
from unittest.mock import MagicMock
# Import under alias so pytest does not try to collect the decorator itself
# as a test function (it starts with 'test').
from testmu_selenium._decorator import test as _testmu_test_decorator


def test_decorator_wraps_function():
    @_testmu_test_decorator
    def my_test():
        return "hello"
    assert callable(my_test)
    assert my_test() == "hello"


def test_decorator_preserves_function_name():
    @_testmu_test_decorator
    def my_test_function():
        pass
    assert my_test_function.__name__ == "my_test_function"


def test_decorator_marks_function_as_test():
    @_testmu_test_decorator
    def my_test():
        pass
    assert getattr(my_test, "_testmu_test", False) is True


def test_decorator_propagates_exception():
    @_testmu_test_decorator
    def failing_test():
        raise ValueError("boom")
    with pytest.raises(ValueError, match="boom"):
        failing_test()


def test_decorator_passes_args_through():
    @_testmu_test_decorator
    def my_test(driver):
        return driver
    mock_driver = MagicMock()
    assert my_test(mock_driver) is mock_driver


def test_decorator_logs_lifecycle(caplog):
    @_testmu_test_decorator
    def my_test():
        return "ok"
    with caplog.at_level(logging.INFO):
        my_test()
    # Should log start + pass; specific message format is implementation choice
    assert any("start" in r.message.lower() or "test" in r.message.lower() for r in caplog.records)
