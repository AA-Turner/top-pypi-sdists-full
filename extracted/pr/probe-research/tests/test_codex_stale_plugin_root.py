"""Hooks must survive the plugin being upgraded out from under a live session.

Codex installs a plugin at a VERSION-QUALIFIED path,
`~/.codex/plugins/cache/<marketplace>/<plugin>/<version>/`, and hands hooks that
path in `$PLUGIN_ROOT`. Two facts about it collide:

  * a session binds `$PLUGIN_ROOT` ONCE, at session start, and keeps it for its
    whole life (the SKILLS root, by contrast, is re-resolved every turn — one
    rollout showed skills advancing 0.27 -> 0.28 -> 0.29 while the hooks stayed
    pinned to 0.27);
  * installing a new version REPLACES the plugin directory. The old version dir
    is removed, not kept alongside.

So the moment a release lands, every already-running session's hooks exec a path
that no longer exists, and keep doing it until the user restarts. Two failure
strings, one cause: `.sh` targets die at 127 (`bash: ... No such file or
directory`), `.py` targets at 2 (`python3: can't open file`).

SEVERITY IS NOT COSMETIC. `PreToolUse` and `UserPromptSubmit` treat a non-zero
hook as a VETO, so a pruned directory does not just print errors — it blocks
tool calls and prompts. Both were observed on 2026-08-19 as
`PreToolUse hook (blocked)` against a pruned `0.40.0` while `0.41.0` was
installed. The fail-open half of this fix is what turns a veto back into an
abstention.

The mirror publishes a version bump on nearly every merge to main (18 in the six
days to 2026-08-19), so "a session older than the last release" is the normal
case, which is why it presents as sessions rotting after a period of inactivity.

Codex should not prune a version a live session is still bound to; that is not
ours to fix. What IS ours: a hook that cannot find its own script re-resolves to
the installed version, and never exits non-zero because the file it was pointed
at is gone. Both halves are asserted here against the REAL command strings.

Confined to Codex's versioned cache, over-determined so no single edit re-opens
it: the fallback is gated on `$PLUGIN_ROOT` (only Codex sets it) AND only globs
version-shaped siblings. Claude Code installs to an unversioned path and updates
it in place, so it never had this bug — and its plugin dir sits beside OTHER
plugins, where a sibling scan would find probe-research-tap's identically-named
`session-start.sh`.

Known residuals, deliberately not chased:
  * the check-then-exec window is inherent — a prune landing between `[ -x ]`
    and `exec` still emits one line, and self-heals on the next event;
  * `[0-9]*.[0-9]*` is looser than a version comparator, but a stray directory
    would ALSO have to carry the exact hook script to be selected;
  * a path containing a literal newline breaks the line-oriented lookup. Spaces
    do not — that is asserted below.
"""

from __future__ import annotations

import json
import os
import re
import subprocess
from pathlib import Path

import pytest


_ROOT = Path(__file__).resolve().parent.parent
_PLUGINS = _ROOT / "plugins"
_PLUGIN_NAMES = ("probe-research", "probe-research-tap")
_STALE_PROLOGUE = 'ROOT="${PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}"; PY='
_DEAD = "0.23.0"
_LIVE = "0.42.0"


def _hooks(plugin: str) -> dict:
    return json.loads((_PLUGINS / plugin / "hooks" / "hooks.json").read_text())["hooks"]


def _commands(plugin: str) -> list[str]:
    return [e["command"] for ev in _hooks(plugin).values() for g in ev for e in g["hooks"]]


def _every_hook() -> list[tuple[str, str]]:
    """(plugin, command) for every registered hook in both plugins."""
    return [(p, c) for p in _PLUGIN_NAMES for c in _commands(p)]


def _target(command: str) -> str:
    """The one script this command execs, e.g. `telemetry.py`."""
    names = set(re.findall(r"\$ROOT/hooks/([A-Za-z0-9_.-]+)", command))
    assert len(names) == 1, f"expected exactly one exec target: {names}"
    return names.pop()


