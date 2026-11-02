"""Typed data payload definitions for the streaming event system.

Every data event MUST use a typed DataPayload subclass with a Literal `type`
field. The DATA_TYPE_REGISTRY maps type names to models so the TS generator
can produce a discriminated union.
"""

from __future__ import annotations

from typing import Annotated, Any, Generic, Literal

from typing_extensions import TypeVar

from pydantic import BaseModel, BeforeValidator, Field, JsonValue, field_validator
from pydantic.json_schema import SkipJsonSchema

from matrx_utils import client_error_text

from matrx_connect.context.media_block import UnifiedMediaBlock


#: The ``__kind`` slot of a stream payload that is NOT a kind (Content IR rule 28): its ``type``
#: discriminates it. A value an older journal row carries is read as ``""``, never written back,
#: and the slot is absent from the published schema.
_NoKindMarker = SkipJsonSchema[Annotated[str, BeforeValidator(lambda _value: "")]]


def _no_kind_marker() -> Any:
    return Field(default="", alias="__kind", serialization_alias="__kind", exclude=True)


PayloadType = TypeVar("PayloadType", bound=str, default=str)


class DataPayload(BaseModel, Generic[PayloadType]):
    model_config = {"extra": "forbid"}
    type: PayloadType


# ---------------------------------------------------------------------------
# Core data types
# ---------------------------------------------------------------------------


class ConversationIdData(DataPayload[Literal["conversation_id"]]):
    type: Literal["conversation_id"] = "conversation_id"
    conversation_id: str


class ClaudeManagedSdkMessageData(DataPayload[Literal["claude_managed_sdk_message"]]):
    """One opaque official Claude Agent SDK message on the managed-runtime wire."""

    type: Literal["claude_managed_sdk_message"] = "claude_managed_sdk_message"
    runtime_id: str
    session_id: str
    sdk_message_type: str
    message: dict[str, JsonValue]


class ClaudeManagedWarningData(DataPayload[Literal["claude_managed_warning"]]):
    """A recoverable managed-runtime warning with stable machine-readable identity."""

    type: Literal["claude_managed_warning"] = "claude_managed_warning"
    code: str
    runtime_id: str
    session_id: str


class AudioOutputData(DataPayload[Literal["audio_output"]]):
    type: Literal["audio_output"] = "audio_output"
    url: str
    mime_type: str
    # cld_files row id — the durable identity; url/cdn_url/download_url
    # are the durable contract (never a signed URL).
    file_id: str | None = None
    cdn_url: str | None = None
    download_url: str | None = None


class ImageOutputData(DataPayload[Literal["image_output"]]):
    type: Literal["image_output"] = "image_output"
    url: str
    mime_type: str
    file_id: str | None = None
    cdn_url: str | None = None
    download_url: str | None = None


class VideoOutputData(DataPayload[Literal["video_output"]]):
    type: Literal["video_output"] = "video_output"
    url: str
    mime_type: str
    file_id: str | None = None
    cdn_url: str | None = None
    download_url: str | None = None


class PartialImageData(DataPayload[Literal["partial_image"]]):
    """Streaming partial image during image generation.

    DEPRECATED — replaced by ``MediaBlockData(block=ImageBlock(status="streaming", ...))``.
    Kept temporarily for back-compat during the Phase 0 rollout; will be
    removed once every emitter migrates to MediaBlockData.

    Emitted by providers that support progressive image streaming (gpt-image-2
    via ``partial_images=N`` + ``stream=True``). The final image still arrives
    via ``ImageOutputData`` once generation completes; partials are intended
    for the UI to render a low-fidelity preview while the user waits.

    ``b64_json`` carries the base64-encoded raw image bytes (always PNG/JPEG/
    WEBP per the model's ``output_format``). ``progress`` is a 0..1 float;
    ``partial_index`` is monotonically increasing per generation.
    """

    type: Literal["partial_image"] = "partial_image"
    b64_json: str
    partial_index: int
    progress: float = 0.0
    mime_type: str = "image/png"


class AudioStreamChunkData(DataPayload[Literal["audio_stream_chunk"]]):
    """A live segment of streaming TTS audio, emitted as it arrives from the provider.

    Gemini TTS yields raw PCM segments for Web Audio playback. ElevenLabs yields
    consecutive MP3 bytes for MediaSource playback. Individual chunks are not
    standalone files in either case: clients append them in monotonic ``seq``
    order until ``AudioStreamEndData`` hands over the authoritative persisted
    file.

    ``take`` names WHICH provider render of the stream this is. When the
    provider call fails mid-render and the run retries it, the retry is a new
    take: a larger ``take``, ``seq`` from zero again, the same ``stream_id``.
    The abandoned take never ends; the saved file is the last take. A client
    replaces its player when a newer take opens and treats ``seq`` zero again
    inside the same take as a gap (2026-10-22, run 395d67ed: a Google 500 on
    TTS segment 3/4 re-rendered the episode from seq 0 and the player dropped).

    ``audio_base64`` is base64 of the provider bytes in the format described by
    ``encoding`` and ``mime_type``. PCM additionally uses ``sample_rate`` /
    ``bits_per_sample`` / ``channels``. ``stream_id`` groups every chunk and the
    end marker for one audio render; ``seq`` is monotonic from zero.
    """

    type: Literal["audio_stream_chunk"] = "audio_stream_chunk"
    stream_id: str
    take: int = 0
    seq: int
    audio_base64: str
    mime_type: str = "audio/L16"
    encoding: Literal["pcm_s16le", "mp3"] = "pcm_s16le"
    sample_rate: int = 24000
    bits_per_sample: int = 16
    channels: int = 1


class AudioStreamEndData(DataPayload[Literal["audio_stream_end"]]):
    """Marks the end of a streaming TTS render — the canonical file is now ready.

    Emitted once per ``stream_id`` after all ``AudioStreamChunkData`` chunks.
    Carries the persisted file's renderable URL(s) so the client can swap its
    progressively-built buffer for the authoritative file (or just bind ``url``
    to an ``<audio>`` element). ``total_chunks`` equals the count of streamed
    chunks (the highest ``seq`` + 1) so the client can confirm it received them all.
    """

    type: Literal["audio_stream_end"] = "audio_stream_end"
    stream_id: str
    take: int = 0
    total_chunks: int
    url: str = ""
    mime_type: str = "audio/wav"
    file_id: str | None = None
    cdn_url: str | None = None
    download_url: str | None = None
    duration_ms: int | None = None
    # Format metadata for the streamed preview. PCM consumers require these;
    # encoded consumers select their decoder from mime_type/encoding.
    sample_rate: int = 24000
    bits_per_sample: int = 16
    channels: int = 1


#: The data events that ARE the product while a run is still working — live TTS
#: audio, partial image renders, and the canonical media reference. A step whose
#: own stream is muted (a nested agent run, a pipeline stage) still delivers
#: these to the person when it names them (``SilentEmitter(forward_data_types=)``
#: / ``run_agent(stream_data_types=)``), and every emitter stack that relays a
#: child's events (workflows included) forwards them. ONE list: a new live-media
#: event joins here, never at one call site.
LIVE_MEDIA_DATA_TYPES: frozenset[str] = frozenset(
    {"audio_stream_chunk", "audio_stream_end", "partial_image", "media_block"}
)


class MediaBlockData(DataPayload[Literal["media_block"]]):
    """Canonical wire payload for any media reference.

    Replaces ``ImageOutputData``, ``AudioOutputData``, ``VideoOutputData``,
    and ``PartialImageData``. The ``block`` field is a discriminated union
    keyed on ``kind`` (image | video | audio | document | youtube); the
    block's own ``status`` field distinguishes in-flight streaming
    partials from complete renderable references.

    See ``matrx_connect.context.media_block`` for shape details and the
    helper functions (``cloud_file_to_media_block``,
    ``asset_variant_to_media_block``, ``external_url_to_media_block``,
    ``streaming_partial_image_block``) that construct the block.
    """

    type: Literal["media_block"] = "media_block"
    block: UnifiedMediaBlock


class DecisionAnswerBlock(BaseModel):
    """ONE answer inside a ``decision_answers`` part, on the wire.

    THE MIRROR, not a second contract. The shape is owned by the
    ``decision_answer`` kind (``matrx_ai.decisions.kinds.DecisionAnswer``);
    matrx-connect cannot import matrx-ai (the package graph runs the other
    way), so the wire twin lives here exactly as ``UnifiedMediaBlock`` is the
    wire twin of a media reference. Drift is caught by a matrx-ai test that
    validates the kind's own ``to_part()`` dump against this model — the one
    place both halves are importable.
    """

    # ``serialize_by_alias``: the emitter dumps a payload with a bare
    # ``model_dump()`` (context/events.py::build_event), so a marker declared
    # only as a serialization alias would reach the wire as ``kind_`` — the
    # frontend's generated MessagePart validator then refuses the part by name
    # and the column renders "This section could not be displayed" (caught in
    # the browser, 2026-09-21). The marker is DATA; it is spelled ``__kind``
    # everywhere, including on a bare dump.
    model_config = {
        "extra": "forbid",
        "populate_by_name": True,
        "serialize_by_alias": True,
    }

    kind_: Literal["decision_answer"] = Field(
        default="decision_answer", alias="__kind", serialization_alias="__kind"
    )
    type: Literal["noul", "choice", "score"]
    #: noul → bool · choice → the chosen option name · score → the
    #: probability-weighted level (a float; "3.4" carries what "3" throws away).
    answer: bool | float | str
    #: noul only — P(true).
    probability: float | None = None
    #: choice/score — the full distribution, never a single winner.
    probabilities: dict[str, float] | None = None
    confidence: float
    #: score only — level key → what that level means, echoed so a renderer
    #: never has to hold the question to draw the answer.
    legend: dict[str, str] | None = None


class DecisionUsageBlock(BaseModel):
    """What the decision call consumed. Zero is a real value, never a stand-in."""

    model_config = {"extra": "forbid"}

    input_tokens: int
    output_tokens: int


class DecisionAnswersData(DataPayload[Literal["decision_answers"]]):
    """A decision turn's answers, LIVE — the ``decision_answers`` part on the wire.

    A decision model is a model in the agent system exactly like an image or a
    TTS model, and those reach a runner or a battle column live as a typed
    ``data`` event (``media_block``). Decisions did not: the answers existed
    only on the persisted ``chat.message`` row, so a battle column said "this
    run finished without writing an answer" until the page was reloaded
    (2026-09-21). This is that missing event, carrying the identical payload
    the part carries, so the live record and the reloaded one agree.

    Emitted by both decision routes — the native holder (TypeSafe System One)
    and a text model's verbalized answer — from ONE place:
    ``matrx_ai.decisions.emit.emit_decision_answers``.
    """

    model_config = {
        "extra": "forbid",
        "populate_by_name": True,
        "protected_namespaces": (),
        # See DecisionAnswerBlock: the emitter dumps without ``by_alias``.
        "serialize_by_alias": True,
    }

    type: Literal["decision_answers"] = "decision_answers"
    kind_: Literal["decision_answers"] = Field(
        default="decision_answers", alias="__kind", serialization_alias="__kind"
    )
    #: The model's NAME (catalog display name / provider model id), never the
    #: ai.model UUID the caller may have named it by.
    model: str
    method: Literal["native", "verbalized", "verbalized_calibrated"]
    answers: dict[str, DecisionAnswerBlock] = Field(default_factory=dict)
    #: question name → why the holder would not answer it. A refusal is an
    #: answer; never replaced by a guess, never silently dropped.
    unanswerable: dict[str, str] = Field(default_factory=dict)
    usage: DecisionUsageBlock
    cost_usd: float


class ConversationLabeledData(DataPayload[Literal["conversation_labeled"]]):
    type: Literal["conversation_labeled"] = "conversation_labeled"
    conversation_id: str
    title: str
    description: str = ""
    keywords: list[str] = Field(default_factory=list)


class MandateInputRequiredData(DataPayload[Literal["mandate_input_required"]]):
    """A mandate run PARKED for input (park-not-die) — the run is not over.

    Emitted on a mandate run's stream (``POST /ai/mandates/{key}``) when its
    Holder stopped to ask: a workflow child that parked ``awaiting_input`` (a
    required input nothing supplied) or ``interrupted`` (a question mid-run).
    The stream then ends with the ``user_request`` completion whose
    ``result.status`` is ``"waiting_input"``. ``inputs`` are the served input
    entries to ask for — each one the ``MandateServedInput`` shape that
    ``GET /mandates/{key}/describe`` serves (name, kind, sourcing, label,
    help, options, json_schema, …), so one form renders both.
    """

    type: Literal["mandate_input_required"] = "mandate_input_required"
    mandate_key: str
    #: The parked Holder run (the workflow child ``run_id``).
    run_id: str
    #: The checkpoint a question resumes from; null for a start-time park.
    checkpoint_id: str | None = None
    inputs: list[dict[str, JsonValue]] = Field(default_factory=list)
    #: The sentence to show the person (the question, or what is missing).
    message: str = ""


class MandateRunData(DataPayload[Literal["mandate_run"]]):
    """WHICH mandate this run is — the run's own identity, sent once at its start.

    Emitted by the mandate door (``POST /ai/mandates/{key}``) — and by every
    continuation turn on a conversation a mandate started — at the start of the
    run's stream, from the SAME object the server stores on this run's
    ``chat.user_request.metadata.mandate_watch`` (one object, two outlets).
    Keyed to ONE request: ``request_id`` is this run's ``chat.user_request`` id,
    so a client binds it to exactly the request it watches — never to a
    conversation, and never to a sibling or child run sharing the wire. A turn
    on a conversation no mandate started emits none, and is not a mandate run.

    ``placement`` is the provision as filled, with every value inline (never a
    reference to a variable a later turn may change); ``placement_captured_at``
    names where it was captured (``door_routing``: before later request shaping
    — memory, skills, surface context — so the wire body stays the truth of
    what the model received).
    """

    type: Literal["mandate_run"] = "mandate_run"
    mandate_key: str
    #: The door that started the run (``chat_start`` for the client door).
    door: str
    #: This run's ``chat.user_request`` id.
    request_id: str | None = None
    conversation_id: str | None = None
    mandate_id: str | None = None
    #: ``real`` | ``test_run`` | ``replay``.
    provenance: str = "real"
    replay_of: str | None = None
    #: The resolution that chose the Holder (``mandate_run_stamp``).
    rung: str | None = None
    holder_type: str = "agent"
    holder_id: str | None = None
    #: The agent VERSION that ran: the pinned version, or the live definition's
    #: current version at run time.
    holder_version_id: str | None = None
    holder_version_number: int | None = None
    #: True when the live definition ran (no pin) — the version is the one it
    #: was at when the run started.
    holder_version_live: bool = False
    model_id: str | None = None
    #: The mandate definition at run time: goal, kinds, required output keys and
    #: its ``version`` (so a later edit shows as "changed since this run").
    goal: str | None = None
    definition_version: int | None = None
    input_kind: str | None = None
    output_kind: str | None = None
    required_output_keys: list[str] = Field(default_factory=list)
    placement: dict[str, JsonValue] | None = None
    placement_captured_at: str = "door_routing"
    #: CONTINUATION TURNS (``door`` = ``conversation_continue`` /
    #: ``conversation_resume``): a turn on a conversation a mandate started. The
    #: mandate is NOT re-resolved there and its provision is NOT re-applied —
    #: ``provision_applied`` is False, ``placement`` is None, the Holder is the
    #: conversation's own agent (``holder_source`` = ``conversation_agent``), and
    #: what the turn DID carry is ``turn_context`` (inline values) plus
    #: ``turn_input`` (the person's words or the host's line, per ``turn_author``).
    provision_applied: bool = True
    holder_source: str = "door_resolution"
    #: The request whose mandate door started this conversation.
    started_by_request_id: str | None = None
    #: ``person`` | ``host`` | ``retry`` | ``resume`` | ``none`` (continuations only).
    turn_author: str | None = None
    turn_input: JsonValue = None
    host_turn_reason: str | None = None
    turn_context: dict[str, JsonValue] | None = None
    #: A resume continues the SAME request: that request's earlier frames
    #: (its door frame, then any earlier resume), oldest first.
    earlier_frames: list[dict[str, JsonValue]] = Field(default_factory=list)


class StructuredInputFailure(BaseModel):
    url: str = ""  # webpage inputs (legacy field name)
    ref: str = ""  # generic resource identifier (note id, task id, …)
    reason: str = ""


class StructuredInputWarningData(DataPayload[Literal["structured_input_warning"]]):
    type: Literal["structured_input_warning"] = "structured_input_warning"
    block_type: str
    failures: list[StructuredInputFailure] = Field(default_factory=list)


class MediaNoticeData(DataPayload[Literal["media_notice"]]):
    """Inline notice that something happened to a media input on the way to the
    model — either it was rerouted/extracted to text (handled) or it could not be
    sent and was dropped. Rendered inline in the chat stream where it occurred, so
    the (agentic-engineer) user sees exactly what the model did/didn't receive."""

    type: Literal["media_notice"] = "media_notice"
    media_kind: str  # "youtube" | "video" | "document" | "audio" | "image"
    # dropped = the model never saw it · extracted/transcribed/converted = we turned
    # it into text the model CAN read and substituted that.
    action: Literal["dropped", "extracted", "transcribed", "converted"]
    user_message: (
        str  # FE-facing, e.g. "YouTube video removed — OpenAI can't accept YouTube as input."
    )
    system_message: str = ""  # fuller detail for logs / hover
    provider: str | None = None
    model: str | None = None
    metadata: dict[str, Any] = Field(default_factory=dict)


class CategorizationResultData(DataPayload[Literal["categorization_result"]]):
    type: Literal["categorization_result"] = "categorization_result"
    prompt_id: str
    category: str
    tags: list[str] = Field(default_factory=list)
    description: str = ""
    dry_run: bool = False
    metadata: dict[str, Any] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# File analysis — per-detector streaming progress (stream-everything mandate)
# ---------------------------------------------------------------------------


class FileAnalysisStartedData(DataPayload[Literal["file_analysis_started"]]):
    """Detector pipeline began — the runnable (detector, tier) count is known."""

    type: Literal["file_analysis_started"] = "file_analysis_started"
    file_id: str
    mime_type: str | None = None
    total_detectors: int


class FileDetectorCompletedData(DataPayload[Literal["file_detector_completed"]]):
    """One (detector, tier) settled — success, skipped, or failed."""

    type: Literal["file_detector_completed"] = "file_detector_completed"
    file_id: str
    detector_kind: str
    tier: str
    status: str  # "success" | "skipped" | "failed"
    elapsed_ms: int = 0
    error: str | None = None
    complete: int  # detectors settled so far (including this one)
    total: int


class FileAnalysisCompleteData(DataPayload[Literal["file_analysis_complete"]]):
    """Terminal analysis result — carries the same head+results payload that
    ``GET /files/{file_id}/analysis`` returns, so a migrating client reads this
    one event as the old fetch response and never needs to poll."""

    type: Literal["file_analysis_complete"] = "file_analysis_complete"
    file_id: str
    status: str  # "complete" | "partial" | "failed" | "not_applicable" | ...
    results_count: int = 0
    failures: list[str] = Field(default_factory=list)
    elapsed_ms: int = 0
    head: dict[str, Any] = Field(
        default_factory=dict
    )  # api-any-ok: mirrors GET /files/{id}/analysis head (FileAnalysisHead)
    results: list[dict[str, Any]] = Field(
        default_factory=list
    )  # api-any-ok: mirrors GET /files/{id}/analysis results (FileAnalysisResultRow)


# ---------------------------------------------------------------------------
# Extraction-run RAG indexing — chunk/embed progress (stream-everything mandate)
# ---------------------------------------------------------------------------


class ExtractionIndexProgressData(DataPayload[Literal["extraction_index_progress"]]):
    """Progress while a page-extraction run is materialized into RAG chunks."""

    type: Literal["extraction_index_progress"] = "extraction_index_progress"
    run_id: str
    stage: str  # "loaded" | "chunked" | "embedding" | "writing"
    message: str = ""
    results_total: int = 0
    chunks_built: int = 0
    chunks_skipped: int = 0
    embedded: int = 0
    total_to_embed: int = 0


class ExtractionIndexCompleteData(DataPayload[Literal["extraction_index_complete"]]):
    """Terminal indexing result — same fields the legacy blocking JSON body
    of ``POST /page-extraction/runs/{run_id}/index`` carried."""

    type: Literal["extraction_index_complete"] = "extraction_index_complete"
    run_id: str
    job_id: str
    derivative_id: str
    derivative_outcome: str  # "created" | "reused"
    results_total: int
    chunks_written: int
    chunks_skipped: int
    priority_applied: int
    agent_id: str | None = None
    embedding_model: str


class PodcastRunEvent(DataPayload[Literal["podcast_run"]]):
    """The resumable run id, streamed first. The client keeps it so a failed
    generation can be resumed (POST /podcast/resume/{run_id}) — completed stages
    replay from the checkpoint and only the missing tail re-runs."""

    type: Literal["podcast_run"] = "podcast_run"
    run_id: str = ""
    total: int = 0


