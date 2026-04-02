"""Typed durable execution primitives for idempotent stage functions.

Durable stages are keyed by a typed ``DurablePath`` descriptor:

    class IngestOutputs(DurableOutputs):
        DURABLE_PATH_TEMPLATE = "{recordings_dir}/{session_id}/raw"

    @durable(
        recordings_dir=FromArg("recordings_dir"),
        session_id=FromArg("session_id"),
    )
    async def ingest_session(session_id: str, recordings_dir: Path) -> IngestOutputs:
        ...

Dependencies are declared with typed ``Requires`` specs:

    @durable(d=FromArg("d"))
    async def downstream(
        d: Path,
        upstream: UpstreamOutputs = Requires(
            d=FromArg("d"),
        ),
    ) -> DownstreamOutputs:
        ...
"""

from __future__ import annotations

import ast
import asyncio
import contextvars
import functools
import glob as glob_mod
import inspect
import json
import logging
import re
import string
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, ClassVar, Generic, TypeVar, Union, cast, get_args, get_origin, get_type_hints

from pydantic import BaseModel, PrivateAttr, ValidationError, model_validator
from pydantic.fields import FieldInfo

logger = logging.getLogger(__name__)

F = TypeVar("F")
T = TypeVar("T", bound=BaseModel)


class _Unloaded:
    """Sentinel that survives deepcopy (Pydantic v2 deepcopies PrivateAttr defaults)."""

    def __deepcopy__(self, memo: dict[int, Any]) -> _Unloaded:
        return self

    def __copy__(self) -> _Unloaded:
        return self


_UNLOADED = _Unloaded()


class DurableFile(BaseModel):
    """Lazy-loaded file reference for durable output fields."""

    path: Path
    _data: Any = PrivateAttr(default=_UNLOADED)

    @model_validator(mode="before")
    @classmethod
    def _coerce(cls, v: Any) -> Any:
        if isinstance(v, cls):
            return {"path": v.path}
        if isinstance(v, (str, Path)):
            return {"path": Path(v)}
        return v

    @property
    def data(self) -> Any:
        if self._data is _UNLOADED:
            self._data = json.loads(self.path.read_text()) if self.path.suffix == ".json" else self.path.read_bytes()
        return self._data

    def exists(self) -> bool:
        return self.path.exists()

    def __fspath__(self) -> str:
        return str(self.path)

    def __str__(self) -> str:
        return str(self.path)


@dataclass(frozen=True)
class FromArg:
    """Reference or expression over decorated function bound arguments."""

    path: str


_DOTTED_ARG_PATH = re.compile(r"^[A-Za-z_]\w*(\.[A-Za-z_]\w*)*$")


