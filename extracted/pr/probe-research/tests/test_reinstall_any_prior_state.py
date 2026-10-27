"""A reinstall over any earlier Probe ends in one working install (plan clean-uninstall-reinstall C5-C7, V-T1).

Every supported install entry goes through `install_pipeline.install_cli`
(recover -> build -> validate -> switch -> cleanup, under the install lock).
Each test sets up one prior state with REAL uv (`reinstall_harness`: offline,
hand-built wheels, a private tool folder) and installs over it:

    fresh, current, older, after an uninstall (`keeper-off`), after `uv tool
    uninstall` (link and scripts gone), after `uv tool install --force` (uv's
    folder over the link), a stale `active.json`, `rejected` for the version
    asked for, a migration leftover, a broken active env of the same version
    (rebuilt as a generation), a dangling link, two installers at once, and an
    install cut short at each step, then run again.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from pathlib import Path

import pytest

from probe._shared import handoff, installs, uninstall_barrier
from probe.cli import install_pipeline
from tests.reinstall_harness import Machine, reinstall_wheels, uv_machine  # noqa: F401 -- fixtures

pytestmark = pytest.mark.skipif(sys.platform == "win32", reason="the side-by-side layout is POSIX only")


def _install(version: str, **kwargs) -> install_pipeline.CliOutcome:
    out = install_pipeline.install_cli(version, **kwargs)
    assert not out.refused, out.refused
    return out


def _settled(m: Machine, version: str) -> None:
    """One working install of `version`: the tool path a link to a complete env
    of it, `probe` on PATH answering it, `active.json` naming what is."""
    assert installs.tool_state(m.tools) == installs.ToolPath.LINKED
    active = installs.active(m.tools)
    assert active is not None and installs.env_version(active) == version
    assert installs.health(active, version) is None
    assert m.probe() == f"probe {version}"
    record = installs.record(m.tools)
    assert Path(record["active"]).resolve() == active
    assert os.readlink(m.bins / "probe") == str(m.tool / "bin" / "probe")


def _corrupt(env: Path) -> None:
    """Break `env`'s update path. A new file, never a write into the old one:
    uv links an env's files to its cache, which a rebuild installs from."""
    run = next(env.glob("lib/python3*/site-packages/probe/core/run.py"))
    run.unlink()
    run.write_text("raise ImportError('corrupted')\n")


def _layout(m: Machine, *versions: str) -> None:
    """Versions installed and switched as the update does, the last one active."""
    for version in versions:
        out = _install(version)
        assert out.ok, out.problems


def test_a_fresh_machine_gets_the_layout_and_the_probe_command(uv_machine):
    """O8: an install into a version folder fills only its private `.bin`; a
    fresh machine also needs `~/.local/bin/probe` (UV_TOOL_BIN_DIR here)."""
    m = uv_machine
    out = _install("1.0.0")
    assert out.ok and out.changed, out.problems
    _settled(m, "1.0.0")
    assert (m.versions / "1.0.0" / "probe-research").is_dir()


def test_the_same_version_again_checks_and_changes_nothing(uv_machine):
    m = uv_machine
    _layout(m, "1.0.0")
    before = installs.active(m.tools)
    out = _install("1.0.0")
    assert out.ok and not out.changed, out.lines
    assert installs.active(m.tools) == before
    _settled(m, "1.0.0")


def test_an_older_install_moves_to_the_version_asked_for_and_keeps_it_to_switch_back_to(uv_machine):
    m = uv_machine
    _layout(m, "1.0.0")
    out = _install("1.0.1")
    assert out.ok and out.changed
    _settled(m, "1.0.1")
    assert installs.previous(m.tools) == m.versions / "1.0.0" / "probe-research"


def test_after_an_uninstall_the_keeper_may_come_back(uv_machine):
    """R1: `keeper-off`, written by an uninstall, survived every reinstall that
    found its plugins present: no lifeboat, no keeper timer after."""
    from probe.service import keeper, paths

    off = paths.root_dir() / keeper.OFF_NAME
    off.parent.mkdir(parents=True, exist_ok=True)
    off.touch()
    out = _install("1.0.0")
    assert out.ok
    assert not off.exists()


