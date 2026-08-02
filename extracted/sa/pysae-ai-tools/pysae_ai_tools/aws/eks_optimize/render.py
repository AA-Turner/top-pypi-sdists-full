"""Markdown and JSON rendering of the node group plans — pure formatting functions.

Every function takes already-scored :class:`NodeGroupPlan` objects and returns
strings / rows; nothing here talks to AWS or Datadog, so the report format can
evolve independently of the scoring.
"""

import json
from typing import Any

from .. import perf
from ..awscli import CACHE_TTL_SECONDS, CACHEABLE_OPERATIONS, AwsCallLog, humanize_duration
from ..timerange import parse_date
from .model import _RATE_MIDPOINT, EnvEvictions, MixMetrics, NodeGroupPlan, TypeOption
from .plan import _HEADROOM_MARGIN, _ng_prefix, mix_metrics

_HOURS_PER_MONTH = 730
# Per-throttle-kind cause text for the CPU-steal warning.
_THROTTLE_CAUSE = {
    "burstable": "`t*` (throttle quand les crédits CPU sont épuisés)",
    "flex": "`*-flex` (baseline 40 %, plein clock garanti ~95 % du temps sur 24 h)",
}


def _fmt_price(price: float | None) -> str:
    return f"${price:.4f}/h" if price is not None else "$ n/a"


def _fmt_cpw(cpw: float | None) -> str:
    return f"{cpw:.5f}" if cpw is not None else "n/a"


def _obs_val(o: TypeOption) -> str:
    """Observed interruption signal: ``rate% (evictions/launches)``.

    The absolute counts are shown next to the rate so a high percentage on a
    tiny sample (e.g. ``100% (1/1)``) is not mistaken for a heavily-evicted pool
    like ``42% (60/142)``. Counts are **region-wide per type** (pooled across
    node groups): a spot pool reclaims the same whichever node group runs it.
    """
    if o.observed_rate is None:
        return "n/a"
    flag = ""
    if o.rate_index is not None and o.observed_rate > _RATE_MIDPOINT.get(o.rate_index, 0) * 1.5 + 2:
        flag = " 🔴"
    return f"{o.observed_rate:.0f}% ({o.observed_evictions or 0}/{o.observed_launches}){flag}"


def _micro(o: TypeOption) -> str:
    return o.microarch.split("-")[-1] if o.microarch else "?"


def _status(o: TypeOption, current_types: set[str]) -> str:
    if o.instance_type in current_types:
        base = "◀ current"
    elif not o.recommendable:
        base = "off-fam"
    else:
        base = ""
    kind = o.throttle_kind
    if kind:
        tag = "flex" if kind == "flex" else "burst"
        base = f"{base} · {tag}" if base else tag
    return base


def _md_table(headers: list[str], rows: list[list[str]]) -> list[str]:
    out = ["| " + " | ".join(headers) + " |", "|" + "|".join("---" for _ in headers) + "|"]
    out += ["| " + " | ".join(r) + " |" for r in rows]
    return out


def _instance_table(plan: NodeGroupPlan, cpu: int, cap: str, *, is_spot: bool) -> list[str]:
    """One Markdown table per node group: every compatible type ranked by score.

    Current types use their per-node-group observed rate; the rest use the
    account-wide rate. A `◀ actuel` / `hors-fam` marker tags each row.
    """
    by_type: dict[str, TypeOption] = {o.instance_type: o for o in plan.compatible}
    for o in plan.current:  # override candidates with the per-node-group current option
        by_type[o.instance_type] = o
    current_types = plan.current_types
    # Show recommendable families + whatever is currently in use; hide other off-family noise.
    shown = [o for o in by_type.values() if o.recommendable or o.instance_type in current_types]
    rows_opts = sorted(shown, key=lambda o: -(o.score or 0.0))

    if is_spot:
        # Placement score is a per-mix signal (shown with the recommended mix below),
        # not per type — AWS scores a diversified request, never a single type.
        headers = ["Type", "Status", "Predicted", "Obs.", "$/h", "µarch", "$/work", "Score"]
        rows = [
            [
                o.instance_type,
                _status(o, current_types),
                f"{o.rate_emoji} {o.rate_label}",
                _obs_val(o),
                f"${o.price(cap):.4f}" if o.price(cap) is not None else "n/a",
                _micro(o),
                _fmt_cpw(o.cost_per_work(cpu, cap)),
                f"{o.score:.0f}" if o.score is not None else "n/a",
            ]
            for o in rows_opts
        ]
    else:
        headers = ["Type", "Status", "$/h", "µarch", "$/work", "Score"]
        rows = [
            [
                o.instance_type,
                _status(o, current_types),
                f"${o.price(cap):.4f}" if o.price(cap) is not None else "n/a",
                _micro(o),
                _fmt_cpw(o.cost_per_work(cpu, cap)),
                f"{o.score:.0f}" if o.score is not None else "n/a",
            ]
            for o in rows_opts
        ]
    return _md_table(headers, rows)


