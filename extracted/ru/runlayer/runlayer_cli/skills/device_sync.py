"""Managed skill reconciler for MDM-deployed aiwatch (native skill sync).

Runs on the aiwatch scan tick (and via ``aiwatch skills sync``): fetch the
assigned-skills manifest for this device user, diff it against local state,
and install/update/remove skill directories across the detected clients in
``SKILLS_DIR_MAP``.

Ownership model — the ``.installed`` marker is self-describing:

- Managed installs live in the shared canonical dir (``~/.agents/skills``)
  with per-client editor symlinks — same layout as ``runlayer skills add
  --global`` — but their marker contains ``managed:<skill_id>``, while user
  installs (``runlayer skills add``) write an empty marker. Ownership is
  read from disk, never inferred from lockfile absence, so a lost or corrupt
  managed lockfile cannot orphan installs or clobber user state.
- The managed lockfile (``~/.runlayer/managed-skill-lock.yml``, keyed by
  skill UUID, separate from the user lockfile) only caches identifiers for
  drift detection — the published identifier plus a disk-content hash that
  enforces managed content (local edits are restored to the published
  version every tick); dirs whose marker matches a manifest item are
  re-adopted (reinstalled) when the lockfile forgot them.
- Editor entries are symlinks into the canonical dir; when symlinking fails
  (Windows non-elevated users without Developer Mode) they fall back to full
  copies that inherit the ``managed:<skill_id>:<identifier>`` marker, so
  staleness and ownership stay detectable per entry.
- Anything not managed-marked is never removed or overwritten: user-local
  dirs, user-lockfile installs, planted symlinks/junctions (never followed),
  and real dirs/files sitting at an editor symlink path are all skipped +
  reported.
- ``user_resolved=False`` or any fetch error keeps state: reconcile-to-empty
  happens only on an affirmative empty manifest for a resolved user.

Concurrency note: a manual ``runlayer skills sync`` can overlap a packaged
scheduler tick. There is no cross-process lock; every step is idempotent and
a torn run converges on the next tick (the lockfile itself is written
atomically).

Import closure contract (enforced by ``tests/test_aiwatch_imports.py``):
httpx + yaml + pydantic + structlog + stdlib + the RE2 ``regex_safe``
wrapper only — no ``anyio``, no
``metrics_flush``.
"""

from __future__ import annotations

import os
import shutil
import tempfile
import time
from pathlib import Path

import httpx
import structlog
from pydantic import BaseModel

from runlayer_cli import regex_safe
from runlayer_cli.api import RunlayerClient
from runlayer_cli.models_api import (
    AssignedSkillManifestItem,
    AssignedSkillsManifest,
)
from runlayer_cli.skill_identifier import SkillFileInput, compute_skill_identifier
from runlayer_cli.skills.installer_core import (
    CANONICAL_BASE,
    SKILLS_DIR_MAP,
    _is_junction,
    _sanitize_name,
    _write_skill_files,
    link_or_copy_skill_dir,
    read_lock_entries,
    write_lock_entries,
)
from runlayer_cli.skills.marker import (
    INSTALLED_MARKER,
    MANAGED_MARKER_PREFIX,
    managed_marker,
    managed_marker_skill_id,
)

logger = structlog.get_logger(__name__)

MANAGED_LOCKFILE = "managed-skill-lock.yml"

# Stricter than installer_core._sanitize_name: matches the backend's install
# name normalization (backend/app/domains/skills/install_name.py), so nested
# paths, leading dots (incl. the reserved staging dir), and case-only
# variants (case-insensitive filesystems) can't come off the wire even from
# a hostile backend.
_MANAGED_INSTALL_NAME_RE = regex_safe.compile(r"^[a-z0-9][a-z0-9-]*$")

# Clients whose editor dir differs from the canonical dir need an install
# presence probe (dir exists in the home) before we drop a symlink; canonical
# clients (goose/opencode/vscode/zed) read straight from CANONICAL_BASE.
_SYMLINK_CLIENTS = {
    client: dirs[1]
    for client, dirs in SKILLS_DIR_MAP.items()
    if dirs[1] != CANONICAL_BASE
}


