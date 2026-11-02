"""Moved to `probe.service.mail.watch` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.mail.watch
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.mail.watch")
