"""Negative control for P1: a SECOND Chromium against a user_data_dir already in use.

PLAN.md asserts: "That directory ... must be unique to one active Chromium instance.
Chromium itself does not permit simultaneous processes to share a user-data directory."

This process is launched by run_p1.py while the first persistent context is live. It
prints exactly one JSON line as its last stdout line:

    {"outcome": "error"|"launched"|"timeout", ...}

`launched` would FALSIFY the plan's assumption and is the result the harness is
specifically looking for.
"""

from __future__ import annotations

import json
import os
import sys
import traceback

os.environ.setdefault("PLAYWRIGHT_BROWSERS_PATH", "/opt/pw-browsers")


def main() -> int:
    udd, display = sys.argv[1], sys.argv[2]
    os.environ["DISPLAY"] = display
    from playwright.sync_api import sync_playwright

    result: dict[str, object] = {}
    try:
        with sync_playwright() as pw:
            ctx = pw.chromium.launch_persistent_context(
                user_data_dir=udd,
                headless=False,
                args=["--no-sandbox", "--window-position=100,100"],
                timeout=60_000,
            )
            # It "launched". Does it actually get its own working browser?
            pages = [p.url for p in ctx.pages]
            page = ctx.pages[0] if ctx.pages else ctx.new_page()
            page.goto("about:blank")
            result = {
                "outcome": "launched",
                "pages": pages,
                "note": "second context launched against a live user_data_dir",
            }
            ctx.close()
    except Exception as exc:  # noqa: BLE001
        result = {
            "outcome": "error",
            "exception_type": type(exc).__name__,
            "message": str(exc)[:4000],
            "traceback_tail": traceback.format_exc()[-1200:],
        }
    print(json.dumps(result))
    return 0


if __name__ == "__main__":
    sys.exit(main())
