"""Moved to `probe.sdk.capture.logs.logs` (agent:11); this path stays importable and runnable for good (an older
release's log helper runs this file by path)."""

# restructure-shim: probe.sdk.capture.logs.logs permanent
import os
import sys

if __name__ == "__main__":
    # The log helper runs its file by path under `-I -S` (no site-packages, no package): a process
    # that loaded an older release finds this stub there, so run the moved file the same way.
    import runpy

    runpy.run_path(os.path.join(os.path.dirname(os.path.abspath(__file__)), "capture", "logs", "logs.py"),
                   run_name="__main__")
else:
    import importlib

    sys.modules[__name__] = importlib.import_module("probe.sdk.capture.logs.logs")
