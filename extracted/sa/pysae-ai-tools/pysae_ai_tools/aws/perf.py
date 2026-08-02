"""Coarse per-CPU effective-performance model for EC2 instance types.

There is **no free, normalized benchmark API** per EC2 type (AWS's ECU metric is
deprecated). So we approximate per-core performance as ``clock × IPC``, where:

* ``clock`` (sustained GHz) comes from ``describe-instance-types`` (real, exact);
* ``IPC`` is a curated factor per **CPU microarchitecture**, derived from the
  instance family's generation + vendor (Intel ``i`` / AMD ``a`` / Graviton
  ``g``). These factors are *estimates* anchored on AWS's published
  generational uplift claims (~15 %/gen), relative to Intel Skylake = 1.00.

Effective compute of a type ≈ ``vCPU × clock × IPC``. Combined with price this
gives a **cost per unit of work** that lets a faster-but-pricier type win when
it actually does more work per euro. The factors are deliberately coarse — they
rank generations/vendors sensibly, not benchmark-grade precision.
"""

import re

# IPC factor per microarchitecture, relative to Intel Skylake (1.00).
# Coarse estimates from AWS's published "~15 % per generation" claims; meant for
# ranking, not exact prediction.
IPC: dict[str, float] = {
    # Intel
    "intel-skylake": 1.00,
    "intel-cascade-lake": 1.05,
    "intel-ice-lake": 1.18,
    "intel-sapphire-rapids": 1.32,
    "intel-emerald-rapids": 1.40,
    "intel-granite-rapids": 1.50,
    # AMD EPYC
    # Naples calibrated to a measured ~2.3x per-core deficit vs Milan (m5ad 2.2 GHz
    # vs m6a 3.6 GHz) on a latency-bound async-Python service (prod-ndp, 2026-06):
    # its poor memory / inter-CCX latency punishes such workloads more than a
    # throughput-IPC estimate suggests. Lowered 0.85 -> 0.80 to match.
    "amd-naples": 0.80,
    "amd-rome": 1.00,  # Zen 2; no AWS general-purpose gen maps here (kept for reference)
    "amd-milan": 1.12,
    "amd-genoa": 1.30,
    "amd-turin": 1.48,
    # AWS Graviton (arm64; cross-arch comparison is workload-dependent — rough)
    "graviton2": 0.92,
    "graviton3": 1.08,
    "graviton4": 1.30,
}

# (vendor, generation) -> microarchitecture. Vendor is the family suffix marker:
# 'i'/none = Intel, 'a' = AMD, 'g' = Graviton.
_INTEL_GEN = {
    5: "intel-skylake",
    6: "intel-ice-lake",
    7: "intel-sapphire-rapids",
    8: "intel-emerald-rapids",
    9: "intel-granite-rapids",
}
# AWS's AMD line jumped from Naples (gen 5: m5a/m5ad/c5a/r5a, EPYC 7000 "Naples"/Zen 1)
# straight to Milan (gen 6a) — there is no "Rome" general-purpose AWS generation, so
# gen 5 maps to Naples, NOT Rome (a past bug that over-rated m5a/m5ad at IPC 1.00).
_AMD_GEN = {5: "amd-naples", 6: "amd-milan", 7: "amd-genoa", 8: "amd-turin"}
_GRAVITON_GEN = {6: "graviton2", 7: "graviton3", 8: "graviton4"}

_FAMILY_RE = re.compile(r"^([a-z]+?)(\d+)([a-z]*)")


def _vendor(suffix: str) -> str:
    """Vendor marker from the family suffix: 'a' → AMD, 'g' → Graviton, else Intel."""
    for ch in suffix:
        if ch == "a":
            return "amd"
        if ch == "g":
            return "graviton"
        if ch == "i":
            return "intel"
    return "intel"


def microarchitecture(instance_type: str) -> str | None:
    """Map an instance type to its CPU microarchitecture, or ``None`` if unknown."""
    family = instance_type.split(".", 1)[0]
    match = _FAMILY_RE.match(family)
    if not match:
        return None
    generation = int(match.group(2))
    vendor = _vendor(match.group(3))
    table = {"intel": _INTEL_GEN, "amd": _AMD_GEN, "graviton": _GRAVITON_GEN}[vendor]
    return table.get(generation)


