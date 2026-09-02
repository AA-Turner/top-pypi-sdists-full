"""Canonical ``metadata.__ir`` envelope assembler — the ``py-block-detector`` engine.

The frontend accepts a pre-built ``CanonicalBlockIR`` on a ``render_block``
event and renders it WITHOUT re-parsing. This module builds that envelope.
Wire contract: ``/Users/armanisadeghi/code/common-docs/systems/content-ir-system/PYTHON_ENVELOPE_CONTRACT.md``.
TS twin (shape reference): ``features/content-ir/core/normalize.ts#envelopeFromCompleteValue``
and ``core/ir-types.ts``.

THREE LAWS (each one is a defect if broken):

1. **Complete-only.** Never stamp a streaming/partial block. A premature
   envelope is seeded into the FE's fingerprint-keyed envelope cache and
   poisons every later read of that region. The caller gates on the block's
   own completion signal (``BlockStatus.COMPLETE``), never on a parser's
   "looks done" heuristic.
2. **Validate what you emit.** ``value`` is validated against the kind's
   registered ``emitted_json_schema`` before stamping. An envelope the FE
   would reject (``sanitizeInboundEnvelopeMetadata``) or that misdescribes its
   kind is worse than no envelope — no envelope simply degrades to the FE's
   ordinary content-driven parse.
3. **Zero data loss.** A CLOSED kind schema (``additionalProperties: false``,
   the common case) lets ``value`` hold schema fields + ``__kind`` ONLY; keys
   the schema does not know are carried verbatim in ``residue.extra`` (root) or
   ``nodeIndex[pathKey].residue.extra`` (children) — Protobuf unknown-fields
   discipline. Nothing the parser produced is ever dropped. An OPEN node
   (``additionalProperties: true`` or a sub-schema — e.g. ``item_presentation``'s
   ``additionalDetails``) DECLARES that it accepts unnamed keys, so those keys
   are known to the schema and stay in ``value``; routing them to residue would
   render the node empty and, via the collapse rule below, suppress the
   envelope entirely.

Residue semantics (why the partition exists):
  * unknown key                      -> ``residue.extra``
  * schema field absent from output  -> ``residue.optionalMissing``
  * schema field present but ``None`` where the schema forbids null
    -> dropped from ``value``, recorded in ``residue.optionalMissing``.
    Pydantic's ``model_dump`` has no ``exclude_none`` here, so unset optional
    fields surface as explicit ``null`` and would fail ``type: "string"``.
    An absent optional and a null optional mean the same thing; recording it
    in ``optionalMissing`` is the contract's channel for exactly that.

Failure posture — LOUD, never blocking (mirrors ``matrx_graph.kinds``): an
unmapped block type, an unregistered kind, a cold catalog, or a schema-invalid
value all mean "do not stamp", logged once per cause. The stream is never
interrupted and the block still renders via the FE's own parser.
"""

from __future__ import annotations

import asyncio
import copy
import json
import logging
from typing import Any

# Shared Content IR primitives live in matrx-graph (matrx-ai depends on
# matrx-graph, never the reverse) so the workflow scheduler's producer
# (matrx_graph.content_ir.envelope) and this
# chat-side producer share ONE fingerprint + one set of wire constants.
from matrx_graph.content_ir.envelope import (
    IR_ENVELOPE_KEY as IR_ENVELOPE_KEY,  # re-export: stream_processor reads it here
)
from matrx_graph.content_ir.envelope import IR_VERSION, KIND_KEY
from matrx_graph.content_ir.fingerprint import fingerprint_text

logger = logging.getLogger(__name__)

IR_ENGINE = "py-block-detector"


