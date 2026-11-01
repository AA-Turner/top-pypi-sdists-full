"""Moved to `probe.foundation.request_identity.surface` (agent:3); this path stays importable for one release."""

# restructure-shim: probe.foundation.request_identity.surface
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.request_identity.surface")
