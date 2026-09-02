"""Privilege-boundary tests for packaged self-update."""

import os
from pathlib import Path
from types import SimpleNamespace
import stat
import subprocess
import tempfile
from unittest.mock import patch

import pytest

from runlayer_cli.commands.update_privilege import (
    PRIVILEGED_HOST_ENV,
    PRIVILEGED_ORG_KEY_ENV,
    configure_privileged_temp_root,
    elevating_runner,
    run_privileged_update,
    validate_installation_layout,
)


@pytest.mark.parametrize(
    "argv",
    [
        ["/usr/sbin/installer", "-pkg", "/tmp/target.pkg", "-target", "/"],
        [
            "/usr/bin/dpkg",
            "--force-confdef",
            "--force-confold",
            "--install",
            "/tmp/target.deb",
        ],
        ["/usr/bin/rpm", "-U", "--oldpackage", "/tmp/target.rpm"],
    ],
)
def test_unix_native_install_requires_whole_process_elevation(
    argv: list[str],
) -> None:
    with (
        patch("runlayer_cli.commands.update_privilege.os.geteuid", return_value=501),
        patch("runlayer_cli.commands.update_privilege.subprocess.run") as run,
        pytest.raises(RuntimeError, match="privileged self-update continuation"),
    ):
        elevating_runner(
            argv,
            check=False,
            capture_output=True,
            text=True,
            shell=False,
            env=None,
        )

    run.assert_not_called()


def test_unix_native_verification_does_not_elevate() -> None:
    completed = subprocess.CompletedProcess([], 0, stdout="", stderr="")
    with (
        patch("runlayer_cli.commands.update_privilege.os.geteuid", return_value=501),
        patch(
            "runlayer_cli.commands.update_privilege.subprocess.run",
            return_value=completed,
        ) as run,
    ):
        elevating_runner(
            ["/usr/sbin/pkgutil", "--check-signature", "/tmp/target.pkg"],
            check=False,
            capture_output=True,
            text=True,
            shell=False,
            env=None,
        )
        elevating_runner(
            [
                "/usr/bin/rpm",
                "--query",
                "--package",
                "--queryformat",
                "%{NAME}",
                "/tmp/target.rpm",
            ],
            check=False,
            capture_output=True,
            text=True,
            shell=False,
            env=None,
        )

    assert run.call_args_list[0].args[0][0] == "/usr/sbin/pkgutil"
    assert run.call_args_list[1].args[0][0] == "/usr/bin/rpm"


def test_unix_native_install_runs_directly_inside_privileged_continuation() -> None:
    completed = subprocess.CompletedProcess([], 0, stdout="", stderr="")
    argv = ["/usr/bin/dpkg", "--install", "/var/tmp/target.deb"]
    with (
        patch("runlayer_cli.commands.update_privilege.os.geteuid", return_value=0),
        patch(
            "runlayer_cli.commands.update_privilege.subprocess.run",
            return_value=completed,
        ) as run,
    ):
        elevating_runner(
            argv,
            check=False,
            capture_output=True,
            text=True,
            shell=False,
            env=None,
        )

    assert run.call_args.args[0] == argv


