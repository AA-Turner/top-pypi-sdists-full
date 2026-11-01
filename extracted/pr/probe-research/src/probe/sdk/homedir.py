"""Moved to `probe.foundation.durable.homedir` (agent:3). Kept while released hooks import it: the
vendored `_session_marker.py` imports `probe.sdk.homedir` so it works against every CLI version."""

# restructure-shim: probe.foundation.durable.homedir
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.durable.homedir")
