"""Moved to `probe.foundation.safe_warn.safe_warn` (agent:3); this path stays importable for one release."""

# restructure-shim: probe.foundation.safe_warn.safe_warn
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.safe_warn.safe_warn")
