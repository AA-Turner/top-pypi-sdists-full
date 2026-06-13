"""Benchmark CLI — `kanban benchmark run <suite.yml>` and `generate --from-kb`."""
from __future__ import annotations
from pathlib import Path


def dispatch(args: list[str]) -> dict:
    """Route benchmark subcommands."""
    sub = args[0] if args else ""

    if sub in ("--help", "-h", "help", ""):
        return {
            "help": True,
            "message": (
                "Usage: kanban benchmark <subcommand> [options]\n"
                "  run <suite.yml> [--output report.json] [--md-output report.md] [--compare FILE]\n"
                "  generate --from-kb [--kb-id K1,K2] [--domain X] [--count N] [--output suite.yml]\n"
                "  judge-kb <suite.yml> — LLM judge KB compliance for executed tasks\n"
                "  compare <current.json> <previous.json> — compare two reports"
            ),
            "commands": {
                "run": "Execute all cases in a benchmark suite YAML file",
                "generate": "Prepare KB data for agent to generate suite (needs orchestrator)",
                "judge-kb": "LLM judge: verify KB constraints in actual code",
                "compare": "Compare two benchmark reports (score deltas, verdict changes)",
            },
        }

    if sub == "run":
        return _cmd_run(args[1:])

    if sub == "generate":
        return _cmd_generate(args[1:])

    if sub == "judge-kb":
        return _cmd_judge_kb(args[1:])

    if sub == "compare":
        return _cmd_compare(args[1:])

    return {"error": f"unknown subcommand: {sub}. Try: kanban benchmark --help"}


def _cmd_run(args: list[str]) -> dict:
    """Run benchmark suite."""
    if not args or args[0] in ("--help", "-h"):
        return {
            "help": True,
            "message": "Usage: kanban benchmark run <suite.yml> [--output report.json] [--md-output report.md] [--bundle checklist.md] [--compare FILE]"
        }

    suite_path = args[0]
    output_path = None
    md_output_path = None
    bundle_path = None
    compare_path = None

    i = 1
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output_path = args[i + 1]
            i += 2
        elif args[i] == "--md-output" and i + 1 < len(args):
            md_output_path = args[i + 1]
            i += 2
        elif args[i] == "--bundle" and i + 1 < len(args):
            bundle_path = args[i + 1]
            i += 2
        elif args[i] == "--compare" and i + 1 < len(args):
            compare_path = args[i + 1]
            i += 2
        elif args[i] == "--json":
            i += 1
        else:
            i += 1

    from pathlib import Path
    from kanban_framework.domain.benchmark_runner import BenchmarkRunner

    runner = BenchmarkRunner()
    result = runner.execute(Path(suite_path).resolve(), output_path=output_path)

    if md_output_path:
        md_content = _build_markdown_report(result)
        Path(md_output_path).write_text(md_content, encoding="utf-8")
        result["md_output"] = md_output_path

    if bundle_path:
        from kanban_framework.domain.benchmark_runner import parse_suite
        suite = parse_suite(Path(suite_path).resolve())
        checklist = _build_review_checklist(result, suite)
        Path(bundle_path).write_text(checklist, encoding="utf-8")
        result["bundle_output"] = bundle_path

    if compare_path:
        from kanban_framework.domain.benchmark_runner import compare_reports
        prev = compare_reports(result, Path(compare_path).resolve())
        result["comparison"] = prev

    return result


