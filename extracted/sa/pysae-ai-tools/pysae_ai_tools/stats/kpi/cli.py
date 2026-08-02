"""Collect the tech KPIs of the « Suivi des indicateurs Opérations » sheet over a window.

Best-effort: each metric is collected independently; a failing source yields
an ``error`` field in the JSON output instead of aborting the run.

Usage:
    pysae-ai-tools stats kpi --since 2026-05-29 [--until 2026-06-05] [--ai-seats-monthly-usd 0]
"""

import datetime as dt
import json
import sys
from collections.abc import Callable
from typing import Annotated, Any

import typer

from ...common.group import resolve_group_id
from . import airtable, anthropic_cost, datadog, gitlab
from .models import KpiSnapshot, Metric

app = typer.Typer(no_args_is_help=True, add_completion=False, help=__doc__)

DAYS_PER_MONTH = 30.4375


def _collect(
    snapshot: KpiSnapshot,
    key: str,
    unit: str,
    fn: Callable[[], tuple[float | int | None, dict[str, Any]]],
) -> None:
    try:
        value, detail = fn()
        snapshot.add(Metric(key=key, value=value, unit=unit, detail=detail))
    except Exception as exc:  # noqa: BLE001 — best-effort by design
        print(f"  ⚠ {key}: {exc}", file=sys.stderr)
        snapshot.add(Metric(key=key, value=None, unit=unit, error=str(exc)))


def _collect_datadog(snapshot: KpiSnapshot, since: dt.date, until: dt.date) -> None:
    from_ts, to_ts = _ts(since), _ts(until)
    quarter_from_ts = _ts(datadog.quarter_start(until))
    try:
        dd = datadog.client()
    except Exception as exc:  # noqa: BLE001
        for key, unit in (
            ("uptime_pct", "%"),
            ("uptime_quarter_pct", "%"),
            ("latency_p95_ms", "ms"),
            ("error_ratio_4xx_pct", "%"),
            ("error_ratio_5xx_pct", "%"),
            ("error_budget_burn_pct", "%"),
        ):
            snapshot.add(Metric(key=key, value=None, unit=unit, error=str(exc)))
        return

    with dd:
        _collect(snapshot, "uptime_pct", "%", lambda: (datadog.slo_sli_pct(dd, from_ts, to_ts), {}))
        _collect(snapshot, "uptime_quarter_pct", "%", lambda: (datadog.slo_sli_pct(dd, quarter_from_ts, to_ts), {}))
        _collect(snapshot, "latency_p95_ms", "ms", lambda: (datadog.latency_p95_ms(dd, from_ts, to_ts), {}))

        def ratios() -> tuple[tuple[float, float], dict[str, Any]]:
            return datadog.error_ratios_pct(dd, from_ts, to_ts), {}

        try:
            (ratio_4xx, ratio_5xx), _ = ratios()
            snapshot.add(Metric(key="error_ratio_4xx_pct", value=ratio_4xx, unit="%"))
            snapshot.add(Metric(key="error_ratio_5xx_pct", value=ratio_5xx, unit="%"))
        except Exception as exc:  # noqa: BLE001
            print(f"  ⚠ error_ratios: {exc}", file=sys.stderr)
            snapshot.add(Metric(key="error_ratio_4xx_pct", value=None, unit="%", error=str(exc)))
            snapshot.add(Metric(key="error_ratio_5xx_pct", value=None, unit="%", error=str(exc)))

        def burn() -> tuple[float, dict[str, Any]]:
            sli = datadog.slo_sli_pct(dd, quarter_from_ts, to_ts)
            return datadog.budget_burn_pct(sli), {"quarter_sli_pct": sli, "target_pct": datadog.SLO_TARGET_PCT}

        _collect(snapshot, "error_budget_burn_pct", "%", burn)