# ---------------------------------------------------------------------------
# Block type -> kind slug. A SMALL, REVIEWED TABLE — never a guess.
# ---------------------------------------------------------------------------
#
# Every pair below was verified by running the real parser over real block
# source and validating its output against the kind's LIVE
# ``content_ir.kind_definition.emitted_json_schema`` (Draft 2020-12, recursive,
# ``additionalProperties: false`` at every level).
#
# Legacy parser vocabularies are converted by ``adapt_block_data`` below. The
# adapter is deliberately outside the parser: provider/client payloads keep
# their established shape, while the Content IR boundary gets canonical data.
# Original keys are retained and therefore travel in residue (law 3).
#
BLOCK_KIND_MAP: dict[str, str] = {
    "transcript": "transcript",
    "tasks": "task_list",
    "timeline": "timeline",
    "cooking_recipe": "cooking_recipe",
    "troubleshooting": "troubleshooting_guide",
    "research": "research_report",
    "decision_tree": "decision_tree",
    "comparison_table": "comparison_set",
    "diagram": "diagram_spec",
    "flashcards": "flashcard_set",
    "quiz": "quiz_set",
    "mermaid": "mermaid_diagram",
    "progress_tracker": "progress_tracker",
    "presentation": "presentation_deck",
    "resources": "resource_collection",
    "math_problem": "math_problem",
    "item_presentation": "item_presentation",
    "questionnaire": "questionnaire",
    "structured_info": "structured_info",
}


# ---------------------------------------------------------------------------
# Reviewed NON-envelope block types — every deliberate bypass, classified.
# ---------------------------------------------------------------------------
#
# Every block type the detector/processor can emit is either in BLOCK_KIND_MAP
# (Shape-backed -> canonical envelope) or listed here with the reviewed reason
# it gets none. A type in NEITHER table is an UNCLASSIFIED bypass and screams
# via ``_log_once`` in ``envelope_for_block`` — no silent bypasses, ever.
#
# Classifications (common-docs/systems/content-ir-system/FEATURE.md — framed protocols
# carry kind/version out of band; protocol/control events are not display
# Shapes unless explicitly classified as such):
#
NON_ENVELOPE_BLOCK_TYPES: dict[str, str] = {
    # -- protocol/control: framed stream/reasoning channels, not display Shapes
    "thinking": "protocol — model reasoning channel",
    "reasoning": "protocol — model reasoning channel",
    "consolidated_reasoning": "protocol — merged reasoning channel",
    "info": "protocol — inline notice channel",
    "task": "protocol — task/agent control channel",
    "database": "protocol — DB operation notice channel",
    "private": "protocol — hidden-from-user channel",
    "plan": "protocol — planning channel",
    "event": "protocol — event notice channel",
    "tool": "protocol — tool-call notice channel",
    "matrx": "protocol — pre-framed matrx envelope (carries its own typing)",
    "decision": "protocol — interactive decision block (attribute-XML framed)",
    "artifact": "protocol — artifact framing; the artifact CONTENT is typed separately",
    "schema_proposal": "protocol — output-schema authoring proposal, not display content",
    "editor_error": "protocol — editor diagnostic reference",
    "editor_code_snippet": "protocol — editor selection reference",
    "audiocite": "protocol — timestamped audio citation reference",
    # -- generic/scalar content: no kind identity to carry
    "text": "generic — plain markdown prose",
    "code": "generic — code fence; language is metadata, not a kind",
    "image": "generic — media reference",
    "video": "generic — media reference",
    "html": "generic — source-code rendering mode",
    "react": "generic — source-code rendering mode",
    "svg": "generic — source-code rendering mode",
    "diff": "generic — source-code rendering mode",
    "chart": "generic — legacy visualization renderer without a registered kind",
    "map": "generic — legacy visualization renderer without a registered kind",
    "stats": "generic — legacy visualization renderer without a registered kind",
    "audio": "generic — media reference",
    "youtube": "generic — media reference (external embed)",
    "matrx_file": "generic — a reference to one of OUR files; identity is the file_id",
    "tree": "generic — ASCII/box-drawing tree rendering of prose",
    "accent-divider": "generic — a visual rule; no content",
    "heavy-divider": "generic — a visual rule; no content",
    # -- markdown-first by RATIFIED RULING: never a kind, never enveloped
    "table": (
        "RATIFIED 2026-07-15: tables stay markdown-first + click-to-convert "
        "FOREVER — never auto-kind. The core content is the markdown table "
        "itself (rendered richly by the FE table component); promotion to a "
        "live data table is an explicit USER action (the Convert button), "
        "never an envelope. Do NOT register a table kind or move this entry "
        "to BLOCK_KIND_MAP — this is the Convert Pattern exemplar (see "
        "matrx-frontend features/content-ir/docs/SHAPE_SYSTEM.md)."
    ),
}


