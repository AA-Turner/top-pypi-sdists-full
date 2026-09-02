"""Behavior tests for frozen-binary update orchestration."""

from __future__ import annotations

import json
from pathlib import Path
import sys
from unittest.mock import patch

import pytest

from runlayer_cli.updater import (
    Artifact,
    ArtifactSelectionError,
    InstallDisposition,
    InstallTarget,
    TargetRelease,
    UpdateStatus,
    check_and_update,
)


class RecordingSource:
    def __init__(self, target: TargetRelease | None) -> None:
        self.target = target
        self.fetches: list[str] = []
        self.fetch_variants: list[str | None] = []
        self.downloads: list[tuple[str, str, Artifact]] = []
        self.destinations: list[Path] = []

    def fetch_target(
        self, package: str, *, variant: str | None
    ) -> TargetRelease | None:
        self.fetches.append(package)
        self.fetch_variants.append(variant)
        return self.target

    def download(
        self,
        package: str,
        version: str,
        artifact: Artifact,
        destination: Path,
    ) -> None:
        self.downloads.append((package, version, artifact))
        self.destinations.append(destination)
        destination.write_bytes(b"installer")


class RecordingInstaller:
    def __init__(
        self,
        disposition: InstallDisposition = InstallDisposition.APPLIED,
    ) -> None:
        self.installs: list[tuple[str, str, str]] = []
        self.disposition = disposition

    def verify_and_install(
        self,
        artifact_path: Path,
        *,
        artifact: Artifact,
        from_version: str,
        to_version: str,
    ) -> InstallDisposition:
        assert artifact_path.read_bytes() == b"installer"
        assert artifact_path.name == artifact.filename
        self.installs.append((artifact.filename, from_version, to_version))
        return self.disposition


class FailingInstaller:
    def __init__(self) -> None:
        self.artifact_path: Path | None = None

    def verify_and_install(
        self,
        artifact_path: Path,
        *,
        artifact: Artifact,
        from_version: str,
        to_version: str,
    ) -> None:
        self.artifact_path = artifact_path
        raise RuntimeError("vendor signature rejected")


def _target(version: str = "2.0.0", variant: str | None = None) -> TargetRelease:
    return TargetRelease(
        version=version,
        artifacts=(
            Artifact(
                platform="macos",
                arch="arm64",
                filename=f"aiwatch-{version}-macos-arm64.pkg",
                sha256="0" * 64,
                size_bytes=9,
                format="pkg",
                variant=variant,
            ),
        ),
    )


def _windows_target(version: str = "2.0.0") -> TargetRelease:
    return TargetRelease(
        version=version,
        artifacts=(
            Artifact(
                platform="windows",
                arch="x64",
                filename=f"aiwatch-{version}-windows-x64.msi",
                sha256="0" * 64,
                size_bytes=9,
                format="msi",
            ),
        ),
    )


@pytest.mark.parametrize(
    ("frozen_value", "expected_status"),
    [(None, UpdateStatus.NOT_FROZEN), (True, UpdateStatus.UPDATED)],
)
def test_runtime_defaults_to_sys_frozen_flag(
    monkeypatch: pytest.MonkeyPatch,
    frozen_value: bool | None,
    expected_status: UpdateStatus,
) -> None:
    if frozen_value is None:
        monkeypatch.delattr(sys, "frozen", raising=False)
    else:
        monkeypatch.setattr(sys, "frozen", frozen_value, raising=False)
    source = RecordingSource(_target())
    installer = RecordingInstaller()

    result = check_and_update(
        package="ai-watch",
        installed_version="1.0.0",
        source=source,
        installer=installer,
        install_target=InstallTarget(platform="macos", arch="arm64", format="pkg"),
    )

    assert result.status is expected_status
    expected_count = int(expected_status is UpdateStatus.UPDATED)
    assert len(source.fetches) == expected_count
    assert len(installer.installs) == expected_count


def test_equal_target_version_is_a_noop() -> None:
    source = RecordingSource(_target(version="2.0.0"))
    installer = RecordingInstaller()

    result = check_and_update(
        package="ai-watch",
        installed_version="2.0.0",
        source=source,
        installer=installer,
        install_target=InstallTarget(platform="macos", arch="arm64", format="pkg"),
        frozen=True,
    )

    assert result.status is UpdateStatus.UP_TO_DATE
    assert result.from_version == "2.0.0"
    assert result.to_version == "2.0.0"
    assert source.fetches == ["ai-watch"]
    assert source.downloads == []
    assert installer.installs == []


