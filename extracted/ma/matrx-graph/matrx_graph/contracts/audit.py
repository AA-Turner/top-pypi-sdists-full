"""Recursive type-contract audit over node schemas.

Walks every registered node's ``input_schema`` / ``output_schema`` /
``config_schema`` (and, transitively, every nested model) and reports
exactly where a contract stops being typed — the boundary between a fully
specified Pydantic shape and an untyped escape hatch (``Any``, bare
``dict``/``list``, ``dict[str, Any]``, ``object``, ``extra="allow"``, …).

Everything is computed from the live model classes via runtime reflection —
there is no hand-maintained list to drift. Conformance is transitive: a
referenced model is an acceptable leaf iff that model itself passes; cycles
are detected and are not leaks.

The ruleset is versioned data (:class:`Ruleset`), not hardcoded logic —
tighten it by shipping a new version.
"""

from __future__ import annotations

import collections.abc as _abc
import datetime as _dt
import decimal
import enum
import ipaddress
import pathlib
import types as _types
import typing
import uuid
from typing import Annotated, Any, Literal, Union, get_args, get_origin

from pydantic import BaseModel, ConfigDict, Field

if typing.TYPE_CHECKING:  # pragma: no cover
    from matrx_graph.executor.registry import NodeRegistry

# ---------------------------------------------------------------------------
# Ruleset — versioned config
# ---------------------------------------------------------------------------


class LeakRule(str, enum.Enum):
    """Why a branch of a contract is considered untyped."""

    ANY = "any"  # typing.Any
    OBJECT = "object"  # bare `object`
    BARE_CONTAINER = "bare_container"  # dict / list / set / tuple without params
    EXTRA_ALLOW = "extra_allow"  # model_config extra="allow" (open shape)
    UNBOUND_TYPEVAR = "unbound_typevar"  # unparameterized Generic field
    UNKNOWN_TYPE = "unknown_type"  # not a scalar, enum, or Pydantic model
    # extra="allow" that carries an in-code justification — the model is
    # dynamic FOREVER by design (raw provider passthrough, client-authored
    # payload). Declared beside the config, never in a suppression list:
    #   model_config = ConfigDict(
    #       extra="allow",
    #       json_schema_extra={"x-contract-dynamic": "<why this stays open>"},
    #   )
    ACKNOWLEDGED_DYNAMIC = "acknowledged_dynamic"


class SchemaRole(str, enum.Enum):
    INPUT = "input"
    OUTPUT = "output"
    CONFIG = "config"


class Ruleset(BaseModel):
    """The conformance rules in force. Versioned, additive-only."""

    model_config = ConfigDict(frozen=True)

    version: int
    enabled_rules: tuple[LeakRule, ...]
    # Dotted names of non-model leaf types accepted as scalar primitives.
    allowed_scalars: tuple[str, ...]
    # Named type aliases accepted as fully-typed leaves. pydantic.JsonValue is
    # the canonical primitive for a genuinely-dynamic JSON field — it is a
    # closed recursive union of JSON primitives, i.e. typed "JSON by design",
    # never an escape hatch like Any.
    allowed_aliases: tuple[str, ...] = ()
    # Rules applied to INPUT schemas only (outputs/config always get
    # enabled_rules). Input schemas are open by engine design — edge mappings
    # deliver arbitrary keys — so v2 excuses extra="allow" there while keeping
    # every other rule.
    input_rules: tuple[LeakRule, ...] | None = None


_SCALAR_TYPES: tuple[type, ...] = (
    str,
    int,
    float,
    bool,
    bytes,
    type(None),
    decimal.Decimal,
    _dt.datetime,
    _dt.date,
    _dt.time,
    _dt.timedelta,
    uuid.UUID,
    pathlib.Path,
    ipaddress.IPv4Address,
    ipaddress.IPv6Address,
)

# Frozen rule tuples per version — never `tuple(LeakRule)`, which would let a
# newly added enum member silently rewrite an already-shipped ruleset.
_V1_RULES: tuple[LeakRule, ...] = (
    LeakRule.ANY,
    LeakRule.OBJECT,
    LeakRule.BARE_CONTAINER,
    LeakRule.EXTRA_ALLOW,
    LeakRule.UNBOUND_TYPEVAR,
    LeakRule.UNKNOWN_TYPE,
)