def _json_string(value: Any) -> str:
    if isinstance(value, str):
        return value
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), default=str)


def _alias(source: dict[str, Any], *names: str, default: Any = None) -> Any:
    """First present key among ``names`` — the parsers' own alias discipline.

    ``adapt_block_data`` promises "a lossless canonical view", and on the final
    path it is always handed PARSER output (camelCase by ``by_alias=True``), so
    reading only the camel spelling was invisibly fine. It is not fine for any
    caller handing it SOURCE-shaped data: the snake spelling the model actually
    wrote silently produced an EMPTY canonical field — a value that looks
    populated and renders blank. The parsers already accept both spellings
    (``quiz_parser._get``); the adapter now does too. Camel wins first, so the
    final path is bit-for-bit unchanged.
    """
    for name in names:
        if name in source:
            return source[name]
    return default


def adapt_block_data(block_type: str, data: dict[str, Any]) -> dict[str, Any]:
    """Return a lossless canonical view of a legacy parser result.

    The input is never mutated. Renamed/wrapped source fields remain alongside
    their canonical equivalents and are routed into envelope residue by the
    schema partition. This makes each conversion reversible and keeps the
    existing render-block wire contract untouched.
    """
    adapted = copy.deepcopy(data)

    if block_type == "flashcards":
        adapted.setdefault("title", "Flashcards")

    elif block_type == "quiz":
        adapted.setdefault(
            "title", str(_alias(data, "quizTitle", "quiz_title") or "Quiz")
        )
        questions: list[dict[str, Any]] = []
        for source in _alias(data, "multipleChoice", "multiple_choice") or []:
            if not isinstance(source, dict):
                continue
            options = source.get("options") or []
            answer = _alias(source, "correctAnswer", "correct_answer", default="")
            if isinstance(answer, int) and 0 <= answer < len(options):
                answer = options[answer]
            questions.append(
                {
                    "type": "multiple_choice",
                    "question": str(source.get("question") or ""),
                    "options": options,
                    "correct_answer": str(answer),
                    "explanation": source.get("explanation"),
                }
            )
        adapted.setdefault("questions", questions)

    elif block_type == "mermaid":
        adapted.setdefault("code", str(data.get("source") or ""))

    elif block_type == "progress_tracker":
        root_aliases = {
            "overallProgress": "overall_progress",
            "totalItems": "total_items",
            "completedItems": "completed_items",
        }
        for old, new in root_aliases.items():
            if old in data:
                adapted.setdefault(new, data[old])
        phases: list[dict[str, Any]] = []
        for category in data.get("categories") or []:
            if not isinstance(category, dict):
                continue
            phase = {
                "id": category.get("id"),
                "name": category.get("name") or "Phase",
                "description": category.get("description"),
                "color": category.get("color"),
                "completion_percentage": _alias(
                    category, "completionPercentage", "completion_percentage"
                ),
                "steps": [],
            }
            for item in category.get("items") or []:
                if not isinstance(item, dict):
                    continue
                phase["steps"].append(
                    {
                        "id": item.get("id"),
                        "text": item.get("text") or item.get("name") or "",
                        "completed": bool(item.get("completed", False)),
                        "priority": item.get("priority"),
                        "estimated_hours": _alias(
                            item, "estimatedHours", "estimated_hours"
                        ),
                        "optional": item.get("optional"),
                        "category": item.get("category"),
                    }
                )
            phases.append(phase)
        adapted.setdefault("phases", phases)

    elif block_type == "presentation":
        slides: list[dict[str, Any]] = []
        for original in data.get("slides") or []:
            if not isinstance(original, dict):
                continue
            slide = copy.deepcopy(original)
            extra = slide.get("extra")
            if isinstance(extra, dict):
                slide["extra"] = {key: _json_string(value) for key, value in extra.items()}
                slide["legacyExtra"] = extra
            slides.append(slide)
        adapted["slides"] = slides

    elif block_type == "resources":
        allowed_types = {
            "documentation",
            "tool",
            "video",
            "article",
            "course",
            "book",
            "tutorial",
            "other",
        }
        categories: list[dict[str, Any]] = []
        for original in data.get("categories") or []:
            if not isinstance(original, dict):
                continue
            category = copy.deepcopy(original)
            resources = copy.deepcopy(original.get("items") or [])
            for resource in resources:
                if isinstance(resource, dict) and resource.get("type") not in allowed_types:
                    resource["type"] = "other"
            category.setdefault("resources", resources)
            categories.append(category)
        adapted["categories"] = categories

    elif block_type == "math_problem":
        inner = data.get("math_problem")
        if isinstance(inner, dict):
            aliases = {
                "courseName": "course_name",
                "topicName": "topic_name",
                "moduleName": "module_name",
                "introText": "intro_text",
                "finalStatement": "final_statement",
                "problemStatement": "problem_statement",
            }
            for key, value in inner.items():
                adapted.setdefault(aliases.get(key, key), copy.deepcopy(value))

    elif block_type == "questionnaire":
        questions: list[dict[str, Any]] = []
        for index, section in enumerate(data.get("sections") or []):
            if not isinstance(section, dict):
                continue
            items = section.get("items") or []
            question: dict[str, Any] = {
                "id": f"question-{index + 1}",
                "type": "radio" if items else "text",
                "question": section.get("title") or f"Question {index + 1}",
                "description": section.get("content") or None,
            }
            if items:
                question["options"] = [
                    {"name": str(item.get("name") or "")}
                    for item in items
                    if isinstance(item, dict)
                ]
            questions.append(question)
        adapted.setdefault("title", "Questionnaire")
        adapted.setdefault("questions", questions)

    return adapted


