"""The plugin's vendored `_telemetry_core` must match the canonical one.

`plugins/probe-research/hooks/_telemetry_core.py` is a COPY of
`src/probe/sdk/_telemetry_core.py`, for the same hard reason as
version_policy.py: the hook runs under the SYSTEM python3 with no probe
package on its path, so a shared import is impossible and a shipped duplicate
is the only option.

`make sync-telemetry-core` reconciles them. This guards it, because the drift
is silent in the worst way — telemetry is fail-silent BY CONTRACT, so two
copies that disagree about the PostHog key, the killswitch spellings, the
identity cache path, or a property name do not error anywhere: the funnel
just splits into two half-populated ones, and the first detection is someone
staring at a broken dashboard weeks later.

Same contract as tests/test_policy_sync.py: guard it, never rely on someone
remembering.
"""

from __future__ import annotations

import filecmp
import subprocess
import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parent.parent
_CANONICAL = _ROOT / "src" / "probe" / "sdk" / "_telemetry_core.py"
_PLUGIN_COPY = _ROOT / "plugins" / "probe-research" / "hooks" / "_telemetry_core.py"


def test_plugin_core_copy_matches_canonical() -> None:
    assert _CANONICAL.is_file(), "canonical src/probe/sdk/_telemetry_core.py is missing"
    assert _PLUGIN_COPY.is_file(), (
        "plugin copy of _telemetry_core.py is missing; run `make sync-telemetry-core`"
    )
    assert filecmp.cmp(_CANONICAL, _PLUGIN_COPY, shallow=False), (
        "plugins/probe-research/hooks/_telemetry_core.py has drifted from "
        "src/probe/sdk/_telemetry_core.py — run `make sync-telemetry-core` "
        "(and add a plugin CHANGELOG line: core changes ship with the next "
        "plugin release)"
    )


_STANDALONE_PROBE = (
    "import sys, importlib.util; "
    f"spec = importlib.util.spec_from_file_location('c', {str(_PLUGIN_COPY)!r}); "
    "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); "
    "assert 'probe' not in sys.modules, 'core pulled in the probe package'; "
    "assert 'httpx' not in sys.modules, 'core pulled in httpx'; "
    "print(m.hosted_base_url('https://api.research.prbe.ai'))"
)


def test_vendored_core_stands_up_with_no_probe_package() -> None:
    """The copy must stay stdlib-only: it runs under system python3."""
    result = subprocess.run(
        [sys.executable, "-c", _STANDALONE_PROBE], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "True"


def test_vendored_core_runs_under_the_system_python() -> None:
    """The hook executes under /usr/bin/python3 (macOS ships 3.9) — a core
    edit using newer syntax would go green under the dev interpreter and then
    traceback on every tool call in the field. Checked against the real
    system interpreter when one exists; skipped where there is none (CI
    containers whose only python IS the dev one)."""
    import os

    system_python = "/usr/bin/python3"
    if not os.path.exists(system_python):
        import pytest

        pytest.skip("no system python3 on this machine")
    result = subprocess.run(
        [system_python, "-c", _STANDALONE_PROBE], capture_output=True, text=True, timeout=30
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "True"
