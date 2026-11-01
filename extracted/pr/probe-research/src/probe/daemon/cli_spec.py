"""Moved to `probe.shared.command_rules.cli_spec` (agent:12); `python -m probe.daemon.cli_spec` keeps working for good (an entry path older installs run)."""

# restructure-shim: probe.shared.command_rules.cli_spec permanent
import importlib
import runpy
import sys

if __name__ == "__main__":
    runpy.run_module("probe.shared.command_rules.cli_spec", run_name="__main__", alter_sys=True)
else:
    sys.modules[__name__] = importlib.import_module("probe.shared.command_rules.cli_spec")
