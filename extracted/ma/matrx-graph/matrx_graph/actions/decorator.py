"""``@register_node`` decorator — the primary Python authoring surface.

Wrap an async function with explicit Pydantic input/output models to get:

- Typed validation of both sides of the boundary
- Automatic registration as a graph node under the bare dotted name
  (``news_api.top_headlines`` — the name IS the spec_type)
- Automatic registration in the action registry
- A hook for ``tool.call`` to look it up by name

(``@action`` is the deprecated legacy name — the ``action.*`` identifier
namespace was eradicated 2026-08-08, see docs/workflow/NOMENCLATURE.md.
Stored definitions with ``action.<name>`` spec_types resolve through the
node registry's legacy alias; nothing is rewritten.)

Example::

    from pydantic import BaseModel, Field
    from matrx_graph.actions import register_node
    from matrx_graph.types.primitives import ActionTier, NodeCategory

    class Inputs(BaseModel):
        country: str = Field(default="us", description="ISO country code")
        limit: int = Field(default=5, ge=1, le=50)

    class Outputs(BaseModel):
        headlines: list[str]

    @register_node(
        name="news_api.top_headlines",
        description="Fetch today's top N headlines from the News API.",
        category=NodeCategory.IO,
        determinism=ActionTier.NON_DETERMINISTIC,
        input_schema=Inputs,
        output_schema=Outputs,
        icon="newspaper",
    )
    async def top_headlines(ctx, inputs: Inputs) -> NodeResult[Outputs]:
        return success(Outputs(headlines=[...]))

The decorated function signature is
``(ctx: NodeExecutionContext, inputs: T) -> Awaitable[NodeResult[U]]`` —
every action returns the NodeResult envelope (``success(...)`` /
``failure(...)``; bare payload returns are a hard error since ratchet zero).
The adapter class registers itself in the node registry so the scheduler can
dispatch it by ``news_api.top_headlines`` without any further wiring.
"""

from __future__ import annotations

import inspect
import warnings
from collections.abc import Awaitable, Callable
from typing import TYPE_CHECKING, Any, Literal

from pydantic import BaseModel

from matrx_graph.actions.registry import (
    ActionRegistry,
    default_action_registry,
)
from matrx_graph.actions.doors import validate_doors
from matrx_graph.actions.engines import ActionStarted, run_action, validate_engine
from matrx_graph.actions.spec import ActionFailed, ActionSpec, build_action_node_spec
from matrx_graph.errors import ActionAuthorizationError
from matrx_graph.executor.registry import (
    alias_spec_type,
    NodeRegistry,
    default_registry,
)
from matrx_graph.types.context import NodeExecutionContext
from matrx_graph.types.events import (
    AGENT_STEP_PHASE_COMPLETE,
    AGENT_STEP_PHASE_PREPARING,
)
from matrx_graph.types.node_spec import NodeSpec
from matrx_graph.types.primitives import ActionTier, NodeCategory, RetryPolicy
from matrx_graph.types.result import NodeResult, failure, success

if TYPE_CHECKING:
    pass

#: The AGENT FAMILY (SPEC §5.1) — the step categories whose invocations get the
#: automatic phase bookends. An LLM or AGENT step is the one that can sit
#: silent for minutes behind a provider call; a DATA or CONTROL step settles in
#: milliseconds and would only add noise. Widening this set is a deliberate
#: decision, not a side effect of registering a node.
AGENT_STEP_CATEGORIES: frozenset[NodeCategory] = frozenset({NodeCategory.LLM, NodeCategory.AGENT})

# NOTE: the return alias is a string — NodeResult is a parametrized-pydantic
# union (Success[T] | Failure), which is not runtime-subscriptable.
ActionFn = Callable[[NodeExecutionContext, BaseModel], Awaitable["NodeResult[BaseModel]"]]


class ActionSignatureError(TypeError):
    """Raised at decoration (import) time when an @action wraps a function
    that is not a valid ``async def (ctx, inputs)`` executor.

    This is a fail-LOUD-AT-BOOT gate, not a runtime bug: it exists because a
    misregistered action (e.g. a synchronous helper accidentally placed under
    the decorator) otherwise registers cleanly and only explodes at RUNTIME,
    deep inside a paid workflow, with a cryptic ``AttributeError`` after every
    expensive upstream node already ran. (2026-06: a ``_resolve_topic(inputs,
    ctx)`` helper got decorated as ``study_pack.assemble``; the scheduler
    called it as ``(ctx, inputs)`` → ``'NodeExecutionContext' has no attribute
    'topic'`` at the final node.) Catching it here makes that entire class
    impossible to ship.
    """


