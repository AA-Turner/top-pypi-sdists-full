"""RFC-0017 readiness gate — per-KSI checklist of the 5 PVA items.

[RFC-0017 (Persistent Validation and Assessment Standard)](https://www.fedramp.gov/rfcs/0017/)
names 5 required items per KSI:

  1. Implementation goal with pass/fail criteria
  2. Consolidated resource inventory being validated
  3. Automated validation processes + cadence
  4. Human validation processes + cadence
  5. Current status + clarifications

The existing `compute_readiness` (in `score.py`) reduces this to a
single heuristic percentage, useful for tracking progress but NOT
sufficient for the "are we ready to submit?" question. v0.1.167
adds `compute_rfc_0017_gate` which evaluates each KSI against the
5 items individually and returns pass/fail.

Use this for the pre-submission check; use `compute_readiness` for
the on-the-way-there progress signal.

## Item-by-item mapping

For each KSI in the baseline:

  1. **Implementation goal** — from FRMR catalog `Indicator.statement`.
     Always present when the catalog is loaded.
  2. **Consolidated inventory** — from Evidence records + manifest
     files. Passes when the KSI is cited by ≥1 Evidence record OR
     has a signed manifest at `.efterlev/manifests/`.
  3. **Automated cadence** — from `[cadence].machine_validation_cadence`.
     Workspace-level: passes when the config string is non-empty.
  4. **Human cadence** — from `[cadence].non_machine_validation_cadence`.
     Workspace-level: passes when the config string is non-empty.
  5. **Current status** — from Gap-Agent classifications. Passes when
     the KSI has a `KsiClassification` record. Any status counts;
     `not_implemented` is a valid current status.

Items 3 and 4 are workspace-level so they apply uniformly to every
KSI — if the workspace declares a machine cadence in `config.toml`,
every KSI passes item 3.

## Gate semantics

- **All 5 items pass per KSI → KSI passes**
- **Every KSI in the baseline passes → gate passes**
- **Any KSI fails any item → gate fails**

The CLI exits 0 on gate-pass, 2 on gate-fail. Pre-submission CI
should make `efterlev readiness --strict` a required check.

## Deliberate scope limits

- We do NOT evaluate the RFC-0017-recommended assessment-evidence
  fields (assessor identity, ongoing-assessment timestamp). Those
  are 3PAO-side; Efterlev produces the artifact, not the assessment.
- We do NOT enforce minimum evidence-count per KSI. A KSI with 1
  evidence record passes item 2; a KSI with 0 fails. Quality of
  evidence is the Gap Agent's classification job, not the gate's.
- We do NOT require the manifest to be CURRENT (per-manifest
  `next_review` date in the future). That's a separate compliance
  question; the gate is structural.
"""

from __future__ import annotations

import json
import sqlite3
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal

GateItem = Literal[
    "implementation_goal",
    "consolidated_inventory",
    "automated_validation_cadence",
    "human_validation_cadence",
    "current_status",
]
"""The 5 RFC-0017 required items, in canonical order."""

ALL_ITEMS: tuple[GateItem, ...] = (
    "implementation_goal",
    "consolidated_inventory",
    "automated_validation_cadence",
    "human_validation_cadence",
    "current_status",
)


@dataclass(frozen=True)
class KsiGateResult:
    """Per-KSI gate evaluation."""

    ksi_id: str
    passed_items: set[GateItem]
    failed_items: set[GateItem]
    # Optional per-failure detail for human-readable rendering. Keyed
    # by the failed item name. Pass-items don't get a detail.
    failure_details: dict[str, str] = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        """A KSI passes the gate iff every required item passes."""
        return len(self.failed_items) == 0


@dataclass(frozen=True)
class Rfc0017GateReport:
    """Workspace-level RFC-0017 gate evaluation."""

    ksi_results: list[KsiGateResult]
    machine_cadence_declared: str
    """The machine-cadence string from [cadence] in workspace config. Empty
    means item 3 fails universally."""
    human_cadence_declared: str
    """Counterpart for item 4."""
    baseline_ksi_count: int

    @property
    def passed(self) -> bool:
        """Gate passes iff every KSI passes."""
        return all(k.passed for k in self.ksi_results)

    @property
    def passing_count(self) -> int:
        return sum(1 for k in self.ksi_results if k.passed)

    @property
    def failing_count(self) -> int:
        return sum(1 for k in self.ksi_results if not k.passed)


