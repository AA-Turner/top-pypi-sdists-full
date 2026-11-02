"""Moved to `probe.foundation.service_api.paths` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.foundation.service_api.paths
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.service_api.paths")
