"""Moved to `probe.integrations.miles.dashboard` (W1); `python -m probe.integrations.miles_dashboard` keeps working for good."""

# restructure-shim: probe.integrations.miles.dashboard permanent
import importlib
import sys

if __name__ == "__main__":
    from probe.integrations.miles.dashboard import main

    main()
else:
    sys.modules[__name__] = importlib.import_module("probe.integrations.miles.dashboard")
