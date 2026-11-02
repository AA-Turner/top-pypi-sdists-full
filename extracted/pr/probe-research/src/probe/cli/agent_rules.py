"""Moved to `probe.cli.wizard.apply.agent_rules` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.wizard.apply.agent_rules
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.wizard.apply.agent_rules")
