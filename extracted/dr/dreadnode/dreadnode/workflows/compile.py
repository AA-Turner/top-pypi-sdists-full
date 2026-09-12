"""Compile an authored workflow into a topology document.

Runs at **build time, in the SDK** — during ``dn capability push`` — not on the
platform. Capabilities reach the platform as OCI artifacts and the API extracts
metadata from the config blob; it never imports capability Python. The precedent
is ``dreadnode.packaging.oci._resolve_produced_item_types``, which resolves
``produces`` models to JSON Schema at build time for the same reason.

Compiling client-side also puts validation errors where the author's source is,
which is where multi-error output belongs.

**Never executes a step body.** It reads decorators, type annotations,
docstrings, and a narrow AST scan of each body for literal ``ctx.agent("name")``
and ``ctx.result(step)`` references.
"""

import ast
import hashlib
import inspect
import json
import pathlib
import types
import typing as t

from dreadnode_workflow_core.events import (
    ApprovalDecision,
    ApprovalRequest,
    Collect,
    StartEvent,
    StopEvent,
    WorkflowEvent,
)
from dreadnode_workflow_core.topology import (
    TOPOLOGY_SIZE_CAP_BYTES,
    TOPOLOGY_VERSION,
    EventTypeDoc,
    FanOutPoint,
    FieldDoc,
    JoinPoint,
    NodeConfig,
    NodeConsumes,
    NodeEmit,
    NodeKind,
    ParamDoc,
    SourceSpan,
    Topology,
    TopologyEdge,
    TopologyInput,
    TopologyNode,
    WorkflowConfig,
)
from pydantic import BaseModel

from dreadnode.workflows.errors import CompileError, WorkflowCompileError
from dreadnode.workflows.workflow import DEFAULT_MATERIALIZATION_CAP, StepDef, Workflow

__all__ = ["compile_workflow", "extract_agent_refs"]

_BUILTIN_EVENTS: dict[str, type[WorkflowEvent]] = {
    "ApprovalRequest": ApprovalRequest,
    "ApprovalDecision": ApprovalDecision,
}


# ── Signature analysis ───────────────────────────────────────────────────


class _Consumed(t.NamedTuple):
    """What a step's event parameter declares."""

    events: list[type]
    collect: bool
    param_name: str
    annotation_text: str


class _Emitted(t.NamedTuple):
    event: type | None
    name: str
    cardinality: t.Literal["one", "many"]
    arm: int | None
    fork_index: int | None


def _annotation_text(annotation: t.Any) -> str:
    """Render an annotation the way the author spelled it.

    ``str | None`` rather than ``Optional[str]`` — this is display text for the
    node detail panel, so fidelity to the source matters more than canonical form.
    """
    if annotation is inspect.Parameter.empty:
        return ""
    if isinstance(annotation, str):
        return annotation
    if isinstance(annotation, type):
        return annotation.__name__
    origin = t.get_origin(annotation)
    if origin is types.UnionType or origin is t.Union:
        return " | ".join(_annotation_text(a) for a in t.get_args(annotation))
    if origin is not None:
        args = ", ".join(_annotation_text(a) for a in t.get_args(annotation))
        name = getattr(origin, "__name__", str(origin))
        return f"{name}[{args}]" if args else name
    return str(annotation).replace("typing.", "")


def _is_event_class(obj: t.Any) -> bool:
    return isinstance(obj, type) and issubclass(obj, WorkflowEvent)


def _generic_origin(annotation: t.Any) -> t.Any:
    """Origin of a generic, for both ``typing`` aliases and Pydantic generics.

    Pydantic v2 materializes ``StartEvent[AnalysisInput]`` as a real subclass
    rather than a ``typing`` alias, so ``get_origin()`` returns None for it. The
    parameterization is recorded in ``__pydantic_generic_metadata__`` instead.
    """
    origin = t.get_origin(annotation)
    if origin is not None:
        return origin
    metadata = getattr(annotation, "__pydantic_generic_metadata__", None)
    if metadata:
        return metadata.get("origin")
    return None


def _generic_args(annotation: t.Any) -> tuple[t.Any, ...]:
    args = t.get_args(annotation)
    if args:
        return args
    metadata = getattr(annotation, "__pydantic_generic_metadata__", None)
    if metadata:
        return tuple(metadata.get("args") or ())
    return ()


def _is_start_event(annotation: t.Any) -> bool:
    return _generic_origin(annotation) is StartEvent


def _is_stop_event(annotation: t.Any) -> bool:
    return _generic_origin(annotation) is StopEvent


def _unwrap_collect(annotation: t.Any) -> list[type] | None:
    """Return the declared types if the annotation is ``Collect[...]``."""
    if t.get_origin(annotation) is Collect or annotation is Collect:
        return [a for a in t.get_args(annotation) if isinstance(a, type)]
    return None


def _event_name(event: type) -> str:
    """The key an event is referenced by in the topology document."""
    origin = _generic_origin(event)
    if origin in (StartEvent, StopEvent):
        args = _generic_args(event)
        inner = args[0].__name__ if args and isinstance(args[0], type) else "Any"
        return f"{origin.__name__}[{inner}]"
    return getattr(event, "__name__", str(event))


