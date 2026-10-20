from __future__ import annotations

from dataclasses import dataclass

from fixture_origins import allow_fixture_origins
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
    allow_fixture_origins(monkeypatch, "https://x", "https://y")  # stand-in hosts; the engine is stubbed
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
    allow_fixture_origins(monkeypatch, "https://x", "https://y")  # stand-in hosts; the engine is stubbed
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


class _Cookie:
    def __init__(self, name: str, value: str) -> None:
        self.domain, self.name, self.value = "x", name, value


class _Jar:
    def __init__(self) -> None:
        self.jar: list[_Cookie] = []


class _CookieSession(_Session):
    """A session whose responses may set a cookie, like a real cookie-jar client."""

    def __init__(self, responses: list[_Response], sets_cookie_on: set[int]) -> None:
        super().__init__(responses)
        self.cookies = _Jar()
        self.sets_cookie_on = sets_cookie_on

    def get(self, url: str, *, allow_redirects: bool, **_kwargs) -> _Response:
        index = len(self.calls)
        response = super().get(url, allow_redirects=allow_redirects)
        if index in self.sets_cookie_on:
            self.cookies.jar.append(_Cookie("session", f"v{index}"))
        return response


def test_revisiting_the_first_url_after_a_cookie_was_set_is_a_handshake_not_a_loop(
    monkeypatch,
) -> None:
    """ai.google.dev: page -> oauth2authorize -> oauth2callback (sets session) -> page -> 200."""
    allow_fixture_origins(monkeypatch, "https://x")
    session = _CookieSession(
        [
            _Response(302, "https://x/page", {"location": "/auth"}),
            _Response(302, "https://x/auth", {"location": "/callback"}),
            _Response(302, "https://x/callback", {"location": "/page"}),
            _Response(200, "https://x/page", {"content-type": "text/html"}),
        ],
        sets_cookie_on={2},
    )
    monkeypatch.setattr(scraper, "CurlCffiSession", lambda **_kwargs: session)

    result = scraper._curl_cffi_get_sync(
        "https://x/page", impersonate="chrome", headers={}, proxy=None, is_likely_binary=False
    )

    assert result["redirect_loop"] is False
    assert result["status_code"] == 200
    assert result["response_url"] == "https://x/page"


def test_a_revisit_with_nothing_changed_is_still_a_loop(monkeypatch) -> None:
    allow_fixture_origins(monkeypatch, "https://x")
    session = _CookieSession(
        [
            _Response(302, "https://x/a", {"location": "/b"}),
            _Response(302, "https://x/b", {"location": "/a"}),
        ],
        sets_cookie_on=set(),
    )
    monkeypatch.setattr(scraper, "CurlCffiSession", lambda **_kwargs: session)

    result = scraper._curl_cffi_get_sync(
        "https://x/a", impersonate="chrome", headers={}, proxy=None, is_likely_binary=False
    )

    assert result["redirect_loop"] is True
