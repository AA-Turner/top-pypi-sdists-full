"""CLI entry point: option parsing, AWS/Datadog data gathering, then delegation.

The heavy lifting lives in :mod:`plan` (scoring) and :mod:`render` (report);
``main`` only wires the fetches to those pure functions and emits Markdown/JSON.
"""

import json
from collections.abc import Callable
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Annotated, TypeVar

import typer

from ..awscli import CACHE_TTL_SECONDS, call_log, clear_all_caches
from ..eks import NodeGroup, discover_nodegroups
from ..eks_cpu import CpuUtil, nodegroup_cpu_util
from ..instance_specs import fetch_instance_specs
from ..ondemand_prices import fetch_ondemand_prices
from ..spot_advisor import load_dataset, resolve_region
from ..spot_evictions import parse_run_instances, run_aws_lookup
from ..spot_prices import fetch_spot_prices
from ..timerange import parse_date, resolve_window
from .model import EnvEvictions
from .plan import (
    _fetch_placement,
    _ng_prefix,
    _shape_of,
    apply_scores,
    build_plans,
    compatible_types,
    evictions_by_env,
    evictions_by_type,
    evictions_per_nodegroup,
    launches_by_type,
)
from .render import _plan_json, render_markdown

T = TypeVar("T")


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _iso(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def main(
    region: Annotated[
        str, typer.Option("--region", "-r", help="AWS region code or alias (default eu-west-3).")
    ] = "eu-west-3",
    period: Annotated[
        str, typer.Option("--period", "-p", help="Look-back window for evictions/spot prices: 7d, 1m, 2w…")
    ] = "2w",
    since: Annotated[str, typer.Option("--from", help="Absolute window start (YYYY-MM-DD); overrides --period.")] = "",
    until: Annotated[str, typer.Option("--to", help="Absolute window end (defaults to now). Requires --from.")] = "",
    goal: Annotated[
        str, typer.Option("--goal", help="Score weighting: 'balanced' (default), 'cost', or 'evictions'.")
    ] = "balanced",
    os_name: Annotated[str, typer.Option("--os", help="Operating system: Linux or Windows.")] = "Linux",
    arch: Annotated[str, typer.Option("--arch", help="CPU architecture: x86_64 (default) or arm64.")] = "x86_64",
    new_cpu: Annotated[
        int, typer.Option("--cpu", help="Greenfield mode: design a NEW node group of this vCPU count.")
    ] = 0,
    new_ram: Annotated[int, typer.Option("--ram", help="Greenfield mode: RAM in GiB to pair with --cpu.")] = 0,
    new_capacity: Annotated[
        str, typer.Option("--capacity", help="Greenfield capacity type: spot (default) or on-demand.")
    ] = "spot",
    new_desired: Annotated[int, typer.Option("--desired", help="Greenfield desired node count.")] = 1,
    family: Annotated[
        list[str] | None,
        typer.Option("--family", help="Preferred family prefixes for the recommended mix (repeatable)."),
    ] = None,
    all_families: Annotated[
        bool, typer.Option("--all-families", help="Allow burstable/accelerated families in the recommended mix.")
    ] = False,
    no_placement: Annotated[
        bool, typer.Option("--no-placement", help="Skip Spot Placement Score lookups (saves AWS calls).")
    ] = False,
    no_cpu: Annotated[
        bool, typer.Option("--no-cpu", help="Skip the Datadog per-node CPU lookup (no t*/flex head-room analysis).")
    ] = False,
    exclude_throttled: Annotated[
        list[str] | None,
        typer.Option(
            "--exclude-throttled",
            help="Node group prefix where burstable/flex must never be recommended (repeatable), e.g. prod-api.",
        ),
    ] = None,
    force_throttled: Annotated[
        list[str] | None,
        typer.Option(
            "--force-throttled",
            help="Node group prefix where burstable/flex are forced recommendable at full perf (repeatable).",
        ),
    ] = None,
    refresh_cache: Annotated[
        bool,
        typer.Option(
            "--refresh-cache",
            help="Bypass the local caches (placement scores, on-demand prices, instance specs) and force fresh "
            "lookups; spends the placement quota. The store is still refreshed for later runs.",
        ),
    ] = False,
    clear_cache: Annotated[
        bool,
        typer.Option("--clear-cache", help="Delete all local cache files and exit (does not run an analysis)."),
    ] = False,
    run_buffer_days: Annotated[
        int, typer.Option("--run-buffer-days", help="Extra days before the window for RunInstances.")
    ] = 3,
    max_items: Annotated[int, typer.Option("--max-items", help="Max events per CloudTrail stream.")] = 20000,
    profile: Annotated[str, typer.Option("--profile", help="AWS profile.")] = "",
    output: Annotated[
        str, typer.Option("--output", "-o", help="Write the Markdown report to this file instead of stdout.")
    ] = "",
    as_json: Annotated[bool, typer.Option("--json", help="Emit the structured plan as JSON.")] = False,
) -> None:
    """Score EKS node group instance types (reliability + cost + performance) and propose the best mix."""
    if clear_cache:
        removed = clear_all_caches()
        if removed:
            for path in sorted(removed):
                typer.secho(f"✓ removed {path}", fg=typer.colors.GREEN, err=True)
        else:
            typer.secho("No local cache files to remove.", fg=typer.colors.YELLOW, err=True)
        raise typer.Exit(code=0)
    if goal not in ("balanced", "cost", "evictions"):
        typer.secho(f"✗ --goal must be balanced, cost, or evictions (got {goal!r}).", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    if os_name not in ("Linux", "Windows") or arch not in ("x86_64", "arm64"):
        typer.secho("✗ --os must be Linux/Windows and --arch x86_64/arm64.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)
    greenfield = bool(new_cpu and new_ram)
    if new_capacity not in ("spot", "on-demand"):
        typer.secho(f"✗ --capacity must be spot or on-demand (got {new_capacity!r}).", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    resolved = resolve_region(region)
    call_log().reset()  # fresh AWS call accounting for this run
    now = _now()
    shape_override: tuple[int, int] | None = (new_cpu, new_ram) if greenfield else None
    ng_type_evictions: dict[tuple[str, str, str], int] = {}
    ng_type_launches: dict[tuple[str, str, str], int] = {}
    ng_evictions: dict[tuple[str, str], int] = {}
    env_evictions: dict[str, EnvEvictions] = {}

    try:
        start_iso, end_iso = resolve_window(period, since, until, now=now)
    except ValueError as exc:
        typer.secho(f"✗ {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    if greenfield:
        cap = "SPOT" if new_capacity == "spot" else "ON_DEMAND"
        nodegroups = [
            NodeGroup(cluster="(new)", name="new-node-group", capacity_type=cap, instance_types=[], desired=new_desired)
        ]
    else:
        run_start = _iso(parse_date(start_iso) - timedelta(days=max(run_buffer_days, 0)))
        try:
            if not as_json:
                typer.secho(f"Discovering EKS node groups + CloudTrail history ({resolved})…", err=True)
            nodegroups = discover_nodegroups(resolved, profile=profile)
            evictions = run_aws_lookup(
                resolved, "BidEvictedEvent", start_iso, end_iso=end_iso, max_items=max_items, profile=profile
            )
            run_events = run_aws_lookup(
                resolved, "RunInstances", run_start, end_iso=end_iso, max_items=max_items, profile=profile
            )
        except RuntimeError as exc:
            typer.secho(f"✗ {exc}", fg=typer.colors.RED, err=True)
            raise typer.Exit(code=1) from exc
        instances = parse_run_instances(run_events)
        ng_evictions = evictions_per_nodegroup(evictions, instances)
        ng_type_evictions = evictions_by_type(evictions, instances)
        # Attribution uses the full (buffer-extended) instance map, but the rate
        # denominator counts only launches inside the eviction window so a bursty
        # pool is not diluted by the buffer's extra launches.
        ng_type_launches = launches_by_type(instances, window=(start_iso, end_iso))
        in_scope = {(ng.cluster, _ng_prefix(ng.name)) for ng in nodegroups}
        env_evictions = evictions_by_env(evictions, instances, in_scope)

    # Sustained per-node CPU utilisation (Datadog) — drives the t*/flex head-room call.
    cpu_util: dict[str, CpuUtil] = {}
    if not greenfield and not no_cpu:
        try:
            cpu_util = nodegroup_cpu_util([ng.name for ng in nodegroups], start_iso, end_iso)
        except Exception as exc:  # best-effort: never fail the run on a Datadog hiccup
            typer.secho(f"⚠ Datadog CPU lookup unavailable ({exc}).", fg=typer.colors.YELLOW, err=True)

    dataset = load_dataset()

    # Price/spec the union of current + all compatible types (one fetch each).
    spot_types: set[str] = set()
    ondemand_types: set[str] = set()
    for ng in nodegroups:
        bucket = spot_types if ng.is_spot else ondemand_types
        bucket.update(ng.instance_types)
        shape = (_shape_of(dataset, ng.instance_types[0]) if ng.instance_types else None) or shape_override
        if shape:
            bucket.update(compatible_types(dataset, resolved, shape, os_name, arch))
    all_types = spot_types | ondemand_types

    def _safe(fetch: Callable[[], dict[str, T]], label: str) -> dict[str, T]:
        try:
            return fetch()
        except RuntimeError as exc:
            typer.secho(f"⚠ {label} unavailable ({exc}).", fg=typer.colors.YELLOW, err=True)
            return {}

    use_cache = not refresh_cache
    specs = (
        _safe(
            lambda: fetch_instance_specs(resolved, sorted(all_types), profile=profile, use_cache=use_cache),
            "instance specs",
        )
        if all_types
        else {}
    )
    spot_prices = (
        _safe(
            lambda: fetch_spot_prices(resolved, sorted(spot_types), start_iso, end_iso, profile=profile), "spot prices"
        )
        if spot_types
        else {}
    )
    ondemand_prices = (
        _safe(
            lambda: fetch_ondemand_prices(
                resolved, sorted(ondemand_types), os_name=os_name, profile=profile, use_cache=use_cache
            ),
            "on-demand prices",
        )
        if ondemand_types
        else {}
    )

    plans = build_plans(
        dataset,
        resolved,
        os_name,
        nodegroups,
        ng_evictions,
        specs,
        spot_prices,
        ondemand_prices,
        family=family,
        all_families=all_families,
        arch=arch,
        shape_override=shape_override,
        ng_type_evictions=ng_type_evictions,
        ng_type_launches=ng_type_launches,
        cpu_util=cpu_util,
        exclude_throttled=exclude_throttled,
        force_throttled=force_throttled,
    )
    apply_scores(plans, goal)
    # Placement is scored per mix (current vs recommended), so it must run after
    # scoring has determined each node group's recommended mix.
    if not no_placement:
        try:
            _fetch_placement(plans, resolved, profile, use_cache=use_cache)
        except RuntimeError as exc:
            typer.secho(f"⚠ placement scores unavailable ({exc}).", fg=typer.colors.YELLOW, err=True)

    if as_json:
        typer.echo(
            json.dumps(
                {
                    "region": resolved,
                    "window": {"from": start_iso, "to": end_iso},
                    "goal": goal,
                    "env_evictions": {
                        env: {
                            "total": s.total,
                            "in_scope": s.in_scope,
                            "out_of_scope": s.out_of_scope,
                            "orphans": s.orphans,
                        }
                        for env, s in env_evictions.items()
                    },
                    "node_groups": [_plan_json(p) for p in plans],
                    "api_calls": {
                        "played": call_log().played,
                        "ok": call_log().ok,
                        "failed": call_log().failed,
                        "quota_failed": call_log().quota_failed,
                        "cache_reads": call_log().cache_reads,
                        "cache_writes": call_log().cache_writes,
                        "by_operation": {
                            op: {
                                "played": s.played,
                                "ok": s.ok,
                                "failed": s.failed,
                                "quota_failed": s.quota_failed,
                                "cache_reads": s.cache_reads,
                                "cache_writes": s.cache_writes,
                                "cache_ttl_seconds": CACHE_TTL_SECONDS.get(op),
                            }
                            for op, s in sorted(call_log().ops.items())
                        },
                    },
                },
                indent=2,
                ensure_ascii=False,
            )
        )
        return
    if not plans:
        typer.secho(f"No EKS node groups found in {resolved}.", fg=typer.colors.YELLOW)
        return
    report = render_markdown(plans, resolved, start_iso, end_iso, goal, env_evictions, call_log())
    if output:
        path = Path(output)
        path.write_text(report, encoding="utf-8")
        typer.secho(f"✓ Markdown report written: {path}", fg=typer.colors.GREEN, err=True)
    else:
        typer.echo(report)
