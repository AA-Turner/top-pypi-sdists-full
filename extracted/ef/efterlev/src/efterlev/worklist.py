"""Worklist — `efterlev next`: the companion that walks an ISV to submission-ready.

A scanner *judges* you ("here are 38 gaps"); a companion *walks you through*
("do this next, here's the command, here's why it matters most"). This builds an
impact-ranked, stage-aware worklist from the current workspace state and re-ranks
every time you run it as items close.

It reuses the readiness scorer (verdicts + score), the manifest loader (which
procedural KSIs already have an attestation), the boundary config (declared yet?),
and report artifact mtimes (a cheap funnel-timing signal — where did the user
stall?). Deterministic: no LLM, no network, no writes.
"""

from __future__ import annotations

import time
from dataclasses import dataclass
from pathlib import Path

# KSI themes that are procedural by nature (no scanner can see them) — they need
# a human-authored Evidence Manifest. Mirrors readiness's classification.
_PROCEDURAL_PREFIXES = ("KSI-AFR-", "KSI-CED-", "KSI-INR-")

_IMPACT_RANK = {"high": 0, "medium": 1, "low": 2}
_EFFORT_RANK = {"quick": 0, "medium": 1, "involved": 2}


@dataclass(frozen=True)
class WorkItem:
    """One ranked next step, with the exact command to run."""

    title: str
    why: str
    command: str
    impact: str  # "high" | "medium" | "low"
    effort: str  # "quick" | "medium" | "involved"
    ksi_id: str | None = None


@dataclass(frozen=True)
class Worklist:
    """The full worklist: where you are, the single next step, the ranked items."""

    stage: str  # "uninitialized" | "unscanned" | "unclassified" | "classified"
    headline: str
    items: tuple[WorkItem, ...]
    activity: tuple[tuple[str, str], ...]  # (stage_label, "2d ago" | "not yet")
    overall_pct: float | None = None


def rank_work_items(items: list[WorkItem]) -> list[WorkItem]:
    """Impact first (high → low), then effort (quick → involved) so high-impact
    quick wins float to the top, then KSI id for stable ordering."""
    return sorted(
        items,
        key=lambda w: (_IMPACT_RANK[w.impact], _EFFORT_RANK[w.effort], w.ksi_id or ""),
    )


def classified_work_items(
    baseline_ksi_ids: list[str],
    procedural_ksi_ids: set[str],
    statuses: dict[str, str],
    *,
    manifest_covered: set[str],
    boundary_declared: bool,
) -> list[WorkItem]:
    """Build the ranked worklist for a classified workspace (pure — no I/O).

    - boundary undeclared → declare it (high impact, quick; gates a defensible posture)
    - not_implemented (non-procedural) → remediate (high impact, involved)
    - procedural KSI without a manifest → author one (quick)
    - partial → strengthen the evidence (medium)
    """
    items: list[WorkItem] = []

    if not boundary_declared:
        items.append(
            WorkItem(
                title="Declare your authorization boundary",
                why="Findings flow unfiltered until you declare scope.",
                command="efterlev boundary discover",
                impact="high",
                effort="quick",
            )
        )

    for ksi in baseline_ksi_ids:
        status = statuses.get(ksi)
        is_procedural = ksi in procedural_ksi_ids
        has_manifest = ksi in manifest_covered

        if (
            is_procedural
            and not has_manifest
            and status
            in (
                None,
                "not_implemented",
                "evidence_layer_inapplicable",
            )
        ):
            items.append(
                WorkItem(
                    title=f"Author a manifest for {ksi}",
                    why="Procedural KSI — needs a human-authored Evidence Manifest.",
                    command=f"efterlev manifests draft {ksi}",
                    impact="medium",
                    effort="quick",
                    ksi_id=ksi,
                )
            )
        elif status == "not_implemented":
            items.append(
                WorkItem(
                    title=f"Remediate {ksi}",
                    why="not_implemented — a HIGH-severity open in the POA&M.",
                    command=f"efterlev agent remediate --ksi {ksi}",
                    impact="high",
                    effort="involved",
                    ksi_id=ksi,
                )
            )
        elif status == "partial":
            items.append(
                WorkItem(
                    title=f"Strengthen {ksi}",
                    why="partial — evidence exists but doesn't fully satisfy the KSI yet.",
                    command=f"efterlev agent remediate --ksi {ksi}",
                    impact="medium",
                    effort="medium",
                    ksi_id=ksi,
                )
            )

    return rank_work_items(items)


