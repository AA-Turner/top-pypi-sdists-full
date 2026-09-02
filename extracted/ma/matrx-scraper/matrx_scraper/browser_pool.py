from __future__ import annotations

import asyncio
import logging
import os
from dataclasses import dataclass, field
from typing import Any

from matrx_scraper.screenshot_dimensions import png_dimensions
from matrx_scraper.user_agents import normalize_user_agent

logger = logging.getLogger(__name__)


# Number of concurrent headless Chromium contexts the crawl/capture path may
# hold at once — the real ceiling on screenshot throughput. This is a CAPS
# constant ON PURPOSE, never an env var: it is not a secret and not
# per-environment, and a concurrency ceiling that silently differs between
# hosts is exactly the class of "works locally, melts in prod" failure the
# no-env-var rule exists to prevent. Changing it is a code push (fine — that
# beats a silent per-host drift). If it ever needs to vary per tenant, it
# belongs in the DB config table, still never in the environment.
#
# Sized for the current shared t3.xlarge sandbox host (4 vCPU / 16 GiB, shared
# with the sandbox workload). Each context is ~150-250 MB under load. 5 leaves
# headroom for the co-resident sandboxes; a dedicated crawl box could go higher.
DEFAULT_BROWSER_POOL_SIZE = 5
# Chrome can need several seconds to rasterize/encode a media-heavy page even
# after the DOM is ready. The pool lease already budgets 30 seconds per image;
# keep the operation bounded inside that envelope instead of dropping valid
# evidence at the former five-second cliff.
SCREENSHOT_CAPTURE_TIMEOUT_MS = 20_000
PLAYWRIGHT_SKIP_FONT_READY_ENV = "PW_TEST_SCREENSHOT_NO_FONTS_READY"

# Playwright's message when the driver subprocess is gone before a Browser
# proxy is closed. Expected during teardown, never an incident. Matched as a
# substring because Playwright wraps it in a longer Error(...) payload.
DRIVER_ALREADY_CLOSED = "Connection closed while reading from the driver"

try:
    from playwright.async_api import (
        Browser,
        Playwright,
        async_playwright,
    )
    from playwright.async_api import (
        TimeoutError as PlaywrightTimeoutError,
    )

    PLAYWRIGHT_AVAILABLE = True
except ImportError:
    PLAYWRIGHT_AVAILABLE = False
    Browser = None  # type: ignore[assignment,misc]
    Playwright = None  # type: ignore[assignment,misc]
    PlaywrightTimeoutError = TimeoutError  # type: ignore[assignment,misc]


# Default viewport presets used by `fetch_with_capture`. Override via the
# `screenshot_kinds` argument when calling.
VIEWPORT_PRESETS: dict[str, dict[str, int]] = {
    "viewport_desktop": {"width": 1366, "height": 768},
    "viewport_laptop": {"width": 1280, "height": 800},
    "viewport_tablet": {"width": 820, "height": 1180},
    "viewport_mobile": {"width": 390, "height": 844},
    "desktop_fold": {"width": 1440, "height": 900},
    "mobile_fold": {"width": 390, "height": 844},
}

FULL_PAGE_PRESETS: dict[str, dict[str, int]] = {
    "full_page": VIEWPORT_PRESETS["viewport_desktop"],
    "desktop_full": VIEWPORT_PRESETS["desktop_fold"],
    "laptop_full": VIEWPORT_PRESETS["viewport_laptop"],
    "tablet_full": VIEWPORT_PRESETS["viewport_tablet"],
    "mobile_full": VIEWPORT_PRESETS["mobile_fold"],
}

# The canonical breakage-review set: full-page capture at four real widths
# (1440 desktop / 1280 laptop / 820 tablet / 390 phone). This is what the AI
# visual-review pass consumes — one image per width, each the WHOLE page as
# that device class renders it. Named once so no caller hand-lists widths.
BREAKAGE_REVIEW_KINDS: list[str] = [
    "desktop_full",
    "laptop_full",
    "tablet_full",
    "mobile_full",
]


_DESKTOP_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36"
)
_MOBILE_UA = (
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 "
    "(KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1"
)


