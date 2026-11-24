"""Generated skills for every tool and every data-declared combination (chat-agent-skills lane F).

Pure logic, no database: the host reads the registries, builds the facts below and writes the
results through the ONE skill write path (``matrx_ai.skills.ingest.upsert_parsed_skills``). The
same facts always produce the same bytes, so an unchanged source never rewrites its skill.

Four generated families, each a ``skill.definition`` row stamped in ``config``:

* a TOOL skill (``tool-<name>``): what the tool does, when to reach for it, its inputs, its own
  example call (only when the tool declares one), pitfalls true for THIS tool, and how to get it.
  ``allowed_tools = [tool id]`` and ``config.tool_definition_id`` link it to its tool.
* a FAMILY skill (``tools-family-<label>``): one skill for a cluster of catalog tools that differ
  only by the proper noun they target (one tool per store, per site…). Its members get no skill
  of their own; the coverage guard counts them covered by the family, like a bundle's lister.
* a BUNDLE skill (``tools-bundle-<bundle>``): a bundle's members, the shape each returns, and the
  lister that loads them. It is also the one skill of the bundle's lister tool.
* a SHAPE-TOOLS skill (``tools-for-shape-<kind>``): a registered shape and the tools whose declared
  output it is. ``config.kind_definition_id`` names the shape.

Every tool name in the text is the WIRE name the model sees (``matrx_ai.config.wire_names``).
A skill is never more visible than its tool: an admin-only or unpublished tool's skill is
unpublished, and a published combination never names one. Nothing here attaches a skill to an
agent or carries ``attach_with_tools``: these skills are found by search only. Owner rulings:
common-docs/systems/agents/agent-skills/VISION.md 15.
"""

from __future__ import annotations

import hashlib
import json
import re
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any

from matrx_ai.config.wire_names import to_wire_name

#: ``config.ingested_from`` of every row this module generates (ownership for the write path).
COVERAGE_SOURCE = "skill_coverage"
#: Bump when the templates change, so every generated row is rewritten once. Version 3 (lane F8) says
#: what a tool is FOR in the words people use (``ToolFacts.asked_as``, held as data on the tool row) and
#: names an MCP tool's service in its label; versions below 3 render exactly the version-2 bytes.
TEMPLATE_VERSION = 4
#: The version whose templates speak the person's words (see ``_v3``).
PEOPLE_WORDS_VERSION = 3

TOOL_PREFIX = "tool-"
FAMILY_PREFIX = "tools-family-"
BUNDLE_PREFIX = "tools-bundle-"
SHAPE_PREFIX = "tools-for-shape-"

TOOL_CATEGORY = {
    "slug": "tool-guides",
    "name": "Tool guides",
    "icon": "Wrench",
    "position": 71,
    "description": "One short guide per tool: what it does, when to use it, its inputs and how to get it.",
}
COMBO_CATEGORY = {
    "slug": "tool-combinations",
    "name": "Tool combinations",
    "icon": "Boxes",
    "position": 72,
    "description": "Tools that go together: a bundle's tools, or the tools that return one shape.",
}


def body_limit() -> int:
    from matrx_ai.skills.knobs import skill_knob_int

    return skill_knob_int("generated_skill_body_chars", 1500)  # KNOB MIRROR agents.context.generated_skill_body_chars


def description_limit() -> int:
    from matrx_ai.skills.knobs import skill_knob_int

    return skill_knob_int("generated_skill_description_chars", 200)  # KNOB MIRROR agents.context.generated_skill_description_chars


def family_min_members() -> int:
    from matrx_ai.skills.knobs import skill_knob_int

    return skill_knob_int("generated_family_min_members", 21)  # KNOB MIRROR agents.context.generated_family_min_members


def family_body_limit() -> int:
    from matrx_ai.skills.knobs import skill_knob_int

    return skill_knob_int("generated_family_body_chars", 24000)  # KNOB MIRROR agents.context.generated_family_body_chars


@dataclass(frozen=True)
class ToolFacts:
    id: str
    name: str
    description: str
    parameters: Any
    source_kind: str
    display_name: str | None = None
    job_key: str | None = None
    summary: str | None = None
    trap_notes: str | None = None
    output_kind: str | None = None
    side_effect_class: str | None = None
    admin_only: bool = False
    destructive: bool = False
    mcp_server_slug: str | None = None
    mcp_server_name: str | None = None
    bundles: tuple[str, ...] = ()
    published: bool = True
    #: the lister tools (internal names) of the bundles that hold this tool
    listers: tuple[str, ...] = ()
    #: catalog price in points (``tool.catalog_entry.price_hint_points``); None = unknown
    price_points: int | None = None
    #: plain-language run conditions from ``tool.definition.gating``
    requires: tuple[str, ...] = ()
    tags: tuple[str, ...] = ()
    #: set by the host when the tool belongs to a family skill
    family_skill: str | None = None
    family_label: str | None = None
    #: what people ask for when they need this tool, in their own words
    #: (``tool.definition.metadata.people_ask_for``; read by this generator only, never sent to a model)
    asked_as: tuple[str, ...] = ()


@dataclass(frozen=True)
class BundleFacts:
    id: str
    name: str
    description: str
    lister_id: str
    lister_name: str
    members: tuple[ToolFacts, ...]
    mcp_server_slug: str | None = None
    mcp_server_name: str | None = None
    published: bool = True


@dataclass(frozen=True)
class ShapeFacts:
    id: str
    kind: str
    label: str
    description: str | None
    producers: tuple[ToolFacts, ...]
    has_kind_skill: bool = True
    published: bool = True


