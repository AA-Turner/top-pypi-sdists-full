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
    expected_knowledge: list[str] | None = None  # KB entry IDs expected in search


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
            expected_knowledge=c.get("expected_knowledge"),
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

        # Normalize raw sub-agent scores to standard 5 dimensions + kb_usage
        matched_ratio = (sum(1 for a in verdict.acceptance_results if a["matched"])
                         / len(verdict.acceptance_results)
                         if verdict.acceptance_results else 0)
        # If case was generated from a KB entry (verify_K001 → K001), get usage data
        kb_entry_id = None
        if verdict.case_id.startswith("verify_"):
            kb_entry_id = verdict.case_id.replace("verify_", "")
        kb_usage = self._score_kb_usage(kb_entry_id) if kb_entry_id else None
        # Search quality: compare KB search results vs expected knowledge
        search_quality = None
        if case.expected_knowledge:
            from kanban_framework.domain.benchmark_judge import score_search_quality
            search_quality = score_search_quality(
                case.requirement, case.expected_knowledge,
            )
        verdict.dimensions = self._normalize_dimensions(verdict.dimensions, matched_ratio, kb_usage)
        if search_quality:
            verdict.dimensions["search_quality"] = search_quality["f1"] * 10.0
            verdict.evidence += (
                f" | Search: precision={search_quality['precision']} "
                f"recall={search_quality['recall']} f1={search_quality['f1']}"
            )

        # Recompute score using dimension weights
        if verdict.dimensions:
            weighted_sum = 0.0
            total_weight = 0.0
            for dim_name, score in verdict.dimensions.items():
                weight = self._DIMENSION_WEIGHTS.get(dim_name, 0.05)
                weighted_sum += score * weight
                total_weight += weight
            verdict.score = round(weighted_sum / total_weight, 1) if total_weight > 0 else 0.0

        # If no evaluation happened yet, report as pending instead of fail
            verdict.verdict = "pending"
            verdict.evidence = (
                f"Task {task_id} created. Run `kanban run {task_id}` to execute, "
                f"then re-run benchmark to judge."
            )

        return verdict

    # Standard 5-dimension scoring with default weights
    _DIMENSION_WEIGHTS = {
        "code_correctness": 0.30,
        "test_coverage": 0.20,
        "kb_utilization": 0.20,
        "solution_quality": 0.15,
        "acceptance_match": 0.15,
    }

    # Map sub-agent report roles to standard dimensions
    _ROLE_TO_DIMENSION = {
        "code_reviewer": "code_correctness",
        "qa": "test_coverage",
        "knowledge_manager": "kb_utilization",
        "product_reviewer": "solution_quality",
        "designer": "solution_quality",
    }

    # KB usage dimension: maps entry effectiveness to a 0-10 score
    # ref_count=0 → 0, ref_count>=5 → 8, ref_count>=10 → 10
    def _score_kb_usage(self, entry_id: str) -> float | None:
        """Score knowledge entry usage/reference frequency as a 0-10 dimension."""
        try:
            from kanban_framework.infra.filesystem import Filesystem as FS
            from kanban_framework.domain.knowledge import KnowledgeManager
            root = FS.find_project_root()
            fs = FS(root=root)
            km = KnowledgeManager(fs, read_only=True)
            entry = km.get_entry(entry_id)
            if not entry:
                return None
            ref_count = entry.get("referenced_count") or 0
            eff = entry.get("effectiveness")
            if isinstance(eff, str):
                import json as _json
                try:
                    eff = _json.loads(eff)
                except Exception:
                    eff = None
            eff_score = eff.get("score") if isinstance(eff, dict) else None
            # Usage score: 40% ref count + 60% effectiveness
            ref_score = min(10.0, ref_count * 2.0)
            eff_component = (eff_score or 0.5) * 10.0
            return round(0.4 * ref_score + 0.6 * eff_component, 1)
        except Exception:
            return None

    def _normalize_dimensions(self, raw_dimensions: dict, acceptance_match: float,
                               kb_usage: float | None = None) -> dict:
        """Map raw sub-agent scores to standard 5 dimensions + kb_usage."""
        dims = {}
        for role, score in raw_dimensions.items():
            dim_name = self._ROLE_TO_DIMENSION.get(role)
            if dim_name:
                dims[dim_name] = max(dims.get(dim_name, 0), score)
        dims["acceptance_match"] = round(acceptance_match * 10, 1)
        if kb_usage is not None:
            dims["kb_usage"] = kb_usage
        return dims

    def _report_dimension_summary(self, case_results: list) -> dict:
        """Compute per-dimension averages across all cases."""
        dim_totals: dict[str, float] = {}
        dim_counts: dict[str, int] = {}
        for c in case_results:
            for dim_name in self._DIMENSION_WEIGHTS:
                val = c.dimensions.get(dim_name)
                if val is not None:
                    dim_totals[dim_name] = dim_totals.get(dim_name, 0) + val
                    dim_counts[dim_name] = dim_counts.get(dim_name, 0) + 1
        return {
            dim_name: {
                "avg": round(dim_totals[dim_name] / dim_counts[dim_name], 1),
                "weight": weight,
            }
            for dim_name, weight in self._DIMENSION_WEIGHTS.items()
            if dim_name in dim_totals and dim_counts[dim_name] > 0
        }

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
            "dimensions": self._report_dimension_summary(case_results),
            "weights": self._DIMENSION_WEIGHTS,
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
