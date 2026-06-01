"""`generate_inspector_report` — single-page HTML for 3PAO assessment review.

[RFC-0017 (Persistent Validation and Assessment Standard)](https://www.fedramp.gov/rfcs/0017/)
defines what an assessor needs to see per KSI: the 5 PVA items
(implementation goal, consolidated inventory, automated cadence,
human cadence, current status) plus supporting evidence + narrative.

The existing reports (gap_report.py + documentation_report.py) are
**customer-facing** — action-oriented for the team building the
system. The inspector view is **assessor-facing** — verification-
oriented for the 3PAO confirming the system meets RFC-0017.

## Shape

Single HTML page, no JS framework, no external assets. Survives email
attachment, archival, and airgapped review. Per-KSI rows render
collapsed by default (just id + status pill + 5-item checklist);
clicking expands to show statement + controls + cadence + evidence
citations + narrative.

## Data sources

- **FRMR document** (`.efterlev/cache/frmr_document.json`) — per-KSI
  statement, theme, mapped controls. Always required.
- **Attestation artifact** (`efterlev-out/reports/attestation-*.json`)
  — per-KSI narrative + citations + cadence + mode + status. Optional;
  rows without an attestation indicator still render with empty
  detail and a "no attestation generated yet" note.
- **Gate report** (computed inline from gate.py) — per-KSI RFC-0017
  pass/fail per item. Always required (cheap to compute).

The primitive is deterministic given the same inputs. Generated_at
is the only timestamp surfaced.

## Why a separate primitive rather than extending gap_report

gap_report renders **claim-oriented** detail (status + rationale per
KSI). The inspector mixes data sources gap_report doesn't read
(attestation narratives + RFC-0017 gate). A separate primitive
keeps gap_report's customer-facing shape stable while letting the
inspector evolve toward 3PAO needs without churn risk to existing
customers consuming gap_report.html.

## Deliberate scope

- We do NOT include raw evidence excerpts (config snippets, IAM JSON
  bodies). Risk of leaking secrets. file:line citations + manifest
  excerpts only.
- We do NOT compute a "ready/not-ready" verdict beyond what the gate
  reports. Assessor reads the gate verdict + per-KSI checklist; their
  professional judgment is the verdict.
- We do NOT mutate the workspace. Pure read.
"""

from __future__ import annotations

from datetime import UTC, datetime
from typing import Literal

from markupsafe import Markup, escape
from pydantic import BaseModel, ConfigDict, Field

from efterlev.models.attestation_artifact import (
    AttestationArtifact,
    AttestationArtifactIndicator,
)
from efterlev.primitives.base import primitive
from efterlev.primitives.readiness import ALL_ITEMS, Rfc0017GateReport
from efterlev.reports.html import render_base_document

INSPECTOR_SCHEMA_VERSION = "0.1.0"

# UI labels for the 5 RFC-0017 items, in canonical order. Short for the
# inline 5-dot checklist; long for the expanded-row detail.
_ITEM_SHORT_LABELS: dict[str, str] = {
    "implementation_goal": "goal",
    "consolidated_inventory": "inventory",
    "automated_validation_cadence": "machine-cadence",
    "human_validation_cadence": "human-cadence",
    "current_status": "status",
}

_ITEM_LONG_LABELS: dict[str, str] = {
    "implementation_goal": "Implementation goal",
    "consolidated_inventory": "Consolidated resource inventory",
    "automated_validation_cadence": "Automated validation + cadence",
    "human_validation_cadence": "Human validation + cadence",
    "current_status": "Current status",
}


class InspectorKsiRow(BaseModel):
    """Per-KSI row in the inspector view.

    Composed from the FRMR catalog (statement, theme, controls_mapped),
    the attestation artifact (narrative, citations, cadence, status —
    when present), and the gate report (per-item pass/fail).
    """

    model_config = ConfigDict(frozen=True)

    ksi_id: str
    theme: str
    statement: str
    controls_mapped: list[str] = Field(default_factory=list)

    # From attestation artifact when available.
    status: str | None = None
    narrative: str | None = None
    citations: list[str] = Field(default_factory=list)
    controls_evidenced: list[str] = Field(default_factory=list)
    machine_validation_cadence: str | None = None
    non_machine_validation_cadence: str | None = None
    attestation_mode: str | None = None

    # From gate report.
    gate_passed: bool
    gate_passed_items: list[str] = Field(default_factory=list)
    gate_failed_items: list[str] = Field(default_factory=list)

    @property
    def has_attestation(self) -> bool:
        return self.narrative is not None or self.status is not None


