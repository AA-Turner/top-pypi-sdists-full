"""Moved to `probe.sdk.settings.settings` (agent:6). Kept while released hooks import it: the
vendored `_session_marker.py` imports `probe.sdk.config` so it works against every CLI version."""

# restructure-shim: probe.sdk.settings.settings
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.settings.settings")
