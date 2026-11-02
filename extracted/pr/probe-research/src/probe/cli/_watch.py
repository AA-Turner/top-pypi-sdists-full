"""Moved to `probe.cli.commands.runs.watch_loop` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.commands.runs.watch_loop
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.commands.runs.watch_loop")
