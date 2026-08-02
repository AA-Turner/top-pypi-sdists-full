#!/usr/bin/env python3
"""Audit open GitLab issues for label compliance, board placement, and template conformance.

Usage:
    pysae-ai-tools glab_issue_audit.audit_issues [--project PROJECT] [--scope ...]

Without --fix: generates an audit report (no changes applied).
With --fix: generates the same report, then applies the fixable corrections.
"""

import json
import sys
import threading
import time
import traceback
import urllib.request
import webbrowser
from collections.abc import Sequence
from dataclasses import asdict
from typing import Annotated, Any

import typer

from ...common.glab.fetch_issues import (
    CommonAllProjects,
    CommonIssueFilters,
    CommonMe,
    CommonProject,
    CommonSearch,
    CommonUser,
    fetch_open_issues,
    issue_age_days,
    resolve_issue_filters,
)
from ...common.glab.models import GitLabIssue
from .apply import apply_plan, save_plan
from .checks import fetch_group_labels, fetch_group_projects
from .diagnostic import CheckTiming, FixTiming, IssueReport, RuleContext
from .fix_plan import build_fix_plan
from .models import (
    AggregatedTiming,
    AuditContext,
    AuditResults,
    DiagnosticPerf,
    IssueResult,
    PlanPerf,
)
from .models import Violation as ViolationModel
from .rules import RULES
from .server import (
    ensure_server,
    post_audit_progress,
    post_audit_results,
    post_plan_issue,
    post_plan_results,
    post_result_issue,
)

# ---------------------------------------------------------------------------
# Report formatting
# ---------------------------------------------------------------------------


def format_report(reports: list[IssueReport], top: int | None) -> str:
    """Format the audit report as structured text."""
    reports.sort(
        key=lambda r: (
            -sum(1 for v in r.violations if v.severity == "error"),
            -len(r.violations),
        )
    )

    if top:
        reports = reports[:top]

    total_issues = len(reports)
    issues_with_errors = sum(1 for r in reports if r.has_errors)
    total_violations = sum(len(r.violations) for r in reports)
    fixable = sum(len(r.fixable_violations) for r in reports)

    by_check: dict[str, dict[str, int]] = {}
    for r in reports:
        for v in r.violations:
            by_check.setdefault(v.check, {"error": 0, "warning": 0})
            by_check[v.check][v.severity] += 1

    lines = [
        "=" * 60,
        "AUDIT REPORT — Issues ouvertes Pysae",
        "=" * 60,
        "",
        f"Issues auditees    : {total_issues}",
        f"Issues en erreur   : {issues_with_errors}",
        f"Violations totales : {total_violations} ({fixable} auto-fixable)",
        "",
    ]

    if by_check:
        lines.append("Par categorie :")
        for check, counts in sorted(by_check.items()):
            lines.append(f"  {check:12s} : {counts['error']} erreur(s), {counts['warning']} warning(s)")
        lines.append("")

    issues_with_violations = [r for r in reports if r.violations]
    if issues_with_violations:
        lines.append("-" * 60)
        lines.append("DETAIL PAR ISSUE")
        lines.append("-" * 60)

        for r in issues_with_violations:
            lines.append("")
            lines.append(f"#{r.iid} -- {r.title}")
            lines.append(f"  {r.web_url}")
            lines.append(f"  Labels: {', '.join(r.labels) if r.labels else '(aucun)'}")
            for v in r.violations:
                icon = "x" if v.severity == "error" else "!"
                fix_tag = " [FIXABLE]" if v.fixable is True else ""
                lines.append(f"  {icon} [{v.check}] {v.message}{fix_tag}")
    else:
        lines.append("Aucune violation detectee.")

    return "\n".join(lines)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

cli = typer.Typer()