@patch("runlayer_cli.commands.update_privilege.os.access", return_value=False)
def test_privileged_reexec_accepts_only_secure_installed_bundle(
    _caller_access: object,
    tmp_path: Path,
) -> None:
    installation_root = tmp_path / "usr"
    bin_dir = installation_root / "bin"
    bundle_root = installation_root / "lib" / "runlayer"
    bin_dir.mkdir(parents=True)
    bundle_root.mkdir(parents=True)
    executable = bundle_root / "runlayer"
    executable.write_text("packaged binary")
    library = bundle_root / "library.so"
    library.write_text("packaged library")
    (bundle_root / "library-alias.so").symlink_to(library)
    entrypoint = bin_dir / "runlayer"
    entrypoint.symlink_to(executable)
    secure_dirs = [
        installation_root,
        bin_dir,
        installation_root / "lib",
        bundle_root,
    ]
    try:
        executable.chmod(0o555)
        (bundle_root / "library.so").chmod(0o444)
        for directory in secure_dirs:
            directory.chmod(0o555)

        trusted = validate_installation_layout(
            entrypoint=entrypoint,
            bundle_root=bundle_root,
            installation_root=installation_root,
            running_executable=executable,
            required_uid=os.getuid(),
            ancestor_stop=installation_root,
        )
        assert trusted == executable.resolve()

        library.chmod(0o466)
        with pytest.raises(
            RuntimeError,
            match="group/other-writable|writable by the caller",
        ):
            validate_installation_layout(
                entrypoint=entrypoint,
                bundle_root=bundle_root,
                installation_root=installation_root,
                running_executable=executable,
                required_uid=os.getuid(),
                ancestor_stop=installation_root,
            )
        library.chmod(0o444)

        with pytest.raises(RuntimeError, match="not root-owned"):
            validate_installation_layout(
                entrypoint=entrypoint,
                bundle_root=bundle_root,
                installation_root=installation_root,
                running_executable=executable,
                required_uid=os.getuid() + 1,
                ancestor_stop=installation_root,
            )

        portable = tmp_path / "portable-runlayer"
        portable.write_text("portable binary")
        with pytest.raises(RuntimeError, match="fixed package-installed"):
            validate_installation_layout(
                entrypoint=entrypoint,
                bundle_root=bundle_root,
                installation_root=installation_root,
                running_executable=portable,
                required_uid=os.getuid(),
                ancestor_stop=installation_root,
            )
    finally:
        for directory in reversed(secure_dirs):
            directory.chmod(0o755)


def test_privileged_reexec_hands_off_only_required_update_context() -> None:
    completed = subprocess.CompletedProcess([], 0, stdout="", stderr="")
    executable = Path("/usr/local/lib/runlayer/runlayer/runlayer")
    host = "https://tenant.example.com"
    org_api_key = "rl_org_super-secret"
    with (
        patch.dict(
            os.environ,
            {
                "RUNLAYER_CA_BUNDLE": "/tmp/caller-ca.pem",
                "SSL_CERT_FILE": "/tmp/caller-cert.pem",
                "HTTPS_PROXY": "https://proxy.example.com",
            },
            clear=True,
        ),
        patch("runlayer_cli.commands.update_privilege.os.geteuid", return_value=501),
        patch(
            "runlayer_cli.commands.update_privilege._trusted_installed_executable",
            return_value=executable,
        ),
        patch(
            "runlayer_cli.commands.update_privilege.subprocess.run",
            return_value=completed,
        ) as run,
    ):
        run_privileged_update(
            package="cli",
            platform="macos",
            host=host,
            org_api_key=org_api_key,
            ca_bundle="/tmp/caller-ca.pem",
            ca_bundle_dir="/tmp/caller-ca-dir",
        )

    argv = run.call_args.args[0]
    assert argv == [
        "/usr/bin/sudo",
        (
            f"--preserve-env={PRIVILEGED_HOST_ENV},{PRIVILEGED_ORG_KEY_ENV},"
            "RUNLAYER_SELF_UPDATE_CA_BUNDLE,RUNLAYER_SELF_UPDATE_CA_DIR"
        ),
        "--",
        str(executable),
        "__self-update-root",
        "cli",
    ]
    assert host not in argv
    assert org_api_key not in argv
    assert run.call_args.kwargs["env"] == {
        PRIVILEGED_HOST_ENV: host,
        PRIVILEGED_ORG_KEY_ENV: org_api_key,
        "RUNLAYER_SELF_UPDATE_CA_BUNDLE": "/tmp/caller-ca.pem",
        "RUNLAYER_SELF_UPDATE_CA_DIR": "/tmp/caller-ca-dir",
    }
    assert "HTTPS_PROXY" not in run.call_args.kwargs["env"]
    assert run.call_args.kwargs["shell"] is False