def discriminator_for_block(block_type: str, language: str | None) -> dict[str, Any]:
    """Which wire syntax established this block's kind (provenance only).

    Derived from the detector's OWN registries, not guessed. A fence language
    wins over an XML tag because ``cooking_recipe`` is registered in both and
    a detected fence language proves which one actually arrived.

    CAVEAT (contract gap, reported): the FE's ``IrDiscriminator`` json variant
    is hard-typed ``{format: "json", key: "__kind"}``. Our JSON blocks resolve
    their kind from a legacy root WRAPPER key (``decision_tree``, ``comparison``,
    ``diagram``) — there is no ``__kind`` in the source. ``format: "json"``
    correctly names the wire format; ``key`` is the only value the type allows.
    """
    from matrx_ai.processing.blocks.block_detector import (
        JSON_BLOCK_PATTERNS,
        SPECIAL_CODE_LANGUAGES,
        XML_TAG_BLOCKS,
    )

    if language and language in SPECIAL_CODE_LANGUAGES:
        return {"format": "fence", "language": language}
    if block_type in XML_TAG_BLOCKS:
        return {"format": "xml", "tag": block_type}
    if block_type in JSON_BLOCK_PATTERNS:
        return {"format": "json", "key": KIND_KEY}
    return {"format": "fence", "language": block_type}


# ---------------------------------------------------------------------------
# Schema-guided partition (the zero-data-loss split)
# ---------------------------------------------------------------------------


def _resolve_ref(schema: dict[str, Any], root: dict[str, Any]) -> dict[str, Any]:
    seen = 0
    while "$ref" in schema:
        seen += 1
        if seen > 32:  # pathological / cyclic $ref chain
            return {}
        name = str(schema["$ref"]).rsplit("/", 1)[-1]
        target = (root.get("$defs") or {}).get(name)
        if not isinstance(target, dict):
            return {}
        schema = target
    return schema


