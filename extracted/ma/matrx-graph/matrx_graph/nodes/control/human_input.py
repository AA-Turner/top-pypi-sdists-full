from __future__ import annotations

from typing import ClassVar, Literal

from pydantic import BaseModel, ConfigDict, Field, JsonValue, field_validator, model_validator

from matrx_graph.decision_spec import (
    DecisionSeat,
    DecisionSpec,
    decision_schema_hint,
    default_answer_problems,
    merge_items,
)
from matrx_graph.decisions import (
    DecisionFallback,
    DecisionProvenance,
    EscalationPolicy,
    build_escalation_payload,
)
from matrx_graph.nodes._template import render_template_string
from matrx_graph.nodes.output.to_frontend import (
    WORKFLOW_RENDER_SURFACE,
    EmitPresentation,
)
from matrx_graph.content_ir.model import KindModel
from matrx_graph.content_ir.sdk import kind
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory
from matrx_graph.types.result import NodeResult, failure, success
from matrx_graph.types.usl import field_extras


class HumanInputInput(BaseModel):
    model_config = ConfigDict(extra="allow")

    context: dict[str, JsonValue] = Field(
        default_factory=dict,
        description=(
            "Arbitrary context passed to the UI to help the person answer. A set "
            "of named values; a bare text, number or list is accepted and shown "
            "under the name 'context'."
        ),
    )

    @field_validator("context", mode="before")
    @classmethod
    def _wrap_bare_context(cls, value: object) -> object:
        # 2026-09-11 (expert-book challenge W23): an author wired a plain
        # summary string into ``context`` and the run died at the human pause
        # with a dict_type error. The person only needs to SEE the context, so
        # a bare value is carried under one name rather than refused.
        if value is None or isinstance(value, dict):
            return value
        return {"context": value}

    items: list[JsonValue] | None = Field(
        default=None,
        description=(
            "List preset only: the list the person edits. Shown one item per "
            "line; their edited lines come back as the step's answer, a list."
        ),
    )

    decision_items: list[dict[str, JsonValue]] = Field(
        default_factory=list,
        description=(
            "Decision preset only: items an upstream step produced, appended to "
            "config.decision.items (same shape: key, label, value, source, "
            "confidence, choices, options, required, writes)."
        ),
    )


@kind(
    "human_answer",
    disposition="record",
    label="Human Answer",
    family="control_flow",
    example={
        "answer": "Approved — ship it.",
        "matrx_decision": None,
        "extras": {"ticket_id": "T-9"},
    },
    # DISTILLED. This node was BLOCKED through the whole burndown because its
    # resume payload is client-authored and used to be recorded at the root, so
    # there was no stable key set to declare. Arman's 2026-08-21 ruling gave the
    # open half a declared home (``extras``), which is what makes the shape
    # declarable at all. ``answer`` remains JsonValue because a person may
    # answer with a string, number, choice, or whole object.
    maturity="distilled",
)
class HumanInputOutput(KindModel, kind="human_answer"):
    """On normal (resumed) execution, the value the user supplied becomes this
    node's output. On resume, the scheduler populates this model from the
    resume payload.
    """

    # CLOSED (Arman's ruling, 2026-08-21). The resume payload is CLIENT-authored
    # — the UI may collect keys nobody declared — but those keys now land in the
    # declared ``extras`` map instead of at the root, so this node HAS an honest
    # output shape and can carry a kind. The engine folds them on resume; see
    # ``matrx_graph.executor.client_payload``. Nothing is dropped and nothing is
    # renamed: a key moves one level down, keeping its name. (``extra="forbid"``
    # now comes from KindModel — a kind is a CONTRACT, same rule, one source.)

    answer: JsonValue = Field(
        default=None, description="The value the person supplied when the run resumed."
    )
    extras: dict[str, JsonValue] = Field(
        default_factory=dict,
        description=(
            "Anything else the UI collected alongside the answer. Declared so "
            "client-authored keys have a readable home — at the root nothing "
            "could know to look for them."
        ),
        # The published contract has always permitted a self-description marker
        # in this open map. Keep that affordance while moving publication to the
        # owning model; it is optional because ordinary client extras need no
        # marker at all.
        json_schema_extra={
            "properties": {
                "__kind": {
                    "type": "string",
                    "description": "The registered kind this payload is an instance of, when it is one.",
                }
            }
        },
    )
    decision: list[dict[str, JsonValue]] | None = Field(
        default=None,
        description=(
            "Decision preset only: every item of the gate joined with the "
            "person's verdict and settled value, plus the write target the "
            "AUTHOR declared. Built by the engine from the durable checkpoint "
            "on resume — never client-authored."
        ),
    )
    matrx_decision: DecisionProvenance | None = Field(
        default=None,
        description=(
            "WHO decided — the person who was asked, or the fallback that "
            "decided for them once the deadline passed. Stamped by the engine "
            "on resume; never author-supplied, never client-supplied. Travels "
            "downstream with the answer so any surface can show a user that an "
            "agent decided because nobody answered in time."
        ),
    )


