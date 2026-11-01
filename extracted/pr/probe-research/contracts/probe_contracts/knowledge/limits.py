"""Gatherer deadlines research-os sizes its client timeouts against, in seconds.

Lifted from the engine (engine/retrieval/gatherer/tuning.py, engine:3); the engine imports this package.
"""

# Client-side cap on one gatherer model turn. Nested inside
# SEARCH_AGENT_LOOP_TIMEOUT_SECONDS, which bounds the complete loop via
# asyncio.wait_for and is the hard backstop.
#
# This number, not the gateway's, is what ends a stalled turn. MEASURED: a
# stalled turn runs to exactly this deadline (repeated `litellm.Timeout ...
# time taken=<deadline>.01` with `x-litellm-attempted-fallbacks: 0`), never to
# the 12s Cerebras deployment deadline, so the Cerebras -> Fireworks failover
# the old 60s value was sized for does not actually fire. Treat this purely as
# "how long are we willing to wait", not as failover headroom.
#
# The stall is reproducible and specific: large context COMBINED WITH
# tool-calling. A 300KB prompt alone returns in ~1.5s; the same prompt with
# `tools` + tool_choice="required" was measured at 61.6s. Neither ingredient
# alone does it, which is why isolated probes look healthy and only real
# gatherer turns hang.
#
# 5s, CUT FROM 70s (2026-08-04), and the strategy changed with it: this is no
# longer "how long are we willing to wait for Cerebras to unstick", it is "how
# long before we give up on Cerebras and finish the run on Fireworks".
#
# Waiting was the wrong trade. Measured over 105 production turns:
#
#     healthy turns (n=92, 87.6%)   mean 971ms   p50 812ms   p90 1.6s   max 3.9s
#     stalled turns (n=13, 12.4%)   59.5s - 63.8s, NOTHING in between
#
# The distribution is bimodal with a 55-second empty gap, so a deadline
# anywhere in 4s..59s separates the two modes perfectly. 5s sits above the
# healthy max (3.9s) with headroom and cuts every stall. It cannot truncate
# healthy traffic: a turn slower than 5s has never been observed to then
# succeed quickly -- it goes to ~60s.
#
# Why waiting out the stall did not work. The 70s value assumed the stalled
# turn eventually returns something useful, and it does (finish_reason
# tool_calls at ~60s). But turns are per-RETRIEVAL dice rolls: at a mean 2.23
# turns/retrieval, a 12.4% per-turn stall rate compounds to ~30% of retrievals
# degrading. And research-os hangs up at 30s (ENGINE_TIMEOUT_SECONDS), so for
# that caller a 60s success is indistinguishable from a failure -- it had
# already returned an empty result set.
#
# The failover this enables is OURS, not the gateway's. The proxy's
# Cerebras -> Fireworks route fallback provably never fires: stalled turns end
# at exactly this client deadline carrying `x-litellm-attempted-fallbacks: 0`,
# never at the gateway's own 12s deployment deadline (see the block above).
# So the loop owns it: on the first stall it flips to
# SEARCH_AGENT_FALLBACK_INFERENCE_MODEL and STAYS there for the rest of the
# run -- see `_run_turn`. Retrying Cerebras every turn would re-pay this 5s on
# each one.
#
# Caller budgets this now fits inside:
#   * research-os /v1/search: 30s total. Worst case is now ~4s deterministic
#     + one 5s cut + Fireworks turns, which fits. It did not before.
#   * MCP search_knowledge: 180s. Unaffected; it just stops spending 60s of
#     that on a stalled provider.
#
# 12s, RAISED FROM 5s (2026-08-14). Everything above is still the right
# reasoning; its INPUT expired. That analysis rested on a bimodal distribution
# with a 55-second empty gap -- healthy max 3.9s, stalls at 59.5-63.8s, nothing
# between -- which made "a turn slower than 5s never then succeeds" true, and a
# 5s cut free. Re-measured over 54 successful production turns:
#
#     healthy turns   p50 2.17s   p90 4.66s   p95 6.69s   max 10.6s
#     stalls at ~60s: NONE observed
#
# The gap is gone and the healthy tail now runs past 10s, so 5s sits at roughly
# p90 of HEALTHY traffic and cuts about one turn in ten that would have
# returned. 12s clears the observed p100 with headroom.
#
# WHY THIS MATTERS MORE THAN THE 7s IT COSTS. Cutting the primary fails the run
# over, and the failover is sticky, and the new provider has no cached prefix.
# Measured on the same conversations: turns BEFORE a failover run p50 926ms at
# mean cache_hit 0.56; turns AFTER it run p50 4.80s, max 10.6s, and 5 of 12
# failovers then died on the gateway's 12s Fireworks deadline. So a cut
# triggered by one slow turn makes every remaining turn ~5x slower, which is
# what pushed ~11-14% of /v1/search past its 30s budget. The failover itself is
# fine -- it rescued 7 of 12 -- it just must not fire on healthy traffic.
#
# NOT the 10s that was tried before and reverted: charts/research-os
# values.yaml records a 10s/10s experiment that clipped healthy turns, and the
# 10.6s max above is exactly why. This raises ONE rung; the Fireworks rung
# stays where it is.
#
# The proxy's own cerebras/* deployment timeout must stay ABOVE this or it cuts
# first and this value never binds -- research-os charts/research-os/values.yaml
# `litellm.searchAgentTimeout`, moved to 14 in the same change.
SEARCH_AGENT_GATHERER_TIMEOUT_SECONDS = 12.0

