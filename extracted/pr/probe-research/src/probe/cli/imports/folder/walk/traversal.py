"""the one traversal into census, records and index, and the lines saying what it could not see, skipped by rule, or refused."""

from __future__ import annotations
from pathlib import Path

from ... import folder as bf
from probe.cli.imports.folder import evidence as evidence_mod
from . import index as index_mod


#: How often the walk repaints its counter. Every file would be a syscall per
#: file on top of the stat; every 2,000 is imperceptible to a reader and free.
PROGRESS_EVERY = 2_000

#: How many linked/unreadable directories the warning names before summarising.
#: A reviewer who cannot reproduce what they were shown cannot act on it, so
#: the list is sorted and the remainder is counted rather than dropped.
WARN_SHOWN = 5


def _index(
    folder: Path, report: "Report", *, include_hidden: tuple[str, ...] = ()
) -> tuple[bf.Census, list, evidence_mod.WalkWarnings, "index_mod.Index", list]:
    """THE walk. One traversal → census, records, and what it could not see.

    Everything downstream reads these records; nothing walks the folder again.
    Sampling and clustering are NOT done here -- see `evidence.enrich`, which
    the early exits below must be able to skip.

    The counter is painted by THIS loop rather than by a callback handed into
    `walk`, which is what keeps `backfill_evidence` free of any terminal. On a
    research drive this loop runs for minutes; before it existed the screen
    showed the previous menu the whole time and read as a hung program.
    """
    from probe.cli.wizard import terminal as tui

    warn = evidence_mod.WalkWarnings()
    records: list = []
    count = total = 0

    # THE CALLER GUARDS, not the Board. `Board.open()` writes absolute cursor
    # escapes unconditionally -- piped into a log that is a screenful of
    # garbage. Same shape as the unit board below.
    board = None
    if tui.interactive():
        # EMPTY label, not "counting …". A Board label is a permanent row
        # PREFIX -- `update` renders `f"{label:<width}{text}"` -- so a
        # placeholder-looking label is never replaced, it is glued to every
        # repaint: `counting …12,000 files · 4.2 GB`. In `run_units` the labels
        # are project names, which is what the field is for.
        board = tui.Board(f"Reading {folder}", [""])
        board.open()
    # WRITTEN DOWN ON THE WAY PAST. `Index.write` is a generator that yields
    # what it was given, so this loop is unchanged and the walk is not paid
    # for twice. The previous index is still on disk and still readable at
    # this point -- the diff below reads it BEFORE the new one replaces it.
    index = index_mod.Index.for_folder(folder)
    previous = index.read()
    try:
        for f in index.collect(
            evidence_mod.walk(folder, warn, include_hidden=include_hidden), root=folder
        ):
            records.append(f)
            count += 1
            total += f.size
            if board is not None and count % PROGRESS_EVERY == 0:
                board.update(0, f"{count:,} files · {bf.human_bytes(total)}")
        if board is not None:
            board.update(0, f"{count:,} files · {bf.human_bytes(total)}")
    finally:
        # In a `finally` so Ctrl-C mid-walk cannot leave the terminal in
        # absolute-cursor mode with no prompt.
        if board is not None:
            board.close()

    census = bf.Census(
        files=count,
        bytes=total,
        linked_dirs=tuple(warn.linked),
        unreadable_dirs=tuple(warn.unreadable),
        skipped_hidden=tuple(f.pair() for f in warn.skipped_hidden),
        skipped_worktrees=tuple(f.pair() for f in warn.skipped_worktrees),
        # What was ADMITTED: a name no option can admit (`refused_includes`)
        # is not carried into the re-walk's instructions.
        include_hidden=tuple(n for n in include_hidden if n not in bf.SKIP_DIRS),
        walk_rules=bf.WALK_RULES,
    )
    report.add(*incomplete_lines(census))
    report.add(*skipped_lines(census))
    if count >= index_mod.LARGE_WALK_FILES:
        # NAMED, not refused. The index streams, but `sample`/`cluster_by_mtime`
        # downstream still hold the whole record list, so a tree far past this
        # can be OOM-killed with nothing to show for the walk.
        report.add(
            f"{count:,} files is past what one import holds comfortably in "
            "memory — import subfolders separately if this run is killed."
        )
    return census, records, warn, index, previous


