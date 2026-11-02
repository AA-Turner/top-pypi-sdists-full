"""Moved to `probe.service.watch.statepost` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.watch.statepost
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.watch.statepost")
