"""`generate_inventory` primitive — deterministic consolidated-resource-
inventory report assembly.

[RFC-0017 (Persistent Validation and Assessment Standard)](https://www.fedramp.gov/rfcs/0017/)
names "consolidated resource inventory being validated" as one of the
5 required items per Key Security Indicator. We already capture this
data in the provenance store (every Evidence record carries
`source_ref` + `content.resource_type` + `content.resource_name`); the
inventory primitive promotes it to a first-class artifact a 3PAO can
read.

What an inventory entry looks like:
- `resource_id`: stable, deterministic id = `<resource_type>:<resource_name>`
- `resource_type`: AWS service / Terraform type / CFN type / CDK
  construct / GitHub workflow (e.g. `aws_s3_bucket`, `github_workflow`)
- `resource_name`: the Terraform / CFN / CDK / workflow declared name
- `source_files`: every file:line range that emitted evidence about this
  resource (one resource can be evidenced by multiple detectors)
- `evidence_count`: how many evidence records mention it
- `boundary_state`: in_boundary / out_of_boundary / boundary_undeclared
- `ksi_coverage`: which KSI ids have evidence citing this resource
- `controls_coverage`: which 800-53 controls have evidence citing this
  resource
- `import_source`: `iac_detector` (default) or the import source for
  runtime-evidence records (`aws.security_hub.asff`, `aws.config.evaluations`,
  `aws.prowler.native`)

Two output formats:
- JSON (machine-readable, RFC-0017-shaped) for 3PAO tooling
- HTML (one-page table, grouped by resource type) for human review

Deterministic: same store contents → same inventory. No LLM call.

Status: this is the v0.1.164 / #369 first cut. Field shape is
relatively stable; if RFC-0017 finalizes with a different inventory
field-name convention we'll revise (versioned via
`inventory_schema_version` in the JSON output).
"""

from __future__ import annotations

import json
from collections import defaultdict
from datetime import UTC, datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

from efterlev.primitives.base import primitive

INVENTORY_SCHEMA_VERSION = "0.1.0-rfc-0017-aligned"
RFC_REFERENCE = "RFC-0017 (Persistent Validation and Assessment Standard)"

InventoryOutputFormat = Literal["json", "html"]


class InventorySourceFile(BaseModel):
    """One file:line range where a resource was evidenced."""

    model_config = ConfigDict(frozen=True)

    file: str
    line_start: int | None = None
    line_end: int | None = None
    commit: str | None = None


class InventoryEntry(BaseModel):
    """One row of the consolidated resource inventory."""

    model_config = ConfigDict(frozen=True)

    resource_id: str  # "<resource_type>:<resource_name>"
    resource_type: str
    resource_name: str
    source_files: list[InventorySourceFile]
    evidence_count: int
    boundary_state: str  # in_boundary | out_of_boundary | boundary_undeclared
    ksi_coverage: list[str]  # sorted, deduped
    controls_coverage: list[str]  # sorted, deduped, lowercased per FRMR
    import_source: str  # iac_detector | aws.security_hub.asff | etc.


class GenerateInventoryInput(BaseModel):
    """Input: every evidence payload from the store."""

    model_config = ConfigDict(frozen=True, arbitrary_types_allowed=True)

    evidence_payloads: list[dict[str, Any]]
    output_format: InventoryOutputFormat = "json"
    generated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    baseline_id: str = "fedramp-20x-moderate"


class GenerateInventoryOutput(BaseModel):
    """Output: rendered inventory + structured entries."""

    model_config = ConfigDict(frozen=True)

    rendered: str
    output_format: InventoryOutputFormat
    entry_count: int
    entries: list[InventoryEntry]
    # Count of DETECTOR evidence payloads we couldn't fold into the inventory
    # (no resource_type / resource_name in content). Surfaced so callers
    # can detect drift in detector evidence shape. Excludes manifest
    # evidence (see skipped_manifest).
    skipped_no_resource: int = 0
    # v0.1.176 / #383: count of manifest-sourced evidence skipped. These are
    # procedural KSI attestations with no resource — skipping them is
    # expected, not drift. Tracked separately so the CLI doesn't false-alarm.
    skipped_manifest: int = 0


