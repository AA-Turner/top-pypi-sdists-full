"""finish or undo a swap the probe-swap program left halfway, and sweep old bundles and downloads beside the app."""

from __future__ import annotations
import json
import os
import shutil
import stat
from pathlib import Path

from . import locate as appupdate
from probe.service.updater.app.archive import _real_dir
from probe.service.updater.app.bundle_check import bundle_info
from probe.service.updater.app.errors import InstallError
from probe.service.updater.app.manifest import newer, same_version
from probe.service.updater.app.running import processes, running_from
from probe.service.updater.app.swap import (
    HELPER_DELETING_SUFFIX,
    HELPER_JOURNAL_NAME,
    HELPER_REFUSED,
    HELPER_REMOVED,
    helper_of,
    run_helper,
)
#: Beside the bundle: the staged bundle (after the swap, the old one) and its
#: archive. A name without `.app`: Finder and LaunchServices see a folder.
#: prbe-ai/desktop `probe-swap.rs` `STAGING_PREFIX`: its `--remove` takes only these.
STAGING_PREFIX = f".{appupdate.APP_NAME}.probe-update-"


def _remove(path: Path) -> bool:
    """Delete a download or staged copy of ours that was never the app (a real
    folder or file of this user, never through a link)."""
    try:
        info = os.lstat(path)
    except FileNotFoundError:
        return True
    except OSError:
        return False
    if info.st_uid != os.getuid():
        return False
    try:
        if stat.S_ISDIR(info.st_mode):
            shutil.rmtree(path)
        else:
            os.unlink(path)
    except OSError:
        return False
    return True


def leftovers(app: Path) -> list[Path]:
    """Downloads, staged copies and old bundles of ours beside `app`."""
    try:
        return sorted(p for p in app.parent.iterdir() if p.name.startswith(STAGING_PREFIX))
    except OSError:
        return []


def recover(home: Path, *, runner=run_helper, log=lambda message: None) -> list[str]:
    """A swap the helper left halfway (two renames, stopped between them: the
    app missing, the journal beside it): the staged bundle's own helper runs
    again and finishes it. The service never moves a bundle itself. Run before
    the app is looked for: until then there is no app to find. The helper
    writes its journal with real paths (`/private/var/...` for `/var/...`):
    both sides are compared resolved."""
    done = []
    for folder in (Path("/Applications"), home / "Applications"):
        journal = folder / HELPER_JOURNAL_NAME
        try:
            data = json.loads(journal.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            continue
        if not isinstance(data, dict) or not isinstance(data.get("target"), str) or not isinstance(data.get("own"), str):
            continue
        real = os.path.realpath(folder)
        target, own = Path(os.path.realpath(data["target"])), Path(os.path.realpath(data["own"]))
        if (
            str(target.parent) != real
            or target.name != appupdate.APP_NAME
            or str(own.parent) != real
            or not own.name.startswith(STAGING_PREFIX)
        ):
            continue
        if os.path.lexists(target):
            continue  # the app is there: nothing to finish
        helper = helper_of(own)
        answer = runner([str(helper), str(target)])[1] if helper is not None else None
        if answer is not None and answer.get("result") != HELPER_REFUSED:
            done.append(f"finished an interrupted swap of {target}: {answer.get('result')} ({answer.get('reason')})")
            continue
        # The new bundle's helper cannot finish (it refuses: its signature fails, say, after
        # its swap was stopped mid-undo) or is gone: the old app moved aside puts itself back
        # with its own helper (`restored`), when the journal names it and it has one.
        aside = Path(os.path.realpath(data["aside"])) if isinstance(data.get("aside"), str) else None
        old_helper = (
            helper_of(aside)
            if aside is not None and str(aside.parent) == real and aside.name == own.name + ".previous"
            else None
        )
        if old_helper is None:
            why = f"refused ({answer.get('reason')})" if answer is not None else "has no update helper"
            done.append(f"{target} is missing, the new release's helper {why}, and the old app cannot put itself "
                        "back; reinstall Probe")
            continue
        _, restored = runner([str(old_helper), str(target)])
        done.append(f"put the old app back at {target}: {restored.get('result')} ({restored.get('reason')})")
    for line in done:
        log(line)
    return done


def sweep(app: Path, home: Path, *, runner=run_helper, lister=processes, keep_old: bool = False) -> list[str]:
    """What earlier installs left beside `app`: an OLD bundle (older than the
    app, left by a swap), the same version failing its signature check (the
    app a repair replaced) and what a stopped `--remove` left (`<name>.deleting`)
    are deleted by the installed app's own helper (`--remove`), never by this
    Python; a download or a staged copy that was never swapped in (newer than
    the app, or the same version that the helper refuses) is ours and deleted
    here. Anything a process runs from, or that cannot be read, is left.
    `keep_old`: the installed app may not verify (an install's undo failed):
    older bundles stay, the last verified copy among them, until it is repaired."""
    found = leftovers(app)
    if not found:
        return []
    try:
        installed = bundle_info(app).get("CFBundleShortVersionString")
    except InstallError:
        return []
    removed = []
    helper = None
    for path in found:
        if not _real_dir(path):
            if path.name.endswith(".tar.gz") and _remove(path):
                removed.append(path.name)
            continue
        if path.name.endswith(HELPER_DELETING_SUFFIX):
            helper = helper or helper_of(app)
            if helper is not None and not running_from(path, lister=lister):
                _, answer = runner([str(helper), "--remove", str(path)])
                if answer.get("result") == HELPER_REMOVED:
                    removed.append(path.name)
            continue
        try:
            version = bundle_info(path).get("CFBundleShortVersionString")
        except InstallError:
            continue
        if not isinstance(version, str) or not isinstance(installed, str) or running_from(path, lister=lister):
            continue
        if newer(installed, version):
            helper = helper or helper_of(app)
            if helper is None or keep_old:
                continue
            _, answer = runner([str(helper), "--remove", str(path)])
            if answer.get("result") == HELPER_REMOVED:
                removed.append(path.name)
            continue
        if same_version(version, installed):
            # The same version: the app a repair replaced (failing its signature check: the
            # installed app's helper removes it), or a staged copy that was never the app
            # (which that helper refuses: ours, deleted here).
            helper = helper or helper_of(app)
            if helper is not None:
                _, answer = runner([str(helper), "--remove", str(path)])
                if answer.get("result") == HELPER_REMOVED:
                    removed.append(path.name)
                    continue
                if answer.get("result") != HELPER_REFUSED:
                    continue
        if _remove(path):
            removed.append(path.name)
    return removed