@pytest.mark.parametrize("target_version", ["3.0.0", "1.0.0"])
def test_any_different_target_installs_for_upgrade_or_downgrade(
    target_version: str,
) -> None:
    source = RecordingSource(_target(version=target_version))
    installer = RecordingInstaller()

    result = check_and_update(
        package="ai-watch",
        installed_version="2.0.0",
        source=source,
        installer=installer,
        install_target=InstallTarget(platform="macos", arch="arm64", format="pkg"),
        frozen=True,
    )

    filename = f"aiwatch-{target_version}-macos-arm64.pkg"
    assert result.status is UpdateStatus.UPDATED
    assert result.from_version == "2.0.0"
    assert result.to_version == target_version
    assert result.artifact_filename == filename
    assert source.downloads == [
        ("ai-watch", target_version, _target(target_version).artifacts[0])
    ]
    assert installer.installs == [("installer.pkg", "2.0.0", target_version)]


def test_minimum_target_skips_incompatible_scheduled_rollback() -> None:
    source = RecordingSource(_target(version="0.29.1"))
    installer = RecordingInstaller()

    result = check_and_update(
        package="cli",
        installed_version="0.29.2",
        source=source,
        installer=installer,
        install_target=InstallTarget(
            platform="macos",
            arch="arm64",
            format="pkg",
        ),
        frozen=True,
        minimum_target_version="0.29.2",
    )

    assert result.status is UpdateStatus.TARGET_BELOW_MINIMUM
    assert result.to_version == "0.29.1"
    assert source.fetches == ["cli"]
    assert source.downloads == []
    assert installer.installs == []


def test_minimum_target_allows_compatible_scheduled_target() -> None:
    source = RecordingSource(_target(version="0.29.2"))
    installer = RecordingInstaller()

    result = check_and_update(
        package="cli",
        installed_version="0.29.1",
        source=source,
        installer=installer,
        install_target=InstallTarget(
            platform="macos",
            arch="arm64",
            format="pkg",
        ),
        frozen=True,
        minimum_target_version="0.29.2",
    )

    assert result.status is UpdateStatus.UPDATED
    assert installer.installs == [("installer.pkg", "0.29.1", "0.29.2")]


def test_minimum_target_allows_newer_prerelease() -> None:
    source = RecordingSource(_target(version="0.29.3-rc.1"))
    installer = RecordingInstaller()

    result = check_and_update(
        package="cli",
        installed_version="0.29.2",
        source=source,
        installer=installer,
        install_target=InstallTarget(
            platform="macos",
            arch="arm64",
            format="pkg",
        ),
        frozen=True,
        minimum_target_version="0.29.2",
    )

    assert result.status is UpdateStatus.UPDATED
    assert installer.installs == [("installer.pkg", "0.29.2", "0.29.3-rc.1")]


def test_uses_short_local_filename_for_backend_artifact() -> None:
    remote_filename = f"{'é' * 250}.pkg"
    artifact = Artifact("macos", "arm64", remote_filename, "0" * 64, 9, "pkg")
    source = RecordingSource(TargetRelease(version="2.0.0", artifacts=(artifact,)))
    installer = RecordingInstaller()

    result = check_and_update(
        package="ai-watch",
        installed_version="1.0.0",
        source=source,
        installer=installer,
        install_target=InstallTarget(platform="macos", arch="arm64", format="pkg"),
        frozen=True,
    )

    assert result.status is UpdateStatus.UPDATED
    assert result.artifact_filename == remote_filename
    assert source.destinations[0].name == "installer.pkg"
    assert installer.installs == [("installer.pkg", "1.0.0", "2.0.0")]


def test_selects_exact_platform_arch_and_format_slot() -> None:
    artifacts = (
        Artifact("linux", "x86_64", "agent.deb", "0" * 64, 9, "deb"),
        Artifact("linux", "x86_64", "agent.rpm", "0" * 64, 9, "rpm"),
        Artifact("linux", "arm64", "agent-arm.rpm", "0" * 64, 9, "rpm"),
        Artifact("windows", "x64", "agent.msi", "0" * 64, 9, "msi"),
    )
    source = RecordingSource(TargetRelease(version="2.0.0", artifacts=artifacts))
    installer = RecordingInstaller()

    result = check_and_update(
        package="cli",
        installed_version="1.0.0",
        source=source,
        installer=installer,
        install_target=InstallTarget(platform="linux", arch="x86_64", format="rpm"),
        frozen=True,
    )

    assert result.artifact_filename == "agent.rpm"
    assert source.downloads == [("cli", "2.0.0", artifacts[1])]


