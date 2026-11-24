"""ActionSpec — a typed wrapper around a callable, registered as a node type.

An Action is a single unit of work with a strict I/O contract and an explicit
determinism tier. Under the hood every Action is registered as a `NodeSpec`
in the graph engine's node registry (so the palette can show it and the
scheduler can invoke it), plus it's registered in the action registry (so
`tool.call` can look it up by name at runtime).

The `@register_node` decorator is the primary authoring surface. It wraps a Python
async function with a NodeExecutor adapter that validates inputs, invokes
the underlying callable, and validates the output — giving full Pydantic
type-safety at the node boundary.
"""

from __future__ import annotations

import re

from collections.abc import Awaitable, Callable
from typing import Any, Generic, TypeVar

from matrx_utils.text_case import humanize_identifier
from pydantic import BaseModel, ConfigDict, Field, model_validator

from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import EmptyConfig, NodeSpec, model_json_schema_once
from matrx_graph.types.primitives import ActionTier, EdgeKind, NodeCategory

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


#: Namespaces of platform machinery: an Action named under one is hidden from a person's picker by
#: default (``ActionSpec.person_facing``). A namespace ending ``_test`` / starting ``test_`` counts too.
INTERNAL_ACTION_NAMESPACES: frozenset[str] = frozenset({"admin", "dev", "sql", "builder", "build", "test"})


#: The agent factory's own steps (``agent.build.*``, ``agent.proof.*``, ``agent.spec.*`` …): machinery that builds an
#: agent, never something a person picks. A person's own agents (``agent.id_<hex>``, ``agent.run``) stay.
AGENT_FACTORY_SEGMENTS: frozenset[str] = frozenset(
    {"build", "builder", "proof", "spec", "definition", "model", "foundry", "exemplar"}
)


def is_internal_action_name(name: str) -> bool:
    """True when ``name`` is machinery: its first segment is an internal namespace, any segment is a build step
    (``records.build.x``), or it is one of the agent factory's steps."""
    parts = name.split(".")
    head = parts[0]
    if head in INTERNAL_ACTION_NAMESPACES or head.endswith("_test") or head.startswith("test_"):
        return True
    if any(p in {"build", "builder"} for p in parts[1:]):
        return True
    return head == "agent" and len(parts) > 1 and (parts[1] in AGENT_FACTORY_SEGMENTS or parts[1].startswith("test"))