def _session_start(plugin: str = "probe-research") -> str:
    """The SessionStart command — the one in the first bug report."""
    return _hooks(plugin)["SessionStart"][0]["hooks"][0]["command"]


_SH_STUB = (
    '#!/usr/bin/env bash\n'
    'printf "ran=%s root=%s\\n" "$(cd "$(dirname "$0")/.." && pwd)" "${PLUGIN_ROOT:-unset}"\n'
)
# The python targets are exec'd as `python3 <file>`, so the stub has to be
# valid python, not a shell script with a shebang.
_PY_STUB = (
    "import os, sys\n"
    "root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))\n"
    "print('ran=%s root=%s' % (root, os.environ.get('PLUGIN_ROOT', 'unset')))\n"
)


def _install(
    cache: Path,
    version: str,
    target: str = "session-start.sh",
    *,
    plugin: str = "probe-research",
    executable: bool = True,
) -> Path:
    """Lay one version of the plugin down the way Codex's cache does.

    The stub echoes what it resolved, so a test can tell WHICH install ran and
    prove the re-exported `$PLUGIN_ROOT` is the live one — the tap reads that
    variable to find its own `.venv/bin/python3`, so a stale value breaks more
    than the hook itself.
    """
    root = cache / plugin / version
    (root / "hooks").mkdir(parents=True, exist_ok=True)
    (root / ".codex-plugin").mkdir(parents=True, exist_ok=True)
    (root / ".codex-plugin" / "plugin.json").write_text('{"name": "%s"}' % plugin)
    script = root / "hooks" / target
    script.write_text(_SH_STUB if target.endswith(".sh") else _PY_STUB)
    script.chmod(0o755 if executable else 0o644)
    return root


def _run(command: str, env: dict[str, str], **extra: str) -> subprocess.CompletedProcess:
    base = {
        "PATH": os.environ.get("PATH", "/usr/bin:/bin"),
        "HOME": os.environ.get("HOME", "/tmp"),
        # The session the reads hook's fast path looks up (Codex exports it).
        "CODEX_THREAD_ID": _THREAD,
    }
    return subprocess.run(
        ["/bin/bash", "-c", command],
        capture_output=True,
        text=True,
        input="{}",
        env={**base, **env, **extra},
    )


# ---------------------------------------------------------------------------
# the reported failure
# ---------------------------------------------------------------------------


def test_the_old_prologue_is_the_bug(tmp_path):
    """The control. Without the fallback a pruned version dir cannot execute — if
    this ever goes green, everything below is testing nothing."""
    cache = tmp_path / "cache"
    _install(cache, _LIVE)

    old = (
        '/bin/bash -c \'ROOT="${PLUGIN_ROOT:-${CLAUDE_PLUGIN_ROOT:-}}"; '
        'exec "$ROOT/hooks/session-start.sh"\''
    )
    result = _run(old, {"PLUGIN_ROOT": str(cache / "probe-research" / _DEAD)})

    # GNU Bash reports 127; macOS's /bin/bash reports 126 for this exec failure.
    assert result.returncode in {126, 127}
    assert "No such file or directory" in result.stderr


@pytest.mark.parametrize(("plugin", "command"), _every_hook(), ids=lambda v: v[:28])
def test_every_hook_re_resolves_to_the_installed_version(tmp_path, plugin, command):
    """Not just SessionStart, and not just "exits 0" — a hook that did nothing
    at all would pass that. Each hook must actually RUN, from the live install.

    MUTANT: drop the fallback -> the stub never runs and `ran=` is absent.
    """
    cache = tmp_path / "cache"
    target = _target(command)
    live = _install(cache, _LIVE, target, plugin=plugin)

    result = _run(
        command,
        {"PLUGIN_ROOT": str(cache / plugin / _DEAD)},
        # The gated hooks return before their target unless their gate is met.
        XDG_STATE_HOME=str(_flag_home(tmp_path)),
    )

    assert result.returncode == 0, result.stderr
    assert f"ran={live}" in result.stdout, result.stdout or result.stderr
    assert f"root={live}" in result.stdout, "the live root must be re-exported"


