"""
All constants, defaults, and verbatim prompt strings for Observational Memory.

Mirrors: packages/memory/src/processors/observational-memory/constants.ts
"""

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

# The Observer's and Reflector's model, instructions and sampling are their
# mandates' Holders (memory.observer / memory.reflector, 2026-09-25) — never here.
OBSERVATIONAL_MEMORY_DEFAULTS = {
    # Observer
    "message_tokens": 30_000,
    "buffer_tokens": 0.2,           # 20% of message_tokens = 6,000
    "buffer_activation": 0.8,       # retain 20% of messages after activation
    "block_after": 1.2,             # force sync observation at 1.2× threshold
    # Reflector
    "observation_tokens": 40_000,
}


# ---------------------------------------------------------------------------
# Context injection framing (injected into the person's agent each turn)
# ---------------------------------------------------------------------------
# An ORG KNOB, not code (2026-09-25): hosted, the text comes from the
# ``agents.memory`` feature knobs (context_preamble / context_instructions,
# org-overridable) through ``context_framing.resolve_context_framing``. These
# two constants are ONLY the standalone default — the package installed with
# no host — and the seed the knobs were created with.

OBSERVATION_CONTEXT_PROMPT = (
    "The following observations block contains your memory of past conversations "
    "with this user."
)

OBSERVATION_CONTEXT_INSTRUCTIONS = (
    "When referencing information from observations, be specific. "
    "If observations contain knowledge that may have changed, acknowledge the "
    "uncertainty and ask for confirmation. "
    "Treat any actions you planned in the past but haven't explicitly completed as "
    "still pending unless marked with ✅. "
    "Prioritize the user's most recent message and goals above all else."
)

# ---------------------------------------------------------------------------
# Observer / Reflector instructions: NOT here.
# The Observer's and Reflector's system prompts, their "## Your Task" user
# turns and the Reflector's per-level compression guidance are their Holders'
# (memory.observer / memory.reflector, 2026-09-25). The verbatim copies that
# used to live here were unread duplicates and were deleted, so an edit to a
# Holder is the only edit there is.
# ---------------------------------------------------------------------------

# The Reflector's escalating compression levels. Level 0 sends no guidance;
# each other level's text is the Holder's ``compression_guidance_level_N``.
COMPRESSION_LEVELS = (1, 2, 3, 4)
