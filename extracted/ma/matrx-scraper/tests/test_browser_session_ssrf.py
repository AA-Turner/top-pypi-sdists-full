"""SSRF gate on the stateful browser sessions (`/browser/*`) and `/preview`.

These surfaces hand any authenticated caller (or anything holding
ADMIN_API_TOKEN) an arbitrary-URL, JS-executing fetch from INSIDE the scraper
network, so the guards ARE the contract:

  * publicly-routable targets only, and the CORRECTED url is what gets
    navigated — never the raw input;
  * the FINAL address re-validated after the browser follows redirects OR
    after a click/Enter navigates somewhere the pre-gate never saw, with the
    content withheld and the page parked when it isn't public;
  * every reader (html, text, screenshot, DOM, eval, wait) gated independently,
    so no single missed call site re-opens the hole;
  * the rejection reason never echoed — it names the resolved address, which
    would make any caller an internal-network resolution oracle.
"""

from __future__ import annotations

import importlib
from typing import Any

import pytest

actions = importlib.import_module("matrx_scraper.ai_browser.actions")
url_guard = importlib.import_module("matrx_scraper.ai_browser.url_guard")
preview_mod = importlib.import_module("matrx_scraper.preview")

INTERNAL = "http://169.254.169.254/latest/meta-data/"
SECRET = "AWS_SECRET_IN_THE_BODY"
# The resolver's real message names the resolved address. Nothing that reaches
# a caller may contain it.
ORACLE_LEAK = "10.1.2.3"


# ── Fakes ──────────────────────────────────────────────────────────────────


class _Resp:
    def __init__(self, status: int = 200) -> None:
        self.status = status


class FakePage:
    """A Playwright page whose url can be moved out from under the caller."""

    def __init__(self, url: str = "about:blank", *, lands_on: str | None = None) -> None:
        self.url = url
        self._lands_on = lands_on
        self.goto_calls: list[str] = []

    async def goto(self, url: str, **kwargs: Any) -> _Resp:
        self.goto_calls.append(url)
        # `lands_on` models a redirect / DNS rebind: we asked for one address
        # and the browser ended up on another.
        self.url = self._lands_on or url
        self._lands_on = None
        return _Resp()

    async def title(self) -> str:
        return "Internal Title"

    async def inner_text(self, selector: str = "body") -> str:
        return SECRET

    async def content(self) -> str:
        return f"<html><body>{SECRET}</body></html>"

    async def click(self, selector: str, **kwargs: Any) -> None:
        self.url = self._lands_on or self.url
        self._lands_on = None

    async def screenshot(self, **kwargs: Any) -> bytes:
        return b"PNG-OF-INTERNAL-PAGE"

    async def query_selector(self, selector: str) -> Any:
        return None

    async def query_selector_all(self, selector: str) -> list[Any]:
        return []

    async def evaluate(self, expression: Any, *args: Any) -> Any:
        return SECRET

    async def wait_for_selector(self, *args: Any, **kwargs: Any) -> None:
        return None

    async def wait_for_function(self, *args: Any, **kwargs: Any) -> None:
        return None

    async def wait_for_timeout(self, ms: int) -> None:
        return None


class FakeSession:
    def __init__(self, page: FakePage, session_id: str = "sess1") -> None:
        self.session_id = session_id
        self.page = page


class FakeManager:
    def __init__(self, session: FakeSession | None = None) -> None:
        self.session = session
        self.create_calls: list[dict[str, Any]] = []

    async def get(self, session_id: str) -> FakeSession | None:
        return self.session

    async def create(self, **kwargs: Any) -> FakeSession:
        self.create_calls.append(kwargs)
        if self.session is None:
            self.session = FakeSession(FakePage())
        return self.session


def _install_validator(monkeypatch: pytest.MonkeyPatch, allow: set[str]) -> None:
    """Only the URLs in `allow` are 'publicly routable'. Everything else fails
    with a message carrying the resolved address, exactly like the real one."""

    async def fake_validate(url: str) -> str:
        if url not in allow:
            raise ValueError(f"URL host resolves to a non-public IP address: h ({ORACLE_LEAK})")
        return url

    monkeypatch.setattr(url_guard, "validate_public_http_url", fake_validate)
    monkeypatch.setattr(preview_mod, "validate_public_http_url", fake_validate)


def _assert_no_leak(*values: Any) -> None:
    for value in values:
        text = "" if value is None else str(value)
        assert ORACLE_LEAK not in text, f"resolution oracle leaked: {text!r}"
        assert SECRET not in text, f"internal content leaked: {text!r}"