_THREAD = "0199a1b2-c3d4-7e5f-8a9b-0c1d2e3f4a5b"


def _flag_home(tmp_path: Path) -> Path:
    """XDG_STATE_HOME carrying what the gated hooks check in the shell before
    they start their target: the statusline-notify flag (the Stop hook) and a
    message waiting for this session (the reads hook's fast path)."""
    home = tmp_path / "state"
    (home / "probe").mkdir(parents=True, exist_ok=True)
    (home / "probe" / "statusline-notify").write_text("")
    waiting = home / "probe" / "reads" / "messages" / _THREAD
    waiting.mkdir(parents=True, exist_ok=True)
    (waiting / "00000000000000000001-m0.json").write_text("{}")
    return home


def test_a_healthy_root_is_used_as_given(tmp_path):
    """The fast path must not go looking. A session bound to a version that is
    still installed runs THAT version, even with a newer one beside it."""
    cache = tmp_path / "cache"
    bound = _install(cache, "0.39.0")
    _install(cache, _LIVE)

    result = _run(_session_start(), {"PLUGIN_ROOT": str(bound)})

    assert f"ran={bound}" in result.stdout


def test_the_most_recently_installed_version_wins(tmp_path):
    """Two survivors, and the newest INSTALL is the right answer — that is what
    Codex just wrote, and what the session would have got had it started now.

    Selection is by mtime (`ls -dt`), NOT `sort -V`: version-sort is a GNU
    extension that stock BSD `sort` on macOS does not carry, and its failure
    mode is an empty pipeline — recovery would silently become a no-op on every
    Mac while every Linux test stayed green.
    """
    cache = tmp_path / "cache"
    older = _install(cache, "0.9.0")
    newer = _install(cache, "0.10.0")
    os.utime(older, (1_600_000_000, 1_600_000_000))
    os.utime(older / "hooks" / "session-start.sh", (1_600_000_000, 1_600_000_000))

    result = _run(_session_start(), {"PLUGIN_ROOT": str(cache / "probe-research" / "0.8.0")})

    assert f"ran={newer}" in result.stdout


def test_a_trailing_slash_on_the_bound_root_still_resolves(tmp_path):
    """MUTANT: drop `ROOT="${ROOT%/}"` -> `${ROOT%/*}` strips the slash instead
    of the version segment, the glob searches UNDER the pruned directory, finds
    nothing, and the hook silently does nothing forever."""
    cache = tmp_path / "cache"
    live = _install(cache, _LIVE)

    result = _run(_session_start(), {"PLUGIN_ROOT": f"{cache / 'probe-research' / _DEAD}/"})

    assert f"ran={live}" in result.stdout


def test_a_path_with_spaces_resolves(tmp_path):
    """macOS home directories routinely contain a space. Word splitting here
    would resolve to a truncated path and fail open forever, invisibly."""
    cache = tmp_path / "Agent Cache" / "cache"
    live = _install(cache, _LIVE)

    result = _run(_session_start(), {"PLUGIN_ROOT": str(cache / "probe-research" / _DEAD)})

    assert f"ran={live}" in result.stdout


# ---------------------------------------------------------------------------
# fail-open: nothing runnable is still exit 0
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "shape", ["nothing-installed", "no-hooks-dir", "empty-hooks-dir", "not-yet-executable"]
)
@pytest.mark.parametrize(("plugin", "command"), _every_hook(), ids=lambda v: v[:28])
def test_every_hook_fails_open_when_nothing_is_runnable(tmp_path, plugin, command, shape):
    """Codex rewrites the tree IN PLACE, so another session's hook can land
    mid-extraction, in any of these states. None of them may produce a non-zero
    exit: on PreToolUse and UserPromptSubmit that is a veto, not a warning.

    MUTANT: guard `[ -d "$ROOT/hooks" ]` instead of the script -> `empty-hooks-dir`
    is 127/2 again. MUTANT: `-f` instead of `-x` on the shell targets ->
    `not-yet-executable` is 126.
    """
    cache = tmp_path / "cache"
    target = _target(command)
    if shape == "no-hooks-dir":
        (cache / plugin / _LIVE).mkdir(parents=True)
    elif shape == "empty-hooks-dir":
        (cache / plugin / _LIVE / "hooks").mkdir(parents=True)
    elif shape == "not-yet-executable" and target.endswith(".sh"):
        _install(cache, _LIVE, target, plugin=plugin, executable=False)
    elif shape == "not-yet-executable":
        pytest.skip("python targets are exec'd via the interpreter; no bit to miss")

    result = _run(
        command,
        {"PLUGIN_ROOT": str(cache / plugin / _DEAD)},
        XDG_STATE_HOME=str(_flag_home(tmp_path)),
    )

    assert result.returncode == 0, result.stderr
    assert "No such file or directory" not in result.stderr
    assert "can't open file" not in result.stderr
    assert "Permission denied" not in result.stderr


