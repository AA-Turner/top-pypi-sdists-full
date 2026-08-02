"""Business logic: eviction attribution, plan building, scoring, and mix selection.

Every function here is pure over plain dicts/dataclasses (the AWS/Datadog fetches
happen in :mod:`cli`), so scoring and plan construction are testable in isolation
without HTTP-level mocks.
"""

import re
from typing import Any

from .. import perf
from ..eks import NodeGroup
from ..eks_cpu import CpuUtil
from ..instance_specs import InstanceSpec
from ..placement_scores import Config, fetch_placement_scores
from ..scoring import Signals, global_scores, reliability
from ..spot_advisor import advise, is_accelerated_family, is_excluded_family
from ..spot_evictions import cluster_to_env
from .model import _RATE_MIDPOINT, _RECOMMENDED_SPOT, EnvEvictions, MixCandidate, MixMetrics, NodeGroupPlan, TypeOption

# Candidate SPOT mixes scored by placement, in preferred order. The placement
# score breaks ties between candidates whose mean global score is within
# _SCORE_BAND points (0-100): a near-as-good mix that places clearly better wins.
_CANDIDATE_STRATEGIES = ("score", "reliability", "cost")
_SCORE_BAND = 5.0
# Fraction of a throttled type's baseline the sustained load must stay under for
# the throttle to be considered safely out of reach (head-room safety margin).
_HEADROOM_MARGIN = 0.8

_NG_ID_SUFFIX_RE = re.compile(r"-\d+$")


def _ng_prefix(name: str) -> str:
    """Strip a node group's trailing Terraform-generated numeric id.

    e.g. ``dev-bo-20260401040725979400000013`` → ``dev-bo``. Changing a node
    group's instance types recreates it with a **new** suffix but a **stable**
    prefix, so attribution (evictions, launches) and display both key on the
    prefix — this merges the history of a recreated node group instead of
    losing it under the old suffix.
    """
    return _NG_ID_SUFFIX_RE.sub("", name)


def evictions_per_nodegroup(
    eviction_events: list[dict[str, Any]], instances: dict[str, Any]
) -> dict[tuple[str, str], int]:
    """Count reclaimed instances per ``(cluster, nodegroup)``."""
    counts: dict[tuple[str, str], int] = {}
    for e in eviction_events:
        for iid in (e.get("serviceEventDetails") or {}).get("instanceIdSet", []) or []:
            info = instances.get(iid)
            if not info or not info.cluster:
                continue
            key = (info.cluster, _ng_prefix(info.nodegroup or "?"))
            counts[key] = counts.get(key, 0) + 1
    return counts


def _by_key(items: list[tuple[str, str, str]]) -> dict[tuple[str, str, str], int]:
    counts: dict[tuple[str, str, str], int] = {}
    for key in items:
        counts[key] = counts.get(key, 0) + 1
    return counts


def evictions_by_type(
    eviction_events: list[dict[str, Any]], instances: dict[str, Any]
) -> dict[tuple[str, str, str], int]:
    """Count reclaimed instances per ``(cluster, nodegroup, instance_type)``."""
    keys: list[tuple[str, str, str]] = []
    for e in eviction_events:
        for iid in (e.get("serviceEventDetails") or {}).get("instanceIdSet", []) or []:
            info = instances.get(iid)
            if info and info.cluster:
                keys.append((info.cluster, _ng_prefix(info.nodegroup or "?"), info.instance_type or "?"))
    return _by_key(keys)


def launches_by_type(
    instances: dict[str, Any], window: tuple[str, str] | None = None
) -> dict[tuple[str, str, str], int]:
    """Count launched instances per ``(cluster, nodegroup-prefix, instance_type)`` (the rate denominator).

    ``window`` (``(start_iso, end_iso)``) restricts the count to instances
    **launched within the analysis window** — the same window the evictions are
    counted over. The instances map itself is intentionally wider (a buffer
    before the window) so an eviction of an older instance still resolves to its
    type, but those pre-window launches must **not** inflate the denominator, or
    a bursty pool's rate gets diluted (e.g. m6i.xlarge reads 8% instead of 40%).
    """
    keys: list[tuple[str, str, str]] = []
    for i in instances.values():
        if not i.cluster:
            continue
        if window is not None and not (i.launched_at and window[0] <= i.launched_at <= window[1]):
            continue
        keys.append((i.cluster, _ng_prefix(i.nodegroup or "?"), i.instance_type or "?"))
    return _by_key(keys)


