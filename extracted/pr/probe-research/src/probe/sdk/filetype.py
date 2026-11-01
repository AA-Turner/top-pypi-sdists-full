"""Moved to `probe.sdk.artifact.filetype` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.artifact.filetype
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.artifact.filetype")
