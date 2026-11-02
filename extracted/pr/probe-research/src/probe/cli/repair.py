"""Moved to `probe.cli.install.repair` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.install.repair
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.install.repair")
