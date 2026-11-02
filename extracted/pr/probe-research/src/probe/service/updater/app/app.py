"""The Probe service installs a CLOSED desktop app's update (plan E1/E3; owner 2026-10-24).

An open app is asked (`app.check`) and its own signed updater installs at a
quiet moment. A closed app used to wait for its next launch, and the person
waited for the update there. Now the update cycle installs it while nothing
of the app runs, starting no app process (a hidden `--background-update`
launch showed a Dock icon and "Stop Running in Background"; removed 10-23):

    manifest   the endpoint the app's updater reads (ENDPOINTS), parsed as
               tauri-plugin-updater 2.14.0 parses it, the entry its updater
               would pick (`darwin-<arch>-app`, then `darwin-<arch>`); never a
               version older than or equal to the installed bundle's
               CFBundleShortVersionString
    download   to a staging folder beside the bundle (same volume), bounded
               in time (each read too) and size, https only
    verify     the minisign signature exactly as the app's updater checks it
               (minisign-verify 0.3.0 with legacy allowed, then the signed
               version, `requireSignedVersion`): the key id, `Ed` (the file
               itself) or `ED` (its BLAKE2b-512, what Tauri's signer makes),
               the global signature over the trusted comment, and the trusted
               comment's `version:` equal to the announced version (build
               metadata compared literally, as the semver crate does). The
               key is PUBKEY, pinned here; anything that does not verify is
               refused
    extract    regular files, folders and links that stay inside the bundle
               (every link resolved, through chains of links); no `..`, no
               absolute paths, no hard links, devices or setuid bits, no entry
               twice (case- and normalization-folded, as APFS compares names),
               bounded in count and size; then the bundle id
               `ai.prbe.desktop`, the version the signature names, its
               executable, and `codesign --verify --deep --strict -R` against
               the Probe team's Developer ID (TEAM_REQUIREMENT)
    swap       NEVER by this Python: macOS App Management blocks a change to a
               notarized app by code not signed by the app's team and tells
               the person (WWDC22 10096). The staged release's own helper
               (`Contents/MacOS/probe-swap`, prbe-ai/desktop
               `src-tauri/src/bin/probe-swap.rs`, signed by the same team) runs
               as its OWN responsible process (posix_spawn with
               `responsibility_spawnattrs_setdisclaim`; a macOS without it
               fails the step before the download, and the app's own updater
               installs at its launch): it takes the app's instance lock,
               checks the app again under it, finds no process under the app,
               swaps with `renamex_np(RENAME_SWAP)` (two journalled renames
               where the volume cannot swap, finished by the next run:
               `recover`), verifies the new app and swaps back if it does not
               verify or an old copy started from the old bundle meanwhile.
               Its answer is read by its machine words (`result`, `reason`),
               never its `detail`. The old bundle is deleted by the NEW app's
               helper (`--remove`), now or on a later cycle (`sweep`); this
               Python deletes only a staged copy that still holds the NEW
               version with nothing running from it

Skipped, never prompted: a bundle or folder this user cannot write
(`not_writable`), a Probe app process or the instance lock held
(`app_running`), macOS refusing the helper's rename (the helper's
`not_permitted`: EPERM or EACCES, App Management or permissions), a
release without the helper (`no_helper`, every release before it; not
downloaded again): the app's own updater handles those at its next launch.

Someone opening the app mid-install: before the swap the old app opens as
always (its launch check is handed to it and its own updater runs; the helper
then finds the instance lock held and the staged copy is thrown away). During
the swap (milliseconds, under the instance lock) the launch resolves the
bundle path to the old or the new bundle, never a mix (one atomic rename). An
old copy that started from the old bundle in that window opens its window and
waits for the instance lock only at its update gate (the desktop app takes the
lock on a thread); the helper finds it under the old bundle's new name and
swaps back under it, so for those few milliseconds it may read resources from
the new bundle.

macOS only (`supported`): Linux and Windows have no desktop app; their app
step stays as it was. Stdlib at import (the service's start path, plan S1);
`cryptography` (Ed25519) is imported when a signature is checked, and
`preload` (the update cycle, before step 1 replaces the CLI's files, plan R2).
"""

