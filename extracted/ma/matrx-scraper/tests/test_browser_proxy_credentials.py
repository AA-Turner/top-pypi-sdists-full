"""The pooled browser must receive credentials in Playwright's actual fields."""
from types import SimpleNamespace
from unittest.mock import AsyncMock, Mock

import pytest

from matrx_scraper.browser_pool import PlaywrightBrowserPool


@pytest.mark.asyncio
async def test_pooled_fetch_preserves_proxy_credentials():
    response = Mock(status=200, all_headers=AsyncMock(return_value={}))
    page = Mock(
        goto=AsyncMock(return_value=response), content=AsyncMock(return_value="ok"),
        title=AsyncMock(return_value="Example"), close=AsyncMock(), url="https://example.com",
    )
    context = Mock(new_page=AsyncMock(return_value=page), close=AsyncMock())
    browser = Mock(new_context=AsyncMock(return_value=context))
    pool = PlaywrightBrowserPool.__new__(PlaywrightBrowserPool)
    pool.acquire = AsyncMock(return_value=browser)
    pool.release = Mock()
    await pool.fetch("https://example.com", proxy="http://account%40team:p%3Ass@proxy.example:33335")
    assert browser.new_context.call_args.kwargs["proxy"] == {
        "server": "http://proxy.example:33335", "username": "account@team", "password": "p:ss",
    }
    context.close.assert_awaited_once()
    pool.release.assert_called_once_with(browser)


@pytest.mark.parametrize(('url', 'expected'), [
    ('http://proxy.example:8080', {'server': 'http://proxy.example:8080'}),
    ('proxy.example:8080', {'server': 'http://proxy.example:8080'}),
    ('http://user:@[2001:db8::1]:8080', {'server': 'http://[2001:db8::1]:8080', 'username': 'user', 'password': ''}),
    ('socks5://proxy.example:1080', {'server': 'socks5://proxy.example:1080'}),
    # A raw "@" inside the password: userinfo ends at the LAST "@". Splitting on
    # the first one leaks "ss@" into the server address Playwright dials.
    ('http://user:p@ss@proxy.example:8080', {'server': 'http://proxy.example:8080', 'username': 'user', 'password': 'p@ss'}),
])
def test_proxy_address_forms(url, expected):
    from matrx_scraper.utils.proxy import playwright_proxy
    assert playwright_proxy(url) == expected


class _RecordingBrowser:
    """Playwright stand-in: records each context's kwargs; pages answer like a loaded page."""

    def __init__(self) -> None:
        self.context_kwargs: list[dict] = []

    async def new_context(self, **kwargs):
        self.context_kwargs.append(kwargs)
        response = SimpleNamespace(
            status=200,
            all_headers=AsyncMock(return_value={}),
            request=SimpleNamespace(redirected_from=None),
        )
        page = SimpleNamespace(
            url="https://example.com/",
            goto=AsyncMock(return_value=response),
            wait_for_load_state=AsyncMock(),
            title=AsyncMock(return_value="Example"),
            content=AsyncMock(return_value="<html><body>ok</body></html>"),
            close=AsyncMock(),
            on=lambda *_args: None,
        )
        return SimpleNamespace(new_page=AsyncMock(return_value=page), close=AsyncMock())


async def _call_fetch(pool, proxy):
    await pool.fetch("https://example.com/", proxy=proxy)


async def _call_fetch_with_capture(pool, proxy):
    await pool.fetch_with_capture("https://example.com/", proxy=proxy)


async def _call_capture_url(pool, proxy):
    await pool.capture_url("https://example.com/", kinds=["desktop_fold"], proxy=proxy)


async def _call_inspect_url(pool, proxy):
    await pool.inspect_url("https://example.com/", proxy=proxy, settle_seconds=0)


@pytest.mark.asyncio
@pytest.mark.parametrize(
    "entry_point",
    [_call_fetch, _call_fetch_with_capture, _call_capture_url, _call_inspect_url],
    ids=["fetch", "fetch_with_capture", "capture_url", "inspect_url"],
)
async def test_every_pooled_entry_point_hands_each_call_its_own_proxy_credentials(
    monkeypatch: pytest.MonkeyPatch, entry_point
) -> None:
    """Each navigation's context must carry THAT call's proxy, split into
    Playwright's fields — never dropped, never another call's credentials,
    never userinfo left in the server address."""

    async def no_screenshots(*_args, **_kwargs):
        return []

    monkeypatch.setattr("matrx_scraper.browser_pool.capture_screenshots", no_screenshots)
    browser = _RecordingBrowser()
    pool = PlaywrightBrowserPool.__new__(PlaywrightBrowserPool)
    pool.acquire = AsyncMock(return_value=browser)
    pool.release = Mock()

    await entry_point(pool, "http://alpha%40team:first%3Apw@proxy-a.example:33335")
    await entry_point(pool, "socks5://beta:second-pw@proxy-b.example:1080")

    assert [kwargs.get("proxy") for kwargs in browser.context_kwargs] == [
        {"server": "http://proxy-a.example:33335", "username": "alpha@team", "password": "first:pw"},
        {"server": "socks5://proxy-b.example:1080", "username": "beta", "password": "second-pw"},
    ]


