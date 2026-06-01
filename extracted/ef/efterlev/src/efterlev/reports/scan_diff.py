"""Diff between two scan-result JSON sidecars (ConMon Lite v0).

Per DECISIONS 2026-05-11 "Tier 4 #1 design: ConMon Lite (PR-delta scan
comparison)", this module operates at the **per-detector gap-emission**
abstraction — distinct from `gap_diff.py` which operates at the
KSI-verdict layer. The scanner-only diff is deterministic, low-noise,
and does not require a Gap Agent run on either branch (cheaper + more
stable than KSI-verdict diffs at v0; v1 will add the Gap-Agent-level
diff once a verdict-stability mechanism is in place).

Diff keying: `(detector_id, resource_name)` -- one entry per detector
times resource. The dominant detector pattern emits one record per
resource per dimension; multi-record-per-resource detectors degenerate
to last-write-wins on key collision (acceptable at v0 — the
canonical-form upgrade is a v1 candidate if it surfaces real noise).

Gap predicate: an evidence record is a "gap" if its content payload
contains a `gap` field (string). Every Tier 2 / Tier 3 detector
follows this convention; older detectors that don't may not produce
diff entries — acceptable v0 trade-off.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

ScanDiffOutcome = Literal[
    "new_gap",  # not present in prior or not a gap in prior, gap in current
    "resolved_gap",  # gap in prior, not present in current or not a gap in current
    "modified_gap",  # gap in both, content differs
]


class ScanDiffEntry(BaseModel):
    """One detector x resource pair's diff outcome between two scans."""

    model_config = ConfigDict(frozen=True)

    detector_id: str
    resource_name: str
    outcome: ScanDiffOutcome
    # The gap message text from the current scan (for new_gap, modified_gap)
    # or from the prior scan (for resolved_gap). Truncated to 200 chars at
    # render time; persisted full here so downstream tools see the entire
    # gap text.
    gap_text: str | None = None
    # Human-readable description of the modification on modified_gap (e.g.
    # "rule_count: 3 → 1"). None on new_gap and resolved_gap.
    modification_summary: str | None = None
    # Source citation: "<file>" or "<file>:<line_start>-<line_end>".
    source_ref: str | None = None


class ScanDiff(BaseModel):
    """Diff between two scan-result JSON sidecars (ConMon Lite v0)."""

    model_config = ConfigDict(frozen=True)

    schema_version: int = 1
    prior_generated_at: str | None = None
    current_generated_at: str | None = None
    prior_scan_root: str | None = None
    current_scan_root: str | None = None

    new_gaps: list[ScanDiffEntry] = Field(default_factory=list)
    modified_gaps: list[ScanDiffEntry] = Field(default_factory=list)
    resolved_gaps: list[ScanDiffEntry] = Field(default_factory=list)


def _is_gap(content: dict[str, Any]) -> bool:
    """Canonical gap predicate: an evidence record is a gap iff its
    content payload contains a string `gap` field. See DECISIONS
    2026-05-11 Decision #2 carry-forward.
    """
    return isinstance(content.get("gap"), str)


def _format_source_ref(source_ref: dict[str, Any] | None) -> str | None:
    """Render a SourceRef dict as `file:line_start-line_end` or just
    `file` if line numbers are absent (plan-JSON mode)."""
    if not isinstance(source_ref, dict):
        return None
    file = source_ref.get("file")
    if not isinstance(file, str):
        return None
    line_start = source_ref.get("line_start")
    line_end = source_ref.get("line_end")
    if isinstance(line_start, int) and isinstance(line_end, int):
        return f"{file}:{line_start}-{line_end}"
    return file


def _modification_summary(prior_content: dict[str, Any], current_content: dict[str, Any]) -> str:
    """For a modified-gap entry, summarize what changed between prior
    and current content. Surfaces the most-meaningful field deltas
    (count fields, list-length deltas, gap-text changes) in a one-line
    string. Returns a placeholder if nothing significant differs.
    """
    changes: list[str] = []
    # Count-style scalar changes (rule_count, ip_set_count, etc.).
    for key in sorted(set(prior_content) | set(current_content)):
        if key in {"gap", "detail"}:
            continue
        prior_val = prior_content.get(key)
        current_val = current_content.get(key)
        if prior_val == current_val:
            continue
        # Render scalars and small lists; suppress dicts (too noisy).
        if isinstance(prior_val, (int, float, str, bool)) or isinstance(
            current_val, (int, float, str, bool)
        ):
            changes.append(f"{key}: {prior_val!r} → {current_val!r}")
        elif isinstance(prior_val, list) and isinstance(current_val, list):
            changes.append(f"{key}: list len {len(prior_val)} → {len(current_val)}")
        if len(changes) >= 3:
            break
    if not changes:
        return "content changed"
    return "; ".join(changes)


