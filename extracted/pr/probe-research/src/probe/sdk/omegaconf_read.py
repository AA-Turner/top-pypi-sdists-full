"""Moved to `probe.sdk.values.omegaconf_read` (agent:6); this path stays importable for one release."""

# restructure-shim: probe.sdk.values.omegaconf_read
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.values.omegaconf_read")
