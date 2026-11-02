"""Moved to `probe.cli.commands.projects.filed_workspace` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.commands.projects.filed_workspace
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.commands.projects.filed_workspace")
