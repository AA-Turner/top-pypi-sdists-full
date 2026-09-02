"""Read-only scheduled scanner for AI PR Loop supervisor candidates."""

from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import sys
from collections.abc import Mapping, Sequence
from dataclasses import dataclass, replace
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from agentic_devtools.cli.ci.github_provider import GitHubActionsProvider
from agentic_devtools.cli.ci.logging_config import setup_logging
from agentic_devtools.cli.ci.scheduler import AUTO_MERGE_LABEL
from agentic_devtools.cli.ci.supervisor import (
    SupervisorConfig,
    SupervisorEvidence,
    collect_supervisor_evidence,
    discover_supervisor_candidates,
    parse_agent_tasks,
)
from agentic_devtools.cli.github.repo_resolution import resolve_github_repo
from agentic_devtools.cli.subprocess_utils import run_safe


@dataclass(frozen=True)
class SupervisorRuntimeConfig:
    """Validated runtime configuration for a supervisor scan."""

    mode: str
    max_candidates: int
    thresholds: SupervisorConfig


def load_supervisor_config(path: Path) -> SupervisorRuntimeConfig:
    """Load staged supervisor settings, falling back to report-only defaults."""
    if not path.exists():
        return SupervisorRuntimeConfig("report_only", 10, SupervisorConfig())
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"could not load supervisor config: {exc}") from exc
    if not isinstance(payload, dict):
        raise ValueError("supervisor config must be a JSON object")
    mode = payload.get("mode", "report_only")
    max_candidates = payload.get("max_candidates", 10)
    thresholds = payload.get("thresholds", {})
    if not isinstance(mode, str) or not mode.strip():
        raise ValueError("mode must be a non-empty string")
    if type(max_candidates) is not int or max_candidates <= 0:
        raise ValueError("max_candidates must be a positive integer")
    if not isinstance(thresholds, dict):
        raise ValueError("thresholds must be a JSON object")
    return SupervisorRuntimeConfig(
        mode=mode.strip(),
        max_candidates=max_candidates,
        thresholds=SupervisorConfig(
            loop_stale_seconds=thresholds.get("loop_stale_seconds", 1800),
            task_stale_seconds=thresholds.get("task_stale_seconds", 1800),
            review_wait_seconds=thresholds.get("review_wait_seconds", 3600),
        ),
    )


def load_agent_tasks(repo: str) -> tuple[list[dict[str, Any]], str]:
    """Load task metadata through the GitHub CLI without raising on optional failure."""
    command = [
        "gh",
        "agent-task",
        "list",
        "--repo",
        repo,
        "--json",
        "id,status,pullRequestNumber,createdAt",
    ]
    try:
        result = run_safe(command, capture_output=True, text=True, shell=False, timeout=60)
    except subprocess.TimeoutExpired:
        return [], "agent_tasks: command timed out after 60s"
    except OSError as exc:
        return [], f"agent_tasks: {exc}"
    if result.returncode != 0:
        return [], f"agent_tasks: {result.stderr.strip() or 'command failed'}"
    return parse_agent_tasks(result.stdout), ""


def _candidate_to_dict(candidate: Any) -> dict[str, Any]:
    evidence = candidate.evidence
    return {
        "pr_number": evidence.pr_number,
        "head_sha": evidence.head_sha,
        "state": candidate.classification.state.value,
        "reasons": list(candidate.classification.reasons),
        "fingerprint": candidate.fingerprint,
        "api_errors": list(evidence.api_errors),
    }


