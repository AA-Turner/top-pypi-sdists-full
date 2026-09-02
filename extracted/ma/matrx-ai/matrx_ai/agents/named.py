"""Typed, declarative agent definitions.

Layer 3 of the agent stack:

  Layer 1 — ``Agent`` (matrx_ai.agents.definition):
      Loads + applies variables + executes against an LLM provider.

  Layer 2 — ``run_agent`` (matrx_ai.agents.executor):
      Wraps ``agent.execute()`` in ``child_agent_context``; returns a
      typed ``AgentRunResult``; optional JSON parse + validation.

  Layer 3 — ``NamedAgent`` (this module):
      A declarative class. Bakes in the loader (an ``AgentSource``), a
      typed Pydantic ``Inputs`` model, an optional Pydantic ``Output``
      model, and small hooks for combining inputs into variables or
      post-processing the parsed object. Call sites become one line:
      ``await MyAgent.run(inputs=MyAgent.Inputs(...))``.

The two flavors of agent the request asked for both fall out of this:

  * **DB-backed agents** (records in the ``agents`` table — the GUIDs
    research currently sprinkles around as ``GENERIC_*_AGENT_ID``):

        class PageSummaryAgent(NamedAgent):
            name = "page_summary"
            source = AgentRecordSource(
                agent_id="7e021d98-…",
                is_version=False,   # required: pinned vs floating
            )

            class Inputs(BaseModel):
                topic: str
                page_content: str
                page_url: str = ""
                page_title: str = ""

  * **Hardcoded inline agents** (system prompt + model + params declared
    in code, not in the DB):

        class TitleSuggesterAgent(NamedAgent):
            name = "title_suggester"
            source = InlineAgentSource(
                config_dict={
                    "messages": [{"role": "system", "content": SYSTEM_PROMPT}],
                    "model": "anthropic/claude-3-5-sonnet-latest",
                    "temperature": 0.4,
                },
            )

            class Inputs(BaseModel):
                topic_name: str
                topic_description: str = ""

            class Output(BaseModel):
                title: str
                description: str = ""

The runtime override path (``topic.agent_config.page_summary_agent_id``
in research) flows in via ``source_override=AgentRecordSource(…)`` on
the ``run`` call, so the declarative class still owns the default and
the call site just supplies an alternative when the user has configured
one.
"""

from __future__ import annotations

import json
from abc import ABC, abstractmethod
from enum import StrEnum
from typing import Annotated, Any, ClassVar, Generic, Literal, TypeVar

from matrx_utils import vcprint
from pydantic import BaseModel, ConfigDict, Field, JsonValue, TypeAdapter, ValidationError

from matrx_ai.agents.definition import Agent
from matrx_ai.agents.executor import AgentRunResult, run_agent
from matrx_ai.agents.variables import AgentVariable
from matrx_ai.config.llm_params import LLMParams
from matrx_ai.tools.models import CustomTool