def compute_rfc_0017_gate(
    root: Path,
    *,
    baseline_ksi_ids: list[str],
    machine_validation_cadence: str,
    human_validation_cadence: str,
) -> Rfc0017GateReport:
    """Evaluate every baseline KSI against the 5 RFC-0017 PVA items.

    Pure-read; no mutation. Same store-access posture as
    `compute_readiness`.

    `machine_validation_cadence` and `human_validation_cadence` are
    workspace-level — the caller pulls them from `Config.cadence`.
    Items 3 and 4 are evaluated by checking these are non-empty;
    every KSI gets the same verdict for those two items.
    """
    store_path = root / ".efterlev" / "store.db"
    manifests_dir = root / ".efterlev" / "manifests"

    # Item 5 source: per-KSI Gap-Agent classifications. Any classification
    # (including not_implemented) counts as "current status declared."
    classified_ksis = _load_classified_ksis(store_path, baseline_ksi_ids=set(baseline_ksi_ids))
    # Item 2 source A: per-KSI evidence citations. Build a map.
    evidence_citations = _load_ksi_evidence_citations(
        store_path, baseline_ksi_ids=set(baseline_ksi_ids)
    )
    # Item 2 source B: signed manifests. The manifest filename is keyed
    # by KSI id (e.g. `ksi-afr-fsi.yml`) per the v0.1.137 convention.
    manifest_ksi_ids = _load_manifest_ksi_ids(manifests_dir, set(baseline_ksi_ids))

    # Items 3 and 4 are workspace-level — same verdict for every KSI.
    machine_ok = bool(machine_validation_cadence and machine_validation_cadence.strip())
    human_ok = bool(human_validation_cadence and human_validation_cadence.strip())

    ksi_results: list[KsiGateResult] = []
    for ksi_id in baseline_ksi_ids:
        passed: set[GateItem] = set()
        failed: set[GateItem] = set()
        details: dict[str, str] = {}

        # Item 1: implementation goal — the FRMR catalog provides this.
        # Always passes when the catalog is loaded (caller is responsible
        # for ensuring `baseline_ksi_ids` are real catalog ids).
        passed.add("implementation_goal")

        # Item 2: consolidated inventory citation — evidence OR manifest.
        has_evidence = ksi_id in evidence_citations
        has_manifest = ksi_id in manifest_ksi_ids
        if has_evidence or has_manifest:
            passed.add("consolidated_inventory")
        else:
            failed.add("consolidated_inventory")
            details["consolidated_inventory"] = (
                "no Evidence record cites this KSI AND no signed manifest "
                f"at .efterlev/manifests/{ksi_id.lower()}.yml. Either run "
                "`efterlev scan` to surface IaC evidence, or author a manifest."
            )

        # Item 3: automated cadence — workspace-level.
        if machine_ok:
            passed.add("automated_validation_cadence")
        else:
            failed.add("automated_validation_cadence")
            details["automated_validation_cadence"] = (
                "[cadence].machine_validation_cadence is empty in "
                "workspace config.toml. Set a non-empty string describing "
                "how often automated validation runs (e.g., 'every PR via "
                "pr-compliance-scan.yml')."
            )

        # Item 4: human cadence — workspace-level.
        if human_ok:
            passed.add("human_validation_cadence")
        else:
            failed.add("human_validation_cadence")
            details["human_validation_cadence"] = (
                "[cadence].non_machine_validation_cadence is empty in "
                "workspace config.toml. Set a non-empty string describing "
                "how often human review runs (e.g., 'per-manifest "
                "next_review interval; quarterly minimum')."
            )

        # Item 5: current status — Gap-Agent classification.
        if ksi_id in classified_ksis:
            passed.add("current_status")
        else:
            failed.add("current_status")
            details["current_status"] = (
                "no Gap-Agent classification for this KSI. Run `efterlev agent gap` to classify."
            )

        ksi_results.append(
            KsiGateResult(
                ksi_id=ksi_id,
                passed_items=passed,
                failed_items=failed,
                failure_details=details,
            )
        )

    return Rfc0017GateReport(
        ksi_results=ksi_results,
        machine_cadence_declared=machine_validation_cadence,
        human_cadence_declared=human_validation_cadence,
        baseline_ksi_count=len(baseline_ksi_ids),
    )


# --- store + manifest readers (mirror `score.py` patterns) -----------