@dataclass(frozen=True)
class DeviceProfile:
    """Browser-context emulation for one device class.

    A screenshot is only a truthful record of what a visitor sees if the page
    was LOADED under that device's emulation. Resizing the viewport after load
    is not equivalent and produces a misleading capture: the user agent stays
    desktop (so UA-sniffing sites serve the desktop site), `is_mobile` and
    `has_touch` stay false (so hover menus render open and mobile nav never
    engages), the device pixel ratio stays 1, and responsive images have
    already committed to their desktop `srcset` candidates.

    Each profile therefore requires its OWN context and its OWN navigation.
    """

    name: str
    viewport: dict[str, int]
    user_agent: str
    device_scale_factor: int
    is_mobile: bool
    has_touch: bool

    def context_kwargs(self, user_agent_override: str | None = None) -> dict[str, Any]:
        """Playwright context options for this device.

        `user_agent_override` replaces ONLY the UA string. Viewport,
        `device_scale_factor`, `is_mobile` and `has_touch` are the device's
        GEOMETRY and stay intact — a caller asking to be seen as Googlebot
        still wants the mobile screenshot taken at mobile dimensions.
        """
        return {
            "viewport": dict(self.viewport),
            "user_agent": user_agent_override or self.user_agent,
            "device_scale_factor": self.device_scale_factor,
            "is_mobile": self.is_mobile,
            "has_touch": self.has_touch,
        }


DESKTOP_PROFILE = DeviceProfile(
    name="desktop",
    viewport=VIEWPORT_PRESETS["desktop_fold"],
    user_agent=_DESKTOP_UA,
    device_scale_factor=1,
    is_mobile=False,
    has_touch=False,
)

LAPTOP_PROFILE = DeviceProfile(
    name="laptop",
    viewport=VIEWPORT_PRESETS["viewport_laptop"],
    user_agent=_DESKTOP_UA,
    device_scale_factor=1,
    is_mobile=False,
    has_touch=False,
)

MOBILE_PROFILE = DeviceProfile(
    name="mobile",
    viewport=VIEWPORT_PRESETS["viewport_mobile"],
    user_agent=_MOBILE_UA,
    device_scale_factor=3,
    is_mobile=True,
    has_touch=True,
)

TABLET_PROFILE = DeviceProfile(
    name="tablet",
    viewport=VIEWPORT_PRESETS["viewport_tablet"],
    user_agent=_MOBILE_UA,
    device_scale_factor=2,
    is_mobile=True,
    has_touch=True,
)

# Which device a screenshot kind must be captured under. A kind absent here is
# a programming error, not a default — an unknown kind raises rather than
# silently capturing the wrong device.
PROFILE_BY_KIND: dict[str, DeviceProfile] = {
    "viewport_desktop": DESKTOP_PROFILE,
    "desktop_fold": DESKTOP_PROFILE,
    "full_page": DESKTOP_PROFILE,
    "desktop_full": DESKTOP_PROFILE,
    # A laptop is a desktop-class render (not mobile), just narrower.
    "viewport_laptop": LAPTOP_PROFILE,
    "laptop_full": LAPTOP_PROFILE,
    "viewport_tablet": TABLET_PROFILE,
    "tablet_full": TABLET_PROFILE,
    "viewport_mobile": MOBILE_PROFILE,
    "mobile_fold": MOBILE_PROFILE,
    "mobile_full": MOBILE_PROFILE,
}


def profile_for_kind(kind: str) -> DeviceProfile:
    profile = PROFILE_BY_KIND.get(kind)
    if profile is None:
        raise ValueError(f"unknown screenshot kind: {kind!r} (known: {sorted(PROFILE_BY_KIND)})")
    return profile


def group_kinds_by_profile(kinds: list[str]) -> dict[str, tuple[DeviceProfile, list[str]]]:
    """Group requested kinds into one navigation per device profile."""
    grouped: dict[str, tuple[DeviceProfile, list[str]]] = {}
    for kind in kinds:
        profile = profile_for_kind(kind)
        if profile.name not in grouped:
            grouped[profile.name] = (profile, [])
        grouped[profile.name][1].append(kind)
    return grouped


@dataclass
class CapturedScreenshot:
    kind: str
    width: int
    height: int
    bytes: bytes