@dataclass(frozen=True)
class FamilyFacts:
    skill_id: str
    label: str
    noun: str
    #: the shared sentence, its proper noun replaced by "one <noun>"
    what: str
    #: (proper noun, tool) per member, sorted by proper noun
    members: tuple[tuple[str, ToolFacts], ...]
    #: "catalog" (got through find_tools / use_tool) or "connector" (got through its service's lister)
    kind: str = "catalog"


@dataclass(frozen=True)
class GeneratedSkill:
    skill_id: str
    label: str
    description: str
    body: str
    category: str
    allowed_tools: tuple[str, ...]
    link: dict[str, Any] = field(default_factory=dict)
    published: bool = True

    @property
    def source_hash(self) -> str:
        payload = json.dumps(
            [TEMPLATE_VERSION, self.label, self.description, self.body, list(self.allowed_tools), self.link],
            sort_keys=True,
            ensure_ascii=False,
        )
        return hashlib.sha256(payload.encode("utf-8")).hexdigest()[:16]


# ---------------------------------------------------------------------------
# text helpers


_SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z`\"(])")
_WS = re.compile(r"\s+")


def slug(value: str) -> str:
    return re.sub(r"-{2,}", "-", re.sub(r"[^a-z0-9]+", "-", value.lower())).strip("-")


def wire(name: str) -> str:
    """The name the model sees for a tool (the ONE wire-name function)."""
    return to_wire_name(name)


def clean(text: str | None) -> str:
    return _WS.sub(" ", (text or "").replace(" ", " ")).strip()


def sentences(text: str | None) -> list[str]:
    return [s.strip() for s in _SENTENCE.split(clean(text)) if s.strip()]


def _balanced(text: str) -> bool:
    return (
        text.count("(") == text.count(")")
        and text.count("[") == text.count("]")
        and text.count("{") == text.count("}")
        and text.count("`") % 2 == 0
        and text.count('"') % 2 == 0
    )


_DANGLING = {"a", "an", "the", "to", "of", "and", "or", "for", "with", "by", "in", "on", "at", "from", "as", "its", "their", "your", "is", "are"}


def fit_words(text: str, limit: int, *, prefer_punctuation: bool = True) -> str | None:
    """``text`` cut at a clause boundary so it fits ``limit`` and is still a whole phrase: never a
    cut word, never an open bracket or quote, never a dangling article. ``None`` when no cut works."""
    text = clean(text).rstrip(" .;:,")
    if len(text) <= limit:
        return text
    cuts: list[tuple[int, int]] = []  # (priority, index); punctuation before prepositions
    for m in re.finditer(r";|,|:| —| - | \(", text):
        cuts.append((0, m.start()))
    for m in re.finditer(r" (?:and|or|with|by|for|from|to|in|on|at|as|so|that|which|when|where|using|via) ", text):
        cuts.append((1, m.start()))
    for prio in ((0, 1) if prefer_punctuation else (None,)):
        best = None
        for p, i in cuts:
            if (prio is not None and p != prio) or i > limit:
                continue
            cand = text[:i].rstrip(" ,;:—-")
            if len(cand) < limit * 0.45 or not _balanced(cand):
                continue
            if cand.split(" ")[-1].lower() in _DANGLING:
                continue
            if best is None or len(cand) > len(best):
                best = cand
        if best:
            return best
    return None


def clip(text: str, limit: int) -> str:
    """A whole phrase within ``limit`` (clause boundary), else whole words; never an ellipsis."""
    text = clean(text)
    if len(text) <= limit:
        return text
    fitted = fit_words(text, limit)
    if fitted:
        return fitted
    words = text[:limit].rsplit(" ", 1)[0].rstrip(" ,;:-(")
    while words and (not _balanced(words) or words.split(" ")[-1].lower() in _DANGLING):
        if " " not in words:
            break
        words = words.rsplit(" ", 1)[0].rstrip(" ,;:-(")
    return words


def first_sentences(text: str | None, limit: int) -> str:
    out = ""
    for s in sentences(text):
        nxt = f"{out} {s}".strip()
        if len(nxt) > limit:
            break
        out = nxt
    if out:
        return out
    first = clip(text or "", limit)
    return first if not first or first.endswith((".", "!", "?")) else first + "."


#: A line scoped to ONE action or argument ("- patch: …", "query: …", "1. …"): what it says is
#: true only of that action, never of the whole tool.
_SCOPED_LINE = re.compile(r"^\s*(?:[-*•]|\d+[.)])\s|^\s*[\w`][\w ,/|`'\-]{0,38}:\s")


def tool_wide_sentences(text: str | None) -> list[str]:
    """The sentences of a description that speak about the WHOLE tool (scoped lines dropped)."""
    out: list[str] = []
    for line in (text or "").splitlines():
        if not line.strip() or _SCOPED_LINE.match(line):
            continue
        out.extend(sentences(line))
    return out


#: MCP-style descriptions ("Use: … When: … Needs: … Do: … Avoid: …").
_FIELD = re.compile(r"(?:^|\n)\s*(Use|When|Needs|Do|Avoid|Returns)\s*:\s*", re.IGNORECASE)


def labelled_fields(text: str | None) -> dict[str, str]:
    raw = text or ""
    parts = _FIELD.split(raw)
    if len(parts) < 3:
        return {}
    out: dict[str, str] = {}
    for i in range(1, len(parts) - 1, 2):
        out[parts[i].lower()] = clean(parts[i + 1])
    return out


_BRACES = re.compile(r"\{\{(?!!)([^{}\s]+)\}\}")


def escape_variables(text: str) -> str:
    """Nothing in a generated text may be read as a variable: a space-free ``{{name}}`` becomes the
    one escape ``{{!name}}``; any other ``{{`` is split so it is no tag at all (VARIABLE RULE)."""
    text = _BRACES.sub(r"{{!\1}}", text)
    return re.sub(r"\{\{(?!!)", "{ {", text)


