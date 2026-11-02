"""record what a walk saw: observe in batches with verified hashes, the rows, and the files a skip rule left out."""

from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
import os
from pathlib import Path, PurePath

from probe.foundation.compat.compat import StrEnum

#: Files hashed per commit, and the longest a batch may stay uncommitted. The
#: census used to be ONE transaction over the whole folder, so a crash at file
#: 190,000 of 200,000 rolled back every hash it had paid for.
OBSERVE_BATCH_FILES = 1_000
OBSERVE_BATCH_SECONDS = 5.0

#: Hashing threads. `hashlib` releases the GIL on the 1 MB chunks `hash_current`
#: already reads, so these genuinely run in parallel; the ceiling is the disk,
#: not the interpreter. SQLite is never touched from them -- see `observe`.
OBSERVE_HASH_WORKERS = 4


class SkipRule(StrEnum):
    """Why a file this store saw before is no longer walked: `files.skipped`.

    The walk's rules changed under existing stores (CLI 0.328.0): hidden
    folders and nested worktree copies are now counted and skipped
    (`backfill.RESEARCH_DOT_DIRS`, `backfill_evidence.worktree_copy`). A file an
    older CLI imported from one of them is still on disk, so calling it
    `vanished` was false -- and `vanished` held its project's draft
    until the file came back, which a skipped file never does. 65,491 such
    files for one customer.

    The rule stays on the row while the file is unseen, including after the
    file is deleted (an agent's worktree is removed when the agent finishes):
    then it is absent, as any deleted file is, but still out of the import, so
    it holds nothing either (`files.skipped_on_disk` tells the two apart).
    """

    #: Under a hidden folder the walk does not admit.
    HIDDEN_FOLDER = "hidden_folder"
    #: Under a git worktree of a repo the import already carries.
    WORKTREE_COPY = "worktree_copy"


@dataclass(frozen=True)
class WalkSkips:
    """What one walk left out by rule, as `Coverage.observe` takes it.

    `worktrees` and `hidden` are the root-relative folders the walk counted
    and skipped. `hidden_rule` says whether a path's folders put it under a
    hidden folder the walk skips, so a file is placed by the rule even when its
    folder is gone from disk -- a worktree under `.claude/worktrees/` removed
    before this CLI ever walked the folder. `legacy` is a walk by the rules
    before the skips (`Census.walk_rules` 0): it imports everything, so no
    rule leaves anything out.
    """

    worktrees: tuple[str, ...] = ()
    hidden: tuple[str, ...] = ()
    hidden_rule: Callable[[tuple[str, ...]], bool] | None = None
    legacy: bool = False



def skipped_folders(source, *, census=None, root_name: str = "") -> WalkSkips:
    """What a walk left out by rule, from its `backfill_evidence.WalkWarnings`
    or its `backfill.Census` (a queued job's comes back from JSON with lists
    for tuples). `census` is the import's, whose admissions
    (`include_hidden`) and rules (`walk_rules`) the walk ran by; `source`
    itself when it is the census. `root_name` is the folder's own name, which
    the walk consults for its top-level entries (a root named `.dvc`)."""
    from ..walk.walk import skipped_by_hidden_rule

    def paths(items):
        return tuple(item.path if hasattr(item, "path") else item[0] for item in items or ())

    census = source if census is None else census
    if getattr(census, "walk_rules", 0) < 1:
        return WalkSkips(legacy=True)
    include = frozenset(getattr(census, "include_hidden", ()) or ())
    return WalkSkips(
        worktrees=paths(getattr(source, "skipped_worktrees", ())),
        hidden=paths(getattr(source, "skipped_hidden", ())),
        hidden_rule=lambda parts: skipped_by_hidden_rule(parts, include, root_name=root_name),
    )


def _skip_rules(root: Path, unseen: dict[str, str | None],
                skipped: WalkSkips | None) -> dict[str, tuple[SkipRule, bool]]:
    """Which unseen files a rule leaves out, and whether each is on disk.

    path -> (rule, on disk), for `unseen` (path -> the rule recorded before,
    or None). The nearest skipped folder decides, so the agent worktrees inside
    `.claude` are worktree copies, not hidden files. In order: a worktree this
    walk skipped; a worktree copy recorded before whose folder is gone (a
    removed worktree is not listed any more, though `.claude` around it may
    be; a folder still there is walked, so its files are the import's again);
    a hidden folder this walk skipped; else, from its path alone, a hidden
    folder this walk's rules skip (`--include-hidden` admits one again).

    Without `skipped`, or for a `legacy` walk (a queued job resumed under the
    rules before the skips, which say nothing about them), the rules recorded
    before stand and none is added.

    A stat per file, never a read: out of the import, its bytes are not the
    store's business any more. `lexists`, because the walk counts a broken
    symlink as a file too.
    """
    keep_only = skipped is None or skipped.legacy
    folders: dict[str, SkipRule] = {}
    if not keep_only:
        for rule, items in ((SkipRule.HIDDEN_FOLDER, skipped.hidden),
                            (SkipRule.WORKTREE_COPY, skipped.worktrees)):  # a worktree wins a tie
            for folder in items:
                folders[str(PurePath(folder))] = rule
    gone_folders: dict[PurePath, bool] = {}

    def folder_gone(folder: PurePath) -> bool:
        if folder not in gone_folders:
            gone_folders[folder] = not os.path.isdir(root / folder)
        return gone_folders[folder]

    out: dict[str, tuple[SkipRule, bool]] = {}
    for path, before in unseen.items():
        known = SkipRule(before) if before in SkipRule._value2member_map_ else None
        pure = PurePath(path)
        if keep_only:
            rule = known
        else:
            rule = next((folders[str(parent)] for parent in pure.parents
                         if str(parent) in folders), None)
            if (known is SkipRule.WORKTREE_COPY and rule is not SkipRule.WORKTREE_COPY
                    and folder_gone(pure.parent)):
                rule = known
            if rule is None and skipped.hidden_rule is not None \
                    and skipped.hidden_rule(pure.parent.parts):
                rule = SkipRule.HIDDEN_FOLDER
        if rule is not None:
            out[path] = (rule, os.path.lexists(root / path))
    return out
