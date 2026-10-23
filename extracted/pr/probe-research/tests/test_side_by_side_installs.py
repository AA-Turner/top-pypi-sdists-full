"""Side-by-side installs of the CLI's uv tool env, and the switch back (plan D6, D5).

Each version gets its own environment under `<uv tool dir>/../probe-versions/<v>/`;
the tool path becomes a symlink switched in one rename; the previous version
stays to switch back to. These tests build fake environments (an executable
`bin/python` that answers the three questions `installs` asks: its version, the
service's start path, the CLI's import) so nothing is installed for real.
"""

from __future__ import annotations

import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from probe._shared import installs

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="POSIX symlinks and shebangs")

_FAKE_PYTHON = """#!/bin/sh
here="$(cd "$(dirname "$0")/.." && pwd)"
case "$*" in
  *importlib.metadata*) cat "$here/VERSION" ;;
  *--selftest*) [ -f "$here/BROKEN" ] && { echo "ImportError: broken" >&2; exit 1; }; echo '[]' ;;
  *probe.cli.main*) exit 0 ;;
  *) exit 0 ;;
esac
"""


def _fake_env(env: Path, version: str, *, broken: bool = False) -> Path:
    (env / "bin").mkdir(parents=True, exist_ok=True)
    python = env / "bin" / "python"
    python.write_text(_FAKE_PYTHON)
    python.chmod(0o755)
    (env / "VERSION").write_text(version + "\n")
    if broken:
        (env / "BROKEN").write_text("")
    return env


@pytest.fixture
def tools(tmp_path, monkeypatch) -> Path:
    """uv's tool folder with today's install: a real `probe-research` folder (0.1.0)."""
    folder = tmp_path / "share" / "uv" / "tools"
    _fake_env(folder / installs.DIST, "0.1.0")
    monkeypatch.setenv("UV_TOOL_DIR", str(folder))
    return folder


def _uv(version: str, *, broken: bool = False):
    """A stand-in `uv tool install`: makes `<UV_TOOL_DIR>/probe-research` at `version`."""
    calls = []

    def run(argv, env, **_kw):
        calls.append((argv, env["UV_TOOL_DIR"], env["UV_TOOL_BIN_DIR"]))
        _fake_env(Path(env["UV_TOOL_DIR"]) / installs.DIST, version, broken=broken)
        return subprocess.CompletedProcess(argv, 0, "", "")

    run.calls = calls
    return run


def test_a_version_installs_beside_the_running_one(tools):
    run = _uv("0.2.0")
    env = installs.install("0.2.0", "probe-research[all]==0.2.0", python="/usr/bin/python3.12", tools=tools, run=run)
    assert env == tools.parent / "probe-versions" / "0.2.0" / installs.DIST
    (argv, tool_dir, bin_dir), = run.calls
    assert argv[:3] == ["uv", "tool", "install"] and "probe-research[all]==0.2.0" in argv
    assert argv[argv.index("--python") + 1] == "/usr/bin/python3.12"
    assert tool_dir == str(env.parent) and bin_dir == str(env.parent / ".bin")
    # The running install is untouched.
    assert installs.env_version(tools / installs.DIST) == "0.1.0"
    assert not (tools / installs.DIST).is_symlink()


def test_an_install_that_lands_another_version_changes_nothing(tools):
    with pytest.raises(RuntimeError, match="left 0.1.9"):
        installs.install("0.2.0", "probe-research[all]==0.2.0", tools=tools, run=_uv("0.1.9"))
    assert not (tools.parent / "probe-versions" / "0.2.0").exists()
    assert installs.env_version(tools / installs.DIST) == "0.1.0"


def test_the_first_switch_keeps_today_s_install_to_switch_back_to(tools):
    new = installs.install("0.2.0", "x==0.2.0", tools=tools, run=_uv("0.2.0"))
    record = installs.activate(new, tools=tools)
    tool = tools / installs.DIST
    assert tool.is_symlink() and tool.resolve() == new.resolve()
    assert installs.env_version(tool) == "0.2.0"  # the tool path is the active version
    previous = tools.parent / "probe-versions" / "0.1.0" / installs.DIST
    assert record["previous"] == str(previous) and installs.env_version(previous) == "0.1.0"
    assert installs.active(tools) == new.resolve()


