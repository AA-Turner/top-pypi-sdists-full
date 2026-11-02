"""evidence as classification-prompt rows: the two row shapes, rollups split where they hide structure, token estimates and chunks."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from probe.cli.imports.folder.walk.evidence import Evidence, FileEvidence, Tier

#: How deep a rollup key goes. Below this, a directory folds into its
#: depth-limited ancestor.
#:
#: A classifier assigns near the TOP of a tree -- a project boundary is one or
#: two levels down, not seven -- so `a/b/c/d/e/f/g` as its own row buys nothing
#: and a real checkout has thousands of them. Measured on a 109,706-file tree:
#: unbounded depth gave 15,842 rollup rows and ~800k tokens; depth 3 gives a few
#: hundred. The files are still all counted; only the grouping is coarser.
#:
#: FOUR, not three: `<person>/<project>/<run>/checkpoints/` is a routine
#: layout, and at three every run under one project collapses into a single
#: row the agent cannot split at any confidence.
ROLLUP_MAX_DEPTH = 4


def _rel(root: Path, path: str) -> str:
    try:
        return str(Path(path).relative_to(root))
    except ValueError:  # pragma: no cover - the walk never leaves the root
        return path


@dataclass(frozen=True)
class EvidenceRow:
    """One line of the classification prompt and the walked files it stands for.

    The prompt shows ROWS (a sampled file, or a directory's rolled-up tail); the
    plan is made of FILES. Recording the mapping here, where the rows are built,
    is what lets `probe-backfill-plan` select by file and directory instead of
    asking the model to copy row keys back -- and what keeps one slice's rollup
    from claiming a file another slice owns.
    """

    key: str
    line: str
    files: tuple[str, ...]


def to_jsonl(evidence: Evidence) -> str:
    """Evidence as JSONL for the classification prompt. See `rows`."""
    return "\n".join(row.line for row in rows(evidence))


def rows(evidence: Evidence) -> list[EvidenceRow]:
    """Evidence as JSONL rows for the classification prompt. TWO row shapes.

    Evidence files get a row each, because their contents are the whole point.
    TAIL files are ROLLED UP per directory, one row for the lot.

    That is not a size hack, it is the tier's own definition applied honestly: a
    tail file carries no text identifying anything, so a per-file row for
    `step_04000.pt` tells the agent exactly what a per-directory row does and
    costs 4,000 times more. Emitting them individually put a 200,000-file drive
    at ~5.8 MILLION tokens -- past any context window, and `--autocompact`
    cannot help because it compacts across TURNS and cannot shrink one
    oversized message. The pass was not slow at that size; it was rejected.

    Rolled up it is ~290k tokens for the same drive, and it reads better:
    "4,000 checkpoints written across two hours" is more use to a classifier
    than four thousand near-identical lines.

    The agent assigns a DIRECTORY in a rollup row, and
    :func:`probe.cli.imports.folder.classify.plan.resolve` expands that back to its files. The
    assumption -- that tail files in one directory belong together -- is the
    same one inheritance already makes, and it fails in the same case: a
    directory holding two projects' checkpoints. Evidence files in that
    directory are still listed individually, so the split stays visible.

    Paths are RELATIVE to the root. The agent's job is deciding what belongs
    together; a constant absolute prefix on every line costs budget and says
    nothing.
    """
    root = Path(evidence.root)
    #: (sort key, line). ROWS ARE INTERLEAVED BY DIRECTORY, not emitted in two
    #: blocks. Sampled rows used to come first and every rollup after them,
    #: which is harmless in one prompt and ruinous once the evidence is sliced:
    #: sampling stops at SAMPLE_BUDGET_FILES, so on any folder big enough to
    #: chunk the sampled rows fill the early slices and EVERY rollup lands in a
    #: later one containing no sample text at all. Those slices are then asked
    #: to place tail files "with their neighbours" while holding no neighbours,
    #: and `resolve` expands each rollup to every file beneath it -- so one
    #: blind guess misfiles thousands of files and the reconcile still reports
    #: a clean plan, because they were assigned, just wrongly.
    #:
    #: Sorting both kinds on the rollup key puts a directory's readable files
    #: next to the count of what else is in it, in one slice.
    out: list[tuple[tuple[str, str], EvidenceRow]] = []
    tail: dict[str, list[FileEvidence]] = {}

    def rollup_key(rel: str) -> str:
        return "/".join(Path(rel).parent.parts[:ROLLUP_MAX_DEPTH])

    for f in evidence.files:
        rel = _rel(root, f.path)
        # KEYED ON HAVING A SAMPLE, not on the tier. An evidence-tier file whose
        # sample the budget never reached carries exactly what a tail file
        # carries -- a path -- so listing it individually buys nothing and costs
        # the same. Measured on a real 109,706-file tree: tier-keyed rollup left
        # 50,295 sampleless evidence rows and 2.3M tokens; sample-keyed leaves
        # 600 and fits.
        if not f.sample:
            tail.setdefault(rollup_key(rel), []).append(f)
            continue
        row: dict[str, object] = {"path": rel, "size": f.size, "tier": f.tier.value}
        if f.mtime:
            row["mtime"] = int(f.mtime)
        if f.sample:
            row["sample"] = f.sample
            if f.truncated:
                row["sample_truncated"] = True
        out.append(((rollup_key(rel), rel),
                    EvidenceRow(rel, json.dumps(row, ensure_ascii=False), (rel,))))

    tail = _split_wide_rollups(tail, root)

    for directory in sorted(tail):
        group = tail[directory]
        stamps = [f.mtime for f in group if f.mtime > 0]
        exts = sorted({Path(f.path).suffix.lower() for f in group if Path(f.path).suffix})
        row = {
            # "." for the root, never "": an empty string is falsy and every
            # consumer that checks truthiness drops it, so root-level
            # checkpoints -- the most common place to leave them -- became
            # unassignable.
            "dir": directory or ".",
            "tier": "tail",
            "files": len(group),
            "bytes": sum(f.size for f in group),
            # The extensions are what a reader uses to tell a checkpoint
            # directory from an image directory without opening anything.
            "ext": exts[:8],
        }
        unsampled = sum(1 for f in group if f.tier is Tier.EVIDENCE)
        if unsampled:
            # Text files the sample budget never reached. Named so the agent can
            # tell "4,000 checkpoints" from "4,000 scripts I did not get to read".
            row["unread_text_files"] = unsampled
        if stamps:
            row["mtime_span"] = [int(min(stamps)), int(max(stamps))]
        # "￿" sorts after any real filename, so the rollup closes its
        # directory's group: the files that could be read, then the count of
        # what else is in there.
        out.append(((directory, "\uffff"), EvidenceRow(
            row["dir"], json.dumps(row, ensure_ascii=False),
            tuple(_rel(root, f.path) for f in group),
        )))

    out.sort(key=lambda pair: pair[0])
    return [row for _, row in out]


# -- fitting the evidence into a context window ------------------------------

#: Rough tokens per character. English prose is ~4; this evidence is JSON --
#: punctuation, quoted keys, paths -- which tokenises WORSE, so 3.2 is used and
#: the estimate deliberately runs high. Guessing low is the expensive direction:
#: it sends a prompt the model rejects after the walk has already been paid for.
_CHARS_PER_TOKEN = 3.2

#: Evidence that fits this goes to ONE agent, whole folder in view. That is the
#: better classification when it is possible -- every file is judged against
#: every other -- so chunking is a fallback, not the default.
#:
#: 90k leaves room in a 200k window for the instructions, the agent's reasoning
#: and an assignment per row on the way out.
SINGLE_SHOT_TOKEN_BUDGET = 90_000

#: Evidence tokens per chunk once chunking is on.
CHUNK_TOKEN_BUDGET = 55_000

#: Rows per chunk, which is a SEPARATE limit and not a redundant one. The assign
#: pass emits one object per row, so a chunk that fits the input budget on tiny
#: rollup rows can still ask for more output than the model will produce -- and
#: a truncated final message loses assignments silently.
CHUNK_MAX_ROWS = 500


def estimate_tokens(text: str) -> int:
    """Roughly how many tokens `text` costs. Deliberately pessimistic."""
    return int(len(text) / _CHARS_PER_TOKEN) + 1


def needs_chunking(evidence) -> bool:
    """Whether this folder's evidence is too big for one prompt.

    One place, because two callers have to agree: `classify` uses it to pick a
    route, and the review gate uses it to decide where a correction goes. If
    they ever disagreed, a correction on a chunked folder would be handed to
    the single-shot reviser -- which starts cold and is told to re-read a
    folder that does not fit.
    """
    return estimate_tokens(to_jsonl(evidence)) > SINGLE_SHOT_TOKEN_BUDGET


def chunk_lines(
    jsonl: str,
    *,
    token_budget: int = CHUNK_TOKEN_BUDGET,
    max_rows: int = CHUNK_MAX_ROWS,
) -> list[list[str]]:
    """Split evidence rows into chunks that each fit a prompt.

    Rows are kept in their emitted order, which is not cosmetic: `to_jsonl`
    lists sampled files then rollups sorted by directory, so neighbours in the
    list are usually neighbours on disk. Shuffling them would scatter each
    project's evidence across every chunk and leave no chunk able to say
    anything specific.

    A single row larger than the budget still gets its own chunk rather than
    being dropped or split -- half a JSON object is not evidence, and a
    classification silently missing files is the one outcome worth failing over.
    """
    chunks: list[list[str]] = []
    current: list[str] = []
    size = 0
    for line in jsonl.splitlines():
        if not line.strip():
            continue
        cost = estimate_tokens(line)
        if current and (size + cost > token_budget or len(current) >= max_rows):
            chunks.append(current)
            current, size = [], 0
        current.append(line)
        size += cost
    if current:
        chunks.append(current)
    return chunks


#: A rollup row this big is worth splitting into its children. Below it, the
#: coarser row costs the classifier nothing it can act on -- one directory of
#: four hundred checkpoints is one decision either way.
ROLLUP_SPLIT_FILES = 500

#: ...or this many distinct extensions under one key. A mixed subtree is the
#: shape that says "several things live here", and it is exactly the shape a
#: fixed depth cap hides: `<person>/<project>/<run>/checkpoints/` fits in four
#: levels, `<person>/<project>/<phase>/<run>/checkpoints/` does not, and at the
#: cap the whole phase collapses into one row the agent cannot split at any
#: confidence.
ROLLUP_SPLIT_EXTS = 4

#: How far past ROLLUP_MAX_DEPTH refinement may go. Unbounded splitting on a
#: pathological tree reproduces the row explosion the cap exists to prevent --
#: measured at unbounded depth on a 109,706-file tree: 15,842 rows, ~800k
#: tokens.
ROLLUP_REFINE_MAX_DEPTH = 8


def _split_wide_rollups(tail: dict, root: str) -> dict:
    """Refine rollup keys that are hiding structure, one level at a time.

    `ROLLUP_MAX_DEPTH` is a fixed cap, and a fixed cap is wrong in both
    directions: at four levels a shallow tree is over-detailed and a deep one
    collapses whole phases of work into a single row carrying nothing but a
    count. This splits the rows that are actually hiding something -- large, or
    mixed -- and leaves the rest alone, so depth follows the content instead of
    a constant.

    Only SAMPLELESS rows are affected, which is the whole population here:
    a file with a sample is already emitted individually at full path whatever
    its depth, so the depth cap never applied to it.
    """
    out = dict(tail)
    for depth in range(ROLLUP_MAX_DEPTH + 1, ROLLUP_REFINE_MAX_DEPTH + 1):
        wide = {k: g for k, g in out.items() if _worth_splitting(g)}
        if not wide:
            break
        for key, group in wide.items():
            children: dict[str, list] = {}
            for f in group:
                rel = str(Path(f.path).relative_to(root)) if root else f.path
                children.setdefault("/".join(Path(rel).parent.parts[:depth]), []).append(f)
            # A split that produces one child has not split anything -- every
            # file shares the next path component -- and re-adding it would
            # loop until the depth ceiling for no gain.
            if len(children) > 1:
                del out[key]
                out.update(children)
    return out


def _worth_splitting(group: list) -> bool:
    if len(group) >= ROLLUP_SPLIT_FILES:
        return True
    exts = {Path(f.path).suffix.lower() for f in group if Path(f.path).suffix}
    return len(exts) >= ROLLUP_SPLIT_EXTS