RULESET_V1 = Ruleset(
    version=1,
    enabled_rules=_V1_RULES,
    allowed_scalars=tuple(f"{t.__module__}.{t.__qualname__}" for t in _SCALAR_TYPES),
)

RULESET_V2 = Ruleset(
    version=2,
    enabled_rules=_V1_RULES,
    allowed_scalars=RULESET_V1.allowed_scalars,
    allowed_aliases=("pydantic.JsonValue",),
    input_rules=tuple(r for r in _V1_RULES if r is not LeakRule.EXTRA_ALLOW),
)

# v3 — v2 plus the acknowledged-dynamic rule: a justified extra="allow"
# (x-contract-dynamic in the model's json_schema_extra) is reported as its own
# rule and yields the DYNAMIC state instead of counting as debt. Inputs
# already excuse extra_allow, so acknowledged inputs don't reappear as leaks.
RULESET_V3 = Ruleset(
    version=3,
    enabled_rules=(*_V1_RULES, LeakRule.ACKNOWLEDGED_DYNAMIC),
    allowed_scalars=RULESET_V1.allowed_scalars,
    allowed_aliases=RULESET_V2.allowed_aliases,
    input_rules=tuple(r for r in _V1_RULES if r is not LeakRule.EXTRA_ALLOW),
)


# ---------------------------------------------------------------------------
# Report models
# ---------------------------------------------------------------------------


class ConformanceState(str, enum.Enum):
    FULL = "full"  # zero leaks, all the way down
    DYNAMIC = "dynamic"  # only acknowledged-dynamic leaks — open BY DESIGN
    PARTIAL = "partial"  # this layer is typed; a deeper branch is not
    NON_CONFORMANT = "non_conformant"  # a top-level field is itself untyped


class TypeLeak(BaseModel):
    """One exact point where typing stops."""

    model_config = ConfigDict(frozen=True)

    path: str  # e.g. "usage.details[value]" — field hops + container drills
    rule: LeakRule
    annotation: str  # repr of the offending annotation
    owner_model: str  # qualname of the model class the field lives on
    depth: int  # field hops from the schema root (0 = direct field)


class SchemaReport(BaseModel):
    """Audit of one schema class (an input/output/config root, or a shared model)."""

    schema_name: str  # qualname
    module: str
    state: ConformanceState
    leaks: list[TypeLeak]
    field_count: int
    cyclic: bool = False  # a reference cycle was encountered (not a leak)


class NodeContractReport(BaseModel):
    node_type: str  # stable identifier
    category: str
    display_name: str
    state: ConformanceState  # worst of the three schemas
    input: SchemaReport
    output: SchemaReport
    config: SchemaReport


class ModelReport(BaseModel):
    """A distinct model class and every node that (transitively) uses it —
    fixing one shared model shows its blast radius here."""

    schema_name: str
    module: str
    state: ConformanceState
    own_leak_count: int  # leaks on this model's DIRECT fields only
    referenced_by: list[str]  # node types that reach this model


class RuleCount(BaseModel):
    rule: LeakRule
    count: int


class AuditTotals(BaseModel):
    nodes: int
    full: int
    dynamic: int  # DYNAMIC nodes — every leak acknowledged, open by design
    partial: int
    non_conformant: int
    percent_full: float  # FULL only — dynamic never counts as fully typed
    leaks_by_rule: list[RuleCount]


class ContractAuditReport(BaseModel):
    ruleset: Ruleset
    totals: AuditTotals
    nodes: list[NodeContractReport]
    models: list[ModelReport]


# ---------------------------------------------------------------------------
# The walker
# ---------------------------------------------------------------------------

_UNION_TYPES = (Union, _types.UnionType)

_ALIAS_TYPES: tuple[type, ...]
try:  # pydantic uses typing_extensions.TypeAliasType, which is a distinct class
    from typing_extensions import TypeAliasType as _ExtTypeAliasType

    _ALIAS_TYPES = (typing.TypeAliasType, _ExtTypeAliasType)
except ImportError:  # pragma: no cover
    _ALIAS_TYPES = (typing.TypeAliasType,)


