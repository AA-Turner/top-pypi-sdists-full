"""SmartUI visual comparison screenshot.

Thin pass-through to `lambdatest_playwright_driver.smartui_snapshot_async`
so the binding uses the same DOM-serialization + SmartUI-server POST path
that the non-binding generator relies on. The SDK handles its own server
availability check via `is_smartui_enabled`, so we don't duplicate that.

Cloud-gated: only fires when run_target == "cloud" because the local
SmartUI server is started by HE pre commands (`npx smartui exec:start`).
Local runs skip with a warning since the SmartUI server typically isn't
running.

Requires `lambdatest-playwright-driver >= 1.1.0` (ships the async variant).
Installed at HE runtime by code-export's `update_pre_post_for_smartui()`.
Missing SDK at local-dev time → ImportError surfaces clearly.
"""

import logging

from testmu import _config

_log = logging.getLogger("testmu")


async def smartui_snapshot(page, name, options=None):
    """Capture a SmartUI visual comparison screenshot via the SDK.

    Args:
        page:    Playwright async Page instance
        name:    SmartUI comparison name
        options: Optional SmartUI options dict (viewports, ignoreRegions, ...)
    """
    options = options or {}
    _log.info("    [smartui_snapshot] name=%r", name)
    if _config.run_target != "cloud":
        _log.warning(
            "    [smartui_snapshot] requires cloud run target — skipping name=%r", name
        )
        return None
    try:
        # Lazy import: only required when the step is actually reached.
        # SDK v1.1.0+ exposes the async counterpart under this name.
        from lambdatest_playwright_driver import smartui_snapshot_async as _sdk_snapshot

        await _sdk_snapshot(page, name, options)
        _log.info("    [smartui_snapshot] captured name=%r", name)
    except ImportError:
        _log.warning(
            "    [smartui_snapshot] lambdatest_playwright_driver not installed — "
            "install `lambdatest-playwright-driver>=1.1.0` or add it to requirements.txt"
        )
        raise
    except Exception as e:
        _log.warning("    [smartui_snapshot] failed: %s", e)
    return None
