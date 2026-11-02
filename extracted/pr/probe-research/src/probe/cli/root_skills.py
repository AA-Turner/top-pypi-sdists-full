"""Moved to `probe.cli.wizard.apply.root_skills` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.wizard.apply.root_skills
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.wizard.apply.root_skills")
