"""Moved to `probe.analytics.report_policy` (agent:4); this path stays importable for one release."""

# restructure-shim: probe.analytics.report_policy
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.analytics.report_policy")
