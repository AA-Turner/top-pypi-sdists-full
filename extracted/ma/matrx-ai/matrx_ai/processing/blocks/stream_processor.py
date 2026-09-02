"""
StreamBlockProcessor — stateful processor between LLM token stream and NDJSON output.

Accumulates tokens, detects block boundaries, runs per-block parsers,
and emits RenderBlockEvent objects for streaming to the client.

Usage:
    processor = StreamBlockProcessor()
    for token in llm_stream:
        events = processor.process_token(token)
        for event in events:
            yield json.dumps(event.to_stream_event()) + "\n"
    # When stream ends:
    for event in processor.finalize():
        yield json.dumps(event.to_stream_event()) + "\n"
"""

from __future__ import annotations

import json
from collections.abc import Callable
from typing import Any

from matrx_graph.content_ir.envelope import KIND_KEY
from matrx_graph.content_ir.partial import (
    IR_PARTIAL_KEY,
    PartialKindTracker,
    close_partial_json,
    partial_kind_event,
    retracted_event,
    superseded_event,
)
from matrx_utils import vcprint

from matrx_ai.processing.blocks.block_detector import (
    ATTRIBUTE_XML_BLOCKS,
    CODE_LANGUAGE_ALIASES,
    JSON_BLOCK_PATTERNS,
    SPECIAL_CODE_LANGUAGES,
    XML_TAG_BLOCKS,
    DetectedBlock,
    detect_json_block_type,
    root_kind_declaration,
    split_content_into_blocks,
)
from matrx_ai.processing.blocks.envelope import (
    BLOCK_KIND_MAP,
    IR_ENVELOPE_KEY,
    adapt_block_data,
    discriminator_for_block,
    envelope_for_block,
)
from matrx_ai.processing.blocks.models.base import (
    BlockStatus,
    BlockType,
    RenderBlockEvent,
    RenderBlockState,
)
from matrx_ai.processing.blocks.parsers.timeline_stream_parser import TimelineStreamParser
from matrx_ai.processing.blocks.tag_detection_buffer import TagDetectionBuffer

# ---------------------------------------------------------------------------
# Parser dispatch — maps block type keys to parser functions
# ---------------------------------------------------------------------------

def _build_parser_map() -> dict[str, Callable[[str], Any]]:
    """Lazily build the parser dispatch map."""
    from matrx_ai.processing.blocks.parsers.artifact_parser import parse_artifact
    from matrx_ai.processing.blocks.parsers.comparison_parser import parse_comparison
    from matrx_ai.processing.blocks.parsers.decision_parser import parse_decision
    from matrx_ai.processing.blocks.parsers.decision_tree_parser import parse_decision_tree
    from matrx_ai.processing.blocks.parsers.diagram_parser import parse_diagram
    from matrx_ai.processing.blocks.parsers.flashcard_parser import parse_flashcards
    from matrx_ai.processing.blocks.parsers.item_presentation_parser import (
        parse_item_presentation,
    )
    from matrx_ai.processing.blocks.parsers.math_problem_parser import parse_math_problem
    from matrx_ai.processing.blocks.parsers.mermaid_parser import parse_mermaid
    from matrx_ai.processing.blocks.parsers.presentation_parser import parse_presentation
    from matrx_ai.processing.blocks.parsers.progress_parser import parse_progress
    from matrx_ai.processing.blocks.parsers.questionnaire_parser import parse_questionnaire
    from matrx_ai.processing.blocks.parsers.quiz_parser import parse_quiz
    from matrx_ai.processing.blocks.parsers.recipe_parser import parse_recipe
    from matrx_ai.processing.blocks.parsers.research_parser import parse_research
    from matrx_ai.processing.blocks.parsers.resources_parser import parse_resources
    from matrx_ai.processing.blocks.parsers.schema_proposal_parser import (
        parse_schema_proposal,
    )
    from matrx_ai.processing.blocks.parsers.structured_info_parser import parse_structured_info
    from matrx_ai.processing.blocks.parsers.table_parser import parse_table
    from matrx_ai.processing.blocks.parsers.task_parser import parse_tasks
    from matrx_ai.processing.blocks.parsers.timeline_parser import parse_timeline
    from matrx_ai.processing.blocks.parsers.transcript_parser import parse_transcript
    from matrx_ai.processing.blocks.parsers.troubleshooting_parser import parse_troubleshooting

    def _parse_artifact_with_metadata(c: str, metadata: dict | None = None, **_kw: Any) -> Any:
        """
        Parse an artifact block, using pre-extracted metadata from the detector.
        """
        return _model_to_dict(parse_artifact(c, metadata))

    def _parse_decision_with_metadata(c: str, metadata: dict | None = None, **_kw: Any) -> Any:
        """
        Parse a decision block, preferring pre-extracted metadata when available.

        The detector already parses option structure during extraction and stores
        it in metadata["decision"]. When that pre-parsed dict is present we
        reconstruct a DecisionBlockData directly from it — no need to re-parse
        the XML. If metadata is absent (e.g. called standalone) we fall back to
        parsing `c` as inner XML content with an empty attributes dict.
        """
        from matrx_ai.processing.blocks.models.decision import DecisionBlockData, DecisionOption

        if metadata:
            pre_parsed = metadata.get("decision")
            if pre_parsed and isinstance(pre_parsed, dict):
                try:
                    return _model_to_dict(
                        DecisionBlockData(
                            id=pre_parsed.get("id", "decision-0"),
                            prompt=pre_parsed.get("prompt", "Make a selection"),
                            options=[
                                DecisionOption(
                                    id=opt.get("id", f"opt-{i}"),
                                    label=opt.get("label", ""),
                                    text=opt.get("text", ""),
                                )
                                for i, opt in enumerate(pre_parsed.get("options", []))
                            ],
                        )
                    )
                except Exception:
                    pass
            attrs = metadata.get("attributes", {})
        else:
            attrs = {}

        return _model_to_dict(parse_decision(c, attrs))

    def _parse_json_object(c: str) -> dict[str, Any]:
        value = json.loads(c)
        if not isinstance(value, dict):
            raise ValueError("JSON block must contain an object")
        return value

    return {
        # PARTIAL_UPDATE parsers accept is_final and MUST receive it — a
        # `lambda c:` wrapper silently swallows the kwarg via _run_parser's
        # TypeError fallback, so the parser never learns the block completed
        # and withholds the last in-progress item forever (found via the
        # per-family envelope fixtures: the final flashcard's back stayed None).
        "flashcards": lambda c, *, is_final=False: _model_to_dict(
            parse_flashcards(c, is_final=is_final)
        ),
        "transcript": lambda c, *, is_final=False: _model_to_dict(
            parse_transcript(c, is_final=is_final)
        ),
        "tasks": lambda c, *, is_final=False: _model_to_dict(parse_tasks(c, is_final=is_final)),
        "quiz": lambda c: _model_to_dict(parse_quiz(c)),
        "presentation": lambda c: _model_to_dict(parse_presentation(c)),
        "math_problem": lambda c: _model_to_dict(parse_math_problem(c)),
        "item_presentation": lambda c: _model_to_dict(parse_item_presentation(c)),
        "schema_proposal": lambda c: _model_to_dict(parse_schema_proposal(c)),
        "cooking_recipe": lambda c, *, is_final=False: _model_to_dict(
            parse_recipe(c, is_final=is_final)
        ),
        "timeline": lambda c: _model_to_dict(parse_timeline(c)),
        "research": lambda c: _model_to_dict(parse_research(c)),
        "resources": lambda c: _model_to_dict(parse_resources(c)),
        "progress_tracker": lambda c: _model_to_dict(parse_progress(c)),
        "comparison_table": lambda c: _model_to_dict(parse_comparison(c)),
        "troubleshooting": lambda c: _model_to_dict(parse_troubleshooting(c)),
        "decision_tree": lambda c: _model_to_dict(parse_decision_tree(c)),
        "diagram": lambda c: _model_to_dict(parse_diagram(c)),
        "mermaid": lambda c: _model_to_dict(parse_mermaid(c)),
        "table": lambda c, *, is_final=False: _model_to_dict(parse_table(c, is_final=is_final)),
        "questionnaire": lambda c, *, is_final=False: _model_to_dict(
            parse_questionnaire(c, is_final=is_final)
        ),
        "structured_info": lambda c: _model_to_dict(parse_structured_info(c)),
        "decision": _parse_decision_with_metadata,
        "artifact": _parse_artifact_with_metadata,
        # ```matrx — the whole envelope object IS the data; the detector has
        # already lifted its control fields into metadata.
        "matrx": _parse_json_object,
    }


