"""Moved to `probe.generated.enums` (agent:2); this path stays importable for one release."""

# restructure-shim: probe.generated.enums
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.generated.enums")
