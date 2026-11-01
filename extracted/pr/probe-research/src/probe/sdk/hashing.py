"""Moved to `probe.sdk.artifact.hashing` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.artifact.hashing
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.artifact.hashing")
