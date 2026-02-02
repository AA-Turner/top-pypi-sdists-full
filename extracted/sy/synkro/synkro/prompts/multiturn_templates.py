"""Multi-turn conversation prompt templates for dataset generation."""

# =============================================================================
# FOLLOW-UP QUESTION GENERATION
# =============================================================================

FOLLOW_UP_GENERATION_PROMPT = """You are generating a follow-up question for a multi-turn policy conversation.

Generate a {question_type} follow-up question based on the conversation so far.

QUESTION TYPES:
- **clarification**: Ask for more details about an ambiguous point in the previous response
- **edge_case**: Probe a boundary condition or unusual scenario related to the policy
- **what_if**: Explore a hypothetical variation ("What if X changes?")
- **specificity**: Drill into specific implementation details or examples
- **challenge**: Question the reasoning or ask for justification of a recommendation

CONVERSATION SO FAR:
{conversation}

POLICY:
{policy}

Generate a follow-up that:
1. Builds naturally on the conversation context
2. Tests deeper understanding of the policy
3. Is realistic - something a user would actually ask
4. Matches the specified question type
5. Is specific enough to require a substantive response

Respond with ONLY the follow-up question text."""

# =============================================================================
# MULTI-TURN RESPONSE GENERATION
# =============================================================================

MULTI_TURN_RESPONSE_PROMPT = """You are a domain expert continuing a multi-turn policy conversation.

CONVERSATION HISTORY:
{conversation}

LATEST QUESTION:
{question}

POLICY:
{policy}

Provide a response that:
1. Directly addresses the latest question
2. Maintains consistency with your previous responses
3. Cites specific policy sections that apply
4. Builds on the established context
5. Uses <reasoning> tags to show your thought process
6. Gives specific, actionable recommendations

Your response should acknowledge what was discussed before and add new insights.
Keep the response appropriately concise for a conversational turn."""

MULTI_TURN_INITIAL_PROMPT = """You are a domain expert starting a multi-turn conversation.

This conversation will have {target_turns} turns. Start with a response that:
1. Addresses the initial question thoroughly
2. Uses <reasoning> tags to show your thought process
3. Cites specific policy sections
4. Leaves room for natural follow-up questions
5. Gives specific, actionable initial guidance

SCENARIO:
{scenario}

CONTEXT:
{context}

POLICY:
{policy}

Respond as the assistant. Your response should be comprehensive but leave room for the user to ask follow-up questions that will deepen the discussion."""

# =============================================================================
# MULTI-TURN GRADING
# =============================================================================

MULTI_TURN_GRADE_PROMPT = """You are a strict evaluator grading a multi-turn policy conversation.

CONVERSATION:
{conversation}

POLICY:
{policy}

Evaluate EACH assistant turn AND the overall conversation.

For EACH assistant turn, check:
1. **Policy Compliant** - Recommendations follow the policy exactly
2. **Properly Cited** - Relevant policy sections are referenced
3. **Complete Reasoning** - Logic is sound with no gaps
4. **Actionable** - Recommendations are specific, not vague

For the OVERALL conversation, check:
1. **Coherence** - No contradictions across turns
2. **Progressive Depth** - Each turn appropriately builds on context
3. **Consistency** - Recommendations don't conflict with earlier statements

The conversation PASSES only if:
- ALL individual turns pass their criteria
- The overall coherence and consistency checks pass

Respond with a structured evaluation for each turn and overall assessment."""

TURN_GRADE_FORMAT = """{{
  "turn_index": {turn_index},
  "pass": <true/false>,
  "policy_violations": ["<violation>", ...],
  "missing_citations": ["<missing>", ...],
  "incomplete_reasoning": ["<gap>", ...],
  "vague_recommendations": ["<vague>", ...],
  "feedback": "<specific feedback for this turn>"
}}"""

CONVERSATION_GRADE_FORMAT = """{{
  "index": {index},
  "overall_pass": <true/false>,
  "turn_grades": [<array of turn grades>],
  "coherence_pass": <true/false>,
  "coherence_issues": ["<contradiction or incoherence>", ...],
  "progressive_depth": <true/false>,
  "overall_feedback": "<summary of what needs fixing across the conversation>"
}}"""

# =============================================================================
# MULTI-TURN REFINEMENT
# =============================================================================

MULTI_TURN_REFINE_PROMPT = """You are improving a multi-turn conversation based on grader feedback.

ORIGINAL CONVERSATION:
{conversation}

POLICY:
{policy}

GRADING FEEDBACK:
{feedback}

Fix ALL issues while maintaining conversation coherence:
1. Address every policy violation in each turn
2. Add missing citations where indicated
3. Fill reasoning gaps with step-by-step logic
4. Make vague recommendations specific and actionable
5. Fix any coherence issues between turns
6. Ensure progressive depth in the conversation

IMPORTANT: Maintain the same conversation structure (same number of turns, same topics).
Only improve the CONTENT of the assistant responses.

Output the improved conversation with all turns."""
