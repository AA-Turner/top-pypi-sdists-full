# pylint: disable=missing-function-docstring,missing-module-docstring
import inspect
import logging
import os
import pytest

from token_runtime_id import (
    get_runtime_id,
    require_runtime_id,
    runtime_id,
    RuntimeIdException,
    RuntimeIdLogFilter,
)


def test__get_runtime_id__returns_none_when_not_set() -> None:
    assert get_runtime_id() is None


def test__get_runtime_id__returns_value_within_decorated_function() -> None:
    @runtime_id
    def sample_function() -> str | None:
        return get_runtime_id()

    rid = sample_function()

    assert rid is not None
    assert isinstance(rid, str)
    assert len(rid) > 0

def test__runtime_id__without_arguments() -> None:
    @runtime_id()
    def sample_function() -> str | None:
        return get_runtime_id()

    rid = sample_function()

    assert rid is not None
    assert isinstance(rid, str)
    assert len(rid) > 0



def test__get_runtime_id__returns_none_after_decorated_function_exits() -> None:
    @runtime_id
    def sample_function() -> None:
        pass

    sample_function()
    rid = get_runtime_id()
    assert rid is None


def test__require_runtime_id__raises_when_not_set() -> None:
    with pytest.raises(RuntimeIdException, match="RuntimeId is required but it was not set"):
        require_runtime_id()


def test__require_runtime_id__returns_value_when_set() -> None:
    @runtime_id
    def sample_function() -> str:
        return require_runtime_id()

    rid = sample_function()

    assert rid is not None
    assert isinstance(rid, str)
    assert len(rid) > 0


def test__runtime_id__decorator_generates_unique_ids() -> None:
    @runtime_id
    def sample_function() -> str | None:
        return get_runtime_id()

    rid1 = sample_function()
    rid2 = sample_function()

    assert rid1 != rid2


def test__runtime_id__with_process_id_prefix() -> None:
    @runtime_id(prefix_process_id=True)
    def sample_function() -> str | None:
        return get_runtime_id()

    rid = sample_function()
    assert rid is not None
    assert rid.startswith(str(os.getpid()))


def test__runtime_id__without_process_id_prefix() -> None:
    @runtime_id(prefix_process_id=False)
    def sample_function() -> str | None:
        return get_runtime_id()

    rid = sample_function()
    assert rid is not None
    assert str(os.getpid()) not in rid


def test__runtime_id__with_custom_prefix() -> None:
    @runtime_id(prefix="test", prefix_process_id=False)
    def sample_function() -> str | None:
        return get_runtime_id()

    rid = sample_function()

    assert rid is not None
    assert rid.startswith("test:")


def test__runtime_id__with_custom_length() -> None:
    @runtime_id(prefix_process_id=False, length=16)
    def sample_function() -> str | None:
        return get_runtime_id()

    rid = sample_function()

    assert rid is not None
    assert len(rid) == 16


async def test__runtime_id__async_method() -> None:
    @runtime_id(prefix_process_id=False, length=16)
    async def sample_function() -> str | None:
        return get_runtime_id()

    rid = await sample_function()

    assert rid is not None
    assert len(rid) == 16


async def test__runtime_id__async_method__returned_value_is_async_method() -> None:
    @runtime_id(prefix_process_id=False, length=16)
    async def sample_function() -> str | None:
        return get_runtime_id()

    assert inspect.iscoroutinefunction(sample_function)


def test__runtime_id__with_custom_separator() -> None:
    @runtime_id(sep="-", prefix_process_id=True)
    def sample_function() -> str | None:
        return get_runtime_id()

    rid = sample_function()

    assert rid is not None
    assert rid.startswith(f"{str(os.getpid())}-")


def test__runtime_id__nested_calls() -> None:
    @runtime_id
    def inner_function() -> str | None:
        return get_runtime_id()

    @runtime_id
    def outer_function() -> tuple[str | None, str | None]:
        outer_rid = get_runtime_id()
        inner_rid = inner_function()
        return outer_rid, inner_rid

    outer_rid, inner_rid = outer_function()

    assert outer_rid is not None
    assert inner_rid is not None

    assert inner_rid.startswith(outer_rid)
    assert len(inner_rid) > len(outer_rid)


def test__runtime_id__max_depth_exceeded() -> None:
    called = []

    @runtime_id(max_depth=2, prefix_process_id=True)
    def recursive_depth_1() -> None:
        called.append(1)
        recursive_depth_2()

    @runtime_id(max_depth=2, prefix_process_id=True)
    def recursive_depth_2() -> None:
        called.append(2)
        return recursive_depth_3()

    @runtime_id(max_depth=2, prefix_process_id=True)
    def recursive_depth_3() -> None:
        assert False, "This method should not be called"


    with pytest.raises(RuntimeIdException, match="Max depth of 2 is reached"):
        recursive_depth_1()


    assert called == [1, 2]


def test__runtime_id__max_depth_not_exceeded() -> None:
    @runtime_id
    def recursive_depth_1() -> bool:
        return recursive_depth_2()

    @runtime_id
    def recursive_depth_2() -> bool:
        return True


    assert recursive_depth_1()


