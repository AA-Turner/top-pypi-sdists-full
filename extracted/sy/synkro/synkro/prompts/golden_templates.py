"""Prompt templates for Golden Trace generation.

These prompts implement the 4-stage Golden Trace pipeline:
1. Logic Extraction (The Cartographer) - Extract rules as DAG
2. Scenario Synthesis (The Adversary) - Generate typed scenarios
3. Trace Synthesis (The Thinker) - Produce grounded reasoning
4. Verification (The Auditor) - Verify trace against Logic Map
"""

# =============================================================================
# STAGE 1: LOGIC EXTRACTION (The Cartographer)
# =============================================================================

LOGIC_EXTRACTION_PROMPT = """You are a policy analyst tasked with extracting a Logic Map from a policy document.

A Logic Map is a Directed Acyclic Graph (DAG) where:
- Each node is a RULE with a unique ID (R001, R002, etc.)
- Edges represent DEPENDENCIES between rules
- Root rules have no dependencies (they are entry points)

POLICY DOCUMENT:
{policy_text}

EXTRACTION INSTRUCTIONS:

1. **Identify All Rules**: Extract every distinct rule, condition, or requirement from the policy.
   - Look for: "must", "shall", "should", "can", "cannot", "if...then", "unless", "except"
   - Each rule should be atomic (one condition -> one action)

2. **Categorize Each Rule**:
   - CONSTRAINT: Must/must not conditions (e.g., "Refunds must be requested within 30 days")
   - PERMISSION: Allowed actions (e.g., "Customers can request store credit")
   - PROCEDURE: Step-by-step processes (e.g., "To cancel, first verify identity, then...")
   - EXCEPTION: Special cases that override other rules (e.g., "VIP customers are exempt from...")

3. **Identify Dependencies**:
   - If Rule B can only be evaluated after Rule A is known, then B depends on A
   - Example: "If refund is approved (R001), customer can choose cash or credit (R002)" - R002 depends on R001
   - Root rules are those that can be evaluated independently

4. **Ensure DAG Properties**:
   - No circular dependencies (A -> B -> A is invalid)
   - All rules must be reachable from root rules

5. **CRITICAL - Rule Precision Requirements**:

   a) **Explicit Scope**: Each rule must clearly state WHO or WHAT it applies to.
      - BAD: "Maximum $75 per person" (ambiguous - applies to what?)
      - GOOD: "Team events have a maximum of $75 per person. Client meals have no per-person limit."

   b) **Boundary Clarity**: For thresholds, specify inclusive vs exclusive.
      - BAD: "Expenses over $50 need approval" (is $50 exactly included?)
      - GOOD: "Expenses of $50 or more require manager approval" (inclusive)
      - GOOD: "Expenses exceeding $50 require manager approval" (exclusive, $50 does not need approval)

   c) **Distinguish Similar Rules**: If a policy treats categories differently, create SEPARATE rules.
      - Example: If "client meals" and "team events" have different limits, they need separate rule IDs
      - R008a: "Client meals: no per-person spending limit"
      - R008b: "Team events: maximum $75 per person"

   d) **No Ambiguous Groupings**: Avoid rules that bundle unrelated constraints.
      - BAD: "Meals have various limits depending on type"
      - GOOD: Separate rules for each meal type with specific limits

OUTPUT FORMAT:
Provide the Logic Map with:
- rules: List of all extracted rules with their IDs, text, conditions, actions, dependencies, and categories
- root_rules: List of rule IDs that have no dependencies (entry points)
- reasoning: Brief explanation of the extraction process and key relationships identified"""


# =============================================================================
# STAGE 2: SCENARIO SYNTHESIS (The Adversary)
# =============================================================================