def _analyze_return(annotation: t.Any) -> list[_Emitted]:
    """Derive emitted events from a return annotation.

    Three shapes carry meaning:

    * ``list[E]``  → fan-out, one node per element
    * ``tuple[A, B]`` → fork, each element routed to its own consumer
    * ``A | B``   → branch, exactly one arm taken at runtime
    """
    origin = t.get_origin(annotation)

    if origin is list:
        (inner,) = t.get_args(annotation) or (None,)
        return [_Emitted(inner, _event_name(inner) if inner else "?", "many", None, None)]

    if origin is tuple:
        return [
            _Emitted(arg, _event_name(arg), "one", None, index)
            for index, arg in enumerate(t.get_args(annotation))
        ]

    if origin is types.UnionType or origin is t.Union:
        emitted: list[_Emitted] = []
        for arm, arg in enumerate(t.get_args(annotation)):
            if arg is type(None):
                continue
            inner_origin = t.get_origin(arg)
            if inner_origin is list:
                (inner,) = t.get_args(arg) or (None,)
                emitted.append(
                    _Emitted(inner, _event_name(inner) if inner else "?", "many", arm, None)
                )
            else:
                emitted.append(_Emitted(arg, _event_name(arg), "one", arm, None))
        return emitted

    if annotation is None or annotation is inspect.Signature.empty:
        return []

    return [_Emitted(annotation, _event_name(annotation), "one", None, None)]


# ── AST scan ─────────────────────────────────────────────────────────────


class _FieldSource(t.NamedTuple):
    """Where an event field's values come from, as far as the AST can say.

    Either an inline literal sequence, or the name of a module-level constant
    to resolve against the step function's globals.
    """

    literals: tuple[str, ...] | None
    global_name: str | None


def _field_source(expr: ast.expr) -> _FieldSource | None:
    """A literal string sequence, or a bare name that might resolve to one."""
    if isinstance(expr, ast.Constant) and isinstance(expr.value, str):
        return _FieldSource((expr.value,), None)
    if isinstance(expr, (ast.List, ast.Tuple, ast.Set)):
        values = [
            element.value
            for element in expr.elts
            if isinstance(element, ast.Constant) and isinstance(element.value, str)
        ]
        if len(values) == len(expr.elts) and values:
            return _FieldSource(tuple(values), None)
        return None
    if isinstance(expr, ast.Name):
        return _FieldSource(None, expr.id)
    return None


def resolve_field_source(source: _FieldSource, namespace: dict[str, t.Any]) -> list[str]:
    """Turn a field source into concrete strings, or nothing.

    A global is read, never called: only an already-built sequence of strings
    resolves. Anything computed at import time is still just a value by the time
    compile runs, so this stays a lookup rather than an evaluation.
    """
    if source.literals is not None:
        return list(source.literals)
    if source.global_name is None:
        return []
    value = namespace.get(source.global_name)
    if isinstance(value, str) or not isinstance(value, (list, tuple, set, frozenset)):
        return []
    entries = list(value)
    if not entries or not all(isinstance(entry, str) for entry in entries):
        return []
    return entries


class _RefScanner(ast.NodeVisitor):
    """Collect literal ``ctx.agent("x")`` and ``ctx.result(step)`` references.

    Deliberately narrow: literal string arguments only, resolving nothing else.
    A non-literal agent name sets ``agents_dynamic`` rather than failing — the
    shape stays authored even when the contents are computed.

    Two extra passes exist purely to name a *dynamic* agent step, because
    ``agents_dynamic`` alone renders a five-way specialist fan-out as an
    anonymous box:

    - ``dynamic_agent_fields`` — ``ctx.agent(ev.agent, ...)`` records ``"agent"``,
      naming the event field the agent comes from.
    - ``constructed_fields`` — ``Task(agent=x) for x in ROSTER`` records the
      iterable's name against ``("Task", "agent")``, so the producer's constant
      can be resolved later.

    Neither executes anything: the first is a name off the event parameter, the
    second is a name looked up in the module's globals at compile time.
    """

    def __init__(self, ctx_param: str, event_param: str = "") -> None:
        self.ctx_param = ctx_param
        self.event_param = event_param
        self.agents: list[str] = []
        self.agents_dynamic = False
        self.results: list[str] = []
        self.dynamic_agent_fields: list[str] = []
        self.constructed_fields: dict[tuple[str, str], _FieldSource] = {}
        self._comprehension_sources: dict[str, _FieldSource] = {}

    def visit_Call(self, node: ast.Call) -> None:
        func = node.func
        if isinstance(func, ast.Attribute) and isinstance(func.value, ast.Name):
            if func.value.id == self.ctx_param:
                if func.attr == "agent":
                    self._record_agent(node)
                elif func.attr == "result":
                    self._record_result(node)
        self._record_construction(node)
        self.generic_visit(node)

    def _record_agent(self, node: ast.Call) -> None:
        if not node.args:
            self.agents_dynamic = True
            return
        first = node.args[0]
        if isinstance(first, ast.Constant) and isinstance(first.value, str):
            if first.value not in self.agents:
                self.agents.append(first.value)
            return
        self.agents_dynamic = True
        # `ctx.agent(ev.agent, ...)` — remember which field carries the name.
        if (
            isinstance(first, ast.Attribute)
            and isinstance(first.value, ast.Name)
            and first.value.id == self.event_param
            and first.attr not in self.dynamic_agent_fields
        ):
            self.dynamic_agent_fields.append(first.attr)

    def visit_ListComp(self, node: ast.ListComp) -> None:
        self._visit_comprehension(node.generators, node.elt)

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:
        self._visit_comprehension(node.generators, node.elt)

    def _visit_comprehension(self, generators: list[ast.comprehension], elt: ast.expr) -> None:
        """Bind each loop variable to the iterable it draws from, then descend.

        Only the simple `for <name> in <iterable>` shape is bound; anything
        else just falls through to the generic visit and stays unresolved.
        """
        bound: list[str] = []
        for generator in generators:
            source = _field_source(generator.iter)
            if isinstance(generator.target, ast.Name) and source is not None:
                self._comprehension_sources[generator.target.id] = source
                bound.append(generator.target.id)
        try:
            self.visit(elt)
            for generator in generators:
                for condition in generator.ifs:
                    self.visit(condition)
                self.visit(generator.iter)
        finally:
            for name in bound:
                self._comprehension_sources.pop(name, None)

    def _record_construction(self, node: ast.Call) -> None:
        """`Event(field=<expr>)` — remember where `<expr>` gets its values."""
        if not isinstance(node.func, ast.Name):
            return
        event_name = node.func.id
        for keyword in node.keywords:
            if keyword.arg is None:
                continue
            source: _FieldSource | None = None
            if isinstance(keyword.value, ast.Name):
                source = self._comprehension_sources.get(keyword.value.id)
            if source is None:
                source = _field_source(keyword.value)
            if source is not None:
                self.constructed_fields.setdefault((event_name, keyword.arg), source)

    def _record_result(self, node: ast.Call) -> None:
        if not node.args:
            return
        first = node.args[0]
        name: str | None = None
        if isinstance(first, ast.Name):
            name = first.id
        elif isinstance(first, ast.Constant) and isinstance(first.value, str):
            name = first.value
        if name and name not in self.results:
            self.results.append(name)