class _Auditor:
    def __init__(self, ruleset: Ruleset) -> None:
        self.ruleset = ruleset
        self._enabled = set(ruleset.enabled_rules)
        self._scalars = set(ruleset.allowed_scalars)
        # model class -> leaks relative to that model's root (memoized)
        self._model_cache: dict[type[BaseModel], tuple[list[TypeLeak], bool]] = {}
        # model class -> node types that transitively reference it
        self.model_refs: dict[type[BaseModel], set[str]] = {}
        # models whose subtree hit a reference cycle while being walked
        self._had_cycle: dict[type[BaseModel], bool] = {}
        # bare names of allowlisted type aliases (e.g. {"JsonValue"})
        self._alias_names = {a.rsplit(".", 1)[-1] for a in ruleset.allowed_aliases}
        # non-allowlisted recursive aliases currently being unwrapped
        self._alias_stack: set[object] = set()

    # -- public -------------------------------------------------------------

    def audit_schema(
        self,
        model: type[BaseModel],
        *,
        node_type: str | None = None,
        role: SchemaRole = SchemaRole.OUTPUT,
    ) -> SchemaReport:
        leaks, cyclic = self._audit_model(model, stack=())
        if role is SchemaRole.INPUT and self.ruleset.input_rules is not None:
            # Leaks are always computed at full strictness (the memo cache is
            # role-agnostic); the role filter applies at report time.
            allowed = set(self.ruleset.input_rules)
            leaks = [leak for leak in leaks if leak.rule in allowed]
        if node_type is not None:
            self._record_refs(model, node_type, seen=set())
        return SchemaReport(
            schema_name=model.__qualname__,
            module=model.__module__,
            state=_state_of(leaks),
            leaks=sorted(leaks, key=lambda leak: (leak.depth, leak.path)),
            field_count=len(model.model_fields),
            cyclic=cyclic,
        )

    # -- model-level --------------------------------------------------------

    def _audit_model(
        self, model: type[BaseModel], *, stack: tuple[type[BaseModel], ...]
    ) -> tuple[list[TypeLeak], bool]:
        if model in stack:  # cycle — the reference is fine, stop descending
            return [], True
        cached = self._model_cache.get(model)
        if cached is not None:
            return cached
        leaks: list[TypeLeak] = []
        cyclic = False
        extra = (model.model_config or {}).get("extra")
        if extra == "allow":
            reason = _dynamic_acknowledgment(model)
            if reason is not None and LeakRule.ACKNOWLEDGED_DYNAMIC in self._enabled:
                leaks.append(
                    TypeLeak(
                        path="<model>",
                        rule=LeakRule.ACKNOWLEDGED_DYNAMIC,
                        annotation=f'extra="allow" — {reason}',
                        owner_model=model.__qualname__,
                        depth=0,
                    )
                )
            elif LeakRule.EXTRA_ALLOW in self._enabled:
                leaks.append(
                    TypeLeak(
                        path="<model>",
                        rule=LeakRule.EXTRA_ALLOW,
                        annotation='extra="allow"',
                        owner_model=model.__qualname__,
                        depth=0,
                    )
                )
        for name, field in model.model_fields.items():
            leaks.extend(
                self._walk(
                    field.annotation,
                    path=name,
                    owner=model,
                    depth=0,
                    stack=(*stack, model),
                )
            )
        for name, computed in model.model_computed_fields.items():
            leaks.extend(
                self._walk(
                    computed.return_type,
                    path=name,
                    owner=model,
                    depth=0,
                    stack=(*stack, model),
                )
            )
        cyclic = self._had_cycle.pop(model, False)
        if cyclic and stack:
            # This walk was truncated by a back-edge to an ancestor still on
            # the stack — the result is only valid in that context. Caching it
            # would let a cycle-cut subtree masquerade as the model's full
            # standalone audit (false FULL). Recompute when asked standalone.
            return leaks, cyclic
        self._model_cache[model] = (leaks, cyclic)
        return leaks, cyclic

    # -- annotation-level ---------------------------------------------------

    def _walk(
        self,
        annotation: object,
        *,
        path: str,
        owner: type[BaseModel],
        depth: int,
        stack: tuple[type[BaseModel], ...],
    ) -> list[TypeLeak]:
        ann = annotation
        origin = get_origin(ann)

        if origin is Annotated:
            return self._walk(get_args(ann)[0], path=path, owner=owner, depth=depth, stack=stack)

        if ann is Any:
            return self._leak(path, LeakRule.ANY, ann, owner, depth)
        if ann is object:
            return self._leak(path, LeakRule.OBJECT, ann, owner, depth)

        if origin in _UNION_TYPES:
            out: list[TypeLeak] = []
            for arm in get_args(ann):
                out.extend(self._walk(arm, path=path, owner=owner, depth=depth, stack=stack))
            return out

        if origin is Literal:
            return []

        # Containers -------------------------------------------------------
        if ann in (dict, list, set, frozenset, tuple):
            return self._leak(path, LeakRule.BARE_CONTAINER, ann, owner, depth)
        if origin is not None and isinstance(origin, type) and issubclass(origin, _abc.Mapping):
            key_t, val_t = (get_args(ann) + (Any, Any))[:2]
            out = self._walk(key_t, path=f"{path}[key]", owner=owner, depth=depth, stack=stack)
            out.extend(
                self._walk(val_t, path=f"{path}[value]", owner=owner, depth=depth, stack=stack)
            )
            return out
        if origin in (list, set, frozenset) or (
            origin is not None
            and isinstance(origin, type)
            and issubclass(origin, _abc.Collection)
            and origin is not tuple
        ):
            (item_t,) = get_args(ann) or (Any,)
            return self._walk(item_t, path=f"{path}[]", owner=owner, depth=depth, stack=stack)
        if origin is tuple:
            out = []
            for i, arm in enumerate(a for a in get_args(ann) if a is not Ellipsis):
                out.extend(
                    self._walk(arm, path=f"{path}[{i}]", owner=owner, depth=depth, stack=stack)
                )
            return out

        if isinstance(ann, typing.TypeVar):
            return self._leak(path, LeakRule.UNBOUND_TYPEVAR, ann, owner, depth)

        if isinstance(ann, _ALIAS_TYPES):
            if ann.__name__ in self._alias_names:
                return []
            if ann in self._alias_stack:  # recursive alias not on the allowlist
                return self._leak(path, LeakRule.UNKNOWN_TYPE, ann, owner, depth)
            self._alias_stack.add(ann)
            try:
                return self._walk(ann.__value__, path=path, owner=owner, depth=depth, stack=stack)
            finally:
                self._alias_stack.discard(ann)

        # Leaves -------------------------------------------------------------
        if isinstance(ann, type):
            if issubclass(ann, enum.Enum):
                return []
            if issubclass(ann, BaseModel):
                nested, cyclic = self._audit_model(ann, stack=stack)
                if cyclic:
                    self._had_cycle[owner] = True
                return [
                    leak.model_copy(
                        update={"path": f"{path}.{leak.path}", "depth": depth + 1 + leak.depth}
                    )
                    if leak.path != "<model>"
                    else leak.model_copy(update={"path": path, "depth": depth + 1})
                    for leak in nested
                ]
            if f"{ann.__module__}.{ann.__qualname__}" in self._scalars:
                return []
            return self._leak(path, LeakRule.UNKNOWN_TYPE, ann, owner, depth)

        # Anything else (Callable, ForwardRef that never resolved, …)
        return self._leak(path, LeakRule.UNKNOWN_TYPE, ann, owner, depth)

    def _leak(
        self, path: str, rule: LeakRule, ann: object, owner: type[BaseModel], depth: int
    ) -> list[TypeLeak]:
        if rule not in self._enabled:
            return []
        return [
            TypeLeak(
                path=path,
                rule=rule,
                annotation=_repr_annotation(ann),
                owner_model=owner.__qualname__,
                depth=depth,
            )
        ]

    # -- shared-model reference graph ----------------------------------------

    def _record_refs(
        self, model: type[BaseModel], node_type: str, *, seen: set[type[BaseModel]]
    ) -> None:
        if model in seen:
            return
        seen.add(model)
        self.model_refs.setdefault(model, set()).add(node_type)
        for field in model.model_fields.values():
            for nested in _nested_models(field.annotation):
                self._record_refs(nested, node_type, seen=seen)


