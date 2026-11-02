"""Server data-event render-block vocabulary — the generator source of truth.

These are the render-block WRAPPERS the frontend synthesizes when it converts a
``data`` stream event (or an FE-internal parse state, for ``search_replace``)
into a renderable block. They are NOT ``render_block`` wire events — the wire
payloads are the typed data models in ``data_types.py`` (``DATA_TYPE_REGISTRY``)
— but the wrapper vocabulary is platform contract: the frontend's block
pipeline (SplitterBlock / BlockRenderer) types against it.

Historically this vocabulary was hand-maintained in matrx-frontend
``types/python-generated/missing-types.ts`` ("temporary patch" file). It is now
generated: ``scripts/generate_types.py`` reads ``DATA_EVENT_RENDER_BLOCKS`` and
emits one interface per entry plus classification-grouped unions into
``stream-events.ts``. Adding a data event the FE renders as a block means
adding a row HERE, never editing the generated TS.

Classification law (Content IR Wave 1, common-docs/systems/architecture/content-ir/FEATURE.md):
every entry carries the classification ratified by the frontend content-vocab
crosswalk (matrx-frontend ``scripts/shape/content-vocab-crosswalk.json``; the
authority is ``scripts/shape/generate-content-vocab-crosswalk.ts``'s rule
tables). The crosswalk check FAILS if this table and the crosswalk disagree —
protocol/lifecycle events are generated into a distinct protocol union and are
never silently mixed into Shape blocks.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field

# ---------------------------------------------------------------------------
# Wrapper-specific data models (no wire twin in DATA_TYPE_REGISTRY)
# ---------------------------------------------------------------------------


class SearchReplaceRenderData(BaseModel):
    """FE parse state for a streamed search/replace edit operation.

    camelCase by contract: this shape is produced and consumed entirely by the
    frontend's search/replace block parser; Python only owns the vocabulary so
    the generated union is complete.
    """

    search: str
    replace: str
    searchComplete: bool
    replaceComplete: bool
    isComplete: bool
    language: str | None = None


class DirectiveReceiptRenderData(BaseModel):
    """THE RECEIPT CARD's payload — what a directive apply actually did (DD-118).

    A side-effect Kind Directive used to leave nothing on the timeline but the
    re-rendered request: applied, deduped, and merely proposed all looked the
    same. The receipt events (``directive_apply.*``) carry the outcome AND the
    server-authored sentence, and the frontend synthesizes one block per receipt
    from them.

    ``message`` is NEVER composed client-side. Only the server knows whether the
    ledger replayed, what the write-tree touched, or what the handler called it —
    a client sentence would be a guess wearing a receipt's clothes.
    """

    #: The directive SLUG — the one identity (`directive_v1_action_plan_tree`).
    directive: str
    #: Which of the outcomes this is. Distinct values, distinct sentences.
    outcome: Literal[
        "proposed", "applied", "already_applied", "failed", "blocked", "pending"
    ]
    #: The server's own sentence, rendered verbatim.
    message: str
    #: What was written, for linking. Empty on a proposal, a failure, a block.
    resource_kind: str = ""
    resource_ids: list[str] = Field(default_factory=list)


class UnknownDataEventData(BaseModel):
    """Deliberate catch-all for unrecognized server data events.

    ``_dataType`` preserves the original wire ``type`` string; everything else
    passes through untyped (intentionally opaque by design).
    """

    model_config = ConfigDict(extra="allow", populate_by_name=True)

    data_type: str = Field(alias="_dataType")


# ---------------------------------------------------------------------------
# The vocabulary table
# ---------------------------------------------------------------------------

DataRenderBlockClassification = Literal[
    "protocol", "scalar_generic", "shape", "intentionally_opaque"
]


@dataclass(frozen=True)
class DataEventRenderBlock:
    """One FE-synthesized render-block wrapper over a data event."""

    block_type: str
    # TS interface name of the wrapper's `data` field (must be emitted earlier
    # in stream-events.ts — a DATA_TYPE_REGISTRY model, a value-store event
    # model, or one of the wrapper-specific models above).
    data_interface: str
    # DATA_TYPE_REGISTRY key backing this wrapper (generation-time validation
    # that data_interface matches the registered model); None when the data
    # shape is not a `type`-discriminated data event (value-store events are
    # `kind`-discriminated; search_replace/unknown_data_event are FE-owned).
    registry_type: str | None
    classification: DataRenderBlockClassification
    doc: str
    # `content` field: "text" → `content: string`; "always_null" → `content: null`
    # (a non-null content would leak into committed message parts — see the FE's
    # assembleMessageParts Pass 2).
    content: Literal["text", "always_null"] = "text"
    data_required: bool = True


DATA_EVENT_RENDER_BLOCKS: tuple[DataEventRenderBlock, ...] = (
    # ── scalar_generic — generated-media delivery blocks (media primitives) ──
    DataEventRenderBlock(
        block_type="audio_output",
        data_interface="AudioOutputData",
        registry_type="audio_output",
        classification="scalar_generic",
        doc="Audio output from the AI (TTS or file).",
    ),
    DataEventRenderBlock(
        block_type="image_output",
        data_interface="ImageOutputData",
        registry_type="image_output",
        classification="scalar_generic",
        doc=(
            "Image output from the AI. Display priority: cdn_url → file handler "
            "(via file_id) → url (durable)."
        ),
    ),
    DataEventRenderBlock(
        block_type="video_output",
        data_interface="VideoOutputData",
        registry_type="video_output",
        classification="scalar_generic",
        doc="Video output from the AI.",
    ),
    # ── shape — typed server result displays (registered kind or candidate) ──
    DataEventRenderBlock(
        block_type="search_results",
        data_interface="SearchResultsData",
        registry_type="search_results",
        classification="shape",
        doc="Web search results block — registered kind `search_results` (inactive; data-event arrival unchanged).",
    ),
    DataEventRenderBlock(
        block_type="fetch_results",
        data_interface="FetchResultsData",
        registry_type="fetch_results",
        classification="shape",
        doc="URL fetch results block — registered kind `fetch_results` (inactive; data-event arrival unchanged).",
    ),
    DataEventRenderBlock(
        block_type="categorization_result",
        data_interface="CategorizationResultData",
        registry_type="categorization_result",
        classification="shape",
        doc="Prompt categorization result — registered kind `categorization_result` (inactive; data-event arrival unchanged).",
    ),
    DataEventRenderBlock(
        block_type="decision_answers",
        data_interface="DecisionAnswersData",
        registry_type="decision_answers",
        classification="shape",
        doc=(
            "A decision turn's answers — registered kind `decision_answers`. The "
            "LIVE arrival of the same part the assistant message persists, so a "
            "runner or a battle column shows the decision as it lands instead of "
            "only after a reload. `content` is null: the frontend commits the "
            "payload as a real `decision_answers` message part (the same part the "
            "server persists), never as reconstructed markdown."
        ),
        content="always_null",
    ),
    DataEventRenderBlock(
        block_type="display_questionnaire",
        data_interface="QuestionnaireDisplayData",
        registry_type="display_questionnaire",
        classification="shape",
        doc="Questionnaire to display — alias of the registered `questionnaire` kind.",
    ),
    # ── protocol — lifecycle / ack / edit-operation events, never Shapes ──
    DataEventRenderBlock(
        block_type="function_result",
        data_interface="FunctionResultData",
        registry_type="function_result",
        classification="protocol",
        doc="Generic tool-result envelope — payload typing is owned by tool_io contracts.",
    ),
    DataEventRenderBlock(
        block_type="workflow_step",
        data_interface="WorkflowStepData",
        registry_type="workflow_step",
        classification="protocol",
        doc="Workflow progress event.",
    ),
    DataEventRenderBlock(
        block_type="mandate_input_required",
        data_interface="MandateInputRequiredData",
        registry_type="mandate_input_required",
        classification="protocol",
        doc=(
            "A mandate run PARKED for a person's answer — the frontend renders the "
            "server's sentence plus the served inputs as a form whose Continue posts "
            "`POST /mandates/runs/{request_id}/answer` and streams the resumed run. "
            "Until 2026-10-17 it fell to the Unknown Data Event card."
        ),
    ),
    DataEventRenderBlock(
        block_type="search_error",
        data_interface="SearchErrorData",
        registry_type="search_error",
        classification="protocol",
        doc="Web search failure event.",
    ),
    DataEventRenderBlock(
        block_type="structured_input_warning",
        data_interface="StructuredInputWarningData",
        registry_type="structured_input_warning",
        classification="protocol",
        doc="Warning about malformed structured input blocks.",
    ),
    DataEventRenderBlock(
        block_type="podcast_stage",
        data_interface="PodcastStageEvent",
        registry_type="podcast_stage",
        classification="protocol",
        doc="Podcast pipeline lifecycle event (stage finished).",
    ),
    DataEventRenderBlock(
        block_type="podcast_complete",
        data_interface="PodcastCompleteEvent",
        registry_type="podcast_complete",
        classification="protocol",
        doc="Podcast pipeline lifecycle event (generation complete).",
    ),
    DataEventRenderBlock(
        block_type="scrape_batch_complete",
        data_interface="ScrapeBatchCompleteData",
        registry_type="scrape_batch_complete",
        classification="protocol",
        doc="Scrape pipeline lifecycle event.",
    ),
    DataEventRenderBlock(
        block_type="value_store_stored",
        data_interface="ValueStoredEvent",
        registry_type=None,  # kind-discriminated data event, not in DATA_TYPE_REGISTRY
        classification="protocol",
        doc=(
            "Conversation Value Store 'result ready' card — FE-synthesized from the "
            "kind-discriminated value_store.stored data event. Never persisted to "
            "cx_message.content."
        ),
        content="always_null",
    ),
    DataEventRenderBlock(
        block_type="context_groomed",
        data_interface="ContextGroomedEvent",
        registry_type=None,  # kind-discriminated data event, not in DATA_TYPE_REGISTRY
        classification="protocol",
        doc=(
            "Context-groom receipt line — FE-synthesized from the value_store.groomed "
            "data event. Subtle indicator only; never persisted."
        ),
        content="always_null",
    ),
    DataEventRenderBlock(
        block_type="search_replace",
        data_interface="SearchReplaceRenderData",
        registry_type=None,  # FE-owned parse state, no wire data event
        classification="protocol",
        doc="Search-and-replace block for code editing (FE parse state).",
        data_required=False,
    ),
    DataEventRenderBlock(
        block_type="directive_receipt",
        data_interface="DirectiveReceiptRenderData",
        registry_type=None,  # kind-discriminated `directive_apply.*` receipt events
        classification="protocol",
        doc=(
            "Kind Directive apply receipt — FE-synthesized from the "
            "kind-discriminated directive_apply.* events. Carries the SERVER's own "
            "sentence for the outcome (created / already applied / proposed / "
            "failed / blocked); never composed client-side. Never persisted to "
            "cx_message.content."
        ),
        content="always_null",
    ),
    # ── intentionally_opaque ──
    DataEventRenderBlock(
        block_type="unknown_data_event",
        data_interface="UnknownDataEventData",
        registry_type=None,  # by definition: the catch-all for unregistered types
        classification="intentionally_opaque",
        doc=(
            "Fallback for data events whose type is not recognized; _dataType "
            "preserves the original type string."
        ),
    ),
)

# Extra data models the generator must emit before the wrapper interfaces
# (models with no DATA_TYPE_REGISTRY / value-store emission elsewhere).
DATA_RENDER_BLOCK_EXTRA_MODELS: tuple[type[BaseModel], ...] = (
    SearchReplaceRenderData,
    DirectiveReceiptRenderData,
    UnknownDataEventData,
)


def validate_data_event_render_blocks(
    data_type_registry: dict[str, type[Any]],
) -> None:
    """Generation-time drift guard.

    Every entry with a ``registry_type`` must point at the registered model
    whose class name equals its ``data_interface`` — a rename or remap in
    ``DATA_TYPE_REGISTRY`` without a matching edit here fails generation
    loudly instead of emitting a stale union.
    """
    seen: set[str] = set()
    for entry in DATA_EVENT_RENDER_BLOCKS:
        if entry.block_type in seen:
            raise RuntimeError(
                f"DATA_EVENT_RENDER_BLOCKS: duplicate block_type {entry.block_type!r}"
            )
        seen.add(entry.block_type)
        if entry.registry_type is None:
            continue
        model = data_type_registry.get(entry.registry_type)
        if model is None:
            raise RuntimeError(
                f"DATA_EVENT_RENDER_BLOCKS: {entry.block_type!r} claims registry_type "
                f"{entry.registry_type!r} which is not in DATA_TYPE_REGISTRY"
            )
        if model.__name__ != entry.data_interface:
            raise RuntimeError(
                f"DATA_EVENT_RENDER_BLOCKS: {entry.block_type!r} declares data_interface "
                f"{entry.data_interface!r} but DATA_TYPE_REGISTRY[{entry.registry_type!r}] "
                f"is {model.__name__} — update the vocabulary row"
            )