class PodcastRaceStartedEvent(DataPayload[Literal["podcast_race_started"]]):
    """The race row id, streamed the instant the row exists — before any arm
    does paid work. The client keeps it so the comparison surface can follow
    THIS race (never "the newest row", which races other starts), and so a
    closed tab loses nothing: the arms keep running server-side and the row is
    re-read on return."""

    type: Literal["podcast_race_started"] = "podcast_race_started"
    race_id: str = ""
    arms: list[str] = Field(default_factory=list)


class WorkflowComparisonStartedEvent(DataPayload[Literal["workflow_comparison_started"]]):
    """The comparison row id, streamed the instant the row exists — before any
    arm does paid work. The client keeps it so the Workflow Battle surface can
    follow THIS comparison (never "the newest row", which races other starts),
    and so a closed tab loses nothing: the arms keep running server-side and
    the row is re-read on return. Arm run_ids land on the durable row as each
    arm's run is created."""

    type: Literal["workflow_comparison_started"] = "workflow_comparison_started"
    comparison_id: str = ""
    arm_labels: list[str] = Field(default_factory=list)


class MatrixBattleCellRef(BaseModel):
    """One Matrix Battle cell's address: (row variant, column variant, repeat)."""

    row_id: str
    column_id: str
    repeat: int = 0


class MatrixBattleSkippedCell(MatrixBattleCellRef):
    """A requested cell this run did not queue, and why (a live lease, mostly)."""

    reason: str = ""


class MatrixBattleStartedEvent(DataPayload[Literal["matrix_battle_started"]]):
    """A Matrix Battle run call accepted its cells. Every cell row exists and every
    queued cell is already ``queued`` on its row, so a closed tab loses nothing:
    the client polls the entry rows and the cells keep running server-side."""

    type: Literal["matrix_battle_started"] = "matrix_battle_started"
    set_id: str
    run_token: str
    total_cells: int = 0
    queued: int = 0
    concurrency: int = 0
    stalled_settled: int = 0
    skipped: list[MatrixBattleSkippedCell] = Field(default_factory=list)


class MatrixBattleCellStartedEvent(DataPayload[Literal["matrix_battle_cell_started"]]):
    """One cell claimed its row and started its agent run (a NEW conversation)."""

    type: Literal["matrix_battle_cell_started"] = "matrix_battle_cell_started"
    set_id: str
    entry_id: str
    row_id: str
    column_id: str
    repeat: int = 0
    attempt: int = 1
    conversation_id: str


class MatrixBattleCellFinishedEvent(DataPayload[Literal["matrix_battle_cell_finished"]]):
    """One cell settled. ``result`` is the same summary written to the row's
    ``metadata.result`` (tokens, cost, tools used, answer); ``skipped`` means the
    cell never started (canceled while queued, or another run took it)."""

    type: Literal["matrix_battle_cell_finished"] = "matrix_battle_cell_finished"
    set_id: str
    entry_id: str
    row_id: str
    column_id: str
    repeat: int = 0
    status: str
    skipped: bool = False
    error: str | None = None
    conversation_id: str | None = None
    result: dict[str, JsonValue] | None = None


class MatrixBattleFinishedEvent(DataPayload[Literal["matrix_battle_finished"]]):
    """Every cell this run call queued has settled; counts by final status."""

    type: Literal["matrix_battle_finished"] = "matrix_battle_finished"
    set_id: str
    run_token: str
    counts: dict[str, int] = Field(default_factory=dict)


class AgentTestRunStartedEvent(DataPayload[Literal["agent_test_run_started"]]):
    """The FIRST frame of an Agent Evaluation run stream: the run and its execution exist and
    every work item is seeded. A returning client rejoins through
    ``/runtime/operations/by-link/agent_test_run/{run_id}``."""

    type: Literal["agent_test_run_started"] = "agent_test_run_started"
    run_id: str
    execution_id: str
    result_count: int = 0
    status: str = "queued"


class AgentTestResultEvent(DataPayload[Literal["agent_test_result"]]):
    """One result row of the run settled (a door answer, a parity row or a battle's pairwise verdict)."""

    type: Literal["agent_test_result"] = "agent_test_result"
    run_id: str
    result_id: str
    verdict: str | None = None
    door: str | None = None
    setup_key: str | None = None


class AgentTestProgressEvent(DataPayload[Literal["agent_test_progress"]]):
    """The run's counts (``agent.test_run.counts``) re-read after a work item settled."""

    type: Literal["agent_test_progress"] = "agent_test_progress"
    run_id: str
    counts: dict[str, Any] = Field(default_factory=dict)


class AgentTestRunStatusEvent(DataPayload[Literal["agent_test_run_status"]]):
    """The run reached a terminal or paused status; the stream ends after this frame."""

    type: Literal["agent_test_run_status"] = "agent_test_run_status"
    run_id: str
    status: str


class PodcastStageStartedEvent(DataPayload[Literal["podcast_stage_started"]]):
    """A pipeline stage just began. Render a live "running" row so the UI is
    never silent during long stages (research, audio, each image/video)."""

    type: Literal["podcast_stage_started"] = "podcast_stage_started"
    stage: str
    label: str = ""
    step: int = 0
    total: int = 0


class PodcastTickEvent(DataPayload[Literal["podcast_tick"]]):
    """Periodic 'still working' pulse during long, otherwise-silent stages
    (research / script / audio / each media render). The UI binds ``label`` +
    ``elapsed_seconds`` to a live counter so it never looks frozen."""

    type: Literal["podcast_tick"] = "podcast_tick"
    stage: str
    label: str = ""
    elapsed_seconds: float = 0.0
    step: int = 0
    total: int = 0


class PodcastStageEvent(DataPayload[Literal["podcast_stage"]]):
    """A pipeline stage finished (success or failure).

    Merged with the legacy ``PodcastStageData`` (same ``podcast_stage`` wire
    type) — this richer shape is what the generator actually emits; the old
    ``result_keys`` shape never had an emitter."""

    type: Literal["podcast_stage"] = "podcast_stage"
    stage: str
    label: str = ""
    success: bool
    output: str = ""
    error: str | None = None
    step: int = 0
    total: int = 0


class PodcastMetadataEvent(DataPayload[Literal["podcast_metadata"]]):
    """Structured metadata, streamed the instant it parses — the UI renders the
    title/description and lays out the image/video slots from the prompts long
    before any media has rendered."""

    type: Literal["podcast_metadata"] = "podcast_metadata"
    title: str = ""
    description: str = ""
    image_descriptions: list[str] = Field(default_factory=list)
    video_descriptions: list[str] = Field(default_factory=list)


class PodcastAssetEvent(DataPayload[Literal["podcast_asset"]]):
    """One image or video landed during full generation. ``index`` maps 1:1 to
    the matching prompt in the metadata event's image_descriptions /
    video_descriptions."""

    type: Literal["podcast_asset"] = "podcast_asset"
    asset_kind: Literal["image", "video"]
    index: int
    url: str = ""
    prompt: str = ""
    success: bool = True
    error: str | None = None
    # Informational-only note on a SUCCESSFUL asset (e.g. the primary model
    # was rejected and a backup model rendered it). Render as a quiet chip,
    # never as an error.
    note: str | None = None


class PodcastOfficialVideoEvent(DataPayload[Literal["podcast_official_video"]]):
    """The composed "official" slideshow video landed — a single crossfaded
    video stitched from all generated clips + stills. This is the episode's
    primary, share-ready video."""

    type: Literal["podcast_official_video"] = "podcast_official_video"
    url: str = ""
    success: bool = True
    error: str | None = None


class PodcastCompleteEvent(DataPayload[Literal["podcast_complete"]]):
    """Terminal event of a full podcast generation.

    Merged with the legacy ``PodcastCompleteData`` (same ``podcast_complete``
    wire type) — this richer shape is what the generator actually emits; the
    old ``episode_count`` shape never had an emitter."""

    type: Literal["podcast_complete"] = "podcast_complete"
    show_id: str
    success: bool
    # Set once the episode is persisted to pc_episodes.
    episode_id: str | None = None
    # The episode's URL slug — the UI builds the public link from this.
    episode_slug: str | None = None
    script: str = ""
    audio_url: str = ""
    title: str = ""
    description: str = ""
    image_urls: list[str] = Field(default_factory=list)
    video_urls: list[str] = Field(default_factory=list)
    # THE IDENTITY RULE (common-docs/systems/files/media-durability/FEATURE.md): the
    # URLs above are the handoff; these are the durable handles behind them.
    # Every element is positionally paired with its URL sibling and an entry is
    # "" when the id could not be recovered (an externally-hosted asset) — the
    # lists are therefore ALWAYS the same length as their URL list, so a
    # consumer can index across them without a second lookup.
    audio_file_id: str = ""
    image_file_ids: list[str] = Field(default_factory=list)
    video_file_ids: list[str] = Field(default_factory=list)
    official_video_file_id: str = ""
    # The composed crossfaded slideshow video (clips + stills). Empty when
    # there wasn't enough media or composition failed.
    official_video_url: str = ""
    # Why the official video is missing, surfaced to the client. Empty on
    # success or when there wasn't enough media; otherwise the compose error.
    official_video_error: str = ""
    # "live" (default) or "shadow". A shadow run executed the full real
    # pipeline but published NOTHING — episode_id/episode_slug are always null
    # for it, by design, not by failure. Labeled loudly so no consumer ever
    # mistakes a shadow result for a live episode.
    run_mode: str = "live"
    # The resolved cast: [{name, voice}] in turn-priority order + host count.
    host_count: int = 2
    speakers: list[dict[str, Any]] = Field(default_factory=list)
    error: str | None = None


# Deprecated aliases — the legacy class names kept for import back-compat
# (re-exported through the context shims). Same classes, same wire types.
PodcastStageData = PodcastStageEvent
PodcastCompleteData = PodcastCompleteEvent


class PodcastAssetGenStartedEvent(DataPayload[Literal["podcast_asset_gen_started"]]):
    """A single-asset (re)generation began (POST /podcast/runs/{run_id}/assets/
    regenerate | add). Render a live "rendering" state on the slot; provider
    progress (``partial_image`` / ``media_block``) streams in between this and
    the terminal ``podcast_asset_result``."""

    type: Literal["podcast_asset_gen_started"] = "podcast_asset_gen_started"
    run_id: str
    asset_kind: Literal["image", "video"]
    slot: int
    prompt: str = ""
    model_alias: str | None = None
    is_manual: bool = False


class PodcastAssetResultEvent(DataPayload[Literal["podcast_asset_result"]]):
    """Terminal event of a single-asset regenerate/add — carries the recorded
    pc_studio_run_assets row (everything the legacy blocking JSON response
    carried, plus ``run_id`` / ``asset_id`` / ``error``)."""

    type: Literal["podcast_asset_result"] = "podcast_asset_result"
    run_id: str
    # pc_studio_run_assets row id (also sent via record_update events).
    asset_id: str | None = None
    asset_kind: Literal["image", "video"]
    slot: int
    status: str
    url: str | None = None
    # Extracted so the FE can re-mint (durable for owner).
    file_id: str | None = None
    prompt: str | None = None
    model_alias: str | None = None
    is_manual: bool = False
    error: str | None = None


class WorkflowStepData(DataPayload[Literal["workflow_step"]]):
    type: Literal["workflow_step"] = "workflow_step"
    step_name: str
    status: str
    data: dict[str, Any] = Field(default_factory=dict)


class FunctionResultData(DataPayload[Literal["function_result"]]):
    type: Literal["function_result"] = "function_result"
    function_name: str
    success: bool
    result: Any = None
    error: str | None = None
    duration_ms: float | None = None


class QuestionnaireQuestion(BaseModel):
    """A single interactive question in the questionnaire UI."""

    id: str
    prompt: str
    component_type: Literal[
        "dropdown", "checkboxes", "radio", "toggle", "slider", "input", "textarea"
    ]
    options: list[str] = Field(default_factory=list)
    min: float | None = None
    max: float | None = None
    step: float | None = None
    default: Any = None
    required: bool = False


class QuestionnaireDisplayData(DataPayload[Literal["display_questionnaire"]]):
    type: Literal["display_questionnaire"] = "display_questionnaire"
    introduction: str
    questions: list[QuestionnaireQuestion] = Field(default_factory=list)


class ScrapeBatchCompleteData(DataPayload[Literal["scrape_batch_complete"]]):
    type: Literal["scrape_batch_complete"] = "scrape_batch_complete"
    total_scraped: int


class YouTubeTranscriptSourceData(DataPayload[Literal["youtube_transcript_source"]]):
    """``POST /media/youtube/transcript``'s result: the Source the transcript landed as.

    ``processed_document_id`` is the Source (one ``segment`` portion per timed segment, with
    ``t0_ms``/``t1_ms`` locators); ``transcript_id`` is its ``transcripts.transcripts`` row.
    ``reused_existing`` is true when the organization already held this video's transcript."""

    type: Literal["youtube_transcript_source"] = "youtube_transcript_source"
    processed_document_id: str
    transcript_id: str
    video_id: str
    title: str
    segment_count: int
    reused_existing: bool


class FetchResultItem(BaseModel):
    model_config = {"extra": "allow"}
    url: str = ""
    title: str = ""
    content: str = ""
    status: str = ""


class FetchResultsData(DataPayload[Literal["fetch_results"]]):
    type: Literal["fetch_results"] = "fetch_results"
    metadata: dict[str, Any] = Field(default_factory=dict)
    results: list[FetchResultItem] = Field(default_factory=list)


class SearchResultItem(BaseModel):
    """One result entry from a web search."""

    model_config = {"extra": "allow"}
    url: str = ""
    title: str = ""
    snippet: str = ""
    published: str | None = None
    source: str | None = None


class SearchResultsData(DataPayload[Literal["search_results"]]):
    type: Literal["search_results"] = "search_results"
    metadata: dict[str, Any] = Field(default_factory=dict)
    results: list[SearchResultItem] = Field(default_factory=list)


class SearchErrorData(DataPayload[Literal["search_error"]]):
    type: Literal["search_error"] = "search_error"
    metadata: dict[str, Any] = Field(default_factory=dict)
    error: str


class ContextChangedData(DataPayload[Literal["context_changed"]]):
    """A ContextManifest object was mutated by ctx_patch / ctx_create.

    Emitted whenever the server edits a context object in place so the
    frontend can re-render documents, flush pending UI state, or schedule a
    persist-back to its own storage.
    """

    type: Literal["context_changed"] = "context_changed"
    key: str
    command: str
    object_type: str = ""
    mutable: bool = False
    persist: str = "auto"
    source_kind: str = ""
    source_id: str | None = None


class ContextPersistedData(DataPayload[Literal["context_persisted"]]):
    """The server successfully persisted a ctx_patch / ctx_create mutation.

    Emitted after the fire-and-forget writeback finishes. Lets the client
    know it can trust its own cached copy (or trigger a refresh).
    """

    type: Literal["context_persisted"] = "context_persisted"
    key: str
    command: str
    source_kind: str = ""
    source_id: str | None = None
    # True when this write CREATED the row (materialize-on-write): the source
    # pointed at a reserved id that did not exist yet and the handler inserted
    # it. The client uses this to finalize a deferred-existence object — bind to
    # the now-real id and create its association edge.
    materialized: bool = False


class ContextConflictData(DataPayload[Literal["context_conflict"]]):
    """A ctx_patch landed on a row a concurrent edit had already advanced.

    The agent's edit STILL persisted (every version is captured in history), so
    nothing is lost — but the base version the agent edited no longer matched
    the current row. The client surfaces a diff/merge from version history so
    the user can reconcile. `base_version` is what the agent edited; the live
    row is now `base_version + 1` (the agent's write).
    """

    type: Literal["context_conflict"] = "context_conflict"
    key: str
    command: str
    source_kind: str = ""
    source_id: str | None = None
    base_version: int | None = None


class ContextDeltaData(DataPayload[Literal["context_delta"]]):
    """The CONTENT of a ctx_patch / create mutation, streamed as it is applied.

    ``context_changed`` (unchanged, still emitted) announces THAT an object
    mutated but carries no content, forcing clients to re-read the row after
    the writeback — which made agent edits appear all-at-once after the turn.
    This event closes that gap: emitted at the same moment, in stream order,
    carrying the edit itself so the client can update its copy immediately.

    Two delivery forms, discriminated by ``delta_kind``:
      - ``splice`` — a single contiguous replacement against the pre-edit
        content: replace ``[start, end)`` with ``text``. ``base_len`` /
        ``new_len`` guard application — if the client copy's length differs
        from ``base_len`` its copy diverged (e.g. the user typed mid-turn);
        skip the delta and rely on the ``context_persisted`` re-read.
      - ``full`` — ``content`` carries the complete post-edit content
        (create / JSON commands / non-string content, or whenever the splice
        would not be smaller than the full content).

    ``seq`` is monotonically increasing so a client can detect reordering.
    """

    type: Literal["context_delta"] = "context_delta"
    key: str
    command: str
    object_type: str = ""
    source_kind: str = ""
    source_id: str | None = None
    seq: int = 0
    delta_kind: Literal["splice", "full"] = "full"
    # Splice form — all present together.
    start: int | None = None
    end: int | None = None
    text: str | None = None
    base_len: int | None = None
    # Length of the post-edit content (both forms; application guard).
    new_len: int = 0
    # Full form — the complete post-edit content.
    content: str | None = None


class ContextPersistFailedData(DataPayload[Literal["context_persist_failed"]]):
    """A ctx_patch / ctx_create writeback failed after the in-memory edit.

    The manifest still reflects the new content for the rest of the request,
    but the DB was not updated. The client should decide whether to retry or
    surface the failure to the user.
    """

    type: Literal["context_persist_failed"] = "context_persist_failed"
    key: str
    command: str
    source_kind: str = ""
    source_id: str | None = None
    error: str = ""
    traceback: str = ""


# ---------------------------------------------------------------------------
# Context receipt — what the server actually did with every context value
# (common-docs/systems/data/scopes-context/context-delivery/RULES.md §5)
# ---------------------------------------------------------------------------

ContextRuleLayer = Literal["default", "page", "agent", "you"]


class ContextDecidedBy(BaseModel):
    """Which layer decided each knob of one context value."""

    model_config = {"extra": "forbid"}

    include: ContextRuleLayer
    max_inline_chars: ContextRuleLayer


class ContextRule(BaseModel):
    """A person's saved rule for one context value (``users.user_surface_state``,
    ``feature='context_rules'``). Each field is optional: a rule that sets one knob leaves the
    other to the lower layers. In a receipt, it is what the server READ (valid fields only)."""

    model_config = {"extra": "forbid"}

    include: bool | None = None
    max_inline_chars: int | None = Field(default=None, ge=0)


class ContextDeliveredRef(BaseModel):
    """What the model read for one value or block, by SIZE and HASH only — never the text
    (RULES.md §5/§5b, owner law 2026-10-01: a server-shaped value is fetched on demand, never
    pushed). The text itself is served by ``GET /ai/context/delivered`` (a sent turn) or
    ``POST /ai/context/preview`` with ``view`` (the next turn), byte-exact, matched by this hash."""

    model_config = {"extra": "forbid"}

    #: Code-point length of the whole text the model read.
    chars: int
    #: SHA-256 hex of that whole text (UTF-8).
    sha256: str


class ContextReceiptBlock(BaseModel):
    """One block of text the server put in front of the model this turn that is NOT a single
    context value: the turn's ``<active_context>``, earlier-turn context, the sandbox briefing,
    unplaced bound data, skills, observational memory, the organization catalog, the
    dictionary… (RULES.md §5 ``blocks``). Captured from the final config just before the model
    call — the exact text the model received, never a rebuilt copy."""

    model_config = {"extra": "forbid"}

    #: Stable id — the per-turn context slot it rode in, or the system-prompt addition's name.
    id: str
    #: The id in words (``humanize_context_key``).
    label: str
    #: The block's size and hash; its text is served on demand (``/ai/context/delivered``).
    delivered: ContextDeliveredRef


class ContextReceiptWithheldItem(BaseModel):
    """One message of the group the participant's view policy kept from the model this turn."""

    model_config = {"extra": "forbid"}

    message_id: str
    conversation_id: str
    #: The participant key of the speaker, or ``"person"`` for the person's own words.
    speaker: str
    #: The policy rule that withheld it: ``"sees"``, ``"reveal.after_round"``,
    #: ``"reveal.every_rounds"``, ``"budget"`` (oldest dropped first) or ``"policy_invalid"``.
    rule: str


class ContextReceiptRoomView(BaseModel):
    """What the Group Chat view (per-turn slot ``room_view``) chose for this participant this
    turn and why. The receipt's ``blocks`` carry the TEXT; this explains the CHOICE."""

    model_config = {"extra": "forbid"}

    #: The participant edge (``platform.associations.id``) this view was built for.
    participant_id: str
    participant_key: str
    #: The group's round this turn (person messages anywhere in the group, this one included).
    round: int
    policy_version: int
    #: Messages rendered verbatim (said since this participant's last reply).
    included: list[str] = Field(default_factory=list)
    #: Older messages rendered as a shortened line in the digest.
    digested: list[str] = Field(default_factory=list)
    withheld: list[ContextReceiptWithheldItem] = Field(default_factory=list)
    #: Set when the policy could not be read; the view was then withheld whole.
    error: str | None = None


