"""Moved to `probe.cli.wizard.actions.onboarding` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.wizard.actions.onboarding
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.wizard.actions.onboarding")
