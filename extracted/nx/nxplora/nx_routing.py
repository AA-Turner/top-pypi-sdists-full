"""
nx_routing.py — NX Intent Router (5-tier)

World → tier → model. The primary provider runs the bulk; the secondary is
the fallback when the primary is unreachable. Model IDs and provider URLs
are obfuscated in nx_obfuscate.py and never appear as literals here.

Tiers (cost order, cheap → expensive):
  flash     — cheapest workhorse, escalates on signals
  frontier  — deep reasoning, strategy, finance, legal, compliance
  agentic   — long-horizon orchestration
  code      — coding specialist
  council   — $council mode (handled by nx_council.py)

Escalation: a flash-tier request escalates to frontier if the input
contains strategy/decision keywords, exceeds 500 chars, or starts with
$council.
"""

import json
import os
import re
import threading
from dataclasses import dataclass, field
from typing import Optional

from nx_key_pool import get_deepinfra_key, get_fireworks_key, get_pool
from nx_obfuscate import ENV, FW, M, MR, NATIVE, OAI_FALLBACK, OR_FALLBACK, P
from nx_vpn import get_rotator


# ─── cache-hit + token counter (cost observability) ──────────────────────────
# The single biggest cost lever is the prefix-cache HIT RATE: cached input runs
# ~90% cheaper than uncached (the frontier model cached $0.145 vs $1.74). Nothing
# in NX measured it — so nobody could tell whether the system prompt + history
# were hitting the cache or being paid for in full every turn. This in-process
# counter accumulates the `usage` the provider returns per turn (prompt / cached
# / completion tokens) so the operator can SEE the real hit rate instead of
# guessing. Best-effort and fully isolated: a recording failure can never touch
# the request path. Seeded from and persisted to ~/.nx/cache_stats.json so the
# number survives a CLI restart (the counter STICKS across sessions).
_CACHE_LOCK = threading.Lock()
_CACHE_KEYS = ("requests", "prompt_tokens", "cached_tokens", "completion_tokens")
_CACHE_STATS = {k: 0 for k in _CACHE_KEYS}

# ─── autonomous provider cost-tuner (self-measure → self-shadow → self-shift) ─
# NX doesn't just RECORD usage — it acts on it. It keeps a per-provider ledger
# (tokens + health), and on its own routes a fraction of traffic to the
# secondary provider to gather a live comparison, then SHIFTS the split toward
# whichever is cheaper-at-equal-health. No operator step: the model runs its own
# shadow test. Guardrails keep it safe:
#   • Only engages when BOTH the primary and secondary provider
#     keys are configured — i.e. the operator already authorized that provider.
#     The secondary provider is already in the failover chain, so this adds no NEW
#     data destination, only changes how often an already-reachable one is used.
#   • A health gate never sends bulk traffic to a provider that's failing more.
#   • The shift is capped (never 100/0 — a floor keeps re-checking for drift)
#     and fully reversible: NX_TUNER=off reverts to the static order next turn.
# `local_prompt` = OUR independent estimate of prompt size (chars/4 of what we sent), accumulated alongside
# the provider-REPORTED `prompt_tokens`. The tuner routes on the provider's own usage frame, so a provider
# that under-reports prompt tokens (or over-reports cached) looks cheaper and would earn more traffic —
# vendors grading their own homework. We keep a local yardstick to catch that (see _avg_cost_from / _suspect).
_PROV_KEYS = ("requests", "prompt_tokens", "cached_tokens", "completion_tokens", "failures", "local_prompt")
_PROV_STATS = {}            # provider -> {k: 0 for k in _PROV_KEYS}
_TUNE_COUNTER = [0]         # rolling 0..99 request counter → DETERMINISTIC split (no RNG)

# Public list-price estimate ($/M tokens), blended across the stack — used ONLY
# to RANK providers by relative cost, never for billing. No model names appear
# (keyed by provider). A HARDCODED price sheet goes stale silently the moment a
# vendor changes pricing, so it is: (1) stamped with an as-of date that /cache
# surfaces, and (2) overridable at runtime via NX_PROVIDER_RATES (JSON) or
# ~/.nx/provider_rates.json — so the operator can correct it without a release.
_RATES_ASOF = "2026-07"   # bump when the defaults below are re-checked against list prices
_PROVIDER_RATES_DEFAULT = {
    P["fireworks"]: {"in": 1.35, "cached": 0.16, "out": 3.74},
    P["fallback"]:  {"in": 1.03, "cached": 0.13, "out": 3.05},
}


def _load_provider_rates() -> dict:
    """Defaults, overlaid by any operator override (env NX_PROVIDER_RATES as JSON, else
    ~/.nx/provider_rates.json). Override shape: {"<provider>": {"in":_, "cached":_, "out":_}}.
    Best-effort — a malformed override is ignored, never crashes routing."""
    rates = {p: dict(r) for p, r in _PROVIDER_RATES_DEFAULT.items()}
    for src in (os.environ.get("NX_PROVIDER_RATES"),
                _read_file_if_exists(os.path.join(os.path.expanduser("~"), ".nx", "provider_rates.json"))):
        if not src:
            continue
        try:
            over = json.loads(src)
            for prov, r in (over or {}).items():
                if isinstance(r, dict):
                    rates.setdefault(prov, {}).update({k: float(v) for k, v in r.items()
                                                       if k in ("in", "cached", "out")})
        except Exception:
            pass
    return rates


def _read_file_if_exists(path):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


_PROVIDER_RATES = _load_provider_rates()

# Guardrails (all env-overridable; defaults are the autonomous posture).
_TUNER_MIN_SAMPLE = int(os.environ.get("NX_TUNER_MIN_SAMPLE", "20") or 20)      # need N reqs/side before shifting
_TUNER_MAX_SHADOW = min(95, int(os.environ.get("NX_TUNER_MAX_SHADOW", "80") or 80))  # cap toward the secondary
_TUNER_EXPLORE    = int(os.environ.get("NX_TUNER_EXPLORE", "15") or 15)         # baseline exploration weight
_TUNER_FLOOR      = int(os.environ.get("NX_TUNER_FLOOR", "5") or 5)             # never fully abandon a provider
_TUNER_HEALTH_TOL = float(os.environ.get("NX_TUNER_HEALTH_TOL", "0.05") or 0.05)  # success-rate tolerance


def _cache_stats_path() -> str:
    return os.path.join(os.path.expanduser("~"), ".nx", "cache_stats.json")


def _load_cache_stats() -> None:
    """Seed the in-process counters (global + per-provider ledger) from the
    persisted file at import (best-effort) — so the numbers STICK across restart."""
    try:
        with open(_cache_stats_path(), encoding="utf-8") as f:
            data = json.load(f)
        with _CACHE_LOCK:
            for k in _CACHE_KEYS:
                v = data.get(k)
                if isinstance(v, (int, float)) and v >= 0:
                    _CACHE_STATS[k] = int(v)
            by_prov = data.get("by_provider")
            if isinstance(by_prov, dict):
                for prov, d in by_prov.items():
                    if not isinstance(d, dict):
                        continue
                    slot = _PROV_STATS.setdefault(prov, {k: 0 for k in _PROV_KEYS})
                    for k in _PROV_KEYS:
                        v = d.get(k)
                        if isinstance(v, (int, float)) and v >= 0:
                            slot[k] = int(v)
    except Exception:
        pass