def _model_to_dict(model: Any) -> dict[str, Any] | None:
    """Convert a Pydantic model to dict with camelCase keys, or return None if model is None."""
    if model is None:
        return None
    return model.model_dump(by_alias=True)


# Cache the parser map after first build
_parser_map: dict[str, Callable[[str], Any]] | None = None


def _get_parser_map() -> dict[str, Callable[[str], Any]]:
    global _parser_map
    if _parser_map is None:
        _parser_map = _build_parser_map()
    return _parser_map


# ---------------------------------------------------------------------------
# Block type classification helpers
# ---------------------------------------------------------------------------

# Text Channel: content grows token-by-token, no parser, data field always null.
# `code` is included here — its content streams live; data (language, isDiff) is
# populated only when the block reaches status=complete.
_INCREMENTAL_TYPES = frozenset({
    "text", "thinking", "reasoning", "info", "task", "database",
    "private", "plan", "event", "tool", "code",
})

# Block Channel — stateless parser on every content change; returns completed
# items only (growing snapshot). Partial/in-progress items are withheld.
_PARTIAL_UPDATE_TYPES = frozenset({
    "flashcards", "cooking_recipe", "questionnaire",
    "table", "tasks", "transcript",
})

# Block Channel — dedicated stateful stream parser emits a growing structured
# snapshot whenever a renderable unit seals (semantic boundary).
_SEMANTIC_STREAM_TYPES = frozenset({
    "timeline",
})

# Block Channel — stream raw content so React has a live preview; parse into
# structured data only when the closing tag is detected (is_final=True).
# "mermaid" streams its raw DSL live (client renders progressively) and gets
# its metadata (title, diagram_type) parsed exactly once on close; content
# stays the raw source so the fence round-trips losslessly.
_MARKDOWN_COMPLETE_TYPES = frozenset({
    "research", "resources", "progress_tracker", "troubleshooting", "artifact", "mermaid",
    "structured_info",
    # Deliverable / raw-body fences: the body IS the artifact, so it streams
    # live and is never parsed into structured data. No registered kind (see
    # NON_ENVELOPE_BLOCK_TYPES in envelope.py for each reviewed reason).
    "svg", "html", "react", "chart", "map", "stats", "diff",
    # A ```matrx fence carries exactly one envelope — parsed whole on close.
    "matrx",
    # Editor pills + audio citations: the ATTRIBUTES are the payload and the
    # detector already lifted them into metadata.
    "editor_error", "editor_code_snippet", "audiocite",
})

# Block Channel — JSON-based blocks; parse only when the full JSON is received
# and valid. Raw content streams as a preview until then.
# "decision" is an attribute-bearing XML block; data is always complete on close.
_COMPLETE_ONLY_TYPES = frozenset({
    "quiz", "presentation", "decision_tree", "comparison_table",
    "diagram", "math_problem", "decision",
    # JSON-root-key families: a partial object is never renderable, so they
    # promote and parse only once the fence closes.
    "item_presentation", "schema_proposal",
})

# Types deliberately classified with NO parser: the fence/tag BODY (or the
# detector-lifted metadata) IS the payload, so ``data=null`` is correct, not a
# gap. Declared here so the integrity alarm stays meaningful — an alarm that
# always fires is an alarm nobody reads.
_NO_PARSER_BY_DESIGN = frozenset({
    # Deliverable / raw-body fences: the body IS the artifact.
    "svg", "html", "react", "chart", "map", "stats", "diff",
    # Editor pills + audio citations — the ATTRIBUTES are the payload, already
    # lifted into metadata by extract_attribute_xml_block.
    "editor_error", "editor_code_snippet", "audiocite",
})


def _is_incremental(block_type: str) -> bool:
    return block_type in _INCREMENTAL_TYPES


def _is_partial_update(block_type: str) -> bool:
    return block_type in _PARTIAL_UPDATE_TYPES


def _is_semantic_stream(block_type: str) -> bool:
    return block_type in _SEMANTIC_STREAM_TYPES


def _is_markdown_complete(block_type: str) -> bool:
    return block_type in _MARKDOWN_COMPLETE_TYPES


def _is_complete_only(block_type: str) -> bool:
    return block_type in _COMPLETE_ONLY_TYPES


# ---------------------------------------------------------------------------
# Startup integrity check
# ---------------------------------------------------------------------------

_integrity_checked: bool = False


