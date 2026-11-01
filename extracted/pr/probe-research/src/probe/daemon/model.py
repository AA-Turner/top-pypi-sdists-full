"""Moved to `probe.daemon.agent.model.model` (agent:15); this path stays importable for one release."""

# restructure-shim: probe.daemon.agent.model.model
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.daemon.agent.model.model")
