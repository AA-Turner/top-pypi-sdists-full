from __future__ import annotations

import asyncio
from types import SimpleNamespace

import pytest

from matrx_ai.providers.admission import (
    admit_provider_call,
    provider_admission_snapshot,
    reset_provider_admission_for_tests,
)
from matrx_ai.providers.errors import RetryableError


def _profile(
    *, initial: int = 3, maximum: int = 8, rpm: int | None = None
) -> SimpleNamespace:
    provider_admission: dict[str, int] = {
        "initial_concurrency": initial,
        "max_concurrency": maximum,
    }
    if rpm is not None:
        provider_admission["requests_per_minute"] = rpm
    return SimpleNamespace(
        endpoint_id="endpoint-openai-platform",
        vendor="openai",
        base_url="https://api.openai.com",
        offering_metadata={"provider_admission": provider_admission},
    )


@pytest.fixture(autouse=True)
def _reset() -> None:
    reset_provider_admission_for_tests()


@pytest.mark.asyncio
async def test_all_callers_dispatch_while_provider_concurrency_is_centralized() -> None:
    profile = _profile(initial=3)
    active = 0
    peak = 0
    release = asyncio.Event()

    async def run() -> None:
        nonlocal active, peak
        async with admit_provider_call(profile):
            active += 1
            peak = max(peak, active)
            await release.wait()
            active -= 1

    tasks = [asyncio.create_task(run()) for _ in range(100)]
    await asyncio.sleep(0.02)

    assert len(tasks) == 100
    assert peak == 3
    assert provider_admission_snapshot()[
        "openai:endpoint-openai-platform:https://api.openai.com"
    ]["active"] == 3

    release.set()
    await asyncio.gather(*tasks)


@pytest.mark.asyncio
async def test_rate_limit_halves_admission_and_honors_retry_after() -> None:
    profile = _profile(initial=8)
    error = RuntimeError("provider refused")
    error.error_info = RetryableError(  # type: ignore[attr-defined]
        error_type="rate_limit",
        message="too many requests",
        status_code=429,
        retry_after=0.03,
    )

    with pytest.raises(RuntimeError, match="provider refused"):
        async with admit_provider_call(profile):
            raise error

    snapshot = provider_admission_snapshot()[
        "openai:endpoint-openai-platform:https://api.openai.com"
    ]
    assert snapshot["current_concurrency"] == 4
    assert 0 < float(snapshot["cooldown_seconds"] or 0) <= 0.03

    entered_at = 0.0
    loop = asyncio.get_running_loop()
    started_at = loop.time()
    async with admit_provider_call(profile):
        entered_at = loop.time()
    assert entered_at - started_at >= 0.02


@pytest.mark.asyncio
async def test_successes_expand_admission_toward_the_configured_ceiling() -> None:
    profile = _profile(initial=2, maximum=4)
    for _ in range(2):
        async with admit_provider_call(profile):
            pass

    snapshot = provider_admission_snapshot()[
        "openai:endpoint-openai-platform:https://api.openai.com"
    ]
    assert snapshot["current_concurrency"] == 3


@pytest.mark.asyncio
async def test_non_rate_limit_failure_does_not_expand_admission() -> None:
    profile = _profile(initial=2, maximum=4)

    with pytest.raises(RuntimeError, match="provider failed"):
        async with admit_provider_call(profile):
            raise RuntimeError("provider failed")

    snapshot = provider_admission_snapshot()[
        "openai:endpoint-openai-platform:https://api.openai.com"
    ]
    assert snapshot["current_concurrency"] == 2