InputsT = TypeVar("InputsT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


# ---------------------------------------------------------------------------
# Registry + validation (the "check every agent at ship time" mechanism)
# ---------------------------------------------------------------------------

# Every concrete NamedAgent subclass registers itself here at import time.
# A validation script imports the agent-defining modules, then iterates this
# list and calls ``validate()`` on each — no LLM calls, just contract checks.
_REGISTERED_NAMED_AGENTS: list[type[NamedAgent]] = []


def iter_registered_named_agents() -> tuple[type[NamedAgent], ...]:
    """Return every concrete ``NamedAgent`` subclass imported so far."""
    return tuple(_REGISTERED_NAMED_AGENTS)


class MandateSourceUnresolved(RuntimeError):
    """``.run()`` was called on a mandated agent without resolving its Mandate.

    A mandated class carries no agent id, so there is nothing to fall back to —
    and inventing one is exactly the defect the Mandate system exists to prevent.
    Route the call through ``run_mandated`` (or the host's Mandate-aware ``run``).
    """

    def __init__(self, agent_class: str, mandate_key: str | None) -> None:
        super().__init__(
            f"{agent_class} declares mandate_key={mandate_key!r} and no hardcoded source, "
            f"so .run() cannot know which agent to run. Call it through "
            f"run_mandated() so the database decides."
        )
        self.agent_class = agent_class
        self.mandate_key = mandate_key


class AgentValidationReport(BaseModel):
    """Result of validating one ``NamedAgent`` against its source.

    ``ok`` is False when ``errors`` is non-empty. ``warnings`` never flip
    ``ok`` — they surface likely-but-not-certain drift (e.g. an Inputs
    field that maps to a variable the template never references).
    """

    label: str
    source_kind: str
    ok: bool = True
    errors: list[str] = []
    warnings: list[str] = []
    # Version discipline (DB-backed agents only). ``is_floating`` = no pinned
    # version (tracks latest — the safe dev default). When pinned, the two
    # version numbers let the caller flag a stale pin. Never flips ``ok``.
    is_floating: bool = False
    pinned_version: int | None = None
    latest_version: int | None = None
    validation_target: Literal["seed", "resolved"] = "seed"


class CodeValueMapping(BaseModel):
    """LEGACY spelling of :class:`OfferedValueMapping`.

    Kept in the union so persisted maps still VALIDATE, but the one read funnel
    (:func:`parse_value_mapping`) normalizes every ``code_value`` to the neutral
    ``offered_value`` before any consumer sees it — a persisted shape has ONE
    deserializer, and post-funnel code never branches on ``code_value``.
    """

    mapType: Literal["code_value"] = "code_value"
    target: str
    required: bool = False


class OfferedValueMapping(BaseModel):
    """The neutral map type: consume one offered/code-supplied value.

    ``target`` names the SOURCE value (the offered value / code value name);
    when it differs from the map key the value is renamed on delivery.
    ``deliver`` decides the channel: ``variable`` (immutable, turn-1,
    prompt-substituted) or ``context`` (mutable, context-policy path).
    ``when_absent`` is REQUIRED for a non-guaranteed offered value at bind
    time (validated by the binding write path): ``skip`` delivers nothing,
    ``use_default`` delivers ``default``, ``fail`` makes absence fatal.
    """

    mapType: Literal["offered_value"] = "offered_value"
    target: str
    required: bool = False
    deliver: Literal["variable", "context"] = "variable"
    when_absent: Literal["skip", "use_default", "fail"] | None = None
    default: JsonValue | None = None


class DirectValueMapping(BaseModel):
    """A fixed literal, written on the binding itself.

    ``deliver`` is the same channel flag :class:`OfferedValueMapping` carries,
    and it is here for the same reason: the channel is a property of the
    TARGET, not of the source. A mandate consumption map may feed a context
    slot from a literal exactly as it may feed one from an offered value, and
    every source of one target must agree on where it lands. A surface binding
    never sets it and never reads it — the default is the pre-existing
    behaviour, so nothing stored before this field existed changes meaning.
    """

    mapType: Literal["direct_value"] = "direct_value"
    target: JsonValue
    deliver: Literal["variable", "context"] = "variable"


class UnmappedValueMapping(BaseModel):
    mapType: Literal["unmapped"] = "unmapped"


class PromptUserValueMapping(BaseModel):
    """Ask the person for this input, at the moment of the run.

    ``deliver``: see :class:`DirectValueMapping`.

    🚨 WHO ASKS depends on WHERE this is stored, and the two are not the same
    thing. On a SURFACE binding the client asks in a dialog before it launches,
    and this shape never reaches a server-side resolve (:func:
    `resolve_variable_mapping` refuses it, loudly, because no human is present
    inside a server run). On a MANDATE consumption map the ask is served: the
    mandate's input surface publishes this target as a real named field, the
    run form asks for it there, and the answer arrives in the supplied values
    like any other input. Same promise to the person, asked by whichever half
    actually has them on screen.
    """

    mapType: Literal["prompt_user"] = "prompt_user"
    prompt: str = ""
    defaultValue: JsonValue | None = None
    required: bool = False
    deliver: Literal["variable", "context"] = "variable"


ValueMapping = Annotated[
    CodeValueMapping
    | OfferedValueMapping
    | DirectValueMapping
    | UnmappedValueMapping
    | PromptUserValueMapping,
    Field(discriminator="mapType"),
]

_VALUE_MAPPING_ADAPTER = TypeAdapter(ValueMapping)

ParsedValueMapping = (
    OfferedValueMapping | DirectValueMapping | UnmappedValueMapping | PromptUserValueMapping
)


#: The source names a person actually chooses between, in the words the UI uses.
#: Ordered as the binding screen lists them, so an error reads like the screen.
VALUE_MAPPING_SOURCE_WORDS = (
    "take a value the job offers ('offered_value')",
    "write a fixed value ('direct_value')",
    "ask the person ('prompt_user')",
    "leave it to the holder's own default ('unmapped')",
)


#: (mapType, field) → what that field IS, said to whoever has to fix the row.
#: A source is stored by a UI, so "this is missing" has to name the thing the
#: person chose, never the attribute the model happens to call it.
_FIELD_WORDS: dict[tuple[str, str], str] = {
    ("offered_value", "target"): "it does not say WHICH offered value to take",
    ("code_value", "target"): "it does not say WHICH offered value to take",
    ("direct_value", "target"): "it has no fixed value to write — a 'direct_value' source IS its value",
    ("prompt_user", "prompt"): "it has no question to ask — a blank box nobody can answer",
}


def _field_problem(tag: Any, error: dict[str, Any]) -> str:
    """One stored-field failure, in words rather than validator jargon."""
    field = next(
        (str(part) for part in error.get("loc", ()) if isinstance(part, str) and part != tag),
        "",
    )
    known = _FIELD_WORDS.get((str(tag), field))
    if known:
        return known
    # Unknown field: still no model-class dump, and still actionable — name the
    # field and what was actually stored there.
    return (
        f"its {field!r} is not usable"
        if field
        else "its stored shape is not one this source accepts"
    )


class ValueMappingParseError(ValueError):
    """A stored mapping entry cannot be read — said in words, never a dump.

    🚨 A PYDANTIC DUMP IS NOT A REFUSAL. Before 2026-08-31 an unknown
    ``mapType`` reached the client verbatim as
    ``tagged-union[CodeValueMapping,…] Input tag 'totally_bogus' found using
    'mapType' does not match any of the expected tags`` — the class names of
    five internal models, no entry name, no remedy, and the hand-written
    sentence in ``validate_consumption_map`` was unreachable because this
    parser raised first (V3-CORRECTNESS F9, request
    ``497b9e28266d4c0598b12f7e6fa44026``). Every read funnel inherits this one
    wrapper, so there is nowhere left for a raw dump to escape from.
    """


def parse_value_mapping(raw: Any) -> ParsedValueMapping:
    """THE one deserializer for a persisted ValueMapping entry.

    Every read of a stored mapping (mandate ``contract.variable_mapping``,
    binding ``consumption_map``, shortcut ``value_mappings``) goes through
    here. Legacy ``code_value`` entries are normalized to the neutral
    ``offered_value`` shape, so no consumer ever branches on the legacy
    spelling — normalize on read, ONE funnel, no second parser.

    Raises :class:`ValueMappingParseError` — a worded refusal naming the tag it
    found and the sources that exist — for anything it cannot read.
    """
    if isinstance(
        raw,
        CodeValueMapping
        | OfferedValueMapping
        | DirectValueMapping
        | UnmappedValueMapping
        | PromptUserValueMapping,
    ):
        value: Any = raw
    else:
        if not isinstance(raw, dict):
            raise ValueMappingParseError(
                f"a source must be an object saying where the value comes from, and this "
                f"one is {type(raw).__name__} — " + "; ".join(VALUE_MAPPING_SOURCE_WORDS)
            )
        tag = raw.get("mapType")
        try:
            value = _VALUE_MAPPING_ADAPTER.validate_python(raw)
        except ValidationError as exc:
            tag_problem = any(
                error.get("type") in ("union_tag_invalid", "union_tag_not_found")
                for error in exc.errors()
            )
            if tag_problem:
                raise ValueMappingParseError(
                    (
                        f"{tag!r} is not a kind of source a binding can carry"
                        if tag is not None
                        else "this source does not say what kind it is (no 'mapType')"
                    )
                    + " — " + "; ".join(VALUE_MAPPING_SOURCE_WORDS)
                ) from exc
            # A KNOWN source whose own fields are wrong. 🚨 PYDANTIC'S `msg` IS
            # NOT A SENTENCE — "target Field required" reached a client
            # (V3-CORRECTNESS F9's sibling, found by the FIX-3 independent
            # verifier, request 983166eb267e). Every field this union has says
            # what it IS, in words; only a field nobody has written a sentence
            # for falls back, and it falls back to something a person can act on.
            raise ValueMappingParseError(
                f"the {tag!r} source is stored wrong: "
                + "; ".join(
                    _field_problem(tag, error) for error in exc.errors()
                )
            ) from exc
    if isinstance(value, CodeValueMapping):
        return OfferedValueMapping(target=value.target, required=value.required)
    return value


class VariableVerdictKind(StrEnum):
    OK = "ok"
    RENAMED = "renamed"
    DEFAULT_USED = "default_used"
    INTENTIONALLY_BLANK = "intentionally_blank"
    SPILLED_TO_USER_INPUT = "spilled_to_user_input"
    DROPPED = "dropped"
    MISSING_FROM_CODE = "missing_from_code"
    REQUIRED_UNMAPPED = "required_unmapped"
    TYPE_MISMATCH = "type_mismatch"


class VariableVerdict(BaseModel):
    variable: str
    verdict: VariableVerdictKind
    code_name: str | None = None
    message: str
    caution: bool = False
    blocking: bool = False
    lossy: bool = False


class VariableResolution(BaseModel):
    variables: dict[str, JsonValue] = Field(default_factory=dict)
    user_input: str | None = None
    verdicts: list[VariableVerdict] = Field(default_factory=list)
    blocking: bool = False
    # The spilled lines ALONE, without the caller's own user_input folded in.
    # `user_input` above is the merged string and is only usable by a call site
    # that passed a string; a multimodal call site (a list of content blocks)
    # needs just the spill so it can append it as one more block.
    spilled_text: str | None = None


def _has_agent_default(variable: AgentVariable) -> bool:
    return variable.default_value is not None and variable.default_value != ""


def _coerce_declared_value(
    variable: AgentVariable, value: Any
) -> tuple[Any, bool, bool, str | None]:
    """Return value, mismatched, lossy, note. Only proven lossless casts pass."""
    extra = variable.model_extra or {}
    expected = extra.get("dataType") or extra.get("data_type") or extra.get("type")
    if expected in (None, "string", "text"):
        if expected and not isinstance(value, str):
            return (
                to_template_value(value),
                True,
                False,
                f"losslessly coerced {type(value).__name__} to string",
            )
        return value, False, False, None
    if expected in ("number", "float"):
        if isinstance(value, bool):
            return value, True, True, "boolean cannot be safely coerced to number"
        if isinstance(value, int | float):
            return value, False, False, None
        if isinstance(value, str):
            try:
                return float(value), True, False, "losslessly coerced numeric string to number"
            except ValueError:
                pass
        return value, True, True, f"{type(value).__name__} is not a number"
    if expected in ("integer", "int"):
        if isinstance(value, int) and not isinstance(value, bool):
            return value, False, False, None
        if isinstance(value, str):
            try:
                return int(value), True, False, "losslessly coerced integer string to integer"
            except ValueError:
                pass
        return value, True, True, f"{type(value).__name__} is not an integer"
    if expected in ("boolean", "bool"):
        if isinstance(value, bool):
            return value, False, False, None
        if isinstance(value, str) and value.lower() in {"true", "false"}:
            return (
                value.lower() == "true",
                True,
                False,
                "losslessly coerced boolean string to boolean",
            )
        return value, True, True, f"{type(value).__name__} is not a boolean"
    return value, False, False, None


def resolve_variable_mapping(
    code_values: dict[str, Any],
    declarations: dict[str, AgentVariable],
    mapping: dict[str, ValueMapping | dict[str, Any]] | None = None,
    *,
    spill: set[str] | None = None,
    user_input: str | None = None,
) -> VariableResolution:
    """Resolve ValueMapping against one agent; mapping keys are agent variables."""
    parsed: dict[str, ParsedValueMapping] = {}
    for agent_name, raw in (mapping or {}).items():
        value = parse_value_mapping(raw)
        if isinstance(value, PromptUserValueMapping):
            raise ValueError(
                f"mapping for {agent_name!r} uses prompt_user, but a server-side "
                "mandate run has no human present; use code_value, direct_value, or unmapped"
            )
        parsed[agent_name] = value

    variables: dict[str, JsonValue] = {}
    verdicts: list[VariableVerdict] = []
    consumed: set[str] = set()
    for agent_name, declaration in declarations.items():
        choice = parsed.get(agent_name)
        if isinstance(choice, UnmappedValueMapping):
            required = declaration.required
            verdicts.append(
                VariableVerdict(
                    variable=agent_name,
                    verdict=VariableVerdictKind.REQUIRED_UNMAPPED
                    if required
                    else VariableVerdictKind.INTENTIONALLY_BLANK,
                    message="required agent variable is explicitly unmapped"
                    if required
                    else "agent variable is intentionally blank",
                    blocking=required,
                )
            )
            continue
        if isinstance(choice, DirectValueMapping):
            resolved_value, mismatched, lossy, note = _coerce_declared_value(
                declaration, choice.target
            )
            variables[agent_name] = to_template_value(resolved_value)
            verdicts.append(
                VariableVerdict(
                    variable=agent_name,
                    verdict=VariableVerdictKind.TYPE_MISMATCH
                    if mismatched
                    else VariableVerdictKind.OK,
                    message=note or "fixed binding literal supplied",
                    caution=mismatched and not lossy,
                    blocking=lossy,
                    lossy=lossy,
                )
            )
            continue
        code_name = choice.target if isinstance(choice, OfferedValueMapping) else agent_name
        if code_name in code_values:
            consumed.add(code_name)
            resolved_value, mismatched, lossy, note = _coerce_declared_value(
                declaration, code_values[code_name]
            )
            variables[agent_name] = to_template_value(resolved_value)
            verdicts.append(
                VariableVerdict(
                    variable=agent_name,
                    code_name=code_name,
                    verdict=VariableVerdictKind.TYPE_MISMATCH
                    if mismatched
                    else (
                        VariableVerdictKind.RENAMED
                        if code_name != agent_name
                        else VariableVerdictKind.OK
                    ),
                    message=note
                    or (
                        f"code value {code_name!r} mapped to agent variable {agent_name!r}"
                        if code_name != agent_name
                        else "code and agent variable names match"
                    ),
                    caution=mismatched and not lossy,
                    blocking=lossy,
                    lossy=lossy,
                )
            )
        elif _has_agent_default(declaration):
            verdicts.append(
                VariableVerdict(
                    variable=agent_name,
                    code_name=code_name,
                    verdict=VariableVerdictKind.DEFAULT_USED,
                    message="code supplied no value; agent default is preserved",
                )
            )
        elif declaration.required:
            verdicts.append(
                VariableVerdict(
                    variable=agent_name,
                    code_name=code_name,
                    verdict=VariableVerdictKind.MISSING_FROM_CODE,
                    message="required agent value does not exist in the calling code path",
                    blocking=True,
                )
            )
        else:
            verdicts.append(
                VariableVerdict(
                    variable=agent_name,
                    code_name=code_name,
                    verdict=VariableVerdictKind.INTENTIONALLY_BLANK,
                    message="optional agent variable is blank",
                )
            )

    spill_lines: list[str] = []
    for code_name, value in code_values.items():
        if code_name in consumed:
            continue
        if code_name in (spill or set()):
            spill_lines.append(f"{code_name.replace('_', ' ').title()}: {to_template_value(value)}")
            verdicts.append(
                VariableVerdict(
                    variable=code_name,
                    code_name=code_name,
                    verdict=VariableVerdictKind.SPILLED_TO_USER_INPUT,
                    message="undeclared code value appended to user_input",
                    caution=True,
                )
            )
        else:
            verdicts.append(
                VariableVerdict(
                    variable=code_name,
                    code_name=code_name,
                    verdict=VariableVerdictKind.DROPPED,
                    message="THE DEVELOPER ILLUSION: code supplies this value but the agent does not consume it",
                    caution=True,
                )
            )
    combined = user_input
    spilled_text = "\n".join(spill_lines) if spill_lines else None
    if spill_lines:
        combined = "\n".join(part for part in (user_input, *spill_lines) if part)
    return VariableResolution(
        variables=variables,
        user_input=combined,
        spilled_text=spilled_text,
        verdicts=verdicts,
        blocking=any(item.blocking for item in verdicts),
    )


def _declared_variable_names(agent: Agent) -> set[str]:
    """Named variables the agent declares in its ``variable_definitions`` field.

    This is the authoritative variable contract — the data, never the prompt
    content. ``variable_defaults`` is keyed by the declared variable name.
    """
    return set(getattr(agent, "variable_defaults", {}) or {})


def _required_variable_names(agent: Agent) -> set[str]:
    """Declared variables marked ``required`` in ``variable_definitions``."""
    required: set[str] = set()
    for name, var in (getattr(agent, "variable_defaults", {}) or {}).items():
        if getattr(var, "required", False):
            required.add(name)
    return required


def _declared_context_names(agent: Agent) -> set[str]:
    """Named context policies the agent declares in its ``context_policies`` field.

    Each slot is a JSONB descriptor keyed by ``key`` (see ContextPolicy). These
    are valid fill targets at request time — never inferred from content.
    """
    names: set[str] = set()
    for slot in getattr(agent, "context_policies", None) or []:
        if isinstance(slot, dict):
            key = slot.get("key")
            if isinstance(key, str) and key:
                names.add(key)
    return names


def offer_view(agent_cls: type[NamedAgent], inputs_obj: BaseModel) -> dict[str, Any]:
    """Every name under which a CALL SITE's values can honestly be looked up.

    🚨 THE TWO-NAME TRUTH. A NamedAgent carries two vocabularies and they are
    not the same vocabulary:

    * the CALL SITE's names — the typed ``Inputs`` field names, which is what a
      Provision's ``offered`` values are declared in (``code_truth`` records
      these as ``name``);
    * the HOLDER's names — the agent-template variables that
      ``variable_map`` / ``prepare_variables`` rename them into
      (``code_truth``'s ``mapped_name``).

    An offer check asks "did the call site supply this?", so it must read the
    CALL-SITE vocabulary. Reading only ``prepare_variables`` output made every
    renaming agent look like a broken promise: ``PdfCleanerAgent`` renames
    ``content`` -> ``text_extracted_from_pdf`` and its production runs refused
    with ``content`` "not supplied" while ``content`` was right there
    (2026-08-27 incident).

    So the view is the UNION of both vocabularies — a value present under
    either name is supplied. It never weakens the guarantee: a value the call
    site genuinely did not supply is absent (or ``None``) under BOTH names, and
    a ``prepare_variables`` override that SYNTHESIZES an offered value out of
    several fields still satisfies it under the synthesized name.
    """
    raw = {name: to_template_value(value) for name, value in inputs_obj.model_dump().items()}
    view = {
        name: to_template_value(value)
        for name, value in agent_cls.prepare_variables(inputs_obj).items()
    }
    for name, value in raw.items():
        if view.get(name) is None:
            view[name] = value
    return view


def to_template_value(value: Any) -> Any:
    """Coerce a Python value into a form sensible for ``{{var}}`` substitution.

    The agent template engine does ``str(value)`` on every variable when
    rendering placeholders. That works for strings and scalars but turns
    structured data into Python repr (``[{'name': 'foo'}]``) which is not
    what an LLM expects. This helper produces JSON for lists/dicts/Pydantic
    models so structured Inputs round-trip cleanly through the template,
    while leaving primitive types alone so the existing string-based
    behaviour is preserved bit-for-bit.

    * ``None``                  -> ``None`` (unchanged; ``str(None) == "None"``
                                  is the historical behaviour, kept for parity).
    * ``str``                   -> unchanged (no trim, no escaping).
    * ``BaseModel``             -> ``model_dump_json()``.
    * ``list`` / ``dict`` / ``tuple`` / ``set`` -> ``json.dumps`` with
                                  ``ensure_ascii=False`` and ``default=str``.
    * everything else           -> unchanged (``str()`` conversion happens
                                  later inside ``replace_variables``).
    """
    if value is None or isinstance(value, str):
        return value
    if isinstance(value, BaseModel):
        return value.model_dump_json()
    if isinstance(value, list | dict | tuple | set):
        if isinstance(value, tuple | set):
            value = list(value)
        return json.dumps(value, ensure_ascii=False, default=str)
    return value


# ---------------------------------------------------------------------------
# Sources — one shape per Agent.* loader
# ---------------------------------------------------------------------------


class AgentSource(BaseModel, ABC):
    """Loader descriptor. ``load()`` returns a fresh ``Agent`` ready for
    variable application."""

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    @abstractmethod
    async def load(self) -> Agent: ...


class AgentRecordSource(AgentSource):
    """Load from the ``agents`` table.

    ``is_version`` is REQUIRED — every caller must decide explicitly
    whether they want a floating reference (``is_version=False``, picks
    up edits made to the agent) or a pinned reference (``is_version=True``,
    locks in a specific committed version). Forgetting which mode you're
    in is the most expensive way to mis-deploy an agent, so the type
    system makes it impossible to omit.
    """

    agent_id: str
    is_version: bool

    async def load(self) -> Agent:
        return await Agent.from_agent(self.agent_id, is_version=self.is_version)


async def _master_latest_version(master_id: str) -> int | None:
    from matrx_ai.db.agx_manager import agx_agent_manager_instance

    try:
        master = await agx_agent_manager_instance.load_by_id(master_id)
        return getattr(master, "version", None)
    except Exception:  # noqa: BLE001 — best-effort; never crash the bulk run
        return None


async def _agent_version_status(
    source: AgentRecordSource,
) -> tuple[bool, int | None, int | None]:
    """Return ``(is_floating, pinned_version, latest_version)`` for a DB agent.

    Development-stage philosophy (2026-06-22): while an agent is actively
    evolving, a FLOATING reference (``is_version=False``) is the SAFE default —
    it always loads the latest definition, so an improvement can never silently
    fail to reach the running code. The real hazard is a PIN that has fallen
    BEHIND the latest version: the code keeps executing an old snapshot while
    every new edit is invisible to it. The caller renders this as a table; it
    does NOT push a warning string here, so the report's ``warnings`` carry only
    non-version issues.
    """
    if not source.is_version:
        return (True, None, await _master_latest_version(source.agent_id))
    try:
        from matrx_ai.db.agx_manager import agx_version_manager_instance

        version_row = await agx_version_manager_instance.load_by_id(source.agent_id)
        pinned_n = getattr(version_row, "version_number", None)
        master_id = getattr(version_row, "agent_id", None)
        latest_n = await _master_latest_version(str(master_id)) if master_id else None
        return (False, pinned_n, latest_n)
    except Exception:  # noqa: BLE001 — version lookup is best-effort; never crash the bulk run
        return (False, None, None)


class AnyIdAgentSource(AgentSource):
    """Generic fallback-chain loader (``Agent.from_id``).

    Use only for transitional code that legitimately can't tell whether
    the id is an agent record or some legacy source. New code should pick
    ``AgentRecordSource`` or ``InlineAgentSource``.
    """

    id: str
    source: str | None = None

    async def load(self) -> Agent:
        return await Agent.from_id(self.id, source=self.source)


class InlineAgentSource(AgentSource):
    """Hardcoded agent defined entirely in code — no DB lookup.

    ``config_dict`` is the same shape that ``Agent.from_dict`` consumes
    (``messages``, ``model``, ``temperature``, etc. — anything
    ``UnifiedConfig.from_dict`` accepts). ``variable_defaults`` lets the
    inline agent declare ``AgentVariable`` definitions for templating.
    """

    config_dict: dict[str, Any]
    variable_defaults: dict[str, AgentVariable] | None = None
    name: str = "InlineAgent"

    async def load(self) -> Agent:
        agent = Agent.from_dict(
            self.config_dict,
            variable_defaults=self.variable_defaults,
        )
        agent.name = self.name
        return agent


# ---------------------------------------------------------------------------
# Declarative agent class
# ---------------------------------------------------------------------------


class NamedAgent(Generic[InputsT, OutputT], ABC):
    """Declarative agent definition with typed inputs and optional typed output.

    Subclasses MUST set ``name``, ``source``, and the ``Inputs`` inner
    class. ``Output`` is optional — when set, ``run`` automatically uses
    it as the JSON schema for the executor.

    Subclasses MAY override:

    * ``prepare_variables(inputs)`` — to combine multiple typed inputs
      into a different set of template variables (e.g. concatenate two
      fields, JSON-encode a list, fetch a related record).
    * ``post_process(parsed)`` — to massage the validated Pydantic
      output before it's attached to the result.
    """

    name: ClassVar[str]
    # 🚨 A MANDATETED AGENT CARRIES NO AGENT ID (Arman, 2026-08-16). Declare
    # ``mandate_key`` and the DATABASE decides which agent runs — including
    # whether it is a version pin, which is a dynamic DB setting, never a
    # code constant. ``source`` remains ONLY for the genuinely un-mandated
    # agent (an inline config in a test). A class must declare exactly one of
    # the two; declaring an id "as a fallback" for a Mandate is the antipattern
    # this rule exists to kill.
    source: ClassVar[AgentSource | None] = None
    mandate_key: ClassVar[str | None] = None
    Inputs: ClassVar[type[BaseModel]]
    Output: ClassVar[type[BaseModel] | None] = None
    # Optional code-side safety override for machine-consumed agents whose
    # output contract must never share the wire with automatically injected
    # surface/capability tools. None preserves the resolved definition policy.
    auto_tools_disabled: ClassVar[bool | None] = None
    child_source_app: ClassVar[str | None] = None
    child_source_feature: ClassVar[str | None] = None

    # Ratified citations policy (2026-07-17, docs/handoffs/citations-system.md):
    # citations are default-ON for user-facing runs and OFF for machine-consumed
    # runs — every exclusion explicit and LOUD. ``None`` = platform default
    # (agents with ``Output`` set are already excluded via response_format).
    # Set ``False`` on agents whose plain-text output is machine-parsed
    # (TTS-prep scripts, extraction/cleanup pipelines): the Anthropic
    # translator's gate then strips document citability and announces it.
    citations_enabled: ClassVar[bool | None] = None

    # Declarative local-field -> agent-template-variable rename map. Carried
    # over from the old AgentRunnerSpec.required_variables so a call site
    # whose Inputs field name differs from the agent's template placeholder
    # (e.g. Inputs.content -> {{text_extracted_from_pdf}}) can express that
    # mapping declaratively AND have it validated at ship time, instead of
    # silently rendering the placeholder empty. Fields not present in the
    # map pass through under their own name (identity).
    variable_map: ClassVar[dict[str, str]] = {}

    def __init_subclass__(cls, **kwargs: Any) -> None:
        super().__init_subclass__(**kwargs)
        # Register only fully-defined concrete agents. Abstract intermediates
        # (missing name/source/Inputs) are skipped — they get registered when
        # their concrete subclass is created.
        if (
            getattr(cls, "name", None)
            and (getattr(cls, "source", None) is not None or getattr(cls, "mandate_key", None))
            and getattr(cls, "Inputs", None) is not None
        ):
            _REGISTERED_NAMED_AGENTS.append(cls)

    @classmethod
    def prepare_variables(cls, inputs: BaseModel) -> dict[str, Any]:
        """Map typed ``Inputs`` -> the flat ``{var_name: value}`` dict that
        ``Agent.set_variables`` expects.

        Default: pass each declared field through, applying ``variable_map``
        to rename a local field to its agent-template variable name. Fields
        absent from ``variable_map`` keep their own name. Includes ``None``
        and empty-string defaults filled in by Pydantic — matching the
        behaviour of the existing ``_execute_agent`` callers in ``research/``
        which always pass the full set of variables they care about, even
        when some are empty. Subclasses can override to combine or transform
        fields (call ``super().prepare_variables(inputs)`` to keep the rename).
        """
        return {
            cls.variable_map.get(field, field): value
            for field, value in inputs.model_dump().items()
        }

    @classmethod
    def post_process(cls, parsed: BaseModel | None) -> BaseModel | None:
        """Hook for shaping the validated output further. Default: passthrough."""
        return parsed

    @classmethod
    async def run(
        cls,
        *,
        inputs: BaseModel | dict[str, Any],
        source_override: AgentSource | None = None,
        config_overrides: LLMParams | dict[str, Any] | None = None,
        user_input: str | list[dict[str, Any]] | None = None,
        custom_tools: list[CustomTool | dict[str, Any]] | None = None,
        client_tools: list[str] | None = None,
        request_metadata: dict[str, Any] | None = None,
        label: str | None = None,
        source_app: str | None = None,
        source_feature: str | None = None,
        independent_request: bool = False,
        suppress_stream: bool = False,
        variable_mapping: dict[str, ValueMapping | dict[str, Any]] | None = None,
        spill_variables: set[str] | None = None,
    ) -> AgentRunResult:
        """Load -> apply variables -> apply overrides -> execute.

        Mirrors the feature surface of the ``/agents/`` HTTP endpoint for
        programmatic callers. Runtime concerns that are intrinsic to the
        request (memory, scope, sandbox binding, IDE state, cache bypass,
        debug, block_mode, snapshot) inherit automatically from the
        parent ``AppContext`` via ``child_agent_context.fork_for_child_agent``.

        Args:
            inputs: An instance of ``cls.Inputs`` OR a dict that will be
                    coerced into one. The typed-class path is preferred.
            source_override: Replace ``cls.source`` for this call only.
                             The runtime config-driven override path
                             (``topic.agent_config.<key>``) flows in here.
            config_overrides: ``LLMParams`` or kwargs dict applied to the
                              agent's UnifiedConfig before execution.
            user_input: Optional user message (string or rich content
                        blocks — images, files, multimodal). Appended
                        verbatim to the conversation.
            custom_tools: Optional list of ``CustomTool`` instances or
                          dicts (parsed via ``CustomTool.from_dict``).
                          Appended to ``agent.config.custom_tools`` and
                          their names merged into the forked
                          ``AppContext.client_tools`` so the dispatcher
                          delegates them client-side. Mirrors what
                          ``prepare_agent_run`` does for the HTTP path.
            client_tools: Optional list of additional client-delegated
                          tool names. Merged into the forked
                          ``AppContext.client_tools``.
            request_metadata: Optional dict merged into
                              ``agent.request_metadata`` (flows to
                              ``execute_ai_request(metadata=...)``).
            label: Sub-agent label for ``child_agent_context``. Defaults
                   to ``cls.name``.
            source_app: Optional override for child CX source_app. Defaults
                        to ``cls.child_source_app`` or the host default.
            source_feature: Optional override for child CX source_feature.
                            Defaults to ``cls.child_source_feature`` or
                            ``cls.name`` (required — one must resolve).
            independent_request: When True, the forked child context gets
                                a fresh ``request_id`` so this call is
                                rooted as its own ``cx_user_request``
                                rather than as a sub-step of the parent.
                                Use for fan-out workloads where each call
                                is a standalone user-level unit (e.g.
                                concurrent per-page summaries in the
                                research pipeline). Passes straight
                                through to ``run_agent``.

        Returns:
            ``AgentRunResult`` — never raises. Inspect ``success``,
            ``error_kind``, ``output``, ``parsed`` / ``parse_error``.
        """
        cls._check_definition()

        inputs_obj = cls._coerce_inputs(inputs)
        source = source_override or cls.source
        if source is None:
            # A mandated class reaches here only if something called .run()
            # directly without resolving the Mandate. Refuse — never guess.
            raise MandateSourceUnresolved(cls.__name__, getattr(cls, "mandate_key", None))
        agent = await source.load()
        if cls.auto_tools_disabled is not None:
            agent.auto_tools_disabled = cls.auto_tools_disabled
        code_values = inputs_obj.model_dump()
        effective_mapping: dict[str, ValueMapping | dict[str, Any]] = {
            destination: CodeValueMapping(target=local)
            for local, destination in cls.variable_map.items()
        }
        effective_mapping.update(variable_mapping or {})
        # Custom preparation is already expressed in agent-variable names.
        if cls.prepare_variables.__func__ is not NamedAgent.prepare_variables.__func__:  # type: ignore[attr-defined]
            code_values = cls.prepare_variables(inputs_obj)
        resolution = resolve_variable_mapping(
            code_values,
            getattr(agent, "variable_defaults", {}) or {},
            effective_mapping,
            spill=spill_variables,
            user_input=user_input if isinstance(user_input, str) or user_input is None else None,
        )
        if resolution.blocking:
            detail = "; ".join(v.message for v in resolution.verdicts if v.blocking)
            raise ValueError(f"{cls.name}: resolved agent variable binding is invalid: {detail}")
        variables = {k: to_template_value(v) for k, v in resolution.variables.items()}
        if isinstance(user_input, str) or user_input is None:
            user_input = resolution.user_input
        elif resolution.spilled_text:
            # A MULTIMODAL call site (a list of content blocks) must still
            # receive spilled values. Before 2026-08-16 the spill was computed
            # and then silently discarded here, so a Mandate whose remedy is
            # "pass it as user text" kept dropping the value on exactly the
            # call sites that attach files or a prep message — the podcast
            # topic path being the live one. Append it as one more input_text
            # block; `resolve_variable_mapping` joins with "\n" and is
            # string-only, so it cannot build this shape itself.
            user_input = [*user_input, {"type": "input_text", "text": resolution.spilled_text}]
        if variables:
            agent.set_variables(**variables)
        if config_overrides is not None:
            if isinstance(config_overrides, LLMParams):
                agent.apply_config_overrides(overrides=config_overrides)
            else:
                agent.apply_config_overrides(**config_overrides)

        extra_client_tools: list[str] = []
        if custom_tools:
            parsed_tools = [
                t if isinstance(t, CustomTool) else CustomTool.from_dict(t) for t in custom_tools
            ]
            agent.config.custom_tools = list(agent.config.custom_tools or []) + parsed_tools
            extra_client_tools.extend(t.name for t in parsed_tools)
        if client_tools:
            extra_client_tools.extend(client_tools)

        if request_metadata:
            agent.request_metadata.update(request_metadata)

        # Explicit machine-run citations policy — flows to the provider
        # translator gate via config.metadata (resolve_citations_disabled_reason;
        # the strip announces itself loudly whenever documents are present).
        if cls.citations_enabled is not None:
            agent.config.metadata["citations_enabled"] = cls.citations_enabled

        from matrx_ai.agents.source_tracking import resolve_child_source

        resolved_app, resolved_feature = resolve_child_source(
            source_app=source_app or cls.child_source_app,
            source_feature=source_feature or cls.child_source_feature or cls.name,
            caller=f"{cls.__name__}.run",
        )

        result = await run_agent(
            agent,
            label=label or cls.name,
            source_app=resolved_app,
            source_feature=resolved_feature,
            user_input=user_input,
            json_schema=cls.Output,
            extra_client_tools=extra_client_tools or None,
            independent_request=independent_request,
            suppress_stream=suppress_stream,
        )

        if result.parsed is not None:
            processed = cls.post_process(result.parsed)
            if processed is not None and processed is not result.parsed:
                result.parsed = processed

        return result

    @classmethod
    def _coerce_inputs(cls, inputs: BaseModel | dict[str, Any]) -> BaseModel:
        if isinstance(inputs, cls.Inputs):
            return inputs
        if isinstance(inputs, BaseModel):
            return cls.Inputs.model_validate(inputs.model_dump())
        if isinstance(inputs, dict):
            return cls.Inputs.model_validate(inputs)
        raise TypeError(
            f"{cls.__name__}.run(inputs=...) expects an instance of {cls.__name__}.Inputs "
            f"or a dict; got {type(inputs).__name__}."
        )

    @classmethod
    def _check_definition(cls) -> None:
        missing: list[str] = []
        if not getattr(cls, "name", None):
            missing.append("name")
        if not getattr(cls, "Inputs", None):
            missing.append("Inputs")
        has_source = getattr(cls, "source", None) is not None
        has_mandate = bool(getattr(cls, "mandate_key", None))
        if not has_source and not has_mandate:
            missing.append("mandate_key (or, for an un-mandated agent, source)")
        if missing:
            raise TypeError(
                f"{cls.__name__} is missing required class attribute(s): "
                f"{', '.join(missing)}. Every NamedAgent must declare name, "
                f"Inputs, and a way to know WHICH agent runs — normally "
                f"mandate_key, so the database decides."
            )
        if has_source and has_mandate:
            # The antipattern that produced two years of stale ids: a Mandate for
            # the real answer plus a hardcoded one "just in case". There is no
            # in-case — resolution failure refuses the run.
            raise TypeError(
                f"{cls.__name__} declares BOTH mandate_key={cls.mandate_key!r} and a "
                f"hardcoded source. A mandated agent never carries an agent id: "
                f"the DB owns which agent runs and whether it is version-pinned. "
                f"Delete the source."
            )

    @classmethod
    async def validate(cls, *, source_override: AgentSource | None = None) -> AgentValidationReport:
        """Load the agent's source and verify the Inputs contract matches it.

        No LLM call. This is the per-agent half of the ship-time check that
        replaces ``AgentRunnerSpec.validate_spec`` — it catches the exact
        class of drift behind the 2026-05-26 PDF incident (an Inputs field
        named ``content`` while the agent's declared variable is
        ``text_extracted_from_pdf``, which would silently render empty).

        Validation is DATA-DRIVEN — it reads ONLY the agent's declared
        contract (``variable_definitions`` -> ``variable_defaults`` and
        ``context_policies``). It never inspects prompt content / messages; the
        named variables and context entries are the single source of truth.

        Checks:
          * Every mapped target (``variable_map`` value) names an Inputs
            field that exists. A dangling map entry is an ERROR.
          * Every mapped target's destination names a declared variable or
            context policy on the agent. Mapping onto a name the agent doesn't
            declare is an ERROR.
          * Every ``required=True`` declared variable is covered by a
            supplied value. A missing required var is an ERROR.
          * Every supplied name that matches no declared variable/context
            slot is a WARNING (likely a rename/typo).

        Returns an ``AgentValidationReport`` — never raises on drift, so a
        bulk validator can aggregate across every registered agent.
        """
        try:
            cls._check_definition()
        except TypeError as exc:
            # A class that declares BOTH mandate_key and source used to crash
            # the bulk ship-time validator. Report it; never abort the run.
            report = AgentValidationReport(
                label=getattr(cls, "name", None) or cls.__name__,
                source_kind="invalid",
            )
            report.errors.append(str(exc))
            report.ok = False
            return report

        validation_source = source_override or cls.source
        validation_target: Literal["seed", "resolved"] = (
            "resolved" if source_override else "seed"
        )
        if validation_source is None and getattr(cls, "mandate_key", None):
            try:
                from matrx_ai.mandates import resolve_mandate_for

                resolution = await resolve_mandate_for(cls)
                validation_source = resolution.source
                validation_target = "resolved"
            except Exception as exc:  # noqa: BLE001 — report, never crash the bulk run
                report = AgentValidationReport(
                    label=cls.name,
                    source_kind="MandateResolution",
                    validation_target="resolved",
                )
                report.errors.append(
                    f"failed to resolve mandate {cls.mandate_key!r}: {exc}"
                )
                report.ok = False
                return report

        source_kind = type(validation_source).__name__
        report = AgentValidationReport(
            label=cls.name,
            source_kind=source_kind,
            validation_target=validation_target,
        )

        input_fields = set(cls.Inputs.model_fields.keys())

        # Dangling map targets: a variable_map value whose key isn't an Inputs field.
        for local_field in cls.variable_map.keys():
            if local_field not in input_fields:
                report.errors.append(
                    f"variable_map key {local_field!r} is not a field on "
                    f"{cls.Inputs.__name__} (has: {sorted(input_fields)})."
                )

        supplied_vars = {cls.variable_map.get(f, f) for f in input_fields}

        # Version discipline (see _agent_version_status): floating is the SAFE
        # default during active dev; a stale PIN is the real hazard. Recorded as
        # structured fields; the caller renders them as a table.
        version_source = (
            validation_source
            if isinstance(validation_source, AgentRecordSource)
            else cls.source
        )
        if isinstance(version_source, AgentRecordSource):
            (
                report.is_floating,
                report.pinned_version,
                report.latest_version,
            ) = await _agent_version_status(version_source)

        if validation_source is None:
            report.errors.append(
                f"{cls.__name__} has no source to validate against "
                f"(mandate_key={getattr(cls, 'mandate_key', None)!r})."
            )
            report.ok = False
            return report

        try:
            agent = await validation_source.load()
        except Exception as exc:  # noqa: BLE001 — report, never crash the bulk run
            report.errors.append(f"failed to load source ({source_kind}): {exc}")
            report.ok = False
            return report

        # The DECLARED contract — the data, never the content.
        declared_vars = _declared_variable_names(agent)
        declared_context = _declared_context_names(agent)
        declared_all = declared_vars | declared_context
        required_vars = _required_variable_names(agent)

        # Every variable_map destination must name a real declared variable or
        # context policy. Mapping onto a name the agent doesn't declare is the
        # exact drift the map exists to prevent — flag it loudly.
        for dest in cls.variable_map.values():
            if dest not in declared_all:
                report.errors.append(
                    f"variable_map maps onto {dest!r}, which the agent does not "
                    f"declare. Declared variables: {sorted(declared_vars)}; "
                    f"declared context policies: {sorted(declared_context)}."
                )

        # If the subclass overrides prepare_variables, the runtime variable set
        # is computed imperatively and can't be derived statically from Inputs +
        # variable_map. Don't false-positive — note it and skip the supply-based
        # checks (the dangling-map and load checks above still apply).
        overrides_prepare = (
            cls.prepare_variables.__func__  # type: ignore[attr-defined]
            is not NamedAgent.prepare_variables.__func__  # type: ignore[attr-defined]
        )
        if overrides_prepare:
            report.warnings.append(
                "custom prepare_variables() — static required/coverage checks "
                "skipped; relies on runtime mapping."
            )
        else:
            # Required declared variables must be covered by a supplied value.
            missing_required = required_vars - supplied_vars
            if missing_required:
                report.errors.append(
                    f"agent requires variable(s) {sorted(missing_required)} but "
                    f"the Inputs contract supplies {sorted(supplied_vars)}."
                )

            # Supplied a name the agent doesn't declare (variable OR context) —
            # warn (likely a rename/typo that would render empty / be ignored).
            undeclared = supplied_vars - declared_all
            if undeclared:
                report.warnings.append(
                    f"Inputs supply name(s) {sorted(undeclared)} that match no "
                    f"declared variable or context policy — possible rename/typo. "
                    f"Declared: {sorted(declared_all)}."
                )

        report.ok = not report.errors
        return report


async def validate_all_named_agents(*, scream: bool = True) -> list[AgentValidationReport]:
    """Validate every registered ``NamedAgent``. No LLM calls.

    Callers (the ship-time script) import the agent-defining modules first
    so the registry is populated, then call this. On any error, emits a loud
    red ``vcprint`` banner per failing agent when ``scream`` is True. Returns
    every report so the caller can compute an exit code / summary.
    """
    reports: list[AgentValidationReport] = []
    for agent_cls in iter_registered_named_agents():
        try:
            report = await agent_cls.validate()
        except Exception as exc:  # noqa: BLE001 — one bad class must not abort the run
            report = AgentValidationReport(
                label=getattr(agent_cls, "name", None) or agent_cls.__name__,
                source_kind="crash",
            )
            report.errors.append(f"{type(exc).__name__}: {exc}")
            report.ok = False
        reports.append(report)
        if scream and not report.ok:
            vcprint(
                report.model_dump(),
                title=f"[NamedAgent] VALIDATION FAILED: {report.label}",
                color="red",
            )
    return reports
