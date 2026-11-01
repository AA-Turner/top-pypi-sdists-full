"""Moved to `probe.sdk.run.context.failure` (agent:10); this path stays importable for one release."""

# restructure-shim: probe.sdk.run.context.failure
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.run.context.failure")
