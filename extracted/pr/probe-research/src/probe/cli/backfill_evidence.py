"""Evidence extraction: the ENUMERATE half of a backfill, deepened.

:mod:`probe.cli.backfill` names the split this feature is built on -- ENUMERATE
deterministic, DECIDE agent, RECONCILE deterministic. ENUMERATE used to mean
"count files and bytes", and that is not enough to DECIDE with.

The reason is that project membership is a per-FILE property and not a
per-directory one. A researcher's directory routinely holds pieces of several
lines of work, and one line of work routinely spills across directories nobody
would think to group. Handing an agent a directory tree and asking which folder
is which project is asking it to guess from the one signal that does not carry
the answer.

So this module turns a folder into EVIDENCE, without asking anyone to read a
terabyte:

    Tier 1   every file        path, size, mtime. Free -- the stat is already
                              paid by the census walk. mtime CLUSTERING is the
                              signal that survives a messy tree: files written
                              inside one window are usually one run.

    Tier 2   evidence-bearing  a bounded head sample of the files that can NAME
                              a project -- readme, markdown, config, yaml/json,
                              notebook and script headers, result tables, logs.
                              A few hundred out of tens of thousands.

    Tier 3   the long tail     checkpoints, shards, images, weights. No text in
                              them identifies a project, so they INHERIT from
                              their neighbours, and the rule that placed them is
                              RECORDED per file rather than implied. An
                              inherited assignment a reader cannot audit is
                              indistinguishable from a guess.

Two budgets, both real. Tier 2 opens files, so it is bounded by total bytes read
AND by file count -- an unbounded sample over a network mount is minutes of I/O
before anything uploads. Nothing here reads a file twice.

stdlib only, like the rest of cli/ -- ``probe log`` runs inside training loops
and must not pay for any of this.
"""

from __future__ import annotations

import json
import os
from collections.abc import Iterator
from dataclasses import dataclass, field
from probe._compat import StrEnum
from pathlib import Path

from ..sdk.redaction import scrub_text
from .backfill import (
    REFERENCE_ABOVE_BYTES,
    SKIP_DIRS,
    SKIP_FILES,
    SKIP_SUFFIXES,
    human_bytes,
)


class Tier(StrEnum):
    """Which evidence tier a file falls in. See the module docstring."""

    #: Carries text that can name a line of work. Sampled.
    EVIDENCE = "evidence"
    #: Carries no identifying text. Inherits, with the rule recorded.
    TAIL = "tail"


#: Extensions whose CONTENT can name a project. Deliberately a closed list
#: rather than "anything that decodes as text": a 4GB jsonl shard decodes fine
#: and tells you nothing, and sampling it costs the budget a config would have
#: spent better.
EVIDENCE_SUFFIXES = frozenset(
    {
        ".md", ".markdown", ".rst", ".txt",
        ".yaml", ".yml", ".json", ".toml", ".ini", ".cfg", ".conf",
        ".py", ".sh", ".r", ".jl", ".lua",
        ".ipynb",
        ".csv", ".tsv",
        ".log", ".out", ".err",
        ".tex", ".bib",
    }
)

#: Filenames that are evidence whatever their extension. A README with no
#: suffix is the single most informative file in most research folders.
EVIDENCE_NAMES = frozenset(
    {
        "readme", "notes", "makefile", "dockerfile", "license",
        "requirements", "pyproject", "setup", "environment",
        "config", "params", "hparams", "args", "run", "train",
    }
)

#: Never sampled however they are named -- these decode as text but carry no
#: project identity, and they are big.
TAIL_SUFFIXES = frozenset(
    {
        ".pt", ".pth", ".ckpt", ".safetensors", ".bin", ".h5", ".pkl", ".pickle",
        ".npy", ".npz", ".parquet", ".arrow", ".feather", ".pb", ".onnx",
        ".png", ".jpg", ".jpeg", ".gif", ".pdf", ".svg", ".mp4", ".wav",
        ".zip", ".tar", ".gz", ".bz2", ".xz", ".7z",
        ".so", ".dylib", ".dll", ".o", ".a",
        ".db", ".sqlite", ".sqlite3", ".wandb",
    }
)

#: Head bytes sampled from ONE evidence file. Enough for a header, a docstring,
#: a config block or a table's columns; short enough that a few hundred of them
#: still fit a classification prompt.
SAMPLE_BYTES = 700

#: Total bytes Tier 2 may read across the whole folder. At SAMPLE_BYTES each
#: that is ~1500 files, comfortably above the few hundred a real research folder
#: carries and far below what would stall the import.
SAMPLE_BUDGET_BYTES = 3 * 1024 * 1024

#: Ceiling on sampled FILES, independent of bytes. A folder of ten thousand
#: tiny configs would satisfy the byte budget and still blow the prompt.
SAMPLE_BUDGET_FILES = 600

