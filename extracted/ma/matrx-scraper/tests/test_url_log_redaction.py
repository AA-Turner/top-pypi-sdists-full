"""A caller's URL never reaches a log line carrying its credentials.

Every SSRF gate in this package logs the URL it rejected (a gate that fires
silently teaches nobody it fired) — and the REAL validator's message echoes
that URL again. A caller URL can carry ``user:password@`` or a secret query
parameter (``?api_key=``, a signed ``X-Amz-Signature``), so each log line must
keep the address and lose the secret. Each test drives the real function with
the real validator (a literal private IP is refused before any DNS lookup) and
reads what was actually logged.

Break each one catches: the site logs the raw ``url`` / ``request.url`` / the
validator's raw message instead of passing it through
``utils.proxy.redact_url_secrets``.
"""

from __future__ import annotations

import importlib

import pytest

scrape_router = importlib.import_module("matrx_scraper.api.scrape_router")

# Credentials in userinfo AND in a secret query param; the address is private,
# so every gate refuses it and logs.
LEAKY_URL = "http://acct-7731:s3cr3tPass@10.0.0.5:8080/admin?page=2&api_key=K3YVALUE99"
SECRETS = ("acct-7731", "s3cr3tPass", "K3YVALUE99")
ADDRESS = "10.0.0.5:8080"


@pytest.mark.parametrize(
    ("text", "expected"),
    [
        # userinfo, and a raw "@" inside the password must not leave its tail
        ("http://u:pw@proxy.example:8080/x", "http://***@proxy.example:8080/x"),
        ("http://user:p@ss@proxy.example:8080", "http://***@proxy.example:8080"),
        # secret params lose only their value; other params and the path stay
        (
            "https://cdn.example/a.png?w=10&X-Amz-Signature=abc123&token=t0k#frag",
            "https://cdn.example/a.png?w=10&X-Amz-Signature=***&token=***#frag",
        ),
        ("https://api.example/v1?key=AIzaSECRET", "https://api.example/v1?key=***"),
        # names that merely CONTAIN a secret word are not secrets
        ("https://shop.example/?monkey=1&tokens_left=3", "https://shop.example/?monkey=1&tokens_left=3"),
        # URL embedded in a validator message, quoted by %r
        (
            "URL points to localhost: 'http://a:b@127.0.0.1/?api_key=z'",
            "URL points to localhost: 'http://***@127.0.0.1/?api_key=***'",
        ),
        ("no url here at all", "no url here at all"),
    ],
)
def test_redaction_cuts_credentials_and_keeps_the_address(text: str, expected: str) -> None:
    from matrx_scraper.utils.proxy import redact_url_secrets

    assert redact_url_secrets(text) == expected


def _logged(caplog: pytest.LogCaptureFixture) -> str:
    return "\n".join(record.getMessage() for record in caplog.records)


def _assert_address_kept_secrets_gone(caplog: pytest.LogCaptureFixture) -> None:
    logged = _logged(caplog)
    # Positive control: the rejection IS logged with its address — a site that
    # logs nothing at all must fail here, not pass as "redacted".
    assert ADDRESS in logged, f"the refused address was not logged at all:\n{logged}"
    for secret in SECRETS:
        assert secret not in logged, f"{secret!r} leaked into the log:\n{logged}"


@pytest.mark.asyncio
async def test_session_target_gate_log_keeps_address_but_not_credentials(
    caplog: pytest.LogCaptureFixture,
) -> None:
    from matrx_scraper.ai_browser.url_guard import UnsafeUrlError, guard_target

    caplog.set_level("DEBUG")
    with pytest.raises(UnsafeUrlError):
        await guard_target(LEAKY_URL)
    _assert_address_kept_secrets_gone(caplog)


@pytest.mark.asyncio
async def test_preview_gate_log_keeps_address_but_not_credentials(
    caplog: pytest.LogCaptureFixture,
) -> None:
    from matrx_scraper.preview import quick_preview

    caplog.set_level("DEBUG")
    envelope = await quick_preview(LEAKY_URL)
    assert envelope["ok"] is False
    assert envelope["error"] == "url must be a publicly routable http(s) address"
    _assert_address_kept_secrets_gone(caplog)


def _enable_browser_pool(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_scraper._ext as ext

    monkeypatch.setattr(ext, "has_ext", lambda name: name == "browser_pool")
    monkeypatch.setattr(ext, "get_ext", lambda name: object())


async def _call_page_capture() -> None:
    await scrape_router.page_capture(scrape_router.PageCaptureRequest(url=LEAKY_URL), ctx=None)


async def _call_browser_fetch() -> None:
    await scrape_router.browser_fetch(scrape_router.BrowserFetchRequest(url=LEAKY_URL), ctx=None)


async def _call_browser_inspect() -> None:
    await scrape_router.browser_inspect(
        scrape_router.BrowserInspectRequest(url=LEAKY_URL), ctx=None
    )


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "endpoint",
    [_call_page_capture, _call_browser_fetch, _call_browser_inspect],
    ids=["page-capture", "browser-fetch", "browser-inspect"],
)
async def test_router_rejection_log_keeps_address_but_not_credentials(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture, endpoint
) -> None:
    from fastapi import HTTPException

    _enable_browser_pool(monkeypatch)
    caplog.set_level("DEBUG")
    with pytest.raises(HTTPException) as excinfo:
        await endpoint()
    assert excinfo.value.status_code == 422
    for secret in SECRETS:
        assert secret not in str(excinfo.value.detail)
    _assert_address_kept_secrets_gone(caplog)
