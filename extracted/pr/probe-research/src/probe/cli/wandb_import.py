"""Moved to `probe.cli.commands.data.wandb` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.commands.data.wandb
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.commands.data.wandb")