def _positional_params(fn: ActionFn) -> list[inspect.Parameter]:
    try:
        sig = inspect.signature(fn)
    except (TypeError, ValueError):  # builtins / C-callables
        return []
    return [
        p for p in sig.parameters.values() if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)
    ]


def _accepts_config(fn: ActionFn) -> bool:
    """True when the action opts into the node's validated config model.

    Opting in is purely positional: ``async def fn(ctx, inputs, config)``.
    Two parameters — the overwhelming default — keep the historical
    behavior of never seeing the config.
    """
    return len(_positional_params(fn)) >= 3


def _validate_action_signature(fn: ActionFn, *, name: str, input_schema: type[BaseModel]) -> None:
    """Reject anything that isn't a proper async ``(ctx, inputs)`` executor.

    Best-effort but high-signal: the async + arity checks alone make the
    accidental-helper class impossible, and the annotation swap-detector
    catches the specific ``(inputs, ctx)`` ordering mistake even when both
    params are annotated as forward-ref strings (``from __future__`` imports).
    """
    if not inspect.iscoroutinefunction(fn):
        raise ActionSignatureError(
            f"@register_node(name={name!r}) must decorate an `async def` — got "
            f"{getattr(fn, '__qualname__', fn)!r}, which is not a coroutine "
            "function. An action executor is `async def fn(ctx, inputs) -> Output`. "
            "If this is a helper, move it OUT from under the @register_node decorator."
        )

    positional = _positional_params(fn)
    if not positional:
        return  # builtins / C-callables — nothing more we can verify
    if len(positional) < 2:
        raise ActionSignatureError(
            f"@register_node(name={name!r}) executor {getattr(fn, '__qualname__', fn)!r} "
            f"must accept (ctx, inputs); found {len(positional)} positional "
            "parameter(s)."
        )

    # Swap-detector: the SECOND param carries the input model. If the FIRST
    # param is annotated as the input schema (and the second is not), the
    # author almost certainly wrote (inputs, ctx) instead of (ctx, inputs).
    schema_name = input_schema.__name__

    def _ann_name(annotation: Any) -> str | None:
        if annotation is inspect.Parameter.empty:
            return None
        if isinstance(annotation, str):
            return annotation.rsplit(".", 1)[-1]
        return getattr(annotation, "__name__", None)

    first_ann = _ann_name(positional[0].annotation)
    second_ann = _ann_name(positional[1].annotation)
    if first_ann == schema_name and second_ann != schema_name:
        raise ActionSignatureError(
            f"@register_node(name={name!r}) executor {getattr(fn, '__qualname__', fn)!r} "
            f"appears to declare parameters as (inputs: {schema_name}, ctx) — the "
            "input model must be the SECOND parameter: `async def fn(ctx, "
            f"inputs: {schema_name})`. The scheduler always calls executors as "
            "(ctx, inputs); a reversed signature crashes at runtime on the first "
            "attribute access against the context object."
        )


