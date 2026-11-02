"""Moved to `probe.foundation.service_api.winpipe` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.foundation.service_api.winpipe
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.service_api.winpipe")
