"""Moved to `probe.sdk.settings.key_refusal` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.settings.key_refusal
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.settings.key_refusal")
