"""Moved to `probe.shared.command_rules.command_rules` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.command_rules.command_rules
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.command_rules.command_rules")