def _build_markdown_report(report: dict) -> str:
    """Convert JSON benchmark report to human-readable Markdown."""
    lines = []
    suite = report.get("suite", "benchmark")
    ts = report.get("timestamp", "")
    elapsed = report.get("elapsed_seconds", 0)
    is_multi = report.get("mode") == "multi"
    modes = report.get("modes", [])
    summary = report.get("summary", {})

    # Title
    lines.append(f"# Benchmark Report — {suite}")
    lines.append("")
    lines.append(f"> {ts} | 耗时 {elapsed}s")
    lines.append("")

    # Summary
    total = summary.get("total", 0)
    total_runs = summary.get("total_runs", total)
    passed = summary.get("passed", 0)
    failed = summary.get("failed", 0)
    pending = summary.get("pending", 0)
    avg = summary.get("avg_score", 0)

    lines.append("## 总览")
    lines.append("")
    lines.append(f"| 指标 | 值 |")
    lines.append(f"|------|-----|")
    lines.append(f"| 用例数 | {total} |")
    lines.append(f"| 总执行数 | {total_runs} |")
    lines.append(f"| 通过 | **{passed}** |")
    lines.append(f"| 失败 | **{failed}** |")
    if pending:
        lines.append(f"| 待执行 | {pending} |")
    lines.append(f"| 平均分 | **{avg}** / 10 |")
    lines.append("")

    # Multi-mode comparison
    if is_multi and modes:
        by_mode = report.get("by_mode", {})
        best = report.get("best_mode", "")
        worst = report.get("worst_mode", "")

        lines.append("## Mode 对比")
        lines.append("")
        lines.append("| Mode | 平均分 | 通过 | 失败 | 待执行 | 平均耗时 |")
        lines.append("|------|--------|------|------|--------|---------|")
        for m in modes:
            s = by_mode.get(m, {})
            badge = ""
            if m == best:
                badge = " ⬆ 最佳"
            elif m == worst:
                badge = " ⬇ 最差"
            elapsed = s.get('avg_elapsed_seconds', 0)
            lines.append(
                f"| {m}{badge} | {s.get('avg_score', 0)} | {s.get('passed', 0)} | "
                f"{s.get('failed', 0)} | {s.get('pending', 0)} | {elapsed}s |"
            )
        lines.append("")

    # Mode deltas: per-case score differences between modes
    mode_deltas = report.get("mode_deltas", [])
    if is_multi and mode_deltas and len(modes) >= 2:
        lines.append("## Mode Delta（分数差）")
        lines.append("")
        lines.append("> 正值 = 后一个 mode 更好；负值 = 前一个 mode 更好")
        lines.append("")

        # Build delta table dynamically
        delta_keys = [k for k in mode_deltas[0].keys() if k.startswith("delta_")]
        header_modes = modes + [k.replace("delta_", "").replace("_to_", " → ") for k in delta_keys]
        lines.append("| 用例 | " + " | ".join(str(h) for h in header_modes) + " |")
        lines.append("|------" + "|".join(["------"] * len(header_modes)) + "|")
        for row in mode_deltas:
            cells = [row.get(m, "—") for m in modes]
            for dk in delta_keys:
                val = row.get(dk)
                if val is not None:
                    icon = "📈" if val > 0.5 else ("📉" if val < -0.5 else "➡️")
                    cells.append(f"{icon} {val:+.1f}")
                else:
                    cells.append("—")
            lines.append("| " + row.get("case_id", "?") + " | " + " | ".join(str(c) for c in cells) + " |")
        lines.append("")

    # Task type analysis: which mode suits which task type
    by_task_type = report.get("by_task_type", {})
    if is_multi and by_task_type:
        lines.append("## 按任务类型分析")
        lines.append("")
        lines.append("> 不同类型的任务适合不同的 mode — 基于知识库 category 分组")
        lines.append("")
        for cat, data in by_task_type.items():
            cat_best = data.get("best_mode", "")
            lines.append(f"### {cat}（{data.get('case_count', 0)} 个用例）")
            lines.append("")
            lines.append("| Mode | 平均分 | 执行数 |")
            lines.append("|------|--------|--------|")
            cat_modes = data.get("by_mode", {})
            for m in modes:
                if m in cat_modes:
                    ms = cat_modes[m]
                    badge = " ⭐ 推荐" if m == cat_best else ""
                    lines.append(f"| {m}{badge} | {ms.get('avg_score', 0)} | {ms.get('runs', 0)} |")
            lines.append("")

            # Insight
            if cat_best:
                lines.append(f"**洞察**: {cat} 类任务推荐用 **{cat_best}** mode")
                lines.append("")

    lines.append("## 用例详情")

    # Per-case details
    cases = report.get("cases", [])
    lines.append("")

    for case in cases:
        cid = case.get("id", "?")
        lines.append(f"### {cid}")
        lines.append("")

        if is_multi and "results_by_mode" in case:
            # Multi-mode: table per case
            lines.append("| Mode | Verdict | Score | KB合规 | 验收匹配 |")
            lines.append("|------|---------|-------|--------|---------|")
            results = case.get("results_by_mode", {})
            for m in modes:
                if m not in results:
                    lines.append(f"| {m} | — | — | — | — |")
                    continue
                v = results[m]
                verdict = v.get("verdict", "?")
                icon = {"pass": "✅", "fail": "❌", "pending": "⏳", "error": "💥"}.get(verdict, "?")
                score = v.get("score", 0)
                dims = v.get("dimensions", {})
                kb = dims.get("kb_compliance", "—")
                acc = dims.get("acceptance_match", "—")
                lines.append(f"| {m} | {icon} {verdict} | {score} | {kb} | {acc} |")
            lines.append("")

            # Dimensions detail for first mode (representative)
            first_mode_results = list(results.values())
            if first_mode_results:
                dims = first_mode_results[0].get("dimensions", {})
                if dims:
                    lines.append("<details><summary>维度详情</summary>")
                    lines.append("")
                    lines.append("| 维度 | 分数 |")
                    lines.append("|------|------|")
                    for dk, dv in dims.items():
                        if dk == "efficiency":
                            continue
                        lines.append(f"| {dk} | {dv} |")
                    lines.append("")
                    lines.append("</details>")
                    lines.append("")
        else:
            # Single mode: flat format
            verdict = case.get("verdict", "?")
            icon = {"pass": "✅", "fail": "❌", "pending": "⏳", "error": "💥"}.get(verdict, "?")
            score = case.get("score", 0)
            dims = case.get("dimensions", {})

            lines.append(f"- **Verdict**: {icon} {verdict}")
            lines.append(f"- **Score**: {score} / 10")
            lines.append("")

            if dims:
                lines.append("| 维度 | 分数 |")
                lines.append("|------|------|")
                for dk, dv in dims.items():
                    if dk == "efficiency":
                        continue
                    lines.append(f"| {dk} | {dv} |")
                lines.append("")

            evidence = case.get("evidence", "")
            if evidence:
                lines.append(f"<details><summary>Evidence</summary>")
                lines.append("")
                lines.append(f"``")
                lines.append(evidence[:500])
                lines.append(f"```")
                lines.append("")
                lines.append("</details>")
                lines.append("")

    # Footer
    lines.append("---")
    lines.append(f"*由 kanban benchmark 自动生成 | {suite}*")

    return "\n".join(lines)


