from __future__ import annotations

from dataclasses import dataclass

import pytest

from matrx_scraper import scraper


@dataclass
class _Response:
    status_code: int
    url: str
    headers: dict[str, str]
    text: str = "ok"
    content: bytes = b"ok"


class _Session:
    def __init__(self, responses: list[_Response]) -> None:
        self.responses = responses
        self.calls: list[tuple[str, bool]] = []

    def __enter__(self):
        return self

    def __exit__(self, *_args) -> None:
        return None

    def get(self, url: str, *, allow_redirects: bool, **_kwargs) -> _Response:
        self.calls.append((url, allow_redirects))
        return self.responses.pop(0)


def test_curl_redirect_chain_is_captured_without_response_history(monkeypatch) -> None:
    session = _Session(
        [
            _Response(301, "https://x/start", {"location": "/middle"}),
            _Response(302, "https://x/middle", {"location": "https://y/final"}),
            _Response(200, "https://y/final", {"content-type": "text/html"}),
        ]
    )
    monkeypatch.setattr(scraper, "CurlCffiSession", lambda **_kwargs: session)

    result = scraper._curl_cffi_get_sync(
        "https://x/start",
        impersonate="chrome",
        headers={},
        proxy=None,
        is_likely_binary=False,
    )

    assert result["redirect_chain"] == [
        {"status": 301, "url": "https://x/start"},
        {"status": 302, "url": "https://x/middle"},
    ]
    assert result["response_url"] == "https://y/final"
    assert session.calls == [
        ("https://x/start", False),
        ("https://x/middle", False),
        ("https://y/final", False),
    ]


def test_curl_redirect_limit_fails_loudly(monkeypatch) -> None:
    session = _Session(
        [_Response(302, f"https://x/{index}", {"location": f"/{index + 1}"}) for index in range(11)]
    )
    monkeypatch.setattr(scraper, "CurlCffiSession", lambda **_kwargs: session)

    with pytest.raises(RuntimeError, match="redirect limit exceeded"):
        scraper._curl_cffi_get_sync(
            "https://x/0",
            impersonate="chrome",
            headers={},
            proxy=None,
            is_likely_binary=False,
        )
