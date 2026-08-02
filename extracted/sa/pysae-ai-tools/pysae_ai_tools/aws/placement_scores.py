"""AWS EC2 Spot Placement Scores (``get-spot-placement-scores``).

A forward-looking, **account- and region-scoped** score from 1 (poor) to 10
(excellent) of how likely a spot **request** is to be fulfilled and kept. The
request is a *diversified pool*: ``get-spot-placement-scores`` takes a **set** of
instance types and a target capacity, evaluates them together, and returns **one
score per region** — not one score per type. AWS is explicit that a request of
one or two types is always scored low, so the score is only meaningful for a mix
of **≥3 types**. We therefore score per **mix** (a node group's current vs
recommended instance-type set), not per type.

Each ``(types, target_capacity)`` set is one **configuration** against an opaque,
unreadable AWS *daily configuration budget*: once exhausted, every new config
returns ``MaxConfigLimitExceeded`` until it refills. A configuration already
requested in the **last 24 h** is replayed for free. We exploit that with a local
24 h cache (a mix seen recently is served from disk, no API hit, no budget spend)
and stop early when AWS rejects a config on the quota — the rest would only fail.
"""

import time
from pathlib import Path
from tempfile import gettempdir

from .awscli import CACHE_TTL_SECONDS, OP_PLACEMENT, AwsQuotaError, DiskCache, call_log, run_aws_json

OPERATION = OP_PLACEMENT
# AWS replays a configuration requested within 24 h for free — the TTL (see
# CACHE_TTL_SECONDS) mirrors that window so a cached score is always one AWS
# would still honour without spend.
_CACHE = DiskCache(Path(gettempdir()) / "pysae-spot-placement-scores.json", CACHE_TTL_SECONDS[OP_PLACEMENT])

# A scored configuration: the sorted instance-type set + its target capacity.
Config = tuple[tuple[str, ...], int]


def _cache_key(region: str, types: tuple[str, ...], target: int) -> str:
    return f"{region}|{','.join(types)}|{target}"


def fetch_placement_scores(
    region: str,
    configs: set[Config],
    *,
    profile: str = "",
    use_cache: bool = True,
) -> dict[Config, int]:
    """Return ``{(sorted_types, target_capacity): score 1-10}`` per **mix**.

    Each config is one ``get-spot-placement-scores`` call passing the whole type
    set (``--instance-types``) at the target capacity, keeping the single region
    score. Configs seen within the last 24 h are served from the local cache
    (counted as cache reads, never an API call) unless ``use_cache`` is False.
    A non-quota failure for a config is skipped (absent from the result); a
    :class:`AwsQuotaError` (``MaxConfigLimitExceeded`` or throttle) **stops the
    loop** — once the daily configuration budget is spent every further new
    config would only add another rejection.
    """
    out: dict[Config, int] = {}
    now = time.time()

    for types, target in sorted(configs):
        if not types:
            continue
        tc = max(int(target), 1)
        key = _cache_key(region, types, tc)
        if use_cache:
            hit, value = _CACHE.get(key, now)
            if hit:
                call_log().record_cache_read(OPERATION)
                if value is not None:
                    out[(types, tc)] = int(value)
                continue
        try:
            payload = run_aws_json(
                [
                    "ec2",
                    "get-spot-placement-scores",
                    "--region",
                    region,
                    "--instance-types",
                    *types,
                    "--target-capacity",
                    str(tc),
                    "--region-names",
                    region,
                ],
                profile=profile,
            )
        except AwsQuotaError:
            break  # daily configuration budget spent — the rest would only re-fail
        except RuntimeError:
            continue
        scores = payload.get("SpotPlacementScores") or []
        score = scores[0].get("Score") if scores else None
        # Cache even a miss (score=None) so we don't re-spend the budget on a mix
        # AWS does not score in this region within the 24 h window.
        _CACHE.set(key, int(score) if score is not None else None, now)
        call_log().record_cache_write(OPERATION)
        if score is not None:
            out[(types, tc)] = int(score)

    _CACHE.save()
    return out
