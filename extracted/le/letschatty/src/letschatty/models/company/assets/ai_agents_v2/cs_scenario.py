"""CSScenarioComponent — recipe for how the CS PGP handles a conversation pattern.

A CS scenario is an ai_component subtype that bundles three things into one
record:

1. A retrieval-recipe override (what to load into the prompt — top-K, threshold,
   asset-type whitelists).
2. A workflow-routing override (which N8N webhook URL to hit, optional MCP tool
   whitelist).
3. A behavioural override (what's allowed / required: forbid actions, force
   pre-flight summaries, queue all creates, etc.) plus extra instructions.

The CS-specific tagger (`pgp-implementator-tagger-cs`) matches the user's
intent against scenarios via embedding similarity and stamps
``metadata.matched_scenarios: list[{scenario_id, confidence}]`` (top-K with
merge — see the design spec at
``cintia-lambdas/docs/superpowers/specs/2026-04-30-cs-scenarios-architecture.md``).
The CS PGP merges the matched scenarios' configs and uses the result to
configure the Anthropic call.

``examples`` are references to real ``CintiaExecution`` records — promoted
either by an operator or auto-promoted on positive feedback. They render in
the system prompt as worked examples. Negative-feedback can flip
``CSScenarioExample.suppressed`` so the prompt builder skips that example.
"""

from datetime import datetime
from typing import ClassVar, Literal, Optional, Type

from pydantic import BaseModel, Field, model_validator

from letschatty.models.base_models.ai_agent_component import (
    AiAgentComponent,
    AiAgentComponentPreview,
    AiAgentComponentType,
)
from letschatty.models.company.assets.embeddable import build_chunks


# Whitelist of n8n hosts that ``CSScenarioConfig.n8n_webhook_url`` may target.
# Any other host raises a ValueError at model construction time. Locked down to
# stop a backoffice editor from pointing scenarios at attacker-controlled URLs.
_ALLOWED_N8N_URL_PREFIX = "https://n8n.letschatty.com/"

# Ceiling on examples per scenario to keep the rendered prompt bounded.
_MAX_EXAMPLES_PER_SCENARIO = 50

# Bounds for top_k_overrides values. Above 50 the prompt blows up; below 1 is
# meaningless ("load zero of these").
_TOP_K_MIN = 1
_TOP_K_MAX = 50

_VALID_FORBIDDEN_ACTIONS = {"create", "update", "delete"}


class CSScenarioConfig(BaseModel):
    """Recipe attribute on ``CSScenarioComponent``.

    All fields are independently mergeable across multiple matched scenarios.
    See the merge table in the design doc — retrieval is permissive (UNION /
    MAX / MIN-threshold) and execution is restrictive (UNION of forbids,
    OR-of-restrictive-flags).
    """

    # — Retrieval recipe —
    asset_types_to_force_top_k: list[str] = Field(
        default_factory=list,
        description=(
            "Asset types the system loads at top-K regardless of similarity "
            "threshold when this scenario activates."
        ),
    )
    top_k_overrides: dict[str, int] = Field(
        default_factory=dict,
        description="Per-asset-type top-K override (e.g. {'product': 15}).",
    )
    threshold_overrides: dict[str, float] = Field(
        default_factory=dict,
        description="Per-asset-type similarity-threshold override (0.0–1.0).",
    )
    fallback_to_top_k_overrides: dict[str, bool] = Field(
        default_factory=dict,
        description=(
            "Per-asset-type override for ``CintiaConfig.embedding_fallback_to_top_k``."
        ),
    )

    # — Workflow routing —
    n8n_webhook_url: Optional[str] = Field(
        default=None,
        description=(
            "Override the PGP-level N8N webhook URL when this scenario "
            "activates. Must start with the n8n.letschatty.com host."
        ),
    )
    available_mcp_tools: Optional[list[str]] = Field(
        default=None,
        description=(
            "Whitelist of MCP tools the AI can call when this scenario "
            "activates and the workflow uses MCP. ``None`` = no restriction."
        ),
    )

    # — Behavioural —
    forbid_actions: list[Literal["create", "update", "delete"]] = Field(
        default_factory=list,
        description=(
            "Action verbs the AI must not auto-execute on Tier-B; they queue "
            "as suggested_actions for human review."
        ),
    )
    require_pre_flight_summary: bool = Field(
        default=False,
        description=(
            "Make the AI describe its plan before proposing any actions."
        ),
    )
    queue_all_creates: bool = Field(
        default=False,
        description=(
            "Override Tier-B auto-execute for ``create`` actions; queue for "
            "review instead."
        ),
    )
    expected_action_count: Optional[tuple[int, int]] = Field(
        default=None,
        description=(
            "Soft hint to the AI for how many actions a typical resolution "
            "needs (min, max). Surfaced in the prompt."
        ),
    )

    # — Prompt augmentation —
    extra_instructions: Optional[str] = Field(
        default=None,
        description="Free-text instructions appended when this scenario matches.",
    )

    @model_validator(mode="after")
    def _validate_n8n_webhook_url(self) -> "CSScenarioConfig":
        if self.n8n_webhook_url is not None:
            if not self.n8n_webhook_url.startswith(_ALLOWED_N8N_URL_PREFIX):
                raise ValueError(
                    "n8n_webhook_url must start with "
                    f"{_ALLOWED_N8N_URL_PREFIX!r}"
                )
        return self

    @model_validator(mode="after")
    def _validate_top_k_overrides(self) -> "CSScenarioConfig":
        for asset_type, k in self.top_k_overrides.items():
            if not isinstance(k, int) or isinstance(k, bool):
                raise ValueError(
                    f"top_k_overrides[{asset_type!r}] must be an int, got "
                    f"{type(k).__name__}"
                )
            if k < _TOP_K_MIN or k > _TOP_K_MAX:
                raise ValueError(
                    f"top_k_overrides[{asset_type!r}]={k} out of range "
                    f"[{_TOP_K_MIN}, {_TOP_K_MAX}]"
                )
        return self

    @model_validator(mode="after")
    def _validate_threshold_overrides(self) -> "CSScenarioConfig":
        for asset_type, t in self.threshold_overrides.items():
            if isinstance(t, bool) or not isinstance(t, (int, float)):
                raise ValueError(
                    f"threshold_overrides[{asset_type!r}] must be a number, got "
                    f"{type(t).__name__}"
                )
            if t < 0.0 or t > 1.0:
                raise ValueError(
                    f"threshold_overrides[{asset_type!r}]={t} out of range [0.0, 1.0]"
                )
        return self