def _persist_cache_stats() -> None:
    """Atomically write the counters (global + per-provider) to disk (best-effort; never raises)."""
    try:
        p = _cache_stats_path()
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with _CACHE_LOCK:
            snap = dict(_CACHE_STATS)
            snap["by_provider"] = {prov: dict(d) for prov, d in _PROV_STATS.items()}
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(snap, f)
        os.replace(tmp, p)
    except Exception:
        pass


def _to_int(v) -> int:
    """Floor any provider-supplied usage value at 0 (None / negatives / garbage → 0)."""
    try:
        return max(0, int(v or 0))
    except (TypeError, ValueError):
        return 0


def record_usage(prompt_tokens=0, cached_tokens=0, completion_tokens=0, provider=None,
                 local_prompt_tokens=0) -> None:
    """Record ONE turn's token usage for cache-hit-rate measurement AND the
    per-provider cost-tuner ledger. The streaming layer calls this when the
    provider returns a `usage` object (requires stream_options.include_usage).
    Thread-safe, best-effort, side-effect-free on the request: any failure is
    swallowed. `cached_tokens` is 0 when the provider doesn't report
    prompt_tokens_details.cached_tokens — an honest miss, never a fabricated hit.
    Negative/garbage values are floored at 0. `provider`, when given, feeds the
    autonomous split decision; `local_prompt_tokens` is OUR independent estimate
    of the prompt we sent, kept so the tuner can cross-check the provider's
    self-reported numbers instead of trusting them blindly."""
    pt, ct, cp = _to_int(prompt_tokens), _to_int(cached_tokens), _to_int(completion_tokens)
    lp = _to_int(local_prompt_tokens)
    try:
        with _CACHE_LOCK:
            _CACHE_STATS["requests"] += 1
            _CACHE_STATS["prompt_tokens"] += pt
            _CACHE_STATS["cached_tokens"] += ct
            _CACHE_STATS["completion_tokens"] += cp
            if provider:
                d = _PROV_STATS.setdefault(provider, {k: 0 for k in _PROV_KEYS})
                d["requests"] += 1
                d["prompt_tokens"] += pt
                d["cached_tokens"] += ct
                d["completion_tokens"] += cp
                d["local_prompt"] += lp
    except Exception:
        return
    _persist_cache_stats()


def record_provider_failure(provider) -> None:
    """Record a failed attempt against a provider — the HEALTH signal the tuner
    uses so it never shifts bulk traffic onto a provider that's failing more.
    Best-effort; never raises."""
    if not provider:
        return
    try:
        with _CACHE_LOCK:
            d = _PROV_STATS.setdefault(provider, {k: 0 for k in _PROV_KEYS})
            d["failures"] += 1
    except Exception:
        return
    _persist_cache_stats()


def cache_stats() -> dict:
    """Snapshot of cumulative usage + the derived `cache_hit_rate` (cached/prompt,
    0..1) and `output_ratio` (completion/prompt). Both are None until at least one
    request has reported prompt tokens — a rate is never fabricated as 0.0 before
    any data exists."""
    with _CACHE_LOCK:
        s = dict(_CACHE_STATS)
    pt = s["prompt_tokens"]
    s["cache_hit_rate"] = (s["cached_tokens"] / pt) if pt > 0 else None
    s["output_ratio"] = (s["completion_tokens"] / pt) if pt > 0 else None
    return s


def reset_cache_stats() -> None:
    """Zero the counters (global + per-provider ledger, in-process AND persisted) —
    start a fresh measurement window."""
    with _CACHE_LOCK:
        for k in _CACHE_KEYS:
            _CACHE_STATS[k] = 0
        _PROV_STATS.clear()
        _TUNE_COUNTER[0] = 0
    _persist_cache_stats()


# ─── the autonomous brain: measure → decide → apply ──────────────────────────
# How far a provider's SELF-REPORTED prompt tokens may fall below OUR local estimate
# before we stop trusting its frame. Under-reporting prompt (or over-reporting cached)
# makes a provider look cheaper; beyond this ratio we bill it on the local estimate and
# flag it suspect, so it can't earn traffic by gaming its own numbers.
_TUNER_REPORT_TRUST = float(os.environ.get("NX_TUNER_REPORT_TRUST", "0.7") or 0.7)


def _suspect_report(d: dict) -> bool:
    """True when a provider reports far fewer prompt tokens than our independent local
    estimate — i.e. its usage frame can't be trusted for cost ranking. Needs a local
    yardstick with real magnitude before it can flag (avoids noise on tiny samples)."""
    reported, local = d.get("prompt_tokens", 0), d.get("local_prompt", 0)
    if local < 2000:            # not enough independent signal yet
        return False
    return reported < local * _TUNER_REPORT_TRUST


def _avg_cost_from(provider: str, d: dict):
    """Estimated avg $/request. Bills UNCACHED input against the LARGER of the
    provider-reported prompt and our local estimate — so a provider cannot look
    cheaper by under-reporting prompt tokens; and cached is clamped to that base so
    it can't over-discount. None when there's no rate or no requests yet."""
    r = _PROVIDER_RATES.get(provider)
    if not r or d.get("requests", 0) == 0:
        return None
    billable_in = max(d.get("prompt_tokens", 0), d.get("local_prompt", 0))   # can't shrink the bill by under-reporting
    cached = min(d.get("cached_tokens", 0), billable_in)                     # cached can't exceed real input
    uncached = max(0, billable_in - cached)
    cost = (uncached * r["in"] + cached * r["cached"]
            + d.get("completion_tokens", 0) * r["out"]) / 1_000_000.0
    return cost / d["requests"]


def _provider_view() -> dict:
    """Pure snapshot: {provider: {requests, success_rate, avg_cost, suspect}} — the
    only input plan_split needs, so the decision is a deterministic function of state."""
    with _CACHE_LOCK:
        snap = {p: dict(d) for p, d in _PROV_STATS.items()}
    view = {}
    for p, d in snap.items():
        reqs, fails = d.get("requests", 0), d.get("failures", 0)
        total = reqs + fails
        view[p] = {
            "requests": reqs,
            "success_rate": (reqs / total) if total else 1.0,
            "avg_cost": _avg_cost_from(p, d),
            "suspect": _suspect_report(d),
        }
    return view


