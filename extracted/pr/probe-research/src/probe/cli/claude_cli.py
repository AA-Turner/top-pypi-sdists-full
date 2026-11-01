"""Moved to `probe.shared.harness.harnesses.claude_code.binary` (agent:13); this path stays importable for one release."""

# restructure-shim: probe.shared.harness.harnesses.claude_code.binary
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.harness.harnesses.claude_code.binary")
