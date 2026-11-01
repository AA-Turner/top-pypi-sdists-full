"""Moved to `probe.shared.harness.session_filter` (agent:13); this path stays importable for one release."""

# restructure-shim: probe.shared.harness.session_filter
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.harness.session_filter")