class _FromArgExprValidator(ast.NodeVisitor):
    """Allow a restricted expression subset for FromArg."""

    _BIN_OPS = (ast.Add, ast.Sub, ast.Mult, ast.Div, ast.FloorDiv, ast.Mod, ast.Pow)
    _UNARY_OPS = (ast.UAdd, ast.USub)
    _BOOL_OPS = (ast.And, ast.Or)
    _CMP_OPS = (ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE, ast.In, ast.NotIn, ast.Is, ast.IsNot)

    def generic_visit(self, node: ast.AST) -> None:
        raise TypeError(f"FromArg expression contains unsupported syntax: {type(node).__name__}")

    def visit_Expression(self, node: ast.Expression) -> None:  # noqa: N802
        self.visit(node.body)

    def visit_Name(self, node: ast.Name) -> None:  # noqa: N802
        return None

    def visit_Constant(self, node: ast.Constant) -> None:  # noqa: N802
        return None

    def visit_Attribute(self, node: ast.Attribute) -> None:  # noqa: N802
        self.visit(node.value)

    def visit_Subscript(self, node: ast.Subscript) -> None:  # noqa: N802
        self.visit(node.value)
        self.visit(node.slice)

    def visit_Slice(self, node: ast.Slice) -> None:  # noqa: N802
        if node.lower is not None:
            self.visit(node.lower)
        if node.upper is not None:
            self.visit(node.upper)
        if node.step is not None:
            self.visit(node.step)

    def visit_BinOp(self, node: ast.BinOp) -> None:  # noqa: N802
        if not isinstance(node.op, self._BIN_OPS):
            raise TypeError(f"FromArg expression uses unsupported binary operator: {type(node.op).__name__}")
        self.visit(node.left)
        self.visit(node.right)

    def visit_UnaryOp(self, node: ast.UnaryOp) -> None:  # noqa: N802
        if not isinstance(node.op, self._UNARY_OPS):
            raise TypeError(f"FromArg expression uses unsupported unary operator: {type(node.op).__name__}")
        self.visit(node.operand)

    def visit_BoolOp(self, node: ast.BoolOp) -> None:  # noqa: N802
        if not isinstance(node.op, self._BOOL_OPS):
            raise TypeError(f"FromArg expression uses unsupported bool operator: {type(node.op).__name__}")
        for value in node.values:
            self.visit(value)

    def visit_Compare(self, node: ast.Compare) -> None:  # noqa: N802
        for op in node.ops:
            if not isinstance(op, self._CMP_OPS):
                raise TypeError(f"FromArg expression uses unsupported comparator: {type(op).__name__}")
        self.visit(node.left)
        for comparator in node.comparators:
            self.visit(comparator)

    def visit_IfExp(self, node: ast.IfExp) -> None:  # noqa: N802
        self.visit(node.test)
        self.visit(node.body)
        self.visit(node.orelse)

    def visit_List(self, node: ast.List) -> None:  # noqa: N802
        for elt in node.elts:
            self.visit(elt)

    def visit_Tuple(self, node: ast.Tuple) -> None:  # noqa: N802
        for elt in node.elts:
            self.visit(elt)

    def visit_Set(self, node: ast.Set) -> None:  # noqa: N802
        for elt in node.elts:
            self.visit(elt)

    def visit_Dict(self, node: ast.Dict) -> None:  # noqa: N802
        for key in node.keys:
            if key is not None:
                self.visit(key)
        for value in node.values:
            self.visit(value)

    def visit_Call(self, node: ast.Call) -> None:  # noqa: N802
        raise TypeError("FromArg expressions do not allow function calls")

    def visit_Lambda(self, node: ast.Lambda) -> None:  # noqa: N802
        raise TypeError("FromArg expressions do not allow lambda expressions")

    def visit_ListComp(self, node: ast.ListComp) -> None:  # noqa: N802
        raise TypeError("FromArg expressions do not allow comprehensions")

    def visit_SetComp(self, node: ast.SetComp) -> None:  # noqa: N802
        raise TypeError("FromArg expressions do not allow comprehensions")

    def visit_DictComp(self, node: ast.DictComp) -> None:  # noqa: N802
        raise TypeError("FromArg expressions do not allow comprehensions")

    def visit_GeneratorExp(self, node: ast.GeneratorExp) -> None:  # noqa: N802
        raise TypeError("FromArg expressions do not allow comprehensions")


def _extract_template_roots(template: str) -> tuple[str, ...]:
    roots: list[str] = []
    for _, field_name, _, _ in string.Formatter().parse(template):
        if not field_name:
            continue
        root = field_name.split(".", 1)[0].split("[", 1)[0]
        if root and root not in roots:
            roots.append(root)
    return tuple(roots)


def _resolve_arg_path(args: dict[str, Any], arg_path: str) -> Any:
    parts = arg_path.split(".")
    if not parts or not parts[0]:
        raise TypeError("FromArg path must be non-empty")
    if parts[0] not in args:
        raise TypeError(f"FromArg('{arg_path}') references unknown argument '{parts[0]}'")

    value: Any = args[parts[0]]
    for attr in parts[1:]:
        if hasattr(value, attr):
            value = getattr(value, attr)
        elif isinstance(value, dict) and attr in value:
            value = value[attr]
        else:
            raise TypeError(f"FromArg('{arg_path}') could not resolve attribute/key '{attr}'")
    return value


def _resolve_arg_expr(args: dict[str, Any], expr: str) -> Any:
    try:
        parsed = ast.parse(expr, mode="eval")
    except SyntaxError as exc:
        raise TypeError(f"FromArg('{expr}') is not a valid expression") from exc

    _FromArgExprValidator().visit(parsed)
    try:
        return eval(compile(parsed, "<FromArg>", "eval"), {"__builtins__": {}}, args)
    except NameError as exc:
        # Matches: "name 'foo' is not defined"
        msg = str(exc)
        missing = msg.split("'")[1] if "'" in msg else msg
        raise TypeError(f"FromArg('{expr}') references unknown argument '{missing}'") from exc
    except Exception as exc:  # pragma: no cover - surfaced as config error
        raise TypeError(f"FromArg('{expr}') could not be evaluated: {exc}") from exc