class _ActionExecutor:
    """Adapter that presents an @action function as a NodeExecutor.

    The scheduler only knows about NodeExecutor protocol objects (spec +
    `async execute(ctx, inputs, config)`). An action's author-time
    configuration is normally its inputs, so the two-parameter form
    `(ctx, inputs)` is the default and the config arg is dropped. An action
    that declares a THIRD positional parameter opts in and receives the
    validated `config_schema` model, exactly like a class executor. That is
    the only way to author a value on a node whose merged inputs are gated by
    a CLOSED `input_kind` — a static input would be an undeclared key and
    park the run (`rag.embed`'s embedding model, 2026-08-23).

    This is the SINGLE convergence point for every way an action can run:
    a direct registered node dispatched by the Scheduler (inline,
    queued-worker, or resumed-from-checkpoint — all funnel through
    `Scheduler._execute_invocation_body` → `executor.execute(...)`), and the
    dynamic `tool.call` node (`ToolCallExecutor.execute` resolves this same
    adapter via `resolve_action_executor` and calls `target.execute(...)`
    directly). Gating `admin_only` here — rather than duplicating a check in
    both the scheduler and `tool.call` — makes it structurally impossible for
    a new dispatch path to bypass the gate.
    """

    # Contract-slug family for auto-derived I/O kinds. The `action_io` FAMILY
    # name is bookkeeping vocabulary owned by contract_kinds.py (a separate
    # workstream) — it is NOT part of the eradicated spec_type namespace.
    # Kept as the plain enum VALUE (ContractFamily.ACTION_IO) to avoid a
    # circular import (contract_kinds → executor → registry → contract_kinds);
    # NodeRegistry._contract_family coerces it.
    contract_family = "action_io"

    def __init__(
        self,
        spec: NodeSpec,
        fn: ActionFn,
        *,
        admin_only: bool = False,
        result_version: Callable[..., Awaitable[str | None]] | None = None,
        sample_preflight: Callable[..., Awaitable[Any]] | None = None,
    ) -> None:
        self.spec = spec
        self._fn = fn
        self.admin_only = admin_only
        self._wants_config = _accepts_config(fn)
        # Run once per key (matrx_graph/once.py): what decides this step's answer BESIDES its
        # inputs — an AI step names the agent/mandate Holder and its version, so a prompt or
        # model change is never answered from a saved result. ``None`` = nothing does.
        if result_version is not None:
            self.result_version = result_version
        # A TEST run's sampled step (``Scheduler(sampled_outputs=...)``) still runs this check on
        # its resolved inputs and config — sends nothing; raises exactly as the live call would.
        if sample_preflight is not None:
            self.sample_preflight = sample_preflight

    async def execute(
        self,
        ctx: NodeExecutionContext,
        inputs: BaseModel,
        config: BaseModel,
    ) -> NodeResult[BaseModel]:
        if self.admin_only and not bool(getattr(ctx.app, "is_admin", False)):
            raise ActionAuthorizationError(self.spec.node_type, user_id=ctx.app.user_id)
        # -- AUTOMATIC LIVENESS (SPEC-workflow-ui-contract §5.1) -------------
        # This adapter is the single convergence point for every way an action
        # runs (see the class docstring), and by the time we are here the
        # scheduler has RESOLVED AND VALIDATED this invocation's inputs — which
        # is precisely the moment the contract names for ``preparing``. So an
        # agent-family step's phase bookends are emitted HERE, by the runner,
        # for every such node that exists or will ever exist. No workflow
        # author writes a line, and no node class can forget.
        #
        # ``streaming`` (first token), ``tool`` (each call) and ``retrying``
        # come from the provider/tool/retry funnels further in; ``finalizing``
        # from the structured-output funnel. Together they are the moments
        # table, and none of them is per-node code.
        live = self.spec.category in AGENT_STEP_CATEGORIES
        if live:
            await ctx.phase(AGENT_STEP_PHASE_PREPARING)
        if self._wants_config:
            result = await self._fn(ctx, inputs, config)  # type: ignore[call-arg]
        else:
            result = await self._fn(ctx, inputs)
        # Only a RETURN is ``complete``. A raise belongs to the scheduler's
        # node_failed / node_retry_scheduled path — announcing "complete" on
        # the way out of a failure is the exact lie liveness exists to kill.
        if live:
            await ctx.phase(AGENT_STEP_PHASE_COMPLETE)
        return result