def test__runtime_id__decorator_preserves_function_metadata() -> None:
    @runtime_id
    def sample_function() -> None:
        """This is a sample function."""

    assert sample_function.__name__ == "sample_function"
    assert sample_function.__doc__ == "This is a sample function."


def test__runtime_id__decorator_with_arguments() -> None:
    @runtime_id
    def function_with_args(a: int, b: str) -> tuple[int, str, str | None]:
        return a, b, get_runtime_id()

    result = function_with_args(42, "test")

    assert result[0] == 42
    assert result[1] == "test"
    assert result[2] is not None


def test__runtime_id__decorator_with_return_value() -> None:
    @runtime_id
    def function_with_return() -> int:
        return 42

    assert 42 == function_with_return()


def test__runtime_id__decorator_with_exception() -> None:
    @runtime_id
    def function_with_error() -> None:
        rid = get_runtime_id()
        assert rid is not None
        raise ValueError("Test error")

    with pytest.raises(ValueError):
        function_with_error()

    assert get_runtime_id() is None


def test__runtime_id__invalid_length() -> None:
    with pytest.raises(ValueError, match="length must be an integer greater than 0"):
        @runtime_id(length=0)
        def sample_function() -> None:
            pass


def test__runtime_id__invalid_max_depth() -> None:
    with pytest.raises(ValueError, match="max_depth must be an integer greater than 0"):
        @runtime_id(max_depth=0)
        def sample_function() -> None:
            pass


def test__runtime_id__invalid_characters() -> None:
    with pytest.raises(ValueError, match="characters must be a non-empty string"):
        @runtime_id(characters="")
        def sample_function() -> None:
            pass


def test__runtime_id__invalid_separator() -> None:
    with pytest.raises(ValueError, match="sep must be a non-empty string"):
        @runtime_id(sep="")
        def sample_function() -> None:
            pass


def test__runtime_id__invalid_prefix() -> None:
    with pytest.raises(ValueError, match="prefix must be None or a non-empty string"):
        @runtime_id(prefix="")
        def sample_function() -> None:
            pass


def test__runtime_id__invalid_prefix_process_id() -> None:
    with pytest.raises(ValueError, match="prefix_process_id must be a boolean"):
        @runtime_id(prefix_process_id="true")  # type: ignore
        def sample_function() -> None:
            pass


def test__runtime_id__with_custom_characters() -> None:
    @runtime_id(prefix_process_id=False, characters="ABC", length=10)
    def sample_function() -> str | None:
        return get_runtime_id()

    rid = sample_function()

    assert rid is not None
    assert all(c in "ABC" for c in rid)


def test__runtime_id__sanity_check_100_unique_values() -> None:
    @runtime_id
    def sample_function() -> str | None:
        return get_runtime_id()

    runtime_ids = set()

    for _ in range(100):
        rid = sample_function()
        assert rid is not None
        runtime_ids.add(rid)

    assert len(runtime_ids) == 100


def test__runtime_id_log_filter__default_attribute_name() -> None:
    log_filter = RuntimeIdLogFilter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test message",
        args=(),
        exc_info=None
    )

    result = log_filter.filter(record)

    assert result is True
    assert hasattr(record, "runtime_id")
    assert record.runtime_id is None  # pylint: disable=no-member


def test__runtime_id_log_filter__custom_attribute_name() -> None:
    log_filter = RuntimeIdLogFilter(record_attr_name="custom_rid")
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test message",
        args=(),
        exc_info=None
    )

    result = log_filter.filter(record)

    assert result is True
    assert hasattr(record, "custom_rid")
    assert record.custom_rid is None  # pylint: disable=no-member


def test__runtime_id_log_filter__with_runtime_id_set() -> None:
    @runtime_id
    def test_with_filter() -> tuple[bool, str | None]:
        log_filter = RuntimeIdLogFilter()
        record = logging.LogRecord(
            name="test",
            level=logging.INFO,
            pathname="",
            lineno=0,
            msg="test message",
            args=(),
            exc_info=None
        )

        result = log_filter.filter(record)
        return result, record.runtime_id  # pylint: disable=no-member

    result, rid = test_with_filter()

    assert result is True
    assert rid is not None
    assert isinstance(rid, str)
    assert len(rid) > 0


def test__runtime_id_log_filter__always_returns_true() -> None:
    log_filter = RuntimeIdLogFilter()
    record = logging.LogRecord(
        name="test",
        level=logging.INFO,
        pathname="",
        lineno=0,
        msg="test message",
        args=(),
        exc_info=None
    )

    assert log_filter.filter(record) is True


def test__runtime_id_log_filter__invalid_attribute_name() -> None:
    with pytest.raises(ValueError, match="record_attr_name must be a valid Python identifier"):
        RuntimeIdLogFilter(record_attr_name="")

    with pytest.raises(ValueError, match="record_attr_name must be a valid Python identifier"):
        RuntimeIdLogFilter(record_attr_name="runtime id")

    with pytest.raises(ValueError, match="record_attr_name must be a valid Python identifier"):
        RuntimeIdLogFilter(record_attr_name="123runtime")

    with pytest.raises(ValueError, match="record_attr_name must be a valid Python identifier"):
        RuntimeIdLogFilter(record_attr_name="runtime-id")
