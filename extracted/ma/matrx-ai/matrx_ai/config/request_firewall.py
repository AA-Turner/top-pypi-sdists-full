"""THE REQUEST FIREWALL — refuse a mandate call whose fully rendered request carries what must not reach the model.

WHY. Some jobs have a rule only the finished request can prove: a blind judge must not see which
answer is the champion's, an agent under construction must not see its held-out test cases, a
summarizer must not see privileged documents. Input gates cannot prove it — a Holder's own system
prompt, its attached resources, term lists or the per-turn context channel can carry the term no
matter how the inputs were built. This module scans the request exactly as it will be sent and
refuses BEFORE anything is spent.

WHAT IS SCANNED. Every string value of ``UnifiedConfig.to_dict()`` (system, every message, the
dictionary, tool declarations) AND the per-turn context channel
(``MessageList.render_turn_context``: attachments, sandbox briefing, deferred-context manifest,
earlier-turn context). 🚨 ``to_dict`` does NOT carry the context channel — the translator renders
it into the provider's system channel — so a scan of ``to_dict`` alone is blind to exactly the
ambient context a firewall exists to stop. Structural JSON keys are never matched (a setting named
``stream`` is not the product "Stream"); the hash covers the whole rendered request.

THE TERM NEVER ECHOES. A refusal names the hit CLASS, the term's 1-based position in the list and
the request hash — never the term. Refusals land in step errors, run records, logs and error
queues that people and other agents read, and the list itself is often the secret (held-out test
cases, a privileged party's name). Whoever holds the list can find the term by its position.

WHERE IT RUNS — two layers, each refusing alone. A caller (the workflow ``ai.mandate.start``
step, or code) opens :func:`request_firewall_scope`; with no scope open every check below pays one
ContextVar read and nothing else.

1. THE SEND BOUNDARY (the wall). :func:`check_at_send` runs inside
   ``matrx_ai.config.send_boundary.prepare_for_send`` — the one place every wire-facing mutation
   passes, on every loop turn and every retry — on the EXACT outgoing wire config, after every
   step that adds to it (response format, observational memory, group view, remarks and surface
   notes, picked shapes, agent identity, live plan, tool results of earlier turns). Nothing
   reaches a provider after this scan. A ``no_auto_context`` firewall only a door can prove: with
   no door record on the scope, the boundary refuses BEFORE the call (it cannot see the switch).
2. THE DOORS (the records). The host calls :func:`check_request` at its last step before the
   request is assembled (``prepare_agent_run``, the programmatic hook, the batch render) — the
   door knows whether automatic context was closed, and its record names the door.

A path that cannot be scanned call by call (a whole-workflow Holder, a compiled Orchestra whose
members run detached, a provider batch body sent hours later) refuses while a scope is open.

WHAT CANNOT BE SCANNED REFUSES. A term with no letters or digits, or one written in a script the
shared matcher cannot find inside unspaced text, refuses the step at its start
(:func:`firewall_from_step_fields`; the refusal states the count, never the terms). A request
carrying files or images while a term list is set refuses: their contents are not text here.

THE PLATFORM DOES NOT DESCRIBE ITSELF to a firewalled call (owner ruling, 2026-10-27). While a
term list is open (:func:`self_description_withheld`), the context frame's note drops "the AI
Matrx platform" and the who-made-this-agent note is not staged — at the one place each is added.
The scan is unchanged: a term the request still carries (a value, a document) refuses.
"""

from __future__ import annotations

import contextlib
import contextvars
import hashlib
import html
import json
import unicodedata
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any, Literal

from matrx_graph.text_match import TermMatcher
from matrx_utils import register_detached_context_carrier, register_detached_work_guard
from pydantic import BaseModel, ConfigDict, Field

FirewallMatch = Literal["exact", "folded"]


class FirewallTerm(BaseModel):
    """One term that must not reach the model, with the class a refusal names instead of it."""

    model_config = ConfigDict(extra="forbid", populate_by_name=True)

    term: str = Field(min_length=1, description="The words that must not appear in the request.")
    term_class: str = Field(
        default="term",
        alias="class",
        description="What kind of term this is (e.g. 'brand', 'test_case'). A refusal names this, never the term.",
    )
    match: Literal["any", "proper_name_only"] | None = Field(
        default=None,
        description=(
            "proper_name_only: a brand that is also an everyday word ('Render') hits only where it is "
            "written as a name, never in 'Render times got slow' (matrx_graph.text_match)."
        ),
    )


