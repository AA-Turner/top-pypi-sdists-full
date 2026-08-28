"""Numeric constants + env-overridable defaults for the context optimizer.

Kept separate from ``context_optimizer.py`` so the optimizer module stays
focused on the class itself. All values here are module-level immutables;
the only logic is the small ``_env_*`` parsers, the call-time
``compaction_provider_override()`` reader, and the rate-limit classifier
(a pure helper used by the map-reduce retry loop).
"""

import os

# Auto-compaction circuit breaker — disabled after this many consecutive
# Layer 2 failures. Reset to 0 on success.
MAX_CONSECUTIVE_COMPACT_FAILURES = 3

# ---- Robust-L2 loop guards ------------------------------------------ #
# Hard caps that bound how many times any single task can fire L2. When
# any of these trip the optimizer transitions into Finalize-Only Mode
# instead of looping further. Numbers chosen against production failure
# logs (Mode-1 cases fired 5-8 compactions before the agent gave up):
# capping at 8 per task (and 2 per agno arun) preserves headroom for
# genuinely long tasks while preventing runaway loops.

# Total L2 compactions allowed across the lifetime of a single task.
MAX_COMPACTIONS_PER_TASK = 8

# Maximum L2 compactions per agno arun() turn (excluding emergency).
# Most healthy runs need 0; a single one is normal. Two means we already
# compacted, came back, and grew again — likely a loop.
MAX_COMPACTIONS_PER_ARUN = 2

# Maximum pre_retry compactions allowed for a single task. The SDK's
# plan-retry loop allows up to MAX_PLAN_RETRIES retries; without this
# cap the optimizer can fire pre_retry once per retry and produce the
# Mode-1 cascading-compaction signature.
MAX_PRE_RETRY_COMPACTIONS = 2

# Token-floor guard. After a successful L2, if estimated post-compaction
# tokens drop below this AND the action ledger shows zero new entries
# since the previous compaction, the optimizer enters Finalize-Only
# (token starvation, Mode 3 in the failure-mode catalog).
TOKEN_FLOOR_PROGRESS_GUARD = 30_000

# Stagnant-compaction guard. The token-floor guard above only fires at
# very low post-compaction tokens; this catches the orthogonal failure
# mode where tokens stay high but the action ledger does not advance
# between compactions — i.e. the LLM is looping on a tool call that
# keeps growing context without producing real progress. Production
# evidence: an orchestrator agent repeatedly called
# ``delegate_task_to_member`` with the same payload across 6 auto-
# compactions over 46 minutes; tokens never dropped below the
# token-floor threshold so no existing guard tripped.
MAX_STAGNANT_COMPACTIONS = 3
STAGNANT_COMPACTION_WARN_AT = 2

# Cross-arun repeated-tool-call guard. The per-arun stuck detector in
# the agno tool hook catches 3 identical calls in a single arun(), but
# each Layer-2 compaction restarts arun() with an empty deque, so a
# pathological loop spread across N compactions evades it. These
# thresholds operate on a task-scoped history that survives arun
# restarts and plan retries. WARN_AT injects a tool-result warning;
# MAX_REPEATED_TOOL_CALLS aborts via Finalize-Only Mode on the next
# identical call.
# Chunked writes and per-item lookups never count here: the signature hashes the
# arguments, so a different chunk/content/item is a different signature. Only
# CONSECUTIVE byte-identical calls advance this - the headroom above the warn is
# for transient-failure retries of the same call.
REPEATED_TOOL_CALL_WARN_AT = 3
MAX_REPEATED_TOOL_CALLS = 5

# Consecutive-error circuit breaker. Unlike the identical-args stuck
# detector above, this counts consecutive ERRORED calls of the same tool
# regardless of arguments (a flailing agent varies args every retry) and
# has no xp* exemption. At the cap the task enters Finalize-Only Mode.
ERROR_STREAK_FINALIZE_AT = 5

