"""Benchmark CLI — `kanban benchmark run <suite.yml>` orchestrator."""
from __future__ import annotations


def dispatch(args: list[str]) -> dict:
    """Route benchmark subcommands."""
    sub = args[0] if args else ""

    if sub in ("--help", "-h", "help", ""):
        return {
            "help": True,
            "message": "Usage: kanban benchmark run <suite.yml> [--model X] [--output report.json] [--compare FILE]",
            "commands": {
                "run": "Execute all cases in a benchmark suite YAML file",
            },
        }

    if sub == "run":
        return _cmd_run(args[1:])

    return {"error": f"unknown subcommand: {sub}. Try: kanban benchmark --help"}


def _cmd_run(args: list[str]) -> dict:
    """Run benchmark suite."""
    if not args or args[0] in ("--help", "-h"):
        return {
            "help": True,
            "message": "Usage: kanban benchmark run <suite.yml> [--output report.json] [--compare FILE]"
        }

    suite_path = args[0]
    output_path = None
    compare_path = None

    i = 1
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output_path = args[i + 1]
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

    if compare_path:
        from kanban_framework.domain.benchmark_runner import compare_reports
        prev = compare_reports(result, Path(compare_path).resolve())
        result["comparison"] = prev

    return result