def register_node(
    *,
    name: str,
    description: str = "",
    category: NodeCategory = NodeCategory.CUSTOM,
    determinism: ActionTier = ActionTier.NON_DETERMINISTIC,
    input_schema: type[BaseModel],
    output_schema: type[BaseModel],
    config_schema: type[BaseModel] | None = None,
    icon: str | None = None,
    tags: tuple[str, ...] = (),
    version: str = "1.0.0",
    admin_only: bool = False,
    display_name: str | None = None,
    input_kind: str | None = None,
    output_kind: str | None = None,
    dynamic_output: bool = False,
    launches_nodes: bool = False,
    values_are: Literal["deterministic", "outside", "ai"] = "ai",
    extra_output_handles: tuple[str, ...] = (),
    output_in_run_row: bool = True,
    node_registry: NodeRegistry | None = None,
    action_registry: ActionRegistry | None = None,
    overwrite: bool = False,
    timeout_ms: int | None = None,
    retry: RetryPolicy | None = None,
    result_version: Callable[..., Awaitable[str | None]] | None = None,
    sample_preflight: Callable[..., Awaitable[Any]] | None = None,
) -> Callable[[ActionFn], ActionFn]:
    """Register a callable as an action + a graph node in one step.

    The decorated function is returned unchanged, so it can still be called
    directly in tests. Registration happens at decoration time.

    ``config_schema`` — the node's author-time config model. An action body
    receives it only when it declares a third positional parameter
    (``async def fn(ctx, inputs, config)``); the two-parameter form never
    sees it. Prefer inputs; reach for config when a value must be authored on
    a node whose merged inputs are gated by a closed ``input_kind``, where a
    static input would be an undeclared key and park the run.

    ``retry`` — the node's default ``RetryPolicy`` (``NodeSpec.retry``; default: one attempt). A
    returned failure is retried when its ``code`` is in ``retry_on``; a ``retry_policy`` set on the
    node in a workflow replaces it.

    ``admin_only`` — when True, execution refuses to run unless the
    invoking run's ``AppContext.is_admin`` is True (checked in
    ``_ActionExecutor.execute``, see its docstring for why that's the right
    place). Use for any action with no built-in ownership/RLS scoping —
    raw-pool DB access, cross-user reads, anything a `sql`-tool-equivalent
    `admin_only` tool_def gate would cover.

    ``input_kind`` / ``output_kind`` — canonical platform-kind declaration
    (``content_ir.kind_definition`` slugs), same semantics as on any
    ``NodeSpec``: a declared ``input_kind`` gates merged inputs fatally
    pre-execute; ``output_kind`` is drift-checked loudly and stamped on every
    NodeOutcome. Left unset, the registry auto-derives exact ``action_io_*``
    contract kinds from the pydantic schemas — declare a curated kind here
    only when a registered platform Shape (e.g. ``office_document``) IS the
    node's I/O contract.

    ``dynamic_output`` — the node's real output shape is not the pydantic
    ``output_schema`` (which is a permissive transport) but something resolved
    per node INSTANCE: the author's ``data.output_kind``, or a schema the
    config computes. Setting it stops the registry from minting a fingerprint
    ``action_io_*`` contract kind for the node, which would otherwise read as
    "this node declares a kind" while describing nothing a renderer can attach
    to. ``ai.agent.produce`` is the reference case.

    ``extra_output_handles`` — named emission handles this action targets via
    ``ctx.emit(handle_id, ...)``, declared so authored edges may reference
    them as ``sourceHandle`` (validate_definition rejects a sourceHandle the
    NodeSpec does not declare). The action twin of ``control.branch``'s
    'true'/'false'. The default 'in'/'out' pair is always present.

    ``sample_preflight`` — ``async (ctx, inputs, config) -> record | None``: what a TEST run's
    sampled step (answered from its declared sample) still checks, on its resolved inputs, before
    the sample is used. It must send nothing and raise exactly as the live call would refuse; its
    return lands on the sampled outcome as ``metadata.preflight``. ``ai.mandate.start`` uses it
    to run the request firewall without a provider call.
    """

    def decorator(fn: ActionFn) -> ActionFn:
        _validate_action_signature(fn, name=name, input_schema=input_schema)
        _install(
            fn,
            name=name,
            description=description,
            category=category,
            determinism=determinism,
            input_schema=input_schema,
            output_schema=output_schema,
            config_schema=config_schema,
            icon=icon,
            tags=tags,
            version=version,
            admin_only=admin_only,
            display_name=display_name,
            input_kind=input_kind,
            output_kind=output_kind,
            dynamic_output=dynamic_output,
            launches_nodes=launches_nodes,
            values_are=values_are,
            extra_output_handles=extra_output_handles,
            output_in_run_row=output_in_run_row,
            node_registry=node_registry,
            action_registry=action_registry,
            overwrite=overwrite,
            timeout_ms=timeout_ms,
            retry=retry,
            result_version=result_version,
            sample_preflight=sample_preflight,
            doors=frozenset({"step"}),
            work=None,
            source_fn=fn,
        )
        return fn

    return decorator


