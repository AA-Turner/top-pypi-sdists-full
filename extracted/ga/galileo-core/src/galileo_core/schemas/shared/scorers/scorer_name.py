from enum import Enum
from typing import Dict


# In python, if multiple enum members have the same value, the first one is the "canonical" one.
# Secondary aliases must come after the canonical one.
# Reference: https://docs.python.org/3.10/library/enum.html#duplicating-enum-members-and-values
class ScorerName(str, Enum):
    action_completion_luna = "action_completion_luna"

    action_advancement_luna = "action_advancement_luna"

    agentic_session_success = "agentic_session_success"
    action_completion = "agentic_session_success"

    agentic_workflow_success = "agentic_workflow_success"
    action_advancement = "agentic_workflow_success"

    agent_efficiency = "agent_efficiency"

    agent_flow = "agent_flow"

    bleu = "bleu"

    chunk_attribution_utilization_luna = "chunk_attribution_utilization_luna"

    chunk_attribution_utilization = "chunk_attribution_utilization"

    completeness_luna = "completeness_luna"

    completeness = "completeness"

    context_adherence = "context_adherence"

    context_adherence_luna = "context_adherence_luna"

    context_relevance = "context_relevance"

    context_relevance_luna = "context_relevance_luna"

    conversation_quality = "conversation_quality"

    correctness = "correctness"

    ground_truth_adherence = "ground_truth_adherence"

    input_pii = "input_pii"
    input_pii_gpt = "input_pii_gpt"

    input_sexist = "input_sexist"
    input_sexism = "input_sexist"

    input_sexist_luna = "input_sexist_luna"
    input_sexism_luna = "input_sexist_luna"

    input_tone = "input_tone"
    input_tone_gpt = "input_tone_gpt"

    input_toxicity = "input_toxicity"

    input_toxicity_luna = "input_toxicity_luna"

    instruction_adherence = "instruction_adherence"

    output_pii = "output_pii"
    output_pii_gpt = "output_pii_gpt"

    output_sexist = "output_sexist"
    output_sexism = "output_sexist"

    output_sexist_luna = "output_sexist_luna"
    output_sexism_luna = "output_sexist_luna"

    output_tone = "output_tone"
    output_tone_gpt = "output_tone_gpt"

    output_toxicity = "output_toxicity"

    output_toxicity_luna = "output_toxicity_luna"

    prompt_injection = "prompt_injection"

    prompt_injection_luna = "prompt_injection_luna"

    prompt_perplexity = "prompt_perplexity"

    rouge = "rouge"

    reasoning_coherence = "reasoning_coherence"

    sql_efficiency = "sql_efficiency"

    sql_adherence = "sql_adherence"

    sql_injection = "sql_injection"

    sql_correctness = "sql_correctness"

    tool_error_rate = "tool_error_rate"

    tool_error_rate_luna = "tool_error_rate_luna"

    tool_selection_quality = "tool_selection_quality"

    tool_selection_quality_luna = "tool_selection_quality_luna"

    uncertainty = "uncertainty"

    user_intent_change = "user_intent_change"


LegacyGPTScorerNameMapping: Dict[str, ScorerName] = {
    "agentic_session_success_gpt": ScorerName.agentic_session_success,
    "agentic_workflow_success_gpt": ScorerName.agentic_workflow_success,
    "chunk_attribution_utilization_gpt": ScorerName.chunk_attribution_utilization,
    "completeness_gpt": ScorerName.completeness,
    "context_adherence_gpt": ScorerName.context_adherence,
    "input_sexist_gpt": ScorerName.input_sexist,
    "input_toxicity_gpt": ScorerName.input_toxicity,
    "output_sexist_gpt": ScorerName.output_sexist,
    "output_toxicity_gpt": ScorerName.output_toxicity,
    "prompt_injection_gpt": ScorerName.prompt_injection,
    "tool_error_rate_gpt": ScorerName.tool_error_rate,
    "tool_selection_quality_gpt": ScorerName.tool_selection_quality,
}
