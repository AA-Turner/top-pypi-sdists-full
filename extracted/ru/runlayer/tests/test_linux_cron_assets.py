"""Static checks for the shipped Linux AI Watch packaging assets.

The Linux product mode is Detect-only: a root cron job
(``/etc/cron.d/runlayer-aiwatch``) runs ``run-aiwatch-scan.sh`` every 15
minutes, which fans out over ALL passwd users via privilege drop (``runuser``)
— the Linux analog of the Windows ``aiwatch scan --all-users`` orchestrator
(``runlayer_cli/scan/windows_users.py``) and the macOS LaunchAgent. The same
cron asset runs the root update wrapper hourly; Detect remains the only Linux
AI Watch product mode.

Pinned invariants:

* the cron.d destination basename is dot-free (run-parts skips dotted names);
* the unconfigured-fleet gate (empty ``RUNLAYER_API_KEY`` -> silent exit 0)
  fires BEFORE any scan invocation, matching the Windows ``OrgApiKey`` gate in
  ``tests/test_windows_ps1_gates.py``;
* the fan-out enumerates ALL users — no uid or login-shell filtering (root,
  system, and service accounts are scanned by explicit product requirement);
* the config template carries only Host and no credentials — the API key lives
  only in the root-only credentials file;
* the update wrapper delegates managed ``AutoUpdate`` policy to the binary;
* no asset enables hooks or device onboarding flows.
"""

from __future__ import annotations

import json
import os
import shlex
import subprocess
import time
from pathlib import Path

import pytest
import yaml

from runlayer_cli import regex_safe

_PACKAGING_LINUX = Path(__file__).parent.parent / "packaging" / "linux"

_CRON_ASSET = _PACKAGING_LINUX / "cron.d-runlayer-aiwatch"
_WRAPPER = _PACKAGING_LINUX / "run-aiwatch-scan.sh"
_UPDATE_WRAPPER = _PACKAGING_LINUX / "run-aiwatch-update.sh"
_CONFIG_TEMPLATE = _PACKAGING_LINUX / "aiwatch-config.json"
_CREDENTIALS_EXAMPLE = _PACKAGING_LINUX / "aiwatch-credentials.example"
_NFPM_CONFIG = _PACKAGING_LINUX / "nfpm-aiwatch.yaml"
_BUILD_SCRIPT = _PACKAGING_LINUX / "build_aiwatch_packages.sh"

_VERSION_JSON_DST = "/etc/runlayer/aiwatch/version.json"
_UPDATE_WRAPPER_DST = "/usr/lib/runlayer/run-aiwatch-update.sh"
_CREDENTIALS_DST = "/etc/runlayer/aiwatch/credentials"

_ALL_ASSETS: tuple[Path, ...] = (
    _CRON_ASSET,
    _WRAPPER,
    _UPDATE_WRAPPER,
    _CONFIG_TEMPLATE,
    _CREDENTIALS_EXAMPLE,
)

# The source filename carries a "cron.d-" prefix (dots are fine in the repo);
# the DESTINATION basename under /etc/cron.d/ is what run-parts naming rules
# constrain.
_CRON_DEST_BASENAME = _CRON_ASSET.name.removeprefix("cron.d-")


def test_cron_destination_basename_is_run_parts_safe() -> None:
    """cron/run-parts skip files whose names contain dots (or other characters
    outside [A-Za-z0-9_-]); a dotted destination name would silently disable
    the scan fleet-wide."""
    assert _CRON_DEST_BASENAME == "runlayer-aiwatch"
    assert regex_safe.fullmatch(r"[A-Za-z0-9_-]+", _CRON_DEST_BASENAME), (
        f"/etc/cron.d/{_CRON_DEST_BASENAME} would be ignored by cron naming rules"
    )


def test_cron_entry_runs_wrapper_every_15_minutes_as_root() -> None:
    """15-minute cadence = parity with the macOS LaunchAgent StartInterval=900
    and the Windows AIWatchScan scheduled task."""
    text = _CRON_ASSET.read_text()

    assert "*/15 * * * * root /usr/lib/runlayer/run-aiwatch-scan.sh" in text