def extract_agent_refs(
    fn: t.Callable[..., t.Any], ctx_param: str, event_param: str = ""
) -> _RefScanner:
    """Scan a step body. Returns empty results when source is unavailable."""
    scanner = _RefScanner(ctx_param, event_param)
    try:
        source = inspect.getsource(fn)
    except (OSError, TypeError):
        return scanner
    try:
        tree = ast.parse(_dedent(source))
    except SyntaxError:
        return scanner
    scanner.visit(tree)
    return scanner


def _dedent(source: str) -> str:
    lines = source.splitlines()
    if not lines:
        return source
    indent = len(lines[0]) - len(lines[0].lstrip())
    return "\n".join(line[indent:] if len(line) > indent else line.lstrip() for line in lines)


# ── Model documentation ──────────────────────────────────────────────────


def _field_docs(model: type[BaseModel]) -> list[FieldDoc]:
    docs: list[FieldDoc] = []
    for name, field in model.model_fields.items():
        default = None if field.is_required() else field.default
        if default is not None and not isinstance(default, (str, int, float, bool, list, dict)):
            default = None
        docs.append(
            FieldDoc(
                name=name,
                type=_annotation_text(field.annotation),
                required=field.is_required(),
                default=default,
                doc=field.description,
            )
        )
    return docs


def _source_span(obj: t.Any, root: str | None) -> SourceSpan | None:
    """Locate an authored object, with its path relative to the capability root.

    The path is what the run page links to, so it must be capability-relative —
    an absolute build-machine path is both useless to a reader and a small
    information leak into a stored artifact. ``root`` may be given relative, so
    resolve both sides before comparing.
    """
    try:
        lines, start = inspect.getsourcelines(obj)
        path = inspect.getsourcefile(obj) or ""
    except (OSError, TypeError):
        return None
    if root and path:
        resolved_root = str(pathlib.Path(root).resolve())
        resolved_path = str(pathlib.Path(path).resolve())
        if resolved_path.startswith(resolved_root):
            path = resolved_path[len(resolved_root) :].lstrip("/")
    return SourceSpan(path=path, start_line=start, end_line=start + len(lines) - 1)


def _event_doc(event: type, root: str | None) -> EventTypeDoc:
    builtin = event.__name__ in _BUILTIN_EVENTS
    schema: dict[str, t.Any] = {}
    fields: list[FieldDoc] = []
    if isinstance(event, type) and issubclass(event, BaseModel):
        try:
            schema = event.model_json_schema()
        except Exception:
            schema = {}
        fields = _field_docs(event)
    return EventTypeDoc(
        doc=inspect.getdoc(event),
        schema=schema,
        fields=fields,
        source=None if builtin else _source_span(event, root),
        builtin=builtin,
    )


# ── The compiler ─────────────────────────────────────────────────────────


