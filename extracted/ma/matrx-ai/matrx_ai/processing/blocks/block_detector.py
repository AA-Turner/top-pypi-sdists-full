"""
Block boundary detection — Python port of content-splitter-v2.ts.

Detects and extracts content blocks from raw markdown text.
Operates on complete text (used by StreamBlockProcessor after accumulation).

Detection priority (same as TypeScript):
1. MATRX patterns
2. Code blocks (with JSON special types)
3. XML tag blocks
4. Images
5. Videos
6. Tables
7. Text (fallback)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any

from matrx_graph.content_ir.directives import (
    is_reserved_directive_slug,
    parse_directive_slug,
)
from matrx_graph.content_ir.envelope import KIND_KEY

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------


@dataclass
class DetectedBlock:
    """A block detected by the splitter."""

    type: str
    content: str
    language: str | None = None
    src: str | None = None
    alt: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ExtractionResult:
    content: str
    next_index: int
    metadata: dict[str, Any] = field(default_factory=dict)


# ---------------------------------------------------------------------------
# Line normalization
# ---------------------------------------------------------------------------


def normalize_line(text: str) -> str:
    """Normalize a raw line: whitespace-only lines collapse to the empty string.

    Must stay byte-for-byte equivalent to the TypeScript ``normalizeLine`` in
    ``content-splitter-v2.ts`` — the parity gate diffs the two splitters.
    """
    return "" if text.strip() == "" else text


# ---------------------------------------------------------------------------
# JSON block detection
# ---------------------------------------------------------------------------

JSON_BLOCK_PATTERNS: dict[str, dict[str, Any]] = {
    "quiz": {
        "root_key": "quiz_title",
        "validate": lambda p: bool(
            p
            and p.get("quiz_title")
            and isinstance(p.get("multiple_choice"), list)
            and len(p["multiple_choice"]) > 0
        ),
    },
    "presentation": {
        "root_key": "presentation",
        "validate": lambda p: bool(
            p
            and p.get("presentation", {}).get("slides")
            and isinstance(p["presentation"]["slides"], list)
        ),
    },
    "decision_tree": {
        "root_key": "decision_tree",
        "validate": lambda p: bool(
            p and p.get("decision_tree", {}).get("title") and p["decision_tree"].get("root")
        ),
    },
    "comparison_table": {
        "root_key": "comparison",
        "validate": lambda p: bool(
            p
            and p.get("comparison", {}).get("title")
            and isinstance(p.get("comparison", {}).get("items"), list)
            and isinstance(p.get("comparison", {}).get("criteria"), list)
        ),
    },
    "diagram": {
        "root_key": "diagram",
        "validate": lambda p: bool(
            p
            and p.get("diagram", {}).get("title")
            and isinstance(p.get("diagram", {}).get("nodes"), list)
        ),
    },
    "math_problem": {
        "root_key": "math_problem",
        "validate": lambda p: bool(p and isinstance(p.get("math_problem"), dict)),
    },
    # A clickable reference to a platform entity (agent, note, task, file, ...).
    # Deliberately forgiving: any object under the key with a string ``type``
    # qualifies -- the renderer handles unknown types via a neutral fallback.
    "item_presentation": {
        "root_key": "item_presentation",
        "validate": lambda p: bool(
            p
            and isinstance(p.get("item_presentation"), dict)
            and isinstance(p["item_presentation"].get("type"), str)
        ),
    },
    # An output-schema proposal -- what the "JSON Schema Generator" agent emits:
    # ``{ name: str, schema: object, strict?: bool }``. Deliberately strict so
    # ordinary JSON that merely begins with a "name" key never misfires.
    "schema_proposal": {
        "root_key": "name",
        "validate": lambda p: bool(
            p
            and isinstance(p.get("name"), str)
            and isinstance(p.get("schema"), dict)
        ),
    },
}

_FIRST_JSON_KEY_RE = re.compile(r'^\{\s*"([^"]+)"')


def _extract_first_json_key(content: str) -> str | None:
    m = _FIRST_JSON_KEY_RE.match(content.lstrip())
    return m.group(1) if m else None


def _is_kind_directive(parsed: Any) -> bool:
    """THE CURRENT detector — a ``matrx`` body whose ``__kind`` sits in the
    reserved Kind Directives namespace (``directive_v…``).

    This is the live gate. One discriminator, and it is the same ``__kind`` key
    every other kind instance already carries, so a directive is typed by the
    ordinary kind machinery rather than by a parallel sentinel. Spec:
    ``docs/protocol/KIND_DIRECTIVES.md``. The authoritative decoder + per-shape
    validation live host-side (``aidream/services/content_ir_directives``);
    detection only needs the namespace (matrx-ai must not import the host)."""
    if not isinstance(parsed, dict):
        return False
    return is_reserved_directive_slug(parsed.get(KIND_KEY))


def _is_legacy_matrx_shell(parsed: Any) -> bool:
    """LEGACY READ PATH ONLY — the RETIRED 4-key shell, detected by its
    ``matrx_version`` sentinel.

    🚨 This is NOT the current detector; :func:`_is_kind_directive` is. It
    exists for exactly one reason: stored conversations written before
    2026-08-23 hold ` ```matrx ` fences in the old shell and must keep
    rendering forever. Nothing in the platform EMITS this shape any more, and
    nothing may start. It is the detection-side twin of the host's read-only
    translation shim
    (``aidream/services/content_ir_directives/legacy_shell.py``), which owns
    the decode half and carries the campaign's Strictness Law clause 4
    constraints in full.

    If you are adding a new emitter: emit ``{"__kind":
    "directive_v1_<class>_<noun>", "items": [...]}`` and this function is
    irrelevant to you."""
    return isinstance(parsed, dict) and "matrx_version" in parsed


def _is_matrx_body(parsed: Any) -> bool:
    """A ``matrx`` fence body: a current Kind Directive, or a stored legacy shell."""
    return _is_kind_directive(parsed) or _is_legacy_matrx_shell(parsed)


def detect_json_block_type(content: str) -> str | None:
    trimmed = content.strip()
    if trimmed.startswith("{"):
        try:
            if _is_matrx_body(json.loads(trimmed)):
                return "matrx"
        except (json.JSONDecodeError, ValueError):
            pass  # Partial stream -- fall through to the first-key heuristic.

    first_key = _extract_first_json_key(content)
    if not first_key:
        return None

    # A partial stream. ``__kind`` first is NOT enough on its own -- every kind
    # instance leads with it -- so a directive is only claimed once the slug's
    # closing quote has arrived and it is in the reserved namespace. An
    # ordinary kind keeps routing to the ordinary kind path.
    if first_key == KIND_KEY:
        if is_reserved_directive_slug(root_kind_declaration(content)):
            return "matrx"
        return None

    if first_key == "matrx_version":  # LEGACY read path -- stored content only.
        return "matrx"

    for block_type, pattern in JSON_BLOCK_PATTERNS.items():
        if pattern["root_key"] == first_key:
            return block_type
    return None


def _build_matrx_block(content: str) -> DetectedBlock:
    """Build the block for a ```matrx fence — the CURRENT two-key Kind Directive
    shell, or a stored legacy shell.

    Exposes the already-public routing fields in metadata so a server consumer
    routes without a second parse; the frontend re-derives them itself and
    ignores the extra keys. A body that is neither shape degrades to a muted
    card so a typo can never break the stream.

    The gate is the reserved ``__kind`` namespace (see
    ``docs/protocol/KIND_DIRECTIVES.md``). The authoritative decoder + per-shape
    validation live host-side (``aidream/services/content_ir_directives``);
    detection only needs the namespace, so the check is inlined here (matrx-ai
    must not import the host)."""
    trimmed = re.sub(r"```+\s*$", "", content.strip()).strip()
    try:
        parsed = json.loads(trimmed)
    except (json.JSONDecodeError, ValueError):
        parsed = None

    if not _is_matrx_body(parsed):
        # A malformed body still renders through the directive card (a muted
        # card) -- the block type is the fence language, exactly as in TS.
        return DetectedBlock(type="matrx", content=content, language="matrx")

    items = parsed.get("items")
    metadata: dict[str, Any] = {
        "isComplete": True,
        "itemCount": len(items) if isinstance(items, list) else 0,
    }
    if _is_kind_directive(parsed):
        slug = parsed[KIND_KEY]
        metadata["directiveSlug"] = slug
        parsed_slug = parse_directive_slug(slug)
        if parsed_slug is not None:
            metadata["directiveClass"] = parsed_slug.directive_class
            metadata["noun"] = parsed_slug.noun
            metadata["capability"] = parsed_slug.capability
    else:
        # LEGACY shell -- the retired control fields, surfaced verbatim so a
        # stored fence keeps rendering. Never produced by a current emitter.
        # `matrxVersion` present IS the legacy signal; a separate `legacyShell`
        # flag would add a key the TypeScript splitter does not emit, and the
        # parity gate is right to call that a Python defect.
        metadata["matrxVersion"] = parsed.get("matrx_version")
        metadata["kind"] = parsed.get("kind")
        metadata["envelopeType"] = parsed.get("type")
    return DetectedBlock(
        type="matrx", content=content, language="matrx", metadata=metadata
    )


_PLACEHOLDER_PATTERNS = [
    re.compile(
        r"\[\s*(array|object|string|number|boolean|description|example|etc|list|item)[^\]]*\]",
        re.IGNORECASE,
    ),
    re.compile(r':\s*"?\[?(array|list) of ', re.IGNORECASE),
    re.compile(r':\s*"?object with ', re.IGNORECASE),
    re.compile(r':\s*"?<[a-z_]+>', re.IGNORECASE),
    re.compile(r':\s*"?\.\.\."?'),
]


def _contains_placeholder_text(content: str) -> bool:
    return any(p.search(content) for p in _PLACEHOLDER_PATTERNS)


def validate_json_block(content: str, block_type: str) -> dict[str, Any]:
    """Validate a JSON block and determine its streaming state."""
    trimmed = re.sub(r"```+\s*$", "", content.strip()).strip()

    if block_type == "matrx":
        try:
            if _is_matrx_body(json.loads(trimmed)):
                return {"is_complete": True, "should_show": True}
        except (json.JSONDecodeError, ValueError):
            pass  # Still streaming the two-key shell.
        first_key = _extract_first_json_key(trimmed)
        return {
            "is_complete": False,
            "should_show": (
                is_reserved_directive_slug(root_kind_declaration(trimmed))
                or first_key == "matrx_version"  # LEGACY read path.
            ),
        }

    if _contains_placeholder_text(trimmed):
        return {"is_complete": False, "should_show": False}

    # Try full parse
    try:
        parsed = json.loads(trimmed)
        pattern = JSON_BLOCK_PATTERNS[block_type]
        if pattern["validate"](parsed):
            return {"is_complete": True, "should_show": True, "metadata": {"isComplete": True}}
        return {"is_complete": True, "should_show": False, "metadata": {"isComplete": True}}
    except (json.JSONDecodeError, KeyError):
        pass

    # Brace counting
    open_braces = trimmed.count("{")
    close_braces = trimmed.count("}")

    if open_braces > close_braces:
        return {"is_complete": False, "should_show": False}
    if trimmed.endswith("}") and open_braces == close_braces:
        return {"is_complete": True, "should_show": False, "metadata": {"isComplete": True}}
    if close_braces > open_braces:
        return {"is_complete": True, "should_show": False, "metadata": {"isComplete": True}}

    return {"is_complete": False, "should_show": False}


# ---------------------------------------------------------------------------
# XML tag block detection
# ---------------------------------------------------------------------------

XML_TAG_BLOCKS: dict[str, list[str]] = {
    "thinking": ["<thinking>", "<think>"],
    "reasoning": ["<reasoning>"],
    "info": ["<info>"],
    "task": ["<task>"],
    "database": ["<database>"],
    "private": ["<private>"],
    "plan": ["<plan>"],
    "event": ["<event>"],
    "tool": ["<tool>"],
    "questionnaire": ["<questionnaire>"],
    "flashcards": ["<flashcards>"],
    "cooking_recipe": ["<cooking_recipe>"],
    "timeline": ["<timeline>"],
    "progress_tracker": ["<progress_tracker>"],
    "troubleshooting": ["<troubleshooting>"],
    "resources": ["<resources>"],
    "research": ["<research>"],
}


def detect_xml_block_type(line: str) -> tuple[str, str] | None:
    """Return (block_type, matched_tag) when line starts with a known XML block tag."""
    trimmed = line.strip()
    for block_type, tags in XML_TAG_BLOCKS.items():
        for tag in tags:
            if trimmed == tag or trimmed.startswith(tag):
                return block_type, tag
    return None


def extract_xml_block(
    block_type: str, matched_tag: str, start_index: int, lines: list[str]
) -> ExtractionResult:
    content_lines: list[str] = []
    i = start_index
    found_closing = False

    tag_name = matched_tag[1:-1]
    closing_tag = f"</{tag_name}>"

    # First line may have content after the opening tag
    first_line = lines[i]
    processed_first = normalize_line(first_line).strip()
    if processed_first.startswith(matched_tag):
        after_tag = processed_first[len(matched_tag) :]
        closing_idx = after_tag.find(closing_tag)
        if closing_idx != -1:
            before_closing = after_tag[:closing_idx].strip()
            if before_closing:
                content_lines.append(before_closing)
            remainder = after_tag[closing_idx + len(closing_tag) :].strip()
            found_closing = True
            i += 1
            if remainder:
                lines.insert(i, remainder)
            full_content = "\n".join(content_lines)
            result = _validate_streaming_xml_block(block_type, full_content, found_closing)
            return ExtractionResult(
                content=result["content"] or full_content,
                next_index=i,
                metadata=result["metadata"],
            )
        after_tag_trimmed = after_tag.strip()
        if after_tag_trimmed:
            content_lines.append(after_tag_trimmed)
        i += 1

    while i < len(lines):
        current = normalize_line(lines[i]).strip()

        if current == closing_tag:
            found_closing = True
            i += 1
            break

        # Closing tag appears inline: e.g. "---</flashcards>" or "text</flashcards><flashcards>"
        closing_idx = current.find(closing_tag)
        if closing_idx != -1:
            before_closing = current[:closing_idx].strip()
            if before_closing:
                content_lines.append(before_closing)
            remainder = current[closing_idx + len(closing_tag) :].strip()
            found_closing = True
            i += 1
            # Re-inject any text after the closing tag so the main loop
            # can detect and parse it as a new block.
            if remainder:
                lines.insert(i, remainder)
            break

        if block_type == "thinking" and current.startswith("### I have everything"):
            content_lines.append(lines[i])
            i += 1
            break

        content_lines.append(lines[i])
        i += 1

    full_content = "\n".join(content_lines)
    result = _validate_streaming_xml_block(block_type, full_content, found_closing)

    return ExtractionResult(
        content=result["content"] or full_content,
        next_index=i,
        metadata=result["metadata"],
    )


# ---------------------------------------------------------------------------
# Attribute-bearing XML block detection (e.g. <decision prompt="...">)
# ---------------------------------------------------------------------------

ATTRIBUTE_XML_BLOCKS: list[str] = [
    "decision",
    "artifact",
    # Editor pills -- round-trip representation of code-editor errors and
    # selected code snippets. Attributes carry file/line/severity/language.
    "editor_error",
    "editor_code_snippet",
    # Audio citation -- a reference to a moment in a scribe session's audio.
    # Emitted mid-sentence (handled by detect_mid_line_attribute_xml).
    "audiocite",
]

# Every tag name a recognized detector above claims. Consulted by the
# unrecognized-XML fallback so a known tag never falls through to it.
KNOWN_XML_TAG_NAMES: frozenset[str] = frozenset(
    [tag[1:-1] for tags in XML_TAG_BLOCKS.values() for tag in tags]
    + ATTRIBUTE_XML_BLOCKS
)


def detect_attribute_xml_block(line: str) -> dict[str, Any] | None:
    """
    Detect XML blocks that carry attributes, e.g. <decision prompt="Choose an option">.
    The tag must be at the start of the (trimmed) line.
    Returns a dict with 'type', 'full_opening_tag', 'attributes' or None.
    """
    trimmed = line.strip()
    for block_type in ATTRIBUTE_XML_BLOCKS:
        prefix = f"<{block_type}"
        if (
            trimmed.startswith(prefix)
            and len(trimmed) > len(prefix)
            and trimmed[len(prefix)] in (" ", ">")
        ):
            close_bracket = trimmed.find(">")
            if close_bracket == -1:
                return None
            full_opening_tag = trimmed[: close_bracket + 1]
            attributes = _parse_xml_attributes(full_opening_tag)
            return {
                "type": block_type,
                "full_opening_tag": full_opening_tag,
                "attributes": attributes,
            }
    return None


def detect_mid_line_attribute_xml(line: str) -> dict[str, Any] | None:
    """
    Detect an attribute-bearing XML tag (e.g. <decision ...> or <artifact ...>)
    that appears mid-line (not at the start of the trimmed line).
    Simple XML tags like <flashcards> are never emitted mid-sentence.

    Returns a dict with 'tag_start' (byte offset in line), 'type',
    'full_opening_tag', 'attributes', or None.
    """
    for block_type in ATTRIBUTE_XML_BLOCKS:
        prefix = f"<{block_type}"
        idx = line.find(prefix)
        if idx == -1:
            continue

        # Must NOT be at the very start of the trimmed line
        if line.lstrip().startswith(prefix):
            continue

        after_prefix = (
            line[idx + len(prefix) : idx + len(prefix) + 1]
            if (idx + len(prefix)) < len(line)
            else ""
        )
        if after_prefix not in (" ", ">"):
            continue

        close_bracket = line.find(">", idx)
        if close_bracket == -1:
            continue

        full_opening_tag = line[idx : close_bracket + 1]
        attributes = _parse_xml_attributes(full_opening_tag)
        return {
            "tag_start": idx,
            "type": block_type,
            "full_opening_tag": full_opening_tag,
            "attributes": attributes,
        }
    return None


def _parse_xml_attributes(opening_tag: str) -> dict[str, str]:
    """Extract key="value" pairs from an XML opening tag."""
    attrs: dict[str, str] = {}
    for m in re.finditer(r'(\w+)\s*=\s*"([^"]*)"', opening_tag):
        attrs[m.group(1)] = m.group(2)
    return attrs


def extract_attribute_xml_block(
    detection: dict[str, Any],
    start_index: int,
    lines: list[str],
    raw_xml_override: str | None = None,
) -> ExtractionResult:
    """
    Extract the content of an attribute-bearing XML block such as <decision ...>
    or <artifact ...>.

    Handles:
    - Block closed on same line
    - Multi-line block
    - Content immediately following the closing tag (re-injected for next iteration)

    raw_xml_override — when the opening tag was found mid-line, the caller
    passes the verbatim source text so rawXml in metadata matches exactly
    what appears in the original content string.
    """
    block_type: str = detection["type"]
    closing_tag = f"</{block_type}>"
    raw_lines: list[str] = []
    consumed_lines: list[str] = []
    i = start_index
    found_closing = False

    first_line = normalize_line(lines[i]).strip()
    consumed_lines.append(lines[i])
    after_opening = first_line[first_line.index(">") + 1 :]

    closing_idx = after_opening.find(closing_tag)
    if closing_idx != -1:
        inner = after_opening[:closing_idx].strip()
        if inner:
            raw_lines.append(inner)
        remainder = after_opening[closing_idx + len(closing_tag) :].strip()
        found_closing = True
        i += 1
        if remainder:
            lines.insert(i, remainder)
    else:
        if after_opening.strip():
            raw_lines.append(after_opening.strip())
        i += 1

        while i < len(lines):
            current = normalize_line(lines[i]).strip()
            closing_idx = current.find(closing_tag)
            if closing_idx != -1:
                before = current[:closing_idx].strip()
                if before:
                    raw_lines.append(before)
                # Track consumed lines up to and including the closing tag
                original_line = lines[i]
                original_closing_idx = original_line.find(closing_tag)
                consumed_lines.append(
                    original_line[: original_closing_idx + len(closing_tag)]
                    if original_closing_idx != -1
                    else original_line
                )
                remainder = current[closing_idx + len(closing_tag) :].strip()
                found_closing = True
                i += 1
                if remainder:
                    lines.insert(i, remainder)
                break
            consumed_lines.append(lines[i])
            raw_lines.append(lines[i])
            i += 1

    inner_content = "\n".join(raw_lines)

    # rawXml must match the exact substring in the original content so that
    # client-side replaceBlockContent(rawXml, chosenText) works correctly.
    raw_xml = raw_xml_override if raw_xml_override is not None else "\n".join(consumed_lines)

    # Type-specific metadata construction

    # Editor pill tags + audio citations -- attributes pass straight through as
    # metadata so the chip component reads file/line/severity/language (editor)
    # or start/end/session (audiocite) without re-parsing the tag.
    if block_type in ("editor_error", "editor_code_snippet", "audiocite"):
        return ExtractionResult(
            content=inner_content,
            next_index=i,
            metadata={
                "isComplete": found_closing,
                **detection["attributes"],
                "rawXml": raw_xml,
            },
        )

    if block_type == "artifact":
        artifact_id = detection["attributes"].get("id", f"artifact-{start_index}")
        # Extract numeric index from id like "artifact_1" -> 1
        artifact_index = start_index
        if "_" in artifact_id:
            try:
                artifact_index = int(artifact_id.rsplit("_", 1)[1])
            except (ValueError, IndexError):
                pass

        return ExtractionResult(
            content=inner_content,
            next_index=i,
            metadata={
                "isComplete": found_closing,
                "artifactId": artifact_id,
                "artifactIndex": artifact_index,
                "artifactType": detection["attributes"].get("type", "text"),
                "artifactTitle": detection["attributes"].get("title", ""),
                # R1: carry the version from the wire form so passthrough and
                # render read the real chain version instead of defaulting to 1.
                **(
                    {"version": int(detection["attributes"]["version"])}
                    if str(detection["attributes"].get("version", "")).lstrip("-").isdigit()
                    else {}
                ),
                "rawXml": raw_xml,
            },
        )

    # Default: decision block parsing
    # Parse <option label="...">...</option> elements
    options: list[dict[str, str]] = []
    for idx, m in enumerate(
        re.finditer(r'<option\s+label="([^"]*)">([\s\S]*?)</option>', inner_content)
    ):
        options.append(
            {
                "id": f"opt-{idx}",
                "label": m.group(1),
                "text": m.group(2).strip(),
            }
        )

    prompt = detection["attributes"].get("prompt", "Make a selection")
    decision_data = {
        "id": f"decision-{start_index}",
        "prompt": prompt,
        "options": options,
    }

    return ExtractionResult(
        content=inner_content,
        next_index=i,
        metadata={
            "isComplete": found_closing,
            "decision": decision_data,
            "rawXml": raw_xml,
        },
    )


def _validate_streaming_xml_block(
    block_type: str, content: str, found_closing: bool
) -> dict[str, Any]:
    if block_type not in ("questionnaire", "flashcards", "cooking_recipe"):
        return {"content": content, "metadata": {"isComplete": found_closing}}

    if block_type == "questionnaire":
        return _validate_questionnaire_streaming(content, found_closing)
    if block_type == "flashcards":
        return _validate_flashcard_streaming(content, found_closing)
    if block_type == "cooking_recipe":
        return _validate_recipe_streaming(content, found_closing)

    return {"content": content, "metadata": {"isComplete": found_closing}}


def _validate_questionnaire_streaming(content: str, found_closing: bool) -> dict[str, Any]:
    lines = content.split("\n")
    complete_questions: list[str] = []
    current_question: list[str] = []
    total_questions = 0

    question_re = re.compile(r"^###\s+\*\*Q\d+:|^###\s+Q\d+:|^\*\*Q\d+:")

    for line in lines:
        trimmed = line.strip()
        if question_re.match(trimmed):
            total_questions += 1
            if current_question:
                complete_questions.append("\n".join(current_question))
            current_question = [line]
        elif trimmed == "---":
            current_question.append(line)
            if len(current_question) > 1:
                complete_questions.append("\n".join(current_question))
            current_question = []
        elif current_question or trimmed:
            current_question.append(line)

    if found_closing and current_question:
        complete_questions.append("\n".join(current_question))

    content_to_release = content if found_closing else "\n\n---\n\n".join(complete_questions)

    return {
        "content": content_to_release,
        "metadata": {
            "isComplete": found_closing,
            "completeQuestionCount": len(complete_questions),
            "totalQuestions": total_questions,
            "hasPartialContent": not found_closing and len(current_question) > 0,
        },
    }


def _validate_flashcard_streaming(content: str, found_closing: bool) -> dict[str, Any]:
    lines = content.split("\n")
    complete_cards: list[str] = []
    current_card: list[str] = []
    total_cards = 0
    has_front = False
    has_back = False

    front_re = re.compile(r"^(?:Front|Question):", re.IGNORECASE)
    back_re = re.compile(r"^(?:Back|Answer):", re.IGNORECASE)

    for line in lines:
        trimmed = line.strip()
        if front_re.match(trimmed):
            if current_card and has_front and has_back:
                complete_cards.append("\n".join(current_card))
            current_card = [line]
            has_front = True
            has_back = False
            total_cards += 1
        elif back_re.match(trimmed):
            current_card.append(line)
            has_back = True
        elif trimmed == "---":
            if current_card and has_front and has_back:
                complete_cards.append("\n".join(current_card))
            current_card = []
            has_front = False
            has_back = False
        elif current_card:
            current_card.append(line)

    if found_closing and current_card and has_front and has_back:
        complete_cards.append("\n".join(current_card))

    content_to_release = content if found_closing else "\n\n---\n\n".join(complete_cards)

    return {
        "content": content_to_release,
        "metadata": {
            "isComplete": found_closing,
            "completeCardCount": len(complete_cards),
            "totalCards": total_cards,
            "hasPartialContent": not found_closing and len(current_card) > 0,
        },
    }


def _validate_recipe_streaming(content: str, found_closing: bool) -> dict[str, Any]:
    has_title = bool(re.search(r"^###\s+.+$", content, re.MULTILINE))
    has_ingredients = bool(re.search(r"####\s*Ingredients?:", content, re.IGNORECASE))
    has_instructions = bool(re.search(r"####\s*Instructions?:", content, re.IGNORECASE))

    if found_closing:
        content_to_release = content
    elif has_title and (has_ingredients or has_instructions):
        content_to_release = content
    else:
        content_to_release = ""

    return {
        "content": content_to_release,
        "metadata": {
            "isComplete": found_closing,
            "hasTitle": has_title,
            "hasIngredients": has_ingredients,
            "hasInstructions": has_instructions,
            "hasPartialContent": not found_closing and len(content) > 0,
        },
    }


# ---------------------------------------------------------------------------
# Markdown element detection
# ---------------------------------------------------------------------------

_CODE_BLOCK_RE = re.compile(r"^```(\w*)")
_TABLE_SEP_RE = re.compile(r"^\|[:\s|\-]+\|?$")
_IMAGE_STD_RE = re.compile(
    r"""^!\[(.*?)\]\((https?://[^\s)]+)(?:\s+(?:"[^"]*"|'[^']*'))?\)"""
)
_IMAGE_COUNT_RE = re.compile(
    r"""!\[(.*?)\]\((https?://[^\s)]+)(?:\s+(?:"[^"]*"|'[^']*'))?\)"""
)
_IMAGE_CUSTOM_RE = re.compile(r"\[Image URL: (https?://[^\s\]]+)\]")
_VIDEO_CUSTOM_RE = re.compile(r"\[Video URL: (https?://[^\s\]]+)\]")


def detect_code_fence(line: str) -> tuple[bool, str | None, int]:
    """Returns (is_code_block, language, opening_tick_count).

    The length of the opening backtick run is LOAD-BEARING: CommonMark closes
    the block only on a later BARE run of at least that many backticks, which
    is how a ``` block nests inside a longer ```` fence.
    """
    trimmed = line.strip()
    ticks = 0
    while ticks < len(trimmed) and trimmed[ticks] == "`":
        ticks += 1
    if ticks < 3:
        return False, None, 0
    rest = trimmed[ticks:].strip()
    lang = rest.split()[0] if rest.split() else None
    return True, lang, ticks


def detect_code_block(line: str) -> tuple[bool, str | None]:
    """Back-compat two-tuple wrapper over :func:`detect_code_fence`."""
    is_code, lang, _ticks = detect_code_fence(line)
    return is_code, lang


def _backtick_run_length(text: str, pos: int) -> int:
    n = 0
    while pos + n < len(text) and text[pos + n] == "`":
        n += 1
    return n


def _advance_json_string_state(
    line: str, start: int, in_string: bool, escaped: bool
) -> tuple[bool, bool]:
    """Advance the JSON string-literal machine across ``line[start:]``."""
    for idx in range(start, len(line)):
        ch = line[idx]
        if escaped:
            escaped = False
            continue
        if ch == "\\" and in_string:
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
    return in_string, escaped


def extract_code_block(
    start_index: int,
    lines: list[str],
    open_ticks: int = 3,
    language: str | None = None,
) -> ExtractionResult:
    """Extract code-block content starting after the opening fence.

    Mirrors the TypeScript ``extractCodeBlock``: a block closes only on a BARE
    run of >= ``open_ticks`` backticks, and inside a ```json fence a ``` that
    sits within a string literal is content, never a fence.
    """
    content_lines: list[str] = []
    i = start_index
    is_json = language == "json"
    in_string = False
    escaped = False

    while i < len(lines):
        line = lines[i]
        trimmed = line.strip()

        if trimmed.startswith("```"):
            if is_json:
                pos = line.find("```")
                inside, in_string, escaped = _json_backtick_inside_string(
                    line, pos, in_string, escaped
                )
                if inside:
                    content_lines.append(line)
                    i += 1
                    in_string, escaped = _advance_json_string_state(
                        line, pos, in_string, escaped
                    )
                    continue

            close_ticks = _backtick_run_length(trimmed, 0)
            if close_ticks >= open_ticks and trimmed[close_ticks:].strip() == "":
                break

            content_lines.append(line)
            i += 1
            if is_json:
                in_string, escaped = _advance_json_string_state(line, 0, in_string, escaped)
            continue

        backtick_idx = line.find("```")
        if backtick_idx != -1:
            if is_json:
                inside, in_string, escaped = _json_backtick_inside_string(
                    line, backtick_idx, in_string, escaped
                )
                if inside:
                    content_lines.append(line)
                    i += 1
                    in_string, escaped = _advance_json_string_state(
                        line, backtick_idx, in_string, escaped
                    )
                    continue

            close_ticks = _backtick_run_length(line, backtick_idx)
            if (
                close_ticks >= open_ticks
                and line[backtick_idx + close_ticks :].strip() == ""
            ):
                before = line[:backtick_idx]
                if before.strip():
                    content_lines.append(before)
                break

            content_lines.append(line)
            i += 1
            if is_json:
                in_string, escaped = _advance_json_string_state(line, 0, in_string, escaped)
            continue

        content_lines.append(line)
        i += 1
        if is_json:
            in_string, escaped = _advance_json_string_state(line, 0, in_string, escaped)

    return ExtractionResult(
        content="\n".join(content_lines),
        next_index=i + 1,
    )


def _json_backtick_inside_string(
    line: str, backtick_pos: int, in_string: bool, escaped: bool
) -> tuple[bool, bool, bool]:
    """Is the backtick run at ``backtick_pos`` inside a JSON string literal?"""
    for idx in range(backtick_pos):
        ch = line[idx]
        if escaped:
            escaped = False
            continue
        if ch == "\\" and in_string:
            escaped = True
            continue
        if ch == '"':
            in_string = not in_string
    return in_string, in_string, escaped


# Block types whose WHOLE container already resolves through a registered
# kind_surface. Their outer kind owns nested composition; exploding a child
# would destroy the canonical parent instance. Generic prose/code/XML and raw
# deliverable blocks remain eligible for embedded-kind recovery.
_ROOT_KIND_BLOCK_TYPES = frozenset(
    {
        *JSON_BLOCK_PATTERNS.keys(),
        "transcript",
        "tasks",
        "structured_info",
        "questionnaire",
        "flashcards",
        "cooking_recipe",
        "mermaid",
        "timeline",
        "progress_tracker",
        "troubleshooting",
        "resources",
        "research",
        "artifact",
    }
)


def _matching_json_object_end(source: str, start: int) -> int | None:
    """Exclusive end of one balanced JSON object candidate, or ``None``.

    This is the Python twin of frontend ``embedded-kind-json.ts``. The OUTER
    syntax is irrelevant; only JSON string/escape and object/array balance are
    interpreted.
    """
    if start >= len(source) or source[start] != "{":
        return None
    stack = ["{"]
    in_string = False
    escaped = False
    for index in range(start + 1, len(source)):
        char = source[index]
        if in_string:
            if escaped:
                escaped = False
            elif char == "\\":
                escaped = True
            elif char == '"':
                in_string = False
            continue
        if char == '"':
            in_string = True
            continue
        if char in "{[":
            stack.append(char)
            continue
        if char not in "}]":
            continue
        opening = stack.pop()
        if (char == "}" and opening != "{") or (char == "]" and opening != "["):
            return None
        if not stack:
            return index + 1
    return None


_ROOT_KIND_OPEN_RE = re.compile(r'^\s*\{\s*"(?P<key>[^"\\]*)"\s*:\s*"(?P<value>[^"\\]*)"')


def root_kind_declaration(source: str) -> str | None:
    """The kind an UNFENCED root JSON document declares on its FIRST key.

    PRE-RECOGNITION, and the "first key" part is the whole point. An agent
    bound to a kind via ``response_format_for_kind`` streams a bare JSON
    document with no fence and no XML tag, so the detector types the region
    ``text``/``code`` and — until this existed — announced no kind at all: the
    user watched raw JSON accumulate and then snap into a component
    (Arman, 2026-08-21). Reading only the first key means the announcement
    lands on the first ~30 characters of the answer rather than at its close,
    which is what makes a kind-specific loading state possible AT ALL.

    Deliberately strict, because a wrong announcement is worse than a late one:

    * the document must OPEN the buffer (leading whitespace only) — an object
      further inside prose is the embedded-recovery path, not this one;
    * ``__kind`` must be the FIRST key. A ``__kind`` arriving later is not
      pre-recognition, and honouring it here would announce a kind after the
      user has already watched the raw text;
    * the slug's CLOSING quote must have arrived, so a half-streamed
      ``"flash`` never announces ``flashcard_set``'s neighbour.

    Returns the slug, or None. Never raises — a partial that cannot be
    recognized is the ordinary early-stream state.
    """
    match = _ROOT_KIND_OPEN_RE.match(source or "")
    if match is None:
        return None
    if match.group("key") != KIND_KEY:
        return None
    slug = match.group("value").strip()
    return slug or None


def _embedded_kind_json_regions(source: str) -> list[tuple[int, int, str]]:
    """Outermost complete objects directly declaring non-empty ``__kind``."""
    regions: list[tuple[int, int, str]] = []
    start = 0
    while start < len(source):
        if source[start] != "{":
            start += 1
            continue
        end = _matching_json_object_end(source, start)
        if end is None:
            start += 1
            continue
        candidate = source[start:end]
        try:
            parsed = json.loads(candidate)
        except (json.JSONDecodeError, ValueError):
            start += 1
            continue
        kind = parsed.get("__kind") if isinstance(parsed, dict) else None
        if not isinstance(kind, str) or not kind.strip():
            start += 1
            continue
        regions.append((start, end, kind))
        start = end
    return regions


def _recover_embedded_kind_json_blocks(
    blocks: list[DetectedBlock],
) -> list[DetectedBlock]:
    """Losslessly promote embedded self-described objects to JSON blocks."""
    recovered: list[DetectedBlock] = []
    for block in blocks:
        if block.type in _ROOT_KIND_BLOCK_TYPES:
            recovered.append(block)
            continue
        regions = _embedded_kind_json_regions(block.content)
        if not regions:
            recovered.append(block)
            continue
        cursor = 0
        for start, end, _kind in regions:
            if start > cursor:
                recovered.append(
                    DetectedBlock(
                        type=block.type,
                        content=block.content[cursor:start],
                        language=block.language,
                        src=block.src,
                        alt=block.alt,
                    )
                )
            recovered.append(
                DetectedBlock(
                    type="code",
                    content=block.content[start:end],
                    language="json",
                )
            )
            cursor = end
        if cursor < len(block.content):
            recovered.append(
                DetectedBlock(
                    type=block.type,
                    content=block.content[cursor:],
                    language=block.language,
                    src=block.src,
                    alt=block.alt,
                )
            )
    return recovered


def detect_table_row(line: str) -> bool:
    trimmed = normalize_line(line).strip()
    return trimmed.startswith("|") and "|" in trimmed[1:]


def _is_table_separator(line: str) -> bool:
    trimmed = normalize_line(line).strip()
    return bool(_TABLE_SEP_RE.match(trimmed))


def extract_table(start_index: int, lines: list[str]) -> ExtractionResult:
    table_lines = [lines[start_index]]
    i = start_index + 1

    while i < len(lines) and detect_table_row(lines[i]):
        table_lines.append(lines[i])
        i += 1

    if len(table_lines) < 2 or not _is_table_separator(table_lines[1]):
        return ExtractionResult(content="", next_index=start_index + 1, metadata={"isValid": False})

    table_has_ended = i < len(lines)
    content = "\n".join(table_lines)

    # Table completion analysis
    data_lines = table_lines[2:]
    complete_count = len(data_lines) if table_has_ended else max(0, len(data_lines) - 1)
    has_partial = not table_has_ended and len(data_lines) > 0

    return ExtractionResult(
        content=content,
        next_index=i,
        metadata={
            "isComplete": table_has_ended or not has_partial,
            "completeRowCount": complete_count,
            "totalRows": len(data_lines),
            "hasPartialContent": has_partial,
        },
    )


def detect_image(line: str) -> tuple[bool, str | None, str | None]:
    """Returns (is_image, src, alt)."""
    trimmed = line.strip()
    m = _IMAGE_STD_RE.match(trimmed)
    if m:
        return True, m.group(2), m.group(1)
    m = _IMAGE_CUSTOM_RE.search(trimmed)
    if m:
        return True, m.group(1), "Image"
    return False, None, None


def count_inline_images(line: str) -> int:
    """Count standalone markdown images on ONE line.

    Drives the standalone-block-vs-inline-flow decision: exactly ONE image
    becomes a full-width ``image`` block; 2+ stay text so the markdown renderer
    lays them out side by side (respect the missing line break).
    """
    return len(_IMAGE_COUNT_RE.findall(line))


def detect_video(line: str) -> tuple[bool, str | None, str | None]:
    """Returns (is_video, src, alt)."""
    trimmed = line.strip()
    m = _VIDEO_CUSTOM_RE.search(trimmed)
    if m:
        return True, m.group(1), "Video"
    return False, None, None




# ---------------------------------------------------------------------------
# Unrecognized XML fallback (TS step 3c)
# ---------------------------------------------------------------------------

# Raw HTML tags the markdown renderer sanitizes and renders itself -- they must
# NOT be captured as XML blocks. Mirrors ALLOWED_RAW_HTML_TAGS in
# components/mardown-display/chat-markdown/rehypeSafeRawHtml.ts.
ALLOWED_RAW_HTML_TAGS: frozenset[str] = frozenset(
    {
        "img", "a", "br", "hr",
        "span", "p", "strong", "b", "em", "i", "u", "s", "del", "ins",
        "sup", "sub", "mark", "kbd", "abbr", "small", "code", "pre",
        "ul", "ol", "li", "blockquote",
        "h1", "h2", "h3", "h4", "h5", "h6",
        "table", "thead", "tbody", "tfoot", "tr", "th", "td", "caption",
        "col", "colgroup",
        "div", "figure", "figcaption", "details", "summary", "dl", "dt", "dd",
    }
)

_STRICT_XML_TAG_RE = re.compile(
    r"""<(/?)([A-Za-z][\w.-]*)(?:\s+(?:[\w.-]+\s*=\s*(?:"[^"]*"|'[^']*')\s*)*)?(/?)>"""
)

_XML_OPENING_RE = re.compile(
    r"""^<([A-Za-z][\w.-]*)(?:\s+(?:[\w.-]+\s*=\s*(?:"[^"]*"|'[^']*')\s*)*)?(/?)>"""
)


def extract_unrecognized_xml_block(
    start_index: int, lines: list[str]
) -> ExtractionResult | None:
    """Extract a COMPLETE, unrecognized XML element so it reuses the enhanced
    XML renderer (a ```xml code block).

    Runs after every recognized XML detector. Requires a line-leading, BALANCED
    root element (or a self-closing one), which keeps inline angle-bracket prose
    and mid-stream partial text on the markdown path. Curated raw HTML stays on
    its sanitized HTML path.
    """
    first_line = normalize_line(lines[start_index])
    first_trimmed = first_line.lstrip()
    opening = _XML_OPENING_RE.match(first_trimmed)
    if not opening:
        return None

    root_tag = opening.group(1)
    if root_tag in KNOWN_XML_TAG_NAMES or root_tag.lower() in ALLOWED_RAW_HTML_TAGS:
        return None

    root_start = len(first_line) - len(first_trimmed)
    depth = 0
    saw_root = False

    for line_index in range(start_index, len(lines)):
        current_line = normalize_line(lines[line_index])
        scan_from = root_start if line_index == start_index else 0

        for tag_match in _STRICT_XML_TAG_RE.finditer(current_line, scan_from):
            if tag_match.group(2) != root_tag:
                continue

            is_closing = tag_match.group(1) == "/"
            is_self_closing = tag_match.group(3) == "/"
            if is_closing:
                depth -= 1
            else:
                saw_root = True
                if not is_self_closing:
                    depth += 1

            if not saw_root or depth != 0:
                continue

            root_end = tag_match.end()
            if line_index == start_index:
                content_lines = [current_line[root_start:root_end]]
            else:
                content_lines = [
                    first_line[root_start:],
                    *[normalize_line(x) for x in lines[start_index + 1 : line_index]],
                    current_line[:root_end],
                ]
            remainder = current_line[root_end:].strip()
            if remainder:
                lines.insert(line_index + 1, remainder)

            return ExtractionResult(
                content="\n".join(content_lines).strip(),
                next_index=line_index + 1,
                metadata={"isComplete": True},
            )

    return None


# ---------------------------------------------------------------------------
# Orphan thinking-family closing tag (TS step 3d)
# ---------------------------------------------------------------------------

_ORPHAN_CLOSERS: list[tuple[str, str]] = [
    ("thinking", "</thinking>"),
    ("thinking", "</think>"),
    ("reasoning", "</reasoning>"),
]


def detect_orphan_thinking_close(trimmed_line: str) -> dict[str, str] | None:
    """Detect an ORPHAN closing tag of the thinking family -- a closer with no
    opener earlier in this content. That shape is the continuation half of a
    region a mid-region tool call split across two persisted parts: everything
    before the closer IS region body, and the literal tag must never leak to the
    user as text. Restricted to the thinking family (the misfire risk of prose
    quoting the tag is accepted; leaking the raw tag was strictly worse).
    """
    for kind, closer in _ORPHAN_CLOSERS:
        idx = trimmed_line.find(closer)
        if idx == -1:
            continue
        return {
            "type": kind,
            "before": trimmed_line[:idx].strip(),
            "remainder": trimmed_line[idx + len(closer) :].strip(),
        }
    return None


# ---------------------------------------------------------------------------
# YouTube / audio / our-own-file link detection (TS steps 3.9, 4.6, 4.7)
# ---------------------------------------------------------------------------

_YOUTUBE_ID_RE = re.compile(r"^[A-Za-z0-9_-]{11}$")
_YT_PATH_RE = re.compile(r"^/(?:embed|shorts|v|live)/([^/?#]+)")


def _parse_youtube_start(value: str | None) -> int | None:
    if not value:
        return None
    v = value.strip()
    if v.isdigit():
        return int(v)
    m = re.fullmatch(r"(?:(\d+)h)?(?:(\d+)m)?(?:(\d+)s)?", v, re.IGNORECASE)
    if not m or not any(m.groups()):
        return None
    h, mnt, sec = (int(g) if g else 0 for g in m.groups())
    return h * 3600 + mnt * 60 + sec


def parse_youtube_url(url: str) -> dict[str, Any] | None:
    """Port of lib/media/youtube.ts::parseYouTubeUrl."""
    from urllib.parse import parse_qs, urlparse

    try:
        u = urlparse(url.strip())
    except ValueError:
        return None
    if not u.scheme or not u.netloc:
        return None
    host = u.hostname.lower().removeprefix("www.") if u.hostname else ""

    video_id: str | None = None
    if host == "youtu.be":
        segs = [x for x in u.path.split("/") if x]
        video_id = segs[0] if segs else None
    elif host.endswith("youtube.com") or host == "youtube-nocookie.com":
        if u.path == "/watch":
            video_id = (parse_qs(u.query).get("v") or [None])[0]
        else:
            m = _YT_PATH_RE.match(u.path)
            video_id = m.group(1) if m else None

    if not video_id or not _YOUTUBE_ID_RE.match(video_id):
        return None

    q = parse_qs(u.query)
    hash_t = re.search(r"[#&]?t=([^&]+)", u.fragment) if u.fragment else None
    start = (
        _parse_youtube_start((q.get("start") or [None])[0])
        or _parse_youtube_start((q.get("t") or [None])[0])
        or _parse_youtube_start(hash_t.group(1) if hash_t else None)
    )
    return {"videoId": video_id, "start": start}


def youtube_watch_url(video_id: str, start: int | None) -> str:
    base = f"https://www.youtube.com/watch?v={video_id}"
    return f"{base}&t={start}s" if start and start > 0 else base


def is_youtube_thumbnail_url(url: str) -> bool:
    return bool(re.search(r"^https?://i\.ytimg\.com/vi/", url.strip(), re.IGNORECASE))


_LINKED_THUMB_RE = re.compile(
    r"^\[!\[(.*?)\]\((https?://[^\s)]+?)\)\]\((https?://[^\s)]+?)\)$"
)
_PLAIN_LINK_RE = re.compile(r"^\[([^\]]*)\]\((https?://[^\s)]+?)\)$")
_BARE_URL_RE = re.compile(r"^https?://\S+$")


def detect_youtube_markdown(line: str) -> dict[str, Any] | None:
    """Detect a standalone YouTube link (linked thumbnail / markdown link /
    bare URL) that is the WHOLE line, so an inline mention stays text."""
    trimmed = line.strip()

    m = _LINKED_THUMB_RE.match(trimmed)
    if m:
        parsed = parse_youtube_url(m.group(3))
        if parsed:
            return {
                "videoId": parsed["videoId"],
                "start": parsed["start"],
                "title": m.group(1) or None,
                "poster": m.group(2) if is_youtube_thumbnail_url(m.group(2)) else None,
                "watchUrl": youtube_watch_url(parsed["videoId"], parsed["start"]),
            }

    m = _PLAIN_LINK_RE.match(trimmed)
    if m:
        parsed = parse_youtube_url(m.group(2))
        if parsed:
            return {
                "videoId": parsed["videoId"],
                "start": parsed["start"],
                "title": m.group(1) or None,
                "poster": None,
                "watchUrl": youtube_watch_url(parsed["videoId"], parsed["start"]),
            }

    if _BARE_URL_RE.match(trimmed):
        parsed = parse_youtube_url(trimmed)
        if parsed:
            return {
                "videoId": parsed["videoId"],
                "start": parsed["start"],
                "title": None,
                "poster": None,
                "watchUrl": youtube_watch_url(parsed["videoId"], parsed["start"]),
            }
    return None


# Audio extensions recognized when a bare/markdown link points at a clip. The
# optional ?query tail keeps signed S3 URLs matching. Mirrors AUDIO_URL_EXT.
_AUDIO_URL_EXT = re.compile(
    r"\.(mp3|wav|m4a|aac|ogg|oga|opus|flac|weba|webm)(\?[^\s)]*)?$", re.IGNORECASE
)
_AUDIO_CUSTOM_RE = re.compile(r"\[Audio URL:\s*(https?://[^\s\]]+)\]")
_AUDIO_LINK_RE = re.compile(r"^!?\[(.*?)\]\((https?://[^\s)]+)\)$")


def extract_audio_link(line: str) -> tuple[str, str] | None:
    """Returns (src, alt) for a line that IS an audio link. Three shapes:
    ``[Audio URL: ...]``, a whole-line markdown link to an audio file, or a
    bare audio URL on its own line."""
    trimmed = line.strip()

    m = _AUDIO_CUSTOM_RE.search(trimmed)
    if m:
        return m.group(1), "Audio"

    m = _AUDIO_LINK_RE.match(trimmed)
    if m and _AUDIO_URL_EXT.search(m.group(2)):
        return m.group(2), (m.group(1) or "Audio")

    if re.fullmatch(r"https?://[^\s)]+", trimmed) and _AUDIO_URL_EXT.search(trimmed):
        return trimmed, "Audio"

    return None


# The cheap substring pre-gate that identifies a URL as ours. Mirrors
# OUR_FILE_URL_MARKERS in lib/media/our-file-sources.ts.
OUR_FILE_URL_MARKERS: tuple[str, ...] = (
    "matrx-user-files.s3",
    "cdn.matrxserver",
    "/podcast-assets/",
    "/share/",
)

_UUID_RE = re.compile(
    r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE
)
_S3_HOST_RE = re.compile(r"(^|\.)matrx-user-files\.s3|s3[.-].*amazonaws\.com", re.IGNORECASE)
_CDN_HOST_RE = re.compile(r"(^|\.)cdn\.matrxserver\.com$", re.IGNORECASE)
_SHARE_PATH_RE = re.compile(r"/share/[^/]+(/download)?$", re.IGNORECASE)


def might_be_our_file_url(text: str) -> bool:
    return any(marker in text for marker in OUR_FILE_URL_MARKERS)


def recognize_our_file_url(url: str) -> bool:
    """Is this URL one of OUR files? Mirrors recognizeOurFileUrl's ORIGIN tests
    (identity recovery is a client-side concern; detection only needs yes/no)."""
    from urllib.parse import urlparse

    if not might_be_our_file_url(url):
        return False
    try:
        u = urlparse(url)
    except ValueError:
        return False
    host = u.hostname or ""

    if _S3_HOST_RE.search(host):
        segs = [x for x in u.path.split("/") if x]
        candidate = segs[1] if len(segs) > 1 else (segs[-1] if segs else "")
        if candidate and _UUID_RE.match(candidate):
            return True
    if _CDN_HOST_RE.search(host):
        return True
    if _SHARE_PATH_RE.search(u.path):
        return True
    return False


_EMPHASIS_END_RE = re.compile(r"(?:\*\*|\*|_){1,2}\s*$")
_EMPHASIS_START_RE = re.compile(r"^\s*(?:\*\*|\*|_){1,2}")
_MD_LINK_RE = re.compile(r"!?\[([^\]]*)\]\((https?://[^\s)]+)\)")
_ANY_URL_RE = re.compile(r"(https?://[^\s)]+)")


def detect_matrx_file_markdown(line: str) -> dict[str, Any] | None:
    """Detect a link (or bare URL) to one of OUR OWN files anywhere in a line.

    Returns the text BEFORE (``pre``) and AFTER (``post``) the file token so a
    renderer can do ``markdown(pre) -> inline file -> markdown(post)`` without
    shattering the paragraph. Returns the FIRST our-file match on the line.
    """
    if not might_be_our_file_url(line):
        return None

    for m in _MD_LINK_RE.finditer(line):
        url = m.group(2)
        if recognize_our_file_url(url):
            return {
                "url": url,
                "label": m.group(1) or "",
                "pre": _EMPHASIS_END_RE.sub("", line[: m.start()]),
                "post": _EMPHASIS_START_RE.sub("", line[m.end() :]),
            }

    for m in _ANY_URL_RE.finditer(line):
        url = re.sub(r"[).,;]+$", "", m.group(1))
        if recognize_our_file_url(url):
            return {
                "url": url,
                "label": "",
                "pre": _EMPHASIS_END_RE.sub("", line[: m.start()]),
                "post": _EMPHASIS_START_RE.sub("", line[m.start() + len(url) :]),
            }

    return None


# ---------------------------------------------------------------------------
# Tree diagrams + custom dividers (TS steps 5.7, 1b)
# ---------------------------------------------------------------------------

_TREE_CHARS_RE = re.compile(r"[├└│┌┐┘┬┴┤┼─]")
_ASCII_TREE_RE = re.compile(r"^[\s│|]*[├└+|][\s─\-]+")
_HEADING_RE = re.compile(r"^#{1,6}\s")
ACCENT_DIVIDER_RE = re.compile(r"^\*\s*\*\s*\*\s*$")
HEAVY_DIVIDER_RE = re.compile(r"^#\s*={3,}\s*$")


def is_tree_line(line: str) -> bool:
    if not line:
        return False
    return bool(_TREE_CHARS_RE.search(line) or _ASCII_TREE_RE.match(line))


def _is_markdown_heading_line(line: str) -> bool:
    return bool(_HEADING_RE.match(line.strip()))


def find_tree_block_start(lines: list[str], first_tree_index: int) -> int:
    """Root label lines sit directly above connector lines and carry no glyphs."""
    start = first_tree_index
    for j in range(first_tree_index - 1, -1, -1):
        trimmed = normalize_line(lines[j]).strip()
        if not trimmed or is_tree_line(trimmed) or _is_markdown_heading_line(trimmed):
            break
        start = j
    return start


def _strip_accumulated_lines_from_text(
    text: str, raw_lines: list[str], from_index: int, to_index: int
) -> str:
    result = text
    for j in range(from_index, to_index):
        processed = normalize_line(raw_lines[j])
        if result.endswith(processed + "\n"):
            result = result[: -(len(processed) + 1)]
        elif processed and result.endswith(processed):
            result = result[: -len(processed)]
    return result


# ---------------------------------------------------------------------------
# Main splitter — Python port of splitContentIntoBlocksV2
# ---------------------------------------------------------------------------

# Fence languages that promote to a first-class block type (the fence language
# becomes the block type). Mirrors SPECIAL_CODE_LANGUAGES in
# content-splitter-v2.ts -- keep the two in lockstep.
SPECIAL_CODE_LANGUAGES = {
    "transcript",
    "tasks",
    "structured_info",
    "questionnaire",
    "flashcards",
    "cooking_recipe",
    "mermaid",
    "svg",
    "chart",
    "map",
    "stats",
    "diff",
    # html + react are DELIVERABLES (a webpage / a live component), not
    # throwaway snippets -- promoted so they materialize into artifacts.
    "html",
    "react",
    # A ```matrx fence carries one Matrx Envelope (reference / secret /
    # directive / validation).
    "matrx",
}

# Fence-language aliases that normalize to a canonical special language.
# Kept OUT of SPECIAL_CODE_LANGUAGES so the integrity check never sees a
# phantom block type. Mirrored client-side in content-splitter-v2.ts.
CODE_LANGUAGE_ALIASES: dict[str, str] = {
    "mmd": "mermaid",
    # jsx/tsx render + materialize as a live React component (same as ```react).
    "jsx": "react",
    "tsx": "react",
}


def normalize_code_language(language: str | None) -> str | None:
    if not language:
        return language
    lower = language.lower()
    return CODE_LANGUAGE_ALIASES.get(lower, lower)


# Every block type ``split_content_into_blocks`` can emit that is NOT already
# named by XML_TAG_BLOCKS / ATTRIBUTE_XML_BLOCKS / JSON_BLOCK_PATTERNS /
# SPECIAL_CODE_LANGUAGES. Without this the envelope-classification guard cannot
# see splitter-only types (tree, youtube, audio, matrx_file, the dividers) and a
# new one would slip past unclassified. Keep in lockstep with the main loop.
SPLITTER_ONLY_BLOCK_TYPES: frozenset[str] = frozenset(
    {
        "text",
        "code",
        "image",
        "video",
        "audio",
        "youtube",
        "matrx_file",
        "table",
        "tree",
        "accent-divider",
        "heavy-divider",
    }
)


def split_content_into_blocks(md_content: str) -> list[DetectedBlock]:
    """
    Split markdown content into typed blocks.

    Direct port of TypeScript splitContentIntoBlocksV2.
    """
    blocks: list[DetectedBlock] = []
    lines = re.split(r"\r?\n", md_content)
    current_text = ""
    i = 0

    # Keyed by the synthetic tagAndRest string that was spliced into `lines`.
    # Consumed once by step 3a so extract_attribute_xml_block gets the correct rawXml.
    pending_raw_xml_overrides: dict[str, str] = {}

    def flush_text() -> None:
        nonlocal current_text
        if current_text.strip():
            blocks.append(DetectedBlock(type="text", content=current_text.rstrip()))
            current_text = ""

    while i < len(lines):
        line = lines[i]
        processed_line = normalize_line(line)
        trimmed_line = processed_line.strip()

        # 1b. Custom divider variants, before they get absorbed as text.
        #     *** = accent divider, #=== = heavy divider. Standard --- is left
        #     for the markdown renderer to handle inside text blocks.
        if ACCENT_DIVIDER_RE.match(trimmed_line):
            flush_text()
            blocks.append(DetectedBlock(type="accent-divider", content=trimmed_line))
            i += 1
            continue
        if HEAVY_DIVIDER_RE.match(trimmed_line):
            flush_text()
            blocks.append(DetectedBlock(type="heavy-divider", content=trimmed_line))
            i += 1
            continue

        # 2. Code block
        is_code, language, open_ticks = detect_code_fence(processed_line)
        if is_code:
            flush_text()
            extraction = extract_code_block(i + 1, lines, open_ticks, language)

            normalized_language = normalize_code_language(language)
            if normalized_language == "matrx":
                # A ```matrx fence carries exactly one Matrx Envelope (the
                # in-content embedding for references and inline envelopes).
                blocks.append(_build_matrx_block(extraction.content))
            elif normalized_language and normalized_language in SPECIAL_CODE_LANGUAGES:
                blocks.append(
                    DetectedBlock(
                        type=normalized_language, content=extraction.content, language=language
                    )
                )
            elif language == "json":
                json_type = detect_json_block_type(extraction.content)
                if json_type:
                    state = validate_json_block(extraction.content, json_type)
                    blocks.append(
                        DetectedBlock(
                            type=json_type,
                            content=extraction.content,
                            language="json",
                            metadata=state.get("metadata", {}),
                        )
                    )
                else:
                    blocks.append(
                        DetectedBlock(type="code", content=extraction.content, language=language)
                    )
            else:
                blocks.append(
                    DetectedBlock(type="code", content=extraction.content, language=language)
                )

            i = extraction.next_index
            continue

        # 3a. Attribute-bearing XML tag block at line start (e.g. <decision prompt="...">)
        attr_xml = detect_attribute_xml_block(processed_line)
        if attr_xml:
            flush_text()
            # If this line was produced by a mid-line split (step 5.5), consume
            # the pre-computed rawXml override so replaceBlockContent works correctly.
            raw_xml_override = pending_raw_xml_overrides.pop(trimmed_line, None)
            extraction = extract_attribute_xml_block(attr_xml, i, lines, raw_xml_override)
            blocks.append(
                DetectedBlock(
                    type=attr_xml["type"],
                    content=extraction.content,
                    metadata=extraction.metadata,
                )
            )
            i = extraction.next_index
            continue

        # 3b. Simple XML tag block
        xml_match = detect_xml_block_type(processed_line)
        if xml_match:
            xml_type, matched_tag = xml_match
            flush_text()
            extraction = extract_xml_block(xml_type, matched_tag, i, lines)
            blocks.append(
                DetectedBlock(
                    type=xml_type,
                    content=extraction.content,
                    metadata=extraction.metadata,
                )
            )
            i = extraction.next_index
            continue

        # 3c. Complete, unrecognized XML falls back to the enhanced XML code
        #     renderer. Recognized XML detectors above retain first refusal.
        unrecognized_xml = extract_unrecognized_xml_block(i, lines)
        if unrecognized_xml is not None:
            flush_text()
            blocks.append(
                DetectedBlock(
                    type="code",
                    content=unrecognized_xml.content,
                    language="xml",
                    metadata=unrecognized_xml.metadata,
                )
            )
            i = unrecognized_xml.next_index
            continue

        # 3d. Orphan closing tag (thinking family) — the continuation half of a
        #     region split across parts by a mid-region tool call. The literal
        #     tag must never leak to the user as text.
        orphan_close = detect_orphan_thinking_close(trimmed_line)
        if orphan_close:
            # Mid-line opener rescue: `Some prose <thinking>` never matches the
            # line-start detector (3b), so the region's OPENER may sit inside
            # the accumulated text. Split there.
            openers = (
                ["<thinking>", "<think>"]
                if orphan_close["type"] == "thinking"
                else ["<reasoning>"]
            )
            opener_idx = -1
            opener_len = 0
            for opener in openers:
                idx = current_text.rfind(opener)
                if idx > opener_idx:
                    opener_idx = idx
                    opener_len = len(opener)
            region_text = current_text
            if opener_idx >= 0:
                prose_before = current_text[:opener_idx]
                region_text = current_text[opener_idx + opener_len :]
                if prose_before.strip():
                    blocks.append(
                        DetectedBlock(type="text", content=prose_before.rstrip())
                    )
            current_text = ""

            body = "\n".join(
                x for x in (region_text.strip(), orphan_close["before"]) if x
            )
            if body:
                blocks.append(
                    DetectedBlock(
                        type=orphan_close["type"],
                        content=body,
                        metadata={"isComplete": True, "continuation": True},
                    )
                )
            if orphan_close["remainder"]:
                lines.insert(i + 1, orphan_close["remainder"])
            i += 1
            continue

        # 3.9. YouTube BEFORE images — a linked thumbnail must become a playable
        #      embed, not the image its thumbnail points at.
        youtube = detect_youtube_markdown(line)
        if youtube:
            flush_text()
            blocks.append(
                DetectedBlock(
                    type="youtube",
                    # Keep the original line as content so the DB round-trip
                    # re-detects it on reload.
                    content=trimmed_line,
                    src=youtube["watchUrl"],
                    # Absent-vs-null parity: JSON.stringify DROPS undefined
                    # keys, so an unset optional must be absent here too.
                    metadata={
                        k: v
                        for k, v in (
                            ("videoId", youtube["videoId"]),
                            ("start", youtube["start"]),
                            ("title", youtube["title"]),
                            ("poster", youtube["poster"]),
                        )
                        if v is not None
                    },
                )
            )
            i += 1
            continue

        # 4. Image. Only a SINGLE image on the line becomes a standalone
        #    full-width block; 2+ fall through to text so they lay out inline.
        is_img, src, alt = detect_image(line)
        if is_img and count_inline_images(line) < 2:
            flush_text()
            blocks.append(DetectedBlock(type="image", content=trimmed_line, src=src, alt=alt))
            i += 1
            continue

        # 4.5. Video
        is_vid, src, alt = detect_video(line)
        if is_vid:
            flush_text()
            blocks.append(DetectedBlock(type="video", content=trimmed_line, src=src, alt=alt))
            i += 1
            continue

        # 4.6. Audio link (the streaming twin of the server audio_output block)
        audio = extract_audio_link(line)
        if audio:
            flush_text()
            blocks.append(
                DetectedBlock(
                    type="audio", content=trimmed_line, src=audio[0], alt=audio[1]
                )
            )
            i += 1
            continue

        # 4.7. A link to one of OUR OWN files. Runs AFTER image/video/audio so
        #      media with a richer home takes that path first, and BEFORE the
        #      table/text fallbacks so a plain [label](our-url) isn't swallowed.
        matrx_file = detect_matrx_file_markdown(line)
        if matrx_file:
            flush_text()
            blocks.append(
                DetectedBlock(
                    type="matrx_file",
                    content=trimmed_line,
                    src=matrx_file["url"],
                    alt=matrx_file["label"],
                    metadata={
                        "pre": matrx_file["pre"],
                        "post": matrx_file["post"],
                        "label": matrx_file["label"],
                    },
                )
            )
            i += 1
            continue

        # 5. Table
        if detect_table_row(line):
            flush_text()
            extraction = extract_table(i, lines)
            if extraction.metadata.get("isValid") is not False:
                blocks.append(
                    DetectedBlock(
                        type="table",
                        content=extraction.content,
                        metadata=extraction.metadata,
                    )
                )
                i = extraction.next_index
            else:
                current_text += processed_line + "\n"
                i += 1
            continue

        # 5.6. Bare JSON objects (no ``` fences) — a model that outputs
        #      { "key": ... } directly. Only triggers on lines starting with
        #      `{`; code/XML/table steps above already consumed their own.
        if trimmed_line.startswith("{"):
            json_lines = [processed_line]
            open_count = trimmed_line.count("{")
            close_count = trimmed_line.count("}")
            j = i + 1
            while j < len(lines) and open_count > close_count:
                next_line = normalize_line(lines[j])
                json_lines.append(next_line)
                open_count += next_line.count("{")
                close_count += next_line.count("}")
                j += 1

            if open_count == close_count and open_count > 0:
                json_content = "\n".join(json_lines).strip()
                parsed_ok = False
                try:
                    parsed_bare = json.loads(json_content)
                    parsed_ok = isinstance(parsed_bare, dict | list)
                except (json.JSONDecodeError, ValueError):
                    parsed_ok = False

                if parsed_ok:
                    flush_text()
                    json_type = detect_json_block_type(json_content)
                    if json_type:
                        state = validate_json_block(json_content, json_type)
                        blocks.append(
                            DetectedBlock(
                                type=json_type,
                                content=json_content,
                                language="json",
                                metadata=state.get("metadata", {}),
                            )
                        )
                    else:
                        blocks.append(
                            DetectedBlock(
                                type="code", content=json_content, language="json"
                            )
                        )
                    i = j
                    continue
            elif open_count > close_count:
                # Incomplete bare JSON — still streaming. If the partial content
                # already reveals a known typed-block root key, commit it as that
                # typed block in a loading state instead of leaking raw JSON as
                # text. Gated on detect_json_block_type, so prose with a stray
                # "{" stays text. On a finalized message braces balance and this
                # branch never fires.
                partial_json = "\n".join(json_lines).strip()
                json_type = detect_json_block_type(partial_json)
                if json_type:
                    flush_text()
                    blocks.append(
                        DetectedBlock(
                            type=json_type,
                            content=partial_json,
                            language="json",
                            metadata={"isComplete": False},
                        )
                    )
                    i = j
                    continue

        # 5.5. Mid-line attribute XML (e.g. "Hello <decision prompt="...">")
        # The opening tag is somewhere inside the line, not at the start.
        # Strategy (mirrors TypeScript step 5.5):
        #   1. Emit the text before the tag as a text block.
        #   2. Replace the current line in `lines` with [text_before?, tag_and_rest]
        #      so the normal attribute-XML path handles the decision on the next pass.
        #   3. Pre-compute rawXmlOverride from the original source lines (before any
        #      insert mutations) so replaceBlockContent can find the exact substring.
        mid_line = detect_mid_line_attribute_xml(processed_line)
        if mid_line:
            # Flush accumulated text from prior lines
            flush_text()

            tag_start: int = mid_line["tag_start"]
            block_type_ml: str = mid_line["type"]
            text_before = processed_line[:tag_start].rstrip()
            tag_and_rest = processed_line[tag_start:]

            # Build rawXmlOverride: scan forward from current line to capture the
            # exact source text up to and including the closing tag.
            closing_tag_ml = f"</{block_type_ml}>"
            raw_xml_parts = [tag_and_rest]
            found_close = closing_tag_ml in tag_and_rest
            if not found_close:
                for j in range(i + 1, len(lines)):
                    j_line = lines[j]
                    j_idx = j_line.find(closing_tag_ml)
                    if j_idx != -1:
                        raw_xml_parts.append(j_line[: j_idx + len(closing_tag_ml)])
                        found_close = True
                        break
                    raw_xml_parts.append(j_line)
            raw_xml_override_ml = "\n".join(raw_xml_parts)

            # Store the override keyed by the trimmed tag line so step 3a
            # picks it up when it processes the synthetic tag_and_rest line.
            pending_raw_xml_overrides[tag_and_rest.strip()] = raw_xml_override_ml

            # Splice current line into [text_before?, tag_and_rest]
            replacements: list[str] = []
            if text_before:
                replacements.append(text_before)
            replacements.append(tag_and_rest)
            lines[i : i + 1] = replacements
            # Re-process from i (the text_before line, or the tag_and_rest line directly)
            continue

        # 5.7. Tree diagrams — consecutive lines with box-drawing or ASCII
        #      tree connectors.
        if is_tree_line(trimmed_line):
            tree_end = i + 1
            while tree_end < len(lines):
                next_trimmed = normalize_line(lines[tree_end]).strip()
                if not next_trimmed or is_tree_line(next_trimmed):
                    tree_end += 1
                    continue
                break
            tree_lines_count = sum(
                1
                for x in lines[i:tree_end]
                if is_tree_line(normalize_line(x).strip())
            )
            # Need at least 3 tree-like lines to constitute a tree block.
            if tree_lines_count >= 3:
                tree_start = find_tree_block_start(lines, i)
                if tree_start < i:
                    current_text = _strip_accumulated_lines_from_text(
                        current_text, lines, tree_start, i
                    )
                flush_text()
                tree_content = "\n".join(
                    normalize_line(x) for x in lines[tree_start:tree_end]
                )
                blocks.append(
                    DetectedBlock(type="tree", content=tree_content.strip())
                )
                i = tree_end
                continue

        # 6. Accumulate as text — DO NOT GOBBLE UP BLANK LINES. A dropped blank
        #    line merges two markdown paragraphs into one.
        current_text += processed_line + ("\n" if i < len(lines) - 1 else "")
        i += 1

    flush_text()
    return _recover_embedded_kind_json_blocks(blocks)