def test_a_switch_and_a_switch_back_are_one_rename_each(tools):
    first = installs.install("0.2.0", "x", tools=tools, run=_uv("0.2.0"))
    installs.activate(first, tools=tools)
    second = installs.install("0.3.0", "x", tools=tools, run=_uv("0.3.0"))
    record = installs.activate(second, tools=tools)
    assert record["previous"] == str(first)
    back = installs.switch_back(tools)
    assert back is not None and installs.active(tools) == first.resolve()
    assert installs.env_version(tools / installs.DIST) == "0.2.0"


def test_a_process_started_before_a_switch_keeps_its_version(tools):
    """A long run or a daemon worker started through the tool path resolves to
    its version's own folder (uv writes each env's scripts with its own
    interpreter path), so the next switch replaces nothing under it."""
    first = installs.install("0.2.0", "x", tools=tools, run=_uv("0.2.0"))
    installs.activate(first, tools=tools)
    started_as = (tools / installs.DIST / "bin" / "python").resolve()
    installs.activate(installs.install("0.3.0", "x", tools=tools, run=_uv("0.3.0")), tools=tools)
    assert started_as.exists()
    assert subprocess.run([str(started_as), "-c", "importlib.metadata"], capture_output=True, text=True).stdout.strip() == "0.2.0"


def test_a_version_that_does_not_start_is_caught_before_the_switch(tools):
    env = installs.install("0.2.0", "x", tools=tools, run=_uv("0.2.0", broken=True))
    assert "the Probe service would not start" in installs.selftest(env)
    installs.discard(env)
    assert not env.exists()
    assert not (tools / installs.DIST).is_symlink()  # never switched


def test_a_rejected_version_is_remembered(tools):
    installs.activate(installs.install("0.2.0", "x", tools=tools, run=_uv("0.2.0")), tools=tools)
    installs.reject("0.2.0", "the new service did not answer within 45 s", tools)
    assert "0.2.0" in installs.rejected(tools)
    assert installs.rejected(tools)["0.2.0"]["reason"].startswith("the new service")


def test_pruning_keeps_the_active_the_previous_and_young_versions(tools, monkeypatch):
    monkeypatch.setattr(installs, "_in_use", lambda folder, commands=None: False)
    envs = []
    for version in ("0.2.0", "0.3.0", "0.4.0", "0.5.0", "0.6.0"):
        env = installs.install(version, "x", tools=tools, run=_uv(version))
        installs.activate(env, tools=tools)
        envs.append(env)
    root = tools.parent / "probe-versions"
    old = time.time() - 3 * 24 * 3600
    for folder in root.iterdir():
        if folder.is_dir():
            _age(folder, old)
    removed = installs.prune(tools, keep=2)
    kept = sorted(p.name for p in root.iterdir() if p.is_dir())
    assert "0.6.0" in kept and "0.5.0" in kept  # active, previous
    assert removed and all(not p.exists() for p in removed)
    # Young folders are never pruned.
    young = installs.install("0.7.0", "x", tools=tools, run=_uv("0.7.0"))
    assert young.parent not in installs.prune(tools, keep=0)


def test_a_version_a_process_runs_from_is_never_pruned(tools):
    env = installs.install("0.2.0", "x", tools=tools, run=_uv("0.2.0"))
    holder = subprocess.Popen(["sh", "-c", "sleep 30", str(env)])
    try:
        assert installs._in_use(env.parent)
    finally:
        holder.kill()
        holder.wait()


def test_the_install_is_recognized_from_a_version_env():
    assert installs.running_from_versions("/home/a/.local/share/uv/probe-versions/0.2.0/probe-research")
    assert not installs.running_from_versions("/home/a/.local/share/uv/tools/probe-research")


def test_only_the_first_switch_needs_a_quiet_machine(tools):
    """The first switch moves the folder every running process reads its files
    through; every later one changes a link only (Codex R2 #1)."""
    assert installs.needs_migration(tools) is True
    installs.activate(installs.install("0.2.0", "x", tools=tools, run=_uv("0.2.0")), tools=tools)
    assert installs.needs_migration(tools) is False