def _resolve_from_arg(args: dict[str, Any], path_or_expr: str) -> Any:
    if _DOTTED_ARG_PATH.fullmatch(path_or_expr):
        return _resolve_arg_path(args, path_or_expr)
    return _resolve_arg_expr(args, path_or_expr)


def _resolve_binding_map(
    *,
    required_vars: tuple[str, ...],
    bindings: dict[str, Any],
    fmt_args: dict[str, Any],
    owner: str,
    template: str,
) -> dict[str, Any]:
    resolved: dict[str, Any] = {}
    for key in required_vars:
        if key not in bindings:
            raise TypeError(f"{owner} is missing binding for '{key}' (path: {template})")
        binding = bindings[key]
        if isinstance(binding, FromArg):
            resolved[key] = _resolve_from_arg(fmt_args, binding.path)
        else:
            resolved[key] = binding
    return resolved


class DurablePath(Generic[T]):
    """Typed durable path descriptor for an output model."""

    def __init__(self, output_type: type[T], template: str):
        if not isinstance(output_type, type) or not issubclass(output_type, BaseModel):
            raise TypeError(f"DurablePath output_type must be BaseModel subclass, got {output_type!r}")
        if not template:
            raise TypeError("DurablePath template must be non-empty")
        self.output_type = output_type
        self.template = template
        self.required_vars = _extract_template_roots(template)

    def resolve(self, **vars: Any) -> Path:
        missing = [k for k in self.required_vars if k not in vars]
        if missing:
            raise TypeError(f"Missing durable path vars for {self.output_type.__name__}: {', '.join(sorted(missing))}")
        return Path(self.template.format(**vars))

    def load(self, **vars: Any) -> T | None:
        return cast(T | None, _check_typed_cache(self.output_type, self.resolve(**vars)))

    def __repr__(self) -> str:
        return f"DurablePath(output_type={self.output_type.__name__}, template={self.template!r})"


class DurableOutputs(BaseModel):
    """Optional mixin for output models that own their durable path template."""

    DURABLE_PATH_TEMPLATE: ClassVar[str] = ""

    @classmethod
    def durable_path(cls: type[T]) -> DurablePath[T]:
        template = getattr(cls, "DURABLE_PATH_TEMPLATE", "")
        if not template:
            raise NotImplementedError(f"{cls.__name__}.DURABLE_PATH_TEMPLATE is not set")
        return DurablePath(cls, template)


@dataclass(frozen=True)
class RequiresSpec(Generic[T]):
    """Typed dependency declaration for durable stages."""

    optional: bool = False
    bindings: dict[str, Any] = field(default_factory=dict)


def _infer_durable_path(output_type: type[BaseModel]) -> DurablePath[Any]:
    path_builder = getattr(output_type, "durable_path", None)
    if not callable(path_builder):
        raise TypeError(
            f"{output_type.__name__} must define durable_path() or inherit DurableOutputs "
            "to be used with inferred durable APIs"
        )
    inferred = path_builder()
    if not isinstance(inferred, DurablePath):
        raise TypeError(f"{output_type.__name__}.durable_path() must return DurablePath")
    return inferred


def Requires(*, optional: bool = False, **bindings: Any) -> Any:
    """Declare a typed dependency on another durable output."""
    return RequiresSpec(optional=optional, bindings=bindings)


class DependencyMissing(RuntimeError):
    """Raised when a required upstream dependency is not found on disk."""

    def __init__(self, param_name: str, model_cls: type, resolved_path: Path):
        self.param_name = param_name
        self.model_cls = model_cls
        self.resolved_path = resolved_path
        super().__init__(
            f"Dependency '{param_name}' ({model_cls.__name__}) not found at {resolved_path}. "
            f"Ensure the upstream stage has run first."
        )


_durable_base_path: contextvars.ContextVar[Path] = contextvars.ContextVar("_durable_base_path")


def durable_path() -> Path:
    """Get the resolved base path of the current @durable function."""
    try:
        return _durable_base_path.get()
    except LookupError:
        raise RuntimeError("durable_path() called outside of a @durable function")


