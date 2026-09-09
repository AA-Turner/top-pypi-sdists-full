"""The pooled browser must receive credentials in Playwright's actual fields."""
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
])
def test_proxy_address_forms(url, expected):
    from matrx_scraper.utils.proxy import playwright_proxy
    assert playwright_proxy(url) == expected


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
