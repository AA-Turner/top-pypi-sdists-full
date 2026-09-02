"""Static checks for shipped macOS LaunchAgent / LaunchDaemon plists + profiles.

Both gated launchd jobs run the signed ``aiwatch`` binary directly (no
``/bin/sh`` wrapper) so the registered background item is attributed to
``com.runlayer.aiwatch`` — covered by the Managed Login Items profile. A shell
wrapper would register an unmanaged ``sh`` login item that re-prompts the user
(ENG-3552). The managed-config short-circuit therefore lives inside the binary:

* ``aiwatch enroll`` exits 0 silently when no enrollment key is configured
  (``runlayer_cli/commands/enroll.py``).
* ``aiwatch setup hooks install --mdm`` exits 0 silently when no managed
  ``OrgApiKey`` is configured (``runlayer_cli/commands/aiwatch_setup.py``), so
  the bootstrap daemon's ``KeepAlive`` doesn't loop on unconfigured fleets.

The bootstrap daemon additionally has ``KeepAlive(SuccessfulExit=false)`` +
``ThrottleInterval=60`` for the bounded install-window fast-retry; see
``runlayer_cli/install_window.py``.

The Managed Login Items profile must match by ``BundleIdentifier`` (the binary's
code-signing identifier), not ``LabelPrefix``: Background Task Management keys a
non-app-bundle LaunchAgent's App Background Activity entry by that identifier, so
a ``LabelPrefix`` rule leaves the entry unmanaged (ENG-3552).
"""

from __future__ import annotations

import plistlib
import subprocess
from pathlib import Path

import pytest

_PACKAGING_MACOS = Path(__file__).parent.parent / "packaging" / "macos"

_BOOTSTRAP_PLIST = "com.runlayer.aiwatch.bootstrap.plist"
_DAEMON_AGENT_PLIST = "com.runlayer.aiwatch.daemon.plist"
_ENROLL_PLIST = "com.runlayer.aiwatch.enroll.plist"
_UPDATE_PLIST = "com.runlayer.aiwatch.update.plist"
_AIWATCH_PROFILE = "com.runlayer.aiwatch.mobileconfig"
_NATIVE_MESSAGING_HOST = "com.runlayer.aiwatch.native-messaging-host.json"
_FIREFOX_NATIVE_MESSAGING_HOST = (
    "com.runlayer.aiwatch.firefox-native-messaging-host.json"
)
_PLIST_NAMES: tuple[str, ...] = (
    _ENROLL_PLIST,
    _BOOTSTRAP_PLIST,
    _DAEMON_AGENT_PLIST,
)

# On-device version record for MDM inventory (ENG-4161). Dedicated domain, kept
# isolated from the MDM-owned com.runlayer.aiwatch config domain read by
# mdm_config.py; the aiwatch binary never reads this record back.
_VERSION_DOMAIN = "com.runlayer.aiwatch.version"
_VERSION_PLIST_PATH = "/Library/Preferences/com.runlayer.aiwatch.version.plist"

# (plist, expected ProgramArguments) — the signed binary is exec'd directly.
_DIRECT_EXEC_PLISTS: tuple[tuple[str, tuple[str, ...]], ...] = (
    (_ENROLL_PLIST, ("/usr/local/bin/aiwatch", "enroll")),
    (_DAEMON_AGENT_PLIST, ("/usr/local/bin/aiwatch", "daemon")),
    (
        _BOOTSTRAP_PLIST,
        ("/usr/local/bin/aiwatch", "setup", "hooks", "install", "--mdm"),
    ),
    (_UPDATE_PLIST, ("/usr/local/bin/aiwatch", "self-update")),
)


def _load_plist(name: str) -> dict:
    with (_PACKAGING_MACOS / name).open("rb") as f:
        return plistlib.load(f)