def _get_field_meta(field_info: FieldInfo) -> tuple[str, str] | None:
    """Extract (kind, path_template) from a pydantic Field's json_schema_extra."""
    extra = field_info.json_schema_extra
    if not isinstance(extra, dict):
        return None
    for kind in ("json", "file", "glob"):
        if kind in extra:
            template = extra[kind]
            if isinstance(template, str):
                return kind, template
            return None
    return None


def _check_typed_cache(output_cls: type[BaseModel], base_path: Path) -> BaseModel | None:
    """Check cache for a typed output model. Returns populated model on hit, None on miss."""
    values: dict[str, Any] = {}

    for field_name, field_info in output_cls.model_fields.items():
        meta = _get_field_meta(field_info)
        if meta is None:
            continue
        kind, template = meta

        if kind == "json":
            p = base_path / template
            if not p.exists():
                return None
            try:
                raw = json.loads(p.read_text())
            except (json.JSONDecodeError, OSError):
                return None
            annotation = output_cls.model_fields[field_name].annotation
            try:
                if annotation is not None and isinstance(annotation, type) and issubclass(annotation, BaseModel):
                    values[field_name] = annotation.model_validate(raw)
                else:
                    values[field_name] = raw
            except ValidationError:
                return None

        elif kind == "file":
            p = base_path / template
            if not p.exists():
                if not field_info.is_required():
                    # Optional file field — skip, let pydantic use default
                    continue
                return None
            values[field_name] = p

        elif kind == "glob":
            matches = sorted(glob_mod.glob(str(base_path / template)))
            if not matches:
                # If the field has a default_factory, use it (e.g. empty list)
                if field_info.default_factory is not None:
                    values[field_name] = field_info.default_factory()
                else:
                    return None
            else:
                values[field_name] = [Path(m) for m in matches]

    try:
        return output_cls.model_validate(values)
    except ValidationError:
        return None


def _save_typed_outputs(model: BaseModel, base_path: Path) -> None:
    """Save json fields from a typed output model to disk."""
    base_path.mkdir(parents=True, exist_ok=True)

    for field_name, field_info in model.__class__.model_fields.items():
        meta = _get_field_meta(field_info)
        if meta is None:
            continue
        kind, template = meta
        if kind != "json":
            continue

        value = getattr(model, field_name)
        p = base_path / template
        p.parent.mkdir(parents=True, exist_ok=True)

        if isinstance(value, BaseModel):
            p.write_text(value.model_dump_json(indent=2))
        else:
            serialized = model.model_dump()[field_name]
            p.write_text(json.dumps(serialized, indent=2, default=str))


def _get_return_type(fn: Any) -> type | None:
    hints = get_type_hints(fn)
    return hints.get("return")


def _unwrap_optional(tp: Any) -> Any:
    """Unwrap Optional[X] / X | None / Union[X, None] to X."""
    import types as _types

    origin = get_origin(tp)
    if origin is Union or isinstance(tp, _types.UnionType):
        args = [a for a in get_args(tp) if a is not type(None)]
        if len(args) == 1:
            return args[0]
    return tp


def load_durable_path(path: DurablePath[T], **kwargs: Any) -> T | None:
    """Imperatively load structured outputs for a typed durable path."""
    if not isinstance(path, DurablePath):
        raise TypeError(f"load_durable_path expects DurablePath, got {type(path).__name__}")
    return path.load(**kwargs)


def load_durable(output_type: type[T], **kwargs: Any) -> T | None:
    """Imperatively load structured outputs inferred from an output type."""
    inferred = _infer_durable_path(output_type)
    if inferred.output_type is not output_type:
        raise TypeError(f"{output_type.__name__}.durable_path() returned path for {inferred.output_type.__name__}")
    return cast(T | None, inferred.load(**kwargs))