GOLDEN_SCENARIO_PROMPT = """You are a scenario generator creating {scenario_type} test cases for a policy.

POLICY DOCUMENT:
{policy_text}

LOGIC MAP (Extracted Rules):
{logic_map}

CATEGORY: {category}
COUNT: Generate exactly {count} scenarios

SCENARIO TYPES:
- POSITIVE (Happy Path): User meets ALL criteria, rules should approve/allow
- NEGATIVE (Violation): User fails EXACTLY ONE criterion, rules should deny/reject
- EDGE_CASE (Boundary): User is at exact limits (e.g., day 30 of 30-day window)
- IRRELEVANT: Query not covered by the policy at all

YOUR TASK - Generate {scenario_type} scenarios:

{type_specific_instructions}

REQUIREMENTS FOR EACH SCENARIO:
1. description: The user's EXACT words — a realistic, specific request
   - Real users naturally mention key details (amounts, items, dates, what they have/don't have)
   - Include enough detail for a substantive first response — not a vague opener
   - GOOD: "I need to expense a $180 client lunch from last Tuesday. I have the receipt and my manager approved it."
   - GOOD: "Can I get reimbursed for a $450 flight I booked yesterday? I don't have approval yet."
   - BAD: "I'd like to submit an expense for a client lunch."
   - BAD: "I have a question about travel expenses."

2. context: Background facts that inform the scenario but the user hasn't explicitly stated
   - Policy implications: which approval tier applies, which rules are triggered
   - Situational details: user's role, department, history
   - GOOD: "Amount falls in $100-$500 tier requiring manager approval (R024). User is in Sales department."
   - BAD: "Expense amount: $180, Purchase date: 5 days ago" (these belong in description — the user knows their own expense)

3. target_rule_ids: Which rules from the Logic Map this scenario tests
4. expected_outcome: What the correct response should do based on the rules

CRITICAL - DESCRIPTION VS CONTEXT:
- Description = what the user says (includes their own details: amounts, dates, receipts)
- Context = what the user doesn't know or hasn't stated (policy implications, rule triggers, background)
- The assistant should NOT need to ask for information the user already provided

BAD EXAMPLE:
  description: "I'd like to submit an expense for a client lunch"
  context: "Expense amount: $180, Purchase date: 5 days ago, Has digital receipt, Has manager approval"

GOOD EXAMPLE:
  description: "I need to expense a $180 client lunch from last Tuesday. I have the digital receipt and my manager already approved it."
  context: "Amount falls in $100-$500 tier (R024). Within 30-day submission window. All procedural requirements met."

IMPORTANT:
- Each scenario must reference specific rule IDs from the Logic Map
- Scenarios should be diverse within the category
- {scenario_type} scenarios should clearly demonstrate the expected behavior"""

POSITIVE_SCENARIO_INSTRUCTIONS = """For POSITIVE scenarios:
- The user's situation should satisfy ALL relevant rule conditions
- The expected outcome should be approval/success/fulfillment
- Include clear context showing why all rules pass
- Example: A customer requesting a refund on day 5 of a 30-day window with receipt"""

NEGATIVE_SCENARIO_INSTRUCTIONS = """For NEGATIVE scenarios:
- The user's situation should FAIL exactly ONE criterion
- Clearly identify which rule fails and why
- The expected outcome should be denial/rejection with explanation
- Example: A customer requesting a refund on day 45 of a 30-day window (violates R001)"""

EDGE_CASE_SCENARIO_INSTRUCTIONS = """For EDGE_CASE scenarios:
- The user's situation should be at EXACT boundaries
- Test limits, thresholds, and edge conditions
- The expected outcome depends on whether boundary is inclusive/exclusive
- Example: A customer requesting a refund on EXACTLY day 30 of a 30-day window"""

IRRELEVANT_SCENARIO_INSTRUCTIONS = """For IRRELEVANT scenarios:
- The user's query should NOT be addressed by ANY rule in the policy
- The expected outcome is a polite explanation that this is outside policy scope
- Should still be a reasonable customer inquiry, just unrelated
- Example: Asking about company history when policy only covers refunds"""