def _run_bootstrap_and_verify(
    tmp_path: Path,
    *,
    bootstrap_exit: int,
    print_exit: int,
) -> subprocess.CompletedProcess[str]:
    postinstall = (_PACKAGING_MACOS / "scripts" / "postinstall").read_text()
    function_body = postinstall.split("bootstrap_and_verify() {", 1)[1].split(
        "\n}\n", 1
    )[0]
    function_source = f"bootstrap_and_verify() {{{function_body}\n}}\n"

    launchctl = tmp_path / "launchctl"
    launchctl.write_text(
        "#!/bin/bash\n"
        'case "$1" in\n'
        f"    bootstrap) exit {bootstrap_exit} ;;\n"
        f"    print) exit {print_exit} ;;\n"
        "esac\n"
    )
    launchctl.chmod(0o755)
    sleep = tmp_path / "sleep"
    sleep.write_text("#!/bin/bash\nexit 0\n")
    sleep.chmod(0o755)

    return subprocess.run(
        [
            "/bin/bash",
            "-c",
            (
                f"{function_source}\n"
                'bootstrap_and_verify "gui/501" "/tmp/job.plist" '
                '"gui/501/com.runlayer.aiwatch"'
            ),
        ],
        check=False,
        capture_output=True,
        text=True,
        env={"PATH": f"{tmp_path}:/usr/bin:/bin"},
    )


@pytest.mark.parametrize(("plist_name", "expected_args"), _DIRECT_EXEC_PLISTS)
def test_plist_runs_signed_binary_directly(
    plist_name: str, expected_args: tuple[str, ...]
) -> None:
    """No ``/bin/sh`` wrapper — exec the signed binary so the background item is
    attributed to ``com.runlayer.aiwatch`` (covered by the login-items profile).
    The managed-config gate moved into the binary (see module docstring).
    """
    data = _load_plist(plist_name)

    args = data["ProgramArguments"]
    assert isinstance(args, list)
    assert args[0] == "/usr/local/bin/aiwatch", (
        "must exec the signed binary directly, not via /bin/sh (an unmanaged "
        '"sh" login item would re-prompt the user)'
    )
    assert "/bin/sh" not in args, "no shell wrapper around the binary"
    assert tuple(args) == expected_args


@pytest.mark.parametrize("plist_name", _PLIST_NAMES)
def test_plist_keeps_run_at_load_and_hourly_reassert(plist_name: str) -> None:
    """Direct-exec must not regress the existing scheduling contract."""
    data = _load_plist(plist_name)

    assert data["RunAtLoad"] is True
    assert data["StartInterval"] == 3600


def test_bootstrap_plist_has_bounded_fast_retry() -> None:
    """Bootstrap daemon: KeepAlive on non-zero exit, throttled to 60s.

    Combined with `runlayer_cli/install_window.py`, this fast-retries every
    60s for the 10-min install window after pkg install, then idles when
    `aiwatch setup hooks install` exits 0 (post-window). Drift correction
    continues via StartInterval=3600.
    """
    data = _load_plist(_BOOTSTRAP_PLIST)

    keep_alive = data["KeepAlive"]
    assert isinstance(keep_alive, dict), "KeepAlive must be conditional, not a bool"
    assert keep_alive == {"SuccessfulExit": False}, (
        "bootstrap daemon must only relaunch on non-zero exit (gate-failure "
        "fast-retry); successful runs idle until next StartInterval tick"
    )
    assert data["ThrottleInterval"] == 60, "60s minimum between fast-retry launches"


def test_daemon_agent_relaunches_failures_without_gate_off_loop() -> None:
    """A killed daemon relaunches, while gate-off clean exits wait for hourly retry."""
    data = _load_plist(_DAEMON_AGENT_PLIST)

    assert data["Label"] == "com.runlayer.aiwatch.daemon"
    assert data["KeepAlive"] == {"SuccessfulExit": False}
    assert data["ThrottleInterval"] == 60
    assert data["StartInterval"] == 3600

    build_script = (_PACKAGING_MACOS / "build_pkg.sh").read_text()
    postinstall = (_PACKAGING_MACOS / "scripts" / "postinstall").read_text()
    assert _DAEMON_AGENT_PLIST in build_script
    assert _DAEMON_AGENT_PLIST in postinstall
    assert "com.runlayer.aiwatch.daemon" in postinstall


