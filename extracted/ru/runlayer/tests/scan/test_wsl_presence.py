import errno
import os
import stat
from pathlib import Path
from types import SimpleNamespace
from unittest import mock

from runlayer_cli.scan import wsl_presence
from runlayer_cli.scan.clients import InstallProbe, MCPClientDefinition
from runlayer_cli.scan.completeness import ScanCompletionStatus
from runlayer_cli.scan.device import DiscoveredWSLDistro
from runlayer_cli.scan.wsl_limits import MAX_WSL_HOMES
from runlayer_cli.scan.wsl_presence import scan_wsl_cli_binaries


def _client(name: str, binary: str) -> MCPClientDefinition:
    return MCPClientDefinition(
        name=name,
        display_name=name,
        paths=[],
        install_probe=InstallProbe(cli_binaries=[binary]),
    )


def test_file_predicate_uses_regular_file_stat() -> None:
    path = mock.MagicMock(spec=Path)
    path.stat.return_value = SimpleNamespace(st_mode=stat.S_IFREG)
    path.is_file.side_effect = AssertionError("Path.is_file must not be called")

    assert wsl_presence._safe_is_file(path) is True
    path.is_file.assert_not_called()


def test_file_predicate_definite_absence_remains_complete() -> None:
    for error_number in (errno.ENOENT, errno.ENOTDIR, errno.EBADF, errno.ELOOP):
        path = mock.MagicMock(spec=Path)
        path.stat.side_effect = OSError(error_number, "absent")
        status = ScanCompletionStatus()

        assert wsl_presence._safe_is_file(path, status) is False
        assert status.complete is True


def test_scans_user_root_and_system_bin_roots(
    tmp_path: Path,
    monkeypatch,
) -> None:
    distro_root = tmp_path / "Ubuntu"
    alice_home = distro_root / "home" / "alice"
    root_home = distro_root / "root"
    paths = (
        alice_home / ".local" / "bin" / "claude",
        root_home / ".local" / "bin" / "codex",
        distro_root / "usr" / "local" / "bin" / "ollama",
    )
    for path in paths:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("binary")

    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_distro_root",
        lambda _distro: distro_root,
    )
    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_user_homes",
        lambda _distro: [alice_home, root_home],
    )

    findings = scan_wsl_cli_binaries(
        [
            _client("claude_code", "claude"),
            _client("codex", "codex"),
            _client("ollama", "ollama"),
        ],
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)],
    )

    assert {(finding.client, finding.context.user) for finding in findings} == {
        ("claude_code", "alice"),
        ("codex", "root"),
        ("ollama", None),
    }
    assert {finding.path for finding in findings} == set(paths)


def test_skips_stopped_distros(monkeypatch) -> None:
    def unexpected_root(_distro: str) -> Path:
        raise AssertionError("stopped distro must not touch UNC")

    monkeypatch.setattr(wsl_presence, "get_wsl_distro_root", unexpected_root)

    findings = scan_wsl_cli_binaries(
        [_client("ollama", "ollama")],
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=False)],
    )

    assert findings == []


def test_uses_helper_bounded_homes_and_propagates_cap(
    tmp_path: Path,
    monkeypatch,
) -> None:
    distro_root = tmp_path / "Ubuntu"
    homes = [
        distro_root / "root",
        *(distro_root / "home" / f"user-{i}" for i in range(5)),
    ]
    for home in homes:
        binary = home / ".local" / "bin" / "claude"
        binary.parent.mkdir(parents=True)
        binary.write_text("binary")

    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_distro_root",
        lambda _distro: distro_root,
    )

    def get_wsl_user_homes(_distro, *, scan_status):
        scan_status.mark_incomplete("wsl_home_discovery_capped")
        return homes[:MAX_WSL_HOMES]

    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_user_homes",
        get_wsl_user_homes,
    )
    status = ScanCompletionStatus()

    findings = scan_wsl_cli_binaries(
        [_client("claude_code", "claude")],
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)],
        scan_status=status,
    )

    assert [finding.context.user for finding in findings] == [
        "root",
        "user-0",
        "user-1",
        "user-2",
    ]
    assert status.reasons == ["wsl_home_discovery_capped"]