def _ref_name(schema: dict[str, Any]) -> str:
    ref = schema.get("$ref")
    return str(ref).rsplit("/", 1)[-1] if isinstance(ref, str) else ""


def _allows_null(schema: dict[str, Any]) -> bool:
    declared = schema.get("type")
    if declared == "null":
        return True
    return isinstance(declared, list) and "null" in declared


def _declared_marker(schema: dict[str, Any]) -> str | None:
    """The kind slug this schema node DECLARES on ``__kind``, or None.

    Only a ``const`` counts. A ``__kind`` property with no const (the open
    "when it is one" form) names nothing, so nothing is stamped there.
    """
    prop = (schema.get("properties") or {}).get(KIND_KEY)
    if not isinstance(prop, dict):
        return None
    const = prop.get("const")
    return const if isinstance(const, str) and const else None


def _branch_fits(value: dict[str, Any], schema: dict[str, Any]) -> bool:
    """Cheap structural test: does this ``anyOf`` branch's non-marker required
    set exist on the value? Used only to CHOOSE a branch, never to validate —
    the real verdict is still ``validate_instance`` on the assembled result."""
    required = [key for key in (schema.get("required") or []) if key != KIND_KEY]
    return all(key in value for key in required)


def _stamp_declared_markers(
    value: Any,
    schema: dict[str, Any],
    root: dict[str, Any],
) -> Any:
    """Write the ``__kind`` markers the SCHEMA ITSELF declares, at every depth.

    THE DEFECT THIS FIXES (2026-08-23). The Schema Law made ``__kind`` a
    REQUIRED root property on all 19 kinds in ``BLOCK_KIND_MAP``, but the
    legacy parsers this module adapts from predate the marker and never emit
    one — so ``validate_instance`` below failed with "'__kind' is a required
    property" for EVERY one of them and no ``__ir`` envelope was ever stamped.
    Chat's entire structured-content channel was silently dead: a flashcard
    deck, a quiz, a recipe, a timeline reached every client as prose.

    Nothing is invented here. A marker is written ONLY where the schema
    declares a ``const`` for it, which is the schema saying, in its own words,
    what an object at this position IS. An existing marker is never
    overwritten — a producer that already named itself is authoritative.

    ``anyOf`` (e.g. ``flashcard_set.cards``): the first branch whose non-marker
    required fields the value satisfies wins. Ambiguity there is real — a plain
    ``{front, back}`` card fits both ``flashcard`` and ``enhanced_flashcard``
    — and the first branch is the base shape by construction, which is what
    the legacy parser actually produced.

    Pure: the input is never mutated.
    """
    resolved = _resolve_ref(schema, root) if isinstance(schema, dict) else {}
    if not resolved:
        return value

    if isinstance(value, list):
        items = resolved.get("items")
        if not isinstance(items, dict):
            return value
        return [_stamp_declared_markers(item, items, root) for item in value]

    if not isinstance(value, dict):
        return value

    branches = resolved.get("anyOf")
    if isinstance(branches, list):
        for branch in branches:
            if not isinstance(branch, dict):
                continue
            target = _resolve_ref(branch, root)
            if target and _branch_fits(value, target):
                return _stamp_declared_markers(value, branch, root)
        return value

    properties = resolved.get("properties")
    out: dict[str, Any] = {}
    marker = _declared_marker(resolved)
    if marker and KIND_KEY not in value:
        # FIRST key, matching ``ensure_root_marker`` and the block-shape
        # doctrine: the discriminator leads the object.
        out[KIND_KEY] = marker
    for key, item in value.items():
        child = (properties or {}).get(key) if isinstance(properties, dict) else None
        out[key] = (
            _stamp_declared_markers(item, child, root) if isinstance(child, dict) else item
        )
    return out