def _install(
    step_fn: ActionFn,
    *,
    name: str,
    description: str,
    category: NodeCategory,
    determinism: ActionTier,
    input_schema: type[BaseModel],
    output_schema: type[BaseModel],
    config_schema: type[BaseModel] | None,
    icon: str | None,
    tags: tuple[str, ...],
    version: str,
    admin_only: bool,
    display_name: str | None,
    input_kind: str | None,
    output_kind: str | None,
    dynamic_output: bool,
    launches_nodes: bool,
    values_are: str,
    extra_output_handles: tuple[str, ...],
    output_in_run_row: bool,
    node_registry: NodeRegistry | None,
    action_registry: ActionRegistry | None,
    overwrite: bool,
    timeout_ms: int | None,
    retry: RetryPolicy | None,
    result_version: Callable[..., Awaitable[str | None]] | None,
    sample_preflight: Callable[..., Awaitable[Any]] | None,
    doors: frozenset[str],
    work: Callable[..., Awaitable[BaseModel]] | None,
    source_fn: Callable[..., Any],
    takes_idempotency_key: bool = False,
    output_exclude_none: bool = False,
    former_step_names: tuple[str, ...] = (),
    engine: str = "code",
    writes_or_spends: bool = False,
    directive_slug: str | None = None,
    apply_rule: str | None = None,
) -> ActionSpec:
    """The ONE registration: the ActionSpec always, the step adapter when ``step`` is a door."""
    spec = build_action_node_spec(
        name=name,
        description=description,
        category=category,
        determinism=determinism,
        input_schema=input_schema,
        output_schema=output_schema,
        config_schema=config_schema,
        icon=icon,
        tags=tags,
        version=version,
        display_name=display_name,
        input_kind=input_kind,
        output_kind=output_kind,
        dynamic_output=dynamic_output,
        launches_nodes=launches_nodes,
        values_are=values_are,
        extra_output_handles=extra_output_handles,
        output_in_run_row=output_in_run_row,
    )
    if timeout_ms is not None:
        # the step's own wall clock (NodeSpec.timeout_ms wins over workflow.step_clock): for a step built to run
        # long that bounds every call it makes itself — an import, a copy in slices — never a stalled model call
        spec = spec.model_copy(update={"timeout_ms": int(timeout_ms)})
    if retry is not None:
        # the node's default retry policy (NodeSpec.retry); a retry_policy set on the node still wins
        spec = spec.model_copy(update={"retry": retry})
    if "step" in doors:
        adapter = _ActionExecutor(
            spec=spec,
            fn=step_fn,
            admin_only=admin_only,
            result_version=result_version,
            sample_preflight=sample_preflight,
        )
        (node_registry or default_registry()).register(adapter, overwrite=overwrite)
        for former in former_step_names:
            alias_spec_type(former, name)

    action_spec = ActionSpec(
        name=name,
        description=description,
        category=category,
        determinism=determinism,
        version=version,
        tags=tags,
        icon=icon,
        admin_only=admin_only,
        input_schema=input_schema,
        output_schema=output_schema,
        node_spec=spec,
        source_module=getattr(source_fn, "__module__", None),
        source_function=getattr(source_fn, "__qualname__", None),
        doors=doors,
        work=work,
        takes_idempotency_key=takes_idempotency_key,
        output_exclude_none=output_exclude_none,
        former_step_names=former_step_names,
        engine=validate_engine(name, engine),
        writes_or_spends=writes_or_spends,
        directive_slug=directive_slug,
        apply_rule=apply_rule,
    )
    (action_registry or default_action_registry()).register(action_spec, overwrite=overwrite)
    setattr(source_fn, "_matrx_action_spec", action_spec)  # noqa: B010
    return action_spec


def step_idempotency_key(ctx: NodeExecutionContext) -> str:
    """The key a step door hands a work function: stable across retries of the SAME
    invocation (run, node, dispatch, item, firing), distinct for every other one."""
    return f"step:{ctx.run_id}:{ctx.node_id}:{ctx.dispatch_id}:{ctx.item_index}:{ctx.firing}"


def _validate_work_signature(work: Callable[..., Any], *, name: str) -> bool:
    """A work function is ``async def work(app, input[, *, idempotency_key])``.

    Returns whether it takes ``idempotency_key``."""
    if not inspect.iscoroutinefunction(work):
        raise ActionSignatureError(
            f"declare_action(name={name!r}) must decorate an `async def work(app, input)` — "
            f"got {getattr(work, '__qualname__', work)!r}, which is not a coroutine function."
        )
    params = inspect.signature(work).parameters
    positional = [p for p in params.values() if p.kind in (p.POSITIONAL_ONLY, p.POSITIONAL_OR_KEYWORD)]
    if len(positional) != 2:
        raise ActionSignatureError(
            f"declare_action(name={name!r}) work function {getattr(work, '__qualname__', work)!r} "
            f"must take exactly (app, input); found {len(positional)} positional parameter(s)."
        )
    return "idempotency_key" in params


