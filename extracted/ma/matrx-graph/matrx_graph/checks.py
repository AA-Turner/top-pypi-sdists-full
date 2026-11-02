"""Response checks — measure an answer against a target, deterministically.

THE ONE CHECK ENGINE (design: common-docs/systems/workflows/projects/
response-checks-and-revisions/DESIGN.md §4). Pure functions: no database, no
model, no network. A check carries a target and a tolerance, measures only the
text the consumer will actually use (a *projection*), and returns facts — never
instructions — so a revision turn can hand them to the agent verbatim.

v1 check types (owner ruling 2026-10-07): ``length`` and ``host``.
Item-list checks (generic-only GAP 2, 2026-10-27): :func:`check_items` checks every
item of a list (typically an agent's answer) against what was sent — ``verbatim``,
``in_set``, ``once``, ``same_set``, ``max_length``, ``not_contains``, ``pattern``, ``required`` —
keeps the items that pass and returns the rest with their reasons. The one text
folding a verbatim check uses (:func:`flat`, :func:`folded`) lives here too.

* ``length`` — counts ``words`` / ``characters`` / ``characters_no_spaces`` / ``line_breaks`` /
  ``characters_collapsed`` /
  ``sentences`` through :func:`text_metrics`, the platform's ONE text counter
  (``text.word_count`` calls it too). A target that resolves blank SKIPS the
  check (recorded ``skipped``) — a length is enforced only when somebody stated
  one; this engine never invents a target.
* ``host`` — a validator the HOST registers by name
  (:func:`configure_host_checks`), so a workflow step and a code path name the
  same validator instead of keeping two.

Projections ("what text counts"): ``plain`` (Markdown / tags / code fences
stripped) plus host projections registered by name
(:func:`configure_host_projections`) — the consumer's own parser, so speaker
labels and voice tags are never counted as words.
"""

from __future__ import annotations

import html
import json
import re
import unicodedata
from collections.abc import Callable, Mapping
from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, model_validator

from matrx_graph.safe_regex import UnsafePatternError, compile_safe
from matrx_graph.text_match import ANY_TAG, INLINE_TAG, FuzzyRule, TermMatcher

# --------------------------------------------------------------------------- #
# The one text counter                                                        #
# --------------------------------------------------------------------------- #

_WORD_RE = re.compile(r"\b[\w']+\b")
_SENTENCE_SPLIT_RE = re.compile(r"[.!?]+\s*")
_PARAGRAPH_SPLIT_RE = re.compile(r"\n\s*\n")


def text_metrics(text: str) -> dict[str, int]:
    """THE platform text counter. ``text.word_count`` and every length check use it."""
    text = text or ""
    return {
        "characters": len(text),
        "characters_no_spaces": len(text) - sum(1 for c in text if c.isspace()),
        "words": len(_WORD_RE.findall(text)),
        "sentences": len([s for s in _SENTENCE_SPLIT_RE.split(text) if s.strip()]),
        "paragraphs": len([p for p in _PARAGRAPH_SPLIT_RE.split(text) if p.strip()]),
        "lines": len(text.splitlines()),
    }


# --------------------------------------------------------------------------- #
# Projections and host checks (host-injected seams)                           #
# --------------------------------------------------------------------------- #

#: ``(text) -> text`` — the consumer's own view of the answer.
HostProjection = Callable[[str], str]
#: ``(text, values) -> None | str`` — None when the answer passes; otherwise the
#: failure as a FACT the agent can act on ("Script has 3 speakers; 2 required").
HostCheck = Callable[[str, Mapping[str, Any]], "str | None"]

_HOST_PROJECTIONS: dict[str, HostProjection] = {}
_HOST_CHECKS: dict[str, HostCheck] = {}


def configure_host_projections(projections: Mapping[str, HostProjection]) -> None:
    """Register host projections by name (``podcast.spoken_text``). Idempotent."""
    _HOST_PROJECTIONS.update(projections)


def configure_host_checks(checks: Mapping[str, HostCheck]) -> None:
    """Register host checks by name (``podcast.script``). Idempotent."""
    _HOST_CHECKS.update(checks)


def registered_host_checks() -> tuple[str, ...]:
    return tuple(sorted(_HOST_CHECKS))


def registered_host_projections() -> tuple[str, ...]:
    return tuple(sorted(_HOST_PROJECTIONS))


_FENCE_RE = re.compile(r"```.*?```", re.DOTALL)
_TAG_RE = re.compile(r"<[^>\n]{1,200}>")
_MD_MARK_RE = re.compile(r"(^|\s)[#>*_`~-]+|[*_`~]+(\s|$)", re.MULTILINE)
_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]*\)")


def project_plain(text: str) -> str:
    """Strip code fences, HTML/XML tags, Markdown links and emphasis marks."""
    out = _FENCE_RE.sub(" ", text or "")
    out = _LINK_RE.sub(r"\1", out)
    out = _TAG_RE.sub(" ", out)
    out = _MD_MARK_RE.sub(lambda m: f"{m.group(1) or ''}{m.group(2) or ''}", out)
    return out


class UnknownHostCheckError(LookupError):
    """A spec named a host check or projection nobody registered — never a silent pass."""


