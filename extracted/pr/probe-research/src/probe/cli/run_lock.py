"""Moved to :mod:`probe._shared.run_lock` (plan 2.11): the SDK needs it without
importing the CLI. This name stays importable and IS that module -- not a
re-export -- so `monkeypatch.setattr(probe.cli.run_lock, ...)` and every
`from probe.cli import run_lock` see exactly what the SDK sees."""

import sys

from probe._shared import run_lock as _moved

sys.modules[__name__] = _moved
