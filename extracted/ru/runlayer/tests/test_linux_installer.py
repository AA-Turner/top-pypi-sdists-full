"""Linux package installer tests."""

from pathlib import Path
from typing import cast

import pytest

from runlayer_cli.installer_common import (
    InstallerExecutionError,
    InstallerVerificationError,
    UnsupportedInstallerError,
    run_checked,
    validate_artifact,
)
from runlayer_cli.linux_installer import LinuxPackageInstaller
from tests.platform_installer_helpers import (
    RecordingRunner,
    artifact,
    artifact_path,
    assert_argv_without_shell,
    result,
)


def test_deb_uses_dpkg_install(tmp_path: Path) -> None:
    value = artifact("linux", "deb", "runlayer_2.0.0_amd64.deb")
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(stdout="runlayer\n"),
        result(stdout="2.0.0\n"),
        result(stdout="amd64\n"),
        result(),
    )

    LinuxPackageInstaller(package_name="runlayer", runner=runner).verify_and_install(
        path,
        artifact=value,
        from_version="1.0.0",
        to_version="2.0.0",
    )

    assert runner.calls[0][0] == [
        "/usr/bin/dpkg-deb",
        "--field",
        str(path.resolve()),
        "Package",
    ]
    assert runner.calls[1][0] == [
        "/usr/bin/dpkg-deb",
        "--field",
        str(path.resolve()),
        "Version",
    ]
    assert runner.calls[2][0] == [
        "/usr/bin/dpkg-deb",
        "--field",
        str(path.resolve()),
        "Architecture",
    ]
    assert runner.calls[3][0] == [
        "/usr/bin/dpkg",
        "--force-confdef",
        "--force-confold",
        "--install",
        str(path.resolve()),
    ]
    env = cast(dict[str, str], runner.calls[3][1]["env"])
    assert env["DEBIAN_FRONTEND"] == "noninteractive"
    assert_argv_without_shell(runner)


@pytest.mark.parametrize(
    ("from_version", "to_version"),
    [
        ("1.0.0", "2.0.0"),
        ("2.0.0", "1.0.0"),
        ("2.0.0", "arbitrary-backend-target"),
    ],
)
def test_rpm_always_allows_backend_authoritative_target(
    tmp_path: Path,
    from_version: str,
    to_version: str,
) -> None:
    value = artifact("linux", "rpm", "runlayer-2.0.0.x86_64.rpm")
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(stdout="runlayer"),
        result(stdout=to_version),
        result(stdout="x86_64"),
        result(),
    )

    LinuxPackageInstaller(package_name="runlayer", runner=runner).verify_and_install(
        path,
        artifact=value,
        from_version=from_version,
        to_version=to_version,
    )

    assert runner.calls[0][0] == [
        "/usr/bin/rpm",
        "--query",
        "--package",
        "--queryformat",
        "%{NAME}",
        str(path.resolve()),
    ]
    assert runner.calls[1][0] == [
        "/usr/bin/rpm",
        "--query",
        "--package",
        "--queryformat",
        "%{VERSION}",
        str(path.resolve()),
    ]
    assert runner.calls[2][0] == [
        "/usr/bin/rpm",
        "--query",
        "--package",
        "--queryformat",
        "%{ARCH}",
        str(path.resolve()),
    ]
    assert runner.calls[3][0] == [
        "/usr/bin/rpm",
        "-U",
        "--oldpackage",
        str(path.resolve()),
    ]


def test_rejects_other_runlayer_product_before_install(tmp_path: Path) -> None:
    value = artifact("linux", "deb", "aiwatch.deb")
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(result(stdout="runlayer\n"))

    with pytest.raises(InstallerVerificationError, match="requested product"):
        LinuxPackageInstaller(
            package_name="runlayer-aiwatch", runner=runner
        ).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )

    assert len(runner.calls) == 1


def test_rejects_package_with_unexpected_version(tmp_path: Path) -> None:
    value = artifact("linux", "deb", "runlayer_2.0.0_amd64.deb")
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(stdout="runlayer\n"),
        result(stdout="1.9.0\n"),
    )

    with pytest.raises(InstallerVerificationError, match="backend-selected version"):
        LinuxPackageInstaller(package_name="runlayer", runner=runner).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )

    assert len(runner.calls) == 2