def test_refuses_missing_or_ambiguous_install_slot() -> None:
    artifact = Artifact("linux", "x86_64", "agent.rpm", "0" * 64, 9, "rpm")
    installer = RecordingInstaller()

    for artifacts in ((), (artifact, artifact)):
        source = RecordingSource(TargetRelease(version="2.0.0", artifacts=artifacts))
        with pytest.raises(ArtifactSelectionError):
            check_and_update(
                package="cli",
                installed_version="1.0.0",
                source=source,
                installer=installer,
                install_target=InstallTarget(
                    platform="linux", arch="x86_64", format="rpm"
                ),
                frozen=True,
            )
        assert source.downloads == []

    assert installer.installs == []


def test_standard_target_ignores_variant_artifacts() -> None:
    artifacts = (
        Artifact("macos", "arm64", "agent-217.pkg", "0" * 64, 9, "pkg", "glibc2.17"),
        Artifact("macos", "arm64", "agent.pkg", "0" * 64, 9, "pkg"),
    )
    source = RecordingSource(TargetRelease(version="2.0.0", artifacts=artifacts))
    installer = RecordingInstaller()

    result = check_and_update(
        package="cli",
        installed_version="1.0.0",
        source=source,
        installer=installer,
        install_target=InstallTarget(platform="macos", arch="arm64", format="pkg"),
        frozen=True,
    )

    assert result.status is UpdateStatus.UPDATED
    assert result.artifact_filename == "agent.pkg"
    assert source.fetch_variants == [None]
    assert source.downloads == [("cli", "2.0.0", artifacts[1])]


def test_variant_target_installs_matching_variant_artifact() -> None:
    source = RecordingSource(_target(version="2.0.0", variant="glibc2.17"))
    installer = RecordingInstaller()

    result = check_and_update(
        package="cli",
        installed_version="1.0.0",
        source=source,
        installer=installer,
        install_target=InstallTarget(
            platform="macos", arch="arm64", format="pkg", variant="glibc2.17"
        ),
        frozen=True,
    )

    assert result.status is UpdateStatus.UPDATED
    assert source.fetch_variants == ["glibc2.17"]
    assert installer.installs == [("installer.pkg", "1.0.0", "2.0.0")]


def test_variant_target_selects_variant_over_standard_in_same_slot() -> None:
    artifacts = (
        Artifact("linux", "x86_64", "runlayer.deb", "0" * 64, 9, "deb"),
        Artifact(
            "linux",
            "x86_64",
            "runlayer-glibc2.17.deb",
            "0" * 64,
            9,
            "deb",
            "glibc2.17",
        ),
    )
    source = RecordingSource(TargetRelease(version="2.0.0", artifacts=artifacts))
    installer = RecordingInstaller()

    result = check_and_update(
        package="cli",
        installed_version="1.0.0",
        source=source,
        installer=installer,
        install_target=InstallTarget(
            platform="linux", arch="x86_64", format="deb", variant="glibc2.17"
        ),
        frozen=True,
    )

    assert result.status is UpdateStatus.UPDATED
    assert result.artifact_filename == "runlayer-glibc2.17.deb"
    assert source.downloads == [("cli", "2.0.0", artifacts[1])]


@pytest.mark.parametrize(
    "artifacts",
    [
        # Old backend ignores the variant param and serves standard artifacts.
        (Artifact("macos", "arm64", "agent.pkg", "0" * 64, 9, "pkg"),),
        (),
    ],
)
def test_variant_target_without_matching_artifact_is_a_quiet_noop(
    artifacts: tuple[Artifact, ...],
) -> None:
    source = RecordingSource(TargetRelease(version="2.0.0", artifacts=artifacts))
    installer = RecordingInstaller()

    with patch("runlayer_cli.updater.logger") as logger:
        result = check_and_update(
            package="cli",
            installed_version="1.0.0",
            source=source,
            installer=installer,
            install_target=InstallTarget(
                platform="macos", arch="arm64", format="pkg", variant="glibc2.17"
            ),
            frozen=True,
        )

    assert result.status is UpdateStatus.NO_TARGET
    assert source.fetch_variants == ["glibc2.17"]
    assert source.downloads == []
    assert installer.installs == []
    logger.info.assert_called_once_with(
        "binary_update_no_variant_target",
        package="cli",
        from_version="1.0.0",
        to_version="2.0.0",
        platform="macos",
        arch="arm64",
        format="pkg",
        variant="glibc2.17",
    )
    logger.error.assert_not_called()


