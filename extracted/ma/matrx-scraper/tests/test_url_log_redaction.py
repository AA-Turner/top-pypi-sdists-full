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
        # Fragments reach logs just as verbatim as queries. Preserve an ordinary
        # anchor and sibling safe parameters while cutting every credential form.
        (
            "https://alice:secret@x.example/a?token=tok&safe=yes#access_token=frag789&panel=overview",
            "https://***@x.example/a?token=***&safe=yes#access_token=***&panel=overview",
        ),
        (
            "https://x.example/#/callback?ACCESS%5ftoken=frag789&safe=yes#summary",
            "https://x.example/#/callback?ACCESS%5ftoken=***&safe=yes#summary",
        ),
        # Semicolons are admitted parameter separators too; a safe value must
        # not consume the secret pair that follows. A percent-encoded semicolon
        # remains literal value data, not a separator.
        (
            "https://x.example/a?safe=one%3Btwo;token=semi-secret&panel=overview#tab=read;access_token=fragment-secret",
            "https://x.example/a?safe=one%3Btwo;token=***&panel=overview#tab=read;access_token=***",
        ),
        (
            "https://x.example/a?safe=yes#section-2",
            "https://x.example/a?safe=yes#section-2",
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
async def test_press_clip_placeholder_log_redacts_userinfo_query_and_fragment_credentials(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture
) -> None:
    """The real PressClip log sink must inherit the canonical fragment redaction.

    This is deliberately a renderer call, not a direct logger assertion: the
    placeholder sweep is the actual path that writes a source URL to PressClip
    logs. Browser collaborators are minimal owned fakes; no network or real
    credentials are involved.
    """
    from types import SimpleNamespace

    from matrx_scraper.press_clip import renderer
    from matrx_scraper.press_clip.logo import LogoResolution
    import matrx_scraper.ai_browser.url_guard as url_guard
    import playwright.async_api as playwright_api

    leaky_url = (
        "https://clip-user:clip-pass@example.test/story?safe=yes;token=query-token&panel=overview"
        "#tab=summary;access_token=fragment-token"
    )
    secrets = ("clip-user", "clip-pass", "query-token", "fragment-token")

    class Page:
        url = leaky_url

        async def goto(self, *_args, **_kwargs):
            return None

        async def wait_for_timeout(self, *_args, **_kwargs):
            return None

        async def evaluate(self, script, *_args):
            if "readMeta" in script:
                return {}
            if "clip(o)" in script:
                return {"removed_placeholders": ["div.ad-slot"], "section_applied": False}
            if "finalSweep" in script:
                return []
            return None

        async def add_style_tag(self, **_kwargs):
            return None

        async def screenshot(self, **_kwargs):
            return b"preview"

        async def pdf(self, **_kwargs):
            return b"pdf"

    class Context:
        async def route(self, *_args, **_kwargs):
            return None

        async def new_page(self):
            return Page()

    class Browser:
        async def new_context(self, **_kwargs):
            return Context()

        async def close(self):
            return None

    class Playwright:
        chromium = SimpleNamespace(launch=lambda **_kwargs: _async(Browser()))

        async def stop(self):
            return None

    async def _async(value):
        return value

    monkeypatch.setattr(playwright_api, "async_playwright", lambda: SimpleNamespace(start=lambda: _async(Playwright())))
    monkeypatch.setattr(url_guard, "guard_target", _async_noop)
    monkeypatch.setattr(url_guard, "install_egress_guard", _async_noop)
    monkeypatch.setattr(renderer, "install_block_route", _async_noop)
    monkeypatch.setattr(renderer, "_scroll_for_lazy_content", _async_noop)
    monkeypatch.setattr(renderer, "rasterize_pdf", lambda _pdf: [b"raster"])

    async def resolve_logo(**_kwargs):
        return LogoResolution("explicit", url="https://logo.example.test/logo.png")

    monkeypatch.setattr(renderer, "resolve_logo", resolve_logo)
    caplog.set_level("INFO", logger="matrx_scraper.press_clip.renderer")

    await renderer.render_clip_document(url=leaky_url, client_name="")

    messages = [record.getMessage() for record in caplog.records if record.getMessage().startswith("press clip ")]
    assert len(messages) == 1, messages
    message = messages[0]
    assert "safe=yes" in message and "panel=overview" in message and "tab=summary" in message
    for secret in secrets:
        assert secret not in message, f"{secret!r} leaked into PressClip logging: {message}"


async def _async_noop(*_args, **_kwargs):
    return None


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


@pytest.mark.asyncio
async def test_preview_gate_log_redacts_secrets_carried_by_the_raised_exception(
    monkeypatch: pytest.MonkeyPatch, caplog: pytest.LogCaptureFixture,
) -> None:
    """The preview SSRF gate (quick_preview's first ``validate_public_http_url``
    call) must redact ``exc`` itself, not only the caller's raw url. The REAL
    validator strips userinfo via ``urlparse`` before building its message, so
    for ``LEAKY_URL`` its exception text never actually contains a secret —
    which is why ``test_preview_gate_log_keeps_address_but_not_credentials``
    (aggregate scan, real validator) cannot tell a redacted ``exc`` from an
    unredacted one: there is nothing to leak either way. Force the validator to
    raise a message that itself carries the credentials, then inspect ONLY
    this gate's own log record (not the whole caplog) so a different,
    already-redacting call site can't accidentally satisfy the assertion."""
    from matrx_scraper import preview as preview_module

    async def _raise_with_embedded_secret(_url: str) -> str:
        raise ValueError(f"blocked target: {LEAKY_URL}")

    monkeypatch.setattr(preview_module, "validate_public_http_url", _raise_with_embedded_secret)
    caplog.set_level("DEBUG")

    envelope = await preview_module.quick_preview(LEAKY_URL)
    assert envelope["ok"] is False

    gate_records = [
        r for r in caplog.records if r.getMessage().startswith("preview BLOCKED target")
    ]
    assert len(gate_records) == 1, (
        f"expected exactly one gate log line, got: {[r.getMessage() for r in caplog.records]}"
    )
    message = gate_records[0].getMessage()
    assert ADDRESS in message, f"the refused address was not logged at all:\n{message}"
    for secret in SECRETS:
        assert secret not in message, f"{secret!r} leaked into the gate's own log line:\n{message}"


def _enable_browser_pool(monkeypatch: pytest.MonkeyPatch) -> None:
    import matrx_scraper._ext as ext

    monkeypatch.setattr(ext, "has_ext", lambda name: name == "browser_pool")
    monkeypatch.setattr(ext, "get_ext", lambda name: object())


async def _call_page_capture() -> None:
    # `/page-capture` is admitted for an organization (it caches a durable
    # parsed page), so the call carries the context the wire installed — the
    # URL rejection under test is what must still happen.
    from types import SimpleNamespace

    await scrape_router.page_capture(
        scrape_router.PageCaptureRequest(url=LEAKY_URL),
        ctx=SimpleNamespace(
            organization_id="7f1d7b9e-3c9a-4a6d-9c3b-2a4b6d8e0f11",
            user_id="",
            auth_type="token",
            is_authenticated=True,
        ),
    )


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