#: The presets a decision point may be authored as. SUGAR OVER ONE PRIMITIVE —
#: never a second node type and never a second endpoint: every preset raises the
#: same interrupt, resumes through the same ``POST /runs/{id}/resume``, and
#: settles into the same ``human_answer`` output. A preset only decides what the
#: question LOOKS like when the author declared no schema of their own.
HumanInputPreset = Literal["free_text", "form", "approval", "decision", "list"]


def list_answer(answer: JsonValue) -> list[str]:
    """The ``list`` preset's answer as the list it stands for: one item per non-empty line,
    trimmed. A list answer (a screen that sends one) is trimmed the same way."""
    lines = answer if isinstance(answer, list) else str(answer or "").splitlines()
    return [text for item in lines if (text := str(item).strip())]

#: The schema the ``approval`` preset derives when the author supplied none.
#: SPEC-workflow-ui-contract §4.2 verbatim — Approve/Reject plus an optional
#: note. Derived, never stored on the node: an author who later writes their own
#: ``schema_hint`` wins, and a change here reaches every existing approval node.
APPROVAL_SCHEMA_HINT: dict[str, JsonValue] = {
    "type": "object",
    "properties": {
        "approved": {"type": "boolean"},
        "note": {"type": "string"},
    },
    "required": ["approved"],
}


class HumanInputConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt: str = Field(
        default="Please provide input to continue",
        description=(
            "Question or instruction shown to the user. '{dot.path}' "
            "placeholders interpolate values from this node's inputs (missing "
            "paths render as ''), so upstream data — a draft, a list of "
            "suggestions — can appear inside the question."
        ),
        json_schema_extra=field_extras(widget="textarea", help="What the user sees"),
    )
    default_answer: str = Field(
        default="",
        description=(
            "Optional pre-filled answer shown in the input box, with the same "
            "'{dot.path}' interpolation from this node's inputs. Use it to "
            "hand the person an editable draft (e.g. suggested keywords, one "
            "per line) instead of an empty box."
        ),
        json_schema_extra=field_extras(widget="textarea"),
    )
    schema_hint: dict[str, JsonValue] | None = Field(
        default=None,
        description=(
            "Optional JSON Schema describing the expected shape of the user's "
            "response. The UI renders a matching form and the engine rejects "
            "a resume value that does not satisfy it."
        ),
        json_schema_extra=field_extras(widget="json"),
    )
    decision: DecisionSpec | None = Field(
        default=None,
        description=(
            "The HUMAN GATE (preset 'decision'): a short list of items the "
            "person settles — confirm / not true / edit / pick one / pick many "
            "/ custom — each showing its source and confidence, with optional "
            "required items, a minimum number of answers, the record whose "
            "editors may answer, and where each answer is written. Downstream "
            "steps cannot start until it is answered."
        ),
        json_schema_extra=field_extras(widget="json", help="Items to confirm before the run goes on"),
    )
    escalation: EscalationPolicy | None = Field(
        default=None,
        description=(
            "Optional deadline. Left empty, the run waits for the person "
            "indefinitely (the historical behavior). Set, the run continues "
            "without them once the deadline passes — an AI agent decides, or "
            "the default answer is applied — and the output records who "
            "decided. The person is always notified first and always wins if "
            "they answer in time."
        ),
        json_schema_extra=field_extras(widget="json", help="Timed hand-off to AI"),
    )

    # ── THE PRESENTATION BLOCK (SPEC-workflow-ui-contract §4.1) ─────────────
    # The emission's block, VERBATIM: a question part-way through a run is
    # presented with the same vocabulary as a deliverable, so one screen
    # renders both. Every default reproduces today's behavior exactly — an
    # existing node's interrupt payload gains keys, never different values.
    preset: HumanInputPreset = Field(
        default="free_text",
        description=(
            "What KIND of question this is: 'free_text' (a box), 'form' (the "
            "schema_hint's fields), 'approval' (Approve / Reject plus an "
            "optional note), 'decision' (the human gate: items to confirm, "
            "correct or pick from — see 'decision'), or 'list' (edit the incoming "
            "'items' one per line; the answer is the edited list). A preset is sugar over this one node — it never "
            "changes how the run pauses or how the answer comes back."
        ),
        json_schema_extra=field_extras(widget="select", help="Pick 'approval' for a sign-off step"),
    )
    title: str | None = Field(
        default=None,
        description="Human label for this question on the screen.",
        json_schema_extra=field_extras(widget="text", placeholder="Approve the draft"),
    )
    presentation: EmitPresentation = Field(
        default="panel",
        description=(
            "How to show it: 'panel' (the step's normal window panel) or "
            "'showcase' (a large, centered presentation of just this question "
            "— the sign-off you want the person to actually see)."
        ),
        json_schema_extra=field_extras(
            widget="select", help="Pick 'showcase' for a decision that must not be missed"
        ),
    )
    component_ref: str | None = Field(
        default=None,
        description=(
            "Name (tool_ui.tool_name) of a custom render component for this "
            "question's context. Leave empty to render the context by its kind."
        ),
    )
    surface: str = Field(
        default=WORKFLOW_RENDER_SURFACE,
        description="The ui_surface the component is resolved against.",
        json_schema_extra=field_extras(hidden=True),
    )

    def effective_schema_hint(self) -> dict[str, JsonValue] | None:
        """The schema the UI renders and the engine validates a resume against.

        The author's own ``schema_hint`` ALWAYS wins; a preset only fills the
        hole when they declared none. ``approval`` is the only preset that
        derives one — 'form' renders whatever schema the author wrote, and
        'free_text' has nothing to derive."""
        if self.schema_hint is not None:
            return self.schema_hint
        if self.preset == "approval":
            return dict(APPROVAL_SCHEMA_HINT)
        return None

    @model_validator(mode="after")
    def _default_answer_can_settle_the_gate(self) -> HumanInputConfig:
        # Refused at SAVE: a deadline that applies this default must be able to
        # resume the run. Before 2026-10-27 a form gate whose default broke its
        # own schema saved fine and FAILED the run when the wait ran out.
        if (
            self.preset == "decision"
            or self.escalation is None
            or self.escalation.fallback != DecisionFallback.DEFAULT_ANSWER
        ):
            return self
        problems = default_answer_problems(self.effective_schema_hint(), self.default_answer)
        if problems:
            raise ValueError(
                "the default answer cannot settle this question when the wait runs out — "
                "it does not fit the answer form: " + "; ".join(problems)
            )
        return self