# Synthetic tool result returned instead of dispatching a call whose
# arguments arrived empty while the schema requires parameters — the
# signature of a tool-call JSON truncated by the provider output-token
# limit. Dispatching would run the tool with defaults against the wrong
# target; telling the model exactly what happened lets it re-emit.
TRUNCATED_TOOL_CALL_MESSAGE = (
    "Tool call rejected: the arguments arrived EMPTY ({}) but this tool has "
    "required parameters. This usually means your tool-call JSON was truncated "
    "by the output-token limit before it finished streaming. Do NOT retry the "
    "identical call. Instead: re-emit the call with smaller arguments (split "
    "large content into chunks across multiple calls), or write large payloads "
    "to a workspace file first and pass the file path, and keep any inline "
    "content well under the output limit."
)

# The other shape a truncated tool call takes: the payload streamed as a JSON
# string that stops mid-object. The pydantic error for this reads as "payload
# must not be a quoted string", which sends the model off re-quoting an argument
# that was never the problem — so name the real cause and the way out.
UNPARSEABLE_PAYLOAD_MESSAGE = (
    "Tool call rejected: the payload arrived as text that stops before the JSON "
    "closes, which is what a tool call cut off by the output-token limit looks "
    "like. The arguments were not run. Re-emit the call with less inline content "
    "— split large content across several calls, or write it to a workspace file "
    "first and pass the path. If the work is already done, answer the user now."
)

# Minimum estimated session tokens required to trigger a pre_retry
# compaction. Below this, the session is small enough that a fresh
# retry without compaction will work — paying for an LLM
# summarization round-trip just to compress 50K tokens is wasteful
# (the next arun() can still fit the full conversation). Fixed in
# response to a production case where pre_retry fired at 22K tokens
# after a healthy 105K-token first arun stopped on output-cap, not
# on context pressure. The plan-retry loop still runs; we just skip
# the compaction step.
MIN_TOKENS_FOR_PRE_RETRY_COMPACT = 80_000

# Robust-L2 feature flags. Both default ON — the implementation is
# additive and falls back to the legacy code path automatically when a
# flag is monkeypatched off in tests. NO env vars: per the project's
# feedback_no_env_vars preference, all knobs live in this module.
LEDGER_ENABLED = True
FINALIZE_MODE_ENABLED = True

# Dedicated model for context-optimizer LLM ops (PRO-1654). When enabled, the
# optimizer picks a cheaper/large model by credential-availability priority
# (bedrock → anthropic → openai → gemini) for compaction/summarisation,
# independent of the agent's configured model. Falls back to the agent's own
# model when none of the preferred providers have credentials. Flip to False to
# always use the agent's model. No env var per the feedback_no_env_vars
# preference; the per-deployment provider pin is XP_COMPACTION_PROVIDER (below).
COMPACTION_MODEL_OVERRIDE_ENABLED = True

# Fixed model ids per provider, in priority order (cheaper → fallback).
COMPACTION_MODEL_BEDROCK = "global.anthropic.claude-haiku-4-5-20251001-v1:0"
COMPACTION_MODEL_ANTHROPIC = "claude-sonnet-5"
COMPACTION_MODEL_OPENAI = "gpt-5.2"
COMPACTION_MODEL_GEMINI = "gemini-2.5-flash"


def compaction_provider_override() -> str:
    """Per-deployment compaction-provider pin, read from XP_COMPACT-family env.

    Read at call time (not import) so tests and long-lived processes see the
    live value. Returns the normalized value of ``XP_COMPACTION_PROVIDER``:
    empty = auto (credential-priority chain); a provider name pins that
    provider, falling back to the chain when its credential is missing;
    ``none`` always uses the agent's own model.
    """
    return os.environ.get("XP_COMPACTION_PROVIDER", "").strip().lower()

# Manual context-compaction tool (xpcompact_context, optimizer Layer 3).
# Temporarily DISABLED: agents were over-triggering manual compaction and
# thrashing (see Mercury issue). Automatic layers 0-2 + emergency are
# unaffected. Flip back to True to re-expose the manual tool.
MANUAL_COMPACT_TOOL_ENABLED = False

# Prompt-composition logging (sizes only, never content). Read-only: it cannot
# change what the agent receives, so the only effect of flipping this off is
# losing the [prompt-budget] log lines.
PROMPT_BUDGET_ENABLED = True