def _index_evidence(scan_data: dict[str, Any]) -> dict[tuple[str, str], dict[str, Any]]:
    """Build a (detector_id, resource_name) → evidence-record dict
    from a scan-result JSON sidecar. Resource_name is taken from
    `content.resource_name` if present, falling back to the empty
    string (some non-resource-tied detectors don't carry a resource
    name; they degenerate to a single keyed entry per detector).
    """
    index: dict[tuple[str, str], dict[str, Any]] = {}
    for record in scan_data.get("evidence", []):
        if not isinstance(record, dict):
            continue
        detector_id = record.get("detector_id")
        if not isinstance(detector_id, str):
            continue
        resource_name = ""
        content = record.get("content")
        if isinstance(content, dict):
            rn = content.get("resource_name")
            if isinstance(rn, str):
                resource_name = rn
        index[(detector_id, resource_name)] = record
    return index


def compute_scan_diff(prior_data: dict[str, Any], current_data: dict[str, Any]) -> ScanDiff:
    """Compute a ScanDiff between two scan-result JSON sidecars.

    Inputs are dict-shaped (parsed from `scan-<ts>.json` sidecars).
    Output is the structured ScanDiff with new_gaps / modified_gaps /
    resolved_gaps lists. Per DECISIONS Decision #3, unchanged_gaps and
    unchanged_non_gaps are excluded from the output (regression focus).
    """
    prior_index = _index_evidence(prior_data)
    current_index = _index_evidence(current_data)
    all_keys = sorted(set(prior_index) | set(current_index))

    new_gaps: list[ScanDiffEntry] = []
    modified_gaps: list[ScanDiffEntry] = []
    resolved_gaps: list[ScanDiffEntry] = []

    for key in all_keys:
        prior_rec = prior_index.get(key)
        current_rec = current_index.get(key)
        prior_content = (prior_rec or {}).get("content") or {}
        current_content = (current_rec or {}).get("content") or {}
        prior_is_gap = isinstance(prior_rec, dict) and _is_gap(prior_content)
        current_is_gap = isinstance(current_rec, dict) and _is_gap(current_content)

        if not prior_is_gap and current_is_gap:
            new_gaps.append(
                ScanDiffEntry(
                    detector_id=key[0],
                    resource_name=key[1],
                    outcome="new_gap",
                    gap_text=current_content.get("gap"),
                    source_ref=_format_source_ref((current_rec or {}).get("source_ref")),
                )
            )
        elif prior_is_gap and not current_is_gap:
            resolved_gaps.append(
                ScanDiffEntry(
                    detector_id=key[0],
                    resource_name=key[1],
                    outcome="resolved_gap",
                    gap_text=prior_content.get("gap"),
                    source_ref=_format_source_ref((prior_rec or {}).get("source_ref")),
                )
            )
        elif prior_is_gap and current_is_gap and prior_content != current_content:
            modified_gaps.append(
                ScanDiffEntry(
                    detector_id=key[0],
                    resource_name=key[1],
                    outcome="modified_gap",
                    gap_text=current_content.get("gap"),
                    modification_summary=_modification_summary(prior_content, current_content),
                    source_ref=_format_source_ref((current_rec or {}).get("source_ref")),
                )
            )
        # else: unchanged_gap or unchanged_non_gap -- excluded per Decision #3.

    return ScanDiff(
        prior_generated_at=prior_data.get("generated_at"),
        current_generated_at=current_data.get("generated_at"),
        prior_scan_root=prior_data.get("scan_root"),
        current_scan_root=current_data.get("scan_root"),
        new_gaps=new_gaps,
        modified_gaps=modified_gaps,
        resolved_gaps=resolved_gaps,
    )


