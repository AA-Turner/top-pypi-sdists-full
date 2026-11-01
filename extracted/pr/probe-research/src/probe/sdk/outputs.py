"""Moved to `probe.sdk.capture.outputs` (agent:11); `python -m probe.sdk.outputs` keeps working for good (the log helper of every release runs it)."""

# restructure-shim: probe.sdk.capture.outputs permanent
import importlib
import sys

if __name__ == "__main__":
    # The door has loaded recovery already: run it there. runpy would exec a second copy,
    # with a RuntimeWarning that `-W error` (inherited by spawned workers) makes fatal.
    from probe.sdk.capture.outputs.recovery import run_command

    run_command(sys.argv[1:])
else:
    sys.modules[__name__] = importlib.import_module("probe.sdk.capture.outputs")