class ContextReceiptPassthroughWithheld(BaseModel):
    """One of the Conductor's values this Orchestra member did not receive, and why."""

    model_config = {"extra": "forbid"}

    key: str
    #: ``closed`` (the connection offers nothing), ``conductor_owned`` (the Conductor's own
    #: resource, passed only by name), ``page_off`` (handed over: not declared, not handed
    #: over), ``refused`` (the member's own layer or the person turned it off),
    #: ``person_and_org_off`` (the connection's switch is off).
    reason: Literal["closed", "conductor_owned", "page_off", "refused", "person_and_org_off"]


class ContextReceiptPassthroughOverride(BaseModel):
    """How one value's display was changed on the way to the member."""

    model_config = {"extra": "forbid"}

    key: str
    #: The Conductor's hand-over asked for this display.
    show: Literal["whole", "pointer"] | None = None
    #: The connection's own per-value limit.
    limit: int | None = None


class ContextReceiptPassthrough(BaseModel):
    """An Orchestra member's turn: what its connection passed from the Conductor (context
    passthrough). The rows say ``page`` where the connection decided; this says why."""

    model_config = {"extra": "forbid"}

    conductor_id: str
    mode: Literal["closed", "handed_over", "mirror"]
    person_and_org: bool
    #: Received because the Conductor named them (or the connection always sends them).
    handed_over: list[str] = Field(default_factory=list)
    #: Received because the connection mirrors the Conductor.
    mirrored: list[str] = Field(default_factory=list)
    #: Received only because the member declares it (its own layer re-admitted it).
    declared: list[str] = Field(default_factory=list)
    withheld: list[ContextReceiptPassthroughWithheld] = Field(default_factory=list)
    overrides: list[ContextReceiptPassthroughOverride] = Field(default_factory=list)


class ContextReceiptRow(BaseModel):
    """One context value this turn: whether it reached the model, and how."""

    model_config = {"extra": "forbid"}

    key: str
    label: str
    #: The surface that emitted the value; ``_default`` when no surface did.
    surface_key: str
    origin: Literal["client", "server", "surroundings", "rule"]
    #: Code-point size of the value; None for an unresolved lazy source (or a rule row).
    chars: int | None = None
    include: bool
    #: The effective limit, after the cap clamp.
    max_inline_chars: int
    delivery: Literal["inline", "on_request", "off"]
    decided_by: ContextDecidedBy
    user_rule: ContextRule | None = None
    clamped: bool = False
    #: The client sent a value the person has turned off (the server dropped it).
    client_sent_excluded: bool = False
    #: Set when something past the rules kept the value from the model: ``"model"`` = this
    #: turn's model cannot read context at all (no function calling); ``"self_check"`` = the
    #: post-render check found it rendered against the rules and stripped it before the call.
    blocked_by: Literal["model", "self_check"] | None = None
    #: Set when the server did not keep the value under its own key — it is still accounted
    #: for here, never missing (RULES.md §5): ``"expanded"`` = a surroundings envelope
    #: (``surface_chain`` / ``window_forms``) became one row per part; ``"directive"`` = a
    #: reserved directive (``__table_access`` / ``__google_files``) the server acted on;
    #: ``"renamed"`` = an earlier key spelling, now held under the stable key;
    #: ``"unaccounted"`` = a server path removed it with no reason (a defect, filed).
    consumed_as: Literal["expanded", "directive", "renamed", "unaccounted"] | None = None
    #: The keys (each with its own row) that now carry what this value held.
    consumed_into: list[str] = Field(default_factory=list)
    #: What the model read for this value in the turn's context block, verbatim: the value's
    #: own element (``inline`` — the whole value; ``on_request`` — the one-entry descriptor);
    #: for a server-authoritative value stated in ``<active_context>`` (``organization``,
    #: ``active_scopes``), the server's own elements there — never the client's copy.
    #: None when the value reached no context block (off, consumed, a preview with no render).
    delivered: ContextDeliveredRef | None = None
    #: For an ``on_request`` value the server holds as text: what the ``context`` tool returns
    #: for it (``mode="full"``). None for a source resolved only when asked (a document).
    on_request: ContextDeliveredRef | None = None


class ContextReceiptData(DataPayload[Literal["context_receipt"]]):
    """The per-turn context receipt, streamed before any model output.

    Derived from the final context objects, never computed separately; the same
    receipt is persisted at ``chat.message.model_context.delivery.receipt``.
    """

    type: Literal["context_receipt"] = "context_receipt"
    version: Literal[1] = 1
    surface: str | None = None
    cap: int
    #: False when this turn's model cannot read context (no function calling): every row is
    #: then ``delivery="off"`` with ``blocked_by="model"``.
    model_reads_context: bool = True
    rows: list[ContextReceiptRow] = Field(default_factory=list)
    #: Set when the person's saved rules could not be read this turn (the turn ran
    #: without them and the failure was recorded) — never a silent "no rules".
    rules_error: str | None = None
    #: Every non-per-value block the model received this turn, in render order.
    blocks: list[ContextReceiptBlock] = Field(default_factory=list)
    #: Set when this conversation is a Group Chat participant: what its view policy chose.
    room_view: ContextReceiptRoomView | None = None
    #: Set when this run is an Orchestra member: what its connection passed from the Conductor.
    passthrough: ContextReceiptPassthrough | None = None


class FirstTurnFilledData(DataPayload[Literal["first_turn_filled"]]):
    """THE VARIABLE RULE for an EPHEMERAL run (store=false): turn 1's filled RESULT.

    Sent once, after a successful first turn that wrote nothing. A stored conversation keeps
    this on its row; an ephemeral one has no row, so the client keeps it and sends it back on
    every later turn with ``first_turn_filled: true`` — the server then runs no first-turn
    pass (no values, no auto-assignment, no scope bindings, no blocks, no definition re-read).
    """

    type: Literal["first_turn_filled"] = "first_turn_filled"
    #: The system prompt exactly as a stored conversation freezes it (the rendered first-turn
    #: text); None when the turn had none.
    system_instruction: str | None = None
    #: The authored messages, filled, in order (system messages are part of
    #: ``system_instruction``). Sent back as the leading messages of the transcript.
    messages: list[dict[str, Any]] = Field(default_factory=list)
    #: Opaque seal of what turn 1 resolved but never wrote into the prompt — the hidden wire text
    #: (pick-list descriptions, reference fences), document context, prompt-block tools, bound
    #: controls, how the first words joined the authored turn. Ciphertext only: the browser never
    #: reads it, and it opens only for the person and organization that ran turn 1, until it
    #: expires. Sent back unchanged as ``wire_swaps`` with ``first_turn_filled: true``.
    wire_swaps: str | None = None


# ---------------------------------------------------------------------------
# Observational memory events (admin-gated, see matrx_ai/memory/)
# ---------------------------------------------------------------------------


class MemoryContextInjectedData(DataPayload[Literal["memory_context_injected"]]):
    """Prior observations were prepended to the system prompt for this turn.

    Emitted once per memory-enabled turn, BEFORE the LLM call, if any
    observations exist yet. ``observation_chars`` is the raw character
    length of the injected block — useful for sizing UI badges.
    """

    type: Literal["memory_context_injected"] = "memory_context_injected"
    conversation_id: str
    observation_chars: int = 0


class MemoryObserverCompletedData(DataPayload[Literal["memory_observer_completed"]]):
    """The Observer LLM extracted observations from unobserved messages.

    Fires when the message-token threshold was crossed and a synchronous
    (or buffered) Observer call completed. ``cost`` is in USD.
    """

    type: Literal["memory_observer_completed"] = "memory_observer_completed"
    conversation_id: str
    model: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0
    duration_ms: int | None = None


class MemoryReflectorCompletedData(DataPayload[Literal["memory_reflector_completed"]]):
    """The Reflector LLM compressed existing observations.

    Fires when the observation-token threshold was crossed. Compression can
    take multiple internal attempts with escalating levels; this event
    represents the final successful result.
    """

    type: Literal["memory_reflector_completed"] = "memory_reflector_completed"
    conversation_id: str
    model: str | None = None
    input_tokens: int = 0
    output_tokens: int = 0
    cost: float = 0.0
    duration_ms: int | None = None


class MemoryBufferSpawnedData(DataPayload[Literal["memory_buffer_spawned"]]):
    """An asynchronous observer/reflector buffering task was spawned.

    Lets the UI show "memory processing in background" without blocking
    the main stream. ``kind`` distinguishes observer buffering from
    reflector buffering.
    """

    type: Literal["memory_buffer_spawned"] = "memory_buffer_spawned"
    conversation_id: str
    kind: Literal["observer", "reflector"] = "observer"


class MemoryErrorData(DataPayload[Literal["memory_error"]]):
    """An OM operation failed. The main conversation turn is unaffected —
    memory errors are non-fatal by design, but the UI may want to surface
    a subtle indicator that memory is degraded."""

    type: Literal["memory_error"] = "memory_error"
    conversation_id: str
    phase: str = ""  # "pre_input", "observer", "reflector", "post_output"
    error: str = ""
    model: str | None = None


# ---------------------------------------------------------------------------
# Legal admin — CourtListener sync / bulk-load progress (stream-everything)
# ---------------------------------------------------------------------------


class LegalSyncEventData(DataPayload[Literal["legal_sync_event"]]):
    """One progress event from a legal-data sync or bulk-load run.

    ``phase`` is the discriminator within the stream. API-sync phases:
    ``started | progress | court_started | court_done | court_errored |
    cluster_done | cluster_errored | done | error``. Bulk-load phases:
    ``started | manifest_lookup | manifest_ready | resource_started |
    resource_skipped | resource_errored | resource_done | download_started |
    download_progress | download_done | copy_started | copy_progress |
    copy_done | insert_started | insert_done | split_started |
    split_progress | done | error``. Every other field is optional and
    populated per phase; ``done`` carries the run summary.
    """

    type: Literal["legal_sync_event"] = "legal_sync_event"
    phase: str
    run_id: str | None = None
    resource: str | None = None
    resources: list[str] | None = None
    court_id: str | None = None
    court_ids: list[str] | None = None
    cluster_id: int | None = None
    cluster_count: int | None = None
    rows: int | None = None
    court_rows: int | None = None
    total_rows: int | None = None
    rows_pumped: int | None = None
    rows_inserted: int | None = None
    bytes_received: int | None = None
    s3_key: str | None = None
    size_bytes: int | None = None
    dump_date: str | None = None
    bucket: str | None = None
    table: str | None = None
    target: str | None = None
    batch_size: int | None = None
    last_id: int | None = None
    reason: str | None = None
    per_court_counts: dict[str, int] | None = None
    per_court_errors: dict[str, str] | None = None
    per_cluster_errors: dict[str, str] | None = None
    per_resource_rows: dict[str, int] | None = None
    per_resource_errors: dict[str, str] | None = None
    error: str | None = None


# ---------------------------------------------------------------------------
# File search — per-page PDF text-search progress (stream-everything)
# ---------------------------------------------------------------------------


class FileSearchBboxItem(BaseModel):
    model_config = {"extra": "forbid"}
    x0: float
    y0: float
    x1: float
    y1: float


class FileSearchHitItem(BaseModel):
    """One search hit — identical shape to the legacy SearchHitOut."""

    model_config = {"extra": "forbid"}
    page_number: int
    page_id: str | None = None
    bbox: FileSearchBboxItem
    snippet: str
    matched_text: str
    char_start: int | None = None
    char_end: int | None = None


class FileSearchStartedData(DataPayload[Literal["file_search_started"]]):
    """Search began — the document is open and the page count is known."""

    type: Literal["file_search_started"] = "file_search_started"
    file_id: str
    query: str
    regex: bool = False
    case_sensitive: bool = False
    total_pages: int


class FileSearchPageData(DataPayload[Literal["file_search_page"]]):
    """A page finished scanning. Emitted for every page that has hits, plus
    periodic zero-hit progress markers so long documents show live progress.
    ``total_hits`` is the running count of kept hits so far."""

    type: Literal["file_search_page"] = "file_search_page"
    page_number: int
    total_pages: int
    hits: list[FileSearchHitItem] = Field(default_factory=list)
    total_hits: int = 0


class FileSearchCompleteData(DataPayload[Literal["file_search_complete"]]):
    """Terminal search result — carries the full legacy SearchResponse body."""

    type: Literal["file_search_complete"] = "file_search_complete"
    file_id: str
    query: str
    regex: bool = False
    case_sensitive: bool = False
    hits: list[FileSearchHitItem] = Field(default_factory=list)
    truncated: bool = False
    pages_scanned: int = 0
    total_pages: int = 0


# ---------------------------------------------------------------------------
# Image edit / Image Studio — per-stage + per-item progress (stream-everything)
# ---------------------------------------------------------------------------


class ImageOpStageData(DataPayload[Literal["image_op_stage"]]):
    """A stage transition inside an image operation.

    ``stage``: ``started | loading_source | running_op | detecting |
    encoding | persisting | rendering_variants | staging | committing``.
    """

    type: Literal["image_op_stage"] = "image_op_stage"
    op: str
    stage: str
    detail: str | None = None
    source_id: str | None = None
    mask_id: str | None = None


class ImageDocumentDetectedData(DataPayload[Literal["image_document_detected"]]):
    """Terminal result of POST /images/detect-document — same fields as the
    legacy DetectDocumentResponse. Corner tuples are ``[x, y]`` in
    post-EXIF-transpose pixel coordinates (TL/TR/BR/BL); all four are null
    when ``found`` is false."""

    type: Literal["image_document_detected"] = "image_document_detected"
    found: bool
    top_left: tuple[float, float] | None = None
    top_right: tuple[float, float] | None = None
    bottom_right: tuple[float, float] | None = None
    bottom_left: tuple[float, float] | None = None
    confidence: float = 0.0
    image_width: int = 0
    image_height: int = 0


class ImageEditCompleteData(DataPayload[Literal["image_edit_complete"]]):
    """Terminal result of an image edit — ``asset`` is the SAME Asset
    envelope the legacy blocking response returned (the OpenAPI ``Asset``
    schema); a migrating client reads this one event as the old response
    body."""

    type: Literal["image_edit_complete"] = "image_edit_complete"
    op: str
    file_id: str | None = None
    asset: dict[str, Any] = Field(default_factory=dict)  # OpenAPI Asset envelope, verbatim


class GeneratedImageFileItem(BaseModel):
    """One generated image persisted to cld_files — same fields as the
    legacy ``ImageResult`` shape the image-studio FE client consumes
    (``cloud_file_id`` + ``public_url``). ``public_url`` is the always-
    renderable ``url`` flavour from the persist envelope (CDN when public,
    signed-inline otherwise); clients should identify by ``cloud_file_id``
    and re-mint on expiry."""

    model_config = {"extra": "forbid"}
    cloud_file_id: str
    public_url: str | None = None
    mime: str | None = None
    width: int | None = None
    height: int | None = None


class ImageGenerateCompleteData(DataPayload[Literal["image_generate_complete"]]):
    """Terminal result of POST /images/generate — ``files`` carries one
    entry per persisted image (the legacy blocking GenerateImageResponse
    body); a migrating client reads this one event as the old response."""

    type: Literal["image_generate_complete"] = "image_generate_complete"
    prompt: str = ""
    model: str | None = None
    files: list[GeneratedImageFileItem] = Field(default_factory=list)


class ImageStudioVariantData(DataPayload[Literal["image_studio_variant"]]):
    """One Image Studio variant finished (rendered + staged) or failed —
    same per-variant shape as the legacy StudioVariantOut entries.
    ``completed``/``total`` are running per-item counters."""

    type: Literal["image_studio_variant"] = "image_studio_variant"
    job_id: str
    preset_id: str
    filename: str | None = None
    format: str | None = None
    width: int | None = None
    height: int | None = None
    quality: int | None = None
    size: int | None = None
    # Row-less staged preview: ephemeral by design (no file row exists).
    ephemeral_url: str | None = None
    expires_in: int | None = None
    compression_ratio: int | None = None
    notes: list[str] = Field(default_factory=list)
    error: str | None = None
    completed: int = 0
    total: int = 0


class ImageStudioProcessCompleteData(DataPayload[Literal["image_studio_process_complete"]]):
    """Terminal result of POST /images/studio/process — ``result`` is the
    full legacy ProcessResponse body (OpenAPI ``ProcessResponse`` schema)."""

    type: Literal["image_studio_process_complete"] = "image_studio_process_complete"
    job_id: str
    result: dict[str, Any] = Field(default_factory=dict)  # OpenAPI ProcessResponse, verbatim


class ImageStudioCommitItemData(DataPayload[Literal["image_studio_commit_item"]]):
    """One staged Image Studio variant (or the source) committed or failed.
    ``preset_id`` is ``"source"`` for the source image."""

    type: Literal["image_studio_commit_item"] = "image_studio_commit_item"
    job_id: str
    preset_id: str
    status: str  # "saved" | "failed"
    file_id: str | None = None
    filename: str | None = None
    file_path: str | None = None
    size: int | None = None
    public_url: str | None = None
    error: str | None = None
    completed: int = 0
    total: int = 0


class ImageStudioCommitCompleteData(DataPayload[Literal["image_studio_commit_complete"]]):
    """Terminal result of POST /images/studio/commit — ``result`` is the
    legacy CommitResponse body (OpenAPI ``CommitResponse`` schema) minus the
    server-only ``storage_uri`` fields, which never reach a client."""

    type: Literal["image_studio_commit_complete"] = "image_studio_commit_complete"
    job_id: str
    folder_path: str
    saved_count: int = 0
    failed_count: int = 0
    result: dict[str, Any] = Field(default_factory=dict)  # CommitResponse minus storage_uri


# ---------------------------------------------------------------------------
# Dictionary publication — ElevenLabs publish (stream-everything)
# ---------------------------------------------------------------------------


class DictionaryPublishCompleteData(DataPayload[Literal["dictionary_publish_complete"]]):
    """Terminal result of POST /dictionary/publish — same fields as the
    legacy PublishResult response."""

    type: Literal["dictionary_publish_complete"] = "dictionary_publish_complete"
    status: str  # "unchanged" | "published" | "updated" | "cleared" | "empty"
    level: str
    owner_id: str | None = None
    external_id: str | None = None
    version_id: str | None = None
    rule_count: int = 0
    rules_hash: str | None = None


# ---------------------------------------------------------------------------
# Masterworks — Rulebook → Masterwork Build progress (stream-everything)
# ---------------------------------------------------------------------------


class MasterworkRunData(DataPayload[Literal["masterwork_run"]]):
    """The FIRST event of every durable Masterwork run — its receipt number.

    The browser stores nothing but this id and rejoins by it through
    ``POST /masterworks/runs/{run_id}/rejoin``; the run's state itself lives
    in ``platform.masterwork_run``. Announced before any work begins, so losing
    the connection one second in still leaves something to come back to.
    """

    type: Literal["masterwork_run"] = "masterwork_run"
    run_id: str
    rulebook_id: str
    operation: str  # "build" | "ingest" | "ingest_file" | "audition"
    label: str | None = None


class MasterworkRunSnapshotData(DataPayload[Literal["masterwork_run_snapshot"]]):
    """What a rejoin gets once the run is no longer executing in this process:
    the durable row, once. It carries the SAME result document the live terminal
    event carried, so a reloaded page lands on the finished answer rather than an
    empty dialog."""

    type: Literal["masterwork_run_snapshot"] = "masterwork_run_snapshot"
    run_id: str
    rulebook_id: str
    operation: str
    label: str | None = None
    status: str  # "processing" | "completed" | "failed"
    live: bool = False
    error: dict[str, Any] | None = None
    result: dict[str, Any] | None = None
    completed_at: str | None = None


class MasterworkRunFailedData(DataPayload[Literal["masterwork_run_failed"]]):
    """A live run died. Mirrored into the replay channel so a connection that is
    already following gets the failure, not silence."""

    type: Literal["masterwork_run_failed"] = "masterwork_run_failed"
    run_id: str
    error: dict[str, Any] | None = None


class MasterworkRunCancelledData(DataPayload[Literal["masterwork_run_cancelled"]]):
    """A PERSON stopped a live run. Distinct from ``masterwork_run_failed`` on
    purpose: nothing broke, so nothing may be reported as broken. The client
    renders this as "Stopped", not as an error, and offers no "try again"
    over a decision somebody just made deliberately."""

    type: Literal["masterwork_run_cancelled"] = "masterwork_run_cancelled"
    run_id: str
    error: dict[str, Any] | None = None


class MasterworkBuildProgressData(DataPayload[Literal["masterwork_build_progress"]]):
    """One step of Building a Rulebook into a Masterwork (agents + workflow)."""

    type: Literal["masterwork_build_progress"] = "masterwork_build_progress"
    step: str  # "pack_loaded" | "auditor_ready" | "agent_created" | "workflow_validated" | ...
    message: str
    agent_id: str | None = None
    agent_name: str | None = None


