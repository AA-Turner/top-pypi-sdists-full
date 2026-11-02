"""Moved to `probe.cli.imports.folder.structure.projects` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.imports.folder.structure.projects
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.imports.folder.structure.projects")