def test_after_uv_tool_uninstall_the_link_and_the_command_come_back(uv_machine):
    """`uv tool uninstall` removes the link and the scripts; the versions and
    active.json stay. A reinstall reuses the env that is there."""
    m = uv_machine
    _layout(m, "1.0.0", "1.0.1")
    m.uv("tool", "uninstall", "probe-research")
    assert installs.tool_state(m.tools) == installs.ToolPath.MISSING
    assert not (m.bins / "probe").exists()
    out = _install("1.0.1")
    assert out.ok, out.problems
    _settled(m, "1.0.1")
    assert not any(p.name.endswith("+g2") for p in m.versions.iterdir()), "a healthy env is reused, not rebuilt"


def test_after_uv_tool_uninstall_and_an_older_version_by_hand(uv_machine):
    """R3's state: uv's own folder of an OLDER version at the tool path, the
    newer env still in the versions folder, active.json naming it. A reinstall
    of the newest adopts uv's folder (kept to switch back to) and switches."""
    m = uv_machine
    _layout(m, "1.0.0", "1.0.1")
    m.uv("tool", "uninstall", "probe-research")
    m.uv("tool", "install", "probe-research[all]==1.0.0")
    assert installs.tool_state(m.tools) == installs.ToolPath.PLAIN
    out = _install("1.0.1")
    assert out.ok, out.problems
    _settled(m, "1.0.1")
    prior = installs.previous(m.tools)
    assert prior is not None and installs.env_version(prior) == "1.0.0"
    assert prior.parent.name == "1.0.0+g2", "uv's folder goes to the next generation, never a name read as a version"


def test_after_uv_tool_install_force_over_the_link(uv_machine):
    """R4: `--force` replaced the link with uv's folder; the next update waited
    as a first switch and left a `<v>-<ts>` leftover."""
    m = uv_machine
    _layout(m, "1.0.0", "1.0.1")
    m.uv("tool", "install", "--force", "probe-research[all]==1.0.1")
    assert installs.tool_state(m.tools) == installs.ToolPath.PLAIN
    out = _install("1.0.1")
    assert out.ok, out.problems
    _settled(m, "1.0.1")
    assert not [p for p in m.versions.iterdir() if installs.folder_parts(p.name)[2]], "no migration leftover"


def test_a_plain_install_through_the_link_is_no_longer_what_npx_runs(uv_machine, monkeypatch):
    """R2: `bootstrap.install_persistent` (npx, the wizard, `probe update` from
    a throwaway copy) ran a plain `uv tool install` THROUGH the link, which
    rewrote the ACTIVE env in place. Now it installs beside it."""
    from probe.cli import bootstrap

    m = uv_machine
    _layout(m, "1.0.0")
    active = installs.active(m.tools)
    result = bootstrap.install_persistent(f"{bootstrap.INSTALL_SPEC}==1.0.1")
    assert result.installed, result.message
    assert installs.env_version(active) == "1.0.0", "the env that was active was not touched"
    _settled(m, "1.0.1")


def test_a_stale_active_json_is_put_right(uv_machine):
    m = uv_machine
    _layout(m, "1.0.0")
    record = installs.record(m.tools)
    record.update(active=str(m.versions / "9.9.9" / "probe-research"), previous=str(m.versions / "gone" / "x"))
    (m.versions / installs.ACTIVE_NAME).write_text(json.dumps(record))
    out = _install("1.0.0")
    assert out.ok
    assert any("active.json named" in line for line in out.lines)
    record = installs.record(m.tools)
    assert Path(record["active"]).resolve() == installs.active(m.tools) and "previous" not in record


def test_a_person_asking_for_a_rejected_version_gets_it(uv_machine):
    m = uv_machine
    _layout(m, "1.0.0")
    installs.reject("1.0.1", "the new service did not answer", m.tools)
    out = _install("1.0.1", person=True)
    assert out.ok
    assert "1.0.1" not in installs.rejected(m.tools)
    _settled(m, "1.0.1")


def test_a_migration_leftover_goes_unless_it_is_the_one_to_switch_back_to(uv_machine):
    m = uv_machine
    _layout(m, "1.0.0", "1.0.1")
    leftover = m.versions / "1.0.0-1730000000"
    (m.versions / "1.0.0").rename(leftover)
    installs.set_fields(m.tools, previous=None)
    out = _install("1.0.1")
    assert out.ok and not leftover.exists(), out.lines
    # As the one to switch back to it stays.
    _layout(m, "1.0.0")
    installs.activate(m.versions / "1.0.1" / "probe-research", tools=m.tools)
    (m.versions / "1.0.0").rename(leftover)
    installs.set_fields(m.tools, previous=str(leftover / "probe-research"))
    _install("1.0.1")
    assert leftover.exists()


