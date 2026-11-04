"""Package-wide static constants — single source of truth for values that were
hard-coded in multiple modules.

Stdlib-free and side-effect-free. Values that are genuinely section-specific
(each store's own column tuples, per-feature timeouts used in one place, the two
differing route HTML pages) are intentionally left in their own modules.
"""
from __future__ import annotations

# --- the two databases ---
# hugpy central's own DB (worker presence, model rows, policies, admission).
DEFAULT_CORE_DSN = "dbname=hugpy_core"          # env HUGPY_CORE_DB overrides
# the call log lives in the wrapper's DB; its DSN helper is calllog_db.dsn()
# (env HUGPY_CALLLOG_DSN overrides) — kept there as the single reader-side source.

# --- this box's own front door (brain / help self-calls) ---
DEFAULT_SELF_BASE = "http://127.0.0.1:7002"     # env HUGPY_SELF_BASE overrides

# --- environment variable names (declared once) ---
ENV_CORE_DB = "HUGPY_CORE_DB"
ENV_CALLLOG_DSN = "HUGPY_CALLLOG_DSN"
ENV_SELF_BASE = "HUGPY_SELF_BASE"
ENV_BRAIN_MODEL = "HUGPY_BRAIN_MODEL"
ENV_ROUTER_URL = "HUGPY_CORE_ROUTER_URL"        # the router core takes each box's telemetry through (intake/)
ENV_ROUTER_KEY = "HUGPY_CORE_ROUTER_KEY"        # its admin key (HUGPY_ROUTER_KEY in router.env)
ENV_UI_DIST = "HUGPY_CORE_UI_DIST"           # the built console (@hugpy/ui dist/) core serves at / (web/ui.py)
ENV_CORE_SCHEMA = "HUGPY_CORE_SCHEMA"        # the Postgres SCHEMA this orbit owns in its database (install/)

# --- the per-(model, worker) PAIR KNOBS (model_workers.user_settings) ---
# The contract shared with the wrapper and the console: core's DB is the truth,
# the box holds a copy pushed through the router. ABSENT = Auto (core never
# stores a default; it pushes only what the operator set, and the box treats an
# absent knob as Auto too). These are the single source for the knob vocabulary:
# the validator (functions.validate_pair_knobs), the effective-value view
# (functions.effective_pair_settings) and the console all read them from here.
#
#   alloc_mode           placement PIN (gpu-only | ram-only | max-gpu | max-ram
#                        | explicit); absent = Auto (the ruling ladder)
#   moe                  bool: pin the MoE expert split on/off; absent = Auto
#   kv_cache_type        f16 | q8_0 | q4_0; absent = Auto (f16)
#   ctx_pct              int 1..100: pin the context window to this % of trained
#   ctx_min_pct          int 1..100: the Auto floor as a % of trained
#   ctx_range_enabled    bool: the polite-eviction context RANGE (RENAMED from
#                        ctx_range 2026-10-08 — `ctx_range` is the console's
#                        computed per-mode range object); absent = Auto
#   ctx_yield            bool: yield context under memory pressure; absent = Auto
#   ctx_restore          bool: restore the yielded context when headroom returns
#   auto_goal            quality (default) | fast
#   quality_alternatives auto (default) | none | ordered list of variant keys
#   cpu_floor_cores      int >= 1 (default 4): the CPU rungs are service-
#                        admissible only when the box's free physical cores are
#                        at least this (the operator's cliff; planner.auto_ladder)
#   max_wait_s           int >= 0 (default 120): how long a call may wait for a seat
#
# The old boolean name is accepted on input and stored under the new one; it is
# never emitted (see functions.validate_pair_knobs). The planner's own computed
# per-mode `ctx_range` objects (brain/planner.py _ctx_block) keep their name.
PAIR_KNOB_RENAMES = {"ctx_range": "ctx_range_enabled"}

# Knobs with a concrete Auto default (effective = knob else this). The ctx_* /
# alloc_mode / moe / kv_cache_type knobs have no fixed default — their Auto is
# "let the planner/box decide" (effective = the explicit value or None).
PAIR_SETTING_DEFAULTS = {

    "auto_goal": "quality",
    "quality_alternatives": "auto",
    "cpu_floor_cores": None,
    "max_wait_s": 120,
    "ctx_restore": True,
}

# Every knob the console shows, in display order. effective_pair_settings returns
# exactly these keys (explicit value, else the default above, else None = Auto).
PAIR_KNOB_KEYS = (
    "alloc_mode", "moe", "kv_cache_type",
    "spill", "attention_gpu_layers", "experts_cpu_layers", "explicit_spill", "layer_gpus",
    "gpu_model_pct", "leniency_pct", "priority_device",
    "ctx_pct", "ctx_min_pct", "ctx_range_enabled", "ctx_yield", "ctx_restore",
    "auto_goal", "tolerance", "disk_mmap", "disk_mmap_cache_gib", "min_decode_tok_s", "quality_alternatives", "cpu_floor_cores", "max_wait_s",
)

# Enums / ranges the validator enforces on SET.
AUTO_GOALS = ("quality", "fast")
# tolerance (wrapper 0.1.110, operator 2026-10-14): the FLOOR on the placement ladder —
# fast = gpu-only only; slow = + MoE split; slowest = + RAM placements; low-quality = + 4-bit
# and lower quants. When set it decides the order (soonest-occupied rung at or above it).
TOLERANCES = ("fast", "slow", "slowest", "low-quality")
QUALITY_ALTERNATIVES_MODES = ("auto", "none")
CPU_FLOOR_CORES_MIN = 1                      # cpu_floor_cores must be an int >= this
MAX_WAIT_S_MIN = 0                           # max_wait_s must be an int >= this
KV_CACHE_TYPES = ("f16", "q8_0", "q4_0")

# --- per-process GPU overheads the header estimate omits (formula sheet G3) ---
# Every GPU-resident model is one llama.cpp / torch process, and every such
# process holds a CUDA context the GGUF-header formula (fitevict.estimate.predict
# -> gguf_need) does not price. The wrapper's own fit adds the MEASURED context
# (G3), per-process driver bytes (G7) and serving growth (G8); until a fresh box
# has measured its card, the planner prices G3 with THIS STATED PRIOR so the
# Memory column is never ~300 MiB light and never silently 0 (the cell is marked
# overhead_source 'prior' until the box measures its own, then 'measured').
# A full CUDA context is ~300 MiB per process on the cards hugpy runs; ae's
# RTX 3090 measured 308,281,344 B (294 MiB) on 2026-10-08. This is a PRIOR, not a
# measurement — the only number in the planner that is not read from a fact.
CUDA_CONTEXT_PRIOR_BYTES = 300 * 1024 * 1024
