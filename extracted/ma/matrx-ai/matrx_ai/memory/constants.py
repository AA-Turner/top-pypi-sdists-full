"""
All constants, defaults, and verbatim prompt strings for Observational Memory.

Mirrors: packages/memory/src/processors/observational-memory/constants.ts
"""

# ---------------------------------------------------------------------------
# Defaults
# ---------------------------------------------------------------------------

OBSERVATIONAL_MEMORY_DEFAULTS = {
    # Observer
    "message_tokens": 30_000,
    "observation_model": "gemini-2.5-flash",
    "observer_temperature": 0.3,
    "observer_max_tokens": 100_000,
    "observer_thinking_budget": 215,
    "buffer_tokens": 0.2,           # 20% of message_tokens = 6,000
    "buffer_activation": 0.8,       # retain 20% of messages after activation
    "block_after": 1.2,             # force sync observation at 1.2× threshold
    # Reflector
    "observation_tokens": 40_000,
    "reflection_model": "gemini-2.5-flash",
    "reflector_temperature": 0.0,
    "reflector_max_tokens": 100_000,
    "reflector_thinking_budget": 1024,
}


# ---------------------------------------------------------------------------
# Context injection prompts (injected into actor's system prompt each turn)
# ---------------------------------------------------------------------------

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

# Injected after observations to prevent awkward memory acknowledgment preamble
OBSERVATION_CONTINUATION_HINT = (
    "Continue naturally. Do not start your response by acknowledging you have memory "
    "of past conversations or summarizing what you know about the user."
)

# Injected when retrieval mode is enabled
OBSERVATION_RETRIEVAL_INSTRUCTIONS = (
    "When you need to recall specific details from past conversations that may not be "
    "in your current observations, use the `recall` tool. "
    "Observation groups are numbered — pass the group number range to retrieve the "
    "raw messages behind those observations."
)


# ---------------------------------------------------------------------------
# Observer extraction instructions
# (Verbatim translation from observer-agent.ts OBSERVER_EXTRACTION_INSTRUCTIONS)
# ---------------------------------------------------------------------------

OBSERVER_EXTRACTION_INSTRUCTIONS = """## Observation Extraction Instructions

### 1. User Assertions vs Questions
- User STATEMENTS → extract as observations: "I have two kids" → `User stated they have two kids`
- User QUESTIONS → do NOT extract as assertions of fact: "Do I have any kids?" is a question, not a claim

### 2. State Changes
- When user switches from A to B, note the transition explicitly
- "I'm switching from Python to TypeScript" → `User switching from Python to TypeScript`
- Include what was true before if mentioned

### 3. Temporal Anchoring (Three-Date Model)
Each observation may have up to three temporal references:
- **Observation date**: The timestamp of when the message was sent (ALWAYS present — use the message timestamp, formatted at start of observation in (HH:MM) format)
- **Referenced date**: A specific date mentioned in the content (e.g., "my flight is January 31") — add at end in `(meaning Jan 31 2026)` format
- **Relative date**: A computed date from a relative expression (e.g., "next Tuesday" → compute the actual date based on observation date)

Format: `(HH:MM) [observation text]. (meaning DATE)` — only add end date when a specific future/past date is referenced.
When date is vague ("someday", "eventually"), omit the end date.

### 4. Preserve Unusual Phrasing
- When users use distinctive or unusual language, preserve it verbatim in quotes
- "User said they want the UI to feel 'buttery smooth'" — keep the quote
- Do not paraphrase unique expressions

### 5. Precise Action Verbs
Use the most specific verb:
- Not "used" → "ran", "executed", "called", "invoked"
- Not "changed" → "renamed", "deleted", "moved", "refactored"
- Not "got" → "received", "fetched", "returned"
- Not "looked at" → "viewed", "read", "scanned", "searched"

### 6. Recommendations and Lists (Preserve Details)
When assistant recommends items (hotels, books, products, restaurants, etc.):
- Preserve at least one distinguishing attribute per item
- Include: name, key differentiator, price range, location, relevant feature
- Don't compress: "recommended 3 hotels" — use sub-bullets with specifics

### 7. Names, Handles, and Creative Content
- People's names: preserve exactly, note relationship ("brother Mark", "manager Sarah Kim")
- Social handles/usernames: preserve exactly
- Creative titles, project names, brand names: exact capitalization

### 8. Technical Numbers and Values
- Code values, IDs, config settings: preserve exactly
- Port numbers, token counts, timeouts, file paths: exact values
- Version numbers: exact (not approximate)

### 9. Completion Tracking
- Use ✅ ONLY when something is definitively done:
  - User confirmed completion ("it worked", "fixed!", "done")
  - Assistant gave a complete, direct answer to a question
  - A task ended with a clear success state
- Do NOT use ✅ for partial progress or "probably will work"

### 10. Group Repeated Similar Actions
When the same type of action repeats (viewing files, running commands, searching):
- Create a parent bullet: `* 🟡 (14:30) Searched for auth-related files`
- Add sub-bullets for each: `  * -> viewed src/auth.ts`
- Cap at ~5 sub-bullets; summarize the rest: `  * -> ... and 7 more files`

### 11. Avoiding Repetitive Observations
- Never duplicate an observation from prior observations
- If user repeats something noted before, add a note about recurrence but don't re-create the original
- Check existing observations before adding a new one about the same fact"""