class RequestFirewall(BaseModel):
    """What a request must not carry, and the channels it must not have open."""

    model_config = ConfigDict(extra="forbid")

    must_not_contain: list[FirewallTerm] = Field(default_factory=list)
    match: FirewallMatch = "folded"
    no_tools: bool = False
    no_auto_context: bool = False

    @property
    def active(self) -> bool:
        return bool(self.must_not_contain) or self.no_tools or self.no_auto_context


class UnmatchableFirewallTerms(ValueError):
    """A step's term list carries terms the firewall cannot find. States the count, never the terms."""

    def __init__(self, count: int, total: int) -> None:
        self.count = count
        self.total = total
        super().__init__(
            f"Refused at step start: {count} of the {total} terms that must not reach the model "
            "cannot be matched (no letters or digits, or a script the matcher cannot find inside "
            "unspaced text). A term the firewall cannot find would pass unchecked. Remove or "
            "rewrite them. Nothing was sent or spent."
        )


#: Scripts written without spaces between words. A term in one of them is only matchable when
#: the shared matcher finds it INSIDE a run of the same script, not just as a whole word.
_UNSPACED_SCRIPTS = (
    "CJK", "HIRAGANA", "KATAKANA", "HANGUL", "THAI", "LAO", "KHMER", "MYANMAR", "TIBETAN", "YI ",
)


def _unspaced_script(ch: str) -> bool:
    name = unicodedata.name(ch, "")
    return any(name.startswith(prefix) for prefix in _UNSPACED_SCRIPTS)


def unmatchable_terms(firewall: RequestFirewall) -> list[int]:
    """1-based positions of the terms ``firewall`` could never find in a request.

    ``exact`` matches the literal characters, so only a blank term is unmatchable there. ``folded``
    uses THE shared matcher: a term it skips (no letters or digits — "++") or that does not find
    itself is unmatchable; a term in an unspaced script ("北京") must also be found inside a run of
    its own script ("总部在北京"), since that is how such text is written."""
    if firewall.match == "exact":
        return [i for i, t in enumerate(firewall.must_not_contain, 1) if not t.term.strip()]
    bad: list[int] = []
    for i, t in enumerate(firewall.must_not_contain, 1):
        term = t.term.strip()
        single = RequestFirewall(must_not_contain=[FirewallTerm(term=term, match=t.match)])
        probes = [f"x {term} x"]
        if term and (_unspaced_script(term[0]) or _unspaced_script(term[-1])):
            probes.append(f"{term[-1]}{term}{term[0]}")
        if not term or not all(find_hits(probe, single) for probe in probes):
            bad.append(i)
    return bad


def firewall_from_step_fields(
    must_not_contain: list[str | FirewallTerm] | None,
    *,
    match: FirewallMatch = "folded",
    no_tools: bool = False,
    no_auto_context: bool = False,
) -> RequestFirewall | None:
    """The firewall a step's fields declare, or None when they declare nothing (the no-op).

    Raises :class:`UnmatchableFirewallTerms` (the count, never the terms) when any term could never
    be found — a term the matcher silently skips would read as scanned and pass anything."""
    terms = [
        FirewallTerm(term=t) if isinstance(t, str) else t
        for t in (must_not_contain or [])
        if not (isinstance(t, str) and not t.strip())
    ]
    firewall = RequestFirewall(
        must_not_contain=terms, match=match, no_tools=no_tools, no_auto_context=no_auto_context
    )
    bad = unmatchable_terms(firewall)
    if bad:
        raise UnmatchableFirewallTerms(len(bad), len(terms))
    return firewall if firewall.active else None


@dataclass(frozen=True, slots=True)
class FirewallRecord:
    """What one cleared dispatch was scanned for — never the terms themselves."""

    request_hash: str
    scanned_chars: int
    term_count: int
    match: str
    no_tools: bool
    no_auto_context: bool
    door: str
    mandate_key: str | None

    def to_dict(self) -> dict[str, Any]:
        return {
            "request_sha256": self.request_hash,
            "scanned_chars": self.scanned_chars,
            "term_count": self.term_count,
            "match": self.match,
            "no_tools": self.no_tools,
            "no_auto_context": self.no_auto_context,
            "door": self.door,
            "mandate_key": self.mandate_key,
        }