def compile_workflow(
    workflow: Workflow,
    *,
    capability: str | None = None,
    source_root: str | None = None,
    known_agents: t.Collection[str] | None = None,
) -> Topology:
    """Derive the topology document from an authored ``Workflow``.

    Raises:
        WorkflowCompileError: with *every* problem found.
    """
    errors: list[CompileError] = []
    root = source_root.rstrip("/") if source_root else None

    consumed_by: dict[str, _Consumed] = {}
    emitted_by: dict[str, list[_Emitted]] = {}
    event_types: dict[str, type] = {}
    scanners: dict[str, _RefScanner] = {}
    entry_steps: list[str] = []

    for key, step in workflow.steps.items():
        span = _source_span(step.fn, root)
        consumed, emits, step_errors = _analyze_step(step, span)
        errors.extend(step_errors)
        if consumed is None:
            continue

        consumed_by[key] = consumed
        emitted_by[key] = emits
        scanners[key] = extract_agent_refs(
            step.fn, consumed.param_name or "ctx", _event_param_name(step)
        )

        for event in consumed.events:
            if _is_start_event(event):
                entry_steps.append(key)
            _register_event(event_types, event, key, errors)
        for emit in emits:
            if emit.event is not None:
                _register_event(event_types, emit.event, key, errors)

    # Entry and terminal
    if not entry_steps:
        errors.append(
            CompileError(
                code="WF-VALID-001",
                message="no step consumes StartEvent[...]",
                hint="one step must take `ev: StartEvent[YourInput]` as its event parameter",
            )
        )
    elif len(entry_steps) > 1:
        errors.append(
            CompileError(
                code="WF-VALID-002",
                message=f"{len(entry_steps)} steps consume StartEvent: {', '.join(sorted(entry_steps))}",
                hint="exactly one step is the entry point; fork from it with a tuple return",
            )
        )

    terminals = [
        key
        for key, emits in emitted_by.items()
        if any(_is_stop_event(e.event) for e in emits if e.event is not None)
    ]
    if not terminals:
        errors.append(
            CompileError(
                code="WF-VALID-003",
                message="no step emits StopEvent[...]",
                hint="a step must return `StopEvent(result=...)` to end the run",
            )
        )

    # Edges: an emitted type routes to whichever step consumes it.
    consumers: dict[str, list[str]] = {}
    for key, consumed in consumed_by.items():
        for event in consumed.events:
            consumers.setdefault(_event_name(event), []).append(key)

    edges: list[TopologyEdge] = []
    fan_out_points: list[FanOutPoint] = []

    for key, emits in emitted_by.items():
        step = workflow.steps[key]
        for emit in emits:
            if _is_stop_event(emit.event):
                continue
            # An emitted ApprovalRequest suspends the run; what wakes it is the
            # ApprovalDecision the platform records. So the edge runs from the
            # gate to whichever step consumes the decision, carrying the decision.
            emitted_name = emit.name
            if emitted_name == "ApprovalRequest":
                targets = consumers.get("ApprovalDecision", [])
                emitted_name = "ApprovalDecision"
                if not targets:
                    errors.append(
                        CompileError(
                            code="WF-VALID-006",
                            message=f"step {key!r} requests approval but no step consumes ApprovalDecision",
                            step=key,
                            path=_span_path(key, workflow, root),
                            hint="add a step taking `decision: ApprovalDecision` to resume after the gate",
                        )
                    )
                    continue
            else:
                targets = consumers.get(emit.name, [])
                if not targets:
                    errors.append(
                        CompileError(
                            code="WF-VALID-006",
                            message=f"event {emit.name!r} is emitted but no step consumes it",
                            step=key,
                            path=_span_path(key, workflow, root),
                            hint=f"add a step taking `ev: {emit.name}`, or stop emitting it",
                        )
                    )
                    continue
            for target in targets:
                kind = _edge_kind(emit, consumed_by[target])
                edges.append(
                    TopologyEdge(
                        id=f"{key}->{target}:{emitted_name}",
                        **{"from": key},
                        to=target,
                        event=emitted_name,
                        kind=kind,
                        label=emitted_name,
                        arm=emit.arm,
                    )
                )
                if emit.cardinality == "many":
                    cap = step.materialization_cap or DEFAULT_MATERIALIZATION_CAP
                    fan_out_points.append(FanOutPoint(node=key, target=target, cap=cap))

    # Joins
    join_points: list[JoinPoint] = []
    for key, consumed in consumed_by.items():
        if not consumed.collect:
            continue
        sources = sorted({e.from_ for e in edges if e.to == key})
        names = [_event_name(ev) for ev in consumed.events]
        min_success = consumed_min_success(workflow.steps[key], consumed)
        join_points.append(
            JoinPoint(node=key, collects=names, **{"from": sources}, min_success=min_success)
        )
        for name in names:
            if not any(e.event == name and e.to == key for e in edges):
                errors.append(
                    CompileError(
                        code="WF-VALID-017",
                        message=f"Collect declares {name!r} but no step emits it",
                        step=key,
                        path=_span_path(key, workflow, root),
                        hint=f"a step upstream must return {name}",
                    )
                )

    errors.extend(_check_collect_has_fanout(consumed_by, emitted_by, edges, workflow, root))
    errors.extend(_check_result_refs(scanners, emitted_by, workflow, root))
    errors.extend(_check_agents(scanners, known_agents, workflow, root))
    errors.extend(_check_keys(workflow, root))
    errors.extend(_check_title_template(workflow))

    reachable = _reachable(entry_steps[0], edges) if entry_steps else set()
    for key in workflow.steps:
        if key in consumed_by and entry_steps and key not in reachable:
            errors.append(
                CompileError(
                    code="WF-VALID-005",
                    message=f"step {key!r} is unreachable from the entry point",
                    step=key,
                    path=_span_path(key, workflow, root),
                    hint="nothing emits the event it consumes",
                )
            )

    candidates = _agent_candidates(workflow, consumed_by, scanners, edges)

    for cycle in _find_cycles(edges):
        errors.append(
            CompileError(
                code="WF-VALID-007",
                message=f"cycle in the graph: {' -> '.join(cycle)}",
                hint=(
                    "cycles are not supported in v1. Bounded loops "
                    "(`max_iterations=` on a step in the cycle) are planned"
                ),
            )
        )

    topology = Topology(
        topology_version=TOPOLOGY_VERSION,
        name=workflow.name,
        capability=capability,
        doc=_module_doc(workflow),
        source=_module_span(workflow, root),
        source_sha256=_module_sha256(workflow),
        input=_input_doc(workflow),
        config=WorkflowConfig(
            timeout_sec=workflow.timeout_sec,
            title_template=workflow.title or _default_title_template(workflow),
        ),
        event_types={
            name: _event_doc(event, root)
            for name, event in sorted(event_types.items())
            if _generic_origin(event) not in (StartEvent, StopEvent)
        },
        nodes=[
            _node(
                workflow.steps[key],
                consumed_by[key],
                emitted_by[key],
                scanners[key],
                entry=key in entry_steps,
                terminal=key in terminals,
                root=root,
                agent_candidates=candidates.get(key, []),
            )
            for key in workflow.steps
            if key in consumed_by
        ],
        edges=edges,
        fan_out_points=fan_out_points,
        join_points=join_points,
        entry=entry_steps[0] if entry_steps else "",
        terminals=sorted(terminals),
    )

    errors.extend(_check_min_success_bounds(topology))

    size = len(json.dumps(topology.to_json_dict()).encode())
    if size > TOPOLOGY_SIZE_CAP_BYTES:
        errors.append(
            CompileError(
                code="WF-VALID-010",
                message=(
                    f"topology document is {size} bytes, over the "
                    f"{TOPOLOGY_SIZE_CAP_BYTES} byte cap"
                ),
                hint="reduce the number of steps or the size of event schemas",
            )
        )

    if errors:
        raise WorkflowCompileError(workflow.name, errors)
    return topology


