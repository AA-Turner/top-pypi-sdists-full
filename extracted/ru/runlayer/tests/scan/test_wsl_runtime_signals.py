from pathlib import Path
from unittest import mock

from runlayer_cli.scan import wsl_runtime_signals
from runlayer_cli.scan.device import DiscoveredWSLDistro
from runlayer_cli.scan.wsl_runtime_signals import scan_wsl_runtime_file_signals


def test_path_probe_distinguishes_missing_from_inaccessible() -> None:
    missing = mock.Mock()
    missing.stat.side_effect = FileNotFoundError
    inaccessible = mock.Mock()
    inaccessible.stat.side_effect = PermissionError

    assert wsl_runtime_signals._safe_exists(missing) is False
    assert wsl_runtime_signals._safe_exists(inaccessible) is None


def test_reports_docker_and_podman_file_signals(
    tmp_path: Path,
    monkeypatch,
) -> None:
    (tmp_path / "var" / "lib" / "docker").mkdir(parents=True)
    (tmp_path / "var" / "lib" / "containers").mkdir(parents=True)
    monkeypatch.setattr(
        wsl_runtime_signals,
        "get_wsl_distro_root",
        lambda _distro: tmp_path,
    )

    result = scan_wsl_runtime_file_signals(
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)]
    )

    assert result[0].scanned is True
    assert result[0].container_runtimes == ("docker", "podman")


def test_inaccessible_probe_keeps_true_runtime_but_withholds_scan_authority(
    tmp_path: Path,
    monkeypatch,
) -> None:
    outcomes = iter((True, None, False, False))
    monkeypatch.setattr(
        wsl_runtime_signals,
        "get_wsl_distro_root",
        lambda _distro: tmp_path,
    )
    monkeypatch.setattr(
        wsl_runtime_signals,
        "_safe_exists",
        lambda _path: next(outcomes),
    )

    result = scan_wsl_runtime_file_signals(
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)]
    )

    assert result[0].scanned is False
    assert result[0].container_runtimes == ("docker",)


def test_unreachable_and_stopped_distros_are_not_marked_scanned(monkeypatch) -> None:
    monkeypatch.setattr(
        wsl_runtime_signals,
        "get_wsl_distro_root",
        lambda _distro: None,
    )

    result = scan_wsl_runtime_file_signals(
        [
            DiscoveredWSLDistro(name="Running", wsl_version=2, is_running=True),
            DiscoveredWSLDistro(name="Stopped", wsl_version=2, is_running=False),
        ]
    )

    assert [distro.scanned for distro in result] == [False, False]
    assert [distro.container_runtimes for distro in result] == [(), ()]


def test_stopped_distro_does_not_probe_unc_root(
    tmp_path: Path,
    monkeypatch,
) -> None:
    calls: list[str] = []

    def fake_root(distro: str) -> Path:
        calls.append(distro)
        return tmp_path

    monkeypatch.setattr(
        wsl_runtime_signals,
        "get_wsl_distro_root",
        fake_root,
    )

    result = scan_wsl_runtime_file_signals(
        [DiscoveredWSLDistro(name="Stopped", wsl_version=2, is_running=False)]
    )

    assert result[0].scanned is False
    assert calls == []