# ---------------------------------------------------------------------------
# Claude Code must not be dragged into this
# ---------------------------------------------------------------------------


def test_a_dead_root_that_still_has_an_empty_hooks_dir_re_resolves(tmp_path):
    """Codex rewrites the tree IN PLACE, so a live session's OWN version dir can
    survive as an empty shell while its files are replaced — the directory is
    there, the script is not.

    MUTANT: guard `[ ! -d "$ROOT/hooks" ]` instead of the script -> the fallback
    never fires (the directory exists), and the hook execs a file that is gone:
    exit 127, the original bug, from the fix meant to prevent it.
    """
    cache = tmp_path / "cache"
    live = _install(cache, _LIVE)
    dead = cache / "probe-research" / _DEAD
    (dead / "hooks").mkdir(parents=True)

    result = _run(_session_start(), {"PLUGIN_ROOT": str(dead)})

    assert result.returncode == 0, result.stderr
    assert f"ran={live}" in result.stdout


def test_a_scratch_dir_of_loose_hook_files_is_never_selected(tmp_path):
    """The 2026-08-19 shape, reproduced from what was actually on disk.

    When 0.42.0 pruned 0.41.0, another session hand-wrote three compatibility
    shims INTO the dead directory — `tracking_guard.py`, `telemetry.py`,
    `statusline_refresh.py` and nothing else. No manifest, no other module. That
    left a directory which:

      * carries the exact filenames the resolver was globbing for, and
      * has a NEWER mtime than the real install, because it was written after.

    So the previous anchor (the hook script) selected it, and the hook ran with
    `$PLUGIN_ROOT` pointing at three loose files — no `_session_marker`, no
    `plugin.json`. The shims happened to forward, but nothing about that was
    guaranteed: an ImportError there is exit 1, which on PreToolUse is a veto.

    MUTANT: anchor on `hooks/<target>` again -> the scratch dir wins.
    """
    cache = tmp_path / "cache"
    live = _install(cache, _LIVE, "tracking_guard.py")
    scratch = cache / "probe-research" / "0.41.0" / "hooks"
    scratch.mkdir(parents=True)
    for name in ("tracking_guard.py", "telemetry.py", "statusline_refresh.py"):
        (scratch / name).write_text("import sys; sys.exit(1)\n")
    os.utime(live, (1_600_000_000, 1_600_000_000))
    os.utime(live / "hooks" / "tracking_guard.py", (1_600_000_000, 1_600_000_000))
    assert scratch.parent.stat().st_mtime > live.stat().st_mtime, "scratch must be newer"

    command = next(c for c in _commands("probe-research") if "tracking_guard.py" in c)
    result = _run(command, {"PLUGIN_ROOT": str(cache / "probe-research" / "0.40.0")})

    assert result.returncode == 0, result.stderr
    assert f"ran={live}" in result.stdout, "must pick the real install, not the scratch dir"
    assert "0.41.0" not in result.stdout


