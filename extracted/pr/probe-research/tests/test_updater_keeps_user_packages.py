"""`probe update` keeps what the user added to the install (#2043 review, MED1).

Plan 2.11 has every update restate `probe-research[all]` so the release that
takes the CLI's dependencies out of core cannot strip `probe`. But `uv tool
install` REPLACES the tool's receipt: an install made with `--with wandb`
(which `probe import wandb` needs) came out of the update as `[all]` only,
wandb uninstalled -- on every `probe update` and every background auto-update.

These run the REAL `uv` against hand-built wheels, offline, in a private tool
directory: a fake `probe-research` whose `all` extra needs `fakecli` and whose
`mcp-http` extra needs `fakehttp`, and a `sixfake` the user added with `--with`.
"""

from __future__ import annotations

import base64
import hashlib
import json
import os
import shutil
import subprocess
import sys
import zipfile
from pathlib import Path

import pytest

from probe.cli import updater

pytestmark = pytest.mark.skipif(shutil.which("uv") is None, reason="needs uv on PATH")


def _wheel(directory: Path, name: str, version: str, *, extras=None, script=None) -> None:
    dist = name.replace("-", "_")
    module = f"{dist}_mod"
    info = f"{dist}-{version}.dist-info"
    meta = ["Metadata-Version: 2.1", f"Name: {name}", f"Version: {version}"]
    for extra, needs in (extras or {}).items():
        meta.append(f"Provides-Extra: {extra}")
        meta += [f'Requires-Dist: {need}; extra == "{extra}"' for need in needs]
    files = {
        f"{module}/__init__.py": b"def main():\n    print('ok')\n",
        f"{info}/METADATA": ("\n".join(meta) + "\n").encode(),
        f"{info}/WHEEL": b"Wheel-Version: 1.0\nGenerator: test\nRoot-Is-Purelib: true\nTag: py3-none-any\n",
    }
    if script:
        files[f"{info}/entry_points.txt"] = f"[console_scripts]\n{script} = {module}:main\n".encode()
    record = []
    for path, data in files.items():
        digest = base64.urlsafe_b64encode(hashlib.sha256(data).digest()).rstrip(b"=").decode()
        record.append(f"{path},sha256={digest},{len(data)}")
    record.append(f"{info}/RECORD,,")
    files[f"{info}/RECORD"] = ("\n".join(record) + "\n").encode()
    with zipfile.ZipFile(directory / f"{dist}-{version}-py3-none-any.whl", "w") as whl:
        for path, data in files.items():
            whl.writestr(path, data)


@pytest.fixture
def uv_tools(tmp_path, monkeypatch):
    """A private, offline uv tool setup with the fake wheels on a find-links dir.
    Yields (run, tool_dir): ``run(cmd)`` runs a command in that setup."""
    wheels = tmp_path / "wheels"
    wheels.mkdir()
    for version in ("1.0.0", "1.0.1"):
        _wheel(
            wheels, "probe-research", version,
            extras={"all": ["fakecli"], "mcp-http": ["fakehttp"], "cli": ["fakecli"], "daemon": ["fakedaemon"]},
            script="probe",
        )
    for name in ("fakecli", "fakehttp", "sixfake", "fakedaemon"):
        _wheel(wheels, name, "1.0.0")
    env = {
        **os.environ,
        "UV_TOOL_DIR": str(tmp_path / "tools"),
        "UV_TOOL_BIN_DIR": str(tmp_path / "bin"),
        "UV_FIND_LINKS": str(wheels),
        "UV_NO_INDEX": "1",
        "UV_OFFLINE": "1",
        "UV_PYTHON": sys.executable,
        "UV_CACHE_DIR": str(tmp_path / "cache"),
    }
    # The test process may have the daemon's AI libraries; the fake has no
    # `daemon` extra, so keep `_dist()` from asking for one.
    monkeypatch.setitem(sys.modules, "pydantic_ai", None)
    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", None)
    # Also for code that runs `uv` itself (bootstrap), reading os.environ.
    for key in ("UV_TOOL_DIR", "UV_TOOL_BIN_DIR", "UV_FIND_LINKS", "UV_NO_INDEX", "UV_OFFLINE", "UV_PYTHON", "UV_CACHE_DIR"):
        monkeypatch.setenv(key, env[key])

    def run(cmd: list[str]) -> subprocess.CompletedProcess:
        done = subprocess.run(cmd, env=env, capture_output=True, text=True, timeout=120)
        assert done.returncode == 0, done.stderr[-2000:]
        return done

    yield run, tmp_path / "tools" / "probe-research"


