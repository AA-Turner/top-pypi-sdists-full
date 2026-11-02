"""Moved to `probe.cli.wizard.session.on_service` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.wizard.session.on_service
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.wizard.session.on_service")
