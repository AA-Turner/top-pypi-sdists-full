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
    #: ``data`` came from the json-repair tier, not a strict parse.
    repaired: bool = False
    #: ``data`` is a repair that CLOSED a document the text left open (cut off at an output cap,
    #: a RECITATION stop, or mid-object). Everything after the cut is lost: the value is offered so
    #: the caller can report it, never so it can be treated as the complete answer.
    truncated: bool = False


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


# A FILLER ROW IS NOT A COLLAPSE. A list-producing agent sometimes writes ONE
# row it has nothing for — ``{"field": "google_business_profile", "value": "",
# "reason": "placeholder", ...}`` — between and after complete rows. That is a
# finished answer carrying a "nothing found" row, not an abandoned generation
# (live 2026-11-16, request a41a8b59, brand_basics: 24 complete facts, one
# filler row, model stopped normally; 11 of 77 runs of that agent in 4 days,
# every one a filler ROW inside ``facts``, never a top-level field). Refusing
# the whole answer re-ran a 20-25 s paid call. The row is dropped (loudly, by
# path) and the answer kept — but only while the filler rows are a small
# minority of their list and at least one clean row remains; filler anywhere
# else, or a list that is mostly filler, is still the collapse and refused.
_MAX_FILLER_ROW_SHARE = 0.25


def prune_degenerate_rows(data: Any, path: str = "$") -> tuple[Any, list[str]]:
    """Drop list elements that carry literal filler, when they are a small minority.

    Returns ``(data_without_filler_rows, pruned_paths)``. A list is pruned only
    when its filler elements are ≤ ``_MAX_FILLER_ROW_SHARE`` of it and at least
    one clean element remains; otherwise it is left untouched so
    ``degenerate_output_error`` refuses it. Never mutates the input.
    """
    pruned: list[str] = []
    if isinstance(data, dict):
        out: dict[str, Any] = {}
        for key, value in data.items():
            out[key], sub = prune_degenerate_rows(value, f"{path}.{key}")
            pruned.extend(sub)
        return out, pruned
    if isinstance(data, list):
        children = [prune_degenerate_rows(v, f"{path}[{i}]") for i, v in enumerate(data)]
        filler = [
            i
            for i, (value, _) in enumerate(children)
            if isinstance(value, dict | list) and find_degenerate_strings(value)
        ]
        clean = len(data) - len(filler)
        if filler and clean >= 1 and len(filler) <= _MAX_FILLER_ROW_SHARE * len(data):
            drop = set(filler)
            out_list = []
            for i, (value, sub) in enumerate(children):
                if i in drop:
                    pruned.append(f"{path}[{i}]")
                else:
                    out_list.append(value)
                    pruned.extend(sub)
            return out_list, pruned
        for _, sub in children:
            pruned.extend(sub)
        return [value for value, _ in children], pruned
    return data, pruned


def degenerate_output_error(data: Any) -> str | None:
    """THE one verdict on a parsed structured answer: ``None`` when clean, else the
    ``DegenerateOutputError: …`` message every path (AgentExecutor's parse helper,
    ``parse_agent_output`` and so the orchestrator / agent route / agent service)
    reports for it."""
    paths = find_degenerate_strings(data)
    if not paths:
        return None
    shown = ", ".join(paths[:8])
    return (
        f"DegenerateOutputError: {len(paths)} field(s) contain "
        f"literal placeholder filler ({shown}) — the model abandoned "
        "the generation; the run must be retried, not persisted"
    )


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


# ---------------------------------------------------------------------------
# Residual escapes — the DOUBLE-ESCAPED artifact class
# ---------------------------------------------------------------------------
# A model asked for JSON sometimes escapes its own escapes: it writes
# ``"certificate turnaround \\u2014 24 hours"`` where it meant ``—``. That
# document is VALID JSON, so nothing anywhere fails — ``json.loads`` faithfully
# decodes the outer escape and hands the consumer a string that still carries
# the six literal characters ``—``. The artifact is then stored, rendered
# and shown to a person exactly like that (seo.landscape_brief b532255e,
# 2026-09-14: 3 in `brief_markdown`, 10 in `facts`, "certificate turnaround
# — 24 hours" on the owner's own brief).
#
# The class fix lives HERE, at the ONE funnel every agent artifact passes
# through, never as a `.replace` in whichever consumer noticed it.
#
# The rule is deliberately TIGHT — the same discipline as
# `_DEGENERATE_STRUCTURED_VALUES` above:
#   * ONLY ``\uXXXX``. ``\n`` / ``\t`` / ``\"`` are left alone: they appear
#     legitimately in code samples, regexes and Windows paths a model quotes.
#   * ONLY non-ASCII code points (>= U+0080). ``A`` in decoded prose is
#     plausibly deliberate (documentation ABOUT escaping); ``—`` never is.
#   * NOT when the backslash is itself escaped (``\\u2014`` in the decoded
#     string is a real backslash followed by the text ``u2014``).
#   * Surrogate PAIRS decode together; a lone surrogate is left untouched.
# Idempotent: a second pass finds nothing to do.
_RESIDUAL_UNICODE_ESCAPE_RE = re.compile(
    r"(?<!\\)\\u(?:(?P<hi>[dD][89abAB][0-9a-fA-F]{2})\\u(?P<lo>[dD][c-fC-F][0-9a-fA-F]{2})"
    r"|(?P<bmp>[0-9a-fA-F]{4}))"
)


