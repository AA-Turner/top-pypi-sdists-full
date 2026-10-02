"""Two filesystem conventions, seven hand-written mirrors each. Pin them together.

A capture daemon and everything that reports on one never talk. They agree by
computing the SAME two paths independently:

  * the watcher prefix — `/tmp/<prefix>-watcher-<session_id>.pid` and its
    `.shutdown` sibling, the only fact that says a daemon is live;
  * the tap's state directory — which holds `.token`, `.disabled`,
    `.disabled_paths`, `state.db`, `logs/` and `heal/<session_id>`.

`tap/config.py` is the source of truth for both (over `tap/sources.py`'s
registry rows). Nothing else can import it: the tap is a separately installable
package living in a coding agent's plugin cache, the probe CLI is a different
distribution, the hooks run under the SYSTEM python3 with neither package on
their path, and `paths.ts` is TypeScript in a third process. So every other home
is a hand-written mirror, and this test is the only thing that keeps them equal.

DRIFT HERE IS SILENT IN BOTH DIRECTIONS, which is why it gets a test rather
than a comment. A wrong prefix finds no pid file and reads as "no daemon", so a
live capture is reported as broken. A wrong state dir finds no `.disabled` and
no `heal/` marker, so a killswitch reads as a crash and the ten-minute heal
bound quietly becomes two independent windows, each blind to the other.

Same shape as `test_telemetry_core_parity.py` — the house pattern for a
sanctioned duplicate: assert the canonical behaviour by running it, then assert
each copy against it.
"""

from __future__ import annotations

import importlib.util
import json
import os
import re
import subprocess
import sys
import uuid
from pathlib import Path

import pytest

_ROOT = Path(__file__).resolve().parents[2]
_AGENT = _ROOT / "agent"
_TAP_ROOT = _AGENT / "plugins" / "probe-research-tap"
_REFRESH = _AGENT / "plugins" / "probe-research" / "hooks" / "statusline_refresh.py"

#: `tap/config.py::watcher_prefix()` — codex is the only source that differs.
EXPECTED_PREFIX = {
    "claude_code": "probe-research-tap",
    "codex": "prbe-codex-tap",
    "pi": "probe-research-tap",
}

#: `tap/config.py::plugin_dir()` over `tap/sources.py::plugin_state_dir()`:
#: (env override, default path relative to $HOME).
EXPECTED_PLUGIN_DIR = {
    "claude_code": ("PROBE_RESEARCH_TAP_PLUGIN_DIR", ".claude/plugins/probe-research-tap"),
    "codex": ("PRBE_CODEX_TAP_PLUGIN_DIR", ".codex/state/probe-research-tap"),
    "pi": ("PROBE_PI_TAP_PLUGIN_DIR", ".pi/agent/state/probe-research-tap"),
}

#: The one-way fallback in `plugin_dir()`: a standalone Codex tap keeps the
#: state directory it already has; a clean install gets the unified name.
CODEX_LEGACY_DIR = ".codex/state/prbe-codex-tap-plugin"

#: Every hand-written mirror of the WATCHER PREFIX, found by reading the tree
#: rather than by trusting a list. A new one belongs here the day it is written.
PREFIX_MIRRORS = (
    "agent/plugins/probe-research-pi/src/paths.ts",
    "agent/plugins/probe-research-tap/hooks/session-start.sh",
    "agent/plugins/probe-research-tap/hooks/session-end.sh",
    "agent/plugins/probe-research-tap/hooks/ensure-daemon.sh",
    "agent/plugins/probe-research/hooks/statusline_refresh.py",
    "agent/src/probe/cli/capture_state.py",
    "agent/src/probe/cli/capture.py",
)

#: Every hand-written mirror of the TAP STATE DIRECTORY. `version_check.py` and
#: `agent_session.py` read a different file out of it (`.installed_version`,
#: `.token`) but resolve the same directory, legacy fallback included, so they
#: drift the same way.
PLUGIN_DIR_MIRRORS = (
    "agent/plugins/probe-research-pi/src/paths.ts",
    "agent/plugins/probe-research-tap/hooks/session-start.sh",
    "agent/plugins/probe-research-tap/hooks/ensure-daemon.sh",
    "agent/plugins/probe-research/hooks/statusline_refresh.py",
    "agent/plugins/probe-research/hooks/version_check.py",
    "agent/src/probe/cli/capabilities.py",
    "agent/src/probe/sdk/agent_session.py",
)


def _text(rel: str) -> str:
    path = _ROOT / rel
    assert path.is_file(), f"{rel} is gone — a mirror was deleted or moved"
    return path.read_text(encoding="utf-8")


# --- the source of truth, asked rather than described ----------------------


