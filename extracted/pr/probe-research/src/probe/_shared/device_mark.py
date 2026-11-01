"""Moved to `probe.foundation.remote_settings.remote_settings` (agent:3); this path stays importable for one release."""

# restructure-shim: probe.foundation.remote_settings.remote_settings
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.remote_settings.remote_settings")
