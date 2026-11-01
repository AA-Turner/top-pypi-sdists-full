"""Moved to `probe.sdk.settings.workspace_limit` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.settings.workspace_limit
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.settings.workspace_limit")
