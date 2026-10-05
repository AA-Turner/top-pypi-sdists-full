"""Kimi Code's plugin install: Probe writes Kimi's own plugin list, the way
Kimi's `/plugins install <path>` does (recorded from Kimi Code 2.1.1)."""

from __future__ import annotations

import json
import os
import stat
from pathlib import Path

import pytest

from probe.cli import kimi_config, plugin_cli

AGENT = Path(__file__).resolve().parents[1]


@pytest.fixture()
def kimi(tmp_path, monkeypatch):
    """A Kimi home in scratch, a stub `kimi` on PATH, plugins from this checkout."""
    home = tmp_path / "kimi"
    bin_dir = tmp_path / "bin"
    bin_dir.mkdir()
    stub = bin_dir / "kimi"
    stub.write_text("#!/bin/sh\necho 2.1.1\n")
    stub.chmod(stub.stat().st_mode | stat.S_IEXEC)
    monkeypatch.setenv("PATH", f"{bin_dir}:/usr/bin:/bin")
    monkeypatch.setenv("KIMI_CODE_HOME", str(home))
    monkeypatch.setenv("HOME", str(tmp_path / "home"))
    monkeypatch.setenv(kimi_config.SOURCE_ENV, str(AGENT))
    return home


def _installed(home: Path) -> dict:
    return json.loads((home / "plugins" / "installed.json").read_text())


def test_install_writes_the_record_kimis_own_install_writes(kimi):
    result = plugin_cli.install("kimi_code", "probe-research@research-os-agent")
    assert result.ok, result.detail
    doc = _installed(kimi)
    assert doc["version"] == 1
    (record,) = doc["plugins"]
    assert set(record) == {"id", "root", "source", "enabled", "installedAt", "updatedAt", "originalSource"}
    assert record["id"] == "probe-research"
    assert record["source"] == "local-path"
    assert record["enabled"] is True
    version = json.loads((AGENT / "plugins/probe-research/.kimi-plugin/plugin.json").read_text())["version"]
    # A folder per version: an update never swaps files under a running session.
    assert record["root"] == str(kimi / "plugins" / "managed" / f"probe-research@{version}")
    manifest = Path(record["root"]) / ".kimi-plugin" / "plugin.json"
    assert json.loads(manifest.read_text())["name"] == "probe-research"
    # The hooks it ships are executable where they must be.
    assert (Path(record["root"]) / "hooks" / "session-start.sh").stat().st_mode & stat.S_IEXEC


def test_reinstall_keeps_installed_at_and_one_record(kimi):
    assert plugin_cli.install("kimi_code", "probe-research").ok
    first = _installed(kimi)["plugins"][0]["installedAt"]
    assert plugin_cli.install("kimi_code", "probe-research").ok
    (record,) = _installed(kimi)["plugins"]
    assert record["installedAt"] == first


def test_other_plugins_are_left_alone(kimi):
    path = kimi / "plugins" / "installed.json"
    path.parent.mkdir(parents=True)
    theirs = {"id": "someone-else", "root": "/x", "source": "github", "enabled": True}
    path.write_text(json.dumps({"version": 1, "plugins": [theirs]}))
    assert plugin_cli.install("kimi_code", "probe-research-daemon").ok
    assert plugin_cli.uninstall("kimi_code", "probe-research-daemon").ok
    assert _installed(kimi)["plugins"] == [theirs]
    assert not (kimi / "plugins" / "managed" / "probe-research-daemon").exists()


def test_an_unknown_plugin_list_layout_is_never_touched(kimi):
    """Kimi ships about daily: a layout this Probe does not know is refused,
    with the manual step, and the file is byte-identical afterwards."""
    path = kimi / "plugins" / "installed.json"
    path.parent.mkdir(parents=True)
    path.write_text('{"version": 2, "entries": []}')
    result = plugin_cli.install("kimi_code", "probe-research")
    assert not result.ok
    assert "/plugins install" in result.detail
    assert path.read_text() == '{"version": 2, "entries": []}'


def test_list_names_what_is_installed_and_enabled(kimi):
    assert plugin_cli.install("kimi_code", "probe-research").ok
    lines = plugin_cli.list_plugins("kimi_code").detail.splitlines()
    assert len(lines) == 1 and lines[0].startswith("probe-research ") and lines[0].endswith(" enabled")


