"""Moved to `probe.sdk.catalog.vocab` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.catalog.vocab
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.catalog.vocab")