class MasterworkAgentBuildData(DataPayload[Literal["masterwork_agent_build"]]):
    """AF-D door #11: one Masterwork agent built through the Agent Factory.

    Sent only when ``agent_factory.door_masterwork`` says ``pipeline``: once when the
    agent's build starts (``outcome`` None) and once when it ends. The Build page mounts
    the factory's progress for ``build_id``. A kept agent carries ``agent_id``; a refused
    one carries the ``outcome`` word and ``reason`` instead.
    """

    type: Literal["masterwork_agent_build"] = "masterwork_agent_build"
    role: str  # "editor" | "chief" | "maker"
    agent_name: str
    message: str
    build_id: str | None = None
    outcome: str | None = None
    agent_id: str | None = None
    reason: str | None = None
    #: Real cases the build was handed (O8); below the proof count the agent is built unproven.
    proof_cases: int = 0


class MasterworkSealedCaseDisclosureData(DataPayload[Literal["masterwork_sealed_case_disclosure"]]):
    """ONE fact a sealed case released, as it happens.

    THE POINT OF THE EVENT: a run that asks a sealed source for facts is doing
    its real work between the spinner and the answer, and nobody could see it.
    A run box renders these as "Question 3: … → …", so an Expert watches the
    Masterwork investigate instead of watching it think.

    A ``commit`` disclosure carries ``question``/``answer`` as the committed
    conclusion and NO correctness of any kind — the sealed source never grades.
    """

    type: Literal["masterwork_sealed_case_disclosure"] = "masterwork_sealed_case_disclosure"
    case_id: str
    #: The run this ledger belongs to (``workflow_run:<id>`` / ``request:<id>``).
    run_scope: str
    #: 1-based position in THIS run's ledger.
    seq: int
    #: "ask" | "commit".
    event: str = "ask"
    question: str = ""
    answer: str = ""
    #: False = the record does not say. A complete answer, not a failure.
    found: bool = True
    cost: str | None = None
    risk: str | None = None
    asked_kind: str | None = None
    disclosures_so_far: int = 0


class MasterworkIngestProgressData(DataPayload[Literal["masterwork_ingest_progress"]]):
    """One step of distilling a source into draft Rulebook rules."""

    type: Literal["masterwork_ingest_progress"] = "masterwork_ingest_progress"
    step: str  # "chunked" | "chunk_distilled" | "deduped" | "verified" | "saved"
    message: str
    chunk_index: int | None = None
    total_chunks: int | None = None
    rules_found: int | None = None


class MasterworkSourceAlreadyDistilled(BaseModel):
    """This source has ALREADY produced rules in this Rulebook.

    The named field that makes a repeat press honest (2026-09-12: a link was
    distilled twice into one Rulebook — 115 rules then 123 more — and the
    duplicate check reported 0, because rule-level dedupe cannot answer a
    source-level question). ``message`` is the sentence to show; ``can_replace``
    says whether offering "Distil again and replace" is meaningful (it is not
    when every earlier rule has already been approved by the Expert, since a
    machine never removes those)."""

    #: The source identity (``url:…`` / ``entity:…`` / ``file:…`` /
    #: ``conversation:…`` / ``text:<hash>``) — matches ``source_ref.source``.
    source: str
    #: What the person calls it (page title, file name, the URL itself).
    label: str | None = None
    rules: int = 0
    draft_rules: int = 0
    approved_rules: int = 0
    #: The durable masterwork run(s) that wrote them, when the rules carry one.
    run_ids: list[str] = Field(default_factory=list)
    message: str
    can_replace: bool = True


class MasterworkSectionYield(BaseModel):
    """What ONE part of a source — a chapter, a lesson, a heading — produced.

    🚨 The answer to W42 (2026-09-12): a 31k-word book was cut by a ruler, its
    most prescriptive chapter contributed 3 rules against its siblings' 15–23,
    and NOTHING anywhere said so. A source is now chunked by its own structure
    and every part reports its own yield, so a thin chapter is a row on a screen
    the Expert can point at and re-read, not a silent hole.
    """

    #: 1-based, in reading order. Matches ``source_ref.section_index``.
    index: int
    #: The source's own words for this part ("CHAPTER FIVE — NIGHT- AND
    #: DAY-TIME CARE OF THE CHILD"). Empty when the part has no heading.
    label: str = ""
    words: int = 0
    #: Distiller calls this part was spread across.
    chunks: int = 0
    #: Rules it contributed to the Rulebook, after dedupe.
    rules: int = 0
    #: True when the run read this part a SECOND time because its first yield
    #: was far below the rest of the source.
    second_pass: bool = False


class MasterworkIngestCompleteData(DataPayload[Literal["masterwork_ingest_complete"]]):
    """Terminal result of POST /masterworks/ingest."""

    type: Literal["masterwork_ingest_complete"] = "masterwork_ingest_complete"
    rulebook_id: str
    rulebook_version: int
    added: int = 0
    duplicates_skipped: int = 0
    quotes_verified: int = 0
    quotes_unverified: int = 0
    # Pieces of the source that could not be distilled even after being
    # retried smaller, and the words they held. Non-zero means rules are
    # MISSING from this run — the screen must say so (2026-09-10: a whole
    # chapter's method vanished behind "14 rules added, every quote verified").
    failed_chunks: int = 0
    skipped_words: int = 0
    # 🚨 How many of `added` were SET ASIDE as the document's PACKAGING rather
    # than its method — course administration, publisher boilerplate, exercises,
    # front/back matter, license text (W59, 2026-09-12: a participant workbook
    # produced 189 drafts, 26 of them the course's own logistics written as
    # clinical craft). They ARE written — as rejected drafts carrying the reason,
    # one click from being overruled — so `added` still counts every row this run
    # wrote, and the dialog says "N-M rules added, M set aside as packaging".
    packaging_set_aside: int = 0
    # Monologue (recording) lane only: a ready-to-use composer seed listing the
    # areas the expert touched but never explained, so the Scout interview
    # panel can offer "want me to ask about what you didn't cover?".
    followup_seed: str | None = None
    # 🚨 Set when the run REFUSED to re-distil a source this Rulebook already
    # holds rules from: `added` is 0 and this says why, names the earlier run
    # and its rule count, and is the client's cue to offer "Distil again and
    # replace" (`redistill="replace"`). Never prose in a progress message —
    # a screen must be able to render the choice.
    # A LIST because a lane can face several sources in one run: the chat lanes
    # distil many conversations, and each is refused or read on its own.
    # Single-source lanes (text, file, monologue) carry exactly one entry.
    already_distilled: list[MasterworkSourceAlreadyDistilled] = Field(default_factory=list)
    # How many earlier DRAFT rules a `redistill="replace"` run removed before
    # writing this pass. Approved rules are never removed.
    replaced_rules: int = 0
    # How many APPROVED rules this run NARROWED (never removed, never
    # touched otherwise) — the one exception to "a machine never touches an
    # approved rule": the same statement, read again from the same source,
    # produced a real (SEGMENT_GRAIN) time anchor strictly inside the
    # rule's existing range (`rulebook_writes.narrow_time_ranges_cas`).
    narrowed_rules: int = 0
    # ── The unfolding-case lane (POST /masterworks/ingest-timeline) ──────────
    # The `platform.masterwork_corpus_item` row the case was stored as. Named
    # on the terminal payload because a case is a THING the Expert now owns —
    # a screen that cannot address it is a dead end.
    corpus_item_id: str | None = None
    # This case was stored as a SEALED held-out exam case: `added` is 0 BY
    # DESIGN, not because the run found nothing. A screen must be able to tell
    # those two apart without reading prose.
    sealed: bool = False
    # How many moments the narrative was unfolded into.
    timeline_steps: int = 0
    # "teaching" | "heldout" — the role the Expert chose for this case. The
    # client seals on it, so it has to BE on the payload: without it a held-out
    # case parsed as a teaching one and its answer rendered.
    role: str | None = None
    # The unfolded `serial_observation_timeline` kind instance, ready for the
    # kind component. 🚨 For a held-out case this is the SEALED payload —
    # `sealed: true` and NO `resolution` — built by
    # `timeline_ingest.wire_timeline_payload`. The answer to an exam case never
    # rides this field.
    timeline: dict[str, JsonValue] | None = None
    # Per-part yield when the source divides itself into parts (chapters,
    # lessons, headings). Empty for a source with no structure — never a fake
    # single row, because "one section" is exactly what a ruler produces and
    # the point of this field is to show the difference.
    sections: list[MasterworkSectionYield] = Field(default_factory=list)


class MasterworkTriageDecision(BaseModel):
    """What the triage pass decided about ONE draft rule, and why.

    The unit of the dry-run PLAN. ``verdict`` is ``retire`` | ``keep`` |
    ``rewrite``; ``statement`` carries the generalised wording on a ``rewrite``
    and is empty otherwise. A decision always names the rule it is about — a
    plan the Expert cannot check rule by rule is prose again.
    """

    rule_id: str
    name: str = ""
    verdict: str = "keep"
    reason: str = ""
    statement: str = ""


class MasterworkTriageProgressData(DataPayload[Literal["masterwork_triage_progress"]]):
    """One batch of the draft-triage pass (POST /masterworks/triage).

    Counts are CUMULATIVE across the run so a run box can show the pile
    shrinking instead of a spinner — the wall this closes (W59/W61) was a run
    that showed nothing for minutes and then died.
    """

    type: Literal["masterwork_triage_progress"] = "masterwork_triage_progress"
    # "planned" | "batch_done" | "batch_failed" | "batch_split" | "applied"
    step: str
    message: str
    batch_index: int | None = None
    batch_count: int | None = None
    drafts_total: int = 0
    retired: int = 0
    kept: int = 0
    rewritten: int = 0


class MasterworkTriageCompleteData(DataPayload[Literal["masterwork_triage_complete"]]):
    """Terminal result of POST /masterworks/triage."""

    type: Literal["masterwork_triage_complete"] = "masterwork_triage_complete"
    rulebook_id: str
    rulebook_version: int
    drafts_considered: int = 0
    retired: int = 0
    kept: int = 0
    rewritten: int = 0
    #: Ids the write REFUSED to retire because the Expert has approved them.
    #: A machine never removes what a human approved (the human-first law), and
    #: the screen says so rather than reporting a clean sweep.
    refused: list[str] = Field(default_factory=list)
    #: Batches that could not be triaged even after being retried smaller.
    #: Non-zero means drafts were NOT looked at — the screen must say so.
    failed_batches: int = 0
    drafts_unreviewed: int = 0
    #: True when nothing was written: the Expert asked to see the plan first.
    dry_run: bool = False
    #: The plan, rule by rule. Always carried on a dry run; on a real run it is
    #: the record of what was done.
    decisions: list[MasterworkTriageDecision] = Field(default_factory=list)


class MasterworkShortlistItem(BaseModel):
    """One conversation the shortlister picked, with its plain-language reason."""

    key: str
    reason: str = ""


class MasterworkShortlistData(DataPayload[Literal["masterwork_shortlist"]]):
    """Result of the chat-import shortlister: which of the Expert's
    conversations look worth distilling. Selection help only — the Expert
    confirms the selection in the picker."""

    type: Literal["masterwork_shortlist"] = "masterwork_shortlist"
    selected: list[MasterworkShortlistItem] = Field(default_factory=list)
    considered: int = 0


class MasterworkTriadItem(BaseModel):
    """ONE of the three short items the Expert reacts to in a Triad.

    Deliberately tiny: a candidate answer, a way of opening an email, a bid.
    ``key`` is ``"a"`` / ``"b"`` / ``"c"`` — the stable handle the pick names,
    never the position on screen."""

    key: str
    text: str
    #: A few words naming the item ("the cautious bid"), when the generator has
    #: one. NEVER the answer, and never a hint at which item is "right" — a
    #: forced choice with a labeled winner measures nothing.
    note: str = ""


class MasterworkTriad(BaseModel):
    """THREE short items and the one question put to the Expert.

    The repertory-grid unit (``platform.approach`` key ``triad_game``): the
    triad is the EVIDENCE, the Expert's one-line reason is the rule candidate.
    ``id`` is the provenance every rule distilled from this triad cites
    (``source_ref.triad`` and ``source_ref.source = "triad:<id>"``)."""

    id: str
    prompt: str
    items: list[MasterworkTriadItem] = Field(default_factory=list)
    #: ``"best_one"`` (which of these three would you actually use?) or
    #: ``"odd_one_out"`` (which two are alike, and which is the odd one?).
    mode: str = "best_one"


class MasterworkTriadsReadyData(DataPayload[Literal["masterwork_triads_ready"]]):
    """Terminal result of POST /masterworks/triads — the deck for one session.

    Nothing is written to the Rulebook by this call: a generated triad is a
    QUESTION, and only the Expert's answer to it is ever distilled."""

    type: Literal["masterwork_triads_ready"] = "masterwork_triads_ready"
    rulebook_id: str
    triads: list[MasterworkTriad] = Field(default_factory=list)
    mode: str = "best_one"
    #: How many the session asked for (the knob, or the caller's override).
    requested: int = 0
    #: How many the generator returned that this session had ALREADY played and
    #: were therefore dropped. Named, never silent: a repeated triad is the one
    #: way this lane can waste an Expert's attention.
    repeats_dropped: int = 0
    #: Is the microphone armed when the "why?" box opens? The org knob's
    #: resolved answer, sent WITH the deck so the play surface never reads the
    #: knob table itself and an org override cannot be half-applied.
    voice_default_on: bool = True


class MasterworkSortCase(BaseModel):
    """ONE case on THE SORTING TABLE — a thing an Expert sorts with a thumb.

    Deliberately tiny: a claim, a lead, a submission, a ticket. ``note`` is
    where it came from in the Expert's own terms ("from your CRM"), NEVER a
    hint at which pile it belongs in — a sort with a labeled answer measures
    nothing."""

    id: str
    text: str
    note: str = ""


class MasterworkSortCasesReadyData(DataPayload[Literal["masterwork_sort_cases_ready"]]):
    """Terminal result of POST /masterworks/sort/cases — one round of cases
    written for an Expert who brought none.

    Nothing is written to the Rulebook by this call: an unsorted case is not
    expertise, and only the Expert's answer to a BOUNDARY question is ever
    distilled."""

    type: Literal["masterwork_sort_cases_ready"] = "masterwork_sort_cases_ready"
    rulebook_id: str
    cases: list[MasterworkSortCase] = Field(default_factory=list)
    #: How many the round asked for (the knob, or the caller's override).
    requested: int = 0
    #: How many the writer returned that this sitting had ALREADY sorted and
    #: were therefore dropped. Named, never silent.
    repeats_dropped: int = 0
    #: The org knobs' resolved answers, sent WITH the round so the sorting
    #: surface never reads the knob table itself and an org override cannot be
    #: half-applied by a stale tab.
    pile_count: int = 3
    boundary_questions: int = 5
    voice_default_on: bool = True


class MasterworkProbeRoundData(DataPayload[Literal["masterwork_probe_round"]]):
    """Terminal result of POST /masterworks/probe — ONE round of the Bad
    Example probe.

    Two things in one payload, because one call does two things: whatever the
    Expert's critique of the PREVIOUS round produced (``rules_added`` and the
    ids, so the screen can say what their catch was worth), and the NEXT
    plausible-but-wrong piece of work for them to attack.

    🚨 ``done`` is not derived on the client. A probe ends because the Expert
    said "I'd never see that" or because the organization's round knob ran out,
    and ``done_reason`` says which in the Expert's own terms — a screen that
    guessed would eventually guess wrong.
    """

    type: Literal["masterwork_probe_round"] = "masterwork_probe_round"
    rulebook_id: str
    rulebook_version: int = 0
    #: 1-based. The round this payload CARRIES when ``done`` is false; the last
    #: round that was shown when it is true.
    round_index: int = 0
    #: The cap this session is running to — the org knob, or the session's own
    #: lower choice. Shown, so "round 3 of 5" is never invented by the client.
    round_count: int = 0
    done: bool = False
    #: Why the probe stopped, in plain words ("you said you would never see
    #: that"). Empty while it is still running.
    done_reason: str = ""
    #: The work product itself — confident, well-formed, and wrong. Empty on a
    #: ``done`` payload, because there is nothing more to show.
    example_title: str = ""
    example_body: str = ""
    #: The boundary this variant probes, as the generator named it. Carried back
    #: on the next request so a later round cannot re-probe covered ground; it
    #: is NOT the answer and must never be rendered beside the example.
    probe_label: str = ""
    #: What the Expert's LAST critique produced. Zero is an honest answer: a
    #: catch that carried no reusable judgment writes no rule.
    rules_added: int = 0
    rule_ids: list[str] = Field(default_factory=list)
    duplicates_skipped: int = 0
    quotes_verified: int = 0
    quotes_unverified: int = 0
    #: Set when this round's critique was ALREADY distilled (a double submit).
    #: `rules_added` is 0 and this says why — never silence, never a second
    #: paid pass over one answer.
    already_distilled: list[MasterworkSourceAlreadyDistilled] = Field(default_factory=list)
    #: How many rounds of this session the Expert has actually answered.
    answered_rounds: int = 0


class MasterworkTeachBackRoundData(DataPayload[Literal["masterwork_teach_back_round"]]):
    """Terminal result of POST /masterworks/teach-back — ONE round of a
    Teach-Back.

    Two things in one payload, because one call does two things: whatever the
    Expert's CORRECTION of the previous round produced (``rules_added`` and the
    ids, so the screen can say what their interruption was worth), and the NEXT
    explanation for them to hear and interrupt.

    🚨 ``basis`` is not cosmetic and is never derived on the client. A
    teach-back on an EMPTY Rulebook explains what a competent generalist would
    do, and the screen must say so in the Expert's own terms — a generalist
    explanation presented as "here is what we learned from you" is the
    platform lying about whose judgment it is reading back.

    🚨 ``done`` is not derived on the client either. A teach-back ends because
    the Expert said "yes, that's it" or because the organization's round knob
    ran out, and ``done_reason`` says which in their own terms.
    """

    type: Literal["masterwork_teach_back_round"] = "masterwork_teach_back_round"
    rulebook_id: str
    rulebook_version: int = 0
    #: The durable ``platform.masterwork_run`` row this round ran under — the
    #: SUBJECT the Expert's signature is written against when they sign this
    #: explanation (`masterwork.expert_signature` on `platform.output_feedback`).
    #: Empty only when the run was not durable, and the screen then says the
    #: signature cannot be recorded rather than pretending it was.
    run_id: str = ""
    #: 1-based. The round this payload CARRIES when ``done`` is false; the last
    #: round that was shown when it is true.
    round_index: int = 0
    #: The cap this session is running to — the org knob, or the session's own
    #: lower choice. Shown, so "round 3 of 6" is never invented by the client.
    round_count: int = 0
    done: bool = False
    #: Why the teach-back stopped, in plain words ("you said that's it").
    done_reason: str = ""
    #: The ONE decision this round explained back, in the Expert's own words.
    subject: str = ""
    #: The explanation itself — plain words, meant to be read aloud AND shown.
    #: Empty on a ``done`` payload, because there is nothing more to say back.
    explanation: str = ""
    #: `rulebook` | `generalist` | "" (on a done payload). See the class note.
    basis: str = ""
    #: The Rulebook rule ids this explanation leaned on — empty on the
    #: generalist basis. These are the rules a "yes, that's it" signs.
    rule_ids_cited: list[str] = Field(default_factory=list)
    #: The part the explainer says it is least sure about, in its own words.
    #: Shown under the explanation: it is the invitation to interrupt.
    uncertain_part: str = ""
    #: WHICH round this call actually distilled, 1-based — or 0 when there was
    #: nothing to distil (round one, or a "yes, that's it" pressed without
    #: correcting anything first).
    #:
    #: 🚨 The screen may NOT derive this from ``rules_added``. Zero rules from a
    #: correction and zero rules because nobody corrected anything are different
    #: facts, and the sentence for the first ("nothing new came out of that one")
    #: is a lie when said about the second — observed on the live sign-off
    #: screen, 2026-09-15, and this field is the fix.
    distilled_round: int = 0
    #: What the Expert's LAST correction produced. Zero is an honest answer: a
    #: correction that carried no reusable judgment writes no rule.
    rules_added: int = 0
    rule_ids: list[str] = Field(default_factory=list)
    duplicates_skipped: int = 0
    quotes_verified: int = 0
    quotes_unverified: int = 0
    #: The rules a "yes, that's it" stamped as a signed teach-back. Empty until
    #: the Expert signs, and empty (with ``signature_note`` saying why) when the
    #: signed explanation cited no rule that is still on the Rulebook.
    signed_rule_ids: list[str] = Field(default_factory=list)
    #: The honest sentence about the signature: what was signed, or why nothing
    #: was. Never silence.
    signature_note: str = ""
    #: Set when this round's correction was ALREADY distilled (a double submit).
    already_distilled: list[MasterworkSourceAlreadyDistilled] = Field(default_factory=list)
    #: How many rounds of this session the Expert has actually corrected.
    answered_rounds: int = 0