def test_a_broken_active_env_is_rebuilt_as_a_generation_and_switched_to(uv_machine):
    """R-T3, R10: the active env of the version asked for fails its import
    check. Its folder is in use, so the rebuild goes in `<v>+g2`; the version is
    read from dist-info, and the broken folder stays to switch back to until
    nothing uses it."""
    m = uv_machine
    _layout(m, "1.0.0")
    broken = installs.active(m.tools)
    _corrupt(broken)
    assert installs.health(broken, "1.0.0") is not None
    out = _install("1.0.0")
    assert out.ok and out.changed, out.problems
    _settled(m, "1.0.0")
    assert installs.active(m.tools).parent.name == "1.0.0+g2"
    assert installs.previous(m.tools) == broken
    # A second repair of the same version reuses the good generation.
    assert not _install("1.0.0").changed


def test_a_dangling_link_is_reinstalled(uv_machine):
    """R10: the active env deleted under the link."""
    import shutil

    m = uv_machine
    _layout(m, "1.0.0")
    shutil.rmtree(m.versions / "1.0.0")
    assert installs.tool_state(m.tools) == installs.ToolPath.DANGLING
    out = _install("1.0.0")
    assert out.ok, out.problems
    _settled(m, "1.0.0")


def test_the_uninstall_barrier_refuses_while_live_and_is_cleared_when_stale(uv_machine, monkeypatch):
    m = uv_machine
    barrier = uninstall_barrier.path()
    from probe.service import procid

    def write(data: dict) -> None:
        barrier.parent.mkdir(parents=True, exist_ok=True)
        barrier.write_text(json.dumps(data))

    live = {"v": 1, "pid": os.getpid(), "start": procid.start_time(os.getpid()), "at": time.time(),
            "plan": "x", "phase": "planned"}
    write(live)
    out = install_pipeline.install_cli("1.0.0")
    assert out.refused and "uninstall" in out.refused
    assert installs.tool_state(m.tools) == installs.ToolPath.MISSING, "nothing was installed"
    with pytest.raises(uninstall_barrier.UninstallRunning):
        installs.activate(m.versions / "x", tools=m.tools)
    # Its owner gone before the point of no return: stale, cleared, installed.
    write({**live, "pid": 2 ** 22 - 3, "start": "1"})
    out = install_pipeline.install_cli("1.0.0")
    assert out.ok and not barrier.exists()
    assert any("stale uninstall barrier" in line for line in out.lines)
    # Past the point of no return its owner's death does not matter: it must be finished.
    write({**live, "pid": 2 ** 22 - 3, "start": "1", "phase": "server"})
    assert install_pipeline.install_cli("1.0.1").refused


_CHILD = """
import sys
from probe.cli import install_pipeline
out = install_pipeline.install_cli(sys.argv[1])
print("ok" if out.ok else "refused: " + out.refused if out.refused else "failed: " + "; ".join(out.problems))
"""


def test_two_installers_at_once_end_in_one_install(uv_machine):
    """Two processes (an npx and a `probe repair`, say) take the install lock
    in turn: both end with the one working install; neither builds into the
    other's folder."""
    m = uv_machine
    env = {**os.environ}
    children = [subprocess.Popen([sys.executable, "-c", _CHILD, "1.0.1"], env=env, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True) for _ in range(2)]
    said = [child.communicate(timeout=300) for child in children]
    assert [out.strip().splitlines()[-1] for out, _err in said] == ["ok", "ok"], said
    _settled(m, "1.0.1")
    assert sorted(p.name for p in m.versions.iterdir() if p.is_dir()) == ["1.0.1"]


def test_an_install_cut_short_while_building_is_finished_by_the_next_run(uv_machine):
    """Killed during the build: a version folder without uv's receipt. The next
    run never switches to it, rebuilds it, and nothing else is left."""
    m = uv_machine
    _layout(m, "1.0.0")
    half = m.versions / "1.0.1" / "probe-research"
    half.mkdir(parents=True)
    (half / "bin").mkdir()
    out = _install("1.0.1")
    assert out.ok, out.problems
    _settled(m, "1.0.1")