def plan_split(primary: str, secondary: str, view: dict) -> dict:
    """PURE. Given the two providers and a stats snapshot, return integer weights
    {primary: w, secondary: w} summing to 100 — how NX splits the NEXT window of
    traffic. Deterministic and fully unit-testable (see test_routing):
      • too little data on either side → EXPLORE (gather the comparison)
      • secondary's usage frame is SUSPECT (self-report diverges from our local
        estimate) → FLOOR it (never reward a provider gaming its own numbers)
      • secondary failing more than tolerance → FLOOR it (health gate)
      • secondary cheaper AND healthy AND trusted → shift up to MAX_SHADOW (optimize)
      • secondary not cheaper (or cost unknown) → keep majority primary, keep exploring
    Never returns 100/0 — a floor keeps re-checking so a later drift is caught."""
    p = view.get(primary, {})
    s = view.get(secondary, {})
    if s.get("requests", 0) < _TUNER_MIN_SAMPLE or p.get("requests", 0) < _TUNER_MIN_SAMPLE:
        return {primary: 100 - _TUNER_EXPLORE, secondary: _TUNER_EXPLORE}
    if s.get("suspect"):
        return {primary: 100 - _TUNER_FLOOR, secondary: _TUNER_FLOOR}
    if s.get("success_rate", 1.0) < p.get("success_rate", 1.0) - _TUNER_HEALTH_TOL:
        return {primary: 100 - _TUNER_FLOOR, secondary: _TUNER_FLOOR}
    sc, pc = s.get("avg_cost"), p.get("avg_cost")
    if sc is not None and pc is not None and sc < pc:
        return {primary: 100 - _TUNER_MAX_SHADOW, secondary: _TUNER_MAX_SHADOW}
    return {primary: 100 - _TUNER_EXPLORE, secondary: _TUNER_EXPLORE}


def _tuner_enabled() -> bool:
    """Autonomous by default. NX_TUNER=off (or 0/false/no) is the kill switch."""
    return os.environ.get("NX_TUNER", "on").strip().lower() not in ("0", "off", "false", "no", "")


def _tuner_pick(primary: str, secondary: str) -> str:
    """Apply the current split deterministically: the first `secondary_weight` of
    every 100-request window go to the secondary. No RNG → reproducible + testable."""
    split = plan_split(primary, secondary, _provider_view())
    with _CACHE_LOCK:
        n = _TUNE_COUNTER[0]
        _TUNE_COUNTER[0] = (n + 1) % 100
    return secondary if (n % 100) < split.get(secondary, 0) else primary


def _resolve_active_provider() -> tuple:
    """Provider resolution WITH the autonomous tuner. When both the primary
    and secondary provider keys are configured and the tuner is
    on, the split decides which serves this turn. Otherwise (0/1 eligible key, or
    tuner off) fall back to the static preference order — behaviour is unchanged,
    so no-key/single-key setups and every existing test route exactly as before."""
    if _tuner_enabled():
        fw = get_fireworks_key()
        di = get_deepinfra_key()
        if fw and di:
            chosen = _tuner_pick(P["fireworks"], P["fallback"])
            if chosen == P["fallback"]:
                return P["fallback"], di, -1
            return P["fireworks"], fw, -1
    return _resolve_provider_credentials()


def provider_recommendation(primary: str = None, secondary: str = None) -> dict:
    """The autonomous decision + the numbers behind it, for display (/cache).
    Reports the live split NX is applying and each provider's measured cost/health."""
    primary = primary or P["fireworks"]
    secondary = secondary or P["fallback"]
    view = _provider_view()
    split = plan_split(primary, secondary, view)
    p, s = view.get(primary, {}), view.get(secondary, {})
    return {
        "enabled": _tuner_enabled(),
        "primary": primary, "secondary": secondary,
        "split": split,
        "primary_reqs": p.get("requests", 0), "secondary_reqs": s.get("requests", 0),
        "primary_avg_cost": p.get("avg_cost"), "secondary_avg_cost": s.get("avg_cost"),
        "primary_health": p.get("success_rate"), "secondary_health": s.get("success_rate"),
        "primary_suspect": p.get("suspect", False), "secondary_suspect": s.get("suspect", False),
        "min_sample": _TUNER_MIN_SAMPLE,
        "rates_asof": _RATES_ASOF,
    }


_load_cache_stats()


# Provider order (0.3.96+): primary → secondary → legacy pool → aggregator → final fallback.
# The primary provider runs the bulk; the secondary is the next-tier fallback (different
# model-id namespace, so TIERS swaps the model set when the secondary resolves);
# the legacy pooled provider's 6-key pool is preserved as deep fallback for incident resilience.
PRIMARY_PROVIDER = P["fireworks"]
SECONDARY_PROVIDER = P["fallback"]    # the secondary provider
TERTIARY_PROVIDER = P["primary"]      # the legacy pooled provider


# ─── tier registry, per-provider ─────────────────────────────────────────────
# Tier semantics are identical across providers; only the model-id strings
# differ. TIERS_BY_PROVIDER[resolved_provider] returns the right set. Models
# referenced through FW / M dicts — never literal slash-paths here.
#
# Why two registries instead of one with provider-agnostic aliases:
# the primary and secondary providers use disjoint catalog-name conventions for the
# same underlying model. The resolved provider decides which dict to read.

# ── per-tier generation ceiling (explicit max_tokens) ────────────────────────
# Every tier now carries an EXPLICIT max_tokens ceiling instead of falling
# through to stream_chat's silent 4096 default. Two forces, opposite directions:
#   • COST — the high-VOLUME chat tiers (flash / frontier) stay tightly bounded.
#     Output tokens are the single biggest line-item (the code-tier model's output
#     is 4x its input; the frontier model's "high"-effort reasoning is otherwise
#     unbounded), so a runaway reasoning trace on the tiers that run most turns
#     can't sprawl to the context limit. This is the "cap the thinking budget"
#     lever, expressed as the generation ceiling the chat-completions-compatible
#     providers actually honor (they don't split hidden-reasoning tokens from
#     answer tokens in the API — `reasoning_effort` is the only qualitative knob,
#     `max_tokens` the ceiling).
#   • CORRECTNESS — the code / agentic tiers produce DIFFS and multi-step plans.
#     The old silent 4096 could TRUNCATE a large multi-file patch mid-file (a
#     latent write-corruption bug). They get a diff-safe ceiling so a generated
#     diff or plan is never cut off. Low-volume tiers, so the cost is marginal.
_MAXTOK_FLASH    = 700      # conversational — 3-4 sentences or a short list
_MAXTOK_FRONTIER = 4096     # a deep reasoning answer (~3k words) — bounded for cost
_MAXTOK_COUNCIL  = 6144     # multi-model deliberation needs a little more room
_MAXTOK_CODE     = 16384    # a multi-file diff must NEVER truncate mid-patch
_MAXTOK_AGENTIC  = 16384    # long-horizon orchestration output
_MAXTOK_FALLBACK = 8192     # last-resort single-model providers serve every tier