GOLDEN_SCENARIO_BATCHED_PROMPT = """You are a scenario generator creating diverse test cases for a policy.

POLICY DOCUMENT:
{policy_text}

LOGIC MAP (Extracted Rules):
{logic_map}

CATEGORY: {category}

══════════════════════════════════════════════════════════════════════════════
MANDATORY DISTRIBUTION - YOU MUST FOLLOW THIS EXACTLY:
══════════════════════════════════════════════════════════════════════════════

Generate EXACTLY {total_count} scenarios with THIS EXACT distribution:
  • {positive_count} scenarios with scenario_type="positive"
  • {negative_count} scenarios with scenario_type="negative"
  • {edge_case_count} scenarios with scenario_type="edge_case"
  • {irrelevant_count} scenarios with scenario_type="irrelevant"

⚠️  CRITICAL: Each scenario's "scenario_type" field MUST match the required type.
    Do NOT generate all positive scenarios. Follow the distribution above.

══════════════════════════════════════════════════════════════════════════════

SCENARIO TYPE DEFINITIONS:
- POSITIVE: User meets ALL criteria, rules should approve/allow
- NEGATIVE: User fails EXACTLY ONE criterion, rules should deny/reject
- EDGE_CASE: User is at exact limits (e.g., exactly $50 when threshold is $50)
- IRRELEVANT: Query not covered by the policy at all (unrelated topic)

REQUIREMENTS FOR EACH SCENARIO:
1. description: The user's EXACT words — a realistic, specific request
   - Real users naturally mention key details (amounts, items, dates, what they have/don't have)
   - Include enough detail for a substantive first response — not a vague opener
   - GOOD: "I need to expense a $180 client lunch from last Tuesday. I have the receipt and my manager approved it."
   - GOOD: "Can I get reimbursed for a $450 flight I booked yesterday? I don't have approval yet."
   - BAD: "I'd like to submit an expense for a client lunch."
   - BAD: "I have a question about travel expenses."

2. context: Background facts that inform the scenario but the user hasn't explicitly stated
   - Policy implications: which approval tier applies, which rules are triggered
   - Situational details: user's role, department, history
   - GOOD: "Amount falls in $100-$500 tier requiring manager approval (R024). User is in Sales department."
   - BAD: "Expense amount: $180, Purchase date: 5 days ago" (these belong in description — the user knows their own expense)

3. scenario_type: Must be one of "positive", "negative", "edge_case", "irrelevant"
4. target_rule_ids: Which rules from the Logic Map this scenario tests
5. expected_outcome: What the correct response should do based on the rules

CRITICAL - DIVERSITY:
- Each scenario within a type should test DIFFERENT rules or rule combinations
- Vary user tone (formal, casual, frustrated, confused)
- Vary complexity (simple single-rule to multi-rule scenarios)
- Avoid repetitive patterns

CRITICAL - DESCRIPTION VS CONTEXT:
- Description = what the user says (includes their own details: amounts, dates, receipts)
- Context = what the user doesn't know or hasn't stated (policy implications, rule triggers, background)
- The assistant should NOT need to ask for information the user already provided

BAD EXAMPLE:
  description: "I'd like to submit an expense for a client lunch"
  context: "Expense amount: $180, Purchase date: 5 days ago, Has digital receipt, Has manager approval"

GOOD EXAMPLE:
  description: "I need to expense a $180 client lunch from last Tuesday. I have the digital receipt and my manager already approved it."
  context: "Amount falls in $100-$500 tier (R024). Within 30-day submission window. All procedural requirements met."

══════════════════════════════════════════════════════════════════════════════
FINAL REMINDER - DISTRIBUTION IS MANDATORY:
══════════════════════════════════════════════════════════════════════════════
You MUST generate:
  • EXACTLY {positive_count} with scenario_type="positive"
  • EXACTLY {negative_count} with scenario_type="negative"
  • EXACTLY {edge_case_count} with scenario_type="edge_case"
  • EXACTLY {irrelevant_count} with scenario_type="irrelevant"

Generate all {total_count} scenarios now with the EXACT distribution above."""


# =============================================================================
# STAGE 3: TRACE SYNTHESIS (The Thinker)
# =============================================================================