def _register_event(
    registry: dict[str, type], event: type, step: str, errors: list[CompileError]
) -> None:
    name = _event_name(event)
    previous = registry.setdefault(name, event)
    if previous is not event:
        errors.append(
            CompileError(
                code="WF-VALID-019",
                step=step,
                message=f"distinct event types share the topology name {name!r}",
                hint="give each event type a unique class name",
            )
        )


def _check_min_success_bounds(topology: Topology) -> list[CompileError]:
    """Reject only thresholds above a conservative upper bound on input count.

    Propagate fan-out caps through ordinary steps; joins collapse their inputs
    to one instance. Summing branch alternatives deliberately overestimates,
    so a valid graph is never rejected for mutually exclusive paths.
    """
    widths: dict[str, int | None] = {}
    visiting: set[str] = set()

    def instances(key: str) -> int | None:
        if key in widths:
            return widths[key]
        if key in visiting:
            return None  # The cycle validator owns this error.
        node = topology.node(key)
        if key == topology.entry or node.consumes.collect:
            return 1
        visiting.add(key)
        counts = [outputs(edge.from_, edge.event) for edge in topology.predecessors(key)]
        visiting.remove(key)
        width = (
            None
            if any(count is None for count in counts)
            else sum(count for count in counts if count is not None)
        )
        widths[key] = width
        return width

    def outputs(key: str, event: str) -> int | None:
        width = instances(key)
        if width is None:
            return None
        node = topology.node(key)
        return width * sum(
            (node.config.materialization_cap or DEFAULT_MATERIALIZATION_CAP)
            if emit.cardinality == "many"
            else 1
            for emit in node.emits
            if emit.event == event
            or (emit.event == "ApprovalRequest" and event == "ApprovalDecision")
        )

    errors: list[CompileError] = []
    for join in topology.join_points:
        if not isinstance(join.min_success, int):
            continue
        counts = [outputs(edge.from_, edge.event) for edge in topology.predecessors(join.node)]
        if any(count is None for count in counts):
            continue
        maximum = sum(count for count in counts if count is not None)
        if join.min_success > maximum:
            errors.append(
                CompileError(
                    code="WF-VALID-012",
                    step=join.node,
                    message=f"min_success={join.min_success} exceeds the maximum {maximum} inputs",
                    hint="lower min_success or increase the upstream fan-out materialization cap",
                )
            )
    return errors


def consumed_min_success(step: StepDef, consumed: _Consumed) -> int | t.Literal["all"] | None:
    """Resolve the effective ``min_success`` for a join.

    Multi-type joins default to ``"all"`` — a diamond wants both inputs. Fan-out
    joins default to 1, so a zero-width fan-out fails rather than silently
    producing an empty report.
    """
    if step.min_success is not None:
        return step.min_success
    return "all" if len(consumed.events) > 1 else 1


# ── Per-step analysis ────────────────────────────────────────────────────