def _nested_models(annotation: object) -> list[type[BaseModel]]:
    out: list[type[BaseModel]] = []
    if isinstance(annotation, type) and issubclass(annotation, BaseModel):
        return [annotation]
    for arg in get_args(annotation):
        if arg is not Ellipsis:
            out.extend(_nested_models(arg))
    return out


def _dynamic_acknowledgment(model: type[BaseModel]) -> str | None:
    """The in-code justification for a forever-dynamic model, or None.

    Only a dict ``json_schema_extra`` carrying a non-empty ``x-contract-dynamic``
    string counts — a callable is not an acknowledgment.
    """
    jse = (model.model_config or {}).get("json_schema_extra")
    if not isinstance(jse, dict):
        return None
    reason = jse.get("x-contract-dynamic")
    if isinstance(reason, str) and reason.strip():
        return reason
    return None


def _state_of(leaks: list[TypeLeak]) -> ConformanceState:
    # full / partial / non_conformant are computed from NON-acknowledged
    # leaks only; a schema whose every leak is acknowledged is DYNAMIC.
    real = [leak for leak in leaks if leak.rule is not LeakRule.ACKNOWLEDGED_DYNAMIC]
    if real:
        if any(leak.depth == 0 for leak in real):
            return ConformanceState.NON_CONFORMANT
        return ConformanceState.PARTIAL
    if leaks:
        return ConformanceState.DYNAMIC
    return ConformanceState.FULL


