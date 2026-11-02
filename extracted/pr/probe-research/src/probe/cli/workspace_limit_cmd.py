"""Moved to `probe.cli.commands.account.workspace_limit` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.commands.account.workspace_limit
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.commands.account.workspace_limit")
