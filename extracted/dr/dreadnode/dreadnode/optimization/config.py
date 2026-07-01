from __future__ import annotations

import typing as t

from pydantic import BaseModel, ConfigDict, Field

OptimizationBackendName = t.Literal["gepa"]
ReflectionPrompt: t.TypeAlias = str | list[dict[str, t.Any]]
ReflectionLanguageModel: t.TypeAlias = t.Callable[[ReflectionPrompt], str]
ReflectionLM: t.TypeAlias = str | ReflectionLanguageModel


class EngineConfig(BaseModel):
    """Execution settings for the optimization engine."""

    model_config = ConfigDict(extra="forbid")

    run_dir: str | None = None
    seed: int = 0
    display_progress_bar: bool = False
    raise_on_exception: bool = True
    use_cloudpickle: bool = True
    track_best_outputs: bool = False
    max_metric_calls: int | None = 100
    max_candidate_proposals: int | None = None
    val_evaluation_policy: str | None = None
    candidate_selection_strategy: str | None = None
    parallel: bool = True
    max_workers: int | None = None
    cache_evaluation: bool = False
    cache_evaluation_storage: t.Literal["memory", "disk", "auto"] | None = None
    best_example_evals_k: int | None = None
    frontier_type: t.Literal["instance", "objective", "hybrid", "cartesian"] | None = None
    capture_stdio: bool = False
    extra: dict[str, t.Any] = Field(default_factory=dict)

    def to_gepa_kwargs(self) -> dict[str, t.Any]:
        """Return GEPA-compatible keyword arguments for the engine config."""
        kwargs: dict[str, t.Any] = {}
        for key in (
            "run_dir",
            "seed",
            "display_progress_bar",
            "raise_on_exception",
            "use_cloudpickle",
            "track_best_outputs",
            "max_metric_calls",
            "max_candidate_proposals",
            "val_evaluation_policy",
            "candidate_selection_strategy",
            "parallel",
            "max_workers",
            "cache_evaluation",
            "cache_evaluation_storage",
            "best_example_evals_k",
            "frontier_type",
            "capture_stdio",
        ):
            value = getattr(self, key)
            if value is not None:
                kwargs[key] = value
        kwargs.update(self.extra)
        return kwargs


class ReflectionConfig(BaseModel):
    """Reflection-model settings passed through to GEPA."""

    model_config = ConfigDict(extra="forbid")

    skip_perfect_score: bool | None = None
    perfect_score: float | None = None
    batch_sampler: str | None = None
    reflection_minibatch_size: int | None = None
    module_selector: str | None = None
    reflection_lm: ReflectionLM | None = None
    reflection_prompt_template: str | dict[str, str] | None = None
    custom_candidate_proposer: t.Any = None
    extra: dict[str, t.Any] = Field(default_factory=dict)

    def to_gepa_kwargs(self) -> dict[str, t.Any]:
        """Return GEPA-compatible keyword arguments for the reflection config."""
        kwargs: dict[str, t.Any] = {}
        for key in (
            "skip_perfect_score",
            "perfect_score",
            "batch_sampler",
            "reflection_minibatch_size",
            "module_selector",
            "reflection_lm",
            "reflection_prompt_template",
            "custom_candidate_proposer",
        ):
            value = getattr(self, key)
            if value is not None:
                kwargs[key] = value
        kwargs.update(self.extra)
        return kwargs


class MergeConfig(BaseModel):
    """Merge-policy settings for candidate combination."""

    model_config = ConfigDict(extra="forbid")

    max_merge_invocations: int | None = None
    merge_val_overlap_floor: int | None = None
    extra: dict[str, t.Any] = Field(default_factory=dict)

    def to_gepa_kwargs(self) -> dict[str, t.Any]:
        """Return GEPA-compatible keyword arguments for merge settings."""
        kwargs: dict[str, t.Any] = {}
        for key in ("max_merge_invocations", "merge_val_overlap_floor"):
            value = getattr(self, key)
            if value is not None:
                kwargs[key] = value
        kwargs.update(self.extra)
        return kwargs


class RefinerConfig(BaseModel):
    """Candidate-refinement settings for optimize_anything."""

    model_config = ConfigDict(extra="forbid")

    refiner_lm: str | None = None
    max_refinements: int | None = None
    extra: dict[str, t.Any] = Field(default_factory=dict)

    def to_gepa_kwargs(self) -> dict[str, t.Any]:
        """Return GEPA-compatible keyword arguments for refiner settings."""
        kwargs: dict[str, t.Any] = {}
        for key in ("refiner_lm", "max_refinements"):
            value = getattr(self, key)
            if value is not None:
                kwargs[key] = value
        kwargs.update(self.extra)
        return kwargs


class TrackingConfig(BaseModel):
    """Tracing and reflection-data settings for optimization runs."""

    model_config = ConfigDict(extra="forbid")

    capture_traces: bool = True
    include_outputs: bool = True
    include_errors: bool = True
    max_reflection_examples: int = Field(default=10, ge=1)
    max_side_info_chars: int = Field(default=4000, ge=256)
    use_wandb: bool | None = None
    wandb_api_key: str | None = None
    wandb_init_kwargs: dict[str, t.Any] | None = None
    use_mlflow: bool | None = None
    mlflow_tracking_uri: str | None = None
    mlflow_experiment_name: str | None = None
    logger: t.Any = None
    extra: dict[str, t.Any] = Field(default_factory=dict)

    def to_gepa_kwargs(self) -> dict[str, t.Any]:
        """Return GEPA-compatible keyword arguments for tracking settings."""
        kwargs: dict[str, t.Any] = {}
        for key in (
            "use_wandb",
            "wandb_api_key",
            "wandb_init_kwargs",
            "use_mlflow",
            "mlflow_tracking_uri",
            "mlflow_experiment_name",
            "logger",
        ):
            value = getattr(self, key)
            if value is not None:
                kwargs[key] = value
        kwargs.update(self.extra)
        return kwargs


class OptimizationConfig(BaseModel):
    """Top-level configuration for Dreadnode optimize_anything runs."""

    model_config = ConfigDict(extra="forbid")

    backend: OptimizationBackendName = "gepa"
    engine: EngineConfig = Field(default_factory=EngineConfig)
    reflection: ReflectionConfig | None = None
    merge: MergeConfig | None = None
    refiner: RefinerConfig | None = None
    tracking: TrackingConfig = Field(default_factory=TrackingConfig)
    stop_callbacks: t.Any = None
    extra: dict[str, t.Any] = Field(default_factory=dict)