def test_uses_single_time_budget_across_distros(monkeypatch) -> None:
    now = [0.0]
    checked_distros = []

    monkeypatch.setattr(wsl_presence.time, "monotonic", lambda: now[0])
    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_distro_root",
        lambda distro: Path("/") / distro,
    )
    monkeypatch.setattr(wsl_presence, "get_wsl_user_homes", lambda _distro: [])

    def check_candidate(path: Path, *_args) -> bool:
        checked_distros.append(path.parts[1])
        now[0] += 2.0
        return False

    monkeypatch.setattr(wsl_presence, "_safe_is_file", check_candidate)

    scan_wsl_cli_binaries(
        [_client("claude_code", "claude")],
        [
            DiscoveredWSLDistro(
                name=f"Distro-{index}",
                wsl_version=2,
                is_running=True,
            )
            for index in range(4)
        ],
    )

    assert set(checked_distros) == {"Distro-0", "Distro-1", "Distro-2"}


def test_binary_scan_ignores_expired_deadline_after_last_runnable_distro(
    monkeypatch,
) -> None:
    clock = 0.0
    roots: list[str] = []
    status = ScanCompletionStatus()

    def get_root(distro: str) -> Path:
        roots.append(distro)
        return Path("/") / distro

    def check_candidate(_path: Path, *_args) -> bool:
        nonlocal clock
        clock = 1.0
        return True

    monkeypatch.setattr(wsl_presence.time, "monotonic", lambda: clock)
    monkeypatch.setattr(wsl_presence, "WSL_PRESENCE_TIME_BUDGET_S", 1.0)
    monkeypatch.setattr(wsl_presence, "_SYSTEM_BIN_ROOTS", ())
    monkeypatch.setattr(wsl_presence, "get_wsl_distro_root", get_root)
    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_user_homes",
        lambda _distro, **_kwargs: [],
    )
    monkeypatch.setattr(wsl_presence, "_safe_is_file", check_candidate)

    findings = scan_wsl_cli_binaries(
        [_client("claude_code", "claude")],
        [
            DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True),
            DiscoveredWSLDistro(name="Debian", wsl_version=2, is_running=False),
            DiscoveredWSLDistro(
                name="docker-desktop",
                wsl_version=2,
                is_running=True,
            ),
        ],
        scan_status=status,
    )

    assert [finding.context.distro for finding in findings] == ["Ubuntu"]
    assert roots == ["Ubuntu"]
    assert status.reasons == []


def test_binary_scan_marks_expired_deadline_before_next_runnable_distro(
    monkeypatch,
) -> None:
    clock = 0.0
    roots: list[str] = []
    status = ScanCompletionStatus()

    def get_root(distro: str) -> Path:
        roots.append(distro)
        return Path("/") / distro

    def check_candidate(_path: Path, *_args) -> bool:
        nonlocal clock
        clock = 1.0
        return True

    monkeypatch.setattr(wsl_presence.time, "monotonic", lambda: clock)
    monkeypatch.setattr(wsl_presence, "WSL_PRESENCE_TIME_BUDGET_S", 1.0)
    monkeypatch.setattr(wsl_presence, "_SYSTEM_BIN_ROOTS", ())
    monkeypatch.setattr(wsl_presence, "get_wsl_distro_root", get_root)
    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_user_homes",
        lambda _distro, **_kwargs: [],
    )
    monkeypatch.setattr(wsl_presence, "_safe_is_file", check_candidate)

    findings = scan_wsl_cli_binaries(
        [_client("claude_code", "claude")],
        [
            DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True),
            DiscoveredWSLDistro(name="Debian", wsl_version=2, is_running=False),
            DiscoveredWSLDistro(
                name="docker-desktop",
                wsl_version=2,
                is_running=True,
            ),
            DiscoveredWSLDistro(name="Fedora", wsl_version=2, is_running=True),
        ],
        scan_status=status,
    )

    assert [finding.context.distro for finding in findings] == ["Ubuntu"]
    assert roots == ["Ubuntu"]
    assert status.reasons == ["wsl_binary_scan_timed_out"]


