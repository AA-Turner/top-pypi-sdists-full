"""Moved to :mod:`probe.analytics` (plan 2.11): the SDK needs it without
importing the CLI. This name stays importable and IS that package -- not a
re-export -- so `from probe.cli import telemetry` sees what the SDK sees. Patch
a name in the piece that defines it (`telemetry.sender._ensure_sender`): the
pieces call each other directly, not through this front door."""

import sys

from probe import analytics as _moved

sys.modules[__name__] = _moved
