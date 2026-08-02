"""CLI entry point: pysae-ai-tools ci test-report [PIPELINE_ID].

Fetch the pipeline-level JUnit test report (GitLab aggregates every
`artifacts:reports:junit` of the pipeline) and surface the failing test
cases — name, class, message and stack trace — as a readable report or
structured JSON. This is the preferred entry point for diagnosing test
failures: it is more reliable than scraping raw job logs. With --slowest it
becomes a timing view, ranking the slowest tests to guide test-suite speedups.

Examples:
    pysae-ai-tools ci test-report
    pysae-ai-tools ci test-report 123456 --json
    pysae-ai-tools ci test-report --all
    pysae-ai-tools ci test-report --slowest 20
    pysae-ai-tools ci test-report https://gitlab.com/grp/proj/-/pipelines/123456
"""

import json
import sys
from dataclasses import asdict, dataclass, field
from typing import Annotated, Any

import typer

from .common.glab import glab_api, resolve_target

app = typer.Typer(help="Pipeline JUnit test report")

_FAILED_STATUSES = {"failed", "error"}


@dataclass
class TestCase:
    """A single test case from a JUnit report."""

    suite: str
    classname: str
    name: str
    status: str
    execution_time: float = 0.0
    message: str = ""

    @property
    def selector(self) -> str:
        """Best-effort `classname › name` selector for local reproduction."""
        return f"{self.classname} › {self.name}" if self.classname else self.name


@dataclass
class TestReport:
    """Parsed pipeline test report."""

    total_count: int = 0
    success_count: int = 0
    failed_count: int = 0
    error_count: int = 0
    skipped_count: int = 0
    total_time: float = 0.0
    cases: list[TestCase] = field(default_factory=list)

    @property
    def has_report(self) -> bool:
        return self.total_count > 0 or bool(self.cases)

    @property
    def failed_cases(self) -> list[TestCase]:
        return [c for c in self.cases if c.status in _FAILED_STATUSES]

    def slowest(self, n: int) -> list[TestCase]:
        """The n slowest test cases (any status), by execution time desc."""
        ranked = sorted(self.cases, key=lambda c: c.execution_time, reverse=True)
        return ranked[:n] if n > 0 else ranked


def parse_test_report(data: dict[str, Any]) -> TestReport:
    """Parse the GitLab `test_report` JSON into a TestReport.

    Pure function (no I/O) so it can be unit-tested against fixtures.
    """
    report = TestReport(
        total_count=int(data.get("total_count", 0)),
        success_count=int(data.get("success_count", 0)),
        failed_count=int(data.get("failed_count", 0)),
        error_count=int(data.get("error_count", 0)),
        skipped_count=int(data.get("skipped_count", 0)),
        total_time=float(data.get("total_time", 0) or 0),
    )
    for suite in data.get("test_suites", []) or []:
        suite_name = str(suite.get("name", "") or "")
        for case in suite.get("test_cases", []) or []:
            report.cases.append(
                TestCase(
                    suite=suite_name,
                    classname=str(case.get("classname", "") or ""),
                    name=str(case.get("name", "") or ""),
                    status=str(case.get("status", "") or ""),
                    execution_time=float(case.get("execution_time", 0) or 0),
                    # system_output usually holds the assertion; stack_trace is a fallback
                    message=str(case.get("system_output") or case.get("stack_trace") or "").strip(),
                )
            )
    return report


def _render_human(report: TestReport, *, show_all: bool, slowest: int) -> str:
    lines: list[str] = []
    lines.append(
        f"Tests: {report.total_count} total · "
        f"{report.success_count} passed · "
        f"{report.failed_count} failed · "
        f"{report.error_count} errors · "
        f"{report.skipped_count} skipped "
        f"({report.total_time:.1f}s)"
    )

    if slowest:
        lines.append("")
        lines.append(f"Slowest {min(slowest, len(report.cases))} tests:")
        for case in report.slowest(slowest):
            lines.append(f"  {case.execution_time:7.2f}s  [{case.suite}] {case.selector}")
        return "\n".join(lines)

    cases = report.cases if show_all else report.failed_cases
    if not cases:
        lines.append("" if show_all else "No failed test cases.")
        return "\n".join(lines)
    for case in cases:
        marker = "✗" if case.status in _FAILED_STATUSES else "·"
        lines.append("")
        lines.append(f"{marker} [{case.suite}] {case.selector}  ({case.status}, {case.execution_time:.2f}s)")
        if case.message:
            for msg_line in case.message.splitlines():
                lines.append(f"    {msg_line}")
    return "\n".join(lines)


@app.command()
def main(
    pipeline: Annotated[
        str,
        typer.Argument(help="Pipeline id or URL (defaults to detected context)"),
    ] = "",
    project_id: Annotated[str, typer.Option("--project-id", help="GitLab project id")] = "",
    pipeline_id: Annotated[str, typer.Option("--pipeline-id", help="Pipeline id (overrides positional)")] = "",
    show_all: Annotated[bool, typer.Option("--all", help="Show all test cases, not just failures")] = False,
    slowest: Annotated[
        int,
        typer.Option("--slowest", help="Show the N slowest tests by duration (timing view)", min=0),
    ] = 0,
    as_json: Annotated[bool, typer.Option("--json", help="Emit structured JSON instead of human output")] = False,
) -> None:
    """Fetch and display the pipeline JUnit test report."""
    refs = [pipeline] if pipeline else []
    target = resolve_target(project_id=project_id, pipeline_id=pipeline_id or pipeline, refs=refs)

    if not target.project_id or not target.pipeline_id:
        print(
            "Could not resolve project_id / pipeline_id. Pass a pipeline URL or --project-id/--pipeline-id.",
            file=sys.stderr,
        )
        raise typer.Exit(1)

    data = glab_api(f"projects/{target.project_id}/pipelines/{target.pipeline_id}/test_report")
    if data is None:
        print("No test report available for this pipeline (no JUnit artifact published).", file=sys.stderr)
        raise typer.Exit(1)

    report = parse_test_report(data)
    if not report.has_report:
        print("No test report available for this pipeline (no JUnit artifact published).", file=sys.stderr)
        raise typer.Exit(1)

    if as_json:
        if slowest:
            cases = report.slowest(slowest)
        elif show_all:
            cases = report.cases
        else:
            cases = report.failed_cases
        payload = {
            "pipeline_id": target.pipeline_id,
            "total_count": report.total_count,
            "success_count": report.success_count,
            "failed_count": report.failed_count,
            "error_count": report.error_count,
            "skipped_count": report.skipped_count,
            "total_time": report.total_time,
            "cases": [asdict(c) for c in cases],
        }
        print(json.dumps(payload, ensure_ascii=False, indent=2))
    else:
        print(_render_human(report, show_all=show_all, slowest=slowest))

    # Non-zero exit when there are failures, so CI callers can branch on it.
    if report.failed_count or report.error_count:
        raise typer.Exit(2)


if __name__ == "__main__":
    app()
