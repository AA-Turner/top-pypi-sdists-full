from __future__ import annotations

import pytest

from matrx_scraper import browser_pool as browser_pool_module
from matrx_scraper.browser_pool import PlaywrightBrowserPool, capture_screenshots
from matrx_scraper.crawler import SiteCrawlerConfig


@pytest.mark.asyncio
async def test_pool_disables_playwrights_unbounded_font_gate_before_driver_start(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: list[str | None] = []

    class FakeBrowser:
        async def close(self) -> None:
            return None

    class FakeChromium:
        async def launch(self, *, headless: bool) -> FakeBrowser:
            assert headless is True
            return FakeBrowser()

    class FakePlaywright:
        chromium = FakeChromium()

        async def stop(self) -> None:
            return None

    class FakeStarter:
        async def start(self) -> FakePlaywright:
            observed.append(
                browser_pool_module.os.environ.get(
                    browser_pool_module.PLAYWRIGHT_SKIP_FONT_READY_ENV
                )
            )
            return FakePlaywright()

    monkeypatch.delenv(browser_pool_module.PLAYWRIGHT_SKIP_FONT_READY_ENV, raising=False)
    monkeypatch.setattr(browser_pool_module, "async_playwright", lambda: FakeStarter())

    pool = PlaywrightBrowserPool(pool_size=1)
    await pool.start()
    await pool.stop()

    assert observed == ["1"]


@pytest.mark.asyncio
async def test_capture_uses_commit_then_bounded_dom_settle() -> None:
    calls: list[tuple[str, object]] = []

    class FakeResponse:
        status = 200

        async def all_headers(self) -> dict[str, str]:
            return {"content-type": "text/html"}

    class FakePage:
        url = "https://example.com/"

        async def goto(self, url: str, **kwargs: object) -> FakeResponse:
            calls.append(("goto", kwargs))
            return FakeResponse()

        async def wait_for_load_state(self, state: str, **kwargs: object) -> None:
            calls.append((state, kwargs))
            raise browser_pool_module.PlaywrightTimeoutError("slow DOM")

        async def title(self) -> str:
            return "Example"

        async def content(self) -> str:
            return "<html><title>Example</title></html>"

        async def close(self) -> None:
            return None

    class FakeContext:
        async def new_page(self) -> FakePage:
            return FakePage()

        async def close(self) -> None:
            return None

    class FakeBrowser:
        async def new_context(self, **kwargs: object) -> FakeContext:
            return FakeContext()

    pool = PlaywrightBrowserPool.__new__(PlaywrightBrowserPool)

    async def acquire(*, timeout: float = 30.0) -> FakeBrowser:  # noqa: ASYNC109
        assert timeout == 45.5
        return FakeBrowser()

    pool.acquire = acquire  # type: ignore[method-assign]
    pool.release = lambda browser: None  # type: ignore[method-assign]

    result = await pool.fetch_with_capture(
        "https://example.com",
        timeout_ms=8_000,
        settle_timeout_ms=2_500,
    )

    assert result.status_code == 200
    assert calls == [
        ("goto", {"timeout": 8_000, "wait_until": "commit"}),
        ("domcontentloaded", {"timeout": 2_500}),
    ]


def test_browser_capture_timeouts_are_configurable() -> None:
    config = SiteCrawlerConfig(
        base_url="https://example.com",
        browser_navigation_timeout_ms=8_000,
        browser_settle_timeout_ms=2_500,
    )
    assert config.browser_navigation_timeout_ms == 8_000
    assert config.browser_settle_timeout_ms == 2_500


async def _no_sleep() -> None:
    return None


@pytest.mark.asyncio
async def test_mixed_device_kinds_navigate_once_per_device_profile(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """A mobile screenshot requires a mobile-emulated LOAD, not a resize.

    This replaces a test that asserted the opposite ("full page capture always
    uses desktop viewport"), which pinned a real defect: resizing the viewport
    after a desktop load leaves the desktop UA, is_mobile=False, has_touch=False
    and device_scale_factor=1, so UA-sniffing sites serve the desktop site and
    the capture is not what a phone renders.
    """
    contexts: list[dict[str, object]] = []
    resizes: list[dict[str, int]] = []

    class FakeResponse:
        status = 200

        async def all_headers(self) -> dict[str, str]:
            return {"content-type": "text/html"}

    class FakePage:
        url = "https://example.com/"

        async def goto(self, url: str, **kwargs: object) -> FakeResponse:
            return FakeResponse()

        async def wait_for_load_state(self, state: str, **kwargs: object) -> None:
            return None

        async def title(self) -> str:
            return "Example"

        async def content(self) -> str:
            return "<html></html>"

        async def set_viewport_size(self, viewport: dict[str, int]) -> None:
            resizes.append(viewport)

        async def evaluate(self, expression: str) -> None:
            return None

        async def screenshot(self, **kwargs: object) -> bytes:
            return b"PNG"

        async def close(self) -> None:
            return None

    class FakeContext:
        async def new_page(self) -> FakePage:
            return FakePage()

        async def close(self) -> None:
            return None

    class FakeBrowser:
        async def new_context(self, **kwargs: object) -> FakeContext:
            contexts.append(kwargs)
            return FakeContext()

    pool = PlaywrightBrowserPool.__new__(PlaywrightBrowserPool)

    async def acquire(*, timeout: float = 30.0) -> FakeBrowser:  # noqa: ASYNC109
        return FakeBrowser()

    pool.acquire = acquire  # type: ignore[method-assign]
    pool.release = lambda browser: None  # type: ignore[method-assign]
    monkeypatch.setattr(browser_pool_module, "png_dimensions", lambda png: (1366, 2400))
    monkeypatch.setattr(browser_pool_module.asyncio, "sleep", lambda seconds: _no_sleep())

    result = await pool.fetch_with_capture(
        "https://example.com",
        screenshot_kinds=["full_page", "viewport_mobile"],
        settle_timeout_ms=1,
    )

    assert len(contexts) == 2, "desktop and mobile must be separate navigations"
    desktop, mobile = contexts[0], contexts[1]
    assert desktop["is_mobile"] is False
    assert desktop["viewport"] == {"width": 1440, "height": 900}
    assert mobile["is_mobile"] is True
    assert mobile["has_touch"] is True
    assert mobile["device_scale_factor"] == 3
    assert mobile["viewport"] == {"width": 390, "height": 844}
    assert "iPhone" in str(mobile["user_agent"])
    assert "iPhone" not in str(desktop["user_agent"])

    assert resizes == [], "viewport must come from device emulation, never a resize"
    # Caller-requested order is preserved even though capture order is by device.
    assert [shot.kind for shot in result.screenshots] == ["full_page", "viewport_mobile"]


@pytest.mark.asyncio
async def test_capture_screenshots_refuses_kinds_from_two_devices() -> None:
    """The guard that makes the resize bug unrepresentable."""
    with pytest.raises(ValueError, match="multiple device profiles"):
        await capture_screenshots(object(), kinds=["full_page", "viewport_mobile"])


def test_every_screenshot_kind_maps_to_a_device_profile() -> None:
    """An unmapped kind must raise, never silently capture the wrong device."""
    from matrx_scraper.browser_pool import (
        FULL_PAGE_PRESETS,
        VIEWPORT_PRESETS,
        group_kinds_by_profile,
        profile_for_kind,
    )

    for kind in set(VIEWPORT_PRESETS) | set(FULL_PAGE_PRESETS):
        assert profile_for_kind(kind) is not None

    with pytest.raises(ValueError, match="unknown screenshot kind"):
        profile_for_kind("viewport_watch")

    grouped = group_kinds_by_profile(["desktop_full", "desktop_fold", "mobile_full", "mobile_fold"])
    assert set(grouped) == {"desktop", "mobile"}
    assert grouped["desktop"][1] == ["desktop_full", "desktop_fold"]
    assert grouped["mobile"][1] == ["mobile_full", "mobile_fold"]


@pytest.mark.asyncio
async def test_site_initialization_captures_both_kinds_of_one_device(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Two kinds on one device still cost ONE navigation and one settle."""
    calls: list[bool] = []
    sleeps: list[float] = []

    class FakePage:
        async def evaluate(self, expression: str) -> None:
            return None

        async def screenshot(self, **kwargs: object) -> bytes:
            calls.append(bool(kwargs["full_page"]))
            return b"PNG"

    async def _record_sleep(seconds: float) -> None:
        sleeps.append(seconds)

    monkeypatch.setattr(browser_pool_module.asyncio, "sleep", _record_sleep)
    monkeypatch.setattr(browser_pool_module, "png_dimensions", lambda png: (390, 2400))

    shots = await capture_screenshots(FakePage(), kinds=["mobile_full", "mobile_fold"])

    assert [shot.kind for shot in shots] == ["mobile_full", "mobile_fold"]
    assert calls == [True, False], "full_page vs viewport must be driven by kind"
    assert len(sleeps) == 1, "one settle per capture set, not one per kind"


@pytest.mark.asyncio
async def test_optional_screenshot_failure_is_reported_without_losing_other_kinds(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    from matrx_scraper.browser_pool import ScreenshotCaptureFailure

    class FakePage:
        async def evaluate(self, expression: str) -> None:
            return None

        async def screenshot(self, **kwargs: object) -> bytes:
            if kwargs["full_page"]:
                raise TimeoutError("fonts never settled")
            return b"PNG"

    async def no_sleep(seconds: float) -> None:
        return None

    monkeypatch.setattr(browser_pool_module.asyncio, "sleep", no_sleep)
    monkeypatch.setattr(browser_pool_module, "png_dimensions", lambda png: (1366, 768))
    failures: list[ScreenshotCaptureFailure] = []

    shots = await capture_screenshots(
        FakePage(),
        kinds=["full_page", "viewport_desktop"],
        failure_sink=failures,
    )

    assert [shot.kind for shot in shots] == ["viewport_desktop"]
    assert len(failures) == 1
    assert failures[0].kind == "full_page"
    assert failures[0].error_class == "TimeoutError"
    assert failures[0].error_message == "fonts never settled"


@pytest.mark.asyncio
async def test_font_readiness_timeout_stops_pending_loads_and_retries_once(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    evaluations: list[str] = []
    screenshot_calls = 0

    class FakePage:
        async def evaluate(self, expression: str) -> None:
            evaluations.append(expression)

        async def screenshot(self, **_kwargs: object) -> bytes:
            nonlocal screenshot_calls
            screenshot_calls += 1
            if screenshot_calls == 1:
                raise TimeoutError(
                    "Page.screenshot: Timeout 5000ms exceeded; waiting for fonts to load"
                )
            return b"PNG"

    async def no_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr(browser_pool_module.asyncio, "sleep", no_sleep)
    monkeypatch.setattr(browser_pool_module, "png_dimensions", lambda _png: (1366, 768))

    shots = await capture_screenshots(FakePage(), kinds=["viewport_desktop"])

    assert len(shots) == 1
    assert screenshot_calls == 2
    assert evaluations[:2] == ["window.scrollTo(0,0)", "window.stop()"]
    assert "window.stop()" in evaluations[2]
    assert "document.fonts.clear()" in evaluations[2]
    assert 'Object.defineProperty(document.fonts, "ready"' in evaluations[2]


@pytest.mark.asyncio
async def test_focused_screenshot_can_preserve_recipe_scroll(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    evaluations: list[str] = []

    class FakePage:
        async def evaluate(self, expression: str) -> None:
            evaluations.append(expression)

        async def screenshot(self, **_kwargs: object) -> bytes:
            return b"PNG"

    async def no_sleep(_seconds: float) -> None:
        return None

    monkeypatch.setattr(browser_pool_module.asyncio, "sleep", no_sleep)
    monkeypatch.setattr(browser_pool_module, "png_dimensions", lambda _png: (1366, 768))

    shots = await capture_screenshots(
        FakePage(),
        kinds=["viewport_desktop"],
        preserve_scroll=True,
    )

    assert len(shots) == 1
    assert evaluations == ["window.stop()"]
