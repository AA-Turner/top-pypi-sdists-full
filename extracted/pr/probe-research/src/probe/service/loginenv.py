"""Moved to `probe.service.actions.loginenv` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.actions.loginenv
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.actions.loginenv")
