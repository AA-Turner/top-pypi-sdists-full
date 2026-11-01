"""Moved to `probe.foundation.tls.network_down` (agent:3); this path stays importable for one release."""

# restructure-shim: probe.foundation.tls.network_down
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.tls.network_down")
