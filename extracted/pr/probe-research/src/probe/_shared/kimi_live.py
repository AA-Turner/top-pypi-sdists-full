"""Moved to `probe.shared.harness.harnesses.kimi_code.live` (agent:13); this path stays importable for one release."""

# restructure-shim: probe.shared.harness.harnesses.kimi_code.live
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.harness.harnesses.kimi_code.live")