@pytest.mark.parametrize(
    ("format_", "filename"),
    [
        ("deb", "runlayer_2.0.0_amd64.deb"),
        ("rpm", "runlayer-2.0.0.x86_64.rpm"),
    ],
)
def test_rejects_package_with_unexpected_architecture(
    tmp_path: Path,
    format_: str,
    filename: str,
) -> None:
    value = artifact("linux", format_, filename)
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(stdout="runlayer\n"),
        result(stdout="2.0.0\n"),
        result(stdout="wrong-arch\n"),
    )

    with pytest.raises(InstallerVerificationError, match="architecture"):
        LinuxPackageInstaller(package_name="runlayer", runner=runner).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )

    assert len(runner.calls) == 3


@pytest.mark.parametrize(
    ("format_", "filename"),
    [
        ("deb", "runlayer_2.0.0_amd64.deb"),
        ("rpm", "runlayer-2.0.0.x86_64.rpm"),
    ],
)
def test_package_commands_use_minimal_environment(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    format_: str,
    filename: str,
) -> None:
    for name in ("RUNLAYER_API_KEY", "AWS_SECRET_ACCESS_KEY", "GITHUB_TOKEN"):
        monkeypatch.setenv(name, "secret")
    value = artifact("linux", format_, filename)
    path = artifact_path(tmp_path, value)
    runner = RecordingRunner(
        result(stdout="runlayer\n"),
        result(stdout="2.0.0\n"),
        result(stdout="amd64\n" if format_ == "deb" else "x86_64\n"),
        result(),
    )

    LinuxPackageInstaller(package_name="runlayer", runner=runner).verify_and_install(
        path,
        artifact=value,
        from_version="1.0.0",
        to_version="2.0.0",
    )

    for _, kwargs in runner.calls:
        env = cast(dict[str, str], kwargs["env"])
        expected = {
            "LANG": "C",
            "LC_ALL": "C",
            "PATH": "/usr/sbin:/usr/bin:/sbin:/bin",
        }
        if format_ == "deb":
            expected["DEBIAN_FRONTEND"] = "noninteractive"
        assert env == expected


def test_run_checked_includes_native_failure_output() -> None:
    runner = RecordingRunner(
        result(
            returncode=1,
            stdout="partial package output\n",
            stderr="dependency conflict\n",
        )
    )

    with pytest.raises(InstallerExecutionError) as exc_info:
        run_checked(runner, ["/usr/bin/dpkg"], verification=False)

    message = str(exc_info.value)
    assert "partial package output" in message
    assert "dependency conflict" in message


def test_run_checked_bounds_native_failure_output() -> None:
    runner = RecordingRunner(
        result(returncode=1, stderr=f"discarded-prefix\n{'x' * 5000}\nfinal error")
    )

    with pytest.raises(InstallerExecutionError) as exc_info:
        run_checked(runner, ["/usr/bin/dpkg"], verification=False)

    message = str(exc_info.value)
    assert "discarded-prefix" not in message
    assert "[output truncated]" in message
    assert message.endswith("final error")
    assert len(message) < 4300


def test_rejects_non_native_format(tmp_path: Path) -> None:
    value = artifact("linux", "tar.gz", "aiwatch.tar.gz")
    path = artifact_path(tmp_path, value)

    with pytest.raises(UnsupportedInstallerError):
        LinuxPackageInstaller(
            package_name="runlayer-aiwatch",
            runner=RecordingRunner(),
        ).verify_and_install(
            path,
            artifact=value,
            from_version="1.0.0",
            to_version="2.0.0",
        )


def test_shared_validator_accepts_compound_format(tmp_path: Path) -> None:
    value = artifact("linux", "tar.gz", "aiwatch-2.0.0-linux-x86_64.tar.gz")
    path = artifact_path(tmp_path, value)

    assert validate_artifact(
        path,
        value,
        platform="linux",
        formats=("tar.gz",),
    ) == path.resolve()
