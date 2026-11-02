"""Moved to `probe.cli.commands.ref_syntax` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.commands.ref_syntax
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.commands.ref_syntax")