def _has(tool_dir: Path, module: str) -> bool:
    python = tool_dir / "bin" / "python"
    return subprocess.run([str(python), "-c", f"import {module}"], capture_output=True).returncode == 0


def test_the_update_restates_the_users_with_packages_and_extras(uv_tools):
    run, tool = uv_tools
    run(["uv", "tool", "install", "probe-research[mcp-http]", "--with", "sixfake"])
    kept = updater.kept_from_uv_receipt(tool)
    assert kept is not None
    assert kept.extras == ("mcp-http",) and kept.with_packages == ("sixfake",)

    run(updater.uv_tool_install_command(kept))

    assert _has(tool, "sixfake_mod"), "the update uninstalled a package the user added"
    assert _has(tool, "fakehttp_mod") and _has(tool, "fakecli_mod")
    after = updater.kept_from_uv_receipt(tool)
    assert after is not None and after.with_packages == ("sixfake",)
    assert set(after.extras) == {"all", "mcp-http"}


def test_the_old_restatement_drops_them(uv_tools):
    """Negative control, and the bug as shipped in dc60fda43: restating only
    `probe-research[all]` replaces the receipt and uninstalls `--with` packages."""
    run, tool = uv_tools
    run(["uv", "tool", "install", "probe-research[mcp-http]", "--with", "sixfake"])
    run(["uv", "tool", "install", "probe-research[all]"])
    assert not _has(tool, "sixfake_mod")
    assert not _has(tool, "fakehttp_mod")


def test_the_pinned_fallback_keeps_them_too(uv_tools):
    """`uv tool upgrade` no-ops on a pinned install; the `@latest` install that
    follows must carry the same things."""
    run, tool = uv_tools
    run(["uv", "tool", "install", "probe-research[mcp-http]==1.0.0", "--with", "sixfake"])
    kept = updater.kept_from_uv_receipt(tool)
    run(updater.uv_tool_install_command(kept, version="@latest"))
    assert _has(tool, "sixfake_mod") and _has(tool, "fakehttp_mod") and _has(tool, "fakecli_mod")


def _sentinel(tool: Path) -> Path:
    """A file in the environment's `lib/pythonX.Y`, standing in for the files a
    running `probe` (a daemon worker) reads after it started."""
    lib = next((tool / "lib").glob("python3*"))
    path = lib / "site-packages" / "a-running-probe-reads-me.txt"
    path.write_text("x")
    return path


def _version(tool: Path) -> str:
    python = tool / "bin" / "python"
    done = subprocess.run(
        [str(python), "-c", "import importlib.metadata as m; print(m.version('probe-research'))"],
        capture_output=True, text=True, check=True,
    )
    return done.stdout.strip()


def test_the_daemon_install_adds_the_extra_without_rebuilding_the_environment(uv_tools):
    """2026-10-12: `--force` deleted and rebuilt the environment under a live
    daemon worker. `probe daemon install`'s command adds the extra in place."""
    run, tool = uv_tools
    run(["uv", "tool", "install", "probe-research[mcp-http]==1.0.0"])
    sentinel = _sentinel(tool)
    kept = updater.kept_from_uv_receipt(tool)
    wanted = updater.KeptInstall(extras=("daemon", *kept.extras), with_packages=kept.with_packages, python=kept.python)
    run(updater.uv_tool_install_command(wanted, version="==1.0.0"))
    assert sentinel.exists(), "the install rebuilt the environment under a running probe"
    assert _has(tool, "fakedaemon_mod") and _has(tool, "fakehttp_mod")


def test_the_update_fallback_upgrades_a_pinned_install_in_place(uv_tools):
    run, tool = uv_tools
    run(["uv", "tool", "install", "probe-research[mcp-http]==1.0.0"])
    sentinel = _sentinel(tool)
    run(updater.uv_tool_install_command(updater.kept_from_uv_receipt(tool), version="@latest"))
    assert _version(tool) == "1.0.1"
    assert sentinel.exists(), "the upgrade rebuilt the environment under a running probe"


