"""Moved to `probe.cli.imports.folder.record.tool` (agent:14); this path keeps working for good
(a record session's `probe` launcher imports `main` from it)."""

# restructure-shim: probe.cli.imports.folder.record.tool permanent
import importlib
import runpy
import sys

if __name__ == "__main__":
    runpy.run_module("probe.cli.imports.folder.record.tool", run_name="__main__", alter_sys=True)
else:
    sys.modules[__name__] = importlib.import_module("probe.cli.imports.folder.record.tool")