class MasterworkDumpResourceOutcome(BaseModel):
    """One resource's outcome inside a dump ingest — honest per-resource
    accounting, so a refused URL or an unsupported entity type is a visible
    row, never a silent skip."""

    kind: str  # "entity" | "url" | "kept_source"
    token: str | None = None
    id: str | None = None
    url: str | None = None
    #: 🚨 THE ONLY IDENTITY A `kept_source` ROW HAS ON THIS WIRE. `token`/`id`
    #: /`url` are all null for material the Rulebook already holds, so a screen
    #: that wanted to offer "read it again" for a refused kept source had
    #: nothing to send back and the offer could not be built (cold walk 13,
    #: N7 — the refusal sentence named a control the panel could not render).
    #: Echoed straight from the request's own resource.
    source_key: str | None = None
    title: str | None = None
    status: str  # "ok" | "failed" | "unsupported" | "already_distilled"
    rules_added: int = 0
    duplicates: int = 0
    error: str | None = None
    #: 🚨 WHY A SUCCESSFUL SOURCE ADDED NOTHING. A source read end to end whose
    #: content held no reusable rule is `status="ok"` with `rules_added=0` — it
    #: did not fail — and this carries the distiller's own sentence saying so,
    #: which would otherwise be the one fact the row cannot express. It is never
    #: an error: a reader must not render it as one (board row B4e, 2026-09-18).
    note: str | None = None
    #: Set when status == "already_distilled": this resource was refused
    #: because the Rulebook already holds rules from it.
    already_distilled: MasterworkSourceAlreadyDistilled | None = None
    #: Earlier drafts removed by a `redistill="replace"` run of this resource.
    replaced_rules: int = 0


class MasterworkDumpProgressData(DataPayload[Literal["masterwork_dump_progress"]]):
    """One step of the resource-dump distillation lane (POST
    /masterworks/ingest-dump). Chunk-level detail still arrives as the
    underlying lane's ``masterwork_ingest_progress`` events; this event is the
    per-RESOURCE frame around them."""

    type: Literal["masterwork_dump_progress"] = "masterwork_dump_progress"
    # "resource_started" | "resource_done" | "resource_failed"
    # | "resource_unsupported" | "resource_already_distilled"
    step: str
    message: str
    resource_index: int
    resource_count: int
    kind: str | None = None
    token: str | None = None
    id: str | None = None
    url: str | None = None
    title: str | None = None
    rules_added: int | None = None
    rules_added_total: int = 0


class MasterworkDumpCompleteData(DataPayload[Literal["masterwork_dump_complete"]]):
    """Terminal result of POST /masterworks/ingest-dump — totals plus the full
    per-resource outcome list."""

    type: Literal["masterwork_dump_complete"] = "masterwork_dump_complete"
    rulebook_id: str
    rulebook_version: int
    added: int = 0
    duplicates_skipped: int = 0
    quotes_verified: int = 0
    quotes_unverified: int = 0
    resources: list[MasterworkDumpResourceOutcome] = Field(default_factory=list)
    #: Every resource this run refused because the Rulebook already holds rules
    #: from it — the run-level named field, beside the per-resource outcomes.
    already_distilled: list[MasterworkSourceAlreadyDistilled] = Field(default_factory=list)
    #: Earlier drafts removed across the run by `redistill="replace"`.
    replaced_rules: int = 0


class AuditionRuleFinding(BaseModel):
    """One rule's comparison verdict inside an Audition."""

    rule_id: str
    winner: str  # "candidate" | "reference" | "tie"
    note: str = ""


class MasterworkAuditionProgressData(DataPayload[Literal["masterwork_audition_progress"]]):
    """One stage of an Audition (vanilla arm generation, per-arm judging)."""

    type: Literal["masterwork_audition_progress"] = "masterwork_audition_progress"
    step: (
        str  # "vanilla_generating" | "vanilla_generated" | "judging_masterwork" | "judging_vanilla"
    )
    message: str


class MasterworkAuditionOutcomeVerdictData(DataPayload[Literal["masterwork_audition_outcome_verdict"]]):
    """Terminal result of POST /masterworks/audition-outcome — the OUTCOME mode:
    a Masterwork run over a SEALED CASE judged by the fact the case only reveals
    at the bottom, plus the path it took to get there.

    The judge returned the enumerated ``verdict`` (match | partial | miss) and
    the ``dangerous_branch`` finding and NOTHING numeric. Every number here is
    derived mechanically from the case's own disclosure ledger and the
    ``masterwork.outcome_weights`` knob (echoed in ``weights`` so a reader can
    reproduce ``quality_score`` exactly):

        quality_score = outcome_points - cost_weight * cost_points
                        - risk_weight * risk_points - dangerous_branch_penalty,
        floored at 0.

    The ``vanilla_*`` fields exist only for ``compare_vanilla`` runs: the same
    model tier handed the WHOLE case (resolution stripped) in one call, with
    zero disclosures by construction, judged by the same judge."""

    type: Literal["masterwork_audition_outcome_verdict"] = "masterwork_audition_outcome_verdict"
    rulebook_id: str
    case_id: str
    run_scope: str
    verdict: str  # "match" | "partial" | "miss"
    why: str = ""
    summary: str = ""
    judge_confidence: float | None = None
    dangerous_branch: bool = False
    dangerous_branch_quote: str = ""
    decisive_question_seq: int | None = None
    missed_cheaper_question: str = ""
    disclosures: int = 0
    asks: int = 0
    cost_points: int = 0
    risk_points: int = 0
    quality_score: float | None = None
    weights: dict[str, float] = {}
    vanilla_compared: bool = False
    vanilla_verdict: str | None = None
    vanilla_answer: str | None = None
    vanilla_score: float | None = None
    vanilla_model: str | None = None
    vanilla_error: str | None = None
    beat_vanilla: bool | None = None
    verdict_sentence: str | None = None


class MasterworkAuditionVerdictData(DataPayload[Literal["masterwork_audition_verdict"]]):
    """Terminal result of POST /masterworks/audition — the R2 outcome
    signal: Masterwork output vs the real published exemplar, judged rule-by-rule
    against the Rulebook.

    ``quality_score`` is DERIVED 0-100 (win 1 / tie 0.5 / loss 0 over the
    judged rules) — the judge's verdicts stay enumerated. The ``vanilla_*``
    fields exist only for three-way runs (``compare_vanilla``): the same judge
    scored a raw no-Rulebook model of the Masterwork's own tier against the
    same reference, and ``verdict_sentence`` states the result plainly."""

    type: Literal["masterwork_audition_verdict"] = "masterwork_audition_verdict"
    rulebook_id: str
    verdict: str  # "candidate_better" | "parity" | "reference_better"
    summary: str
    findings: list[AuditionRuleFinding] = []
    gaps: list[str] = []
    gaps_captured: int = 0
    rulebook_version: int | None = None
    quality_score: float | None = None
    judge_confidence: float | None = None
    vanilla_compared: bool = False
    vanilla_score: float | None = None
    vanilla_verdict: str | None = None
    vanilla_findings: list[AuditionRuleFinding] = []
    vanilla_text: str | None = None
    vanilla_model: str | None = None
    #: How the vanilla arm was built, in one sentence — which model tier it
    #: mirrors, how many of the Masterwork's steps run that tier, and where the
    #: plain-English ask came from. A Masterwork with several models has no
    #: single "its model"; the arm picks the dominant one and SAYS SO here.
    vanilla_note: str | None = None
    vanilla_error: str | None = None
    beat_vanilla_rules: int | None = None
    lost_to_vanilla_rules: int | None = None
    vanilla_rules_compared: int | None = None
    verdict_sentence: str | None = None


class UnfoldingArmResult(BaseModel):
    """One arm's result on one sealed case in an unfolding Audition.

    `diagnosis` / `dangerous_branch` are the judge's ENUM verdicts; every number
    here is DERIVED in code (`audition_unfolding.py`) — the judge is never asked
    for one, and `steps`/`cost`/`risk` are read off the case oracle's ledger."""

    arm: str  # "desk:<masterwork_id>" | "vanilla"
    label: str = ""
    diagnosis: str = "miss"  # "match" | "partial" | "miss"
    diagnosis_score: float = 0.0
    dangerous_branch: str = "none"  # "none" | "considered" | "committed"
    branch_named: str = ""
    safety_score: float = 0.0
    steps: int = 0
    cost: int = 0
    risk: int = 0
    committed_at_step: int | None = None
    answer: str = ""
    reasoning: str = ""
    judge_confidence: float | None = None
    run_id: str | None = None
    error: str | None = None


class UnfoldingCaseResult(BaseModel):
    """One sealed held-out case, every arm judged against its sealed outcome."""

    case_item_id: str
    label: str = ""
    arms: list[UnfoldingArmResult] = []


class MasterworkAuditionUnfoldingVerdictData(DataPayload[Literal["masterwork_audition_unfolding_verdict"]]):
    """Terminal result of POST /masterworks/audition with `mode="unfolding"`.

    The unfolding benchmark (unfolding-case-contract §4): one or two Masterwork
    desks each WALK a sealed case through the case oracle, a vanilla model of the
    desk's own tier is told every step's facts at once, and one judge ranks each
    arm's diagnosis against the case's sealed `resolution.outcome`.
    `quality_score` is the first desk's mean diagnosis_score (0-100)."""

    type: Literal["masterwork_audition_unfolding_verdict"] = "masterwork_audition_unfolding_verdict"
    rulebook_id: str
    masterwork_ids: list[str] = []
    cases: list[UnfoldingCaseResult] = []
    quality_score: float | None = None
    desk_match_rate: float | None = None
    vanilla_match_rate: float | None = None
    desk_beats_vanilla: bool | None = None
    vanilla_compared: bool = False
    vanilla_model: str | None = None
    cases_judged: int = 0
    arm_errors: list[str] = []
    verdict_sentence: str = ""


class ElicitationArmResult(BaseModel):
    """One arm's scorecard on one sealed counterparty profile.

    EVERY number here is COUNTED in `audition_elicitation.py` from the arm's
    transcript and the sealed profile — the LLM judge is asked one enum per
    utterance (advice | question | reflection | other) and nothing else.

    `frame_order_status` is the honest half: a Rulebook whose moves carry no
    frame or order cannot be compared with the source's own ordering, so the
    distance is `null` with status "unmeasured" and a remedy sentence — never
    a zero, which would read as a perfect score."""

    arm: str  # "desk:<masterwork_id>" | "vanilla"
    label: str = ""
    facts_surfaced: int = 0
    facts_total: int = 0
    facts_surfaced_rate: float = 0.0
    turns: int = 0
    turns_to_frame: int | None = None
    frame_held: bool = False
    premature_advice_events: int = 0
    #: What the counterparty node counted from the desk's OWN move_class, beside
    #: the judged count above. A gap between the two is a finding, not noise: a
    #: desk that calls its prescription "reflect" fools the person, not the
    #: Audition.
    ledger_premature_advice: int | None = None
    lockouts_caused: int = 0
    frame_order_distance: int | None = None
    frame_order_status: str = "unmeasured"  # "measured" | "unmeasured"
    frame_order_remedy: str = ""
    frames_walked: list[str] = []
    utterance_classes: list[str] = []
    unclassified_turns: int = 0
    note: str = ""
    run_id: str | None = None
    error: str | None = None


class ElicitationProfileResult(BaseModel):
    """One sealed counterparty profile, every arm scored against it."""

    profile_item_id: str
    label: str = ""
    arms: list[ElicitationArmResult] = []


class MasterworkAuditionElicitationVerdictData(DataPayload[Literal["masterwork_audition_elicitation_verdict"]]):
    """Terminal result of POST /masterworks/audition with `mode="elicitation"`.

    The first move (trial 12): one or two Masterwork desks each hold a real
    conversation with a sealed, reactive counterparty while a vanilla model of
    the desk's own tier is handed the opening line and answers it. The headline
    IS the contrast — the vanilla arm surfaces ~no decisive facts and advises
    anyway. `quality_score` is the first desk's mean facts-surfaced rate
    (0-100)."""

    type: Literal["masterwork_audition_elicitation_verdict"] = (
        "masterwork_audition_elicitation_verdict"
    )
    rulebook_id: str
    masterwork_ids: list[str] = []
    profiles: list[ElicitationProfileResult] = []
    quality_score: float | None = None
    desk_facts_surfaced_rate: float | None = None
    vanilla_facts_surfaced_rate: float | None = None
    desk_premature_advice: int | None = None
    vanilla_premature_advice: int | None = None
    desk_beats_vanilla: bool | None = None
    vanilla_compared: bool = False
    vanilla_model: str | None = None
    profiles_scored: int = 0
    arm_errors: list[str] = []
    verdict_sentence: str = ""


class MasterworkPairwiseDifference(BaseModel):
    """ONE concrete, word-level difference between the two answers, UNSEALED —
    the judge wrote "A does X"; this says "the Masterwork does X"."""

    aspect: str
    one_does: str = ""
    two_does: str = ""
    matters: str = ""


class MasterworkPairwiseRuleNote(BaseModel):
    """One rule's reading in a pairwise Audition. ``winner`` names the arm
    ("one" | "two" | "tie"), already unsealed. In the faithfulness mode this
    carries a DEPARTURE: the rule the arm left, and the words that left it."""

    rule_id: str
    winner: str  # "one" | "two" | "tie"
    note: str = ""


class MasterworkPairwiseArmFaithfulness(BaseModel):
    """One arm's standing against ITS OWN school."""

    side: str  # "one" | "two"
    label: str
    rulebook_id: str
    verdict: str  # "faithful" | "partly_faithful" | "unfaithful"
    reasoning: str = ""
    confidence: float | None = None
    departures: list[MasterworkPairwiseRuleNote] = []
    honored_rule_ids: list[str] = []


class MasterworkPairwiseVerdictData(DataPayload[Literal["masterwork_pairwise_verdict"]]):
    """Terminal result of POST /masterworks/audition-pairwise — TWO candidates
    judged BLIND against each other, with no reference.

    The judge saw "A" and "B" and never the arms' real labels. Which arm was A
    was randomised and SEALED on the run row before the judge was called;
    ``blind_key`` is that same sealed mapping, revealed here and only here, with
    ``blind_key_sealed_at`` as the timestamp it was written.

    ``preference`` mode fills ``preferred`` / ``differences`` / ``rule_notes``;
    ``faithfulness`` mode fills ``faithfulness``, one entry per arm against its
    own Rulebook. NO SCORE FIELD EXISTS HERE and none may be added: a preference
    is an enumeration, and nuance rides ``judge_confidence``."""

    type: Literal["masterwork_pairwise_verdict"] = "masterwork_pairwise_verdict"
    rulebook_id: str
    mode: str  # "preference" | "faithfulness"
    candidate_one_label: str
    candidate_two_label: str
    preferred: str | None = None  # "one" | "two" | "tie"
    preferred_label: str | None = None
    judge_verdict: str = ""
    judge_confidence: float | None = None
    summary: str = ""
    differences: list[MasterworkPairwiseDifference] = []
    rule_notes: list[MasterworkPairwiseRuleNote] = []
    faithfulness: list[MasterworkPairwiseArmFaithfulness] = []
    blind_key: dict[str, str] = {}
    blind_key_sealed_at: str | None = None
    verdict_sentence: str | None = None


class MasterworkBuildCompleteData(DataPayload[Literal["masterwork_build_complete"]]):
    """Terminal result of POST /masterworks/build."""

    type: Literal["masterwork_build_complete"] = "masterwork_build_complete"
    workflow_id: str
    name: str
    masterwork_kind: str  # "edit" | "generate"
    rulebook_id: str
    rulebook_slug: str
    rulebook_version: int
    agent_ids: list[str] = Field(default_factory=list)
    #: The run button's words from the builder's own intake design
    #: ("Find my keywords"). None = the button shows its icon alone rather than
    #: inventing a verb (Arman, 2026-08-25: "'Do the work' as the button —
    #: that is fucking stupid. If you don't know what the button does, just
    #: put an icon.").
    submit_label: str | None = None


# ---------------------------------------------------------------------------
# Masterworks — the Final Checkup ("did we screw up?")
# ---------------------------------------------------------------------------


class MasterworkCorpusProgressData(DataPayload[Literal["masterwork_corpus_progress"]]):
    """One step of cleaning up everything the Expert said."""

    type: Literal["masterwork_corpus_progress"] = "masterwork_corpus_progress"
    step: str  # "loaded" | "segment_cleaned" | "segment_failed"
    message: str
    segment_label: str | None = None
    segment_index: int | None = None
    total_segments: int | None = None


class MasterworkCorpusCleanedData(DataPayload[Literal["masterwork_corpus_cleaned"]]):
    """Terminal result of POST /masterworks/clean-corpus.

    ``text`` is the whole cleaned corpus, labeled and in order — what the
    Expert is shown so they can see what they actually have. The same text is
    persisted on the Rulebook (``metadata.expert_corpus``), so this event is a
    convenience, never the only copy.
    """

    type: Literal["masterwork_corpus_cleaned"] = "masterwork_corpus_cleaned"
    rulebook_id: str
    rulebook_version: int
    segments: int = 0
    cleaned: int = 0
    reused: int = 0
    failed: int = 0
    total_chars: int = 0
    text: str = ""


class CheckupFinding(BaseModel):
    """ONE thing the Checkup believes we got wrong or missed.

    This is the contract every producer emits and every consumer reads. The
    two fields that make it trustworthy rather than noise: ``evidence`` is a
    VERBATIM quote of what the Expert actually said (mechanically verified
    against the corpus before it is emitted — an unverifiable quote is dropped,
    never shown), and ``confidence`` is the producer's honest certainty.
    """

    id: str
    kind: str  # "add" | "modify" | "remove"
    target_rule_id: str | None = None
    proposed: dict[str, Any] | None = None
    #: Optional extra `proposed` shapes the Expert can pick between (Arman:
    #: "where we have options they click to select the one that they want").
    #: Additive — the Final Checkup UI ignores it when absent.
    alternatives: list[dict[str, Any]] = Field(default_factory=list)
    reason: str = ""
    evidence: str = ""
    evidence_ref: dict[str, Any] = Field(default_factory=dict)
    confidence: float = 0.0
    source: str = ""
    #: The SAME finding as a canonical Content-IR value
    #: (``__kind: "masterwork_checkup_finding"``), projected ONCE on the server
    #: by ``masterwork_checkup/finding_ir.py``. It rides the finding itself so
    #: the terminal document — and therefore the durable run row a rejoin reads
    #: after a refresh — carries it too: a restored checkup renders through the
    #: same ONE kind component as a live one, with no second projection on the
    #: client to drift from this one.
    content_ir: dict[str, Any] | None = None


class MasterworkBenchProgressData(DataPayload[Literal["masterwork_bench_progress"]]):
    """One stage of a Trial Bench run (`POST /masterworks/{id}/bench/runs`).

    The Bench is the PROOF: six arms, a blind panel the expert's own withheld
    work has to win, dollars and seconds on every row. It runs for minutes and
    spends real money on every arm, so it narrates itself — a spinner over a
    paid six-arm trial is the silent-failure defect with a price tag.

    ``message`` is the sentence the SERVER wrote for this person; a surface
    renders it and never translates a stage name into copy of its own.
    ``arm`` is "" for a stage that belongs to no single arm (the corpus screen,
    the blinding, the extraction, the calibration leg, the panel).
    """

    type: Literal["masterwork_bench_progress"] = "masterwork_bench_progress"
    rulebook_id: str
    trial_id: str
    stage: str
    message: str
    arm: str = ""


class MasterworkBenchArmData(DataPayload[Literal["masterwork_bench_arm"]]):
    """One ARM of a Trial Bench run, the moment it finishes — with its price.

    Part III §4.1 puts quality, dollars and seconds on every row, and a screen
    that shows the verdict without them is showing a claim with its evidence
    removed. So each arm lands here as it completes rather than all six at the
    end: the person watching a run that costs money can see what it has cost.

    ``ran`` false with a non-empty ``error`` is an arm that did not produce an
    answer — a fact about the trial, never hidden and never rendered as a zero.
    """

    type: Literal["masterwork_bench_arm"] = "masterwork_bench_arm"
    rulebook_id: str
    trial_id: str
    #: a0 | a1 | a2 | b | c | gt
    arm: str
    #: The arm's own doctrine label ("A1 — frontier + the full corpus in context").
    label: str
    ran: bool = False
    error: str = ""
    cost_usd: float = 0.0
    seconds: float = 0.0
    #: False when the arm ran outside a priced path — the dollars are UNKNOWN
    #: on that row, which is a different thing from free.
    priced: bool = True
    #: The model tier this arm declared. Named `model` on the wire because that
    #: is the word a screen shows beside a row; the record's own field is
    #: `ArmResult.model_ref`.
    model: str = ""
    note: str = ""