def test_a_first_switch_that_fails_puts_the_folder_back(tools, monkeypatch):
    """A full disk or a refused rename after the folder moved: it moves back,
    so the CLI keeps its tool path (Codex R2 #2)."""
    new = installs.install("0.2.0", "x", tools=tools, run=_uv("0.2.0"))
    real_replace = installs.os.replace

    def refuse(src, dst):
        if Path(dst) == installs.tool_env(tools):
            raise OSError(28, "No space left on device")
        return real_replace(src, dst)

    monkeypatch.setattr(installs.os, "replace", refuse)
    with pytest.raises(OSError):
        installs.activate(new, tools=tools)
    env = installs.tool_env(tools)
    assert env.is_dir() and not env.is_symlink()
    assert (env / "VERSION").read_text().strip() == "0.1.0"
    assert "migrating" not in installs.record(tools)
    assert not list(tools.glob(f".{installs.DIST}.switch-*"))


def test_a_first_switch_cut_short_is_recovered(tools):
    """Killed between moving the folder and linking it: the next switch (or
    `recover`) moves it back first."""
    moved = installs._migrate(tools)
    assert moved is not None and not installs.tool_env(tools).exists()
    assert installs.recover(tools) is True
    assert (installs.tool_env(tools) / "VERSION").read_text().strip() == "0.1.0"
    assert installs.recover(tools) is False


def test_a_version_envs_receipt_names_the_real_scripts_folder(tools, tmp_path, monkeypatch):
    """uv reads the receipt of whatever the tool path names: one naming
    `probe-versions/<v>/.bin` makes a plain `uv tool install` (npx on a stale
    CLI) delete the tool path (critic R2 P1, reproduced with uv 0.12.5)."""
    bins = tmp_path / "local-bin"
    (installs.tool_env(tools) / installs.RECEIPT).write_text(
        f'[tool]\nentrypoints = [\n    {{ name = "probe", install-path = "{bins}/probe", from = "probe-research" }},\n]\n')
    new = installs.install("0.2.0", "x", tools=tools, run=_uv("0.2.0"))
    (new / installs.RECEIPT).write_text(
        f'[tool]\nentrypoints = [\n    {{ name = "probe", install-path = "{new.parent / ".bin"}/probe", from = "probe-research" }},\n]\n')
    installs.activate(new, tools=tools)
    text = (new / installs.RECEIPT).read_text()
    assert f'"{bins}/probe"' in text and ".bin" not in text
    assert installs.record(tools)["bin"] == str(bins)
    # The next version learns the folder from the record (the receipt it would
    # read is a version env's now).
    newer = installs.install("0.3.0", "x", tools=tools, run=_uv("0.3.0"))
    (newer / installs.RECEIPT).write_text(f'install-path = "{newer.parent / ".bin"}/probe"\n')
    installs.activate(newer, tools=tools)
    assert (newer / installs.RECEIPT).read_text() == f'install-path = "{bins}/probe"\n'


def test_a_version_another_machine_runs_from_is_kept(tools, monkeypatch):
    """A home shared by several machines: this one sees only its own
    processes, so another's fresh mark keeps the version."""
    monkeypatch.setattr(installs, "_commands", lambda: [])
    for version in ("0.2.0", "0.3.0", "0.4.0", "0.5.0"):
        installs.activate(installs.install(version, "x", tools=tools, run=_uv(version)), tools=tools)
    root = tools.parent / "probe-versions"
    elsewhere = root / "0.2.0" / (installs.USED_PREFIX + "another-machine")
    elsewhere.touch()
    old = time.time() - 3 * 24 * 3600
    for folder in root.iterdir():
        if folder.is_dir():
            _age(folder, old)
    removed = {p.name for p in installs.prune(tools, keep=0)}
    assert "0.2.0" not in removed, "another machine's mark keeps it"
    assert "0.3.0" in removed
    stale = time.time() - installs.USED_FRESH_S - 60
    os.utime(elsewhere, (stale, stale))
    assert "0.2.0" in {p.name for p in installs.prune(tools, keep=0)}


def _age(folder: Path, when: float) -> None:
    """Make a version folder look installed at `when` (prune reads its env's install time)."""
    for path in (folder, folder / installs.DIST / "bin" / "python", folder / installs.DIST / "pyvenv.cfg"):
        if path.exists():
            os.utime(path, (when, when))
