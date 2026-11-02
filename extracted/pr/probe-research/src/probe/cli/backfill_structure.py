"""Moved to `probe.cli.imports.folder.structure` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.imports.folder.structure
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.imports.folder.structure")