class ActionSpec(BaseModel, Generic[InputT, OutputT]):
    """Metadata for a registered Action.

    Not a Pydantic-validated row — just a typed container the registry hands
    out. Kept alongside the generated NodeSpec so introspection (for `/actions`
    and tool.call) doesn't have to re-derive determinism / author metadata
    from handle walks.
    """

    model_config = ConfigDict(arbitrary_types_allowed=True, frozen=True)

    name: str = Field(
        min_length=1,
        max_length=120,
        pattern=r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)+$",
        description="Dotted identifier, e.g. 'news_api.top_headlines'.",
    )
    description: str = ""
    category: NodeCategory = NodeCategory.CUSTOM
    determinism: ActionTier = ActionTier.NON_DETERMINISTIC
    version: str = "1.0.0"
    tags: tuple[str, ...] = ()
    icon: str | None = None
    admin_only: bool = Field(
        default=False,
        description=(
            "When True, the action refuses to execute unless the run's "
            "AppContext.is_admin is True — enforced in "
            "_ActionExecutor.execute, the single convergence point for both "
            "a directly-dispatched registered node and dynamic tool.call. "
            "Mirrors matrx_ai's tool_def.admin_only gate for the equivalent "
            "capability (e.g. raw cross-user SQL)."
        ),
    )
    input_schema: type[BaseModel]
    output_schema: type[BaseModel]
    node_spec: NodeSpec
    source_module: str | None = None
    source_function: str | None = None
    doors: frozenset[str] = Field(
        default=frozenset({"step"}),
        description=(
            "Where this Action can be run from: step (workflow node), tool (agent "
            "tool), directive (the action class of the Kind Directives grammar), "
            "mcp (the product_action MCP tool). Every door runs ``work`` — the ONE "
            "function — through an adapter generated from this declaration."
        ),
    )
    work: Callable[..., Awaitable[BaseModel]] | None = Field(
        default=None,
        description=(
            "The plain work function ``async (app: AppContext, input) -> output`` "
            "(``declare_action``). None for a step-only ``register_node`` whose body "
            "takes the node context."
        ),
    )
    takes_idempotency_key: bool = False
    takes_node_context: bool = False
    owns_idempotency: bool = Field(
        default=False,
        description=(
            "The work runs its OWN idempotency ledger on the door's key (it takes "
            "``idempotency_key`` and claims it itself, e.g. the table API's body-checked "
            "claim): the router hands the key through and does not claim it a second time."
        ),
    )
    requires_action_claim: bool = False
    output_exclude_none: bool = Field(
        default=False,
        description="Drop None fields when a door hands the output on as JSON (tool, mcp).",
    )
    former_step_names: tuple[str, ...] = Field(
        default=(),
        description="Step types this Action was stored under before; they resolve to it.",
    )
    former_names: tuple[str, ...] = Field(
        default=(),
        description=(
            "Action names this Action was registered under before (two Actions collapsed into "
            "one); every door resolving a former name runs this Action."
        ),
    )
    engine: str = Field(
        default="code",
        description=(
            "HOW the Action runs (matrx_graph.actions.engines.ENGINES): code, record_write, "
            "record_tree, workflow, client, outside. Every door calls run_action, which "
            "sends the call to this engine."
        ),
    )
    writes_or_spends: bool = Field(
        default=False,
        description=(
            "The Action changes stored records or spends money. With a record_write / "
            "record_tree engine this is always true; every door then asks the host's "
            "apply policy (auto / ask / off) before it runs."
        ),
    )
    generated: bool = Field(
        default=False,
        description=(
            "Resolved from a host's lazy source (a workflow, an agent row) rather than declared "
            "in code; it is never registered at boot, so it has no automatic directive."
        ),
    )
    apply_rule: str | None = Field(
        default=None,
        pattern=r"^(auto|ask|off)$",
        description=(
            "The Action's REGISTERED apply rule (Arman, 2026-10-29: permissions are registered "
            "with the Action): what happens when a caller that carries no authority of its own "
            "runs it. None = the default: ``ask`` when it writes or spends, else ``auto``. A "
            "caller that carries authority (a workflow step, a person, an agent's own config) "
            "decides for itself; a person's or organization's explicit ``off`` still wins."
        ),
    )
    apply_rule_resolver: str | None = Field(
        default=None,
        pattern=r"^[a-z][a-z0-9_]*(\.[a-z0-9_]+)*$",
        description=(
            "The name of a host-registered rule resolver that decides THIS call's apply rule "
            "(auto / ask / off) from the organization's own settings — the registered rule "
            "computed per call instead of one fixed word. The host's apply gate runs it for "
            "every authority (an organization's setting is not the caller's to waive); only a "
            "recorded approval of the exact call (authority ``approved``) skips it."
        ),
    )
    consent_step: bool = Field(
        default=False,
        description=(
            "The Action's own step IS the person's confirmation: it puts something in front of "
            "the person (a private form they fill in and submit, a proposal they confirm on their "
            "own screen) and nothing is written until they do. The host's apply gate then lets an "
            "``ask`` go straight to that step instead of asking a second time; an explicit "
            "``off`` (the person's, the agent author's, the surface's) still refuses."
        ),
    )
    person_facing: bool | None = Field(
        default=None,
        description=(
            "Whether a person picks this Action in a product picker (a trigger's target, a "
            "binding). None = the default: hidden when admin-only, schedule-only, or in an "
            "internal namespace (INTERNAL_ACTION_NAMESPACES — admin, dev, sql, builder, build, "
            "test), else shown. Declare True/False only to overrule the default."
        ),
    )
    bring_in: bool = Field(
        default=False,
        description=(
            "A person may bring this Action's answer into a table: it READS (never writes or spends) and its "
            "answer is a list of rows (contacts, templates, places, search results). Declared, never guessed "
            "from the output schema; ``GET /actions?bring_in=true`` lists exactly these."
        ),
    )
    beside_kind: tuple[str, ...] = Field(
        default=(),
        description=(
            "Top-level output keys that ride BESIDE ``node_spec.output_kind`` (run facts a later step "
            "reads). The step door declares them (``ctx.declare_beside_kind``); every check of the "
            "output against its kind leaves them out."
        ),
    )
    directive_slug: str | None = Field(
        default=None,
        description=(
            "The directive slug this Action is reached by when it is not the generated "
            "``directive_v1_action_<noun>`` (a record write keeps its create/update/delete slug)."
        ),
    )

    @model_validator(mode="after")
    def _validate_claim_requirement(self) -> ActionSpec:
        if self.requires_action_claim and (
            self.doors != frozenset({"step"}) or self.engine != "code"
            or self.work is None or not self.writes_or_spends or self.owns_idempotency
            or self.apply_rule_resolver is not None
        ):
            raise ValueError("A durable Action claim requires a gated code step using the host ledger without an approval resolver.")
        return self

    @property
    def gated(self) -> bool:
        """Every door asks the apply policy before running this Action."""
        from matrx_graph.actions.engines import WRITING_ENGINES

        return self.writes_or_spends or self.engine in WRITING_ENGINES

    @property
    def declared_apply_rule(self) -> str:
        """The registered apply rule, with its default filled in (see ``apply_rule``)."""
        return self.apply_rule or ("ask" if self.gated else "auto")

    @property
    def is_person_facing(self) -> bool:
        """Shown in a person's Action picker (see ``person_facing``). Never an Action with nothing to run (a
        trigger would refuse it at save: "runs only as a workflow step"), even when declared person-facing."""
        if not self.runnable:
            return False
        if self.person_facing is not None:
            return self.person_facing
        return not (self.admin_only or self.schedule_only or is_internal_action_name(self.name))

    @property
    def runnable(self) -> bool:
        """It has something to run: a work function, or a host engine."""
        return self.engine != "code" or self.work is not None

    @property
    def schedule_only(self) -> bool:
        """It declared only the ``schedule`` door: no door opens for it by construction and
        ``run_action`` refuses every other door (``matrx_graph.actions.doors``)."""
        from matrx_graph.actions.doors import SCHEDULE_ONLY_DOORS

        return frozenset(self.doors) == SCHEDULE_ONLY_DOORS

    def dump_output(self, out: BaseModel) -> dict[str, Any]:
        """The output as a door hands it on as JSON — one dump for every door."""
        return out.model_dump(mode="json", by_alias=True, exclude_none=self.output_exclude_none)

    def to_descriptor(self) -> dict[str, Any]:
        """JSON descriptor shape consumed by the Studio action palette."""
        return {
            "name": self.name,
            "description": self.description,
            "category": self.category.value,
            "determinism": self.determinism.value,
            "version": self.version,
            "tags": list(self.tags),
            "icon": self.icon,
            "admin_only": self.admin_only,
            # Built once per class (node_spec.model_json_schema_once): every generated Action shares the same
            # two classes, and /actions rebuilt them per mandate on the loop (event_loop_stall, 2026-11-13).
            "input_schema": model_json_schema_once(self.input_schema),
            "output_schema": model_json_schema_once(self.output_schema),
            "spec_type": self.node_spec.node_type,
            "source_module": self.source_module,
            "source_function": self.source_function,
            "doors": sorted(self.doors),
            "door_names": self.door_names(),
            "engine": self.engine,
            "writes_or_spends": self.gated,
            "apply_rule": self.declared_apply_rule,
            "apply_rule_resolver": self.apply_rule_resolver,
            "consent_step": self.consent_step,
            "input_kind": self.node_spec.input_kind,
            "output_kind": self.node_spec.output_kind,
            "person_facing": self.is_person_facing,
            "bring_in": self.bring_in,
        }

    def door_names(self) -> dict[str, str]:
        """The name each open door is reached by — derived, never typed. The directive
        door is open on every runnable Action (``directive_noun_of``); it is named by its
        full slug."""
        from matrx_graph.actions.doors import api_path_for, directive_noun_of, tool_name_for

        names = {
            "step": self.node_spec.node_type,
            "mcp": self.name,
            "api": api_path_for(self.name),
            "binding": self.name,
            "schedule": self.name,
            "service": f"/actions/service/{self.name}/run",
            "trigger": self.name,
            "visitor": f"/actions/visitor/{self.name}/run",
        }
        names["tool"] = tool_name_for(self.name)
        out = {door: names[door] for door in sorted(self.doors) if door != "directive"}
        if self.runnable and not self.schedule_only:
            # Every runnable Action is wrapped in the API, by construction (Arman, 2026-10-29).
            out["api"] = names["api"]
            # ...and can fill an agent variable or context item (the binding door, 2026-10-30).
            out["binding"] = names["binding"]
            # ...and can be fired by a workflow.trigger row (the trigger door, Triggers Phase 2).
            out["trigger"] = names["trigger"]
        noun = directive_noun_of(self)
        if self.directive_slug:
            out["directive"] = self.directive_slug
        elif noun is not None:
            out["directive"] = f"directive_v1_action_{noun}"
        return dict(sorted(out.items()))


