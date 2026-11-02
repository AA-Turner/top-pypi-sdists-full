"""Moved to `probe.cli.install.uninstall` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.install.uninstall
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.install.uninstall")
