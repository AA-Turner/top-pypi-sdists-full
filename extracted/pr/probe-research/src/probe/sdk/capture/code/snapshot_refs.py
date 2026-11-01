"""retired refs/probe/snapshots: say once per repo that they remain, bundle them, prune them."""

from __future__ import annotations
import contextlib
import hashlib
import os
import subprocess
import sys
from ....foundation.durable import homedir


#: Where the retired shadow commits lived. Still READ (to report and prune them).
SNAPSHOT_REFS_PREFIX = "refs/probe/snapshots/"


def old_snapshot_refs(cwd: str) -> list[tuple[str, str]]:
    """Every ``refs/probe/snapshots/*`` ref in this repo as ``(ref, sha)``, loose
    or packed (``for-each-ref`` reads both). A ref name cannot hold a space."""
    out: list[tuple[str, str]] = []
    listing = _git(
        cwd, "for-each-ref", "--format=%(objectname) %(refname)", SNAPSHOT_REFS_PREFIX, check=False
    )
    for line in listing.splitlines():
        sha, _, ref = line.partition(" ")
        if ref.startswith(SNAPSHOT_REFS_PREFIX):
            out.append((ref, sha))
    return out


def bundle_snapshot_refs(cwd: str, refs: list[str], path: str) -> None:
    """Back ``refs`` up, with every object they reach, to a git bundle at
    ``path``, and verify it. Undo a prune with
    ``git fetch <path> 'refs/probe/snapshots/*:refs/probe/snapshots/*'``, even
    after gc has removed the objects from the repo.

    The bundle holds the same bytes the refs do (an untracked ``.env`` among
    them), so it may not land in the working tree: the next code capture would
    upload it, and ``git add .`` would commit it.
    """
    top = _git(cwd, "rev-parse", "--show-toplevel", check=False)
    target = os.path.realpath(path)
    if top:
        top = os.path.realpath(top)
        git_dir = os.path.realpath(os.path.join(top, ".git"))
        inside = target == top or target.startswith(top + os.sep)
        if inside and not target.startswith(git_dir + os.sep):
            raise SnapshotError(
                f"{path} is inside the working tree ({top}); code capture would upload "
                "it. Write the bundle somewhere outside the repository."
            )
    if os.path.exists(target):
        raise SnapshotError(f"{path} already exists; refusing to overwrite it")
    proc = subprocess.run(
        ["git", "bundle", "create", target, "--stdin"],
        cwd=cwd,
        input="".join(f"{ref}\n" for ref in refs),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SnapshotError(f"git bundle create: {proc.stderr.strip()}")
    check = subprocess.run(
        ["git", "bundle", "list-heads", target], cwd=cwd, capture_output=True, text=True
    )
    held = {line.split(" ", 1)[1] for line in check.stdout.splitlines() if " " in line}
    if check.returncode != 0 or not set(refs) <= held:
        raise SnapshotError(f"git bundle {path} does not hold every ref; nothing deleted")


def prune_snapshot_refs(cwd: str, refs: list[tuple[str, str]]) -> None:
    """Delete exactly these ``(ref, sha)`` pairs, in one transaction.

    EXPLICIT ONLY (decision D10): a shadow commit may be the only copy of a dirty
    tree whose upload failed, so nothing deletes these on its own, and the CLI
    decides which are safe. One ``update-ref --stdin`` transaction removes packed
    refs as well as loose ones, and each delete names the sha it expects: a ref
    that moved after it was listed fails the whole transaction rather than
    deleting a commit nobody saw. The objects stay until git's gc removes them.
    """
    if not refs:
        return
    proc = subprocess.run(
        ["git", "update-ref", "--stdin"],
        cwd=cwd,
        input="".join(f"delete {ref} {sha}\n" for ref, sha in refs),
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        raise SnapshotError(f"git update-ref: {proc.stderr.strip()}")
    # What the notice counted is gone: the refs still left get one fresh notice.
    forget_snapshot_ref_notice(cwd)


_NOTICED: set[str] = set()


def _notice_marker(common_dir: str) -> str:
    base = os.environ.get("XDG_STATE_HOME") or os.path.join(str(homedir.home()), ".local", "state")
    key = hashlib.sha256(os.path.abspath(common_dir).encode("utf-8", "surrogateescape")).hexdigest()[:16]
    return os.path.join(base, "probe", "notices", f"snapshot-refs-{key}")


def _shown_count(marker: str) -> int | None:
    """How many refs the last notice counted, or None if it was never shown."""
    try:
        with open(marker, encoding="utf-8") as fh:
            return int(fh.read().strip() or "0")
    except (OSError, ValueError):
        return None


def _write_marker(marker: str, count: int) -> None:
    try:
        os.makedirs(os.path.dirname(marker), exist_ok=True)
        with open(marker, "w", encoding="utf-8") as fh:
            fh.write(f"{count}\n")
    except OSError:
        pass  # once per process instead of once per machine


def forget_snapshot_ref_notice(cwd: str) -> None:
    """Let the notice show again for this repo (after a prune)."""
    try:
        common = _common_dir(cwd)
        if common:
            _NOTICED.discard(common)
            with contextlib.suppress(FileNotFoundError):
                os.remove(_notice_marker(common))
    except Exception:  # noqa: BLE001, S110 -- a notice may never cost the prune
        pass


def notice_old_snapshot_refs(cwd: str) -> bool:
    """Say once per repo per machine that old snapshot refs are still here, and
    again when there are more of them than last time. Never deletes (D10). True
    when the notice was shown.

    Written straight to stderr, not through ``warnings``: training scripts run
    with warnings ignored often enough (``PYTHONWARNINGS=ignore``,
    ``simplefilter("ignore")``) that a once-only warning could be marked shown
    and never seen. The marker is written only after the notice was.
    """
    try:
        common = _common_dir(cwd)
        if not common or common in _NOTICED:
            return False
        _NOTICED.add(common)
        refs = old_snapshot_refs(cwd)
        marker = _notice_marker(common)
        shown = _shown_count(marker)
        if shown is not None and len(refs) <= shown:
            if len(refs) < shown:
                _write_marker(marker, len(refs))  # so that growth from here is seen
            return False
        if not refs:
            return False
        print(
            f"probe: this repo still holds {len(refs)} old code-snapshot ref(s) "
            f"({SNAPSHOT_REFS_PREFIX}*) from earlier Probe versions. Each is a copy of "
            "the working tree at run start, untracked files included, and `git push "
            "--mirror` publishes them. Probe no longer writes them and never deletes "
            "them on its own: review with `probe snapshot-prune-refs --dry-run`, "
            "remove with `probe snapshot-prune-refs`. This notice is shown once "
            "(again only if more appear).",
            file=sys.stderr,
            flush=True,
        )
        _write_marker(marker, len(refs))
        return True
    except Exception:  # noqa: BLE001 -- a notice may never cost the capture
        return False
from probe.sdk.capture.code.code import SnapshotError  # noqa: E402 -- pieces need each other; the front door loads this one first
from probe.sdk.capture.code.git import _common_dir, _git  # noqa: E402 -- pieces need each other; the front door loads this one first