GOLDEN_TRACE_PROMPT = """You are a customer support agent generating a response with explicit reasoning.

POLICY DOCUMENT:
{policy_text}

LOGIC MAP (Rules to Apply):
{logic_map}

SCENARIO:
{scenario_description}

CONTEXT:
{scenario_context}

TARGET RULES: {target_rule_ids}
SCENARIO TYPE: {scenario_type}
EXPECTED OUTCOME: {expected_outcome}

YOUR TASK:
Generate a response with GROUNDED Chain-of-Thought reasoning.

CHAIN-OF-THOUGHT REQUIREMENTS:
1. For EACH relevant rule in the Logic Map:
   - State the rule (with Rule ID)
   - Evaluate whether it applies to this scenario
   - Explain WHY it applies or doesn't apply
   - If it doesn't apply, list which rules are EXCLUDED as a result

2. Follow the dependency order:
   - Evaluate root rules first
   - Then evaluate dependent rules only if their dependencies are satisfied

3. Be EXPLICIT about exclusions:
   - When a rule doesn't apply, state "R00X does NOT apply because..."
   - This prevents hallucination of non-applicable rules

RESPONSE REQUIREMENTS:
- messages: The conversation (system, user, assistant)
- reasoning_chain: Step-by-step reasoning with Rule IDs
- rules_applied: List of Rule IDs that were applied
- rules_excluded: List of Rule IDs that were explicitly excluded

CRITICAL - MESSAGE CONSTRUCTION RULES:

USER MESSAGE:
- Contains the scenario_description — the user's realistic request with natural detail
- Users naturally include relevant details (amounts, dates, items) when asking questions
- Should read as a complete request from someone who knows their own situation

ASSISTANT MESSAGE:
- Respond with substantive policy analysis based on what the user stated
- Give a clear determination: approved, denied, needs a specific additional step, etc.
- Only ask for information that is genuinely missing AND needed for a decision
- Do NOT ask for information the user already provided
- Use CONTEXT for additional reasoning depth, not as hidden info to "discover"
- Vary response style naturally:
  * Some responses should be conversational and flowing prose
  * Some should use brief structured points
  * Some should be direct and concise (2-3 sentences)
  * NEVER use the same bullet-list-of-rules template every time
- Reference policy rules naturally — don't mechanically list every applicable rule

EXAMPLE:
  User says: "I need to expense a $180 client lunch from last Tuesday. I have the receipt and my manager signed off."
  Context: "Amount is in $100-$500 tier. Within 30-day window. All requirements met."

  GOOD response: "You're all set. The $180 is within the client meal limit, you've got the receipt, and manager approval covers this tier. Go ahead and submit it through the portal."
  BAD response: "I can help with that! Could you tell me the amount and whether you have a receipt?"
  BAD response: "Let me check each rule: R001 states... R015 requires... R016 mandates..."

The assistant response should:
- Be professional and helpful
- Reference the policy naturally (without exposing Rule IDs to user)
- Provide clear next steps or explanations
- Match response depth to question complexity (simple question = short answer)"""