def ipc_factor(instance_type: str) -> float:
    """IPC multiplier for a type's microarchitecture (1.0 when unknown)."""
    micro = microarchitecture(instance_type)
    return IPC.get(micro, 1.0) if micro else 1.0


def effective_compute(instance_type: str, vcpu: int, clock_ghz: float | None) -> float | None:
    """Peak compute ≈ ``vCPU × clock × IPC``. ``None`` without a clock.

    This is the *nominal* (burst) compute — what the type does at full clock on
    every vCPU. For burstable (``t*``) types this is only sustainable while CPU
    credits last; see :func:`sustained_compute` for the credit-adjusted figure.
    """
    if not clock_ghz or vcpu <= 0:
        return None
    return vcpu * clock_ghz * ipc_factor(instance_type)


# Sustained baseline as a fraction of nominal compute, per burstable size — AWS's
# "baseline utilization % per vCPU", the level a ``t*`` instance holds at net-zero
# CPU credits. Above it, it burns credits; once exhausted, the hypervisor throttles
# it back to this baseline, which surfaces as CPU ``%steal``. Coarse, like IPC.
_BASELINE_T3 = {  # t3, t3a, t4g share these
    "nano": 0.05,
    "micro": 0.10,
    "small": 0.20,
    "medium": 0.20,
    "large": 0.30,
    "xlarge": 0.40,
    "2xlarge": 0.40,
}
_BASELINE_T2 = {
    "nano": 0.05,
    "micro": 0.10,
    "small": 0.20,
    "medium": 0.20,
    "large": 0.20,
    "xlarge": 0.226,
    "2xlarge": 0.17,
}
_BURSTABLE_RE = re.compile(r"^t\d")  # t2/t3/t3a/t4g — NOT trn1 (accelerated)
_BASELINE_FALLBACK = 0.20  # unknown burstable size
# Flex (``*-flex``) types hold a 40 % baseline and only reach full clock ~95 % of
# the time over a rolling 24 h window — so they too throttle under sustained load,
# just less aggressively than t*. AWS publishes the same 40 % baseline across sizes.
_FLEX_BASELINE = 0.40


def throttle_kind(instance_type: str) -> str | None:
    """Classify CPU throttling: ``'burstable'`` (``t*``), ``'flex'`` (``*-flex``), else ``None``."""
    family = instance_type.split(".", 1)[0]
    if "-flex" in family:
        return "flex"
    if _BURSTABLE_RE.match(family):
        return "burstable"
    return None


def baseline_ratio(instance_type: str) -> float:
    """Sustained-compute fraction for a throttled type; ``1.0`` for full-perf families.

    A ``t*`` instance sustains only a fraction of its nominal vCPUs at net-zero CPU
    credits; a ``*-flex`` holds a 40 % baseline above which full clock is best-effort.
    Beyond their baseline both throttle (CPU steal). Every other family returns ``1.0``.
    """
    family = instance_type.split(".", 1)[0]
    if "-flex" in family:
        return _FLEX_BASELINE
    if not _BURSTABLE_RE.match(family):
        return 1.0
    size = instance_type.split(".", 1)[1] if "." in instance_type else ""
    table = _BASELINE_T2 if family.startswith("t2") else _BASELINE_T3
    return table.get(size, _BASELINE_FALLBACK)


def sustained_compute(instance_type: str, vcpu: int, clock_ghz: float | None) -> float | None:
    """Credit-adjusted compute ≈ ``effective_compute × baseline_ratio``.

    Equals :func:`effective_compute` for non-burstable types (ratio ``1.0``);
    for ``t*`` it is penalised to the sustainable baseline. ``None`` without a clock.
    """
    base = effective_compute(instance_type, vcpu, clock_ghz)
    return base * baseline_ratio(instance_type) if base is not None else None


def cost_per_work(price: float | None, instance_type: str, vcpu: int, clock_ghz: float | None) -> float | None:
    """``price / sustained_compute`` — lower is better. ``None`` if inputs missing.

    Uses sustained (credit-adjusted) compute, so a burstable type is costed on the
    work it can actually hold under sustained load, not its burst peak.
    """
    compute = sustained_compute(instance_type, vcpu, clock_ghz)
    if price is None or compute is None or compute <= 0:
        return None
    return price / compute
