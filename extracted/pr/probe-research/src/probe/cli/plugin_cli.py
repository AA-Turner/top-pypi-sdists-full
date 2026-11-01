"""Moved to `probe.shared.harness.plugins` (agent:13); this path stays importable for one release."""

# restructure-shim: probe.shared.harness.plugins
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.harness.plugins")
