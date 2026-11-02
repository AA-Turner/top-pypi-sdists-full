"""Moved to `probe.cli.wizard.session.lock` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.wizard.session.lock
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.wizard.session.lock")
