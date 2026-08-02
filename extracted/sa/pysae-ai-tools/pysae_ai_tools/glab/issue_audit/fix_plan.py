"""Fix plan — resolve violations and build action plan using rules.

Per-issue pipeline: enrich violations → build actions → callback.
Issues are processed in parallel via ThreadPoolExecutor so that
Claude API calls (title translation, type classification) don't block each other.
"""

import sys
import threading
import time
from collections.abc import Callable
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Any

from ...common.glab.models import GitLabIssue
from .diagnostic import FixTiming, IssueReport, ProgressCallback, RuleContext
from .rules import RULES

IssuePlanCallback = Callable[[dict[str, Any]], None]

MAX_WORKERS = 10


def _process_one_issue(
    r: IssueReport,
    issues_by_key: dict[tuple[int, int], GitLabIssue],
    ctx: RuleContext,
    on_progress: ProgressCallback | None,
    on_issue_plan: IssuePlanCallback | None,
    counter: list[int],
    counter_lock: threading.Lock,
    total: int,
) -> list[FixTiming]:
    """Process a single issue: enrich violations, build actions, call back."""
    issue_key = f"{r.project_path}#{r.iid}"
    issue_data = issues_by_key.get((r.project_id, r.iid), GitLabIssue())
    fix_timings: list[FixTiming] = []

    # Enrich violations
    for v in r.violations:
        rule = RULES.get(v.check)
        if not rule:
            v.fixable = False
            with counter_lock:
                counter[0] += 1
                idx = counter[0]
            if on_progress:
                on_progress(idx, total, issue_key, "")
            continue

        t0 = time.monotonic()
        rule.enrich(v, r, issue_data, ctx)
        elapsed = (time.monotonic() - t0) * 1000

        if v.fix and v.method:
            fix_type = f"{v.check}:{v.fix.type}:{v.method}"
        elif v.fix:
            fix_type = f"{v.check}:{v.fix.type}"
        else:
            fix_type = v.check
        if v.fixable is True:
            fix_timings.append(
                FixTiming(check=v.check, fix_type=fix_type, issue_key=issue_key, duration_ms=round(elapsed, 2))
            )

        with counter_lock:
            counter[0] += 1
            idx = counter[0]
        if on_progress:
            base_fix_type = f"{v.check}:{v.fix.type}" if v.fix else v.check
            display = rule.fix_types.get(fix_type) or rule.fix_types.get(base_fix_type) or rule.display_name
            on_progress(idx, total, issue_key, display)

    # Build actions
    fixable = [v for v in r.violations if v.fixable is True]
    if not fixable:
        return fix_timings

    actions: list[dict[str, Any]] = []
    for v in fixable:
        rule = RULES.get(v.check)
        if rule:
            actions.extend(rule.build_actions(v, r, issue_data, ctx))

    if actions and on_issue_plan:
        on_issue_plan(
            {
                "project_id": r.project_id,
                "project_path": r.project_path,
                "iid": r.iid,
                "title": r.title,
                "web_url": r.web_url,
                "actions": actions,
            }
        )

    return fix_timings


def build_fix_plan(
    reports: list[IssueReport],
    issues_by_key: dict[tuple[int, int], GitLabIssue],
    ctx: RuleContext,
    on_progress: ProgressCallback | None = None,
    on_issue_plan: IssuePlanCallback | None = None,
) -> tuple[dict[str, Any], list[FixTiming], float]:
    """Enrich violations, build actions, and call back per issue.

    Issues are processed in parallel (up to MAX_WORKERS threads).
    Returns (plan_dict, fix_timings, total_plan_ms).
    """
    plan_start = time.monotonic()
    total = sum(len(r.violations) for r in reports)
    counter = [0]  # mutable int for thread-safe counter
    counter_lock = threading.Lock()

    all_fix_timings: list[FixTiming] = []
    issues_plans: list[dict[str, Any]] = []

    # Wrap on_issue_plan to also collect plans
    plan_lock = threading.Lock()

    def _on_issue_plan_wrapper(issue_plan: dict[str, Any]) -> None:
        with plan_lock:
            issues_plans.append(issue_plan)
        if on_issue_plan:
            on_issue_plan(issue_plan)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
        futures = {
            pool.submit(
                _process_one_issue,
                r,
                issues_by_key,
                ctx,
                on_progress,
                _on_issue_plan_wrapper,
                counter,
                counter_lock,
                total,
            ): r
            for r in reports
        }
        for future in as_completed(futures):
            try:
                timings = future.result(timeout=120)
                all_fix_timings.extend(timings)
            except KeyboardInterrupt:
                pool.shutdown(wait=False, cancel_futures=True)
                break
            except Exception as e:
                print(f"fix_plan thread error: {e}", file=sys.stderr)

    total_plan_ms = (time.monotonic() - plan_start) * 1000
    return {"issues": issues_plans}, all_fix_timings, total_plan_ms