def _repr_annotation(ann: object) -> str:
    if isinstance(ann, type):
        return ann.__qualname__
    return repr(ann).replace("typing.", "")


_STATE_RANK = {
    ConformanceState.FULL: 0,
    ConformanceState.DYNAMIC: 1,
    ConformanceState.PARTIAL: 2,
    ConformanceState.NON_CONFORMANT: 3,
}


# ---------------------------------------------------------------------------
# Entry points
# ---------------------------------------------------------------------------


def audit_model(model: type[BaseModel], *, ruleset: Ruleset = RULESET_V3) -> SchemaReport:
    """Audit one model class in isolation."""
    return _Auditor(ruleset).audit_schema(model)


def audit_registry(
    registry: "NodeRegistry | None" = None, *, ruleset: Ruleset = RULESET_V3
) -> ContractAuditReport:
    """Audit every registered node's contracts. The single entry point for
    the admin dashboard — derived entirely from live model classes."""
    from matrx_graph.executor.registry import default_registry

    reg = registry if registry is not None else default_registry()
    auditor = _Auditor(ruleset)

    node_reports: list[NodeContractReport] = []
    for spec in sorted(reg.all_specs(), key=lambda s: s.node_type):
        inp = auditor.audit_schema(
            spec.input_schema, node_type=spec.node_type, role=SchemaRole.INPUT
        )
        out = auditor.audit_schema(spec.output_schema, node_type=spec.node_type)
        cfg = auditor.audit_schema(
            spec.config_schema, node_type=spec.node_type, role=SchemaRole.CONFIG
        )
        worst = max((inp.state, out.state, cfg.state), key=lambda s: _STATE_RANK[s])
        node_reports.append(
            NodeContractReport(
                node_type=spec.node_type,
                category=spec.category.value,
                display_name=spec.display_name,
                state=worst,
                input=inp,
                output=out,
                config=cfg,
            )
        )

    model_reports: list[ModelReport] = []
    for model, refs in sorted(auditor.model_refs.items(), key=lambda kv: kv[0].__qualname__):
        leaks, _cyclic = auditor._model_cache.get(model, ([], False))
        own = [leak for leak in leaks if leak.owner_model == model.__qualname__ and leak.depth == 0]
        model_reports.append(
            ModelReport(
                schema_name=model.__qualname__,
                module=model.__module__,
                state=_state_of(leaks),
                own_leak_count=len(own),
                referenced_by=sorted(refs),
            )
        )

    by_rule: dict[LeakRule, int] = {}
    full = dynamic = partial = non = 0
    for nr in node_reports:
        if nr.state is ConformanceState.FULL:
            full += 1
        elif nr.state is ConformanceState.DYNAMIC:
            dynamic += 1
        elif nr.state is ConformanceState.PARTIAL:
            partial += 1
        else:
            non += 1
        for sr in (nr.input, nr.output, nr.config):
            for leak in sr.leaks:
                by_rule[leak.rule] = by_rule.get(leak.rule, 0) + 1

    totals = AuditTotals(
        nodes=len(node_reports),
        full=full,
        dynamic=dynamic,
        partial=partial,
        non_conformant=non,
        percent_full=round(100.0 * full / len(node_reports), 1) if node_reports else 100.0,
        leaks_by_rule=sorted(
            (RuleCount(rule=r, count=c) for r, c in by_rule.items()),
            key=lambda rc: -rc.count,
        ),
    )
    return ContractAuditReport(
        ruleset=ruleset, totals=totals, nodes=node_reports, models=model_reports
    )
