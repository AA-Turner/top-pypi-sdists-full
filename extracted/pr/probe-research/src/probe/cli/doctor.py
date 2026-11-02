"""Moved to `probe.cli.wizard.doctor` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.wizard.doctor
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.wizard.doctor")
