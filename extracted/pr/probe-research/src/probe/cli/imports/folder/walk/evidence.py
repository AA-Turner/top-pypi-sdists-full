"""Evidence extraction: the ENUMERATE half of a backfill, deepened.

:mod:`probe.cli.imports.folder` names the split this feature is built on -- ENUMERATE
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
from dataclasses import dataclass, field
from probe.foundation.compat.compat import StrEnum
from .skip_rules import REFERENCE_ABOVE_BYTES
from .census import human_bytes


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
