"""the walk's census (the denominator) and its printed reconcile against what landed."""

from __future__ import annotations
from dataclasses import dataclass


#: How many skipped folders of each kind a structured summary lists by name.
#: The counts cover all of them; the list is for reading.
SKIPPED_LISTED = 50


@dataclass(frozen=True)
class Census:
    """What the deterministic walk found. The denominator.

    Produced by folding :func:`probe.cli.imports.folder.walk.walk.walk`, which is now
    the only traversal in the flow. There used to be a second walker here --
    `scan` -- computing these two integers over provably the same file set,
    so a large folder was read end to end twice before the agent started.

    There is no `capped` any more. It existed for the folder picker, which
    wanted a bounded count so the cursor could move; the picker no longer
    counts at all, and the import was always uncapped. Its only lasting effect
    was a branch in `reconcile` that suppressed the shortfall warning -- a
    safety net that switched itself off at exactly the size that needed it.
    """

    files: int
    bytes: int
    #: Symlinked directories the walk declined to follow.
    #:
    #: NOT followed, and that is the right call -- a symlink can point at its
    #: own parent (an unbounded walk) or, on a shared drive, at somebody else's
    #: dataset, which an import would then file under this project. What was
    #: wrong is that it happened SILENTLY: the census reported the smaller
    #: number, the reconcile agreed with it, and a folder reachable through a
    #: link was simply absent with nothing to say so. That is the "silent 2%
    #: coverage that reads as done" this module exists to make impossible.
    #: Sorted, so two runs over the same drive show the same list -- the gate
    #: prints only the first few, and a reviewer who cannot reproduce what they
    #: were shown cannot act on it. Each entry is (link, target): the advice is
    #: "import what it points at", which is unusable without the target.
    linked_dirs: tuple[tuple[str, str], ...] = ()
    #: Directories the walk could not list at all. The SAME failure as
    #: `linked_dirs`, arriving through permissions instead of symlinks:
    #: everything beneath them is missing from this count and from the
    #: evidence, and it used to happen without a word.
    unreadable_dirs: tuple[str, ...] = ()
    #: Hidden folders the policy skipped (RESEARCH_DOT_DIRS), as
    #: (root-relative path, files under it). COUNTED, not merely pruned: the
    #: files are on disk and out of the import by a rule, and the plan says so
    #: -- a denominator that silently shrank is the bug the hidden-folder
    #: comment above describes. Not part of `files`, which is what the import
    #: places and reconciles against, so a policy skip never reads as partial.
    skipped_hidden: tuple[tuple[str, int], ...] = ()
    #: Nested git worktrees whose main working tree is also under the root --
    #: copies of a repo this import already carries -- as (path, files).
    skipped_worktrees: tuple[tuple[str, int], ...] = ()
    #: The `--include-hidden` names this walk admitted. Kept with the census
    #: because the census travels with a queued import: the closing re-walk
    #: must admit the same folders or their files would read as deleted.
    include_hidden: tuple[str, ...] = ()
    #: Which rules the walk ran by (`WALK_RULES`); 0 for a census an older CLI
    #: saved, which the closing re-walk must repeat (`backfill_evidence.walk`).
    walk_rules: int = 0

    @property
    def incomplete(self) -> bool:
        """True when the walk is known to have missed part of the folder."""
        return bool(self.linked_dirs or self.unreadable_dirs)

    @property
    def skipped_hidden_files(self) -> int:
        return sum(n for _, n in self.skipped_hidden)

    @property
    def skipped_worktree_files(self) -> int:
        return sum(n for _, n in self.skipped_worktrees)

    @property
    def on_disk(self) -> int:
        """Every file the walk saw: the ones it places plus the ones it skipped
        by rule. The figure the skips are measured against."""
        return self.files + self.skipped_hidden_files + self.skipped_worktree_files

    def skipped_json(self) -> dict:
        """The skips as structured fields (the desktop's job record, and the
        same numbers `backfill.scanned` carries). Additive and bounded: the
        lists stop at SKIPPED_LISTED entries, the counts never do."""
        def rows(items):
            ordered = sorted(items, key=lambda item: (-item[1], item[0]))
            return [{"path": path, "files": n} for path, n in ordered[:SKIPPED_LISTED]]

        return {
            "hiddenFolders": rows(self.skipped_hidden),
            "hiddenFolderCount": len(self.skipped_hidden),
            "hiddenFiles": self.skipped_hidden_files,
            "worktrees": rows(self.skipped_worktrees),
            "worktreeCount": len(self.skipped_worktrees),
            "worktreeFiles": self.skipped_worktree_files,
            "includedHidden": list(self.include_hidden),
        }

    def describe(self) -> str:
        noun = "file" if self.files == 1 else "files"
        line = f"{self.files:,} {noun}   {human_bytes(self.bytes)}"
        skipped = self.skipped_hidden_files + self.skipped_worktree_files
        if skipped:
            line += f"   ({skipped:,} more skipped: hidden folders and worktree copies)"
        if self.linked_dirs:
            n = len(self.linked_dirs)
            line += f"   ({n} linked director{'y' if n == 1 else 'ies'} not followed)"
        if self.unreadable_dirs:
            n = len(self.unreadable_dirs)
            line += f"   ({n} director{'y' if n == 1 else 'ies'} unreadable)"
        return line


def human_bytes(n: int) -> str:
    size = float(n)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.0f} {unit}" if unit == "B" else f"{size:.1f} {unit}"
        size /= 1024
    return f"{size:.1f} TB"  # pragma: no cover - loop always returns


def reconcile(census: Census, landed: int, at_least: bool) -> list[str]:
    """The denominator, printed. The whole point of enumerating first."""
    found = f"{census.files:,}"
    if landed < 0:
        return [f"{found} files found — could not read back the project to confirm what landed."]
    shown = f"{landed:,}{'+' if at_least else ''}"
    lines = [f"{found} files found on disk · {shown} artifacts now on the project."]
    # UNCONDITIONAL now, bar the one honest exclusion. `census.capped` used to
    # gate this too, which meant the shortfall warning switched itself off on
    # exactly the folders big enough to need it. The census is never capped.
    if not at_least and landed < census.files:
        lines.append(
            f"{census.files - landed:,} unaccounted for — build noise and caches are "
            "expected here; re-run to pick up anything genuinely missed."
        )
    return lines