def _run_integrity_check() -> None:
    """
    Cross-check all block type registrations for gaps and mismatches.

    Runs once on first use (lazy). Emits vcprint warnings (yellow) for
    non-critical gaps and errors (red) for broken configurations that will
    cause silent runtime failures.

    Open tasks referenced below are tracked in ai/processing/PROCESSING_TASKS.md.
    """
    global _integrity_checked
    if _integrity_checked:
        return
    _integrity_checked = True

    parser_map = _get_parser_map()

    # All types the system knows about
    all_enum_types = {e.value for e in BlockType}
    classified = (
        _INCREMENTAL_TYPES
        | _PARTIAL_UPDATE_TYPES
        | _SEMANTIC_STREAM_TYPES
        | _MARKDOWN_COMPLETE_TYPES
        | _COMPLETE_ONLY_TYPES
        | {"image", "video", "consolidated_reasoning"}
        | set(ATTRIBUTE_XML_BLOCKS)
    )

    # --- Gap 1: BlockType values not classified in any processing set --------
    unclassified = all_enum_types - classified
    for t in sorted(unclassified):
        vcprint(
            f"Block type '{t}' is declared in BlockType enum but not classified in any "
            f"processing type set (_INCREMENTAL_TYPES, _PARTIAL_UPDATE_TYPES, _COMPLETE_ONLY_TYPES). "
            f"_apply_block_content will fall through to plain-text fallback — data will never be parsed.",
            "[BlockProcessor] UNCLASSIFIED TYPE",
            color="red",
        )

    # --- Gap 2: COMPLETE_ONLY types with no parser ---------------------------
    for t in sorted(_COMPLETE_ONLY_TYPES):
        if t not in parser_map:
            vcprint(
                f"Block type '{t}' is in _COMPLETE_ONLY_TYPES but has no parser in _build_parser_map(). "
                f"Blocks of this type will always finalize with data=null. "
                f"See PROCESSING_TASKS.md for the open task.",
                "[BlockProcessor] MISSING PARSER",
                color="red",
            )

    # --- Gap 3: PARTIAL_UPDATE types with no parser (warning, not error) -----
    for t in sorted(_PARTIAL_UPDATE_TYPES):
        if t not in parser_map:
            vcprint(
                f"Block type '{t}' is in _PARTIAL_UPDATE_TYPES but has no parser. "
                f"Blocks will stream content only — no structured data field will be emitted.",
                "[BlockProcessor] NO PARSER (partial-update)",
                color="yellow",
            )

    # --- Gap 3b: MARKDOWN_COMPLETE types with no parser ----------------------
    for t in sorted(_MARKDOWN_COMPLETE_TYPES - _NO_PARSER_BY_DESIGN):
        if t not in parser_map:
            vcprint(
                f"Block type '{t}' is in _MARKDOWN_COMPLETE_TYPES but has no parser. "
                f"Blocks will finalize with data=null.",
                "[BlockProcessor] MISSING PARSER (markdown-complete)",
                color="red",
            )

    # --- Gap 3c: SEMANTIC_STREAM types — these use dedicated stream parsers,
    #             not the parser_map.  Just a sanity note, not an error.  ----

    # --- Gap 4: JSON_BLOCK_PATTERNS entries not in _COMPLETE_ONLY_TYPES ------
    for t in sorted(JSON_BLOCK_PATTERNS.keys()):
        if t not in _COMPLETE_ONLY_TYPES:
            vcprint(
                f"Block type '{t}' has a JSON_BLOCK_PATTERN for detection but is not in "
                f"_COMPLETE_ONLY_TYPES. JSON blocks that aren't classified will never "
                f"trigger the parser after type promotion.",
                "[BlockProcessor] JSON TYPE MISCONFIGURED",
                color="red",
            )

    # --- Gap 5: XML_TAG_BLOCKS entries not classified anywhere ---------------
    for t in sorted(XML_TAG_BLOCKS.keys()):
        if t not in classified:
            vcprint(
                f"Block type '{t}' has XML detection tags but is not in any processing type set. "
                f"The detector can identify it, but _apply_block_content has no handler for it.",
                "[BlockProcessor] XML TYPE UNCLASSIFIED",
                color="red",
            )

    # --- Gap 6: SPECIAL_CODE_LANGUAGES entries not classified anywhere -------
    for t in sorted(SPECIAL_CODE_LANGUAGES):
        if t not in classified:
            vcprint(
                f"'{t}' is in SPECIAL_CODE_LANGUAGES but not in any processing type set. "
                f"It will be detected via code fence but _apply_block_content has no handler.",
                "[BlockProcessor] SPECIAL_LANG UNCLASSIFIED",
                color="red",
            )

    # --- Gap 7: consolidated_reasoning has no detection path -----------------
    if "consolidated_reasoning" not in XML_TAG_BLOCKS:
        all_detectable = set(XML_TAG_BLOCKS.keys()) | set(JSON_BLOCK_PATTERNS.keys()) | SPECIAL_CODE_LANGUAGES
        if "consolidated_reasoning" not in all_detectable:
            vcprint(
                "Block type 'consolidated_reasoning' is registered but has no detection mechanism "
                "(not in XML_TAG_BLOCKS, JSON_BLOCK_PATTERNS, or SPECIAL_CODE_LANGUAGES). "
                "The detector can never produce this type. See TASK-003 in PROCESSING_TASKS.md.",
                "[BlockProcessor] UNDETECTABLE TYPE",
                color="yellow",
            )


# ---------------------------------------------------------------------------
# StreamBlockProcessor
# ---------------------------------------------------------------------------

