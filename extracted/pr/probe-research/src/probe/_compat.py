"""Moved to `probe.foundation.compat.compat` (agent:3); this path stays importable for one release."""

# restructure-shim: probe.foundation.compat.compat
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.compat.compat")
