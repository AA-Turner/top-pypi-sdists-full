"""The plugin's vendored `_session_marker` must match the canonical one.

`plugins/probe-research/hooks/_session_marker.py` is a COPY of
`src/probe/sdk/session_marker.py`, for the same reason `_telemetry_core` is
copied: the status-line renderer and the refresh hook run under the SYSTEM
python3 with no probe package on their path, so a shared import is impossible.

`make sync-session-marker` reconciles them, and this guards it — the drift is
silent in the nastiest way available. Both sides are fail-soft by contract, so
two copies that disagree about the marker's filename, its expiry window or its
JSON keys do not error anywhere: the writer writes one shape, the reader reads
another and finds nothing, and the status line just says "untracked" forever.

Same contract as tests/test_telemetry_core_parity.py: guard it, never rely on
someone remembering.
"""

from __future__ import annotations

import filecmp
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_CANONICAL = _ROOT / "src" / "probe" / "sdk" / "session_marker.py"
_PLUGIN_COPY = _ROOT / "plugins" / "probe-research" / "hooks" / "_session_marker.py"


def test_plugin_copy_matches_canonical() -> None:
    assert _CANONICAL.is_file(), "canonical src/probe/sdk/session_marker.py is missing"
    assert _PLUGIN_COPY.is_file(), (
        "plugin copy of _session_marker.py is missing; run `make sync-session-marker`"
    )
    assert filecmp.cmp(_CANONICAL, _PLUGIN_COPY, shallow=False), (
        "plugins/probe-research/hooks/_session_marker.py has drifted from "
        "src/probe/sdk/session_marker.py — run `make sync-session-marker` (and add "
        "a plugin CHANGELOG line: it ships with the next plugin release)"
    )


_STANDALONE_PROBE = (
    "import sys, importlib.util; "
    f"spec = importlib.util.spec_from_file_location('m', {str(_PLUGIN_COPY)!r}); "
    "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); "
    "assert 'probe' not in sys.modules, 'the marker pulled in the probe package'; "
    "assert 'httpx' not in sys.modules, 'the marker pulled in httpx'; "
    "assert 'urllib.request' not in sys.modules, 'urllib.request costs ~23ms of "
    "startup on the render path'; "
    "print(m.render({'project': 'folding'}, configured=True, tracking=True, color=False))"
)


def test_vendored_copy_stands_up_with_no_probe_package() -> None:
    """Stdlib-only, and specifically WITHOUT the expensive stdlib.

    The import assertion is a performance regression guard with teeth: this runs
    once per status-line render, and `urllib.request` alone doubled the time. A
    future edit reaching for it would not fail any behavioural test.
    """
    result = subprocess.run(
        [sys.executable, "-c", _STANDALONE_PROBE], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "● tracking → folding"


def test_vendored_copy_runs_under_the_system_python() -> None:
    """The renderer executes under /usr/bin/python3 (macOS ships 3.9). An edit
    using newer syntax goes green under the dev interpreter and then renders
    nothing at all in the field, on every prompt."""
    import os

    system_python = "/usr/bin/python3"
    if not os.path.exists(system_python):
        import pytest

        pytest.skip("no system python3 on this machine")
    result = subprocess.run(
        [system_python, "-c", _STANDALONE_PROBE], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "● tracking → folding"