def _residual_escape_replacement(match: re.Match[str]) -> str:
    hi, lo, bmp = match.group("hi"), match.group("lo"), match.group("bmp")
    if hi and lo:
        code = 0x10000 + ((int(hi, 16) - 0xD800) << 10) + (int(lo, 16) - 0xDC00)
        return chr(code)
    code = int(bmp, 16)
    if code < 0x80 or 0xD800 <= code <= 0xDFFF:
        # ASCII escapes and lone surrogates are left exactly as written.
        return match.group(0)
    return chr(code)


def decode_residual_escapes(value: Any) -> Any:
    """Decode double-escaped ``\\uXXXX`` sequences left inside already-parsed
    JSON strings, walking dicts and lists.

    Values only — a dict KEY is never rewritten, because two keys could collapse
    onto one and silently drop a field. Keys in our schemas are ASCII.
    """
    if isinstance(value, str):
        if "\\u" not in value:
            return value
        return _RESIDUAL_UNICODE_ESCAPE_RE.sub(_residual_escape_replacement, value)
    if isinstance(value, dict):
        return {key: decode_residual_escapes(item) for key, item in value.items()}
    if isinstance(value, list):
        return [decode_residual_escapes(item) for item in value]
    return value


def _try_parse(candidate: str) -> dict | list | None:
    candidate = candidate.strip()
    if not candidate:
        return None
    candidate = _TRAILING_COMMA_RE.sub(r"\1", candidate)
    try:
        result = json.loads(candidate)
        if isinstance(result, (dict, list)):
            return decode_residual_escapes(result)
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
    # Faithfulness is judged against the RAW text; the decode happens after it.
    return decode_residual_escapes(result)


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


def parse_json_document(text: Any) -> dict | list | None:
    """A string that IS one JSON object or array, read whole — or ``None``.

    For a JSON value a model wrote INSIDE a tool argument (``payload: "{\\"questions\\": [...]"``):
    the whole string is the document, so no fragment is ever carved out of it and no prose is
    searched. Strict parse first; then the funnel's faithful repair (a dropped closing brace — the
    live shape, 3 of 3 ask_person calls on 2026-11-06 — an unescaped quote, a trailing comma).
    ``None`` means the text is not readable as one document: the caller refuses, it never guesses.
    """
    if not isinstance(text, str):
        return None
    stripped = text.strip()
    if stripped[:1] not in ("{", "["):
        return None
    try:
        value = json.loads(stripped)
    except (json.JSONDecodeError, ValueError):
        # Text cut off inside a string is a lost tail, not a near miss: repairing it would hand the
        # person a half sentence as if the agent wrote it.
        value = None if _ends_inside_string(stripped) else (_try_parse(stripped) or _try_parse_repaired(stripped))
    return value if isinstance(value, (dict, list)) else None


def _document_was_cut_off(candidate: str) -> bool:
    """True when the FIRST JSON document in ``candidate`` never closes — the text ends inside a
    string or with an opener still unclosed. A repair of such text closes it by invention: the
    tail the model never finished is gone. Lossless repairs (a fence, a trailing comma, an
    unescaped quote inside a closed document) leave the document balanced and are not cut off."""
    starts = [i for i in (candidate.find("{"), candidate.find("[")) if i != -1]
    if not starts:
        return False
    depth = 0
    inside = escaped = False
    for ch in candidate[min(starts):]:
        if inside:
            if escaped:
                escaped = False
            elif ch == "\\":
                escaped = True
            elif ch == '"':
                inside = False
        elif ch == '"':
            inside = True
        elif ch in "{[":
            depth += 1
        elif ch in "}]":
            depth -= 1
            if depth <= 0:
                return False
    return True


def _ends_inside_string(text: str) -> bool:
    inside = escaped = False
    for ch in text:
        if escaped:
            escaped = False
        elif ch == "\\":
            escaped = True
        elif ch == '"':
            inside = not inside
    return inside