#: An evidence file at or above this size is sampled but flagged: its head is
#: unlikely to represent it, and a reader should know the sample is a corner of
#: something much larger rather than the whole thing.
LARGE_EVIDENCE_BYTES = 4 * 1024 * 1024

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

#: Below this many dated files, one cluster means nothing either way -- a small
#: folder written in one sitting genuinely IS one burst.
UNINFORMATIVE_MIN_FILES = 25

#: Files written within this many seconds of each other are treated as one
#: burst. Research runs write their outputs together; the gaps between runs are
#: minutes to days, so this separates cleanly without tuning per folder.
CLUSTER_GAP_SECONDS = 15 * 60


@dataclass(frozen=True, slots=True)
class FileEvidence:
    """One file's Tier 1 facts, plus its Tier 2 sample when it has one.

    SLOTTED. One of these exists per file in the folder, so the per-instance
    ``__dict__`` a plain dataclass carries is the single largest allocation in
    an import: measured at 458 B/file without slots and 202 B with. Nothing
    reads ``__dict__``, ``vars()`` or ``asdict()`` on it, so the slot table
    costs nothing.

    This is NOT the peak footprint. ``sample`` copies the whole list and sorts
    an index over it, and ``cluster_by_mtime`` sorts again -- see the peak-RSS
    caveat there before quoting a memory number.
    """

    path: str
    size: int
    mtime: float
    tier: Tier
    sample: str | None = None
    #: Set when the sample is a head of something much larger than the sample.
    truncated: bool = False
    #: Why a TAIL file was placed where it was. Set by the caller that resolves
    #: inheritance, never guessed here -- an unaudited inheritance is a guess
    #: wearing a rule's clothes.
    inherited_from: str | None = None


@dataclass
class Cluster:
    """A burst of files written together. The same-run signal."""

    started: float
    ended: float
    paths: list[str] = field(default_factory=list)

    @property
    def span_seconds(self) -> float:
        return max(0.0, self.ended - self.started)


@dataclass
class Evidence:
    """Everything ENUMERATE produces for one folder."""

    root: str
    files: list[FileEvidence]
    clusters: list[Cluster]
    sampled_files: int
    sampled_bytes: int
    #: True when a budget stopped the sampling early. The classification prompt
    #: MUST say so: an agent told it saw everything, when it saw a prefix, will
    #: report confidence it has not earned.
    sample_budget_hit: bool = False

    @property
    def mtime_uninformative(self) -> bool:
        """True when every file's mtime falls in one window, so it separates nothing.

        Clustering is the grouping signal that survives a messy tree -- files
        written within minutes of each other are usually one run. A COPY
        destroys it: `cp -r`, or an rsync without `--times`, stamps files with
        the copy time rather than the original, and "written together" stops
        distinguishing anything. That is the normal state of a shared drive
        someone was handed, and left unsaid the classifier goes on being told
        timestamps group work the directory tree does not -- and goes on
        believing it, which is worse than having no signal.

        THE SPAN, not the cluster count, and the first version got this wrong
        in both directions. `cluster_by_mtime` chains transitively across a
        15-minute gap, so a real run writing a checkpoint every 5 minutes for
        five hours collapsed into ONE cluster and was declared dead -- throwing
        away timestamps that genuinely spanned the afternoon. And a copy
        interrupted a few times produced several clusters and was declared
        healthy, which is the case this exists for.

        WHAT IT CANNOT SEE, stated rather than papered over: a copy that runs
        for hours spreads its mtimes over those hours, and by timestamps alone
        that is indistinguishable from work done over the same hours. This
        catches the clear case -- everything inside one window -- and says
        nothing about the rest, which is the honest limit of the evidence.

        The floor matters as much as the span. A folder of eight files written
        in one sitting IS one burst, and flagging it would be noise on exactly
        the folders where a person can see the answer anyway.
        """
        stamps = [f.mtime for f in self.files if f.mtime > 0]
        if len(stamps) < UNINFORMATIVE_MIN_FILES:
            return False
        return max(stamps) - min(stamps) <= CLUSTER_GAP_SECONDS

    @property
    def total_files(self) -> int:
        return len(self.files)

    @property
    def total_bytes(self) -> int:
        return sum(f.size for f in self.files)

    def describe(self) -> str:
        ev = sum(1 for f in self.files if f.tier is Tier.EVIDENCE)
        return (
            f"{self.total_files:,} files   {human_bytes(self.total_bytes)}   "
            f"{ev:,} evidence-bearing, {self.sampled_files:,} sampled"
            + ("  (sample budget reached)" if self.sample_budget_hit else "")
        )


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

    def sort(self) -> None:
        """Stable order, so two runs over one drive show the same list."""
        self.linked.sort()
        self.unreadable.sort()