class GenerateInspectorReportInput(BaseModel):
    """Input: catalog + attestation (optional) + gate verdict."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    # Per-KSI catalog data. Each entry: {"ksi_id", "theme", "statement",
    # "controls_mapped"}. Caller pulls from the loaded FrmrDocument.
    catalog_entries: list[dict[str, object]]
    # Loaded attestation artifact. None = no artifact yet (fresh workspace
    # that ran `init` + `scan` but not yet `agent document`).
    attestation: AttestationArtifact | None = None
    # v0.1.173 / #379: per-KSI status from the latest STORE claim (the same
    # source the RFC-0017 gate reads). Authoritative for the status pill —
    # the attestation is only an enrichment (narrative/citations) and may
    # lag the store (e.g. `scope apply` writes an inherited claim with no
    # attestation; `agent gap` without `agent document` likewise). Keying
    # the pill off the store keeps it consistent with the gate dots in the
    # same row. Empty dict → fall back to the attestation status.
    store_statuses: dict[str, str] = Field(default_factory=dict)
    gate_report: Rfc0017GateReport
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    workspace_label: str = "workspace"
    profile_label: str | None = None
    baseline_id: str = "fedramp-20x-moderate"
    tool_version: str = ""


class GenerateInspectorReportOutput(BaseModel):
    """Output: rendered HTML + structured rows."""

    model_config = ConfigDict(frozen=True)

    rendered: str
    output_format: Literal["html"] = "html"
    rows: list[InspectorKsiRow]
    passing_count: int
    failing_count: int


@primitive(
    capability="generate",
    side_effects=False,
    version=INSPECTOR_SCHEMA_VERSION,
    deterministic=True,
)
def generate_inspector_report(
    input: GenerateInspectorReportInput,
) -> GenerateInspectorReportOutput:
    """Assemble the 3PAO inspector HTML view.

    Deterministic: same inputs → byte-identical output (modulo the
    `generated_at` timestamp surfaced in the page header).
    """
    # Lookup tables for fast per-KSI assembly.
    attestation_by_ksi = _flatten_attestation_indicators(input.attestation)
    gate_by_ksi = {k.ksi_id: k for k in input.gate_report.ksi_results}

    rows: list[InspectorKsiRow] = []
    for entry in input.catalog_entries:
        ksi_id = str(entry.get("ksi_id", ""))
        if not ksi_id:
            continue
        theme = str(entry.get("theme", "?"))
        statement = str(entry.get("statement", ""))
        controls_mapped_raw = entry.get("controls_mapped", [])
        controls_mapped = (
            [str(c) for c in controls_mapped_raw if isinstance(c, str)]
            if isinstance(controls_mapped_raw, list)
            else []
        )

        gate = gate_by_ksi.get(ksi_id)
        if gate is None:
            # Defensive: KSI in catalog but not evaluated by gate. Mark as
            # failing (caller likely passed a stale gate report).
            gate_passed = False
            gate_passed_items: list[str] = []
            gate_failed_items = list(ALL_ITEMS)
        else:
            gate_passed = gate.passed
            gate_passed_items = sorted(gate.passed_items)
            gate_failed_items = sorted(gate.failed_items)

        att = attestation_by_ksi.get(ksi_id)
        citations: list[str] = []
        if att is not None:
            for c in att.citations:
                # AttestationCitation has source_file (str) +
                # source_lines (str | None, e.g. "12-24"). Compose to
                # "path:lines" or just "path" when no line range.
                file_line = c.source_file
                if c.source_lines:
                    file_line += f":{c.source_lines}"
                citations.append(file_line)

        # Status pill: the STORE claim is authoritative (it's what the gate
        # reads), so it wins. Fall back to the attestation status only when
        # the store has no claim for this KSI. Keeps the pill consistent
        # with the gate dots in the same row (v0.1.173 fix).
        row_status = input.store_statuses.get(ksi_id) or (att.status if att else None)

        rows.append(
            InspectorKsiRow(
                ksi_id=ksi_id,
                theme=theme,
                statement=statement,
                controls_mapped=controls_mapped,
                status=row_status,
                narrative=att.narrative if att else None,
                citations=citations,
                controls_evidenced=list(att.controls_evidenced) if att else [],
                machine_validation_cadence=(att.machine_validation_cadence if att else None),
                non_machine_validation_cadence=(
                    att.non_machine_validation_cadence if att else None
                ),
                attestation_mode=att.mode if att else None,
                gate_passed=gate_passed,
                gate_passed_items=gate_passed_items,
                gate_failed_items=gate_failed_items,
            )
        )

    passing = sum(1 for r in rows if r.gate_passed)
    failing = len(rows) - passing

    rendered = _render_html(
        rows=rows,
        gate_report=input.gate_report,
        generated_at=input.generated_at,
        workspace_label=input.workspace_label,
        profile_label=input.profile_label,
        baseline_id=input.baseline_id,
        tool_version=input.tool_version,
        passing=passing,
        failing=failing,
    )

    return GenerateInspectorReportOutput(
        rendered=rendered,
        rows=rows,
        passing_count=passing,
        failing_count=failing,
    )


def _flatten_attestation_indicators(
    artifact: AttestationArtifact | None,
) -> dict[str, AttestationArtifactIndicator]:
    """Walk the theme-nested artifact and return {ksi_id: indicator}.

    Returns an empty dict when artifact is None or has no themes.
    """
    out: dict[str, AttestationArtifactIndicator] = {}
    if artifact is None:
        return out
    for theme in artifact.KSI.values():
        for ksi_id, indicator in theme.indicators.items():
            out[ksi_id] = indicator
    return out


# --- HTML rendering ----------------------------------------------------


def _render_html(
    *,
    rows: list[InspectorKsiRow],
    gate_report: Rfc0017GateReport,
    generated_at: datetime,
    workspace_label: str,
    profile_label: str | None,
    baseline_id: str,
    tool_version: str,
    passing: int,
    failing: int,
) -> str:
    """Compose the inspector HTML body and wrap with the shared scaffold."""
    body_parts: list[str] = []
    body_parts.append(_render_header_banner(gate_report, passing, failing))
    body_parts.append(_render_workspace_meta(workspace_label, profile_label, baseline_id))
    body_parts.append(_render_per_item_summary(rows))
    body_parts.append(_render_ksi_rows(rows))
    body_parts.append(_render_how_to_verify(tool_version))

    # nosec B704: every `_render_*` helper either calls `escape()` on
    # caller-controlled strings (workspace_label, narrative, citations,
    # statement, controls) or emits fixed HTML/CSS literals. The Markup
    # wrap marks the composed body as "already escaped" for the Jinja
    # consumer in `render_base_document` — same defensive pattern as
    # the other report renderers in src/efterlev/reports/.
    body_html = Markup("".join(body_parts))  # nosec B704

    subtitle = (
        "Single-page view for the 3PAO assessor. Each baseline KSI is one row; "
        "click to expand. RFC-0017 PVA items: implementation goal, consolidated "
        "inventory, automated cadence, human cadence, current status."
    )

    return render_base_document(
        title="3PAO Inspector — RFC-0017 readiness",
        body_html=body_html,
        generated_at=generated_at.isoformat(),
        subtitle=subtitle,
    )


def _render_header_banner(gate_report: Rfc0017GateReport, passing: int, failing: int) -> str:
    """The top verdict banner — green PASS or red FAIL with counts."""
    if gate_report.passed:
        cls = "verdict-pass"
        verdict = "PASS"
        msg = (
            f"All {passing} baseline KSIs meet the 5 RFC-0017 PVA items. The "
            "structural gate is satisfied; assessor judgment determines the "
            "submission verdict."
        )
    else:
        cls = "verdict-fail"
        verdict = "FAIL"
        msg = (
            f"{failing} of {passing + failing} baseline KSIs fail one or more "
            "RFC-0017 PVA items. Per-item failure counts and per-KSI detail "
            "below."
        )
    return (
        f'<div class="verdict-banner {cls}">'
        f'<div class="verdict-label">RFC-0017 gate: <strong>{verdict}</strong></div>'
        f'<div class="verdict-msg">{escape(msg)}</div>'
        "</div>" + _VERDICT_STYLESHEET
    )


def _render_workspace_meta(
    workspace_label: str, profile_label: str | None, baseline_id: str
) -> str:
    """Workspace identity block — what was scanned."""
    profile_html = (
        f" &middot; Profile: <code>{escape(profile_label)}</code>" if profile_label else ""
    )
    return (
        '<p class="meta">'
        f"Workspace: <code>{escape(workspace_label)}</code>{profile_html} "
        f"&middot; Baseline: <code>{escape(baseline_id)}</code>"
        "</p>"
    )


def _render_per_item_summary(rows: list[InspectorKsiRow]) -> str:
    """Per-item rollup — quickly see which item drives the most failures."""
    counts: dict[str, int] = {item: 0 for item in ALL_ITEMS}
    for row in rows:
        for failed in row.gate_failed_items:
            if failed in counts:
                counts[failed] += 1
    cells: list[str] = []
    for item in ALL_ITEMS:
        c = counts[item]
        label = _ITEM_LONG_LABELS[item]
        if c == 0:
            cells.append(
                '<div class="item-cell item-cell-ok">'
                f'<div class="item-name">{escape(label)}</div>'
                '<div class="item-stat">all pass</div>'
                "</div>"
            )
        else:
            cells.append(
                '<div class="item-cell item-cell-fail">'
                f'<div class="item-name">{escape(label)}</div>'
                f'<div class="item-stat">{c} failing</div>'
                "</div>"
            )
    return (
        "<h2>Per-item summary</h2>"
        f'<div class="item-grid">{"".join(cells)}</div>' + _ITEM_GRID_STYLESHEET
    )


def _render_ksi_rows(rows: list[InspectorKsiRow]) -> str:
    """Per-KSI collapsible rows, grouped by theme prefix."""
    grouped: dict[str, list[InspectorKsiRow]] = {}
    for row in rows:
        grouped.setdefault(row.theme, []).append(row)

    parts: list[str] = ["<h2>Per-KSI checklist</h2>"]
    for theme in sorted(grouped.keys()):
        theme_rows = grouped[theme]
        parts.append(
            f'<h3 class="theme-h3">{escape(theme)} '
            f'<span class="theme-count">({len(theme_rows)} KSIs)</span></h3>'
        )
        for row in theme_rows:
            parts.append(_render_one_row(row))
    parts.append(_KSI_ROW_STYLESHEET)
    return "".join(parts)


def _render_one_row(row: InspectorKsiRow) -> str:
    """One collapsible <details> per KSI.

    Default-collapsed; click summary to expand. Summary shows id + status
    pill + 5-item dot row. Expanded shows statement + controls + cadence
    + citations + narrative.
    """
    # Status pill — none-classified gets a plain pill rather than the
    # color-coded ones from html.py.
    status_class = f"status-{row.status}" if row.status else "status-unclassified"
    status_label = (row.status or "unclassified").replace("_", " ")
    # 5-dot RFC-0017 checklist row.
    dots = "".join(_dot_for_item(row, item) for item in ALL_ITEMS)
    # Top-level summary chrome.
    summary = (
        "<summary>"
        f'<span class="ksi-id">{escape(row.ksi_id)}</span>'
        f'<span class="status-pill {escape(status_class)}">{escape(status_label)}</span>'
        f'<span class="rfc-dots">{dots}</span>'
        "</summary>"
    )

    # Expanded detail body.
    detail_parts: list[str] = []
    detail_parts.append(f'<p class="ksi-statement">{escape(row.statement)}</p>')

    # Controls — mapped + evidenced. SPEC-57.2 distinguishes them; surface
    # both lists so the assessor sees both "what FRMR maps" and "what
    # the scan evidenced."
    detail_parts.append(_render_controls_block(row))
    detail_parts.append(_render_cadence_block(row))
    detail_parts.append(_render_citations_block(row))
    detail_parts.append(_render_narrative_block(row))
    detail_parts.append(_render_failure_block(row))

    open_attr = "" if row.gate_passed else " open"
    row_cls = "ksi-row " + ("ksi-pass" if row.gate_passed else "ksi-fail")
    return (
        f'<details class="{row_cls}"{open_attr}>'
        + summary
        + '<div class="ksi-detail">'
        + "".join(detail_parts)
        + "</div>"
        + "</details>"
    )


def _dot_for_item(row: InspectorKsiRow, item: str) -> str:
    """Render a single ✓ / ✗ dot with title-tooltip for an item."""
    short = _ITEM_SHORT_LABELS[item]
    if item in row.gate_passed_items:
        return f'<span class="rfc-dot rfc-dot-pass" title="{escape(short)}: pass">&#10003;</span>'
    return f'<span class="rfc-dot rfc-dot-fail" title="{escape(short)}: fail">&#10007;</span>'


def _render_controls_block(row: InspectorKsiRow) -> str:
    """800-53 controls — FRMR-mapped vs scan-evidenced."""
    mapped = ", ".join(escape(c) for c in row.controls_mapped) or "—"
    evidenced = ", ".join(escape(c) for c in row.controls_evidenced) or "<em>no evidence yet</em>"
    return (
        '<div class="kv-block">'
        '<div class="kv-row"><span class="kv-key">Controls mapped (FRMR)</span>'
        f'<span class="kv-val">{mapped}</span></div>'
        '<div class="kv-row"><span class="kv-key">Controls evidenced (scan)</span>'
        f'<span class="kv-val">{evidenced}</span></div>'
        "</div>"
    )


def _render_cadence_block(row: InspectorKsiRow) -> str:
    """CSX-SUM machine + human cadence."""
    machine = (
        escape(row.machine_validation_cadence)
        if row.machine_validation_cadence
        else "<em>unspecified</em>"
    )
    human = (
        escape(row.non_machine_validation_cadence)
        if row.non_machine_validation_cadence
        else "<em>unspecified</em>"
    )
    return (
        '<div class="kv-block">'
        '<div class="kv-row"><span class="kv-key">Machine cadence</span>'
        f'<span class="kv-val">{machine}</span></div>'
        '<div class="kv-row"><span class="kv-key">Human cadence</span>'
        f'<span class="kv-val">{human}</span></div>'
        "</div>"
    )


def _render_citations_block(row: InspectorKsiRow) -> str:
    """file:line evidence citations (no raw excerpts — secret-leak risk)."""
    if not row.citations:
        return (
            '<div class="kv-block">'
            '<div class="kv-row"><span class="kv-key">Evidence citations</span>'
            '<span class="kv-val"><em>no citations yet</em></span></div>'
            "</div>"
        )
    items = "".join(f"<li><code>{escape(c)}</code></li>" for c in row.citations)
    return (
        '<div class="kv-block">'
        '<div class="kv-row"><span class="kv-key">Evidence citations</span>'
        f'<span class="kv-val"><ul class="citation-list">{items}</ul></span></div>'
        "</div>"
    )


def _render_narrative_block(row: InspectorKsiRow) -> str:
    """Gap-Agent narrative (DRAFT banner — it's an LLM output)."""
    if not row.narrative:
        return ""
    mode_label = f" ({escape(row.attestation_mode)})" if row.attestation_mode else ""
    return (
        '<div class="narrative-block">'
        f'<div class="narrative-banner">DRAFT narrative{mode_label} — requires human review</div>'
        f'<div class="narrative-body">{escape(row.narrative)}</div>'
        "</div>"
    )


def _render_failure_block(row: InspectorKsiRow) -> str:
    """When the KSI fails, surface which items + actionable hints."""
    if row.gate_passed:
        return ""
    items = ", ".join(
        _ITEM_LONG_LABELS[item] for item in ALL_ITEMS if item in row.gate_failed_items
    )
    return (
        '<div class="failure-block">'
        f"<strong>RFC-0017 gate failure:</strong> missing {escape(items)}"
        "</div>"
    )


def _render_how_to_verify(tool_version: str) -> str:
    """Footer block telling the assessor how to verify provenance."""
    version_html = f" v{escape(tool_version)}" if tool_version else ""
    return (
        "<h2>How to verify</h2>"
        '<div class="verify-block">'
        f"<p>This report was generated by Efterlev{version_html}. To verify "
        "the build provenance of the Efterlev binary used:</p>"
        "<pre><code>scripts/verify-release.sh v&lt;version&gt;</code></pre>"
        "<p>The release pipeline emits PEP 740 PyPI attestations, cosign "
        "keyless OIDC signatures on the container image, and SLSA build "
        "provenance — verifiable from a clean machine.</p>"
        "</div>"
    )


# --- Inline stylesheet add-ons ----------------------------------------


_VERDICT_STYLESHEET = """<style>
.verdict-banner {
  border-radius: 8px;
  padding: 18px 22px;
  margin-bottom: 18px;
  border: 1px solid transparent;
}
.verdict-banner.verdict-pass {
  background: #e7f6ea;
  border-color: #98d9a8;
  color: #0a4a17;
}
.verdict-banner.verdict-fail {
  background: #fde2e2;
  border-color: #e09898;
  color: #7a1f1f;
}
.verdict-label { font-size: 18px; letter-spacing: 0.5px; }
.verdict-msg { font-size: 13px; margin-top: 6px; }
</style>"""

_ITEM_GRID_STYLESHEET = """<style>
.item-grid {
  display: grid;
  grid-template-columns: repeat(5, 1fr);
  gap: 8px;
  margin-bottom: 18px;
}
.item-cell {
  border-radius: 6px;
  padding: 10px 12px;
  text-align: center;
  font-size: 12px;
  border: 1px solid transparent;
}
.item-cell-ok   { background: #e7f6ea; border-color: #98d9a8; color: #0a4a17; }
.item-cell-fail { background: #fde2e2; border-color: #e09898; color: #7a1f1f; }
.item-name { font-weight: 600; margin-bottom: 4px; }
.item-stat { font-size: 11px; opacity: 0.8; }
@media (max-width: 720px) {
  .item-grid { grid-template-columns: repeat(2, 1fr); }
}
</style>"""

_KSI_ROW_STYLESHEET = """<style>
.theme-h3 {
  margin-top: 24px;
  font-size: 14px;
  color: #4a4a4a;
  border-bottom: 1px solid #eaeef2;
  padding-bottom: 4px;
}
.theme-count { color: #6a737d; font-weight: 400; font-size: 12px; }
details.ksi-row {
  background: white;
  border-radius: 6px;
  margin-bottom: 6px;
  border-left: 4px solid #d0d7de;
  box-shadow: 0 1px 2px rgba(0,0,0,0.04);
}
details.ksi-row.ksi-pass { border-left-color: #1a7f37; }
details.ksi-row.ksi-fail { border-left-color: #c93131; }
details.ksi-row > summary {
  cursor: pointer;
  padding: 10px 14px;
  list-style: none;
  display: flex;
  align-items: center;
  gap: 10px;
}
details.ksi-row > summary::-webkit-details-marker { display: none; }
details.ksi-row > summary::before {
  content: "▸";
  font-size: 11px;
  color: #6a737d;
}
details[open].ksi-row > summary::before { content: "▾"; }
.rfc-dots {
  margin-left: auto;
  font-family: ui-monospace, SFMono-Regular, Menlo, Consolas, monospace;
  letter-spacing: 4px;
}
.rfc-dot {
  display: inline-block;
  width: 18px;
  text-align: center;
  font-weight: 700;
}
.rfc-dot-pass { color: #1a7f37; }
.rfc-dot-fail { color: #c93131; }
.status-pill.status-unclassified { background: #eaeef2; color: #555; }
.ksi-detail { padding: 14px 18px 16px; border-top: 1px solid #eaeef2; }
.ksi-statement { color: #333; margin: 4px 0 12px; }
.kv-block { margin: 8px 0; }
.kv-row { display: flex; font-size: 13px; padding: 3px 0; }
.kv-key {
  flex: 0 0 220px;
  color: #6a737d;
  font-weight: 600;
}
.kv-val { flex: 1; color: #1a1a1a; word-break: break-word; }
.citation-list { margin: 0; padding-left: 18px; }
.citation-list code { font-size: 12px; }
.narrative-block {
  margin-top: 10px;
  background: #fff8e6;
  border: 1px solid #f0c36d;
  border-radius: 6px;
  padding: 10px 12px;
}
.narrative-banner {
  color: #72570e;
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.4px;
  margin-bottom: 6px;
}
.narrative-body { color: #1a1a1a; }
.failure-block {
  margin-top: 10px;
  background: #fdeded;
  border-left: 3px solid #c93131;
  padding: 8px 12px;
  font-size: 13px;
  color: #7a1f1f;
}
.verify-block { font-size: 13px; color: #4a4a4a; }
.verify-block pre {
  background: #f6f8fa;
  padding: 10px 14px;
  border-radius: 5px;
  overflow-x: auto;
  font-size: 12px;
}
@media print {
  /* Expand every collapsed row on paper so the assessor sees everything. */
  details.ksi-row > *:not(summary) { display: block !important; }
  details.ksi-row > summary::before { content: ""; }
}
</style>"""
