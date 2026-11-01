"""Moved to `probe.foundation.harness_registry.harness_registry` (agent:3); this path stays importable for one release."""

# restructure-shim: probe.foundation.harness_registry.harness_registry
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.harness_registry.harness_registry")
