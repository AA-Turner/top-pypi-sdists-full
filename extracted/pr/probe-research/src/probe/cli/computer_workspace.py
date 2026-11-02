"""Moved to `probe.cli.wizard.account.computer_workspace` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.wizard.account.computer_workspace
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.wizard.account.computer_workspace")
