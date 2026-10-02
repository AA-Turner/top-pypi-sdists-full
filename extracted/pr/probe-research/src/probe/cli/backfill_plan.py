"""The agent's classification, checked against the walk, packed into units.

DECIDE hands back prose-adjacent JSON. This module is the seam where that
becomes something the rest of the import can act on, and it is deliberately
suspicious: the denominator comes from the filesystem, never from the model, and
the same rule applies one step earlier here. An agent that quietly drops four
thousand files must not be able to produce a plan that looks complete.

So :func:`reconcile_assignments` compares what came back against what was walked
and reports THREE separate discrepancies rather than one boolean:

    missing     walked, never assigned  -- would be silently skipped
    unknown     assigned, never walked  -- hallucinated, or a path typo
    duplicated  assigned more than once -- would upload twice, into two projects

Only `missing` is recoverable by falling back (an unassigned file still has a
home: the project its neighbours went to). `unknown` and `duplicated` mean the
answer cannot be trusted as given, so they surface rather than get patched over.

Packing into units is the other half. A unit is one agent's turn: one project,
a bounded number of files, and -- where it can be arranged -- files that were
written together, because an agent describing a coherent burst writes better
notes than one describing an arbitrary slice.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from .backfill import REFERENCE_ABOVE_BYTES, _embedded_summaries
from .backfill_evidence import Evidence, Tier
from .backfill_ledger import Unit, UnitKind, new_unit_id

#: Files per unit. Sized so one agent turn stays inside a context it can hold
#: while still reading each file it describes -- and so a crash costs a bounded
#: amount of re-reading rather than an hour.
MAX_UNIT_FILES = 400

#: Bytes per unit, counting only what will actually be uploaded. One unit full
#: of small configs and one full of 90MB archives are very different jobs.
MAX_UNIT_BYTES = 2 * 1024 * 1024 * 1024


@dataclass
class ProjectSpec:
    """A project the classification asked for."""

    slug: str
    name: str = ""
    description: str = ""
    tags: list[str] = field(default_factory=list)


@dataclass
class Assignment:
    path: str
    project: str
    confidence: str = "high"
    why: str = ""


@dataclass
class Discrepancy:
    """What the walk and the classification disagree about."""

    missing: list[str] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)
    duplicated: list[str] = field(default_factory=list)

    @property
    def clean(self) -> bool:
        return not (self.missing or self.unknown or self.duplicated)

    @property
    def trustworthy(self) -> bool:
        """Whether the plan can be used at all, with or without a fallback.

        `missing` is recoverable. `unknown` and `duplicated` are not: one means
        the model invented paths, the other means it would file one file into
        two projects, and neither is something to paper over silently.
        """
        return not (self.unknown or self.duplicated)

    def describe(self) -> list[str]:
        out: list[str] = []
        if self.missing:
            out.append(
                f"{len(self.missing):,} files were walked but never assigned "
                "— they will follow their neighbours."
            )
        if self.unknown:
            out.append(
                f"{len(self.unknown):,} assigned paths are not in this folder "
                f"(e.g. {self.unknown[0]}) — the classification cannot be trusted."
            )
        if self.duplicated:
            out.append(
                f"{len(self.duplicated):,} files were assigned more than once "
                f"(e.g. {self.duplicated[0]}) — they would upload twice."
            )
        return out


@dataclass
class Plan:
    projects: list[ProjectSpec]
    assignments: list[Assignment]
    unsure: list[str] = field(default_factory=list)
    summary: str = ""


def parse(tail: str) -> Plan | None:
    """Pull the classification out of an agent's event stream.

    Reuses :func:`probe.cli.backfill._embedded_summaries` rather than writing a
    second extractor. That function already solves the hard part: both agents
    are run with `--output-format stream-json`, so the JSON we want is a STRING
    FIELD inside an envelope and its braces are nested in one line of stdout.
    A second implementation here would rot against that one.
    """
    best: Plan | None = None
    for line in reversed(tail.splitlines()):
        if "projects" not in line:
            continue
        for data in _embedded_summaries(line.strip()):
            if not isinstance(data.get("assignments"), list):
                continue  # a run summary, not a classification
            best = _plan_from(data)
            if best is not None:
                return best
    return best


def _plan_from(data: dict) -> Plan | None:
    projects: list[ProjectSpec] = []
    for p in data.get("projects") or []:
        if isinstance(p, str):
            projects.append(ProjectSpec(slug=p, name=p))
        elif isinstance(p, dict) and p.get("slug"):
            projects.append(
                ProjectSpec(
                    slug=str(p["slug"]),
                    name=str(p.get("name") or p["slug"]),
                    description=str(p.get("description") or ""),
                    tags=[str(t) for t in (p.get("tags") or []) if t],
                )
            )
    assignments: list[Assignment] = []
    for a in data.get("assignments") or []:
        if not isinstance(a, dict) or not a.get("project"):
            continue
        # A rollup row is addressed by `dir`, and the agent may echo either key.
        # Accepting only `path` dropped every directory assignment silently, so
        # thousands of files fell to inheritance with nothing reported.
        raw = a.get("path")
        if raw is None:
            raw = a.get("dir")
        if raw is None:
            continue
        assignments.append(
            Assignment(
                path=str(raw),
                project=str(a["project"]),
                confidence=str(a.get("confidence") or "high"),
                why=str(a.get("why") or ""),
            )
        )
    if not assignments:
        return None
    return Plan(
        projects=projects,
        assignments=assignments,
        unsure=[str(u) for u in (data.get("unsure") or []) if u],
        summary=str(data.get("summary") or ""),
    )


def relative_paths(evidence: Evidence) -> list[str]:
    root = Path(evidence.root)
    out: list[str] = []
    for f in evidence.files:
        try:
            out.append(str(Path(f.path).relative_to(root)))
        except ValueError:  # pragma: no cover - the walk never leaves the root
            out.append(f.path)
    return out


def reconcile_assignments(evidence: Evidence, plan: Plan) -> Discrepancy:
    """What the walk and the classification disagree about. See module docs."""
    walked = relative_paths(evidence)
    walked_set = set(walked)
    seen: dict[str, int] = {}
    unknown: list[str] = []
    for a in plan.assignments:
        if a.path not in walked_set:
            unknown.append(a.path)
            continue
        seen[a.path] = seen.get(a.path, 0) + 1
    return Discrepancy(
        missing=sorted(walked_set - set(seen)),
        unknown=sorted(set(unknown)),
        duplicated=sorted(p for p, n in seen.items() if n > 1),
    )


def _neighbour_project(path: str, assigned: dict[str, str]) -> str | None:
    """The project of the nearest assigned file, walking up the tree.

    This is the Tier 3 inheritance rule made concrete, and it is applied to
    UNASSIGNED files too. Nearest-directory-first rather than nearest-by-name:
    a checkpoint's siblings are what identify it, and its name is a step number.
    """
    parent = str(Path(path).parent)
    while True:
        prefix = "" if parent == "." else parent + "/"
        here = [p for p in assigned if p.startswith(prefix) and p != path]
        if here:
            counts: dict[str, int] = {}
            for p in here:
                counts[assigned[p]] = counts.get(assigned[p], 0) + 1
            return max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]
        if parent in (".", "", "/"):
            return None
        nxt = str(Path(parent).parent)
        if nxt == parent:
            return None
        parent = nxt


def resolve(evidence: Evidence, plan: Plan) -> tuple[dict[str, str], Discrepancy]:
    """Final path -> project map, with unassigned files placed by inheritance.

    Returns the map and the discrepancy that produced it, so a caller can show
    what it had to fill in. Silently completing the map would hide exactly the
    thing worth showing a human before anything uploads.
    """
    # A rollup row names a DIRECTORY, so an assignment against one stands for
    # every tail file under it. Expanded BEFORE the reconcile, or the walk would
    # report thousands of "missing" files the agent did in fact place -- turning
    # the honest-denominator check into noise nobody reads.
    walked = set(relative_paths(evidence))
    expanded: list[Assignment] = []
    # ONLY expansion claims. A directly-named path is appended every time it
    # appears, so two rows naming the same file still reach the reconcile as a
    # DUPLICATE -- deduping those here silently discarded the second assignment
    # and made `duplicated` unfireable, which is the one signal that says the
    # plan cannot be trusted.
    claimed: set[str] = set()
    # LONGEST PREFIX FIRST. Rollup keys are capped at ROLLUP_MAX_DEPTH but not
    # padded to it, so `a/b` and `a/b/c` can both be rows -- and recursive
    # expansion of the shorter one would claim the longer one's files as well,
    # assigning them twice. Twice is not a cosmetic problem: `duplicated` makes
    # the whole plan untrustworthy, which is correct, so the specific row has to
    # win before the general one is applied.
    ordered = sorted(plan.assignments, key=lambda a: (a.path not in walked, -len(a.path)))
    for a in ordered:
        if a.path in walked:
            claimed.add(a.path)
            expanded.append(a)
            continue
        prefix = "" if a.path in ("", ".") else a.path.rstrip("/") + "/"
        # RECURSIVE, because the rollup that produced this row is. Keys are
        # capped at ROLLUP_MAX_DEPTH, so a `dir` of "michael/odyssey/ckpt"
        # stands for everything beneath it too -- non-recursive expansion would
        # leave every deeper file unassigned and the reconcile would report
        # thousands of files as missing that the agent did place.
        #
        # A more specific row still wins: `direct` is applied after this loop,
        # so an evidence file inside the subtree keeps its own assignment.
        covers = any(w.startswith(prefix) for w in walked)
        members = [w for w in walked if w.startswith(prefix) and w not in claimed]
        if members:
            claimed.update(members)
            expanded += [
                Assignment(path=m, project=a.project, confidence=a.confidence,
                           why=a.why or f"directory {a.path}")
                for m in members
            ]
        elif covers:
            # Every file under it was already claimed by a longer, more specific
            # row. The agent naming a parent as well is normal and harmless --
            # REDUNDANT, not hallucinated. Reporting it as unknown killed the
            # whole import over a correct answer.
            continue
        else:
            # Neither a file nor a directory we walked. Genuinely unknown, and
            # the reconcile must still say so.
            expanded.append(a)
    plan = Plan(projects=plan.projects, assignments=expanded,
                unsure=plan.unsure, summary=plan.summary)

    disc = reconcile_assignments(evidence, plan)
    assigned = {a.path: a.project for a in plan.assignments if a.path not in disc.unknown}
    for path in disc.missing:
        inherited = _neighbour_project(path, assigned)
        if inherited is not None:
            assigned[path] = inherited
    return assigned, disc


def pack(
    evidence: Evidence,
    assigned: dict[str, str],
    *,
    max_files: int = MAX_UNIT_FILES,
    max_bytes: int = MAX_UNIT_BYTES,
) -> list[Unit]:
    """Group the EVIDENCE-tier assignments into units: one project, bounded size.

    Files are ordered by mtime inside a project before chunking, so a unit tends
    to hold one burst of work rather than an arbitrary slice. An agent
    describing a coherent burst writes better notes than one describing a
    scatter, and the notes are the part that makes a file findable later.

    TAIL FILES ARE NOT HERE, and that is the whole cost story. A file is TAIL
    precisely because it carries no text that identifies anything -- checkpoints,
    shards, weights -- and its project is already resolved without a model, by
    rollup expansion and neighbour inheritance with `inherited_from` recording
    the rule. Packing them anyway meant one agent turn per 400 of them, so a
    200k-file checkpoint folder cost ~500 turns to have a model open binaries
    and write the manifest row `tail_rows` now writes by hand. They are
    manifested there; every one of them still uploads, so coverage is
    unchanged and only the bill moves.
    """
    root = Path(evidence.root)
    size_of: dict[str, int] = {}
    mtime_of: dict[str, float] = {}
    evidence_paths: set[str] = set()
    for f in evidence.files:
        rel = _relative(root, f)
        size_of[rel] = f.size
        mtime_of[rel] = f.mtime
        if f.tier is Tier.EVIDENCE:
            evidence_paths.add(rel)

    by_project: dict[str, list[str]] = {}
    for path, project in assigned.items():
        if path in evidence_paths:
            by_project.setdefault(project, []).append(path)

    units: list[Unit] = []
    for project in sorted(by_project):
        paths = sorted(by_project[project], key=lambda p: (mtime_of.get(p, 0.0), p))
        batch: list[str] = []
        batch_bytes = 0
        for path in paths:
            size = _billable_bytes(size_of.get(path, 0))
            over_files = len(batch) >= max_files
            over_bytes = batch and batch_bytes + size > max_bytes
            if over_files or over_bytes:
                units.append(
                    Unit(unit_id=new_unit_id(), project=project, paths=tuple(batch))
                )
                batch, batch_bytes = [], 0
            batch.append(path)
            batch_bytes += size
        if batch:
            units.append(Unit(unit_id=new_unit_id(), project=project, paths=tuple(batch)))
    return units


def _relative(root: Path, f) -> str:
    try:
        return str(Path(f.path).relative_to(root))
    except ValueError:  # pragma: no cover - the walk never leaves the root
        return f.path


def _billable_bytes(size: int) -> int:
    """What a file costs the unit's byte budget.

    A file over `REFERENCE_ABOVE_BYTES` is recorded as a path plus a hash and
    its bytes never move, so charging the full size against `MAX_UNIT_BYTES`
    split units on transfers that do not happen -- one 10GB checkpoint filled
    a 2GB budget five times over on its own, giving units of one or two files
    and one agent turn each. `MAX_UNIT_BYTES` has always said it counts "only
    what will actually be uploaded"; this makes that true.
    """
    return 0 if size > REFERENCE_ABOVE_BYTES else size


def pack_tails(
    evidence: Evidence,
    assigned: dict[str, str],
    *,
    max_files: int = MAX_UNIT_FILES,
    max_bytes: int = MAX_UNIT_BYTES,
) -> list[Unit]:
    """TAIL files as ordinary ledger units, marked so no model ever sees them.

    Bounded on BOTH caps, exactly like an agent unit. Nothing reads these
    files, but a unit is also the resume granularity and the enqueue
    granularity: files under REFERENCE_ABOVE_BYTES upload by VALUE, so 400
    99MB shards in one unit is a 39GB `artifact add --from-manifest` whose
    failure costs all of it. The file cap alone would have removed the byte
    bound that `pack` has always had.
    """
    sizes = sizes_by_path(evidence)
    by_project: dict[str, list[str]] = {}
    for rel, project in _tail_assignments(evidence, assigned):
        by_project.setdefault(project, []).append(rel)
    units: list[Unit] = []
    for project in sorted(by_project):
        batch: list[str] = []
        batch_bytes = 0
        for rel in sorted(by_project[project]):
            billable = _billable_bytes(sizes.get(rel, 0))
            if batch and (len(batch) >= max_files or batch_bytes + billable > max_bytes):
                units.append(Unit(unit_id=new_unit_id(), project=project,
                                  paths=tuple(batch), kind=UnitKind.TAIL))
                batch, batch_bytes = [], 0
            batch.append(rel)
            batch_bytes += billable
        if batch:
            units.append(Unit(unit_id=new_unit_id(), project=project,
                              paths=tuple(batch), kind=UnitKind.TAIL))
    return units


def _tail_assignments(evidence: Evidence, assigned: dict[str, str]):
    root = Path(evidence.root)
    for f in evidence.files:
        if f.tier is Tier.EVIDENCE:
            continue
        rel = _relative(root, f)
        project = assigned.get(rel)
        if project is not None:
            yield rel, project


def tail_manifest(unit: Unit, sizes: dict[str, int]) -> list[dict]:
    """One TAIL unit's manifest rows, written by code instead of a model.

    The shape `artifact add --from-manifest` already accepts, so this joins the
    existing enqueue path rather than adding a second one.

    `notes` is deliberately ABSENT rather than invented. The import prompt has
    always conceded that "a file with nothing worth saying still goes in the
    manifest, just without notes", and a generated sentence about a checkpoint
    would be a model's guess wearing a fact's clothes. What the file IS lives in
    its name, its project, and the neighbours whose assignment it inherited.
    """
    rows: list[dict] = []
    for rel in unit.paths:
        reference = sizes.get(rel, 0) > REFERENCE_ABOVE_BYTES
        row: dict = {"path": rel, "reference": reference}
        if reference:
            # A shared mount the enqueuing machine may not see at the same path
            # is the ordinary case for a checkpoint directory.
            row["allow_missing"] = True
        rows.append(row)
    return rows


def sizes_by_path(evidence: Evidence) -> dict[str, int]:
    """Relative path -> size, for callers that need it after packing."""
    root = Path(evidence.root)
    return {_relative(root, f): f.size for f in evidence.files}


#: What a classify pass costs, in agent turns. One for a folder whose evidence
#: fits a single prompt; the chunked route runs a survey pass and an assign
#: pass per chunk, and `needs_chunking` is not answerable before sampling.
#: Two is the honest floor to quote before the walk has been sampled.
CLASSIFY_TURNS = 2


@dataclass
class Estimate:
    """What an import is about to cost, before anything is spent.

    Both caps, because either can bind and they bind on different folders. A
    folder of small configs is FILE-bound and a checkpoint folder is BYTE-bound
    -- 2GB of units against GB-scale checkpoints is two or three files a unit,
    so counting `files / MAX_UNIT_FILES` alone understated a real import by one
    to two orders of magnitude, on exactly the folder type that ran a plan out
    of tokens mid-import.
    """

    evidence_files: int
    #: A LOWER BOUND, and it has to be. `pack` groups by PROJECT, so a folder
    #: holding twenty lines of work costs at least twenty units however small
    #: they are -- and this runs BEFORE classification, which is the only thing
    #: that knows how many projects there are. Quoting it as exact would
    #: understate a scattered drive badly; quoting it as a floor is true, and
    #: the floor is what a user needs before deciding to start.
    agent_units: int
    tail_files: int
    tail_units: int

    @property
    def turns(self) -> int:
        """Agent turns, at least. TAIL units are not here -- they cost none."""
        return self.agent_units + CLASSIFY_TURNS

    def describe(self) -> str:
        if not self.evidence_files and not self.tail_files:
            return ""
        parts = [
            f"{self.turns:,} agent turn{'s' if self.turns != 1 else ''} or more"
        ]
        if self.tail_files:
            parts.append(
                f"{self.tail_files:,} checkpoint-like file"
                f"{'s' if self.tail_files != 1 else ''} imported without one"
            )
        return " · ".join(parts)


def estimate(records, *, max_files: int = MAX_UNIT_FILES,
             max_bytes: int = MAX_UNIT_BYTES) -> Estimate:
    """Cost the import from the WALK, before a single agent starts.

    Takes walk records rather than `Evidence` on purpose: tiers are decided
    during the walk, so this is answerable at the census screen -- which is
    the last moment a warning can still change the answer for free. After
    sampling, the classify pass has already been paid for.

    The packing here mirrors `pack`/`pack_tails` rather than calling them
    because those need an assignment map and this runs before one exists --
    which is also why the unit counts are LOWER BOUNDS: packing is per-project
    and the projects are not known yet. See `Estimate.agent_units`.
    """
    evidence_sizes = [f.size for f in records if f.tier is Tier.EVIDENCE]
    tail_count = sum(1 for f in records if f.tier is not Tier.EVIDENCE)
    units = 0
    batch, batch_bytes = 0, 0
    for size in sorted(evidence_sizes):
        billable = _billable_bytes(size)
        if batch and (batch >= max_files or batch_bytes + billable > max_bytes):
            units += 1
            batch, batch_bytes = 0, 0
        batch += 1
        batch_bytes += billable
    if batch:
        units += 1
    return Estimate(
        evidence_files=len(evidence_sizes),
        agent_units=units,
        tail_files=tail_count,
        tail_units=-(-tail_count // max_files) if tail_count else 0,
    )
