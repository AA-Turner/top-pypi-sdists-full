"""`generate_vdr_report` primitive — deterministic Vulnerability Detection
& Response (VDR) report assembly.

VDR is the artifact FedRAMP 20x is moving to as a replacement for the
traditional POA&M, per [RFC-0012 Continuous Vulnerability Management
Standard](https://www.fedramp.gov/rfcs/0012/) (closed for public comment
2025-08-21; signaling clearly though still draft). The RFC reframes the
ConMon output from "tracked items to remediate someday" to "vulnerabilities
detected with explicit timelines for mitigation/remediation."

We ship this AHEAD of RFC-0012 finalization so when it lands (likely
Q3 2026 ahead of Phase 3 wide-submission opening), Efterlev already
emits the right artifact. Versioned via `vdr_version` so when the RFC
shape shifts between draft and final, we can adapt without breaking
existing customers.

Required fields per RFC-0012:
- Internal identifier + CVE IDs
- Detection / mitigation / remediation timelines
- Internet-reachability status
- Exploitability and impact assessments
- Mitigation/remediation plans and actions taken

Timeframes the RFC defines (we surface but don't enforce):
- Internet-reachable + credibly exploitable: 3 days
- Non-internet-reachable + credibly exploitable: 7-21 days
- Monthly reporting minimum (continuous preferred)

**Deterministic: no LLM involvement.** Every field is either derived
from the gap classification + Evidence content, or emitted as a clearly-
marked DRAFT placeholder a qualified reviewer must fill before submission.
Mirrors `generate_poam_markdown` posture; mappings between the two are
documented in the field-level comments below.

**Open items only.** `implemented` and `not_applicable` classifications
produce no VDR entries — by definition, those don't represent
vulnerabilities. Every `partial` and `not_implemented` classification
becomes one VDR entry. `evidence_layer_inapplicable` is also skipped
(SPEC-57.1 coverage statement, not a vulnerability).
"""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field

from efterlev.models import Indicator
from efterlev.primitives.base import primitive

# Output schema version. Pin so consumers can detect breaking changes
# when RFC-0012 finalizes and we revise the shape.
VDR_SCHEMA_VERSION = "0.1.0-draft-rfc-0012"
RFC_REFERENCE = "RFC-0012 (closed 2025-08-21; ahead-of-finalization shape)"

# Only classifications in these two statuses produce VDR entries.
_STATUS_IN_SCOPE = {"partial", "not_implemented"}

# Severity mapping. Same heuristic as POA&M for cross-artifact consistency.
_SEVERITY_FOR_STATUS = {
    "not_implemented": "HIGH",
    "partial": "MEDIUM",
}

# RFC-0012 timeframes for mitigation/remediation. We surface these as
# defaults but don't pretend to know whether each detection is genuinely
# internet-reachable or credibly exploitable — that's reviewer judgment.
# These constants give the reviewer the right ballpark to start from.
_DAYS_REACHABLE_EXPLOITABLE = 3
_DAYS_NONREACHABLE_HIGH = 7
_DAYS_NONREACHABLE_MEDIUM = 21

_DRAFT_PLACEHOLDER = "DRAFT — SET BEFORE SUBMISSION"

VdrOutputFormat = Literal["json", "markdown"]


class VdrClassificationInput(BaseModel):
    """Minimal shape needed from a KsiClassification to emit a VDR entry.

    Parallel to `PoamClassificationInput` — same architectural decoupling
    at the primitive boundary. CLI loops over Gap-Agent classifications
    and constructs these by picking fields.
    """

    model_config = ConfigDict(frozen=True)

    ksi_id: str
    status: str
    rationale: str
    evidence_ids: list[str] = Field(default_factory=list)
    claim_record_id: str | None = None
    # CVE IDs cited by the underlying detector evidence (when available).
    # Today this is empty for the IaC layer — detectors don't yet emit
    # CVE references. Runtime-evidence imports (Security Hub ASFF,
    # Prowler) DO carry CVE IDs in their finding payloads; the CLI
    # populates this list from those records when present. v0.1.162
    # ships the field and accepts populated lists; the population path
    # from Security Hub findings lands in v0.1.163.
    cve_ids: list[str] = Field(default_factory=list)


class GenerateVdrReportInput(BaseModel):
    """Input to `generate_vdr_report`."""

    model_config = ConfigDict(frozen=True)

    classifications: list[VdrClassificationInput]
    indicators: dict[str, Indicator]
    baseline_id: str
    frmr_version: str
    # Generated-at timestamp — frozen at construction so the primitive
    # is deterministic. Same inputs → same JSON output.
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    # Output format. JSON is the canonical machine-readable shape;
    # markdown is a 3PAO-readable view. CLI calls the primitive twice
    # when both are requested (same input → both formats).
    output_format: VdrOutputFormat = "json"
    # Count of KSI classifications dropped by the boundary filter (same
    # surface as the POA&M generator).
    out_of_boundary_excluded_count: int = 0