@dataclass(frozen=True)
class ScreenshotCaptureFailure:
    kind: str
    error_class: str
    error_message: str


@dataclass
class FetchWithCaptureResult:
    content: str
    response_url: str
    status_code: int
    headers: dict[str, str]
    title: str
    screenshots: list[CapturedScreenshot] = field(default_factory=list)
    screenshot_failures: list[ScreenshotCaptureFailure] = field(default_factory=list)
    recipe_action_log: list[str] = field(default_factory=list)
    # Full navigation chain, oldest hop first, final document last — same
    # {"status", "url"} hop shape as the HTTP transports. Length 1 = no redirect.
    redirect_chain: list[dict[str, Any]] = field(default_factory=list)


# `inspect_url` wait/timeout discipline — CAPS constants, never env vars.
# A render check must not report "no console errors" for a page whose scripts
# had not run yet, so this waits for `load` (not `commit`) and then gives the
# page a bounded quiet window. The hard budget bounds how long ONE caller can
# hold pooled browsers.
INSPECT_NAV_TIMEOUT_MS = 15_000
INSPECT_NETWORK_IDLE_TIMEOUT_MS = 5_000
INSPECT_SETTLE_SECONDS = 1.5
INSPECT_HARD_BUDGET_SECONDS = 25.0


class BrowserInspectTimeout(Exception):
    """`inspect_url` exceeded its hard budget — retryable, page-level failure."""


@dataclass
class PageInspection:
    """What the browser SAW at a URL — the render-correctness evidence set.

    Distinct from `FetchWithCaptureResult` (which carries HTML for a parser):
    this carries the console/network error streams and DOM probe answers that
    only exist while the page is open and cannot be recovered from HTML.
    """

    http_status: int | None
    final_url: str
    title: str = ""
    console_errors: list[str] = field(default_factory=list)
    failed_requests: list[str] = field(default_factory=list)
    dom_text_found: bool | None = None
    dom_selector_found: bool | None = None
    screenshots: list[CapturedScreenshot] = field(default_factory=list)
    screenshot_failures: list[ScreenshotCaptureFailure] = field(default_factory=list)