def project(text: str, projection: str) -> str:
    if projection == "plain":
        return project_plain(text)
    fn = _HOST_PROJECTIONS.get(projection)
    if fn is None:
        raise UnknownHostCheckError(
            f"Projection '{projection}' is not registered. Registered: "
            f"plain, {', '.join(registered_host_projections()) or '(no host projections)'}."
        )
    return fn(text)


# --------------------------------------------------------------------------- #
# Spec and result                                                             #
# --------------------------------------------------------------------------- #

LengthUnit = Literal[
    "words", "characters", "characters_no_spaces", "sentences", "line_breaks", "characters_collapsed"
]


def length_of(text: str, unit: str) -> int:
    """``text`` measured in ``unit``: the ``text_metrics`` counts, plus two a check needs that a word counter does
    not report — ``line_breaks`` (every break, a trailing one too: "one line" is ``max 0``) and
    ``characters_collapsed`` (characters once runs of whitespace are one space and the ends trimmed: what a
    reader sees)."""
    text = text or ""
    if unit == "line_breaks":
        return text.count("\n") + text.replace("\r\n", "").count("\r")
    if unit == "characters_collapsed":
        return len(" ".join(text.split()))
    return text_metrics(text)[unit]

#: Starting tolerance when neither the spec nor the knob says otherwise. The live
#: value is knob ``workflow.response_checks.length_tolerance_pct`` (read by the
#: caller and passed in as ``default_tolerance_pct``).
STARTING_TOLERANCE_PCT = 20.0


class ResponseCheckSpec(BaseModel):
    """One check. Not a registered kind: it is an element of the step's ``checks`` config
    list (``ConversationReviseInput.checks``), never stored or passed on its own."""

    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1, max_length=80, description="Stable id, e.g. 'length'.")
    type: Literal["length", "host"]
    projection: str = Field(
        default="plain",
        description="What text counts: 'plain' or a registered host projection.",
    )
    unit: LengthUnit = "words"
    target: float | None = Field(
        default=None, description="Literal target. Blank → read from values[target_value]."
    )
    target_value: str | None = Field(
        default=None,
        description="Name of the mapped value that holds the target (e.g. 'target_word_count').",
    )
    tolerance_pct: float | None = Field(default=None, ge=0, le=100)
    min: float | None = None
    max: float | None = None
    host_check: str | None = Field(default=None, description="Registered host check name.")
    severity: Literal["revise", "warn"] = "revise"
    on_exhausted: Literal["continue", "fail"] = "continue"


