"""Moved to `probe.sdk.delivery.outbox` (agent:7); `python -m probe.sdk.outbox_worker` keeps working for good (an entry path older installs run)."""

# restructure-shim: probe.sdk.delivery.outbox permanent
import importlib
import sys

if __name__ == "__main__":
    # The door has loaded the worker already: run it there. runpy would exec a second copy,
    # with a RuntimeWarning that `-W error` (inherited by spawned workers) makes fatal.
    from probe.sdk.delivery.outbox.outbox import main

    sys.exit(main(sys.argv[1:]))
else:
    sys.modules[__name__] = importlib.import_module("probe.sdk.delivery.outbox")