def _collect_repaired_candidates(text: str) -> list[tuple[dict | list, bool]]:
    """Repair-tier candidates, in the same discovery order as the strict tiers, each paired with
    whether the repair closed a cut-off document (:func:`_document_was_cut_off`)."""
    cleaned = _strip_thinking(text)
    candidates: list[tuple[dict | list, bool]] = []
    seen: set[str] = set()

    def _add(value: dict | list | None, source: str) -> None:
        if value is None:
            return
        try:
            key = json.dumps(value, sort_keys=True, default=str)
        except (TypeError, ValueError):
            key = repr(value)
        if key in seen:
            return
        seen.add(key)
        candidates.append((value, _document_was_cut_off(source)))

    for match in _FENCE_RE.finditer(cleaned):
        _add(_try_parse_repaired(match.group(1)), match.group(1))
    _add(_try_parse_repaired(cleaned), cleaned)
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

    # Each candidate carries (value, repaired, truncated) so the selected value's provenance
    # reaches ``JsonExtraction`` — a cut-off document closed by repair must never pass as whole.
    tagged: list[tuple[Any, bool, bool]] = [(c, False, False) for c in candidates]

    def _filter(cands: list[tuple[Any, bool, bool]]) -> list[tuple[Any, bool, bool]]:
        if schema is None:
            return list(cands)
        kept: list[tuple[Any, bool, bool]] = []
        for c, was_repaired, was_cut in cands:
            adjusted = _try_normalize_to_schema(c, schema)
            if _candidate_matches_schema(adjusted, schema):
                kept.append((adjusted, was_repaired, was_cut))
        return kept

    # A WHOLE DOCUMENT WITH ONE TYPO IS STILL THE ANSWER. When the response is
    # one JSON document (it opens with ``{``/``[``) that strict parsing rejects
    # — a stray bracket deep inside thousands of minified characters — the
    # brace-walker above still finds the document's inner arrays, and without a
    # schema the first of those "wins": the caller gets the first table instead
    # of the template and reports the real keys as missing (describe box,
    # 2026-10-08). A faithful repair of the whole document outranks any
    # fragment carved out of it.
    whole = _strip_thinking(text).strip()
    if whole[:1] in ("{", "[") and _try_parse(whole) is None:
        repaired_whole = _try_parse_repaired(whole)
        if repaired_whole is not None:
            vcprint(
                "[ResponseParser] The response is one JSON document with malformed "
                "syntax; recovered the whole document via json-repair instead of a fragment.",
                color="yellow",
            )
            tagged = [(repaired_whole, True, _document_was_cut_off(whole)), *tagged]

    tagged_matches = _filter(tagged)
    empty_reason = (
        "no JSON candidate matched the supplied schema"
        if schema is not None
        else "no valid JSON found in response"
    )

    # Repair tier — LAST resort, entered only when nothing strict matched.
    # Reached both when the text held no parseable JSON at all and when it held
    # parseable fragments (the brace-walker's inner arrays) that missed the
    # schema because the enclosing object was malformed.
    if not tagged_matches:
        try:
            repaired = _collect_repaired_candidates(text)
        except Exception as exc:
            vcprint(f"[ResponseParser] Repair pass failed: {exc}", color="yellow")
            repaired = []
        tagged_matches = _filter([(value, True, cut) for value, cut in repaired])
        if tagged_matches:
            # Loud on purpose: a model emitted malformed JSON and we recovered
            # it. The run survives, but the agent's output contract is slipping.
            vcprint(
                "[ResponseParser] Strict JSON parse failed; recovered the value "
                "via json-repair. The model emitted malformed JSON.",
                color="yellow",
            )
        else:
            empty_reason += " (json-repair recovered nothing faithful to the input)"

    matches: list[Any] = [value for value, _, _ in tagged_matches]
    first_repaired = bool(tagged_matches) and tagged_matches[0][1]
    first_truncated = bool(tagged_matches) and tagged_matches[0][2]
    if first_truncated:
        vcprint(
            "[ResponseParser] 🚨 The JSON was CUT OFF before it closed; json-repair closed it, so "
            "everything after the cut is lost. The value is incomplete — never the whole answer.",
            color="red",
        )

    if return_all:
        if detailed:
            return JsonExtraction(
                data=matches if matches else None,
                success=bool(matches),
                reason="" if matches else empty_reason,
                all_matches=matches,
                repaired=first_repaired,
                truncated=first_truncated,
            )
        return matches

    if nth is not None:
        if 0 <= nth < len(matches):
            value = matches[nth]
            if detailed:
                was_repaired, was_cut = tagged_matches[nth][1], tagged_matches[nth][2]
                return JsonExtraction(
                    data=value, success=True, reason="", all_matches=matches,
                    repaired=was_repaired, truncated=was_cut,
                )
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
            return JsonExtraction(
                data=value, success=True, reason="", all_matches=matches,
                repaired=first_repaired, truncated=first_truncated,
            )
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
