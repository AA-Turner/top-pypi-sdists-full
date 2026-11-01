"""Moved to `probe.sdk.artifact.storage_handlers.r2` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.artifact.storage_handlers.r2
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.artifact.storage_handlers.r2")