from __future__ import annotations
import contextlib
import os
import secrets
import stat
from pathlib import Path
from probe.service.updater.app.archive import ARCHIVE_MAX_BYTES, _real_dir, extract
from probe.service.updater.app.bundle_check import (
    BUNDLE_ID,
    app_broken,
    bundle_info,
    check_bundle,
    codesign_verify,
)
from probe.service.updater.app.download import ENDPOINTS, _Deadline, check, fetch
from probe.service.updater.app.errors import InstallError
from probe.service.updater.app.manifest import newer, parse_version, same_version, supported, targets
from probe.service.updater.app.recovery import STAGING_PREFIX, _remove, sweep
from probe.service.updater.app.running import lock_held, processes, running_from
from probe.service.updater.app.signature import PUBKEY, parse_public_key, parse_signature, verify_file
from probe.service.updater.app.swap import (
    HELPER_APP_RUNNING,
    HELPER_JOURNAL_NAME,
    HELPER_NOT_PERMITTED,
    HELPER_REMOVED,
    HELPER_SWAPPED,
    INSTALLED_ANYWAY,
    _disclaim_available,
    helper_of,
    run_helper,
)

#: The app's own bound (`background_update.rs` TIME_LIMIT): manifest and download.
TIME_LIMIT_S = 10 * 60
#: A refused swap (`not_permitted`) is not tried again for this long: each try
#: can raise a macOS notification about the refusal.
REFUSED_BACKOFF_S = 7 * 24 * 3600


class Outcome:
    """What `install_closed` did: the cycle's `app` step outcome."""

    #: The newer app is in place (`version_before` -> `version_after`).
    INSTALLED = "installed"
    #: The installed app is the newest (nothing downloaded).
    CURRENT = "current"
    #: The manifest, download, signature, archive or swap failed (`error`).
    FAILED = "failed"
    #: Skipped: this user cannot write the bundle or its folder.
    NOT_WRITABLE = "not_writable"
    #: Skipped: a Probe app process runs, or holds the instance lock.
    APP_RUNNING = "app_running"
    #: Skipped: the system refused the helper's rename (macOS App Management).
    NOT_PERMITTED = "not_permitted"
    #: Skipped: the release has no update helper (`ProbeSwapHelper`); the app's
    #: own updater installs it at its next launch.
    NO_HELPER = "no_helper"
    #: Skipped: this release's helper refused it earlier for a reason that does
    #: not change for the same release (`PERMANENT_REFUSALS`); not downloaded
    #: again for REFUSED_BACKOFF_S or until another release is the latest.
    REFUSED_RELEASE = "refused_release"


SKIPS = frozenset({
    Outcome.NOT_WRITABLE, Outcome.APP_RUNNING, Outcome.NOT_PERMITTED, Outcome.NO_HELPER, Outcome.REFUSED_RELEASE,
})


class Skip(Exception):
    """A step that cannot go ahead now, harmlessly (`Outcome` in SKIPS)."""

    def __init__(self, outcome: str, detail: str) -> None:
        super().__init__(detail)
        self.outcome = outcome


def preload() -> None:
    """What an install imports later, now (`updater.preload`, plan R2)."""
    import ctypes  # noqa: F401
    import ctypes.util  # noqa: F401
    import fcntl  # noqa: F401
    import signal  # noqa: F401
    import tempfile  # noqa: F401
    import plistlib  # noqa: F401
    import ssl  # noqa: F401
    import tarfile  # noqa: F401
    import urllib.request  # noqa: F401
    import zlib  # noqa: F401

    with contextlib.suppress(Exception):
        from probe.foundation.tls import tls  # noqa: F401
    with contextlib.suppress(ImportError):
        from cryptography.hazmat.primitives.asymmetric import ed25519  # noqa: F401


# -- the install -------------------------------------------------------------------


def _writable(path: Path) -> bool:
    """Can this user write `path`, read from its owner, group and mode bits?
    Never `os.access(W_OK)`: on macOS that asks App Management about a
    protected app bundle, and a background caller's ask is logged as a refused
    approval request (seen on a real Mac, 2026-10-25). Reading the mode asks
    nothing. ACLs are not read: an ACL-only grant reads as not writable, which
    skips (the app's own updater installs at its launch), never prompts."""
    try:
        st = os.stat(path)
    except OSError:
        return False
    if not hasattr(os, "geteuid"):
        return os.access(path, os.W_OK)  # Windows: no App Management to ask
    uid = os.geteuid()
    if uid == 0:
        return True
    if st.st_uid == uid:
        return bool(st.st_mode & stat.S_IWUSR)
    if st.st_gid == os.getegid() or st.st_gid in os.getgroups():
        return bool(st.st_mode & stat.S_IWGRP)
    return bool(st.st_mode & stat.S_IWOTH)


def check_links(root: Path) -> None:
    """Every link in the unpacked bundle resolves inside it, through any chain
    of links (each was checked on its own while unpacking)."""
    top = os.path.realpath(root)
    for folder, dirs, files in os.walk(root):
        for name in dirs + files:
            path = os.path.join(folder, name)
            if os.path.islink(path):
                real = os.path.realpath(path)
                if real != top and not real.startswith(top + os.sep):
                    raise InstallError(f"the link {os.path.relpath(path, root)!r} resolves outside the bundle")