def test_enroll_plist_has_no_keep_alive() -> None:
    """Enroll agent stays on its hourly StartInterval; no fast-retry there."""
    data = _load_plist(_ENROLL_PLIST)
    assert "KeepAlive" not in data
    assert "ThrottleInterval" not in data


def test_update_plist_is_a_plain_hourly_daemon() -> None:
    data = _load_plist(_UPDATE_PLIST)
    assert "KeepAlive" not in data
    assert "RunAtLoad" not in data
    assert data["StartInterval"] == 3600

    build_script = (_PACKAGING_MACOS / "build_pkg.sh").read_text()
    postinstall = (_PACKAGING_MACOS / "scripts" / "postinstall").read_text()
    assert _UPDATE_PLIST in build_script
    assert _UPDATE_PLIST in postinstall
    assert "com.runlayer.aiwatch.update" in postinstall
    assert 'launchctl bootstrap system "$UPDATE_DAEMON_PLIST"' in postinstall
    assert 'launchctl bootout "system/com.runlayer.aiwatch.update"' not in postinstall
    bootout_labels = postinstall.split("DAEMON_LABELS=(", 1)[1].split(")", 1)[0]
    assert "com.runlayer.aiwatch.update" not in bootout_labels, (
        "postinstall must not unload the updater during its own package transaction"
    )


def test_postinstall_waits_for_bootout_and_verifies_bootstrap() -> None:
    """Upgrades must not race an asynchronous launchd bootout.

    A running scan can take time to drain after ``bootout``. Bootstrapping the
    same label immediately may fail and leave the scan agent unloaded forever.
    """
    postinstall = (_PACKAGING_MACOS / "scripts" / "postinstall").read_text()

    assert "wait_for_job_to_unload() {" in postinstall
    assert "bootstrap_and_verify() {" in postinstall
    assert 'launchctl print "$service_target"' in postinstall
    assert 'wait_for_job_to_unload "$service_target"' in postinstall
    assert 'bootstrap_and_verify "$domain" "$plist" "$service_target"' in postinstall
    assert (
        'launchctl bootstrap "gui/${CONSOLE_UID}" "${AGENT_PLISTS[$i]}" '
        "2>/dev/null || true"
    ) not in postinstall
    assert (
        'launchctl bootstrap system "${DAEMON_PLISTS[$i]}" 2>/dev/null || true'
        not in postinstall
    )


def test_postinstall_does_not_verify_failed_bootstrap_from_draining_job(
    tmp_path: Path,
) -> None:
    """A still-registered old job must not verify a failed replacement."""
    result = _run_bootstrap_and_verify(
        tmp_path,
        bootstrap_exit=1,
        print_exit=0,
    )

    assert result.returncode != 0, (
        "a failed bootstrap must not be reported successful merely because "
        "launchctl print still sees the draining old job"
    )


def test_postinstall_verifies_successful_bootstrap(tmp_path: Path) -> None:
    result = _run_bootstrap_and_verify(
        tmp_path,
        bootstrap_exit=0,
        print_exit=0,
    )

    assert result.returncode == 0, (
        "a successfully registered and printable replacement should verify"
    )


