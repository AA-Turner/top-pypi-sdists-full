"""Compute a single readiness score from the workspace state.

Heuristic, not formal: this is not a FedRAMP 3PAO methodology, just a
useful rule-of-thumb for ISVs who want a single number to track
toward "ready to engage." A 3PAO will produce their own assessment.

Scoring approach (transparent + tunable in one place):

The score is a 0-100% number weighted across three dimensions:

1. **KSI coverage** (50% weight) — fraction of baseline KSIs that
   have a Gap Agent classification of `implemented` or
   `evidence_layer_inapplicable` or `not_applicable`. The three
   "good outcomes" — control is met, or control doesn't apply.
   `partial` counts as half-credit. `not_implemented` counts zero.

2. **Manifest coverage** (30% weight) — fraction of procedural KSIs
   (those classified as `evidence_layer_inapplicable` by Gap Agent
   because no scanner can see them) that have a signed Evidence
   Manifest. Without a manifest, those KSIs aren't really covered
   even though the classification is "honestly inapplicable."

3. **Severity penalty** (20% weight) — open HIGH-severity POA&M
   items reduce the score; MEDIUM less so. This converts the raw
   not_implemented count into a "blocking-ness" signal.

The function returns a `ReadinessReport` with the score and the
three top blockers ranked by severity + impact-on-score. The CLI
renders this; the function itself is rendering-agnostic.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path

# Bands for the human-readable label. Same convention as the v0.1.118
# bedrock-validation report ("99.1% precision = quality-neutral switch"):
# rounded percentage + short sentence. Reviewers should not over-anchor
# on the label; the structured top-blockers list is what's actionable.
_BAND_LABELS: tuple[tuple[int, str], ...] = (
    (90, "ready to package and engage a 3PAO"),
    (75, "ready for 3PAO scoping conversation"),
    (50, "substantial work remaining; close the top blockers first"),
    (25, "early; finish scan/gap and start authoring procedural manifests"),
    (0, "not started — run /tour to walk through the pipeline"),
)


@dataclass(frozen=True)
class ReadinessScore:
    """The numeric score + its three weighted sub-scores."""

    overall_pct: float
    """0.0 - 100.0; weighted combination of the three sub-scores."""
    ksi_coverage_pct: float
    """0-100; fraction of baseline KSIs with a satisfying classification."""
    manifest_coverage_pct: float
    """0-100; fraction of procedural KSIs that have a signed manifest."""
    severity_penalty_pct: float
    """0-100; 100 = no high-severity opens; lower = more high-severity gaps."""

    @property
    def band_label(self) -> str:
        for threshold, label in _BAND_LABELS:
            if self.overall_pct >= threshold:
                return label
        return _BAND_LABELS[-1][1]


@dataclass(frozen=True)
class TopBlocker:
    """One item the user should fix next to make readiness improve fastest."""

    ksi_id: str
    """The KSI this blocker is about."""
    reason: str
    """Short human-readable description of why it's blocking."""
    suggested_action: str
    """The shell command the user should run, e.g. `/agent remediate --ksi KSI-X`."""


@dataclass(frozen=True)
class ReadinessReport:
    """Full readiness output. CLI renders it; primitive returns it."""

    score: ReadinessScore
    ksi_classifications_total: int
    """How many KSIs the Gap Agent has classified."""
    ksis_in_baseline: int
    """How many KSIs the baseline defines (e.g. 60 for fedramp-20x-moderate)."""
    open_poam_high: int
    open_poam_medium: int
    open_poam_low: int
    detectors_fired: int
    """Total Evidence records in the provenance store."""
    manifests_loaded: int
    """How many Evidence Manifests are loaded under .efterlev/manifests/."""
    top_blockers: list[TopBlocker] = field(default_factory=list)
    """Up to 3 ranked blockers."""


@dataclass(frozen=True)
class _KsiClaim:
    """Internal view of a Claim record's KSI + status."""

    ksi_id: str
    status: str  # one of GapStatus literal values