def _find_requires_params(fn: Any) -> dict[str, tuple[DurablePath[Any], RequiresSpec[Any], type[BaseModel]]]:
    """Find all parameters with Requires defaults."""
    sig = inspect.signature(fn)
    hints = get_type_hints(fn)
    deps: dict[str, tuple[DurablePath[Any], RequiresSpec[Any], type[BaseModel]]] = {}

    for name, param in sig.parameters.items():
        if isinstance(param.default, RequiresSpec):
            raw_type = hints.get(name)
            if raw_type is None:
                raise TypeError(f"Parameter '{name}' on {fn.__name__} has Requires() default but no type annotation")
            model_cls = _unwrap_optional(raw_type)
            if not (isinstance(model_cls, type) and issubclass(model_cls, BaseModel)):
                raise TypeError(
                    f"Parameter '{name}' on {fn.__name__} has Requires() default "
                    f"but annotation {model_cls} is not a BaseModel subclass"
                )
            dep_path = _infer_durable_path(model_cls)
            expected_cls = dep_path.output_type
            if model_cls is not expected_cls:
                raise TypeError(
                    f"Parameter '{name}' on {fn.__name__} expects {model_cls.__name__}, "
                    f"but Requires path is for {expected_cls.__name__}"
                )
            unknown = sorted(set(param.default.bindings) - set(dep_path.required_vars))
            if unknown:
                raise TypeError(
                    f"Requires bindings include unknown vars for {expected_cls.__name__}: {', '.join(unknown)}"
                )
            deps[name] = (dep_path, param.default, cast(type[BaseModel], model_cls))

    return deps


def _resolve_requires_vars(
    dep_path: DurablePath[Any],
    req: RequiresSpec[Any],
    fmt_args: dict[str, Any],
    param_name: str,
) -> dict[str, Any]:
    return _resolve_binding_map(
        required_vars=dep_path.required_vars,
        bindings=req.bindings,
        fmt_args=fmt_args,
        owner=f"Requires for parameter '{param_name}'",
        template=dep_path.template,
    )


def _resolve_deps(
    deps: dict[str, tuple[DurablePath[Any], RequiresSpec[Any], type[BaseModel]]],
    fmt_args: dict[str, Any],
) -> dict[str, BaseModel | None]:
    """Resolve all dependencies, returning {param_name: loaded_model_or_None}."""
    resolved: dict[str, BaseModel | None] = {}

    for param_name, (path, req, model_cls) in deps.items():
        dep_vars = _resolve_requires_vars(path, req, fmt_args, param_name)
        resolved_path = path.resolve(**dep_vars)
        loaded = _check_typed_cache(model_cls, resolved_path)

        if loaded is None and not req.optional:
            raise DependencyMissing(param_name, model_cls, resolved_path)

        resolved[param_name] = loaded

    return resolved


def _get_otel_ids() -> tuple[str | None, str | None]:
    """Extract trace_id and span_id from the current OTel context, if available."""
    try:
        from opentelemetry import trace

        span = trace.get_current_span()
        ctx = span.get_span_context()
        if ctx and ctx.is_valid:
            return format(ctx.trace_id, "032x"), format(ctx.span_id, "016x")
    except Exception:
        pass
    return None, None


def _start_otel_span(name: str) -> Any:
    """Start a new OTel span as a context manager. Returns a no-op if OTel is unavailable."""
    try:
        from opentelemetry import trace

        tracer = trace.get_tracer("plato.durable")
        return tracer.start_as_current_span(name)
    except Exception:
        import contextlib

        return contextlib.nullcontext()


async def _report_stage_started(
    stage_name: str,
    output_type: str,
    base_path: str,
    args_snapshot: dict[str, Any] | None,
    started_at: datetime,
) -> str | None:
    """Report stage started to Chronos. Returns public_id for parent tracking."""
    try:
        from plato.worlds.stage_tracking import report_stage

        trace_id, span_id = _get_otel_ids()
        return await report_stage(
            stage_name=stage_name,
            stage_type="durable",
            status="started",
            started_at=started_at,
            output_type=output_type,
            base_path=base_path,
            args_snapshot=args_snapshot,
            trace_id=trace_id,
            span_id=span_id,
        )
    except Exception:
        logger.debug("Stage tracking (started) failed for %s", stage_name, exc_info=True)
        return None


async def _report_stage_completed(
    stage_name: str, output_type: str, elapsed: float, base_path: str, started_at: datetime
) -> None:
    """Report stage completed to Chronos. Also sends Slack notification via server."""
    try:
        from plato.worlds.stage_tracking import report_stage

        await report_stage(
            stage_name=stage_name,
            stage_type="durable",
            status="completed",
            started_at=started_at,
            output_type=output_type,
            completed_at=datetime.now(timezone.utc),
            elapsed_seconds=elapsed,
            base_path=base_path,
        )
    except Exception:
        logger.debug("Stage tracking (completed) failed for %s", stage_name, exc_info=True)