def _window_hours(start_iso: str, end_iso: str) -> float:
    return (parse_date(end_iso) - parse_date(start_iso)).total_seconds() / 3600.0


def _period_cost_line(cur_cost: float | None, new_cost: float | None, desired: int, hours: float) -> str | None:
    nodes = max(desired, 1)
    if new_cost is None:
        return None
    new_total = new_cost * nodes * hours
    if cur_cost is None:
        monthly = new_cost * nodes * _HOURS_PER_MONTH
        return f"period cost (~{nodes} nodes × {hours:.0f}h): ~${new_total:,.0f}  (~${monthly:,.0f}/month)"
    cur_total = cur_cost * nodes * hours
    delta = new_total - cur_total
    monthly = (new_cost - cur_cost) * nodes * _HOURS_PER_MONTH
    sign, msign = ("+" if delta >= 0 else "−"), ("+" if monthly >= 0 else "−")
    return (
        f"period cost (~{nodes} nodes × {hours:.0f}h): ~${cur_total:,.0f} → ~${new_total:,.0f}  "
        f"Δ {sign}${abs(delta):,.0f}  (~{msign}${abs(monthly):,.0f}/month)"
    )


def _api_calls_section(log: AwsCallLog) -> list[str]:
    """Render the AWS API footprint: per-operation played / ok / failed / quota / cached.

    Surfaces the placement-score quota story (``MaxConfigLimitExceeded``) right
    in the deterministic report rather than leaving it to the synthesis: a type
    showing ``n/a`` because its configuration was quota-blocked is materially
    different from one AWS simply does not score.
    """
    if not log.ops:
        return []
    lines = ["\n## AWS API calls"]
    lines.append(
        "_Requests issued this run. **Cache Hit** = served from a local store (no API hit, no quota spend); "
        "**Cached** = fresh results stored for later runs; **Cache TTL** = how long each store stays valid._"
    )
    lines.append("")  # blank line so the Markdown table renders below the intro
    headers = ["Operation", "Played", "OK", "Failed", "Quota-blocked", "Cached", "Cache Hit", "Cache TTL"]

    def _cell(op: str, value: int) -> str:
        # Non-cacheable operations show "-" so a 0 is not read as "cacheable but never hit".
        return str(value) if op in CACHEABLE_OPERATIONS else "-"

    def _ttl(op: str) -> str:
        return humanize_duration(CACHE_TTL_SECONDS[op]) if op in CACHEABLE_OPERATIONS else "-"

    rows = [
        [
            op,
            str(s.played),
            str(s.ok),
            str(s.failed),
            str(s.quota_failed),
            _cell(op, s.cache_writes),
            _cell(op, s.cache_reads),
            _ttl(op),
        ]
        for op, s in sorted(log.ops.items())
    ]
    rows.append(
        [
            "**Total**",
            f"**{log.played}**",
            f"**{log.ok}**",
            f"**{log.failed}**",
            f"**{log.quota_failed}**",
            f"**{log.cache_writes}**",
            f"**{log.cache_reads}**",
            "",
        ]
    )
    lines += _md_table(headers, rows)
    if log.quota_failed:
        lines.append(
            f"\n> ⚠️ **{log.quota_failed} request(s) hit an AWS quota/throttle limit** "
            "(`MaxConfigLimitExceeded` for Spot Placement Score = the daily configuration budget). "
            "Affected mixes show placement `n/a`; the per-type score relies on observed + predictive signals "
            "and is unaffected. A configuration already requested in the last 24h replays for free — re-run "
            "later (the local cache will reuse it) or pass `--no-placement` to skip these lookups entirely."
        )
    return lines


def _placement_line(plan: NodeGroupPlan, greenfield: bool) -> str | None:
    """One line: the mix Spot Placement Score (proposed, and current → proposed otherwise).

    The score rates the whole mix as a diversified request (1-10, higher = more
    likely to be fulfilled and kept) — it is a pool-level signal, not per type.
    """

    def fmt(v: int | None) -> str:
        return f"{v}/10" if v is not None else "n/a"

    new = plan.recommended_placement
    if greenfield:
        return f"placement score (proposed mix, ≥3 types): {fmt(new)}" if new is not None else None
    cur = plan.current_placement
    if cur is None and new is None:
        return None
    return f"placement score (mix as a diversified request): {fmt(cur)} → {fmt(new)}"


