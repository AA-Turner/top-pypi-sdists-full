"""Count EC2 SPOT interruptions from CloudTrail, broken down by environment.

    pysae-ai-tools aws spot-evictions --region eu-west-3 --period 7d
    pysae-ai-tools aws spot-evictions -r eu-west-3 -p 1m --json

AWS records every spot reclamation as a CloudTrail ``BidEvictedEvent`` whose
``serviceEventDetails.instanceIdSet`` lists the reclaimed instances — but it
carries no cluster/env tag. To attribute each interruption to **dev / prod /
…**, this command cross-references those instance IDs with ``RunInstances``
events, which *do* carry the ``eks:cluster-name`` tag (and the instance type)
set at launch. The cluster name is then mapped to an environment.

Everything is scripted: it shells out to the ``aws`` CLI (using your current
credentials), auto-paginates, parses both event streams, and prints a per-day
breakdown by environment plus per-cluster / per-instance-type rollups. Use
``--json`` for the structured payload.

CloudTrail's ``lookup-events`` reads the 90-day event history (no trail
required), so the period is capped at 90 days.
"""

import json
import subprocess
from collections import Counter
from dataclasses import dataclass, field
from datetime import datetime, timedelta, timezone
from typing import Annotated, Any

import typer

from .awscli import AwsCliError, AwsQuotaError, aws_env, call_log, is_quota_error
from .spot_advisor import resolve_region
from .timerange import parse_date, parse_period, resolve_window  # noqa: F401 (parse_period re-exported)

_AWS_TIMEOUT = 600


@dataclass
class InstanceInfo:
    """Launch metadata for one instance, resolved from a ``RunInstances`` event."""

    cluster: str
    instance_type: str
    nodegroup: str = ""
    launched_at: str = ""  # CloudTrail eventTime (ISO-8601 UTC), "" when unknown


@dataclass
class EvictionReport:
    """Aggregated spot-interruption counts for a region over a period."""

    region: str
    start_iso: str
    per_day_env: dict[str, dict[str, int]] = field(default_factory=dict)
    per_env: dict[str, int] = field(default_factory=dict)
    per_cluster: dict[str, int] = field(default_factory=dict)
    per_type: dict[str, int] = field(default_factory=dict)
    total: int = 0
    unresolved: int = 0

    @property
    def days(self) -> list[str]:
        return sorted(self.per_day_env)

    @property
    def envs(self) -> list[str]:
        """Environment columns, prod/dev first then the rest alphabetically."""
        priority = {"prod": 0, "dev": 1, "staging": 2, "review": 3, "test": 4}
        return sorted(self.per_env, key=lambda e: (priority.get(e, 9), e))

    @property
    def peak_day(self) -> tuple[str, int]:
        if not self.per_day_env:
            return ("", 0)
        return max(((d, sum(c.values())) for d, c in self.per_day_env.items()), key=lambda kv: kv[1])


def cluster_to_env(cluster: str) -> str:
    """Map an EKS cluster name to an environment by keyword, else return it as-is."""
    name = cluster.lower()
    for env in ("prod", "staging", "review", "test", "dev"):
        if env in name:
            return env
    return cluster or "unknown"


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def run_aws_lookup(
    region: str,
    event_name: str,
    start_iso: str,
    *,
    max_items: int,
    end_iso: str = "",
    profile: str = "",
) -> list[dict[str, Any]]:
    """Call ``aws cloudtrail lookup-events`` and return the decoded events.

    Each returned dict is the parsed ``CloudTrailEvent`` JSON (not the thin
    envelope). When ``end_iso`` is given, the lookup is bounded with
    ``--end-time`` (needed for absolute ``--from/--to`` windows). Raises
    ``RuntimeError`` on CLI failure and a clear message when ``aws`` is missing.
    """
    cmd = [
        "aws",
        "cloudtrail",
        "lookup-events",
        "--region",
        region,
        "--lookup-attributes",
        f"AttributeKey=EventName,AttributeValue={event_name}",
        "--start-time",
        start_iso,
        "--max-items",
        str(max_items),
        # CloudTrail caps lookup-events at 50 results/page (API hard limit); set
        # it explicitly so we always fetch the max per call (fewest requests).
        "--page-size",
        "50",
        "--output",
        "json",
    ]
    if end_iso:
        cmd += ["--end-time", end_iso]
    if profile:
        cmd += ["--profile", profile]
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=_AWS_TIMEOUT,
            env=aws_env(),
        )
    except FileNotFoundError as exc:
        call_log().record("cloudtrail lookup-events", ok=False)
        raise AwsCliError("the 'aws' CLI is not installed or not on PATH.") from exc
    except subprocess.TimeoutExpired as exc:
        call_log().record("cloudtrail lookup-events", ok=False)
        raise AwsCliError(f"aws cloudtrail lookup-events timed out after {_AWS_TIMEOUT}s.") from exc
    if result.returncode != 0:
        stderr = (result.stderr or "").strip()
        if is_quota_error(stderr):
            call_log().record("cloudtrail lookup-events", ok=False, quota=True)
            raise AwsQuotaError(f"aws cloudtrail lookup-events hit a quota/throttle limit: {stderr}")
        call_log().record("cloudtrail lookup-events", ok=False)
        raise AwsCliError(f"aws cloudtrail lookup-events failed: {stderr}")
    call_log().record("cloudtrail lookup-events", ok=True)

    payload = json.loads(result.stdout or "{}")
    events: list[dict[str, Any]] = []
    for envelope in payload.get("Events", []):
        raw = envelope.get("CloudTrailEvent")
        if not raw:
            continue
        try:
            events.append(json.loads(raw))
        except json.JSONDecodeError:
            continue
    return events