_TIERS_FIREWORKS = {
    "flash": {
        "primary":  FW["fast"],
        "secondary": FW["fast"],
        "provider": P["fireworks"],
        "reasoning_effort": "low",
        # Cap flash generation — conversational answers are 3-4 sentences (or a
        # short list); bounding tokens keeps worst-case latency tight and
        # reinforces brevity. The highest-volume tier — kept tightest.
        "extra_body": {"max_tokens": _MAXTOK_FLASH},
    },
    "frontier": {
        "primary":  FW["pro"],
        "secondary": FW["fast"],
        "provider": P["fireworks"],
        "reasoning_effort": "high",
        # The frontier model is the biggest cost line-item — bound it explicitly
        # (was the silent 4096). A deep strategy/finance answer fits in ~4k tokens.
        "extra_body": {"max_tokens": _MAXTOK_FRONTIER},
    },
    "agentic": {
        "primary":  FW["kimi_code"],
        "secondary": FW["pro"],
        "provider": P["fireworks"],
        "reasoning_effort": "high",
        "extra_body": {"max_tokens": _MAXTOK_AGENTIC},
    },
    "code": {
        "primary":  FW["kimi_code"],
        # NO silent downgrade: a coding turn produces a diff and can push, so its fallback must stay a CAPABLE
        # model — never the cheap chat/flash model. Secondary is the frontier reasoning model, not FW["fast"].
        # (Invariant: the code lane never silently serves from a weaker chat model. See test_routing.)
        "secondary": FW["pro"],
        "provider": P["fireworks"],
        "reasoning_effort": "high",
        # Diff-safe ceiling — a multi-file patch at the old silent 4096 could be
        # cut off mid-file (write corruption). Raised so a diff never truncates.
        "extra_body": {"max_tokens": _MAXTOK_CODE},
    },
    "council": {
        "primary":  FW["pro"],
        "secondary": FW["kimi"],
        "provider": P["fireworks"],
        "reasoning_effort": "high",
        "extra_body": {"max_tokens": _MAXTOK_COUNCIL},
    },
}

_TIERS_DEEPINFRA = {
    "flash":    {"primary": MR["fast"],      "secondary": MR["small"], "provider": P["fallback"], "reasoning_effort": "low",  "extra_body": {"max_tokens": _MAXTOK_FLASH}},
    "frontier": {"primary": MR["pro"],       "secondary": MR["fast"],  "provider": P["fallback"], "reasoning_effort": "high", "extra_body": {"max_tokens": _MAXTOK_FRONTIER}},
    "agentic":  {"primary": MR["code_kimi"], "secondary": MR["pro"],   "provider": P["fallback"], "reasoning_effort": "high", "extra_body": {"max_tokens": _MAXTOK_AGENTIC}},
    "code":     {"primary": MR["code_kimi"], "secondary": MR["pro"],   "provider": P["fallback"], "reasoning_effort": "high", "extra_body": {"max_tokens": _MAXTOK_CODE}},  # no silent chat-model downgrade + diff-safe ceiling (see test_routing)
    "council":  {"primary": MR["pro"],       "secondary": MR["peer"],  "provider": P["fallback"], "reasoning_effort": "high", "extra_body": {"max_tokens": _MAXTOK_COUNCIL}},
}

# Aggregator / final-fallback last-resort registries — every tier maps to that
# provider's single fallback model so route() returns a COHERENT (provider,
# model) pair when the chain falls all the way through. Without these, a
# resolved aggregator/final-fallback provider would silently inherit the primary
# provider's model ids it can't serve.
_one_model = lambda mdl, prov: {
    t: {"primary": mdl, "secondary": mdl, "provider": prov,
        # Last-resort providers serve every tier from one model, so a code turn
        # can land here — give it a diff-safe ceiling, not the tight flash cap.
        "reasoning_effort": "medium", "extra_body": {"max_tokens": _MAXTOK_FALLBACK}}
    for t in ("flash", "frontier", "agentic", "code", "council")
}
_TIERS_OPENROUTER = _one_model(OR_FALLBACK, P["openrouter"])
_TIERS_OPENAI     = _one_model(OAI_FALLBACK, P["openai"])

# The legacy pooled provider serves its own namespace models. Map every tier to
# the coordinator model id (the only legacy-pool-namespace model in the registry),
# so a legacy-pool-resolved request gets an id that provider can actually serve.
_TIERS_NVIDIA = _one_model(MR["coord"], P["primary"])

# ── NATIVE raw-price tier maps (0.4+) ────────────────────────────────────────
# Read the native model ids at CALL time (env-overridable), so setting e.g.
# NX_QWEN_MODEL_MAX=qwen3.8-max-preview takes effect with no code edit.
def _qwen_max() -> str:   return (os.environ.get("NX_QWEN_MODEL_MAX") or NATIVE["qwen_max"]).strip()
def _ds_chat() -> str:    return (os.environ.get("NX_DEEPSEEK_MODEL_CHAT") or NATIVE["ds_chat"]).strip()
def _ds_reason() -> str:  return (os.environ.get("NX_DEEPSEEK_MODEL_REASONER") or NATIVE["ds_reason"]).strip()
def _dashscope_key() -> str: return (os.environ.get(ENV["dashscope_api_key"], "") or "").strip()
def _deepseek_key() -> str:  return (os.environ.get(ENV["deepseek_api_key"], "") or "").strip()

# DeepSeek serves the light/reasoning tiers; DashScope (Qwen) serves the heavy tier. These maps exist so a resolved
# native provider always has a coherent tier set (the import-time invariant) — the tier-aware LEAD is picked in
# route() via _native_override, but if a native provider is ever the resolved provider it serves a sane model.
_TIERS_DEEPSEEK = {
    "flash":    {"primary": _ds_chat(),   "secondary": _ds_chat(),   "provider": P["deepseek"], "reasoning_effort": "low",  "extra_body": {"max_tokens": _MAXTOK_FLASH}},
    "frontier": {"primary": _ds_reason(), "secondary": _ds_chat(),   "provider": P["deepseek"], "reasoning_effort": "high", "extra_body": {"max_tokens": _MAXTOK_FRONTIER}},
    "agentic":  {"primary": _ds_reason(), "secondary": _ds_chat(),   "provider": P["deepseek"], "reasoning_effort": "high", "extra_body": {"max_tokens": _MAXTOK_AGENTIC}},
    "code":     {"primary": _ds_chat(),   "secondary": _ds_reason(), "provider": P["deepseek"], "reasoning_effort": "high", "extra_body": {"max_tokens": _MAXTOK_CODE}},
    "council":  {"primary": _ds_reason(), "secondary": _ds_chat(),   "provider": P["deepseek"], "reasoning_effort": "high", "extra_body": {"max_tokens": _MAXTOK_COUNCIL}},
}
_TIERS_DASHSCOPE = _one_model(_qwen_max(), P["dashscope"])  # Qwen serves every tier if it resolves; leads heavy via _native_override

TIERS_BY_PROVIDER = {
    P["fireworks"]:  _TIERS_FIREWORKS,
    P["fallback"]:   _TIERS_DEEPINFRA,
    P["primary"]:    _TIERS_NVIDIA,
    P["openrouter"]: _TIERS_OPENROUTER,
    P["openai"]:     _TIERS_OPENAI,
    P["deepseek"]:   _TIERS_DEEPSEEK,
    P["dashscope"]:  _TIERS_DASHSCOPE,
}

# Import-time invariant: every provider NX can resolve to MUST have a tier set,
# so route() never silently serves a wrong-namespace model id.
assert set(P.values()).issubset(set(TIERS_BY_PROVIDER.keys())), (
    "TIERS_BY_PROVIDER is missing a provider from P — a resolved provider "
    "would inherit the wrong model namespace."
)

