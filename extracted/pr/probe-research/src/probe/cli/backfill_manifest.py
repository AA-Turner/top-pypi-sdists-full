"""Moved to `probe.cli.imports.folder.upload.manifest` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.imports.folder.upload.manifest
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.imports.folder.upload.manifest")
