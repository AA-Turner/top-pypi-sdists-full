from typing import Literal, Union

from pydantic import Field
from typing_extensions import Annotated

from galileo_core.schemas.shared.scorers.base_configs import (
    GalileoScorerConfig,
    LunaOrPlusScorerTypeConfig,
    PlusScorerConfig,
    PlusScorerTypeConfig,
    PlusScorerWithNumJudgesConfig,
)
from galileo_core.schemas.shared.scorers.scorer_name import ScorerName
from galileo_core.schemas.shared.scorers.scorer_type import LunaOrPlusScorerType, ScorerType


class AgenticSessionSuccessScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.agentic_session_success] = ScorerName.agentic_session_success
    type: LunaOrPlusScorerType = ScorerType.plus


class AgenticWorkflowSuccessScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.agentic_workflow_success] = ScorerName.agentic_workflow_success
    type: LunaOrPlusScorerType = ScorerType.plus


class BleuScorer(GalileoScorerConfig):
    name: Literal[ScorerName.bleu] = ScorerName.bleu


class ChunkAttributionUtilizationScorer(LunaOrPlusScorerTypeConfig, PlusScorerConfig):
    name: Literal[ScorerName.chunk_attribution_utilization] = ScorerName.chunk_attribution_utilization


class CompletenessScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.completeness] = ScorerName.completeness


class ContextAdherenceScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.context_adherence] = ScorerName.context_adherence


class ContextRelevanceScorer(GalileoScorerConfig):
    name: Literal[ScorerName.context_relevance] = ScorerName.context_relevance


class CorrectnessScorer(PlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.correctness] = ScorerName.correctness


class GroundTruthAdherenceScorer(PlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.ground_truth_adherence] = ScorerName.ground_truth_adherence


class InputPIIScorer(GalileoScorerConfig):
    name: Literal[ScorerName.input_pii] = ScorerName.input_pii


class InputSexistScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.input_sexist] = ScorerName.input_sexist


class InputToneScorer(GalileoScorerConfig):
    name: Literal[ScorerName.input_tone] = ScorerName.input_tone


class InputToxicityScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.input_toxicity] = ScorerName.input_toxicity


class InstructionAdherenceScorer(PlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.instruction_adherence] = ScorerName.instruction_adherence


class OutputPIIScorer(GalileoScorerConfig):
    name: Literal[ScorerName.output_pii] = ScorerName.output_pii


class OutputSexistScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.output_sexist] = ScorerName.output_sexist


class OutputToneScorer(GalileoScorerConfig):
    name: Literal[ScorerName.output_tone] = ScorerName.output_tone


class OutputToxicityScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.output_toxicity] = ScorerName.output_toxicity


class PromptInjectionScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.prompt_injection] = ScorerName.prompt_injection


class PromptPerplexityScorer(GalileoScorerConfig):
    name: Literal[ScorerName.prompt_perplexity] = ScorerName.prompt_perplexity


class RougeScorer(GalileoScorerConfig):
    name: Literal[ScorerName.rouge] = ScorerName.rouge


class ToolSelectionQualityScorer(LunaOrPlusScorerTypeConfig, PlusScorerWithNumJudgesConfig):
    name: Literal[ScorerName.tool_selection_quality] = ScorerName.tool_selection_quality
    type: LunaOrPlusScorerType = ScorerType.plus


class ToolErrorRateScorer(LunaOrPlusScorerTypeConfig, PlusScorerConfig):
    name: Literal[ScorerName.tool_error_rate] = ScorerName.tool_error_rate
    type: LunaOrPlusScorerType = ScorerType.plus


class UncertaintyScorer(GalileoScorerConfig):
    name: Literal[ScorerName.uncertainty] = ScorerName.uncertainty


GalileoScorersUnion = Union[
    AgenticWorkflowSuccessScorer,
    AgenticSessionSuccessScorer,
    BleuScorer,
    ChunkAttributionUtilizationScorer,
    CompletenessScorer,
    ContextAdherenceScorer,
    ContextRelevanceScorer,
    CorrectnessScorer,
    GroundTruthAdherenceScorer,
    InputPIIScorer,
    InputSexistScorer,
    InputToneScorer,
    InputToxicityScorer,
    InstructionAdherenceScorer,
    OutputPIIScorer,
    OutputSexistScorer,
    OutputToneScorer,
    OutputToxicityScorer,
    PromptInjectionScorer,
    PromptPerplexityScorer,
    RougeScorer,
    ToolErrorRateScorer,
    ToolSelectionQualityScorer,
    UncertaintyScorer,
]


GalileoScorer = Annotated[
    GalileoScorersUnion,
    Field(discriminator="name"),
]