class ActionFailed(Exception):  # noqa: N818 — the name says what the caller reads
    """A work function's honest refusal, shaped once for every door.

    The step door turns it into ``failure(code, message)``; the tool and mcp doors into
    an error the agent reads, with ``suggested_action`` (the next call to make, or what
    to tell the person). ``error_type`` is ``validation`` when the caller can fix it.

    A code that NAMES a refusal is one: left unset, ``error_type`` follows the code —
    ``refused`` stays ``refused`` and ``not_found`` / ``*_not_found`` become ``not_found`` —
    and everything else is ``execution``. Before 2026-11-05 every unset refusal read
    ``execution``, so the tool executor filed each "That placement was not found" /
    "There is no job called …" an agent had already read and corrected as a
    ``tool_execution_failed`` platform error (31 ``code="refused"`` call sites).
    An explicit ``error_type`` always wins.
    """

    def __init__(
        self,
        code: str,
        message: str,
        *,
        suggested_action: str = "",
        error_type: str | None = None,
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.suggested_action = suggested_action
        self.error_type = error_type if error_type is not None else _error_type_of_code(code)
        self.details = details or {}


def _error_type_of_code(code: str) -> str:
    """The error type a code with no explicit one carries (``ActionFailed``)."""
    c = (code or "").strip().lower()
    if c == "refused":
        return "refused"
    if c == "not_found" or c.endswith("_not_found"):
        return "not_found"
    if _NAMES_BAD_INPUT.search(c):
        return "validation"
    return "execution"


#: A code that names the CALLER's input as the problem (``invalid_input``, ``place_needed``,
#: ``organization_required``, ``bad_room``, ``cerbo_request_invalid``) is ``validation``: the
#: caller fixes it. Before 2026-11-14 these read ``execution``, so a connected-app preview that
#: left out a place id answered 502 and was filed as a server crash.
_NAMES_BAD_INPUT = re.compile(r"^(invalid|bad)_|_(invalid|needed|required)$")


ActionCallable = Callable[[NodeExecutionContext, BaseModel], Awaitable[BaseModel]]


class ActionNameError(ValueError):
    """Raised when a @register_node name carries the eradicated ``action.`` prefix."""


def _validate_action_name(name: str) -> None:
    if name.startswith("action."):
        raise ActionNameError(
            f"@register_node name {name!r} must not include an 'action.' prefix — "
            "the namespace was eradicated (docs/workflow/NOMENCLATURE.md); the "
            f"canonical spec_type IS the bare name ({name.removeprefix('action.')!r}). "
            "Stored definitions with the old spelling resolve through the "
            "registry's legacy alias."
        )


def build_action_node_spec(
    *,
    name: str,
    description: str,
    category: NodeCategory,
    determinism: ActionTier,
    input_schema: type[BaseModel],
    output_schema: type[BaseModel],
    config_schema: type[BaseModel] | None = None,
    icon: str | None,
    tags: tuple[str, ...],
    version: str,
    display_name: str | None = None,
    input_kind: str | None = None,
    output_kind: str | None = None,
    dynamic_output: bool = False,
    launches_nodes: bool = False,
    extra_output_handles: tuple[str, ...] = (),
    values_are: str = "ai",
    output_in_run_row: bool = True,
    spends: bool | None = None,
) -> NodeSpec:
    """Build the NodeSpec that represents this action in the graph engine.

    Every action is invocable as a node directly — authors drag it onto the
    canvas and the scheduler treats it like any other node. The `tool.call`
    generic dispatcher exists for the dynamic case where the action name
    isn't known at design time.
    """
    _validate_action_name(name)
    return NodeSpec(
        type=name,
        category=category,
        # A friendly label the palette shows. Falls back to prettifying the
        # LAST dotted segment ("ai.agent.start" → "Start"), which is often a
        # poor label — pass display_name explicitly for anything user-facing.
        display_name=display_name or _prettify(name),
        description=description,
        icon=icon,
        input_schema=input_schema,
        output_schema=output_schema,
        config_schema=config_schema or EmptyConfig,
        handles=(
            HandleSpec(
                id="in",
                direction=HandleDirection.INPUT,
                accepted_kinds=(EdgeKind.DATA,),
                required=False,
            ),
            HandleSpec(
                id="out",
                direction=HandleDirection.OUTPUT,
                accepted_kinds=(EdgeKind.DATA,),
                required=False,
            ),
            # Named emission handles (ctx.emit targets) a branching action
            # declares so edges may reference them as sourceHandle — the
            # action twin of control.branch's 'true'/'false'.
            *(
                HandleSpec(
                    id=handle_id,
                    direction=HandleDirection.OUTPUT,
                    accepted_kinds=(EdgeKind.DATA,),
                    required=False,
                )
                for handle_id in extra_output_handles
            ),
        ),
        determinism=determinism,
        tags=tags,
        version=version,
        input_kind=input_kind,
        output_kind=output_kind,
        dynamic_output=dynamic_output,
        launches_nodes=launches_nodes,
        values_are=values_are,
        output_in_run_row=output_in_run_row,
        spends=spends,
    )


def _prettify(name: str) -> str:
    return humanize_identifier(name.split(".")[-1])
