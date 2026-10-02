"""matrx_seo.access — the ONE canonical-access kernel for seo.collection_run.

DEF-12/WS-5: reads call `iam.has_access_for`; lists call `iam.is_discoverable`.
Both host (aidream) and standalone import these two functions directly —
never a creator/org comparison re-implemented per call site.
"""

from __future__ import annotations

import pytest

from matrx_seo import access as access_module


@pytest.mark.asyncio
async def test_collection_run_readable_calls_has_access_for(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_seo.access import collection_run_readable

    calls: list[tuple[object, ...]] = []

    async def fake_call_function(*args: object, **kwargs: object) -> bool:
        calls.append((*args, kwargs))
        return True

    monkeypatch.setattr(access_module, "call_function", fake_call_function)

    assert await collection_run_readable("user-1", "run-1") is True
    assert calls == [
        (
            "matrx_seo",
            "iam",
            "has_access_for",
            "user-1",
            "seo_collection_run",
            "run-1",
            "viewer",
            {"mode": "scalar"},
        )
    ]


@pytest.mark.asyncio
async def test_collection_run_readable_honors_explicit_level(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_seo.access import collection_run_readable

    calls: list[tuple[object, ...]] = []

    async def fake_call_function(*args: object, **kwargs: object) -> bool:
        calls.append((*args, kwargs))
        return True

    monkeypatch.setattr(access_module, "call_function", fake_call_function)

    await collection_run_readable("user-1", "run-1", level="admin")
    assert calls[0][6] == "admin"


@pytest.mark.asyncio
async def test_collection_run_readable_denies_when_kernel_says_no(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_seo.access import collection_run_readable

    async def deny(*_args: object, **_kwargs: object) -> bool:
        return False

    monkeypatch.setattr(access_module, "call_function", deny)
    assert await collection_run_readable("stranger", "run-1") is False


@pytest.mark.asyncio
async def test_collection_run_readable_fails_closed_on_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_seo.access import collection_run_readable

    async def boom(*_args: object, **_kwargs: object) -> bool:
        raise RuntimeError("db hiccup")

    monkeypatch.setattr(access_module, "call_function", boom)
    assert await collection_run_readable("user-1", "run-1") is False


@pytest.mark.asyncio
async def test_collection_run_readable_fails_closed_on_blank_ids() -> None:
    from matrx_seo.access import collection_run_readable

    assert await collection_run_readable(None, "run-1") is False
    assert await collection_run_readable("user-1", "") is False


@pytest.mark.asyncio
async def test_collection_run_discoverable_calls_is_discoverable(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_seo.access import collection_run_discoverable

    calls: list[tuple[object, ...]] = []

    async def fake_call_function(*args: object, **kwargs: object) -> bool:
        calls.append((*args, kwargs))
        return True

    monkeypatch.setattr(access_module, "call_function", fake_call_function)

    assert await collection_run_discoverable("user-1", "run-1") is True
    assert calls == [
        (
            "matrx_seo",
            "iam",
            "is_discoverable",
            "user-1",
            "seo_collection_run",
            "run-1",
            "viewer",
            {"mode": "scalar"},
        )
    ]


@pytest.mark.asyncio
async def test_collection_run_discoverable_fails_closed_on_error(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_seo.access import collection_run_discoverable

    async def boom(*_args: object, **_kwargs: object) -> bool:
        raise RuntimeError("db hiccup")

    monkeypatch.setattr(access_module, "call_function", boom)
    assert await collection_run_discoverable("user-1", "run-1") is False