def test_variant_target_still_refuses_ambiguous_install_slot() -> None:
    artifact = Artifact("macos", "arm64", "agent.pkg", "0" * 64, 9, "pkg", "glibc2.17")
    source = RecordingSource(TargetRelease(version="2.0.0", artifacts=(artifact,) * 2))
    installer = RecordingInstaller()

    with pytest.raises(ArtifactSelectionError, match=r"variant=glibc2\.17"):
        check_and_update(
            package="cli",
            installed_version="1.0.0",
            source=source,
            installer=installer,
            install_target=InstallTarget(
                platform="macos", arch="arm64", format="pkg", variant="glibc2.17"
            ),
            frozen=True,
        )

    assert source.downloads == []
    assert installer.installs == []


def test_structured_attempt_and_success_include_version_transition() -> None:
    source = RecordingSource(_target("2.0.0"))
    installer = RecordingInstaller()

    with patch("runlayer_cli.updater.logger") as logger:
        check_and_update(
            package="ai-watch",
            installed_version="1.0.0",
            source=source,
            installer=installer,
            install_target=InstallTarget(platform="macos", arch="arm64", format="pkg"),
            frozen=True,
        )

    fields = {
        "package": "ai-watch",
        "from_version": "1.0.0",
        "to_version": "2.0.0",
        "platform": "macos",
        "arch": "arm64",
        "format": "pkg",
        "variant": None,
    }
    assert logger.info.call_args_list == [
        (("binary_update_attempt",), fields),
        (("binary_update_success",), fields),
    ]
    logger.error.assert_not_called()


def test_scheduled_handoff_has_distinct_status_and_log_event() -> None:
    source = RecordingSource(_target("2.0.0"))
    installer = RecordingInstaller(InstallDisposition.SCHEDULED)

    with patch("runlayer_cli.updater.logger") as logger:
        result = check_and_update(
            package="ai-watch",
            installed_version="1.0.0",
            source=source,
            installer=installer,
            install_target=InstallTarget(platform="macos", arch="arm64", format="pkg"),
            frozen=True,
        )

    fields = {
        "package": "ai-watch",
        "from_version": "1.0.0",
        "to_version": "2.0.0",
        "platform": "macos",
        "arch": "arm64",
        "format": "pkg",
        "variant": None,
    }
    assert result.status is UpdateStatus.SCHEDULED
    assert logger.info.call_args_list == [
        (("binary_update_attempt",), fields),
        (("binary_update_scheduled",), fields),
    ]
    logger.error.assert_not_called()


def test_scheduled_handoff_persists_pending_outcome_marker(tmp_path: Path) -> None:
    marker_path = tmp_path / "aiwatch-update-outcome.json"

    result = check_and_update(
        package="ai-watch",
        installed_version="1.0.0",
        source=RecordingSource(_target("2.0.0")),
        installer=RecordingInstaller(InstallDisposition.SCHEDULED),
        install_target=InstallTarget(platform="macos", arch="arm64", format="pkg"),
        frozen=True,
        outcome_marker_path=marker_path,
        clock=lambda: 1_776_000_000.0,
    )

    assert result.status is UpdateStatus.SCHEDULED
    assert json.loads(marker_path.read_text()) == {
        "from_version": "1.0.0",
        "scheduled_at": 1_776_000_000.0,
        "to_version": "2.0.0",
    }


def test_next_tick_logs_verified_scheduled_update(tmp_path: Path) -> None:
    marker_path = tmp_path / "aiwatch-update-outcome.json"
    marker_path.write_text(
        json.dumps(
            {
                "from_version": "1.0.0",
                "scheduled_at": 1_776_000_000.0,
                "to_version": "2.0.0",
            }
        )
    )

    with patch("runlayer_cli.updater.logger") as logger:
        result = check_and_update(
            package="ai-watch",
            installed_version="2.0.0",
            source=RecordingSource(_target("2.0.0")),
            installer=RecordingInstaller(),
            install_target=InstallTarget(platform="windows", arch="x64", format="msi"),
            frozen=True,
            outcome_marker_path=marker_path,
            clock=lambda: 1_776_003_600.0,
        )

    assert result.status is UpdateStatus.UP_TO_DATE
    assert not marker_path.exists()
    logger.info.assert_called_once_with(
        "binary_update_verified",
        package="ai-watch",
        from_version="1.0.0",
        to_version="2.0.0",
        installed_version="2.0.0",
        platform="windows",
        arch="x64",
        format="msi",
        variant=None,
    )
    logger.warning.assert_not_called()