class VdrEntry(BaseModel):
    """One VDR entry — RFC-0012 shape, ahead-of-finalization version.

    Fields are named per the RFC-0012 list. The schema version pins
    the field shape so when the RFC finalizes and the names/structure
    shift, we can detect old vs new on the reader side.
    """

    model_config = ConfigDict(frozen=True)

    # RFC-0012 §required: internal identifier
    internal_id: str
    # RFC-0012 §required: CVE IDs (may be empty when the underlying
    # evidence is detector-only with no CVE reference)
    cve_ids: list[str]
    # RFC-0012 §required: detection timestamp (when Efterlev's scan saw
    # the gap — surrogate for "when did we detect this vulnerability")
    detection_timestamp: str  # ISO-8601
    # RFC-0012 §required: mitigation deadline (timeframe heuristic — see
    # `mitigation_deadline_basis`)
    mitigation_deadline: str
    # RFC-0012 §required: remediation deadline
    remediation_deadline: str
    # RFC-0012 §required: internet-reachable status. We don't try to
    # infer this from IaC; reviewer marks. Defaulted to "REVIEW" so the
    # reviewer can't accidentally accept a draft as-is.
    internet_reachable: str  # "true" | "false" | "REVIEW"
    # RFC-0012 §required: exploitability assessment. Same DRAFT posture.
    exploitability: str
    # RFC-0012 §required: impact assessment. Derived from severity for
    # the heuristic; reviewer adjusts.
    impact: str
    # RFC-0012 §required: mitigation plan
    mitigation_plan: str
    # RFC-0012 §required: remediation plan
    remediation_plan: str
    # RFC-0012 §required: actions taken (initially empty for a fresh
    # detection; populated by the operator as remediation progresses).
    actions_taken: list[str]
    # RFC-0012 §implied: current status of the entry
    status: str  # "open" | "in_progress" | "mitigated" | "remediated"
    # --- traceability back to the source classification ---
    ksi_id: str
    severity: str
    rationale: str
    evidence_ids: list[str]
    # Basis for the deadline calculation, so a reviewer adjusting the
    # internet_reachable field knows which heuristic applied.
    mitigation_deadline_basis: str


class GenerateVdrReportOutput(BaseModel):
    """Output: VDR report (JSON or markdown) + per-entry count + skipped KSIs."""

    model_config = ConfigDict(frozen=True)

    # The rendered output. Caller writes this to disk.
    rendered: str
    output_format: VdrOutputFormat
    entry_count: int
    # KSIs skipped because the classification references an id that
    # isn't in the loaded indicator dict (same posture as POA&M).
    skipped_unknown_ksi: list[str] = Field(default_factory=list)
    # The structured VdrEntry list, returned alongside the rendered
    # output so downstream callers can re-use without re-parsing.
    entries: list[VdrEntry] = Field(default_factory=list)


@primitive(capability="generate", side_effects=False, version="0.1.0", deterministic=True)
def generate_vdr_report(input: GenerateVdrReportInput) -> GenerateVdrReportOutput:
    """Emit a VDR report from Gap-Agent classifications.

    Deterministic: same inputs → byte-identical output. No LLM call.
    Every entry corresponds to a `partial` or `not_implemented` KSI
    classification. `implemented`, `not_applicable`, and
    `evidence_layer_inapplicable` are skipped.

    Unknown-KSI classifications are reported in `skipped_unknown_ksi` —
    never fabricated into a VDR entry. Same posture as POA&M.
    """
    open_items = [c for c in input.classifications if c.status in _STATUS_IN_SCOPE]
    # Sort by severity (HIGH first), then KSI id for stability. Matches
    # POA&M default sort so the two artifacts read in the same order.
    open_items.sort(
        key=lambda c: (
            0 if c.status == "not_implemented" else 1,
            c.ksi_id,
        )
    )

    entries: list[VdrEntry] = []
    skipped: list[str] = []
    seen_skipped: set[str] = set()

    for idx, clf in enumerate(open_items):
        ind = input.indicators.get(clf.ksi_id)
        if ind is None:
            if clf.ksi_id not in seen_skipped:
                skipped.append(clf.ksi_id)
                seen_skipped.add(clf.ksi_id)
            continue
        entries.append(_build_entry(clf, ind, idx, input.generated_at))

    if input.output_format == "json":
        rendered = _render_json(
            entries=entries,
            baseline_id=input.baseline_id,
            frmr_version=input.frmr_version,
            generated_at=input.generated_at,
            out_of_boundary_excluded_count=input.out_of_boundary_excluded_count,
        )
    else:
        rendered = _render_markdown(
            entries=entries,
            baseline_id=input.baseline_id,
            frmr_version=input.frmr_version,
            generated_at=input.generated_at,
            out_of_boundary_excluded_count=input.out_of_boundary_excluded_count,
        )

    return GenerateVdrReportOutput(
        rendered=rendered,
        output_format=input.output_format,
        entry_count=len(entries),
        skipped_unknown_ksi=skipped,
        entries=entries,
    )


