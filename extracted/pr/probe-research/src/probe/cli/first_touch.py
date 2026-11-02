"""Moved to `probe.cli.commands.notes.first_touch` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.commands.notes.first_touch
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.commands.notes.first_touch")