_VERBS = {
    "add", "analyze", "analyse", "append", "apply", "approve", "archive", "ask", "assign", "attach", "browse",
    "build", "calculate", "call", "cancel", "capture", "change", "check", "clear", "click", "clone", "close",
    "compare", "compose", "compute", "configure", "connect", "convert", "copy", "count", "crawl", "create",
    "deactivate", "delete", "describe", "design", "detach", "detect", "discover", "download", "draft", "drag",
    "edit", "email", "emit", "enable", "disable", "estimate", "evaluate", "execute", "explain", "export",
    "extract", "fetch", "fill", "find", "focus", "format", "generate", "get", "grant", "identify", "import",
    "insert", "inspect", "install", "invite", "invoke", "link", "list", "load", "look", "lookup", "make",
    "manage", "map", "mark", "measure", "merge", "monitor", "move", "navigate", "notify", "open", "pause",
    "perform", "pin", "plan", "post", "preview", "print", "propose", "publish", "pull", "push", "put",
    "query", "rank", "read", "record", "register", "reload", "remove", "rename", "render", "reorder", "replace",
    "reply", "report", "request", "resolve", "restore", "resume", "retrieve", "return", "review", "revoke", "run",
    "save", "schedule", "scrape", "score", "scroll", "search", "see", "select", "send", "set", "share", "show",
    "sort", "start", "stop", "submit", "summarize", "sync", "take", "test", "toggle", "track", "transcribe",
    "translate", "trigger", "turn", "type", "undo", "unpin", "update", "upload", "upsert", "validate",
    "verify", "wait", "watch", "write",
}
#: words that start a noun phrase, never an imperative
_NOUN_LEADS = {
    "a", "an", "the", "one", "this", "that", "these", "those", "your", "our", "my", "its", "their", "what",
    "who", "how", "which", "whether", "current", "public", "full", "new", "all", "each", "every", "some",
    "any", "multiple", "several", "deep", "comments", "posts", "reviews",
}
#: a word right after an imperative verb
_OBJECT_LEADS = {
    "a", "an", "the", "one", "every", "each", "all", "its", "their", "your", "part", "some", "any", "this",
    "that", "these", "those", "multiple", "several", "up", "it", "them",
}


def _verb_form(word: str) -> str | None:
    w = word.lower().strip("`'\",:;")
    if w in _VERBS:
        return w
    for suffix, repl in (("ies", "y"), ("es", ""), ("s", "")):
        if w.endswith(suffix) and (w[: -len(suffix)] + repl) in _VERBS:
            return w[: -len(suffix)] + repl
    return None


def _imperative(words: list[str]) -> tuple[str, int] | None:
    """``(verb phrase, words consumed)`` when the phrase opens with an action, else None."""
    if not words:
        return None
    w0 = words[0].lower().strip("`'\"")
    nxt = words[1].lower().strip(",") if len(words) > 1 else ""
    after = words[2] if len(words) > 2 else ""
    if w0.rstrip(",") in _NOUN_LEADS:
        return None
    verb = _verb_form(w0)
    if verb:
        return (verb + ("," if w0.endswith(",") else "")), 1
    if w0.endswith("ly") and nxt and _verb_form(nxt):
        return f"{w0} {_verb_form(nxt)}", 2
    if re.fullmatch(r"[a-z]+", w0) and nxt in _OBJECT_LEADS and w0 not in ("for", "with", "from", "by", "in", "on"):
        return w0, 1
    if re.fullmatch(r"[a-z]+", w0) and nxt in ("and", "or") and after and after.lower() in _VERBS:
        return w0, 1
    return None


_LEAD_NOISE = re.compile(
    r"^(?:admins?(?: only)?\s*[:.\-—]\s*|"
    r"(?:this|the) (?:tool|api|function|endpoint)\s+(?:is used to|lets you|allows you to|can be used to|will)\s+)",
    re.I,
)
_USE_LEAD = re.compile(r"^(?:use (?:it|this(?: tool)?) (?:to|when|for)|use to|use for|use when|use\b)\s*:?\s*", re.I)


def trigger_description(job: str, *, fallback: str) -> str:
    """A whole "Use when …" sentence within ``description_limit()`` characters, from the first
    sentence of ``job``. Cut only at a clause boundary; never an ellipsis."""
    first = (sentences(job) or [clean(job)])[0] if clean(job) else ""
    # A sentence ends at ". " even before a lowercase word ("Chrome downloads. list: …"), and an
    # arrow starts a result sketch ("… -> {run_id}"), never part of a trigger.
    head = re.split(r"(?<=[a-z0-9)\]])[.!?]\s+|\s+->\s+", first)[0]
    if len(head) >= 15:
        first = head
    text = _LEAD_NOISE.sub("", _USE_LEAD.sub("", first)).rstrip(".").strip()
    if not text:
        text = fallback
    words = text.split(" ")
    imp = _imperative(words)
    if imp:
        verb, used = imp
        rest = " ".join(words[used:])
        phrase = f"Use when you need to {verb} {rest}".strip()
    elif re.match(r"^(when|if)\b", text, re.I):
        phrase = f"Use {text[0].lower() + text[1:]}"
    elif re.match(r"^you\b", text, re.I):
        phrase = f"Use when {text[0].lower() + text[1:]}"
    else:
        lead = text if words[0].isupper() and len(words[0]) > 1 else text[0].lower() + text[1:]
        phrase = f"Use when you need {lead}"
    limit = description_limit() - 1
    fitted = fit_words(phrase, limit)
    if not fitted:
        fitted = fit_words(f"Use when you need {clean(fallback)}", limit) or "Use when you need this tool"
    return escape_variables(fitted + ".")


# ---------------------------------------------------------------------------
# parameters


@dataclass(frozen=True)
class Param:
    name: str
    type: str
    required: bool
    hint: str
    spec: dict[str, Any]