def _analyze_step(
    step: StepDef, span: SourceSpan | None
) -> tuple[_Consumed | None, list[_Emitted], list[CompileError]]:
    errors: list[CompileError] = []
    path = span.path if span else None
    line = span.start_line if span else None

    try:
        hints = t.get_type_hints(step.fn)
    except Exception as exc:
        errors.append(
            CompileError(
                code="WF-VALID-015",
                message=f"cannot resolve type hints for {step.key!r}: {exc}",
                step=step.key,
                path=path,
                line=line,
                hint=(
                    "`from __future__ import annotations` breaks runtime "
                    "introspection and is banned in this repo — remove it"
                ),
            )
        )
        return None, [], errors

    signature = inspect.signature(step.fn)
    params = list(signature.parameters.values())
    if len(params) != 2:
        errors.append(
            CompileError(
                code="WF-VALID-013",
                message=f"step {step.key!r} must take exactly (ctx, event), got {len(params)} params",
                step=step.key,
                path=path,
                line=line,
                hint="cross-cutting handles belong on ctx; data belongs in the event",
            )
        )
        return None, [], errors

    event_param = params[1]
    annotation = hints.get(event_param.name, inspect.Parameter.empty)
    collect_types = _unwrap_collect(annotation)

    if collect_types is not None:
        consumed = _Consumed(
            events=collect_types,
            collect=True,
            param_name=params[0].name,
            annotation_text=_annotation_text(annotation),
        )
    elif _is_event_class(annotation) or _is_start_event(annotation):
        consumed = _Consumed(
            events=[annotation],
            collect=False,
            param_name=params[0].name,
            annotation_text=_annotation_text(annotation),
        )
    else:
        errors.append(
            CompileError(
                code="WF-VALID-016",
                message=(
                    f"step {step.key!r} parameter {event_param.name!r} is not a "
                    f"WorkflowEvent, StartEvent[...], or Collect[...]"
                ),
                step=step.key,
                path=path,
                line=line,
                hint="annotate it with the event type this step consumes",
            )
        )
        return None, [], errors

    return_annotation = hints.get("return", inspect.Signature.empty)
    if return_annotation is inspect.Signature.empty:
        errors.append(
            CompileError(
                code="WF-VALID-014",
                message=f"step {step.key!r} has no return annotation",
                step=step.key,
                path=path,
                line=line,
                hint="the return annotation *is* the outgoing edge — it cannot be inferred",
            )
        )
        return consumed, [], errors

    emits = _analyze_return(return_annotation)
    for emit in emits:
        if emit.event is None or not (_is_event_class(emit.event) or _is_stop_event(emit.event)):
            errors.append(
                CompileError(
                    code="WF-VALID-016",
                    message=f"step {step.key!r} returns {emit.name!r}, which is not a WorkflowEvent",
                    step=step.key,
                    path=path,
                    line=line,
                )
            )
    return consumed, emits, errors


def _agent_candidates(
    workflow: Workflow,
    consumed_by: dict[str, _Consumed],
    scanners: dict[str, _RefScanner],
    edges: list[TopologyEdge],
) -> dict[str, list[str]]:
    """Names a dynamic agent step *might* run, resolved from its producer.

    A step written as ``ctx.agent(ev.agent, ...)`` cannot be named by the
    topology — but the step that builds those events usually can be. The
    idiomatic fan-out is ``[Task(agent=a) for a in ROSTER]`` with ``ROSTER`` a
    module-level constant, and that is exactly what this walks back to.

    Best-effort and clearly labelled as such at every layer: an unresolvable
    producer yields nothing and the node stays anonymous rather than guessing.
    Candidates are what the graph *could* run, which is why they never populate
    ``agents`` — that field means "this step calls these", and only a run can
    say which ones it actually did.
    """
    resolved: dict[str, list[str]] = {}

    for key, scanner in scanners.items():
        if not scanner.agents_dynamic or not scanner.dynamic_agent_fields:
            continue
        consumed = consumed_by.get(key)
        if consumed is None:
            continue

        consumed_names = {_event_name(event) for event in consumed.events}
        producers = {
            edge.from_ for edge in edges if edge.to == key and edge.event in consumed_names
        }

        names: list[str] = []
        for field in scanner.dynamic_agent_fields:
            for producer in sorted(producers):
                producer_step = workflow.steps.get(producer)
                producer_scanner = scanners.get(producer)
                if producer_step is None or producer_scanner is None:
                    continue
                namespace = getattr(producer_step.fn, "__globals__", {}) or {}
                for event_name in sorted(consumed_names):
                    source = producer_scanner.constructed_fields.get((event_name, field))
                    if source is None:
                        continue
                    for name in resolve_field_source(source, namespace):
                        if name not in names:
                            names.append(name)
        if names:
            resolved[key] = names

    return resolved


