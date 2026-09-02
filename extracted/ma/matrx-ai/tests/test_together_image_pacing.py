import asyncio
from types import SimpleNamespace

import pytest

from matrx_ai.providers import errors
from matrx_ai.providers.together import together_image_api


@pytest.mark.asyncio
async def test_concurrent_together_images_reserve_steady_start_times(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    sleeps: list[float] = []

    async def fake_sleep(delay: float) -> None:
        sleeps.append(delay)

    monkeypatch.setattr(together_image_api.time, "monotonic", lambda: 100.0)
    monkeypatch.setattr(together_image_api.asyncio, "sleep", fake_sleep)
    monkeypatch.setattr(
        together_image_api,
        "TOGETHER_IMAGE_MIN_START_INTERVAL_SECONDS",
        2.0,
    )
    monkeypatch.setattr(together_image_api, "_together_image_next_start_at", 0.0)

    await asyncio.gather(
        together_image_api._pace_together_image_request(),
        together_image_api._pace_together_image_request(),
        together_image_api._pace_together_image_request(),
    )

    assert sleeps == [2.0, 4.0]


@pytest.mark.parametrize(
    ("header", "expected"),
    [
        ("2", 2.0),
        ("2s", 2.0),
        ("850ms", 0.85),
        ("1.5m", 90.0),
    ],
)
def test_together_reset_header_is_used(
    header: str,
    expected: float,
) -> None:
    exception = RuntimeError("rate limited")
    exception.response = SimpleNamespace(headers={"x-ratelimit-reset": header})  # type: ignore[attr-defined]

    assert errors._extract_retry_after(exception) == expected
