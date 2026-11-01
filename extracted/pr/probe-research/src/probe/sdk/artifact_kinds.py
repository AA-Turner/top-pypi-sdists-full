"""Moved to `probe.sdk.artifact.kinds` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.artifact.kinds
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.artifact.kinds")