def test_cron_entry_runs_update_wrapper_hourly_as_root() -> None:
    """The package-owned root scheduler checks the backend-selected target
    hourly, offset from quarter-hour scans so the shared lock cannot starve
    every update tick."""
    text = _CRON_ASSET.read_text()

    assert "7 * * * * root /usr/lib/runlayer/run-aiwatch-update.sh" in text


def test_cron_entry_pins_shell_and_path() -> None:
    """cron.d files inherit a minimal environment; SHELL and PATH must be
    explicit so the wrapper resolves flock/runuser/getent deterministically."""
    lines = _CRON_ASSET.read_text().splitlines()

    assert any(line.startswith("SHELL=") for line in lines)
    assert any(line.startswith("PATH=") for line in lines)


def test_wrapper_is_posix_sh() -> None:
    """/bin/sh is dash on Debian — the shebang pins POSIX sh, no bashisms."""
    assert _WRAPPER.read_text().startswith("#!/bin/sh")


def test_update_wrapper_invokes_packaged_binary_directly() -> None:
    """Cron already runs as root, so the wrapper executes the package-owned
    binary without sudo, runuser, or a PATH lookup."""
    text = _UPDATE_WRAPPER.read_text()

    assert text.startswith("#!/bin/sh")
    assert "/usr/lib/runlayer/aiwatch/aiwatch self-update" in text
    assert "sudo" not in text
    assert "runuser" not in text


def test_update_wrapper_sources_root_credentials_before_invocation() -> None:
    """The root scheduler hands credentials to ``aiwatch self-update`` from
    the existing 0600 file and quietly skips an unconfigured device."""
    text = _UPDATE_WRAPPER.read_text()
    source_marker = '. "$CREDENTIALS_FILE"'
    key_gate_marker = '[ -z "${RUNLAYER_API_KEY:-}" ]'
    update_marker = "/usr/lib/runlayer/aiwatch/aiwatch self-update"

    assert "CREDENTIALS_FILE=/etc/runlayer/aiwatch/credentials" in text
    assert source_marker in text
    assert key_gate_marker in text
    assert "export RUNLAYER_API_KEY" in text
    assert "export RUNLAYER_HOST" in text
    assert (
        text.find(source_marker) < text.find(key_gate_marker) < text.find(update_marker)
    )


def test_scan_and_update_wrappers_serialize_package_access_without_starvation() -> None:
    """A package upgrade must never mutate the PyInstaller onedir tree while
    scan children execute. Scans skip on the shared package lock; the updater
    deduplicates itself, then waits for that shared lock so a long scan cannot
    deterministically starve every hourly update attempt."""
    scan_text = _WRAPPER.read_text()
    update_text = _UPDATE_WRAPPER.read_text()

    assert 'exec 9>"$LOCK_DIR/package.lock"' in scan_text
    assert "flock -n 9 || exit $EX_TEMPFAIL" in scan_text
    assert scan_text.find("flock -n") < scan_text.find("CREDENTIALS_FILE=")

    assert 'exec 9>"$LOCK_DIR/update.lock"' in update_text
    assert "flock -n 9 || exit $EX_TEMPFAIL" in update_text
    assert 'exec 8>"$LOCK_DIR/package.lock"' in update_text
    assert "flock 8 || exit 1" in update_text
    assert "flock -w" not in update_text
    assert (
        update_text.find("flock -n")
        < update_text.find("flock 8")
        < update_text.find("CREDENTIALS_FILE=")
    )


def test_wrapper_lock_skip_exits_tempfail_not_success() -> None:
    """`aiwatch config sync` / `update-now` invoke these wrappers directly and
    report "started" on exit 0. A lock-contention skip ran nothing, so it must
    exit EX_TEMPFAIL (75) — the code `_kick_unit` maps to an honest skip
    message — never 0."""
    for path in (_WRAPPER, _UPDATE_WRAPPER):
        text = path.read_text()
        assert "EX_TEMPFAIL=75" in text
        assert text.find("EX_TEMPFAIL=75") < text.find("flock -n")