class CSScenarioExample(BaseModel):
    """Reference to a real ``CintiaExecution`` promoted as a worked example.

    Manual examples (``is_manual=True``) are picked by an operator from the
    backoffice. Auto-promoted examples are appended on positive feedback
    (rating >= 4). Negative feedback flips ``suppressed=True`` so the prompt
    builder skips them.
    """

    cintia_execution_id: str = Field(
        description="ObjectId (string) of the source CintiaExecution."
    )
    is_manual: bool = Field(
        default=False,
        description=(
            "True when an operator hand-picked this example; False when "
            "auto-promoted from feedback."
        ),
    )
    promoted_at: datetime = Field(
        description="When this example was added to the scenario."
    )
    promoted_by: Optional[str] = Field(
        default=None,
        description=(
            "Operator user_id (manual) or ``'auto:feedback'`` (auto-promoted)."
        ),
    )
    feedback_rating: Optional[int] = Field(
        default=None,
        description=(
            "If auto-promoted: the rating that triggered promotion (1–5). "
            "None for manual examples."
        ),
    )
    notes: Optional[str] = Field(
        default=None,
        description="Optional backoffice annotation visible to operators only.",
    )
    suppressed: bool = Field(
        default=False,
        description=(
            "Set when negative feedback later landed on the same execution; "
            "the prompt builder skips suppressed examples."
        ),
    )


class CSScenarioComponent(AiAgentComponent):
    """An ai_component that configures the CS PGP for a conversation pattern.

    See the module docstring for the full architecture. Stored in the
    ``ai_components`` collection alongside other ``AiAgentComponent``
    subtypes (Context, ChatExample, Instruction, FastAnswerReference,
    TagReference). Discriminated by ``type="cs_scenario"``.
    """

    type: Literal[AiAgentComponentType.CS_SCENARIO] = AiAgentComponentType.CS_SCENARIO
    description: str = Field(
        description=(
            "Human-readable summary of when this scenario applies. Used "
            "both for the embedding query and the backoffice editor."
        )
    )
    enabled: bool = Field(
        default=True,
        description=(
            "Soft toggle; disabled scenarios are not embedded by the worker "
            "and not matched by the tagger."
        ),
    )
    triggers: list[str] = Field(
        default_factory=list,
        description=(
            "Free-text phrases an operator wrote as canonical examples of "
            "when this scenario should fire. Each is embedded independently."
        ),
    )
    config: CSScenarioConfig = Field(
        description="The retrieval / routing / behavioural recipe."
    )
    examples: list[CSScenarioExample] = Field(
        default_factory=list,
        description=(
            "Worked examples the prompt builder hydrates from the referenced "
            "cintia executions. Capped at 50."
        ),
    )

    preview_class: ClassVar[Type[AiAgentComponentPreview]] = AiAgentComponentPreview

    @model_validator(mode="after")
    def _validate_forbid_actions(self) -> "CSScenarioComponent":
        # Literal already enforces this at the type level, but a hand-rolled
        # dict slipping through ``model_validate`` could carry junk; defend.
        for action in self.config.forbid_actions:
            if action not in _VALID_FORBIDDEN_ACTIONS:
                raise ValueError(
                    f"forbid_actions contains invalid value {action!r}; "
                    f"must be one of {sorted(_VALID_FORBIDDEN_ACTIONS)}"
                )
        return self

    @model_validator(mode="after")
    def _validate_examples_cap(self) -> "CSScenarioComponent":
        if len(self.examples) > _MAX_EXAMPLES_PER_SCENARIO:
            raise ValueError(
                f"examples length {len(self.examples)} exceeds cap "
                f"{_MAX_EXAMPLES_PER_SCENARIO}"
            )
        return self

    def embedding_chunks(self) -> list[dict[str, str]]:
        """Compose the chunks the asset-embedding-worker upserts.

        ``name`` and ``description`` go in as ``system_embedding`` chunks;
        each entry of ``triggers`` goes in too. Examples are NOT embedded —
        their text lives on the source CintiaExecution and is hydrated at
        prompt-build time, not at retrieval time.
        """
        fields: dict[str, str] = {
            "name": self.name,
            "description": self.description,
        }
        for idx, trigger in enumerate(self.triggers):
            fields[f"trigger_{idx}"] = trigger
        return build_chunks("cs_scenario", fields)
