"""The service's install of a closed desktop app, on a real Mac, with the real release (plan E1).

Opt-in: `PROBE_APP_INSTALL_REAL=1` on macOS, with `PROBE_APP_INSTALL_APP` naming
an OLDER released `Probe.app` installed in a scratch Applications folder and
`PROBE_APP_INSTALL_HOME` a scratch home (the app's instance lock lives there).
`agent-os-matrix.yml` (`run: app-install`) downloads the older release from
prbe-ai/desktop-releases and runs this on `macos-latest`.

The install is the service's own step (`appinstall.install_closed`) with its
pinned endpoint, key and team, against the real `latest.json`, the real
archive and its real minisign signature. A latest release without the update
helper (prbe-ai/desktop `probe-swap`, every release before it) must be skipped
as `no_helper` with the app untouched. One with it is installed by that helper:
then the swapped bundle must pass `codesign --verify --deep --strict -R` (the
Probe team) and `spctl` (notarized), carry the manifest's version, and its
binary must start and exit (the app's `--background-update` launch; the app has
no `--version`): it checks the same feed, finds itself current and exits 3. A
second install finds it current and downloads nothing.
"""

from __future__ import annotations

import json
import os
import plistlib
import shutil
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

import pytest

from probe.service import appinstall

pytestmark = pytest.mark.skipif(
    sys.platform != "darwin" or os.environ.get("PROBE_APP_INSTALL_REAL") != "1",
    reason="a real Mac and PROBE_APP_INSTALL_REAL=1 (agent-os-matrix.yml, run: app-install)",
)


def _version(app: Path) -> str:
    with open(app / "Contents" / "Info.plist", "rb") as handle:
        return plistlib.load(handle)["CFBundleShortVersionString"]


def _latest() -> str:
    request = urllib.request.Request(appinstall.ENDPOINTS[0], headers={"Accept": "application/json"})
    with urllib.request.urlopen(request, timeout=60) as response:  # noqa: S310 -- the pinned https endpoint
        return json.load(response)["version"]


@pytest.fixture
def installed() -> dict:
    app = Path(os.environ["PROBE_APP_INSTALL_APP"])
    home = Path(os.environ["PROBE_APP_INSTALL_HOME"])
    assert app.name == "Probe.app" and (app / "Contents" / "Info.plist").is_file()
    return {"app": app, "home": home}


def _latest_has_helper(tmp_path: Path) -> bool:
    """Does the latest release carry the update helper (`ProbeSwapHelper`)?
    Read from its real archive, verified like the install verifies it."""
    deadline = appinstall._Deadline(appinstall.TIME_LIMIT_S)  # noqa: SLF001
    version, entry = appinstall.check(deadline=deadline)
    archive = tmp_path / "latest.tar.gz"
    with open(archive, "wb") as sink:
        appinstall.fetch(entry["url"], accept="application/octet-stream", limit=appinstall.ARCHIVE_MAX_BYTES,
                         deadline=deadline, sink=sink)
    appinstall.verify_file(archive, appinstall.parse_signature(entry["signature"]),
                           appinstall.parse_public_key(appinstall.PUBKEY), version)
    root = tmp_path / "latest"
    root.mkdir()
    appinstall.extract(archive, root)
    return appinstall.helper_of(root) is not None


