"""SmartUI visual comparison screenshot.

Captures through a running SmartUI server (`npx smartui exec:start`, started
by the run's pre commands), with the same calls the SmartUI Playwright driver
makes, taken from `lambdatest-sdk-utils`: fetch the DOM serializer, serialize
the page with it, post the snapshot.

Server-gated: a snapshot is taken only when the server answers its health
check (`is_smartui_enabled`, as the driver checks); otherwise the step skips
with a warning. A SmartUI error is logged and never fails the step.

Requires `lambdatest-sdk-utils` (a dependency of this package). The server
address comes from `SMARTUI_SERVER_ADDRESS` (default `http://localhost:49152`).
"""

import json
import logging

_log = logging.getLogger("testmu")

# The grid session's id, looked up once per process.
_lt_session_id = None


async def _session_id(page):
    """The LambdaTest session id of `page`'s grid session (getTestDetails), or
    None when it cannot be read."""
    global _lt_session_id
    if _lt_session_id is None:
        try:
            details = await page.evaluate(
                "_ => {}", 'lambdatest_action: {"action": "getTestDetails"}'
            )
            _lt_session_id = (json.loads(details).get("data") or {}).get("session_id") or ""
        except Exception as e:  # noqa: BLE001 — linking is best-effort
            _log.warning("    [smartui_snapshot] could not read the session id: %s", e)
            _lt_session_id = ""
    return _lt_session_id or None


async def smartui_snapshot(page, name, options=None):
    """Capture a SmartUI visual comparison screenshot through the SmartUI server.

    Args:
        page:    Playwright async Page instance
        name:    SmartUI comparison name
        options: Optional SmartUI options dict (viewports, ignoreRegions, ...)
    """
    from lambdatest_sdk_utils import fetch_dom_serializer, is_smartui_enabled, post_snapshot

    options = options or {}
    _log.info("    [smartui_snapshot] name=%r", name)
    if not is_smartui_enabled():
        _log.warning("    [smartui_snapshot] no SmartUI server — skipping name=%r", name)
        return None
    try:
        # The session id links the snapshot to the session in the Automation
        # dashboard; the Selenium SDK sends driver.session_id the same way.
        if not options.get("sessionId"):
            session_id = await _session_id(page)
            if session_id:
                options = {**options, "sessionId": session_id}
        serializer = fetch_dom_serializer()
        await page.evaluate(serializer["data"]["dom"])
        dom = await page.evaluate("([options]) => SmartUIDOM.serialize(options)", [options])
        response = post_snapshot(
            {"name": name, "url": page.url, "dom": dom},
            "lambdatest-playwright-driver",
            options=options,
        )
        for warning in ((response or {}).get("data") or {}).get("warnings") or []:
            _log.warning("    [smartui_snapshot] %s", warning)
        _log.info("    [smartui_snapshot] captured name=%r", name)
    except Exception as e:
        _log.warning("    [smartui_snapshot] failed: %s", e)
    return None