class RequestFirewallRefused(Exception):
    """The firewall refused a request before it was sent. Carries classes and positions, never terms."""

    def __init__(
        self,
        sentence: str,
        *,
        request_hash: str,
        hit_classes: tuple[str, ...] = (),
        hit_positions: tuple[int, ...] = (),
        door: str = "",
    ) -> None:
        self.request_hash = request_hash
        self.hit_classes = hit_classes
        self.hit_positions = hit_positions
        self.door = door
        tail = f" (request sha256 {request_hash})" if request_hash else ""
        super().__init__(f"{sentence} Nothing was sent or spent.{tail}")


@dataclass
class FirewallScope:
    """One caller's firewall and what the doors and the send boundary did with it.

    ``records`` are DOOR records (a door saw the auto-context switch); ``sends`` are the send
    boundary's, one per provider call that cleared."""

    firewall: RequestFirewall
    mandate_key: str | None = None
    records: list[FirewallRecord] = field(default_factory=list)
    sends: list[FirewallRecord] = field(default_factory=list)
    refusals: list[RequestFirewallRefused] = field(default_factory=list)


_ACTIVE: contextvars.ContextVar[FirewallScope | None] = contextvars.ContextVar(
    "matrx_ai_request_firewall", default=None
)


def active_request_firewall() -> FirewallScope | None:
    return _ACTIVE.get()


def self_description_withheld() -> bool:
    """True while an open scope lists terms that must not reach the model (owner ruling,
    2026-10-27): the platform's notes about ITSELF — the context frame's "the AI Matrx platform"
    and the who-made-this-agent note — are left out of the request where they are added
    (``message_config._turn_context_note``, ``send_boundary._stage_agent_identity``). A blind
    writer gains nothing from them, and a blind run about any brand sharing words with our
    platform must be able to run. The scan is never weakened: everything that IS sent is checked."""
    scope = _ACTIVE.get()
    return scope is not None and bool(scope.firewall.must_not_contain)


@contextlib.contextmanager
def request_firewall_scope(
    firewall: RequestFirewall | None, *, mandate_key: str | None = None
) -> Iterator[FirewallScope | None]:
    """Every provider call inside this block is checked against ``firewall`` (None = no-op)."""
    if firewall is None or not firewall.active:
        yield None
        return
    scope = FirewallScope(firewall=firewall, mandate_key=mandate_key)
    token = _ACTIVE.set(scope)
    try:
        yield scope
    finally:
        _ACTIVE.reset(token)


# ── Rendering and matching ──────────────────────────────────────────────────────────────────


def _rendered(owner: Any, method: str) -> Any:
    render = getattr(owner, method, None)
    return render() if callable(render) else None


def _rendered_dictionary(config: Any) -> list[str] | None:
    """The Custom Dictionary block as a translator renders it into the system channel (both
    shapes: the tool-capable model's and the terse pronunciation directive)."""
    raw = getattr(config, "dictionary", None)
    if raw is None:
        return None
    from matrx_ai.config.dictionary_config import DictionaryConfig

    dictionary = DictionaryConfig.coerce(raw)
    if dictionary is None or dictionary.is_empty:
        return None
    return [dictionary.render_for_system(supports_tools=flag) for flag in (True, False)]


#: EVERY channel a provider translator renders from a ``UnifiedConfig``, beside ``to_dict``:
#: ``BaseTranslator.get_system_text`` (resolved system instruction + dictionary + turn context),
#: ``get_trailing_context_text`` (turn context + the TAIL channel — the live plan after a tool
#: result). A new channel added to the wire must be added here; the guard
#: ``tests/test_request_firewall_at_send.py::test_the_scan_covers_every_word_a_translator_sends``
#: renders a request through every chat translator and fails on any word the scan did not see.
SCANNED_CHANNELS = ("config", "turn_context", "tail_context", "system", "dictionary")