# Per-turn deadline once the run has failed over.
#
# This was 12.0, on two claims that production contradicts.
#
# 1. "Mirrors the gateway's own Fireworks route timeout (12s)." It does not.
#    The deployed proxy config gives `accounts/fireworks/*` a timeout of 40 and
#    `cerebras/*` a timeout of 12 -- 12 is the CEREBRAS deployment deadline, so
#    the mirror was taken off the wrong route and held the fallback to a
#    deadline 28s tighter than the gateway itself allows.
# 2. "Fireworks ... does not exhibit the large-context + tool-calling stall."
#    It does. The stall is driven by the ~300-chunk pre-fan-out prompt with
#    tool_choice=required, not by the provider, so the hop lands on a model
#    that stalls the same way.
#
# The 5s primary cut is safe because Cerebras is bimodal -- healthy maxes at
# 3.9s, stalls start at 59.5s, and nothing lives in the 55s gap. Fireworks has
# no such gap, so the same reasoning does NOT transfer. Measured over 16h on
# the managed data plane (111 failovers): successful fallback turns ran a
# smooth continuum from 451ms to 11904ms, and 72 of 76 failures landed within
# 100ms of exactly 12000ms. That is a clipped distribution -- the deadline was
# truncating turns that were going to succeed, which is the exact failure the
# old comment claimed to be avoiding by not reusing the 5s value.
#
# 30, not the gateway's 40: SEARCH_AGENT_LOOP_TIMEOUT_SECONDS caps the whole
# stage at 60s with setup subtracted, and measured setup (grounding +
# extraction + pre-fan-out) is p50 32s, leaving ~28s for all turns at the
# median. 40 is unreachable there, so it would be a number that never binds.
# This is a CEILING, not a guarantee: the stage deadline usually fires first
# and degrades through the normal loop_timeout path. It is still strictly
# better than 12, which cut the turn while ~16s of stage budget sat unused.
# Capping the pre-fan-out is what would make this deadline fully reachable.
#
# 12s, cut back from 30s (2026-08-14), because 30 was never the deadline that
# fired. This is a CLIENT deadline, and the gateway enforces its own on the
# same call: `accounts/fireworks/*` carries `timeout: 12` in research-os
# charts/research-os/values.yaml (`litellm.searchAgentFallbackTimeout`). Every
# observed fallback failure in production is that one, not this:
#
#   litellm.Timeout: ... Fireworks_aiException ... Timeout passed=12.0,
#   time taken=12.003 seconds        (n=9, all within 51ms of 12.000)
#
# So raising this to 30 bought nothing and, worse, made the ladder arithmetic
# below reason about a number the system cannot produce -- the stage cap was
# sized against 30s fallback turns that always ended at 12. Setting it to what
# actually binds keeps `test_stage_cap_leaves_room_for_the_failover_to_land`
# honest instead of accidentally true.
#
# If the fallback should really get 30s, raise the GATEWAY value; this one
# follows it, never leads. And check the caller first: research-os abandons at
# 30s total, so a 30s fallback turn cannot land there whatever this says.
SEARCH_AGENT_FALLBACK_TIMEOUT_SECONDS = 12.0

# Overall agent loop cap, and a HARD ceiling on the whole gatherer stage:
# `run_gatherer` converts this into a deadline measured from its own entry, so
# grounding + extraction + pre-fan-out (~4s) come OUT of this budget rather
# than being added to it. Whatever happens, the stage returns within this many
# seconds; timeout degrades to the citable pre-fan-out evidence the harness
# already retrieved (`_answer_from_pool` off `state.prefanout`), which is
# a real result set, not an error.
#
# 60s, cut from 90s (2026-08-04). With a 5s primary cut and a 12s fallback
# deadline, a 3-turn run lands ~40s worst case, so 60s is the backstop for
# pathological cases rather than a routine ceiling.
#
# 25s, cut from 60s (2026-08-14), because 60 was never reachable by the caller
# that matters. research-os /v1/search abandons at ENGINE_TIMEOUT_SECONDS = 30,
# so a stage permitted to run 60s spends up to half its budget producing an
# answer nobody is still waiting for -- and the caller reports state:"partial"
# while this pod is still working. A backstop above the caller's own deadline
# is not a backstop, it is a leak.
#
# 25 not 30: the deadline is measured from `run_gatherer` entry, so setup
# (grounding + extraction + pre-fan-out) comes OUT of it, not on top. Setup
# measures p50 6.5s / p90 10.7s in production -- the "~4s" above is stale --
# leaving ~14s of turns at p90 setup, which fits one full 12s primary cut plus
# the degrade to pre-fan-out. The 5s of slack under 30 covers response
# serialisation and the hop back to research-os.
#
# Timing out here is not an error: it degrades to `_answer_from_pool` off
# `state.prefanout`, which is a real citable result set. Returning that at 25s
# beats returning nothing at 30.
SEARCH_AGENT_LOOP_TIMEOUT_SECONDS = 25.0
