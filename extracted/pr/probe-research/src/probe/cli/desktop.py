"""Moved to `probe.cli.imports.desktop` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.imports.desktop
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.imports.desktop")
