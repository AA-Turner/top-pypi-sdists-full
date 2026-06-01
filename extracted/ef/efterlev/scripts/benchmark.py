#!/usr/bin/env python3
"""Time-to-FRMR benchmark harness (M2, v0.1.112).

Measures wall-clock + LLM cost for the full `efterlev report run`
pipeline against a fixture. Output is structured JSON suitable for
aggregation across runs and publication in `docs/benchmark-2026-05.md`.

Usage:

    uv run python scripts/benchmark.py \\
        --fixture evals/fixtures/csp-starter-cfn \\
        --model claude-haiku-4-5 \\
        --runs 1 \\
        --output /tmp/efterlev-benchmark-results/

**IMPORTANT — `--output` must be OUTSIDE the efterlev repo.** The
benchmark copies the fixture to `<output>/<timestamp>/runs/<id>/workspace`
and runs `efterlev report run --target <workspace>` against it.
`efterlev scan` hard-errors when `--target` sits below a
`.github/workflows/` ancestor (the v0.1.x funnel-killer guard) — and
the efterlev repo itself has `.github/workflows/`, so any subdir under
the repo trips the guard. Default `--output` is `/tmp/efterlev-benchmark-results`
to avoid this; the dispatch workflow uses `${RUNNER_TEMP}/`.

What "time-to-FRMR" measures:
- Wall-clock from `efterlev init --target <fixture>` to the LAST
  artifact (OSCAL CD JSON, since v0.1.111 doc graduation) written.
- Total LLM cost in USD (sum of receipts.log entries past run-start).
- Total LLM token usage (input + output, per model).
- KSI classifications produced.

What this is NOT measuring:
- Authorization timeline (3PAO assessment, FedRAMP PMO acceptance).
- Customer review time on drafted artifacts.
- Anything other than tool runtime against a fixture.

The benchmark intentionally runs the full pipeline (not just gap agent)
to reflect what a customer actually invokes via `report run`. This
includes deterministic stages (init, scan, poam, oscal) which add
seconds but no LLM cost.
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import time
from datetime import UTC, datetime
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent

# Lazy import — keep CLI startup fast.


def _read_receipts_window(workspace: Path, started_at: datetime) -> dict[str, dict]:
    """Aggregate token usage + estimated cost from receipts past `started_at`.

    Returns: {model_id: {"input_tokens": N, "output_tokens": N, "estimated_cost_usd": F}}.
    """
    receipts_path = workspace / ".efterlev" / "receipts.log"
    if not receipts_path.is_file():
        return {}

    from efterlev.llm.pricing import estimate_cost_usd

    by_model: dict[str, dict] = {}
    for line in receipts_path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        ts_str = entry.get("ts")
        model = entry.get("model")
        in_tok = entry.get("input_tokens")
        out_tok = entry.get("output_tokens")
        if not ts_str or not model or in_tok is None or out_tok is None:
            continue
        try:
            ts = datetime.fromisoformat(ts_str)
        except ValueError:
            continue
        if ts < started_at:
            continue
        agg = by_model.setdefault(
            model, {"input_tokens": 0, "output_tokens": 0, "estimated_cost_usd": 0.0}
        )
        agg["input_tokens"] += int(in_tok)
        agg["output_tokens"] += int(out_tok)
        # estimate_cost_usd takes the model_id string + token counts and
        # returns USD float (or None when the model isn't registered).
        # Returning None — rather than raising — means unregistered models
        # contribute zero to the cost line; the token line stays accurate.
        cost = estimate_cost_usd(model, int(in_tok), int(out_tok))
        if cost is not None:
            agg["estimated_cost_usd"] += float(cost)
    return by_model


def _count_ksi_classifications(workspace: Path) -> int | None:
    """Return the count of classifications in the latest gap report, or None."""
    reports = list((workspace / ".efterlev" / "reports").glob("gap-*.json"))
    if not reports:
        return None
    latest = max(reports, key=lambda p: p.stat().st_mtime)
    try:
        data = json.loads(latest.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None
    return len(data.get("ksi_classifications") or [])


def _has_artifact(workspace: Path, glob: str) -> bool:
    """True iff at least one file matching glob exists under .efterlev/reports/.

    Glob is relative to .efterlev/reports/. Use `**/*.md` or `subdir/*.md`
    for files in subdirectories — bare `*.md` only matches top-level.
    """
    return any((workspace / ".efterlev" / "reports").glob(glob))


def _run_pipeline(
    fixture_workspace: Path,
    model: str,
    backend: str,
    region: str | None,
    capture_log: Path,
) -> tuple[int, float]:
    """Invoke `efterlev init` (with --llm-backend + --llm-model) then `report run`.

    v0.1.115 fix: prior versions set `EFTERLEV_LLM_BACKEND/MODEL` env vars
    that the agents don't read, so the benchmark's `--model` flag was a
    no-op. Now we call `init` explicitly with the model flags so the
    workspace config carries them through the whole pipeline. We pass
    `--skip-init` to `report run` since init already happened.
    """
    import os

    env = os.environ.copy()
    log_path_writer = capture_log.open("w", encoding="utf-8")
    started = time.monotonic()

    init_args = [
        "uv",
        "run",
        "efterlev",
        "init",
        "--target",
        str(fixture_workspace),
        "--baseline",
        "fedramp-20x-moderate",
        "--llm-backend",
        backend,
        "--llm-model",
        model,
        "--force",
    ]
    if backend == "bedrock" and region:
        init_args.extend(["--llm-region", region])

    log_path_writer.write(f"=== init ===\n{' '.join(init_args)}\n\n")
    log_path_writer.flush()
    # subprocess.run with list-form argv (no shell=True) — safe by construction.
    init_proc = subprocess.run(  # nosemgrep
        init_args,
        cwd=REPO_ROOT,
        env=env,
        stdout=log_path_writer,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if init_proc.returncode != 0:
        log_path_writer.close()
        return init_proc.returncode, time.monotonic() - started

    report_args = [
        "uv",
        "run",
        "efterlev",
        "report",
        "run",
        "--target",
        str(fixture_workspace),
        "--skip-init",
    ]
    log_path_writer.write(f"\n=== report run ===\n{' '.join(report_args)}\n\n")
    log_path_writer.flush()
    report_proc = subprocess.run(  # nosemgrep
        report_args,
        cwd=REPO_ROOT,
        env=env,
        stdout=log_path_writer,
        stderr=subprocess.STDOUT,
        check=False,
    )
    log_path_writer.close()
    elapsed = time.monotonic() - started
    return report_proc.returncode, elapsed


def benchmark_one_run(
    fixture: Path,
    model: str,
    backend: str,
    region: str | None,
    run_id: str,
    output_root: Path,
) -> dict:
    """Execute one full pipeline run; return a structured result dict."""
    output_root.mkdir(parents=True, exist_ok=True)
    workspace = output_root / "workspace"
    if workspace.exists():
        shutil.rmtree(workspace)
    shutil.copytree(fixture, workspace)
    log_path = output_root / "pipeline.log"

    # Wipe any inherited .efterlev/ — we want a clean init from scratch
    # so the model config is what THIS run requested, not whatever the
    # fixture might have shipped with.
    inherited = workspace / ".efterlev"
    if inherited.exists():
        shutil.rmtree(inherited)

    # Use UTC for receipts-log filtering — receipts.log writes ISO-format UTC.
    started_at = datetime.now(UTC).replace(microsecond=0)
    pipeline_started = time.monotonic()
    exit_code, wall_seconds = _run_pipeline(workspace, model, backend, region, log_path)
    pipeline_ended = time.monotonic()
    by_model = _read_receipts_window(workspace, started_at)
    total_cost = sum(m.get("estimated_cost_usd", 0.0) for m in by_model.values())

    return {
        "run_id": run_id,
        "fixture": str(fixture.relative_to(REPO_ROOT))
        if fixture.is_relative_to(REPO_ROOT)
        else str(fixture),
        "model_requested": model,
        "backend": backend,
        "started_at": started_at.isoformat(),
        "exit_code": exit_code,
        "wall_clock_seconds": round(wall_seconds, 2),
        "pipeline_seconds": round(pipeline_ended - pipeline_started, 2),
        "ksi_classifications_produced": _count_ksi_classifications(workspace),
        "artifacts_present": {
            "scan_json": _has_artifact(workspace, "scan-*.json"),
            "gap_json": _has_artifact(workspace, "gap-*.json"),
            "documentation_json": _has_artifact(workspace, "documentation-*.json"),
            "poam_md": _has_artifact(workspace, "poam/poam-*.md"),
            "oscal_poam_json": _has_artifact(workspace, "oscal/poam-*.json"),
            "oscal_cd_json": _has_artifact(workspace, "oscal/component-definition-*.json"),
        },
        "cost_by_model": by_model,
        "total_estimated_cost_usd": round(total_cost, 4),
        "log_path": str(log_path.relative_to(output_root)),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--fixture",
        type=Path,
        required=True,
        help="Path to the fixture directory (under evals/fixtures/).",
    )
    parser.add_argument(
        "--model",
        default="claude-haiku-4-5",
        help="LLM model ID. Default: claude-haiku-4-5 (cheapest published-quality).",
    )
    parser.add_argument(
        "--backend",
        choices=["anthropic", "bedrock"],
        default="anthropic",
        help="LLM backend. Default: anthropic.",
    )
    parser.add_argument(
        "--region",
        default=None,
        help=(
            "AWS region for --backend bedrock (e.g., us-east-1). "
            "Required when backend=bedrock; ignored otherwise."
        ),
    )
    parser.add_argument(
        "--runs",
        type=int,
        default=1,
        help="Number of runs (latency is bimodal; >=3 recommended for medians).",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path("/tmp/efterlev-benchmark-results"),
        help=(
            "Output directory root. Each run goes under <output>/<timestamp>/runs/<N>/. "
            "MUST be outside the efterlev repo (the per-run workspace is a fixture "
            "COPY, and `efterlev scan` rejects --target below a `.github/workflows/` "
            "ancestor — the efterlev repo itself has one). Default /tmp/... avoids "
            "this trip; the dispatch workflow uses ${RUNNER_TEMP}/."
        ),
    )
    args = parser.parse_args()

    if not args.fixture.is_dir():
        print(f"error: fixture path is not a directory: {args.fixture}", file=sys.stderr)
        return 2

    if args.backend == "bedrock" and not args.region:
        print("error: --region is required when --backend=bedrock", file=sys.stderr)
        return 2

    fixture_resolved = args.fixture.resolve()
    timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
    run_root = args.output / timestamp
    run_root.mkdir(parents=True, exist_ok=True)

    results: list[dict] = []
    for i in range(args.runs):
        run_id = f"run-{i + 1:02d}"
        per_run_root = run_root / "runs" / run_id
        print(
            f"[benchmark] {run_id}: fixture={fixture_resolved.name} "
            f"model={args.model} backend={args.backend}",
            file=sys.stderr,
        )
        result = benchmark_one_run(
            fixture_resolved,
            args.model,
            args.backend,
            args.region,
            run_id,
            per_run_root,
        )
        results.append(result)
        print(
            f"[benchmark] {run_id}: exit={result['exit_code']} "
            f"wall={result['wall_clock_seconds']}s "
            f"cost=${result['total_estimated_cost_usd']:.4f}",
            file=sys.stderr,
        )
        # Surface pipeline.log on non-zero exit so CI runs can see WHY
        # the pipeline failed without having to download artifacts.
        if result["exit_code"] != 0:
            log_path = per_run_root / "pipeline.log"
            if log_path.is_file():
                tail = log_path.read_text(encoding="utf-8").splitlines()[-80:]
                print(f"[benchmark] {run_id} pipeline.log tail:", file=sys.stderr)
                for line in tail:
                    print(f"  {line}", file=sys.stderr)

    summary = {
        "tool_version": _read_version(),
        "fixture": str(fixture_resolved.relative_to(REPO_ROOT))
        if fixture_resolved.is_relative_to(REPO_ROOT)
        else str(fixture_resolved),
        "model_requested": args.model,
        "backend": args.backend,
        "runs_requested": args.runs,
        "runs": results,
        "aggregate": _aggregate(results),
        "completed_at": datetime.now(UTC).isoformat(),
    }
    summary_path = run_root / "summary.json"
    summary_path.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")

    print(f"\n[benchmark] wrote {summary_path}", file=sys.stderr)
    print(f"[benchmark] aggregate: {json.dumps(summary['aggregate'], indent=2)}")
    return 0 if all(r["exit_code"] == 0 for r in results) else 1


def _aggregate(results: list[dict]) -> dict:
    """Compute mean / median / p95 / max for wall-clock + cost across runs."""
    if not results:
        return {}
    successful = [r for r in results if r["exit_code"] == 0]
    if not successful:
        return {"successful_runs": 0, "total_runs": len(results)}

    wall = sorted(r["wall_clock_seconds"] for r in successful)
    cost = sorted(r["total_estimated_cost_usd"] for r in successful)
    n = len(successful)

    def _p(vals: list[float], q: float) -> float:
        idx = max(0, min(n - 1, round(q * (n - 1))))
        return round(vals[idx], 4)

    return {
        "successful_runs": n,
        "total_runs": len(results),
        "wall_clock_seconds": {
            "mean": round(sum(wall) / n, 2),
            "median": _p(wall, 0.5),
            "p95": _p(wall, 0.95),
            "max": _p(wall, 1.0),
        },
        "estimated_cost_usd": {
            "mean": round(sum(cost) / n, 4),
            "median": _p(cost, 0.5),
            "p95": _p(cost, 0.95),
            "max": _p(cost, 1.0),
        },
    }


def _read_version() -> str:
    """Read efterlev.__version__ without forcing the package to import the CLI."""
    init = REPO_ROOT / "src" / "efterlev" / "__init__.py"
    for line in init.read_text(encoding="utf-8").splitlines():
        if line.startswith("__version__"):
            return line.split("=", 1)[1].strip().strip('"').strip("'")
    return "unknown"


if __name__ == "__main__":
    sys.exit(main())