def test_the_daemon_profile_swaps_the_plugins_like_on_claude_code(kimi):
    """`apply_recorder`'s second-plugin swap is install + uninstall, the same
    calls as Claude Code's; for Kimi they edit the plugin list."""
    from probe.cli import setup
    from probe.cli.capabilities import installed_plugins

    assert setup.install_plugin("probe-research", source="kimi_code").ok
    assert setup.install_plugin("probe-research-daemon", source="kimi_code").ok
    assert setup.uninstall_plugin("probe-research", source="kimi_code").ok
    state = installed_plugins(source="kimi_code")
    assert state.verified
    assert state.names == frozenset({"probe-research-daemon"})


def test_no_kimi_binary_is_unreachable_not_a_failure(kimi, monkeypatch):
    monkeypatch.setenv("PATH", "/usr/bin:/bin")
    result = plugin_cli.install("kimi_code", "probe-research")
    assert not result.ok and not result.reachable


def test_a_kimi_below_the_floor_is_named(kimi, tmp_path):
    (tmp_path / "bin" / "kimi").write_text("#!/bin/sh\necho 2.0.3\n")
    assert "older than 2.1.1" in (kimi_config.version_floor_problem() or "")


def _mirror_tarball(*, evil: bool = False) -> bytes:
    import io
    import tarfile

    buf = io.BytesIO()
    with tarfile.open(fileobj=buf, mode="w:gz") as archive:
        archive.add(AGENT / "plugins" / "probe-research", arcname="research-os-agent-main/plugins/probe-research")
        if evil:
            data = b"pwned"
            info = tarfile.TarInfo("research-os-agent-main/plugins/../../evil.txt")
            info.size = len(data)
            archive.addfile(info, io.BytesIO(data))
    return buf.getvalue()


def test_a_machine_without_a_checkout_installs_from_the_mirror(kimi, monkeypatch, tmp_path):
    """No checkout and no override: the plugin comes from the mirror's tarball."""
    import io

    monkeypatch.delenv(kimi_config.SOURCE_ENV)
    monkeypatch.setattr(kimi_config, "_checkout_source", lambda: None)
    monkeypatch.setattr(kimi_config, "_DOWNLOADED", None)
    calls = []

    def fake_urlopen(url, timeout, context):
        calls.append((url, context))
        return io.BytesIO(_mirror_tarball())

    monkeypatch.setattr(kimi_config.urllib.request, "urlopen", fake_urlopen)
    result = plugin_cli.install("kimi_code", "probe-research")
    assert result.ok, result.detail
    assert calls and calls[0][0] == kimi_config.MIRROR_TARBALL and calls[0][1] is not None
    (record,) = _installed(kimi)["plugins"]
    assert record["originalSource"] == f"https://github.com/{kimi_config.MIRROR_REPO}"


@pytest.mark.parametrize("member", [
    "research-os-agent-main/plugins/../../../evil.txt",
    "/plugins/evil.txt",
])
def test_an_escaping_archive_member_fails_the_install_and_lands_nowhere(kimi, monkeypatch, tmp_path, member):
    import io
    import tarfile

    scratch = tmp_path / "scratch"
    scratch.mkdir()
    monkeypatch.delenv(kimi_config.SOURCE_ENV)
    monkeypatch.setattr(kimi_config, "_checkout_source", lambda: None)
    monkeypatch.setattr(kimi_config, "_DOWNLOADED", None)
    monkeypatch.setattr(kimi_config.tempfile, "mkdtemp", lambda prefix="": str(scratch / "dl"))
    (scratch / "dl").mkdir()

    def archive():
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tar:
            tar.add(AGENT / "plugins" / "probe-research", arcname="research-os-agent-main/plugins/probe-research")
            info = tarfile.TarInfo(member)
            info.size = 5
            tar.addfile(info, io.BytesIO(b"pwned"))
        return io.BytesIO(buf.getvalue())

    monkeypatch.setattr(kimi_config.urllib.request, "urlopen", lambda url, timeout, context: archive())
    result = plugin_cli.install("kimi_code", "probe-research")
    assert not result.ok and "refusing archive member" in result.detail
    assert not any(p.name == "evil.txt" for p in tmp_path.rglob("evil.txt"))
    assert not (scratch / "dl").exists(), "a failed download leaves no scratch behind"