@primitive(capability="generate", side_effects=False, version="0.1.0", deterministic=True)
def generate_inventory(input: GenerateInventoryInput) -> GenerateInventoryOutput:
    """Build a consolidated resource inventory from evidence payloads.

    Deterministic: same payloads → byte-identical output. Resources are
    keyed by `<resource_type>:<resource_name>`; multiple evidence
    records for the same resource (across detectors) collapse into one
    entry whose `source_files` and `ksi_coverage` aggregate everything
    cited.
    """
    # Aggregate by resource_id.
    grouped: dict[str, dict[str, Any]] = defaultdict(
        lambda: {
            "source_files": [],
            "ksi_set": set(),
            "controls_set": set(),
            "evidence_count": 0,
            "boundary_state": "boundary_undeclared",
            "import_source": "iac_detector",
            "resource_type": "",
            "resource_name": "",
        }
    )
    skipped_no_resource = 0
    skipped_manifest = 0

    for payload in input.evidence_payloads:
        if not isinstance(payload, dict):
            skipped_no_resource += 1
            continue
        # v0.1.176 / #383: manifest-sourced evidence (procedural KSI
        # attestations, detector_id="manifest") legitimately has no
        # resource_type/resource_name — it's not a cloud resource. Skipping
        # it from the resource inventory is correct + expected, NOT
        # "detector evidence shape drift." Count it separately so the CLI
        # doesn't false-alarm. Only genuine detector evidence missing the
        # resource fields counts toward the drift signal.
        if payload.get("detector_id") == "manifest":
            skipped_manifest += 1
            continue
        raw_content = payload.get("content")
        content: dict[str, Any] = raw_content if isinstance(raw_content, dict) else {}
        rt = content.get("resource_type")
        rn = content.get("resource_name")
        if not isinstance(rt, str) or not isinstance(rn, str):
            skipped_no_resource += 1
            continue
        resource_id = f"{rt}:{rn}"
        grp = grouped[resource_id]
        grp["resource_type"] = rt
        grp["resource_name"] = rn
        grp["evidence_count"] += 1

        # Boundary precedence: in_boundary > out_of_boundary > undeclared.
        # If ANY evidence record marks the resource in_boundary, the
        # resource is in scope; out_of_boundary only sticks when EVERY
        # record agrees; otherwise undeclared.
        bs = payload.get("boundary_state", "boundary_undeclared")
        if bs == "in_boundary":
            grp["boundary_state"] = "in_boundary"
        elif bs == "out_of_boundary" and grp["boundary_state"] != "in_boundary":
            grp["boundary_state"] = "out_of_boundary"

        # Source file aggregation. Multiple detector evidence records
        # for the same resource may cite different files (e.g., the
        # SSE-config block vs the bucket declaration); preserve all.
        sr = payload.get("source_ref")
        if isinstance(sr, dict) and isinstance(sr.get("file"), str):
            sf = (
                sr["file"],
                sr.get("line_start"),
                sr.get("line_end"),
                sr.get("commit"),
            )
            if sf not in grp["source_files"]:
                grp["source_files"].append(sf)

        for ksi_id in payload.get("ksis_evidenced", []) or []:
            if isinstance(ksi_id, str):
                grp["ksi_set"].add(ksi_id)
        for ctrl in payload.get("controls_evidenced", []) or []:
            if isinstance(ctrl, str):
                grp["controls_set"].add(ctrl.lower())

        # Import source surfaces whether the evidence came from IaC
        # detectors or a runtime-evidence import. The first non-default
        # value wins (defaults stay iac_detector).
        if "import_source" in content and isinstance(content["import_source"], str):
            grp["import_source"] = content["import_source"]

    # Build entries in deterministic order (resource_id alphabetical).
    entries: list[InventoryEntry] = []
    for resource_id in sorted(grouped.keys()):
        grp = grouped[resource_id]
        source_files = [
            InventorySourceFile(
                file=f,
                line_start=ls,
                line_end=le,
                commit=c,
            )
            for (f, ls, le, c) in grp["source_files"]
        ]
        # Stabilize source_files order.
        source_files = sorted(
            source_files, key=lambda s: (s.file, s.line_start or 0, s.line_end or 0)
        )
        entries.append(
            InventoryEntry(
                resource_id=resource_id,
                resource_type=grp["resource_type"],
                resource_name=grp["resource_name"],
                source_files=source_files,
                evidence_count=grp["evidence_count"],
                boundary_state=grp["boundary_state"],
                ksi_coverage=sorted(grp["ksi_set"]),
                controls_coverage=sorted(grp["controls_set"]),
                import_source=grp["import_source"],
            )
        )

    if input.output_format == "json":
        rendered = _render_json(
            entries=entries,
            generated_at=input.generated_at,
            baseline_id=input.baseline_id,
            skipped_no_resource=skipped_no_resource,
        )
    else:
        rendered = _render_html(
            entries=entries,
            generated_at=input.generated_at,
            baseline_id=input.baseline_id,
            skipped_no_resource=skipped_no_resource,
        )

    return GenerateInventoryOutput(
        rendered=rendered,
        output_format=input.output_format,
        entry_count=len(entries),
        entries=entries,
        skipped_no_resource=skipped_no_resource,
        skipped_manifest=skipped_manifest,
    )


def _render_json(
    *,
    entries: list[InventoryEntry],
    generated_at: datetime,
    baseline_id: str,
    skipped_no_resource: int,
) -> str:
    doc = {
        "inventory_schema_version": INVENTORY_SCHEMA_VERSION,
        "rfc_reference": RFC_REFERENCE,
        "baseline_id": baseline_id,
        "generated_at": generated_at.isoformat(),
        "entry_count": len(entries),
        "skipped_no_resource": skipped_no_resource,
        "entries": [e.model_dump(mode="json") for e in entries],
    }
    return json.dumps(doc, indent=2, sort_keys=False) + "\n"