def test_a_version_dir_without_a_manifest_is_not_an_install(tmp_path):
    """Generalises the above: the manifest is what makes a directory an install.
    A version-shaped directory carrying a complete-looking hooks/ but no
    `.codex-plugin/plugin.json` was never installed by Codex and must not be
    treated as one, however new it is."""
    cache = tmp_path / "cache"
    live = _install(cache, _LIVE)
    impostor = cache / "probe-research" / "9.9.9" / "hooks"
    impostor.mkdir(parents=True)
    (impostor / "session-start.sh").write_text('#!/usr/bin/env bash\nprintf "IMPOSTOR\\n"\n')
    (impostor / "session-start.sh").chmod(0o755)
    os.utime(live, (1_600_000_000, 1_600_000_000))

    result = _run(_session_start(), {"PLUGIN_ROOT": str(cache / "probe-research" / _DEAD)})

    assert "IMPOSTOR" not in result.stdout
    assert f"ran={live}" in result.stdout


def test_claude_code_never_runs_a_sibling_plugins_hook(tmp_path):
    """Claude Code's plugin dir sits BESIDE other plugins rather than beside
    other versions of itself, so a sibling scan there could run a different
    plugin's hook of the same name — probe-research-tap ships a
    `session-start.sh` too, which is exactly the collision.

    Over-determined so no single edit re-opens it: the fallback is gated on
    `$PLUGIN_ROOT` (which only Codex sets) AND only globs version-shaped names,
    which no plugin directory is. This asserts the guarantee; the glob half is
    pinned below.
    """
    plugins = tmp_path / "claude" / "plugins" / "cache" / "research-os-agent"
    tap = plugins / "probe-research-tap" / "hooks"
    tap.mkdir(parents=True)
    (tap / "session-start.sh").write_text('#!/usr/bin/env bash\nprintf "WRONG PLUGIN\\n"\n')
    (tap / "session-start.sh").chmod(0o755)

    result = _run(_session_start(), {"CLAUDE_PLUGIN_ROOT": str(plugins / "probe-research")})

    assert result.returncode == 0
    assert "WRONG PLUGIN" not in result.stdout


def test_only_version_shaped_siblings_are_candidates(tmp_path):
    """MUTANT: widen the glob to `*/` -> the stray directory wins.

    Selection takes the most recent candidate, so a non-version directory
    touched later would outrank every real install.
    """
    cache = tmp_path / "cache"
    live = _install(cache, _LIVE)
    stray = _install(cache, "zz-scratch")
    # Newer than the real install on purpose: selection is most-recent-first, so
    # a stray that only loses on tie-break would not challenge the glob at all.
    os.utime(live, (1_600_000_000, 1_600_000_000))
    os.utime(live / "hooks" / "session-start.sh", (1_600_000_000, 1_600_000_000))
    assert stray.stat().st_mtime > live.stat().st_mtime

    result = _run(_session_start(), {"PLUGIN_ROOT": str(cache / "probe-research" / _DEAD)})

    assert "zz-scratch" not in result.stdout
    assert f"ran={live}" in result.stdout


# ---------------------------------------------------------------------------
# the invariant, so a new hook cannot be added without it
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("plugin", _PLUGIN_NAMES)
def test_no_hook_still_carries_the_stale_prologue(plugin):
    """The resolver is inlined per command because it has to run BEFORE any file
    in the plugin can be read — there is no shared script to factor it into that
    would not itself be the missing file. Duplication is the design; this is
    what keeps the copies honest, so a hook added with the old one-liner is red.
    """
    for command in _commands(plugin):
        target = _target(command)
        test = "x" if target.endswith(".sh") else "f"
        assert _STALE_PROLOGUE not in command, command[:120]
        assert 'ROOT="${ROOT%/}"' in command, command[:120]
        assert 'ls -dt "${ROOT%/*}"/[0-9]*.[0-9]*/.codex-plugin/plugin.json' in command, command[:200]
        assert f"/hooks/{target} 2>/dev/null" not in command, (
            "anchor on the install manifest, not on the hook script"
        )
        assert f'[ -{test} "$ROOT/hooks/{target}" ] || exit 0' in command, command[:160]
        assert "sort -V" not in command, "version-sort is not portable to BSD sort"