def test_a_truncated_download_is_a_failed_install_not_a_crash(kimi, monkeypatch):
    import io

    monkeypatch.delenv(kimi_config.SOURCE_ENV)
    monkeypatch.setattr(kimi_config, "_checkout_source", lambda: None)
    monkeypatch.setattr(kimi_config, "_DOWNLOADED", None)
    data = _mirror_tarball()
    monkeypatch.setattr(kimi_config.urllib.request, "urlopen",
                        lambda url, timeout, context: io.BytesIO(data[: len(data) // 2]))
    result = plugin_cli.install("kimi_code", "probe-research")
    assert not result.ok and "download failed" in result.detail


def test_a_reinstall_keeps_fields_kimi_wrote_and_entries_it_does_not_understand(kimi):
    path = kimi / "plugins" / "installed.json"
    path.parent.mkdir(parents=True)
    path.write_text(json.dumps({"version": 1, "plugins": [
        "a-string-entry",
        {"id": "probe-research", "root": "/old", "source": "local-path", "enabled": True,
         "installedAt": "2026-01-01T00:00:00.000Z", "trusted": True},
    ]}))
    assert plugin_cli.install("kimi_code", "probe-research").ok
    doc = _installed(kimi)
    assert "a-string-entry" in doc["plugins"]
    (record,) = [p for p in doc["plugins"] if isinstance(p, dict)]
    assert record["trusted"] is True and record["installedAt"] == "2026-01-01T00:00:00.000Z"


def test_old_versions_are_pruned_but_the_previous_one_is_kept(kimi, monkeypatch, tmp_path):
    """An open session may still run the version before; older ones go."""
    import shutil

    src = tmp_path / "src"
    shutil.copytree(AGENT / "plugins" / "probe-research", src / "plugins" / "probe-research")
    monkeypatch.setenv(kimi_config.SOURCE_ENV, str(src))
    manifest = src / "plugins" / "probe-research" / ".kimi-plugin" / "plugin.json"
    for version in ("9.0.0", "9.0.1", "9.0.2"):
        data = json.loads(manifest.read_text())
        data["version"] = version
        manifest.write_text(json.dumps(data))
        assert plugin_cli.install("kimi_code", "probe-research").ok
    managed = kimi / "plugins" / "managed"
    # Within a week every version stays (a long session may still run one).
    assert sorted(p.name for p in managed.glob("probe-research@*")) == [
        "probe-research@9.0.0", "probe-research@9.0.1", "probe-research@9.0.2"]
    old = managed / "probe-research@9.0.0"
    os.utime(old, (0, 0))
    data = json.loads(manifest.read_text())
    data["version"] = "9.0.3"
    manifest.write_text(json.dumps(data))
    os.utime(managed / "probe-research@9.0.1", (0, 0))
    assert plugin_cli.install("kimi_code", "probe-research").ok
    kept = sorted(p.name for p in managed.glob("probe-research@*"))
    # Older than a week and not the previous version: gone. 9.0.2 (previous) stays.
    assert kept == ["probe-research@9.0.2", "probe-research@9.0.3"]
    assert _installed(kimi)["plugins"][0]["root"].endswith("probe-research@9.0.3")


def test_a_kimi_below_the_floor_is_not_installed_into(kimi, tmp_path):
    (tmp_path / "bin" / "kimi").write_text("#!/bin/sh\necho 2.0.3\n")
    result = plugin_cli.install("kimi_code", "probe-research")
    assert not result.ok and "older than 2.1.1" in result.detail
    assert not (kimi / "plugins" / "installed.json").exists()


def test_the_import_lane_finds_kimi_main_sessions_only(tmp_path, monkeypatch):
    """History import walks Kimi's own root for main wires (never Codex's
    folder, never a helper agent's wire) and reads the session's folder."""
    import shutil

    from probe.cli import backfill_transcripts as bt

    shutil.copytree(Path(__file__).parent / "fixtures" / "kimi_code" / "sessions", tmp_path / "kimi" / "sessions")
    monkeypatch.setenv("KIMI_CODE_HOME", str(tmp_path / "kimi"))
    monkeypatch.delenv("PROBE_KIMI_SESSIONS_DIR", raising=False)
    files = [p for root in bt.transcript_roots("kimi_code") for p in bt._walk(root, "kimi_code")]
    assert len(files) == 4 and all(p.parent.name == "main" for p in files)
    ids = {bt.session_id_for(p, "kimi_code") for p in files}
    assert "e240efe5-da6a-4407-9c61-91d8a3a53d24" in ids and all(len(i) == 36 for i in ids)
    assert bt.read_cwd(files[0], "kimi_code") == "/home/researcher/kimi-fixture/proj"