GOLDEN_TRACE_MULTI_TURN_PROMPT = """You are a customer support agent generating a multi-turn conversation with explicit reasoning.

POLICY DOCUMENT:
{policy_text}

LOGIC MAP (Rules to Apply):
{logic_map}

INITIAL SCENARIO:
{scenario_description}

CONTEXT:
{scenario_context}

TARGET RULES: {target_rule_ids}
SCENARIO TYPE: {scenario_type}
TARGET TURNS: {target_turns}

YOUR TASK:
Generate a {target_turns}-turn conversation where:
- Turn 1: Address the initial query with grounded reasoning
- Subsequent turns: Handle follow-up questions that probe deeper into the policy

MULTI-TURN GUIDELINES:
1. Each assistant response should have its own reasoning chain
2. Turn 1: User provides a specific request → Assistant gives substantive policy analysis
3. Subsequent turns: User explores variations, edge cases, challenges, or related scenarios
4. NEVER waste a turn on basic information gathering
5. Every turn should teach something new about the policy
6. Maintain context consistency across turns
7. Each turn should cite relevant Rule IDs in its reasoning

CRITICAL - MESSAGE CONSTRUCTION RULES:

TURN 1 - USER MESSAGE:
- Contains the scenario_description — the user's realistic, specific request
- Users naturally include relevant details when asking questions

TURN 1 - ASSISTANT MESSAGE:
- Respond with substantive policy analysis based on what the user stated
- Give a clear determination, not just "I can help! What's the amount?"
- Use CONTEXT for reasoning depth

SUBSEQUENT TURNS:
- User follow-ups explore variations, edge cases, what-ifs, or challenges
- Each follow-up should test a DIFFERENT aspect than previous turns
- Assistant can build on established context across turns

GOOD MULTI-TURN FLOW:
  Turn 1 User: "I need to expense a $180 client lunch from last Tuesday. I have the receipt and my manager approved it."
  Turn 1 Assistant: "You're good to go. The $180 is within the client meal limit, your receipt satisfies the documentation requirement, and manager approval covers the $100-$500 range. Submit it through the expense portal."
  Turn 2 User: "What if I wanted to add a $50 tip to that? Does the limit still apply?"
  Turn 2 Assistant: "Tips count toward the total. At $230 you're still under the $300 per-person cap for client meals, so it's covered. Just make sure the receipt shows the tip."
  Turn 3 User: "My colleague was at the lunch too. Can I submit for both of us?"
  Turn 3 Assistant: "The $300 limit is per person, so you'd be at $115 each — well within range. You can submit for both, but note both attendees on the expense report."

BAD MULTI-TURN FLOW:
  Turn 1 User: "I need to submit an expense"
  Turn 1 Assistant: "I can help! What type of expense and the amount?"
  Turn 2 User: "It's a client lunch for $180"
  Turn 2 Assistant: "For $180, you'll need manager approval. Do you have a receipt?"
  ← Two turns wasted collecting basic facts

CONVERSATION VARIATION:
- Vary user personality: formal professional, casual, frustrated, confused, time-pressured
- Vary follow-up types: what-if, challenge ("that doesn't sound right"), related scenario, edge case, policy clarification
- Some users should be confrontational, some cooperative, some confused
- Vary assistant tone to match: empathetic with frustrated users, efficient with busy ones
- AVOID having every trace follow the same conversation arc

The final output should include:
- Complete conversation messages
- Reasoning chain for EACH assistant turn
- Cumulative rules_applied and rules_excluded"""


# =============================================================================
# STAGE 4: VERIFICATION (The Auditor)
# =============================================================================

VERIFICATION_PROMPT = """You are a verification system checking if a generated trace correctly applies the policy rules.

LOGIC MAP (Ground Truth):
{logic_map}

SCENARIO:
Type: {scenario_type}
Description: {scenario_description}
Target Rules: {target_rule_ids}
Expected Outcome: {expected_outcome}

GENERATED TRACE:
{trace_messages}

REASONING CHAIN PROVIDED:
{reasoning_chain}

RULES CLAIMED APPLIED: {rules_applied}
RULES CLAIMED EXCLUDED: {rules_excluded}

VERIFICATION FOCUS - Check these in order of importance:

1. **Response Correctness** (MOST IMPORTANT):
   - Does the assistant response CORRECTLY apply the policy rules?
   - For POSITIVE scenarios: Response should allow/approve/help
   - For NEGATIVE scenarios: Response should deny/reject/explain why not allowed
   - For EDGE_CASE: Response should handle the boundary appropriately
   - For IRRELEVANT: Response should redirect or explain it's outside policy scope
   - PASS if the response reaches the correct conclusion, even if rule IDs aren't cited

2. **Policy Accuracy**:
   - Does the response accurately reflect what the policy says?
   - Are the conditions and actions correctly described?
   - FAIL only if the response contradicts or misrepresents the policy

3. **No Hallucination**:
   - Does the response invent rules that don't exist?
   - Does the response cite incorrect thresholds or conditions?
   - FAIL only if made-up information is presented as policy

4. **Professional Quality**:
   - Is the response helpful and professional?
   - Does it provide clear guidance to the user?
   - Minor tone issues should NOT cause failure

IMPORTANT GUIDELINES:
- The assistant does NOT need to cite rule IDs (R001, R002) to pass - users don't see rule IDs
- Focus on whether the SUBSTANCE of the response is correct
- If reasoning_chain is "Not provided", evaluate based on the assistant's response content
- A trace should PASS if it gives the correct guidance, even without explicit rule citations
- Be lenient on formatting; be strict on correctness

OUTPUT:
- passed: true/false (true if response is substantively correct)
- issues: List of actual problems (not just missing citations)
- skipped_rules: Rules that were INCORRECTLY ignored (content-wise, not citation-wise)
- hallucinated_rules: Made-up rules or incorrect policy information
- contradictions: Logical contradictions in the response
- rules_verified: Rules correctly reflected in the response content
- feedback: Summary focusing on content correctness"""


