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

from collections.abc import Awaitable, Callable
from typing import Any, Generic, TypeVar

from matrx_utils.text_case import humanize_identifier
from pydantic import BaseModel, ConfigDict, Field

from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.handle import HandleDirection, HandleSpec
from matrx_graph.types.node_spec import EmptyConfig, NodeSpec
from matrx_graph.types.primitives import ActionTier, EdgeKind, NodeCategory

InputT = TypeVar("InputT", bound=BaseModel)
OutputT = TypeVar("OutputT", bound=BaseModel)


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
    output_exclude_none: bool = Field(
        default=False,
        description="Drop None fields when a door hands the output on as JSON (tool, mcp).",
    )
    former_step_names: tuple[str, ...] = Field(
        default=(),
        description="Step types this Action was stored under before; they resolve to it.",
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
    directive_slug: str | None = Field(
        default=None,
        description=(
            "The directive slug this Action is reached by when it is not the generated "
            "``directive_v1_action_<noun>`` (a record write keeps its create/update/delete slug)."
        ),
    )

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
    def runnable(self) -> bool:
        """It has something to run: a work function, or a host engine."""
        return self.engine != "code" or self.work is not None

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
            "input_schema": self.input_schema.model_json_schema(),
            "output_schema": self.output_schema.model_json_schema(),
            "spec_type": self.node_spec.node_type,
            "source_module": self.source_module,
            "source_function": self.source_function,
            "doors": sorted(self.doors),
            "door_names": self.door_names(),
            "engine": self.engine,
            "writes_or_spends": self.gated,
            "apply_rule": self.declared_apply_rule,
            "input_kind": self.node_spec.input_kind,
            "output_kind": self.node_spec.output_kind,
        }

    def door_names(self) -> dict[str, str]:
        """The name each open door is reached by — derived, never typed. The directive
        door is open on every runnable Action (``directive_noun_of``); it is named by its
        full slug."""
        from matrx_graph.actions.doors import api_path_for, directive_noun_of, tool_name_for

        names = {"step": self.node_spec.node_type, "mcp": self.name, "api": api_path_for(self.name)}
        names["tool"] = tool_name_for(self.name)
        out = {door: names[door] for door in sorted(self.doors) if door != "directive"}
        if self.runnable:
            # Every runnable Action is wrapped in the API, by construction (Arman, 2026-10-29).
            out["api"] = names["api"]
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
    """

    def __init__(
        self,
        code: str,
        message: str,
        *,
        suggested_action: str = "",
        error_type: str = "execution",
        details: dict[str, Any] | None = None,
    ) -> None:
        super().__init__(message)
        self.code = code
        self.message = message
        self.suggested_action = suggested_action
        self.error_type = error_type
        self.details = details or {}


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
    )


def _prettify(name: str) -> str:
    return humanize_identifier(name.split(".")[-1])