def rendered_request_text(config: Any) -> str:
    """The request as one canonical string: ``to_dict`` AND every channel a translator renders
    (:data:`SCANNED_CHANNELS`). A rendered provider body (a dict) is scanned as it is."""
    if isinstance(config, dict):
        channels: dict[str, Any] = {"config": config}
    else:
        to_dict = getattr(config, "to_dict", None)
        messages = getattr(config, "messages", None)
        channels = {
            "config": to_dict() if callable(to_dict) else config,
            "turn_context": _rendered(messages, "render_turn_context"),
            "tail_context": _rendered(messages, "render_tail_context"),
            "system": getattr(config, "resolved_system_instruction", None),
            "dictionary": _rendered_dictionary(config),
        }
    return json.dumps(channels, sort_keys=True, default=str, ensure_ascii=False)


def _string_values(value: Any) -> Iterator[str]:
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for v in value.values():
            yield from _string_values(v)
    elif isinstance(value, (list, tuple)):
        for v in value:
            yield from _string_values(v)


def find_hits(words: str, firewall: RequestFirewall) -> list[tuple[int, str]]:
    """(1-based position, class) of every term present. ``exact``: the literal characters
    anywhere; ``folded``: THE shared matcher (``matrx_graph.text_match``), accent-blind — whole
    words, run-together names ("AIMatrx" = "AI Matrx"), symbols kept ("C++" is never a lone "c"),
    web addresses as their host, HTML read as text ("<b>Ac</b>me" is "Acme", entities as their
    character: "Ac&shy;me" is "Acme"), a one-word term written as two adjacent words ("Ac me")
    — the matcher's rule, so ``text.term_scan`` and ``data.check_items`` agree. A firewall has no
    near-miss mode: only a real hit refuses.

    OUT OF SCOPE, said plainly: encodings a person must decode to read — leetspeak ("4cme"),
    base64 ("QWNtZQ=="), reversed text ("emcA"), translations and descriptions of the term. The
    firewall stops the words, not every way of hinting at them."""
    hits: list[tuple[int, str]] = []
    if firewall.match == "exact":
        for i, t in enumerate(firewall.must_not_contain, 1):
            if t.term in words:
                hits.append((i, t.term_class))
        return hits
    terms = firewall.must_not_contain
    # Entities read as their character BEFORE the matcher folds: "Ac&shy;me" is a soft hyphen,
    # which the matcher drops like any invisible format character.
    if "&" in words:
        words = html.unescape(words)
    # The list position rides as the class, so every entry stays its own term (the matcher
    # merges entries that fold alike within one class) and a hit maps back to its position.
    found, _near = TermMatcher(
        [(t.term, str(i), t.match) for i, t in enumerate(terms, 1)], strip_accents=True, strip_html=True
    ).scan(words)
    positions = {int(m.term_class or 0) for m in found}
    for i in sorted(positions):
        hits.append((i, terms[i - 1].term_class))
    return hits



#: Provider-hosted capabilities a ``UnifiedConfig`` switches on — each a tool the model can use
#: to look anything up. (No code-execution switch exists on ``UnifiedConfig``.)
HOSTED_TOOL_SWITCHES = ("internal_web_search", "internal_url_context", "internal_x_search")


def _tool_count(config: Any) -> int:
    """Every tool the model can call: registered, custom, MCP servers and provider-hosted ones.
    A rendered provider body (a dict) counts its ``tools`` and ``mcp_servers``."""
    if isinstance(config, dict):
        return _body_tool_count(config)
    count = sum(
        len(list(getattr(config, name, None) or []))
        for name in ("tools", "custom_tools", "mcp_servers")
    )
    return count + sum(1 for name in HOSTED_TOOL_SWITCHES if getattr(config, name, None))


#: Keys under which a rendered provider body declares tools, at any depth: OpenAI / Anthropic
#: ``tools``, Google ``tools`` (top level or inside ``config`` / ``generationConfig``) with
#: ``functionDeclarations`` / ``googleSearch`` / ``urlContext`` / ``codeExecution`` entries.
_BODY_TOOL_KEYS = frozenset({"tools", "mcp_servers", "function_declarations", "functionDeclarations"})


def _body_tool_count(value: Any) -> int:
    if isinstance(value, dict):
        return sum(
            (len(v) if k in _BODY_TOOL_KEYS and isinstance(v, (list, tuple)) else 0) + _body_tool_count(v)
            for k, v in value.items()
        )
    if isinstance(value, (list, tuple)):
        return sum(_body_tool_count(v) for v in value)
    return 0


