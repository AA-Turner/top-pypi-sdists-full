"""THE walk: Tier 1 facts for every file under the folder, pruning skip rules, worktree copies and links that leave it, and what it could not see."""

from __future__ import annotations
import os
import re
from collections.abc import Iterator
from dataclasses import dataclass, field
from pathlib import Path
from .skip_rules import (
    SKIP_DIRS,
    SKIP_FILES,
    SKIP_SUFFIXES,
    RESEARCH_DOT_DIR_SKIPS,
    hidden_admitted)
from probe.cli.imports.folder.walk.evidence import FileEvidence, tier_for


@dataclass
class WalkWarnings:
    """What one traversal could NOT see. Filled in as `walk` iterates.

    A generator cannot return this: the caller is consuming files lazily and
    the last directory is not read until the last file is yielded. So the
    caller owns the collector, hands it in, and reads it after the loop.

    Everything here is the same failure: the folder is bigger than what was
    counted, and saying nothing turns that into a partial import reported as a
    complete one. `linked` was already handled; `unreadable` is the same bug
    arriving through permissions instead of symlinks.
    """

    #: (link, target) for symlinked directories pointing OUTSIDE the root.
    #: Not followed -- a link can point at its own parent or at somebody else's
    #: dataset. Links resolving inside the root are walked by their real path
    #: and are deliberately not listed: crying wolf on `latest -> runs/2024-05`
    #: is how the one real cross-drive link stops being read.
    linked: list[tuple[str, str]] = field(default_factory=list)
    #: Directories that could not be listed at all -- permissions, a dead
    #: mount, a race with a delete. Everything beneath them is missing from
    #: both the count and the evidence.
    unreadable: list[str] = field(default_factory=list)
    #: The ROOT itself could not be read. Distinct from "the root is empty",
    #: and the difference is the whole point: one means there is nothing to
    #: import, the other means we could not look.
    root_unreadable: bool = False
    #: Hidden folders skipped by policy (`backfill.RESEARCH_DOT_DIRS`), each
    #: with the files under it. Not a blind spot like the two above -- the walk
    #: went in and counted -- but the same duty: what is left out is said.
    skipped_hidden: list["SkippedFolder"] = field(default_factory=list)
    #: Nested git worktrees of a repo whose main checkout is under the root:
    #: copies, counted and skipped. See `worktree_copy`.
    skipped_worktrees: list["SkippedFolder"] = field(default_factory=list)

    def sort(self) -> None:
        """Stable order, so two runs over one drive show the same list."""
        self.linked.sort()
        self.unreadable.sort()
        self.skipped_hidden.sort(key=lambda f: f.path)
        self.skipped_worktrees.sort(key=lambda f: f.path)


@dataclass
class SkippedFolder:
    """One folder the walk counted but did not import, and its file count.

    Counted by the walk's own rules -- SKIP_DIRS pruned, SKIP_FILES not counted
    -- so its number is comparable with the import's own."""

    path: str
    files: int = 0

    def pair(self) -> tuple[str, int]:
        return (self.path, self.files)


def worktree_copy(directory: str, entries, resolved_root: str, include=frozenset()) -> bool:
    """True when `directory` is a git worktree of a repo this import already carries.

    A linked worktree's `.git` is a FILE reading `gitdir: <main>/.git/worktrees/<name>`.
    When `<main>` -- the main working tree -- is inside the import root and is
    itself imported, this directory is a second checkout of that repo:
    7 Claude Code agent worktrees under `.claude/worktrees/` were 65,491 of one
    customer's 78,628 uploaded files. Any tool's worktrees look the same
    (Claude Code, Codex, Conductor, gstack), dot-folder or not.

    NOT a copy, so walked as before:
    - a SUBMODULE (its `gitdir:` points into `.git/modules/`, and its files
      exist nowhere else);
    - a worktree whose main checkout is OUTSIDE the root (it is then the only
      copy being imported), or inside it but skipped itself -- under a hidden
      folder the walk does not admit (`include` is `--include-hidden`) or a
      SKIP_DIRS one -- since then no checkout of the repo would be imported;
    - a worktree of a BARE repo (`core.bare = true`, which a bare clone into
      `proj/.git` also says): there is no main working tree carrying the files;
    - anything whose `gitdir:` or main checkout does not resolve to a
      directory on disk.
    Paths are resolved -- a relative `gitdir:` and symlinks both -- before they
    are compared. The caller never asks about the root itself.

    `entries` is the directory's own listing, already read by the walk, so a
    folder without a `.git` costs nothing here.
    """
    marker = next((e for e in entries if e.name == ".git"), None)
    if marker is None:
        return False
    try:
        if not marker.is_file():  # a `.git` DIRECTORY is a main checkout or a clone
            return False
        with open(marker.path, encoding="utf-8", errors="replace") as fh:
            head = fh.read(4096)
    except OSError:
        return False
    target = next((line.split(":", 1)[1].strip() for line in head.splitlines()
                   if line.startswith("gitdir:")), "")
    if not target:
        return False
    gitdir = Path(os.path.realpath(os.path.join(directory, target)))
    if gitdir.parent.name != "worktrees" or not gitdir.is_dir():
        return False
    common = gitdir.parent.parent  # <main>/.git
    if common.name != ".git" or _bare(common):
        return False  # a bare repo's worktree, or one under `.git/modules/`
    main = common.parent
    here = Path(os.path.realpath(directory))
    root = Path(resolved_root)
    if main == here or not main.is_dir():
        return False
    if main == root:
        return True
    if root not in main.parents:
        return False
    return all(
        part not in SKIP_DIRS and (not part.startswith(".") or hidden_admitted(part, include))
        for part in main.relative_to(root).parts
    )


