"""Moved to `probe.shared.updates.handoff` (agent:12); `python -m probe._shared.handoff` keeps working for one release."""

# restructure-shim: probe.shared.updates.handoff
import importlib
import runpy
import sys

if __name__ == "__main__":
    runpy.run_module("probe.shared.updates.handoff", run_name="__main__", alter_sys=True)
else:
    sys.modules[__name__] = importlib.import_module("probe.shared.updates.handoff")