def _ask_the_tap(source: str, home: Path, overrides: dict[str, str] | None = None) -> dict:
    """Run `tap/config.py` itself and report what it computes for `source`.

    A subprocess with `PYTHONPATH` at the plugin root, like
    `test_telemetry_core_parity.py`'s standalone probe: the tap is not
    importable from this suite's environment, and importing it by path would
    put a half-initialised `tap` package into every later test's `sys.modules`.
    """
    env = {
        "PATH": os.environ.get("PATH", ""),
        "HOME": str(home),
        "PYTHONPATH": str(_TAP_ROOT),
        "PROBE_TAP_SOURCE": source,
        **(overrides or {}),
    }
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import json;"
            "from tap import config as cfg;"
            "print(json.dumps({"
            "'source': cfg.capture_source(),"
            "'prefix': cfg.watcher_prefix(),"
            "'plugin_dir': str(cfg.plugin_dir()),"
            "'pid_file': str(cfg.pid_file('S')),"
            "'sentinel': str(cfg.shutdown_sentinel('S')),"
            "'heal_marker': str(cfg.heal_marker('S')),"
            "}))",
        ],
        capture_output=True,
        text=True,
        timeout=60,
        env=env,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    return json.loads(result.stdout)


@pytest.mark.parametrize("source", sorted(EXPECTED_PREFIX))
def test_the_tap_defines_the_prefix_every_mirror_copies(source, tmp_path):
    answer = _ask_the_tap(source, tmp_path)
    assert answer["source"] == source
    assert answer["prefix"] == EXPECTED_PREFIX[source]
    assert answer["pid_file"] == f"/tmp/{EXPECTED_PREFIX[source]}-watcher-S.pid"
    assert answer["sentinel"] == f"/tmp/{EXPECTED_PREFIX[source]}-watcher-S.shutdown"


@pytest.mark.parametrize("source", sorted(EXPECTED_PLUGIN_DIR))
def test_the_tap_defines_the_state_dir_every_mirror_copies(source, tmp_path):
    env_name, relative = EXPECTED_PLUGIN_DIR[source]

    answer = _ask_the_tap(source, tmp_path)
    assert answer["plugin_dir"] == str(tmp_path / relative)
    assert answer["heal_marker"] == str(tmp_path / relative / "heal" / "S")

    elsewhere = tmp_path / "elsewhere"
    overridden = _ask_the_tap(source, tmp_path, {env_name: str(elsewhere)})
    assert overridden["plugin_dir"] == str(elsewhere), (
        f"{source}'s plugin-dir override is not {env_name}"
    )


def test_the_codex_legacy_state_dir_is_a_one_way_fallback(tmp_path):
    """An existing standalone install keeps its directory; a clean one does not."""
    clean = _ask_the_tap("codex", tmp_path)
    assert clean["plugin_dir"] == str(tmp_path / EXPECTED_PLUGIN_DIR["codex"][1])

    legacy_home = tmp_path / "legacy"
    (legacy_home / CODEX_LEGACY_DIR).mkdir(parents=True)
    migrated = _ask_the_tap("codex", legacy_home)
    assert migrated["plugin_dir"] == str(legacy_home / CODEX_LEGACY_DIR)

    both = tmp_path / "both"
    (both / CODEX_LEGACY_DIR).mkdir(parents=True)
    (both / EXPECTED_PLUGIN_DIR["codex"][1]).mkdir(parents=True)
    assert _ask_the_tap("codex", both)["plugin_dir"] == str(
        both / EXPECTED_PLUGIN_DIR["codex"][1]
    ), "once the unified directory exists it wins — the fallback is one-way"


def test_the_tap_source_of_truth_is_still_one_ternary():
    """MUTANT: a second source-dependent prefix in `config.py` -> red.

    `watcher_prefix()` is where the whole convention is decided. If it grows a
    branch, every mirror below needs the same branch, and the literal-equality
    assertions in this file would keep passing while the shapes diverged.
    """
    src = _text("agent/plugins/probe-research-tap/tap/config.py")
    match = re.search(r'return "([\w-]+)" if capture_source\(\) == "codex" else (\w+)', src)
    assert match is not None, "tap/config.py::watcher_prefix() changed shape"
    assert match.group(1) == EXPECTED_PREFIX["codex"]
    assert match.group(2) == "PLUGIN_NAME"


# --- the mirrors -----------------------------------------------------------


@pytest.mark.parametrize("rel", PREFIX_MIRRORS)
def test_every_prefix_mirror_carries_both_literals(rel):
    """Both spellings, in every mirror — including the one that only explains itself.

    `paths.ts` is pi-only and takes the default branch, so it never *uses* the
    codex prefix; it carries the literal in the comment saying why pi shares
    Claude Code's. That comment is the whole reason a later reader does not
    invent `probe-research-pi-watcher-*` and leave the daemon unable to see its
    own shutdown sentinel, so losing it is losing the convention.
    """
    src = _text(rel)
    for prefix in sorted(set(EXPECTED_PREFIX.values())):
        assert prefix in src, f"{rel} lost the {prefix!r} watcher prefix"