def _bare(common: Path) -> bool:
    """Whether the repo whose git dir is `common` says `core.bare = true`."""
    try:
        with open(common / "config", encoding="utf-8", errors="replace") as fh:
            config = fh.read(65536)
    except OSError:
        return False
    return re.search(r"(?im)^\s*bare\s*=\s*true\s*$", config) is not None


def skipped_by_hidden_rule(folders, include=frozenset(), *, root_name: str = "") -> bool:
    """Whether these root-relative folders (a file's, outermost first) put it
    under a hidden folder `walk` skips -- the same test `walk` applies to each
    folder it enters, decided from the path alone, so it holds for a folder
    that is gone from disk (`backfill_coverage.Coverage.observe`). `root_name`
    is the import folder's own name, the parent `walk` sees for a top-level
    folder (`.dvc/cache` when the import IS `.dvc`)."""
    parts = tuple(folders)
    return any(
        (part.startswith(".") and not hidden_admitted(part, include))
        or part in RESEARCH_DOT_DIR_SKIPS.get(parts[index - 1] if index else root_name, ())
        for index, part in enumerate(parts)
    )


def _rel_to(root: Path, path: str) -> str:
    """`path` relative to `root`, falling back to the absolute path.

    Every entry in `WalkWarnings` goes through here so the report never mixes
    bare basenames with root-relative paths -- a reader who cannot locate what
    was skipped cannot act on it.
    """
    try:
        return str(Path(path).relative_to(root))
    except ValueError:  # pragma: no cover - entries are always under root
        return path