# ---------------------------------------------------------------------------
# Observer guidelines (concise behavior rules)
# ---------------------------------------------------------------------------

OBSERVER_GUIDELINES = """## Observer Guidelines

- Generate 1-5 observations per exchange (more for dense/important content)
- Use terse, note-like language — not full sentences
- Group all tool calls under their triggering request
- 🔴 = high priority (user facts, preferences, unresolved goals, critical context)
- 🟡 = medium priority (project info, learned context, tool results)
- 🟢 = low priority (minor details, uncertain observations)
- ✅ = completed (definitive success, confirmed done)
- Sub-bullets (  * ->) for supporting details and tool results
- Only include what would be valuable to remember in a future session
- Skip pleasantries, confirmations, and routine acknowledgments"""


# ---------------------------------------------------------------------------
# Reflector compression levels
# ---------------------------------------------------------------------------

COMPRESSION_GUIDANCE = {
    0: "",  # No guidance on first attempt
    1: (
        "Aim for approximately 8/10 detail level. "
        "Condense the beginning of the observations more aggressively, "
        "but retain more detail from the recent/end section."
    ),
    2: (
        "Aim for approximately 6/10 detail level. "
        "Apply aggressive compression throughout. "
        "Keep essential facts, user preferences, and unresolved goals. "
        "Remove redundant context, minor details, and tool call sequences where outcome is known."
    ),
    3: (
        "Aim for approximately 4/10 detail level. "
        "Critical compression — only keep final outcomes, confirmed user facts, "
        "active goals, and pivotal decisions. "
        "Collapse entire multi-day sequences into single-line summaries."
    ),
    4: (
        "Aim for approximately 2/10 detail level. "
        "Extreme compression — collapse all tool call sequences to outcome-only. "
        "Keep only: user identity facts, active unresolved goals, final confirmed outcomes. "
        "Use maximum possible brevity."
    ),
}

# ---------------------------------------------------------------------------
# System prompt templates (built dynamically, these are the static sections)
# ---------------------------------------------------------------------------

OBSERVER_PERSONA = (
    "You are an expert memory assistant. Your role is to observe conversations and "
    "extract the most important information into a structured observation log. "
    "You work in the background — your output will be used to help an AI assistant "
    "remember key facts across sessions."
)

REFLECTOR_PERSONA = (
    "You are another part of the same AI assistant's cognitive system — specifically, "
    "the memory consolidation module. You receive a set of observations previously "
    "created by the Observer (another part of the same psyche that you understand "
    "completely). Your job is to re-organize, condense, and streamline those "
    "observations to reduce their size while preserving all important information. "
    "You understand exactly how observations were created because you know the same "
    "extraction instructions the Observer follows."
)

REFLECTOR_RULES = """## Reflector Rules

- Preserve ALL ✅ completion markers — do not drop completed items
- Preserve all user identity facts (preferences, stated facts about themselves)
- Preserve all unresolved goals and active tasks
- Preserve all dates and timestamps — temporal context is critical
- Condense older observations more aggressively; retain more detail for recent ones
- Draw connections between related observations when appropriate
- Identify if the agent got off track and note course corrections
- For resource scope: maintain thread attribution for context-specific facts, consolidate universal user facts
- The output IS the entire memory — there is no other record. Preserve everything important.
- Do NOT add new information that wasn't in the source observations
- Output ONLY the refined observations block (same format as input)"""