def evictions_by_env(
    eviction_events: list[dict[str, Any]],
    instances: dict[str, Any],
    in_scope: set[tuple[str, str]],
) -> dict[str, EnvEvictions]:
    """Aggregate every eviction per environment, flagging the out-of-scope share.

    ``in_scope`` is the set of ``(cluster, nodegroup-prefix)`` of the current
    node groups. An eviction whose ``(cluster, prefix)`` is not in that set is
    counted under ``orphans`` (by node group prefix, or ``(unattributed)`` when
    the launch could not be resolved) — these are evictions on renamed / deleted
    / out-of-perimeter node groups that per-node-group attribution drops.
    """
    out: dict[str, EnvEvictions] = {}
    for e in eviction_events:
        for iid in (e.get("serviceEventDetails") or {}).get("instanceIdSet", []) or []:
            info = instances.get(iid)
            cluster = info.cluster if info and info.cluster else ""
            env = cluster_to_env(cluster) if cluster else "unknown"
            summary = out.setdefault(env, EnvEvictions())
            summary.total += 1
            prefix = _ng_prefix(info.nodegroup) if info and info.nodegroup else ""
            if cluster and (cluster, prefix) in in_scope:
                summary.in_scope += 1
            else:
                label = prefix or "(unattributed)"
                summary.orphans[label] = summary.orphans.get(label, 0) + 1
    return out


def _rate_index(dataset: dict[str, Any], region: str, os_name: str, itype: str) -> int | None:
    spot = dataset.get("spot_advisor", {}).get(region, {}).get(os_name, {}).get(itype)
    return int(spot["r"]) if spot and "r" in spot else None


def _shape_of(dataset: dict[str, Any], itype: str) -> tuple[int, int] | None:
    spec = dataset.get("instance_types", {}).get(itype)
    if not spec or "cores" not in spec or "ram_gb" not in spec:
        return None
    return int(spec["cores"]), round(float(spec["ram_gb"]))


def compatible_types(
    dataset: dict[str, Any], region: str, shape: tuple[int, int], os_name: str, arch: str
) -> list[str]:
    """Every same-shape, same-arch type, minus GPU/accelerated families.

    Burstable is kept (it is a real same-shape CPU alternative, and some node
    groups run it) — it is just flagged non-recommendable downstream. GPU /
    accelerated families are dropped outright: they are never a fit for a
    general-purpose node group.
    """
    cpu, ram = shape
    return [
        a.instance_type
        for a in advise(dataset, region, cpu, ram, os_name=os_name, all_families=True, arch=arch)
        if not is_accelerated_family(a.instance_type)
    ]


def _option(
    itype: str,
    dataset: dict[str, Any],
    region: str,
    os_name: str,
    specs: dict[str, InstanceSpec],
    spot_prices: dict[str, float],
    ondemand_prices: dict[str, float],
    *,
    recommendable: bool,
) -> TypeOption:
    spec = specs.get(itype)
    return TypeOption(
        instance_type=itype,
        rate_index=_rate_index(dataset, region, os_name, itype),
        spot_price=spot_prices.get(itype),
        ondemand_price=ondemand_prices.get(itype),
        clock_ghz=spec.clock_ghz if spec else None,
        vendor=spec.vendor if spec else "",
        microarch=perf.microarchitecture(itype),
        recommendable=recommendable,
    )


def _ng_matches(ng_name: str, patterns: list[str]) -> bool:
    """True when a node group matches an override pattern (prefix of name or stable prefix)."""
    prefix = _ng_prefix(ng_name)
    return any(prefix.startswith(p) or ng_name.startswith(p) for p in patterns)


def _apply_throttle_policy(
    plan: NodeGroupPlan,
    cpu_util: dict[str, CpuUtil],
    exclude: list[str],
    force: list[str],
) -> None:
    """Set ``recommendable`` / ``sustained_relief`` on throttled (t*/flex) options.

    Order: ``--exclude-throttled`` wins (never recommend), then ``--force-throttled``
    (recommend + treat at full perf), else Datadog head-room — when the sustained
    per-node utilisation (p95 fraction) fits under a type's baseline fraction (×
    margin), the throttle never fires, so the type becomes recommendable and keeps
    its full (un-penalised) perf. Comparing fractions is valid because the candidate
    types share the node group's vCPU shape.
    """
    cpu = cpu_util.get(plan.ng.name)
    plan.observed_cpu = cpu
    excluded = _ng_matches(plan.ng.name, exclude)
    forced = _ng_matches(plan.ng.name, force)
    for o in (*plan.current, *plan.compatible):
        if not o.throttle_kind:
            continue
        if excluded:
            o.recommendable, o.sustained_relief = False, False
        elif forced:
            o.recommendable, o.sustained_relief = True, True
        elif cpu is not None and cpu.p95 < perf.baseline_ratio(o.instance_type) * _HEADROOM_MARGIN:
            o.recommendable, o.sustained_relief = True, True


