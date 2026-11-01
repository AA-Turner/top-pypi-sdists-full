"""Moved to `probe.foundation.durable.durable` (agent:3); this path stays importable for one release."""

# restructure-shim: probe.foundation.durable.durable
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.foundation.durable.durable")