def test_a_first_switch_cut_short_is_put_back_then_finished(uv_machine):
    """Killed between moving uv's folder and linking the tool path: `recover`
    puts it back first, then the install switches."""
    m = uv_machine
    m.uv("tool", "install", "probe-research[all]==1.0.0")
    installs._migrate(m.tools)  # noqa: SLF001 -- the first half of a switch, then "killed"
    assert installs.tool_state(m.tools) == installs.ToolPath.MISSING
    out = _install("1.0.1")
    assert out.ok, out.problems
    assert any("put back" in line for line in out.lines)
    _settled(m, "1.0.1")


def test_a_switch_whose_scripts_were_not_made_gets_them_next_run(uv_machine):
    """Killed after the switch, before the public scripts: the next run (or the
    cheap repair every wizard start makes) puts them back."""
    from probe.cli import bootstrap

    m = uv_machine
    _layout(m, "1.0.0")
    (m.bins / "probe").unlink()
    assert "put the `probe` command back" in bootstrap._repair_layout()  # noqa: SLF001
    assert m.probe() == "probe 1.0.0"


def test_without_uv_the_install_is_refused_with_the_command(uv_machine, monkeypatch):
    monkeypatch.setattr(install_pipeline.shutil, "which", lambda name: None)
    out = install_pipeline.install_cli("1.0.0")
    assert out.refused and install_pipeline.UV_INSTALL in out.refused
    assert "uv tool install 'probe-research[all]==1.0.0'" in out.refused


def test_the_daemon_extra_goes_in_a_generation_beside_the_running_env(uv_machine):
    """`probe daemon install` used to `uv tool install` the extra INTO the env
    every running `probe` reads its files from."""
    m = uv_machine
    _layout(m, "1.0.0")
    running = installs.active(m.tools)
    out = _install("1.0.0", mode=install_pipeline.Mode.DAEMON)
    assert out.ok and out.changed, out.problems
    assert installs.active(m.tools).parent.name == "1.0.0+g2"
    from probe.cli import updater

    assert "daemon" in updater.kept_from_uv_receipt(m.tool).extras
    assert "daemon" not in updater.kept_from_uv_receipt(running).extras, "the running env is as it was"


def test_prune_keeps_the_active_previous_and_in_use_generations(uv_machine, monkeypatch):
    m = uv_machine
    _layout(m, "1.0.0", "1.0.1", "1.0.2")
    broken = installs.active(m.tools)
    _corrupt(broken)
    _install("1.0.2")  # -> 1.0.2+g2 active, 1.0.2 previous
    old = time.time() - 3 * 24 * 3600
    for folder in m.versions.iterdir():
        if folder.is_dir():
            for path in (folder, folder / "probe-research" / "pyvenv.cfg"):
                if path.exists():
                    os.utime(path, (old, old))
    monkeypatch.setattr(installs, "_in_use", lambda folder, commands=None: folder.name == "1.0.0")
    removed = {p.name for p in installs.prune(m.tools, keep=0)}
    kept = {p.name for p in m.versions.iterdir() if p.is_dir()}
    assert {"1.0.2+g2", "1.0.2", "1.0.0"} <= kept and removed == {"1.0.1"}
    assert installs._version_key("1.0.2+g2") > installs._version_key("1.0.2") > installs._version_key("1.0.1")


def test_the_current_handoffs_stage1_reads_a_generation_from_dist_info(uv_machine, monkeypatch):
    """Deployed hand-offs read the active version from the env's dist-info,
    else the link target's folder name only when it is a release: `+g2` is not,
    so a generation is never read as another version. Today's stage 1 against a
    `+g2` layout: current at its version, and a newer release is installed and
    handed to."""
    m = uv_machine
    _layout(m, "1.0.0")
    _corrupt(installs.active(m.tools))
    _install("1.0.0")
    assert installs.active(m.tools).parent.name == "1.0.0+g2"
    layout = handoff.Layout(m.tools)
    assert layout.usable() and layout.active_version() == "1.0.0"
    assert handoff.release("1.0.0+g2") is None
    monkeypatch.setattr(handoff, "latest_release", lambda base_url, env: ("1.0.0", "manifest"))
    assert handoff.stage1("cli", tools=str(m.tools), install_inputs={"extras": ["all"], "with": []})["result"] \
        == handoff.Result.CURRENT
    # Newer: installed beside, then exec'd (stopped here, before the exec).
    monkeypatch.setattr(handoff, "latest_release", lambda base_url, env: ("1.0.1", "manifest"))
    execs = []

    def no_exec(python, argv, env, fd, before_exec):
        execs.append(str(python))
        raise OSError("not in a test")

    monkeypatch.setattr(handoff, "_exec", no_exec)
    answer = handoff.stage1("cli", tools=str(m.tools), install_inputs={"extras": ["all"], "with": []})
    assert answer["result"] == handoff.Result.EXEC_FAILED and answer["active"] == "1.0.0"
    assert execs == [str(m.versions / "1.0.1" / "probe-research" / "bin" / "python")]
    # A dangling generation link: no folder-name fallback reads `1.0.0+g2` as a release.
    import shutil

    shutil.rmtree(m.versions / "1.0.0+g2")
    assert layout.active_version() is None


