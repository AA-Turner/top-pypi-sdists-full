"""Moved to `probe.shared.reads.search_contract` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.reads.search_contract
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.reads.search_contract")