def _candidates_table(plan: NodeGroupPlan) -> list[str]:
    """Markdown table of the placement-scored candidate mixes (only when ≥2 distinct mixes)."""
    if len(plan.candidates) < 2:
        return []
    rows = [
        [
            "✓" if c is plan.chosen else "",
            c.strategy,
            ", ".join(c.instance_types),
            f"{c.mean_score:.0f}",
            f"{c.placement}/10" if c.placement is not None else "n/a",
        ]
        for c in plan.candidates
    ]
    lines = ["\n_Candidate mixes (placement-scored; ✓ = chosen, placement breaks near-ties on score):_"]
    return lines + _md_table(["", "Strategy", "Mix", "Mean score", "Placement"], rows)


def _recap_placement(plan: NodeGroupPlan) -> str:
    """Recap suffix with the recommended mix's Spot Placement Score (SPOT only)."""
    if not plan.ng.is_spot:
        return ""
    p = plan.recommended_placement
    return f"  · Plc {p}/10" if p is not None else "  · Plc n/a"


def _env_eviction_line(summary: EnvEvictions) -> str:
    """One italic line: env total, in-scope share, and the out-of-scope breakdown."""
    line = f"_Environment evictions (window): **{summary.total}** total · " f"{summary.in_scope} on current node groups"
    if summary.out_of_scope:
        details = ", ".join(f"`{k}` {v}" for k, v in sorted(summary.orphans.items(), key=lambda kv: -kv[1]))
        line += f" · **{summary.out_of_scope} out of scope** (renamed/deleted/other): {details}"
    return line + "_"