def _collect_gitlab(snapshot: KpiSnapshot, group_id: int, since_iso: str, until_iso: str) -> None:
    try:
        issues = gitlab.closed_issues(group_id, since_iso, until_iso)
        vel = gitlab.velocity(issues)
        snapshot.add(Metric(key="issues_closed", value=vel["issues_closed"], unit="issues"))
        snapshot.add(
            Metric(
                key="weight_delivered",
                value=vel["weight_delivered"],
                unit="points",
                detail={"unweighted_issues": vel["unweighted_issues"]},
            )
        )
        snapshot.add(Metric(key="lead_time_days", value=vel["lead_time_days"], unit="days"))
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ velocity: {exc}", file=sys.stderr)
        for key, unit in (("issues_closed", "issues"), ("weight_delivered", "points"), ("lead_time_days", "days")):
            snapshot.add(Metric(key=key, value=None, unit=unit, error=str(exc)))

    try:
        mrs = gitlab.merged_mrs(group_id, since_iso, until_iso)
        team = gitlab.mr_metrics(mrs)
        snapshot.add(Metric(key="cycle_time_days", value=team["cycle_time_days"], unit="days"))
        snapshot.add(
            Metric(
                key="change_failure_rate_pct",
                value=team["change_failure_rate_pct"],
                unit="%",
                detail={"mrs_merged": team["mrs_merged"], "revert_mrs": team["revert_mrs"]},
            )
        )
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ mr_metrics: {exc}", file=sys.stderr)
        for key, unit in (("cycle_time_days", "days"), ("change_failure_rate_pct", "%")):
            snapshot.add(Metric(key=key, value=None, unit=unit, error=str(exc)))

    _collect(
        snapshot,
        "deploy_frequency",
        "deploys",
        lambda: (gitlab.prod_deploy_count(group_id, since_iso, until_iso), {}),
    )


def _collect_ai_cost(snapshot: KpiSnapshot, since: dt.date, until: dt.date, seats_monthly_usd: float) -> None:
    def cost_per_point() -> tuple[float | None, dict[str, Any]]:
        api_cost = anthropic_cost.api_cost_usd(since.isoformat(), until.isoformat())
        seats_cost = round(seats_monthly_usd * (until - since).days / DAYS_PER_MONTH, 2)
        weight = snapshot.metrics.get("weight_delivered")
        detail = {"api_cost_usd": api_cost, "seats_cost_usd": seats_cost}
        if weight is None or weight.value is None or not weight.value:
            raise RuntimeError(f"weight_delivered unavailable or zero (cost collected: {detail})")
        return round((api_cost + seats_cost) / float(weight.value), 2), detail

    _collect(snapshot, "ai_cost_per_point", "USD/point", cost_per_point)


def _ts(day: dt.date) -> int:
    return int(dt.datetime(day.year, day.month, day.day, tzinfo=dt.UTC).timestamp())


@app.command()
def kpi(
    since: Annotated[str, typer.Option(help="Window start, YYYY-MM-DD (inclusive).")],
    until: Annotated[str, typer.Option(help="Window end, YYYY-MM-DD (exclusive). Default: today.")] = "",
    group_id: Annotated[
        int | None, typer.Option(help="GitLab group id (default: resolved live from the group path).")
    ] = None,
    ai_seats_monthly_usd: Annotated[
        float, typer.Option(help="Monthly Claude seats cost (USD), prorated over the window.")
    ] = 0.0,
    skip_coverage: Annotated[bool, typer.Option(help="Skip test coverage collection (slow).")] = True,
) -> None:
    """Collect all KPIs over the window and print the snapshot as JSON."""
    if group_id is None:
        group_id = resolve_group_id()
    since_day = dt.date.fromisoformat(since)
    until_day = dt.date.fromisoformat(until) if until else dt.datetime.now(dt.UTC).date()
    if until_day <= since_day:
        raise typer.BadParameter("--until must be after --since")
    since_iso, until_iso = f"{since_day}T00:00:00Z", f"{until_day}T00:00:00Z"

    snapshot = KpiSnapshot(since=since_day.isoformat(), until=until_day.isoformat())

    print(f"Collecting KPIs over [{since_day} → {until_day})...", file=sys.stderr)
    _collect_datadog(snapshot, since_day, until_day)

    def incidents() -> tuple[None, dict[str, Any]]:
        records = airtable.fetch_critical_tickets()
        p1, p2 = airtable.count_p1_p2(records, since_day.isoformat(), until_day.isoformat())
        snapshot.add(Metric(key="incidents_p1", value=p1, unit="incidents"))
        snapshot.add(Metric(key="incidents_p2", value=p2, unit="incidents"))
        return None, {}

    try:
        incidents()
    except Exception as exc:  # noqa: BLE001
        print(f"  ⚠ incidents: {exc}", file=sys.stderr)
        snapshot.add(Metric(key="incidents_p1", value=None, unit="incidents", error=str(exc)))
        snapshot.add(Metric(key="incidents_p2", value=None, unit="incidents", error=str(exc)))

    _collect_gitlab(snapshot, group_id, since_iso, until_iso)
    _collect_ai_cost(snapshot, since_day, until_day, ai_seats_monthly_usd)

    if not skip_coverage:

        def coverage() -> tuple[float, dict[str, Any]]:
            data = gitlab.test_coverage_pct(group_id)
            return data["average_pct"], {"per_repo": data["per_repo"]}

        _collect(snapshot, "test_coverage_pct", "%", coverage)

    print(json.dumps(snapshot.to_dict(), indent=2, ensure_ascii=False))