def test_binary_distro_cap_ignores_skippable_rows(monkeypatch) -> None:
    monkeypatch.setattr(wsl_presence, "MAX_WSL_DISTROS", 1)
    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_distro_root",
        lambda distro: Path("/") / distro,
    )
    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_user_homes",
        lambda _distro, **_kwargs: [],
    )
    status = ScanCompletionStatus()

    findings = scan_wsl_cli_binaries(
        [_client("claude_code", "claude")],
        [
            DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True),
            DiscoveredWSLDistro(name="Stopped", wsl_version=2, is_running=False),
            DiscoveredWSLDistro(
                name="docker-desktop",
                wsl_version=2,
                is_running=True,
            ),
        ],
        scan_status=status,
    )

    assert findings == []
    assert status.reasons == []


def test_candidate_cap_marks_wsl_presence_incomplete(monkeypatch) -> None:
    monkeypatch.setattr(wsl_presence, "MAX_WSL_BINARY_CANDIDATES_PER_DISTRO", 1)
    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_distro_root",
        lambda _distro: Path("/Ubuntu"),
    )
    monkeypatch.setattr(wsl_presence, "get_wsl_user_homes", lambda _distro, **_: [])
    monkeypatch.setattr(wsl_presence, "_safe_is_file", lambda *_args: False)
    status = ScanCompletionStatus()

    scan_wsl_cli_binaries(
        [_client("claude_code", "claude")],
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)],
        scan_status=status,
    )

    assert status.reasons == ["wsl_binary_candidate_capped"]


def test_binary_access_error_marks_wsl_presence_incomplete(
    monkeypatch,
) -> None:
    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_distro_root",
        lambda _distro: Path("/Ubuntu"),
    )
    monkeypatch.setattr(wsl_presence, "get_wsl_user_homes", lambda _distro, **_: [])
    monkeypatch.setattr(
        Path,
        "stat",
        lambda _path: (_ for _ in ()).throw(PermissionError(errno.EACCES, "denied")),
    )
    status = ScanCompletionStatus()

    scan_wsl_cli_binaries(
        [_client("claude_code", "claude")],
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)],
        scan_status=status,
    )

    assert "wsl_binary_access_failed" in status.reasons


def test_wsl_presence_caps_nvm_version_listing(
    tmp_path: Path,
    monkeypatch,
) -> None:
    distro_root = tmp_path / "Ubuntu"
    home = distro_root / "home" / "alice"
    versions = home / ".nvm" / "versions" / "node"
    for index in range(128):
        binary = versions / f"v{index}" / "bin" / "claude"
        binary.parent.mkdir(parents=True)
        binary.write_text("binary")

    listed = 0
    real_scandir = os.scandir

    class CountingScandir:
        def __init__(self, path: Path | str) -> None:
            self._path = Path(path)
            self._iterator = real_scandir(path)

        def __enter__(self):
            self._iterator.__enter__()
            return self

        def __exit__(self, *exc):
            return self._iterator.__exit__(*exc)

        def __iter__(self):
            for entry in self._iterator:
                if self._path == versions:
                    nonlocal listed
                    listed += 1
                yield entry

    monkeypatch.setattr("runlayer_cli.scan.cli_binaries.os.scandir", CountingScandir)
    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_distro_root",
        lambda _distro: distro_root,
    )
    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_user_homes",
        lambda _distro: [home],
    )

    findings = scan_wsl_cli_binaries(
        [_client("claude_code", "claude")],
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)],
    )

    assert listed == 64
    assert len(findings) == 64
