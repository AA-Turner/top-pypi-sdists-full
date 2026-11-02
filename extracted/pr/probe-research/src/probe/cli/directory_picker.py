"""Moved to `probe.cli.wizard.terminal.directory_picker` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.wizard.terminal.directory_picker
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.wizard.terminal.directory_picker")
