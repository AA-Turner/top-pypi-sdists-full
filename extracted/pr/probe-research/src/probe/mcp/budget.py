"""Moved to `probe.foundation.token_budget.token_budget` (agent:3); this path stays importable for one release."""

# restructure-shim: probe.foundation.token_budget.token_budget
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.token_budget.token_budget")