def _build_entry(
    clf: VdrClassificationInput,
    indicator: Indicator,
    idx: int,
    generated_at: datetime,
) -> VdrEntry:
    """Construct one VdrEntry from a classification + KSI indicator."""
    severity = _SEVERITY_FOR_STATUS.get(clf.status, "TBD")
    internal_id = _entry_id(clf, idx)
    detection_iso = generated_at.isoformat()

    # Default to the conservative "REVIEW" posture for internet-
    # reachability. IaC scanners CAN'T reliably determine this — a
    # bucket might be technically internet-reachable via a CloudFront
    # distribution that isn't in this Terraform stack. Don't pretend.
    internet_reachable = "REVIEW"
    # Conservative-default deadline calculation: assume non-reachable
    # at the severity tier (longer deadline). Reviewer adjusts when
    # marking internet_reachable=true (deadline tightens to 3 days).
    days = _DAYS_NONREACHABLE_HIGH if severity == "HIGH" else _DAYS_NONREACHABLE_MEDIUM
    deadline = (generated_at + timedelta(days=days)).date().isoformat()
    deadline_basis = (
        f"non-internet-reachable + {severity.lower()} severity ({days}d). "
        f"If reviewer marks internet_reachable=true and credibly_exploitable=true, "
        f"deadline tightens to {_DAYS_REACHABLE_EXPLOITABLE}d per RFC-0012."
    )

    return VdrEntry(
        internal_id=internal_id,
        cve_ids=list(clf.cve_ids),
        detection_timestamp=detection_iso,
        mitigation_deadline=deadline,
        remediation_deadline=deadline,
        internet_reachable=internet_reachable,
        exploitability=_DRAFT_PLACEHOLDER,
        impact=severity,
        mitigation_plan=_DRAFT_PLACEHOLDER,
        remediation_plan=_DRAFT_PLACEHOLDER,
        actions_taken=[],
        status="open",
        ksi_id=clf.ksi_id,
        severity=severity,
        rationale=clf.rationale,
        evidence_ids=list(clf.evidence_ids),
        mitigation_deadline_basis=deadline_basis,
    )


def _entry_id(clf: VdrClassificationInput, idx: int) -> str:
    """VDR entry id pattern: VDR-<KSI-ID>-<idx-zero-padded>.

    Parallel to POA&M's POAM-<KSI>-<idx> shape so the two artifacts
    cross-reference cleanly when shipped together.
    """
    return f"VDR-{clf.ksi_id}-{idx:03d}"


def _render_json(
    *,
    entries: list[VdrEntry],
    baseline_id: str,
    frmr_version: str,
    generated_at: datetime,
    out_of_boundary_excluded_count: int,
) -> str:
    """Emit the canonical machine-readable VDR JSON.

    Schema version is pinned via `vdr_schema_version` so consumers
    can detect breaking changes when RFC-0012 finalizes and the field
    shape moves.
    """
    import json

    doc = {
        "vdr_schema_version": VDR_SCHEMA_VERSION,
        "rfc_reference": RFC_REFERENCE,
        "baseline_id": baseline_id,
        "frmr_version": frmr_version,
        "generated_at": generated_at.isoformat(),
        "out_of_boundary_excluded_count": out_of_boundary_excluded_count,
        "entry_count": len(entries),
        "entries": [e.model_dump(mode="json") for e in entries],
        "_draft_notice": (
            "DRAFT — requires human review. Generated from Gap-Agent KSI "
            "classifications by the Efterlev VDR primitive. Every field marked "
            f'"{_DRAFT_PLACEHOLDER}" must be completed by a qualified reviewer '
            "before submission to any authorizing body. The 'REVIEW' value on "
            "internet_reachable must be replaced with a true/false judgment; "
            "the mitigation/remediation deadlines tighten to 3 days when "
            "marked internet-reachable + credibly-exploitable per RFC-0012."
        ),
    }
    return json.dumps(doc, indent=2, sort_keys=False) + "\n"


