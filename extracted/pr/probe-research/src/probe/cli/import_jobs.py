"""Moved to `probe.cli.imports.jobs` (agent:14); `python -m probe.cli.import_jobs` keeps working for good
(the Probe service starts every import worker by this name)."""

# restructure-shim: probe.cli.imports.jobs permanent
import importlib
import sys

if __name__ == "__main__":
    # The worker runs in the one runner module every piece and hook shares (its door loads
    # it), never a second copy under `__main__`.
    importlib.import_module("probe.cli.imports.jobs.runner").main()
else:
    sys.modules[__name__] = importlib.import_module("probe.cli.imports.jobs")