def test_linux_cli_privileged_reexec_uses_exact_nfpm_layout() -> None:
    """The nfpm package installs one onedir tree at ``/usr/lib/runlayer`` and
    exposes its executable through ``/usr/bin/runlayer``; only that exact
    root-owned layout may cross the sudo boundary."""
    completed = subprocess.CompletedProcess([], 0, stdout="", stderr="")
    packaged_executable = Path("/usr/lib/runlayer/runlayer")
    with (
        patch("runlayer_cli.commands.update_privilege.os.geteuid", return_value=1000),
        patch(
            "runlayer_cli.commands.update_privilege.sys.executable",
            str(packaged_executable),
        ),
        patch(
            "runlayer_cli.commands.update_privilege.validate_installation_layout",
            return_value=packaged_executable,
        ) as validate,
        patch(
            "runlayer_cli.commands.update_privilege.subprocess.run",
            return_value=completed,
        ) as run,
    ):
        run_privileged_update(
            package="cli",
            platform="linux",
            host="https://tenant.example.com",
            org_api_key="test-key",
        )

    validate.assert_called_once_with(
        entrypoint=Path("/usr/bin/runlayer"),
        bundle_root=Path("/usr/lib/runlayer"),
        installation_root=Path("/usr"),
        running_executable=packaged_executable,
        required_uid=0,
        ancestor_stop=Path("/"),
    )
    assert run.call_args.args[0][3:] == [
        str(packaged_executable),
        "__self-update-root",
        "cli",
    ]


def test_privileged_reexec_omits_ca_handoff_when_unconfigured() -> None:
    completed = subprocess.CompletedProcess([], 0, stdout="", stderr="")
    executable = Path("/usr/local/lib/runlayer/runlayer/runlayer")
    with (
        patch("runlayer_cli.commands.update_privilege.os.geteuid", return_value=501),
        patch(
            "runlayer_cli.commands.update_privilege._trusted_installed_executable",
            return_value=executable,
        ),
        patch(
            "runlayer_cli.commands.update_privilege.subprocess.run",
            return_value=completed,
        ) as run,
    ):
        run_privileged_update(
            package="cli",
            platform="macos",
            host="https://tenant.example.com",
            org_api_key="rl_org_super-secret",
        )

    assert run.call_args.args[0][1] == (
        f"--preserve-env={PRIVILEGED_HOST_ENV},{PRIVILEGED_ORG_KEY_ENV}"
    )
    assert "RUNLAYER_SELF_UPDATE_CA_BUNDLE" not in run.call_args.kwargs["env"]
    assert "RUNLAYER_SELF_UPDATE_CA_DIR" not in run.call_args.kwargs["env"]


def test_privileged_reexec_hands_off_ca_directory_without_bundle() -> None:
    completed = subprocess.CompletedProcess([], 0, stdout="", stderr="")
    executable = Path("/usr/local/lib/runlayer/runlayer/runlayer")
    with (
        patch("runlayer_cli.commands.update_privilege.os.geteuid", return_value=501),
        patch(
            "runlayer_cli.commands.update_privilege._trusted_installed_executable",
            return_value=executable,
        ),
        patch(
            "runlayer_cli.commands.update_privilege.subprocess.run",
            return_value=completed,
        ) as run,
    ):
        run_privileged_update(
            package="cli",
            platform="macos",
            host="https://tenant.example.com",
            org_api_key="rl_org_super-secret",
            ca_bundle_dir="/tmp/caller-ca-dir",
        )

    assert run.call_args.args[0][1] == (
        f"--preserve-env={PRIVILEGED_HOST_ENV},{PRIVILEGED_ORG_KEY_ENV},"
        "RUNLAYER_SELF_UPDATE_CA_DIR"
    )
    assert run.call_args.kwargs["env"] == {
        PRIVILEGED_HOST_ENV: "https://tenant.example.com",
        PRIVILEGED_ORG_KEY_ENV: "rl_org_super-secret",
        "RUNLAYER_SELF_UPDATE_CA_DIR": "/tmp/caller-ca-dir",
    }


def test_privileged_reexec_rejects_an_already_root_caller() -> None:
    with (
        patch("runlayer_cli.commands.update_privilege.os.geteuid", return_value=0),
        patch(
            "runlayer_cli.commands.update_privilege._trusted_installed_executable"
        ) as trusted,
        patch("runlayer_cli.commands.update_privilege.subprocess.run") as run,
        pytest.raises(RuntimeError, match="non-root POSIX caller"),
    ):
        run_privileged_update(
            package="cli",
            platform="macos",
            host="https://tenant.example.com",
            org_api_key="rl_org_secret",
        )

    trusted.assert_not_called()
    run.assert_not_called()