def _render_html(
    *,
    entries: list[InventoryEntry],
    generated_at: datetime,
    baseline_id: str,
    skipped_no_resource: int,
) -> str:
    """Render a one-page HTML table grouped by resource type.

    Designed to print/screenshot for a 3PAO scoping conversation:
    one row per resource, grouped by type so a reviewer scanning
    "what's in scope" sees the resource shape immediately.
    """
    # Group entries by resource_type for the table-of-contents view.
    by_type: dict[str, list[InventoryEntry]] = defaultdict(list)
    for e in entries:
        by_type[e.resource_type].append(e)

    # Boundary-state counts for the header.
    boundary_counts: dict[str, int] = defaultdict(int)
    for e in entries:
        boundary_counts[e.boundary_state] += 1

    rows_html: list[str] = []
    for rtype in sorted(by_type.keys()):
        rows_html.append(
            f'<tr class="rt"><td colspan="6"><b>{_esc(rtype)}</b> '
            f"({len(by_type[rtype])} resource(s))</td></tr>"
        )
        for e in by_type[rtype]:
            sf = (
                "<br/>".join(
                    _esc(f"{s.file}:{s.line_start}-{s.line_end}" if s.line_start else s.file)
                    for s in e.source_files
                )
                or "<i>none</i>"
            )
            ksi = ", ".join(_esc(k) for k in e.ksi_coverage) or "<i>none</i>"
            ctrls = ", ".join(_esc(c.upper()) for c in e.controls_coverage) or "<i>none</i>"
            bs_class = (
                "ok"
                if e.boundary_state == "in_boundary"
                else ("warn" if e.boundary_state == "boundary_undeclared" else "drop")
            )
            rows_html.append(
                f"<tr>"
                f"<td>{_esc(e.resource_name)}</td>"
                f"<td>{sf}</td>"
                f"<td>{e.evidence_count}</td>"
                f'<td class="{bs_class}">{_esc(e.boundary_state)}</td>'
                f"<td>{ksi}</td>"
                f"<td>{ctrls}</td>"
                f"</tr>"
            )

    header_summary = (
        f"<b>{len(entries)} resource(s)</b>"
        f" &middot; in-boundary {boundary_counts.get('in_boundary', 0)}"
        f" / out-of-boundary {boundary_counts.get('out_of_boundary', 0)}"
        f" / undeclared {boundary_counts.get('boundary_undeclared', 0)}"
    )
    skipped_note = (
        f'<p class="note">{skipped_no_resource} evidence record(s) skipped '
        f"(no resource_type/resource_name in content).</p>"
        if skipped_no_resource
        else ""
    )

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8"/>
<title>Consolidated Resource Inventory — {_esc(baseline_id)}</title>
<style>
body {{ font-family: -apple-system,BlinkMacSystemFont,system-ui,sans-serif;
        max-width: 1200px; margin: 2em auto; padding: 0 1em; color: #1a1a1a; }}
h1 {{ font-size: 1.6em; }}
.meta {{ color: #666; font-size: 0.92em; }}
.note {{ color: #aa6; background: #fffce0; padding: 0.6em 0.9em;
         border-left: 3px solid #cc9; }}
table {{ border-collapse: collapse; width: 100%; margin-top: 1em;
         font-size: 0.92em; }}
th, td {{ text-align: left; padding: 0.5em 0.7em;
          border-bottom: 1px solid #ddd; vertical-align: top; }}
th {{ background: #f4f4f4; }}
tr.rt td {{ background: #eef2f7; padding-top: 0.7em; padding-bottom: 0.3em;
            font-size: 0.95em; }}
td.ok {{ color: #285028; }}
td.warn {{ color: #886a00; }}
td.drop {{ color: #903030; }}
</style></head><body>
<h1>Consolidated Resource Inventory</h1>
<p class="meta">
Baseline: <b>{_esc(baseline_id)}</b> &middot;
Generated: {_esc(generated_at.isoformat())} &middot;
Schema: <code>{INVENTORY_SCHEMA_VERSION}</code> &middot;
RFC: {_esc(RFC_REFERENCE)}<br/>
{header_summary}
</p>
{skipped_note}
<table>
<thead><tr>
<th>Name</th><th>Source(s)</th><th>Evidence</th>
<th>Boundary</th><th>KSI coverage</th><th>800-53 controls</th>
</tr></thead>
<tbody>
{chr(10).join(rows_html)}
</tbody></table>
<p class="meta" style="margin-top: 2em;">
Generated by Efterlev. This artifact is the consolidated resource
inventory required by RFC-0017 §implementation. Hand to a 3PAO
alongside the gap report and POA&amp;M.
</p>
</body></html>
"""


def _esc(s: str) -> str:
    """Minimal HTML escape — Inventory entries are scanner-derived and
    don't contain attacker-controlled HTML, but we escape defensively
    because `resource_name` traces back to Terraform / CFN / CDK
    identifiers that a malicious upstream could craft to inject."""
    return s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")
