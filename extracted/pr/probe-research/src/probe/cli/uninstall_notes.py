"""Moved to `probe.cli.install.uninstall.unsent_notes` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.install.uninstall.unsent_notes
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.install.uninstall.unsent_notes")