def _holds_version(bundle: Path, version: str) -> bool:
    """Is `bundle` a real folder whose Info.plist names `version`?"""
    if not _real_dir(bundle):
        return False
    try:
        found = bundle_info(bundle).get("CFBundleShortVersionString")
    except InstallError:
        return False
    return isinstance(found, str) and same_version(found, version)


def install_closed(
    app: Path,
    *,
    home: Path,
    endpoints=ENDPOINTS,
    pubkey: str = PUBKEY,
    fetcher=fetch,
    lister=processes,
    runner=run_helper,
    machine_arch: str | None = None,
    time_limit_s: float = TIME_LIMIT_S,
    skip_version: str | None = None,
    refused_version: str | None = None,
    repair: bool = False,
    log=lambda message: None,
) -> dict:
    """Install the newest release over the closed app at `app`.

    `{outcome, version_before, version_after, latest, error, detail, helper}`
    (`Outcome`; `helper`: the helper's `result`, `reason` and `undo_failed`).
    `skip_version`: a release found earlier to have no update helper;
    `refused_version`: one whose helper refused it for a reason that does not
    change (PERMANENT_REFUSALS). Neither is downloaded again. `repair`: an
    earlier install's undo failed and left an app that may not verify; the app
    is never `current` while it fails `codesign_verify`, and the latest release
    of the same version is installed over it (the helper takes the same version
    over an app that fails its signature check). Never raises;
    never prompts; never starts the app; never renames, swaps or deletes the
    app's bundle (the release's own helper does)."""
    out: dict = {"outcome": Outcome.FAILED, "version_before": None, "version_after": None, "error": None}
    staged: Path | None = None
    archive: Path | None = None
    try:
        info = bundle_info(app)
        if info.get("CFBundleIdentifier") != BUNDLE_ID:
            raise InstallError(f"{app} is not the Probe app")
        before = info.get("CFBundleShortVersionString")
        if parse_version(before) is None:
            raise InstallError(f"the installed app's version {before!r} is not a version")
        out["version_before"] = out["version_after"] = before
        if os.path.islink(app):
            raise Skip(Outcome.NOT_WRITABLE, f"{app} is a link; the app's own updater installs it")
        for path in (app, app.parent):
            if not _writable(path):
                raise Skip(Outcome.NOT_WRITABLE, f"{path} is not writable by this user")
        removed = sweep(app, home, runner=runner, lister=lister, keep_old=repair)
        if removed:
            log(f"removed {', '.join(removed)} left by an earlier install")
        if running_from(app, lister=lister) or lock_held(home):
            raise Skip(Outcome.APP_RUNNING, "the app is running; it installs its own update")
        deadline = _Deadline(time_limit_s)
        version, entry = check(endpoints, deadline=deadline, fetcher=fetcher, machine_arch=machine_arch)
        if version is None or not newer(version, before):
            broken = app_broken(app) if repair else None
            if broken is None:
                out["outcome"] = Outcome.CURRENT
                out["latest"] = version
                log(f"the installed app ({before}) is the newest" + (f" (latest {version})" if version else ""))
                return out
            out["latest"] = version
            if version is None or not same_version(version, before):
                raise InstallError(f"{broken}; no release can repair it: reinstall Probe")
            out["repair"] = True
            log(f"{broken}: installing {version} over it")
        out["latest"] = version
        if skip_version is not None and same_version(version, skip_version):
            raise Skip(Outcome.NO_HELPER, f"{version} has no update helper; the app updates itself at its launch")
        if refused_version is not None and same_version(version, refused_version):
            raise Skip(Outcome.REFUSED_RELEASE,
                       f"{version}'s update helper refused it earlier; the app updates itself at its launch")
        if entry is None:
            raise InstallError(f"the {version} manifest has no entry for {', '.join(targets(machine_arch))}")
        if supported() and not _disclaim_available():
            # Run any other way, the helper's change would be judged by this Python
            # (App Management: refused, with a notification). Nothing is downloaded.
            raise InstallError(
                "this macOS cannot start the update helper as its own process; the app updates itself at its launch"
            )
        key = parse_public_key(pubkey)
        signature = parse_signature(entry["signature"])
        token = secrets.token_hex(6)
        staged = app.parent / f"{STAGING_PREFIX}{token}"
        archive = app.parent / f"{STAGING_PREFIX}{token}.tar.gz"
        log(f"downloading {version} for the closed app ({before})")
        flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL | getattr(os, "O_NOFOLLOW", 0)
        with os.fdopen(os.open(archive, flags, 0o600), "wb") as sink:
            fetcher(entry["url"], accept="application/octet-stream", limit=ARCHIVE_MAX_BYTES, deadline=deadline, sink=sink)
        verify_file(archive, signature, key, version)
        os.mkdir(staged, 0o700)
        if os.stat(staged).st_dev != os.stat(app).st_dev:
            raise InstallError("the staging folder is not on the app's volume")
        extract(archive, staged)
        archive.unlink()
        archive = None
        check_links(staged)
        check_bundle(staged, version)
        signed = codesign_verify(staged)
        helper = helper_of(staged)
        if helper is None:
            raise Skip(Outcome.NO_HELPER, f"{version} has no update helper; the app updates itself at its launch")
        # The installed bundle's root keeps the folder's usual mode.
        os.chmod(staged, 0o755)
        if running_from(app, lister=lister) or lock_held(home):
            raise Skip(Outcome.APP_RUNNING, "the app started during the download; it installs its own update")
        code, answer = runner([str(helper), str(app)])
        result, reason = answer.get("result"), answer.get("reason")
        undo_failed = answer.get("undo_failed") is True
        detail = str(answer.get("detail") or "")
        out["helper"] = {"result": result, "reason": reason, "undo_failed": undo_failed}
        # The staged path is this Python's to delete only while it still holds the NEW
        # release with nothing running from it, and no swap is halfway. After a swap
        # it holds the OLD app (the new app's helper removes it); after a swap the
        # helper could not undo, either one: the sweep looks again later. The helper's
        # `old` names it when it holds the old app (a repair's old app has the same
        # version as the new one).
        old_at = answer.get("old") if isinstance(answer.get("old"), str) else None
        if old_at is not None:
            out["old_app"] = old_at
        if staged is not None and (
            (app.parent / HELPER_JOURNAL_NAME).exists()
            or result == HELPER_SWAPPED
            or (old_at is not None and os.path.realpath(old_at) == os.path.realpath(staged))
            or not _holds_version(staged, version)
            or running_from(staged, lister=lister)
        ):
            staged = None
        try:
            after = bundle_info(app).get("CFBundleShortVersionString")
        except InstallError:
            after = None
        reads_new = isinstance(after, str) and same_version(after, version)
        # Without `swapped`, the version alone says the new release went in only when it
        # differs from the one before (a repair keeps the version).
        moved = reads_new and not same_version(str(before), version)
        if result == HELPER_SWAPPED and not reads_new:
            raise InstallError(f"after the swap {app} reads version {after!r}, not {version}")
        if result != HELPER_SWAPPED and not (moved and reason in INSTALLED_ANYWAY):
            if result == HELPER_APP_RUNNING:
                # Nothing moved, or the helper undid its swap under an old copy that started.
                raise Skip(Outcome.APP_RUNNING, detail or "the app started during the install")
            if result == HELPER_NOT_PERMITTED:
                raise Skip(Outcome.NOT_PERMITTED, detail or "the system refused the update helper's rename")
            message = f"the update helper answered {result} ({reason}{', undo failed' if undo_failed else ''}, " \
                      f"exit {code}): {detail}"
            if isinstance(answer.get("old"), str):
                message += f"; the old app is at {answer['old']}"
            raise InstallError(message)
        # In place: swapped, or an answer that is not `swapped` with the new release
        # already the app (INSTALLED_ANYWAY: the answer lost, or an old copy started).
        out.update(outcome=Outcome.INSTALLED, version_after=after, codesign=signed)
        out["old_bundle"] = "kept until no Probe process runs from it"
        old, new_helper = answer.get("old"), helper_of(app)
        if result == HELPER_SWAPPED and isinstance(old, str) and new_helper is not None:
            # Only after a swap the helper verified: otherwise the old app may be the last
            # verified copy, and the sweep looks at it later.
            _, removal = runner([str(new_helper), "--remove", old])
            if removal.get("result") == HELPER_REMOVED:
                out["old_bundle"] = "removed"
        if result == HELPER_SWAPPED:
            log(f"installed {after} over the closed app ({before}) with its update helper")
        else:
            log(f"the update helper answered {result} ({reason}), and {after} is the app now: installed")
        return out
    except Skip as skip:
        out.update(outcome=skip.outcome, detail=str(skip))
        log(f"app install skipped ({skip.outcome}): {skip}")
        return out
    except InstallError as exc:
        out.update(outcome=Outcome.FAILED, error=str(exc)[:500])
        log(f"app install failed: {exc}")
        return out
    except Exception as exc:  # noqa: BLE001 -- a bug costs this install, never the cycle
        out.update(outcome=Outcome.FAILED, error=f"{type(exc).__name__}: {exc}"[:500])
        log(f"app install failed: {exc!r}")
        return out
    finally:
        for leftover in (archive, staged):
            if leftover is not None:
                _remove(leftover)
