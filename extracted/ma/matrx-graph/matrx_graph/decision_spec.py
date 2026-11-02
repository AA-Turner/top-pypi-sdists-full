"""The HUMAN GATE's typed decision spec — what a person is asked to settle.

A human gate is ``control.human_input`` with ``preset="decision"`` (sugar over
the ONE pause primitive — same interrupt, same ``POST /runs/{id}/resume``, same
``human_answer`` output). Its question is not a free-text box but a short list
of ITEMS, each a thing we believe (a value, where it came from, how sure we
are) and the quick choices the person may make about it:

* ``confirm``   — "yes, that's right"
* ``not_true``  — "Not true": the item is wrong (shown as "Not true" in every decision panel)
* ``edit``      — "almost — here is the right value"
* ``pick_one`` / ``pick_many`` — choose from the item's ``options``
* ``custom``    — "none of those — here is mine"

**The engine owns the gate, not the UI.** Downstream nodes cannot start until
the gate node completes, and it completes only on a resume whose answer passes
the schema derived here (:func:`decision_schema_hint`) — every required item
answered, every verdict one the item allows, at least ``min_answers`` answered.
A malformed answer leaves the run INTERRUPTED.

**What the answers write** is declared per item (``writes``) and travels in the
durable checkpoint. On resume the ENGINE (never the client) joins the spec with
the answers into ``decision`` on the node's output (:func:`resolve_decision`),
so a downstream writer applies exactly the targets the author declared — a
client cannot add a target, rename one, or forge a value it never answered.
The targets are opaque strings to this package; the host registers what each
one means (aidream: ``human.apply_decision``).

Contract doc: common-docs/systems/workflows/human-gates/FEATURE.md.
"""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator

DecisionChoice = Literal["confirm", "not_true", "edit", "pick_one", "pick_many", "custom"]

#: Verdicts that carry a ``value`` from the person (the rest settle the item's own value).
VALUE_VERDICTS: frozenset[str] = frozenset({"edit", "pick_one", "pick_many", "custom"})

DEFAULT_CHOICES: tuple[DecisionChoice, ...] = ("confirm", "not_true", "edit")


class DecisionOption(BaseModel):
    model_config = ConfigDict(extra="forbid")

    value: JsonValue = Field(description="What is recorded when this option is picked.")
    label: str = Field(description="What the person sees.")


class DecisionWrite(BaseModel):
    """Where an answered item lands. ``target`` is a host-registered name."""

    model_config = ConfigDict(extra="forbid")

    target: str = Field(
        description=(
            "Host-registered write target, e.g. 'brand.profile_key', 'brand.name', "
            "'web.discovered_item'. Unknown targets are refused by the host writer, loudly."
        )
    )
    key: str | None = Field(default=None, description="Field/key inside the target (e.g. profile key).")
    record_id: str | None = Field(default=None, description="Exact row when the target is one row.")


class DecisionItem(BaseModel):
    model_config = ConfigDict(extra="forbid")

    key: str = Field(min_length=1, description="Stable id of the item inside this gate.")
    label: str = Field(description="What the item is, e.g. 'What you do'.")
    value: JsonValue = Field(default=None, description="What we currently believe.")
    source: str | None = Field(default=None, description="Where the value came from.")
    confidence: float | None = Field(default=None, ge=0, le=1, description="0..1, when known.")
    choices: list[DecisionChoice] = Field(default_factory=lambda: list(DEFAULT_CHOICES))
    options: list[DecisionOption] = Field(default_factory=list)
    required: bool = Field(default=False, description="Must be answered before the gate opens.")
    writes: DecisionWrite | None = None

    @field_validator("choices")
    @classmethod
    def _non_empty(cls, value: list[str]) -> list[str]:
        if not value:
            raise ValueError("an item needs at least one choice")
        return list(dict.fromkeys(value))


class DecisionSubject(BaseModel):
    """The record this gate decides about. Its EDITORS may answer (host-enforced)."""

    model_config = ConfigDict(extra="forbid")

    entity_type: str = Field(description="platform.entity_types token, e.g. 'web_brand'.")
    id: str = Field(description="The record id. '{dot.path}' interpolates from the node's inputs.")
    level: Literal["editor", "admin", "owner"] = "editor"