def _stem_key(name: str) -> str:
    """The lowercased stem, for matching against EVIDENCE_NAMES."""
    return name.rsplit(".", 1)[0].lower() if "." in name else name.lower()


def tier_for(name: str, size: int) -> Tier:
    """Which tier a file belongs to, from its NAME and SIZE alone.

    Name and size only, deliberately: this runs for every file in the tree, so
    it may not open anything. Size participates because a 10GB ``.json`` is a
    dataset shard whatever its extension claims, and sampling its head would
    spend the budget describing a bracket.
    """
    suffix = ("." + name.rsplit(".", 1)[1].lower()) if "." in name else ""
    if suffix in TAIL_SUFFIXES:
        return Tier.TAIL
    if size >= REFERENCE_ABOVE_BYTES:
        # Uploaded by reference anyway; its bytes are never read for content.
        return Tier.TAIL
    if suffix in EVIDENCE_SUFFIXES or _stem_key(name) in EVIDENCE_NAMES:
        return Tier.EVIDENCE
    return Tier.TAIL


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


def walk(root: Path, warn: WalkWarnings | None = None) -> Iterator[FileEvidence]:
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
    """
    root = Path(root).resolve()
    warn = warn if warn is not None else WalkWarnings()
    resolved_root = str(root)
    stack: list[str] = [str(root)]
    first = True

    while stack:
        here = stack.pop()
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
            else:
                warn.unreadable.append(_rel_to(root, here))
            first = False
            continue
        first = False

        for entry in entries:
            name = entry.name
            # NO blanket dotfile skip. It used to be `name.startswith(".")`,
            # which silently lost `.hydra/config.yaml` -- the file that names a
            # Hydra experiment -- plus `.dvc/` and `.condarc`, from the evidence
            # AND from the census. SKIP_DIRS now carries the machine-written
            # dot-directories by name, so what is dropped is a decision someone
            # can read instead of a side effect of the leading character.
            try:
                is_dir = entry.is_dir()  # FOLLOWS links, exactly as os.walk does
            except OSError:
                is_dir = False
            if is_dir:
                if name in SKIP_DIRS:
                    continue
                try:
                    if entry.is_symlink():
                        _record_link(warn, root, resolved_root, entry)
                        continue  # recorded, still not followed
                except OSError:
                    # ROOT-RELATIVE, like every other entry in this list. A
                    # bare `locked` for `datasets/2024/locked/` is a name the
                    # reader cannot find, and being findable is the entire
                    # point of naming it.
                    warn.unreadable.append(_rel_to(root, entry.path))
                    continue
                stack.append(entry.path)
                continue
            if name in SKIP_FILES or Path(name).suffix.lower() in SKIP_SUFFIXES:
                continue
            size, mtime = _entry_stat(entry)
            yield FileEvidence(
                path=entry.path, size=size, mtime=mtime, tier=tier_for(name, size)
            )

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


def cluster_by_mtime(
    files: list[FileEvidence], *, gap_seconds: float = CLUSTER_GAP_SECONDS
) -> list[Cluster]:
    """Group files into write bursts.

    The one grouping signal that does not care how the tree is laid out. Files
    with no usable mtime (the OSError path in :func:`walk`) are left out
    entirely rather than pooled into a fictional cluster at the epoch.
    """
    dated = sorted((f for f in files if f.mtime > 0), key=lambda f: f.mtime)
    clusters: list[Cluster] = []
    for f in dated:
        if clusters and f.mtime - clusters[-1].ended <= gap_seconds:
            clusters[-1].ended = f.mtime
            clusters[-1].paths.append(f.path)
        else:
            clusters.append(Cluster(started=f.mtime, ended=f.mtime, paths=[f.path]))
    return clusters


def read_head(path: str, *, limit: int = SAMPLE_BYTES) -> str | None:
    """A text head of `path`, SCRUBBED, or None when it is not usefully text.

    Decoded with ``errors="replace"`` rather than skipped on a decode error: a
    config with one stray byte is still a config, and losing it because of that
    byte is worse than a replacement character in a prompt. Binary is rejected
    by NUL sniffing instead, which is cheap and does not depend on the suffix
    list being complete.

    THE SCRUB IS THE CHOKEPOINT, and it is here rather than at the prompt
    because this is the one place every sample passes through. Filtering by
    FILENAME would not have worked: `.env` is already never sampled (`tier_for`
    calls it TAIL -- no `.env` suffix in EVIDENCE_SUFFIXES, no bare stem in
    EVIDENCE_NAMES), while the files that DO carry keys in an ML folder are
    ordinary sampled evidence -- `.hydra/config.yaml`, `overrides.yaml`, a
    plain `config.yaml` with `wandb_api_key:` in it. Those samples go into an
    agent prompt and into the captured transcript, neither of which passes the
    ingest redaction gate, so an unscrubbed head is a key in team memory.
    """
    try:
        with open(path, "rb") as fh:
            raw = fh.read(limit)
    except OSError:
        return None
    if b"\x00" in raw:
        return None
    text = scrub_text(raw.decode("utf-8", errors="replace")).strip()
    return text or None


def sample(
    files: list[FileEvidence],
    *,
    budget_bytes: int = SAMPLE_BUDGET_BYTES,
    budget_files: int = SAMPLE_BUDGET_FILES,
) -> tuple[list[FileEvidence], int, int, bool]:
    """Tier 2. Returns ``(files, sampled_count, sampled_bytes, budget_hit)``.

    Evidence files are sampled SMALLEST FIRST. That is not arbitrary: a folder's
    identity lives in its readmes and configs, which are small, while its big
    "evidence" files are usually logs whose head is boilerplate. Smallest-first
    spends a fixed budget on the most files, and the ones it drops are the ones
    that would have said least.
    """
    order = sorted(
        (i for i, f in enumerate(files) if f.tier is Tier.EVIDENCE),
        key=lambda i: files[i].size,
    )
    out = list(files)
    used_bytes = 0
    used_files = 0
    budget_hit = False
    for i in order:
        if used_files >= budget_files or used_bytes >= budget_bytes:
            budget_hit = True
            break
        f = files[i]
        head = read_head(f.path)
        if head is None:
            # Reads as binary despite its name. Reclassify rather than pretend:
            # the classifier must not be handed replacement characters as if
            # they meant something.
            out[i] = FileEvidence(
                path=f.path, size=f.size, mtime=f.mtime, tier=Tier.TAIL
            )
            continue
        # WHAT WAS READ, not what survived. `read_head` scrubs, so measuring
        # the returned string charged the budget for the leftovers: a config
        # whose body redacted down to `<redacted>` cost 10 bytes against a
        # budget that exists to bound how much of the folder gets opened. The
        # read is capped at SAMPLE_BYTES, so this is exact.
        used_bytes += min(f.size, SAMPLE_BYTES)
        used_files += 1
        out[i] = FileEvidence(
            path=f.path,
            size=f.size,
            mtime=f.mtime,
            tier=Tier.EVIDENCE,
            sample=head,
            # AGAINST WHAT WAS READ, not against the scrubbed head. `read_head`
            # redacts, so comparing the file size to `len(head)` marked a
            # 400-byte config as truncated because one `wandb_api_key` line
            # became `<redacted>` -- telling the classifier it saw a corner of
            # something larger when it saw the whole file.
            truncated=f.size > LARGE_EVIDENCE_BYTES or f.size > SAMPLE_BYTES,
        )
    return out, used_files, used_bytes, budget_hit


def enrich(root: Path, files: list[FileEvidence]) -> Evidence:
    """PHASE 2. Sample and cluster records phase 1 already walked.

    Split out from :func:`gather` so the caller can run phase 1, answer the
    cheap questions, and leave without paying for this. `sample` opens up to
    :data:`SAMPLE_BUDGET_FILES` files and `cluster_by_mtime` sorts every record
    -- on the filesystems this feature exists for, 600 opens is not free.

    The two callers that must never reach here are the already-imported and
    resume checks in `backfill_run`: both are answered by the census alone, and
    both used to run before the evidence walk happened at all. Folding the
    census into phase 1 without splitting this out would have made the fastest
    path in the flow slower.
    """
    files, n_files, n_bytes, hit = sample(files)
    return Evidence(
        root=str(Path(root).resolve()),
        files=files,
        clusters=cluster_by_mtime(files),
        sampled_files=n_files,
        sampled_bytes=n_bytes,
        sample_budget_hit=hit,
    )


def gather(root: Path, warn: WalkWarnings | None = None) -> Evidence:
    """Both phases, for callers that always want the whole thing.

    `backfill_run` does NOT use this -- it runs the phases separately so the
    early exits can skip phase 2. Kept because the phases are only separate for
    that one reason, and every other caller wants them together.
    """
    root = Path(root).resolve()
    return enrich(root, list(walk(root, warn)))


def _rel(root: Path, path: str) -> str:
    try:
        return str(Path(path).relative_to(root))
    except ValueError:  # pragma: no cover - the walk never leaves the root
        return path


def to_jsonl(evidence: Evidence) -> str:
    """Evidence as JSONL for the classification prompt. TWO row shapes.

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
    :func:`probe.cli.backfill_plan.resolve` expands that back to its files. The
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
    rows: list[tuple[tuple[str, str], str]] = []
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
        rows.append(((rollup_key(rel), rel), json.dumps(row, ensure_ascii=False)))

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
        rows.append(((directory, "￿"), json.dumps(row, ensure_ascii=False)))

    rows.sort(key=lambda pair: pair[0])
    return "\n".join(line for _, line in rows)


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