async def _open_seat(
    ctx: NodeExecutionContext,
    seat: DecisionSeat,
    namespace: dict[str, object],
    *,
    title: str | None,
    prompt: str,
) -> tuple[DecisionSeat, NodeResult[HumanInputOutput] | None]:
    """Resolve the seat's holder NOW (gate-open time) and tell them.

    An empty seat is honest: the gate opens anyway, says nobody holds the seat,
    and waits — it never falls back to someone else. A seat that does not exist,
    or no resolver to ask, fails the step loudly."""
    import logging

    from matrx_graph import seats

    position_id, _ = render_template_string(seat.position_id, namespace, whole_key="inputs")
    position_id = position_id.strip()
    if not position_id:
        return seat, failure("seat_missing", "This decision is addressed to a seat, but no seat id was given.")
    app = ctx.app
    user_id = getattr(app, "user_id", None) or None
    organization_id = getattr(app, "organization_id", None) or None
    try:
        holder = await seats.resolve_seat(position_id, user_id=user_id, organization_id=organization_id)
    except Exception as exc:  # noqa: BLE001 — reported as the step's failure, never swallowed
        return seat, failure("seat_unresolved", f"Could not find who holds seat {position_id}: {exc}")
    if holder is None:
        return seat, failure(
            "seat_not_found",
            f"This decision is addressed to seat {seat.label or position_id}, which does not exist "
            "(or you cannot see it). Fix the seat on the step.",
        )
    name = holder.seat_name or seat.label or "this seat"
    filled = bool(holder.holder_user_id)
    stamped = seat.model_copy(
        update={
            "position_id": position_id,
            "seat_name": holder.seat_name,
            "holder_user_id": holder.holder_user_id,
            "holder_name": holder.holder_name,
            "filled": filled,
            "notice": (f"Waiting on {holder.holder_name} ({name})" if filled and holder.holder_name else
                       f"Waiting on {name}" if filled else f"No one holds {name}"),
            "notified": False,
        }
    )
    if filled:
        try:
            notified = await seats.notify_seat(
                holder,
                run_id=ctx.run_id,
                node_id=ctx.node_id,
                title=title,
                prompt=prompt,
                organization_id=organization_id,
            )
        except Exception:  # noqa: BLE001 — the gate still opens; the miss is recorded and logged
            logging.getLogger(__name__).exception(
                "seat gate: notifying the holder of seat %s failed (run %s, node %s)",
                position_id, ctx.run_id, ctx.node_id,
            )
            notified = False
        stamped = stamped.model_copy(update={"notified": notified})
    return stamped, None


