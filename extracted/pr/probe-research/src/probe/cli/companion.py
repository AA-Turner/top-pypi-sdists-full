"""Moved to `probe.cli.commands.daemon.companion` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.commands.daemon.companion
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.commands.daemon.companion")
