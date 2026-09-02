import os
from pathlib import Path

from runlayer_cli.scan import wsl_presence
from runlayer_cli.scan.clients import InstallProbe, MCPClientDefinition
from runlayer_cli.scan.device import DiscoveredWSLDistro
from runlayer_cli.scan.wsl_presence import scan_wsl_cli_binaries


def _client(name: str, binary: str) -> MCPClientDefinition:
    return MCPClientDefinition(
        name=name,
        display_name=name,
        paths=[],
        install_probe=InstallProbe(cli_binaries=[binary]),
    )


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


def test_caps_user_homes_per_distro_and_keeps_root_first(
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
    monkeypatch.setattr(
        wsl_presence,
        "get_wsl_user_homes",
        lambda _distro: homes,
    )

    findings = scan_wsl_cli_binaries(
        [_client("claude_code", "claude")],
        [DiscoveredWSLDistro(name="Ubuntu", wsl_version=2, is_running=True)],
    )

    assert [finding.context.user for finding in findings] == [
        "root",
        "user-0",
        "user-1",
        "user-2",
    ]


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

    def check_candidate(path: Path) -> bool:
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
