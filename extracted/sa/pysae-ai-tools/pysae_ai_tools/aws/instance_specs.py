"""Per-type hardware specs from ``aws ec2 describe-instance-types``."""

import time
from dataclasses import asdict, dataclass
from pathlib import Path
from tempfile import gettempdir

from .awscli import CACHE_TTL_SECONDS, OP_SPECS, DiskCache, call_log, run_aws_json

# describe-instance-types caps at 100 type filters per call.
_CHUNK = 100
# Hardware facts (clock, arch, vendor) are immutable per instance type — the TTL
# (see CACHE_TTL_SECONDS) is long so specs are fetched once and reused for weeks.
_CACHE = DiskCache(Path(gettempdir()) / "pysae-instance-specs.json", CACHE_TTL_SECONDS[OP_SPECS])


@dataclass
class InstanceSpec:
    """The performance-relevant facts AWS publishes for an instance type."""

    arch: str  # "x86_64" | "arm64"
    vendor: str  # Intel | AMD | AWS
    clock_ghz: float | None  # sustained clock, GHz
    network: str  # e.g. "Up to 12.5 Gigabit"


def fetch_instance_specs(
    region: str, instance_types: list[str], *, profile: str = "", use_cache: bool = True
) -> dict[str, InstanceSpec]:
    """Return ``{instance_type: InstanceSpec}`` for the given types (chunked).

    Types seen within the cache window are served from disk (no API call) unless
    ``use_cache`` is False; only the misses are queried from AWS, chunked at 100
    per call. Cache accounting is at the **call** granularity (not per type): a
    chunk fetched and stored is one cache write, and a chunk's worth of types
    fully served from cache is one cache read (an avoided call) — so the call
    log's cache columns stay in the same unit as ``played`` for every operation.
    """
    out: dict[str, InstanceSpec] = {}
    now = time.time()
    types = sorted(set(instance_types))

    misses: list[str] = []
    for t in types:
        if use_cache:
            hit, value = _CACHE.get(f"{region}|{t}", now)
            if hit:
                if value is not None:
                    out[t] = InstanceSpec(**value)
                continue
        misses.append(t)

    # Reads, in call units: the chunk-calls we avoided by serving cached types.
    calls_without_cache = -(-len(types) // _CHUNK)
    calls_with_cache = -(-len(misses) // _CHUNK)
    for _ in range(calls_without_cache - calls_with_cache):
        call_log().record_cache_read(OP_SPECS)

    for start in range(0, len(misses), _CHUNK):
        chunk = misses[start : start + _CHUNK]
        if not chunk:
            continue
        payload = run_aws_json(
            ["ec2", "describe-instance-types", "--region", region, "--instance-types", *chunk],
            profile=profile,
        )
        found: set[str] = set()
        for it in payload.get("InstanceTypes", []):
            name = it.get("InstanceType")
            if not name:
                continue
            proc = it.get("ProcessorInfo") or {}
            archs = proc.get("SupportedArchitectures") or []
            spec = InstanceSpec(
                arch=archs[0] if archs else "?",
                vendor=proc.get("Manufacturer", "") or "",
                clock_ghz=proc.get("SustainedClockSpeedInGhz"),
                network=(it.get("NetworkInfo") or {}).get("NetworkPerformance", "") or "",
            )
            out[name] = spec
            _CACHE.set(f"{region}|{name}", asdict(spec), now)
            found.add(name)
        call_log().record_cache_write(OP_SPECS)  # one write per stored chunk (call unit)
        # Cache types AWS did not return as a miss so the next run skips them too.
        for t in chunk:
            if t not in found:
                _CACHE.set(f"{region}|{t}", None, now)

    _CACHE.save()
    return out
