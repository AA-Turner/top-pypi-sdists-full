"""CLI handler for `efterlev readiness`. Renders the ReadinessReport.

Two modes:

  - default: heuristic 0-100% score (good for "how close am I?")
  - `--strict`: RFC-0017 per-KSI gate (good for "am I ready to submit?")

v0.1.167 / #373 added the strict mode. The default heuristic is unchanged
so existing CI/customers don't break; pre-submission CI should adopt
`--strict` because that's the check that maps to the actual RFC-0017
requirements.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

import typer

from efterlev.errors import ConfigError
from efterlev.frmr import FrmrDocument
from efterlev.primitives.readiness import (
    ALL_ITEMS,
    Rfc0017GateReport,
    compute_readiness,
    compute_rfc_0017_gate,
)


def _identify_procedural_ksis(frmr_doc: FrmrDocument) -> set[str]:
    """KSIs in the AFR / CED / INR themes are procedural by nature.

    These are the themes whose KSIs scanner code can't evidence — they
    cover personnel security, training, incident response, etc. The
    Gap Agent will typically classify them as `evidence_layer_inapplicable`;
    the customer needs to author a signed Evidence Manifest to "really
    cover" them.

    Heuristic by theme prefix. Could be refined later by checking the
    actual `varies_by_level.moderate.evidence_type` field in the FRMR
    catalog, but theme prefix is a useful first pass.
    """
    procedural_prefixes = ("KSI-AFR-", "KSI-CED-", "KSI-INR-")
    return {ksi_id for ksi_id in frmr_doc.indicators if ksi_id.startswith(procedural_prefixes)}


def run_readiness(
    target: Path,
    *,
    json_output: bool = False,
    strict: bool = False,
) -> int:
    """Execute the readiness command. Returns the process exit code.

    Default mode (strict=False): heuristic 0-100% score, exit 0 always.
    Strict mode (strict=True): per-KSI RFC-0017 gate, exit 2 if any
    KSI fails any of the 5 required items. Strict mode is the right
    check to wire into pre-submission CI.
    """
    root = target.resolve()
    frmr_cache = root / ".efterlev" / "cache" / "frmr_document.json"
    if not frmr_cache.is_file():
        typer.echo(
            f"error: FRMR cache missing at {frmr_cache}. Run `efterlev init` first.",
            err=True,
        )
        return 1

    frmr_doc = FrmrDocument.model_validate_json(frmr_cache.read_text(encoding="utf-8"))
    baseline_ksi_ids = list(frmr_doc.indicators.keys())
    procedural_ksi_ids = _identify_procedural_ksis(frmr_doc)

    if strict:
        return _run_strict_gate(root, baseline_ksi_ids, json_output=json_output)

    report = compute_readiness(
        root,
        baseline_ksi_ids=baseline_ksi_ids,
        procedural_ksi_ids=procedural_ksi_ids,
    )

    if json_output:
        # Stable JSON shape; downstream tools consume this.
        typer.echo(
            json.dumps(
                {
                    "score": {
                        "overall_pct": report.score.overall_pct,
                        "ksi_coverage_pct": report.score.ksi_coverage_pct,
                        "manifest_coverage_pct": report.score.manifest_coverage_pct,
                        "severity_penalty_pct": report.score.severity_penalty_pct,
                        "band_label": report.score.band_label,
                    },
                    "ksi_classifications_total": report.ksi_classifications_total,
                    "ksis_in_baseline": report.ksis_in_baseline,
                    "open_poam": {
                        "high": report.open_poam_high,
                        "medium": report.open_poam_medium,
                        "low": report.open_poam_low,
                    },
                    "detectors_fired": report.detectors_fired,
                    "manifests_loaded": report.manifests_loaded,
                    "top_blockers": [
                        {
                            "ksi_id": b.ksi_id,
                            "reason": b.reason,
                            "suggested_action": b.suggested_action,
                        }
                        for b in report.top_blockers
                    ],
                },
                indent=2,
            )
        )
        return 0

    # Human-readable scorecard.
    _render_scorecard(report)
    return 0


def _render_scorecard(report) -> None:
    """Print the scorecard in the format the README mocks."""
    score = report.score

    # Progress bar — 10 cells, ▰ filled, ▱ empty.
    filled = round(score.overall_pct / 10)
    bar = "▰" * filled + "▱" * (10 - filled)

    typer.echo("")
    typer.echo("  Readiness for FedRAMP 20x Moderate")
    typer.echo("")
    typer.echo(f"  Score      {bar}  {score.overall_pct:.0f}%  {score.band_label}")
    typer.echo("")

    # Coverage sub-scores
    typer.echo(
        f"  KSI coverage      "
        f"{report.ksi_classifications_total} / {report.ksis_in_baseline} ksis classified"
    )
    typer.echo(
        f"  Open POA&M items  "
        f"{report.open_poam_high + report.open_poam_medium}  "
        f"({report.open_poam_high} HIGH, {report.open_poam_medium} MEDIUM)"
    )
    typer.echo(f"  Detector firings  {report.detectors_fired} evidence records in the store")
    typer.echo(f"  Manifests         {report.manifests_loaded} procedural attestations loaded")
    typer.echo("")

    # v0.1.146 / #351: detect the shell context via EFTERLEV_SHELL=1
    # (set by `efterlev shell` when it dispatches subcommands). When set,
    # use /-prefixed command names that match the shell registry, ANSI-styled
    # for visibility. When unset (bare CLI run), use the original
    # `efterlev <verb>` syntax. Either way, commands are highlighted so they
    # stand out from the rest of the suggestion text.
    in_shell = os.environ.get("EFTERLEV_SHELL") == "1"

    def cmd(shell_form: str, cli_form: str) -> str:
        text = shell_form if in_shell else cli_form
        return typer.style(text, fg=typer.colors.CYAN, bold=True)

    if report.top_blockers:
        # v0.1.147 / #352: group blockers by reason — three lines of
        # `procedural KSI without a signed Evidence Manifest` reads as a
        # single problem (3 KSIs of the same flavor), not three separate
        # ones. Also dedup the suggested-next bullets.
        from collections import OrderedDict

        by_reason: OrderedDict[str, list[str]] = OrderedDict()
        for b in report.top_blockers:
            by_reason.setdefault(b.reason, []).append(b.ksi_id)

        typer.echo("  Top blockers")
        for reason, ksi_ids in by_reason.items():
            if len(ksi_ids) == 1:
                typer.echo(f"    • {ksi_ids[0]}: {reason}")
            else:
                # Group: "3 KSIs: procedural KSI without a signed Evidence Manifest"
                # then list the ids.
                typer.echo(f"    • {len(ksi_ids)} KSIs: {reason}")
                typer.echo(f"        {', '.join(ksi_ids)}")
        typer.echo("")
        typer.echo("  Suggested next")
        # Dedup suggested_actions; preserve order.
        seen_actions: set[str] = set()
        for b in report.top_blockers:
            if b.suggested_action in seen_actions:
                continue
            seen_actions.add(b.suggested_action)
            typer.echo(f"    • {b.suggested_action}")
        typer.echo("")
    else:
        if report.ksi_classifications_total == 0:
            typer.echo("  Suggested next")
            typer.echo(
                f"    • {cmd('/scan', 'efterlev scan')} then "
                f"{cmd('/agent gap', 'efterlev agent gap')}     to get classifications"
            )
            typer.echo("")
        else:
            typer.echo("  No HIGH-severity blockers — ready to package and engage a 3PAO.")
            typer.echo("")

    typer.echo("  When ready")
    typer.echo(
        f"    • {cmd('/package', 'efterlev submission package')}     to bundle for your 3PAO"
    )
    typer.echo("")


# --- RFC-0017 strict gate (v0.1.167 / #373) ----------------------------


def _run_strict_gate(root: Path, baseline_ksi_ids: list[str], *, json_output: bool) -> int:
    """Drive `compute_rfc_0017_gate` and render the result.

    Pulls cadence strings from the workspace config (items 3 + 4 of the
    gate are workspace-level). When the config can't be loaded we still
    run the gate with empty cadence — every KSI fails items 3/4 and the
    failure-detail messages tell the customer to populate config.
    """
    from efterlev.config import load_config

    config_path = root / ".efterlev" / "config.toml"
    machine_cadence = ""
    human_cadence = ""
    try:
        config = load_config(config_path)
        machine_cadence = config.cadence.machine_validation_cadence
        human_cadence = config.cadence.non_machine_validation_cadence
    except ConfigError as e:
        # Don't bail — running the gate with empty cadence yields
        # actionable per-item failure messages. Surface the config
        # error to stderr for the customer to see.
        typer.echo(f"warning: {e}", err=True)

    report = compute_rfc_0017_gate(
        root,
        baseline_ksi_ids=baseline_ksi_ids,
        machine_validation_cadence=machine_cadence,
        human_validation_cadence=human_cadence,
    )

    if json_output:
        typer.echo(json.dumps(_gate_to_json(report), indent=2))
    else:
        _render_strict_gate(report)

    # Exit code 2 on gate-fail so pre-submission CI naturally blocks on
    # `efterlev readiness --strict`. 0 on pass; reserve 1 for our usual
    # "tool error" (missing FRMR cache).
    return 0 if report.passed else 2


# Short labels for the per-KSI status row, in canonical order. Aligned
# with `ALL_ITEMS` from the gate module.
_ITEM_LABELS: dict[str, str] = {
    "implementation_goal": "goal",
    "consolidated_inventory": "inventory",
    "automated_validation_cadence": "machine-cadence",
    "human_validation_cadence": "human-cadence",
    "current_status": "status",
}


def _render_strict_gate(report: Rfc0017GateReport) -> None:
    """Per-KSI checklist + summary. Failing-KSI detail at the bottom."""
    typer.echo("")
    typer.echo("  RFC-0017 readiness gate (per-KSI checklist)")
    typer.echo("")

    if report.passed:
        verdict = typer.style("PASS", fg=typer.colors.GREEN, bold=True)
    else:
        verdict = typer.style("FAIL", fg=typer.colors.RED, bold=True)
    typer.echo(
        f"  Verdict      {verdict}  "
        f"{report.passing_count}/{report.baseline_ksi_count} KSIs pass all 5 items"
    )
    typer.echo("")

    # Per-item failure counts — surfaces the dominant gap at a glance.
    item_fail_counts: dict[str, int] = {item: 0 for item in ALL_ITEMS}
    for ksi in report.ksi_results:
        for failed in ksi.failed_items:
            item_fail_counts[failed] += 1
    typer.echo("  Per-item failures across baseline:")
    for item in ALL_ITEMS:
        count = item_fail_counts[item]
        if count == 0:
            mark = typer.style("ok", fg=typer.colors.GREEN)
            typer.echo(f"    • {_ITEM_LABELS[item]:<16} {mark}")
        else:
            mark = typer.style(f"{count} failing", fg=typer.colors.RED)
            typer.echo(f"    • {_ITEM_LABELS[item]:<16} {mark}")
    typer.echo("")

    # Failing-KSI detail. Suppress on a fully-passing gate — the verdict
    # line carries enough signal there. On a failing gate the table
    # tells you which KSI is missing what.
    failing = [k for k in report.ksi_results if not k.passed]
    if failing:
        typer.echo(f"  Failing KSIs ({len(failing)}):")
        for ksi in failing:
            failed_labels = ", ".join(
                _ITEM_LABELS[item] for item in ALL_ITEMS if item in ksi.failed_items
            )
            typer.echo(f"    {ksi.ksi_id}  missing: {failed_labels}")
        typer.echo("")
        # First-failure details — one example of each distinct failed item.
        # Avoids dumping 60 copies of the same "configure cadence" message.
        typer.echo("  Sample fixes (first failure per item):")
        shown_items: set[str] = set()
        for ksi in failing:
            for item in ALL_ITEMS:
                if item in ksi.failed_items and item not in shown_items:
                    detail = ksi.failure_details.get(item, "")
                    typer.echo(f"    • [{_ITEM_LABELS[item]}] {ksi.ksi_id}: {detail}")
                    shown_items.add(item)
            if len(shown_items) == len(ALL_ITEMS):
                break
        typer.echo("")


def _gate_to_json(report: Rfc0017GateReport) -> dict[str, object]:
    """Stable JSON shape for the strict gate report. Downstream tools
    consume this; keep the shape backward-compatible across releases."""
    return {
        "passed": report.passed,
        "baseline_ksi_count": report.baseline_ksi_count,
        "passing_count": report.passing_count,
        "failing_count": report.failing_count,
        "machine_cadence_declared": report.machine_cadence_declared,
        "human_cadence_declared": report.human_cadence_declared,
        "ksi_results": [
            {
                "ksi_id": k.ksi_id,
                "passed": k.passed,
                "passed_items": sorted(k.passed_items),
                "failed_items": sorted(k.failed_items),
                "failure_details": k.failure_details,
            }
            for k in report.ksi_results
        ],
    }