def incomplete_lines(census: bf.Census) -> list[str]:
    """Say what the walk could not see. Rendered in TWO places, on purpose.

    `_index` puts these in the report, which every exit returns -- that is the
    fix for the four paths (resume, already-imported, empty folder, stranded
    recovery) that never reach the review gate and so never said a word about
    a skipped directory.

    The GATE renders them too, ahead of the plan, because that is the moment
    they can still change the answer: after the import, "a directory was
    skipped" is only a regret. The gate splices this list in rather than
    `describe_plan` embedding it, so the copy that lands in the final report
    via `report.add(*body)` is not a second one.
    """
    lines: list[str] = []
    for items, noun, advice in (
        (census.linked_dirs, "linked",
         "Import the directory each one points at separately."),
        (census.unreadable_dirs, "unreadable",
         "Check permissions — anything under them is not counted or imported."),
    ):
        if not items:
            continue
        n = len(items)
        was = "directory was" if n == 1 else "directories were"
        lines += ["", f"{n} {noun} {was} skipped, so anything only reachable "
                      "through them is NOT in this import:"]
        lines += [f"  {i[0] + ' -> ' + i[1] if isinstance(i, tuple) else i}"
                  for i in items[:WARN_SHOWN]]
        if n > WARN_SHOWN:
            lines.append(f"  ... and {n - WARN_SHOWN} more")
        lines.append(f"  {advice}")
    return lines


#: How many skipped hidden folders the plan names before summarising the rest.
SKIPPED_SHOWN = 8


def skipped_lines(census: bf.Census) -> list[str]:
    """Say what the walk skipped BY RULE, with counts. Rendered where
    `incomplete_lines` is, for the same reason: the plan is where a reader can
    still change the answer (`--include-hidden <name>`).

    Worktree copies first and in one line: they are the large number, and the
    one a reader should not want back. Hidden folders by name, largest first.
    """
    def files(n: int) -> str:
        return f"{n:,} file{'' if n == 1 else 's'}"

    lines: list[str] = []
    if census.skipped_worktrees:
        n = len(census.skipped_worktrees)
        lines += ["", f"Skipped {n} git worktree{'' if n == 1 else 's'} "
                      f"({files(census.skipped_worktree_files)}): checkouts of a repo this import "
                      "already carries."]
        ordered = sorted(census.skipped_worktrees, key=lambda item: (-item[1], item[0]))
        lines += [f"  {path} ({files(count)})" for path, count in ordered[:SKIPPED_SHOWN]]
        if n > SKIPPED_SHOWN:
            lines.append(f"  ... and {n - SKIPPED_SHOWN:,} more")
    if census.skipped_hidden:
        ordered = sorted(census.skipped_hidden, key=lambda item: (-item[1], item[0]))
        shown = ", ".join(f"{path} ({files(count)})" for path, count in ordered[:SKIPPED_SHOWN])
        rest = ordered[SKIPPED_SHOWN:]
        lines += ["", f"Skipped hidden folders: {shown}"
                      + (f", and {len(rest):,} more ({files(sum(n for _, n in rest))})" if rest else "")
                      + ".",
                  "  Re-run with --include-hidden <name> to import one."]
    return lines


def refused_includes(include_hidden) -> list[str]:
    """`--include-hidden` names no option can admit, said rather than ignored."""
    refused = [name for name in include_hidden or () if name in bf.SKIP_DIRS]
    if not refused:
        return []
    credentials = [name for name in refused if name in bf.CREDENTIAL_DIRS]
    other = [name for name in refused if name not in bf.CREDENTIAL_DIRS]
    lines = []
    if credentials:
        lines.append(f"Not included: {', '.join(credentials)} — credential stores are never imported.")
    if other:
        lines.append(f"Not included: {', '.join(other)} — tool and cache folders are never imported.")
    return lines
from probe.cli.imports.folder.flow.plan_run import Report  # noqa: E402 -- pieces need each other; the front door loads this one first
