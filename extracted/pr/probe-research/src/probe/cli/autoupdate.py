"""Moved to :mod:`probe.shared.updates.autoupdate` (Probe service, T4): the service
records its deferrals with it, and importing anything under `probe.cli` loads
the whole CLI. This name stays importable and IS that module -- not a
re-export -- so `monkeypatch.setattr(probe.cli.autoupdate, ...)` and every
`from probe.cli import autoupdate` see exactly what the service sees."""

import sys

from probe.shared.updates import autoupdate as _moved

sys.modules[__name__] = _moved