def _residue(extra: dict[str, Any], optional_missing: list[str]) -> dict[str, Any] | None:
    """An IrResidue, or None when every channel is empty (FE `isEmptyResidue`)."""
    if not extra and not optional_missing:
        return None
    return {
        "extra": extra or None,
        "optionalMissing": sorted(set(optional_missing)) or None,
        "notices": None,
    }


def _partition(
    value: Any,
    schema: dict[str, Any],
    root: dict[str, Any],
    path: list[str],
    node_index: dict[str, dict[str, Any]],
    collapses: list[str],
) -> Any:
    """Split `value` into a schema-clean form, routing unknowns into node_index.

    Returns the cleaned value. Residue for the ROOT node (path == []) is left
    in ``node_index[""]`` for the caller to lift onto ``root.residue``.

    ``collapses`` collects the path of every object node that had source keys
    but retained NONE of them — a parser/schema VOCABULARY MISMATCH. See
    ``_partition_value`` for why that must never be stamped.
    """
    ref_name = _ref_name(schema)
    resolved = _resolve_ref(schema, root)

    if resolved.get("type") == "array" and isinstance(value, list):
        items = resolved.get("items")
        if not isinstance(items, dict):
            return value
        return [
            _partition(item, items, root, path + [str(i)], node_index, collapses)
            for i, item in enumerate(value)
        ]

    properties = resolved.get("properties")
    if (
        resolved.get("type") == "object"
        and isinstance(value, dict)
        and isinstance(properties, dict)
    ):
        required = set(resolved.get("required") or [])
        # An OPEN object (`additionalProperties: true` or a schema) DECLARES
        # that it accepts keys it does not name — such a key is known to the
        # schema, so it belongs in `clean`, never in residue. Treating it as
        # unknown collapses the node and suppresses the whole envelope (this
        # is what silently killed every `item_presentation` stamp).
        additional = resolved.get("additionalProperties")
        open_schema: dict[str, Any] | None = (
            additional if isinstance(additional, dict) else None
        )
        accepts_unknown = additional is True or open_schema is not None

        clean: dict[str, Any] = {}
        extra: dict[str, Any] = {}
        missing: list[str] = []

        for key, item in value.items():
            prop_schema = properties.get(key)
            if not isinstance(prop_schema, dict):
                if accepts_unknown:
                    clean[key] = (
                        _partition(item, open_schema, root, path + [key], node_index, collapses)
                        if open_schema is not None
                        else item
                    )
                else:
                    extra[key] = item
                continue
            if (
                item is None
                and key not in required
                and not _allows_null(_resolve_ref(prop_schema, root))
            ):
                # Unset optional surfaced as explicit null — semantically absent.
                missing.append(key)
                continue
            clean[key] = _partition(item, prop_schema, root, path + [key], node_index, collapses)

        missing.extend(key for key in properties if key not in value)

        # Vocabulary collapse: the node kept NOTHING and at least one key was
        # unknown to the schema. An all-optional object whose fields are simply
        # unset (`extra` empty) is NOT a collapse — it legitimately renders `{}`.
        if value and not clean and extra:
            collapses.append(".".join(path) or "(root)")

        residue = _residue(extra, missing)
        if residue is not None:
            node_index[".".join(path)] = {
                "kind": ref_name,
                "kindState": "resolved" if ref_name else "raw",
                "status": "complete",
                "residue": residue,
            }
        return clean

    return value


def _partition_value(
    data: dict[str, Any], schema: dict[str, Any]
) -> tuple[dict[str, Any], dict[str, Any] | None, dict[str, dict[str, Any]], list[str]]:
    """Partition once; return (clean, root_residue, node_index, collapses).

    A COLLAPSE is an object node whose source had keys and whose schema-clean
    form has none — every key was unknown or an unset optional. It means the
    parser and the kind share no vocabulary at that node. Such an envelope can
    still be *schema-valid* (a node with no required fields validates as `{}`)
    and still *round-trip* (residue restores everything) — yet the FE renders
    from `root.value`, so it would draw an EMPTY block where its own parser
    would have drawn the real one. That is strictly worse than not stamping.
    """
    node_index: dict[str, dict[str, Any]] = {}
    collapses: list[str] = []
    clean = _partition(data, schema, schema, [], node_index, collapses)
    root_meta = node_index.pop("", None)
    root_residue = root_meta["residue"] if root_meta else None
    return clean, root_residue, node_index, collapses


