"""Moved to `probe.cli.install.bootstrap` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.install.bootstrap
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.install.bootstrap")