# =============================================================================
# GOLDEN REFINEMENT
# =============================================================================

GOLDEN_REFINE_PROMPT = """You are refining a trace that failed verification.

ORIGINAL TRACE:
{original_trace}

VERIFICATION FAILURE:
{verification_result}

LOGIC MAP (Ground Truth):
{logic_map}

SCENARIO:
{scenario_description}

ISSUES TO FIX:
- Skipped Rules: {skipped_rules}
- Hallucinated Rules: {hallucinated_rules}
- Contradictions: {contradictions}

YOUR TASK:
Generate a CORRECTED trace that:
1. Addresses ALL skipped rules in the reasoning chain
2. Removes references to hallucinated rules
3. Resolves all contradictions
4. Follows the DAG dependency order
5. Produces a response that matches the reasoning

REQUIREMENTS:
- Include complete reasoning_chain covering all target rules
- Ensure rules_applied only contains actually applicable rules
- Maintain professional, helpful tone in response
- Preserve the scenario context"""


# =============================================================================
# TOOL CALL SPECIFIC PROMPTS
# =============================================================================

GOLDEN_TOOL_TRACE_PROMPT = """You are a customer support agent with tools, generating a response with explicit reasoning.

POLICY DOCUMENT:
{policy_text}

LOGIC MAP (Rules to Apply):
{logic_map}

AVAILABLE TOOLS:
{tools_description}

SCENARIO:
{scenario_description}

CONTEXT:
{scenario_context}

TARGET RULES: {target_rule_ids}
SCENARIO TYPE: {scenario_type}

YOUR TASK:
Generate a response that may use tools, with GROUNDED reasoning.

TOOL USAGE REASONING:
When deciding whether to call a tool:
1. Reference which RULE requires this information
2. Explain why the tool is necessary to evaluate the rule
3. State what you expect to learn from the tool call

Example reasoning:
"To evaluate R002 (verify purchase date), I need the order details.
Calling get_order(order_id) to retrieve purchase date.
This will determine if the 30-day window applies."

RESPONSE STRUCTURE:
1. Reasoning chain with tool decisions tied to rules
2. Tool calls (if needed) with rule citations
3. Final response synthesizing tool results
4. rules_applied and rules_excluded lists

CRITICAL - MESSAGE CONSTRUCTION RULES:

USER MESSAGE:
- Contains the scenario_description — the user's realistic request with natural detail
- Should read as a complete request, not a vague opener

ASSISTANT MESSAGE:
- Respond substantively based on what the user stated
- Use CONTEXT for reasoning but don't ask for details the user already provided
- Tool calls should gather information that neither user nor context provides

The trace should include:
- System message with tool descriptions
- User message (scenario_description ONLY)
- Assistant message (with tool_calls if needed)
- Tool response messages (if tools were called)
- Final assistant response"""


__all__ = [
    "LOGIC_EXTRACTION_PROMPT",
    "GOLDEN_SCENARIO_PROMPT",
    "GOLDEN_SCENARIO_BATCHED_PROMPT",
    "POSITIVE_SCENARIO_INSTRUCTIONS",
    "NEGATIVE_SCENARIO_INSTRUCTIONS",
    "EDGE_CASE_SCENARIO_INSTRUCTIONS",
    "IRRELEVANT_SCENARIO_INSTRUCTIONS",
    "GOLDEN_TRACE_PROMPT",
    "GOLDEN_TRACE_MULTI_TURN_PROMPT",
    "VERIFICATION_PROMPT",
    "GOLDEN_REFINE_PROMPT",
    "GOLDEN_TOOL_TRACE_PROMPT",
]