def build_plans(
    dataset: dict[str, Any],
    region: str,
    os_name: str,
    nodegroups: list[NodeGroup],
    ng_evictions: dict[tuple[str, str], int],
    specs: dict[str, InstanceSpec],
    spot_prices: dict[str, float],
    ondemand_prices: dict[str, float],
    *,
    family: list[str] | None = None,
    all_families: bool = False,
    arch: str = "x86_64",
    shape_override: tuple[int, int] | None = None,
    ng_type_evictions: dict[tuple[str, str, str], int] | None = None,
    ng_type_launches: dict[tuple[str, str, str], int] | None = None,
    cpu_util: dict[str, CpuUtil] | None = None,
    exclude_throttled: list[str] | None = None,
    force_throttled: list[str] | None = None,
) -> list[NodeGroupPlan]:
    """Build one :class:`NodeGroupPlan` per node group (compatible field, unscored).

    ``family`` / ``all_families`` set which types are *recommendable* (the mix
    preference). ``ng_type_evictions`` / ``ng_type_launches`` are summed across
    node groups into a **region-wide per-type** observed rate, used identically
    for current types and candidates — spot reclamation is a pool property
    (type × AZ × region), so a type's rate does not depend on the node group.
    """
    ng_ev = ng_type_evictions or {}
    ng_lc = ng_type_launches or {}
    acct_ev: dict[str, int] = {}
    acct_lc: dict[str, int] = {}
    for (_, _, t), n in ng_ev.items():
        acct_ev[t] = acct_ev.get(t, 0) + n
    for (_, _, t), n in ng_lc.items():
        acct_lc[t] = acct_lc.get(t, 0) + n
    allowed = family or []

    plans: list[NodeGroupPlan] = []
    for ng in nodegroups:
        shape = _shape_of(dataset, ng.instance_types[0]) if ng.instance_types else shape_override
        prefix = _ng_prefix(ng.name)  # merge history across recreations (stable prefix, changing suffix)
        plan = NodeGroupPlan(ng=ng, observed_evictions=ng_evictions.get((ng.cluster, prefix), 0), shape=shape)

        for t in ng.instance_types:
            opt = _option(
                t,
                dataset,
                region,
                os_name,
                specs,
                spot_prices,
                ondemand_prices,
                recommendable=not is_excluded_family(t, allowed, all_families),
            )
            # Spot reclamation is a *pool* property (type × AZ × region), not a
            # node-group one — so the observed rate is region-wide per type, the
            # same number whichever node group runs it (the per-NG total stays in
            # the header). This also pools the sample for a less noisy rate.
            opt.observed_launches = acct_lc.get(t) or None
            opt.observed_evictions = acct_ev.get(t) if t in acct_lc else None
            plan.current.append(opt)

        if shape is None:
            plan.note = "could not resolve a vCPU/RAM shape from its instance types — no proposal."
            plans.append(plan)
            continue

        for t in compatible_types(dataset, region, shape, os_name, arch):
            opt = _option(
                t,
                dataset,
                region,
                os_name,
                specs,
                spot_prices,
                ondemand_prices,
                recommendable=not is_excluded_family(t, allowed, all_families),
            )
            opt.observed_launches = acct_lc.get(t) or None
            opt.observed_evictions = acct_ev.get(t) if t in acct_lc else None
            plan.compatible.append(opt)
        _apply_throttle_policy(plan, cpu_util or {}, exclude_throttled or [], force_throttled or [])
        plans.append(plan)
    return plans


def apply_scores(plans: list[NodeGroupPlan], goal: str) -> None:
    """Compute the 0-100 global score for every option and sort the compatible field by it."""
    for plan in plans:
        if not plan.shape:
            continue
        cpu, cap = plan.shape[0], plan.ng.capacity_type
        group = plan.current + plan.compatible
        if not group:
            continue
        sigs = [Signals(o.rate_index, o.observed_rate, o.price(cap), o.perf(cpu)) for o in group]
        for o, sc in zip(group, global_scores(sigs, goal), strict=True):
            o.score = sc
        plan.compatible.sort(key=lambda o: -(o.score or 0.0))


def _mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