# ── Pre-gate: the requested target ─────────────────────────────────────────


@pytest.mark.asyncio
async def test_navigate_to_internal_address_is_blocked(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_validator(monkeypatch, allow=set())
    page = FakePage()
    mgr = FakeManager(FakeSession(page))

    result = await actions.navigate(INTERNAL, mgr=mgr)

    assert result.success is False
    assert result.error_type == "blocked"
    # Nothing was navigated and no session was minted for a blocked target.
    assert page.goto_calls == []
    assert mgr.create_calls == []
    _assert_no_leak(result.error_message, result.url, result.text_preview)


@pytest.mark.asyncio
async def test_navigate_uses_the_corrected_url_not_the_raw_input(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Validate one thing and fetch another is how these gates get walked around."""
    corrected = "https://example.com/"

    async def fake_validate(url: str) -> str:
        if url in ("example.com", corrected):
            return corrected
        raise ValueError(f"non-public ({ORACLE_LEAK})")

    monkeypatch.setattr(url_guard, "validate_public_http_url", fake_validate)
    page = FakePage()
    mgr = FakeManager(FakeSession(page))

    result = await actions.navigate("example.com", mgr=mgr)

    assert result.success is True
    assert page.goto_calls == [corrected]


@pytest.mark.asyncio
async def test_internal_proxy_is_blocked(monkeypatch: pytest.MonkeyPatch) -> None:
    """A caller-supplied proxy is the same reach with an extra hop."""
    _install_validator(monkeypatch, allow={"https://example.com/"})
    page = FakePage()
    mgr = FakeManager(FakeSession(page))

    result = await actions.navigate(
        "https://example.com/", proxy="http://169.254.169.254:80", mgr=mgr
    )

    assert result.success is False
    assert result.error_type == "blocked"
    assert page.goto_calls == []
    _assert_no_leak(result.error_message)


@pytest.mark.asyncio
async def test_session_manager_create_rejects_an_internal_proxy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Gated in the manager so every caller of create() inherits it — including
    POST /browser/sessions, which never passes a url at all."""
    _install_validator(monkeypatch, allow=set())
    from matrx_scraper.ai_browser.session import BrowserSessionManager

    with pytest.raises(url_guard.UnsafeUrlError):
        await BrowserSessionManager().create(proxy="http://10.1.2.3:3128")


# ── Post-gate: where the browser actually landed ───────────────────────────


@pytest.mark.asyncio
async def test_public_url_redirecting_to_internal_withholds_everything(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    public = "https://evil.example/"
    _install_validator(monkeypatch, allow={public})
    page = FakePage(lands_on=INTERNAL)
    mgr = FakeManager(FakeSession(page))

    result = await actions.navigate(public, extract_text=True, mgr=mgr)

    assert result.success is False
    assert result.error_type == "blocked"
    assert result.text_preview is None
    assert result.title is None
    # The page is PARKED, so a later reader on this session has nothing to read
    # even if it somehow skipped its own gate.
    assert page.url == "about:blank"
    _assert_no_leak(result.error_message, result.url, result.text_preview, result.title)


@pytest.mark.asyncio
async def test_click_navigating_to_internal_is_blocked(monkeypatch: pytest.MonkeyPatch) -> None:
    """A link to an internal host is the cheapest way around a navigate-only gate."""
    _install_validator(monkeypatch, allow={"https://evil.example/"})
    page = FakePage(url="https://evil.example/", lands_on=INTERNAL)
    mgr = FakeManager(FakeSession(page))

    result = await actions.click("sess1", "a#pwn", mgr=mgr)

    assert result.success is False
    assert result.error_type == "blocked"
    assert result.text_preview is None
    assert page.url == "about:blank"
    _assert_no_leak(result.error_message, result.text_preview, result.title)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "call",
    [
        pytest.param(lambda m: actions.get_html("sess1", mgr=m), id="get_html"),
        pytest.param(lambda m: actions.get_text("sess1", mgr=m), id="get_text"),
        pytest.param(lambda m: actions.screenshot("sess1", mgr=m), id="screenshot"),
        pytest.param(lambda m: actions.get_element("sess1", "body", mgr=m), id="get_element"),
        pytest.param(
            lambda m: actions.query_selectors("sess1", ["a"], mgr=m), id="query_selectors"
        ),
        pytest.param(
            lambda m: actions.eval_js(
                "sess1", "document.body.innerText", allow_eval_js=True, mgr=m
            ),
            id="eval_js",
        ),
        pytest.param(lambda m: actions.wait_for("sess1", text="root:x:0", mgr=m), id="wait_for"),
        pytest.param(lambda m: actions.scroll("sess1", mgr=m), id="scroll"),
    ],
)
async def test_every_reader_refuses_a_session_sitting_on_an_internal_page(
    monkeypatch: pytest.MonkeyPatch, call: Any
) -> None:
    """Layer 2: each reader is independently sufficient. A session parked on an
    internal address by any means yields nothing through any of them."""
    _install_validator(monkeypatch, allow=set())
    mgr = FakeManager(FakeSession(FakePage(url=INTERNAL)))

    result = await call(mgr)

    assert result.success is False
    assert result.error_type == "blocked"
    _assert_no_leak(*[getattr(result, f, None) for f in type(result).model_fields])


@pytest.mark.asyncio
async def test_reader_on_a_fresh_session_says_no_page_not_blocked(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """about:blank is not an SSRF hit — it must not read as a security error."""
    _install_validator(monkeypatch, allow=set())
    mgr = FakeManager(FakeSession(FakePage(url="about:blank")))

    result = await actions.get_html("sess1", mgr=mgr)

    assert result.success is False
    assert result.error_type == "validation"
    assert result.html is None


# ── /preview ───────────────────────────────────────────────────────────────


@pytest.mark.asyncio
async def test_preview_blocks_an_internal_target(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_validator(monkeypatch, allow=set())

    async def explode(*args: Any, **kwargs: Any) -> Any:  # pragma: no cover
        raise AssertionError("preview must not fetch a blocked target")

    monkeypatch.setattr(preview_mod, "_fetch_text", explode)
    monkeypatch.setattr(preview_mod, "_take_homepage_screenshot", explode)

    out = await preview_mod.quick_preview(INTERNAL)

    assert out["ok"] is False
    _assert_no_leak(out["error"])


@pytest.mark.asyncio
async def test_preview_discards_a_body_read_off_a_non_public_redirect(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    _install_validator(monkeypatch, allow={"https://evil.example/"})

    class _R:
        status_code = 200
        text = SECRET
        url = INTERNAL  # httpx followed a redirect off the public internet

    class _Client:
        async def get(self, url: str) -> _R:
            return _R()

    fetched = await preview_mod._fetch_text(_Client(), "https://evil.example/")

    assert fetched.status == 0
    assert fetched.text == ""
    # The transport facts are discarded with the body — a check must answer
    # n_a on them, never score a page we refused to read.
    assert fetched.redirect_chain == []
    assert fetched.final_url is None
    assert fetched.response_bytes is None
    assert fetched.response_time_ms is None


# ── Layer 3: EGRESS — the request itself, not the page's address ───────────
#
# The two gates above key on where the PAGE is. Neither can see a request the
# page ISSUES, so on a legitimately-public page this was still open:
#   eval_js("fetch('http://169.254.169.254/latest/meta-data/')...")
# — and so was a public page's own script fetching an internal host and painting
# the response into the DOM, where get_text returns it. `install_egress_guard`
# is the layer that sees those, because it gates the requests themselves.


class FakeRoute:
    """A Playwright route: exactly one of continue_/abort must be called."""

    def __init__(self, url: str) -> None:
        self.request = type("Req", (), {"url": url})()
        self.continued = False
        self.aborted_with: str | None = None

    async def continue_(self) -> None:
        self.continued = True

    async def abort(self, reason: str = "failed") -> None:
        self.aborted_with = reason


class FakeContext:
    def __init__(self) -> None:
        self.handler: Any = None
        self.pattern: str | None = None

    async def route(self, pattern: str, handler: Any) -> None:
        self.pattern = pattern
        self.handler = handler


async def _guarded_context() -> FakeContext:
    context = FakeContext()
    await url_guard.install_egress_guard(context)
    assert context.handler is not None, "the guard installed no route"
    assert context.pattern == "**/*", "the guard must cover every request"
    return context


PUBLIC_PAGE = "https://example.com/"
PUBLIC_ASSET = "https://example.com/app.js"


@pytest.mark.asyncio
async def test_public_page_fetching_an_internal_host_is_aborted(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """THE finding. The page is public and every address gate passes; the
    request it makes is the leak, and only this layer sees it."""
    _install_validator(monkeypatch, allow={PUBLIC_PAGE, PUBLIC_ASSET})
    context = await _guarded_context()

    route = FakeRoute(INTERNAL)
    await context.handler(route)

    assert route.aborted_with == url_guard.BLOCKED_EGRESS_REASON
    assert not route.continued, "an internal-host request reached the network"
    _assert_no_leak(route.aborted_with)


@pytest.mark.asyncio
async def test_ordinary_subresources_still_load(monkeypatch: pytest.MonkeyPatch) -> None:
    """The gate is worthless if it breaks real pages — over-blocking is a
    defect, not extra safety."""
    _install_validator(monkeypatch, allow={PUBLIC_PAGE, PUBLIC_ASSET})
    context = await _guarded_context()

    for url in (PUBLIC_PAGE, PUBLIC_ASSET):
        route = FakeRoute(url)
        await context.handler(route)
        assert route.continued, f"blocked a public request: {url}"
        assert route.aborted_with is None


@pytest.mark.asyncio
async def test_host_verdict_is_memoised_per_context(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Cost control is part of the contract: one DNS resolution per unique
    host for the life of the context, not one per request. A page pulling 80
    subresources off one host must not pay 80 lookups."""
    calls: list[str] = []

    async def counting_validate(url: str) -> str:
        calls.append(url)
        if url.startswith("https://example.com"):
            return url
        raise ValueError(f"URL host resolves to a non-public IP address: h ({ORACLE_LEAK})")

    monkeypatch.setattr(url_guard, "validate_public_http_url", counting_validate)
    context = await _guarded_context()

    for i in range(25):
        route = FakeRoute(f"https://example.com/asset-{i}.png")
        await context.handler(route)
        assert route.continued
    for i in range(25):
        route = FakeRoute(f"{INTERNAL}?probe={i}")
        await context.handler(route)
        assert route.aborted_with == url_guard.BLOCKED_EGRESS_REASON

    assert len(calls) == 2, (
        f"expected one resolution per unique host (2), got {len(calls)} — "
        "the memo is broken and every subresource now pays for DNS"
    )


@pytest.mark.asyncio
async def test_non_network_schemes_pass_without_resolution(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """data:/blob: fetch nothing off the network — resolving them would be
    pure cost and would break inline assets."""
    calls: list[str] = []

    async def counting_validate(url: str) -> str:
        calls.append(url)
        return url

    monkeypatch.setattr(url_guard, "validate_public_http_url", counting_validate)
    context = await _guarded_context()

    for url in ("data:image/png;base64,iVBORw0KGgo=", "blob:https://example.com/abc"):
        route = FakeRoute(url)
        await context.handler(route)
        assert route.continued, f"blocked a non-network scheme: {url}"
    assert calls == [], "a non-network scheme was sent to the resolver"


@pytest.mark.asyncio
async def test_guard_failure_aborts_rather_than_allowing(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A bug in OUR handler must not become an accidental allow, and must not
    hang the page on an unanswered route."""

    async def exploding_validate(url: str) -> str:
        raise RuntimeError("resolver blew up in a way we did not anticipate")

    monkeypatch.setattr(url_guard, "validate_public_http_url", exploding_validate)
    context = await _guarded_context()

    route = FakeRoute(PUBLIC_PAGE)
    await context.handler(route)
    assert route.aborted_with == url_guard.BLOCKED_EGRESS_REASON
    assert not route.continued


@pytest.mark.asyncio
async def test_a_url_with_no_host_is_not_public(monkeypatch: pytest.MonkeyPatch) -> None:
    _install_validator(monkeypatch, allow={PUBLIC_PAGE})
    context = await _guarded_context()
    route = FakeRoute("http:///nohost")
    await context.handler(route)
    assert route.aborted_with == url_guard.BLOCKED_EGRESS_REASON


def test_every_js_capable_context_installs_the_egress_guard() -> None:
    """Structural pin. The guard only works where it is INSTALLED, and both
    call sites are one easily-deleted line. `session.py` covers every
    ai_browser session (the eval_js surface); `preview.py` covers the
    screenshot render of an arbitrary caller URL.

    The crawler's browser pool is deliberately NOT here — it runs no
    caller-supplied JS, and a Python callback in front of every subresource of
    every crawl is a real cost on the hottest path. Widening it is a measured
    decision, not a reflex.
    """
    import inspect

    session_mod = importlib.import_module("matrx_scraper.ai_browser.session")
    session_src = inspect.getsource(session_mod.BrowserSessionManager.create)
    assert "install_egress_guard(context)" in session_src, (
        "browser sessions no longer install the egress guard — eval_js can "
        "reach internal hosts again"
    )
    preview_src = inspect.getsource(preview_mod._take_homepage_screenshot)
    assert "install_egress_guard(ctx)" in preview_src, (
        "/preview no longer installs the egress guard"
    )
