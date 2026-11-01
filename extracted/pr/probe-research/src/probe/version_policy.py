"""Moved to `probe.shared.updates.version_policy` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.updates.version_policy
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.updates.version_policy")