def _build_review_checklist(report: dict, suite) -> str:
    """Generate human review checklist with task paths + acceptance verification."""
    lines = []
    suite_name = report.get("suite", "benchmark")
    is_multi = report.get("mode") == "multi"
    modes = report.get("modes", [])

    lines.append(f"# Review Checklist — {suite_name}")
    lines.append("")
    lines.append("> 人工审核清单 — 核对评分、查看任务产物、确认 acceptance、做决策")
    lines.append("")

    cases = report.get("cases", [])
    # Build case_id → acceptance_criteria map from suite
    case_acceptance: dict[str, list[str]] = {}
    for c in suite.cases:
        case_acceptance[c.id] = c.acceptance

    for case in cases:
        cid = case.get("id", "?")
        lines.append(f"---")
        lines.append(f"")
        lines.append(f"## 用例: {cid}")
        lines.append("")

        if is_multi and "results_by_mode" in case:
            results = case.get("results_by_mode", {})
            # Score table
            lines.append("### 评分")
            lines.append("")
            lines.append("| Mode | Verdict | Score | KB合规 |")
            lines.append("|------|---------|-------|--------|")
            for m in modes:
                v = results.get(m, {})
                verdict = v.get("verdict", "?")
                icon = {"pass": "✅", "fail": "❌", "pending": "⏳", "error": "💥"}.get(verdict, "?")
                score = v.get("score", 0)
                dims = v.get("dimensions", {})
                kb = dims.get("kb_compliance", "—")
                lines.append(f"| {m} | {icon} {verdict} | {score} | {kb} |")
            lines.append("")

            # Task artifacts — use first available mode's task_dir
            lines.append("### 任务产物（直接查看）")
            lines.append("")
            for m in modes:
                v = results.get(m, {})
                tid = v.get("task_id", "")
                tdir = v.get("task_dir", "")
                if tid:
                    lines.append(f"**{m}** ({tid}):")
                    if tdir:
                        lines.append(f"- spec: `{tdir}/spec.md`")
                        lines.append(f"- plan: `{tdir}/plan/index.md`")
                        lines.append(f"- execution: `{tdir}/execution_summary.md`")
                        lines.append(f"- review: `{tdir}/reports_1/reviews/`")
                    lines.append("")
        else:
            # Single mode
            verdict = case.get("verdict", "?")
            icon = {"pass": "✅", "fail": "❌", "pending": "⏳", "error": "💥"}.get(verdict, "?")
            tid = case.get("task_id", "")
            tdir = case.get("task_dir", "")
            # Also check results_by_mode if available (newer format)
            if not tid and "results_by_mode" in case:
                first = list(case["results_by_mode"].values())
                if first:
                    tid = first[0].get("task_id", "")
                    tdir = first[0].get("task_dir", "")
            lines.append(f"### 评分")
            lines.append("")
            lines.append(f"- Verdict: {icon} {verdict}")
            lines.append(f"- Score: {case.get('score', 0)}")
            if tid:
                lines.append(f"- Task: {tid}")
            lines.append("")

            if tdir:
                lines.append("### 任务产物（直接查看）")
                lines.append("")
                lines.append(f"- spec: `{tdir}/spec.md`")
                lines.append(f"- plan: `{tdir}/plan/index.md`")
                lines.append(f"- execution: `{tdir}/execution_summary.md`")
                lines.append(f"- review: `{tdir}/reports_1/reviews/`")
                lines.append("")

        # Acceptance checklist
        acceptance_criteria = case_acceptance.get(cid, [])
        if acceptance_criteria:
            lines.append("### Acceptance 核对")
            lines.append("")
            # Try to get acceptance_results from first mode result or flat
            acc_results = []
            if is_multi and "results_by_mode" in case:
                first_result = list(case.get("results_by_mode", {}).values())
                if first_result:
                    # acceptance_results aren't in report; use criteria with unknown status
                    pass
            # We don't have per-criterion matched status in the report JSON,
            # so show criteria as unchecked items for human verification
            for criterion in acceptance_criteria:
                lines.append(f"- [ ] {criterion}")
            lines.append("")

        # Decision
        lines.append("### 决策")
        lines.append("")
        lines.append("- [ ] 归档（评分满意）")
        lines.append("- [ ] 反馈 issue（发现问题）")
        lines.append("- [ ] 重新执行（需要改进）")
        lines.append("")

    lines.append("---")
    lines.append(f"*Review checklist generated by kanban benchmark | {suite_name}*")
    return "\n".join(lines)