class ManagedLockEntry(BaseModel):
    """One managed skill install, keyed by skill UUID (``id``).

    ``identifier`` is the server's published content identifier (drift vs the
    manifest). ``disk_identifier`` is the hash of the files as actually
    written to disk (install-time frontmatter rewrites make it differ from
    ``identifier``); a tick-time recompute that doesn't match it means a
    local edit. ``None`` on pre-enforcement lockfiles = unverifiable, so the
    install is refreshed once and the hash backfilled.
    """

    id: str
    name: str
    identifier: str
    disk_identifier: str | None = None


class SyncReport(BaseModel):
    installed: list[str] = []
    updated: list[str] = []
    removed: list[str] = []
    # Managed installs whose content was locally edited and re-fetched back
    # to the published version (enforcement, not upstream drift).
    restored: list[str] = []
    up_to_date: list[str] = []
    skipped: list[str] = []
    errors: list[str] = []

    @property
    def changed(self) -> bool:
        return bool(self.installed or self.updated or self.removed or self.restored)


def managed_lockfile_path(home: Path) -> Path:
    return home / ".runlayer" / MANAGED_LOCKFILE


def read_managed_lockfile(path: Path) -> list[ManagedLockEntry]:
    return read_lock_entries(path, ManagedLockEntry)


def write_managed_lockfile(path: Path, entries: list[ManagedLockEntry]) -> None:
    write_lock_entries(
        path,
        sorted(entries, key=lambda e: e.id),
        header="aiwatch skills sync",
    )


def detect_sync_clients(home: Path) -> list[str]:
    """Symlink-clients present on this device (client config dir exists)."""
    detected: list[str] = []
    for client, editor_rel in _SYMLINK_CLIENTS.items():
        client_root = home / Path(editor_rel).parts[0]
        try:
            if client_root.is_dir():
                detected.append(client)
        except OSError:
            continue
    return detected


def _dedupe_by_install_name(
    items: list[AssignedSkillManifestItem], report: SyncReport
) -> list[AssignedSkillManifestItem]:
    """First skill by UUID wins an install_name; later ones are skipped."""
    winners: dict[str, AssignedSkillManifestItem] = {}
    for item in sorted(items, key=lambda i: i.skill_id):
        if item.install_name in winners:
            report.skipped.append(
                f"{item.name} ({item.skill_id}): install name "
                f"'{item.install_name}' already used by skill "
                f"{winners[item.install_name].skill_id}"
            )
            continue
        winners[item.install_name] = item
    # Preserve manifest order for the survivors.
    winner_ids = {i.skill_id for i in winners.values()}
    return [i for i in items if i.skill_id in winner_ids]


def _canonical_owner(skill_dir: Path) -> str | None:
    """Classify who owns the canonical path: ``"absent"``, ``"foreign"``, or
    the owning skill UUID for a device-sync install.

    ``foreign`` covers everything that is never ours to touch: user installs
    (empty marker), hand-made dirs (no marker), and planted symlinks or
    junctions (never followed — a junction's marker read would land in the
    target and rmtree could delete the target tree through it).
    """
    if skill_dir.is_symlink() or _is_junction(skill_dir):
        return "foreign"
    if not skill_dir.exists():
        return "absent"
    return managed_marker_skill_id(skill_dir) or "foreign"


def _rmtree_managed(path: Path) -> None:
    """``shutil.rmtree`` that keeps the managed marker alive across partial
    failure.

    On Windows, rmtree can delete the ``.installed`` marker before hitting a
    locked file and raising. A partially-deleted managed dir must keep its
    marker or later ticks classify it as user-owned and never retry the
    removal/refresh. The rewrite happens only after rmtree failed with the
    dir still present; the re-raise preserves the caller's error handling.
    """
    try:
        marker_text = (path / INSTALLED_MARKER).read_text(encoding="utf-8")
    except OSError:
        marker_text = None
    try:
        shutil.rmtree(path)
    except OSError:
        if marker_text is not None and path.is_dir():
            try:
                (path / INSTALLED_MARKER).write_text(marker_text, encoding="utf-8")
            except OSError:
                pass  # Best-effort; the original rmtree error is the story.
        raise