def build_worklist(root: Path) -> Worklist:
    """Assemble the worklist for the workspace at `root` (stage-aware)."""
    root = Path(root)
    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"

    if not frmr_cache.is_file():
        return Worklist(
            stage="uninitialized",
            headline="Initialize a workspace — efterlev init",
            items=(
                WorkItem(
                    title="Discover your boundary first",
                    why="See the external dependencies your scope must account for first.",
                    command="efterlev boundary discover",
                    impact="high",
                    effort="quick",
                ),
                WorkItem(
                    title="Initialize the workspace",
                    why="Creates .efterlev/ and loads the FedRAMP 20x catalog.",
                    command="efterlev init --baseline fedramp-20x-moderate",
                    impact="high",
                    effort="quick",
                ),
            ),
            activity=(),
        )

    from efterlev.frmr import FrmrDocument
    from efterlev.primitives.readiness import compute_readiness, load_latest_claim_statuses

    frmr_doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    baseline = list(frmr_doc.indicators.keys())
    procedural = {k for k in baseline if k.startswith(_PROCEDURAL_PREFIXES)}

    report = compute_readiness(root, baseline_ksi_ids=baseline, procedural_ksi_ids=procedural)
    statuses = load_latest_claim_statuses(root, baseline_ksi_ids=set(baseline))
    activity = _activity(root)
    pct = report.score.overall_pct

    if report.detectors_fired == 0 and report.manifests_loaded == 0 and not statuses:
        return Worklist(
            stage="unscanned",
            headline="Scan your infrastructure-as-code — efterlev scan",
            items=(
                WorkItem(
                    title="Scan your IaC",
                    why="Deterministic detectors emit evidence for the 60 KSIs. No LLM, no key.",
                    command="efterlev scan",
                    impact="high",
                    effort="quick",
                ),
            ),
            activity=activity,
            overall_pct=pct,
        )

    if not statuses:
        return Worklist(
            stage="unclassified",
            headline="Classify the KSIs — efterlev agent gap",
            items=(
                WorkItem(
                    title="Classify the KSIs",
                    why="The Gap Agent turns the scanned evidence into per-KSI verdicts.",
                    command="efterlev agent gap",
                    impact="high",
                    effort="medium",
                ),
            ),
            activity=activity,
            overall_pct=pct,
        )

    items = classified_work_items(
        baseline,
        procedural,
        statuses,
        manifest_covered=_manifest_covered_ksis(root),
        boundary_declared=_boundary_declared(root),
    )

    if items:
        headline = f"{items[0].title} — {items[0].command}"
    else:
        headline = (
            "No open blockers. Confirm the gate (efterlev readiness --strict), "
            "then package for your 3PAO (efterlev submission package)."
        )

    return Worklist(
        stage="classified",
        headline=headline,
        items=tuple(items),
        activity=activity,
        overall_pct=pct,
    )


def _boundary_declared(root: Path) -> bool:
    try:
        from efterlev.config import load_config

        cfg = load_config(root / ".efterlev" / "config.toml")
    except Exception:
        return False
    boundary = getattr(cfg, "boundary", None)
    return bool(boundary and (boundary.include or boundary.exclude))


def _manifest_covered_ksis(root: Path) -> set[str]:
    # A procedural KSI counts as covered only when its manifest is *substantive*
    # (real attester + statement + cadence) — a scaffolded TODO stub keeps
    # showing up in the worklist until it's actually filled in.
    from efterlev.manifests.loader import discover_manifest_files, load_manifest_file
    from efterlev.manifests.substantiveness import is_substantive

    covered: set[str] = set()
    for f in discover_manifest_files(root / ".efterlev" / "manifests"):
        try:
            manifest = load_manifest_file(f)
        except Exception:
            continue
        if is_substantive(manifest):
            covered.add(manifest.ksi)
    return covered


def _activity(root: Path) -> tuple[tuple[str, str], ...]:
    from efterlev.paths import oscal_dir, poam_dir, reports_dir

    reports = reports_dir(root)
    stages = (
        ("scan", _latest_mtime(reports, "scan-*.json") or _latest_mtime(reports, "scan-*.html")),
        ("gap", _latest_mtime(reports, "gap-*.html")),
        ("poam", _latest_mtime(poam_dir(root), "poam-*.md")),
        ("oscal", _latest_mtime(oscal_dir(root), "*poam*.json")),
    )
    return tuple((label, _ago(ts)) for label, ts in stages)


def _latest_mtime(directory: Path, pattern: str) -> float | None:
    if not directory.is_dir():
        return None
    files = list(directory.glob(pattern))
    if not files:
        return None
    return max(f.stat().st_mtime for f in files)


def _ago(ts: float | None) -> str:
    if ts is None:
        return "not yet"
    delta = max(0.0, time.time() - ts)
    if delta < 90:
        return "just now"
    if delta < 3600:
        return f"{int(delta // 60)}m ago"
    if delta < 86400:
        return f"{int(delta // 3600)}h ago"
    return f"{int(delta // 86400)}d ago"
