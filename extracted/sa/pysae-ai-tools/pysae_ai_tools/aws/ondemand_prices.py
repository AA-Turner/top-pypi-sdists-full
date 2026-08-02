"""On-demand EC2 prices from the AWS Price List API (``aws pricing get-products``).

The Price List API is only served from a few endpoints (we use ``us-east-1``)
but prices the target region via the ``regionCode`` filter. One query per type
keeps the filter set simple and robust; candidate sets are small.
"""

import json
import time
from pathlib import Path
from tempfile import gettempdir
from typing import Any

from .awscli import CACHE_TTL_SECONDS, OP_ONDEMAND, DiskCache, call_log, run_aws_json

_PRICING_ENDPOINT = "us-east-1"
# On-demand list prices change rarely (occasional AWS price drops) — the TTL (see
# CACHE_TTL_SECONDS) spares one Price List call per type on every run.
_CACHE = DiskCache(Path(gettempdir()) / "pysae-ondemand-prices.json", CACHE_TTL_SECONDS[OP_ONDEMAND])


def _extract_hourly(product: dict[str, Any]) -> float | None:
    """Pull the on-demand USD/hour from one Price List product document."""
    on_demand = (product.get("terms") or {}).get("OnDemand") or {}
    for term in on_demand.values():
        for dim in (term.get("priceDimensions") or {}).values():
            usd = (dim.get("pricePerUnit") or {}).get("USD")
            if usd is not None:
                try:
                    return float(usd)
                except (TypeError, ValueError):
                    return None
    return None


def fetch_ondemand_prices(
    region: str,
    instance_types: list[str],
    *,
    os_name: str = "Linux",
    profile: str = "",
    use_cache: bool = True,
) -> dict[str, float]:
    """Return ``{instance_type: on_demand_usd_per_hour}`` for ``region``.

    Types with no priced product are simply absent. A per-type query failure is
    skipped rather than aborting the whole batch. Prices seen within the cache
    window are served from disk (counted as cache hits, no API call) unless
    ``use_cache`` is False, which forces fresh lookups while still refreshing the
    store.
    """
    out: dict[str, float] = {}
    now = time.time()
    for itype in sorted(set(instance_types)):
        key = f"{region}|{os_name}|{itype}"
        if use_cache:
            hit, value = _CACHE.get(key, now)
            if hit:
                call_log().record_cache_read(OP_ONDEMAND)
                if value is not None:
                    out[itype] = float(value)
                continue
        args = [
            "pricing",
            "get-products",
            "--region",
            _PRICING_ENDPOINT,
            "--service-code",
            "AmazonEC2",
            "--filters",
            f"Type=TERM_MATCH,Field=instanceType,Value={itype}",
            f"Type=TERM_MATCH,Field=regionCode,Value={region}",
            f"Type=TERM_MATCH,Field=operatingSystem,Value={os_name}",
            "Type=TERM_MATCH,Field=tenancy,Value=Shared",
            "Type=TERM_MATCH,Field=preInstalledSw,Value=NA",
            "Type=TERM_MATCH,Field=capacitystatus,Value=Used",
            "--max-results",
            "1",
        ]
        try:
            payload = run_aws_json(args, profile=profile)
        except RuntimeError:
            continue
        price_list = payload.get("PriceList") or []
        product = None
        if price_list:
            try:
                product = json.loads(price_list[0])
            except (json.JSONDecodeError, TypeError):
                product = None
        hourly = _extract_hourly(product) if product is not None else None
        # Cache the result (including a miss) so the next run skips the call.
        _CACHE.set(key, hourly, now)
        call_log().record_cache_write(OP_ONDEMAND)
        if hourly is not None:
            out[itype] = hourly
    _CACHE.save()
    return out