def test_the_typescript_mirror_pins_the_prefix_as_a_constant():
    src = _text("agent/plugins/probe-research-pi/src/paths.ts")
    assert f'WATCHER_PREFIX = "{EXPECTED_PREFIX["pi"]}"' in src
    assert "`${WATCHER_PREFIX}-watcher-${sessionId}.pid`" in src
    assert "`${WATCHER_PREFIX}-watcher-${sessionId}.shutdown`" in src


@pytest.mark.parametrize("rel", PLUGIN_DIR_MIRRORS)
def test_every_state_dir_mirror_names_the_right_env_var(rel):
    """A mirror that reads the wrong env var silently ignores every override.

    Each mirror covers the sources it can actually see — `paths.ts` is pi-only,
    `version_check.py` and `agent_session.py` predate pi — so this asserts that
    whatever a mirror DOES claim about a source is the tap's own answer, not
    that every mirror claims all three.
    """
    src = _text(rel)
    claimed = [s for s, (env, _) in EXPECTED_PLUGIN_DIR.items() if env in src]
    assert claimed, f"{rel} names no tap plugin-dir env var at all"
    for source in claimed:
        relative = EXPECTED_PLUGIN_DIR[source][1]
        # `~/.claude/plugins/probe-research-tap` is spelled in segments by the
        # Python homes and as a literal by the shell ones; the tail segment
        # plus the parent directory is what every spelling shares.
        parent, leaf = relative.rsplit("/", 1)
        assert leaf in src, f"{rel} lost {source}'s state-dir name"
        assert any(part in src for part in parent.split("/")), (
            f"{rel} lost {source}'s state-dir root ({parent})"
        )


def test_the_codex_legacy_fallback_is_mirrored_wherever_codex_is_resolved():
    """Every home that resolves Codex's state dir keeps the one-way fallback.

    Dropping it does not error anywhere: it silently points at an empty
    directory, so a paired standalone tap reads as unpaired and uninstalled.
    """
    for rel in PLUGIN_DIR_MIRRORS:
        src = _text(rel)
        if EXPECTED_PLUGIN_DIR["codex"][0] not in src:
            continue
        assert "prbe-codex-tap-plugin" in src, f"{rel} resolves codex without the legacy fallback"


# --- the two live implementations must AGREE, not merely look alike --------


@pytest.fixture
def hook():
    """`statusline_refresh.py` loaded the way its hook runner loads it."""
    spec = importlib.util.spec_from_file_location("statusline_refresh_parity", _REFRESH)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


#: UNIQUE PER PROCESS, not the fixture uuid the sibling suites share. The pid
#: file this id names is a real path in a real `/tmp` — that is the convention
#: under test, so it cannot be redirected into `tmp_path` — and CI runs the
#: suite `-n auto`, where a shared id means one worker unlinking another's file
#: mid-assertion. A per-worker id makes the collision impossible rather than
#: unlikely.
SID = f"parity-{os.getpid()}-{uuid.uuid4()}"

_SOURCES = ("claude_code", "codex", "pi")


@pytest.fixture
def both(hook, monkeypatch, tmp_path):
    """Ask the hook and the CLI the same question about the same fixture.

    These are the two implementations a person actually reads: the Claude Code
    status segment renders the hook's answer out of the marker, and
    `probe session status` / `probe doctor` render the CLI's. They must not
    disagree about the same machine.

    `_looks_like_the_uploader` is the ONE documented divergence — the CLI asks
    `/bin/ps` what a live pid IS, the hook takes it at face value because it
    runs every few seconds for the life of a session — so it is stubbed out
    rather than compared.
    """
    from probe.cli import capture_state

    monkeypatch.setattr(capture_state, "_looks_like_the_uploader", lambda pid: True)

    def ask(source: str) -> tuple[dict, dict]:
        state_dir = tmp_path / source
        monkeypatch.setenv("PROBE_AGENT", source)
        for env_name, _ in EXPECTED_PLUGIN_DIR.values():
            monkeypatch.delenv(env_name, raising=False)
        monkeypatch.setenv(EXPECTED_PLUGIN_DIR[source][0], str(state_dir))
        cli = capture_state.session_capture_state(SID, source)
        return (
            hook._capture_reading(SID),
            {"running": cli.running, "reason": cli.reason},
        )

    return ask


def _pid_path(source: str) -> Path:
    return Path("/tmp") / f"{EXPECTED_PREFIX[source]}-watcher-{SID}.pid"


