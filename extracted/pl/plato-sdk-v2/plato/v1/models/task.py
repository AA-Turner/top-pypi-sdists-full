from collections.abc import Callable
from enum import Enum
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, field_serializer


class ScoringType(str, Enum):
    """Enum for different types of scoring in Plato tasks."""

    OUTPUT = "output"
    MUTATIONS = "mutations"


class BasePlatoEvalConfig(BaseModel):
    """Base configuration class for Plato evaluation settings.

    This class serves as the base configuration for different types of evaluation
    methods in the Plato system.

    Attributes:
        type (Literal["base", "state_mutation_match"]): The type of evaluation configuration.
            Can be either "base" or "state_mutation_match".
    """

    model_config = ConfigDict(arbitrary_types_allowed=True)
    type: Literal["state_mutation_match", "custom"]


class StateMutationMatch(BaseModel):
    tablename: str
    action: Literal["INSERT", "UPDATE", "DELETE"]
    values: dict[str, Any]


class MutationVariable(BaseModel):
    type: Literal["mutation_variable"] = "mutation_variable"
    name: str


class SemanticMatchVariable(BaseModel):
    type: Literal["semantic_match_variable"] = "semantic_match_variable"
    description: str


class EnumMatchVariable(BaseModel):
    type: Literal["enum_match_variable"] = "enum_match_variable"
    values: list[Any]


class StateMutationMatchEvalConfig(BasePlatoEvalConfig):
    """Configuration for state mutation matching evaluation.

    This class defines the configuration for evaluating tasks based on matching
    state mutations. It inherits from BasePlatoEvalConfig and specifies
    state mutations that should be matched during evaluation.

    Attributes:
        type (Literal["state_mutation_match"]): The type of evaluation, fixed as
            "state_mutation_match" for this configuration.
        state_mutations (List[dict]): A list of state mutation specifications that
            define the expected changes in state during task execution.
    """

    type: Literal["state_mutation_match"] = "state_mutation_match"
    mutations: list[StateMutationMatch]


class CustomEvalConfig(BasePlatoEvalConfig):
    """Configuration for custom evaluation.

    This class defines the configuration for custom evaluation of tasks. It inherits from BasePlatoEvalConfig and specifies
    a custom evaluation function that should be used during evaluation.

    Attributes:
        type (Literal["custom"]): The type of evaluation, fixed as "custom" for this configuration.
        custom_eval_function (Callable): A custom evaluation function that should be used during evaluation.
    """

    type: Literal["custom"] = "custom"
    score_fn: Callable

    @field_serializer("score_fn")
    def serialize_score_fn(self, score_fn: Callable, _info):
        return score_fn.__name__


class EvaluationResult(BaseModel):
    """Result of an evaluation containing both success status and reason if failed.

    Attributes:
        success: Whether the evaluation was successful
        reason: If success is False, contains the reason for failure. None if successful.
    """

    success: bool
    reason: str | None = None
    diffs: list[dict[str, Any]] | None = None
    expected_mutations: list[dict[str, Any]] | None = None
    actual_mutations: list[dict[str, Any]] | None = None


class PlatoTaskMetadata(BaseModel):
    """Metadata for a Plato task."""

    reasoning_level: Literal["level_1", "level_2", "level_3", "level_4", "level_5"] | None = None
    skills: list[str] | None = None
    capabilities: list[str] | None = None
    tags: list[str] | None = None
    rejected: bool | None = False


class PlatoTask(BaseModel):
    """Represents a task in the Plato system.

    This class defines the structure of a task, including its name, prompt, and starting URL.
    Tasks are used to specify what actions should be performed in a Plato environment.

    Attributes:
        name (str): The name of the task.
        prompt (str): The prompt describing what should be done in this task.
        start_url (str): The URL where the task should begin execution.
    """

    public_id: str
    name: str
    prompt: str
    env_id: str
    start_url: str
    dataset_name: str | None = None
    eval_config: BasePlatoEvalConfig | None = None
    average_time: float | None = None
    average_steps: int | None = None
    num_validator_human_scores: int | None = None
    default_scoring_config: dict[str, Any] | None = None
    scoring_type: list[ScoringType] = [ScoringType.MUTATIONS]
    output_schema: dict[str, Any] | None = None
    is_sample: bool | None = False
    simulator_artifact_id: str | None = None
    metadata: PlatoTaskMetadata | None = None
    version: int | None = 1

    @field_serializer("eval_config")
    def serialize_eval_config(self, eval_config: BasePlatoEvalConfig | None, _info):
        return eval_config.model_dump() if eval_config else None