#: Content-part types whose contents are not text in the request (files, images, audio, video).
_BINARY_PART_TYPES = frozenset(
    {
        "image", "audio", "video", "document", "media", "youtube_video", "file",
        "image_url", "input_image", "input_file", "input_audio",
    }
)
_BINARY_PART_KEYS = ("inline_data", "file_data")
#: ``UnifiedConfig`` media inputs (MediaRef) — sent as files, never as text.
_MEDIA_INPUT_FIELDS = ("image_input", "image_inputs", "mask", "last_frame_image", "video_input",
                       "reference_images", "frame_images")


def _binary_part_count(config: Any, payload: Any) -> int:
    """How many files, images, audio or video parts the request carries."""

    def walk(value: Any) -> int:
        if isinstance(value, dict):
            own = 1 if value.get("type") in _BINARY_PART_TYPES or any(k in value for k in _BINARY_PART_KEYS) else 0
            return own + sum(walk(v) for v in value.values())
        if isinstance(value, (list, tuple)):
            return sum(walk(v) for v in value)
        return 0

    media = 0 if isinstance(config, dict) else sum(
        len(v) if isinstance(v, (list, tuple)) else 1
        for v in (getattr(config, name, None) for name in _MEDIA_INPUT_FIELDS)
        if v
    )
    return walk(payload) + media


def check_request(
    config: Any,
    firewall: RequestFirewall,
    *,
    auto_context_disabled: bool,
    door: str,
    mandate_key: str | None = None,
) -> FirewallRecord:
    """Refuse (raise :class:`RequestFirewallRefused`) or return the record of what was cleared."""
    text = rendered_request_text(config)
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    who = f"mandate {mandate_key!r}" if mandate_key else "this call"
    payload = json.loads(text)
    if firewall.no_auto_context and not auto_context_disabled:
        raise RequestFirewallRefused(
            f"Refused {who}: this step says no automatic context, but the run had automatic "
            "context open. Turn off automatic context on the agent that does the job.",
            request_hash=digest,
            door=door,
        )
    tools = _tool_count(config)
    if firewall.no_tools and tools:
        raise RequestFirewallRefused(
            f"Refused {who}: this step says no tools, but the agent doing the job carries "
            f"{tools} tool(s). Give the job to an agent with no tools.",
            request_hash=digest,
            door=door,
        )
    if firewall.must_not_contain:
        files = _binary_part_count(config, payload)
        if files:
            raise RequestFirewallRefused(
                f"Refused {who}: the request carries {files} file(s), image(s) or recording(s), "
                "whose contents the firewall cannot read, while this step lists terms that must "
                "not reach the model. Send their text instead, or remove them.",
                request_hash=digest,
                door=door,
            )
        words = "\n".join(_string_values(payload))
        hits = find_hits(words, firewall)
        if hits:
            classes = tuple(sorted({c for _, c in hits}))
            positions = tuple(p for p, _ in hits)
            raise RequestFirewallRefused(
                f"Refused {who}: the request about to be sent contains {len(hits)} of the "
                f"{len(firewall.must_not_contain)} terms that must not reach the model "
                f"(class {', '.join(classes)}; list position {', '.join(map(str, positions))}).",
                request_hash=digest,
                hit_classes=classes,
                hit_positions=positions,
                door=door,
            )
    return FirewallRecord(
        request_hash=digest,
        scanned_chars=len(text),
        term_count=len(firewall.must_not_contain),
        match=firewall.match,
        no_tools=firewall.no_tools,
        no_auto_context=firewall.no_auto_context,
        door=door,
        mandate_key=mandate_key,
    )


# ── The send boundary and the doors that cannot be scanned ──────────────────────────────────

#: The door name the send boundary's records and refusals carry.
SEND_BOUNDARY_DOOR = "send_boundary"


