from pathlib import Path, PureWindowsPath

from runlayer_cli.scan.wsl_paths import parse_wsl_unc_path


def test_parses_wsl_localhost_path_with_spaces() -> None:
    parsed = parse_wsl_unc_path(
        r"\\wsl.localhost\Ubuntu 24.04\home\alice\work repo\.cursor\mcp.json"
    )

    assert parsed is not None
    assert parsed.distro == "Ubuntu 24.04"
    assert parsed.user == "alice"
    assert parsed.linux_path == "/home/alice/work repo/.cursor/mcp.json"


def test_parses_legacy_wsl_share_from_pure_windows_path() -> None:
    parsed = parse_wsl_unc_path(
        PureWindowsPath(r"\\wsl$\Debian\home\sam\.claude\skills\review")
    )

    assert parsed is not None
    assert parsed.distro == "Debian"
    assert parsed.user == "sam"
    assert parsed.linux_path == "/home/sam/.claude/skills/review"


def test_parses_path_object_using_windows_semantics_on_any_host() -> None:
    parsed = parse_wsl_unc_path(Path(r"\\wsl.localhost\Ubuntu\opt\runlayer"))

    assert parsed is not None
    assert parsed.user is None
    assert parsed.linux_path == "/opt/runlayer"


def test_attributes_root_home_to_root_user() -> None:
    parsed = parse_wsl_unc_path(r"\\wsl.localhost\Ubuntu\root\.local\bin\claude")

    assert parsed is not None
    assert parsed.user == "root"
    assert parsed.linux_path == "/root/.local/bin/claude"


def test_preserves_none_and_rejects_other_unc_shares() -> None:
    assert parse_wsl_unc_path(None) is None
    assert parse_wsl_unc_path(r"\\server\share\home\alice") is None
    assert parse_wsl_unc_path("/home/alice/project") is None