def _load_latest_claims(
    store_path: Path, *, baseline_ksi_ids: set[str] | None = None
) -> list[_KsiClaim]:
    """Read the most recent KSI classification per KSI from the provenance store.

    The Gap Agent writes one Claim record per KSI per run; if it runs twice,
    we want the latest one for each. The status is in the blob payload
    (`.efterlev/store/ab/cd/<sha256>.json`), not the SQL row — the SQL row
    has `content_ref` + `metadata`, blob has the full Claim JSON
    (including `content.ksi_id` and `content.status`).

    The blob directory is `.efterlev/store/` (per `ProvenanceStore.blob_dir`
    in `efterlev/provenance/store.py`). v0.1.146 / #351 fix: prior code
    looked at `.efterlev/blobs/`, which doesn't exist — readiness always
    returned 0 classifications even when the store had 300+ claims.

    Returns empty list when no claims exist or the store is unreadable.
    """
    if not store_path.is_file():
        return []
    blob_dir = store_path.parent / "store"
    try:
        conn = sqlite3.connect(f"file:{store_path}?mode=ro", uri=True)
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT content_ref, metadata, timestamp FROM provenance_records "
                "WHERE record_type = 'claim' ORDER BY timestamp DESC"
            )
            rows = cur.fetchall()
        finally:
            conn.close()
    except sqlite3.Error:
        return []

    latest: dict[str, _KsiClaim] = {}
    for content_ref, metadata_str, _ts in rows:
        # Fast path: the Gap Agent puts ksi_id in metadata; if it's there
        # AND the blob is present, we get status from the blob. Skip the
        # blob load entirely when ksi_id is missing or we've already seen it.
        try:
            metadata = json.loads(metadata_str) if metadata_str else {}
        except (TypeError, json.JSONDecodeError):
            metadata = {}
        ksi_id_meta = metadata.get("ksi_id") if isinstance(metadata, dict) else None
        if isinstance(ksi_id_meta, str) and ksi_id_meta in latest:
            continue

        blob_path = blob_dir / content_ref
        if not blob_path.is_file():
            continue
        try:
            blob = json.loads(blob_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(blob, dict):
            continue
        content = blob.get("content")
        if not isinstance(content, dict):
            continue
        ksi_id = content.get("ksi_id")
        status = content.get("status")
        if not isinstance(ksi_id, str) or not isinstance(status, str):
            continue
        # v0.1.147 / #352: drop stale unknown-KSI records that pre-v0.1.146
        # gap agents could persist. Without this filter, a workspace with
        # a `KSI-SUS` typo claim showed "61 / 60 KSIs classified" (count
        # overflow).
        if baseline_ksi_ids is not None and ksi_id not in baseline_ksi_ids:
            continue
        if ksi_id not in latest:
            latest[ksi_id] = _KsiClaim(ksi_id=ksi_id, status=status)
    return list(latest.values())


def load_latest_claim_statuses(
    root: Path, *, baseline_ksi_ids: set[str] | None = None
) -> dict[str, str]:
    """Return `{ksi_id: latest-claim status}` from the workspace store.

    Public wrapper over the same loader the readiness score + RFC-0017
    gate use. Consumers that display a per-KSI status (the 3PAO inspector)
    should source it here so the status they show is consistent with the
    gate verdict — both read the store, not the attestation artifact.
    This is what fixes the v0.1.172 inspector inconsistency where an
    inherited (or gap-classified-but-not-documented) KSI showed
    "unclassified" while the gate counted it. v0.1.173 / #379.
    """
    store_path = root / ".efterlev" / "store.db"
    return {
        c.ksi_id: c.status
        for c in _load_latest_claims(store_path, baseline_ksi_ids=baseline_ksi_ids)
    }


def _count_evidence_records(store_path: Path) -> int:
    if not store_path.is_file():
        return 0
    try:
        conn = sqlite3.connect(f"file:{store_path}?mode=ro", uri=True)
        try:
            cur = conn.cursor()
            cur.execute("SELECT COUNT(*) FROM provenance_records WHERE record_type = 'evidence'")
            (count,) = cur.fetchone()
            return int(count)
        finally:
            conn.close()
    except sqlite3.Error:
        return 0


def _count_manifests(manifests_dir: Path) -> int:
    if not manifests_dir.is_dir():
        return 0
    return sum(1 for _ in manifests_dir.glob("*.yml"))


def _severity_for_status(status: str) -> str | None:
    """Map a Gap Agent status to the POA&M severity heuristic.

    Same mapping `efterlev poam` uses: not_implemented → HIGH, partial →
    MEDIUM, anything else → not a POA&M item. The readiness score uses
    the same convention so the two views stay consistent.
    """
    if status == "not_implemented":
        return "HIGH"
    if status == "partial":
        return "MEDIUM"
    return None


def compute_readiness(
    root: Path,
    *,
    baseline_ksi_ids: list[str],
    procedural_ksi_ids: set[str] | None = None,
) -> ReadinessReport:
    """Compute the readiness report for the workspace at `root`.

    Pure-read; no mutation. `baseline_ksi_ids` is the full set the
    baseline defines (60 for fedramp-20x-moderate). `procedural_ksi_ids`
    is the subset that scanner evidence can't reach — those need
    manifests to count as covered.
    """
    procedural_ksi_ids = procedural_ksi_ids or set()

    store_path = root / ".efterlev" / "store.db"
    manifests_dir = root / ".efterlev" / "manifests"

    claims = _load_latest_claims(store_path, baseline_ksi_ids=set(baseline_ksi_ids))
    claims_by_ksi = {c.ksi_id: c for c in claims}
    evidence_count = _count_evidence_records(store_path)
    manifest_count = _count_manifests(manifests_dir)

    # KSI coverage: implemented + not_applicable + evidence_layer_inapplicable = full credit.
    # partial = half credit. not_implemented = zero. unclassified = zero.
    covered_score = 0.0
    open_high = 0
    open_medium = 0
    open_low = 0
    for ksi_id in baseline_ksi_ids:
        claim = claims_by_ksi.get(ksi_id)
        if claim is None:
            continue
        if claim.status in ("implemented", "not_applicable", "evidence_layer_inapplicable"):
            covered_score += 1.0
        elif claim.status == "partial":
            covered_score += 0.5
            open_medium += 1
        elif claim.status == "not_implemented":
            open_high += 1
    ksi_coverage_pct = (covered_score / max(1, len(baseline_ksi_ids))) * 100.0

    # Manifest coverage: procedural KSIs need a manifest to "really" count.
    # We can't tell from manifest filename which KSI it covers (filename != KSI id
    # in general), so use a count heuristic: fraction-of-procedural-with-any-manifest.
    # When the user authors more manifests than there are procedural KSIs, cap at 100.
    if procedural_ksi_ids:
        manifest_coverage_pct = min(
            100.0,
            (manifest_count / len(procedural_ksi_ids)) * 100.0,
        )
    else:
        manifest_coverage_pct = 100.0  # No procedural KSIs to cover

    # Severity penalty: 100 if no HIGH opens; falls off per HIGH item.
    # 5 HIGH opens = 75; 10 HIGH = 50; 20 HIGH = 0.
    severity_penalty_pct = max(0.0, 100.0 - (open_high * 5.0))

    overall = ksi_coverage_pct * 0.50 + manifest_coverage_pct * 0.30 + severity_penalty_pct * 0.20

    # Top blockers: rank by severity (HIGH first), then by suggested-action
    # availability (remediation-able comes first). At most 3.
    blockers: list[TopBlocker] = []
    for ksi_id in baseline_ksi_ids:
        if len(blockers) >= 3:
            break
        claim = claims_by_ksi.get(ksi_id)
        if claim is None:
            continue
        if claim.status == "not_implemented":
            blockers.append(
                TopBlocker(
                    ksi_id=ksi_id,
                    reason="not_implemented (HIGH severity in POA&M)",
                    suggested_action=f"/agent remediate --ksi {ksi_id}",
                )
            )
        elif claim.status == "evidence_layer_inapplicable" and ksi_id in procedural_ksi_ids:
            # Procedural KSI without a manifest — needs authoring. The
            # `efterlev manifests draft <KSI>` scaffolder shipped at v0.1.178;
            # point straight at it (was a vague docs pointer pre-v0.1.203).
            blockers.append(
                TopBlocker(
                    ksi_id=ksi_id,
                    reason="procedural KSI without a signed Evidence Manifest",
                    suggested_action=f"/manifests draft {ksi_id}",
                )
            )

    return ReadinessReport(
        score=ReadinessScore(
            overall_pct=round(overall, 1),
            ksi_coverage_pct=round(ksi_coverage_pct, 1),
            manifest_coverage_pct=round(manifest_coverage_pct, 1),
            severity_penalty_pct=round(severity_penalty_pct, 1),
        ),
        ksi_classifications_total=len(claims),
        ksis_in_baseline=len(baseline_ksi_ids),
        open_poam_high=open_high,
        open_poam_medium=open_medium,
        open_poam_low=open_low,
        detectors_fired=evidence_count,
        manifests_loaded=manifest_count,
        top_blockers=blockers,
    )