class MasterworkBenchVerdictData(DataPayload[Literal["masterwork_bench_verdict"]]):
    """Terminal result of POST /masterworks/{rulebook_id}/bench/runs.

    THREE terminal shapes, and they are not interchangeable:

    * ``void`` — the expert's own artifact was in the blind pool and did not win
      it. The trial proves NOTHING and is never banked as a result.
    * ``not_scored`` — the panel failed its own calibration leg, so its votes
      decide nothing. Not a pass, not a fail, not a void: a void would blame the
      trial's inputs for a defect in the bench.
    * ``passed`` true/false — a real result, with ``win_claimed`` naming which
      of the three §4.2 wins (ceiling | quality | efficiency) was earned, or
      null for the honest "no win claimed".

    ``headline`` is the server's own sentence for the screen; it is derived from
    this record and travels with it so no client re-writes the claim.
    ``stored`` says whether the trial reached ``platform.masterwork_run``, and
    ``storage_note`` says WHY when it did not — a trial that could not be
    persisted is never a trial that quietly was not.
    """

    type: Literal["masterwork_bench_verdict"] = "masterwork_bench_verdict"
    rulebook_id: str
    trial_id: str
    passed: bool = False
    void: bool = False
    not_scored: bool = False
    void_reason: str = ""
    not_scored_reason: str = ""
    #: "ceiling" | "quality" | "efficiency" | None
    win_claimed: str | None = None
    win_rationale: str = ""
    #: The A arm the claim was made against, and the budget ceiling it ran to.
    arm: str = "a2"
    budget_multiple: float | None = None
    panel_winner: str | None = None
    panel_votes: int = 0
    gt_in_pool: bool = False
    gt_won: bool = False
    c_cost_usd: float | None = None
    c_seconds: float | None = None
    #: Every arm plus every judge call — what this trial cost in total.
    total_cost_usd: float = 0.0
    record_path: str | None = None
    report_path: str | None = None
    row_id: str | None = None
    stored: bool = False
    storage_note: str = ""
    headline: str = ""


class MasterworkCheckupProgressData(DataPayload[Literal["masterwork_checkup_progress"]]):
    """One step of a Final Checkup — including per-producer start/finish, so a
    slow producer never looks like a hung run."""

    type: Literal["masterwork_checkup_progress"] = "masterwork_checkup_progress"
    step: str  # "corpus_loaded" | "producer_started" | "producer_done" | "producer_failed"
    message: str
    producer: str | None = None
    findings_found: int | None = None
    findings_dropped: int | None = None


class MasterworkCheckupFindingData(DataPayload[Literal["masterwork_checkup_finding"]]):
    """One finding, streamed the moment the producer's agent writes it.

    ``content_ir`` carries the SAME finding as a canonical Content-IR value
    (``__kind: "masterwork_checkup_finding"``). The frontend's one stream
    chokepoint promotes it into a real render block, so the platform's ONE
    renderer draws the finding live — no surface parses this event's content,
    and there is no second renderer to drift. ``finding`` stays exactly as it
    was for the surface's own decision state.
    """

    type: Literal["masterwork_checkup_finding"] = "masterwork_checkup_finding"
    rulebook_id: str
    finding: CheckupFinding
    content_ir: dict[str, Any] | None = None


class MasterworkCheckupCompleteData(DataPayload[Literal["masterwork_checkup_complete"]]):
    """Terminal result of POST /masterworks/checkup — the full finding set.

    ``findings: []`` with ``producers_failed: 0`` is a GOOD outcome, not an
    empty one: it means nothing is demonstrably wrong with the Rulebook.
    """

    type: Literal["masterwork_checkup_complete"] = "masterwork_checkup_complete"
    rulebook_id: str
    rulebook_version: int
    findings: list[CheckupFinding] = Field(default_factory=list)
    producers_run: list[str] = Field(default_factory=list)
    producers_failed: list[str] = Field(default_factory=list)
    evidence_rejected: int = 0
    #: Findings the Expert already dismissed in an earlier checkup, matched on
    #: `rulebook.metadata.checkup.dismissed` and never shown again.
    already_dismissed: int = 0
    corpus_segments: int = 0
    corpus_chars: int = 0
    corpus_cleaned: bool = False
    notes: list[str] = Field(default_factory=list)


# ---------------------------------------------------------------------------
# PDF extraction — real-time per-page progress (stream-everything mandate)
# ---------------------------------------------------------------------------


class PdfExtractStartedData(DataPayload[Literal["pdf_extract_started"]]):
    """Extraction began — the document is open and the page count is known."""

    type: Literal["pdf_extract_started"] = "pdf_extract_started"
    filename: str | None = None
    total_pages: int


class PdfPageExtractedData(DataPayload[Literal["pdf_page_extracted"]]):
    """One page finished extracting (native text or OCR fallback).

    ``preview`` is a capped slice of the page text so the UI can show live
    content without shipping the full document twice — the complete event
    carries the full ``text_content``.
    """

    type: Literal["pdf_page_extracted"] = "pdf_page_extracted"
    page_number: int
    total_pages: int
    extraction_method: str  # "native" | "ocr"
    char_count: int
    preview: str = ""


class PdfExtractCompleteData(DataPayload[Literal["pdf_extract_complete"]]):
    """Terminal extraction result — the full text plus summary counters.

    Carries the same content the legacy blocking JSON response did, so a
    migrating client reads this one event as the old response body.
    """

    type: Literal["pdf_extract_complete"] = "pdf_extract_complete"
    filename: str | None = None
    #: Pages actually extracted (the requested slice, or the whole document).
    page_count: int
    #: The document's full page count, and the 1-based inclusive slice read.
    total_pages: int | None = None
    page_start: int | None = None
    page_end: int | None = None
    ocr_pages: int
    total_chars: int
    text_content: str
    # processed_documents row id when the caller asked to persist.
    file_id: str | None = None


class PdfCleanStartedData(DataPayload[Literal["pdf_clean_started"]]):
    """Content-clean run began. ``mode='per_page'`` marks the run as
    resumable — a dropped client can re-invoke the endpoint and only the
    unfinished pages are re-paid."""

    type: Literal["pdf_clean_started"] = "pdf_clean_started"
    mode: Literal["per_page", "aggregate"] = "per_page"
    doc_id: str
    total_pages: int = 0


# ---------------------------------------------------------------------------
# PDF analyzers — per-page / per-table streaming (stream-everything mandate)
# ---------------------------------------------------------------------------


class PdfTableBboxItem(BaseModel):
    """Bbox of a detected table on its page (PDF coordinates)."""

    x0: float
    y0: float
    x1: float
    y1: float


class PdfExtractedTableItem(BaseModel):
    """One detected table — mirrors matrx-utils ``PdfExtractedTable``."""

    page_number: int
    table_index: int
    bbox: PdfTableBboxItem
    row_count: int
    column_count: int
    header: list[str | None] = Field(default_factory=list)
    rows: list[list[str | None]] = Field(default_factory=list)
    markdown: str = ""


class PdfTablesStartedData(DataPayload[Literal["pdf_tables_started"]]):
    """Table detection began — the document is open, page count known."""

    type: Literal["pdf_tables_started"] = "pdf_tables_started"
    filename: str | None = None
    total_pages: int


class PdfTablesPageData(DataPayload[Literal["pdf_tables_page"]]):
    """One page scanned for tables (fires even when the page has none)."""

    type: Literal["pdf_tables_page"] = "pdf_tables_page"
    page_number: int
    total_pages: int
    tables_found: int


class PdfTableExtractedData(DataPayload[Literal["pdf_table_extracted"]]):
    """One table detected. ``markdown_preview`` is capped; the complete
    event carries every full table."""

    type: Literal["pdf_table_extracted"] = "pdf_table_extracted"
    page_number: int
    total_pages: int
    table_index: int
    row_count: int
    column_count: int
    markdown_preview: str = ""


class PdfTablesCompleteData(DataPayload[Literal["pdf_tables_complete"]]):
    """Terminal — the same content the legacy blocking ``PdfTablesReport``
    response carried, so a migrating client reads this one event as the old
    response body."""

    type: Literal["pdf_tables_complete"] = "pdf_tables_complete"
    page_count: int
    table_count: int
    tables: list[PdfExtractedTableItem] = Field(default_factory=list)
    detector: str = "pymupdf.find_tables"
    detector_version: str = "v1"


class PdfPageClassificationItem(BaseModel):
    """One page's layout classification — mirrors matrx-utils ``PageClassification``."""

    page_number: int
    page_class: str
    confidence: float
    indicators: list[str] = Field(default_factory=list)


class PdfPageClassifiedData(DataPayload[Literal["pdf_page_classified"]]):
    """One page classified (cover / toc / body / exhibit / billing / ...)."""

    type: Literal["pdf_page_classified"] = "pdf_page_classified"
    page_number: int
    total_pages: int
    page_class: str
    confidence: float
    indicators: list[str] = Field(default_factory=list)


class PdfClassifyCompleteData(DataPayload[Literal["pdf_classify_complete"]]):
    """Terminal — the legacy ``LayoutClassificationReport`` response body."""

    type: Literal["pdf_classify_complete"] = "pdf_classify_complete"
    page_count: int
    pages: list[PdfPageClassificationItem] = Field(default_factory=list)
    classifier_version: str = "v1"


class PdfReadingOrderBlockItem(BaseModel):
    """One text block in reading order — mirrors matrx-utils ``ReadingOrderBlock``."""

    block_index: int
    column_index: int
    x0: float
    y0: float
    x1: float
    y1: float
    text: str


class PdfReadingOrderPageItem(BaseModel):
    """One page's ordered blocks — mirrors matrx-utils ``ReadingOrderPage``."""

    page_number: int
    column_count: int
    blocks_in_order: list[PdfReadingOrderBlockItem] = Field(default_factory=list)


class PdfReadingOrderPageData(DataPayload[Literal["pdf_reading_order_page"]]):
    """One page's reading order resolved. ``preview`` is a capped slice of
    the ordered text; the complete event carries the full block lists."""

    type: Literal["pdf_reading_order_page"] = "pdf_reading_order_page"
    page_number: int
    total_pages: int
    column_count: int
    block_count: int
    preview: str = ""


class PdfReadingOrderCompleteData(DataPayload[Literal["pdf_reading_order_complete"]]):
    """Terminal — the legacy ``ReadingOrderReport`` response body."""

    type: Literal["pdf_reading_order_complete"] = "pdf_reading_order_complete"
    page_count: int
    pages: list[PdfReadingOrderPageItem] = Field(default_factory=list)


class PdfRepeatedRegionBboxItem(BaseModel):
    """Per-page bbox of a repeated region — mirrors matrx-utils ``RepeatedRegionBbox``."""

    page_number: int
    x0: float
    y0: float
    x1: float
    y1: float
    raw_text: str = ""


class PdfRepeatedRegionItem(BaseModel):
    """One repeated region — mirrors matrx-utils ``RepeatedRegion``."""

    region_id: str
    kind: str
    text_template: str
    pages: list[int] = Field(default_factory=list)
    bbox_per_page: list[PdfRepeatedRegionBboxItem] = Field(default_factory=list)
    confidence: float


class PdfRepeatedRegionsProgressData(DataPayload[Literal["pdf_repeated_regions_progress"]]):
    """Per-page progress through a repeated-regions stage (detect scan /
    per-page text extraction / strip)."""

    type: Literal["pdf_repeated_regions_progress"] = "pdf_repeated_regions_progress"
    stage: Literal["detect", "extract_text", "strip"]
    page_number: int
    total_pages: int


class PdfRepeatedRegionsCompleteData(DataPayload[Literal["pdf_repeated_regions_complete"]]):
    """Terminal for detect-repeated-regions — the legacy
    ``RepeatedRegionsReport`` response body."""

    type: Literal["pdf_repeated_regions_complete"] = "pdf_repeated_regions_complete"
    page_count: int
    regions: list[PdfRepeatedRegionItem] = Field(default_factory=list)
    detector_version: str = "v1"


class PdfRepeatedRegionsStripCompleteData(DataPayload[Literal["pdf_repeated_regions_strip_complete"]]):
    """Terminal for strip-repeated-regions — the legacy
    ``StripRepeatedRegionsResult`` body, flattened (the nested report's
    ``page_count``/``detector_version`` are lifted to the top level)."""

    type: Literal["pdf_repeated_regions_strip_complete"] = "pdf_repeated_regions_strip_complete"
    page_count: int
    pages_text: list[str] = Field(default_factory=list)
    regions: list[PdfRepeatedRegionItem] = Field(default_factory=list)
    detector_version: str = "v1"
    stripped_region_ids: list[str] = Field(default_factory=list)


class PdfPipelineResultData(DataPayload[Literal["pdf_pipeline_result"]]):
    """Terminal result of the PDF AI / full-pipeline streams — the typed
    replacement for the raw ``PdfResult.model_dump()``. Per-page payloads and
    server-only fields (``storage_uri``, ``tables_path``) are NOT shipped;
    ``file_id`` addresses the persisted row."""

    type: Literal["pdf_pipeline_result"] = "pdf_pipeline_result"
    raw_text: str | None = None
    page_count: int = 0
    chunks: list[str] | None = None
    ai_processed: list[dict[str, Any]] | None = None
    cloud_uri: str | None = None
    file_id: str | None = None


class WorkflowNodeTestResultData(DataPayload[Literal["workflow_node_test_result"]]):
    """Terminal event for POST /workflows/{id}/nodes/{node_id}/test.

    Carries exactly what the old blocking TestNodeResponse JSON body carried,
    so the FE migration is "read one event"."""

    type: Literal["workflow_node_test_result"] = "workflow_node_test_result"
    success: bool
    duration_ms: int
    node_id: str
    spec_type: str
    output: dict[str, Any] | None = (
        None  # api-any-ok: typed per the node's output_schema, varies per node
    )
    error_type: str | None = None
    error_message: str | None = None

    @field_validator("error_message", mode="before")
    @classmethod
    def _client_safe_error_message(cls, value: Any) -> Any:
        if not isinstance(value, str):
            return value
        return client_error_text(value) or (
            "" if not value.strip() else "This step stopped with an internal error."
        )


class MandateTryResultData(DataPayload[Literal["mandate_try_result"]]):
    """Terminal event for POST /mandates/{key}/try (the job page's "Try it" door).

    The run is minutes of agent work at most, past the gateway's 60 s sever, so the
    door streams: the nested agent's own chunks/tool events flow live, and this one
    event carries exactly what the old blocking JSON body carried, so the client
    migration is "read one event". ``result`` is aidream's ``MandateTestResult``
    (services/mandates/testing.py), which this package cannot import; the client
    validates it with its own ``isMandateTestResult`` guard."""

    type: Literal["mandate_try_result"] = "mandate_try_result"
    mandate_key: str
    result: dict[str, Any]  # api-any-ok: aidream MandateTestResult, guarded client-side


class PlanGenStartedData(DataPayload[Literal["plan_gen_started"]]):
    """Content-plan generator kickoff: which site, which research angles, and
    how much keyword context (seo.site_keyword_value) the waves get to see."""

    type: Literal["plan_gen_started"] = "plan_gen_started"
    site_id: str
    domain: str
    angles: list[str] = Field(default_factory=list)
    keyword_count: int = 0


class PlanGenCandidateData(DataPayload[Literal["plan_gen_candidate"]]):
    """One research wave finished: its candidate tree size and rationale."""

    type: Literal["plan_gen_candidate"] = "plan_gen_candidate"
    angle: str
    node_count: int
    rationale: str = ""


class PlanGenMergedData(DataPayload[Literal["plan_gen_merged"]]):
    """The merger produced the final tree."""

    type: Literal["plan_gen_merged"] = "plan_gen_merged"
    node_count: int
    summary: str = ""
    candidates_used: int = 0


class PlanGenAppliedData(DataPayload[Literal["plan_gen_applied"]]):
    """Terminal: the tree was applied through the plan write path (or dry-run)."""

    type: Literal["plan_gen_applied"] = "plan_gen_applied"
    site_id: str
    created: int
    existing: int
    failed: int
    errors: list[str] = Field(default_factory=list)
    dry_run: bool = False


class PlanDeepenResultData(DataPayload[Literal["plan_deepen_result"]]):
    """Terminal event of POST /content-plan/nodes/{id}/deepen: the node's
    refreshed brief size and how many cited sources were attached."""

    type: Literal["plan_deepen_result"] = "plan_deepen_result"
    node_id: str
    route: str = ""
    brief_lines: int = 0
    sources_attached: int = 0


class PlanBriefDraftData(DataPayload[Literal["plan_brief_draft"]]):
    """Terminal event of POST /content-plan/nodes/{id}/draft-brief.

    The draft is ALREADY persisted on `plan.node.metadata.ai_brief_draft` when
    this event is emitted — the client re-reads the node rather than treating
    this payload as the only copy."""

    type: Literal["plan_brief_draft"] = "plan_brief_draft"
    node_id: str
    route: str = ""
    brief: list[str] = Field(default_factory=list)
    angle: str = ""
    must_not_cover: list[str] = Field(default_factory=list)
    concerns: list[str] = Field(default_factory=list)
    suggested_word_count: int | None = None
    #: True when the same request also promoted the draft onto `brief`.
    accepted: bool = False


class PlanPageStepResultData(DataPayload[Literal["plan_page_step_result"]]):
    """Terminal event of POST /content-plan/nodes/{id}/steps/{step} — ONE
    Website Factory pipeline step (family comparison / write / review) for ONE
    page.

    The artifact is ALREADY persisted on `plan.node_artifact` and the step
    stamped on `plan.node_step` when this fires — the client re-reads those
    tables rather than treating this payload as the only copy."""

    type: Literal["plan_page_step_result"] = "plan_page_step_result"
    node_id: str
    #: `p3_family` | `p4_write` | `p5_review`.
    step: str
    route: str = ""
    #: The `plan.node_artifact` row this step produced.
    artifact_id: str = ""
    #: The `chat.agent_run` row holding the complete request + result.
    run_id: str = ""
    summary: str = ""


class PlanSetupAgentResultData(DataPayload[Literal["plan_setup_agent_result"]]):
    """Terminal event of the three whole-plan content-plan Setup passes
    (keyword strategy, entity attachment, plan review).

    The COMPLETE proposal is already persisted on
    `web.site.settings.content_plan.*` and on the run's `chat.agent_run` row
    when this fires — the client re-reads the site rather than treating this
    payload as the only copy. This event carries just enough to say what
    happened and where to find it."""

    type: Literal["plan_setup_agent_result"] = "plan_setup_agent_result"
    site_id: str
    #: `chat.agent_run.kind` — e.g. "content_plan.keyword_strategy".
    kind: str
    #: The `chat.agent_run` row holding the complete request + result.
    run_id: str
    #: Assignments / attachments / findings, depending on `kind`.
    item_count: int = 0
    summary: str = ""
    model_id: str | None = None


class PlanCmsFillPreviewData(DataPayload[Literal["plan_cms_fill_preview"]]):
    """Terminal event of POST /content-plan/sites/{id}/cms-fill/preview: ONE
    authored page (html/css/meta) plus the site's real global CSS and
    header/footer so the client can compose a faithful preview."""

    type: Literal["plan_cms_fill_preview"] = "plan_cms_fill_preview"
    node_id: str
    page_id: str
    route: str = "/"
    title: str = ""
    html: str = ""
    css: str = ""
    meta_title: str = ""
    meta_description: str = ""
    model: str = ""
    wrote: bool = False
    # A PUBLISHED page is re-authored into its draft twins — the live page keeps
    # serving until someone publishes. `write_target` says where a write lands.
    is_published: bool = False
    write_target: Literal["live", "draft"] = "live"
    global_css: str = ""
    header_html: str = ""
    footer_html: str = ""


class CmsLogoFoundData(DataPayload[Literal["cms_logo_found"]]):
    """Terminal event of the CMS logo finder (POST
    /content-plan/sites/{id}/find-logo): what was stored, or an honest miss.

    ``found=False`` is a NORMAL outcome — ``message`` says what was tried and
    ``rejected`` lists every downloaded candidate and why it lost, so "no logo
    found" is never a shrug."""

    type: Literal["cms_logo_found"] = "cms_logo_found"
    site_id: str
    found: bool
    message: str
    asset_id: str | None = None
    asset_url: str | None = None
    #: og:image | twitter:image | apple-touch-icon | icon | msapplication-tile |
    #: image-search — where the winning candidate was declared.
    source: str | None = None
    source_url: str | None = None
    width: int | None = None
    height: int | None = None
    mime_type: str | None = None
    candidates_considered: int = 0
    rejected: list[str] = Field(default_factory=list)


class RagVerifyClaimsData(DataPayload[Literal["rag_verify_claims"]]):
    """POST /rag/verify pass-1 progress: the answer has been split into
    atomic claims; the judge will now settle them one by one."""

    type: Literal["rag_verify_claims"] = "rag_verify_claims"
    claims: list[str] = Field(default_factory=list)
    count: int
    judge_model: str


class RagVerifyVerdictData(DataPayload[Literal["rag_verify_verdict"]]):
    """POST /rag/verify per-claim progress: the streamed judge settled one
    claim. ``index`` is the 0-based position in the claims list. Provisional —
    the terminal ``rag_verify_result`` event is authoritative."""

    type: Literal["rag_verify_verdict"] = "rag_verify_verdict"
    index: int
    claim: str
    verdict: str  # supported | partial | unsupported
    confidence: float
    supporting_chunk_ids: list[str] = Field(default_factory=list)
    reasoning: str = ""


class RagVerifyClaimItem(BaseModel):
    """One settled claim inside the terminal rag_verify_result event."""

    claim: str
    verdict: str  # supported | partial | unsupported
    confidence: float
    supporting_chunk_ids: list[str] = Field(default_factory=list)
    reasoning: str = ""


class RagVerifyResultData(DataPayload[Literal["rag_verify_result"]]):
    """Terminal event for POST /rag/verify — carries exactly what the old
    blocking ``VerifyResponse`` JSON body carried, so the FE migration is
    "read one event"."""

    type: Literal["rag_verify_result"] = "rag_verify_result"
    claims: list[RagVerifyClaimItem] = Field(default_factory=list)
    overall_faithfulness: float
    judge_model: str
    latency_ms: int