class StreamBlockProcessor:
    """
    Stateful processor that sits between LLM token stream and NDJSON output.

    Accumulates tokens, detects block boundaries using the block detector,
    parses structured blocks with per-block parsers, and emits RenderBlockEvent
    objects for each block lifecycle change.

    Design:
    - Tokens are accumulated into a buffer
    - Periodically (on newlines, block boundaries), the buffer is analyzed
    - Detected blocks are tracked in a list with stable IDs
    - Events are emitted for: new block, content update, block complete, error
    """

    def __init__(self) -> None:
        _run_integrity_check()

        self._buffer: str = ""                   # Raw accumulated text from LLM
        self._blocks: list[RenderBlockState] = []    # All blocks seen so far
        self._block_counter: int = 0             # For generating block IDs
        self._last_split_result: list[DetectedBlock] = []  # Previous split for diffing
        self._pending_events: list[RenderBlockEvent] = []
        self._finalized: bool = False

        # Reasoning consolidation state
        self._reasoning_blocks: list[int] = []   # Indices of reasoning/thinking blocks

        # Stateful semantic stream parsers keyed by block_id.
        # Each _SEMANTIC_STREAM_TYPES block gets its own long-lived parser
        # instance that accumulates state across token calls.
        # Typed as Any to accommodate future SEMANTIC_STREAM parsers beyond
        # TimelineStreamParser (see TASK-000 in PROCESSING_TASKS.md).
        self._stream_parsers: dict[str, Any] = {}

        # Tag detection buffer — suppresses emission when the buffer tail
        # looks like a partial XML block tag (e.g. "<timeli") to prevent
        # text→block type flicker.  See streaming-constitution.md Part III.
        self._tag_buffer = TagDetectionBuffer()

        # Streaming partial kinds — the ledger that guarantees every partial
        # this processor announces gets a terminal event. See _stamp_partial.
        self._partials = PartialKindTracker()
        # block_id -> (block_index, block_type) as it stood when the partial was
        # announced. The drain needs an honest event for a block that no longer
        # exists in the split, and law 1 does not get to be conditional on the
        # block still being there. Entries are dropped as their partials close.
        self._partial_shadow: dict[str, tuple[int, str]] = {}

    def process_token(self, token: str) -> list[RenderBlockEvent]:
        """
        Process a single token from the LLM stream.

        Returns a list of RenderBlockEvent objects to emit to the client.
        May return an empty list if the token doesn't trigger any events.

        Suppresses emission when the buffer tail looks like a partial XML
        block tag (e.g. ``<timeli``) to avoid text→block type flicker.
        See streaming-constitution.md Part III — The Detection Buffer.
        """
        if self._finalized:
            return []

        self._buffer += token

        if self._tag_buffer.should_suppress(self._buffer):
            return []

        # Partial-table-row suppression — the pipe twin of the tag buffer.
        # A trailing line that starts with "|" but has no newline yet cannot be
        # classified: with one pipe it's "text", with two it's a table row, and
        # the detector flips between those on every token. Emitting during that
        # window creates a speculative text block per table row (e.g. "| One")
        # that the next re-split absorbs into the table — a phantom block the
        # client was already told about. Hold emission until the row completes.
        tail = self._buffer[self._buffer.rfind("\n") + 1:]
        if tail.lstrip().startswith("|"):
            return []

        return self._detect_and_emit()

    def process_chunk(self, chunk: str) -> list[RenderBlockEvent]:
        """
        Process a larger chunk of text (multiple tokens).
        Convenience method — same as process_token but clearer intent.
        """
        return self.process_token(chunk)

    def finalize(self) -> list[RenderBlockEvent]:
        """
        Called when the LLM stream ends. Closes all open blocks,
        runs final parsing on structured blocks, and performs
        reasoning consolidation.

        Returns final events to emit.
        """
        if self._finalized:
            return []
        self._finalized = True

        events: list[RenderBlockEvent] = []

        # Re-split the full buffer to get the final block set; is_final=True
        # causes _update_existing_block to mark each block COMPLETE and run
        # its final parser in a single pass — no second loop needed.
        final_blocks = split_content_into_blocks(self._buffer)
        events.extend(self._reconcile_blocks(final_blocks, is_final=True))

        # Close any tracked blocks that were NOT present in the final split
        # (e.g. a block whose opening fence was seen mid-stream but the buffer
        # was re-interpreted differently on the final pass).
        for block in self._blocks:
            if block.status == BlockStatus.STREAMING:
                block.status = BlockStatus.COMPLETE
                self._run_parser(block, is_final=True)
                events.append(self._emit(block))

        # Reasoning consolidation
        consolidation_event = self._consolidate_reasoning()
        if consolidation_event:
            events.append(consolidation_event)

        # THE ANTI-STUCK-SKELETON BACKSTOP. Every partial this processor
        # announced must end in a terminal event; anything still open when the
        # stream is over never resolved, and the user is looking at a skeleton
        # that will fill in never. Retract it explicitly, with the reason. This
        # is a second, independent layer: the per-block paths above already
        # close the ordinary cases, and this catches the day one of them
        # silently doesn't.
        events.extend(self.drain_open_partials("stream ended before the block resolved"))

        return events

    def drain_open_partials(self, reason: str) -> list[RenderBlockEvent]:
        """A terminal event for EVERY partial still open. Law 1, unconditionally.

        🚨 A BLOCK MISSING FROM THE FINAL LIST STILL GETS ITS TERMINAL.
        Until 2026-08-31 this loop did ``continue`` when the tracker named a
        block the processor no longer holds — the tracker had already been
        emptied by ``drain()``, so that block's partial was closed on the
        SERVER and left open forever on the CLIENT: the exact stuck skeleton
        law 1 exists to make impossible, in the one case the ordinary
        per-block paths cannot reach. A block that vanished from the split is
        precisely a block nothing else will ever terminate, so it is the case
        that matters most. The event is synthesized from what the block was
        when its partial was announced (``_partial_shadow``) — an honest,
        empty, COMPLETE block carrying the retraction.

        Public because two callers outside ``finalize()`` need it: the
        block-stream scope and the chat task both drain on their failure paths,
        where ``finalize()`` itself may have raised part-way through.
        """
        by_id = {block.block_id: block for block in self._blocks}

        def _became(block_id: str) -> tuple[str | None, str | None]:
            """What the region actually turned out to be — §3.3, populated."""
            block = by_id.get(block_id)
            if block is None:
                shadow = self._partial_shadow.get(block_id)
                return None, (shadow[1] if shadow else None)
            final_type = block.type
            return (BLOCK_KIND_MAP.get(final_type) or self._root_kind(block)), final_type

        events: list[RenderBlockEvent] = []
        for block_id, event in self._partials.drain(reason, resolve=_became):
            block = by_id.get(block_id)
            if block is not None:
                vcprint(
                    f"[partial kinds] block {block_id} ('{block.type}') announced a "
                    f"provisional kind that never resolved — retracting: {reason}",
                    color="yellow",
                )
                block.metadata[IR_PARTIAL_KEY] = event
                events.append(block.to_event())
                self._partial_shadow.pop(block_id, None)
                continue

            index, block_type = self._partial_shadow.get(block_id, (len(self._blocks), "text"))
            vcprint(
                f"[partial kinds] block {block_id} announced a provisional kind and "
                f"then VANISHED from the block list — retracting anyway so the client "
                f"cannot be left with a skeleton that never fills: {reason}",
                color="yellow",
            )
            events.append(
                RenderBlockEvent(
                    block_id=block_id,
                    block_index=index,
                    type=block_type,
                    status=BlockStatus.COMPLETE,
                    content=None,
                    data=None,
                    metadata={IR_PARTIAL_KEY: event, "retracted": True},
                )
            )
            self._partial_shadow.pop(block_id, None)
        return events

    def get_blocks(self) -> list[RenderBlockState]:
        """Get all current blocks (for inspection/testing)."""
        return list(self._blocks)

    def get_buffer(self) -> str:
        """Get current buffer contents (for inspection/testing)."""
        return self._buffer

    # -------------------------------------------------------------------
    # Internal methods
    # -------------------------------------------------------------------

    def _next_block_id(self) -> str:
        """Generate the next stable block ID."""
        block_id = f"blk_{self._block_counter}"
        self._block_counter += 1
        return block_id

    def _emit(self, block: RenderBlockState) -> RenderBlockEvent:
        """
        The single emission choke point — every render_block event leaves here.

        Stamps the canonical Content-IR envelope on ``metadata.__ir`` so the
        frontend renders the block WITHOUT re-parsing it (contract:
        /Users/armanisadeghi/code/common-docs/systems/content-ir-system/PYTHON_ENVELOPE_CONTRACT.md).

        COMPLETE-ONLY, and this guard is the whole law: a streaming block's
        data is a partial snapshot, and an envelope built from it would be
        seeded into the frontend's fingerprint-keyed envelope cache and poison
        every later read of that region.  `block.content` is read AFTER
        `_apply_block_content` has run, so for JSON blocks it is already the
        canonical `json.dumps(block.data)` the client will receive — the exact
        string the envelope's fingerprint must hash.

        `envelope_for_block` returns None (loudly) for any block whose type is
        unmapped, whose kind is unregistered, or whose parser output fails the
        kind's schema — no envelope simply means the client parses it itself.
        """
        if block.status == BlockStatus.COMPLETE:
            envelope = envelope_for_block(
                block.type,
                block.data,
                source_text=block.content,
                language=block.metadata.get("language"),
            )
            if envelope is not None:
                block.metadata[IR_ENVELOPE_KEY] = envelope
            self._stamp_partial_terminal(block)
        else:
            self._stamp_partial(block)
        return block.to_event()

    # -------------------------------------------------------------------
    # Streaming partial kinds — the live-rendering contract (§7.6)
    # -------------------------------------------------------------------
    #
    # Everything here rides ``metadata.__ir_partial`` on the SAME
    # ``render_block`` event the client already receives. It never touches
    # ``__ir``: that key means "validated against the registered schema", and a
    # partial is by definition unvalidated — stamping one there would seed the
    # frontend's fingerprint-keyed envelope cache with a half-built value and
    # poison every later read of the region (the complete-only law of
    # ``envelope.py``, honoured literally rather than relaxed).
    #
    # Partials are deliberately NOT schema-partitioned. The final envelope
    # routes unknown keys to ``residue`` because it claims to be a verified
    # instance; a partial claims nothing, so it carries the whole value and
    # says so in ``residue.notices`` (``partial_unvalidated``). Withholding
    # fields from a provisional render buys no safety and costs the user the
    # thing the contract exists to give them.

    def _partial_value(self, block: RenderBlockState) -> tuple[dict[str, Any], bool] | None:
        """The provisional value for a still-streaming block, or None.

        Two sources, and no third:

        * A block whose parser produces a GROWING snapshot (``_PARTIAL_UPDATE``
          / ``_SEMANTIC_STREAM``) already holds a valid dict in ``block.data``.
        * A JSON-bodied block (``_COMPLETE_ONLY``) holds raw, truncated JSON
          text in ``block.content``, which is exactly the case Arman named:
          Python closes it so the client receives valid JSON.

        Everything else — prose, code, raw-body deliverable fences, media — has
        no structured value to fill in progressively, so it gets no partial.
        Announcing a kind we cannot progressively populate would be a skeleton
        that never fills.
        """
        block_type = block.type

        # An agent BOUND to a kind (``ai.agent.produce`` →
        # ``response_format_for_kind``) streams a bare JSON document with no
        # fence and no XML tag, so the detector types it ``text``/``code``.
        # Its FIRST key is ``__kind``, which is a stronger declaration than any
        # detector heuristic — the model has named the shape itself. The value
        # is already in the kind's own vocabulary, so it needs no adapter and
        # no parser; the closer alone makes it renderable.
        if self._root_kind(block) is not None:
            return self._root_kind_json_value(block)

        if _is_partial_update(block_type) or _is_semantic_stream(block_type):
            if isinstance(block.data, dict) and block.data:
                return block.data, False
            return None

        if _is_complete_only(block_type):
            raw = (block.content or "").strip()
            if not raw.startswith(("{", "[")):
                # e.g. ``decision`` — an attribute-XML block whose payload is
                # lifted into metadata, never a JSON body.
                return None
            closed = close_partial_json(raw)
            if closed is None:
                return None
            # PREFER the real parser: its output is exactly what the final
            # value will be, so a partial rendered from it needs no allowance
            # from the component at all. But these parsers are STRICT by
            # design — ``parse_quiz`` refuses a question missing any field
            # ("a partial question is worse than no question") and one bad
            # question invalidates the whole block. That is right for a final
            # parse and fatal for a partial: relying on it alone produced ZERO
            # partials for an entire quiz stream. So the raw closed JSON is the
            # fallback, and ``adapt_block_data`` maps it into the kind's
            # vocabulary (it reads both key spellings — see ``_alias``).
            parsed = self._parse_detached(block.type, closed)
            if not isinstance(parsed, dict) or not parsed:
                try:
                    parsed = json.loads(closed)
                except ValueError:
                    return None
            if not isinstance(parsed, dict) or not parsed:
                return None
            # "Truncated" means the closer actually had to cut and close, i.e.
            # the tail of what the model has written so far is NOT in the value.
            return parsed, closed != raw

        return None

    def _root_kind(self, block: RenderBlockState) -> str | None:
        """The kind an unfenced root JSON block declares on its first key.

        Only for blocks the detector could NOT type into a kind of its own: a
        ``quiz`` fence is already ``quiz_set`` through ``BLOCK_KIND_MAP``, and
        letting a body-level ``__kind`` override that would put two
        declarations in charge of one region.
        """
        if BLOCK_KIND_MAP.get(block.type) is not None:
            return None
        return root_kind_declaration(block.content or "")

    def _root_kind_json_value(
        self, block: RenderBlockState
    ) -> tuple[dict[str, Any], bool] | None:
        """Closed, parsed JSON for a self-declaring root region."""
        raw = (block.content or "").strip()
        closed = close_partial_json(raw)
        if closed is None:
            return None
        try:
            parsed = json.loads(closed)
        except ValueError:
            return None
        if not isinstance(parsed, dict) or not parsed:
            return None
        return parsed, closed != raw

    def _parse_detached(self, block_type: str, content: str) -> dict[str, Any] | None:
        """Run a block type's parser over ``content`` WITHOUT touching a block.

        ``_run_parser`` writes its result and its failure reasons onto the
        block, which is right for the real parse and wrong here: a partial that
        fails to parse is the ordinary early-stream state, not a parse error
        the client should be told about. Returns None on any failure — the
        block simply gets no partial this token.
        """
        parser = _get_parser_map().get(block_type)
        if parser is None:
            return None
        try:
            result = parser(content)
        except Exception:  # noqa: BLE001 — a partial that won't parse is normal
            return None
        return result if isinstance(result, dict) else None

    def _stamp_partial(self, block: RenderBlockState) -> None:
        """Stamp a provisional kind instance on a streaming block's metadata.

        The block's ``metadata`` dict is LONG-LIVED and ships whole on every
        event, so a previously-stamped partial would silently re-ship on every
        later token — the client would see the same ``seq`` and the same value
        dozens of times, and worse, a partial would outlive its own terminal
        event. The key is therefore cleared first and re-stamped only when this
        event genuinely carries something new.
        """
        block.metadata.pop(IR_PARTIAL_KEY, None)
        kind = BLOCK_KIND_MAP.get(block.type) or self._root_kind(block)
        if kind is None:
            # The block type maps to no registered kind (prose, code, an
            # unregistered fence). If a partial was open under a DIFFERENT kind
            # this block has re-typed away from it — retract, loudly.
            self._retract_if_open(
                block,
                reason=f"block re-typed to '{block.type}', which declares no kind",
                became_kind=None,
            )
            return

        open_kind = self._partials.open_kind(block.block_id)
        if open_kind is not None and open_kind != kind:
            # Re-typed mid-stream (a code fence whose language stabilised into
            # something else, a text block the splitter re-read). Retract now;
            # the next token opens the new kind's partial. One event of lag
            # beats two conflicting states in one frame.
            self._retract_if_open(
                block,
                reason=f"detection changed from '{open_kind}' to '{kind}' mid-stream",
                became_kind=kind,
            )
            return

        if self._partials.regressed(block.block_id, len(block.content or "")):
            # The splitter handed this block LESS source than it already had —
            # a transient, and law 6 says a partial never goes backwards.
            return

        produced = self._partial_value(block)
        if produced is None:
            return
        value, truncated = produced

        try:
            # A self-declaring root region is ALREADY in the kind's vocabulary
            # — the provider was bound to the kind's own schema. The adapter
            # translates LEGACY PARSER vocabularies (``flashcards[].question``
            # → ``cards[].front``) and would find nothing to do here at best,
            # and rename a correct field at worst.
            if BLOCK_KIND_MAP.get(block.type) is not None:
                value = adapt_block_data(block.type, value)
        except Exception as exc:  # noqa: BLE001 — a partial NEVER breaks a stream
            vcprint(
                f"[partial kinds] adapt_block_data failed for '{block.type}' "
                f"(partial skipped, stream unaffected): {type(exc).__name__}: {exc}",
                color="yellow",
            )
            return

        if not self._partials.advanced(block.block_id, value):
            # Nothing new arrived for this region since the last partial — the
            # raw content event still ships, but re-sending an identical
            # payload every token is pure wire cost.
            return

        block.metadata[IR_PARTIAL_KEY] = partial_kind_event(
            kind=kind,
            value=value,
            seq=self._partials.next_seq(block.block_id),
            source_text=block.content or "",
            discriminator=(
                {"format": "json", "key": KIND_KEY}
                if BLOCK_KIND_MAP.get(block.type) is None
                else discriminator_for_block(block.type, block.metadata.get("language"))
            ),
            truncated=truncated,
        )
        self._partials.opened(block.block_id, kind)
        self._partial_shadow[block.block_id] = (block.block_index, block.type)

    def _stamp_partial_terminal(self, block: RenderBlockState) -> None:
        """Close the partial for a block that just completed.

        Every partial ends in exactly one terminal event — that is the whole
        anti-stuck-skeleton guarantee. ``superseded`` when the block completed
        as the kind we announced (the ``__ir`` envelope on this same event is
        the truth); ``retracted`` when it did not.

        The stale-key clear is not belt-and-braces. ``metadata`` is long-lived
        and ships whole on every event, so a terminal already emitted on an
        earlier event would re-ship here and the client would see the same
        partial terminated TWICE — breaking the exactly-one-terminal law it
        relies on. (Measured: a bare-JSON region that re-typed to prose
        retracted correctly and then retracted again on its complete event.)
        """
        open_kind = self._partials.open_kind(block.block_id)
        if open_kind is None:
            block.metadata.pop(IR_PARTIAL_KEY, None)
            return
        final_kind = BLOCK_KIND_MAP.get(block.type) or self._root_kind(block)
        if final_kind == open_kind:
            block.metadata[IR_PARTIAL_KEY] = superseded_event(
                kind=open_kind, seq=self._partials.next_seq(block.block_id)
            )
            self._partials.closed(block.block_id)
            self._partial_shadow.pop(block.block_id, None)
            return
        self._retract_if_open(
            block,
            reason=(
                f"completed as '{block.type}', not the detected kind '{open_kind}'"
            ),
            became_kind=final_kind,
        )

    def _retract_if_open(
        self, block: RenderBlockState, *, reason: str, became_kind: str | None
    ) -> None:
        open_kind = self._partials.open_kind(block.block_id)
        if open_kind is None:
            return
        block.metadata[IR_PARTIAL_KEY] = retracted_event(
            kind=open_kind,
            seq=self._partials.next_seq(block.block_id),
            reason=reason,
            became_kind=became_kind,
            became_block_type=block.type,
        )
        self._partials.closed(block.block_id)
        self._partial_shadow.pop(block.block_id, None)

    def _detect_and_emit(self) -> list[RenderBlockEvent]:
        """
        Run block detection on the current buffer and emit events
        for new/changed blocks.
        """
        # Split the accumulated buffer
        current_blocks = split_content_into_blocks(self._buffer)
        return self._reconcile_blocks(current_blocks, is_final=False)

    def _reconcile_blocks(
        self, detected: list[DetectedBlock], *, is_final: bool
    ) -> list[RenderBlockEvent]:
        """
        Reconcile detected blocks with our tracked block list.
        Emit events for new blocks and updated blocks.

        Strategy:
        - Compare detected blocks with existing blocks by index position
        - New blocks at the end → create new RenderBlockState
        - Existing blocks with changed content → emit update
        - Phantom blocks (tracked but no longer in detected set) → drop silently.
          This happens when a partial line was briefly classified as a new block
          but is re-absorbed into the preceding block on the next token (e.g. a
          table row that arrives byte-by-byte: "|" appears as a text block until
          the full row is received and consumed by extract_table).
        - On finalize, all blocks get status=complete
        """
        events: list[RenderBlockEvent] = []

        for idx, detected_block in enumerate(detected):
            if idx < len(self._blocks):
                # Existing block — check for updates
                existing = self._blocks[idx]
                updated = self._update_existing_block(existing, detected_block, is_final)
                if updated:
                    events.append(self._emit(existing))
            else:
                # New block
                block = self._create_block(detected_block, idx, is_final)
                self._blocks.append(block)
                events.append(self._emit(block))

                # Track reasoning blocks for consolidation
                if block.type in ("thinking", "reasoning"):
                    self._reasoning_blocks.append(idx)

        # Drop phantom blocks: any tracked block whose index is beyond the
        # current detected set was a transient split artifact that has since
        # been re-absorbed into a prior block.  Remove them so finalize() does
        # not emit stale complete events for content that no longer exists as a
        # standalone block.
        if len(detected) < len(self._blocks):
            # Retract, don't just forget: the client was already told about
            # these blocks (streaming upserts), and its store REPLACES a block
            # wholesale on upsert. An empty complete emit removes the phantom
            # from the rendered output; silent truncation left it on screen
            # forever (stale "| One" text fragments beside every table).
            for stale in self._blocks[len(detected):]:
                stale.status = BlockStatus.COMPLETE
                stale.content = ""
                stale.data = None
                stale.metadata = {**stale.metadata, "retracted": True}
                # A phantom that already announced a provisional kind must
                # retract it on the partial channel too — otherwise the client
                # clears the block but keeps a live partial for a block_id that
                # will never resolve. Same law, one layer down.
                self._retract_if_open(
                    stale,
                    reason="block was re-absorbed into a neighbour and no longer exists",
                    became_kind=None,
                )
                events.append(stale.to_event())
            self._blocks = self._blocks[: len(detected)]
            # Prune reasoning block indices that are now out of range
            self._reasoning_blocks = [
                i for i in self._reasoning_blocks if i < len(self._blocks)
            ]

        self._last_split_result = detected
        return events

    def _create_block(
        self, detected: DetectedBlock, index: int, is_final: bool
    ) -> RenderBlockState:
        """Create a new RenderBlockState from a DetectedBlock."""
        block_type = detected.type
        status = BlockStatus.COMPLETE if is_final else BlockStatus.STREAMING

        block = RenderBlockState(
            block_id=self._next_block_id(),
            block_index=index,
            type=block_type,
            status=status,
            raw_content=detected.content,
            metadata=dict(detected.metadata) if detected.metadata else {},
        )

        # Attempt immediate type promotion for code blocks whose language
        # identifies them as a richer type.
        if block_type == "code":
            block_type = self._try_promote_code_block(block, detected) or block_type

        self._apply_block_content(block, detected, block_type, is_final)
        return block

    def _update_existing_block(
        self, existing: RenderBlockState, detected: DetectedBlock, is_final: bool
    ) -> bool:
        """
        Update an existing block with new detected content.
        Returns True if the block was updated (and an event should be emitted).
        """
        if existing.status == BlockStatus.COMPLETE:
            return False

        # Check if content actually changed
        if existing.raw_content == detected.content and not is_final:
            return False

        existing.raw_content = detected.content

        if is_final:
            existing.status = BlockStatus.COMPLETE

        block_type = existing.type

        # Type promotion — resolve the block's true type as early as possible.
        #
        # Case 1: "code" → may be a richer type once the language tag stabilises.
        #   1a: language="json"  → quiz, presentation, decision_tree, etc.
        #   1b: language in SPECIAL_CODE_LANGUAGES → use the language as the type
        #       (structured_info, transcript, tasks, flashcards, questionnaire,
        #        cooking_recipe).  The language token arrives truncated early in
        #       the stream; once complete the detector sets detected.language to
        #       the full keyword, so we promote here.
        if block_type == "code":
            promoted = self._try_promote_code_block(existing, detected)
            if promoted:
                block_type = promoted

        # Case 2: "text" → the splitter may re-classify the same content as a
        #         richer type once more lines arrive (e.g. a table header
        #         becomes a confirmed table once the separator row is seen).
        #         Promote the tracked type to match what the detector now says.
        elif block_type == "text" and detected.type != "text":
            existing.type = detected.type
            block_type = existing.type

        # Case 3: any other mismatch — the full-buffer re-split is the truth.
        # Index-shifted reconciliation used to leave a block frozen at whatever
        # type it was CREATED as while its content silently became something
        # else (a markdown table living inside a "code" block, etc.). A block
        # that hasn't been finalized re-types in place (stable block_id — the
        # client upsert replaces it), dropping any parsed state built under the
        # old type.
        elif detected.type != existing.type:
            existing.type = detected.type
            existing.data = None
            self._stream_parsers.pop(existing.block_id, None)
            block_type = existing.type

        # Merge metadata now that type promotion has been resolved.
        if detected.type == existing.type:
            existing.metadata.update(detected.metadata or {})

        self._apply_block_content(existing, detected, block_type, is_final)
        return True

    def _apply_block_content(
        self,
        block: RenderBlockState,
        detected: DetectedBlock,
        block_type: str,
        is_final: bool,
    ) -> None:
        """
        Apply content/data to a block based on its type.

        This is the single authoritative dispatch for both create and update paths,
        ensuring the content field is always kept in sync with raw_content.
        """
        if _is_incremental(block_type):
            block.content = detected.content
            # code is Text Channel (content streams live), but its structured
            # data (language, isDiff) is only populated once the block is
            # complete — never during streaming, to avoid mid-word language values.
            if block_type == "code":
                self._apply_code_data(block, detected, is_final)

        elif block_type in ("image", "video"):
            self._apply_media_block(block, detected)

        elif _is_semantic_stream(block_type):
            self._apply_semantic_stream_block(block, detected, is_final)

        elif _is_partial_update(block_type):
            # Run the parser incrementally. Parsers that support partial-aware
            # parsing receive is_final so they can withhold the last in-progress
            # item during streaming and include it only on finalize.
            self._run_parser(block, is_final=is_final)
            block.content = detected.content

        elif _is_markdown_complete(block_type):
            # Stream raw content so React has a live markdown preview.
            # The structured data field is populated exactly once: when the
            # block is finalized (is_final=True). We deliberately do NOT parse
            # on detected.metadata["isComplete"] because that fires as soon as
            # the detector sees the closing tag — which may be mid-stream if the
            # LLM keeps writing after the closing tag. Tying parse to is_final
            # ensures the parser sees the complete, stable content exactly once.
            block.content = detected.content

            if is_final:
                # Artifact blocks need metadata forwarded (contains artifactId,
                # artifactType, artifactTitle from the detector).
                if block_type == "artifact":
                    self._run_parser(block, metadata=block.metadata)
                else:
                    self._run_parser(block)

        elif _is_complete_only(block_type):
            # The parser is the authority for this block type.
            #
            # During streaming: content holds the raw accumulating text so the
            # client has something to show (progress indicator / raw preview).
            # The client MUST NOT attempt to parse this partial content.
            #
            # Once complete: the parser runs against the full raw text.
            #   - Success: block.data is the validated, normalized output.
            #              content becomes json.dumps(block.data) — the single
            #              source of truth, guaranteed camelCase, guaranteed shape.
            #   - Failure: block.data stays None; metadata records the reason.
            #              content stays as the raw text so nothing is lost.
            #
            # Special case: "decision" blocks have their structured data pre-parsed
            # during extraction and stored in metadata["decision"]. Pass metadata
            # to the parser so it can use the already-extracted data directly.
            block.content = detected.content  # raw accumulating preview

            if is_final or detected.metadata.get("isComplete"):
                if block_type == "decision":
                    self._run_parser(block, metadata=block.metadata)
                else:
                    self._run_parser(block)
                if block.data is not None:
                    # Replace raw content with the canonical validated output
                    block.content = json.dumps(block.data, ensure_ascii=False)

        else:
            # Unknown type — treat as text
            block.content = detected.content

    def _apply_semantic_stream_block(
        self,
        block: RenderBlockState,
        detected: DetectedBlock,
        is_final: bool,
    ) -> None:
        """
        Handle a _SEMANTIC_STREAM_TYPES block (currently: timeline).

        On every call the block's raw content is updated.  The dedicated
        stream parser decides — based on structural line boundaries — whether
        a new renderable unit has been sealed and, if so, updates block.data
        with the growing, fully-valid structured payload.

        On finalize the parser flushes any pending buffered item and produces
        the final canonical data.

        The React component always receives the same data shape; data just
        grows richer with each emission.
        """
        block.content = detected.content

        if is_final or detected.metadata.get("isComplete"):
            # Flush the stateful parser to get the final complete data
            parser = self._stream_parsers.get(block.block_id)
            if parser is None:
                # Edge case: block was complete before any incremental feed
                parser = TimelineStreamParser()
            result = parser.finalize()
            block.data = result.model_dump(by_alias=True)
            return

        # Incremental: feed the current content into the parser
        if block.block_id not in self._stream_parsers:
            self._stream_parsers[block.block_id] = TimelineStreamParser()
        parser = self._stream_parsers[block.block_id]
        result = parser.feed(detected.content)
        if result is not None:
            # A semantic boundary was crossed — update data
            block.data = result.model_dump(by_alias=True)
        # If result is None, keep block.data as-is (no new semantic unit)

    def _apply_code_data(self, block: RenderBlockState, detected: DetectedBlock, is_final: bool) -> None:
        """
        Populate the structured data field for code blocks.

        Code is a Text Channel type — content streams live on every token.
        The data field (language, code, isDiff) is only written once the block
        is complete, keeping the two-channel contract clean: no structured data
        leaks out during mid-stream emissions.
        """
        from matrx_ai.processing.blocks.parsers.diff_parser import (
            detect_diff_style,
            looks_like_diff,
        )

        language = detected.language or ""
        code = detected.content

        # Only populate data when the block is fully received.
        if not is_final and block.status != BlockStatus.COMPLETE:
            block.data = None
            block.metadata["language"] = language  # stable enough for display hints
            return

        is_diff = looks_like_diff(code)
        block.data = {
            "language": language,
            "code": code,
            "isDiff": is_diff,
        }
        if is_diff:
            block.data["diffStyle"] = detect_diff_style(code)
        block.metadata["language"] = language

    def _apply_media_block(self, block: RenderBlockState, detected: DetectedBlock) -> None:
        """Apply image/video block data."""
        block.data = {
            "src": detected.src,
            "alt": detected.alt,
        }

    def _try_promote_code_block(
        self, block: RenderBlockState, detected: DetectedBlock
    ) -> str | None:
        """
        Attempt to promote a generic 'code' block to its true type as early as
        possible in the stream.

        Three promotion paths:
          • detected.type in SPECIAL_CODE_LANGUAGES → the detector has already
            resolved the full language keyword and emitted the correct type
            (structured_info, transcript, tasks, flashcards, questionnaire,
             cooking_recipe).  The opening fence is truncated in early chunks;
            once the full keyword is seen the detector sets type directly.
          • detected.language in SPECIAL_CODE_LANGUAGES → same, via language field.
          • detected.language == "json" → delegate to JSON type detection
            (quiz, presentation, decision_tree, etc.)

        Returns the new type string if promoted, or None if no promotion.
        """
        rich_type: str | None = None

        if detected.type in SPECIAL_CODE_LANGUAGES:
            rich_type = detected.type
        elif detected.language:
            normalized_language = CODE_LANGUAGE_ALIASES.get(detected.language, detected.language)
            if normalized_language in SPECIAL_CODE_LANGUAGES:
                rich_type = normalized_language

        if rich_type:
            block.type = rich_type
            block.data = None
            block.content = ""
            block.metadata.update(detected.metadata or {})
            return rich_type

        if detected.language == "json":
            if self._try_promote_json_block(block, detected):
                return block.type

        return None

    def _try_promote_json_block(self, block: RenderBlockState, detected: DetectedBlock) -> bool:
        """
        Attempt to promote a generic 'code' block with language='json' to a richer
        type (e.g. 'quiz', 'presentation') once enough content has accumulated.

        Returns True if the block type was promoted.
        """
        json_type = detect_json_block_type(detected.content)
        if json_type and json_type != "code":
            block.type = json_type
            # Clear stale code-block data so the promoted type starts fresh
            block.data = None
            block.content = ""
            # Merge the detected metadata now that types match
            block.metadata.update(detected.metadata or {})
            return True
        return False

    def _run_parser(
        self,
        block: RenderBlockState,
        *,
        is_final: bool = False,
        metadata: dict[str, Any] | None = None,
    ) -> None:
        """
        Run the appropriate parser for a block and set block.data.

        is_final is forwarded to parsers that support partial-aware parsing
        (e.g. table_parser, transcript_parser) so they can withhold the
        last in-progress item during streaming and include it on finalize.

        metadata is forwarded to parsers that need pre-parsed extraction data
        (e.g. the 'decision' parser uses metadata["decision"] from extraction).

        On success: block.data is set to the validated, normalized dict.
        On parser returning None: the content was structurally invalid — we
            record the reason so the client knows the block could not be parsed.
        On unexpected exception: captured and recorded; never crashes the stream.
        """
        parser_map = _get_parser_map()
        parser = parser_map.get(block.type)
        if parser is None:
            return

        try:
            if metadata is not None:
                result = parser(block.raw_content, metadata=metadata)
            else:
                result = parser(block.raw_content, is_final=is_final)
        except TypeError:
            # Parser doesn't accept keyword args — call with raw content only (legacy parsers)
            try:
                result = parser(block.raw_content)
            except Exception as exc:
                block.metadata["parseError"] = True
                block.metadata["parseFailReason"] = f"parser raised {type(exc).__name__}: {exc}"
                return
        except Exception as exc:
            block.metadata["parseError"] = True
            block.metadata["parseFailReason"] = f"parser raised {type(exc).__name__}: {exc}"
            return

        if result is not None:
            block.data = result
        else:
            # Parser returned None — content was recognized as this type but
            # failed structural validation.  Record it; leave content intact.
            block.metadata["parseError"] = True
            block.metadata["parseFailReason"] = (
                f"{block.type} block failed validation — "
                "content may be malformed or incomplete"
            )

    def _consolidate_reasoning(self) -> RenderBlockEvent | None:
        """
        Consolidate multiple reasoning/thinking blocks into a single
        consolidated_reasoning block. Matches TypeScript behavior in
        EnhancedChatMarkdown.

        Returns a new consolidated_reasoning event if there are multiple
        reasoning blocks, otherwise None.
        """
        if len(self._reasoning_blocks) < 2:
            return None

        reasoning_texts: list[str] = []
        for idx in self._reasoning_blocks:
            if idx < len(self._blocks):
                block = self._blocks[idx]
                if block.content:
                    reasoning_texts.append(block.content)

        if not reasoning_texts:
            return None

        consolidated = RenderBlockState(
            block_id=self._next_block_id(),
            block_index=len(self._blocks),
            type="consolidated_reasoning",
            status=BlockStatus.COMPLETE,
            data={"reasoning_texts": reasoning_texts},
        )
        self._blocks.append(consolidated)
        return consolidated.to_event()


# ---------------------------------------------------------------------------
# Convenience function for non-streaming (batch) processing
# ---------------------------------------------------------------------------

def process_complete_content(content: str) -> list[RenderBlockEvent]:
    """
    Process a complete markdown string (non-streaming) and return
    all content block events.

    Useful for:
    - Processing saved messages from the database
    - Testing
    - Non-streaming API responses
    """
    processor = StreamBlockProcessor()
    # Feed entire content at once
    events = processor.process_token(content)
    # Finalize
    events.extend(processor.finalize())
    return events


def process_complete_to_blocks(content: str) -> list[dict[str, Any]]:
    """
    Process complete markdown content and return a list of block dicts.

    Each dict has: block_id, block_index, type, status, content, data, metadata.
    Ready for JSON serialization.
    """
    events = process_complete_content(content)
    result: list[dict[str, Any]] = []

    # Take the last event for each block_id (final state)
    event_map: dict[str, RenderBlockEvent] = {}
    for event in events:
        event_map[event.block_id] = event

    for event in event_map.values():
        result.append(event.model_dump(by_alias=True, exclude_none=True))

    result.sort(key=lambda b: b.get("blockIndex", 0))
    return result