def render_markdown(
    plans: list[NodeGroupPlan],
    region: str,
    start_iso: str,
    end_iso: str,
    goal: str,
    env_evictions: dict[str, EnvEvictions] | None = None,
    api_calls: AwsCallLog | None = None,
) -> str:
    """Build the full Markdown report (one table per node group)."""
    lines = [f"# Node group optimization — {region} · {start_iso} → {end_iso} · goal={goal}"]
    hours = _window_hours(start_iso, end_iso)
    env_ev = env_evictions or {}
    priority = {"prod": 0, "dev": 1, "staging": 2, "review": 3, "test": 4}
    ordered = sorted(plans, key=lambda p: (priority.get(p.ng.env, 9), p.ng.env, p.ng.cluster, p.ng.name))

    recap: list[str] = []  # one line per node group: "name: type, type, …"
    rendered_envs: set[str] = set()
    last_env = None
    for plan in ordered:
        ng = plan.ng
        if ng.env != last_env:
            lines.append(f"\n## ENV {ng.env.upper()} — cluster {ng.cluster}")
            rendered_envs.add(ng.env)
            summary = env_ev.get(ng.env)
            if summary and summary.total:
                lines.append(_env_eviction_line(summary))
            last_env = ng.env

        cpu = plan.shape[0] if plan.shape else 0
        cap = ng.capacity_type
        shape = f"{plan.shape[0]} vCPU/{plan.shape[1]} GiB" if plan.shape else "shape ?"
        evict = f" · {plan.observed_evictions} evictions (window)" if ng.is_spot else ""
        cpu_obs = ""
        if plan.observed_cpu is not None and plan.shape:
            c = plan.observed_cpu
            used_vcpu = c.p95 * plan.shape[0]
            cpu_obs = f" · CPU/node p95 {used_vcpu:.2f} vCPU ({c.p95 * 100:.0f}%) · p99 {c.p99 * 100:.0f}%"
        lines.append(f"\n### ▸ {_ng_prefix(ng.name)} — {cap or '?'} · {shape} · desired {ng.desired}{evict}{cpu_obs}\n")

        if plan.note:
            lines.append(f"_{plan.note}_")
            continue
        if not plan.compatible:
            lines.append("_no compatible alternative found._")
            continue

        lines += _instance_table(plan, cpu, cap, is_spot=ng.is_spot)

        rec = plan.recommended()
        throttled = [o for o in (*plan.current, *rec) if o.throttle_kind]
        relieved = [o for o in throttled if o.sustained_relief]
        if relieved and plan.observed_cpu is not None:
            types = ", ".join(sorted({o.instance_type for o in relieved}))
            used = f"{plan.observed_cpu.p95 * 100:.0f}%"
            if plan.shape:
                used = f"{plan.observed_cpu.p95 * plan.shape[0]:.2f} vCPU/node ({used})"
            lines.append(
                f"\n> ✅ **Type CPU-throttled adapté ici** — conso soutenue p95 {used}, sous la "
                f"baseline de {types} (marge {int(_HEADROOM_MARGIN * 100)} %) : le throttle ne se "
                "déclenchera pas en pratique → t*/flex tient la charge pour un coût réduit."
            )
        elif throttled and plan.observed_cpu is None:
            lines.append(
                "\n> ℹ️ **Head-room CPU non calculable** — aucune métrique Datadog pour ce pool "
                "(nodes éphémères / sans agent, typiquement les runners CI). Les types throttled "
                "(t*/flex) sont donc **non recommandés par défaut** (pénalité statique) : ce n'est "
                "**pas** une reco basée sur la charge réelle. Si ce pool tolère le throttle (cas "
                f"runner CI), relance avec `--force-throttled {_ng_prefix(ng.name)}`."
            )
        elif throttled:
            kinds: set[str] = set()
            for o in throttled:
                k = o.throttle_kind
                if k is not None:
                    kinds.add(k)
            cause = " et ".join(_THROTTLE_CAUSE[k] for k in sorted(kinds))
            lines.append(
                f"\n> ⚠️ **Type CPU-throttled dans ce pool** — {cause}. La perf affichée est la "
                "perf *soutenue* (baseline), pas la perf crête : sous charge soutenue, throttling → "
                "pénurie CPU (`%steal`). Acceptable pour un pool tolérant (runners CI, batch : jobs "
                "plus lents par moments, peu d'évictions, coût bas) ; à proscrire pour du "
                "latency-sensitive (API)."
            )
        if not rec:
            lines.append("\n_no recommendable alternative (preferred families)._")
            continue
        greenfield = not plan.current
        same_as_current = not greenfield and {o.instance_type for o in rec} == plan.current_types
        marker = "  ✓ already the current mix" if same_as_current else ""
        # Note the chosen strategy when placement picked among several candidates.
        if plan.chosen is not None and len(plan.candidates) >= 2:
            marker += f"  _({plan.chosen.strategy}-led)_"
        cur_m = mix_metrics(plan.current, cpu, cap, is_spot=ng.is_spot)
        new_m = mix_metrics(rec, cpu, cap, is_spot=ng.is_spot)
        lines.append(f"\n**Recommended mix**: {', '.join(o.instance_type for o in rec)}{marker}\n")
        if greenfield:
            lines += _md_table(["Factor", "Value"], _absolute_rows(new_m))
        else:
            lines += _md_table(["Factor", "Current", "Proposed", "Δ"], _evolution_rows(cur_m, new_m))
        cost_line = _period_cost_line(None if greenfield else cur_m.cost, new_m.cost, ng.desired, hours)
        if cost_line:
            lines.append(f"\n{cost_line}")
        if ng.is_spot:
            placement_line = _placement_line(plan, greenfield)
            if placement_line:
                lines.append(f"\n{placement_line}")
            lines += _candidates_table(plan)
        lines.append(f"\n`terraform instance_types = {json.dumps([o.instance_type for o in rec])}`")
        recap_mark = "  ✓ already current" if same_as_current else ""
        recap.append(
            f"- **{_ng_prefix(ng.name)}**: {', '.join(o.instance_type for o in rec)}"
            f"{_recap_placement(plan)}{recap_mark}"
        )

    # Evictions in environments that have no current node group in scope would
    # otherwise vanish entirely — surface them so the information is never lost.
    leftover = {e: s for e, s in env_ev.items() if s.total and e not in rendered_envs}
    if leftover:
        lines.append("\n## Out-of-scope evictions")
        lines.append("_Spot interruptions on environments with no current node group (renamed/deleted/other):_")
        for env in sorted(leftover):
            lines.append(f"- **{env}**: {_env_eviction_line(leftover[env])}")

    if api_calls is not None:
        lines += _api_calls_section(api_calls)

    if recap:
        lines.append("\n## Recommended mixes")
        lines += recap
    return "\n".join(lines) + "\n"


def _evolution(cur: float | None, new: float | None, *, lower_is_better: bool) -> tuple[float | None, str]:
    if cur is None or new is None or cur == 0:
        return (None, "·")
    delta = 100 * (new - cur) / cur
    improved = (new < cur) if lower_is_better else (new > cur)
    if abs(delta) < 1:
        return (delta, "≈")
    return (delta, "✅" if improved else "⚠️")