@pytest.mark.asyncio
async def test_blocked_proxy_log_never_contains_its_credentials(
    caplog: pytest.LogCaptureFixture,
) -> None:
    """A caller-supplied proxy that fails the SSRF gate is logged — the log line
    must name the blocked address but never the account or password."""
    from matrx_scraper.ai_browser.url_guard import UnsafeUrlError, guard_proxy

    caplog.set_level("DEBUG")
    with pytest.raises(UnsafeUrlError, match="proxy must be a publicly routable"):
        await guard_proxy("http://acct-7731:S3cret%21Pass@10.1.2.3:3128")

    logged = "\n".join(record.getMessage() for record in caplog.records)
    assert "10.1.2.3:3128" in logged
    assert "S3cret" not in logged
    assert "acct-7731" not in logged


@pytest.mark.asyncio
async def test_pooled_fetch_waits_for_normal_client_challenge_completion():
    response = Mock(status=200, all_headers=AsyncMock(return_value={}))
    finished = False

    async def title():
        return "" if finished else "Client Challenge"

    async def content():
        return '<html><body><pre>{"query":{"pages":[]}}</pre></body></html>' if finished else '<title>Client Challenge</title>'

    async def wait_for_selector(expression, **kwargs):
        nonlocal finished
        assert expression == 'xpath=//title[normalize-space(.)="Client Challenge"]'
        assert kwargs['state'] == 'detached'
        assert 0 < kwargs['timeout'] <= 30000
        finished = True

    page = Mock(goto=AsyncMock(return_value=response), title=title, content=content,
                wait_for_selector=AsyncMock(side_effect=wait_for_selector),
                wait_for_function=AsyncMock(side_effect=RuntimeError("CSP forbids unsafe-eval")),
                wait_for_load_state=AsyncMock(), close=AsyncMock(),
                url='https://wiki.mozilla.org/api.php')
    context = Mock(new_page=AsyncMock(return_value=page), close=AsyncMock())
    browser = Mock(new_context=AsyncMock(return_value=context))
    pool = PlaywrightBrowserPool.__new__(PlaywrightBrowserPool)
    pool.acquire = AsyncMock(return_value=browser)
    pool.release = Mock()
    html, *_ = await pool.fetch(page.url)
    assert '"query"' in html
    page.wait_for_function.assert_not_awaited()
    page.wait_for_selector.assert_awaited_once()
    page.wait_for_load_state.assert_awaited_once()
    assert page.wait_for_load_state.call_args.args == ("domcontentloaded",)
    assert 0 < page.wait_for_load_state.call_args.kwargs["timeout"] <= page.wait_for_selector.call_args.kwargs["timeout"]
    context.close.assert_awaited_once()


@pytest.mark.asyncio
async def test_challenge_timeout_closes_context_without_returning_challenge_html():
    response = Mock(status=200, all_headers=AsyncMock(return_value={}))
    page = Mock(
        goto=AsyncMock(return_value=response), title=AsyncMock(return_value="Client Challenge"),
        wait_for_selector=AsyncMock(side_effect=TimeoutError("challenge did not finish")),
        wait_for_function=AsyncMock(side_effect=RuntimeError("CSP forbids unsafe-eval")),
        wait_for_load_state=AsyncMock(), content=AsyncMock(), close=AsyncMock(),
        url="https://wiki.mozilla.org/api.php",
    )
    context = Mock(new_page=AsyncMock(return_value=page), close=AsyncMock())
    browser = Mock(new_context=AsyncMock(return_value=context))
    pool = PlaywrightBrowserPool.__new__(PlaywrightBrowserPool)
    pool.acquire = AsyncMock(return_value=browser)
    pool.release = Mock()
    with pytest.raises(TimeoutError, match="challenge did not finish"):
        await pool.fetch(page.url)
    page.content.assert_not_awaited()
    page.wait_for_load_state.assert_not_awaited()
    page.wait_for_function.assert_not_awaited()
    page.close.assert_awaited_once()
    context.close.assert_awaited_once()
    pool.release.assert_called_once_with(browser)


@pytest.mark.asyncio
async def test_false_readiness_never_returns_challenge_as_success():
    page = Mock(
        goto=AsyncMock(return_value=Mock(status=200, all_headers=AsyncMock(return_value={}))),
        title=AsyncMock(return_value="Client Challenge"),
        wait_for_selector=AsyncMock(), wait_for_load_state=AsyncMock(),
        content=AsyncMock(), close=AsyncMock(), url="https://wiki.mozilla.org/api.php",
    )
    context = Mock(new_page=AsyncMock(return_value=page), close=AsyncMock())
    browser = Mock(new_context=AsyncMock(return_value=context))
    pool = PlaywrightBrowserPool.__new__(PlaywrightBrowserPool)
    pool.acquire = AsyncMock(return_value=browser)
    pool.release = Mock()
    with pytest.raises(TimeoutError, match="provider challenge remains"):
        await pool.fetch(page.url)
    page.content.assert_not_awaited()
    page.close.assert_awaited_once()
    context.close.assert_awaited_once()
    pool.release.assert_called_once_with(browser)