def _type_of(spec: dict[str, Any]) -> str:
    t = spec.get("type")
    if isinstance(t, list):
        t = next((x for x in t if x != "null"), "any")
    if not t:
        for key in ("anyOf", "oneOf"):
            opts = spec.get(key)
            if isinstance(opts, list):
                types = [o.get("type") for o in opts if isinstance(o, dict) and o.get("type") not in (None, "null")]
                if types:
                    t = types[0]
                    break
    if t == "array" and isinstance(spec.get("items"), dict) and spec["items"].get("type"):
        return f"list of {spec['items']['type']}"
    return str(t or "any")


def params_of(parameters: Any) -> list[Param]:
    """Both stored shapes: a JSON-Schema object, or a flat ``name -> spec`` map with inline ``required``."""
    if not isinstance(parameters, dict):
        return []
    if isinstance(parameters.get("properties"), dict):
        props = parameters["properties"]
        required = set(parameters.get("required") or [])
    else:
        props = {k: v for k, v in parameters.items() if isinstance(v, dict)}
        required = {k for k, v in props.items() if v.get("required") is True}
    out: list[Param] = []
    for name, spec in props.items():
        if not isinstance(spec, dict) or name.startswith(("ui:", "_")):
            continue
        hint = first_sentences(spec.get("description") or spec.get("title") or "", 110)
        enum = spec.get("enum")
        if isinstance(enum, list) and enum and len(enum) <= 8:
            hint = f"{hint} One of: {', '.join(str(e) for e in enum)}.".strip()
        out.append(Param(name, _type_of(spec), name in required, hint, spec))
    out.sort(key=lambda p: (not p.required,))
    return out


def declared_example(parameters: Any, params: list[Param]) -> dict[str, Any] | None:
    """The tool definition's OWN example call: a top-level ``examples`` entry, else one built from
    each argument's declared ``examples``. ``None`` when the tool declares none (no placeholders)."""
    if isinstance(parameters, dict):
        top = parameters.get("examples")
        if isinstance(top, list) and top and isinstance(top[0], dict):
            return top[0]
    chosen = [p for p in params if p.required] or params[:1]
    out: dict[str, Any] = {}
    for p in chosen[:4]:
        ex = p.spec.get("examples")
        if not (isinstance(ex, list) and ex):
            return None
        out[p.name] = ex[0]
    return out or None


def _fence(obj: Any) -> str:
    return "```json\n" + json.dumps(obj, ensure_ascii=False) + "\n```"


def _input_lines(params: list[Param], cap: int = 8) -> list[str]:
    lines = [
        f"- `{p.name}` ({p.type}{', required' if p.required else ''}){' — ' + p.hint if p.hint else ''}"
        for p in params[:cap]
    ]
    if len(params) > cap:
        lines.append(f"_{len(params) - cap} more optional inputs; the tool's own schema lists them._")
    return lines or ["- None. Call it with `{}`."]


# ---------------------------------------------------------------------------
# tool skill


def _v3() -> bool:
    return TEMPLATE_VERSION >= PEOPLE_WORDS_VERSION


def service_of(t: ToolFacts) -> str | None:
    """The service an MCP tool runs on (its server's name), when it has one."""
    return clean(t.mcp_server_name or t.mcp_server_slug or "") or None


def tool_label(t: ToolFacts) -> str:
    if t.display_name:
        label = clean(t.display_name)
    else:
        base = t.name.split(".")[-1].split(":")[-1]
        label = clean(base.replace("_", " ").replace("-", " ")).capitalize() or t.name
    return label


def skill_label(t: ToolFacts) -> str:
    """``<label> (tool)``; from v3 an MCP tool's reads ``<label> (<service> tool)``. The service goes
    AFTER the tool's own words, never before them: a leading service name changes which word heads
    the name, and the offer's anchored-name rule reads the head word (a leading "Fibery:" let a
    database tool through on "you used the database", 2026-11-19)."""
    label = tool_label(t)
    service = service_of(t) if _v3() else None
    if service and service.lower() not in label.lower():
        return clip(f"{label} ({service} tool)", 300)
    return clip(f"{label} (tool)", 300)


def asked_as_of(value: Any) -> tuple[str, ...]:
    """``tool.definition.metadata.people_ask_for`` as clean phrases (a list of short strings; anything
    else reads as none)."""
    if not isinstance(value, (list, tuple)):
        return ()
    out: list[str] = []
    for v in value:
        phrase = clean(str(v)).rstrip(" .;,") if isinstance(v, str) else ""
        if phrase and phrase.lower() not in (p.lower() for p in out):
            out.append(phrase)
    return tuple(out)


def with_service(description: str, service: str | None) -> str:
    """A description that names the service its tool runs on (appended in brackets, the description
    shortened by whole phrases to make room)."""
    if not service or service.lower() in description.lower():
        return description
    core = description.rstrip(".")
    room = description_limit() - 1 - len(service) - 4
    return escape_variables(f"{clip(core, room)} ({service}).")


def _join_or(items: list[str]) -> str:
    return items[0] if len(items) == 1 else ", ".join(items[:-1]) + " or " + items[-1]


def people_description(t: ToolFacts, own: str) -> str | None:
    """Version-3 description: what people ask for, in their words, then the tool's own terms in
    brackets; whole phrases dropped from the end until it fits ``description_limit()``."""
    if not t.asked_as:
        return None
    limit = description_limit() - 1
    own_core = re.sub(r"^Use when you need (?:to )?", "", own).rstrip(".")
    service = service_of(t)
    for n in range(len(t.asked_as), 0, -1):
        lead = "Use when the person wants to " + _join_or(list(t.asked_as[:n]))
        if service and service.lower() not in lead.lower():
            lead += f" in {service}"
        room = limit - len(lead) - 3
        tail = own_core if len(own_core) <= room else ""
        if not tail and room >= 25:
            # The tool's own terms do not fit whole: its first clause, else whole words.
            first = re.split(r"[;,:(]| —| - ", own_core)[0].strip()
            tail = first if 12 <= len(first) <= room else clip(own_core, room)
        text = f"{lead} ({tail})" if tail and _balanced(tail) else lead
        if len(text) <= limit:
            return escape_variables(text + ".")
    return None


