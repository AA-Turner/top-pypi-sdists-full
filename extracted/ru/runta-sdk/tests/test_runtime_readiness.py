from __future__ import annotations

import asyncio
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from runta import AsyncRuntime, Runtime, RuntimeStatus


def readiness_runtime(monkeypatch, *, asynchronous, statuses, request_time=0):
    clock = SimpleNamespace(now=0.0, sleeps=[])
    states = iter(statuses)
    info = SimpleNamespace(id="runtime-readiness", status=RuntimeStatus.CREATING)

    def get_runtime(runtime_id):
        assert runtime_id == info.id
        clock.now += request_time
        info.status = next(states)
        return info

    def sleep(delay):
        clock.sleeps.append(delay)
        clock.now += delay

    monkeypatch.setattr("runta.time.monotonic", lambda: clock.now)
    monkeypatch.setattr(
        "runta._internal.retry.random.uniform", lambda lower, upper: upper
    )
    if asynchronous:
        fetch = AsyncMock(side_effect=get_runtime)
        monkeypatch.setattr("runta.asyncio.sleep", AsyncMock(side_effect=sleep))
        runtime_type = AsyncRuntime
    else:
        fetch = Mock(side_effect=get_runtime)
        monkeypatch.setattr("runta.time.sleep", sleep)
        runtime_type = Runtime
    owner = SimpleNamespace(_http=SimpleNamespace(get_runtime=fetch))
    return runtime_type._from_info(owner, info), clock, fetch


def wait(runtime, **kwargs):
    if isinstance(runtime, AsyncRuntime):
        return asyncio.run(runtime.wait_until_ready(**kwargs))
    return runtime.wait_until_ready(**kwargs)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize(
    ("interval", "expected"),
    [
        (0.5, [0.5, 1, 2, 4, 8, 10, 10, 10, 10]),
        (2, [2, 4, 8, 10, 10, 10, 10, 10, 10]),
        (120, [10] * 9),
        (0, [0] * 9),
    ],
)
def test_readiness_backoff(monkeypatch, asynchronous, interval, expected):
    runtime, clock, fetch = readiness_runtime(
        monkeypatch,
        asynchronous=asynchronous,
        statuses=[RuntimeStatus.CREATING] * 9 + [RuntimeStatus.RUNNING],
    )

    result = wait(runtime, poll_interval=interval, timeout=1000)

    assert result.status == RuntimeStatus.RUNNING
    assert clock.sleeps == expected
    assert fetch.call_count == 10


@pytest.mark.parametrize("asynchronous", [False, True])
def test_readiness_uses_full_jitter(monkeypatch, asynchronous):
    runtime, clock, fetch = readiness_runtime(
        monkeypatch,
        asynchronous=asynchronous,
        statuses=[RuntimeStatus.CREATING] * 9 + [RuntimeStatus.RUNNING],
    )
    sample = Mock(side_effect=lambda lower, upper: upper / 4)
    monkeypatch.setattr("runta._internal.retry.random.uniform", sample)

    assert wait(runtime).status == RuntimeStatus.RUNNING

    assert [call.args for call in sample.call_args_list] == [
        (0.0, bound) for bound in [0.5, 1, 2, 4, 8, 10, 10, 10, 10]
    ]
    assert clock.sleeps == [0.125, 0.25, 0.5, 1, 2, 2.5, 2.5, 2.5, 2.5]
    assert fetch.call_count == 10


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize(("request_time", "expected"), [(0, [0.5, 1, 0.75]), (3, [])])
def test_readiness_timeout_bounds_sleep(
    monkeypatch, asynchronous, request_time, expected
):
    runtime, clock, fetch = readiness_runtime(
        monkeypatch,
        asynchronous=asynchronous,
        statuses=[RuntimeStatus.CREATING] * 3,
        request_time=request_time,
    )

    with pytest.raises(TimeoutError, match="last status: creating"):
        wait(runtime, timeout=2.25)

    assert clock.sleeps == expected
    assert fetch.call_count == (3 if request_time == 0 else 1)


@pytest.mark.parametrize("asynchronous", [False, True])
@pytest.mark.parametrize(
    "status",
    [
        RuntimeStatus.RUNNING,
        RuntimeStatus.ERROR,
        RuntimeStatus.CRASHED,
        RuntimeStatus.DELETING,
    ],
)
def test_readiness_terminal_status_does_not_sleep(monkeypatch, asynchronous, status):
    runtime, clock, fetch = readiness_runtime(
        monkeypatch, asynchronous=asynchronous, statuses=[status]
    )

    if status == RuntimeStatus.RUNNING:
        assert wait(runtime).status == status
    else:
        with pytest.raises(RuntimeError, match=f"entered {status.value} state"):
            wait(runtime)

    assert clock.sleeps == []
    assert fetch.call_count == 1