# `TIERS` is the PRIMARY-provider reference set, exposed for
# callers that only need the per-tier shape (reasoning_effort / extra_body),
# which is identical across provider sets. Callers that need the resolved
# MODEL ID for a specific provider must read TIERS_BY_PROVIDER[result.provider]
# or result.model — never TIERS[...]['primary'] — so there is no stale-model
# hazard here. Frozen so it can't be mutated at runtime.
from types import MappingProxyType as _FrozenT
TIERS = _FrozenT(_TIERS_FIREWORKS)


# ─── world → tier mapping ────────────────────────────────────────────────────
# Direct: no scenario layer. Tier IS the routing key.
# `default_voice` is the internal slot name; its value is now one of the canonical
# MODE_POSTURES (PARTNER · AUTOPILOT · STUDY · REFINE). Tiers are untouched.
# Heuristic: research/knowledge/onboarding default to STUDY (source-grounded),
# execution/coding/pipeline worlds to AUTOPILOT (handle-it), the rest to PARTNER
# (think-it-through). REFINE is user-invoked (no world defaults to it).
WORLD_CONFIG = {
    # High-value worlds — depth matters → frontier
    "strategy":   {"tier": "frontier", "default_voice": "PARTNER"},
    "finance":    {"tier": "frontier", "default_voice": "PARTNER"},
    "legal":      {"tier": "frontier", "default_voice": "PARTNER"},
    "compliance": {"tier": "frontier", "default_voice": "PARTNER"},
    "research":   {"tier": "frontier", "default_voice": "STUDY"},
    "product":    {"tier": "frontier", "default_voice": "PARTNER"},
    "people":     {"tier": "flash", "default_voice": "PARTNER"},   # alias of canonical "hr" — routes as hr (flash)

    # Execution + cheap-volume worlds → flash (escalates on signals)
    "cowork":     {"tier": "flash", "default_voice": "PARTNER"},
    "ops":        {"tier": "flash", "default_voice": "AUTOPILOT"},
    "support":    {"tier": "flash", "default_voice": "AUTOPILOT"},
    "hr":         {"tier": "flash", "default_voice": "PARTNER"},
    "onboarding": {"tier": "flash", "default_voice": "STUDY"},
    "sales":      {"tier": "flash", "default_voice": "AUTOPILOT"},
    "marketing":  {"tier": "flash", "default_voice": "PARTNER"},
    "growth":     {"tier": "flash", "default_voice": "PARTNER"},

    # Coding worlds → code tier (the code-tier model)
    "code":       {"tier": "code", "default_voice": "AUTOPILOT"},
    "nx-code":    {"tier": "code", "default_voice": "AUTOPILOT"},
    "devops":     {"tier": "code", "default_voice": "AUTOPILOT"},

    # Agentic / long-horizon orchestration
    "nx-1":       {"tier": "agentic", "default_voice": "PARTNER"},
    "agents":     {"tier": "agentic", "default_voice": "PARTNER"},

    # Worlds referenced by NX_WORLD_CONTEXT / MCP registry — registered here
    # so they route to a real tier instead of silently falling back to cowork.
    "recruiting": {"tier": "frontier", "default_voice": "PARTNER"},
    "knowledge":  {"tier": "frontier", "default_voice": "STUDY"},
    "brand":      {"tier": "flash",    "default_voice": "PARTNER"},
    "customers":  {"tier": "frontier", "default_voice": "AUTOPILOT"},  # alias of "customers-and-partners" — routes as it (frontier)
    # Lead qualification is decision-making (cohort analysis, buyer-signal reading,
    # pipeline-fit) — frontier tier, not the cheapest flash model.
    "leads":      {"tier": "frontier", "default_voice": "AUTOPILOT"},
    "lead":       {"tier": "frontier", "default_voice": "AUTOPILOT"},  # singular alias of "leads"
    # CRM is data-hygiene + relationship-history judgment, same depth bar as leads.
    "crm":        {"tier": "frontier", "default_voice": "AUTOPILOT"},
    # Capital origination/underwriting is high-stakes financial judgment —
    # same depth bar as finance/strategy; PARTNER (drafts for review, never the
    # one who sends or signs — see NX_WORLD_CONTEXT["capital"]).
    "capital":    {"tier": "frontier", "default_voice": "PARTNER"},

    # ── Canonical reconciliation (worlds.canonical.json) — the CLI adopts the web WorldId taxonomy as the
    #    single source of truth. These are the canonical worlds the CLI was missing; the pre-existing keys above
    #    (ops/lead/leads/strategy/customers/crm/people/nx-1/nx-code) are retained as ALIASES of these. Additive:
    #    no existing world's tier changed. Pinned against the manifest by tests/test_worlds_canonical.py.
    "lead-gen":               {"tier": "frontier", "default_voice": "AUTOPILOT"},
    "seo":                    {"tier": "flash",    "default_voice": "AUTOPILOT"},
    "social":                 {"tier": "flash",    "default_voice": "PARTNER"},
    "analytics":              {"tier": "frontier", "default_voice": "STUDY"},
    "customers-and-partners": {"tier": "frontier", "default_voice": "AUTOPILOT"},
    "data-privacy-security":  {"tier": "frontier", "default_voice": "PARTNER"},
    "operations":             {"tier": "flash",    "default_voice": "AUTOPILOT"},
    "procurement":            {"tier": "flash",    "default_voice": "AUTOPILOT"},
    "product-offer":          {"tier": "frontier", "default_voice": "PARTNER"},
    "design":                 {"tier": "flash",    "default_voice": "PARTNER"},
    "strategic-intelligence": {"tier": "frontier", "default_voice": "PARTNER"},
    "study":                  {"tier": "frontier", "default_voice": "STUDY"},
    "personal":               {"tier": "flash",    "default_voice": "AUTOPILOT"},
}


def assert_world_registries_consistent() -> list:
    """Return the list of worlds present in NX_WORLD_CONTEXT (nx_prompts) but
    MISSING from WORLD_CONFIG — i.e. worlds that would silently fall back to
    cowork/flash. Called at import for an early warning; returns [] when in
    sync. Kept non-fatal so a drift never crashes startup, but surfaced so the
    next person adding a world sees it immediately."""
    try:
        from nx_prompts import NX_WORLD_CONTEXT
        missing = [w for w in NX_WORLD_CONTEXT if w not in WORLD_CONFIG]
        return missing
    except Exception:
        return []


# ─── voice persona triggers (unchanged from 0.3.94) ──────────────────────────
# Auto-shift keys are now MODE_POSTURES. PARTNER is the default (no triggers — it is
# what a turn falls through to). Only STUDY / REFINE / AUTOPILOT pull a turn AWAY
# from the world default when the intent is unmistakable.
VOICE_SHIFT_TRIGGERS = {
    # STUDY — "help me understand / prove it": learning + evidence intent
    "STUDY": [
        "how does", "why does", "what is", "explain", "i dont understand",
        "can you walk me through", "whats the difference", "help me understand",
        "cite", "the source", "according to", "prove it", "the evidence",
    ],
    # REFINE — "make this better": sharpen an existing draft
    "REFINE": [
        "polish", "tighten", "sharpen", "make it better", "improve the",
        "rewrite", "edit this", "punch it up", "cut it down", "make this cleaner",
        "wordsmith", "proofread",
    ],
    # AUTOPILOT — "just handle it": execution intent
    "AUTOPILOT": [
        "do it", "execute", "run", "build", "create", "write", "generate",
        "make", "set up", "implement", "ship", "handle it", "just go",
    ],
}