@pytest.mark.skipif(os.name == "nt", reason="Linux wrapper requires a POSIX shell")
def test_update_waits_until_long_scan_releases_package_lock(tmp_path: Path) -> None:
    """An hourly updater already queued behind a scan must eventually run."""
    lock_dir = tmp_path / "locks"
    credentials = tmp_path / "credentials"
    credentials.write_text("RUNLAYER_API_KEY=stub\n")
    update_marker = tmp_path / "updated"

    wrapper = tmp_path / "run-aiwatch-update.sh"
    wrapper.write_text(
        _UPDATE_WRAPPER.read_text()
        .replace(
            "LOCK_DIR=/run/runlayer-aiwatch",
            f"LOCK_DIR={shlex.quote(str(lock_dir))}",
        )
        .replace(
            "CREDENTIALS_FILE=/etc/runlayer/aiwatch/credentials",
            f"CREDENTIALS_FILE={shlex.quote(str(credentials))}",
        )
        .replace(
            "/usr/lib/runlayer/aiwatch/aiwatch self-update",
            f"touch {shlex.quote(str(update_marker))}",
        )
    )
    wrapper.chmod(0o755)

    fake_bin = tmp_path / "bin"
    fake_bin.mkdir()
    fake_flock = fake_bin / "flock"
    fake_flock.write_text(
        """#!/bin/sh
case "${1:-}" in
-n) exit 0 ;;
-w)
    sleep "$TEST_FLOCK_TIMEOUT"
    [ ! -e "$TEST_PACKAGE_LOCK" ]
    ;;
*)
    while [ -e "$TEST_PACKAGE_LOCK" ]; do sleep 0.01; done
    ;;
esac
"""
    )
    fake_flock.chmod(0o755)

    held_package_lock = tmp_path / "package-lock-held"
    held_package_lock.touch()
    env = {
        **os.environ,
        "PATH": f"{fake_bin}{os.pathsep}{os.environ['PATH']}",
        "TEST_FLOCK_TIMEOUT": "0.1",
        "TEST_PACKAGE_LOCK": str(held_package_lock),
    }
    update = subprocess.Popen(
        [str(wrapper)],
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        time.sleep(1)
        assert update.poll() is None, (
            "updater abandoned its attempt while the scan lock was still held"
        )
    finally:
        held_package_lock.unlink(missing_ok=True)

    stdout, stderr = update.communicate(timeout=2)
    assert update.returncode == 0, (stdout, stderr)
    assert update_marker.exists()


def test_lock_files_are_unavailable_to_standard_user_dos() -> None:
    """A world-readable lock file lets any user hold an exclusive flock and
    suppress scans/updates. Both root wrappers must create locks only inside a
    root-only runtime directory and repair permissions before locking."""
    for path in (_WRAPPER, _UPDATE_WRAPPER):
        text = path.read_text()
        assert "umask 077" in text
        assert "LOCK_DIR=/run/runlayer-aiwatch" in text
        assert 'mkdir -p "$LOCK_DIR"' in text
        assert 'chmod 0700 "$LOCK_DIR"' in text
        assert text.find("umask 077") < text.find('mkdir -p "$LOCK_DIR"')
        assert text.find('chmod 0700 "$LOCK_DIR"') < text.find("\nflock ")
        assert "/run/runlayer-aiwatch.lock" not in text

    assert 'chmod 0600 "$LOCK_DIR/package.lock"' in _WRAPPER.read_text()
    update_text = _UPDATE_WRAPPER.read_text()
    assert 'chmod 0600 "$LOCK_DIR/update.lock"' in update_text
    assert 'chmod 0600 "$LOCK_DIR/package.lock"' in update_text


def test_update_wrapper_routes_output_and_failure_to_syslog() -> None:
    """Cron must never mail update output to root, while native-installer
    failures remain observable in the same product syslog stream as scans."""
    text = _UPDATE_WRAPPER.read_text()

    assert "2>&1" in text
    assert "logger -t runlayer-aiwatch" in text
    assert '"update failed (rc=$update_rc)"' in text
    assert "exit $update_rc" in text


def test_api_key_gate_precedes_scan_invocation() -> None:
    """Unconfigured-fleet gate: with no RUNLAYER_API_KEY the wrapper exits 0
    quietly BEFORE any scan child is spawned (parity with the Windows
    OrgApiKey gate and the macOS unconfigured-fleet gate)."""
    text = _WRAPPER.read_text()

    gate_marker = '[ -z "${RUNLAYER_API_KEY:-}" ]'
    scan_marker = "/usr/lib/runlayer/aiwatch/aiwatch scan"

    gate_index = text.find(gate_marker)
    scan_index = text.find(scan_marker)
    assert gate_index != -1, "missing RUNLAYER_API_KEY empty-gate"
    assert scan_index != -1, "missing aiwatch scan invocation"
    assert gate_index < scan_index, (
        "RUNLAYER_API_KEY gate must precede the first aiwatch scan invocation"
    )
    assert "exit 0" in text


def test_config_refresh_runs_after_gate_and_before_fanout() -> None:
    """Root refresh of the backend settings snapshot sits between the
    credentials gate and the per-user fan-out, so this run's scan children
    already see dashboard-managed settings. Best-effort: the wrapper never
    exits on refresh failure (no exit between refresh and the fan-out)."""
    text = _WRAPPER.read_text()

    gate_marker = '[ -z "${RUNLAYER_API_KEY:-}" ]'
    refresh_marker = "/usr/lib/runlayer/aiwatch/aiwatch config refresh"
    scan_marker = "/usr/lib/runlayer/aiwatch/aiwatch scan"

    gate_index = text.find(gate_marker)
    refresh_index = text.find(refresh_marker)
    scan_index = text.find(scan_marker)
    fanout_index = text.find("rc=0")
    assert refresh_index != -1, "missing aiwatch config refresh step"
    assert gate_index < refresh_index < fanout_index < scan_index
    refresh_block = text[refresh_index:fanout_index]
    assert "exit" not in refresh_block, (
        "refresh failure must never block the scan fan-out"
    )
    # Bounded like every other root step so a hung fetch can't hold the flock.
    assert "timeout -k 30 120" in text


def test_wrapper_drops_privileges_per_user_with_timeout() -> None:
    """Per-user scan children run with dropped privileges (runuser) under a
    bounded timeout, tagged with --username like the Windows orchestrator."""
    text = _WRAPPER.read_text()

    assert "runuser -u" in text
    assert "--username" in text
    # -k: guaranteed SIGKILL after the TERM grace so a wedged child can't
    # hold the flock past the budget.
    assert "timeout -k 30 600" in text


def test_wrapper_enumerates_all_users_without_filtering() -> None:
    """Explicit product requirement: scan ALL passwd entries — root, system,
    and service accounts included. No uid floor, no login-shell filter."""
    text = _WRAPPER.read_text()

    assert "getent passwd" in text
    assert "1000" not in text, "wrapper must not filter users by uid"
    assert "nologin" not in text, "wrapper must not filter users by login shell"
    assert "/bin/false" not in text, "wrapper must not filter users by login shell"


def test_config_template_contains_only_bootstrap_host() -> None:
    """Host carries the REPLACE_WITH sentinel filtered by
    mdm_config._is_placeholder; credentials and capability settings never live
    in this world-readable file."""
    data = json.loads(_CONFIG_TEMPLATE.read_text())

    assert set(data) == {"Host"}
    assert isinstance(data["Host"], str)
    assert data["Host"].startswith("REPLACE_WITH")


def test_auto_update_policy_is_resolved_only_by_aiwatch() -> None:
    """The root wrapper always delegates to the binary; managed
    ``AutoUpdate=false`` is evaluated by ``aiwatch self-update`` so the config
    parser has one cross-platform policy boundary."""
    text = _UPDATE_WRAPPER.read_text()

    assert "AutoUpdate" not in text
    assert "config.json" not in text
    assert "jq" not in text


def test_credentials_example_ships_no_live_values() -> None:
    """The shipped example is fully commented (no live values) and documents
    only the keys the wrapper sources: RUNLAYER_API_KEY, RUNLAYER_HOST."""
    allowed_keys = {"RUNLAYER_API_KEY", "RUNLAYER_HOST"}
    key_value_re = regex_safe.compile(r"^(RUNLAYER_API_KEY|RUNLAYER_HOST)=\S+$")

    live_lines: list[str] = []
    for lineno, raw in enumerate(_CREDENTIALS_EXAMPLE.read_text().splitlines(), 1):
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        match = key_value_re.match(line)
        assert match, (
            f"line {lineno} is not KEY=VALUE with KEY in {sorted(allowed_keys)}: "
            f"{line!r}"
        )
        live_lines.append(f"line {lineno}: {line}")

    assert not live_lines, (
        f"the shipped example must be fully commented — no live values: {live_lines}"
    )


def test_credentials_example_documents_expected_keys() -> None:
    text = _CREDENTIALS_EXAMPLE.read_text()

    assert "RUNLAYER_API_KEY" in text
    assert "RUNLAYER_HOST" in text


def _nfpm_content_by_dst() -> dict[str, dict]:
    """Map each nfpm ``contents`` entry by its install destination."""
    data = yaml.safe_load(_NFPM_CONFIG.read_text())
    return {entry["dst"]: entry for entry in data["contents"]}


def test_nfpm_ships_version_json_as_plain_content() -> None:
    """The MDM version-inventory record ships as PLAIN content (like cron.d), NOT
    a conffile. It embeds the version, so it must be replaced on upgrade and
    removed on uninstall; ``config|noreplace`` semantics (kept on uninstall)
    would strand a stale version. 0644 root:root so any inventory reader can read
    it (ENG-4161)."""
    entry = _nfpm_content_by_dst().get(_VERSION_JSON_DST)
    assert entry is not None, f"nfpm must ship {_VERSION_JSON_DST}"

    assert "type" not in entry, (
        "version.json must be plain content, not type: config|noreplace — a stale "
        "version would survive uninstall/upgrade"
    )
    assert entry["src"] == "./build/aiwatch-version.json", (
        "src must be the build-time-generated file (it embeds the version), not a "
        "static packaging/ asset"
    )
    file_info = entry["file_info"]
    assert file_info["mode"] == 0o644
    assert file_info["owner"] == "root"
    assert file_info["group"] == "root"


def test_nfpm_ships_root_owned_update_wrapper() -> None:
    """The cron target must be package-owned executable content, not a
    conffile that an upgrade or uninstall could preserve independently."""
    entry = _nfpm_content_by_dst().get(_UPDATE_WRAPPER_DST)
    assert entry is not None, f"nfpm must ship {_UPDATE_WRAPPER_DST}"

    assert "type" not in entry
    assert entry["src"] == "./packaging/linux/run-aiwatch-update.sh"
    assert entry["file_info"] == {
        "mode": 0o755,
        "owner": "root",
        "group": "root",
    }


def test_nfpm_keeps_sourced_credentials_root_only() -> None:
    """Both root wrappers source this file, so the package must never make it
    readable or writable by unprivileged users."""
    entry = _nfpm_content_by_dst()[_CREDENTIALS_DST]

    assert entry["type"] == "config|noreplace"
    assert entry["file_info"] == {
        "mode": 0o600,
        "owner": "root",
        "group": "root",
    }


def test_build_script_generates_version_json_before_nfpm() -> None:
    """build_aiwatch_packages.sh must generate build/aiwatch-version.json — the
    src nfpm ships — with the ``{"Version": "X.Y.Z"}`` shape from the pyproject
    ``$VERSION``, and it must be produced BEFORE nfpm packages it."""
    build_script = _BUILD_SCRIPT.read_text()

    assert '{"Version":"%s"}' in build_script, (
        'version record must carry the {"Version": "X.Y.Z"} shape'
    )
    gen_index = build_script.find('"$CLI_DIR/build/aiwatch-version.json"')
    nfpm_index = build_script.find("pkg --config")  # the actual nfpm invocation
    assert gen_index != -1, "build script must generate build/aiwatch-version.json"
    assert nfpm_index != -1, "build script must invoke nfpm (pkg --config ...)"
    assert gen_index < nfpm_index, (
        "version.json must be generated before nfpm reads ./build/aiwatch-version.json"
    )


@pytest.mark.parametrize("asset_path", _ALL_ASSETS, ids=lambda p: p.name)
def test_assets_do_not_enable_hooks(asset_path: Path) -> None:
    """Linux remains Detect-only: no asset may reference hook setup or device
    onboarding flows."""
    text = asset_path.read_text().lower()

    for forbidden in ("setup hooks", "bootstrap", "enroll"):
        assert forbidden not in text, (
            f"{asset_path.name} references {forbidden!r}; Linux must stay Detect-only"
        )
