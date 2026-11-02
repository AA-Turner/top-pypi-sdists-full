"""Moved to `probe.cli.install.identity_check` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.install.identity_check
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.install.identity_check")