def test_next_tick_silently_clears_superseded_outcome_marker(tmp_path: Path) -> None:
    marker_path = tmp_path / "aiwatch-update-outcome.json"
    marker_path.write_text(
        json.dumps(
            {
                "from_version": "1.0.0",
                "scheduled_at": 1_776_000_000.0,
                "to_version": "2.0.0",
            }
        )
    )

    with patch("runlayer_cli.updater.logger") as logger:
        result = check_and_update(
            package="ai-watch",
            installed_version="3.0.0",
            source=RecordingSource(_target("3.0.0")),
            installer=RecordingInstaller(),
            install_target=InstallTarget(platform="windows", arch="x64", format="msi"),
            frozen=True,
            outcome_marker_path=marker_path,
            clock=lambda: 1_776_003_600.0,
        )

    assert result.status is UpdateStatus.UP_TO_DATE
    assert not marker_path.exists()
    logger.info.assert_not_called()
    logger.warning.assert_not_called()


def test_next_tick_warns_and_retries_suspected_rollback(tmp_path: Path) -> None:
    marker_path = tmp_path / "aiwatch-update-outcome.json"
    marker_path.write_text(
        json.dumps(
            {
                "from_version": "1.0.0",
                "scheduled_at": 1_776_000_000.0,
                "to_version": "2.0.0",
            }
        )
    )
    source = RecordingSource(_windows_target("2.0.0"))
    installer = RecordingInstaller(InstallDisposition.SCHEDULED)
    install_target = InstallTarget(platform="windows", arch="x64", format="msi")

    with patch("runlayer_cli.updater.logger") as logger:
        result = check_and_update(
            package="ai-watch",
            installed_version="1.0.0",
            source=source,
            installer=installer,
            install_target=install_target,
            frozen=True,
            outcome_marker_path=marker_path,
            clock=lambda: 1_776_003_600.0,
        )

    assert result.status is UpdateStatus.SCHEDULED
    assert source.downloads == [
        ("ai-watch", "2.0.0", _windows_target("2.0.0").artifacts[0])
    ]
    assert installer.installs == [("installer.msi", "1.0.0", "2.0.0")]
    assert json.loads(marker_path.read_text())["scheduled_at"] == 1_776_003_600.0
    logger.warning.assert_called_once_with(
        "binary_update_rollback_suspected",
        package="ai-watch",
        from_version="1.0.0",
        to_version="2.0.0",
        installed_version="1.0.0",
        platform="windows",
        arch="x64",
        format="msi",
        variant=None,
    )


def test_stale_scheduled_outcome_marker_is_pruned(tmp_path: Path) -> None:
    marker_path = tmp_path / "aiwatch-update-outcome.json"
    marker_path.write_text(
        json.dumps(
            {
                "from_version": "1.0.0",
                "scheduled_at": 1_776_000_000.0,
                "to_version": "2.0.0",
            }
        )
    )

    with patch("runlayer_cli.updater.logger") as logger:
        result = check_and_update(
            package="ai-watch",
            installed_version="2.0.0",
            source=RecordingSource(_target("2.0.0")),
            installer=RecordingInstaller(),
            install_target=InstallTarget(platform="windows", arch="x64", format="msi"),
            frozen=True,
            outcome_marker_path=marker_path,
            clock=lambda: 1_776_086_401.0,
        )

    assert result.status is UpdateStatus.UP_TO_DATE
    assert not marker_path.exists()
    logger.info.assert_not_called()
    logger.warning.assert_not_called()


def test_install_failure_is_logged_reraised_and_cleans_download() -> None:
    source = RecordingSource(_target("2.0.0"))
    installer = FailingInstaller()

    with (
        patch("runlayer_cli.updater.logger") as logger,
        pytest.raises(RuntimeError, match="vendor signature rejected"),
    ):
        check_and_update(
            package="ai-watch",
            installed_version="1.0.0",
            source=source,
            installer=installer,
            install_target=InstallTarget(platform="macos", arch="arm64", format="pkg"),
            frozen=True,
        )

    assert installer.artifact_path is not None
    assert not installer.artifact_path.exists()
    logger.error.assert_called_once_with(
        "binary_update_failure",
        package="ai-watch",
        from_version="1.0.0",
        to_version="2.0.0",
        platform="macos",
        arch="arm64",
        format="pkg",
        variant=None,
        error="vendor signature rejected",
    )
