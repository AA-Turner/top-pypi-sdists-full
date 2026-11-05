"""Lighthouse (performance) report on navigation.

The Selenium hub generates the report by itself: its proxy watches for
``POST /session/<id>/url`` and runs Lighthouse whenever the session carries
``performance``. A CDP/Playwright session never issues that request, so the
grid's only entry point is the explicit ``lambdatest_action: lighthouseReport``
hook — without it ``performance: true`` silently produces no report (TE-34270).
"""

import functools
import json
import logging

_log = logging.getLogger("testmu")

# Lighthouse runs against the session browser's devtools port. The hub rejects
# every other browser and marks the whole test errored, so never ask there.
_LIGHTHOUSE_BROWSERS = ("chrome", "microsoftedge", "pw-chromium", "island")


def install_on_goto(caps: dict) -> None:
    """Patch ``Page.goto`` to request a report after every navigation.

    Patching the class rather than emitting a call per navigation covers every
    goto in a generated test — including the ones inside binding helpers such as
    ``new_tab`` — in one place. No-op unless the session carries ``performance``
    on a browser the grid can run Lighthouse on. Idempotent.

    Args:
        caps: capability dict as sent to the grid
    """
    if not caps.get("LT:Options", {}).get("performance"):
        return

    browser = caps.get("browserName", "")
    if browser.lower() not in _LIGHTHOUSE_BROWSERS:
        _log.warning(
            "    [lighthouse] performance is on, but %s cannot run Lighthouse — "
            "no reports will be generated",
            browser,
        )
        return

    from playwright.async_api import Page

    original = Page.goto
    if getattr(original, "_testmu_lighthouse", False):
        return

    @functools.wraps(original)
    async def goto(self, url, **kwargs):
        response = await original(self, url, **kwargs)
        # page.url is the post-redirect URL, which is what the report covers.
        target = self.url
        payload = json.dumps(
            {"action": "lighthouseReport", "arguments": {"url": target}}
        )
        try:
            await self.evaluate("_ => {}", f"lambdatest_action: {payload}")
            _log.info("    [lighthouse] report generated for %s", target)
        except Exception as e:  # noqa: BLE001 — a missing report must not fail the test
            _log.warning("    [lighthouse] report failed for %s: %s", target, e)
        return response

    goto._testmu_lighthouse = True
    Page.goto = goto
    _log.info("    [lighthouse] a report is generated after every navigation")
