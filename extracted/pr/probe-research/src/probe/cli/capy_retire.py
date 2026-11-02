"""Moved to `probe.cli.install.capy_retire` (agent:14); this path stays importable for one release."""

# restructure-shim: probe.cli.install.capy_retire
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.cli.install.capy_retire")