class DecisionSeat(BaseModel):
    """The SEAT this gate is addressed to — an org-chart position (``matrx_graph.seats``).

    The author names the seat (``position_id``, optional ``label``). Everything
    else is STAMPED BY THE ENGINE when the gate opens, from the host's seat
    resolver: whoever holds the seat at that moment is asked. The seat decides
    who is asked, never who may answer."""

    model_config = ConfigDict(extra="forbid")

    position_id: str = Field(
        min_length=1,
        description="The position (seat) id. '{dot.path}' interpolates from the node's inputs.",
    )
    label: str | None = Field(default=None, description="The author's name for the seat, e.g. 'Brand owner'.")
    # ── engine-stamped at gate open; an author value is overwritten ──
    seat_name: str | None = Field(default=None, description="The seat's name as the org chart has it.")
    holder_user_id: str | None = Field(default=None, description="Who held the seat when the gate opened.")
    holder_name: str | None = Field(default=None, description="That person's name.")
    filled: bool | None = Field(default=None, description="False = nobody held the seat; the gate stays open.")
    notice: str | None = Field(default=None, description="What the gate says about the seat, e.g. 'No one holds Brand owner'.")
    notified: bool | None = Field(default=None, description="Whether the holder was told through the host's notifications.")


class DecisionSpec(BaseModel):
    model_config = ConfigDict(extra="forbid")

    items: list[DecisionItem] = Field(default_factory=list)
    min_answers: int = Field(default=0, ge=0, description="At least this many items answered.")
    subject: DecisionSubject | None = None
    seat: DecisionSeat | None = Field(
        default=None,
        description=(
            "Address the gate to whoever holds this org-chart seat when it opens. "
            "Who may answer is unchanged (the run's or the subject record's rule)."
        ),
    )
    submit_label: str = Field(default="Confirm", description="The one button.")


class DecisionAnswer(BaseModel):
    model_config = ConfigDict(extra="forbid")

    verdict: DecisionChoice
    value: JsonValue = None


class ResolvedDecisionItem(BaseModel):
    """One item after the person answered — what downstream reads and writes."""

    model_config = ConfigDict(extra="forbid")

    key: str
    label: str
    verdict: DecisionChoice | None = Field(default=None, description="None = left unanswered.")
    original: JsonValue = None
    value: JsonValue = Field(default=None, description="The settled value (None for not_true / unanswered).")
    source: str | None = None
    confidence: float | None = None
    writes: DecisionWrite | None = None


def merge_items(spec: DecisionSpec, extra_items: list[object] | None) -> DecisionSpec:
    """The spec plus items an upstream step produced (inputs ``decision_items``).

    Later keys never shadow earlier ones silently — a duplicate key is a wiring
    defect and raises."""
    items = list(spec.items)
    for raw in extra_items or []:
        items.append(DecisionItem.model_validate(raw))
    seen: set[str] = set()
    for item in items:
        if item.key in seen:
            raise ValueError(f"decision item key {item.key!r} appears twice")
        seen.add(item.key)
    if spec.min_answers > len(items):
        raise ValueError(f"min_answers={spec.min_answers} but only {len(items)} items")
    return spec.model_copy(update={"items": items})


def _value_schema(item: DecisionItem, verdict: str) -> dict[str, JsonValue]:
    if verdict in ("pick_one", "pick_many") and item.options:
        allowed: list[JsonValue] = [o.value for o in item.options]
        if verdict == "pick_one":
            return {"enum": allowed}
        return {"type": "array", "minItems": 1, "items": {"enum": allowed}}
    return {}