def _node(
    step: StepDef,
    consumed: _Consumed,
    emits: list[_Emitted],
    scanner: _RefScanner,
    *,
    entry: bool,
    terminal: bool,
    root: str | None,
    agent_candidates: list[str] | None = None,
) -> TopologyNode:
    doc = step.doc
    is_agent = bool(scanner.agents) or scanner.agents_dynamic
    emits_approval = any(e.name == "ApprovalRequest" for e in emits)

    kind: NodeKind = "plain"
    if terminal:
        kind = "terminal"
    elif emits_approval:
        kind = "approval_gate"
    elif consumed.collect:
        kind = "join"
    elif is_agent:
        kind = "agent"
    elif entry:
        kind = "entry"

    return TopologyNode(
        key=step.key,
        title=step.title,
        kind=kind,
        doc=doc,
        doc_summary=doc.split("\n", 1)[0] if doc else None,
        consumes=NodeConsumes(
            events=[_event_name(e) for e in consumed.events],
            collect=consumed.collect,
            min_success=consumed_min_success(step, consumed) if consumed.collect else None,
        ),
        emits=[
            NodeEmit(event=e.name, cardinality=e.cardinality, arm=e.arm, fork_index=e.fork_index)
            for e in emits
        ],
        params=[
            ParamDoc(name=consumed.param_name, annotation="Ctx", kind="context"),
            ParamDoc(
                name=_event_param_name(step),
                annotation=consumed.annotation_text,
                kind="collect" if consumed.collect else "event",
            ),
        ],
        config=NodeConfig(
            max_concurrency=step.max_concurrency,
            retries=step.retries,
            effective_max_attempts=1 if is_agent else 1 + step.retries,
            materialization_cap=(
                (step.materialization_cap or DEFAULT_MATERIALIZATION_CAP)
                if any(e.cardinality == "many" for e in emits)
                else None
            ),
            timeout_sec=step.timeout_sec,
            max_iterations=None,
        ),
        agents=scanner.agents,
        agents_dynamic=scanner.agents_dynamic,
        agent_candidates=agent_candidates or [],
        reads_results_of=scanner.results,
        source=_source_span(step.fn, root),
    )


def _event_param_name(step: StepDef) -> str:
    params = list(inspect.signature(step.fn).parameters.values())
    return params[1].name if len(params) > 1 else "ev"


# ── Graph checks ─────────────────────────────────────────────────────────


def _edge_kind(
    emit: _Emitted, target: _Consumed
) -> t.Literal["sequential", "fan_out", "fork", "join", "branch", "approval"]:
    # Keyed on what was emitted, not on the target: a step that resumes after a
    # gate may also join unrelated inputs, and those edges are ordinary joins.
    if emit.name == "ApprovalRequest":
        return "approval"
    if target.collect:
        return "join"
    if emit.cardinality == "many":
        return "fan_out"
    if emit.fork_index is not None:
        return "fork"
    if emit.arm is not None:
        return "branch"
    return "sequential"


def _check_collect_has_fanout(
    consumed_by: dict[str, _Consumed],
    emitted_by: dict[str, list[_Emitted]],
    edges: list[TopologyEdge],
    workflow: Workflow,
    root: str | None,
) -> list[CompileError]:
    """A single-type ``Collect`` needs a fan-out upstream, or it joins nothing."""
    errors: list[CompileError] = []
    for key, consumed in consumed_by.items():
        if not consumed.collect or len(consumed.events) != 1:
            continue
        name = _event_name(consumed.events[0])
        if name in ("ApprovalDecision",):
            continue
        producers = [e.from_ for e in edges if e.to == key and e.event == name]
        fans_out = any(
            any(em.cardinality == "many" for em in emitted_by.get(p, []))
            for p in _ancestors(producers, edges)
        )
        if not fans_out:
            errors.append(
                CompileError(
                    code="WF-VALID-004",
                    message=f"Collect[{name}] at {key!r} has no matching fan-out",
                    step=key,
                    path=_span_path(key, workflow, root),
                    hint=f"a step upstream must return list[{name}] or list[...] feeding it",
                )
            )
    return errors


def _check_result_refs(
    scanners: dict[str, _RefScanner],
    emitted_by: dict[str, list[_Emitted]],
    workflow: Workflow,
    root: str | None,
) -> list[CompileError]:
    """``ctx.result()`` may not target a fan-out step — which of the five?"""
    errors: list[CompileError] = []
    fanned_out = {
        target
        for key, emits in emitted_by.items()
        for emit in emits
        if emit.cardinality == "many"
        for target in _consumers_of(emit.name, workflow)
    }
    for key, scanner in scanners.items():
        for ref in scanner.results:
            if ref in fanned_out:
                errors.append(
                    CompileError(
                        code="WF-VALID-011",
                        message=(
                            f"ctx.result({ref!r}) is ambiguous — {ref!r} runs once per "
                            f"fan-out element"
                        ),
                        step=key,
                        path=_span_path(key, workflow, root),
                        hint="join it with `Collect[...]` instead of reading its result",
                    )
                )
    return errors


def _check_agents(
    scanners: dict[str, _RefScanner],
    known_agents: t.Collection[str] | None,
    workflow: Workflow,
    root: str | None,
) -> list[CompileError]:
    if known_agents is None:
        return []
    known = set(known_agents)
    return [
        CompileError(
            code="WF-VALID-008",
            message=f"step {key!r} calls unknown agent {agent!r}",
            step=key,
            path=_span_path(key, workflow, root),
            hint=f"declared agents: {', '.join(sorted(known)) or '(none)'}",
        )
        for key, scanner in scanners.items()
        for agent in scanner.agents
        if agent not in known
    ]


_KEY_PATTERN = __import__("re").compile(r"^[a-z][a-z0-9_]*$")