def test_prune_counts_a_generation_as_the_version_it_holds_and_junk_goes_first(uv_machine, monkeypatch):
    """Lane L's rescue and R-T3's repair leave `<v>+g<N>` folders: one counts
    as the version its dist-info holds (newer than the `<v>` it replaced),
    never as junk. A `0.x.y+g2` active, an older previous, junk folders, and
    an inactive `+gN` a running process uses (a rescue's leftover L reuses)."""
    m = uv_machine
    _layout(m, "1.0.0", "1.0.1", "1.0.2")
    _corrupt(installs.active(m.tools))
    _install("1.0.2")
    assert installs.active(m.tools).parent.name == "1.0.2+g2"
    installs.set_fields(m.tools, previous=str(m.versions / "1.0.1" / "probe-research"))
    spare = m.versions / "1.0.0+g2"
    m.uv("tool", "install", "probe-research[all]==1.0.0", UV_TOOL_DIR=str(spare), UV_TOOL_BIN_DIR=str(spare / ".bin"))
    for junk in ("0.9.9", "unknown-1730000000", "1.0.0-1730000000"):
        (m.versions / junk).mkdir()
    old = time.time() - 3 * 24 * 3600
    for folder in m.versions.iterdir():
        if folder.is_dir():
            for path in (folder, folder / "probe-research" / "pyvenv.cfg", folder / "probe-research" / "bin" / "python"):
                if path.exists() or path.is_symlink():
                    os.utime(path, (old, old), follow_symlinks=False)
    ranked = sorted((p for p in m.versions.iterdir() if p.is_dir()), key=installs._place, reverse=True)
    assert [p.name for p in ranked[:4]] == ["1.0.2+g2", "1.0.2", "1.0.1", "1.0.0+g2"]
    assert {p.name for p in ranked[-3:]} == {"0.9.9", "unknown-1730000000", "1.0.0-1730000000"}
    monkeypatch.setattr(installs, "_in_use", lambda folder, commands=None: folder.name == "1.0.0+g2")
    removed = {p.name for p in installs.prune(m.tools, keep=2)}
    kept = {p.name for p in m.versions.iterdir() if p.is_dir()}
    assert {"1.0.2+g2", "1.0.2", "1.0.1", "1.0.0+g2"} <= kept, "active, the newest two, previous, in use"
    assert removed == {"1.0.0", "0.9.9", "unknown-1730000000", "1.0.0-1730000000"}


def test_a_pipx_install_moves_to_uv(uv_machine, tmp_path, monkeypatch):
    """R-T1: the managed install is uv's. pipx's `probe` is no failure of the
    uv install; `pipx uninstall` takes it away, and uv's `probe` takes its place."""
    m = uv_machine
    venv = tmp_path / "pipx" / "venvs" / "probe-research" / "bin"
    venv.mkdir(parents=True)
    (venv / "probe").write_text("#!/bin/sh\necho pipx\n")
    (venv / "probe").chmod(0o755)
    m.bins.mkdir(parents=True)
    (m.bins / "probe").symlink_to(venv / "probe")
    fake = tmp_path / "fakebin"
    fake.mkdir()
    (fake / "pipx").write_text(f"#!/bin/sh\n[ \"$1\" = uninstall ] && rm -f {m.bins / 'probe'}\n")
    (fake / "pipx").chmod(0o755)
    monkeypatch.setenv("PATH", f"{fake}{os.pathsep}{os.environ['PATH']}")
    out = _install("1.0.1")
    assert out.ok and not out.problems, out.problems
    assert any("pipx's until it moves" in line for line in out.lines)
    moved = install_pipeline.migrate_foreign(("pipx", str(m.bins / "probe")))
    assert moved[0].startswith("moved the CLI from pipx to uv"), moved
    _settled(m, "1.0.1")


