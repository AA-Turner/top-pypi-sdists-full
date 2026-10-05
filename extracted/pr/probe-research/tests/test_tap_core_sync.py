"""The tap plugin's transcript-contract modules must match the canonical ones.

`plugins/probe-research-tap/tap/{sanitize,codex_sanitize,transcript}.py` are
COPIES of `src/probe/tap_core/`, not imports: the tap is a separate
distribution running under the SYSTEM python3 with only the plugin root on
sys.path, so it cannot import probe — and the CLI cannot import tap. The
backfill CLI and the live tap must produce identical wire shapes (same
sanitizer, same chunking, same byte-cursor discipline), which is exactly the
property that drifts silently: both copies keep working, they just record the
same session two different ways.

`make sync-tap-core` reconciles them. Same contract as
tests/test_policy_sync.py, tests/test_telemetry_core_parity.py and
tests/test_session_marker_parity.py: guard it, never rely on someone
remembering.
"""

from __future__ import annotations

import filecmp
import subprocess
import sys
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parent.parent
_CANONICAL_DIR = _ROOT / "src" / "probe" / "tap_core"
_PLUGIN_DIR = _ROOT / "plugins" / "probe-research-tap" / "tap"

_SYNCED = (
    "sanitize.py",
    "codex_sanitize.py",
    "transcript.py",
    "pi_sanitize.py",
    "kimi_sanitize.py",
    "session_journal.py",
    "session_identity.py",
    "secrets.py",
)


@pytest.mark.parametrize("name", _SYNCED)
def test_plugin_copy_matches_canonical(name: str) -> None:
    canonical = _CANONICAL_DIR / name
    plugin_copy = _PLUGIN_DIR / name
    assert canonical.is_file(), f"canonical src/probe/tap_core/{name} is missing"
    assert plugin_copy.is_file(), (
        f"plugin copy of {name} is missing; run `make sync-tap-core`"
    )
    assert filecmp.cmp(canonical, plugin_copy, shallow=False), (
        f"plugins/probe-research-tap/tap/{name} has drifted from "
        f"src/probe/tap_core/{name} — run `make sync-tap-core` "
        "(edit the canonical file, never the plugin copy)"
    )


@pytest.mark.parametrize("name", _SYNCED)
def test_synced_files_use_only_relative_cross_imports(name: str) -> None:
    """Identical bytes must resolve in BOTH packages (tap and probe.tap_core).

    An absolute `from tap...` or `from probe...` import inside a synced file
    would work in one home and break in the other — and which one breaks
    depends on which side the author tested. Relative imports resolve in both.
    Parsed with ast, not grepped: docstrings legitimately mention the words.
    """
    import ast

    tree = ast.parse((_CANONICAL_DIR / name).read_text())
    offenders: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            offenders.extend(
                a.name for a in node.names
                if a.name.split(".")[0] in ("tap", "probe")
            )
        elif isinstance(node, ast.ImportFrom) and node.level == 0:
            root = (node.module or "").split(".")[0]
            if root in ("tap", "probe"):
                offenders.append(node.module or "")
    assert not offenders, (
        f"src/probe/tap_core/{name} has absolute imports {offenders}: synced "
        "files must use relative imports (`from .sanitize import ...`) so the "
        "same bytes resolve as both tap.* and probe.tap_core.*"
    )


def test_plugin_copies_import_standalone_without_probe() -> None:
    """The property the copies exist for, tested the way they actually run.

    The tap runs as `PYTHONPATH=<plugin_root> python3 -m tap ...` — no probe
    package anywhere on sys.path. Import the three synced modules in a child
    whose path holds only the plugin root and confirm nothing from probe was
    pulled in.
    """
    probe_script = (
        "import sys; "
        "from tap import sanitize, codex_sanitize, transcript, pi_sanitize, kimi_sanitize; "
        "assert 'probe' not in sys.modules, 'plugin copy pulled in probe'; "
        "assert sanitize.sanitize_event({'type': 'ai-title'}) is None; "
        "assert codex_sanitize.sanitize_event({'type': 'world_state'}) is None; "
        "assert pi_sanitize.sanitize_event({'type': 'session', 'cwd': '/x'})"
        "['subtype'] == 'session_meta'; "
        "assert kimi_sanitize.sanitize_event({'type': 'llm.request'}) is None; "
        "print(transcript.MAX_BATCH_BYTES)"
    )
    result = subprocess.run(
        [sys.executable, "-c", probe_script],
        cwd=str(_PLUGIN_DIR.parent),
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"tap copies do not import standalone: {result.stderr}"
    )
    assert result.stdout.strip() == str(1024 * 1024)


def test_canonical_modules_import_without_tap() -> None:
    """The mirror property: probe.tap_core must stand alone without tap.

    Subprocess for the same reason as the plugin-side test: sys.modules in the
    pytest process is shared state, and the claim is about a fresh interpreter.
    """
    probe_script = (
        "import sys; "
        "from probe.tap_core import sanitize, codex_sanitize, transcript, pi_sanitize, kimi_sanitize; "
        "assert 'tap' not in sys.modules, 'probe.tap_core pulled in tap'; "
        "assert transcript.chunk_lines([b'a'*10, b'b'*10], 15) "
        "== [[b'a'*10], [b'b'*10]]; "
        "assert pi_sanitize.sanitize_event({'type': 'session', 'cwd': '/x'})"
        "['subtype'] == 'session_meta'; "
        "assert kimi_sanitize.sanitize_event({'type': 'metadata'})['subtype'] == 'session_meta'; "
        "print('ok')"
    )
    result = subprocess.run(
        [sys.executable, "-c", probe_script],
        capture_output=True,
        text=True,
        timeout=30,
    )
    assert result.returncode == 0, (
        f"probe.tap_core does not import standalone: {result.stderr}"
    )
    assert result.stdout.strip() == "ok"
