"""Windows MDM console-home reparse-point regression tests."""

from __future__ import annotations

import errno
from pathlib import Path

import pytest

from runlayer_cli.hook_install import (
    Client,
    ClientStatus,
    InstallScope,
    check_absent_client,
    check_client,
    install_client,
)
from runlayer_cli.hook_install import check as check_module
from runlayer_cli.hook_install import clients as clients_module
from runlayer_cli.hook_install import safe_fs
from runlayer_cli.hook_install.clients import uninstall_client


_WINDOWS_CONSOLE_HOME_CASES = (
    (Client.VSCODE, "enterprise_vscode_dir", Path(".copilot/hooks/runlayer.json")),
    (Client.HERMES, "enterprise_hermes_dir", Path(".hermes/config.yaml")),
    (
        Client.GOOSE,
        "enterprise_goose_dir",
        Path(".agents/plugins/runlayer-hooks/hooks/hooks.json"),
    ),
)


def _patch_client_path(
    monkeypatch: pytest.MonkeyPatch,
    *,
    home: Path,
    path_function: str,
    config_path: Path,
) -> Path:
    resolved_path = home / config_path
    config_dir = (
        resolved_path.parent.parent
        if path_function == "enterprise_goose_dir"
        else resolved_path.parent
    )
    monkeypatch.setattr(clients_module, path_function, lambda: config_dir)
    monkeypatch.setattr(clients_module, "_reown_to_console_user", lambda _path: None)
    monkeypatch.setattr(safe_fs.platform, "system", lambda: "Windows")
    return resolved_path


@pytest.mark.parametrize(
    ("client", "path_function", "config_path"),
    _WINDOWS_CONSOLE_HOME_CASES,
)
def test_windows_mdm_install_refuses_reparse_point(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    client: Client,
    path_function: str,
    config_path: Path,
) -> None:
    home = tmp_path / "Users" / "alice"
    target = _patch_client_path(
        monkeypatch,
        home=home,
        path_function=path_function,
        config_path=config_path,
    )
    privileged = tmp_path / "privileged-config"
    privileged.write_text("must remain unchanged")
    target.parent.mkdir(parents=True)
    target.symlink_to(privileged)

    with pytest.raises(OSError) as exc_info:
        install_client(
            client,
            scope=InstallScope.MDM,
            hook_command="C:/Program Files/Runlayer/AIWatch/aiwatch.exe hook",
        )

    assert exc_info.value.errno == errno.ELOOP
    assert target.is_symlink()
    assert privileged.read_text() == "must remain unchanged"


@pytest.mark.parametrize(
    ("client", "path_function", "config_path"),
    _WINDOWS_CONSOLE_HOME_CASES,
)
def test_windows_mdm_uninstall_refuses_reparse_point(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    client: Client,
    path_function: str,
    config_path: Path,
) -> None:
    home = tmp_path / "Users" / "alice"
    target = _patch_client_path(
        monkeypatch,
        home=home,
        path_function=path_function,
        config_path=config_path,
    )
    privileged = tmp_path / "privileged-config"
    privileged.write_text("must remain unchanged")
    target.parent.mkdir(parents=True)
    target.symlink_to(privileged)

    result = uninstall_client(client, scope=InstallScope.MDM)

    assert not result.changed
    assert result.skipped_reason == "unsafe Windows MDM hooks path"
    assert target.is_symlink()
    assert privileged.read_text() == "must remain unchanged"


def test_user_scope_does_not_apply_windows_mdm_guard(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    target = tmp_path / "user" / ".hermes" / "config.yaml"
    target.parent.mkdir(parents=True)
    target.symlink_to(tmp_path / "missing")
    monkeypatch.setattr(safe_fs.platform, "system", lambda: "Windows")

    assert not safe_fs.is_unsafe_windows_mdm_path(target, mdm=False)


def test_windows_mdm_check_reports_console_home_reparse_point(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "Users" / "alice"
    target = _patch_client_path(
        monkeypatch,
        home=home,
        path_function="enterprise_hermes_dir",
        config_path=Path(".hermes/config.yaml"),
    )
    privileged = tmp_path / "privileged-config"
    privileged.write_text("hooks: {}\n")
    target.parent.mkdir(parents=True)
    target.symlink_to(privileged)
    monkeypatch.setattr(check_module, "client_is_installed", lambda *_a, **_kw: True)

    result = check_client(Client.HERMES, scope=InstallScope.MDM)

    assert result.status == ClientStatus.DRIFTED
    assert result.detail == "unsafe Windows MDM hooks path"


def test_windows_mdm_absent_check_reports_console_home_reparse_point(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    home = tmp_path / "Users" / "alice"
    target = _patch_client_path(
        monkeypatch,
        home=home,
        path_function="enterprise_hermes_dir",
        config_path=Path(".hermes/config.yaml"),
    )
    privileged = tmp_path / "privileged-config"
    privileged.write_text("hooks: {}\n")
    target.parent.mkdir(parents=True)
    target.symlink_to(privileged)

    result = check_absent_client(Client.HERMES, scope=InstallScope.MDM)

    assert result.status == ClientStatus.DRIFTED
    assert result.detail == "unsafe Windows MDM hooks path"