def _load_classified_ksis(store_path: Path, *, baseline_ksi_ids: set[str]) -> set[str]:
    """Return the set of KSI ids that have at least one classification.

    Mirrors `_load_latest_claims` in `score.py` but only returns the
    set of ksi_ids — we don't care about the status here, just whether
    the KSI has been classified (item 5 is "status declared", not
    "status is good").
    """
    if not store_path.is_file():
        return set()
    blob_dir = store_path.parent / "store"
    try:
        conn = sqlite3.connect(f"file:{store_path}?mode=ro", uri=True)
        try:
            cur = conn.cursor()
            cur.execute(
                "SELECT content_ref, metadata FROM provenance_records WHERE record_type = 'claim'"
            )
            rows = cur.fetchall()
        finally:
            conn.close()
    except sqlite3.Error:
        return set()

    classified: set[str] = set()
    for content_ref, metadata_str in rows:
        try:
            metadata = json.loads(metadata_str) if metadata_str else {}
        except (TypeError, json.JSONDecodeError):
            metadata = {}
        # Fast path: ksi_id is in metadata when the Gap Agent wrote the record.
        ksi_id = metadata.get("ksi_id") if isinstance(metadata, dict) else None
        if isinstance(ksi_id, str) and ksi_id in baseline_ksi_ids:
            classified.add(ksi_id)
            continue
        # Fallback: parse the blob if metadata didn't carry the id.
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
        ksi_id_blob = content.get("ksi_id")
        if isinstance(ksi_id_blob, str) and ksi_id_blob in baseline_ksi_ids:
            classified.add(ksi_id_blob)
    return classified


def _load_ksi_evidence_citations(store_path: Path, *, baseline_ksi_ids: set[str]) -> set[str]:
    """Return the set of KSI ids that are cited by at least one Evidence record.

    An Evidence record's `ksis_evidenced` array names which KSIs it
    contributes evidence toward. This drives item 2 of the gate.
    """
    if not store_path.is_file():
        return set()
    blob_dir = store_path.parent / "store"
    try:
        conn = sqlite3.connect(f"file:{store_path}?mode=ro", uri=True)
        try:
            cur = conn.cursor()
            cur.execute("SELECT content_ref FROM provenance_records WHERE record_type = 'evidence'")
            rows = cur.fetchall()
        finally:
            conn.close()
    except sqlite3.Error:
        return set()

    cited: set[str] = set()
    for (content_ref,) in rows:
        blob_path = blob_dir / content_ref
        if not blob_path.is_file():
            continue
        try:
            blob = json.loads(blob_path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            continue
        if not isinstance(blob, dict):
            continue
        # Detector-emitted Evidence has `ksis_evidenced` at top level.
        # Primitive-wrapper records ({"input":..., "output":...}) might
        # have it nested under output.evidence[]; handle both shapes.
        for ksi_id in _extract_ksi_ids(blob):
            if ksi_id in baseline_ksi_ids:
                cited.add(ksi_id)
    return cited


def _extract_ksi_ids(payload: dict[str, object]) -> list[str]:
    """Pull ksi ids from either top-level Evidence shape or nested wrapper."""
    result: list[str] = []
    top_level = payload.get("ksis_evidenced")
    if isinstance(top_level, list):
        result.extend(k for k in top_level if isinstance(k, str))
    output = payload.get("output")
    if isinstance(output, dict):
        nested_evidence = output.get("evidence")
        if isinstance(nested_evidence, list):
            for ev in nested_evidence:
                if isinstance(ev, dict):
                    nested_list = ev.get("ksis_evidenced")
                    if isinstance(nested_list, list):
                        result.extend(k for k in nested_list if isinstance(k, str))
    return result


def _load_manifest_ksi_ids(manifests_dir: Path, baseline_ksi_ids: set[str]) -> set[str]:
    """Return the KSI ids that have a signed manifest under `.efterlev/manifests/`.

    Manifests are named `<ksi-id-lowercase>.yml` per the v0.1.137 convention.
    A manifest's filename matters, not its content — content validation
    happens at `load_evidence_manifests` time, not here.
    """
    if not manifests_dir.is_dir():
        return set()
    manifest_ksis: set[str] = set()
    for path in manifests_dir.glob("*.yml"):
        stem = path.stem  # e.g. "ksi-afr-fsi"
        # Try uppercase variant (canonical FRMR form).
        upper = stem.upper()
        if upper in baseline_ksi_ids:
            manifest_ksis.add(upper)
    return manifest_ksis
