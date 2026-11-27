"""LambdaTest accessibility scan of the current page through the grid hook."""

import logging

from testmu import _config

_log = logging.getLogger("testmu")


async def accessibility_scan(page):
    """Scan the current page for accessibility; a no-op off the LambdaTest cloud.

    Returns the grid's reply, or None when skipped or when the hook fails (e.g. before the first page load).
    """
    if _config.run_target != "cloud":
        _log.info("    [accessibility_scan] no-op outside LambdaTest cloud")
        return None
    try:
        reply = await page.evaluate("lambda-accessibility-scan")
    except Exception as e:  # noqa: BLE001 — a scan must not fail the test
        _log.warning("    [accessibility_scan] failed: %s", e)
        return None
    _log.info("    [accessibility_scan] %s", reply)
    return reply
