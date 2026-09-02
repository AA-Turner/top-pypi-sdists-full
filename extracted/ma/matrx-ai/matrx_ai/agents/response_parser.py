"""Robust JSON extraction from LLM responses.

ONE entry point: ``extract_json()``. Default call is the simple, fast,
backward-compatible path. Optional kwargs unlock smarter behavior — schema-
aware filtering, multi-match collection, detailed result wrappers — without
forcing any consumer to migrate.

Usage:
    from matrx_ai.agents.response_parser import extract_json, extract_model

    # Simple — first valid JSON block, raw value or None
    data = extract_json(text)

    # Schema-aware — find the candidate matching an agent's output_schema
    data = extract_json(text, schema=agent.output_schema["schema"])

    # Multi-match — every JSON block in the text, deduped, in discovery order
    every = extract_json(text, return_all=True)

    # Pick the Nth match (0-indexed)
    second = extract_json(text, nth=1)

    # Detailed result wrapper — recommended for new code
    result = extract_json(text, schema=schema, detailed=True)
    if result.success:
        use(result.data)
    else:
        log(result.reason)

    # Pydantic-validated extraction
    model = extract_model(text, MyModel)
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from typing import Any, TypeVar

import json_repair
from matrx_utils import vcprint
from pydantic import BaseModel, ValidationError

T = TypeVar("T", bound=BaseModel)


# ---------------------------------------------------------------------------
# Patterns
# ---------------------------------------------------------------------------

# Strip model reasoning regions before JSON extraction. Covers every wrapper
# the provider streamers emit: <think>/<thinking> (Anthropic-style,
# self-tagged) and <reasoning> (Google/Cerebras/generic-OpenAI streamers, see
# each provider's send_chunk). A JSON draft written INSIDE reasoning must never
# become a candidate that outranks the model's real final answer — this is
# Layer 2; Layer 1 is UnifiedMessage.get_output() excluding ThinkingContent so
# the flattened result.output never contains reasoning in the first place.
_THINKING_RE = re.compile(
    r"<(?P<tag>think(?:ing)?|reasoning)>\s*.*?\s*</(?P=tag)>",
    re.DOTALL | re.IGNORECASE,
)

_FENCE_RE = re.compile(
    r"```(?:json|JSON)?\s*\n?(.*?)\n?\s*```",
    re.DOTALL,
)

_TRAILING_COMMA_RE = re.compile(r",\s*([}\]])")


# ---------------------------------------------------------------------------
# Result wrapper — always returned, never raised
# ---------------------------------------------------------------------------


@dataclass
class JsonExtraction:
    data: dict | list | None
    success: bool
    reason: str
    all_matches: list[dict | list] = field(default_factory=list)


# ---------------------------------------------------------------------------
# Degenerate structured output — the "placeholder" collapse
# ---------------------------------------------------------------------------
# Anthropic constrained decoding (output_config.format json_schema) can
# stochastically give up mid-generation: the model ends the turn a few hundred
# tokens in with schema-VALID JSON whose required string fields carry the
# literal filler "placeholder" (feedback 0788c8a5, Website Factory Page
# Writer, 2026-08-23 — reproduced live on claude-sonnet-5 with and without
# reasoning settings, so this is a model-side failure mode, not a request-
# shaping bug). Schema validation passes, so without this check the corrupt
# result persists silently into live pages. The value set is deliberately
# TIGHT — only strings that are unambiguously constrained-decoding filler,
# never plausible business values ("n/a", "none", "pending" stay legal).

_DEGENERATE_STRUCTURED_VALUES = frozenset(
    {"placeholder", "(placeholder)", "[placeholder]", "{placeholder}", "<placeholder>"}
)


def find_degenerate_strings(data: Any, path: str = "$") -> list[str]:
    """Return the paths of every string in ``data`` that is literal model
    filler (exact match against ``_DEGENERATE_STRUCTURED_VALUES``, case- and
    whitespace-insensitive). Prose that merely CONTAINS the word "placeholder"
    is never flagged. Empty list == clean."""
    hits: list[str] = []
    if isinstance(data, str):
        if data.strip().lower() in _DEGENERATE_STRUCTURED_VALUES:
            hits.append(path)
    elif isinstance(data, dict):
        for key, value in data.items():
            hits.extend(find_degenerate_strings(value, f"{path}.{key}"))
    elif isinstance(data, list):
        for index, value in enumerate(data):
            hits.extend(find_degenerate_strings(value, f"{path}[{index}]"))
    return hits


# ---------------------------------------------------------------------------
# Low-level parsing helpers
# ---------------------------------------------------------------------------


def _strip_thinking(text: str) -> str:
    return _THINKING_RE.sub("", text).strip()


def strip_thinking(text: str) -> str:
    """Public: remove ``<thinking>``/``<reasoning>``/``<think>`` blocks from text.

    ``UnifiedMessage.get_output()`` already excludes ``ThinkingContent`` (Layer 1),
    so a well-behaved provider's ``result.output`` is reasoning-free. But some
    providers stream reasoning INLINE as ``<reasoning>`` tags that land in the
    flattened text as ordinary content — this strips that residual case so any
    consumer of the answer text (JSON extraction, text-mode storage, display)
    never sees chain-of-thought. Idempotent; safe on already-clean text.
    """
    return _strip_thinking(text)


def _try_parse(candidate: str) -> dict | list | None:
    candidate = candidate.strip()
    if not candidate:
        return None
    candidate = _TRAILING_COMMA_RE.sub(r"\1", candidate)
    try:
        result = json.loads(candidate)
        if isinstance(result, (dict, list)):
            return result
    except (json.JSONDecodeError, ValueError):
        pass
    return None


def _walk_brace_spans(text: str, open_char: str, close_char: str) -> list[tuple[int, int]]:
    """Find every balanced top-level [start, end) span of the given bracket type."""
    spans: list[tuple[int, int]] = []
    n = len(text)
    i = 0
    while i < n:
        if text[i] != open_char:
            i += 1
            continue
        depth = 0
        in_string = False
        escape_next = False
        closed = False
        for j in range(i, n):
            ch = text[j]
            if escape_next:
                escape_next = False
                continue
            if ch == "\\":
                escape_next = True
                continue
            if ch == '"':
                in_string = not in_string
                continue
            if in_string:
                continue
            if ch == open_char:
                depth += 1
            elif ch == close_char:
                depth -= 1
                if depth == 0:
                    spans.append((i, j + 1))
                    i = j + 1
                    closed = True
                    break
        if not closed:
            break
    return spans


def _collect_candidates(text: str) -> list[dict | list]:
    """Return every parseable JSON value found in text, in discovery order, deduped."""
    cleaned = _strip_thinking(text)
    candidates: list[dict | list] = []
    seen: set[str] = set()

    def _add(value: dict | list | None) -> None:
        if value is None:
            return
        try:
            key = json.dumps(value, sort_keys=True, default=str)
        except (TypeError, ValueError):
            key = repr(value)
        if key in seen:
            return
        seen.add(key)
        candidates.append(value)

    # 1) Fenced blocks — collect every one
    for match in _FENCE_RE.finditer(cleaned):
        _add(_try_parse(match.group(1)))

    # 2) Whole-text parse (covers the "model returned pure JSON" case)
    _add(_try_parse(cleaned))

    # 3) Brace-walked top-level spans — catches JSON embedded in prose
    for open_c, close_c in (("{", "}"), ("[", "]")):
        for start, end in _walk_brace_spans(cleaned, open_c, close_c):
            _add(_try_parse(cleaned[start:end]))

    return candidates


def _try_parse_repaired(candidate: str) -> dict | list | None:
    """Parse a candidate that strict JSON rejects, repairing near-miss syntax.

    The failure this exists for: a model writes a long prose field and drops a
    nested quote in unescaped — ``"...called the "powerhouse of the cell.""`` —
    or closes an object one key early. Strict ``json.loads`` rejects the whole
    document, and the brace-walker then surfaces only the inner arrays, so a
    schema requiring a top-level key never matches and the run dies with a
    complete, correct answer sitting in the text.

    ``json-repair`` was already a declared dependency of both ``matrx-ai`` and
    the host app with no importer anywhere — this is the consumer it was added
    for. Repair is a LAST tier only: ``extract_json`` reaches it solely when no
    strictly-parsed candidate matched, so a valid parse always wins.
    """
    candidate = candidate.strip()
    if not candidate:
        return None
    try:
        result = json_repair.loads(candidate)
    except Exception:  # never raises out of the funnel
        return None
    if not isinstance(result, (dict, list)) or not result:
        return None
    if not _repair_is_faithful(candidate, result):
        return None
    return result


def _repair_is_faithful(candidate: str, value: dict | list) -> bool:
    """Guard the repair tier against FABRICATION — repair, never invention.

    ``json-repair`` always answers. Handed ``"{{{{ unbalanced"`` it returns
    ``[[[['unbalanced']]]]`` — nesting that exists nowhere in the input — and
    the schema normalizer then wraps that in the required top-level key, so
    pure garbage reports as a successful extraction. That is worse than a clean
    failure: the run continues on a value the model never emitted.

    A genuine repair leaves fingerprints the input already had:

    * **It starts as a JSON document.** There is an opening ``{`` / ``[``.
    * **It carries key/value evidence** — a ``:`` or a quoted string. Real model
      JSON, however mangled, has keys; ``{{{{ unbalanced`` has neither, so every
      structure in the "repaired" result was manufactured.
    * **The top-level type survives.** Text whose first bracket is ``{`` must
      repair to an object, ``[`` to an array. When json-repair flips the type it
      could not find the keys the braces implied and fell back to inventing a
      container.

    The near-miss output this tier exists for — an unescaped nested quote, an
    object closed one key early, a truncated tail — passes all three unchanged.
    """
    first_brace = candidate.find("{")
    first_bracket = candidate.find("[")
    positions = [i for i in (first_brace, first_bracket) if i != -1]
    if not positions:
        return False
    if '"' not in candidate and ":" not in candidate:
        return False
    expected = dict if candidate[min(positions)] == "{" else list
    return isinstance(value, expected)


def _collect_repaired_candidates(text: str) -> list[dict | list]:
    """Repair-tier candidates, in the same discovery order as the strict tiers."""
    cleaned = _strip_thinking(text)
    candidates: list[dict | list] = []
    seen: set[str] = set()

    def _add(value: dict | list | None) -> None:
        if value is None:
            return
        try:
            key = json.dumps(value, sort_keys=True, default=str)
        except (TypeError, ValueError):
            key = repr(value)
        if key in seen:
            return
        seen.add(key)
        candidates.append(value)

    for match in _FENCE_RE.finditer(cleaned):
        _add(_try_parse_repaired(match.group(1)))
    _add(_try_parse_repaired(cleaned))
    return candidates


# ---------------------------------------------------------------------------
# Schema-aware matching — minimal JSON Schema support (type + required, depth 1)
# ---------------------------------------------------------------------------


def _candidate_matches_schema(value: Any, schema: dict) -> bool:
    expected = schema.get("type")
    if expected == "object":
        if not isinstance(value, dict):
            return False
        for key in (schema.get("required") or []):
            if key not in value:
                return False
        return True
    if expected == "array":
        if not isinstance(value, list):
            return False
        item_schema = schema.get("items") or {}
        if isinstance(item_schema, dict) and item_schema.get("type") == "object":
            required = item_schema.get("required") or []
            if required and value:
                for v in value:
                    if isinstance(v, dict) and all(k in v for k in required):
                        return True
                return False
        return True
    return isinstance(value, (dict, list))


def _try_normalize_to_schema(value: Any, schema: dict) -> Any:
    """Reconcile common shape mismatches between agent prompt and declared schema.

    Two real-world cases this fixes:
      - Schema is {type:object, properties:{items:{type:array}}, required:[items]}
        but the model returned the bare array.  → wrap as {items: <array>}.
      - Schema is {type:array, items:{...}} but the model returned
        {<key>: [...]}.  → unwrap to the inner array.
    """
    expected = schema.get("type")
    if expected == "object" and isinstance(value, list):
        properties = schema.get("properties") or {}
        for key in (schema.get("required") or list(properties.keys())):
            prop = properties.get(key) or {}
            if prop.get("type") == "array":
                return {key: value}
    if expected == "array" and isinstance(value, dict):
        for v in value.values():
            if isinstance(v, list):
                return v
    return value


# ---------------------------------------------------------------------------
# Public API — single entry point
# ---------------------------------------------------------------------------


def extract_json(
    text: str,
    *,
    schema: dict | None = None,
    return_all: bool = False,
    nth: int | None = None,
    detailed: bool = False,
) -> Any:
    """Extract JSON from LLM output.  Never raises.

    Args:
        text:       Raw LLM response.
        schema:     Optional JSON Schema dict (e.g. ``agent.output_schema["schema"]``).
                    When set, candidates are filtered to those matching the
                    top-level shape (``type`` + ``required`` at depth 1) and
                    common shape mismatches are auto-normalized.
        return_all: Return a list of every matching candidate.
        nth:        Return the Nth matching candidate (0-indexed).
        detailed:   Return a ``JsonExtraction`` wrapper instead of the raw value.
                    Strongly recommended for new code so the caller can read
                    ``.success`` and ``.reason``.

    Default (no kwargs) returns the first valid JSON block, or ``None``.
    """
    if not text or not str(text).strip():
        if detailed:
            return JsonExtraction(data=None, success=False, reason="empty input")
        return [] if return_all else None

    try:
        candidates = _collect_candidates(text)
    except Exception as exc:
        vcprint(f"[ResponseParser] Candidate collection failed: {exc}", color="yellow")
        candidates = []

    def _filter(cands: list[Any]) -> list[Any]:
        if schema is None:
            return list(cands)
        kept: list[Any] = []
        for c in cands:
            adjusted = _try_normalize_to_schema(c, schema)
            if _candidate_matches_schema(adjusted, schema):
                kept.append(adjusted)
        return kept

    matches: list[Any] = _filter(candidates)
    empty_reason = (
        "no JSON candidate matched the supplied schema"
        if schema is not None
        else "no valid JSON found in response"
    )

    # Repair tier — LAST resort, entered only when nothing strict matched.
    # Reached both when the text held no parseable JSON at all and when it held
    # parseable fragments (the brace-walker's inner arrays) that missed the
    # schema because the enclosing object was malformed.
    if not matches:
        try:
            repaired = _collect_repaired_candidates(text)
        except Exception as exc:
            vcprint(f"[ResponseParser] Repair pass failed: {exc}", color="yellow")
            repaired = []
        matches = _filter(repaired)
        if matches:
            # Loud on purpose: a model emitted malformed JSON and we recovered
            # it. The run survives, but the agent's output contract is slipping.
            vcprint(
                "[ResponseParser] Strict JSON parse failed; recovered the value "
                "via json-repair. The model emitted malformed JSON.",
                color="yellow",
            )
        else:
            empty_reason += " (json-repair recovered nothing faithful to the input)"

    if return_all:
        if detailed:
            return JsonExtraction(
                data=matches if matches else None,
                success=bool(matches),
                reason="" if matches else empty_reason,
                all_matches=matches,
            )
        return matches

    if nth is not None:
        if 0 <= nth < len(matches):
            value = matches[nth]
            if detailed:
                return JsonExtraction(data=value, success=True, reason="", all_matches=matches)
            return value
        if detailed:
            return JsonExtraction(
                data=None,
                success=False,
                reason=f"nth={nth} out of range (found {len(matches)} match(es))",
                all_matches=matches,
            )
        return None

    if matches:
        value = matches[0]
        if detailed:
            return JsonExtraction(data=value, success=True, reason="", all_matches=matches)
        return value

    if detailed:
        return JsonExtraction(data=None, success=False, reason=empty_reason, all_matches=[])
    vcprint(f"[ResponseParser] {empty_reason}", color="yellow")
    return None


# ---------------------------------------------------------------------------
# Pydantic-validated extraction — unchanged public behavior
# ---------------------------------------------------------------------------


def extract_model[T: BaseModel](text: str, model_class: type[T]) -> T | None:
    """Extract JSON from LLM output and validate it against a Pydantic model.

    Returns ``None`` if extraction or validation fails.
    """
    data = extract_json(text)
    if data is None:
        return None
    if not isinstance(data, dict):
        vcprint(
            f"[ResponseParser] Expected dict for {model_class.__name__}, got {type(data).__name__}",
            color="yellow",
        )
        return None
    try:
        return model_class.model_validate(data)
    except ValidationError as exc:
        vcprint(
            f"[ResponseParser] Validation failed for {model_class.__name__}: {exc}",
            color="yellow",
        )
        return None