class AssignmentProgressData(DataPayload[Literal["assignment_progress"]]):
    """Durable coordinated-assignment progress for API and workflow UIs."""

    type: Literal["assignment_progress"] = "assignment_progress"
    session_id: str
    completed: int = Field(ge=0)
    total: int = Field(ge=0)
    status: Literal[
        "pending",
        "running",
        "completed",
        "partially_failed",
        "failed",
        "cancelled",
    ]


# ---------------------------------------------------------------------------
# Proof runs — expensive, real-provider verification runs
# (aidream/services/proof_runs/FEATURE.md). The payload shapes carried here are
# the registered kinds ``proof_result`` / ``proof_attestation``; these events are
# the WIRE, so they stay flat and JSON-shaped rather than importing them.
# ---------------------------------------------------------------------------


class ProofRunStartedData(DataPayload[Literal["proof_run_started"]]):
    type: Literal["proof_run_started"] = "proof_run_started"
    run_id: str
    slug: str
    label: str = ""
    mode: Literal["live", "replay"]
    gate_reason: str = ""
    #: Anchors the run's receipts. Minted in-process immediately before the run,
    #: which is what makes it usable as the run's nonce.
    conversation_id: str | None = None


class ProofRunStepData(DataPayload[Literal["proof_run_step"]]):
    """Human-readable progress from inside a check while it works."""

    type: Literal["proof_run_step"] = "proof_run_step"
    run_id: str
    message: str
    step: int = 0


class ProofEvaluatedData(DataPayload[Literal["proof_evaluated"]]):
    """One proof, the moment it is decided."""

    type: Literal["proof_evaluated"] = "proof_evaluated"
    run_id: str
    proof_id: str
    title: str
    status: Literal["passed", "failed", "skipped"]
    required: bool = True
    detail: str = ""
    observed: dict[str, JsonValue] = Field(default_factory=dict)


class ProofRunCompletedData(DataPayload[Literal["proof_run_completed"]]):
    type: Literal["proof_run_completed"] = "proof_run_completed"
    run_id: str
    slug: str
    mode: Literal["live", "replay"]
    verdict: Literal["pass", "fail", "inconclusive"]
    strength: Literal["live_receipts", "replay_only"]
    summary: str = ""
    passed: int = 0
    failed: int = 0
    skipped: int = 0
    cost_usd: float = 0.0
    total_tokens: int = 0
    provider_calls: int = 0
    duration_ms: int = 0


class ProofRunSkippedData(DataPayload[Literal["proof_run_skipped"]]):
    """The gate refused to run. NEVER a pass — the reason is always named."""

    type: Literal["proof_run_skipped"] = "proof_run_skipped"
    slug: str
    reason: str
    month_to_date_usd: float = 0.0


# ---------------------------------------------------------------------------
# Media Source Catalog — the sync stream and the selection-job stream
# ---------------------------------------------------------------------------
#
# A Library of Sources (a YouTube channel cataloged, a podcast feed, a set of
# captured pages) streams its progress while it runs. Every sync event carries the
# same envelope — which Library, a monotonic `seq` so a client can order what it
# receives, and the wall-clock `at` — because a screen that renders a page out of
# order is worse than one that renders it late.
#
# `seq` is per-sync and starts at 1. A client that sees a gap has missed an event
# and must re-read the Library rather than guess.


class LibrarySyncEventBase(DataPayload[PayloadType], Generic[PayloadType]):
    """The envelope every `library.sync.*` event carries."""

    library_id: str
    seq: int
    at: str


class LibrarySyncStartedData(LibrarySyncEventBase[Literal["library.sync.started"]]):
    type: Literal["library.sync.started"] = "library.sync.started"
    #: `full` or `incremental` — how much of the provider this sync will walk.
    mode: str
    #: What the Library said it held BEFORE this sync. Never a promise about the
    #: result: a channel that published since is legitimately larger.
    expected_total: int | None = None


class LibrarySyncPageData(LibrarySyncEventBase[Literal["library.sync.page"]]):
    """One page of Sources, ON SCREEN before any of it has been written.

    The rows in `videos` are the full Source shape the list endpoint returns, so a
    client renders a page from this event alone and never waits for a database
    round trip it does not need.
    """

    type: Literal["library.sync.page"] = "library.sync.page"
    page_index: int
    page_size: int
    #: Sources listed across every page so far, including this one.
    cumulative: int
    next_page_token_present: bool
    videos: list[dict[str, JsonValue]] = Field(default_factory=list)


class LibrarySyncPersistedData(LibrarySyncEventBase[Literal["library.sync.persisted"]]):
    """A page's rows landed. `ids` maps provider id -> the platform row id."""

    type: Literal["library.sync.persisted"] = "library.sync.persisted"
    ids: dict[str, str] = Field(default_factory=dict)
    count: int


class LibrarySyncListedData(LibrarySyncEventBase[Literal["library.sync.listed"]]):
    """Listing is complete. Typing may still be running behind this."""

    type: Literal["library.sync.listed"] = "library.sync.listed"
    total_listed: int
    elapsed_ms: int
    #: How many Sources still have no decided media kind at this moment.
    deciding: int
    #: WHAT THE WALK THREW AWAY, by cause. A blog crawl reaches taxonomy pages,
    #: pagination, nav widgets and assets; cataloging them as posts is what made
    #: waitbutwhy.com report 346 "Posts" against its own post sitemap's 202. The
    #: narrowed crawl is only half the fix — the other half is saying so, because a
    #: count that quietly drops 23 pages is the same kind of claim as one that
    #: quietly adds them. Empty means nothing was discarded, never "we did not look".
    skipped_by_reason: dict[str, int] = Field(default_factory=dict)
    #: The M in "N posts, M other pages skipped".
    skipped_total: int = 0


class LibrarySyncClassifiedData(LibrarySyncEventBase[Literal["library.sync.classified"]]):
    """A batch of media-kind verdicts.

    `from_cache` is not decoration: a cached verdict cost nothing and a probed one
    cost a provider call, and a screen that says "checked just now" for a verdict
    restored from an earlier sync is lying about work that never happened.
    """

    type: Literal["library.sync.classified"] = "library.sync.classified"
    classifications: list[dict[str, JsonValue]] = Field(default_factory=list)
    from_cache: bool


class LibrarySyncCompletedData(LibrarySyncEventBase[Literal["library.sync.completed"]]):
    """The terminal success event.

    `listed_ms` and `elapsed_ms` are deliberately BOTH here: the first is when the
    channel appeared, the second is when every Source was typed, and collapsing
    them into one number hides the only tail a person ever notices.
    """

    type: Literal["library.sync.completed"] = "library.sync.completed"
    total_listed: int
    elapsed_ms: int
    listed_ms: int
    quota_units_spent: int
    metrics: dict[str, JsonValue] = Field(default_factory=dict)
    #: Sources this run RETIRED because a full re-listing no longer found them. The
    #: contract published this field from the start and nothing computed it, which is
    #: how a narrowed crawl could report 202 Posts over a table still holding 346 rows.
    removed_count: int = 0
    #: True when this run found a candidate retirement that would have removed at
    #: least half of what it JUST PERSISTED and refused to apply it, rather than
    #: retiring the catalog it had just written. `removed_count` stays 0 in that
    #: case — this is the only field that says "refused", not "nothing was gone".
    #: See `aidream.services.media_catalog.libraries._retirement_would_run_away`.
    retire_refused: bool = False
    #: WHAT THIS CATALOG LEFT OUT, and why — carried on the TERMINAL event too,
    #: not only on `library.sync.listed`, because this is the one a client keeps:
    #: the screen's "Up to date" banner is built from this event. A number that
    #: quietly drops pages is the same kind of claim as one that quietly adds them.
    skipped_by_reason: dict[str, int] = Field(default_factory=dict)
    #: The M in "N Sources listed, M other pages skipped".
    skipped_total: int = 0
    #: Why this channel Library could not be joined to its shared channel profile (the
    #: ``catalogs_channel`` edge), in a person's words; None when it is joined.
    channel_link_error: str | None = None


class LibrarySyncUnavailableData(LibrarySyncEventBase[Literal["library.sync.unavailable"]]):
    """The honest announced stop: a named cause, a remedy, and what still stands.

    This is what makes "the channel is empty" impossible to confuse with "we could
    not ask" — a missing key or an exhausted quota arrives as THIS, never as a
    successful sync that listed nothing.
    """

    type: Literal["library.sync.unavailable"] = "library.sync.unavailable"
    code: str
    message: str
    remedy: str | None = None
    #: Sources listed before the stop. They are saved and remain readable.
    partial_total: int = 0


class LibrarySyncFailedData(LibrarySyncEventBase[Literal["library.sync.failed"]]):
    type: Literal["library.sync.failed"] = "library.sync.failed"
    code: str
    message: str
    partial_total: int = 0
    retryable: bool = True


class MediaSelectionJobProgressData(DataPayload[Literal["job.progress"]]):
    """One run of one Action over a selection of Sources, as it drains.

    `totals` carries the item counts by status (total/queued/running/succeeded/
    failed/skipped/cancelled), which is the whole progress picture in one object —
    a client never has to add up events it might have missed.
    """

    type: Literal["job.progress"] = "job.progress"
    job_id: str
    at: str
    totals: dict[str, int] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Catch-all for unregistered data event types
# ---------------------------------------------------------------------------


class UntypedDataPayload(BaseModel):
    """Fallback for data events whose `type` isn't in DATA_TYPE_REGISTRY.

    extra="allow" so the TS generator emits [key: string]: unknown and any
    additional server-side fields pass through without validation errors.
    """

    model_config = {"extra": "allow"}
    type: str


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# Copy again — the Data tables switch's own door to the mover's rerun
# (aidream services/unified_data_campaign/copy_again.py, lane COPY-AGAIN-DOOR)
# ---------------------------------------------------------------------------


class CutoverCopyAgainProgressData(DataPayload[Literal["cutover_copy_again_progress"]]):
    """One table done while an organization's older tables are copied again."""

    type: Literal["cutover_copy_again_progress"] = "cutover_copy_again_progress"
    organization_id: str
    table_id: str | None = None
    table_name: str
    done: int
    total: int
    #: The table was refused and left exactly as it was; the door's words.
    refused: str | None = None
    says: str


class CutoverCopyAgainReportData(DataPayload[Literal["cutover_copy_again_report"]]):
    """What copying again did, with the one line a person reads."""

    type: Literal["cutover_copy_again_report"] = "cutover_copy_again_report"
    organization_id: str
    organization_name: str
    table_id: str | None = None
    table_name: str | None = None
    ok: bool
    tables: int
    tables_refused: list[str] = Field(default_factory=list)
    rows_written: int = 0
    carried: dict[str, int] = Field(default_factory=dict)
    named: list[str] = Field(default_factory=list)
    says: str



class CutoverFinalSwitchStageData(DataPayload[Literal["cutover_final_switch_stage"]]):
    """One stage of the final switch (lane FINAL-SWITCH): copying again, pressing, undoing."""

    type: Literal["cutover_final_switch_stage"] = "cutover_final_switch_stage"
    stage: str
    says: str


class CutoverFinalSwitchResultData(DataPayload[Literal["cutover_final_switch_result"]]):
    """What the final switch (or its undo) did, in the database's own sentence, with its counts."""

    type: Literal["cutover_final_switch_result"] = "cutover_final_switch_result"
    direction: Literal["new", "old"]
    ok: bool
    #: The database's refusal key when it refused (not_ready, not_a_platform_admin, confirm_not_carried…).
    reason: str | None = None
    says: str
    press_id: str | None = None
    counts: dict[str, Any] = Field(default_factory=dict)
    timings_ms: dict[str, int] = Field(default_factory=dict)
    #: The Copy again reports the press ran first, one sentence per organization.
    copied_again: list[str] = Field(default_factory=list)
    #: On an undo refused as confirm_not_carried: what would stay in the new system.
    not_carried: list[str] = Field(default_factory=list)


class CutoverFinalSwitchCopyAgainResultData(DataPayload[Literal["cutover_final_switch_copy_again_result"]]):
    """What a Copy again run before the final switch did (lane FINAL-SWITCH): resumable, per organization."""

    type: Literal["cutover_final_switch_copy_again_result"] = "cutover_final_switch_copy_again_result"
    run_id: str
    resumed: bool = False
    #: Green only when every organization copied without a refusal and nothing still needs copying.
    ok: bool
    says: str
    #: One entry per organization copied in this pass: organization_id, organization_name, ok, says, ms.
    organizations: list[dict[str, Any]] = Field(default_factory=list)
    still_needs: list[str] = Field(default_factory=list)
    timings_ms: dict[str, int] = Field(default_factory=dict)


# ---------------------------------------------------------------------------
# Media-list research (aidream crm/media_list_research.py, Brief 3)
# ---------------------------------------------------------------------------


class MediaResearchProfile(BaseModel):
    """One newly usable named journalist, as research finds them."""

    model_config = {"extra": "forbid"}

    name: str
    outlet: str | None = None
    #: The dated piece of theirs that surfaced them.
    url: str | None = None
    published_at: str | None = None


class MediaResearchAnchor(BaseModel):
    model_config = {"extra": "forbid"}

    title: str | None = None
    url: str
    published_at: str | None = None


class MediaResearchRow(BaseModel):
    """One journalist, judged. The table the person reads."""

    model_config = {"extra": "forbid"}

    party_id: str
    name: str
    outlet: str | None = None
    status: Literal["fit", "soft_fit", "research_needed", "cut"]
    rank: int = 0
    why_them: str = ""
    anchor: MediaResearchAnchor | None = None
    pitch_note: str | None = None
    #: wrong_beat | stale | duplicate | weak_evidence | unsafe_hook | filler (cuts only).
    cut_reason: str | None = None
    contact_state: Literal["verified", "quarantined", "unresolved"] = "unresolved"
    #: The address we hold for them — shown ONLY when verified, or when
    #: quarantined together with the reason it failed the identity check.
    contact_address: str | None = None
    contact_note: str | None = None
    first_wave: bool = False
    #: The journalist fit check's verdict for this angle, when it ran (first wave).
    fit_check: str | None = None
    #: True when this person is now a member of the list (deduplicated).
    on_list: bool = False


class MediaResearchSummaryData(BaseModel):
    model_config = {"extra": "forbid"}

    requested: int
    research_target: int
    multiplier: int
    multiplier_reason: str
    resolved: int = 0
    judged: int = 0
    first_wave: int = 0
    added_to_list: int = 0
    already_on_list: int = 0
    gaps: list[str] = Field(default_factory=list)


class MediaResearchProgressData(DataPayload[Literal["media_research_progress"]]):
    """A meaningful change in a media-list research run — never an identical poll."""

    type: Literal["media_research_progress"] = "media_research_progress"
    run_key: str
    stage: Literal["approved", "search", "resolve", "judge", "contacts", "first_wave", "save"]
    percent: int
    says: str
    found: int = 0
    target: int = 0
    judged: int = 0
    new_profiles: list[MediaResearchProfile] = Field(default_factory=list)
    #: Rows judged in this step (the table fills as batches return).
    rows: list[MediaResearchRow] = Field(default_factory=list)


class MediaResearchResultData(DataPayload[Literal["media_research_result"]]):
    """The run's answer: the outcome first, then the table, then the cuts."""

    type: Literal["media_research_result"] = "media_research_result"
    run_key: str
    list_id: str
    #: complete | partial (a stage failed or the pool fell short — labeled, never hidden)
    status: Literal["complete", "partial"]
    #: True when this campaign already ran: the stored answer, no second job.
    reused: bool = False
    says: str
    summary: MediaResearchSummaryData
    rows: list[MediaResearchRow] = Field(default_factory=list)
    cuts: list[MediaResearchRow] = Field(default_factory=list)
    problems: list[str] = Field(default_factory=list)
    next_action: str = ""


class AgentStudioBriefVariable(BaseModel):
    """One input the new agent takes, with the value THIS chat used."""

    name: str
    description: str = ""
    test_value: str = ""


class SocialStageEvent(DataPayload[Literal["social_stage"]]):
    """One stage of a Social Intelligence door (ingest post / profile, track, refresh) — fetching the
    profile, posts page n of m, storing media, transcript, scoring. ``current``/``total`` are 0 when
    the stage has no count."""

    type: Literal["social_stage"] = "social_stage"
    operation: Literal["ingest_post", "ingest_profile", "track", "refresh"]
    stage: str
    label: str
    current: int = 0
    total: int = 0


class SocialResultEvent(DataPayload[Literal["social_result"]]):
    """The final answer of a Social Intelligence door: exactly the body the blocking door used to
    return (``IngestPostResult`` / ``IngestProfileResult`` / ``TrackResult`` / refresh dict), kind-stamped
    where a kind exists."""

    type: Literal["social_result"] = "social_result"
    operation: Literal["ingest_post", "ingest_profile", "track", "refresh"]
    result: dict[str, JsonValue]


class AgentStudioFromChatProgressData(DataPayload[Literal["agent_studio_from_chat_progress"]]):
    """One step of "Make an agent from this chat" (Agent Studio)."""

    type: Literal["agent_studio_from_chat_progress"] = "agent_studio_from_chat_progress"
    step: Literal["reading", "briefing", "building", "proving"]
    says: str
    #: Set when the door started an Agent Factory build (AF-D door #4, knob
    #: ``agent_factory.door_from_chat`` = pipeline): the window follows that build.
    build_id: str | None = None
    #: With ``build_id``: the proof cases the build really starts with — the chat's own
    #: request (when it has an accepted answer) plus every example that maps onto the
    #: agent's inputs (R55). The window's "N of 3" shows this, never its own guess.
    proof_cases: int | None = None
    #: The stored run this step just finished (its conversation: every message the model
    #: saw and wrote, tool calls, cost), so the window can open exactly what happened.
    run_conversation_id: str | None = None
    #: Agent Studio ``stage="inputs"``: the build brief the chat brief job wrote (name, goals,
    #: variables with the values the person gave across the chat), for the person to confirm
    #: before the build. Sent on the last ``briefing`` event; the stream then ends.
    brief: dict[str, Any] | None = None
    #: Agent Studio ``stage="scope"`` (lane 5B): the scope step's proposal — ``options`` (general to
    #: specific, each ``name`` + ``line``), ``inputs`` (``name``, ``label``, ``example``) and
    #: ``do_not_bake`` (this chat's facts). Sent on the last ``briefing`` event; the stream then ends.
    scope: dict[str, Any] | None = None


class AgentStudioFromChatResultData(DataPayload[Literal["agent_studio_from_chat_result"]]):
    """The new agent, its brief, and the first-try proof beside the accepted result.

    The proof is a SAME-INPUT replay: the new agent runs on this chat's own
    inputs (``variables[*].test_value``) and its answer is shown next to the
    answer the person accepted. The builder never saw that answer. Nothing
    here is a verdict — the person compares."""

    type: Literal["agent_studio_from_chat_result"] = "agent_studio_from_chat_result"
    conversation_id: str
    agent_id: str
    version_id: str
    agent_name: str
    summary: str = ""
    deliverable: str = ""
    goals: list[str] = Field(default_factory=list)
    variables: list[AgentStudioBriefVariable] = Field(default_factory=list)
    #: "single_agent" | "masterwork" — the brief's read of how big the job is.
    fit: str = "single_agent"
    fit_reason: str = ""
    #: The numbered assistant turns that hold the accepted result (empty = no text result).
    accepted_turns: list[int] = Field(default_factory=list)
    accepted_result: str | None = None
    proof_output: str | None = None
    #: Why the proof run produced no answer, in a sentence; None when it did.
    proof_error: str | None = None
    #: Every stored run behind this agent, so the person can open (and keep talking to)
    #: exactly what wrote it: the brief writer, the Agent Builder, the first try.
    brief_conversation_id: str | None = None
    builder_conversation_id: str | None = None
    proof_conversation_id: str | None = None
    says: str


# ---------------------------------------------------------------------------
# Decision reference runs — aidream/services/decision_review/FEATURE.md
# ---------------------------------------------------------------------------


class DecisionReferenceModel(BaseModel):
    """The model that gives a reference run's answers."""

    model_config = {"extra": "forbid"}
    id: str
    name: str


class DecisionReferenceRunStartedData(DataPayload[Literal["decision_reference_run_started"]]):
    """A reference run began: what it will check and which model answers."""

    type: Literal["decision_reference_run_started"] = "decision_reference_run_started"
    run_id: str
    agent_id: str
    item_count: int
    #: Chosen answers left out because this reference model already checked them.
    skipped_existing: int = 0
    #: Chosen answers left out because another live run is checking them.
    in_flight: int = 0
    #: Chosen answers whose judged input cannot be rebuilt (each closes as an
    #: ``decision_reference_item_failed`` with ``status="unbuildable"``; not in item_count).
    unbuildable: int = 0
    reference_model: DecisionReferenceModel
    judge_key: str