# ─── escalation: flash → frontier when the input earns it ────────────────────
#
# Word-boundary keyword match so "plan" doesn't fire on "plant" or "planet".
# Triggers ONLY on flash-tier worlds; code/agentic/council are unaffected.
_ESCALATION_KEYWORDS = (
    "analyze", "strategy", "forecast", "model", "plan",
    "compare", "evaluate", "tradeoff", "decision",
)
_ESCALATION_KEYWORD_RE = re.compile(
    r"\b(" + "|".join(_ESCALATION_KEYWORDS) + r")\b",
    re.IGNORECASE,
)
_ESCALATION_LEN_THRESHOLD = 500
_COUNCIL_PREFIX = "$council"
# Detects low-signal padding: the same word repeated 5+ times in a row
# ("and and and …", "a a a …"). Length-based escalation ignores input whose
# length comes from this kind of repetition rather than real content.
_REPETITION_RE = re.compile(r"\b(\w+)\b(?:\s+\1\b){4,}", re.IGNORECASE)


def needs_escalation(user_input: str) -> bool:
    """True if a flash-tier request should escalate to frontier.

    Length escalation is gated on SIGNAL, not raw character count: an input
    padded with repeated tokens (which inflates length without adding meaning)
    does not escalate. Keyword escalation always applies.
    """
    if not user_input:
        return False
    if _ESCALATION_KEYWORD_RE.search(user_input):
        return True
    if len(user_input) > _ESCALATION_LEN_THRESHOLD:
        # Only escalate on length when the input has real lexical diversity —
        # not when its length is repetition padding.
        deduped = _REPETITION_RE.sub(r"\1", user_input)
        unique_words = len(set(w.lower() for w in re.findall(r"\w+", deduped)))
        if len(deduped) > _ESCALATION_LEN_THRESHOLD and unique_words >= 30:
            return True
    return False


def is_council_request(user_input: str) -> bool:
    """True if the input opens with $council (case-insensitive)."""
    if not user_input:
        return False
    return user_input.lstrip().lower().startswith(_COUNCIL_PREFIX)


# ── operator effort ladder (/effort · the web effort bar) ────────────────────
# The 5 operator-facing effort stops → (tier, reasoning_effort). Kept BYTE-IDENTICAL to the web effort map
# (lib/llm/nx-router.ts EFFORT_TIERS) so the CLI /effort command and the web bar never drift (one canonical
# ladder). CODING ALWAYS stays on the code tier regardless of stop (→ Qwen 3.8 Max when its key is set, else the
# meantime Kimi 2.6/7 lane) — the stop then only sets the reasoning depth on code turns. 'council' is the top stop → the multi-model
# Qwen×DeepSeek debate. When no stop is set the routing is byte-identical to before (zero regression).
_EFFORT_TIERS = {
    "low":     ("flash",    "low"),
    "mid":     ("frontier", "medium"),
    "high":    ("frontier", "high"),
    "extra":   ("agentic",  "high"),
    "council": ("council",  "high"),
}
_EFFORT_ALIASES = {"med": "mid", "medium": "mid", "max": "council", "ultra": "council", "ultracode": "council"}


def normalize_effort(raw) -> Optional[str]:
    """Canonical effort stop (low|mid|high|extra|council) or None. Tolerates a leading / or $ and common aliases
    (/med→mid, /max/$max→council). Unknown → None (caller keeps auto-routing)."""
    if not raw:
        return None
    e = str(raw).strip().lstrip("/$").lower()
    e = _EFFORT_ALIASES.get(e, e)
    return e if e in _EFFORT_TIERS else None


# ── code-tier effort split (Victor-set) ──────────────────────────────────────
# The code tier picks its model by TASK WEIGHT: light coding → the fast code-tier
# model (cheap, the bulk of turns); heavy/complex → the frontier reasoning model;
# the rare HUGE job → both in tandem (draft+review — Phase 2). Deterministic, no
# extra model call.
#   HEAVY  = an architectural / multi-file verb, OR a long lexically-rich prompt.
#   HUGE   = a heavy verb AND a whole-repo scope stacked (targets ~<=10% of turns).
_CODE_HEAVY_RE = re.compile(
    r"\b(refactor|re-?architect|architect|redesign|re-?design|migrat(?:e|ion)|overhaul|"
    r"rewrite|re-?write|port(?:ing)?|scaffold|bootstrap|implement\s+the\s+\w+\s+system|"
    r"build\s+(?:me\s+)?(?:a|an|the)\s+\w+\s+(?:app|service|system|pipeline|backend|frontend)|"
    r"end.to.end|multi.?file|the\s+full\s+(?:stack|app|system))\b",
    re.I)
_CODE_HUGE_RE = re.compile(
    r"\b(whole|entire|full|across\s+the|every\s+file\s+in)\s+(?:the\s+)?(?:repo|repository|"
    r"codebase|code\s?base|project|app|system|stack)\b",
    re.I)


def _code_effort(user_input: str) -> str:
    """Which code model a coding turn should use: 'light' | 'heavy' | 'huge'.
    light → the fast code-tier model (bulk); heavy → the frontier reasoning model;
    huge → tandem (both)."""
    t = user_input or ""
    huge_scope = bool(_CODE_HUGE_RE.search(t))
    heavy = bool(_CODE_HEAVY_RE.search(t)) or len(t) > 600
    if huge_scope and heavy:
        return "huge"       # heaviest signals stacked — the rare big job
    if heavy or huge_scope:
        return "heavy"      # the frontier reasoning model
    return "light"          # the fast code-tier model — fast/cheap, the default coding lane


@dataclass
class RouteResult:
    world: str
    tier: str
    model: str
    voice: str
    provider: str
    api_key: str
    slot_index: int
    extra_body: dict = field(default_factory=dict)
    reasoning_effort: str = "medium"
    secondary_model: str = ""
    # The resolved per-tier generation ceiling (extra_body["max_tokens"]), lifted
    # to a first-class field so callers/telemetry can read the cap without digging
    # into extra_body. None only if a tier somehow carries no ceiling.
    max_output_tokens: Optional[int] = None


def detect_voice_shift(user_input: str, default_voice: str, world: str) -> str:
    """
    Detect if user input triggers a voice mode shift.
    World config sets floor — some worlds never shift (ops, legal).
    """
    locked_worlds = {"ops": "AUTOPILOT", "legal": "PARTNER"}
    if world in locked_worlds:
        return locked_worlds[world]

    text = (user_input or "").lower()
    for voice, triggers in VOICE_SHIFT_TRIGGERS.items():
        if any(trigger in text for trigger in triggers):
            return voice

    return default_voice