def check_at_send(
    config: Any, *, door: str = SEND_BOUNDARY_DOOR, record: bool = True
) -> FirewallRecord | None:
    """THE WALL — called by ``send_boundary.prepare_for_send`` on the exact outgoing config of EVERY
    provider call (each loop turn, each retry), and again (``record=False``) by
    ``UnifiedAIClient._dispatch_with_billing_net`` on the wire copy the client shaped after the
    boundary (message flags, capability gates). No scope open → None after one ContextVar read.

    Refuses (raises :class:`RequestFirewallRefused`, recorded on the scope) BEFORE the call when the
    request carries a term, a tool or a file the firewall forbids — or, for ``no_auto_context``,
    when no door has proved the run's automatic context closed (only a door sees that switch)."""
    scope = _ACTIVE.get()
    if scope is None:
        return None
    mandate_key = scope.mandate_key or next((r.mandate_key for r in scope.records if r.mandate_key), None)
    try:
        if scope.firewall.no_auto_context and not scope.records:
            who = f"mandate {mandate_key!r}" if mandate_key else "this call"
            raise RequestFirewallRefused(
                f"Refused {who}: this step says no automatic context, but this call reached the "
                "provider through a path where no door checked whether automatic context was "
                "closed. Report it: the path that started this call skips the dispatch door.",
                request_hash=hashlib.sha256(rendered_request_text(config).encode("utf-8")).hexdigest(),
                door=door,
            )
        cleared = check_request(
            config,
            scope.firewall,
            # A door already refused any run with automatic context open (see above).
            auto_context_disabled=True,
            door=door,
            mandate_key=mandate_key,
        )
    except RequestFirewallRefused as refusal:
        scope.refusals.append(refusal)
        raise
    if record:
        scope.sends.append(cleared)
    return cleared


def refuse_unscannable_call(what: str, *, door: str) -> None:
    """A paid call whose input is not a config the firewall can read (speech, rerank documents,
    embeddings) — refused while a term list is open. No scope, or no terms → returns."""
    scope = _ACTIVE.get()
    if scope is None or not scope.firewall.must_not_contain:
        return
    who = f"mandate {scope.mandate_key!r}" if scope.mandate_key else "this call"
    refusal = RequestFirewallRefused(
        f"Refused {who}: this step lists terms that must not reach the model, and {what} sends "
        "input the firewall cannot read.",
        request_hash="",
        door=door,
    )
    scope.refusals.append(refusal)
    raise refusal


def _refuse_detached_work(what: str) -> None:
    """The matrx-utils detached-work guard: nothing leaves for a place this scope cannot follow."""
    scope = _ACTIVE.get()
    if scope is None:
        return
    who = f"mandate {scope.mandate_key!r}" if scope.mandate_key else "this call"
    refusal = RequestFirewallRefused(
        f"Refused {who}: it has a request firewall, and it tried to start {what}, which runs "
        "outside the check every AI call passes. Run that work without the firewall, or put the "
        "firewall on its own AI steps.",
        request_hash="",
        door="detached_work",
    )
    scope.refusals.append(refusal)
    raise refusal


# The scope follows every detached task (``matrx_utils.detached_task`` carries only registered
# variables), so background AI work started under a firewall is still checked at its own send;
# work handed to a place it cannot follow (a long-lived detached run, another process's queue)
# is refused before it leaves.
register_detached_context_carrier(_ACTIVE)
register_detached_work_guard(_refuse_detached_work)


def refuse_unscannable_path(what: str, *, door: str) -> None:
    """Refuse a path whose AI calls cannot be checked one by one, when a firewall scope is open.

    ``what`` names the path in plain words ("an Orchestra (a Conductor and its members)"). The
    sentence matches the workflow-Holder refusal of the Run Mandate step. No scope → returns."""
    scope = _ACTIVE.get()
    if scope is None:
        return
    who = f"mandate {scope.mandate_key!r}" if scope.mandate_key else "this call"
    refusal = RequestFirewallRefused(
        f"Refused {who}: it has a request firewall, but this job is done by {what}, whose many AI "
        "calls this step cannot check. Give the job to an agent, or put the firewall on the AI "
        "steps inside it.",
        request_hash="",
        door=door,
    )
    scope.refusals.append(refusal)
    raise refusal


__all__ = [
    "HOSTED_TOOL_SWITCHES",
    "SEND_BOUNDARY_DOOR",
    "UnmatchableFirewallTerms",
    "SCANNED_CHANNELS",
    "check_at_send",
    "refuse_unscannable_call",
    "refuse_unscannable_path",
    "unmatchable_terms",
    "FirewallMatch",
    "FirewallRecord",
    "FirewallScope",
    "FirewallTerm",
    "RequestFirewall",
    "RequestFirewallRefused",
    "active_request_firewall",
    "check_request",
    "find_hits",
    "firewall_from_step_fields",
    "rendered_request_text",
    "request_firewall_scope",
    "self_description_withheld",
]