class DecisionReferenceItemData(DataPayload[Literal["decision_reference_item"]]):
    """One decision answer checked: the reference model's answer beside the agent's."""

    type: Literal["decision_reference_item"] = "decision_reference_item"
    run_id: str
    item_id: str
    question: str
    reference_id: str | None = None
    #: The reference model's own answer (noul → bool, choice → key, score → weighted level).
    reference_answer: bool | float | str
    #: The reference verdict in the item's label vocabulary.
    reference_verdict: str
    #: The reference model's probability of its own verdict.
    reference_p: float | None = None
    #: noul only: the reference's P(true).
    reference_probability: float | None = None
    #: choice/score: the reference's full distribution (key → probability).
    reference_probabilities: dict[str, float] | None = None
    #: score only: the reference's level key → what that level means.
    reference_legend: dict[str, str] | None = None
    item_verdict: str
    #: The decision model's numbers for the same answer, so a live row reads like a reloaded one.
    item_p_answer: float | None = None
    item_probability: float | None = None
    item_probabilities: dict[str, float] | None = None
    item_confidence: float | None = None
    agree: bool
    #: True when this run's answer was NOT stored because a row already stood (the
    #: fields above are then that STORED row's, never the discarded answer).
    already_checked: bool = False
    #: The model that actually answered (a reroute names its fallback).
    model: str | None = None
    cost_usd: float
    latency_ms: int


class DecisionReferenceItemFailedData(DataPayload[Literal["decision_reference_item_failed"]]):
    """One decision answer the run could not check, with why."""

    type: Literal["decision_reference_item_failed"] = "decision_reference_item_failed"
    run_id: str
    item_id: str
    question: str
    error: str
    #: failed — the call or the save failed (stored, re-runnable) · unanswerable — the
    #: reference said it cannot answer (stored, its own bucket in agreement) ·
    #: unbuildable — the judged input cannot be rebuilt (stored as failed) · in_flight —
    #: another live run is checking it (nothing stored by this run).
    status: Literal["failed", "unanswerable", "unbuildable", "in_flight"] = "failed"
    #: The stored reference row that says so, when there is one.
    reference_id: str | None = None
    #: True when the reason is a row that already stood, not this run's own outcome.
    already_checked: bool = False


class DecisionReferenceRunDoneData(DataPayload[Literal["decision_reference_run_done"]]):
    """The run's end: how many were checked, how many agreed, what it cost."""

    type: Literal["decision_reference_run_done"] = "decision_reference_run_done"
    run_id: str
    done: int
    failed: int
    #: The reference said it could not answer: neither agree nor disagree.
    unanswerable: int = 0
    #: Left to another live run.
    in_flight: int = 0
    #: agreed / done (unanswerable excluded); None when nothing was checked.
    agreement_rate: float | None = None
    cost_usd: float


# ── Knowledge buckets dry run (aidream/services/knowledge_buckets, PLAN §6 phase 1) ──────────


class KnowledgeBucketsProgressData(DataPayload[Literal["knowledge_buckets_progress"]]):
    """One step of a knowledge-buckets dry run moved: what it is doing and how far it is."""

    type: Literal["knowledge_buckets_progress"] = "knowledge_buckets_progress"
    stage: Literal["inventory", "homes", "material", "scopes", "spread"]
    detail: str
    organization_id: str | None = None
    done: int = 0
    total: int = 0


class KnowledgeBucketsOrgCounts(BaseModel):
    """One organization's inventory, counted per kind of item."""

    model_config = {"extra": "forbid"}
    organization_id: str
    counts: dict[str, int]


class KnowledgeBucketsInventoryData(DataPayload[Literal["knowledge_buckets_inventory"]]):
    """The person's inventory read through the search index, with its count check."""

    type: Literal["knowledge_buckets_inventory"] = "knowledge_buckets_inventory"
    subject_user_id: str
    #: platform.count_items for the same filters, per kind (every kind, mapped or not).
    direct_counts: dict[str, int]
    #: What the inventory actually paged, per mapped kind.
    gathered_counts: dict[str, int]
    #: True when every mapped kind's gathered count equals its direct count.
    counts_match: bool
    #: kind -> [gathered, direct] for every kind that differs.
    mismatches: dict[str, list[int]] = {}
    #: Kinds the person has that the inventory map does not name (reported, never dropped silently).
    unmapped: dict[str, int] = {}
    #: Kinds the map excludes on purpose (web pages, others' items, templates).
    excluded: dict[str, int] = {}
    per_org: list[KnowledgeBucketsOrgCounts] = []


class KnowledgeBucketCandidateScope(BaseModel):
    """The person's existing scope or scope type a candidate's name matches."""

    model_config = {"extra": "forbid"}
    kind: Literal["scope", "scope_type"]
    id: str
    name: str


class KnowledgeBucketCandidate(BaseModel):
    """One scored candidate topic."""

    model_config = {"extra": "forbid"}
    key: str
    name: str
    origin: list[str]
    homes: int
    by_group: dict[str, int]
    weeks: int
    #: The ranking score (an obvious topic counts only places outside its project / topic).
    score: float
    #: The same formula over every place.
    score_all: float
    entity_share: float
    obvious: bool
    own_homes: list[str] = []
    outside: int
    entity_kinds: dict[str, int] = {}
    existing_scope: KnowledgeBucketCandidateScope | None = None


class KnowledgeBucketsOrgSpreadData(DataPayload[Literal["knowledge_buckets_org_spread"]]):
    """One organization's spread: what was scored and its best candidates."""

    type: Literal["knowledge_buckets_org_spread"] = "knowledge_buckets_org_spread"
    organization_id: str
    homes: int
    items_scored: int
    items_with_text: int
    items_with_entities: int
    #: Conversations left out because a platform automation started them.
    automation_skipped: int = 0
    #: Files left out because the person did not upload them (variants, renders).
    derived_files_skipped: int = 0
    #: Every item left out because the person did not author or bring it: kind → reason → count.
    excluded: dict[str, dict[str, int]] = Field(default_factory=dict)
    candidates: int
    scope_types: int
    scopes: int
    #: How many of ``top`` match an existing scope or scope type.
    top_matching_scopes: int
    top: list[KnowledgeBucketCandidate]


class KnowledgeBucketsDryRunDoneData(DataPayload[Literal["knowledge_buckets_dry_run_done"]]):
    """A knowledge-buckets dry run finished. Nothing was written."""

    type: Literal["knowledge_buckets_dry_run_done"] = "knowledge_buckets_dry_run_done"
    subject_user_id: str
    organizations: int
    items: int
    seconds: float


class KnowledgeBucketsFollowUpProgressData(DataPayload[Literal["knowledge_buckets_follow_up_progress"]]):
    """A split or merge of the person's buckets moved (PLAN §11): what it is doing and how far it is."""

    type: Literal["knowledge_buckets_follow_up_progress"] = "knowledge_buckets_follow_up_progress"
    kind: Literal["split", "merge"]
    stage: Literal["read", "entities", "search", "agent", "write"]
    detail: str
    done: int = 0
    total: int = 0


class KnowledgeBucketsFollowUpDoneData(DataPayload[Literal["knowledge_buckets_follow_up_done"]]):
    """A split or merge finished. ``ids`` are the bucket rows (``platform.assists`` ids) it made or found:
    a split's children, or a merge's one combined bucket."""

    type: Literal["knowledge_buckets_follow_up_done"] = "knowledge_buckets_follow_up_done"
    kind: Literal["split", "merge"]
    #: ``made`` (new rows) · ``existing`` (made before; nothing ran) · ``none`` (the agent found nothing honest).
    outcome: Literal["made", "existing", "none"]
    ids: list[str] = []
    #: One plain sentence when ``outcome`` is ``none``, or what was dropped from the agent's answer.
    why: str = ""


class VaultPasswordHealthScanReferenceData(DataPayload[Literal["vault_password_health_scan_reference"]]):
    """Opaque scan handles; findings never enter the replay journal."""

    model_config = {"extra": "forbid", "populate_by_name": True, "serialize_by_alias": True}
    type: Literal["vault_password_health_scan_reference"] = "vault_password_health_scan_reference"
    marker: _NoKindMarker = _no_kind_marker()
    request_id: str = Field(min_length=1)
    execution_id: str = Field(min_length=1)
    resumed_from_execution_id: str | None = None
    status_path: str
    events_path: str
    rejoin_path: str
    result_path: str
    resume_path: str


class VaultPasswordHealthDiscoveryReference(BaseModel):
    model_config = {"extra": "forbid", "populate_by_name": True, "serialize_by_alias": True}
    marker: _NoKindMarker = _no_kind_marker()
    request_id: str = Field(min_length=1)
    execution_id: str = Field(min_length=1)


class VaultPasswordHealthDiscoveryPageData(DataPayload[Literal["vault_password_health_discovery_page"]]):
    """Authorized scan handles and opaque pagination, never findings."""
    model_config = {"extra": "forbid", "populate_by_name": True, "serialize_by_alias": True}
    type: Literal["vault_password_health_discovery_page"] = "vault_password_health_discovery_page"
    marker: _NoKindMarker = _no_kind_marker()
    references: list[VaultPasswordHealthDiscoveryReference]
    continuation: str | None = None


class VaultPasswordHealthProgressData(DataPayload[Literal["vault_password_health_progress"]]):
    """Count-only progress, safe to persist in stream replay."""

    model_config = {"extra": "forbid", "populate_by_name": True, "serialize_by_alias": True}
    type: Literal["vault_password_health_progress"] = "vault_password_health_progress"
    marker: _NoKindMarker = _no_kind_marker()
    request_id: str = Field(min_length=1)
    execution_id: str = Field(min_length=1)
    checked: int = Field(ge=0, strict=True)
    skipped: int = Field(ge=0, strict=True)


DATA_TYPE_REGISTRY: dict[str, type[DataPayload]] = {
    "vault_password_health_discovery_page": VaultPasswordHealthDiscoveryPageData,
    "vault_password_health_scan_reference": VaultPasswordHealthScanReferenceData,
    "vault_password_health_progress": VaultPasswordHealthProgressData,
    "knowledge_buckets_follow_up_progress": KnowledgeBucketsFollowUpProgressData,
    "knowledge_buckets_follow_up_done": KnowledgeBucketsFollowUpDoneData,
    "knowledge_buckets_progress": KnowledgeBucketsProgressData,
    "knowledge_buckets_inventory": KnowledgeBucketsInventoryData,
    "knowledge_buckets_org_spread": KnowledgeBucketsOrgSpreadData,
    "knowledge_buckets_dry_run_done": KnowledgeBucketsDryRunDoneData,
    "assignment_progress": AssignmentProgressData,
    "claude_managed_sdk_message": ClaudeManagedSdkMessageData,
    "claude_managed_warning": ClaudeManagedWarningData,
    "conversation_id": ConversationIdData,
    "audio_output": AudioOutputData,
    "image_output": ImageOutputData,
    "video_output": VideoOutputData,
    "partial_image": PartialImageData,
    "audio_stream_chunk": AudioStreamChunkData,
    "audio_stream_end": AudioStreamEndData,
    "media_block": MediaBlockData,
    "decision_answers": DecisionAnswersData,
    "decision_reference_run_started": DecisionReferenceRunStartedData,
    "decision_reference_item": DecisionReferenceItemData,
    "decision_reference_item_failed": DecisionReferenceItemFailedData,
    "decision_reference_run_done": DecisionReferenceRunDoneData,
    "conversation_labeled": ConversationLabeledData,
    "mandate_input_required": MandateInputRequiredData,
    "mandate_run": MandateRunData,
    "structured_input_warning": StructuredInputWarningData,
    "media_notice": MediaNoticeData,
    "categorization_result": CategorizationResultData,
    "file_analysis_started": FileAnalysisStartedData,
    "file_detector_completed": FileDetectorCompletedData,
    "file_analysis_complete": FileAnalysisCompleteData,
    "extraction_index_progress": ExtractionIndexProgressData,
    "extraction_index_complete": ExtractionIndexCompleteData,
    "podcast_stage": PodcastStageEvent,
    "podcast_complete": PodcastCompleteEvent,
    "podcast_run": PodcastRunEvent,
    "podcast_stage_started": PodcastStageStartedEvent,
    "podcast_tick": PodcastTickEvent,
    "podcast_metadata": PodcastMetadataEvent,
    "podcast_asset": PodcastAssetEvent,
    "podcast_official_video": PodcastOfficialVideoEvent,
    "podcast_asset_gen_started": PodcastAssetGenStartedEvent,
    "podcast_asset_result": PodcastAssetResultEvent,
    "workflow_step": WorkflowStepData,
    "function_result": FunctionResultData,
    "display_questionnaire": QuestionnaireDisplayData,
    "scrape_batch_complete": ScrapeBatchCompleteData,
    "youtube_transcript_source": YouTubeTranscriptSourceData,
    "fetch_results": FetchResultsData,
    "search_results": SearchResultsData,
    "search_error": SearchErrorData,
    "context_changed": ContextChangedData,
    "context_delta": ContextDeltaData,
    "context_persisted": ContextPersistedData,
    # Was emitted by the writeback dispatcher but never registered — clients
    # received it untyped. Registered 2026-07-07 alongside context_delta.
    "context_conflict": ContextConflictData,
    "context_persist_failed": ContextPersistFailedData,
    "context_receipt": ContextReceiptData,
    "first_turn_filled": FirstTurnFilledData,
    "memory_context_injected": MemoryContextInjectedData,
    "memory_observer_completed": MemoryObserverCompletedData,
    "memory_reflector_completed": MemoryReflectorCompletedData,
    "memory_buffer_spawned": MemoryBufferSpawnedData,
    "memory_error": MemoryErrorData,
    "legal_sync_event": LegalSyncEventData,
    "file_search_started": FileSearchStartedData,
    "file_search_page": FileSearchPageData,
    "file_search_complete": FileSearchCompleteData,
    "image_op_stage": ImageOpStageData,
    "image_document_detected": ImageDocumentDetectedData,
    "image_edit_complete": ImageEditCompleteData,
    "image_generate_complete": ImageGenerateCompleteData,
    "image_studio_variant": ImageStudioVariantData,
    "image_studio_process_complete": ImageStudioProcessCompleteData,
    "image_studio_commit_item": ImageStudioCommitItemData,
    "image_studio_commit_complete": ImageStudioCommitCompleteData,
    "dictionary_publish_complete": DictionaryPublishCompleteData,
    "masterwork_run": MasterworkRunData,
    "masterwork_run_snapshot": MasterworkRunSnapshotData,
    "masterwork_run_failed": MasterworkRunFailedData,
    "masterwork_run_cancelled": MasterworkRunCancelledData,
    "masterwork_build_progress": MasterworkBuildProgressData,
    "agent_test_run_started": AgentTestRunStartedEvent,
    "agent_test_result": AgentTestResultEvent,
    "agent_test_progress": AgentTestProgressEvent,
    "agent_test_run_status": AgentTestRunStatusEvent,
    "masterwork_agent_build": MasterworkAgentBuildData,
    "masterwork_build_complete": MasterworkBuildCompleteData,
    "masterwork_ingest_progress": MasterworkIngestProgressData,
    "masterwork_sealed_case_disclosure": MasterworkSealedCaseDisclosureData,
    "masterwork_ingest_complete": MasterworkIngestCompleteData,
    "masterwork_shortlist": MasterworkShortlistData,
    "masterwork_triads_ready": MasterworkTriadsReadyData,
    "masterwork_sort_cases_ready": MasterworkSortCasesReadyData,
    "masterwork_probe_round": MasterworkProbeRoundData,
    "masterwork_teach_back_round": MasterworkTeachBackRoundData,
    "masterwork_triage_progress": MasterworkTriageProgressData,
    "masterwork_triage_complete": MasterworkTriageCompleteData,
    "masterwork_dump_progress": MasterworkDumpProgressData,
    "masterwork_dump_complete": MasterworkDumpCompleteData,
    "masterwork_audition_progress": MasterworkAuditionProgressData,
    "masterwork_audition_verdict": MasterworkAuditionVerdictData,
    "masterwork_audition_outcome_verdict": MasterworkAuditionOutcomeVerdictData,
    "masterwork_pairwise_verdict": MasterworkPairwiseVerdictData,
    "masterwork_corpus_progress": MasterworkCorpusProgressData,
    "masterwork_corpus_cleaned": MasterworkCorpusCleanedData,
    "masterwork_bench_progress": MasterworkBenchProgressData,
    "masterwork_bench_arm": MasterworkBenchArmData,
    "masterwork_bench_verdict": MasterworkBenchVerdictData,
    "masterwork_checkup_progress": MasterworkCheckupProgressData,
    "masterwork_checkup_finding": MasterworkCheckupFindingData,
    "masterwork_checkup_complete": MasterworkCheckupCompleteData,
    "pdf_extract_started": PdfExtractStartedData,
    "pdf_page_extracted": PdfPageExtractedData,
    "pdf_extract_complete": PdfExtractCompleteData,
    "pdf_clean_started": PdfCleanStartedData,
    "pdf_tables_started": PdfTablesStartedData,
    "pdf_tables_page": PdfTablesPageData,
    "pdf_table_extracted": PdfTableExtractedData,
    "pdf_tables_complete": PdfTablesCompleteData,
    "pdf_page_classified": PdfPageClassifiedData,
    "pdf_classify_complete": PdfClassifyCompleteData,
    "pdf_reading_order_page": PdfReadingOrderPageData,
    "pdf_reading_order_complete": PdfReadingOrderCompleteData,
    "pdf_repeated_regions_progress": PdfRepeatedRegionsProgressData,
    "pdf_repeated_regions_complete": PdfRepeatedRegionsCompleteData,
    "pdf_repeated_regions_strip_complete": PdfRepeatedRegionsStripCompleteData,
    "pdf_pipeline_result": PdfPipelineResultData,
    "workflow_node_test_result": WorkflowNodeTestResultData,
    "mandate_try_result": MandateTryResultData,
    "rag_verify_claims": RagVerifyClaimsData,
    "rag_verify_verdict": RagVerifyVerdictData,
    "rag_verify_result": RagVerifyResultData,
    "plan_gen_started": PlanGenStartedData,
    "plan_gen_candidate": PlanGenCandidateData,
    "plan_gen_merged": PlanGenMergedData,
    "plan_gen_applied": PlanGenAppliedData,
    "plan_brief_draft": PlanBriefDraftData,
    "plan_deepen_result": PlanDeepenResultData,
    "plan_cms_fill_preview": PlanCmsFillPreviewData,
    "cms_logo_found": CmsLogoFoundData,
    "plan_setup_agent_result": PlanSetupAgentResultData,
    "plan_page_step_result": PlanPageStepResultData,
    "proof_run_started": ProofRunStartedData,
    "proof_run_step": ProofRunStepData,
    "proof_evaluated": ProofEvaluatedData,
    "proof_run_completed": ProofRunCompletedData,
    "proof_run_skipped": ProofRunSkippedData,
    # Media Source Catalog
    "library.sync.started": LibrarySyncStartedData,
    "library.sync.page": LibrarySyncPageData,
    "library.sync.persisted": LibrarySyncPersistedData,
    "library.sync.listed": LibrarySyncListedData,
    "library.sync.classified": LibrarySyncClassifiedData,
    "library.sync.completed": LibrarySyncCompletedData,
    "library.sync.unavailable": LibrarySyncUnavailableData,
    "library.sync.failed": LibrarySyncFailedData,
    "job.progress": MediaSelectionJobProgressData,
    "cutover_copy_again_progress": CutoverCopyAgainProgressData,
    "cutover_copy_again_report": CutoverCopyAgainReportData,
    "cutover_final_switch_stage": CutoverFinalSwitchStageData,
    "cutover_final_switch_result": CutoverFinalSwitchResultData,
    "cutover_final_switch_copy_again_result": CutoverFinalSwitchCopyAgainResultData,
    "media_research_progress": MediaResearchProgressData,
    "media_research_result": MediaResearchResultData,
    "agent_studio_from_chat_progress": AgentStudioFromChatProgressData,
    "social_stage": SocialStageEvent,
    "social_result": SocialResultEvent,
    "agent_studio_from_chat_result": AgentStudioFromChatResultData,
}


class BrandOfferingsQuoteData(DataPayload[Literal["brand_offerings_quote"]]):
    """What a brand's products-and-services Refresh will cost, sent BEFORE anything runs. ``points`` is 0 while
    every source it would read is free; a paid source that would run is named in ``paid_sources`` with its points,
    and the run waits for ``confirm_points`` at least ``points``."""

    type: Literal["brand_offerings_quote"] = "brand_offerings_quote"
    brand_id: str
    points: int = 0
    paid_sources: list[dict[str, Any]] = []
    free_steps: list[str] = []
    needs_confirmation: bool = False


class BrandOfferingsRefreshedData(DataPayload[Literal["brand_offerings_refreshed"]]):
    """A brand's products-and-services Refresh finished its first pass: counts, the coverage verdict, and the
    targeted crawl of missing pages it started (its durable follow-up run, when one was queued)."""

    type: Literal["brand_offerings_refreshed"] = "brand_offerings_refreshed"
    brand_id: str
    snapshot_id: str | None = None
    candidates: int = 0
    products: int = 0
    services: int = 0
    certainty: dict[str, int] = {}
    verdict: str | None = None
    verdict_line: str | None = None
    staged: dict[str, int] = {}
    gap_pages: int = 0
    gap_session_ids: list[str] = []
    gap_errors: list[str] = []
    follow_up_run_id: str | None = None
    points: int = 0
