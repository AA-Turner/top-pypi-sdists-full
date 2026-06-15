"""Benchmark orchestrator — parse suite, execute cases, aggregate reports."""
from __future__ import annotations

import json
import time
from dataclasses import dataclass, field
from pathlib import Path


def _find_existing_task(case_id: str, mode: str, tasks_dir: Path) -> dict | None:
    """Find existing task matching case_id + mode by scanning spec.md headers.

    Enables the two-run pattern: first run creates tasks, user executes them,
    second run re-judges the SAME tasks instead of creating new ones.

    Matching criteria:
    - spec.md first line is '# {case_id}'
    - task.json 'mode' field matches

    Returns {task_id, task_dir, iteration} or None.
    """
    if not tasks_dir.exists():
        return None
    for task_subdir in tasks_dir.iterdir():
        if not task_subdir.is_dir():
            continue
        spec_file = task_subdir / "spec.md"
        task_json = task_subdir / "task.json"
        if not spec_file.exists() or not task_json.exists():
            continue
        try:
            first_line = spec_file.read_text(encoding="utf-8").split("\n")[0]
            if not first_line.startswith("# "):
                continue
            if first_line[2:].strip() != case_id:
                continue
            task_data = json.loads(task_json.read_text(encoding="utf-8"))
            if task_data.get("mode", "lightweight") != mode:
                continue
            return {
                "task_id": task_subdir.name,
                "task_dir": str(task_subdir),
                "iteration": task_data.get("iteration", 1),
            }
        except (json.JSONDecodeError, OSError):
            continue
    return None


@dataclass
class BenchmarkCase:
    id: str
    requirement: str
    acceptance: list[str]
    mode: str | None = None
    modes: list[str] | None = None  # case-level mode override (limits which modes this case runs in)
    expected_knowledge: list[str] | None = None  # KB entry IDs expected in search


@dataclass
class BenchmarkSuite:
    path: Path
    mode: str
    cases: list[BenchmarkCase]
    modes: list[str] | None = None  # multi-mode — when set, each case runs in all listed modes


def parse_suite(suite_path: Path) -> BenchmarkSuite:
    """Parse a benchmark suite YAML file."""
    import yaml

    if not suite_path.exists():
        raise FileNotFoundError(f"Suite file not found: {suite_path}")

    with open(suite_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)

    if not data:
        raise ValueError(f"Empty or invalid YAML: {suite_path}")

    if "cases" not in data or not isinstance(data["cases"], list):
        raise ValueError(f"Suite must have a 'cases' list: {suite_path}")

    if len(data["cases"]) == 0:
        raise ValueError(f"Suite must have at least one case: {suite_path}")

    mode = data.get("mode", "lightweight")
    modes = data.get("modes")  # list[str] | None — multi-mode support
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
            modes=c.get("modes"),
            expected_knowledge=c.get("expected_knowledge"),
        ))

    return BenchmarkSuite(path=suite_path, mode=mode, cases=cases, modes=modes)