@pytest.mark.parametrize("source", _SOURCES)
def test_no_state_dir_reads_not_installed_on_both_sides(both, source):
    """THE GAP THIS TEST EXISTS FOR.

    A machine with the tracking plugin and no tap has no daemon and never had
    one. Reading only `/tmp` cannot tell that from a daemon that died, so the
    segment blamed a crash that never happened; the spec's edge-case table
    requires `◐ tracking · not capturing session transcript: not installed` here.
    """
    reading, cli = both(source)
    assert reading == {"running": False, "reason": "not installed"}
    assert reading == cli


@pytest.mark.parametrize("source", _SOURCES)
def test_the_killswitch_outranks_the_pid_file_on_both_sides(both, source, tmp_path):
    state_dir = tmp_path / source
    (state_dir / "heal").mkdir(parents=True)
    (state_dir / ".disabled").write_text("", encoding="utf-8")
    pid_path = _pid_path(source)
    pid_path.write_text(str(os.getpid()), encoding="utf-8")
    try:
        reading, cli = both(source)
    finally:
        pid_path.unlink(missing_ok=True)
    assert reading == {"running": False, "reason": "killswitch"}
    assert reading == cli


@pytest.mark.parametrize("source", _SOURCES)
def test_an_installed_tap_with_no_daemon_reads_not_started_on_both_sides(both, source, tmp_path):
    (tmp_path / source).mkdir(parents=True)
    reading, cli = both(source)
    assert reading == {"running": False, "reason": "not started"}
    assert reading == cli


@pytest.mark.parametrize("source", _SOURCES)
def test_a_dead_pid_reads_not_started_on_both_sides(both, source, tmp_path):
    (tmp_path / source).mkdir(parents=True)
    pid_path = _pid_path(source)
    pid_path.write_text("999999999", encoding="utf-8")
    try:
        reading, cli = both(source)
    finally:
        pid_path.unlink(missing_ok=True)
    assert reading == {"running": False, "reason": "not started"}
    assert reading == cli


@pytest.mark.parametrize("source", _SOURCES)
def test_a_live_pid_reads_running_on_both_sides(both, source, tmp_path):
    """Also pins the PREFIX behaviourally: the two must find the SAME file."""
    (tmp_path / source).mkdir(parents=True)
    pid_path = _pid_path(source)
    pid_path.write_text(str(os.getpid()), encoding="utf-8")
    try:
        reading, cli = both(source)
    finally:
        pid_path.unlink(missing_ok=True)
    assert reading == {"running": True, "reason": "running"}
    assert reading == cli


def test_the_hook_never_signals_a_process_group(hook, monkeypatch, tmp_path):
    """`os.kill(0, 0)` is the whole process group, not a liveness probe.

    A pid file holding `0` (a truncated write, a wrapper that died between
    creating the file and filling it) must read as no daemon.
    """
    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    monkeypatch.setenv(EXPECTED_PLUGIN_DIR["claude_code"][0], str(tmp_path))
    pid_path = _pid_path("claude_code")
    for value in ("0", "-1"):
        pid_path.write_text(value, encoding="utf-8")
        try:
            assert hook._capture_reading(SID) == {"running": False, "reason": "not started"}
        finally:
            pid_path.unlink(missing_ok=True)


def test_the_hooks_reasons_are_in_the_cli_vocabulary(hook, monkeypatch, tmp_path):
    """The renderers print the reason VERBATIM, so the hook may not invent one."""
    from probe.cli import capture_state

    monkeypatch.setenv("PROBE_AGENT", "claude_code")
    monkeypatch.setenv(EXPECTED_PLUGIN_DIR["claude_code"][0], str(tmp_path / "absent"))
    assert hook._capture_reading(SID)["reason"] in capture_state.REASONS

    (tmp_path / "present").mkdir()
    monkeypatch.setenv(EXPECTED_PLUGIN_DIR["claude_code"][0], str(tmp_path / "present"))
    assert hook._capture_reading(SID)["reason"] in capture_state.REASONS
    (tmp_path / "present" / ".disabled").write_text("", encoding="utf-8")
    assert hook._capture_reading(SID)["reason"] in capture_state.REASONS


def test_the_hook_still_imports_nothing_of_ours():
    """It runs under the system python3 with no `probe` and no `tap` on its path.

    That constraint is WHY these are hand-written mirrors; an import creeping in
    would make the duplication look removable and this whole file pointless.
    """
    result = subprocess.run(
        [
            sys.executable,
            "-c",
            "import sys, importlib.util;"
            f"spec = importlib.util.spec_from_file_location('r', {str(_REFRESH)!r});"
            "m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m);"
            "assert 'probe' not in sys.modules, 'the refresh hook imported the probe package';"
            "assert 'tap' not in sys.modules, 'the refresh hook imported the tap package';"
            "print(m._tap_plugin_dir('codex', {'PRBE_CODEX_TAP_PLUGIN_DIR': '/x'}))",
        ],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip() == "/x"