def _paid(t: ToolFacts) -> bool:
    return t.side_effect_class == "paid_read" or (t.price_points or 0) > 0


def conditional_pitfalls(t: ToolFacts, params: list[Param]) -> list[str]:
    """The template's own pitfall sentences, each emitted ONLY when its condition holds for ``t``."""
    out: list[str] = []
    req = [p.name for p in params if p.required]
    if req:
        out.append("Required: " + ", ".join(f"`{n}`" for n in req[:6]) + ". A call missing one is refused.")
    if t.destructive:
        out.append("It changes or deletes data: confirm with the person before calling it.")
    if _paid(t):
        out.append("It spends the person's points; `find_tools` shows the price.")
    if t.admin_only:
        out.append("Only platform admins can run it.")
    out.extend(t.requires)
    return out


def _pitfalls(t: ToolFacts, params: list[Param], fields: dict[str, str]) -> list[str]:
    out: list[str] = []
    if fields.get("avoid"):
        out.append("Avoid: " + clip(fields["avoid"], 170))
    if fields.get("do"):
        out.append(clip(fields["do"], 180))
    if t.trap_notes and clean(t.trap_notes):
        out.extend(clip(s, 180) for s in sentences(t.trap_notes)[:2])
    if not fields:
        for s in tool_wide_sentences(t.description)[1:]:
            if re.search(r"\buse (it|this|when|for|to)\b", s, re.I):
                continue
            if re.search(r"\b(never|do not|don't|must|only|avoid|requires?|before)\b", s, re.I):
                out.append(clip(s, 180))
            if len(out) >= 3:
                break
    out.extend(conditional_pitfalls(t, params))
    seen: set[str] = set()
    uniq = []
    for line in out:
        if line and line not in seen:
            seen.add(line)
            uniq.append(line)
    return uniq[:6]


def _how_to_get(t: ToolFacts) -> list[str]:
    w = wire(t.name)
    lines = [f"Holding `{w}`? Call it by that name."]
    if t.job_key:
        lines.append(
            f'Not holding it: `find_tools` with "{tool_label(t)}" adds it for your next step, or run it at once '
            f"with `use_tool`, job_key `{t.job_key}` and the inputs above."
        )
    elif t.listers:
        listers = ", ".join(f"`{wire(n)}`" for n in t.listers[:2])
        lines.append(f"Not holding it: call {listers} (no inputs) to load it with its family of tools.")
        if t.mcp_server_slug:
            server = t.mcp_server_name or t.mcp_server_slug
            lines.append(f"It runs on the person's {server} connection; if that is missing, ask them to connect it.")
    else:
        load = f' with ["{w}"]' if w == t.name else " with the name it lists"
        lines.append(
            f"Not holding it: when `load_tools` lists it, call `load_tools`{load}; it is ready on your next step. "
            "Otherwise it is not available to you here: say what it would do, never claim you ran it."
        )
    return lines


def _fit_body(parts: list[tuple[str, list[str]]], title: str, limit: int) -> str:
    """Assemble sections, dropping trailing list lines until the body fits ``limit``."""
    parts = [(h, list(lines)) for h, lines in parts]

    def render() -> str:
        chunks = [f"# {title}"]
        for heading, lines in parts:
            if not lines:
                continue
            chunks.append(f"## {heading}\n\n" + "\n".join(lines) if heading else "\n".join(lines))
        return escape_variables("\n\n".join(chunks) + "\n")

    body = render()
    order = ["Pitfalls", "Inputs", "Tools in it", "Tools that return it", "When to reach for it"]
    while len(body) > limit:
        for heading in order:
            sec = next((lines for h, lines in parts if h == heading and len(lines) > 1), None)
            if sec is not None:
                sec.pop(-2 if sec[-1].startswith("_") else -1)
                break
        else:
            # Shorten the free text of the first section as a last resort (whole phrases only).
            head, lines = parts[0]
            short = clip(lines[0], max(80, len(lines[0]) - (len(body) - limit) - 5))
            lines[0] = short if short.endswith((".", "!", "?")) else short + "."
            body = render()
            break
        body = render()
    return body


def build_tool_skill(t: ToolFacts) -> GeneratedSkill:
    params = params_of(t.parameters)
    fields = labelled_fields(t.description)
    wide = tool_wide_sentences(t.description)
    what_src = fields.get("use") or t.summary or " ".join(wide) or t.description
    what = first_sentences(what_src, 360) or f"The `{wire(t.name)}` tool."
    when: list[str] = []
    if _v3() and t.asked_as:
        when.append("- People ask for it as: " + "; ".join(f'"{p}"' for p in t.asked_as) + ".")
    if fields.get("when"):
        when.append(f"- {clip(fields['when'], 220)}")
    else:
        hits = [s for s in wide if re.search(r"\b(use (it|this|when|for)|use to)\b", s, re.I)]
        when.extend(f"- {clip(s, 220)}" for s in hits[:2])
    if t.output_kind:
        when.append(f"- It returns a `{t.output_kind}` shape (skill `kind_{t.output_kind}` explains its fields).")
    if fields.get("needs"):
        when.append(f"- You need first: {clip(fields['needs'], 160)}")
    example = declared_example(t.parameters, params)
    label = tool_label(t)
    body = _fit_body(
        [
            ("", [what]),
            ("When to reach for it", when),
            ("Inputs", _input_lines(params)),
            ("Example call", [_fence(example)] if example else []),
            ("Pitfalls", [f"- {p}" for p in _pitfalls(t, params, fields)]),
            ("How to get it", _how_to_get(t)),
        ],
        f"{label} (`{wire(t.name)}`)",
        body_limit(),
    )
    when_field = fields.get("when") or ""
    if when_field:
        when_field = "when " + when_field[0].lower() + when_field[1:]
    description = trigger_description(when_field or what_src or "", fallback=label)
    if _v3():
        service = service_of(t)
        description = people_description(t, description) or with_service(description, service)
    return GeneratedSkill(
        skill_id=TOOL_PREFIX + slug(t.name),
        label=skill_label(t),
        description=description,
        body=body,
        category=TOOL_CATEGORY["slug"],
        allowed_tools=(t.id,),
        link={"family": "tool", "tool_definition_id": t.id, "tool_name": t.name},
        published=t.published and not t.admin_only,
    )


