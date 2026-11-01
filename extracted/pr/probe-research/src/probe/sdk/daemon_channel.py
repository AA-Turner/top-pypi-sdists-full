"""Moved to `probe.sdk.run.launch.daemon_channel` (agent:10); this path stays importable for one release."""

# restructure-shim: probe.sdk.run.launch.daemon_channel
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.sdk.run.launch.daemon_channel")