async def capture_screenshots(
    page: Any,
    *,
    kinds: list[str],
    failure_sink: list[ScreenshotCaptureFailure] | None = None,
    preserve_scroll: bool = False,
) -> list[CapturedScreenshot]:
    """Capture viewport / full-page screenshots on an already-open Playwright page.

    This is the ONE screenshot-capture implementation. ``fetch_with_capture``
    navigates then calls this; callers that own their own navigation (e.g.
    cms_verify needing console/DOM probes) call it directly. Unknown kinds
    raise — never silently skipped.
    """
    if not kinds:
        return []
    # NEVER resize the viewport here. The caller's context is already emulating
    # the device these kinds belong to (see DeviceProfile) — resizing mid-page
    # silently invalidates that emulation and yields a squeezed desktop render
    # instead of a mobile one. Every kind passed in must share one profile;
    # `group_kinds_by_profile` is what guarantees that.
    profiles = {profile_for_kind(kind).name for kind in kinds}
    if len(profiles) > 1:
        raise ValueError(
            f"capture_screenshots got kinds spanning multiple device profiles "
            f"({sorted(profiles)}); group them with group_kinds_by_profile and "
            f"navigate once per profile"
        )
    out: list[CapturedScreenshot] = []
    if not preserve_scroll:
        await page.evaluate("window.scrollTo(0,0)")
    await asyncio.sleep(0.3)  # one settle for the whole set, not one per kind
    # The caller has already completed its bounded DOM settle and recipe (the
    # backlink recipe highlights + centers the target here). Freeze the
    # rendered evidence before asking Chrome to rasterize it; third-party
    # requests and animation frames otherwise keep media-heavy pages busy long
    # enough for even a viewport capture to time out.
    await page.evaluate("window.stop()")
    for kind in kinds:
        full_page = kind in FULL_PAGE_PRESETS
        try:
            png = await page.screenshot(
                full_page=full_page,
                type="png",
                timeout=SCREENSHOT_CAPTURE_TIMEOUT_MS,
                animations="disabled",
                caret="hide",
            )
        except asyncio.CancelledError:
            raise
        except Exception as exc:
            # Playwright waits for ``document.fonts.ready`` before capture. A
            # third-party font request can remain open after the useful page is
            # fully rendered, exhausting our screenshot budget even though the
            # DOM and highlighted link are ready. Cancel only those outstanding
            # page requests and retry once; parsed capture already completed, so
            # this recovery changes no evidence other than making the PNG
            # available. Every other failure keeps the normal fail-loud path.
            if "waiting for fonts to load" in str(exc).lower():
                logger.warning(
                    "screenshot font readiness timed out for kind=%s; "
                    "stopping outstanding page loads and retrying once",
                    kind,
                )
                try:
                    await page.evaluate(
                        """() => {
                            window.stop();
                            try {
                                document.fonts.clear();
                                Object.defineProperty(document.fonts, "ready", {
                                    configurable: true,
                                    value: Promise.resolve(document.fonts),
                                });
                            } catch (_) {
                                // The retry remains fail-loud if the browser
                                // refuses to shadow FontFaceSet.ready.
                            }
                        }"""
                    )
                    png = await page.screenshot(
                        full_page=full_page,
                        type="png",
                        timeout=SCREENSHOT_CAPTURE_TIMEOUT_MS,
                        animations="disabled",
                        caret="hide",
                    )
                except asyncio.CancelledError:
                    raise
                except Exception as retry_exc:
                    exc = retry_exc
                else:
                    width, height = png_dimensions(png)
                    out.append(
                        CapturedScreenshot(
                            kind=kind,
                            width=width,
                            height=height,
                            bytes=png,
                        )
                    )
                    continue
            if failure_sink is None:
                raise
            failure = ScreenshotCaptureFailure(
                kind=kind,
                error_class=type(exc).__name__,
                error_message=str(exc),
            )
            failure_sink.append(failure)
            logger.warning(
                "screenshot capture failed for kind=%s: %s: %s",
                kind,
                failure.error_class,
                failure.error_message,
                exc_info=True,
            )
            continue
        width, height = png_dimensions(png)
        out.append(CapturedScreenshot(kind=kind, width=width, height=height, bytes=png))
    return out


