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
        # Check if disabled explicitly
        if os.environ.get("KOLO_DISABLE"):
            return

        # Check if enabled (accepts "1", "true", or "True")
        if os.environ.get("KOLO") not in ("1", "true", "True"):
            return

        # Import and activate Kolo using _AutoEnabled
        from kolo.core import _AutoEnabled

        # Create an _AutoEnabled instance with default config
        # IMPORTANT: Use save_in_thread=False to avoid segfaults during process exit.
        #
        # When save_in_thread=True, the trace is saved in a background thread. This works
        # fine in normal usage (middleware, context managers) because the main thread
        # continues execution and the background thread completes before process exit.
        #
        # However, in atexit handlers (like this one), the situation is different:
        # 1. Process is exiting, atexit handlers run
        # 2. __exit__() spawns background thread to save trace
        # 3. atexit handler returns
        # 4. Python interpreter begins shutdown (module cleanup, C extension teardown)
        # 5. Background thread is still running, trying to use msgpack C extension
        # 6. Race condition: thread accesses deallocated Python/C objects → SEGFAULT
        #
        # By using save_in_thread=False, we ensure the trace is saved synchronously
        # in the atexit handler before Python shutdown begins. The blocking on exit
        # is acceptable - users want their trace data saved reliably.
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

        # Activate monitoring and register cleanup only if activation succeeded
        if auto_enabled.activate():
            atexit.register(auto_enabled.cleanup)

    except Exception as e:
        # If anything goes wrong during initialization, print to stderr
        # but don't crash the Python process
        print(f"Kolo .pth initialization error: {e}", file=sys.stderr)
        import traceback

        traceback.print_exc(file=sys.stderr)


pth_init()