def render_scan_diff_markdown(
    diff: ScanDiff,
    *,
    base_branch: str | None = None,
    max_rows: int = 20,
) -> str:
    """Render a ScanDiff as the markdown PR comment per the DECISIONS
    locked format. Tail-truncate at `max_rows` rows total across new
    and modified gaps; full list lives in the JSON sidecar.

    Per Decision #3, resolved gaps are excluded from the comment view
    (counted in the header but not listed). The Gap Agent + downstream
    tooling can read resolved_gaps from the JSON sidecar.

    The trailing `<!-- efterlev-conmon-lite -->` HTML marker lets the
    CI workflow's sticky-comment edit-in-place logic find the existing
    comment to update. Distinct from the existing pr-compliance-scan
    posture comment.
    """
    n_new = len(diff.new_gaps)
    n_modified = len(diff.modified_gaps)
    n_resolved = len(diff.resolved_gaps)
    base = f"`{base_branch}`" if base_branch else "the base branch"

    lines: list[str] = []
    lines.append(f"### Efterlev posture delta (vs {base})")
    lines.append("")
    if n_new == 0 and n_modified == 0 and n_resolved == 0:
        lines.append("**No detector-level gap changes** between this PR and the base branch.")
        lines.append("")
        lines.append("<!-- efterlev-conmon-lite -->")
        return "\n".join(lines)

    lines.append(
        f"**{n_new} new gaps**, {n_modified} modified, {n_resolved} resolved "
        f"(resolved excluded from this view; see scan-diff JSON sidecar)."
    )
    lines.append("")

    if n_new == 0 and n_modified == 0:
        lines.append("_(only resolved gaps in this delta — no regressions to flag.)_")
        lines.append("")
        lines.append("<!-- efterlev-conmon-lite -->")
        return "\n".join(lines)

    lines.append("| Detector | Resource | Gap | Source |")
    lines.append("|---|---|---|---|")

    rendered_rows = 0
    rows_to_render: list[ScanDiffEntry] = list(diff.new_gaps) + list(diff.modified_gaps)
    truncated = False
    for entry in rows_to_render:
        if rendered_rows >= max_rows:
            truncated = True
            break
        gap_label = "New"
        if entry.outcome == "modified_gap":
            mod = entry.modification_summary or "modified"
            gap_label = f"Modified ({mod})"
        source = entry.source_ref or "—"
        lines.append(
            f"| `{entry.detector_id}` | `{entry.resource_name}` | {gap_label} | `{source}` |"
        )
        rendered_rows += 1

    if truncated:
        remaining = len(rows_to_render) - rendered_rows
        lines.append("")
        lines.append(
            f"_(showing {rendered_rows} of {len(rows_to_render)} — see scan-diff JSON "
            f"sidecar workflow artifact for the remaining {remaining}.)_"
        )

    lines.append("")
    lines.append(
        "<sub>scanner-only diff at v0 — Gap Agent verdicts excluded for stability. "
        "ConMon Lite v1 will add KSI-verdict diffs.</sub>"
    )
    lines.append("")
    lines.append("<!-- efterlev-conmon-lite -->")
    return "\n".join(lines)


def render_scan_diff_html(diff: ScanDiff, *, generated_at: datetime) -> str:
    """Render a ScanDiff as a standalone HTML page mirroring the
    gap-diff HTML pattern. Includes resolved gaps for full-context
    review (the markdown comment hides them; the HTML report is the
    "deep dive" surface).
    """
    from html import escape

    from efterlev.reports.html import render_base_document

    rows_html_parts: list[str] = []
    sections: list[tuple[str, list[ScanDiffEntry]]] = [
        ("New gaps", list(diff.new_gaps)),
        ("Modified gaps", list(diff.modified_gaps)),
        ("Resolved gaps", list(diff.resolved_gaps)),
    ]
    for title, entries in sections:
        rows_html_parts.append(f"<h2>{escape(title)} ({len(entries)})</h2>")
        if not entries:
            rows_html_parts.append("<p><em>None.</em></p>")
            continue
        rows_html_parts.append(
            "<table><thead><tr>"
            "<th>Detector</th><th>Resource</th><th>Source</th><th>Detail</th>"
            "</tr></thead><tbody>"
        )
        for entry in entries:
            detail = escape(entry.gap_text or "")
            if entry.modification_summary:
                detail = f"<strong>{escape(entry.modification_summary)}</strong><br>{detail}"
            rows_html_parts.append(
                f"<tr><td>{escape(entry.detector_id)}</td>"
                f"<td>{escape(entry.resource_name)}</td>"
                f"<td>{escape(entry.source_ref or '—')}</td>"
                f"<td>{detail}</td></tr>"
            )
        rows_html_parts.append("</tbody></table>")

    body_html = (
        f"<p>Prior scan root: <code>{escape(diff.prior_scan_root or 'unknown')}</code><br>"
        f"Current scan root: <code>{escape(diff.current_scan_root or 'unknown')}</code></p>"
        + "".join(rows_html_parts)
    )
    return render_base_document(
        title="Efterlev scan-diff",
        body_html=body_html,
        generated_at=generated_at.isoformat(),
    )