# Layer 1 skips every xp* tool by default so new control tools stay exempt
# without anyone remembering to list them. These are the exceptions: xp tools
# whose result is unbounded external/workspace data, not a fixed-shape ack.
# xpworkspace-context-retrieve is deliberately absent — it has its own
# one-turn-then-collapse path in _maybe_reoffload_retrieve.
L1_XP_OFFLOAD_ELIGIBLE = frozenset(
    {
        "xpworkspace-bash",
        "xpworkspace-grep",
        "xpworkspace-glob",
        "xpworkspace-local-db-run-query",
    }
)

# Playbooks are followed verbatim and never re-loaded, so skill-load results must not be
# offloaded - including the gateway's un-prefixed load_skill, otherwise offload-eligible.
SKILL_LOAD_TOOL_NAMES = frozenset({"xpload_skill", "load_skill"})

# Tools whose results L1 must never offload regardless of prefix or size.
L1_ALWAYS_SKIP = frozenset({"think", "analyze"}) | SKILL_LOAD_TOOL_NAMES

# L2 keeps only system messages, so xpload_skill playbooks are re-injected after each
# compaction; the gateway's load_skill result is an 8K routing aid and is never pinned.
SKILL_PIN_TOOL_NAMES = frozenset({"xpload_skill"})
PINNED_SKILLS_MAX = 2
# One rendered bundle is clamped to 32K by the controller; headroom for wrappers.
PINNED_SKILL_MAX_CHARS = 33_000

# The dynamic-tools dispatcher hides the real tool in payload.name and runs it
# without re-entering the tool hook, so a result from any external/MCP tool
# would otherwise reach L1 under this opaque xp* name and be skipped.
DYNAMIC_DISPATCH_META_TOOL = "xp_execute_tool"

# Headroom bands for the Layer 1 offload threshold. Offloading trades a small
# permanent context saving for a likely context-retrieve round-trip, which is a
# bad trade while the window is mostly empty: a 1M-window model at 20% used pays
# ~2 extra turns to save ~10K tokens. Multiplier applies to max_content_length
# at (estimated_tokens / context_window) below each fraction; above the last
# band the configured base value is used unchanged.
L1_HEADROOM_BANDS = ((0.35, 4), (0.60, 2))

# Microcompact passes a pending offload summary waits before being abandoned.
PENDING_SUMMARY_MAX_PASSES = 3
# Cap on a summary spliced into an offload preview, which is line-oriented.
OFFLOAD_SUMMARY_MAX_CHARS = 600

# Emergency fires at 88% of context window — lower than the 95% used previously
# because by then the prompt + reserved-output overhead has often pushed the
# real request past the provider's hard limit, causing fatal overflows that
# only the external retry path could recover from. 88% leaves enough headroom
# for the compaction LLM call itself plus output reservation.
EMERGENCY_COMPACT_FRACTION = 0.88

# Timeout for a single pre-retry compaction LLM call attempt (seconds).
SESSION_COMPACT_TIMEOUT = 120

# Pre-retry compaction retry policy. The L2 LLM call is wrapped in
# a retry loop so transient provider latency (or other transient
# failures) does not abort the whole pre-retry pass — losing the
# pre-retry pass means the fresh agent does not get the compacted
# summary in ``additional_context``, the old session is not deleted,
# and deep-planning state restore is skipped. Bounded at 10 to avoid
# wedging the agent loop forever while still tolerating long
# provider stalls.
PRE_RETRY_COMPACT_MAX_ATTEMPTS = 10
# Non-timeout failures (deterministic provider errors) won't self-heal across
# retries, so they get a much smaller budget than transient timeouts — the full
# 10x60s backoff on a deterministic error is what wedged the agent for hours.
PRE_RETRY_COMPACT_MAX_NONTIMEOUT_ATTEMPTS = 2
PRE_RETRY_COMPACT_RETRY_BASE_DELAY = 2.0  # seconds
PRE_RETRY_COMPACT_RETRY_MAX_DELAY = 60.0  # seconds — cap on backoff
PRE_RETRY_COMPACT_RETRY_JITTER = 0.2  # ± fraction of computed delay