def _render_markdown(
    *,
    entries: list[VdrEntry],
    baseline_id: str,
    frmr_version: str,
    generated_at: datetime,
    out_of_boundary_excluded_count: int,
) -> str:
    """Emit a 3PAO-readable markdown view of the VDR.

    Same surface as `generate_poam_markdown._render_document`: header
    + summary table + per-entry detail section.
    """
    ts_iso = generated_at.isoformat()
    lines: list[str] = []
    lines.append(f"# VDR — {baseline_id}")
    lines.append("")
    lines.append(f"**Schema version:** `{VDR_SCHEMA_VERSION}`  ")
    lines.append(f"**RFC reference:** {RFC_REFERENCE}  ")
    lines.append("")
    lines.append(
        "**DRAFT — requires human review.** This VDR was generated from the "
        "Gap Agent's KSI classifications. Every field marked "
        f"`{_DRAFT_PLACEHOLDER}` must be completed by a qualified reviewer "
        "before submission to any authorizing body. The `REVIEW` value on "
        "`internet_reachable` must be replaced with a true/false judgment; "
        "mitigation/remediation deadlines tighten to 3 days when marked "
        "internet-reachable + credibly-exploitable per RFC-0012."
    )
    lines.append("")
    header_bullets = [
        f"- **Baseline:** {baseline_id}",
        f"- **FRMR version:** {frmr_version}",
        f"- **Generated:** {ts_iso}",
        f"- **Entry count:** {len(entries)}",
    ]
    if out_of_boundary_excluded_count > 0:
        header_bullets.append(
            f"- **Excluded as out-of-boundary:** "
            f"{out_of_boundary_excluded_count} item(s) (cited evidence is "
            f"entirely out_of_boundary; see `efterlev boundary show`)"
        )
    lines.append("  \n".join(header_bullets))
    lines.append("")

    if not entries:
        lines.append(
            "_No open VDR entries._ Every classified KSI is `implemented` or "
            "`not_applicable`; no `partial` or `not_implemented` findings to track."
        )
        lines.append("")
        return "\n".join(lines)

    lines.append("## Summary")
    lines.append("")
    lines.append(
        "| Internal ID | KSI | Severity | Internet-reachable | Mitigation deadline | Status |"
    )
    lines.append("|---|---|---|---|---|---|")
    for e in entries:
        lines.append(
            f"| `{e.internal_id}` | `{e.ksi_id}` | `{e.severity}` | "
            f"`{e.internet_reachable}` | `{e.mitigation_deadline}` | `{e.status}` |"
        )
    lines.append("")

    lines.append("## Entries")
    lines.append("")
    for e in entries:
        lines.extend(_render_entry_markdown(e))
        lines.append("")

    return "\n".join(lines)


def _render_entry_markdown(e: VdrEntry) -> list[str]:
    """Render one VDR entry as a self-contained markdown block."""
    cve_str = ", ".join(f"`{c}`" for c in e.cve_ids) if e.cve_ids else "_(none cited)_"
    evidence_str = (
        ", ".join(_short_id(eid) for eid in e.evidence_ids[:5])
        if e.evidence_ids
        else "_(none — classification has no cited evidence)_"
    )
    if len(e.evidence_ids) > 5:
        evidence_str += f", … (+{len(e.evidence_ids) - 5} more)"
    actions_str = (
        "\n".join(f"  - {a}" for a in e.actions_taken)
        if e.actions_taken
        else f"  - _{_DRAFT_PLACEHOLDER} (none recorded yet)_"
    )
    return [
        f"### {e.internal_id} — {e.ksi_id}",
        "",
        f"- **Detection timestamp:** `{e.detection_timestamp}`",
        f"- **CVE IDs:** {cve_str}",
        f"- **Severity:** `{e.severity}`",
        f"- **Impact:** `{e.impact}`",
        f"- **Internet-reachable:** `{e.internet_reachable}`",
        f"- **Exploitability:** {e.exploitability}",
        f"- **Mitigation deadline:** `{e.mitigation_deadline}`",
        f"- **Remediation deadline:** `{e.remediation_deadline}`",
        f"- **Deadline basis:** {e.mitigation_deadline_basis}",
        f"- **Mitigation plan:** {e.mitigation_plan}",
        f"- **Remediation plan:** {e.remediation_plan}",
        "- **Actions taken:**",
        actions_str,
        f"- **Status:** `{e.status}`",
        f"- **Evidence cited:** {evidence_str}",
        "",
        "**Detection rationale (from Gap Agent):**",
        "",
        f"> {e.rationale}",
    ]


def _short_id(evidence_id: str) -> str:
    """Render an Evidence id as a short, copy-pasteable prefix.

    Same format the POA&M markdown generator uses, so cross-referencing
    works visually.
    """
    if evidence_id.startswith("sha256:"):
        return f"`{evidence_id[: 7 + 8]}`"  # "sha256:" + 8 hex chars
    return f"`{evidence_id[:8]}`"