@cli.command()
def main(
    project: CommonProject = None,
    all_projects: CommonAllProjects = False,
    me: CommonMe = False,
    user: CommonUser = None,
    search: CommonSearch = None,
    scope: Annotated[
        list[str] | None,
        typer.Option(
            "--scope",
            help="Audit scopes to enable (choices: labels, required_labels, board, weight, "
            "assignee, spec, title, template, default, all)",
        ),
    ] = None,
    fix: Annotated[bool, typer.Option("--fix", help="Apply fixable corrections")] = False,
    top: Annotated[int | None, typer.Option("--top", help="Show only top N issues")] = None,
    console: Annotated[bool, typer.Option("--console", help="Console-only mode (no web server)")] = False,
    console_progress: Annotated[bool, typer.Option("--console-progress", help="Show progress in console")] = False,
    plan: Annotated[str | None, typer.Option("--plan", help="Save fix plan to FILE", metavar="FILE")] = None,
    apply: Annotated[str | None, typer.Option("--apply", help="Apply a fix plan from FILE", metavar="FILE")] = None,
) -> None:
    """Audit open GitLab issues for label compliance and template conformance."""
    if apply:
        apply_plan(apply)
        return

    scope_list = scope or ["default"]

    filters = CommonIssueFilters(
        project=project,
        all_projects=all_projects,
        me=me,
        user=user,
        search=search,
    )
    resolved_project, assignee_username = resolve_issue_filters(filters)

    scopes = set(scope_list)
    scope_all = "all" in scopes
    scope_default = "default" in scopes
    active_scopes = {name: scope_all or scope_default or name in scopes for name in RULES}

    # Start server early
    if not console:
        port, is_new = ensure_server()
        if is_new:
            time.sleep(0.5)
            webbrowser.open(f"http://127.0.0.1:{port}")
        else:
            try:
                resp = urllib.request.urlopen(f"http://127.0.0.1:{port}/api/clients", timeout=2)
                clients = json.loads(resp.read()).get("connected", 0)
                if clients == 0:
                    webbrowser.open(f"http://127.0.0.1:{port}")
            except Exception:
                webbrowser.open(f"http://127.0.0.1:{port}")

    # Progress & abort helpers
    _web_port = port if not console else None
    _aborted = False
    _last_web_progress = 0.0
    _WEB_PROGRESS_INTERVAL = 0.1  # seconds -- throttle SSE progress + issue updates

    _console_progress = console_progress

    def _emit_progress(
        phase: str, current: int, total: int, current_issue: str = "", detail: str = "", force: bool = False
    ) -> None:
        nonlocal _last_web_progress
        if _console_progress:
            pct = int(current / total * 100) if total else 0
            bar = f"[{'#' * (pct // 5)}{'.' * (20 - pct // 5)}] {pct}%"
            parts = [f"\r  {phase}: {bar} {current}/{total}"]
            if current_issue:
                parts.append(current_issue)
            if detail:
                parts.append(f"({detail})")
            print(" ".join(parts) + "    ", end="", file=sys.stderr, flush=True)
        if _web_port:
            now = time.monotonic()
            if force or phase == "aborting" or (now - _last_web_progress) >= _WEB_PROGRESS_INTERVAL:
                _last_web_progress = now
                post_audit_progress(
                    {
                        "phase": phase,
                        "current": current,
                        "total": total,
                        "current_issue": current_issue,
                        "detail": detail,
                    },
                    _web_port,
                )

    def _check_abort() -> bool:
        if not _web_port:
            return False
        try:
            resp = urllib.request.urlopen(f"http://127.0.0.1:{_web_port}/api/abort", timeout=1)
            return bool(json.loads(resp.read()).get("abort", False))
        except Exception:
            return False

    # Reset abort flag from previous runs
    if _web_port:
        try:
            # POST to abort with empty body resets; we use a dedicated reset via re-posting results
            req = urllib.request.Request(f"http://127.0.0.1:{_web_port}/api/abort", method="DELETE")
            urllib.request.urlopen(req, timeout=1)
        except Exception:
            pass

    # --- Phase 1: Preload ---
    _emit_progress("preload", 0, 3, "labels groupe")
    group_labels, label_colors = fetch_group_labels()
    _emit_progress("preload", 1, 3, f"{len(group_labels)} labels")

    _emit_progress("preload", 1, 3, "issues ouvertes")
    issues = fetch_open_issues(
        project=resolved_project,
        assignee_username=assignee_username,
        search=search,
    )
    _emit_progress("preload", 2, 3, f"{len(issues)} issues")

    project_path_cache: dict[int, str] = {}
    if not resolved_project:
        _emit_progress("preload", 2, 3, "projets groupe")
        projects = fetch_group_projects()
        for p in projects:
            project_path_cache[p["id"]] = p.get("path_with_namespace", str(p["id"]))
    _emit_progress("preload", 3, 3, "done", force=True)
    if _console_progress:
        print("", file=sys.stderr)

    rule_ctx = RuleContext(group_labels=group_labels)
    enabled_rules = [(name, rule) for name, rule in RULES.items() if active_scopes.get(name)]

    # --- Post initial metadata so UI shows scope toolbar, project list, etc. ---
    if not console:
        all_projects_list = (
            sorted(project_path_cache.values())
            if project_path_cache
            else ([resolved_project] if resolved_project else [])
        )
        initial_payload = AuditResults(
            total_issues=0,
            issues_with_errors=0,
            total_violations=0,
            fixable=0,
            by_check={},
            active_scopes=active_scopes,
            context=AuditContext(
                project=resolved_project,
                user=assignee_username,
                search=", ".join(search) if search else None,
            ),
            issues=[],
            label_colors=label_colors,
            known_projects=all_projects_list,
        )
        post_audit_results(initial_payload.model_dump(), port)

    # --- Phase 2: Diagnostic (incremental via SSE) ---
    reports: list[IssueReport] = []
    issues_by_key: dict[tuple[int, int], GitLabIssue] = {}
    check_timings: list[CheckTiming] = []

    def _build_issue_result(r: IssueReport, issue_data: GitLabIssue) -> IssueResult:
        return IssueResult(
            iid=r.iid,
            project_id=r.project_id,
            title=r.title,
            web_url=r.web_url,
            project_path=r.project_path,
            labels=r.labels,
            author=issue_data.author.name if issue_data.author else "",
            assignees=[a.name for a in issue_data.assignees] if issue_data.assignees else [],
            age_days=issue_age_days(issue_data),
            violations=[
                ViolationModel(
                    check=v.check, severity=v.severity, message=v.message, fixable=v.fixable or False, method=v.method
                )
                for v in r.violations
            ],
        )

    total_issues = len(issues)
    audit_start = time.monotonic()
    _last_issue_post = 0.0

    def _throttled_post_issue(issue_dict: dict[str, Any]) -> None:
        nonlocal _last_issue_post
        now = time.monotonic()
        elapsed = now - _last_issue_post
        if elapsed < _WEB_PROGRESS_INTERVAL:
            time.sleep(_WEB_PROGRESS_INTERVAL - elapsed)
        post_result_issue(issue_dict, port)
        _last_issue_post = time.monotonic()

    try:
        for idx, issue in enumerate(issues):
            if _check_abort():
                _aborted = True
                _emit_progress("aborting", idx, total_issues, f"Interruption apres {idx} issues")
                if _console_progress:
                    print(f"\n  Interrompu apres {idx}/{total_issues} issues", file=sys.stderr)
                break

            url_path = (
                issue.web_url.split("gitlab.com/")[-1].split("/-/")[0] if "gitlab.com/" in issue.web_url else None
            )
            project_path = project_path_cache.get(
                issue.project_id, url_path or resolved_project or str(issue.project_id)
            )

            report = IssueReport(
                iid=issue.iid,
                project_id=issue.project_id,
                project_path=project_path,
                title=issue.title,
                web_url=issue.web_url,
                labels=issue.labels,
            )
            issue_key = f"{project_path}#{issue.iid}"

            for rule_name, rule in enabled_rules:
                t0 = time.monotonic()
                results = rule.diagnose(issue, rule_ctx)
                elapsed = (time.monotonic() - t0) * 1000
                check_timings.append(CheckTiming(check=rule_name, issue_key=issue_key, duration_ms=round(elapsed, 2)))
                report.violations.extend(results)

                display = rule.display_name
                methods = {v.method for v in results if v.method}
                if methods:
                    display = f"{display} (via {', '.join(sorted(methods))})"
                _emit_progress("diagnostic", idx, total_issues, issue_key, display)

            reports.append(report)
            issues_by_key[(issue.project_id, issue.iid)] = issue

            # Post issue via SSE (throttled)
            if not console:
                _throttled_post_issue(_build_issue_result(report, issue).model_dump())

            _emit_progress("diagnostic", idx + 1, total_issues, issue_key)
    except KeyboardInterrupt:
        _aborted = True
        _emit_progress("aborting", len(reports), total_issues, f"Interruption (CTRL+C) apres {len(reports)} issues")
        if _console_progress:
            print(f"\n  Interrompu (CTRL+C) apres {len(reports)}/{total_issues} issues", file=sys.stderr)

    total_audit_ms = (time.monotonic() - audit_start) * 1000
    if _console_progress:
        print("", file=sys.stderr)

    if _aborted:
        print(f"=== RAPPORT PARTIEL ({len(reports)}/{total_issues} issues) ===")

    # --- Post final diagnostic results with perf ---
    if not console:
        try:

            def _aggregate(
                timings: Sequence[CheckTiming | FixTiming], key: str = "check"
            ) -> dict[str, AggregatedTiming]:
                buckets: dict[str, list[float]] = {}
                for t in timings:
                    buckets.setdefault(getattr(t, key), []).append(t.duration_ms)
                return {
                    k: AggregatedTiming(
                        count=len(v),
                        total_ms=round(sum(v), 2),
                        avg_ms=round(sum(v) / len(v), 2),
                        min_ms=round(min(v), 2),
                        max_ms=round(max(v), 2),
                    )
                    for k, v in buckets.items()
                }

            diag_perf = DiagnosticPerf(
                check_timings=[asdict(t) for t in check_timings],
                checks_agg=_aggregate(check_timings),
                total_audit_ms=round(total_audit_ms, 2),
            )

            by_check: dict[str, dict[str, int]] = {}
            for r in reports:
                for v in r.violations:
                    by_check.setdefault(v.check, {"error": 0, "warning": 0})
                    by_check[v.check][v.severity] += 1

            final_payload = AuditResults(
                total_issues=len(reports),
                issues_with_errors=sum(1 for r in reports if r.has_errors),
                total_violations=sum(len(r.violations) for r in reports),
                fixable=sum(len(r.fixable_violations) for r in reports),
                issues_with_fixable=sum(1 for r in reports if r.fixable_violations),
                by_check=by_check,
                active_scopes=active_scopes,
                context=AuditContext(
                    project=resolved_project,
                    user=assignee_username,
                    search=", ".join(search) if search else None,
                ),
                issues=[_build_issue_result(r, issues_by_key[(r.project_id, r.iid)]) for r in reports],
                label_colors=label_colors,
                known_projects=all_projects_list,
                perf=diag_perf,
            )

            post_audit_results(final_payload.model_dump(), port)
            print(f"\nRapport HTML : http://127.0.0.1:{port}", file=sys.stderr)
        except Exception as e:
            print(f"Erreur lors de l'envoi des resultats diagnostic : {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)

    # --- Phase 3: Fix Plan (incremental via SSE) ---
    def _plan_progress(current: int, total: int, issue_key: str, detail: str = "") -> None:
        if _check_abort():
            raise KeyboardInterrupt
        _emit_progress("fix_plan", current, total, issue_key, detail)

    _plan_post_lock = threading.Lock()
    _last_plan_post = 0.0

    def _on_issue_plan(issue_plan: dict[str, Any]) -> None:
        """Post plan + updated issue (with enriched violations) via SSE, throttled."""
        nonlocal _last_plan_post
        if console or not issue_plan.get("actions"):
            return
        # Throttle posts from parallel threads
        with _plan_post_lock:
            now = time.monotonic()
            elapsed = now - _last_plan_post
            if elapsed < _WEB_PROGRESS_INTERVAL:
                time.sleep(_WEB_PROGRESS_INTERVAL - elapsed)
            post_plan_issue(issue_plan, port)
            # Also upsert the issue with updated fixable flags
            iid = issue_plan["iid"]
            project_id = issue_plan["project_id"]
            for r in reports:
                if r.iid == iid and r.project_id == project_id:
                    issue_data = issues_by_key.get((r.project_id, r.iid))
                    if issue_data:
                        post_result_issue(_build_issue_result(r, issue_data).model_dump(), port)
                    break
            _last_plan_post = time.monotonic()

    try:
        plan_result, fix_timings, total_plan_ms = build_fix_plan(
            reports,
            issues_by_key,
            rule_ctx,
            on_progress=_plan_progress,
            on_issue_plan=_on_issue_plan,
        )
    except KeyboardInterrupt:
        plan_result, fix_timings, total_plan_ms = {"issues": []}, [], 0.0

    # Detect abort that was caught internally by build_fix_plan
    if not _aborted and _check_abort():
        _aborted = True

    if _aborted:
        _emit_progress("aborting", 0, 0, "Preparation des resultats partiels")
    if fix_timings and _console_progress:
        print("", file=sys.stderr)

    # Print report (after fix plan so fixable counts are correct)
    print(format_report(reports, top))

    if plan:
        save_plan(plan_result, plan)

    # Post final plan with perf
    if not console:
        try:
            plan_perf = PlanPerf(
                fix_timings=[asdict(t) for t in fix_timings],
                fixes_agg=_aggregate(fix_timings, key="fix_type") if fix_timings else {},
                total_plan_ms=round(total_plan_ms, 2),
            )
            plan_payload = {"plan": plan_result, "perf": plan_perf.model_dump()}
            post_plan_results(plan_payload, port)
        except Exception as e:
            print(f"Erreur lors de l'envoi du plan : {e}", file=sys.stderr)
            traceback.print_exc(file=sys.stderr)


if __name__ == "__main__":
    cli()
