"""Moved to `probe.cli.imports.folder.coverage` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.imports.folder.coverage
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.imports.folder.coverage")