# Map-phase parallelism. Each chunk is an independent LLM summarize, so the
# map calls can run concurrently up to provider rate limits. Default 8 still
# sits under typical anthropic/openai per-key concurrency budgets and lets
# the smaller 20K-token chunks (see DEFAULT_MAX_CHUNK_INPUT_TOKENS) absorb
# the extra chunk count without serializing the tail.
DEFAULT_MAP_PHASE_MAX_CONCURRENCY = 8

# Default fraction of the context window above which Layer 2 proactively
# routes to the chunked map-reduce path. 0.6 means most production runs go
# parallel before they ever hit the slow single-call ceiling.
DEFAULT_CHUNKED_COMPACT_THRESHOLD_FRAC = 0.6

# Default cap on per-map-chunk input size in tokens. Smaller chunks → faster
# TTFT per chunk + more chunks → more parallelism. Combined with
# DEFAULT_MAP_PHASE_MAX_CONCURRENCY this keeps each map call fast. Halved
# from 40K → 20K to push more parallelism into the map phase: at the
# default 0.6 threshold (~120K tokens for a 200K window) we now spawn ~6
# chunks instead of ~3, all of which run inside one concurrency window
# at DEFAULT_MAP_PHASE_MAX_CONCURRENCY=8.
DEFAULT_MAX_CHUNK_INPUT_TOKENS = 20_000

# Per-chunk 429 retry policy.
_MAP_CHUNK_RETRY_ATTEMPTS = 3
_MAP_CHUNK_RETRY_BASE_DELAY = 1.0  # seconds
_MAP_CHUNK_RETRY_JITTER = 0.2  # ± fraction of base


# Recent-actions injection (appended to continuation message after every
# Layer 2 compaction so the resuming agent has a concrete trace alongside
# the abstract summary).
INCLUDE_RECENT_ACTIONS = True
RECENT_ACTIONS_COUNT = 5
# Head/tail preview budget — never render full payloads. Middle is replaced
# with an explicit "[…N chars summarized…]" marker so the model knows content
# was elided (not truncated).
RECENT_ACTIONS_ARGS_HEAD = 500
RECENT_ACTIONS_ARGS_TAIL = 500
RECENT_ACTIONS_RESULT_HEAD = 500
RECENT_ACTIONS_RESULT_TAIL = 500


def _env_int(name: str, default: int) -> int:
    """Read env var *name* as an int, falling back to *default*.

    Returns *default* when the variable is unset, empty, or not parseable
    as an int. Used to make Layer 2 / map-reduce knobs overridable per
    deployment without code changes — see ``XP_COMPACT_*`` env vars.
    """
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return int(raw)
    except (TypeError, ValueError):
        return default


def _env_float(name: str, default: float) -> float:
    """Read env var *name* as a float, falling back to *default*.

    Returns *default* when the variable is unset, empty, or not parseable
    as a float. Used for fractional thresholds (chunked-compaction
    threshold fraction, etc.) that need fine-grained per-deployment
    tuning.
    """
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return float(raw)
    except (TypeError, ValueError):
        return default


def _is_rate_limit_error(exc: BaseException) -> bool:
    """Heuristic: does *exc* look like a provider rate-limit / 429?"""
    try:
        text = str(exc).lower()
    except Exception:
        return False
    if not text:
        return False
    return (
        "429" in text
        or "rate limit" in text
        or "rate_limit" in text
        or "too many requests" in text
        or "quota" in text
    )


def _is_connectivity_error(exc: BaseException) -> bool:
    """Heuristic: does *exc* look like the model endpoint being unreachable?"""
    try:
        text = str(exc).lower()
    except Exception:
        return False
    if not text:
        return False
    return (
        "could not connect to the endpoint" in text
        or "connect timeout" in text
        or "connection timeout" in text
        or "endpointconnectionerror" in text
        or "connecttimeouterror" in text
        or "failed to establish a new connection" in text
        or "name or service not known" in text
        or "temporary failure in name resolution" in text
    )