def test_privileged_temp_root_clears_caller_temp_environment(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    secure_temp = Path("/secure-system-temp")
    metadata = SimpleNamespace(
        st_uid=0,
        st_mode=stat.S_IFDIR | stat.S_ISVTX | 0o777,
    )
    for name in ("TMPDIR", "TMP", "TEMP"):
        monkeypatch.setenv(name, "/caller-controlled")
    monkeypatch.setattr(tempfile, "tempdir", "/caller-controlled")

    with (
        patch(
            "runlayer_cli.commands.update_privilege._PRIVILEGED_TEMP_ROOT",
            secure_temp,
        ),
        patch.object(Path, "stat", return_value=metadata),
    ):
        configure_privileged_temp_root()

    assert tempfile.tempdir == str(secure_temp)
    assert all(name not in os.environ for name in ("TMPDIR", "TMP", "TEMP"))


@pytest.mark.parametrize(
    "metadata",
    [
        SimpleNamespace(
            st_uid=501,
            st_mode=stat.S_IFDIR | stat.S_ISVTX | 0o777,
        ),
        SimpleNamespace(st_uid=0, st_mode=stat.S_IFDIR | 0o777),
        SimpleNamespace(st_uid=0, st_mode=stat.S_IFREG | stat.S_ISVTX | 0o666),
    ],
)
def test_privileged_temp_root_rejects_unsafe_metadata(
    metadata: SimpleNamespace,
) -> None:
    with (
        patch.object(Path, "stat", return_value=metadata),
        pytest.raises(RuntimeError, match="not root-owned and sticky"),
    ):
        configure_privileged_temp_root()


@patch("runlayer_cli.commands.update_privilege.os.access", return_value=False)
def test_privileged_reexec_rejects_external_directory_symlink(
    _caller_access: object,
    tmp_path: Path,
) -> None:
    installation_root = tmp_path / "usr"
    bin_dir = installation_root / "bin"
    bundle_root = installation_root / "lib" / "runlayer"
    bin_dir.mkdir(parents=True)
    bundle_root.mkdir(parents=True)
    executable = bundle_root / "runlayer"
    executable.write_text("packaged binary")
    entrypoint = bin_dir / "runlayer"
    entrypoint.symlink_to(executable)

    external_root = tmp_path / "external"
    external_root.mkdir()
    (external_root / "caller-controlled.so").write_text("replace me")
    (bundle_root / "external").symlink_to(external_root, target_is_directory=True)

    secure_dirs = [
        installation_root,
        bin_dir,
        installation_root / "lib",
        bundle_root,
        external_root,
    ]
    try:
        executable.chmod(0o555)
        (external_root / "caller-controlled.so").chmod(0o666)
        for directory in secure_dirs:
            directory.chmod(0o555)

        with pytest.raises(RuntimeError, match="escapes its package bundle"):
            validate_installation_layout(
                entrypoint=entrypoint,
                bundle_root=bundle_root,
                installation_root=installation_root,
                running_executable=executable,
                required_uid=os.getuid(),
                ancestor_stop=installation_root,
            )
    finally:
        for directory in reversed(secure_dirs):
            directory.chmod(0o755)


@patch("runlayer_cli.commands.update_privilege.os.access", return_value=False)
def test_privileged_reexec_rejects_symlinked_trusted_root(
    _caller_access: object,
    tmp_path: Path,
) -> None:
    actual_root = tmp_path / "actual-usr"
    bin_dir = actual_root / "bin"
    bundle_root = actual_root / "lib" / "runlayer"
    bin_dir.mkdir(parents=True)
    bundle_root.mkdir(parents=True)
    executable = bundle_root / "runlayer"
    executable.write_text("packaged binary")
    (bin_dir / "runlayer").symlink_to(executable)

    installation_root = tmp_path / "usr"
    installation_root.symlink_to(actual_root, target_is_directory=True)
    secure_dirs = [actual_root, bin_dir, actual_root / "lib", bundle_root]
    try:
        executable.chmod(0o555)
        for directory in secure_dirs:
            directory.chmod(0o555)

        with pytest.raises(RuntimeError, match="symbolic link"):
            validate_installation_layout(
                entrypoint=installation_root / "bin" / "runlayer",
                bundle_root=installation_root / "lib" / "runlayer",
                installation_root=installation_root,
                running_executable=executable,
                required_uid=os.getuid(),
                ancestor_stop=installation_root,
            )
    finally:
        for directory in reversed(secure_dirs):
            directory.chmod(0o755)
