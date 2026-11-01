"""Moved to `probe.generated.models` (agent:2); this path stays importable for one release."""

# restructure-shim: probe.generated.models
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.generated.models")
