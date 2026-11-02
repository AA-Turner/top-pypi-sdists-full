"""Moved to `probe.cli.imports.folder.classify.plan_tool` (agent:14); `python -m probe.cli.backfill_plan_tool` keeps working for one release."""

# restructure-shim: probe.cli.imports.folder.classify.plan_tool
import importlib
import runpy
import sys

if __name__ == "__main__":
    runpy.run_module("probe.cli.imports.folder.classify.plan_tool", run_name="__main__", alter_sys=True)
else:
    sys.modules[__name__] = importlib.import_module("probe.cli.imports.folder.classify.plan_tool")