def test_a_forced_reinstall_rebuilds_the_environment(uv_tools):
    """The control: what the two tests above would see with `--force`."""
    run, tool = uv_tools
    run(["uv", "tool", "install", "probe-research[mcp-http]==1.0.0"])
    sentinel = _sentinel(tool)
    run(updater.uv_tool_install_command(updater.kept_from_uv_receipt(tool), force=True, version="@latest"))
    assert not sentinel.exists()


def test_what_a_receipt_cannot_restate_is_left_out_and_named(tmp_path):
    """An editable `--with`, constraints, a receipt that is not TOML: what
    cannot be restated faithfully is left out and NAMED (`dropped`), and the
    rest is restated. It used to make the whole receipt unrestatable, which
    held every later update on the in-place path for good (plan A4)."""
    receipt = tmp_path / "uv-receipt.toml"
    receipt.write_text(
        '[tool]\nrequirements = [{ name = "probe-research", extras = ["mcp-http"] }, '
        '{ name = "mine", editable = "/src/mine" }, { name = "wandb", specifier = ">=0.17" }]\n'
    )
    kept = updater.kept_from_uv_receipt(tmp_path)
    assert kept.extras == ("mcp-http",) and kept.with_packages == ("wandb>=0.17",)
    assert kept.dropped == ("--with mine",)
    assert "--with mine" in updater.dropped_note(kept)
    # What reinstalls the running env in place (no version to switch back to)
    # still leaves such a receipt alone.
    assert updater.faithful_kept_from_uv_receipt(tmp_path) is None
    receipt.write_text('[tool]\nrequirements = [{ name = "probe-research" }]\nconstraints = [{ name = "x" }]\n')
    assert updater.kept_from_uv_receipt(tmp_path).dropped == ("its constraints",)
    receipt.write_text("[tool\nnot toml")
    assert updater.kept_from_uv_receipt(tmp_path) == updater.KeptInstall(dropped=("the uv receipt (not valid TOML)",))
    assert updater.dropped_note(updater.KeptInstall()) == ""


def test_probe_itself_from_a_path_is_never_restated(tmp_path):
    """A checkout's or a build's own probe-research: no update from the index replaces it."""
    (tmp_path / "uv-receipt.toml").write_text(
        '[tool]\nrequirements = [{ name = "probe-research", directory = "/src/research-os/agent" }]\n'
    )
    assert updater.kept_from_uv_receipt(tmp_path) is None


def test_the_update_leaves_an_unrestatable_receipt_alone(monkeypatch):
    """Through `upgrade_cli`: a receipt it cannot restate -> no restating
    install, and the result SAYS `[all]` is not recorded (#2043 review)."""
    calls: list[list[str]] = []
    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: None)
    monkeypatch.setattr(updater, "_run", lambda cmd, timeout: calls.append(cmd) or subprocess.CompletedProcess(cmd, 0))
    monkeypatch.setattr(updater, "_finalize", lambda before, target, tool: updater.CliResult(True, True, True, before, target, "ok"))
    result = updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "1.0.0", "1.1.0")
    assert calls == [["uv", "tool", "upgrade", "probe-research"]]
    assert "NOT recorded" in result.message


def test_a_failed_restatement_is_not_reported_as_an_upgrade(monkeypatch):
    """`[all]` is restated before the upgrade; if that fails, the update stops
    there and says so -- never "CLI upgraded" over a receipt without `[all]`."""
    calls: list[list[str]] = []

    def run(cmd, timeout):
        calls.append(cmd)
        return subprocess.CompletedProcess(cmd, 2 if cmd[:3] == ["uv", "tool", "install"] else 0)

    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: updater.KeptInstall())
    monkeypatch.setitem(sys.modules, "pydantic_ai", None)
    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", None)
    monkeypatch.setattr(updater, "_run", run)
    result = updater.upgrade_cli(updater.Install(updater.Method.UV_TOOL), "1.0.0", "1.1.0")
    assert calls == [["uv", "tool", "install", "probe-research[all]"]]
    assert not result.ok and not result.changed and "not upgraded" in result.message