def decision_schema_hint(spec: DecisionSpec) -> dict[str, JsonValue]:
    """The JSON Schema the resume admission enforces for this gate.

    Shape: ``{"answer": {"answers": {<item key>: {"verdict": ..., "value": ...}}}}``.
    Per item: only its declared choices; value-carrying verdicts REQUIRE a value
    (pick verdicts constrained to the options). Required items and
    ``min_answers`` are enforced here too — so the existing resume validator
    refuses an incomplete gate and the run stays interrupted."""
    properties: dict[str, JsonValue] = {}
    for item in spec.items:
        variants: list[JsonValue] = []
        for verdict in item.choices:
            branch: dict[str, JsonValue] = {
                "type": "object",
                "properties": {"verdict": {"const": verdict}},
                "required": ["verdict"],
                "additionalProperties": False,
            }
            props = branch["properties"]
            assert isinstance(props, dict)
            if verdict in VALUE_VERDICTS:
                props["value"] = _value_schema(item, verdict)
                branch["required"] = ["verdict", "value"]
            else:
                props["value"] = {}
            variants.append(branch)
        properties[item.key] = {"oneOf": variants}
    answers: dict[str, JsonValue] = {
        "type": "object",
        "properties": properties,
        "additionalProperties": False,
        "required": [i.key for i in spec.items if i.required],
    }
    if spec.min_answers:
        answers["minProperties"] = spec.min_answers
    return {
        "type": "object",
        "properties": {
            "answer": {
                "type": "object",
                "properties": {"answers": answers},
                "required": ["answers"],
            }
        },
        "required": ["answer"],
    }


def resolve_decision(
    spec_payload: dict[str, object], resume_value: dict[str, object] | None
) -> list[dict[str, JsonValue]]:
    """Join the DURABLE spec with the person's answers — engine-side, never client-side.

    ``spec_payload`` is the ``decision`` block frozen in the interrupt checkpoint."""
    spec = DecisionSpec.model_validate(spec_payload)
    answer = (resume_value or {}).get("answer")
    raw_answers = answer.get("answers") if isinstance(answer, dict) else None
    answers = raw_answers if isinstance(raw_answers, dict) else {}
    out: list[dict[str, JsonValue]] = []
    for item in spec.items:
        raw = answers.get(item.key)
        verdict: str | None = None
        value: JsonValue = None
        if isinstance(raw, dict):
            parsed = DecisionAnswer.model_validate(raw)
            verdict = parsed.verdict
            if verdict == "confirm":
                value = item.value
            elif verdict in VALUE_VERDICTS:
                value = parsed.value
        out.append(
            ResolvedDecisionItem(
                key=item.key,
                label=item.label,
                verdict=verdict,  # type: ignore[arg-type]
                original=item.value,
                value=value,
                source=item.source,
                confidence=item.confidence,
                writes=item.writes,
            ).model_dump(mode="json")
        )
    return out


class DecisionDefaultError(ValueError):
    """The gate's declared default cannot settle it — named, never guessed."""


def default_decision_answer(
    spec_payload: dict[str, object], default_answer: object
) -> dict[str, JsonValue]:
    """Turn a decision gate's DEFAULT answer into a resume value its schema accepts.

    A ``decision`` gate's resume shape is ``{"answer": {"answers": {...}}}``
    (:func:`decision_schema_hint`), but its author declares ``default_answer``
    as one value (e.g. ``"keep_going"``). This is the ONE translation every
    deadline uses, so every decision gate can time out to its default:

    * an item whose ``pick_one`` options contain the default is answered with it
      (``pick_many``: a one-item list);
    * otherwise an item that allows ``confirm`` is confirmed (its own value stands);
    * otherwise the item is left unanswered — and if it is ``required``, or the
      gate's ``min_answers`` cannot be met, :class:`DecisionDefaultError` names why.

    An already-shaped default (``{"answers": {...}}`` or ``{"answer": {"answers": ...}}``)
    is passed through. The result is checked against the gate's own schema.
    """
    spec = DecisionSpec.model_validate(spec_payload)
    if isinstance(default_answer, dict):
        if isinstance(default_answer.get("answer"), dict):
            return dict(default_answer)  # type: ignore[arg-type]
        if isinstance(default_answer.get("answers"), dict):
            return {"answer": dict(default_answer)}  # type: ignore[dict-item]
    answers: dict[str, JsonValue] = {}
    for item in spec.items:
        option_values = [o.value for o in item.options]
        if "pick_one" in item.choices and default_answer in option_values:
            answers[item.key] = {"verdict": "pick_one", "value": default_answer}  # type: ignore[dict-item]
        elif "pick_many" in item.choices and default_answer in option_values:
            answers[item.key] = {"verdict": "pick_many", "value": [default_answer]}  # type: ignore[list-item]
        elif "confirm" in item.choices:
            answers[item.key] = {"verdict": "confirm"}
        elif item.required:
            raise DecisionDefaultError(
                f"the default answer {default_answer!r} cannot settle required item "
                f"{item.key!r}: it is none of its options and the item does not allow 'confirm'"
            )
    if len(answers) < spec.min_answers:
        raise DecisionDefaultError(
            f"the default answer {default_answer!r} settles {len(answers)} item(s); "
            f"the gate needs at least {spec.min_answers}"
        )
    value: dict[str, JsonValue] = {"answer": {"answers": answers}}
    from matrx_graph.executor.schema_validation import validate_instance

    problems = validate_instance(decision_schema_hint(spec), value)
    if problems:
        raise DecisionDefaultError("; ".join(problems))
    return value


