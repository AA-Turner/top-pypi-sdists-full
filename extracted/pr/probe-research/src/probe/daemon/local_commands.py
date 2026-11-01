"""Moved to `probe.daemon.shell.local_commands` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.shell.local_commands
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.shell.local_commands")