def test_pipx_keeps_the_extras_its_spec_recorded(tmp_path, monkeypatch):
    """`pipx install --force probe-research[all]` would record `[all]` alone:
    the extras the install was made with stay in the spec."""
    (tmp_path / "pipx_metadata.json").write_text(
        json.dumps({"main_package": {"package": "probe-research", "package_or_url": "probe-research[mcp-http]"}})
    )
    monkeypatch.setattr(sys, "prefix", str(tmp_path))
    monkeypatch.setitem(sys.modules, "pydantic_ai", None)
    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", None)
    calls: list[list[str]] = []
    monkeypatch.setattr(updater, "_run", lambda cmd, timeout: calls.append(cmd) or subprocess.CompletedProcess(cmd, 0))
    monkeypatch.setattr(updater, "_finalize", lambda before, target, tool: updater.CliResult(True, True, True, before, target, "ok"))
    updater.upgrade_cli(updater.Install(updater.Method.PIPX), "1.0.0", "1.1.0")
    assert calls == [["pipx", "install", "--force", "probe-research[all,mcp-http]"]]


def test_pipx_injected_packages_go_back_in(tmp_path, monkeypatch):
    """`pipx install --force` drops `pipx inject`-ed packages; the update
    re-injects what `pipx_metadata.json` records."""
    (tmp_path / "pipx_metadata.json").write_text(
        json.dumps(
            {
                "main_package": {"package": "probe-research", "package_or_url": "probe-research"},
                "injected_packages": {"wandb": {"package": "wandb", "package_or_url": "wandb==0.19.1"}},
            }
        )
    )
    monkeypatch.setattr(sys, "prefix", str(tmp_path))
    monkeypatch.setitem(sys.modules, "pydantic_ai", None)
    monkeypatch.setitem(sys.modules, "pydantic_ai_harness", None)
    calls: list[list[str]] = []
    monkeypatch.setattr(updater, "_run", lambda cmd, timeout: calls.append(cmd) or subprocess.CompletedProcess(cmd, 0))
    monkeypatch.setattr(updater, "_finalize", lambda before, target, tool: updater.CliResult(True, True, True, before, target, "ok"))
    updater.upgrade_cli(updater.Install(updater.Method.PIPX), "1.0.0", "1.1.0")
    assert calls == [
        ["pipx", "install", "--force", "probe-research[all]"],
        ["pipx", "inject", "probe-research", "wandb==0.19.1"],
    ]


def test_an_update_from_npx_keeps_the_permanent_installs_packages(uv_tools):
    """#2043 review LOW-MED. `npx probe-research update` (and the wizard's
    Update) runs from a throwaway environment and reinstalls the PERMANENT copy
    with `uv tool install --force probe-research[all]@latest`, which replaced
    its receipt: `--with six` gone, the Python changed. It restates the
    permanent install's receipt, found through `uv tool dir`."""
    from probe.cli import bootstrap

    run, tool = uv_tools
    run(["uv", "tool", "install", "probe-research[mcp-http]", "--with", "sixfake"])
    before = updater.kept_from_uv_receipt(tool)
    result = bootstrap.install_persistent(f"{bootstrap.INSTALL_SPEC}@latest")
    assert result.installed, result.message
    assert _has(tool, "sixfake_mod") and _has(tool, "fakehttp_mod") and _has(tool, "fakecli_mod")
    after = updater.kept_from_uv_receipt(tool)
    assert after.with_packages == ("sixfake",) and set(after.extras) == {"all", "mcp-http"}
    assert after.python == before.python


def test_a_reinstall_over_an_unrestatable_receipt_says_what_it_dropped(uv_tools, monkeypatch):
    """#2043 verify nit. `npx probe-research update` over a receipt it cannot
    restate reinstalls with `[all]` (it must: that is its job) and drops the
    entries it could not carry -- now saying so, as `probe update` does."""
    from probe.cli import bootstrap

    run, tool = uv_tools
    run(["uv", "tool", "install", "probe-research[mcp-http]", "--with", "sixfake"])
    monkeypatch.setattr(updater, "kept_from_uv_receipt", lambda prefix=None: None)
    result = bootstrap.install_persistent(f"{bootstrap.INSTALL_SPEC}@latest")
    assert result.installed, result.message
    assert "NOT carried over" in result.message
    assert _has(tool, "fakecli_mod")  # `[all]` is recorded either way


def test_the_forced_reinstall_reads_a_fresh_index():
    """R9: uv's cached index can predate a release by minutes, and `uv tool
    upgrade` takes no refresh flag, so the forced reinstall re-reads it."""
    command = updater.uv_tool_install_command(updater.KeptInstall(), force=True, version="@latest", refresh=True)
    assert command[:6] == ["uv", "tool", "install", "--force", "--refresh-package", "probe-research"]
    assert "--refresh-package" not in updater.uv_tool_install_command(updater.KeptInstall())