class ResponseCheckMeasure(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str
    type: str
    passed: bool
    skipped: bool = False
    measured: float | None = None
    unit: str | None = None
    band_min: float | None = None
    band_max: float | None = None
    delta: float | None = None
    direction: Literal["cut", "add", "fix"] | None = None
    distance: float = 0.0
    severity: str = "revise"
    on_exhausted: str = "continue"
    detail: str = ""


class ResponseCheckResult(BaseModel):
    """Registered kind ``response_check_result``."""

    model_config = ConfigDict(extra="forbid")

    verdict: Literal["pass", "fail", "skipped"]
    checks: list[ResponseCheckMeasure] = Field(default_factory=list)
    rendered: str = ""

    def revise_misses(self) -> list[ResponseCheckMeasure]:
        return [c for c in self.checks if not c.passed and c.severity == "revise"]

    def misses(self) -> list[ResponseCheckMeasure]:
        return [c for c in self.checks if not c.passed]

    def distance(self) -> float:
        """Total distance to passing — 0 when every check passes. Picks the closest attempt."""
        return sum(c.distance for c in self.checks if not c.passed)


def _num(value: Any) -> float | None:
    if value is None or value == "":
        return None
    try:
        return float(str(value).strip())
    except (TypeError, ValueError):
        return None


def _fmt(n: float | None) -> str:
    if n is None:
        return "?"
    return f"{round(n):,}" if abs(n - round(n)) < 1e-9 or abs(n) >= 10 else f"{n:g}"


def _length(
    text: str, spec: ResponseCheckSpec, values: Mapping[str, Any], default_tol: float
) -> ResponseCheckMeasure:
    base = {"key": spec.key, "type": spec.type, "unit": spec.unit,
            "severity": spec.severity, "on_exhausted": spec.on_exhausted}
    target = spec.target if spec.target is not None else _num(
        values.get(spec.target_value) if spec.target_value else None
    )
    lo, hi = spec.min, spec.max
    if target is not None and (lo is None or hi is None):
        tol = (spec.tolerance_pct if spec.tolerance_pct is not None else default_tol) / 100.0
        lo = target * (1 - tol) if lo is None else lo
        hi = target * (1 + tol) if hi is None else hi
    if lo is None and hi is None:
        return ResponseCheckMeasure(
            **base, passed=True, skipped=True, detail="skipped: no target"
        )
    measured = float(length_of(project(text, spec.projection), spec.unit))
    lo_ = round(lo) if lo is not None else None
    hi_ = round(hi) if hi is not None else None
    if lo_ is not None and measured < lo_:
        delta, direction = lo_ - measured, "add"
    elif hi_ is not None and measured > hi_:
        delta, direction = measured - hi_, "cut"
    else:
        delta, direction = 0.0, None
    passed = direction is None
    want = target if target is not None else ((lo_ or 0) + (hi_ or lo_ or 0)) / 2
    band = f"{_fmt(lo_)}–{_fmt(hi_)}" if lo_ is not None and hi_ is not None else (
        f"at least {_fmt(lo_)}" if lo_ is not None else f"at most {_fmt(hi_)}"
    )
    target_txt = f"target {_fmt(target)} ({band})" if target is not None else f"band {band}"
    detail = f"Length: {_fmt(measured)} {spec.unit}; {target_txt}"
    if not passed:
        gap = abs(measured - want) if target is not None else delta
        detail += f"; {direction} about {_fmt(gap)}."
    else:
        detail += "; within the band."
    return ResponseCheckMeasure(
        **base, passed=passed, measured=measured, band_min=lo_, band_max=hi_,
        delta=delta or None, direction=direction,  # type: ignore[arg-type]
        distance=(delta / max(want, 1.0)) if not passed else 0.0, detail=detail,
    )


def _host(text: str, spec: ResponseCheckSpec, values: Mapping[str, Any]) -> ResponseCheckMeasure:
    name = spec.host_check or ""
    fn = _HOST_CHECKS.get(name)
    if fn is None:
        raise UnknownHostCheckError(
            f"Host check '{name}' is not registered. Registered: "
            f"{', '.join(registered_host_checks()) or '(none)'}."
        )
    failure = fn(text, values)
    return ResponseCheckMeasure(
        key=spec.key, type="host", passed=failure is None, direction=None if failure is None else "fix",
        distance=0.0 if failure is None else 1.0, severity=spec.severity,
        on_exhausted=spec.on_exhausted, detail=f"{name}: {failure}" if failure else f"{name}: passed.",
    )


def run_checks(
    answer: str,
    specs: list[ResponseCheckSpec],
    values: Mapping[str, JsonValue] | None = None,
    *,
    default_tolerance_pct: float = STARTING_TOLERANCE_PCT,
) -> ResponseCheckResult:
    """Run every spec against ``answer``. Pure; raises only on an unregistered host name."""
    values = values or {}
    measures = [
        _length(answer, s, values, default_tolerance_pct) if s.type == "length" else _host(answer, s, values)
        for s in specs
    ]
    live = [m for m in measures if not m.skipped]
    if not live:
        verdict: Literal["pass", "fail", "skipped"] = "skipped"
    else:
        verdict = "pass" if all(m.passed for m in live) else "fail"
    rendered = "\n".join(m.detail for m in measures if not m.skipped)
    return ResponseCheckResult(verdict=verdict, checks=measures, rendered=rendered)


# --------------------------------------------------------------------------- #
# Text folding — THE one normalisation a verbatim check uses                  #
# --------------------------------------------------------------------------- #
# Lifted from aidream/services/mandates/verbatim.py (2026-10-27), which now
# re-exports these, so a reader step in code and a workflow step fold alike.

_QUOTES = str.maketrans({"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-",
                         "—": "-", " ": " ", "…": "...",
                         # apostrophe- and quote-like marks a page or a model may use instead of ' and "
                         "ʼ": "'", "′": "'", "″": '"', "‚": "'", "„": '"'})

#: ``[text](url)`` and ``![alt](src)``: crawled page text keeps link markup; a reader quotes the words.
_MD_LINK = re.compile(r"!?\[([^\]]*)\]\([^)]*\)")
#: Inline formatting tags join the words around them (``<strong>shred</strong>``); any other tag is a break.
_INLINE_TAG = INLINE_TAG
_ANY_TAG = ANY_TAG


def flat(text: Any) -> str:
    """Whitespace, quote marks, dashes, Unicode width (NFKC), markdown links (to their words) and
    emphasis marks folded; case kept. A quote is verbatim when its flat form is a substring of the
    flat text sent."""
    s = unicodedata.normalize("NFKC", str(text or "")).translate(_QUOTES)
    s = _MD_LINK.sub(r"\1", s)
    s = re.sub(r"[*_`#>|]+", " ", s)
    return " ".join(s.split())


def folded(text: Any) -> str:
    """:func:`flat` of the visible text, case-folded: HTML tags stripped, then entities unescaped.
    Tags go before unescaping, so an escaped ``&lt;b&gt;`` stays text."""
    s = _ANY_TAG.sub(" ", _INLINE_TAG.sub("", str(text or "")))
    return flat(html.unescape(s)).casefold()


# --------------------------------------------------------------------------- #
# Item-list checks (generic-only GAP 2)                                       #
# --------------------------------------------------------------------------- #

ItemCheckType = Literal[
    "verbatim", "in_set", "once", "same_set", "max_length", "not_contains", "pattern", "required"
]
#: At most this many patterns (counting each one inside an all-of group) in one pattern check.
MAX_PATTERNS = 50
FoldMode = Literal["exact", "flat", "folded"]

#: How each check type compares text when the spec does not say.
_DEFAULT_FOLD: dict[str, FoldMode] = {
    "verbatim": "flat", "not_contains": "folded", "in_set": "exact", "once": "exact", "same_set": "exact",
}


class ItemCheckConfigError(ValueError):
    """A check names a value the step was not given, or a source of the wrong shape — never a silent pass."""


class ItemCheckSpec(BaseModel):
    """One check over every item of a list. Element of ``data.check_items``' ``checks`` setting."""

    model_config = ConfigDict(extra="forbid")

    type: ItemCheckType
    path: str = Field(
        default="",
        description="Dot path to the checked field inside each item (``quote``, ``evidence.keys``); "
        "empty = the item itself. A list value is checked element by element.",
    )
    key: str | None = Field(
        default=None, max_length=120,
        description="Name used in reasons and counts. Default ``<path>.<type>``.",
    )
    source: str | None = Field(
        default=None,
        description="verbatim: the input (dot path) holding the text sent — one text, a list of texts, "
        "a map key → text(s), or a list of records.",
    )
    source_by: str | None = Field(
        default=None,
        description="verbatim: dot path inside each item naming which source it must quote from "
        "(a map key, or a record's ``source_key_field`` when the source is a list of records).",
    )
    source_key_field: str = Field(default="id", description="verbatim + source_by over records: the key field.")
    source_text_field: str = Field(default="text", description="verbatim over records: the field holding the text.")
    allowed: list[JsonValue] | None = Field(
        default=None, description="in_set / once / same_set: the allowed values (or the ids sent), written here."
    )
    allowed_from: str | None = Field(
        default=None, description="in_set / once / same_set: the input (dot path) holding the allowed values."
    )
    terms: list[str] | None = Field(default=None, description="not_contains: the forbidden terms, written here.")
    terms_from: str | None = Field(
        default=None, description="not_contains: the input (dot path) holding the forbidden terms."
    )
    patterns: list[str | list[str]] | None = Field(
        default=None,
        description="pattern: regular expressions, written here. The field matches when ANY entry matches; "
        "an entry that is a list matches only when ALL of its patterns match (so [[\"won\", \"award\"], "
        "\"certified\"] reads: (won AND award) OR certified). Each is checked at save: valid, at most "
        "500 characters, and no shape that can hang (nested repeats like (a+)+, back-references).",
    )
    patterns_from: str | None = Field(
        default=None,
        description="pattern: the input (dot path) holding the patterns (texts, or lists of texts for all-of "
        "groups); judged the same way when the step runs.",
    )
    mode: Literal["must", "must_not"] = Field(
        default="must",
        description="pattern: must = the field has to match (else `no_pattern_match`); must_not = it must "
        "not match any entry (else `matches_pattern`).",
    )
    ignore_case: bool = Field(default=True, description="pattern: match without regard to case.")
    max_text_chars: int = Field(
        default=10_000, ge=100, le=1_000_000,
        description="pattern: the longest text a pattern reads. A longer value fails the item "
        "(`text_too_long`) instead of being read: some patterns slow down sharply on long text, "
        "and one check runs over every item.",
    )
    when_path: str | None = Field(
        default=None,
        description="Run this check only on items whose value at this dot path is one of `when_in` "
        "(``topic`` + [\"proof\"]); every other item passes it untouched.",
    )
    when_in: list[JsonValue] | None = Field(
        default=None, description="With `when_path`: the values (compared as text) that make the check apply."
    )
    from_field: str | None = Field(
        default=None,
        description="When ``allowed_from`` / ``terms_from`` / ``patterns_from`` is a list of records: the field "
        "read from each.",
    )
    max: float | None = Field(default=None, ge=0, description="max_length: the most allowed, in ``unit``.")
    unit: LengthUnit = Field(default="characters", description="max_length: what is counted (text_metrics).")
    fold: FoldMode | None = Field(
        default=None,
        description="How values are compared: exact (as text, ends trimmed — so 1 and \"1\" are the same "
        "id) | flat (whitespace, quote marks, dashes, width, markdown; case kept) | folded (flat + HTML "
        "stripped + case folded). Default: verbatim flat, set checks exact; not_contains always folds.",
    )
    fuzzy: float | None = Field(
        default=None, gt=0, le=1,
        description="not_contains: also catch near-miss spellings — a one-word term whose closeness "
        "ratio to a word in the text reaches this (0.86 is a good start). A near miss is FLAGGED "
        "(kept, listed in `flagged`) unless `fuzzy_drops`.",
    )
    fuzzy_drops: bool = Field(
        default=False, description="not_contains + fuzzy: drop an item whose only match is a near miss."
    )
    fuzzy_min_length: int = Field(
        default=7, ge=3, le=40, description="not_contains + fuzzy: only words at least this long are compared."
    )
    optional: bool = Field(
        default=False, description="An absent or empty value passes this check (``required`` ignores it)."
    )
    on_fail: Literal["drop_item", "fail"] = Field(
        default="drop_item", description="drop_item: drop the failing item and count it. fail: fail the step."
    )

    @model_validator(mode="after")
    def _settings_fit_the_type(self) -> ItemCheckSpec:
        t = self.type
        if t == "verbatim" and not self.source:
            raise ValueError("a verbatim check needs `source` (the input holding the text sent).")
        if t in ("in_set", "same_set") and self.allowed is None and not self.allowed_from:
            raise ValueError(f"an {t} check needs `allowed` or `allowed_from`.")
        if t == "max_length" and self.max is None:
            raise ValueError("a max_length check needs `max`.")
        if t == "not_contains" and self.terms is None and not self.terms_from:
            raise ValueError("a not_contains check needs `terms` or `terms_from`.")
        if t == "pattern":
            if self.patterns is None and not self.patterns_from:
                raise ValueError("a pattern check needs `patterns` or `patterns_from`.")
            if self.patterns is not None:
                _compile_patterns(self.patterns, self.ignore_case, self.name)
        elif self.mode != "must":
            raise ValueError(f"`mode` applies to a pattern check, not a {t} check.")
        if (self.when_path is None) != (self.when_in is None):
            raise ValueError("`when_path` and `when_in` go together.")
        owner = {
            "source": {"verbatim"}, "source_by": {"verbatim"},
            "allowed": {"in_set", "once", "same_set"}, "allowed_from": {"in_set", "once", "same_set"},
            "terms": {"not_contains"}, "terms_from": {"not_contains"}, "fuzzy": {"not_contains"},
            "max": {"max_length"}, "patterns": {"pattern"}, "patterns_from": {"pattern"},
        }
        wrong = sorted(k for k, types in owner.items() if getattr(self, k) is not None and t not in types)
        if wrong:
            raise ValueError(f"{wrong} do not apply to a {t} check.")
        if self.fold is not None and t in ("not_contains", "required", "max_length", "pattern"):
            raise ValueError(
                f"`fold` does not apply to a {t} check (not_contains always folds case and width; a pattern "
                "reads whitespace runs as one space and uses `ignore_case`)."
            )
        if self.from_field and not (self.allowed_from or self.terms_from or self.patterns_from):
            raise ValueError(
                "`from_field` reads records from `allowed_from` / `terms_from` / `patterns_from`; set one of them."
            )
        return self

    @property
    def name(self) -> str:
        return self.key or f"{self.path or 'item'}.{self.type}"

    @property
    def folding(self) -> FoldMode:
        return self.fold or _DEFAULT_FOLD.get(self.type, "exact")


class ItemCheckReason(BaseModel):
    model_config = ConfigDict(extra="forbid")

    check: str = Field(description="The check's name (its ``key``).")
    code: str = Field(
        description="missing | not_verbatim | no_source | not_in_set | unknown | duplicate | too_long | "
        "contains_term | no_pattern_match | matches_pattern | text_too_long"
    )
    detail: str = Field(default="", description="The failure as a plain fact.")


class RejectedItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index: int = Field(description="The item's position in the list checked.")
    item: JsonValue = Field(description="The item, unchanged.")
    reasons: list[ItemCheckReason] = Field(description="Every check it failed.")


class SetReport(BaseModel):
    model_config = ConfigDict(extra="forbid")

    missing: list[str] = Field(default_factory=list, description="Ids sent that no item answered.")
    unknown: list[str] = Field(default_factory=list, description="Ids answered that were never sent.")
    duplicate: list[str] = Field(default_factory=list, description="Ids answered more than once.")


class FlaggedItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    index: int = Field(description="The item's position in the list checked.")
    check: str = Field(description="The check's name (its ``key``).")
    term: str = Field(description="The term the item nearly contains.")
    matched_text: str = Field(description="The words in the item that nearly match it.")
    score: float = Field(description="How close the spelling is (0–1).")


class ItemsCheckResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[JsonValue] = Field(description="The items that passed every check, in order.")
    rejected: list[RejectedItem] = Field(default_factory=list, description="The items dropped, each with its reasons.")
    kept: int = 0
    dropped: int = 0
    total: int = 0
    counts: dict[str, int] = Field(
        default_factory=dict, description="Failures by reason, ``<check>:<code>`` → how many items."
    )
    sets: dict[str, SetReport] = Field(
        default_factory=dict, description="Per once / same_set check: missing, unknown and duplicate ids."
    )
    failed_checks: list[str] = Field(
        default_factory=list, description="Checks set to on_fail=fail that failed (the step fails)."
    )
    passed: bool = Field(default=True, description="True when nothing was dropped, missing or failed.")
    flagged: list[FlaggedItem] = Field(
        default_factory=list, description="Kept items a person should look at: a near-miss spelling of a term."
    )
    flagged_count: int = Field(default=0, description="How many items were flagged.")


_MISSING = object()
_SET_TYPES = ("once", "same_set")
#: Every reason code each check type can give (``counts`` lists each, 0 when none).
_CODES: dict[str, tuple[str, ...]] = {
    "required": ("missing",),
    "verbatim": ("missing", "no_source", "not_verbatim"),
    "in_set": ("missing", "not_in_set"),
    "once": ("missing", "unknown", "duplicate"),
    "same_set": ("missing", "unknown", "duplicate"),
    "max_length": ("missing", "too_long"),
    "not_contains": ("missing", "contains_term"),
    "pattern": ("missing", "no_pattern_match", "matches_pattern", "text_too_long"),
}


#: One ``patterns`` entry compiled: any-of entries, each an all-of group (``source`` texts kept for reasons).
_PatternGroups = list[tuple[str, list["re.Pattern[str]"]]]


def _compile_patterns(raw: Any, ignore_case: bool, name: str) -> _PatternGroups:
    """Compile a ``patterns`` value (texts, or lists of texts = all-of groups) through the safe compiler.

    Raises ``ValueError`` (a save-time refusal for written patterns, a step failure for ``patterns_from``)."""
    entries = raw if isinstance(raw, list) else [raw]
    groups: _PatternGroups = []
    count = 0
    for entry in entries:
        parts = entry if isinstance(entry, list) else [entry]
        if not parts or not all(isinstance(p, str) and p for p in parts):
            raise ValueError(f"Check '{name}': each pattern must be a non-empty text (or a list of them); got {entry!r:.80}.")
        count += len(parts)
        try:
            compiled = [compile_safe(p, ignore_case=ignore_case) for p in parts]
        except UnsafePatternError as e:
            raise ValueError(f"Check '{name}': {e}") from e
        groups.append((" AND ".join(parts) if len(parts) > 1 else parts[0], compiled))
    if not groups:
        raise ValueError(f"Check '{name}': `patterns` is empty, so nothing could ever match.")
    if count > MAX_PATTERNS:
        raise ValueError(f"Check '{name}': {count} patterns; at most {MAX_PATTERNS}.")
    return groups


def _pattern_hit(groups: _PatternGroups, text: str) -> str | None:
    """The first entry (as written) that matches ``text``, else None."""
    for label, compiled in groups:
        if all(rx.search(text) for rx in compiled):
            return label
    return None


def _dig(obj: Any, path: str) -> Any:
    if not path:
        return obj
    cur = obj
    for part in path.split("."):
        if isinstance(cur, Mapping) and part in cur:
            cur = cur[part]
        elif isinstance(cur, list) and part.lstrip("-").isdigit() and -len(cur) <= int(part) < len(cur):
            cur = cur[int(part)]
        else:
            return _MISSING
    return cur


def _empty(value: Any) -> bool:
    return value is _MISSING or value is None or value == [] or value == {} or (
        isinstance(value, str) and not value.strip()
    )


def _values_of(value: Any) -> list[Any]:
    """A field's checked values: a list element by element, anything else as one value."""
    return [v for v in value] if isinstance(value, list) else [value]


def _fold(value: Any, mode: FoldMode) -> str:
    text = value if isinstance(value, str) else (
        str(value) if isinstance(value, (int, float, bool)) else json.dumps(value, sort_keys=True, default=str)
    )
    if mode == "flat":
        return flat(text)
    if mode == "folded":
        return folded(text)
    return text.strip()


def _ref(values: Mapping[str, Any], name: str, spec: ItemCheckSpec, setting: str) -> Any:
    got = _dig(values, name)
    if got is _MISSING:
        raise ItemCheckConfigError(
            f"Check '{spec.name}': `{setting}` names '{name}', which this step was not given. "
            f"It was given: {', '.join(sorted(values)) or '(nothing besides the items)'}."
        )
    return got


def _ref_list(values: Mapping[str, Any], name: str, spec: ItemCheckSpec, setting: str) -> list[Any]:
    got = _ref(values, name, spec, setting)
    got = got if isinstance(got, list) else [got]
    if spec.from_field:
        picked = [_dig(v, spec.from_field) for v in got]
        if got and all(v is _MISSING for v in picked):
            raise ItemCheckConfigError(
                f"Check '{spec.name}': no record in '{name}' has the field '{spec.from_field}' (`from_field`)."
            )
        got = [v for v in picked if v is not _MISSING]
    return got


def _allowed(spec: ItemCheckSpec, values: Mapping[str, Any]) -> list[Any] | None:
    if spec.allowed_from:
        return _ref_list(values, spec.allowed_from, spec, "allowed_from")
    return spec.allowed


def _source_texts(src: Any, spec: ItemCheckSpec) -> list[str]:
    out: list[str] = []
    elements = src if isinstance(src, list) else [src]
    records = [el for el in elements if isinstance(el, Mapping)]
    if records and all(_dig(r, spec.source_text_field) is _MISSING for r in records):
        raise ItemCheckConfigError(
            f"Check '{spec.name}': the source records have no '{spec.source_text_field}' field "
            "(`source_text_field`)."
        )
    for el in elements:
        if isinstance(el, Mapping):
            el = _dig(el, spec.source_text_field)
            if el is _MISSING:
                continue
        if isinstance(el, list):
            out.extend(_source_texts(el, spec))
        elif not _empty(el):
            out.append(_fold(el, spec.folding))
    return out


class _Verbatim:
    def __init__(self, spec: ItemCheckSpec, values: Mapping[str, Any]) -> None:
        self.spec = spec
        self.src = _ref(values, spec.source or "", spec, "source")
        self._all: list[str] | None = None
        self._by: dict[str, list[str]] = {}

    def texts_for(self, item: Any) -> list[str] | None:
        spec = self.spec
        if not spec.source_by:
            if self._all is None:
                inner = list(self.src.values()) if isinstance(self.src, Mapping) else self.src
                self._all = _source_texts(inner, spec)
            return self._all
        pick = _dig(item, spec.source_by)
        if _empty(pick):
            return None
        k = str(pick)
        if k not in self._by:
            src = self.src
            chosen: Any = _MISSING
            if isinstance(src, Mapping):
                chosen = src.get(k, _MISSING)
            elif isinstance(src, list):
                recs = [r for r in src if isinstance(r, Mapping) and str(_dig(r, spec.source_key_field)) == k]
                if recs:
                    chosen = recs
            else:
                raise ItemCheckConfigError(
                    f"Check '{spec.name}': `source_by` picks from `source`, so the source must be a map "
                    f"or a list; it is a {type(src).__name__}."
                )
            if chosen is _MISSING:
                return None
            self._by[k] = _source_texts(chosen, spec)
        return self._by[k]


def parse_item_checks(raw: Any, where: str = "checks") -> list[ItemCheckSpec]:
    """Validate a checks list that arrived at RUN time (``data.check_items`` ``checks_from``) by the
    same rules the saved ``checks`` setting is held to; raises :class:`ItemCheckConfigError` naming
    the check and giving the same sentence a save would."""
    from pydantic import ValidationError

    if not isinstance(raw, list) or not raw:
        raise ItemCheckConfigError(f"`{where}` must be a non-empty list of checks; it is {type(raw).__name__}"
                                   f"{' (empty)' if raw == [] else ''}.")
    out: list[ItemCheckSpec] = []
    for n, entry in enumerate(raw):
        try:
            out.append(ItemCheckSpec.model_validate(entry))
        except ValidationError as e:
            name = (entry.get("key") or f"{entry.get('path') or 'item'}.{entry.get('type')}") if isinstance(
                entry, Mapping) else repr(entry)[:60]
            msgs = "; ".join(
                (f"{'.'.join(str(x) for x in err['loc'])}: " if err["loc"] else "")
                + str(err["msg"]).removeprefix("Value error, ")
                for err in e.errors()
            )
            raise ItemCheckConfigError(f"{where} #{n} ('{name}'): {msgs}") from e
    return out


def check_items(
    items: list[JsonValue],
    specs: list[ItemCheckSpec],
    values: Mapping[str, Any] | None = None,
) -> ItemsCheckResult:
    """Run every spec over every item. Pure; raises :class:`ItemCheckConfigError` only when a spec
    names an input that is not there (or of an impossible shape)."""
    values = values or {}
    reasons: list[list[ItemCheckReason]] = [[] for _ in items]
    flagged: list[FlaggedItem] = []
    sets: dict[str, SetReport] = {}
    failed: list[str] = []

    def miss(i: int, spec: ItemCheckSpec, code: str, detail: str) -> None:
        reasons[i].append(ItemCheckReason(check=spec.name, code=code, detail=detail))
        if spec.on_fail == "fail":
            if spec.name not in failed:
                failed.append(spec.name)

    # Set checks (once / same_set) run last, over the items every other check kept: an answer that
    # repeats an id with one fake quote keeps the real one, and an id whose only answer was dropped
    # is reported missing.
    for spec in sorted(specs, key=lambda s: s.type in _SET_TYPES):
        mode = spec.folding
        verb = _Verbatim(spec, values) if spec.type == "verbatim" else None
        allowed = _allowed(spec, values) if spec.type in ("in_set", "once", "same_set") else None
        allowed_keys = {_fold(a, mode) for a in allowed} if allowed is not None else None
        terms: list[str] = []
        groups: _PatternGroups = []
        if spec.type == "pattern":
            raw_patterns = (
                _ref_list(values, spec.patterns_from, spec, "patterns_from") if spec.patterns_from else spec.patterns
            )
            try:
                groups = _compile_patterns(raw_patterns, spec.ignore_case, spec.name)
            except ValueError as e:
                raise ItemCheckConfigError(str(e)) from e
        when_keys = {_fold(w, "exact") for w in spec.when_in} if spec.when_in is not None else None
        if spec.type == "not_contains":
            raw = _ref_list(values, spec.terms_from, spec, "terms_from") if spec.terms_from else (spec.terms or [])
            terms = [t for t in (_fold(x, "folded") for x in raw if not _empty(x)) if t]
            # THE shared matcher (matrx_graph.text_match): whole words, run-together names, symbols
            # kept, web addresses as their host; HTML read as its visible text, as `folded` does.
            matcher = TermMatcher(
                [(str(x), None) for x in raw if not _empty(x) and _fold(x, "folded")],
                strip_html=True,
                fuzzy=FuzzyRule(spec.fuzzy, spec.fuzzy_min_length, spec.fuzzy_min_length)
                if spec.fuzzy is not None else None,
            )
            wordless = [t for t in terms if not re.search(r"\w", t)]
            if wordless:
                raise ItemCheckConfigError(
                    f"Check '{spec.name}': terms {wordless[:5]} have no letters or digits, so they could never match."
                )
        seen: dict[str, int] = {}
        for i, item in enumerate(items):
            if spec.type in _SET_TYPES and reasons[i]:
                continue
            if when_keys is not None:
                gate = _dig(item, spec.when_path or "")
                if gate is _MISSING or gate is None or _fold(gate, "exact") not in when_keys:
                    continue
            value = _dig(item, spec.path)
            if spec.type == "required":
                if _empty(value):
                    miss(i, spec, "missing", f"'{spec.path or 'item'}' is missing or empty.")
                continue
            if _empty(value):
                if not spec.optional:
                    miss(i, spec, "missing", f"'{spec.path or 'item'}' is missing or empty.")
                continue
            for v in _values_of(value):
                if spec.type == "verbatim":
                    assert verb is not None
                    texts = verb.texts_for(item)
                    if texts is None:
                        miss(i, spec, "no_source", f"no text was sent for {spec.source_by} "
                             f"'{_dig(item, spec.source_by or '')}'.")
                        break
                    q = _fold(v, mode)
                    if not q or not any(q in t for t in texts):
                        miss(i, spec, "not_verbatim", f"'{str(v)[:120]}' is not in the text sent.")
                        break
                elif spec.type == "in_set":
                    if _fold(v, mode) not in (allowed_keys or set()):
                        miss(i, spec, "not_in_set", f"'{str(v)[:120]}' is not one of the allowed values.")
                        break
                elif spec.type in ("once", "same_set"):
                    k = _fold(v, mode)
                    seen[k] = seen.get(k, 0) + 1
                    if allowed_keys is not None and k not in allowed_keys:
                        miss(i, spec, "unknown", f"id '{k}' was never sent.")
                    elif seen[k] > 1:
                        miss(i, spec, "duplicate", f"id '{k}' appears more than once; the first is kept.")
                elif spec.type == "max_length":
                    n = length_of(v if isinstance(v, str) else str(v), spec.unit)
                    if spec.max is not None and n > spec.max:
                        miss(i, spec, "too_long", f"{n:,} {spec.unit}; at most {_fmt(spec.max)}.")
                        break
                elif spec.type == "pattern":
                    text = " ".join((v if isinstance(v, str) else _fold(v, "exact")).split())
                    if len(text) > spec.max_text_chars:
                        miss(i, spec, "text_too_long", f"{len(text):,} characters; a pattern reads at most "
                             f"{spec.max_text_chars:,} (`max_text_chars`).")
                        break
                    hit = _pattern_hit(groups, text)
                    if spec.mode == "must" and hit is None:
                        miss(i, spec, "no_pattern_match", f"'{text[:120]}' matches none of the patterns.")
                        break
                    if spec.mode == "must_not" and hit is not None:
                        miss(i, spec, "matches_pattern", f"'{text[:120]}' matches '{hit[:120]}'.")
                        break
                elif spec.type == "not_contains":
                    hits, near = matcher.scan(_fold(v, "folded"))
                    if hits:
                        first = min(hits, key=lambda m: m.term_index)
                        miss(i, spec, "contains_term", f"contains '{first.term}'.")
                        break
                    if near:
                        first = min(near, key=lambda m: m.term_index)
                        if spec.fuzzy_drops:
                            miss(i, spec, "contains_term", f"contains '{first.matched_text}' (near '{first.term}').")
                            break
                        if not any(f.index == i and f.check == spec.name for f in flagged):
                            flagged.append(FlaggedItem(
                                index=i, check=spec.name, term=first.term,
                                matched_text=first.matched_text, score=first.ratio or 0.0,
                            ))
        if spec.type in ("once", "same_set"):
            report = SetReport(
                unknown=sorted(k for k in seen if allowed_keys is not None and k not in allowed_keys),
                duplicate=sorted(k for k, n in seen.items() if n > 1),
            )
            if spec.type == "same_set" and allowed is not None:
                order = [_fold(a, mode) for a in allowed]
                report.missing = [k for k in dict.fromkeys(order) if k not in seen]
                if report.missing and spec.on_fail == "fail" and spec.name not in failed:
                    failed.append(spec.name)
            sets[spec.name] = report

    kept: list[JsonValue] = []
    rejected: list[RejectedItem] = []
    counts: dict[str, int] = {f"{s.name}:{code}": 0 for s in specs for code in _CODES[s.type]}
    for i, item in enumerate(items):
        if not reasons[i]:
            kept.append(item)
            continue
        rejected.append(RejectedItem(index=i, item=item, reasons=reasons[i]))
        for code in dict.fromkeys(f"{r.check}:{r.code}" for r in reasons[i]):
            counts[code] = counts.get(code, 0) + 1
    passed = not rejected and not failed and not any(r.missing for r in sets.values())
    return ItemsCheckResult(
        items=kept, rejected=rejected, kept=len(kept), dropped=len(rejected), total=len(items),
        counts=counts, sets=sets, failed_checks=failed, passed=passed,
        flagged=flagged, flagged_count=len(flagged),
    )


__all__ = [
    "STARTING_TOLERANCE_PCT",
    "FlaggedItem",
    "ItemCheckConfigError",
    "MAX_PATTERNS",
    "ItemCheckReason",
    "ItemCheckSpec",
    "ItemsCheckResult",
    "RejectedItem",
    "SetReport",
    "check_items",
    "parse_item_checks",
    "flat",
    "folded",
    "ResponseCheckMeasure",
    "ResponseCheckResult",
    "ResponseCheckSpec",
    "UnknownHostCheckError",
    "configure_host_checks",
    "configure_host_projections",
    "project",
    "project_plain",
    "registered_host_checks",
    "registered_host_projections",
    "run_checks",
    "text_metrics",
]