# ---------------------------------------------------------------------------
# family skills: one skill for tools that differ only by the proper noun they target

_FAMILY_LEAD = re.compile(r"^(.*?)\s+(?:from|for|on|of|at|in|by|about)\s+<X>")


def family_subject(t: ToolFacts) -> str | None:
    """The proper noun a catalog tool targets: its display name minus the trailing noun
    ("CT Sounds products" -> "CT Sounds"), when the tool's own sentence names it."""
    if not (t.job_key and t.display_name):
        return None
    words = clean(t.display_name).split(" ")
    if len(words) < 2:
        return None
    subject = " ".join(words[:-1])
    return subject if subject.lower() in clean(t.summary or t.description).lower() else None


def masked_text(t: ToolFacts) -> str | None:
    subject = family_subject(t)
    if not subject:
        return None
    return re.sub(re.escape(subject), "<X>", clean(t.summary or t.description), flags=re.I)


def _family_noun(members: list[ToolFacts]) -> str:
    common = set(members[0].tags)
    for m in members[1:]:
        common &= set(m.tags)
    plural = sorted(t for t in common if t.endswith("s") and " " in t and "&" not in t)
    if plural:
        last = plural[0].split(" ")[-1]
        return last[:-1]
    return "source"


_CAPS = re.compile(r"\b[A-Z0-9][\w.&'+-]*(?:\s+[A-Z0-9][\w.&'+-]*)*")


def _connector_sentence(t: ToolFacts) -> str:
    return (tool_wide_sentences(t.description) or sentences(t.description) or [""])[0]


def _group_key(t: ToolFacts) -> tuple[str, str] | None:
    """``(kind, key)``: equal keys = tools that differ only by the proper noun they target."""
    if not t.published or t.admin_only:
        return None
    params = sorted(p.name for p in params_of(t.parameters))
    masked = masked_text(t)
    if masked:
        return "catalog", json.dumps([masked, t.output_kind, params, clean(t.display_name).split(" ")[-1].lower()])
    if t.mcp_server_slug and t.listers and not t.job_key:
        first = _connector_sentence(t)
        if len(first) >= 30:
            return "connector", json.dumps([_CAPS.sub("<N>", first), t.output_kind, params])
    return None


def _shared_sentence(members: list[ToolFacts]) -> str:
    """The first member's sentence with every proper noun that is NOT common to all members as <X>."""
    firsts = [_connector_sentence(m) for m in members]
    common = set(_CAPS.findall(firsts[0]))
    for f in firsts[1:]:
        common &= set(_CAPS.findall(f))
    out = _CAPS.sub(lambda m: m.group(0) if m.group(0) in common else "<X>", firsts[0])
    return re.sub(r"<X>(?:\s*<X>)+", "<X>", out)


def find_families(tools: list[ToolFacts], min_members: int | None = None) -> list[FamilyFacts]:
    """Clusters of published tools whose sentence, output shape and inputs are identical once the
    proper noun they target (a store, a site, a connected service) is masked. A cluster of
    ``min_members`` or more becomes one family skill (knob
    ``agents.context.generated_family_min_members``)."""
    threshold = family_min_members() if min_members is None else min_members
    groups: dict[tuple[str, str], list[ToolFacts]] = defaultdict(list)
    for t in tools:
        key = _group_key(t)
        if key:
            groups[key].append(t)
    out: list[FamilyFacts] = []
    for (kind, key), members in groups.items():
        if len(members) < threshold:
            continue
        if kind == "catalog":
            masked = json.loads(key)[0]
            noun = _family_noun(members)
            m = _FAMILY_LEAD.match(masked)
            lead = m.group(1) if m and m.group(1) else clean(members[0].display_name).split(" ")[-1].capitalize()
            label = f"{lead} by {noun}"
            what = masked.replace("<X>", f"one {noun}")
            pairs = [(family_subject(t) or t.name, t) for t in members]
        else:
            noun = "service"
            what = re.sub(r"\bthe <X>", f"one {noun}'s", _shared_sentence(members)).replace("<X>", f"one {noun}")
            label = fit_words(re.split(r";| to | so that ", what)[0], 100, prefer_punctuation=False) or clip(what, 100)
            pairs = [(t.mcp_server_name or t.mcp_server_slug or t.name, t) for t in members]
        pairs.sort(key=lambda p: (p[0].lower(), p[1].name))
        out.append(FamilyFacts(skill_id=FAMILY_PREFIX + slug(label), label=label, noun=noun, what=what, members=tuple(pairs), kind=kind))
    return sorted(out, key=lambda f: f.skill_id)


