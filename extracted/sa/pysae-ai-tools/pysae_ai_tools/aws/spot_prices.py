"""Fetch current EC2 spot prices per instance type from ``describe-spot-price-history``.

    pysae-ai-tools aws spot-prices --region eu-west-3 --types r5.xlarge,r6i.xlarge
    pysae-ai-tools aws spot-prices -r eu-west-3 --cpu 4 --ram 32 --json

Returns the **average spot $/hour** per type over the lookback window (averaged
across Availability Zones and price ticks). Used by ``eks-optimize`` to weigh
cost against reliability when proposing replacement instance types.
"""

import json
from collections import defaultdict
from datetime import datetime, timezone
from typing import Annotated

import typer

from .awscli import run_aws_json
from .spot_advisor import advise, load_dataset, resolve_region
from .timerange import resolve_window

LINUX_PRODUCT = "Linux/UNIX"


def fetch_spot_prices(
    region: str,
    instance_types: list[str],
    start_iso: str,
    end_iso: str,
    *,
    product: str = LINUX_PRODUCT,
    profile: str = "",
    max_items: int = 10000,
) -> dict[str, float]:
    """Return ``{instance_type: avg_spot_usd_per_hour}`` over the window.

    Averages every ``SpotPriceHistory`` tick across all AZs for each type.
    Types with no price data are simply absent from the result.
    """
    if not instance_types:
        return {}
    args = [
        "ec2",
        "describe-spot-price-history",
        "--region",
        region,
        "--instance-types",
        *instance_types,
        "--product-descriptions",
        product,
        "--start-time",
        start_iso,
        "--end-time",
        end_iso,
        "--max-items",
        str(max_items),
    ]
    payload = run_aws_json(args, profile=profile)
    sums: dict[str, float] = defaultdict(float)
    counts: dict[str, int] = defaultdict(int)
    for tick in payload.get("SpotPriceHistory", []):
        itype = tick.get("InstanceType")
        price = tick.get("SpotPrice")
        if not itype or price is None:
            continue
        try:
            value = float(price)
        except (TypeError, ValueError):
            continue
        sums[itype] += value
        counts[itype] += 1
    return {t: sums[t] / counts[t] for t in sums if counts[t]}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def main(
    region: Annotated[
        str, typer.Option("--region", "-r", help="AWS region code or alias (default eu-west-3).")
    ] = "eu-west-3",
    types: Annotated[
        str,
        typer.Option("--types", help="Comma-separated instance types (e.g. r5.xlarge,r6i.xlarge)."),
    ] = "",
    cpu: Annotated[
        int, typer.Option("--cpu", help="Resolve all same-shape types of this vCPU count instead of --types.")
    ] = 0,
    ram: Annotated[int, typer.Option("--ram", help="RAM in GiB to pair with --cpu.")] = 0,
    arch: Annotated[
        str, typer.Option("--arch", help="CPU architecture for --cpu/--ram resolution: x86_64 or arm64.")
    ] = "x86_64",
    period: Annotated[str, typer.Option("--period", "-p", help="Averaging window: 7d, 24h, 1m… (default 1d).")] = "1d",
    since: Annotated[str, typer.Option("--from", help="Absolute window start (YYYY-MM-DD); overrides --period.")] = "",
    until: Annotated[str, typer.Option("--to", help="Absolute window end (defaults to now).")] = "",
    profile: Annotated[str, typer.Option("--profile", help="AWS profile.")] = "",
    as_json: Annotated[bool, typer.Option("--json", help="Emit {type: avg_usd_per_hour} as JSON.")] = False,
) -> None:
    """Fetch average spot $/hour per instance type over a window."""
    resolved = resolve_region(region)
    try:
        start_iso, end_iso = resolve_window(period, since, until, now=_now())
    except ValueError as exc:
        typer.secho(f"✗ {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    type_list = [t.strip() for t in types.split(",") if t.strip()]
    if not type_list and cpu and ram:
        dataset = load_dataset()
        type_list = [a.instance_type for a in advise(dataset, resolved, cpu, ram, arch=arch)]
    if not type_list:
        typer.secho("✗ Provide --types or both --cpu and --ram.", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1)

    try:
        prices = fetch_spot_prices(resolved, type_list, start_iso, end_iso, profile=profile)
    except RuntimeError as exc:
        typer.secho(f"✗ {exc}", fg=typer.colors.RED, err=True)
        raise typer.Exit(code=1) from exc

    if as_json:
        typer.echo(json.dumps(prices, indent=2))
        return

    if not prices:
        typer.secho(f"No spot price data for those types in {resolved}.", fg=typer.colors.YELLOW)
        return
    typer.secho(f"\nAverage spot price — {resolved} · {start_iso} → {end_iso}\n", bold=True)
    for itype, price in sorted(prices.items(), key=lambda kv: kv[1]):
        typer.echo(f"  {itype:<20} ${price:.4f}/h")