def declare_action(
    *,
    name: str,
    description: str,
    input_schema: type[BaseModel],
    output_schema: type[BaseModel],
    doors: frozenset[str] | set[str] | tuple[str, ...],
    category: NodeCategory = NodeCategory.CUSTOM,
    determinism: ActionTier = ActionTier.NON_DETERMINISTIC,
    icon: str | None = None,
    tags: tuple[str, ...] = (),
    version: str = "1.0.0",
    admin_only: bool = False,
    display_name: str | None = None,
    input_kind: str | None = None,
    output_kind: str | None = None,
    values_are: Literal["deterministic", "outside", "ai"] = "ai",
    node_registry: NodeRegistry | None = None,
    action_registry: ActionRegistry | None = None,
    overwrite: bool = False,
    output_exclude_none: bool = False,
    former_step_names: tuple[str, ...] = (),
    writes_or_spends: bool = False,
    apply_rule: str | None = None,
) -> Callable[[Callable[..., Awaitable[BaseModel]]], Callable[..., Awaitable[BaseModel]]]:
    """Declare ONE Action: a named piece of work with typed input → code → typed output.

    The decorated function is the plain work function
    ``async def work(app: AppContext, input: In[, *, idempotency_key: str | None]) -> Out``
    and is returned unchanged. ``doors`` says where it can be run from (``step``,
    ``tool``, ``directive``, ``mcp`` — see ``matrx_graph.actions.doors``); each door is
    an adapter generated from this declaration that calls ``ActionSpec.run`` — the
    SAME function every time. The step door is generated here; the tool door by
    matrx-ai, the directive and mcp doors by the host. Its engine is ``code``; an Action
    whose work runs elsewhere is declared with :func:`declare_engine_action`.

    ``writes_or_spends``: the work changes stored records or spends money — every door
    then asks the host's apply policy first.

    ``apply_rule`` (auto | ask | off): the REGISTERED rule for a caller that carries no
    authority of its own; omitted = ``ask`` when it writes or spends, else ``auto``.
    """
    door_set = validate_doors(name, doors)

    def decorator(work: Callable[..., Awaitable[BaseModel]]) -> Callable[..., Awaitable[BaseModel]]:
        takes_key = _validate_work_signature(work, name=name)
        holder: dict[str, ActionSpec] = {}
        step = _step_door(holder, label=work.__qualname__, module=work.__module__)
        holder["spec"] = _install(
            step,
            name=name,
            description=description,
            category=category,
            determinism=determinism,
            input_schema=input_schema,
            output_schema=output_schema,
            config_schema=None,
            icon=icon,
            tags=tags,
            version=version,
            admin_only=admin_only,
            display_name=display_name,
            input_kind=input_kind,
            output_kind=output_kind,
            dynamic_output=False,
            launches_nodes=False,
            values_are=values_are,
            extra_output_handles=(),
            output_in_run_row=True,
            node_registry=node_registry,
            action_registry=action_registry,
            overwrite=overwrite,
            timeout_ms=None,
            retry=None,
            result_version=None,
            sample_preflight=None,
            doors=door_set,
            work=work,
            source_fn=work,
            takes_idempotency_key=takes_key,
            output_exclude_none=output_exclude_none,
            former_step_names=tuple(former_step_names),
            writes_or_spends=writes_or_spends,
            apply_rule=apply_rule,
        )
        return work

    return decorator


