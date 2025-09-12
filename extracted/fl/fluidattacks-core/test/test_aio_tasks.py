"""Tests for fluidattacks_core.aio.tasks module."""

import asyncio
from collections.abc import AsyncGenerator
from typing import Any

import pytest

from fluidattacks_core.aio.tasks import merge_async_generators


async def async_generator(items: list[Any]) -> AsyncGenerator[Any, None]:
    """Create an async generator from a list of items."""
    for item in items:
        yield item


async def slow_async_generator(items: list[Any], delay: float = 0.1) -> AsyncGenerator[Any, None]:
    """Create a slow async generator for testing timing."""
    for item in items:
        await asyncio.sleep(delay)
        yield item


async def error_async_generator(
    items: list[Any],
    error_at: int | None = None,
) -> AsyncGenerator[Any, None]:
    """Create an async generator that raises an error."""
    for i, item in enumerate(items):
        if error_at is not None and i == error_at:
            raise ValueError(f"Error at index {i}")
        yield item


@pytest.mark.asyncio
async def test_merge_single_generator() -> None:
    """Test merging a single generator."""
    gen = async_generator([1, 2, 3])
    result = []
    async for item in merge_async_generators([gen], limit=1):
        result.append(item)  # noqa: PERF401
    assert result == [1, 2, 3]


@pytest.mark.asyncio
async def test_merge_multiple_generators() -> None:
    """Test merging multiple generators."""
    gens = [
        async_generator([1, 2]),
        async_generator([3, 4]),
        async_generator([5, 6]),
    ]
    result = []
    async for item in merge_async_generators(gens, limit=3):
        result.append(item)  # noqa: PERF401
    # Order may vary due to concurrency, so we sort for comparison
    assert sorted(result) == [1, 2, 3, 4, 5, 6]


@pytest.mark.asyncio
async def test_merge_with_concurrency_limit() -> None:
    """Test merging with concurrency limit smaller than number of generators."""
    gens = [
        slow_async_generator([1, 2], delay=0.1),
        slow_async_generator([3, 4], delay=0.1),
        slow_async_generator([5, 6], delay=0.1),
    ]
    result = []
    async for item in merge_async_generators(gens, limit=2):
        result.append(item)  # noqa: PERF401
    # Should have all items, but order may vary
    assert len(result) == 6
    assert set(result) == {1, 2, 3, 4, 5, 6}


@pytest.mark.asyncio
async def test_merge_empty_generators() -> None:
    """Test merging empty generators."""
    gens = [async_generator([]), async_generator([])]
    result = []
    async for item in merge_async_generators(gens, limit=2):
        result.append(item)  # noqa: PERF401
    assert result == []


@pytest.mark.asyncio
async def test_merge_mixed_length_generators() -> None:
    """Test merging generators of different lengths."""
    gens = [
        async_generator([1, 2, 3, 4]),
        async_generator([5]),
        async_generator([6, 7]),
    ]
    result = []
    async for item in merge_async_generators(gens, limit=3):
        result.append(item)  # noqa: PERF401
    assert len(result) == 7
    assert set(result) == {1, 2, 3, 4, 5, 6, 7}


@pytest.mark.asyncio
async def test_merge_with_generator_error() -> None:
    """Test merging when one generator raises an error."""
    gens = [
        async_generator([1, 2]),
        error_async_generator([3, 4], error_at=1),  # Will error on second item
        async_generator([5, 6]),
    ]
    result = []
    async for item in merge_async_generators(gens, limit=3):
        result.append(item)  # noqa: PERF401
    # Should still get items from other generators
    assert len(result) >= 4  # At least 1,2,3,5,6 (4 might be missing due to error)
    assert 1 in result
    assert 2 in result
    assert 5 in result
    assert 6 in result


@pytest.mark.asyncio
async def test_merge_with_invalid_limit() -> None:
    """Test that invalid limit raises ValueError."""
    gen = async_generator([1, 2, 3])
    with pytest.raises(ValueError, match="limit must be at least 1"):
        async for _ in merge_async_generators([gen], limit=0):
            pass


@pytest.mark.asyncio
async def test_merge_with_zero_limit() -> None:
    """Test that zero limit raises ValueError."""
    gen = async_generator([1, 2, 3])
    with pytest.raises(ValueError, match="limit must be at least 1"):
        async for _ in merge_async_generators([gen], limit=0):
            pass


@pytest.mark.asyncio
async def test_merge_with_negative_limit() -> None:
    """Test that negative limit raises ValueError."""
    gen = async_generator([1, 2, 3])
    with pytest.raises(ValueError, match="limit must be at least 1"):
        async for _ in merge_async_generators([gen], limit=-1):
            pass


@pytest.mark.asyncio
async def test_merge_large_number_of_generators() -> None:
    """Test merging a large number of generators with small limit."""
    gens = [async_generator([i]) for i in range(100)]
    result = []
    async for item in merge_async_generators(gens, limit=5):
        result.append(item)  # noqa: PERF401
    assert len(result) == 100
    assert set(result) == set(range(100))


@pytest.mark.asyncio
async def test_merge_generators_with_different_types() -> None:
    """Test merging generators with different data types."""
    gens = [
        async_generator(["a", "b"]),
        async_generator([1, 2]),
        async_generator([True, False]),
    ]
    result = []
    async for item in merge_async_generators(gens, limit=3):
        result.append(item)  # noqa: PERF401
    assert len(result) == 6
    assert "a" in result
    assert "b" in result
    assert 1 in result
    assert 2 in result
    assert True in result
    assert False in result


@pytest.mark.asyncio
async def test_merge_generators_cleanup_on_exception() -> None:
    """Test that generators are properly cleaned up when an exception occurs."""

    async def failing_consumer() -> AsyncGenerator[Any, None]:
        async for item in merge_async_generators([async_generator([1, 2])], limit=1):
            if item == 1:
                raise RuntimeError("Test exception")
            yield item

    with pytest.raises(RuntimeError, match="Test exception"):
        async for _ in failing_consumer():
            pass
