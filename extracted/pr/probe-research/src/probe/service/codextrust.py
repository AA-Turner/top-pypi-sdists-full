"""Moved to `probe.service.hooks.codex_trust` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.hooks.codex_trust
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.hooks.codex_trust")