def _resolve_provider_credentials() -> tuple[str, str, int]:
    """
    Walk the provider preference order: primary → secondary → legacy pool →
    aggregator → final fallback. Returns (resolved_provider, api_key, slot_index).

    slot_index is the pooled-provider slot for the legacy pool; -1 for every
    single-key provider (primary / secondary / aggregator / final fallback).
    """
    # 1. Primary provider (single key from env or Keychain)
    fw_key = get_fireworks_key()
    if fw_key:
        return P["fireworks"], fw_key, -1

    # 2. Secondary provider (single key from env or Keychain)
    di_key = get_deepinfra_key()
    if di_key:
        return P["fallback"], di_key, -1

    # 3. Tertiary: the legacy pooled provider (6-slot pool). Check all_locked()
    #    BEFORE get_key() — get_key() calls slot.record_use() on whatever slot it
    #    returns (even a locked-fallback slot), so calling it first burned the
    #    per-minute counter on every request when the pool was already locked.
    try:
        pool = get_pool()
        if pool._slots and not pool.all_locked():
            api_key, slot_index = pool.get_key("anonymous")
            if api_key:
                return TERTIARY_PROVIDER, api_key, slot_index
    except Exception:
        pass

    # 4. Aggregator fallback (single key)
    or_key = os.environ.get(ENV["openrouter_api_key"], "").strip()
    if or_key:
        return P["openrouter"], or_key, -1

    # 5. Final fallback (single key, last resort)
    oai_key = os.environ.get(ENV["openai_api_key"], "").strip()
    if oai_key:
        return P["openai"], oai_key, -1

    return PRIMARY_PROVIDER, "", -1


def _native_override(tier: str, user_input: str):
    """Native raw-price LEAD for a tier when its key is set (0.4+). Returns
    (provider, model, secondary, api_key, reasoning_effort, extra_body) or None.

    Qwen (DashScope) leads the HEAVY tier — agentic + heavy/huge coding + long turns. DeepSeek native leads flash
    CHAT + deep reasoning (frontier/council) + light coding QUERIES. No native key ⇒ None ⇒ the existing
    Fireworks → DeepInfra chain is byte-identical (zero regression). Model ids are env-overridable (call-time)."""
    qw = _dashscope_key()
    ds = _deepseek_key()
    if tier == "agentic" and qw:
        return (P["dashscope"], _qwen_max(), (_ds_reason() if ds else _qwen_max()), qw, "high", {"max_tokens": _MAXTOK_AGENTIC})
    if tier == "code":
        # Coding lead = Qwen 3.8 Max the moment its DashScope key is set (light, heavy, and audit/review — every
        # coding turn). No Qwen key ⇒ None ⇒ the MEANTIME Kimi 2.6/7 code lane in route() stands (Qwen 3.8 hasn't
        # released yet; Fireworks/DeepInfra falls back). Casual chat never reaches here — the code tier downgrades
        # to flash for non-coding input in route() BEFORE this. Flip Qwen on later = set the key, nothing else.
        if qw:
            return (P["dashscope"], _qwen_max(), (_ds_reason() if ds else _qwen_max()), qw, "high", {"max_tokens": _MAXTOK_CODE})
        return None
    if tier == "flash" and ds:
        return (P["deepseek"], _ds_chat(), _ds_chat(), ds, "low", {"max_tokens": _MAXTOK_FLASH})
    # frontier = deep reasoning → DeepSeek-V4-Pro. council = the MAX partnership (Qwen × DeepSeek-Pro) — the model
    # PAIR is composed in nx_council.py; here the single-model native lead for a council turn is the pro reasoner.
    if tier in ("frontier", "council") and ds:
        return (P["deepseek"], _ds_reason(), _ds_reason(), ds, "high", {"max_tokens": _MAXTOK_FRONTIER if tier == "frontier" else _MAXTOK_COUNCIL})
    return None


# Coding-vs-casual gate (deterministic, no model call): does the message actually involve code/coding? Code fences,
# file extensions, coding verbs/nouns (incl. "audit"/"review"), or code punctuation ⇒ coding (→ Qwen). Otherwise a
# casual chat/talk turn (→ flash / DeepSeek Flash), even on a code-tier world / the code page.
_CODING_RE = re.compile(
    r"```|\b(code|coding|codebase|function|func|class|method|variable|const|api|endpoint|route|"
    r"bug|debug|error|exception|stack\s?trace|traceback|refactor|implement|compile|deploy|"
    r"migrat|schema|query|regex|import|module|package|dependency|npm|pip|cargo|git|repo|repository|"
    r"commit|branch|merge|test|unit\s?test|lint|typecheck|build|type\s?error|"
    r"typescript|javascript|python|rust|golang|\bgo\b|java|kotlin|swift|ruby|php|sql|css|html|react|vue|node|"
    r"audit|review)\b"
    r"|\.(py|js|ts|tsx|jsx|go|rs|java|rb|php|c|cc|cpp|h|hpp|cs|css|scss|html|json|ya?ml|toml|sql|sh|swift|kt)\b"
    r"|[{}();=<>]|=>|::|->",
    re.I,
)


def involves_coding(user_input: str) -> bool:
    """True if the message is about code/coding (incl. auditing/reviewing code). Casual chat/talk → False."""
    return bool(user_input and _CODING_RE.search(user_input))