def wants_an_object_answer(schema_hint: object) -> bool:
    """True when a gate's ``schema_hint`` asks for the answer AS an object (a form or an
    approval: ``{"decision": ...}``), not wrapped under ``answer``. A schema that itself
    declares an ``answer`` property keeps the wrapped shape."""
    if not isinstance(schema_hint, dict):
        return False
    props = schema_hint.get("properties")
    if schema_hint.get("type") != "object" and not isinstance(props, dict):
        return False
    return not (isinstance(props, dict) and "answer" in props)


def object_default_from_text(schema_hint: object, raw: object) -> dict[str, JsonValue] | None:
    """A ``control.human_input`` default is TEXT; on a gate whose schema wants an object,
    text that parses as a JSON object IS that object (the AI-visibility gates declare
    ``'{"decision": "continue", ...}'``). ``None`` when it does not apply."""
    if not isinstance(raw, str) or not wants_an_object_answer(schema_hint):
        return None
    import json

    try:
        parsed = json.loads(raw)
    except ValueError:
        return None
    return parsed if isinstance(parsed, dict) else None


def default_answer_resume_value(interrupt_payload: dict[str, object]) -> dict[str, JsonValue] | None:
    """The resume value a gate's declared default stands for, for ANY preset.

    ``None`` when the gate declares no default. A ``decision`` gate goes through
    :func:`default_decision_answer`; a gate whose ``schema_hint`` wants an object
    takes JSON-object text as that object (:func:`object_default_from_text`);
    every other preset keeps the long-standing shape (a dict verbatim, a scalar
    as ``{"answer": <default>}``)."""
    raw = interrupt_payload.get("default_answer")
    if raw in (None, ""):
        return None
    block = interrupt_payload.get("decision")
    if isinstance(block, dict):
        return default_decision_answer(block, raw)
    if isinstance(raw, dict):
        return dict(raw)  # type: ignore[arg-type]
    as_object = object_default_from_text(interrupt_payload.get("schema_hint"), raw)
    if as_object is not None:
        return as_object
    return {"answer": raw}  # type: ignore[dict-item]


def default_answer_problems(schema_hint: object, default_answer: object) -> list[str]:
    """Why a gate's declared default could never settle it on timeout (``[]`` = it can).

    The SAVE-time twin of the resume admission: the default is shaped exactly as the
    deadline would shape it and checked against the same schema. A default holding
    ``{placeholders}`` filled at run time (and not JSON) is checked at run time only."""
    if default_answer in (None, "") or not isinstance(schema_hint, dict):
        return []
    from matrx_graph.executor.schema_validation import resume_value_validation_errors

    if isinstance(default_answer, str) and object_default_from_text(schema_hint, default_answer) is None:
        from matrx_graph.nodes._template import render_template_string

        if render_template_string(default_answer, {}, whole_key="inputs")[0] != default_answer:
            return []
    payload: dict[str, object] = {"default_answer": default_answer, "schema_hint": schema_hint}
    value = default_answer_resume_value(payload)
    return resume_value_validation_errors(payload, value)


__all__ = [
    "DEFAULT_CHOICES",
    "VALUE_VERDICTS",
    "DecisionAnswer",
    "DecisionChoice",
    "DecisionDefaultError",
    "DecisionItem",
    "DecisionOption",
    "DecisionSeat",
    "DecisionSpec",
    "DecisionSubject",
    "DecisionWrite",
    "ResolvedDecisionItem",
    "decision_schema_hint",
    "default_answer_problems",
    "default_answer_resume_value",
    "default_decision_answer",
    "merge_items",
    "object_default_from_text",
    "resolve_decision",
]