def test_a_pipx_install_this_process_runs_from_is_not_removed_under_it(monkeypatch):
    from probe.cli import bootstrap

    monkeypatch.setattr(bootstrap, "_is_this_install", lambda binary: True)
    ran = []
    monkeypatch.setattr(install_pipeline.subprocess, "run", lambda *a, **k: ran.append(a))
    said = install_pipeline.migrate_foreign(("pipx", "/home/x/.local/bin/probe"))
    assert ran == [] and "pipx uninstall probe-research" in said[0]


def test_the_wizards_install_over_the_same_version_checks_and_repairs_it(uv_machine, monkeypatch):
    """R-T3 through the wizard's entry (`bootstrap.verify_installed`, what
    `--action configure` runs over a current CLI): a broken active env is
    rebuilt and switched to, the keeper may come back, runtime.json names the
    new env, and a service on the old one is restarted onto it."""
    from probe.cli import bootstrap, repair
    from probe.service import client, keeper, paths

    m = uv_machine
    _layout(m, "1.0.1")
    _corrupt(installs.active(m.tools))
    off = paths.root_dir() / keeper.OFF_NAME
    off.parent.mkdir(parents=True, exist_ok=True)
    off.touch()
    restarted = []
    monkeypatch.setattr(repair, "repair_service", lambda out: restarted.append(out.env) or repair.Part())
    result = bootstrap.verify_installed()
    assert result is not None and result.installed and result.message.startswith("Repaired"), result
    _settled(m, "1.0.1")
    assert installs.active(m.tools).parent.name == "1.0.1+g2" and restarted == [installs.active(m.tools)]
    assert not off.exists()
    assert json.loads(paths.runtime_path().read_text())["python"] == str(installs.env_python(installs.active(m.tools)))
    assert client.runtime_python() == str(installs.env_python(installs.active(m.tools)))
    # Healthy now: the same check changes nothing, and restarts nothing.
    again = bootstrap.verify_installed()
    assert again.already_persistent and not again.installed and len(restarted) == 1


def test_the_real_adopt_switches_to_a_generation_and_prune_keeps_both(uv_machine, monkeypatch):
    """The update's own switch (`core.adopt._adopt`, what a hand-off's exec'd
    release runs; lane L's rescue too) onto a `<v>+g2` target, then `prune`:
    the generation is active, the env it replaced stays to switch back to,
    runtime.json names the generation, and the service's restart check sees
    the env move although the version did not."""
    from probe.cli import updater
    from probe.core import adopt
    from probe.service import client
    from probe.service import updater as service_updater

    m = uv_machine
    _layout(m, "1.0.0")
    replaced = installs.active(m.tools)
    target = installs.install("1.0.0", "probe-research[all]==1.0.0", tools=m.tools, rebuild=True)
    assert target.parent.name == "1.0.0+g2" and installs.env_version(target) == "1.0.0"
    assert replaced.exists(), "the active env was never removed for the rebuild"
    monkeypatch.setattr(adopt, "_runs_from", lambda env: env == target)  # the exec'd release runs from it
    monkeypatch.setattr(updater, "fetch_latest", lambda base_url: (_ for _ in ()).throw(OSError("offline")))
    assert adopt._adopt(target, "", "1.0.0") is None  # noqa: SLF001 -- the switch itself
    assert installs.active(m.tools) == target.resolve()
    assert installs.previous(m.tools) == replaced
    assert client.runtime_python() == str(installs.env_python(target))
    assert service_updater._env_moved(replaced) and not service_updater._env_moved(target.resolve())
    old = time.time() - 3 * 24 * 3600
    for folder in m.versions.iterdir():
        if folder.is_dir():
            os.utime(folder / "probe-research" / "pyvenv.cfg", (old, old))
    assert installs.prune(m.tools, keep=0) == []
    assert {p.name for p in m.versions.iterdir() if p.is_dir()} == {"1.0.0", "1.0.0+g2"}
    _settled(m, "1.0.0")