def test_aiwatch_preinstall_removes_previous_onedir_bundle(tmp_path: Path) -> None:
    """An upgrade must replace the whole PyInstaller onedir bundle.

    PackageKit overlays payload files but does not remove version-named metadata
    that disappeared from the new payload. Leaving both
    ``runlayer-<old>.dist-info`` and ``runlayer-<new>.dist-info`` makes
    ``importlib.metadata.version("runlayer")`` report the old version forever,
    so the hourly updater repeatedly reinstalls the same target.
    """
    aiwatch_bundle = tmp_path / "usr/local/lib/runlayer/aiwatch"
    stale_metadata = aiwatch_bundle / "_internal/runlayer-0.28.8.dist-info"
    stale_metadata.mkdir(parents=True)
    (stale_metadata / "METADATA").write_text("Version: 0.28.8\n")
    cli_sibling = tmp_path / "usr/local/lib/runlayer/runlayer"
    cli_sibling.mkdir()

    result = subprocess.run(
        [
            "/bin/bash",
            str(_PACKAGING_MACOS / "scripts" / "preinstall"),
            "package.pkg",
            "/",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert not aiwatch_bundle.exists()
    assert cli_sibling.exists(), "AI Watch upgrade must not remove the CLI bundle"
    build_script = (_PACKAGING_MACOS / "build_pkg.sh").read_text()
    assert 'cp "$SCRIPT_DIR/scripts/preinstall" "$BUILD_DIR/scripts/preinstall"' in (
        build_script
    )


def test_runlayer_preinstall_removes_previous_onedir_bundle(tmp_path: Path) -> None:
    """The full CLI package must also replace its complete onedir bundle."""
    runlayer_bundle = tmp_path / "usr/local/lib/runlayer/runlayer"
    stale_metadata = runlayer_bundle / "_internal/runlayer-0.28.2.dist-info"
    stale_metadata.mkdir(parents=True)
    (stale_metadata / "METADATA").write_text("Version: 0.28.2\n")
    aiwatch_sibling = tmp_path / "usr/local/lib/runlayer/aiwatch"
    aiwatch_sibling.mkdir()
    desktop_app = tmp_path / "Applications/Runlayer.app"
    desktop_app.mkdir(parents=True)

    result = subprocess.run(
        [
            "/bin/bash",
            str(_PACKAGING_MACOS / "scripts" / "preinstall-runlayer"),
            "package.pkg",
            "/",
            str(tmp_path),
        ],
        check=False,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 0, result.stderr
    assert not runlayer_bundle.exists()
    assert not desktop_app.exists()
    assert aiwatch_sibling.exists(), "CLI upgrade must not remove AI Watch"
    build_script = (_PACKAGING_MACOS / "build_pkg_runlayer.sh").read_text()
    assert (
        'cp "$SCRIPT_DIR/scripts/preinstall-runlayer" "$BUILD_DIR/scripts/preinstall"'
    ) in build_script
    assert '--scripts "$BUILD_DIR/scripts"' in build_script


def test_runlayer_cli_pkg_bundles_and_launches_desktop_app() -> None:
    build_script = (_PACKAGING_MACOS / "build_pkg_runlayer.sh").read_text()
    postinstall = (_PACKAGING_MACOS / "scripts" / "postinstall-runlayer").read_text()
    info_template = (
        _PACKAGING_MACOS.parent.parent.parent / "desktop" / "macos" / "Info.plist.in"
    )
    info = plistlib.loads(
        info_template.read_text().replace("__VERSION__", "1.2.3").encode()
    )

    assert info["CFBundleIdentifier"] == "com.runlayer.desktop"
    assert info["LSUIElement"] is True
    assert info["CFBundleURLTypes"][0]["CFBundleURLSchemes"] == ["runlayer"]
    assert "payload/Applications/Runlayer.app" in build_script
    assert "--identifier com.runlayer.desktop" in build_script
    assert "codesign --verify --deep --strict" in build_script
    assert "DESKTOP_APP=/Applications/Runlayer.app" in postinstall
    assert "/usr/bin/pkill -TERM" in postinstall
    assert postinstall.index("/usr/bin/pkill -TERM") < postinstall.index(
        '/usr/bin/open "$DESKTOP_APP"'
    )
    assert '/usr/bin/open "$DESKTOP_APP"' in postinstall
    assert "/bin/launchctl asuser" in postinstall


def test_loginitems_profile_has_exact_bundle_team_pinned_rule() -> None:
    """Managed Login Items must match by BundleIdentifier, not LabelPrefix.

    Background Task Management keys a non-app-bundle LaunchAgent's App Background
    Activity entry by the binary's code-signing identifier
    (``com.runlayer.aiwatch``); a ``LabelPrefix`` rule leaves that entry
    unmanaged (ENG-3552). Apple ORs dicts across the Rules array, so the
    Developer ID ``TeamIdentifier`` must be a sibling key on the
    BundleIdentifier rule — a standalone team rule would auto-approve every
    background item signed by the team (ENG-3552).
    """
    data = _load_plist(_AIWATCH_PROFILE)

    payloads = [
        item
        for item in data["PayloadContent"]
        if item["PayloadType"] == "com.apple.servicemanagement"
    ]
    assert len(payloads) == 1, "merged profile must carry one login-items payload"
    payload = payloads[0]

    assert payload["Rules"] == [
        {
            "RuleType": "BundleIdentifier",
            "RuleValue": "com.runlayer.aiwatch",
            "TeamIdentifier": "AF2M8HC7A2",
        },
    ], "only the single bundle/team-pinned rule is allowed"


def test_postinstall_writes_install_window_stamp() -> None:
    """Postinstall must touch ``/var/db/com.runlayer.aiwatch/.install-time`` so
    ``runlayer_cli.install_window`` can decide whether the bootstrap daemon's
    KeepAlive should fast-retry (within 10 min) or idle (after).
    """
    from runlayer_cli.install_window import INSTALL_STAMP_PATH

    postinstall = (_PACKAGING_MACOS / "scripts" / "postinstall").read_text()

    parent = str(INSTALL_STAMP_PATH.parent)
    stamp = str(INSTALL_STAMP_PATH)
    assert f"mkdir -p {parent}" in postinstall
    assert f"chown root:wheel {parent}" in postinstall
    assert f"chmod 755 {parent}" in postinstall
    assert f": > {stamp}" in postinstall, "postinstall must touch the stamp"
    assert f"chown root:wheel {stamp}" in postinstall
    assert f"chmod 644 {stamp}" in postinstall


def test_postinstall_writes_version_record() -> None:
    """Postinstall stamps the installed version into the dedicated
    ``com.runlayer.aiwatch.version`` domain so MDM can inventory the version
    without exec'ing the binary (no FDA / TCC prompt). The absolute-path domain
    form writes the global domain, not root's ``~/Library``. ``__VERSION__`` is
    templated in by ``build_pkg.sh`` (asserted separately).
    """
    postinstall = (_PACKAGING_MACOS / "scripts" / "postinstall").read_text()

    assert (
        "defaults write /Library/Preferences/com.runlayer.aiwatch.version "
        'Version "__VERSION__"'
    ) in postinstall, (
        "postinstall must write the templated version to the version domain "
        "(absolute-path form -> global domain)"
    )
    # cfprefsd flushes the plist asynchronously, so the file may not exist yet
    # when chown/chmod run. They must tolerate failure — under `set -e` a strict
    # chown/chmod on a not-yet-flushed plist would abort the whole postinstall
    # (failed install).
    assert (
        f"chown root:wheel {_VERSION_PLIST_PATH} 2>/dev/null || true" in postinstall
    ), "version-plist chown must tolerate cfprefsd's async flush (2>/dev/null || true)"
    assert f"chmod 644 {_VERSION_PLIST_PATH} 2>/dev/null || true" in postinstall, (
        "version-plist chmod must tolerate cfprefsd's async flush (2>/dev/null || true)"
    )


def test_postinstall_preserves_runtime_chrome_policy() -> None:
    """Package upgrades must not rebuild away AI Watch's Chrome policy."""
    postinstall = (_PACKAGING_MACOS / "scripts" / "postinstall").read_text()

    assert "/usr/bin/mcxrefresh" not in postinstall


def test_postinstalls_do_not_expect_caller_environment() -> None:
    """PackageKit strips arbitrary caller env from scripts.

    Test Device configuration therefore runs as a chained command after
    ``installer``. Keeping both postinstalls free of these variables makes an
    MDM/GUI install follow the existing path byte-for-byte.
    """
    aiwatch = (_PACKAGING_MACOS / "scripts" / "postinstall").read_text()
    runlayer = (_PACKAGING_MACOS / "scripts" / "postinstall-runlayer").read_text()

    assert "AIWATCH_HOST" not in aiwatch
    assert "AIWATCH_ORG_API_KEY" not in aiwatch
    assert "RUNLAYER_CLI_HOST" not in runlayer
    assert "RUNLAYER_CLI_ORG_API_KEY" not in runlayer


def test_build_pkg_templates_version_into_postinstall() -> None:
    """``build_pkg.sh`` must sed ``__VERSION__`` into the postinstall (same
    mechanism as ``distribution.xml``), not plain-``cp`` it — otherwise the
    version record ships the literal ``__VERSION__`` placeholder.
    """
    build_script = (_PACKAGING_MACOS / "build_pkg.sh").read_text()

    assert "s|__VERSION__|${VERSION}|g" in build_script, (
        "build_pkg.sh must template __VERSION__"
    )
    assert '"$SCRIPT_DIR/scripts/postinstall"' in build_script, (
        "postinstall must be an input to the templating sed"
    )
    assert 'cp "$SCRIPT_DIR/scripts/postinstall"' not in build_script, (
        "postinstall must be templated, not plain-copied (would ship literal "
        "__VERSION__)"
    )


def test_uninstall_removes_version_record() -> None:
    """``uninstall.sh`` must remove the version record: ``rm`` the plist AND
    ``defaults delete`` the domain to drop the cfprefsd cache so a stale value
    can't be read back after uninstall.
    """
    uninstall = (_PACKAGING_MACOS / "uninstall.sh").read_text()

    assert f"rm -f {_VERSION_PLIST_PATH}" in uninstall
    assert f"defaults delete {_VERSION_DOMAIN}" in uninstall


@pytest.mark.parametrize(
    ("uninstall_name", "domain"),
    [
        ("uninstall.sh", "com.runlayer.aiwatch"),
        ("uninstall-runlayer.sh", "com.runlayer.cli"),
    ],
)
def test_uninstall_removes_only_local_test_device_config(
    uninstall_name: str,
    domain: str,
) -> None:
    uninstall = (_PACKAGING_MACOS / uninstall_name).read_text()
    defaults_delete = (
        f"defaults delete /Library/Preferences/{domain} 2>/dev/null || true"
    )
    remove_plist = f"rm -f /Library/Preferences/{domain}.plist"

    assert remove_plist in uninstall
    assert defaults_delete in uninstall
    assert uninstall.index(defaults_delete) < uninstall.index(remove_plist), (
        "defaults must clear cfprefsd before the backing plist is removed"
    )
    assert f"rm -f /Library/Managed Preferences/{domain}.plist" not in uninstall
    assert f"defaults delete /Library/Managed Preferences/{domain}" not in uninstall


def test_uninstall_removes_update_daemon() -> None:
    uninstall = (_PACKAGING_MACOS / "uninstall.sh").read_text()

    daemon_labels = uninstall.split("DAEMON_LABELS=(", 1)[1].split(")", 1)[0]
    assert "com.runlayer.aiwatch.update" in daemon_labels
    assert "rm -f /Library/LaunchDaemons/com.runlayer.aiwatch.update.plist" in uninstall


def test_uninstall_removes_daemon_agent_and_all_user_endpoints() -> None:
    uninstall = (_PACKAGING_MACOS / "uninstall.sh").read_text()
    cleanup_user = uninstall.split("cleanup_user() {", 1)[1].split("\n}", 1)[0]

    agent_labels = uninstall.split("AGENT_LABELS=(", 1)[1].split(")", 1)[0]
    assert "com.runlayer.aiwatch.daemon" in agent_labels
    assert "rm -f /Library/LaunchAgents/com.runlayer.aiwatch.daemon.plist" in uninstall
    assert "cleanup_user()" in uninstall
    assert "/usr/bin/dscl . -list /Users UniqueID" in uninstall
    assert "/usr/bin/who" in uninstall
    assert '/usr/bin/id -u "$ACTIVE_USER"' in uninstall
    assert 'cleanup_user "$CONSOLE_USER" "$CONSOLE_UID"' in uninstall
    assert 'cleanup_user "$ACTIVE_USER" "$ACTIVE_UID"' in uninstall
    assert 'cleanup_user "$USER_NAME" "$USER_UID"' in uninstall
    assert "CLEANED_UIDS" in uninstall
    assert 'launchctl bootout "gui/${user_uid}/${label}"' in uninstall
    assert '"$DAEMON_DIR/aiwatch.sock"' in uninstall
    assert '"$DAEMON_DIR/aiwatch.sock.lock"' in uninstall
    assert cleanup_user.index('rm -f "$DAEMON_DIR/aiwatch.sock"') < cleanup_user.index(
        'CLEANED_UIDS="$CLEANED_UIDS $user_uid"'
    )


def test_pkg_ships_chrome_native_messaging_host() -> None:
    """The macOS pkg must install the Chrome native host manifest + launcher."""
    import json

    manifest_path = _PACKAGING_MACOS / _NATIVE_MESSAGING_HOST
    manifest = json.loads(manifest_path.read_text())
    assert manifest == {
        "name": "com.runlayer.aiwatch",
        "description": "Runlayer AI Watch native identity host",
        "path": "/usr/local/lib/runlayer/aiwatch/aiwatch-native-messaging-host",
        "type": "stdio",
        "allowed_origins": ["chrome-extension://jijfcalfdbnjfpfcalkodmgmfijpfddi/"],
    }

    build_script = (_PACKAGING_MACOS / "build_pkg.sh").read_text()
    assert "Library/Google/Chrome/NativeMessagingHosts" in build_script
    assert "aiwatch-native-messaging-host" in build_script
    assert "com.runlayer.aiwatch.native-messaging-host.json" in build_script


def test_pkg_ships_firefox_native_messaging_host() -> None:
    """The macOS pkg allows the stable Firefox add-on ID to use identity."""
    import json

    manifest_path = _PACKAGING_MACOS / _FIREFOX_NATIVE_MESSAGING_HOST
    manifest = json.loads(manifest_path.read_text())
    assert manifest == {
        "name": "com.runlayer.aiwatch",
        "description": "Runlayer AI Watch native identity host",
        "path": "/usr/local/lib/runlayer/aiwatch/aiwatch-native-messaging-host",
        "type": "stdio",
        "allowed_extensions": ["aiwatch@runlayer.com"],
    }

    build_script = (_PACKAGING_MACOS / "build_pkg.sh").read_text()
    uninstall = (_PACKAGING_MACOS / "uninstall.sh").read_text()
    assert "Library/Application Support/Mozilla/NativeMessagingHosts" in build_script
    assert "com.runlayer.aiwatch.firefox-native-messaging-host.json" in build_script
    assert "Mozilla/NativeMessagingHosts/com.runlayer.aiwatch.json" in uninstall


# --- Full Runlayer CLI scheduler LaunchAgent (com.runlayer.cli.schedule) ---

_CLI_SCHEDULE_PLIST = "com.runlayer.cli.schedule.plist"
_CLI_PROFILE = "com.runlayer.cli.mobileconfig"


@pytest.mark.parametrize("name", [_CLI_SCHEDULE_PLIST, _CLI_PROFILE])
def test_cli_schedule_assets_lint_clean(name: str) -> None:
    """`plutil -lint` both new CLI plist assets (macOS only; plistlib parse
    everywhere else)."""
    path = _PACKAGING_MACOS / name
    _load_plist(name)  # parseable on every platform
    import shutil

    if shutil.which("plutil") is None:
        pytest.skip("plutil not available on this platform")
    result = subprocess.run(
        ["plutil", "-lint", str(path)], check=False, capture_output=True, text=True
    )
    assert result.returncode == 0, result.stdout + result.stderr


def test_cli_schedule_plist_runs_signed_binary_directly() -> None:
    """Direct binary exec so BTM attributes the item to com.runlayer.cli
    (covered by the CLI login-items profile); no /bin/sh wrapper (ENG-3552).
    """
    data = _load_plist(_CLI_SCHEDULE_PLIST)

    assert data["Label"] == "com.runlayer.cli.schedule"
    args = data["ProgramArguments"]
    assert "/bin/sh" not in args, "no shell wrapper around the binary"
    assert tuple(args) == ("/usr/local/bin/runlayer", "schedule")


def test_cli_schedule_plist_cadence() -> None:
    """RunAtLoad + hourly tick (same cadence as the CLI update daemon);
    no KeepAlive fast-retry (the command exits 0
    for every gated state, so KeepAlive would never fire anyway)."""
    data = _load_plist(_CLI_SCHEDULE_PLIST)

    assert data["RunAtLoad"] is True
    assert data["StartInterval"] == 3600
    assert "KeepAlive" not in data
    assert "ThrottleInterval" not in data


def test_cli_loginitems_profile_has_exact_bundle_team_pinned_rules() -> None:
    """Pin the CLI scheduler and desktop tray item to Runlayer's signing team.

    Apple ORs dicts across the Rules array, so each TeamIdentifier must be a
    sibling key on its BundleIdentifier rule. A standalone team rule would
    auto-approve every background item signed by the team (ENG-3552).
    """
    data = _load_plist(_CLI_PROFILE)

    payloads = [
        item
        for item in data["PayloadContent"]
        if item["PayloadType"] == "com.apple.servicemanagement"
    ]
    assert len(payloads) == 1, "merged profile must carry one login-items payload"
    payload = payloads[0]
    assert payload["Rules"] == [
        {
            "RuleType": "BundleIdentifier",
            "RuleValue": "com.runlayer.cli",
            "TeamIdentifier": "AF2M8HC7A2",
        },
        {
            "RuleType": "BundleIdentifier",
            "RuleValue": "com.runlayer.desktop",
            "TeamIdentifier": "AF2M8HC7A2",
        },
    ], "only the two bundle/team-pinned rules are allowed"


def test_cli_pkg_ships_schedule_agent() -> None:
    build_script = (_PACKAGING_MACOS / "build_pkg_runlayer.sh").read_text()

    assert 'mkdir -p "$BUILD_DIR/payload/Library/LaunchAgents"' in build_script
    assert (
        "$BUILD_DIR/payload/Library/LaunchAgents/com.runlayer.cli.schedule.plist"
        in build_script
    )
    assert "no user LaunchAgents" not in build_script, (
        "header comment must not claim the pkg ships no LaunchAgents anymore"
    )


def test_cli_postinstall_bootstraps_schedule_agent_for_console_user() -> None:
    """The agent is never the install transaction's parent (unlike the update
    daemon), so bootout + bootstrap into the console user's GUI domain picks
    up a refreshed plist on upgrades; both best-effort (|| true) so a
    loginwindow install still succeeds."""
    postinstall = (_PACKAGING_MACOS / "scripts" / "postinstall-runlayer").read_text()

    assert 'chown root:wheel "$SCHEDULE_AGENT_PLIST"' in postinstall
    assert 'chmod 644 "$SCHEDULE_AGENT_PLIST"' in postinstall
    assert "CONSOLE_USER=$(/usr/bin/stat -f '%Su' /dev/console" in postinstall
    assert 'CONSOLE_UID=$(/usr/bin/id -u "$CONSOLE_USER")' in postinstall
    assert (
        'launchctl bootout "gui/${CONSOLE_UID}/${SCHEDULE_AGENT_LABEL}" '
        "2>/dev/null || true" in postinstall
    )
    assert (
        'launchctl bootstrap "gui/${CONSOLE_UID}" "$SCHEDULE_AGENT_PLIST" '
        "2>/dev/null || true" in postinstall
    )
    # The update daemon contract is unchanged: no bootout beneath a possibly
    # parent updater transaction.
    assert 'launchctl bootout "system/com.runlayer.cli.update"' not in postinstall


def test_cli_uninstall_removes_schedule_agent_and_updater() -> None:
    uninstall = (_PACKAGING_MACOS / "uninstall-runlayer.sh").read_text()

    agent_labels = uninstall.split("AGENT_LABELS=(", 1)[1].split(")", 1)[0]
    assert "com.runlayer.cli.schedule" in agent_labels
    daemon_labels = uninstall.split("DAEMON_LABELS=(", 1)[1].split(")", 1)[0]
    assert "com.runlayer.cli.update" in daemon_labels
    assert "rm -f /Library/LaunchAgents/com.runlayer.cli.schedule.plist" in uninstall
    assert "rm -f /Library/LaunchDaemons/com.runlayer.cli.update.plist" in uninstall
    assert "rm -rf /usr/local/lib/runlayer/runlayer" in uninstall
    assert "pkgutil --forget com.runlayer.cli" in uninstall
    assert "aiwatch" not in uninstall.replace("uninstall.sh (AI Watch)", "").replace(
        "AI Watch", ""
    ), "must not touch the AI Watch install"