def route(
    world: str,
    user_input: str,
    user_id: str = "anonymous",
    override_voice: Optional[str] = None,
    prefer_primary_provider: bool = True,
    audio_parts: Optional[list] = None,
    effort_override: Optional[str] = None,
) -> RouteResult:
    """
    Main routing function. Resolves world → tier → model with escalation.

    audio_parts: optional list of chat-completions-shape `input_audio` content parts.
      When non-empty, forces tier to at-least 'frontier' and selects the
      multimodal-audio model alias (MR["glm"]). Caller is responsible for
      assembling messages[].content as a mixed text/audio array before
      invoking the provider.
    """
    del user_id, prefer_primary_provider
    requested_world = world or "cowork"
    if requested_world in WORLD_CONFIG:
        active_world = requested_world
    else:
        # Unknown world — fall back to cowork but log it so a newly-added world
        # that wasn't registered in WORLD_CONFIG doesn't silently misroute.
        active_world = "cowork"
        if requested_world and requested_world != "cowork":
            try:
                import os as _os
                _dbg = _os.path.expanduser("~/.nx/logs/debug.log")
                with open(_dbg, "a", encoding="utf-8") as _f:
                    _f.write(f"\n[routing] unknown world '{requested_world}' → cowork fallback. "
                             f"Register it in WORLD_CONFIG.\n")
            except Exception:
                pass
    config = WORLD_CONFIG.get(active_world, WORLD_CONFIG["cowork"])
    tier = config["tier"]
    default_voice = config["default_voice"]

    # ── escalation: explicit /effort stop wins, then $council prefix, then keyword/length ──
    _effort_stop = normalize_effort(effort_override)   # distinct from _code_effort()'s local _eff below
    if _effort_stop == "council" or is_council_request(user_input):
        tier = "council"
    elif _effort_stop:
        # An explicit effort stop (low|mid|high|extra). Coding ALWAYS stays on the code tier (→ Qwen); the stop
        # only re-sets reasoning depth (re-asserted after the native override). Non-coding follows the ladder tier.
        tier = "code" if involves_coding(user_input) else _EFFORT_TIERS[_effort_stop][0]
    elif tier == "flash" and needs_escalation(user_input):
        tier = "frontier"
    # Casual chat / talk (no coding) on a code-tier world → flash (cheap DeepSeek Flash), even in the code page /
    # NX CLI. Only ACTUAL coding (incl. audit/review) stays on the code tier (→ Qwen). Deterministic, no model call.
    elif tier == "code" and not involves_coding(user_input):
        tier = "flash"

    # ── resolve provider FIRST so we know which tier registry to read ───────
    # _resolve_active_provider consults the autonomous cost-tuner when both the
    # primary + secondary keys are configured; otherwise it IS the static order.
    provider, api_key, slot_index = _resolve_active_provider()
    tiers_for_provider = TIERS_BY_PROVIDER.get(provider, _TIERS_FIREWORKS)

    # ── voice multimodal override: audio in → multimodal model alias ───────
    # Only engage the audio path when there's a REAL input_audio content part,
    # and only when the resolved provider actually hosts a multimodal-audio
    # model (the primary / secondary providers). On the legacy pool / aggregator /
    # final fallback there is no multimodal-audio model in that namespace, so we
    # fall through to the normal text tier rather than emit a model id the
    # provider can't resolve.
    _has_audio = bool(audio_parts) and any(
        isinstance(p, dict) and p.get("type") == "input_audio" for p in audio_parts
    )
    _audio_capable = provider in (P["fireworks"], P["fallback"])
    if _has_audio and _audio_capable:
        # Bump to at-least frontier (audio is heavy) but NEVER downgrade an
        # already-higher tier (code/agentic/council keep their tier).
        if tier == "flash":
            tier = "frontier"
        if provider == P["fireworks"]:
            model = FW["glm"]; secondary = FW["pro"]
        else:
            model = MR["glm"]; secondary = MR["pro"]
        # Audio answers are frontier-class; give them the frontier ceiling rather
        # than an unbounded generation (was {} → the silent 4096 default).
        extra_body: dict = {"max_tokens": _MAXTOK_FRONTIER}
        reasoning_effort = "medium"
    else:
        tier_config = tiers_for_provider.get(tier, tiers_for_provider["flash"])
        model = tier_config["primary"]
        secondary = tier_config.get("secondary", "")
        # COPY — never hand out the shared registry dict; a downstream mutation
        # would corrupt the tier for every later request.
        extra_body = dict(tier_config.get("extra_body", {}))
        reasoning_effort = tier_config.get("reasoning_effort", "medium")

    # ── code tier: effort-aware model split (Victor-set) ─────────────────────
    # light coding → the fast code-tier model (fast/cheap, the bulk); heavy/complex →
    # the frontier reasoning model; the rare HUGE job → the frontier reasoning model
    # now + a fast-code-model review pass in tandem (Phase 2). All three live on the
    # secondary provider, so code turns pin there (the primary provider stays the
    # failover via the outer chain). If the secondary provider key isn't configured
    # (tests / no-key env) we keep the resolved provider's code tier — never a
    # chat-model downgrade. This overrides the cost-tuner's provider pick for code
    # turns only (low-volume, model-by-effort intent).
    if tier == "code" and not (_has_audio and _audio_capable):
        _eff = _code_effort(user_input)
        # Pin code turns to the effort-right secondary-provider model REGARDLESS of a local key:
        #   • local secondary-provider key present → direct secondary-provider call (fast).
        #   • no local key → the outer chain skips the keyless direct attempt and the Nexplora
        #     GATEWAY (which holds the secondary-provider key SERVER-SIDE) carries THIS exact
        #     model, so the fast lane works on any machine with zero local keys (Victor: "works
        #     when my computer is off"). The primary provider stays the failover in the outer
        #     chain for BYOK users.
        provider = P["fallback"]            # the secondary provider hosts the Kimi code models
        api_key = get_deepinfra_key()       # may be "" — then the gateway attempt serves it
        slot_index = -1                     # the secondary provider is single-key (no pooled-provider slot)
        # MEANTIME code lane = Kimi 2.6/7 ("how it was"), until Qwen 3.8 Max releases. The native override above
        # returns None without a DashScope key, so this Kimi default stands; the moment the Qwen key is set, Qwen
        # 3.8 Max leads and this becomes moot. DeepSeek-V4-Pro is the capable cross-family fallback (never a chat model).
        secondary = MR["pro"]
        if _eff == "light":
            model = MR["peer"]; reasoning_effort = "medium"        # Kimi K2.6 — fast bulk coding
        else:                               # heavy | huge → the coding-specialized Kimi
            model = MR["code_kimi"]; reasoning_effort = "high"     # Kimi K2.7-Code
        extra_body = dict(_TIERS_DEEPINFRA["code"].get("extra_body", {}))

    # ── NATIVE raw-price override (0.4+): the native provider LEADS its tier when its key is set. Qwen = heavy /
    # coding / long-turn; DeepSeek = flash chat + deep reasoning. Additive + ZERO-REGRESSION: no native key ⇒ a
    # no-op (routing is byte-identical to before). Never overrides the audio-multimodal path. The Fireworks →
    # DeepInfra chain remains the resilience fallback via the outer provider chain.
    if not (_has_audio and _audio_capable):
        _nat = _native_override(tier, user_input)
        if _nat:
            provider, model, secondary, api_key, reasoning_effort, extra_body = _nat
            slot_index = -1

    # ── re-assert the operator's explicit effort depth LAST ──────────────────
    # The code-effort split and the native override each set their own reasoning_effort; an explicit /effort stop
    # is the operator's deliberate choice and wins. 'council' keeps its own high-effort debate depth (handled by
    # the _council_mode dispatch), so it's excluded here. No stop set ⇒ untouched (zero regression).
    if _effort_stop and _effort_stop != "council":
        reasoning_effort = _EFFORT_TIERS[_effort_stop][1]

    if override_voice:
        # Normalize so a legacy stored value (e.g. voice_override="PEER") resolves to a
        # real posture in RouteResult.voice — not just at gate-lookup time. Keeps
        # cfg['_last_voice'] and the mode chip/menu consistent with the actual mode.
        try:
            from nx_prompts import normalize_mode as _nm
            voice = _nm(override_voice)
        except Exception:
            voice = override_voice.upper()
    else:
        voice = detect_voice_shift(user_input, default_voice, requested_world)

    try:
        get_rotator().on_request()
    except Exception:
        pass

    return RouteResult(
        world=requested_world,
        tier=tier,
        model=model,
        voice=voice,
        provider=provider,
        api_key=api_key,
        slot_index=slot_index,
        extra_body=extra_body,
        reasoning_effort=reasoning_effort,
        secondary_model=secondary,
        max_output_tokens=extra_body.get("max_tokens"),
    )
