"""Moved to `probe.shared.harness.harnesses.pi.pins` (agent:13); `python -m probe.cli.pi_pins` keeps working for good (an entry path older installs run)."""

# restructure-shim: probe.shared.harness.harnesses.pi.pins permanent
import importlib
import runpy
import sys

if __name__ == "__main__":
    runpy.run_module("probe.shared.harness.harnesses.pi.pins", run_name="__main__", alter_sys=True)
else:
    sys.modules[__name__] = importlib.import_module("probe.shared.harness.harnesses.pi.pins")