class PlaywrightBrowserPool:
    """Manages a fixed-size pool of headless Chromium instances."""

    def __init__(self, pool_size: int = DEFAULT_BROWSER_POOL_SIZE) -> None:
        if not PLAYWRIGHT_AVAILABLE:
            raise ImportError(
                "playwright is required for PlaywrightBrowserPool: pip install playwright"
            )
        if pool_size < 1:
            raise ValueError("browser pool size must be at least 1")
        self._pool_size = pool_size
        self._queue: asyncio.Queue[Browser] = asyncio.Queue()
        self._playwright: Playwright | None = None
        self._browsers: list[Browser] = []

    async def start(self) -> None:
        # Playwright otherwise waits on ``document.fonts.ready`` inside its
        # isolated utility world, where page-side timeout recovery cannot
        # reliably reach it. Screenshot evidence must not disappear because a
        # decorative third-party font host stalls. We already give the page a
        # bounded DOM settle before capture, so start the driver with its
        # upstream font-wait bypass and capture the rendered fallback font when
        # necessary. This is a code-owned invariant, not deployment config.
        os.environ[PLAYWRIGHT_SKIP_FONT_READY_ENV] = "1"
        self._playwright = await async_playwright().start()
        for _ in range(self._pool_size):
            browser = await self._playwright.chromium.launch(headless=True)
            self._browsers.append(browser)
            self._queue.put_nowait(browser)
        logger.info("PlaywrightBrowserPool started with %d browsers", self._pool_size)

    async def stop(self) -> None:
        for browser in self._browsers:
            try:
                await browser.close()
            except Exception as exc:
                # Playwright may tear the shared driver down before the
                # individual Browser proxies during app shutdown. The browsers
                # are already gone in that case, so three red tracebacks turn a
                # clean shutdown into a false incident. Every OTHER close error
                # still screams.
                if DRIVER_ALREADY_CLOSED in str(exc):
                    logger.debug("Browser driver already closed during shutdown")
                else:
                    logger.exception("Error closing browser")
        self._browsers.clear()

        if self._playwright:
            await self._playwright.stop()
            self._playwright = None
        logger.info("PlaywrightBrowserPool stopped")

    async def acquire(self, timeout: float = 30.0) -> Browser:  # noqa: ASYNC109
        return await asyncio.wait_for(self._queue.get(), timeout=timeout)

    def release(self, browser: Browser) -> None:
        self._queue.put_nowait(browser)

    async def fetch(
        self,
        url: str,
        proxy: str | None = None,
        timeout_ms: int = 30000,
        user_agent: str | None = None,
    ) -> tuple[str, str, int, dict[str, str], str]:
        """Returns (content, response_url, status_code, headers, title).

        `user_agent` overrides the browser's own UA. Note there is no default
        here to preserve: without an override this context inherits headless
        Chromium's UA, exactly as it does today.
        """
        user_agent = normalize_user_agent(user_agent)
        browser = await self.acquire(timeout=max(30.0, timeout_ms / 1000 + 5.0))
        try:
            context_kwargs: dict = {}
            if proxy:
                context_kwargs["proxy"] = {"server": proxy}
            if user_agent:
                # A browser UA is a CONTEXT option, not a header — setting it
                # via extra_http_headers would leave navigator.userAgent (and
                # therefore every UA-sniffing script on the page) disagreeing
                # with the header the server saw.
                context_kwargs["user_agent"] = user_agent

            context = await browser.new_context(**context_kwargs)
            page = await context.new_page()

            try:
                resp = await page.goto(url, timeout=timeout_ms, wait_until="domcontentloaded")
                content = await page.content()
                title = await page.title()
                response_url = page.url
                status_code = resp.status if resp else 500
                headers = await resp.all_headers() if resp else {}
            finally:
                await page.close()
                await context.close()

            return content, response_url, status_code, headers, title
        finally:
            self.release(browser)

    async def fetch_with_capture(
        self,
        url: str,
        *,
        proxy: str | None = None,
        timeout_ms: int = 45_000,
        settle_timeout_ms: int = 5_000,
        screenshot_kinds: list[str] | None = None,
        recipe_actions: list[Any] | None = None,
        action_runner: Any | None = None,
        user_agent: str | None = None,
        preserve_scroll: bool = False,
    ) -> FetchWithCaptureResult:
        """Single-pass: navigate, run any recipe actions, capture screenshots.

        Returns the rendered HTML (after recipe DOM mutations), final URL,
        status, headers, title, AND a list of `CapturedScreenshot`s — one per
        requested kind.

        `recipe_actions` is an opaque list (typically `RecipeAction` from
        matrx_scraper.recipes) that `action_runner(page, actions)` knows how
        to execute. Pass `recipes.execute_directives` from the host. We accept
        them via parameter to keep this module free of host-specific imports.
        """
        user_agent = normalize_user_agent(user_agent)
        kinds = list(screenshot_kinds or [])
        # A holder can occupy the shared pool for its full navigation, settle,
        # and screenshot budget. Wait for that bounded operation rather than
        # failing healthy concurrent crawls after a fixed 30 seconds.
        acquire_timeout = max(
            30.0,
            (timeout_ms + settle_timeout_ms) / 1000 + (30.0 * max(1, len(kinds))) + 5.0,
        )
        browser = await self.acquire(timeout=acquire_timeout)
        try:
            # Emulate the device the requested kinds belong to for the whole
            # load — never load desktop and resize afterwards. Kinds belonging
            # to OTHER devices get their own navigation after this one.
            profile = profile_for_kind(kinds[0]) if kinds else DESKTOP_PROFILE
            grouped = group_kinds_by_profile(kinds)
            same_profile_kinds = grouped.get(profile.name, (profile, []))[1]
            other_profile_kinds = [
                kind
                for name, (_, profile_kinds) in grouped.items()
                if name != profile.name
                for kind in profile_kinds
            ]
            context_kwargs: dict = profile.context_kwargs(user_agent)
            if proxy:
                context_kwargs["proxy"] = {"server": proxy}

            context = await browser.new_context(**context_kwargs)
            page = await context.new_page()
            screenshots: list[CapturedScreenshot] = []
            screenshot_failures: list[ScreenshotCaptureFailure] = []
            action_log: list[str] = []
            try:
                # A screenshot needs a committed document, not every deferred
                # script required by DOMContentLoaded. Waiting for the latter
                # made a usable page consume the entire 45-second navigation
                # timeout. Commit first, then give the DOM a short bounded
                # settle window and capture whatever the user can already see.
                resp = await page.goto(url, timeout=timeout_ms, wait_until="commit")
                try:
                    await page.wait_for_load_state(
                        "domcontentloaded",
                        timeout=max(0, settle_timeout_ms),
                    )
                except PlaywrightTimeoutError:
                    logger.info(
                        "DOM did not settle within %dms for %s; capturing committed page",
                        settle_timeout_ms,
                        url,
                    )
                response_url = page.url
                status_code = resp.status if resp else 500
                headers = await resp.all_headers() if resp else {}

                # Walk the real navigation redirect chain Playwright already
                # tracked (request.redirected_from), oldest hop first. Do this
                # while the page/context is still open — request handles are
                # only guaranteed live until then.
                redirect_chain: list[dict[str, Any]] = []
                if resp is not None:
                    try:
                        prior_requests: list[Any] = []
                        node = resp.request.redirected_from
                        while node is not None:
                            prior_requests.append(node)
                            node = node.redirected_from
                        for hop_request in reversed(prior_requests):
                            hop_status: int | None = None
                            try:
                                hop_response = await hop_request.response()
                                hop_status = hop_response.status if hop_response else None
                            except Exception:
                                hop_status = None
                            redirect_chain.append({"status": hop_status, "url": hop_request.url})
                    except Exception as exc:
                        # Never lose the fetch over chain introspection, but a
                        # dropped chain is missing evidence — scream about it.
                        logger.warning(
                            "redirect chain capture FAILED for %s — hop evidence lost: %s",
                            url,
                            exc,
                        )
                        redirect_chain = []
                if not redirect_chain or redirect_chain[-1].get("url") != response_url:
                    redirect_chain.append({"status": status_code, "url": response_url})

                # Run recipe actions before reading content / shooting frames.
                if recipe_actions and action_runner is not None:
                    try:
                        action_log = await action_runner(page, recipe_actions) or []
                    except Exception as exc:
                        logger.info("recipe action runner raised: %s", exc)
                        action_log = [f"runner crashed: {type(exc).__name__}: {exc}"]

                title = await page.title()
                # Only this profile's kinds can be captured on this page; any
                # other device gets its own emulated navigation below.
                screenshots = await capture_screenshots(
                    page,
                    kinds=same_profile_kinds,
                    failure_sink=screenshot_failures,
                    preserve_scroll=preserve_scroll,
                )

                # Read the (possibly mutated by recipe) HTML last so any
                # `remove`/`evaluate` actions are reflected in the body that
                # we hand back to the parser.
                content = await page.content()
            finally:
                await page.close()
                await context.close()

        finally:
            self.release(browser)

        # Other device profiles: one further emulated navigation each. Released
        # the browser first so this re-queues rather than holding two slots.
        if other_profile_kinds:
            screenshots.extend(
                await self.capture_url(
                    url,
                    kinds=other_profile_kinds,
                    proxy=proxy,
                    timeout_ms=timeout_ms,
                    settle_timeout_ms=settle_timeout_ms,
                    recipe_actions=recipe_actions,
                    action_runner=action_runner,
                    failure_sink=screenshot_failures,
                    user_agent=user_agent,
                    preserve_scroll=preserve_scroll,
                )
            )
            # Restore the caller's requested order — callers assert kind order.
            by_kind = {shot.kind: shot for shot in screenshots}
            screenshots = [by_kind[kind] for kind in kinds if kind in by_kind]

        return FetchWithCaptureResult(
            content=content,
            response_url=response_url,
            status_code=status_code,
            headers=headers,
            title=title,
            screenshots=screenshots,
            screenshot_failures=screenshot_failures,
            recipe_action_log=action_log,
            redirect_chain=redirect_chain,
        )

    async def capture_url(
        self,
        url: str,
        *,
        kinds: list[str],
        proxy: str | None = None,
        timeout_ms: int = 45_000,
        settle_timeout_ms: int = 5_000,
        recipe_actions: list[Any] | None = None,
        action_runner: Any | None = None,
        failure_sink: list[ScreenshotCaptureFailure] | None = None,
        user_agent: str | None = None,
        preserve_scroll: bool = False,
    ) -> list[CapturedScreenshot]:
        """Capture `kinds` for one URL, navigating once per device profile.

        This is the visual-capture entry point (Phase B). It exists separately
        from `fetch_with_capture` because a truthful mobile screenshot requires
        its own emulated context and its own navigation — desktop and mobile
        were never one page load. Kinds are grouped so N kinds on the same
        device still cost ONE navigation.
        """
        if not kinds:
            return []
        # Same rule as fetch_with_capture: the override replaces the profile's
        # UA and nothing else, so a mobile capture stays a mobile capture.
        user_agent = normalize_user_agent(user_agent)
        captured: list[CapturedScreenshot] = []
        for profile, profile_kinds in group_kinds_by_profile(kinds).values():
            browser = await self.acquire(
                timeout=max(30.0, (timeout_ms + settle_timeout_ms) / 1000 + 30.0)
            )
            try:
                context_kwargs = profile.context_kwargs(user_agent)
                if proxy:
                    context_kwargs["proxy"] = {"server": proxy}
                context = await browser.new_context(**context_kwargs)
                page = await context.new_page()
                try:
                    await page.goto(url, timeout=timeout_ms, wait_until="commit")
                    try:
                        await page.wait_for_load_state(
                            "domcontentloaded", timeout=max(0, settle_timeout_ms)
                        )
                    except PlaywrightTimeoutError:
                        logger.info(
                            "DOM did not settle within %dms for %s (%s); capturing anyway",
                            settle_timeout_ms,
                            url,
                            profile.name,
                        )
                    if recipe_actions and action_runner is not None:
                        try:
                            await action_runner(page, recipe_actions)
                        except Exception as exc:
                            logger.info("recipe action runner raised: %s", exc)
                    captured.extend(
                        await capture_screenshots(
                            page,
                            kinds=profile_kinds,
                            failure_sink=failure_sink,
                            preserve_scroll=preserve_scroll,
                        )
                    )
                finally:
                    await page.close()
                    await context.close()
            finally:
                self.release(browser)
        return captured

    async def inspect_url(
        self,
        url: str,
        *,
        kinds: list[str] | None = None,
        expect_text: str | None = None,
        expect_selector: str | None = None,
        proxy: str | None = None,
        user_agent_suffix: str | None = None,
        nav_timeout_ms: int = INSPECT_NAV_TIMEOUT_MS,
        network_idle_timeout_ms: int = INSPECT_NETWORK_IDLE_TIMEOUT_MS,
        settle_seconds: float = INSPECT_SETTLE_SECONDS,
        hard_budget_seconds: float = INSPECT_HARD_BUDGET_SECONDS,
    ) -> PageInspection:
        """Navigate and report what the BROWSER saw — errors, DOM probes, shots.

        The third stateless entry point, beside `fetch` (HTML only) and
        `capture_url` (pixels only). It exists because neither of those can
        answer "did this page render CORRECTLY": that needs the console error
        stream, the failed-request stream, and a DOM probe — evidence that
        only survives while the page is open, so it cannot be reconstructed by
        a caller holding the returned HTML.

        Wait discipline is deliberately stricter than `capture_url`'s
        commit+domcontentloaded: a render check must not report "no console
        errors" for a page whose scripts had not run yet. `wait_until="load"`
        → bounded best-effort `networkidle` → fixed settle, the whole thing
        under one hard budget so a hung page cannot hold a pooled browser
        forever.

        Kinds are grouped by device profile exactly as `capture_url` does —
        desktop and mobile were never one page load (see `DeviceProfile`).
        Console errors and failed requests are merged across every profile
        navigation (a mobile-only script error is a real defect); status,
        title, final URL and the DOM probes come from the FIRST profile's
        navigation so the result is deterministic.
        """
        kinds = list(kinds or [])
        # No screenshots requested still means one real navigation — the
        # console/DOM evidence IS the product of this call.
        groups = list(group_kinds_by_profile(kinds).values()) if kinds else [(DESKTOP_PROFILE, [])]

        console_errors: list[str] = []
        failed_requests: list[str] = []
        screenshots: list[CapturedScreenshot] = []
        screenshot_failures: list[ScreenshotCaptureFailure] = []
        primary: dict[str, Any] = {}

        async def _run_profile(
            profile: DeviceProfile, profile_kinds: list[str], is_primary: bool
        ) -> None:
            browser = await self.acquire(timeout=max(30.0, hard_budget_seconds + 5.0))
            try:
                context_kwargs = profile.context_kwargs()
                if user_agent_suffix:
                    # Append, never replace: the profile's UA is what makes the
                    # emulation truthful (a desktop UA on a mobile context makes
                    # UA-sniffing sites serve the desktop site). Appending keeps
                    # the bot identifiable without breaking the device identity.
                    context_kwargs["user_agent"] = f"{profile.user_agent} {user_agent_suffix}"
                if proxy:
                    context_kwargs["proxy"] = {"server": proxy}
                context = await browser.new_context(**context_kwargs)
                try:
                    page = await context.new_page()
                    page.on(
                        "console",
                        lambda msg: (
                            console_errors.append(msg.text) if msg.type == "error" else None
                        ),
                    )
                    # An uncaught exception (`throw new Error(...)`) shows in
                    # DevTools' Console as a red error but is a SEPARATE
                    # Playwright event from `console` (console.* calls only).
                    # Miss it and a genuinely broken page passes the check.
                    page.on(
                        "pageerror",
                        lambda exc: console_errors.append(f"Uncaught: {exc}"),
                    )
                    page.on(
                        "requestfailed",
                        lambda req: failed_requests.append(
                            f"{req.method} {req.url} — {req.failure}"
                        ),
                    )
                    try:
                        response = await page.goto(url, timeout=nav_timeout_ms, wait_until="load")
                        try:
                            await page.wait_for_load_state(
                                "networkidle", timeout=network_idle_timeout_ms
                            )
                        except Exception:
                            pass  # best-effort — analytics beacons never go quiet
                        await asyncio.sleep(settle_seconds)

                        if is_primary:
                            primary["http_status"] = response.status if response else None
                            primary["final_url"] = page.url
                            primary["title"] = await page.title()
                            if expect_text:
                                content = await page.content()
                                primary["dom_text_found"] = expect_text in content
                            if expect_selector:
                                primary["dom_selector_found"] = (
                                    await page.locator(expect_selector).count()
                                ) > 0

                        if profile_kinds:
                            screenshots.extend(
                                await capture_screenshots(
                                    page,
                                    kinds=profile_kinds,
                                    failure_sink=screenshot_failures,
                                )
                            )
                    finally:
                        await page.close()
                finally:
                    await context.close()
            finally:
                self.release(browser)

        async def _run_all() -> None:
            for index, (profile, profile_kinds) in enumerate(groups):
                await _run_profile(profile, profile_kinds, is_primary=index == 0)

        try:
            await asyncio.wait_for(_run_all(), timeout=hard_budget_seconds)
        except TimeoutError as exc:
            raise BrowserInspectTimeout(
                f"Timed out inspecting {url} (budget {hard_budget_seconds}s)."
            ) from exc

        # Restore the caller's requested kind order — callers assert on it.
        by_kind = {shot.kind: shot for shot in screenshots}
        ordered = [by_kind[kind] for kind in kinds if kind in by_kind]

        return PageInspection(
            http_status=primary.get("http_status"),
            final_url=primary.get("final_url") or url,
            title=primary.get("title") or "",
            console_errors=console_errors,
            failed_requests=failed_requests,
            dom_text_found=primary.get("dom_text_found"),
            dom_selector_found=primary.get("dom_selector_found"),
            screenshots=ordered,
            screenshot_failures=screenshot_failures,
        )

    @property
    def size(self) -> int:
        return self._pool_size

    @property
    def available(self) -> int:
        return self._queue.qsize()
