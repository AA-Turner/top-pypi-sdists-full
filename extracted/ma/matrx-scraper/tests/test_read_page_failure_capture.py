from __future__ import annotations

from types import SimpleNamespace
from typing import Any

import pytest

from matrx_scraper.features import read_page
from matrx_scraper.scraper import FailureReason


def _failed_response(reason: FailureReason | None) -> SimpleNamespace:
    return SimpleNamespace(
        failed=reason is not None,
        failed_primary_reason=reason,
        content="",
        content_bytes=b"",
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    ("reader_name", "kwargs"),
    [
        ("read_page_mcp_quick", {}),
        ("read_page_mcp_summarized", {"instructions": "summarize"}),
    ],
)
async def test_typed_fetch_failure_is_not_a_system_error(
    monkeypatch: pytest.MonkeyPatch,
    reader_name: str,
    kwargs: dict[str, Any],
) -> None:
    captures: list[tuple[BaseException, str, dict[str, Any]]] = []
    prints: list[dict[str, Any]] = []

    async def fake_fetch(_url: str) -> SimpleNamespace:
        return _failed_response(FailureReason.BAD_STATUS)

    async def fake_capture(exc: BaseException, *, kind: str, **capture_kwargs: Any) -> None:
        captures.append((exc, kind, capture_kwargs))

    monkeypatch.setattr(read_page, "fetch_normally_with_proxy", fake_fetch)
    monkeypatch.setattr(read_page, "capture_error", fake_capture)
    monkeypatch.setattr(read_page, "vcprint", lambda *_args, **print_kwargs: prints.append(print_kwargs))

    result = await getattr(read_page, reader_name)("https://example.com/missing", **kwargs)

    assert result["status"] == "error"
    assert captures == []
    assert prints == [
        {"color": "yellow", "log_level": 30, "stdout": False}
    ]


@pytest.mark.asyncio
async def test_empty_success_response_is_captured_as_empty_content(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    captures: list[tuple[BaseException, dict[str, Any]]] = []

    async def fake_fetch(_url: str) -> SimpleNamespace:
        return _failed_response(None)

    async def fake_capture(exc: BaseException, **kwargs: Any) -> None:
        captures.append((exc, kwargs))

    monkeypatch.setattr(read_page, "fetch_normally_with_proxy", fake_fetch)
    monkeypatch.setattr(read_page, "capture_error", fake_capture)
    monkeypatch.setattr(read_page, "vcprint", lambda *_args, **_kwargs: None)

    await read_page.read_page_mcp_quick("https://example.com/empty")

    assert len(captures) == 1
    exc, capture_kwargs = captures[0]
    assert isinstance(exc, read_page.ReadPageFetchError)
    assert str(exc) == "Page reader fetch completed without usable content"
    assert capture_kwargs["kind"] == "scraper_read_page_empty_content"
    assert capture_kwargs["context"] == {
        "url": "https://example.com/empty",
        "operation": "read_page_mcp_quick",
        "failure_reason": "empty_content",
    }
