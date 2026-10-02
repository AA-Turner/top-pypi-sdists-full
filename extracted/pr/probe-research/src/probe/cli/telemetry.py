"""Moved to :mod:`probe._shared.telemetry` (plan 2.11): the SDK needs it without
importing the CLI. This name stays importable and IS that module -- not a
re-export -- so `monkeypatch.setattr(probe.cli.telemetry, ...)` and every
`from probe.cli import telemetry` see exactly what the SDK sees."""

import sys

from probe._shared import telemetry as _moved

sys.modules[__name__] = _moved
