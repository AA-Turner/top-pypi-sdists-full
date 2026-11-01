"""Moved to `probe.shared.updates.finisher` (agent:12); `python -m probe._shared.finisher` keeps working for one release."""

# restructure-shim: probe.shared.updates.finisher
import importlib
import runpy
import sys

if __name__ == "__main__":
    runpy.run_module("probe.shared.updates.finisher", run_name="__main__", alter_sys=True)
else:
    sys.modules[__name__] = importlib.import_module("probe.shared.updates.finisher")
