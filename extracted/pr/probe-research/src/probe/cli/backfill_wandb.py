"""Moved to `probe.cli.imports.folder.sources.wandb` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.imports.folder.sources.wandb
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.imports.folder.sources.wandb")
