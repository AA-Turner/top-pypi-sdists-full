"""
Initialization module for automatic Kolo activation via .pth file.

This module is imported when KOLO environment variable is set to 1, true, or True,
typically via the kolo.pth file in site-packages.

Uses _AutoEnabled (not Enabled) for cleaner separation between:
- User-controlled activation (Enabled context manager)
- Automatic background activation (_AutoEnabled with atexit cleanup)
"""

import atexit
import os
import sys


def pth_init():
    """Initialize Kolo monitoring when called from .pth file."""
    try:
        if os.environ.get("KOLO_DISABLE"):
            return

        if os.environ.get("KOLO") not in ("1", "true", "True"):
            return

        from kolo.core import _AutoEnabled

        # save_in_thread=False: a save thread still running after this atexit handler
        # segfaults during interpreter shutdown.
        auto_enabled = _AutoEnabled(
            config=None,
            source="KOLO=1",
            one_trace_per_test=False,
            save_in_thread=False,
            upload_token=None,
            db_path=None,
            name=None,
            inline=False,
            inline_returns=False,
        )

        if auto_enabled.activate():
            atexit.register(auto_enabled.cleanup)

    except Exception as e:  # pragma: no cover
        print(f"Kolo .pth initialization error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)


pth_init()