def parse_run_instances(events: list[dict[str, Any]]) -> dict[str, InstanceInfo]:
    """Map ``instanceId -> InstanceInfo`` from ``RunInstances`` events.

    The event ``eventTime`` is kept on each instance as ``launched_at`` so the
    eviction *rate* can use a launch denominator restricted to the analysis
    window, while the full (buffer-extended) map still resolves the type/cluster
    of instances launched before the window.
    """
    out: dict[str, InstanceInfo] = {}
    for e in events:
        launched_at = e.get("eventTime") or ""
        response = e.get("responseElements") or {}
        items = ((response.get("instancesSet") or {}).get("items")) or []
        for item in items:
            iid = item.get("instanceId")
            if not iid:
                continue
            cluster = ""
            nodegroup = ""
            for tag in (item.get("tagSet") or {}).get("items") or []:
                key = tag.get("key")
                if key == "eks:cluster-name":
                    cluster = tag.get("value", "")
                elif key == "eks:nodegroup-name":
                    nodegroup = tag.get("value", "")
            out[iid] = InstanceInfo(
                cluster=cluster,
                instance_type=item.get("instanceType", "?"),
                nodegroup=nodegroup,
                launched_at=launched_at,
            )
    return out


def build_report(
    region: str,
    start_iso: str,
    eviction_events: list[dict[str, Any]],
    instances: dict[str, InstanceInfo],
) -> EvictionReport:
    """Aggregate ``BidEvictedEvent`` instances by day/env/cluster/type.

    A single eviction event can list several instances, so counts are per
    reclaimed instance. Instances with no matching ``RunInstances`` record are
    bucketed under the ``unknown`` env and counted in ``unresolved``.
    """
    report = EvictionReport(region=region, start_iso=start_iso)
    per_day_env: dict[str, Counter[str]] = {}
    per_env: Counter[str] = Counter()
    per_cluster: Counter[str] = Counter()
    per_type: Counter[str] = Counter()

    for e in eviction_events:
        day = (e.get("eventTime") or "")[:10]
        if not day:
            continue
        details = e.get("serviceEventDetails") or {}
        for iid in details.get("instanceIdSet", []) or []:
            info = instances.get(iid)
            cluster = info.cluster if info and info.cluster else ""
            env = cluster_to_env(cluster) if cluster else "unknown"
            itype = info.instance_type if info else "?"
            report.total += 1
            if env == "unknown":
                report.unresolved += 1
            per_day_env.setdefault(day, Counter())[env] += 1
            per_env[env] += 1
            per_cluster[cluster or "unknown"] += 1
            per_type[itype] += 1

    report.per_day_env = {d: dict(c) for d, c in per_day_env.items()}
    report.per_env = dict(per_env)
    report.per_cluster = dict(per_cluster)
    report.per_type = dict(per_type)
    return report