class HumanInputExecutor:
    """Pause the run and surface a prompt to the user.

    Raises GraphInterrupt, which the scheduler catches and converts into an
    INTERRUPTED run with an interrupt checkpoint. The UI reads the interrupt
    payload (prompt + schema_hint + context) to render an input widget. On
    `POST /runs/:id/resume { value: ... }` the scheduler records `value` as
    this node's output and routes to downstream edges as though the node had
    returned it directly.
    """

    spec: ClassVar[NodeSpec] = NodeSpec(
        type="control.human_input",
        category=NodeCategory.CONTROL,
        display_name="Pause & Ask",
        description=(
            "PAUSE partway through a run to ask the person something, then "
            "continue with their answer. (Use 'Collect Inputs' instead if you "
            "just need inputs at the start.)"
        ),
        input_schema=HumanInputInput,
        output_schema=HumanInputOutput,
        output_kind="human_answer",
        config_schema=HumanInputConfig,
        handles=(
            HandleSpec(id="in", direction=HandleDirection.INPUT, required=False),
            HandleSpec(id="out", direction=HandleDirection.OUTPUT, required=False),
        ),
        determinism=ActionTier.NON_DETERMINISTIC,
        can_interrupt=True,
        icon="user-check",
    )

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: HumanInputInput,
        config: HumanInputConfig,
    ) -> NodeResult[HumanInputOutput]:
        namespace = inputs.model_dump(mode="json")
        prompt, _ = render_template_string(config.prompt, namespace, whole_key="inputs")
        default_answer, _ = render_template_string(
            config.default_answer, namespace, whole_key="inputs"
        )
        title, _ = render_template_string(config.title or "", namespace, whole_key="inputs")
        if config.preset == "list" and not default_answer.strip():
            default_answer = "\n".join(list_answer(inputs.items or []))
        schema_hint = config.effective_schema_hint()
        decision_block: dict[str, object] | None = None
        if config.preset == "decision":
            # THE HUMAN GATE. The spec (author items + upstream items) is frozen
            # into the durable interrupt payload; the schema the resume
            # admission enforces is DERIVED from it, so an incomplete or
            # off-menu answer leaves the run interrupted and nothing downstream
            # can start. An author-written schema_hint never applies here: the
            # gate's shape is the spec's, one source.
            spec = merge_items(config.decision or DecisionSpec(), inputs.decision_items)
            if not spec.items:
                return failure(
                    "decision_has_no_items",
                    "This decision step has nothing to ask: no items were "
                    "declared and none arrived from upstream.",
                )
            if spec.subject is not None:
                subject_id, _ = render_template_string(spec.subject.id, namespace, whole_key="inputs")
                spec = spec.model_copy(update={"subject": spec.subject.model_copy(update={"id": subject_id})})
            if spec.seat is not None:
                seat, refusal = await _open_seat(ctx, spec.seat, namespace, title=title or None, prompt=prompt)
                if refusal is not None:
                    return refusal
                spec = spec.model_copy(update={"seat": seat})
            decision_block = spec.model_dump(mode="json")
            schema_hint = decision_schema_hint(spec)
        payload: dict[str, object] = {
            "prompt": prompt,
            # The DERIVED hint: identical to config.schema_hint for every node
            # that declared one, and the approval shape for an approval preset
            # that did not. One value travels — the client, the resume
            # validator and the escalation agent never re-derive it.
            "schema_hint": schema_hint,
            "context": inputs.context,
            "default_answer": default_answer,
            # §4.1's presentation block, beside the question itself. Defaults
            # reproduce today's screen exactly.
            "preset": config.preset,
            "title": title or None,
            "presentation": config.presentation,
            "component_ref": config.component_ref,
            "surface": config.surface,
        }
        # The deadline is frozen ABSOLUTE here, into durable checkpoint state.
        # A worker that boots hours after a restart resolves the same instant
        # this node did — no arithmetic over an unknown downtime.
        if decision_block is not None:
            payload["decision"] = decision_block
        escalation = build_escalation_payload(config.escalation)
        if escalation is not None:
            payload["escalation"] = escalation
        ctx.interrupt(payload)
        # unreachable — ctx.interrupt() raises GraphInterrupt
        return success(HumanInputOutput())
