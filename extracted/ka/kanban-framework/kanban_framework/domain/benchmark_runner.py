"""Benchmark orchestrator — parse suite, execute cases, aggregate reports."""
from __future__ import annotations

import time
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class BenchmarkCase:
    id: str
    requirement: str
    acceptance: list[str]
    mode: str | None = None


@dataclass
class BenchmarkSuite:
    path: Path
    mode: str
    cases: list[BenchmarkCase]


def parse_suite(suite_path: Path) -> BenchmarkSuite:
    """Parse a benchmark suite YAML file."""
    import yaml

    if not suite_path.exists():
        raise FileNotFoundError(f"Suite file not found: {suite_path}")

    with open(suite_path) as f:
        data = yaml.safe_load(f)

    if not data:
        raise ValueError(f"Empty or invalid YAML: {suite_path}")

    if "cases" not in data or not isinstance(data["cases"], list):
        raise ValueError(f"Suite must have a 'cases' list: {suite_path}")

    if len(data["cases"]) == 0:
        raise ValueError(f"Suite must have at least one case: {suite_path}")

    mode = data.get("mode", "lightweight")
    cases = []

    for i, c in enumerate(data["cases"]):
        if "id" not in c:
            raise ValueError(f"Case {i} in {suite_path} missing 'id'")
        if "requirement" not in c:
            raise ValueError(f"Case '{c['id']}' missing 'requirement'")
        if "acceptance" not in c:
            raise ValueError(f"Case '{c['id']}' missing 'acceptance'")

        cases.append(BenchmarkCase(
            id=c["id"],
            requirement=c["requirement"].strip(),
            acceptance=c["acceptance"] if isinstance(c["acceptance"], list) else [c["acceptance"]],
            mode=c.get("mode"),
        ))

    return BenchmarkSuite(path=suite_path, mode=mode, cases=cases)


class BenchmarkRunner:
    """Orchestrate benchmark suite execution."""

    def execute(self, suite_path: Path, output_path: Path | None = None) -> dict:
        """Run all cases in a suite and return aggregate report."""
        suite = parse_suite(suite_path)
        start_time = time.time()

        case_results = []
        for case in suite.cases:
            mode = case.mode or suite.mode
            case_start = time.time()
            try:
                from kanban_framework.domain.benchmark_judge import CaseVerdict
                verdict = self._run_case(case, mode)
                if "efficiency" not in verdict.dimensions:
                    verdict.dimensions["efficiency"] = {}
                verdict.dimensions["efficiency"]["elapsed_seconds"] = int(time.time() - case_start)
                case_results.append(verdict)
            except Exception as exc:
                from kanban_framework.domain.benchmark_judge import CaseVerdict
                case_results.append(CaseVerdict(
                    case_id=case.id,
                    verdict="error",
                    score=0,
                    dimensions={},
                    acceptance_results=[],
                    evidence=str(exc),
                ))

        report = self._build_report(suite, case_results, start_time)

        if output_path:
            import json as _json
            Path(output_path).write_text(_json.dumps(report, indent=2, ensure_ascii=False))

        return report

    def _run_case(self, case: BenchmarkCase, mode: str):
        """Execute a single benchmark case: create task + write spec, then judge.

        Task execution (plan → execute → evaluate) happens via external Claude Code
        agent spawn — the benchmark runner creates the task skeleton and judges the
        results. If the task hasn't been executed yet (no agent reports), it returns
        verdict "pending".
        """
        from kanban_framework.cli.task_create import cmd_create
        from kanban_framework.infra.filesystem import Filesystem
        from kanban_framework.infra.config import Config
        from kanban_framework.domain.task import TaskManager
        from kanban_framework.domain.benchmark_judge import judge_case, CaseVerdict

        # 1. Create task via --manual scaffolding
        title = case.requirement[:60].replace("\n", " ").strip()
        create_result = cmd_create([
            title,
            "--manual",
            "--control-mode", "auto",
            "--mode", mode,
        ])

        task_id = create_result.get("id")
        if not task_id:
            return CaseVerdict(
                case_id=case.id, verdict="error", score=0,
                dimensions={}, acceptance_results=[],
                evidence=f"Task creation failed: {create_result.get('error', 'unknown')}",
            )

        scaffold = create_result.get("scaffold") or {}
        task_dir = scaffold.get("task_dir")

        # 2. Overwrite spec.md with the case requirement
        if task_dir:
            spec_path = Path(task_dir) / "spec.md"
            spec_path.write_text(f"# {case.id}\n\n{case.requirement}\n")

        # 3. Judge — task execution happens externally via kanban run
        root = Filesystem.find_project_root()
        fs = Filesystem(root=root)
        cfg = Config(fs)
        tm = TaskManager(fs, cfg)

        try:
            task = tm.show(task_id)
            iteration = task.iteration
        except Exception:
            return CaseVerdict(
                case_id=case.id, verdict="error", score=0,
                dimensions={}, acceptance_results=[],
                evidence=f"Could not read task {task_id}",
            )
        report_dir = fs.kanban_dir / "tasks" / task_id / f"reports_{iteration}"

        verdict = judge_case(case.id, case.acceptance, report_dir)

        # If no evaluation happened yet, report as pending instead of fail
        if not verdict.dimensions and verdict.score == 0.0:
            verdict.verdict = "pending"
            verdict.evidence = (
                f"Task {task_id} created. Run `kanban run {task_id}` to execute, "
                f"then re-run benchmark to judge."
            )

        return verdict

    def _build_report(self, suite: BenchmarkSuite, case_results: list, start_time: float) -> dict:
        """Build aggregate report from all case results."""
        total = len(case_results)
        passed = sum(1 for c in case_results if c.verdict == "pass")
        failed = total - passed
        scores = [c.score for c in case_results if c.score > 0]

        return {
            "suite": str(suite.path.name),
            "mode": suite.mode,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(start_time)),
            "elapsed_seconds": int(time.time() - start_time),
            "summary": {
                "total": total,
                "passed": passed,
                "failed": failed,
                "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
            },
            "cases": [
                {
                    "id": c.case_id,
                    "verdict": c.verdict,
                    "score": c.score,
                    "dimensions": c.dimensions,
                    "evidence": c.evidence,
                }
                for c in case_results
            ],
        }


def compare_reports(current: dict, previous_path: Path) -> dict:
    """Compare two benchmark reports and highlight deltas."""
    import json as _json

    if not previous_path.exists():
        return {"error": f"Previous report not found: {previous_path}"}

    previous = _json.loads(previous_path.read_text())

    prev_cases = {c["id"]: c for c in previous.get("cases", [])}
    curr_cases = {c["id"]: c for c in current.get("cases", [])}
    deltas = []

    for cid, curr in curr_cases.items():
        prev = prev_cases.get(cid)
        if prev:
            deltas.append({
                "id": cid,
                "score_delta": round(curr["score"] - prev["score"], 1),
                "verdict": f"{prev['verdict']} -> {curr['verdict']}",
            })
        else:
            deltas.append({"id": cid, "score_delta": None, "verdict": "new"})

    return {
        "current_suite": current.get("suite"),
        "previous_suite": previous.get("suite"),
        "deltas": deltas,
    }