def _symlink_points_at(link: Path, target_dir: Path) -> bool:
    """Whether *link* (a symlink) points at *target_dir*.

    A symlink pointing anywhere else is a user's own link, not ours to
    replace or remove.
    """
    try:
        raw = os.readlink(link)
    except OSError:
        return False
    resolved = Path(raw) if os.path.isabs(raw) else link.parent / raw
    return os.path.normpath(resolved) == os.path.normpath(target_dir)


def _place_editor_symlink(
    canonical_dir: Path, editor_dir: Path, name: str, report: SyncReport
) -> None:
    """Create/refresh one editor entry, never clobbering real user content.

    Unlike ``installer_core._symlink_skill`` (interactive install, replace
    allowed), an unattended reconciler must not delete a real dir, file, or
    foreign symlink a user put at the entry path — unless the dir carries our
    ``managed:`` marker (a copy-mode entry from a prior run). When symlinking
    fails (Windows non-elevated users without Developer Mode), fall back to a
    full copy; remaining failure is reported, not raised — the canonical
    install already succeeded and canonical-dir clients keep working.
    """
    src = canonical_dir / name
    dest = editor_dir / name
    if src == dest:
        return
    rel = os.path.relpath(src, dest.parent)
    if dest.is_symlink():
        if not _symlink_points_at(dest, src):
            report.skipped.append(
                f"{name}: {dest} is a symlink to something else, leaving it"
            )
            return
        if os.readlink(dest) == rel:
            return
        dest.unlink()
    elif _is_junction(dest) or (
        # Junction first, and outside the exists() gate: a junction aimed at
        # the canonical dir would read the canonical marker here and get
        # rmtree'd below — deleting the canonical tree through it (pre-3.13
        # rmtree recurses into junctions) — while a *broken* junction has
        # exists() == False yet still occupies the name. Both are foreign.
        dest.exists() and managed_marker_skill_id(dest) is None
    ):
        report.skipped.append(
            f"{name}: {dest} exists and is not a managed symlink, leaving it"
        )
        return
    try:
        if dest.exists():
            # Our own copy-mode entry from a prior run: refresh it. Inside
            # the try — a locked file (Windows AV/open handle) is a report,
            # not an install-aborting error.
            _rmtree_managed(dest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        link_or_copy_skill_dir(src, dest)
    except OSError as e:
        report.skipped.append(f"{name}: could not link into {dest.parent}: {e}")


def _remove_managed_dir(
    canonical_dir: Path, editor_dirs: list[Path], name: str, report: SyncReport
) -> bool:
    """Remove a managed install (dir + editor symlinks). False when not ours.

    A foreign canonical path is not ours, and neither are editor symlinks
    pointing at it, so nothing is touched. Returns True only when something
    was removed.
    """
    skill_dir = canonical_dir / name
    if _canonical_owner(skill_dir) == "foreign":
        report.skipped.append(f"{name}: not a managed install, leaving it")
        return False
    removed_any = False
    editor_failures = 0
    # Editor entries first: the canonical marker is the only thing that lets
    # a future tick rediscover this install, so it must outlive any editor
    # removal that fails (e.g. a copy-mode entry held open by a Windows
    # file lock) or the copy would be orphaned forever.
    for editor_dir in editor_dirs:
        link = editor_dir / name
        if link.is_symlink():
            if _symlink_points_at(link, skill_dir):
                link.unlink()
                removed_any = True
            else:
                report.skipped.append(
                    f"{name}: {link} is a symlink to something else, leaving it"
                )
        elif link.exists():
            # Junction first: its marker read follows the reparse point, so a
            # junction aimed at the canonical dir reads the canonical marker
            # and would be rmtree'd — deleting the canonical tree through it
            # (pre-3.13 rmtree recurses into junctions). Foreign, leave it.
            if _is_junction(link) or managed_marker_skill_id(link) is None:
                report.skipped.append(
                    f"{name}: {link} exists and is not a managed symlink, leaving it"
                )
            else:
                # Copy-mode entry (symlink fallback) — ours to remove.
                try:
                    _rmtree_managed(link)
                    removed_any = True
                except OSError as e:
                    editor_failures += 1
                    report.errors.append(f"{name}: could not remove {link}: {e}")
    if editor_failures:
        # Don't report "removed" for a partial removal; the retained
        # canonical marker drives a retry on the next tick.
        return False
    if skill_dir.exists():
        _rmtree_managed(skill_dir)
        removed_any = True
    return removed_any


# Deterministic "content is broken/gone" hash result — see
# _compute_dir_identifier. Never equals a real merkle root (hex), so plain
# != comparison against a cached baseline classifies it as drift.
_UNHASHABLE_CONTENT = "unhashable-content"


def _compute_dir_identifier(skill_dir: Path) -> str | None:
    """Content hash of a skill dir's files on disk.

    ``None`` means strictly "could not read right now" (OSError: AV/editor
    file lock, permissions) — a transient state callers keep-state on and
    retry next tick. States that will NEVER become readable by waiting are
    content, not I/O: undecodable bytes, an emptied dir, or names the merkle
    rejects all return ``_UNHASHABLE_CONTENT``, a sentinel that can't equal
    any real merkle root, so the ordinary != comparison classifies them as
    drift and the restore fires. (Bonus: a legitimately zero-file skill
    hashes to the sentinel at install time too, so sentinel == sentinel keeps
    it stable instead of refreshing forever.)

    Same merkle as the server (``skill_identifier``, file set = every file's
    relative POSIX path + content), except the agent-added ``.installed``
    marker, which is not part of the published content. Computed on the exact
    bytes written to disk — install-time frontmatter rewrites mean this is
    NOT the manifest identifier; it only ever compares against a value
    produced by this same function (install-time vs tick-time).

    Deliberately runs for every managed skill on every tick: skills are
    KB-scale, so the hashing cost is noise next to the manifest fetch.
    """
    inputs: list[SkillFileInput] = []
    try:
        for root, dirs, file_names in os.walk(skill_dir):
            # Never follow planted symlinks or junctions into someone else's
            # tree. os.walk descends junctions even with followlinks=False, so
            # without the prune a junction target's content leaks into the
            # hash: it drifts every tick and the "restore" rmtree then runs
            # through the junction (pre-3.13 deletes the target tree).
            dirs[:] = [
                d
                for d in dirs
                if not (Path(root) / d).is_symlink()
                and not _is_junction(Path(root) / d)
            ]
            for file_name in sorted(file_names):
                path = Path(root) / file_name
                if path.is_symlink():
                    # File symlinks are foreign too (managed installs never
                    # contain links) — skipped here AND by copy placement
                    # (installer_core._links_and_junctions), so a clean copy
                    # hashes identical to its canonical dir.
                    continue
                rel = path.relative_to(skill_dir).as_posix()
                if rel == INSTALLED_MARKER:
                    continue
                try:
                    content = path.read_text(encoding="utf-8")
                except UnicodeDecodeError:
                    return _UNHASHABLE_CONTENT
                inputs.append(SkillFileInput(name=rel, content=content))
    except OSError:
        return None
    if not inputs:
        return _UNHASHABLE_CONTENT
    try:
        return compute_skill_identifier(inputs).root
    except ValueError:
        return _UNHASHABLE_CONTENT


def _install_managed_skill(
    client: RunlayerClient,
    item: AssignedSkillManifestItem,
    canonical_dir: Path,
    editor_dirs: list[Path],
    report: SyncReport,
    staging_root: Path,
    *,
    username: str | None,
    device_id: str | None,
) -> str | None:
    """Fetch + write one skill via a staging dir, then swap atomically.

    Every file title is validated before anything is written, the staged copy
    is ``managed:``-marked before it reaches the canonical path, and the final
    step is a rename — so no crash or exception at any point can leave a
    half-written dir that looks user-owned (which would be skipped forever) or
    a healthy-looking managed install with missing files.

    Returns the disk-content identifier of the staged files (the local-edit
    baseline cached in the managed lockfile).
    """
    skill_dir = canonical_dir / item.install_name
    content = client.get_assigned_skill_content(
        item.skill_id, username=username, device_id=device_id
    )
    for f in content.files:
        _sanitize_name(f.title)

    stage_dir = staging_root / item.install_name
    try:
        _write_skill_files(staging_root, item.install_name, list(content.files))
        # Marker carries the identifier so copy-mode editor entries (which
        # inherit it) can be detected as stale after a content update.
        (stage_dir / INSTALLED_MARKER).write_text(
            f"{MANAGED_MARKER_PREFIX}{item.skill_id}:{item.identifier}\n",
            encoding="utf-8",
        )
        # Hashed off the staged files so it reflects the exact bytes that
        # land on disk (post frontmatter-rewrite), marker excluded.
        disk_identifier = _compute_dir_identifier(stage_dir)
        # Authorized replace: callers only reach here for managed-marked or
        # absent targets. Remove-then-rename so files dropped from the skill
        # don't linger; a crash between the two leaves only a missing dir,
        # which is a plain fresh install next tick.
        if skill_dir.exists():
            _rmtree_managed(skill_dir)
        os.rename(stage_dir, skill_dir)
    except Exception:
        shutil.rmtree(stage_dir, ignore_errors=True)
        raise
    for editor_dir in editor_dirs:
        _place_editor_symlink(canonical_dir, editor_dir, item.install_name, report)
    return disk_identifier


_STAGING_BASE = ".managed-tmp"
# Staging entries younger than this are presumed to belong to a live
# concurrent reconcile (manual `aiwatch skills sync` overlapping the launchd
# tick) and are left alone; older ones are crashed-run leftovers.
_STAGING_MAX_AGE_SECONDS = 3600.0


def _make_staging_root(canonical_dir: Path) -> Path:
    """Per-run staging dir so concurrent reconciles can't tear each other's
    half-built installs out from under an in-flight rename."""
    root = Path(
        tempfile.mkdtemp(prefix="run-", dir=_ensure_staging_base(canonical_dir))
    )
    return root


def _ensure_staging_base(canonical_dir: Path) -> Path:
    base = canonical_dir / _STAGING_BASE
    base.mkdir(parents=True, exist_ok=True)
    return base


def _clear_stale_staging(canonical_dir: Path) -> None:
    """Drop crashed-run leftovers; recent entries may belong to a live run."""
    base = canonical_dir / _STAGING_BASE
    try:
        children = list(base.iterdir())
    except OSError:
        return
    now = time.time()
    for child in children:
        try:
            if now - child.stat().st_mtime > _STAGING_MAX_AGE_SECONDS:
                shutil.rmtree(child, ignore_errors=True)
        except OSError:
            continue


def fetch_assigned_skills(
    client: RunlayerClient,
    *,
    username: str | None = None,
    device_id: str | None = None,
) -> AssignedSkillsManifest | None:
    """The manifest, or ``None`` on any fetch failure (keep-state).

    ``ValueError`` covers both pydantic validation and ``json.JSONDecodeError``
    (captive portals returning HTML with status 200).
    """
    try:
        return client.get_assigned_skills(username=username, device_id=device_id)
    except (httpx.HTTPError, ValueError) as e:
        logger.debug("skill_sync_manifest_unavailable", error=str(e))
        return None


def _known_managed_names(
    entries: list[ManagedLockEntry], canonical_dir: Path
) -> dict[str, str]:
    """name -> skill_id for every managed install we can attribute.

    Union of the lockfile cache and on-disk ``managed:`` markers, so state
    survives a lost/corrupt lockfile.
    """
    known: dict[str, str] = {e.name: e.id for e in entries}
    try:
        children = list(canonical_dir.iterdir())
    except OSError:
        children = []
    for child in children:
        if child.is_symlink() or _is_junction(child):
            # A symlink or junction at the canonical path is never a managed
            # install; don't follow it into someone else's marker.
            continue
        skill_id = managed_marker_skill_id(child)
        if skill_id is not None:
            known[child.name] = skill_id
    return known


def reconcile_assigned_skills(
    client: RunlayerClient,
    manifest: AssignedSkillsManifest,
    *,
    home: Path | None = None,
    username: str | None = None,
    device_id: str | None = None,
) -> SyncReport:
    """Reconcile local managed installs against an already-fetched manifest.

    Removals (unassigned + renamed skills) run before installs so a skill
    recreated under a new UUID with the same install name converges in one
    tick. Per-skill failures are isolated; the managed lockfile is rewritten
    after every reconcile — including partial ones — so it always reflects
    what is actually on disk.
    """
    report = SyncReport()
    home = home or Path.home()
    canonical_dir = home / CANONICAL_BASE
    lockfile = managed_lockfile_path(home)

    if not manifest.user_resolved:
        logger.debug("skill_sync_user_unresolved_keep_state")
        return report

    lockfile_was_invalid = False
    try:
        entries = read_managed_lockfile(lockfile)
    except ValueError as e:
        # Ownership lives in the on-disk markers, so a corrupt lockfile only
        # loses the identifier cache: installs are re-adopted (reinstalled)
        # below and the lockfile is rebuilt at the end of this reconcile.
        logger.warning("skill_sync_lockfile_invalid", error=str(e))
        report.errors.append(f"managed lockfile unreadable, rebuilding: {e}")
        lockfile_was_invalid = True
        entries = []

    # Crashed-run staging leftovers are ours; a fresh per-run staging dir
    # keeps a concurrent reconcile from tearing this one's half-built installs
    # out from under an in-flight rename.
    _clear_stale_staging(canonical_dir)
    staging_root = _make_staging_root(canonical_dir)

    clients = detect_sync_clients(home)
    editor_dirs = [home / _SYMLINK_CLIENTS[client] for client in clients]
    entries_by_id = {e.id: e for e in entries}
    items = _dedupe_by_install_name(list(manifest.skills), report)
    items_by_id = {i.skill_id: i for i in items}
    target_names = {i.install_name for i in items}

    # Phase 1 — removals: every managed install (lockfile ∪ markers) whose
    # skill is no longer assigned goes first, so recreated skills (new UUID,
    # same name) converge in one tick. Renamed skills are NOT removed here —
    # the old install must survive until the new name actually lands (phase 2
    # cleans it up once the new name is installed or verified up_to_date), or
    # a blocked/failed new name would drop the skill entirely.
    known_managed = _known_managed_names(entries, canonical_dir)
    for name, skill_id in sorted(known_managed.items()):
        if skill_id in items_by_id or name in target_names:
            # Still assigned (same or new name), or the name is claimed by
            # another manifest item (phase-2 authorized managed replace).
            continue
        try:
            if _remove_managed_dir(canonical_dir, editor_dirs, name, report):
                report.removed.append(name)
        except Exception as e:
            logger.warning(
                "skill_sync_remove_failed", skill_id=skill_id, name=name, error=str(e)
            )
            report.errors.append(f"{name}: {e}")

    # Phase 2 — installs/updates.
    new_entries: dict[str, ManagedLockEntry] = {}
    for item in items:
        entry = entries_by_id.get(item.skill_id)
        try:
            if not _MANAGED_INSTALL_NAME_RE.match(item.install_name):
                raise ValueError(f"invalid managed install name: {item.install_name!r}")
            skill_dir = canonical_dir / item.install_name
            owner = _canonical_owner(skill_dir)

            if owner == "foreign":
                # User-owned (empty marker, none, or a planted symlink) —
                # never clobber, never adopt, never follow. Applies equally
                # when a user reclaimed a previously managed name.
                report.skipped.append(
                    f"{item.install_name}: local skill directory exists, "
                    "not overwriting"
                )
                # Keep the still-on-disk old install's entry, mirroring the
                # failure path below.
                if (
                    entry is not None
                    and _canonical_owner(canonical_dir / entry.name) == entry.id
                ):
                    new_entries[entry.id] = entry
                continue

            up_to_date = (
                owner == item.skill_id
                and entry is not None
                and entry.identifier == item.identifier
            )
            local_edit = False
            disk_identifier = entry.disk_identifier if entry is not None else None
            if up_to_date and entry is not None:  # entry check narrows the type
                # Enforce managed content: recompute the disk hash every tick
                # (deliberate — see _compute_dir_identifier) and restore on
                # any mismatch. Managed skills are not user-editable;
                # personal skills = private Runlayer skills or plain local
                # dirs. A None cached hash (pre-enforcement lockfile) is
                # unverifiable and refreshed like an adoption, not an edit.
                current_disk = _compute_dir_identifier(skill_dir)
                if entry.disk_identifier is not None and current_disk is None:
                    # Unreadable this tick (AV/editor file lock): a
                    # verification failure, not an edit. Restoring would
                    # thrash (and rmtree a possibly healthy install) —
                    # keep it, report, retry next tick.
                    report.errors.append(
                        f"{item.install_name}: managed content unreadable, "
                        "skipping verification until next sync"
                    )
                    new_entries[item.skill_id] = entry
                    continue
                if current_disk != entry.disk_identifier:
                    up_to_date = False
                    local_edit = entry.disk_identifier is not None
                elif entry.disk_identifier is None:
                    up_to_date = False
            if up_to_date:
                # Self-heal editor entries (e.g. a newly detected client, a
                # copy-mode entry whose refresh was blocked by a file lock on
                # a prior tick — its inherited marker then lags the canonical
                # one — or a locally edited copy, restored like a canonical
                # edit). A user's real dir (no managed marker) was reported
                # at install time and shouldn't re-report every tick.
                canonical_marker = managed_marker(skill_dir)
                copy_restored = False
                copy_verify_failed = False
                for editor_dir in editor_dirs:
                    dest = editor_dir / item.install_name
                    # Junction guard before the marker read and outside the
                    # exists() gate: a junction's marker reads through to its
                    # target, so it could look like a stale copy and get
                    # rmtree'd (which pre-3.13 can delete the target tree),
                    # and a *broken* junction has exists() == False, which
                    # would otherwise retry placement every tick. Foreign —
                    # never refresh, never re-report.
                    if _is_junction(dest):
                        continue
                    copy_marker = (
                        managed_marker(dest)
                        if not dest.is_symlink() and dest.exists()
                        else None
                    )
                    stale_copy = (
                        copy_marker is not None and copy_marker != canonical_marker
                    )
                    # Copy-mode content enforcement: a marker-current copy is
                    # byte-identical to the canonical install at placement
                    # (marker excluded from the hash), so its disk hash must
                    # equal the canonical install-time hash. A mismatch is a
                    # local edit of the copy — restore it from canonical. An
                    # unreadable copy (None hash) is a verification failure,
                    # not an edit: keep it, report, retry next tick.
                    edited_copy = False
                    if (
                        copy_marker is not None
                        and copy_marker == canonical_marker
                        and disk_identifier is not None
                    ):
                        copy_disk = _compute_dir_identifier(dest)
                        if copy_disk is None:
                            report.errors.append(
                                f"{item.install_name}: editor copy at {dest} "
                                "unreadable, skipping verification until "
                                "next sync"
                            )
                            copy_verify_failed = True
                            continue
                        edited_copy = copy_disk != disk_identifier
                    if (
                        dest.is_symlink()
                        or not dest.exists()
                        or stale_copy
                        or edited_copy
                    ):
                        _place_editor_symlink(
                            canonical_dir, editor_dir, item.install_name, report
                        )
                        if edited_copy:
                            copy_restored = True
                if copy_restored:
                    report.restored.append(item.install_name)
                elif copy_verify_failed:
                    # Mirrors the canonical OSError classification: the error
                    # is recorded and the skill lands in no bucket — calling
                    # it up_to_date would contradict the unverified copy.
                    pass
                else:
                    report.up_to_date.append(item.install_name)
            else:
                # Fresh install, identifier drift, local-edit restore,
                # marker-only adoption (lockfile lost), or managed rename
                # takeover — all one authorized fetch-and-replace.
                disk_identifier = _install_managed_skill(
                    client,
                    item,
                    canonical_dir,
                    editor_dirs,
                    report,
                    staging_root,
                    username=username,
                    device_id=device_id,
                )
                if entry is None and owner == "absent":
                    report.installed.append(item.install_name)
                elif local_edit:
                    report.restored.append(item.install_name)
                else:
                    report.updated.append(item.install_name)

            # Recorded before rename cleanup: the install under the new name
            # is already the authoritative one, so a blocked cleanup below
            # must not discard its entry (or the next tick would verify the
            # new dir against the old name's disk hash and "restore" it).
            new_entries[item.skill_id] = ManagedLockEntry(
                id=item.skill_id,
                name=item.install_name,
                identifier=item.identifier,
                disk_identifier=disk_identifier,
            )

            # Rename cleanup, only after the new name is confirmed present
            # (freshly installed OR verified up_to_date): drop this skill's
            # installs under any previous name (marker-verified). Running on
            # up-to-date ticks too lets a cleanup that a locked file blocked
            # once retry later instead of leaving the old install forever.
            for old_name, sid in sorted(known_managed.items()):
                if sid != item.skill_id or old_name == item.install_name:
                    continue
                if _canonical_owner(canonical_dir / old_name) != item.skill_id:
                    continue
                if _remove_managed_dir(canonical_dir, editor_dirs, old_name, report):
                    report.removed.append(old_name)
        except Exception as e:
            logger.warning(
                "skill_sync_item_failed",
                skill_id=item.skill_id,
                install_name=item.install_name,
                error=str(e),
            )
            report.errors.append(f"{item.install_name}: {e}")
            if (
                entry is not None
                and entry.id not in new_entries
                and _canonical_owner(canonical_dir / entry.name) == entry.id
            ):
                # The previous install (same or old name) is still on disk
                # and nothing newer was recorded this tick: keep its entry so
                # a failed update/rename doesn't orphan it.
                new_entries[entry.id] = entry

    shutil.rmtree(staging_root, ignore_errors=True)

    final_entries = sorted(new_entries.values(), key=lambda e: e.id)
    if lockfile_was_invalid or final_entries != sorted(entries, key=lambda e: e.id):
        try:
            write_managed_lockfile(lockfile, final_entries)
        except OSError as e:
            logger.warning("skill_sync_lockfile_write_failed", error=str(e))
            report.errors.append(f"managed lockfile write failed: {e}")

    return report


def sync_assigned_skills(
    client: RunlayerClient,
    *,
    home: Path | None = None,
    username: str | None = None,
    device_id: str | None = None,
) -> SyncReport | None:
    """Fetch + reconcile. ``None`` means keep-state (fetch failed/unresolved).

    Never raises on backend/network failure — under launchd this must stay a
    silent no-op so a backend blip can't fail the scan tick.
    """
    manifest = fetch_assigned_skills(client, username=username, device_id=device_id)
    if manifest is None or not manifest.user_resolved:
        # Both are keep-state to callers: an unresolved identity must surface
        # as "skipped", not as a successful zero-change sync.
        return None
    return reconcile_assigned_skills(
        client, manifest, home=home, username=username, device_id=device_id
    )
