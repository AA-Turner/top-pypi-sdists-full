"""Moved to `probe.daemon.shell.command_check` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.shell.command_check
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.shell.command_check")