def scan_supervisor(
    provider: Any,
    *,
    tasks: Sequence[object],
    now: datetime,
    repository: str,
    max_candidates: int,
    max_scan_prs: int | None = None,
    config: SupervisorConfig | None = None,
    loop_runs: Sequence[object] = (),
    evidence_overrides: Mapping[int, Mapping[str, Any]] | None = None,
    source_errors: Sequence[str] = (),
) -> dict[str, Any]:
    """Scan eligible PRs and return a JSON-serializable candidate report."""
    if max_scan_prs is not None and (type(max_scan_prs) is not int or max_scan_prs <= 0):
        raise ValueError("max_scan_prs must be a positive integer")
    scan_limit = max_scan_prs or max_candidates
    list_supervisor_prs = getattr(provider, "list_supervisor_prs", None)
    if callable(list_supervisor_prs):
        eligible = list_supervisor_prs(max_prs=scan_limit)
    else:
        eligible = provider.list_eligible_prs(max_prs=scan_limit)
    evidence: list[SupervisorEvidence] = []
    source_error_values = tuple(error for error in source_errors if error)
    errors = list(source_error_values)
    overrides = evidence_overrides or {}

    for eligible_pr in eligible:
        try:
            item = collect_supervisor_evidence(
                provider,
                eligible_pr.number,
                tasks=tasks,
                loop_runs=loop_runs,
                now=now,
            )
            item_overrides = dict(overrides.get(eligible_pr.number, {}))
            labels_to_propagate = getattr(eligible_pr, "labels_to_propagate", ())
            if (
                "has_auto_merge_label" not in item_overrides
                and isinstance(labels_to_propagate, tuple)
                and AUTO_MERGE_LABEL in labels_to_propagate
            ):
                item_overrides["has_auto_merge_label"] = True
            if item_overrides:
                item = replace(item, **item_overrides)
            if source_error_values:
                item = replace(item, api_errors=item.api_errors + source_error_values)
            evidence.append(item)
        except Exception as exc:
            errors.append(f"PR #{eligible_pr.number}: {exc}")

    candidates = discover_supervisor_candidates(
        evidence,
        now=now,
        config=config,
        repository=repository,
        max_candidates=max_candidates,
    )
    return {
        "repository": repository,
        "observed_at": now.astimezone(UTC).isoformat(),
        "scanned_count": len(evidence),
        "candidate_count": len(candidates),
        "candidates": [_candidate_to_dict(candidate) for candidate in candidates],
        "errors": errors,
    }


def _write_step_summary(report: Mapping[str, Any]) -> None:
    summary_path = os.environ.get("GITHUB_STEP_SUMMARY", "").strip()
    if not summary_path:
        return
    candidates = report.get("candidates", [])
    with open(summary_path, "a", encoding="utf-8") as handle:
        handle.write("## AI PR Loop Supervisor Scan\n\n")
        handle.write("| Metric | Value |\n| --- | --- |\n")
        handle.write(f"| PRs scanned | {report.get('scanned_count', 0)} |\n")
        handle.write(f"| Candidates | {report.get('candidate_count', 0)} |\n")
        handle.write(f"| Errors | {len(report.get('errors', []))} |\n")
        for candidate in candidates:
            handle.write(
                f"\n- PR #{candidate['pr_number']}: {', '.join(candidate['reasons'])} (`{candidate['fingerprint']}`)\n"
            )


def ai_pr_loop_supervisor_command() -> None:
    """CLI entry point for the scheduled read-only supervisor scan."""
    setup_logging()
    parser = argparse.ArgumentParser(description="Scan AI PR Loop for stuck pull requests")
    parser.add_argument("--repo", default=None, help="Repository in owner/repo format")
    parser.add_argument("--max-candidates", type=int, default=10, help="Maximum PRs to report")
    args = parser.parse_args()

    if shutil.which("gh") is None:
        print("Error: 'gh' CLI not found on PATH.", file=sys.stderr)
        sys.exit(10)
    if args.max_candidates <= 0:
        print("Error: --max-candidates must be positive.", file=sys.stderr)
        sys.exit(2)

    repo = resolve_github_repo(args.repo or os.environ.get("GITHUB_REPOSITORY"))
    runtime_config = load_supervisor_config(Path(".github/ai-pr-loop-supervisor.json"))
    provider = GitHubActionsProvider(repo=repo)
    tasks, task_error = load_agent_tasks(repo)
    loop_runs: Sequence[object] = ()
    source_errors: list[str] = []
    list_workflow_runs = getattr(provider, "list_workflow_runs", None)
    if callable(list_workflow_runs):
        try:
            try:
                loop_runs = list_workflow_runs(
                    "ai-pr-loop.yml",
                    window_hours=24,
                    status=None,
                    include_dispatch_inputs=True,
                    max_dispatch_enrichments=min(args.max_candidates, runtime_config.max_candidates) * 4,
                )
            except TypeError:
                loop_runs = list_workflow_runs("ai-pr-loop.yml", window_hours=24, status=None)
        except Exception as exc:
            source_errors.append(f"workflow_runs: {exc}")
    if task_error:
        source_errors.append(task_error)
    try:
        candidate_limit = min(args.max_candidates, runtime_config.max_candidates)
        report = scan_supervisor(
            provider,
            tasks=tasks,
            now=datetime.now(UTC),
            repository=repo,
            max_candidates=candidate_limit,
            max_scan_prs=candidate_limit * 4,
            config=runtime_config.thresholds,
            loop_runs=loop_runs,
            source_errors=tuple(source_errors),
        )
    except Exception as exc:
        print(f"Error: supervisor scan failed: {exc}", file=sys.stderr)
        sys.exit(1)
    _write_step_summary(report)
    print(json.dumps(report, sort_keys=True))
