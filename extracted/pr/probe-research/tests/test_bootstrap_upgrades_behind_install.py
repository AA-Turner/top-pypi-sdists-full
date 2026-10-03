"""`npx probe-research` leaves the installed `probe` on the version it ran.

The launcher runs the latest CLI in a throwaway environment exactly when the
installed one is behind, and the wizard's first step upgrades that installed
copy. It reinstalled UNPINNED, and uv satisfied that from its cache with the
very version it replaced: a 0.206.0 wizard left 0.205.4 installed
(2026-10-02), so the coding agents kept calling the old CLI and pi never saw
the daemon its wizard had just set.
"""

from __future__ import annotations

import subprocess

from probe import __version__
from probe.cli import bootstrap


def _behind(monkeypatch, *, before: str, after: str):
    """An installed copy at `before` that reads `after` once reinstalled."""
    calls: list[str] = []
    versions = iter([before, after])
    monkeypatch.setattr(bootstrap, "_resolves_on_path", lambda: False)
    monkeypatch.setattr(bootstrap, "installed_version", lambda: next(versions))

    def install(spec: str = bootstrap.INSTALL_SPEC):
        calls.append(spec)
        return bootstrap.BootstrapResult(installed=True, already_persistent=False, message="Installed")

    monkeypatch.setattr(bootstrap, "install_persistent", install)
    return calls


def test_a_behind_install_is_brought_to_this_exact_version(monkeypatch):
    calls = _behind(monkeypatch, before="0.0.1", after=__version__)

    result = bootstrap.ensure_persistent_install()

    assert calls == [f"{bootstrap.INSTALL_SPEC}=={__version__}"]
    assert result.installed
    assert result.message == f"Updated the installed `probe` 0.0.1 → {__version__}."


def test_an_install_still_behind_afterwards_says_so_and_how_to_fix_it(monkeypatch):
    _behind(monkeypatch, before="0.0.1", after="0.0.1")
    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: "/usr/bin/uv" if name == "uv" else None)

    result = bootstrap.ensure_persistent_install()

    assert not result.installed
    assert result.message.startswith("! the installed `probe` is still 0.0.1")
    assert f"uv tool install --force '{bootstrap.INSTALL_SPEC}=={__version__}'" in result.message


def test_no_install_at_all_installs_the_newest(monkeypatch):
    calls: list[str] = []
    monkeypatch.setattr(bootstrap, "_resolves_on_path", lambda: False)
    monkeypatch.setattr(bootstrap, "installed_version", lambda: None)
    monkeypatch.setattr(
        bootstrap,
        "install_persistent",
        lambda spec=bootstrap.INSTALL_SPEC: calls.append(spec)
        or bootstrap.BootstrapResult(True, False, "Installed"),
    )

    bootstrap.ensure_persistent_install()

    assert calls == [bootstrap.INSTALL_SPEC]


def test_a_pinned_reinstall_pins_the_uv_spec_and_reads_a_fresh_index(monkeypatch):
    seen: list[list[str]] = []

    def run(command, **kwargs):
        seen.append(list(command))
        return subprocess.CompletedProcess(command, 0, "", "")

    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: "/usr/bin/" + name if name == "uv" else None)
    monkeypatch.setattr(bootstrap.subprocess, "run", run)
    monkeypatch.setattr(bootstrap, "_persistent_tool_env", lambda command, name: None)

    result = bootstrap.install_persistent(f"{bootstrap.INSTALL_SPEC}==9.9.9")

    install = next(c for c in seen if c[:3] == ["uv", "tool", "install"])
    assert "--force" in install and "--refresh-package" in install
    assert any(arg.endswith("==9.9.9") for arg in install), install
    assert result.installed


def test_an_update_from_a_stale_copy_pins_to_the_newer_target(monkeypatch):
    """`probe update` passes the manifest's latest: a stale throwaway copy
    must not pin the install to itself when a newer one exists."""
    calls = _behind(monkeypatch, before="0.0.1", after="999.0.0")

    result = bootstrap.ensure_persistent_install(target="999.0.0")

    assert calls == [f"{bootstrap.INSTALL_SPEC}==999.0.0"]
    assert result.installed


def test_the_still_behind_hint_names_the_installer_this_machine_has(monkeypatch):
    _behind(monkeypatch, before="0.0.1", after="0.0.1")
    monkeypatch.setattr(bootstrap.shutil, "which", lambda name: "/usr/bin/pipx" if name == "pipx" else None)

    result = bootstrap.ensure_persistent_install()

    assert f"pipx install --force '{bootstrap.INSTALL_SPEC}=={__version__}'" in result.message