def _check_keys(workflow: Workflow, root: str | None) -> list[CompileError]:
    return [
        CompileError(
            code="WF-VALID-009",
            message=f"step key {key!r} must match [a-z][a-z0-9_]*",
            step=key,
            path=_span_path(key, workflow, root),
            hint="the key is author-visible identity — renaming it creates a new node",
        )
        for key in workflow.steps
        if not _KEY_PATTERN.match(key)
    ]


def _consumers_of(event_name: str, workflow: Workflow) -> list[str]:
    out: list[str] = []
    for key, step in workflow.steps.items():
        try:
            hints = t.get_type_hints(step.fn)
        except Exception:  # noqa: S112
            continue
        params = list(inspect.signature(step.fn).parameters.values())
        if len(params) < 2:
            continue
        annotation = hints.get(params[1].name)
        collect = _unwrap_collect(annotation)
        candidates = collect if collect is not None else [annotation]
        if any(c is not None and _event_name(c) == event_name for c in candidates):
            out.append(key)
    return out


def _ancestors(keys: list[str], edges: list[TopologyEdge]) -> set[str]:
    seen: set[str] = set()
    stack = list(keys)
    while stack:
        node = stack.pop()
        if node in seen:
            continue
        seen.add(node)
        stack.extend(e.from_ for e in edges if e.to == node)
    return seen


def _reachable(entry: str, edges: list[TopologyEdge]) -> set[str]:
    seen = {entry}
    stack = [entry]
    while stack:
        node = stack.pop()
        for edge in edges:
            if edge.from_ == node and edge.to not in seen:
                seen.add(edge.to)
                stack.append(edge.to)
    return seen


def _find_cycles(edges: list[TopologyEdge]) -> list[list[str]]:
    graph: dict[str, list[str]] = {}
    for edge in edges:
        graph.setdefault(edge.from_, []).append(edge.to)

    cycles: list[list[str]] = []
    state: dict[str, int] = {}
    path: list[str] = []

    def walk(node: str) -> None:
        state[node] = 1
        path.append(node)
        for nxt in graph.get(node, []):
            if state.get(nxt, 0) == 0:
                walk(nxt)
            elif state.get(nxt) == 1:
                start = path.index(nxt)
                cycles.append([*path[start:], nxt])
        path.pop()
        state[node] = 2

    for node in list(graph):
        if state.get(node, 0) == 0:
            walk(node)
    return cycles


# ── Module-level docs ────────────────────────────────────────────────────


def _module_of(workflow: Workflow) -> t.Any:
    for step in workflow.steps.values():
        return inspect.getmodule(step.fn)
    return None


def _module_doc(workflow: Workflow) -> str | None:
    module = _module_of(workflow)
    return inspect.getdoc(module) if module else None


def _module_sha256(workflow: Workflow) -> str | None:
    module = _module_of(workflow)
    path = inspect.getsourcefile(module) if module else None
    if not path:
        return None
    try:
        return hashlib.sha256(pathlib.Path(path).read_bytes()).hexdigest()
    except OSError:
        return None


def _module_span(workflow: Workflow, root: str | None) -> SourceSpan | None:
    module = _module_of(workflow)
    return _source_span(module, root) if module else None


def _input_doc(workflow: Workflow) -> TopologyInput:
    model = workflow.input
    schema: dict[str, t.Any] = {}
    fields: list[FieldDoc] = []
    if isinstance(model, type) and issubclass(model, BaseModel):
        try:
            schema = model.model_json_schema()
        except Exception:
            schema = {}
        fields = _field_docs(model)
    return TopologyInput(
        type_name=getattr(model, "__name__", str(model)),
        doc=inspect.getdoc(model),
        schema=schema,
        fields=fields,
    )


def _span_path(key: str, workflow: Workflow, root: str | None) -> str | None:
    span = _source_span(workflow.steps[key].fn, root)
    return span.path if span else None


_TITLE_FIELD = __import__("re").compile(r"\{([a-zA-Z_][a-zA-Z0-9_]*)\}")


def _input_fields(workflow: Workflow) -> dict[str, t.Any]:
    model = workflow.input
    if isinstance(model, type) and issubclass(model, BaseModel):
        return dict(model.model_fields)
    return {}


def _check_title_template(workflow: Workflow) -> list[CompileError]:
    """A title placeholder must name a real input field.

    Caught at push so a typo fails loudly rather than producing runs literally
    titled ``{githuburl}``.
    """
    if not workflow.title:
        return []
    fields = _input_fields(workflow)
    return [
        CompileError(
            code="WF-VALID-018",
            message=(
                f"title template references {{{name}}}, which is not a field of "
                f"{getattr(workflow.input, '__name__', 'the input model')}"
            ),
            hint=f"available fields: {', '.join(sorted(fields)) or '(none)'}",
        )
        for name in _TITLE_FIELD.findall(workflow.title)
        if name not in fields
    ]


def _default_title_template(workflow: Workflow) -> str | None:
    """Fall back to the first required string field.

    A workflow that never thinks about titles still gets something better than
    a UUID, without the author declaring anything.
    """
    for name, field in _input_fields(workflow).items():
        if field.is_required() and field.annotation is str:
            return f"{{{name}}}"
    return None
