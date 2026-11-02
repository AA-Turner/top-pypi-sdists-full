"""Moved to `probe.cli.install.integrations.integrations` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.install.integrations.integrations
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.install.integrations.integrations")