def build_family_skill(f: FamilyFacts) -> GeneratedSkill:
    tools = [t for _, t in f.members]
    first = tools[0]
    params = params_of(first.parameters)
    n = len(tools)
    noun_cap = f.noun.capitalize()
    shape = f" Each returns a `{first.output_kind}` shape (skill `kind_{first.output_kind}` explains its fields)." if first.output_kind else ""
    intro = f"{first_sentences(f.what, 300)} One tool per {f.noun}: {n} {f.noun}s.{shape}"
    example_subject, example_tool = f.members[0]
    if f.kind == "catalog":
        trailing = clean(first.display_name).split(" ")[-1]
        how = [
            f'`find_tools` with the {f.noun}\'s name and "{trailing}": it returns that {f.noun}\'s tool and its job_key, '
            "and adds the tool for your next step. Or run it at once with `use_tool`, that job_key and the inputs below.",
            f"A {f.noun} missing from the list has no tool here: say so, never claim you fetched it.",
        ]
        example = [
            f'{example_subject}: `find_tools` with "{clean(example_tool.display_name)}", or `use_tool` with job_key '
            f"`{example_tool.job_key}` and the inputs below."
        ]
        entries = [subject for subject, _ in f.members]
    else:
        how = [
            f"Call the lister named beside the {f.noun} (no inputs): it adds that {f.noun}'s tools for your next step; "
            f"then call this tool by the name the lister adds. If the lister says a connection is missing, ask the "
            f"person to connect that {f.noun}.",
        ]
        example = [
            f"{example_subject}: call `{wire(example_tool.listers[0])}`, then `{wire(example_tool.name)}`."
        ]
        entries = [f"{subject} (`{wire(t.listers[0])}`)" for subject, t in f.members]
    common_pitfalls = [p for p in conditional_pitfalls(first, params) if all(p in conditional_pitfalls(t, params_of(t.parameters)) for t in tools)]
    fixed = [
        ("", [intro]),
        ("How to get the one for a " + f.noun, how),
        ("Example", example),
        ("Inputs (the same for every " + f.noun + ")", _input_lines(params)),
        ("Pitfalls", [f"- {p}" for p in common_pitfalls]),
    ]
    title = f"{f.label} (one tool per {f.noun})"
    room = family_body_limit() - len(_fit_body(fixed, title, 10**9)) - 60
    names: list[str] = []
    used = 0
    for entry in entries:
        if used + len(entry) + 2 > room:
            break
        names.append(entry)
        used += len(entry) + 2
    listing = ", ".join(names) + ("." if len(names) == n else f", and {n - len(names)} more; `find_tools` finds them by name.")
    parts = fixed[:1] + [(f"{noun_cap}s it covers ({n})", [listing])] + fixed[1:]
    body = _fit_body(parts, title, family_body_limit())
    description = trigger_description(f.what, fallback=f.label)
    ids = sorted(t.id for t in tools)
    return GeneratedSkill(
        skill_id=f.skill_id,
        label=clip(f"{f.label} (tool family)", 300),
        description=description,
        body=body,
        category=TOOL_CATEGORY["slug"],
        allowed_tools=(),
        link={"family": "tool_family", "tool_definition_ids": ids, "noun": f.noun},
        published=all(t.published and not t.admin_only for t in tools),
    )


# ---------------------------------------------------------------------------
# combination skills


def _member_line(t: ToolFacts) -> str:
    what = first_sentences(labelled_fields(t.description).get("use") or t.summary or " ".join(tool_wide_sentences(t.description)) or t.description, 110)
    shape = f" → `{t.output_kind}`" if t.output_kind else ""
    return f"- `{wire(t.name)}`{shape} — {clip(what, 110)}" if what else f"- `{wire(t.name)}`{shape}"


def _member_lines(members: list[ToolFacts], *, public: bool, cap: int, collapse: bool = True) -> tuple[list[str], int]:
    """One line per member; a family's members collapse into one line naming the family skill. A
    public skill never names an admin-only or unpublished tool. Returns (lines, members listed)."""
    shown = [m for m in members if not public or (m.published and not m.admin_only)]
    lines: list[str] = []
    fams: dict[str, list[ToolFacts]] = defaultdict(list)
    for m in shown:
        if m.family_skill and collapse:
            fams[m.family_skill].append(m)
    done: set[str] = set()
    for m in shown:
        if m.family_skill and collapse:
            if m.family_skill not in done:
                done.add(m.family_skill)
                n = len(fams[m.family_skill])
                lines.append(f"- {m.family_label or m.family_skill}: {n} tools, one per name; skill `{m.family_skill}` lists them and how to get one.")
        else:
            lines.append(_member_line(m))
    total = len(lines)
    if total > cap:
        lines = lines[:cap] + [f"_{total - cap} more; `find_tools` finds them by the job._"]
    return lines, len(shown)


