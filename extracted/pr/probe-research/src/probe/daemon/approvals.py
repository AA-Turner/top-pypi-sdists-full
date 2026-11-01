"""Moved to `probe.shared.mailbox.approvals` (agent:12); this path stays importable for one release."""

# restructure-shim: probe.shared.mailbox.approvals
import importlib
import sys

sys.modules[__name__] = importlib.import_module("probe.shared.mailbox.approvals")