async def _report_stage_failed(
    stage_name: str, output_type: str, base_path: str, started_at: datetime, error: str
) -> None:
    """Report stage failure to Chronos."""
    try:
        from plato.worlds.stage_tracking import report_stage

        await report_stage(
            stage_name=stage_name,
            stage_type="durable",
            status="failed",
            started_at=started_at,
            output_type=output_type,
            completed_at=datetime.now(timezone.utc),
            base_path=base_path,
            error_message=error[:2000],
        )
    except Exception:
        logger.debug("Stage tracking (failed) failed for %s", stage_name, exc_info=True)


def _report_stage_sync(
    stage_name: str,
    output_type: str,
    elapsed: float,
    base_path: str,
    started_at: datetime,
    trace_id: str | None = None,
    span_id: str | None = None,
) -> None:
    """Sync version of completed stage reporting."""
    try:
        from plato.worlds.stage_tracking import report_stage_sync

        report_stage_sync(
            stage_name=stage_name,
            stage_type="durable",
            status="completed",
            started_at=started_at,
            output_type=output_type,
            completed_at=datetime.now(timezone.utc),
            elapsed_seconds=elapsed,
            base_path=base_path,
            trace_id=trace_id,
            span_id=span_id,
        )
    except Exception:
        logger.debug("Stage tracking (completed sync) failed for %s", stage_name, exc_info=True)


