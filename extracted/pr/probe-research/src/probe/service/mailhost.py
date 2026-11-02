"""Moved to `probe.service.mail.mail` (agent:16); this path stays importable for one release."""

# restructure-shim: probe.service.mail.mail
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.service.mail.mail")
