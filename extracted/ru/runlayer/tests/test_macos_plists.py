"""Static checks for shipped macOS LaunchAgent / LaunchDaemon plists.

Both gated plists must short-circuit silently on unconfigured fleets so they
don't spam `log stream`. Implementation: ``/bin/sh -c '...defaults read ...
|| exit 0; exec /usr/local/bin/aiwatch "$@"' -- <args>`` so ``defaults read``
failure cleanly exits 0 (no ``KeepAlive`` retry on the bootstrap daemon).

The gate key differs per plist: the bootstrap daemon gates on ``OrgApiKey``
(the single AI Watch key — hooks authenticate with it directly), while the
legacy enroll agent still gates on ``EnrollmentKey``.

The bootstrap daemon additionally has ``KeepAlive(SuccessfulExit=false)`` +
``ThrottleInterval=60`` for the bounded install-window fast-retry; see
``runlayer_cli/install_window.py``.
"""

from __future__ import annotations

import plistlib
from pathlib import Path

import pytest

_PACKAGING_MACOS = Path(__file__).parent.parent / "packaging" / "macos"

_BOOTSTRAP_PLIST = "com.runlayer.aiwatch.bootstrap.plist"
_ENROLL_PLIST = "com.runlayer.aiwatch.enroll.plist"

# (plist, gate key, expected aiwatch args)
_GATED_PLISTS: tuple[tuple[str, str, tuple[str, ...]], ...] = (
    (_ENROLL_PLIST, "EnrollmentKey", ("enroll",)),
    (
        _BOOTSTRAP_PLIST,
        "OrgApiKey",
        ("setup", "hooks", "install", "--mdm"),
    ),
)


def _load_plist(name: str) -> dict:
    with (_PACKAGING_MACOS / name).open("rb") as f:
        return plistlib.load(f)


@pytest.mark.parametrize(
    ("plist_name", "gate_key", "expected_aiwatch_args"), _GATED_PLISTS
)
def test_plist_gates_on_managed_key(
    plist_name: str, gate_key: str, expected_aiwatch_args: tuple[str, ...]
) -> None:
    data = _load_plist(plist_name)

    args = data["ProgramArguments"]
    assert isinstance(args, list)
    assert args[0] == "/bin/sh", "gate must invoke /bin/sh, not aiwatch directly"
    assert args[1] == "-c"

    gate = args[2]
    assert "/usr/bin/defaults read" in gate
    assert '"/Library/Managed Preferences/com.runlayer.aiwatch"' in gate
    assert gate_key in gate
    assert "|| exit 0" in gate, (
        "gate must exit 0 (not propagate `defaults read` failure) so the "
        "bootstrap daemon's KeepAlive doesn't loop on unconfigured fleets"
    )
    assert "exec /usr/local/bin/aiwatch" in gate
    assert '"$@"' in gate, "gate must forward trailing args to aiwatch"

    assert args[3] == "--", "args after gate must be separated by --"
    assert tuple(args[4:]) == expected_aiwatch_args


@pytest.mark.parametrize(("plist_name", "_gate_key", "_args"), _GATED_PLISTS)
def test_plist_keeps_run_at_load_and_hourly_reassert(
    plist_name: str, _gate_key: str, _args: tuple[str, ...]
) -> None:
    """Gate must not regress the existing scheduling contract."""
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


def test_enroll_plist_has_no_keep_alive() -> None:
    """Enroll agent stays on its hourly StartInterval; no fast-retry there."""
    data = _load_plist(_ENROLL_PLIST)
    assert "KeepAlive" not in data
    assert "ThrottleInterval" not in data


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