def _cmd_generate(args: list[str]) -> dict:
    """Prepare KB data for the kanban-benchmark-generator agent.

    This CLI reads KB entries and writes them to a context file, then returns
    spawn instructions. The actual YAML generation is done by the
    kanban-benchmark-generator agent (LLM-driven), which the orchestrator
    (e.g. Claude Code) spawns based on the returned instruction.

    When invoked through Claude Code (natural language: "generate benchmark
    from KB"), the orchestrator automatically spawns the agent and the user
    gets the final YAML. When invoked from a plain terminal, the user must
    manually run the agent or use the returned context_file.
    """
    if not args or args[0] in ("--help", "-h"):
        return {
            "help": True,
            "message": (
                "Usage: kanban benchmark generate --from-kb [options]\n"
                "\n"
                "Reads KB entries and prepares context for the\n"
                "kanban-benchmark-generator agent. The agent (LLM-driven)\n"
                "produces the actual suite YAML — invoke via Claude Code for\n"
                "end-to-end generation, or use context_file manually.\n"
                "\n"
                "Options:\n"
                "  --from-kb              Required flag (source from knowledge base)\n"
                "  --kb-id K001,K002      Specific KB entry IDs (comma-separated)\n"
                "  --domain <domain>      Filter by domain (default: all)\n"
                "  --category <cat>       Filter by category (default: all)\n"
                "  --count <N>            Max entries to include (default: 10)\n"
                "  --output <suite.yml>   Output file path (default: benchmark_suite.yml)\n"
                "  --modes m1,m2,m3        Multi-mode (comma-separated, e.g. quick,lightweight,superpowers)"
            ),
        }

    from_kb = False
    domain = None
    category = None
    count = 10
    output_file = "benchmark_suite.yml"
    modes_str = None
    kb_ids_str = None

    i = 0
    while i < len(args):
        if args[i] == "--from-kb":
            from_kb = True
            i += 1
        elif args[i] == "--domain" and i + 1 < len(args):
            domain = args[i + 1]
            i += 2
        elif args[i] == "--category" and i + 1 < len(args):
            category = args[i + 1]
            i += 2
        elif args[i] == "--count" and i + 1 < len(args):
            count = int(args[i + 1])
            i += 2
        elif args[i] == "--output" and i + 1 < len(args):
            output_file = args[i + 1]
            i += 2
        elif args[i] == "--modes" and i + 1 < len(args):
            modes_str = args[i + 1]
            i += 2
        elif args[i] == "--kb-id" and i + 1 < len(args):
            kb_ids_str = args[i + 1]
            i += 2
        elif args[i] == "--json":
            i += 1
        else:
            i += 1

    if not from_kb:
        return {"error": "generate requires --from-kb flag. See: kanban benchmark generate --help"}

    from kanban_framework.infra.filesystem import Filesystem
    from kanban_framework.domain.knowledge import KnowledgeManager
    import json

    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    km = KnowledgeManager(fs, read_only=True)

    # --kb-id: fetch specific entries by ID (overrides domain/category filter)
    if kb_ids_str:
        kb_ids = [kid.strip() for kid in kb_ids_str.split(",") if kid.strip()]
        entries = []
        for kid in kb_ids:
            entry = km.get_entry(kid)
            if entry and entry.get("status") == "active":
                entries.append(entry)
            # silently skip non-existent or inactive entries
    else:
        entries = km.list_entries(
            domain=domain,
            category=category,
            status="active",
            limit=count,
        )

    if not entries:
        return {
            "generate": False,
            "message": "No KB entries found matching the criteria.",
            "hint": "Try: kanban knowledge list to see available entries, or adjust --domain/--category filters.",
        }

    # Build context data for the agent (only fields the agent needs)
    context_entries = [
        {
            "id": e.get("id"),
            "title": e.get("title", ""),
            "content": e.get("content", ""),
            "category": e.get("category", ""),
            "domain": e.get("domain", ""),
            "tags": e.get("tags", []),
            "severity": e.get("severity", "medium"),
        }
        for e in entries
    ]

    context_file = str(fs.kanban_dir / "benchmark_input.json")
    from pathlib import Path as _P
    _P(context_file).write_text(
        json.dumps(context_entries, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    # Parse modes if provided (comma-separated)
    modes = [m.strip() for m in modes_str.split(",")] if modes_str else None

    result = {
        "generate": True,
        "entries_count": len(context_entries),
        "context_file": context_file,
        "output_file": output_file,
        "agent": "kanban-benchmark-generator",
    }

    if modes:
        result["modes"] = modes
        result["instruction"] = (
            f"Read {context_file} and generate benchmark suite YAML. "
            f"Write output to {output_file}. "
            f"Use 'modes:' field (multi-mode) with these modes: {', '.join(modes)}. "
            f"Each KB entry becomes one case with realistic requirement + acceptance criteria. "
            f"After generation, user can run: kanban benchmark run {output_file}"
        )
    else:
        result["mode"] = "lightweight"
        result["instruction"] = (
            f"Read {context_file} and generate benchmark suite YAML. "
            f"Write output to {output_file}. "
            f"Each KB entry becomes one case with realistic requirement + acceptance criteria. "
            f"After generation, user can run: kanban benchmark run {output_file}"
        )

    return result


def _cmd_judge_kb(args: list[str]) -> dict:
    """LLM judge KB compliance — find executed tasks, write judge context.

    For each case with expected_knowledge, find the corresponding task(s)
    by scanning .kanban/tasks/ for matching spec.md header.
    """
    if not args or args[0] in ("--help", "-h"):
        return {
            "help": True,
            "message": (
                "Usage: kanban benchmark judge-kb <suite.yml> [options]\n"
                "  Finds executed tasks for cases with expected_knowledge,\n"
                "  writes judge context file for kanban-kb-judge agent.\n"
                "  Run after task execution, before final benchmark run."
            ),
        }

    suite_path = args[0]

    from pathlib import Path
    import json
    from kanban_framework.domain.benchmark_runner import parse_suite, _find_existing_task
    from kanban_framework.infra.filesystem import Filesystem

    suite = parse_suite(Path(suite_path).resolve())
    root = Filesystem.find_project_root()
    fs = Filesystem(root=root)
    tasks_dir = fs.kanban_dir / "tasks"

    # Resolve effective modes for task lookup
    effective_modes = suite.modes if suite.modes else [suite.mode]

    # Build judge context for cases with expected_knowledge
    judge_items = []
    for case in suite.cases:
        if not case.expected_knowledge:
            continue
        # Find existing tasks for this case across all modes
        case_modes = case.modes if case.modes else effective_modes
        for mode in case_modes:
            existing = _find_existing_task(case.id, mode, tasks_dir)
            if existing:
                judge_items.append({
                    "case_id": case.id,
                    "task_id": existing["task_id"],
                    "mode": mode,
                    "kb_ids": case.expected_knowledge,
                    "task_dir": existing["task_dir"],
                    "iteration": existing["iteration"],
                    "acceptance": case.acceptance,
                })

    if not judge_items:
        return {
            "judge_kb": False,
            "message": (
                "No cases with expected_knowledge found matching executed tasks. "
                "Ensure: 1) suite cases have expected_knowledge field, "
                "2) tasks have been created and executed."
            ),
        }

    context_file = str(fs.kanban_dir / "benchmark_judge_input.json")
    Path(context_file).write_text(
        json.dumps(judge_items, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    return {
        "judge_kb": True,
        "cases_to_judge": len(judge_items),
        "context_file": context_file,
        "agent": "kanban-kb-judge",
        "instruction": (
            f"Read {context_file} ({len(judge_items)} items). "
            f"For each item: read KB entries via 'kanban knowledge get <id>', "
            f"read task code, verify KB constraints in actual code, "
            f"write kb_compliance_report.json to each task's reviews dir. "
            f"After completion, run: kanban benchmark run {suite_path}"
        ),
    }


def _cmd_compare(args: list[str]) -> dict:
    """Compare two benchmark reports — score deltas and verdict changes."""
    if not args or args[0] in ("--help", "-h") or len(args) < 2:
        return {
            "help": True,
            "message": (
                "Usage: kanban benchmark compare <current.json> <previous.json>\n"
                "  Compares score deltas and verdict changes between two runs.\n"
                "  Output: per-case score_delta and verdict transition."
            ),
        }

    current_path = Path(args[0])
    previous_path = Path(args[1])

    if not current_path.exists():
        return {"error": f"Current report not found: {current_path}"}
    if not previous_path.exists():
        return {"error": f"Previous report not found: {previous_path}"}

    import json as _json
    current = _json.loads(current_path.read_text(encoding="utf-8"))
    from kanban_framework.domain.benchmark_runner import compare_reports
    return compare_reports(current, previous_path)