def _step_door(holder: dict[str, ActionSpec], *, label: str, module: str) -> ActionFn:
    """The generated step door: the node context's app + the inputs → ``run_action``."""

    async def step(ctx: NodeExecutionContext, inputs: BaseModel) -> NodeResult[BaseModel]:
        spec = holder["spec"]
        key = step_idempotency_key(ctx)
        try:
            out = await run_action(spec, inputs, app=ctx.app, idempotency_key=key)
        except ActionFailed as exc:
            return failure(exc.code, exc.message, details=exc.details or None)
        if isinstance(out, ActionStarted):
            # A step waits for its output; an engine that only hands back a handle has
            # not given one. Loud, never a silent empty output.
            return failure(
                "action_started_not_awaited",
                f"{spec.name} started on engine {spec.engine!r} (request {out.request_id}) "
                "and a step cannot wait on it yet.",
                details=out.model_dump(mode="json"),
            )
        return success(out)

    step.__module__ = module
    step.__qualname__ = f"{label}.<step door>"
    return step


def declare_engine_action(
    *,
    name: str,
    description: str,
    input_schema: type[BaseModel],
    output_schema: type[BaseModel],
    engine: str,
    doors: frozenset[str] | set[str] | tuple[str, ...],
    writes_or_spends: bool = False,
    directive_slug: str | None = None,
    apply_rule: str | None = None,
    category: NodeCategory = NodeCategory.CUSTOM,
    determinism: ActionTier = ActionTier.NON_DETERMINISTIC,
    icon: str | None = None,
    tags: tuple[str, ...] = (),
    display_name: str | None = None,
    output_kind: str | None = None,
    values_are: Literal["deterministic", "outside", "ai"] = "deterministic",
    node_registry: NodeRegistry | None = None,
    action_registry: ActionRegistry | None = None,
    overwrite: bool = False,
) -> ActionSpec:
    """Declare an Action whose work runs on a HOST engine (not ``code``).

    Same registry, same doors, same ``run_action`` as :func:`declare_action`; there is
    no work function here — the engine the host registered (``register_engine``) runs it
    from the declaration (its name, input and output). Used for generated Actions
    (record writes, record trees) and, later, workflow / client / outside ones.
    """
    if engine == "code":
        raise ValueError(f"Action {name!r}: a code Action is declared with declare_action.")
    door_set = validate_doors(name, doors)
    holder: dict[str, ActionSpec] = {}
    step = _step_door(holder, label=name, module=__name__)
    holder["spec"] = _install(
        step,
        name=name,
        description=description,
        category=category,
        determinism=determinism,
        input_schema=input_schema,
        output_schema=output_schema,
        config_schema=None,
        icon=icon,
        tags=tags,
        version="1.0.0",
        admin_only=False,
        display_name=display_name,
        input_kind=None,
        output_kind=output_kind,
        dynamic_output=False,
        launches_nodes=False,
        values_are=values_are,
        extra_output_handles=(),
        output_in_run_row=True,
        node_registry=node_registry,
        action_registry=action_registry,
        overwrite=overwrite,
        timeout_ms=None,
        retry=None,
        result_version=None,
        sample_preflight=None,
        doors=door_set,
        work=None,
        source_fn=step,
        engine=engine,
        writes_or_spends=writes_or_spends,
        directive_slug=directive_slug,
        apply_rule=apply_rule,
    )
    return holder["spec"]


def action(**kwargs: Any) -> Callable[[ActionFn], ActionFn]:
    """DEPRECATED alias of :func:`register_node`.

    The ``action.*`` identifier namespace (and with it this decorator name)
    was eradicated 2026-08-08 — docs/workflow/NOMENCLATURE.md. Kept only so
    out-of-repo consumers keep importing while they migrate; every in-repo
    usage is swept and scripts/check_action_namespace.py ratchets new ones
    to zero.
    """
    warnings.warn(
        "@action is deprecated — use @register_node (matrx_graph.actions.register_node). "
        "The action.* spec_type namespace was eradicated; see docs/workflow/NOMENCLATURE.md.",
        DeprecationWarning,
        stacklevel=2,
    )
    return register_node(**kwargs)


def iter_registered_action_specs(
    registry: ActionRegistry | None = None,
) -> list[ActionSpec]:
    return (registry or default_action_registry()).all()


def resolve_action_executor(
    action_name: str,
    *,
    node_registry: NodeRegistry | None = None,
    action_registry: ActionRegistry | None = None,
) -> Any:
    """Return the NodeExecutor registered for the named registered node.

    Raises NodeRegistryError if the name isn't known. Used by the
    ``tool.call`` dispatcher at execution time to look up the target.
    """
    ar = action_registry or default_action_registry()
    spec = ar.get(action_name)
    nr = node_registry or default_registry()
    return nr.get(spec.node_spec.node_type)
