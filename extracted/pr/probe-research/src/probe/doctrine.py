"""Moved to `probe.foundation.skills.doctrine` (agent:3); this path stays importable for one release."""

# restructure-shim: probe.foundation.skills.doctrine
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.skills.doctrine")
