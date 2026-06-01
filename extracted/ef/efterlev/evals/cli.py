"""CLI entry point for the eval harness.

Usage:
  python -m evals run --fixture evals/fixtures/govnotes-v1

`run` lays down the workspace, executes the pipeline, computes
metrics, prints a one-screen summary. Phase 1 PR alpha shipped M1+M2;
PR beta adds M3 (resource-naming) + M4 (manifest-quoting). PR gamma
adds M5 (POAM scope) + delta-vs-prior reporter.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from evals.aggregate import aggregate_runs, format_aggregate_block
from evals.diff import compute_deltas, format_delta_block
from evals.ground_truth import load_ground_truth
from evals.harness import RunResult, run_fixture
from evals.metrics import (
    MetricResult,
    manifest_quoting_accuracy,
    poam_scope_discipline,
    resource_naming_rate,
    status_precision,
    status_recall,
)

REPO_ROOT = Path(__file__).resolve().parent.parent
DEFAULT_RESULTS_ROOT = REPO_ROOT / "evals" / "results"


def _load_latest_report(workspace: Path, glob: str) -> dict | None:
    """Load + JSON-parse the latest report matching `glob` across all known
    report locations. Returns the parsed dict on success, None on no-match
    or parse failure.

    Walks both the v0.1.160 `efterlev-out/reports/` location (default for
    fresh writes) and the legacy `.efterlev/reports/` so older workspaces
    still resolve. Mirrors `_latest_match_across` in
    `src/efterlev/primitives/submission/package.py`.
    """
    from efterlev.paths import iter_report_dirs

    candidates: list[Path] = []
    for d in iter_report_dirs(workspace):
        if d.is_dir():
            candidates.extend(d.glob(glob))
    if not candidates:
        return None
    latest = max(candidates, key=lambda p: p.stat().st_mtime)
    try:
        return json.loads(latest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError) as e:
        print(f"warn: failed to parse {latest}: {e}", file=sys.stderr)
        return None


def _read_gap_classifications(workspace: Path) -> dict[str, str] | None:
    """Extract `KSI-id -> status` mapping from the latest gap report."""
    data = _load_latest_report(workspace, "gap-*.json")
    if data is None:
        return None
    classifications = data.get("ksi_classifications") or []
    return {c["ksi_id"]: c["status"] for c in classifications if "ksi_id" in c and "status" in c}


def _read_gap_rationales(workspace: Path) -> dict[str, str]:
    """Extract `KSI-id -> rationale` mapping (drives M3)."""
    data = _load_latest_report(workspace, "gap-*.json")
    if data is None:
        return {}
    classifications = data.get("ksi_classifications") or []
    return {
        c["ksi_id"]: c["rationale"] for c in classifications if "ksi_id" in c and "rationale" in c
    }


def _read_poam_markdown(workspace: Path) -> str:
    """Read the latest POAM markdown body. POAM lands under
    `<reports>/poam/poam-*.md` (subdirectory, per
    src/efterlev/cli/main.py:1159 — runbook-aligned location).
    Walks both the v0.1.160 `efterlev-out/reports/` location and the legacy
    `.efterlev/reports/` so older workspaces still resolve. Returns empty
    string if no POAM was generated; M5 then sees no excluded-count header
    (treats as 0) and no leaks (vacuously passes Check A).
    """
    from efterlev.paths import iter_report_dirs

    matches: list[Path] = []
    for d in iter_report_dirs(workspace):
        poam_dir = d / "poam"
        if poam_dir.is_dir():
            matches.extend(poam_dir.glob("poam-*.md"))
    if not matches:
        return ""
    matches.sort(key=lambda p: p.stat().st_mtime)
    try:
        return matches[-1].read_text(encoding="utf-8")
    except OSError as e:
        print(f"warn: failed to read {matches[-1]}: {e}", file=sys.stderr)
        return ""


def _read_doc_narratives(workspace: Path) -> dict[str, str]:
    """Extract `KSI-id -> narrative` mapping from the latest
    documentation report (drives M4).

    The shipped doc-report JSON shape (verified against a real run on
    2026-05-09 — see evals/results/govnotes-v1/<ts>/workspace/.efterlev/
    reports/documentation-*.json) flattens the in-memory `KsiAttestation
    -> draft -> AttestationDraft` nesting into a single attestation
    object:

        {"attestations": [{"ksi_id": ..., "narrative": ..., ...}, ...]}

    PR beta's first wiring (2026-05-08) read this as `attestations[].
    draft.ksi_id`, which always returned None and produced an n/a M4
    score on every fixture. The first baseline run's `metrics.json`
    files surface this as `manifest_quoting_accuracy: 0/0`. v0.2
    Phase 1 follow-up fixes the path.
    """
    data = _load_latest_report(workspace, "documentation-*.json")
    if data is None:
        return {}
    out: dict[str, str] = {}
    for att in data.get("attestations") or []:
        ksi_id = att.get("ksi_id")
        narrative = att.get("narrative")
        if ksi_id and narrative:
            out[ksi_id] = narrative
    return out


def _format_metric_line(m: MetricResult) -> str:
    pct = f"{m.score * 100:.1f}%" if m.denominator > 0 else "n/a"
    rating = f"{m.numerator}/{m.denominator}"
    line = f"  {m.name:20s} {pct:>7s}  ({rating})"
    if m.notes:
        line += f"  -- {m.notes}"
    return line


def _execute_one_run(
    fixture_dir: Path,
    results_root: Path,
    llm_backend: str,
    llm_region: str,
    llm_model: str | None,
    gt,
) -> tuple[RunResult, list[MetricResult], Path] | None:
    """Run the pipeline once and compute metrics. Returns (result, metrics,
    metrics_path) on success, None if any pipeline stage failed.
    """
    result = run_fixture(
        fixture_dir,
        results_root,
        llm_backend=llm_backend,
        llm_region=llm_region,
        llm_model=llm_model,
    )
    if not result.all_stages_succeeded:
        print(
            f"\n[evals] pipeline did not complete:\n"
            f"  init={result.init_exit} scan={result.scan_exit} gap={result.gap_exit} "
            f"document={result.document_exit} poam={result.poam_exit}",
            file=sys.stderr,
        )
        return None

    classifications = _read_gap_classifications(result.workspace)
    if classifications is None:
        print(
            f"error: no gap-report found in {result.workspace}/.efterlev/reports/",
            file=sys.stderr,
        )
        return None

    rationales = _read_gap_rationales(result.workspace)
    narratives = _read_doc_narratives(result.workspace)
    poam_md = _read_poam_markdown(result.workspace)
    print(
        f"[evals] gap report has {len(classifications)} KSI classifications; "
        f"rationales: {len(rationales)}; doc narratives: {len(narratives)}; "
        f"poam: {'present' if poam_md else 'absent'}",
        file=sys.stderr,
    )

    metrics = [
        status_precision(classifications, gt),
        status_recall(classifications, gt),
        resource_naming_rate(rationales, classifications, gt),
        manifest_quoting_accuracy(narratives, gt),
        poam_scope_discipline(poam_md, gt),
    ]

    metrics_path = result.workspace.parent / "metrics.json"
    metrics_path.write_text(
        json.dumps(
            {
                "fixture_id": gt.fixture_id,
                "ground_truth_revision": gt.revision,
                "timestamp": result.timestamp,
                "metrics": [
                    {
                        "name": m.name,
                        "score": m.score,
                        "numerator": m.numerator,
                        "denominator": m.denominator,
                        "notes": m.notes,
                    }
                    for m in metrics
                ],
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    return result, metrics, metrics_path


def _cmd_run(args: argparse.Namespace) -> int:
    fixture_dir = Path(args.fixture).resolve()
    if not fixture_dir.is_dir():
        print(f"error: fixture directory not found: {fixture_dir}", file=sys.stderr)
        return 1

    gt_path = fixture_dir / "GROUND_TRUTH.yaml"
    if not gt_path.is_file():
        print(f"error: missing GROUND_TRUTH.yaml in {fixture_dir}", file=sys.stderr)
        return 1

    if args.runs < 1:
        print(f"error: --runs must be >= 1 (got {args.runs})", file=sys.stderr)
        return 1

    print(f"[evals] loading ground-truth: {gt_path}", file=sys.stderr)
    gt = load_ground_truth(gt_path)
    print(f"[evals] fixture_id={gt.fixture_id} revision={gt.revision}", file=sys.stderr)

    results_root = (
        Path(args.results_root) if args.results_root else DEFAULT_RESULTS_ROOT
    ) / gt.fixture_id
    results_root.mkdir(parents=True, exist_ok=True)

    print(
        f"[evals] running pipeline against {fixture_dir} "
        f"({args.runs} run{'s' if args.runs > 1 else ''})",
        file=sys.stderr,
    )

    successful: list[tuple[RunResult, list[MetricResult], Path]] = []
    for i in range(args.runs):
        if args.runs > 1:
            print(f"\n[evals] === run {i + 1}/{args.runs} ===", file=sys.stderr)
        outcome = _execute_one_run(
            fixture_dir,
            results_root,
            args.llm_backend,
            args.llm_region,
            args.llm_model,
            gt,
        )
        if outcome is not None:
            successful.append(outcome)

    if not successful:
        print("\n[evals] all runs failed; nothing to report", file=sys.stderr)
        return 1

    if args.runs > 1 and len(successful) < args.runs:
        print(
            f"\n[evals] WARNING: {len(successful)}/{args.runs} runs succeeded; "
            f"aggregate covers only the successful ones",
            file=sys.stderr,
        )

    # Single-run path: existing summary + delta-vs-prior. Multi-run path
    # additionally prints the aggregate block and writes aggregate.json
    # alongside the LAST successful run's metrics.json.
    last_result, last_metrics, last_metrics_path = successful[-1]

    print()
    print(f"=== {gt.fixture_id} (rev {gt.revision}) ===")
    for m in last_metrics:
        print(_format_metric_line(m))
    print()
    print(format_delta_block(compute_deltas(last_metrics_path, results_root)))
    print()

    if args.runs > 1:
        aggregate = aggregate_runs(metrics for _, metrics, _ in successful)
        print(f"=== {gt.fixture_id} -- {len(successful)}-run aggregate ===")
        print(format_aggregate_block(aggregate))
        print()

        aggregate_path = last_result.workspace.parent / "aggregate.json"
        aggregate_path.write_text(
            json.dumps(
                {
                    "fixture_id": gt.fixture_id,
                    "ground_truth_revision": gt.revision,
                    "n_runs": len(successful),
                    "run_timestamps": [r.timestamp for r, _, _ in successful],
                    "aggregate": [
                        {
                            "name": a.name,
                            "n_runs": a.n_runs,
                            "mean": a.mean,
                            "stddev": a.stddev,
                            "min": a.min_score,
                            "max": a.max_score,
                            "scores": list(a.scores),
                        }
                        for a in aggregate
                    ],
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        print(f"  aggregate:   {aggregate_path}")

    print(f"  workspace:   {last_result.workspace}")
    print(f"  metrics:     {last_metrics_path}")

    return 0


def _build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(
        prog="python -m evals",
        description="Efterlev agent-quality eval harness (Phase 1).",
    )
    sub = p.add_subparsers(dest="cmd", required=True)

    run = sub.add_parser("run", help="Run the pipeline against a fixture and compute metrics.")
    run.add_argument(
        "--fixture",
        required=True,
        help="Path to the fixture directory (e.g. evals/fixtures/govnotes-v1).",
    )
    run.add_argument(
        "--llm-backend",
        choices=["anthropic", "bedrock", "openai"],
        default="bedrock",
        help="LLM backend (default: bedrock per the test-LLM policy).",
    )
    run.add_argument(
        "--llm-region",
        default="us-east-1",
        help="AWS region for bedrock backend (default: us-east-1; ignored for other backends).",
    )
    run.add_argument(
        "--llm-model",
        default=None,
        help=(
            "Model ID. Per-backend defaults if unset: bedrock → "
            "$EFTERLEV_TEST_BEDROCK_MODEL or the public us.* Haiku 4.5 "
            "SYSTEM_DEFINED profile; anthropic → claude-haiku-4-5; "
            "openai → gpt-5.4."
        ),
    )
    run.add_argument(
        "--results-root",
        default=None,
        help=(
            "Where to write run workspaces + metrics. Default: "
            "evals/results/<fixture_id>/<timestamp>/."
        ),
    )
    run.add_argument(
        "--runs",
        type=int,
        default=1,
        help=(
            "Number of independent runs to execute against the fixture. "
            "When > 1, prints a per-metric mean/stddev/min/max aggregate "
            "and writes aggregate.json alongside the last run's metrics. "
            "Use 3-5 to get above the per-metric noise floor when "
            "evaluating prompt or fixture changes (default: 1)."
        ),
    )
    run.set_defaults(func=_cmd_run)

    return p


def main(argv: list[str] | None = None) -> int:
    args = _build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