def build_bundle_skill(b: BundleFacts) -> GeneratedSkill:
    members = sorted(b.members, key=lambda m: m.name)
    lines, _ = _member_lines(members, public=b.published, cap=25, collapse=False)
    if lines and lines[-1].startswith("_"):
        lines[-1] = lines[-1].replace("`find_tools` finds them by the job", "the lister loads them all")
    if not lines:
        lines = [f"- Its tools are listed live from {b.mcp_server_name or b.name} when the lister is called."]
    title = b.mcp_server_name or b.name.replace("-", " ").replace("_", " ").title()
    lister = wire(b.lister_name)
    how = [
        f"Load them with `use_tool` and job_key `{lister}` (no inputs); if you already hold `{lister}`, call it directly. "
        "Every tool above is then added for your next step: call them by name, or through `use_tool` if one is not in your list."
    ]
    if b.mcp_server_slug:
        how.append(
            f"They run on the person's {title} connection. If the lister says the connection is missing or refused, "
            f"ask the person to connect {title}; do not retry the lister."
        )
    shapes = sorted({m.output_kind for m in members if m.output_kind})
    use = ["Pick the member whose line matches the job; its own skill (`tool-<name>`) gives its inputs."]
    if shapes:
        use.append("Shapes returned: " + ", ".join(f"`{s}`" for s in shapes[:8]) + ".")
    what = first_sentences(b.description, 300) or f"The {title} tools."
    body = _fit_body(
        [("", [what]), ("Tools in it", lines), ("Which one", use), ("How to get them", how)],
        f"{title} tools (bundle `{lister}`)",
        body_limit() + 500,
    )
    lead = sentences(what)[0] if sentences(what) else what
    lead = lead if not lead or (lead.split(" ")[0].isupper() and len(lead.split(" ")[0]) > 1) else lead[0].lower() + lead[1:]
    description = trigger_description(f"you need the {title} tools: {lead}", fallback=f"the {title} tools")
    return GeneratedSkill(
        skill_id=BUNDLE_PREFIX + slug(b.name),
        label=clip(f"{title} tools (bundle)", 300),
        description=description,
        body=body,
        category=COMBO_CATEGORY["slug"],
        allowed_tools=(b.lister_id, *sorted(m.id for m in members)[:50]),
        link={
            "family": "bundle",
            "bundle_id": b.id,
            "bundle_name": b.name,
            "tool_definition_id": b.lister_id,
            "tool_definition_ids": sorted(m.id for m in members),
        },
        published=b.published,
    )


def build_shape_tools_skill(s: ShapeFacts) -> GeneratedSkill:
    producers = sorted(s.producers, key=lambda p: (p.job_key is not None, p.name))
    lines, _ = _member_lines(producers, public=s.published, cap=20)
    what = clean(s.description) or f"A `{s.kind}` shape: structured data the platform renders as {s.label}."
    reading = [f'Each returns one `{{"__kind": "{s.kind}"}}` object.']
    if s.has_kind_skill:
        reading.append(f"Skill `kind_{s.kind}` lists its fields and how to emit one yourself.")
    how = ["Holding one of them? Call it by name."]
    solo = [p for p in producers if p.job_key and not p.family_skill and (not s.published or (p.published and not p.admin_only))]
    fam = next((p for p in producers if p.family_skill), None)
    if solo:
        how.append(
            f'Otherwise `find_tools` with the job in plain words (for example "{tool_label(solo[0])}"), '
            "then `use_tool` with the job_key it returns."
        )
    elif fam is not None:
        how.append(f"Otherwise read skill `{fam.family_skill}`: it says how to get the one you need.")
    else:
        how.append("Otherwise read the tool's own skill (`tool-<name>`): it says how to get that tool.")
    body = _fit_body(
        [("", [first_sentences(what, 300)]), ("Tools that return it", lines), ("Reading the result", reading), ("How to get them", how)],
        f"Tools that return {s.label} (`{s.kind}`)",
        body_limit() + 500,
    )
    label_l = s.label.lower()
    noun = label_l if label_l.endswith("data") else f"{label_l} data"
    description = trigger_description(
        f"you need {noun}: which tools return a {s.kind} shape and how to get them", fallback=s.label
    )
    return GeneratedSkill(
        skill_id=SHAPE_PREFIX + slug(s.kind),
        label=clip(f"Tools that return {s.label}", 300),
        description=description,
        body=body,
        category=COMBO_CATEGORY["slug"],
        allowed_tools=tuple(sorted(p.id for p in producers)[:50]),
        link={
            "family": "shape_tools",
            "kind_definition_id": s.id,
            "kind": s.kind,
            "tool_definition_ids": sorted(p.id for p in producers),
        },
        published=s.published,
    )


def to_parsed_skill(g: GeneratedSkill) -> Any:
    """The ingest record for the one skill write path."""
    from matrx_ai.skills.ingest import ParsedSkill

    link = dict(g.link)
    extra = {"source_repo": "aidream", "template_version": TEMPLATE_VERSION, "skill_coverage": link}
    if link.get("tool_definition_id"):
        extra["tool_definition_id"] = link["tool_definition_id"]
    if link.get("kind_definition_id"):
        extra["kind_definition_id"] = link["kind_definition_id"]
    return ParsedSkill(
        skill_id=g.skill_id,
        label=g.label,
        description=g.description,
        skill_type="reference",
        declared_skill_type=True,
        body=g.body,
        category=g.category,
        allowed_tools=list(g.allowed_tools),
        trigger_patterns=[],
        disable_auto_invocation=False,
        version=None,
        source_hash=g.source_hash,
        source_path=f"{COVERAGE_SOURCE}://{link.get('family')}/{g.skill_id}",
        published_to_web=g.published,
        ingested_from=COVERAGE_SOURCE,
        extra_config=extra,
    )


def owns(row: Any) -> bool:
    cfg = getattr(row, "config", None)
    return isinstance(cfg, dict) and cfg.get("ingested_from") == COVERAGE_SOURCE


__all__ = [
    "body_limit",
    "BUNDLE_PREFIX",
    "COMBO_CATEGORY",
    "COVERAGE_SOURCE",
    "description_limit",
    "escape_variables",
    "FAMILY_PREFIX",
    "family_body_limit",
    "family_min_members",
    "PEOPLE_WORDS_VERSION",
    "SHAPE_PREFIX",
    "TOOL_CATEGORY",
    "TOOL_PREFIX",
    "BundleFacts",
    "FamilyFacts",
    "GeneratedSkill",
    "ShapeFacts",
    "ToolFacts",
    "build_bundle_skill",
    "build_family_skill",
    "build_shape_tools_skill",
    "asked_as_of",
    "build_tool_skill",
    "conditional_pitfalls",
    "find_families",
    "owns",
    "params_of",
    "people_description",
    "service_of",
    "skill_label",
    "with_service",
    "slug",
    "to_parsed_skill",
    "tool_wide_sentences",
    "trigger_description",
    "wire",
]
