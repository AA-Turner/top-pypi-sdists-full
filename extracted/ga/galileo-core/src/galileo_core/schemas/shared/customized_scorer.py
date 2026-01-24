from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CustomizedScorerName(str, Enum):
    action_advancement = "_customized_agentic_workflow_success"
    action_completion = "_customized_agentic_session_success"
    chunk_attribution_utilization_plus = "_customized_chunk_attribution_utilization_gpt"
    completeness_plus = "_customized_completeness_gpt"
    context_adherence_plus = "_customized_groundedness"
    correctness = "_customized_factuality"
    ground_truth_adherence = "_customized_ground_truth_adherence"
    instruction_adherence = "_customized_instruction_adherence"
    prompt_injection_plus = "_customized_prompt_injection_gpt"
    tool_errors = "_customized_tool_error_rate"
    tool_selection_quality = "_customized_tool_selection_quality"
    sexist_plus = "_customized_sexist_gpt"
    input_sexist_plus = "_customized_input_sexist_gpt"
    toxicity_plus = "_customized_toxicity_gpt"
    input_toxicity_plus = "_customized_input_toxicity_gpt"


class CustomizedScorer(BaseModel):
    scorer_name: CustomizedScorerName = Field(..., description="Name of the customized scorer.")
    model_alias: Optional[str] = Field(default=None, description="Model alias to use for scoring.")
    num_judges: Optional[int] = Field(default=None, ge=1, le=10, description="Number of judges for the scorer.")

    model_config = ConfigDict(
        # Avoid Pydantic's protected namespace warning since we want to use
        # `model_alias` as a field name.
        protected_namespaces=(),
    )