def _render(report: EvictionReport) -> None:
    """Print the per-day, per-environment breakdown plus rollups."""
    if report.total == 0:
        typer.secho(
            f"No spot interruptions (BidEvictedEvent) found in {report.region} since {report.start_iso}.",
            fg=typer.colors.GREEN,
        )
        return

    envs = report.envs
    typer.secho(
        f"\nSpot interruptions — {report.region} · since {report.start_iso}\n",
        bold=True,
    )
    header = "  " + f"{'day':<12}" + "".join(f"{e:>10}" for e in envs) + f"{'total':>10}"
    typer.secho(header, bold=True)
    typer.echo("  " + "─" * (len(header) - 2))
    peak_day, _ = report.peak_day
    for day in report.days:
        counts = report.per_day_env[day]
        row_total = sum(counts.values())
        row = f"  {day:<12}" + "".join(f"{counts.get(e, 0):>10}" for e in envs) + f"{row_total:>10}"
        typer.secho(row, fg=typer.colors.RED if day == peak_day else None)
    typer.echo("  " + "─" * (len(header) - 2))
    totals = "  " + f"{'TOTAL':<12}" + "".join(f"{report.per_env.get(e, 0):>10}" for e in envs) + f"{report.total:>10}"
    typer.secho(totals, bold=True)

    n_days = len(report.days)
    avg = report.total / n_days if n_days else 0
    pk_day, pk_n = report.peak_day
    typer.echo()
    typer.secho(
        f"  {report.total} interruptions over {n_days} day(s) → ~{avg:.1f}/day · peak {pk_n} on {pk_day}",
        bold=True,
    )
    if report.unresolved:
        pct = 100 * report.unresolved / report.total
        typer.secho(
            f"  ⚠ {report.unresolved} ({pct:.0f}%) could not be attributed to a cluster "
            f"(launched before the RunInstances window — widen --run-buffer-days).",
            fg=typer.colors.YELLOW,
        )

    top_types = sorted(report.per_type.items(), key=lambda kv: -kv[1])[:8]
    if top_types:
        typer.echo("\n  By instance type:")
        for itype, n in top_types:
            typer.echo(f"    {itype:<18} {n:>6}  {'█' * min(n * 40 // max(report.total, 1), 40)}")

    if report.per_cluster:
        typer.echo("\n  By cluster:")
        for cluster, n in sorted(report.per_cluster.items(), key=lambda kv: -kv[1]):
            typer.echo(f"    {cluster:<24} {n:>6}")


def main(
    region: Annotated[
        str,
        typer.Option("--region", "-r", help="AWS region code or alias (default eu-west-3)."),
    ] = "eu-west-3",
    period: Annotated[
        str,
        typer.Option("--period", "-p", help="Look-back window: 7d, 24h, 2w, 1m (month=30d), or a bare day count."),
    ] = "2w",
    since: Annotated[
        str,
        typer.Option("--from", help="Absolute window start (YYYY-MM-DD or ISO); overrides --period."),
    ] = "",
    until: Annotated[
        str,
        typer.Option("--to", help="Absolute window end (defaults to now). Requires --from."),
    ] = "",
    run_buffer_days: Annotated[
        int,
        typer.Option(
            "--run-buffer-days",
            help="Extra days before the window to pull RunInstances (so instances launched earlier still resolve).",
        ),
    ] = 3,
    max_items: Annotated[
        int,
        typer.Option("--max-items", help="Max events fetched per CloudTrail stream (eviction + RunInstances)."),
    ] = 20000,
    profile: Annotated[
        str,
        typer.Option("--profile", help="AWS profile to use (passed to the aws CLI)."),
    ] = "",
    as_json: Annotated[
        bool,
        typer.Option("--json", help="Emit the structured report as JSON instead of the table."),
    ] = False,
) -> None:
    """Count EC2 SPOT interruptions from CloudTrail, broken down by environment."""
    now = _now()
    try:
        evict_start, evict_end = resolve_window(period, since, until, now=now)
    except ValueError as exc:
        typer.secho(f"✗ {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    resolved = resolve_region(region)
    run_start = _iso(parse_date(evict_start) - timedelta(days=max(run_buffer_days, 0)))

    try:
        if not as_json:
            typer.secho(f"Fetching BidEvictedEvent + RunInstances from CloudTrail ({resolved})…", err=True)
        evictions = run_aws_lookup(
            resolved, "BidEvictedEvent", evict_start, end_iso=evict_end, max_items=max_items, profile=profile
        )
        run_events = run_aws_lookup(
            resolved, "RunInstances", run_start, end_iso=evict_end, max_items=max_items, profile=profile
        )
    except RuntimeError as exc:
        typer.secho(f"✗ {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    instances = parse_run_instances(run_events)
    report = build_report(resolved, evict_start, evictions, instances)

    if as_json:
        typer.echo(
            json.dumps(
                {
                    "region": report.region,
                    "since": report.start_iso,
                    "total": report.total,
                    "unresolved": report.unresolved,
                    "per_env": report.per_env,
                    "per_day_env": report.per_day_env,
                    "per_cluster": report.per_cluster,
                    "per_type": report.per_type,
                    "days_covered": len(report.days),
                    "instances_resolved": len(instances),
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return

    _render(report)