def _perf_fmt(v: float | None) -> str:
    return f"{v:.1f}wu" if v is not None else "n/a"


def _risk_fmt(v: float | None) -> str:
    return f"~{v:.1f}%" if v is not None else "n/a"


def _factor_specs(cur: MixMetrics, new: MixMetrics) -> list[tuple[str, float | None, float | None, Any, bool]]:
    return [
        ("cost", cur.cost, new.cost, _fmt_price, True),
        ("perf", cur.perf, new.perf, _perf_fmt, False),
        ("cost/perf", cur.cost_per_work, new.cost_per_work, _fmt_cpw, True),
        ("eviction", cur.eviction_risk, new.eviction_risk, _risk_fmt, True),
    ]


def _evolution_rows(cur: MixMetrics, new: MixMetrics) -> list[list[str]]:
    """Markdown rows: [facteur, actuel, proposé, Δ% verdict] for the 4 factors."""
    rows: list[list[str]] = []
    for label, c, n, fmt, lower in _factor_specs(cur, new):
        delta, emoji = _evolution(c, n, lower_is_better=lower)
        d = f"{delta:+.0f}% {emoji}" if delta is not None else "—"
        rows.append([label, fmt(c), fmt(n), d])
    return rows


def _absolute_rows(m: MixMetrics) -> list[list[str]]:
    """Markdown rows: [facteur, valeur] (greenfield — no current to compare)."""
    return [
        ["cost", _fmt_price(m.cost)],
        ["perf", _perf_fmt(m.perf)],
        ["cost/perf", _fmt_cpw(m.cost_per_work)],
        ["eviction", _risk_fmt(m.eviction_risk)],
    ]


def _plan_json(plan: NodeGroupPlan) -> dict[str, Any]:
    ng = plan.ng
    cpu = plan.shape[0] if plan.shape else 0

    def opt(o: TypeOption) -> dict[str, Any]:
        return {
            "instance_type": o.instance_type,
            "score": o.score,
            "rate": o.rate_label if ng.is_spot else None,
            "observed_rate_pct": o.observed_rate,
            "observed_evictions": o.observed_evictions,
            "observed_launches": o.observed_launches,
            "spot_price": o.spot_price,
            "ondemand_price": o.ondemand_price,
            "clock_ghz": o.clock_ghz,
            "microarch": o.microarch,
            "cost_per_work": o.cost_per_work(cpu, ng.capacity_type),
            "recommendable": o.recommendable,
            "throttle_kind": o.throttle_kind,
            "baseline_ratio": perf.baseline_ratio(o.instance_type) if o.is_burstable else None,
            "sustained_relief": o.sustained_relief,
        }

    def metrics(m: MixMetrics) -> dict[str, Any]:
        return {
            "cost_usd_per_hour": m.cost,
            "perf_work_units": m.perf,
            "cost_per_work": m.cost_per_work,
            "eviction_risk_pct": m.eviction_risk,
        }

    rec = plan.recommended()
    return {
        "env": ng.env,
        "cluster": ng.cluster,
        "nodegroup": ng.name,
        "capacity_type": ng.capacity_type,
        "desired": ng.desired,
        "shape": {"vcpu": plan.shape[0], "ram_gib": plan.shape[1]} if plan.shape else None,
        "observed_evictions": plan.observed_evictions if ng.is_spot else None,
        "observed_cpu_p95_util": plan.observed_cpu.p95 if plan.observed_cpu else None,
        "observed_cpu_p99_util": plan.observed_cpu.p99 if plan.observed_cpu else None,
        "current": [opt(o) for o in plan.current],
        "current_metrics": metrics(mix_metrics(plan.current, cpu, ng.capacity_type, is_spot=ng.is_spot)),
        "other_available": [opt(o) for o in plan.others()],
        "recommended_instance_types": [o.instance_type for o in rec],
        "recommended_metrics": metrics(mix_metrics(rec, cpu, ng.capacity_type, is_spot=ng.is_spot)),
        "current_placement_score": plan.current_placement if ng.is_spot else None,
        "recommended_placement_score": plan.recommended_placement if ng.is_spot else None,
        "recommended_strategy": plan.chosen.strategy if plan.chosen else None,
        "candidate_mixes": [
            {
                "strategy": c.strategy,
                "instance_types": c.instance_types,
                "mean_score": round(c.mean_score, 1),
                "placement_score": c.placement,
                "chosen": c is plan.chosen,
            }
            for c in plan.candidates
        ],
        "note": plan.note,
    }