def mix_metrics(options: list[TypeOption], cpu: int, capacity: str, *, is_spot: bool) -> MixMetrics:
    """Average the four factors across ``options`` (the instance-type mix)."""
    prices = [p for p in (o.price(capacity) for o in options) if p is not None]
    perfs = [p for p in (o.perf(cpu) for o in options) if p is not None]
    cpws = [c for c in (o.cost_per_work(cpu, capacity) for o in options) if c is not None]
    risks = [_RATE_MIDPOINT[o.rate_index] for o in options if o.rate_index is not None] if is_spot else []
    return MixMetrics(_mean(prices), _mean(perfs), _mean(cpws), _mean(risks))


def _mix_config(types: list[str], target: int) -> Config | None:
    """A placement configuration for a mix: the sorted unique type set + target."""
    uniq = tuple(sorted({t for t in types if t}))
    return (uniq, max(target, 1)) if uniq else None


def _reliability_of(o: TypeOption) -> float:
    """Per-type reliability proxy (observed + predictive) used to rank a reliability-led mix."""
    return reliability(Signals(o.rate_index, o.observed_rate, None, None))


def build_candidates(plan: NodeGroupPlan) -> list[MixCandidate]:
    """Up to three SPOT candidate mixes, in preferred order, deduped by their type set.

    Same recommendable field, three compositions: **score** (top by global score),
    **reliability** (lowest observed/predictive eviction risk), **cost** (cheapest
    spot $/h). They overlap when the field is small — identical sets collapse to one.
    """
    n = _RECOMMENDED_SPOT
    rec = [o for o in plan.compatible if o.recommendable]
    if not rec:
        return []
    built: dict[str, list[TypeOption]] = {
        "score": rec[:n],  # compatible is already sorted by global score desc
        "reliability": sorted(rec, key=lambda o: -_reliability_of(o))[:n],
        "cost": sorted(rec, key=lambda o: (o.price("SPOT") is None, o.price("SPOT") or 0.0))[:n],
    }
    out: list[MixCandidate] = []
    seen: set[frozenset[str]] = set()
    for strategy in _CANDIDATE_STRATEGIES:
        opts = built[strategy]
        key = frozenset(o.instance_type for o in opts)
        if opts and key not in seen:
            seen.add(key)
            out.append(MixCandidate(strategy=strategy, options=opts))
    return out


def _choose_candidate(plan: NodeGroupPlan) -> None:
    """Pick the recommended mix: the best mean score, but a near-tie that places clearly better wins.

    Among candidates whose mean global score is within ``_SCORE_BAND`` of the best,
    the one with the highest placement score is chosen (a scored mix beats an
    unscored one; mean score breaks remaining ties). Placement thus only overrides
    when the score cost is negligible.
    """
    if not plan.candidates:
        return
    best_mean = max(c.mean_score for c in plan.candidates)
    eligible = [c for c in plan.candidates if c.mean_score >= best_mean - _SCORE_BAND]
    plan.chosen = max(eligible, key=lambda c: (c.placement if c.placement is not None else -1, c.mean_score))


def _fetch_placement(plans: list[NodeGroupPlan], region: str, profile: str, *, use_cache: bool = True) -> None:
    """Build SPOT candidate mixes, score each (+ the current mix) by placement, pick the recommended one.

    A placement score rates a whole diversified *request* (a set of ≥3 types) as
    one configuration, returning a single pooled score — a one/two-type request is
    always scored low. So we score one config per **mix**: the current set plus a
    few candidate mixes (see :func:`build_candidates`), at the group's target
    capacity. Identical configs across node groups dedupe to a single AWS call.
    Must run **after** scoring (candidates are built from the per-type scores).
    """
    for plan in plans:
        if plan.ng.is_spot:
            plan.candidates = build_candidates(plan)

    wanted: list[tuple[NodeGroupPlan, Config | None, list[Config | None]]] = []
    configs: set[Config] = set()
    for plan in plans:
        if not plan.ng.is_spot:
            continue
        target = max(plan.ng.desired, 1)
        cur = _mix_config([o.instance_type for o in plan.current], target)
        cands = [_mix_config(c.instance_types, target) for c in plan.candidates]
        wanted.append((plan, cur, cands))
        configs.update(c for c in [cur, *cands] if c is not None)
    if not configs:
        return
    scores = fetch_placement_scores(region, configs, profile=profile, use_cache=use_cache)
    for plan, cur, cands in wanted:
        plan.current_placement = scores.get(cur) if cur is not None else None
        for candidate, cfg in zip(plan.candidates, cands, strict=True):
            candidate.placement = scores.get(cfg) if cfg is not None else None
        _choose_candidate(plan)