def durable(
    fn: Any | None = None,
    *,
    validate: Any | None = None,
    **bindings: Any,
) -> Any:
    """Skip function execution if typed outputs already exist on disk.

    Usage:
      - @durable(arg=FromArg("arg"), ...)
      - @durable(validate=..., arg=FromArg("arg"))
    """

    if fn is not None and not callable(fn):
        raise TypeError("@durable does not accept a path argument. Define durable_path() on the output model.")

    def decorator(fn: Any) -> Any:
        sig = inspect.signature(fn)
        return_type = _get_return_type(fn)
        if return_type is None or not (isinstance(return_type, type) and issubclass(return_type, BaseModel)):
            raise TypeError(f"@durable requires a pydantic BaseModel return type, got {return_type} on {fn.__name__}")
        resolved_path = _infer_durable_path(return_type)
        if return_type is not resolved_path.output_type:
            raise TypeError(
                f"@durable path output type {resolved_path.output_type.__name__} does not match "
                f"function return type {return_type.__name__} on {fn.__name__}"
            )
        unknown = sorted(set(bindings) - set(resolved_path.required_vars))
        if unknown:
            raise TypeError(
                f"@durable bindings include unknown vars for {resolved_path.output_type.__name__}: {', '.join(unknown)}"
            )
        missing = sorted(set(resolved_path.required_vars) - set(bindings))
        if missing:
            raise TypeError(
                f"@durable is missing bindings for {resolved_path.output_type.__name__}: {', '.join(missing)}"
            )

        # Pre-compute which params are Requires deps
        requires_params = _find_requires_params(fn)
        # Build a signature without Requires params for binding caller args
        non_dep_params = [p for name, p in sig.parameters.items() if name not in requires_params]
        caller_sig = sig.replace(parameters=non_dep_params)

        def _fmt_args(args: tuple[Any, ...], kwargs: dict[str, Any]) -> dict[str, Any]:
            bound = caller_sig.bind(*args, **kwargs)
            bound.apply_defaults()
            return dict(bound.arguments)

        if asyncio.iscoroutinefunction(fn):

            @functools.wraps(fn)
            async def async_wrapper(*args: Any, **kwargs: Any) -> BaseModel:
                fmt = _fmt_args(args, kwargs)
                path_vars = _resolve_binding_map(
                    required_vars=resolved_path.required_vars,
                    bindings=bindings,
                    fmt_args=fmt,
                    owner=f"@durable for {fn.__name__}",
                    template=resolved_path.template,
                )
                bp = resolved_path.resolve(**path_vars)

                if validate is not None and not validate(*args, **kwargs):
                    pass
                else:
                    cached_model = _check_typed_cache(return_type, bp)
                    if cached_model is not None:
                        logger.debug("Cache hit for %s, loading typed outputs", fn.__name__)
                        return cached_model

                # Cache miss — resolve dependencies and call function
                if requires_params:
                    dep_values = _resolve_deps(requires_params, fmt)
                    kwargs.update(dep_values)

                from plato.worlds.stage_tracking import _current_stage_public_id, serialize_args

                with _start_otel_span(fn.__name__):
                    stage_started_at = datetime.now(timezone.utc)
                    stage_public_id = await _report_stage_started(
                        fn.__name__,
                        return_type.__name__,
                        str(bp),
                        serialize_args(fmt),
                        stage_started_at,
                    )
                    parent_token = _current_stage_public_id.set(stage_public_id)
                    token = _durable_base_path.set(bp)
                    t0 = time.monotonic()
                    try:
                        result = await fn(*args, **kwargs)
                    except Exception as exc:
                        _durable_base_path.reset(token)
                        _current_stage_public_id.reset(parent_token)
                        await _report_stage_failed(
                            fn.__name__,
                            return_type.__name__,
                            str(bp),
                            stage_started_at,
                            str(exc),
                        )
                        raise
                    _durable_base_path.reset(token)
                    _current_stage_public_id.reset(parent_token)
                    elapsed = time.monotonic() - t0
                    _save_typed_outputs(result, bp)
                    await _report_stage_completed(
                        fn.__name__,
                        return_type.__name__,
                        elapsed,
                        str(bp),
                        stage_started_at,
                    )
                    return result

            async_wrapper.__durable_path__ = resolved_path
            async_wrapper.__durable_return_type__ = return_type
            return async_wrapper
        else:

            @functools.wraps(fn)
            def sync_wrapper(*args: Any, **kwargs: Any) -> BaseModel:
                fmt = _fmt_args(args, kwargs)
                path_vars = _resolve_binding_map(
                    required_vars=resolved_path.required_vars,
                    bindings=bindings,
                    fmt_args=fmt,
                    owner=f"@durable for {fn.__name__}",
                    template=resolved_path.template,
                )
                bp = resolved_path.resolve(**path_vars)

                if validate is not None and not validate(*args, **kwargs):
                    pass
                else:
                    cached_model = _check_typed_cache(return_type, bp)
                    if cached_model is not None:
                        logger.debug("Cache hit for %s, loading typed outputs", fn.__name__)
                        return cached_model

                # Cache miss — resolve dependencies and call function
                if requires_params:
                    dep_values = _resolve_deps(requires_params, fmt)
                    kwargs.update(dep_values)

                from plato.worlds.stage_tracking import report_stage_sync as _report_sync
                from plato.worlds.stage_tracking import serialize_args

                with _start_otel_span(fn.__name__):
                    stage_started_at = datetime.now(timezone.utc)
                    trace_id, span_id = _get_otel_ids()
                    _report_sync(
                        stage_name=fn.__name__,
                        stage_type="durable",
                        status="started",
                        started_at=stage_started_at,
                        output_type=return_type.__name__,
                        base_path=str(bp),
                        args_snapshot=serialize_args(fmt),
                        trace_id=trace_id,
                        span_id=span_id,
                    )
                    token = _durable_base_path.set(bp)
                    t0 = time.monotonic()
                    try:
                        result = fn(*args, **kwargs)
                    except Exception as exc:
                        _durable_base_path.reset(token)
                        _report_sync(
                            stage_name=fn.__name__,
                            stage_type="durable",
                            status="failed",
                            started_at=stage_started_at,
                            output_type=return_type.__name__,
                            base_path=str(bp),
                            error_message=str(exc)[:2000],
                            trace_id=trace_id,
                            span_id=span_id,
                        )
                        raise
                    _durable_base_path.reset(token)
                    elapsed = time.monotonic() - t0
                    _save_typed_outputs(result, bp)
                    _report_stage_sync(
                        fn.__name__,
                        return_type.__name__,
                        elapsed,
                        str(bp),
                        stage_started_at,
                        trace_id=trace_id,
                        span_id=span_id,
                    )
                    return result

            sync_wrapper.__durable_path__ = resolved_path
            sync_wrapper.__durable_return_type__ = return_type
            return sync_wrapper

    if fn is None:
        return decorator
    return decorator(fn)