def test_the_service_installs_the_real_release_over_an_older_closed_app(installed, tmp_path):
    """With the helper in the latest release: installed by that helper, then
    verified from outside. Without it (every release before prbe-ai/desktop's
    probe-swap): skipped as no_helper, the app untouched, nothing left behind."""
    app = installed["app"]
    before = _version(app)
    latest = _latest()
    assert appinstall.newer(latest, before), f"the installed {before} must be older than the latest {latest}"
    has_helper = _latest_has_helper(tmp_path)
    inode = os.stat(app).st_ino
    log: list[str] = []
    result = appinstall.install_closed(app, home=installed["home"], log=log.append)
    print(json.dumps(result, indent=2), f"latest has the helper: {has_helper}", *log, sep="\n")
    assert appinstall.leftovers(app) == [] and not (app.parent / appinstall.HELPER_JOURNAL_NAME).exists()
    if not has_helper:
        assert result["outcome"] == appinstall.Outcome.NO_HELPER, result
        assert result["latest"] == latest
        assert _version(app) == before and os.stat(app).st_ino == inode, "the app is untouched"
        return
    assert result["outcome"] == appinstall.Outcome.INSTALLED, result
    assert (result["version_before"], result["version_after"]) == (before, latest)
    assert result["codesign"] == "verified"
    assert result["old_bundle"] == "removed"
    assert _version(app) == latest

    # The swapped bundle, verified again from outside: signed by the Probe team, notarized.
    signed = subprocess.run(["/usr/bin/codesign", "--verify", "--deep", "--strict", "--verbose=2", "-R",
                             appinstall.TEAM_REQUIREMENT, str(app)],
                            capture_output=True, text=True, timeout=120)
    print(signed.stdout, signed.stderr)
    assert signed.returncode == 0, signed.stderr
    gatekeeper = subprocess.run(["/usr/sbin/spctl", "-a", "-vv", str(app)], capture_output=True, text=True, timeout=120)
    print("spctl:", gatekeeper.returncode, gatekeeper.stdout, gatekeeper.stderr)
    assert gatekeeper.returncode == 0 and "source=Notarized Developer ID" in gatekeeper.stdout + gatekeeper.stderr

    # Its binary starts and exits: a background update finds itself current.
    home = tmp_path / "launch-home"
    home.mkdir()
    binary = app / "Contents" / "MacOS" / plistlib.loads((app / "Contents" / "Info.plist").read_bytes())[
        "CFBundleExecutable"]
    started = time.monotonic()
    ran = subprocess.run([str(binary), "--background-update"], env={"HOME": str(home), "PATH": "/usr/bin:/bin"},
                         capture_output=True, text=True, timeout=300)
    report_path = home / ".local" / "state" / "probe" / "service" / "app-update.json"
    report = json.loads(report_path.read_text()) if report_path.exists() else None
    print("background update:", ran.returncode, f"{time.monotonic() - started:.1f}s", report, ran.stderr[-2000:])
    assert ran.returncode == 3, (ran.returncode, report, ran.stderr[-2000:])
    assert report is not None and report["result"] == "current" and report["version_before"] == latest, report

    # The next cycle: current, nothing downloaded, nothing moved.
    inode = os.stat(app).st_ino
    again = appinstall.install_closed(app, home=installed["home"])
    assert again["outcome"] == appinstall.Outcome.CURRENT, again
    assert os.stat(app).st_ino == inode


def test_the_installed_releases_are_signed_by_the_pinned_team(installed):
    """The team the service requires (TEAM_ID) is the one that signs Probe:
    the older release installed here passes the requirement, and Gatekeeper
    accepts it as notarized."""
    app = installed["app"]
    signed = subprocess.run(["/usr/bin/codesign", "--verify", "--deep", "--strict", "-R", appinstall.TEAM_REQUIREMENT,
                             str(app)], capture_output=True, text=True, timeout=120)
    assert signed.returncode == 0, signed.stderr
    gatekeeper = subprocess.run(["/usr/sbin/spctl", "-a", "-vv", str(app)], capture_output=True, text=True, timeout=120)
    print("spctl:", gatekeeper.returncode, gatekeeper.stdout, gatekeeper.stderr)
    assert gatekeeper.returncode == 0 and f"({appinstall.TEAM_ID})" in gatekeeper.stdout + gatekeeper.stderr


def test_macos_sees_where_a_process_runs_from_even_after_its_bundle_moves(tmp_path):
    """`ps` names the path a process started from; `proc_pidpath` follows the
    bundle when it is renamed (the swap's check for an old copy)."""
    bundle = tmp_path / "Probe.app"
    (bundle / "Contents" / "MacOS").mkdir(parents=True)
    binary = bundle / "Contents" / "MacOS" / "desktop"
    shutil.copyfile("/bin/sleep", binary)  # not copy2: /bin/sleep's SIP flag cannot be copied
    binary.chmod(0o755)
    proc = subprocess.Popen([str(binary), "60"])
    try:
        time.sleep(0.5)
        assert proc.pid in appinstall.running_from(bundle)
        moved = tmp_path / f"{appinstall.STAGING_PREFIX}x.previous"
        bundle.rename(moved)
        assert proc.pid in appinstall.running_from(moved), "proc_pidpath follows the rename"
    finally:
        proc.kill()
        proc.wait()