def _assemble(
    clean: dict[str, Any],
    root_residue: dict[str, Any] | None,
    node_index: dict[str, dict[str, Any]],
    kind: str,
    source_text: str,
    discriminator: dict[str, Any],
) -> dict[str, Any]:
    envelope: dict[str, Any] = {
        "v": IR_VERSION,
        "engine": IR_ENGINE,
        "fingerprint": fingerprint_text(source_text),
        "root": {
            "role": "structured",
            "kind": kind,
            "kindState": "resolved",
            "discriminator": discriminator,
            "path": [],
            "status": "complete",
            "value": {**clean, KIND_KEY: kind},
            "residue": root_residue,
        },
    }
    if node_index:
        envelope["nodeIndex"] = node_index
    return envelope


# ---------------------------------------------------------------------------
# The pure assembler
# ---------------------------------------------------------------------------


def build_canonical_envelope(
    value: dict[str, Any],
    kind: str,
    *,
    source_text: str,
    discriminator: dict[str, Any],
    schema: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """Assemble a complete, resolved CanonicalBlockIR. Pure — no IO, no logging.

    Field-for-field mirror of the TS ``envelopeFromCompleteValue``, with two
    contract-mandated additions the TS one-shot path does not need:

    * ``fingerprint`` hashes ``source_text`` (the exact ``render_block.content``
      string), NOT ``JSON.stringify(value)``. That is the FE's reuse key —
      ``reuseEnvelopeIfCurrent`` compares ``fingerprintText(regionSource)``.
    * when ``schema`` is given, ``value`` is partitioned against it so the
      emitted ``value`` holds schema fields + ``__kind`` only and unknown keys
      land in ``residue`` / ``nodeIndex`` (law 3). Without a schema the value
      is wrapped verbatim with ``residue: None``, exactly like the TS twin.
    """
    if schema is None:
        return _assemble(value, None, {}, kind, source_text, discriminator)
    clean, root_residue, node_index, _collapses = _partition_value(value, schema)
    return _assemble(clean, root_residue, node_index, kind, source_text, discriminator)


# ---------------------------------------------------------------------------
# Sync kind-schema snapshot over the async catalog
# ---------------------------------------------------------------------------
#
# ``matrx_graph.kinds.get_kind`` is async (it hits the DB) but the block
# pipeline (``StreamBlockProcessor.process_token``) is sync, driven from an
# async emitter. So the schemas are snapshotted once per process and read
# synchronously. A cold snapshot means "do not stamp this block" — logged
# once, loudly — and schedules the prime so the next block is covered. In
# practice blocks complete at ``finalize()``, long after the first token
# warmed the catalog. Hosts that want zero misses can ``await
# prime_kind_catalog()`` at stream start.

_schema_snapshot: dict[str, dict[str, Any] | None] = {}
_prime_task: asyncio.Task[None] | None = None
_logged_causes: set[str] = set()


def _log_once(cause: str, message: str) -> None:
    if cause not in _logged_causes:
        _logged_causes.add(cause)
        logger.error(message)


async def prime_kind_catalog() -> None:
    """Resolve every mapped kind's schema into the sync snapshot. Idempotent."""
    from matrx_graph.kinds import get_kind

    for block_type, slug in BLOCK_KIND_MAP.items():
        if slug in _schema_snapshot:
            continue
        entry = await get_kind(slug)
        if entry is None:
            # get_kind already logged the unregistered-kind platform defect.
            _log_once(
                f"unregistered:{slug}",
                f"block envelope: kind '{slug}' (block type '{block_type}') is not "
                f"registered in content_ir.kind_definition — NO __ir envelope will "
                f"be stamped for this block type. Register the kind or remove it "
                f"from BLOCK_KIND_MAP.",
            )
            _schema_snapshot[slug] = None
            continue
        if entry.json_schema is None:
            _log_once(
                f"noschema:{slug}",
                f"block envelope: kind '{slug}' has no emitted_json_schema — NO "
                f"__ir envelope will be stamped for block type '{block_type}'.",
            )
        _schema_snapshot[slug] = entry.json_schema


def reset_kind_catalog_snapshot() -> None:
    """Drop the snapshot (registry mutation, or test isolation)."""
    global _prime_task
    _schema_snapshot.clear()
    _logged_causes.clear()
    _prime_task = None


def kind_schema(slug: str) -> dict[str, Any] | None:
    """Sync read of a mapped kind's schema. None = do not stamp."""
    global _prime_task
    if slug in _schema_snapshot:
        return _schema_snapshot[slug]

    _log_once(
        "cold-catalog",
        "block envelope: kind catalog is COLD — __ir envelope stamping is "
        "SKIPPED until it warms (blocks still render via the frontend parser). "
        "Priming now. Await prime_kind_catalog() at stream start to avoid this.",
    )
    if _prime_task is None or _prime_task.done():
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            return None  # sync context (tests) — caller injects the snapshot
        _prime_task = loop.create_task(prime_kind_catalog())
    return None


# ---------------------------------------------------------------------------
# The stamping entry point (called only for COMPLETE blocks)
# ---------------------------------------------------------------------------


def envelope_for_block(
    block_type: str,
    data: dict[str, Any] | None,
    *,
    source_text: str,
    language: str | None = None,
) -> dict[str, Any] | None:
    """Build the envelope for a COMPLETE block, or None when it must not stamp.

    The caller MUST have already established that the block is complete (law 1);
    this function does not and cannot know that.
    """
    slug = BLOCK_KIND_MAP.get(block_type)
    if slug is None:
        if block_type not in NON_ENVELOPE_BLOCK_TYPES:
            _log_once(
                f"unclassified:{block_type}",
                f"block envelope: block type '{block_type}' is in NEITHER "
                f"BLOCK_KIND_MAP nor NON_ENVELOPE_BLOCK_TYPES — an UNCLASSIFIED "
                f"envelope bypass. Classify it: map it to a registered kind, or "
                f"record the reviewed reason it gets no envelope.",
            )
        return None
    if not isinstance(data, dict) or not data or not source_text:
        return None

    schema = kind_schema(slug)
    if schema is None:
        return None

    adapted = adapt_block_data(block_type, data)
    # The schema declares what each node IS; write those markers before
    # partitioning so the discriminator is a KNOWN key (never residue) and the
    # value can satisfy its own `required: ["__kind", ...]`.
    adapted = _stamp_declared_markers(adapted, schema, schema)
    clean, root_residue, node_index, collapses = _partition_value(adapted, schema)

    if collapses:
        _log_once(
            f"collapse:{slug}",
            f"block envelope: '{block_type}' parser output shares NO vocabulary "
            f"with kind '{slug}' at node(s) {collapses[:5]} — every key there is "
            f"unknown to the schema, so the envelope's value would render EMPTY. "
            f"NO __ir envelope stamped. This is parser/kind contract drift.",
        )
        return None

    from matrx_graph.executor.schema_validation import validate_instance

    errors = validate_instance(schema, clean)
    if errors:
        _log_once(
            f"invalid:{slug}",
            f"block envelope: '{block_type}' parser output does not satisfy kind "
            f"'{slug}' emitted_json_schema even after residue partition — NO __ir "
            f"envelope stamped (the block still renders via the frontend parser). "
            f"This is a parser/kind contract drift, not user input. errors={errors[:5]}",
        )
        return None

    return _assemble(
        clean,
        root_residue,
        node_index,
        slug,
        source_text,
        discriminator_for_block(block_type, language),
    )
