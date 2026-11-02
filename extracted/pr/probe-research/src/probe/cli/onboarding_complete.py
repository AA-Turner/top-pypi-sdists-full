"""Moved to `probe.cli.wizard.account.onboarding_complete` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.wizard.account.onboarding_complete
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.wizard.account.onboarding_complete")