class BenchmarkRunner:
    """Orchestrate benchmark suite execution."""

    def execute(self, suite_path: Path, output_path: Path | None = None) -> dict:
        """Run all cases in a suite and return aggregate report.

        Multi-mode: when suite.modes is set, each case runs in all listed modes.
        Single-mode: behaves identically to before (one run per case).
        """
        suite = parse_suite(suite_path)
        start_time = time.time()

        # Resolve effective modes: suite.modes (multi) takes precedence over suite.mode (single)
        effective_modes = suite.modes if suite.modes else [suite.mode]

        # case_results: list of {case, mode_results: {mode: CaseVerdict}}
        case_results = []
        for case in suite.cases:
            # Case-level modes override limits which modes this case runs in
            case_modes = case.modes if case.modes else effective_modes
            mode_results = {}
            for mode in case_modes:
                case_start = time.time()
                try:
                    from kanban_framework.domain.benchmark_judge import CaseVerdict
                    verdict = self._run_case(case, mode)
                    if "efficiency" not in verdict.dimensions:
                        verdict.dimensions["efficiency"] = {}
                    verdict.dimensions["efficiency"]["elapsed_seconds"] = int(time.time() - case_start)
                    mode_results[mode] = verdict
                except Exception as exc:
                    from kanban_framework.domain.benchmark_judge import CaseVerdict
                    mode_results[mode] = CaseVerdict(
                        case_id=case.id,
                        verdict="error",
                        score=0,
                        dimensions={},
                        acceptance_results=[],
                        evidence=str(exc),
                    )
            case_results.append({"case": case, "mode_results": mode_results})

        # Fetch task type metadata (category/domain) from KB for grouping
        task_types = self._fetch_task_types(suite.cases)

        report = self._build_report(suite, case_results, effective_modes, task_types, start_time)

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

        root = Filesystem.find_project_root()
        fs = Filesystem(root=root)
        tasks_dir = fs.kanban_dir / "tasks"

        # Check for existing task — reuse if found (enables two-run pattern:
        # first run creates, user executes, second run re-judges same tasks)
        existing = _find_existing_task(case.id, mode, tasks_dir)
        if existing:
            task_id = existing["task_id"]
            task_dir = existing["task_dir"]
        else:
            # First run: create new task via --manual scaffolding
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

            # Overwrite spec.md with the case requirement (creates matching header)
            if task_dir:
                spec_path = Path(task_dir) / "spec.md"
                spec_path.write_text(f"# {case.id}\n\n{case.requirement}\n")

        # Judge — task execution happens externally via kanban run
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

        # If no evaluation happened yet (no reports), report as pending instead of fail
        has_reports = report_dir.exists() and any(report_dir.rglob("*_report.json"))
        if not has_reports:
            verdict.verdict = "pending"
            verdict.evidence = (
                f"Task {task_id} created. Run `kanban run {task_id}` to execute, "
                f"then re-run benchmark to judge."
            )

        verdict.task_id = task_id
        verdict.task_dir = task_dir or ""

        # v0.188: Inject LLM efficiency stats from Claude Code JSONL logs.
        # This gives each verdict cost/efficiency dimensions alongside
        # quality dimensions, enabling "quality per call" analysis.
        try:
            from kanban_framework.domain.llm_stats import LLMStatsReader
            reader = LLMStatsReader(root)
            # v0.192: Use hybrid algorithm (assistant-only region + API filter).
            # Fixes #652: previous two-step counted user/tool_result mentions of
            # task_id, which caused quick/lightweight windows to overlap in
            # benchmark sessions. Now only assistant tool_use commands define
            # the region → per-task precise + broad coverage.
            llm_stats = reader.get_task_api_calls(task_id)
            _calls = llm_stats.get("total_calls", 0)
            _tokens = llm_stats.get("tokens", {})
            _inp = _tokens.get("input", 0)
            _out = _tokens.get("output", 0)
            _cache = _tokens.get("cache_read", 0)
            verdict.llm_calls = _calls
            verdict.llm_tokens_input = _inp
            verdict.llm_tokens_output = _out
            verdict.llm_tokens_cache_read = _cache
            verdict.llm_tokens_effective = _inp + _out
            if _calls > 0 and verdict.score > 0:
                verdict.llm_quality_per_call = round(
                    verdict.score / _calls, 3
                )
            if verdict.llm_tokens_effective > 0 and verdict.score > 0:
                verdict.llm_score_per_1k_tokens = round(
                    verdict.score / (verdict.llm_tokens_effective / 1000), 3
                )
            total_input = _cache + _inp
            if total_input > 0:
                verdict.llm_cache_efficiency = round(
                    _cache / total_input, 3
                )
        except Exception:
            pass  # LLM stats not available (no JSONL, reader error, etc.)

        return verdict

    # Standard 5-dimension scoring + kb_compliance (LLM judge, optional)
    _DIMENSION_WEIGHTS = {
        "code_correctness": 0.25,
        "test_coverage": 0.20,
        "kb_utilization": 0.15,
        "solution_quality": 0.15,
        "acceptance_match": 0.15,
        "kb_compliance": 0.10,
    }

    # Map sub-agent report roles to standard dimensions
    _ROLE_TO_DIMENSION = {
        "code_reviewer": "code_correctness",
        "qa": "test_coverage",
        "knowledge_manager": "kb_utilization",
        "product_reviewer": "solution_quality",
        "designer": "solution_quality",
        "kb_compliance": "kb_compliance",
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

    def _fetch_task_types(self, cases: list) -> dict:
        """Fetch KB category/domain for each case via expected_knowledge.

        Returns {case_id: {"category": str, "domain": str}} for cases that
        have expected_knowledge. Used for task-type-based mode comparison.
        """
        result = {}
        try:
            from kanban_framework.infra.filesystem import Filesystem
            from kanban_framework.domain.knowledge import KnowledgeManager
            root = Filesystem.find_project_root()
            fs = Filesystem(root=root)
            km = KnowledgeManager(fs, read_only=True)
        except Exception:
            return result

        for case in cases:
            if not case.expected_knowledge:
                continue
            kid = case.expected_knowledge[0]
            try:
                entry = km.get_entry(kid)
                if entry:
                    result[case.id] = {
                        "category": entry.get("category", "未知"),
                        "domain": entry.get("domain", "未知"),
                    }
            except Exception:
                pass
        return result

    def _build_report(self, suite: BenchmarkSuite, case_results: list,
                      effective_modes: list[str], task_types: dict, start_time: float) -> dict:
        """Build aggregate report from all case results.

        Supports both single-mode (backward-compatible flat format) and multi-mode
        (results_by_mode per case + by_mode aggregation).
        """
        is_multi = len(effective_modes) > 1

        # Collect all verdicts for dimension summary (flatten across modes)
        all_verdicts = []
        for cr in case_results:
            all_verdicts.extend(cr["mode_results"].values())

        total_cases = len(case_results)
        total_runs = len(all_verdicts)
        passed = sum(1 for v in all_verdicts if v.verdict == "pass")
        failed = sum(1 for v in all_verdicts if v.verdict == "fail")
        pending = sum(1 for v in all_verdicts if v.verdict == "pending")
        scores = [v.score for v in all_verdicts if v.score > 0]

        # Build per-case output
        cases_output = []
        for cr in case_results:
            case = cr["case"]
            mode_results = cr["mode_results"]

            # results_by_mode: {mode: {task_id, verdict, score, dimensions, evidence}}
            results_by_mode = {}
            for mode, v in mode_results.items():
                results_by_mode[mode] = {
                    "verdict": v.verdict,
                    "score": v.score,
                    "dimensions": v.dimensions,
                    "evidence": v.evidence,
                    "task_id": v.task_id,
                    "task_dir": v.task_dir,
                    # v0.188: LLM efficiency per case per mode
                    "llm_calls": v.llm_calls,
                    "llm_tokens_effective": v.llm_tokens_effective,
                    "llm_quality_per_call": v.llm_quality_per_call,
                    "llm_cache_efficiency": v.llm_cache_efficiency,
                }

            case_entry = {
                "id": case.id,
                "results_by_mode": results_by_mode,
            }

            # Attach task type metadata (category/domain from KB)
            if case.id in task_types:
                case_entry["task_type"] = task_types[case.id]

            # Single-mode backward compat: also emit flat verdict/score at top level
            if not is_multi and len(mode_results) == 1:
                sole_verdict = list(mode_results.values())[0]
                case_entry["verdict"] = sole_verdict.verdict
                case_entry["score"] = sole_verdict.score
                case_entry["dimensions"] = sole_verdict.dimensions
                case_entry["evidence"] = sole_verdict.evidence
                case_entry["task_id"] = sole_verdict.task_id
                case_entry["task_dir"] = sole_verdict.task_dir

            cases_output.append(case_entry)

        # by_mode aggregation
        by_mode = {}
        for mode in effective_modes:
            mode_verdicts = [cr["mode_results"][mode] for cr in case_results if mode in cr["mode_results"]]
            if not mode_verdicts:
                continue
            m_scores = [v.score for v in mode_verdicts if v.score > 0]
            # Collect elapsed_seconds for efficiency comparison
            m_times = [
                v.dimensions.get("efficiency", {}).get("elapsed_seconds", 0)
                for v in mode_verdicts
                if isinstance(v.dimensions.get("efficiency", {}), dict)
            ]
            valid_times = [t for t in m_times if t > 0]
            # v0.188: LLM efficiency aggregation per mode
            m_calls = [v.llm_calls for v in mode_verdicts if v.llm_calls > 0]
            m_tokens = [v.llm_tokens_effective for v in mode_verdicts if v.llm_tokens_effective > 0]
            m_qpc = [v.llm_quality_per_call for v in mode_verdicts if v.llm_quality_per_call > 0]
            m_cache = [v.llm_cache_efficiency for v in mode_verdicts if v.llm_cache_efficiency > 0]
            by_mode[mode] = {
                "avg_score": round(sum(m_scores) / len(m_scores), 1) if m_scores else 0,
                "passed": sum(1 for v in mode_verdicts if v.verdict == "pass"),
                "failed": sum(1 for v in mode_verdicts if v.verdict == "fail"),
                "pending": sum(1 for v in mode_verdicts if v.verdict == "pending"),
                "avg_elapsed_seconds": round(sum(valid_times) / len(valid_times), 1) if valid_times else 0,
                # v0.188: LLM efficiency dimensions
                "avg_llm_calls": round(sum(m_calls) / len(m_calls), 1) if m_calls else 0,
                "avg_llm_tokens": round(sum(m_tokens) / len(m_tokens)) if m_tokens else 0,
                "avg_quality_per_call": round(sum(m_qpc) / len(m_qpc), 3) if m_qpc else 0,
                "avg_cache_efficiency": round(sum(m_cache) / len(m_cache), 3) if m_cache else 0,
            }

        # best/worst mode by avg_score
        best_mode = worst_mode = None
        if by_mode:
            sorted_modes = sorted(by_mode.items(), key=lambda x: x[1]["avg_score"], reverse=True)
            best_mode = sorted_modes[0][0]
            worst_mode = sorted_modes[-1][0]

        # mode_deltas: pairwise score differences between modes per case
        # Shows "how much better is mode A vs B for this specific task"
        mode_deltas = []
        if is_multi and len(effective_modes) >= 2:
            for cr in case_results:
                case = cr["case"]
                mode_results = cr["mode_results"]
                row = {"case_id": case.id}
                for m in effective_modes:
                    v = mode_results.get(m)
                    row[m] = v.score if v and v.score > 0 else None
                # Compute deltas between consecutive mode pairs
                for i in range(len(effective_modes) - 1):
                    m1, m2 = effective_modes[i], effective_modes[i + 1]
                    s1, s2 = row.get(m1), row.get(m2)
                    if s1 is not None and s2 is not None:
                        row[f"delta_{m1}_to_{m2}"] = round(s2 - s1, 1)
                mode_deltas.append(row)

        # by_task_type aggregation: mode performance grouped by KB category
        # Answers "which mode is best for 踩坑 vs 最佳实践 vs 反模式"
        by_task_type: dict[str, dict] = {}
        for cr in case_results:
            case = cr["case"]
            tt = task_types.get(case.id)
            if not tt:
                continue
            category = tt.get("category", "未知")
            if category not in by_task_type:
                by_task_type[category] = {"cases": [], "by_mode": {}}
            by_task_type[category]["cases"].append(case.id)
            for mode, v in cr["mode_results"].items():
                if mode not in by_task_type[category]["by_mode"]:
                    by_task_type[category]["by_mode"][mode] = []
                by_task_type[category]["by_mode"][mode].append(v.score)

        # Compute averages per task_type × mode + identify best mode per type
        for cat_data in by_task_type.values():
            cat_data["case_count"] = len(cat_data["cases"])
            cat_best_score = -1
            cat_best_mode = None
            for mode, score_list in cat_data["by_mode"].items():
                valid = [s for s in score_list if s > 0]
                avg = round(sum(valid) / len(valid), 1) if valid else 0
                cat_data["by_mode"][mode] = {"avg_score": avg, "runs": len(score_list)}
                if avg > cat_best_score:
                    cat_best_score = avg
                    cat_best_mode = mode
            cat_data["best_mode"] = cat_best_mode

        report = {
            "suite": str(suite.path.name),
            "mode": "multi" if is_multi else suite.mode,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S+00:00", time.gmtime(start_time)),
            "elapsed_seconds": int(time.time() - start_time),
            "summary": {
                "total": total_cases,
                "total_runs": total_runs,
                "passed": passed,
                "failed": failed,
                "pending": pending,
                "avg_score": round(sum(scores) / len(scores), 1) if scores else 0,
            },
            "dimensions": self._report_dimension_summary(all_verdicts),
            "weights": self._DIMENSION_WEIGHTS,
            "cases": cases_output,
        }

        # Multi-mode extras
        if is_multi:
            report["modes"] = effective_modes
            report["by_mode"] = by_mode
            report["best_mode"] = best_mode
            report["worst_mode"] = worst_mode
            if by_task_type:
                report["by_task_type"] = by_task_type
            if mode_deltas:
                report["mode_deltas"] = mode_deltas

        # v0.188: Cost-effectiveness analysis — which mode gives best
        # quality per LLM call? Answers "is the extra calls worth it?"
        cost_eff: list[dict] = []
        for mode in effective_modes:
            mv = [cr["mode_results"][mode] for cr in case_results if mode in cr["mode_results"]]
            valid = [v for v in mv if v.llm_calls > 0 and v.score > 0]
            if not valid:
                continue
            avg_calls = sum(v.llm_calls for v in valid) / len(valid)
            avg_score = sum(v.score for v in valid) / len(valid)
            avg_qpc = sum(v.llm_quality_per_call for v in valid) / len(valid)
            cost_eff.append({
                "mode": mode,
                "avg_score": round(avg_score, 1),
                "avg_calls": round(avg_calls, 1),
                "avg_quality_per_call": round(avg_qpc, 3),
                "verdict": (
                    "高性价比" if avg_qpc >= 0.4 else
                    "中等效率" if avg_qpc >= 0.2 else
                    "高质量但低效率"
                ),
            })
        cost_eff.sort(key=lambda x: -x["avg_quality_per_call"])
        if cost_eff:
            report["cost_effectiveness"] = {
                "ranking": cost_eff,
                "best_efficiency_mode": cost_eff[0]["mode"],
                "recommendation": (
                    f"{cost_eff[0]['mode']} 模式效率最高（"
                    f"{cost_eff[0]['avg_quality_per_call']} score/call），"
                    f"在 {cost_eff[0]['avg_score']} 分下只花 {cost_eff[0]['avg_calls']} calls"
                ),
            }

        return report


def compare_reports(current: dict, previous_path: Path) -> dict:
    """Compare two benchmark reports and highlight deltas."""
    import json as _json

    if not previous_path.exists():
        return {"error": f"Previous report not found: {previous_path}"}

    previous = _json.loads(previous_path.read_text())

    # v0.186.2 (#643): defensively handle non-dict previous file.
    # Previously crashed with AttributeError when user passed a JSON list
    # (e.g., `[]`) or other non-dict format. Now returns a friendly error
    # explaining the expected format.
    if not isinstance(previous, dict):
        actual_type = type(previous).__name__
        if isinstance(previous, list):
            return {
                "error": (
                    f"Previous report ({previous_path}) is a JSON list, "
                    f"expected a dict with 'cases' key. "
                    f"Did you pass the wrong file? Expected output of "
                    f"`kanban benchmark run --output FILE`."
                ),
                "expected_format": "dict with 'cases' key",
                "actual_format": f"list (length {len(previous)})",
            }
        return {
            "error": (
                f"Previous report ({previous_path}) is {actual_type}, "
                f"expected a dict with 'cases' key."
            ),
            "expected_format": "dict with 'cases' key",
            "actual_format": actual_type,
        }

    # Also defend against current being non-dict (symmetric protection)
    if not isinstance(current, dict):
        return {
            "error": (
                f"Current report is {type(current).__name__}, "
                f"expected a dict with 'cases' key."
            ),
            "expected_format": "dict with 'cases' key",
        }

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