def walk(
    root: Path, warn: WalkWarnings | None = None, *, include_hidden=(), legacy: bool = False
) -> Iterator[FileEvidence]:
    """Tier 1 for every file under `root`, pruning SKIP_DIRS. THE only walk.

    This is the single traversal of the folder. The census (count and bytes),
    the mtime clusters and the sample all come from what this yields -- there
    used to be a second walker in `backfill.scan` computing the count over
    provably the same file set, so a large folder was read end to end twice
    before the agent started.

    A GENERATOR, and not for memory: the caller materialises the records
    anyway, because whether they are needed is only known after the count.
    It yields so the CALLER's loop can drive the progress line. A function that
    returns a list is gone for the whole traversal and can only report progress
    through a callback handed down into it, which is a terminal inside a
    filesystem module. This keeps the module knowing nothing about screens.

    `os.scandir`, not `os.walk`: `os.walk` calls scandir internally, throws the
    `DirEntry` away, and hands back bare names -- so every file was re-stat'd
    by full path, resolving each path component again. `DirEntry.stat` uses the
    open directory, and `is_dir`/`is_symlink` come off the dirent for free.

    Symlink semantics match `os.walk` exactly, deliberately: a symlinked
    directory is NOT descended into (see `WalkWarnings.linked`) while a
    symlinked FILE is counted like any other file.

    SKIPPED, BUT COUNTED: a hidden folder the policy does not admit
    (`backfill.hidden_admitted`; `include_hidden` adds names) and a nested
    worktree copy (`worktree_copy`) are still walked, without yielding, and
    their files tallied into `warn.skipped_hidden` / `warn.skipped_worktrees`.
    A worktree found inside a skipped hidden folder is counted as a worktree.
    Inside a skipped folder nothing is reported as linked or unreadable: it is
    not being imported, so it cannot make the import incomplete.

    `legacy` walks by the rules before those two skips (`Census.walk_rules`
    0): the closing re-walk of an import a previous CLI approved must see the
    files it approved, or they read as deleted and the job never finishes.
    """
    root = Path(root).resolve()
    warn = warn if warn is not None else WalkWarnings()
    include = frozenset(include_hidden or ())
    resolved_root = str(root)
    #: (directory, the skipped folder it counts toward or None, whether that
    #: folder is a hidden one first seen here and not yet registered).
    stack: list[tuple[str, SkippedFolder | None, bool]] = [(str(root), None, False)]
    first = True

    while stack:
        here, bucket, unregistered = stack.pop()
        try:
            entries = list(os.scandir(here))
        except FileNotFoundError:
            # VANISHED, not unreadable, and the difference is the whole advice.
            # A training job cleaning up temp directories during a walk over a
            # live drive is ordinary; telling its owner to "check permissions"
            # on a directory that no longer exists sends them after nothing.
            # Nothing under it was ever counted, so there is no shortfall to
            # explain either -- this is the one skip that stays quiet.
            first = False
            continue
        except OSError:
            # NAMED, not swallowed. `os.walk(onerror=lambda _: None)` dropped
            # these silently, so a dataset directory the process could not open
            # read as a directory with nothing in it -- and the census agreed,
            # which made the reconcile confirm the wrong denominator.
            if first:
                # EXISTS but cannot be listed -- permissions, a dead mount.
                # A path that is simply not there is a different answer and
                # the caller already has it (`run` checks `is_dir` before it
                # gets here); calling that "unreadable" would turn a typo into
                # a permissions scare.
                warn.root_unreadable = os.path.isdir(here)
            elif bucket is None:
                warn.unreadable.append(_rel_to(root, here))
            first = False
            continue
        if not first and not legacy and worktree_copy(here, entries, resolved_root, include):
            # Checked on the directory's OWN listing, so a folder with no `.git`
            # costs nothing; and checked in skipped folders too, so the agent
            # worktrees under `.claude/worktrees/` are named as the copies they
            # are rather than folded into `.claude`.
            bucket = SkippedFolder(_rel_to(root, here))
            warn.skipped_worktrees.append(bucket)
        elif unregistered:
            warn.skipped_hidden.append(bucket)
        first = False

        for entry in entries:
            name = entry.name
            # Hidden FILES are not skipped: `.condarc` and `.gitignore` are
            # files someone wrote. Hidden FOLDERS are, below, unless admitted.
            try:
                is_dir = entry.is_dir()  # FOLLOWS links, exactly as os.walk does
            except OSError:
                is_dir = False
            if is_dir:
                if name in SKIP_DIRS:
                    continue
                try:
                    if entry.is_symlink():
                        if bucket is None:
                            _record_link(warn, root, resolved_root, entry)
                        continue  # recorded, still not followed
                except OSError:
                    # ROOT-RELATIVE, like every other entry in this list. A
                    # bare `locked` for `datasets/2024/locked/` is a name the
                    # reader cannot find, and being findable is the entire
                    # point of naming it.
                    if bucket is None:
                        warn.unreadable.append(_rel_to(root, entry.path))
                    continue
                if bucket is None and not legacy and (
                    (name.startswith(".") and not hidden_admitted(name, include))
                    or name in RESEARCH_DOT_DIR_SKIPS.get(os.path.basename(here), ())
                ):
                    stack.append((entry.path, SkippedFolder(_rel_to(root, entry.path)), True))
                    continue
                stack.append((entry.path, bucket, False))
                continue
            if name in SKIP_FILES or Path(name).suffix.lower() in SKIP_SUFFIXES:
                continue
            if bucket is not None:
                bucket.files += 1
                continue
            size, mtime = _entry_stat(entry)
            yield FileEvidence(
                path=entry.path, size=size, mtime=mtime, tier=tier_for(name, size)
            )

    # A hidden folder that held nothing but worktree copies (`.claude` around
    # `.claude/worktrees/`), or nothing at all, skipped no file of its own.
    warn.skipped_hidden[:] = [folder for folder in warn.skipped_hidden if folder.files]
    warn.sort()


def _raw_stat(entry):
    """`entry.stat()`, indirected so a test can make one file fail.

    `os.DirEntry` is a C type and cannot be monkeypatched, and an unstattable
    file is not portable to create. Everything real still goes through the
    dirent -- this adds a name, not a behaviour.
    """
    return entry.stat()


def _entry_stat(entry) -> tuple[int, float]:
    """Size and mtime off the dirent, or zeros when the file cannot be stat'd.

    A broken symlink, or a race with a training job deleting a checkpoint. The
    file still COUNTS -- an evidence list that quietly skipped it would not
    reconcile against the number the reader was shown.
    """
    try:
        st = _raw_stat(entry)
        return st.st_size, st.st_mtime
    except OSError:
        return 0, 0.0


def _record_link(warn: WalkWarnings, root: Path, resolved_root: str, entry) -> None:
    """Note a symlinked directory, but only when it leaves the folder.

    A link resolving back inside `root` is walked by its real path anyway, so
    warning about it is noise on the ordinary case -- and noise on the ordinary
    case is how the one real cross-drive link stops being read.
    """
    rel = _rel_to(root, entry.path)
    try:
        target = Path(entry.path).resolve()
    except OSError:
        # An unresolvable link is exactly the interesting kind -- a dead mount,
        # a path this host cannot see -- so it is recorded rather than dropped.
        warn.linked.append((rel, "(unresolvable)"))
        return
    if str(target) == resolved_root or resolved_root in (str(p) for p in target.parents):
        return
    warn.linked.append((rel, str(target)))
