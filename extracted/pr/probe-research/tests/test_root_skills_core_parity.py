"""The vendored root-skills core must not drift from the canonical one.

`plugins/*/hooks/_root_skills_core.py` is a COPY of
`src/probe/root_skills_core.py`, for the same reason `_session_marker.py` is: the
SessionStart hook runs under the SYSTEM python, where `probe` is not importable.
`make sync-root-skills-core` reconciles them.

A drifted copy is invisible in the worst way -- the CLI installs skills one way
and the hook refreshes them another, and the only symptom is a skill folder that
quietly stops matching the plugin.
"""

from __future__ import annotations

import filecmp
import os
import subprocess
import sys
from pathlib import Path

import pytest

AGENT = Path(__file__).resolve().parents[1]
CANONICAL = AGENT / "src" / "probe" / "root_skills_core.py"
COPIES = (
    AGENT / "plugins" / "probe-research" / "hooks" / "_root_skills_core.py",
    AGENT / "plugins" / "probe-research-daemon" / "hooks" / "_root_skills_core.py",
)
SYNCS = (
    AGENT / "plugins" / "probe-research" / "hooks" / "root_skills_sync.py",
    AGENT / "plugins" / "probe-research-daemon" / "hooks" / "root_skills_sync.py",
)


@pytest.mark.parametrize("copy", COPIES, ids=lambda p: p.parts[-3])
def test_the_vendored_core_matches_the_canonical_one(copy: Path) -> None:
    assert copy.is_file(), f"{copy} is missing; run `make sync-root-skills-core`"
    assert filecmp.cmp(CANONICAL, copy, shallow=False), (
        f"{copy} drifted from {CANONICAL} -- run `make sync-root-skills-core` "
        "(edit the canonical file, never the copy)"
    )


def test_both_plugins_ship_the_same_sync_hook() -> None:
    assert all(p.is_file() for p in SYNCS), "run `make sync-root-skills-core`"
    assert filecmp.cmp(*SYNCS, shallow=False)


def test_the_core_imports_only_the_stdlib() -> None:
    """It runs under the system python. One `probe` import makes the hook a
    no-op on every machine, silently."""
    text = CANONICAL.read_text(encoding="utf-8")
    assert "import probe" not in text and "from probe" not in text


def test_the_sync_hook_asks_the_registry_which_harness_it_is() -> None:
    """Both plugins' hooks fire under Codex and Kimi too, and those read the
    plugin's own `agent-skills/` -- writing into their homes would duplicate.
    The hook must ask the registry rather than name an agent: a literal is what
    `test_no_harness_literals` ratchets against, and it goes stale the first
    time a harness is added."""
    text = SYNCS[0].read_text(encoding="utf-8")
    assert "CAPABILITY_ROOT_SKILLS" in text and "get_registry().detect()" in text
    assert "claude_code" not in text and "CLAUDE_CONFIG_DIR" not in text


def _run_hook(plugin: Path, env: dict) -> int:
    """The hook as SessionStart runs it: a separate process, system python, no
    `probe` importable, nothing but the env it is given."""
    clean = {k: v for k, v in os.environ.items() if not k.startswith(("CLAUDE", "PROBE", "PI_", "KIMI"))}
    return subprocess.run(  # noqa: S603
        [sys.executable, str(plugin / "hooks" / "root_skills_sync.py")],
        env={**clean, **env}, capture_output=True, timeout=120, check=False,
    ).returncode


def test_the_hook_installs_the_skills_end_to_end(tmp_path) -> None:
    """Running the real file in a real subprocess, because grepping its text for
    a call proves only that the call is written down."""
    home = tmp_path / "claude"
    code = _run_hook(COPIES[0].parents[1], {"CLAUDE_CONFIG_DIR": str(home), "CLAUDECODE": "1"})

    assert code == 0
    installed = sorted(p.name for p in (home / "skills").iterdir() if p.is_dir())
    assert installed == sorted(p.parent.name for p in (AGENT / "plugins" / "probe-research"
                                                       / "agent-skills").glob("*/SKILL.md"))
    assert (home / "skills" / "probe" / ".probe-installed").is_file()


def test_the_hook_finds_its_own_plugin_without_any_env(tmp_path) -> None:
    """`session-start.sh` never exports PLUGIN_ROOT, so only Claude Code's own
    variable reaches the hook; an install that wires it without plugin-scoped
    env got no skills at all, silently, and the plugin no longer carries them."""
    home = tmp_path / "claude"
    code = _run_hook(COPIES[0].parents[1], {"CLAUDE_CONFIG_DIR": str(home), "CLAUDECODE": "1"})

    assert code == 0 and (home / "skills" / "probe" / "SKILL.md").is_file()


def test_the_hook_writes_nothing_for_another_harness(tmp_path) -> None:
    home = tmp_path / "codex"
    code = _run_hook(COPIES[0].parents[1], {"PROBE_TAP_SOURCE": "codex", "CODEX_HOME": str(home)})

    assert code == 0 and not (home / "skills").exists()