# Bounded exp-backoff retry for emergency compaction when the compaction model is
# unreachable — lets a transient outage self-recover before aborting, since
# emergency bypasses the failure breaker and would otherwise spin. Clamped so bad
# env config can't disable retries (attempts>=0) or collapse the backoff (delays
# >=0, max>=base).
EMERGENCY_CONNECTIVITY_RETRY_MAX_ATTEMPTS = max(
    0, _env_int("XPANDER_EMERGENCY_CONN_RETRY_ATTEMPTS", 5)
)
EMERGENCY_CONNECTIVITY_RETRY_BASE_DELAY = max(
    0.0, _env_float("XPANDER_EMERGENCY_CONN_RETRY_BASE_DELAY", 2.0)
)
EMERGENCY_CONNECTIVITY_RETRY_MAX_DELAY = max(
    EMERGENCY_CONNECTIVITY_RETRY_BASE_DELAY,
    _env_float("XPANDER_EMERGENCY_CONN_RETRY_MAX_DELAY", 30.0),
)


# Label of the stable plan block agno renders into additional_context; the
# compaction prompt's plan section reuses it so the model sees ONE plan name.
PLAN_BLOCK_LABEL = "Execution plan steps"

# Max output tokens for Claude/Bedrock model calls. agno's Claude default
# (8192) silently truncated a 35KB tool-call JSON mid-stream, dispatching
# the tool with empty args. 32K covers any realistic single tool call
# while modern Claude models allow far more.
LLM_MAX_OUTPUT_TOKENS = _env_int("XPANDER_LLM_MAX_OUTPUT_TOKENS", 32_000)

# Args-agnostic per-tool volume ceiling. Pagination runaways vary the cursor
# on every call and alternating-tool loops reset the consecutive counters, so
# neither the identical-args detector nor the error-streak breaker ever fires
# on them. This counts TOTAL calls of one tool across the task (xp* exempt).
# Only mutating-named tools can be disabled; read-class tools are warn-only -
# marathon agents legitimately make hundreds of read calls over hours.
TOTAL_TOOL_CALLS_WARN_AT = _env_int("XPANDER_TOTAL_TOOL_CALLS_WARN_AT", 50)
MAX_TOTAL_TOOL_CALLS_PER_TOOL = _env_int("XPANDER_MAX_TOTAL_TOOL_CALLS_PER_TOOL", 100)
READ_TOOL_CALLS_WARN_AT = _env_int("XPANDER_READ_TOOL_CALLS_WARN_AT", 150)
# clamped: used as a modulo divisor
READ_TOOL_CALLS_REWARN_EVERY = max(1, _env_int("XPANDER_READ_TOOL_CALLS_REWARN_EVERY", 100))

# Plan-churn breaker. Planning/reasoning tools are exempt from stuck detection
# (they legitimately repeat), so a pure plan/think loop - re-emitting the same
# decision step with no real tool call in between - previously ran unbounded.
# Counts consecutive planning/reasoning calls; any other tool resets it.
PLAN_CHURN_WARN_AT = _env_int("XPANDER_PLAN_CHURN_WARN_AT", 10)
MAX_PLAN_CHURN = _env_int("XPANDER_MAX_PLAN_CHURN", 16)

# Plan-less wrap-up budget: advisory-only repeating nudge every N non-mutating calls,
# never finalize - the hard breakers contain storms. XPANDER_WRAPUP_MAX_CALLS is retired.
WRAPUP_GRACE_CALLS = max(1, _env_int("XPANDER_WRAPUP_GRACE_CALLS", 10))

# Run-wide hard ceiling on tool calls when agno_settings.tool_call_limit is unset.
# Over-limit agno refuses ALL calls including finalize, so headroom beats tightness;
# sized for marathon runs (hours, hundreds of legitimate read calls).
TOOL_CALL_LIMIT_DEFAULT = _env_int("XPANDER_TOOL_CALL_LIMIT", 800)
# Safe-read allowance inside finalize mode; past it even reads gate.
FINALIZE_SAFE_READS_CAP = _env_int("XPANDER_FINALIZE_SAFE_READS_CAP", 5)
