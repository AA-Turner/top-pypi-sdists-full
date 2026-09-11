"""Version-routed UDF construction, resolved per target DataFrame.

Shape
-----
``SidecarPythonUDF`` subclasses upstream ``pyspark.sql.connect.expressions.
PythonUDF`` and overrides ONLY ``to_plan``. Upstream's ``to_plan`` is::

    expr.output_type.CopyFrom(pyspark_types_to_proto_types(output_type))
    expr.eval_type = self._eval_type
    expr.command   = CloudPickleSerializer().dumps((self._func, output_type))
    expr.python_ver = self._python_ver

Only ``command`` and ``python_ver`` are version-sensitive, so on a mismatched
connection we take those two from the sidecar and let upstream code produce
everything else. That is what makes complex return types and arrow eval types
work without special cases.

``spark.udf.register`` is the one surface that needs a special case, because it
does NOT reuse the UDF's expression. Connect's ``UDFRegistration.register``
calls ``client.register_udf(f.func, f.returnType, name, f.evalType,
f.deterministic)``, which builds a **fresh upstream** ``PythonUDF`` and stamps
``python_ver`` from the local ``sys.version_info`` -- so ``to_plan`` below is
never invoked and the registered function dies deep in the job. ``register`` is
therefore wrapped (see :func:`install_udf_register_routing`) to send the
register-function command built from a :class:`SidecarPythonUDF`.

Why override ``to_plan`` rather than decide at decoration time: ``to_plan``
receives the ``SparkConnectClient`` that is building THIS plan. That identifies
the target connection exactly, so a single UDF object routes correctly across a
notebook holding several sessions -- and a UDF that is defined but never applied
never touches a sidecar at all.

Descriptive attributes
----------------------
Every UDF this module hands back carries two read-only-by-convention attributes,
so a notebook can see the routing decision without reading logs:

``routed``
    Whether this UDF *will* be built by a sidecar rather than locally.
``python_ver``
    The ``python_ver`` string the proto will carry -- the worker's Python when
    routed, this client's when not. Known ahead of any build because the sidecar
    interpreter is CHOSEN to match the detected worker version.

They are a *prediction* until the UDF is actually applied, made by resolving the
engine that is resolvable right now (:func:`~sagemaker_studio.utils.udf.runtime.
resolve_current`) -- reading them builds nothing, spawns no sidecar and creates
no Spark session. Once a real decision has been made in
:meth:`SidecarPythonUDF.to_plan`, both are refreshed from the AUTHORITATIVE
source: the sidecar's own response. Because routing is per DataFrame, they
describe the most recent decision, so a UDF reused against a second engine at a
different version reports that second engine.
"""

from __future__ import annotations

import base64
import functools
import inspect
import logging
import weakref
from typing import Any, Callable, Dict, List, Optional, Tuple

import pyspark.sql.connect.proto as proto
from pyspark.rdd import PythonEvalType
from pyspark.sql.connect.expressions import (
    CommonInlineUserDefinedFunction,
    PythonUDF,
)
from pyspark.sql.connect.types import UnparsedDataType, pyspark_types_to_proto_types
from pyspark.sql.connect.udf import UserDefinedFunction
from pyspark.sql.types import DataType, StringType

from sagemaker_studio.utils.udf.capture import (
    CapturedFunction,
    build_request,
    capture,
    validate_freevar,
)
from sagemaker_studio.utils.udf.errors import (
    UDFRegistrationError,
    UDFUnsupportedError,
    format_sidecar_error,
)
from sagemaker_studio.utils.udf.registry import (
    client_python_version,
    get_sidecar,
    normalize_python_version,
)
from sagemaker_studio.utils.udf.runtime import resolve_current, resolve_for_client

logger = logging.getLogger("SparkConnect")

_PANDAS_EVAL_TYPES = frozenset(
    {
        PythonEvalType.SQL_SCALAR_PANDAS_UDF,
        PythonEvalType.SQL_SCALAR_PANDAS_ITER_UDF,
        PythonEvalType.SQL_GROUPED_AGG_PANDAS_UDF,
    }
)


def _capability_for(eval_type: int) -> str:
    """Metric dimension: which factory produced this UDF.

    Derived from the eval type rather than passed in, because upstream owns the
    eval-type choice (see ``_to_sidecar``) and the eval type is the only thing
    that still distinguishes a pandas UDF once we are inside ``to_plan``.
    """
    return "pandas_udf" if int(eval_type) in _PANDAS_EVAL_TYPES else "udf"


def _predict_route() -> Tuple[bool, str]:
    """``(routed, python_ver)`` for the engine resolvable right now.

    Best-effort and TOTAL: it must never raise and never build anything, because
    it stands behind plain attribute reads on a UDF object. Resolution goes
    through the same resolver the routing path uses, so the prediction agrees
    with what ``to_plan`` will decide on that engine -- but a still-lazy session
    is invisible to the resolver (see
    :func:`~sagemaker_studio.utils.udf.runtime.resolve_current`), so this cannot
    be what creates a Spark session.

    ``routed`` is only ``True`` when a sidecar is actually REGISTERED for the
    detected worker version: with none registered the UDF cannot be routed at
    all, it raises at build time, so claiming it "will route" would be a lie. A
    seen-but-unparsable mismatch is reported as not routed for the same reason.
    """
    client_version = client_python_version()
    try:
        runtime = resolve_current()
        if runtime is None or runtime.is_mismatched_unknown or runtime.matches_client():
            return False, client_version
        if get_sidecar(runtime.python_version) is None:
            return False, client_version
        return True, runtime.python_version
    except Exception as e:  # an attribute read must never raise
        logger.debug("could not predict the UDF route: %s", e)
        return False, client_version


def _stamp_route(target: Any, is_routed: bool, python_ver: str) -> None:
    """Write the descriptive attributes onto a UDF object, best-effort."""
    try:
        target.routed = bool(is_routed)
        target.python_ver = python_ver
    except Exception as e:  # e.g. a callable with no writable __dict__
        logger.debug("could not stamp route attributes on %r: %s", target, e)


def _same_minor(left: str, right: str) -> bool:
    try:
        return normalize_python_version(left) == normalize_python_version(right)
    except ValueError:
        return str(left) == str(right)


class SidecarPythonUDF(PythonUDF):
    """A ``PythonUDF`` whose command is built by a worker-matched sidecar."""

    def __init__(
        self,
        output_type: Any,
        eval_type: int,
        func: Callable[..., Any],
        python_ver: str,
        *,
        captured: Optional[CapturedFunction] = None,
        imports: Optional[List[str]] = None,
        wrapper_ref: Optional[Callable[[], Any]] = None,
    ) -> None:
        super().__init__(
            output_type=output_type, eval_type=eval_type, func=func, python_ver=python_ver
        )
        self._captured = captured
        self._imports = list(imports or [])
        # A WEAK reference to the function object the caller holds, so `to_plan`
        # can refresh its `routed` / `python_ver` from the real decision. Weak
        # because the wrapper already points here (`_unwrapped` -> the
        # SidecarUserDefinedFunction -> this expression), and a strong link back
        # would make the pair a cycle only the collector could break.
        self._wrapper_ref = wrapper_ref
        # Cache the sidecar result per (worker python, engine spark) so applying
        # one UDF to many DataFrames on the same engine builds once.
        self._command_cache: Dict[tuple, tuple] = {}
        # Engines whose route decision has already been reported. A set rather
        # than a bool, so a UDF reused against a second engine still reports it.
        self._decisions_recorded: set = set()

    def _resolved_output_type(self, session: Any) -> DataType:
        """Mirror upstream: resolve a string return type via the server."""
        if isinstance(self._output_type, UnparsedDataType):
            parsed = session._analyze(
                method="ddl_parse", ddl_string=self._output_type.data_type_string
            ).parsed
            assert isinstance(parsed, DataType)
            return parsed
        return self._output_type

    def _captured_function(self) -> CapturedFunction:
        if self._captured is None:
            self._captured = capture(self._func, imports=self._imports)
        return self._captured

    def _sidecar_command(self, runtime, output_type: DataType) -> tuple:
        """Return ``(command_bytes, python_ver)`` from the matching sidecar."""
        if runtime.is_mismatched_unknown:
            # We saw the engine's own PYTHON_VERSION_MISMATCH but could not read
            # which Python its workers run, so we cannot choose a sidecar. Raise
            # HERE, at build time, with something the user can act on -- never
            # fall through to the local build, which is what "matched" would mean
            # and which would surface the raw mismatch at `.show()` after all.
            raise UDFRegistrationError(
                "this connection's Spark workers reported a Python version mismatch with "
                f"this kernel (Python {client_python_version()}), but the worker's own "
                f"version could not be determined (detected via {runtime.source}: "
                f"{runtime.detail}). Python UDFs cannot be routed without knowing which "
                "worker Python to build for. Set the worker version explicitly with "
                "sagemaker_studio.utils.udf.runtime.set_override(spark, '<major.minor>'), or "
                "use DataFrame/SQL expressions and Java/Scala UDFs on this connection."
            )

        cache_key = (runtime.python_version, runtime.spark_version, output_type.json())
        cached = self._command_cache.get(cache_key)
        if cached is not None:
            return cached

        entry = get_sidecar(runtime.python_version)
        if entry is None:
            raise UDFRegistrationError(
                f"this connection's Spark workers run Python {runtime.python_version} "
                f"(detected via {runtime.source}) but this client is Python "
                f"{client_python_version()}, and no UDF sidecar is registered for "
                f"{runtime.python_version}. Python UDFs cannot run on this engine until one "
                "is. If you are running outside a DataNotebook kernel, register one with "
                "sagemaker_studio.utils.udf.register_sidecar()."
            )

        capability = _capability_for(self._eval_type)
        if not entry.supports(capability):
            # `capabilities` used to be logged at registration and then never
            # consulted, so a sidecar advertising only ["udf"] still got
            # pandas_udf requests and failed somewhere inside its own build. A
            # declared capability has to mean something or not exist; this is the
            # one place that can check it, and it fails at build time with the
            # capability named.
            raise UDFUnsupportedError(
                f"the UDF sidecar registered for Python {runtime.python_version} declares "
                f"capabilities {sorted(entry.capabilities)} and cannot build a "
                f"{capability!r}. Use one of the capabilities it does support on this "
                "connection, or register a sidecar that advertises this one."
            )

        captured = self._captured_function()
        request = build_request(
            captured,
            return_type_json=output_type.json(),
            eval_type=int(self._eval_type),
        )
        logger.info(
            "routing UDF %r to the Python %s / Spark %s sidecar (eval_type=%s)",
            captured.name,
            runtime.python_version,
            runtime.spark_version,
            self._eval_type,
        )
        response = entry.builder(runtime.spark_version).build(request)
        if not response.get("ok"):
            raise format_sidecar_error(response)

        result = (base64.b64decode(response["command_b64"]), response["python_ver"])
        self._command_cache[cache_key] = result
        return result

    def _record_route_on_wrapper(self, is_routed: bool, python_ver: str) -> None:
        """Refresh the caller's UDF object with the decision actually made.

        The attributes are set once at definition time from a prediction; this is
        what makes a later read report what HAPPENED instead. Silent when the
        wrapper is gone -- nobody can read it any more.
        """
        wrapper = self._wrapper_ref() if self._wrapper_ref is not None else None
        if wrapper is None:
            return
        _stamp_route(wrapper, is_routed, python_ver)

    def to_plan(self, session: Any) -> "proto.PythonUDF":
        """Build the proto for THIS target client.

        ``session`` is a ``SparkConnectClient`` (see upstream's own annotation).
        """
        from sagemaker_studio.utils.udf.metrics import (
            record_route_decision,
            record_sidecar_failure,
        )

        runtime = resolve_for_client(session)
        capability = _capability_for(self._eval_type)
        # Key the "already recorded" bookkeeping by ENGINE, not by UDF object. A
        # single bool would mean the first engine a UDF touches is the only one
        # ever reported -- so a UDF reused against a second engine would emit no
        # metric at all, and a DetectionSource regression on that engine would be
        # invisible. That is the exact failure this metric exists to catch.
        decision_key = (runtime.python_version, runtime.spark_version)

        if runtime.matches_client():
            if decision_key not in self._decisions_recorded:
                self._decisions_recorded.add(decision_key)
                record_route_decision(
                    capability=capability,
                    worker_python=runtime.python_version,
                    client_python=client_python_version(),
                    spark_version=runtime.spark_version,
                    source=runtime.source,
                    routed=False,
                )
            self._record_route_on_wrapper(False, self._python_ver)
            return super().to_plan(session)

        output_type = self._resolved_output_type(session)
        try:
            command, python_ver = self._sidecar_command(runtime, output_type)
        except Exception as e:
            record_sidecar_failure(
                capability=capability,
                worker_python=runtime.python_version,
                spark_version=runtime.spark_version,
                error_class=type(e).__name__,
            )
            raise
        if decision_key not in self._decisions_recorded:
            self._decisions_recorded.add(decision_key)
            record_route_decision(
                capability=capability,
                worker_python=runtime.python_version,
                client_python=client_python_version(),
                spark_version=runtime.spark_version,
                source=runtime.source,
                routed=True,
            )

        if not _same_minor(python_ver, runtime.python_version):
            # The sidecar's stamp is what the proto carries, and it is the one
            # that has to satisfy the worker's own `check_python_version` -- so it
            # wins. But it disagreeing with the version we ROUTED FOR means the
            # sidecar registered for a version is not running that version, which
            # is exactly the fidelity bug this whole path exists to prevent.
            # Overwriting the prediction without a trace would hide it.
            logger.warning(
                "the UDF sidecar for Python %s reported python_ver %r, which disagrees with "
                "the worker runtime resolved for this connection (%r, via %s). Using the "
                "sidecar's value, because it is the interpreter that actually built the "
                "command -- but the sidecar registered for %s does not appear to be running "
                "it.",
                runtime.python_version,
                python_ver,
                runtime.python_version,
                runtime.source,
                runtime.python_version,
            )
        self._record_route_on_wrapper(True, python_ver)

        expr = proto.PythonUDF()
        expr.output_type.CopyFrom(pyspark_types_to_proto_types(output_type))
        expr.eval_type = self._eval_type
        expr.command = command
        expr.python_ver = python_ver
        return expr

    def __repr__(self) -> str:
        return f"SidecarPythonUDF({self._output_type}, {self._eval_type}, {self._func})"


class SidecarUserDefinedFunction(UserDefinedFunction):
    """``UserDefinedFunction`` that emits a :class:`SidecarPythonUDF`."""

    def __init__(self, *args: Any, imports: Optional[List[str]] = None, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self._imports = list(imports or [])
        self._python_udf: Optional[SidecarPythonUDF] = None
        self._wrapper_ref: Optional[Callable[[], Any]] = None
        self._validate_captures_eagerly()

    def _validate_captures_eagerly(self) -> None:
        """Refuse an un-shippable closure NOW, at UDF definition time.

        The plan's binding constraint is fail-fast *at registration*: a UDF that
        captures a live session, a nested closure, or an unpicklable object must
        raise here, not confusingly later at ``.show()``. But source capture is
        deliberately lazy -- it happens in ``to_plan``, so a UDF that is defined
        and never applied costs nothing. Freevar validation needs no source text,
        so it is hoisted to definition time and only source extraction stays
        lazy. That split is what makes the constraint true without paying
        ``inspect.getsource`` for UDFs nobody uses.

        Deliberately does NOT reject a function whose closure cannot be
        inspected at all: that is not evidence of an un-shippable capture, and
        ``capture()`` will produce a precise error later if the source is
        genuinely unusable.

        It DOES reject the two shapes we can prove now will never yield source
        text -- see :meth:`_reject_uncapturable_callable`.
        """
        self._reject_uncapturable_callable()
        try:
            nonlocals = inspect.getclosurevars(self.func).nonlocals
        except (TypeError, ValueError) as e:
            logger.debug("could not inspect closure vars for eager validation: %s", e)
            return
        for name, value in nonlocals.items():
            validate_freevar(name, value)

    def _reject_uncapturable_callable(self) -> None:
        """Refuse, NOW, the callables we can already prove have no source text.

        The routed path rebuilds a UDF from source, so a callable with no
        readable source can never be shipped. Two shapes are decidable at
        definition time without reading any source -- which keeps source capture
        itself lazy -- and both previously sailed through eager validation and
        failed at ``.show()``:

          * a ``functools.partial``, which has no source of its own, ever;
          * a function compiled from a string with no ``linecache`` entry, i.e.
            defined by a bare ``exec``/``compile`` or typed into a plain
            interactive interpreter. ``inspect.getsourcefile`` returns ``None``
            for exactly that case, and returns a filename for a notebook cell or
            a ``linecache``-registered synthetic file, which ARE readable.

        This is deliberately bounded. A callable INSTANCE (a class with
        ``__call__``) is still accepted here -- see
        :meth:`_validate_captures_eagerly` -- because ``capture()`` can often
        read its class source, and rejecting it eagerly would refuse working
        UDFs. The residual gap is documented in the package README's unsupported
        list rather than guessed at.
        """
        func = self.func
        if isinstance(func, functools.partial):
            raise UDFRegistrationError(
                "this UDF is a `functools.partial`, which has no source text of its own, so "
                "it cannot be rebuilt by the version-matched UDF sidecar. Define a plain "
                "function that closes over (or takes) the bound arguments and register that."
            )
        if inspect.isfunction(func) and inspect.getsourcefile(func) is None:
            raise UDFRegistrationError(
                f"the source of {getattr(func, '__name__', 'this UDF')!r} cannot be read: it "
                "was compiled from a string with no source on record (a bare `exec`, or a "
                "plain interactive interpreter). The version-routed UDF path rebuilds the "
                "function from its source, so define it in a notebook cell or a module file "
                "instead."
            )

    def _wrapped(self) -> Any:
        """Upstream's wrapper function, carrying the route attributes.

        Overridden here rather than at each call site so that EVERY wrapper this
        object produces carries them -- including the fresh one
        ``asNondeterministic()`` builds, and the one
        ``spark.udf.register(name, plain_function)`` returns.
        """
        wrapper = super()._wrapped()
        self._track_wrapper(wrapper)
        return wrapper

    def _track_wrapper(self, wrapper: Any) -> None:
        """Stamp the predicted route on ``wrapper`` and remember it for refresh.

        Also used for a wrapper this object did not create: ``spark.udf.register``
        re-routes an already-built UDF and returns the caller's own object (see
        :func:`_sidecar_udf_of`), which must still end up describing the decision.
        """
        _stamp_route(wrapper, *_predict_route())
        try:
            ref: Optional[Callable[[], Any]] = weakref.ref(wrapper)
        except TypeError:  # not weak-referenceable: keep the prediction, skip refresh
            logger.debug("UDF wrapper %r is not weak-referenceable", type(wrapper))
            return
        self._wrapper_ref = ref
        if self._python_udf is not None:
            self._python_udf._wrapper_ref = ref

    def _python_udf_expression(self) -> SidecarPythonUDF:
        # One expression object per UDF, so its command cache is shared across
        # every application of this UDF.
        if self._python_udf is None:
            self._python_udf = SidecarPythonUDF(
                output_type=self.returnType,
                eval_type=self.evalType,
                func=self.func,
                python_ver=client_python_version(),
                imports=self._imports,
                wrapper_ref=self._wrapper_ref,
            )
        return self._python_udf

    def _build_common_inline_user_defined_function(
        self, *cols: Any
    ) -> CommonInlineUserDefinedFunction:
        from pyspark.sql.connect.column import Column
        from pyspark.sql.connect.expressions import ColumnReference

        arg_exprs = [
            col._expr if isinstance(col, Column) else Column(ColumnReference(col))._expr
            for col in cols
        ]
        return CommonInlineUserDefinedFunction(
            function_name=self._name,
            function=self._python_udf_expression(),
            deterministic=self.deterministic,
            arguments=arg_exprs,
        )


def _to_sidecar(wrapped: Any, imports: Optional[List[str]]) -> Any:
    """Rebuild an upstream-wrapped UDF as a routed one.

    Deliberately reuses upstream's own argument parsing, return-type coercion,
    and -- importantly -- its conf-driven eval-type choice
    (``spark.sql.execution.pythonUDF.arrow.enabled`` selects
    ``SQL_ARROW_BATCHED_UDF``). We only swap the object that builds the proto.
    """
    udf_obj = SidecarUserDefinedFunction(
        wrapped.func,
        returnType=wrapped.returnType,
        name=wrapped.__name__,
        evalType=wrapped.evalType,
        deterministic=wrapped.deterministic,
        imports=imports,
    )
    return udf_obj._wrapped()


def _route(upstream_result: Any, imports: Optional[List[str]]) -> Any:
    """Convert either an upstream UDF or an upstream decorator into a routed one."""
    if hasattr(upstream_result, "func") and hasattr(upstream_result, "evalType"):
        return _to_sidecar(upstream_result, imports)

    # Decorator form: upstream returned something that takes the function.
    @functools.wraps(upstream_result)
    def decorator(func: Callable[..., Any]) -> Any:
        return _to_sidecar(upstream_result(func), imports)

    return decorator


def udf(
    f: Any = None,
    returnType: Any = StringType(),  # noqa: N803 - mirrors pyspark's own name
    *,
    imports: Optional[List[str]] = None,
    **kwargs: Any,
) -> Any:
    """Version-routing drop-in for ``pyspark.sql.functions.udf``.

    ``imports`` is an SDK extension: import statements to replay inside the
    sidecar so cloudpickle captures the referenced modules by reference, exactly
    as the normal flow would. Availability at RUN time remains the worker
    environment's responsibility, unchanged by this design.

    The returned UDF (call form or decorator form) carries ``routed`` and
    ``python_ver`` describing the engine resolvable right now; see this module's
    docstring. Because routing is decided per DataFrame, they report the MOST
    RECENT decision -- a UDF applied to a Glue 5 DataFrame and then a Glue 6 one
    describes the Glue 6 build afterwards.
    """
    from pyspark.sql.connect.functions import udf as upstream_udf

    if f is None:
        return _route(upstream_udf(returnType=returnType, **kwargs), imports)
    return _route(upstream_udf(f, returnType, **kwargs), imports)


def pandas_udf(
    f: Any = None,
    returnType: Any = None,  # noqa: N803 - mirrors pyspark's own name
    functionType: Any = None,
    *,
    imports: Optional[List[str]] = None,
) -> Any:
    """Version-routing drop-in for ``pyspark.sql.functions.pandas_udf``.

    Like :func:`udf`, the result carries ``routed`` and ``python_ver`` describing
    the currently resolvable engine and, after a real application, the decision
    that was actually made.
    """
    from pyspark.sql.connect.functions import pandas_udf as upstream_pandas_udf

    if f is None:
        return _route(
            upstream_pandas_udf(returnType=returnType, functionType=functionType), imports
        )
    return _route(upstream_pandas_udf(f, returnType, functionType), imports)


udf.__name__ = "udf"
pandas_udf.__name__ = "pandas_udf"


# Eval types Connect's own ``UDFRegistration.register`` accepts. Anything else
# must reach upstream so IT raises its own INVALID_UDF_EVAL_TYPE error rather
# than us inventing a parallel one.
_REGISTRABLE_EVAL_TYPES = frozenset(
    {
        PythonEvalType.SQL_BATCHED_UDF,
        PythonEvalType.SQL_ARROW_BATCHED_UDF,
        PythonEvalType.SQL_SCALAR_PANDAS_UDF,
        PythonEvalType.SQL_SCALAR_PANDAS_ITER_UDF,
        PythonEvalType.SQL_GROUPED_AGG_PANDAS_UDF,
    }
)

_REGISTER_ORIGINALS: List[Any] = []


def _sidecar_udf_of(f: Any, name: str) -> SidecarUserDefinedFunction:
    """The :class:`SidecarUserDefinedFunction` behind an already-built UDF.

    A UDF produced by this module's ``udf`` / ``pandas_udf`` carries its
    ``SidecarUserDefinedFunction`` on ``_unwrapped`` (upstream's ``_wrapped()``
    sets that). Reusing it keeps the sidecar command cache shared with the
    DataFrame-API applications of the same UDF. An upstream-built UDF -- someone
    who imported ``pyspark.sql.functions.udf`` directly -- is rebuilt as a routed
    one from its own parts, exactly as :func:`_to_sidecar` does.
    """
    unwrapped = getattr(f, "_unwrapped", None)
    if isinstance(unwrapped, SidecarUserDefinedFunction):
        return unwrapped
    return SidecarUserDefinedFunction(
        f.func,
        returnType=f.returnType,
        name=name,
        evalType=f.evalType,
        deterministic=f.deterministic,
    )


def _register_through_sidecar(client: Any, name: str, udf_obj: SidecarUserDefinedFunction) -> None:
    """Send the register-function command with a SIDECAR-built command and stamp.

    This deliberately does NOT call ``client.register_udf``: that method's whole
    body is "build a fresh upstream ``PythonUDF`` and stamp the local Python
    version", which is the bug. It reuses everything else -- upstream's
    ``CommonInlineUserDefinedFunction.to_plan_udf`` (which calls our
    :meth:`SidecarPythonUDF.to_plan`, so ``command`` and ``python_ver`` come from
    the worker-matched sidecar and are genuinely correct, not forged) and
    upstream's own request plumbing.

    If that plumbing is not present -- a pyspark whose private surface has moved
    -- this raises :class:`UDFUnsupportedError` at REGISTRATION time naming the
    supported path, rather than registering something mis-stamped that would fail
    deep in a later job.
    """
    if not (
        hasattr(client, "_execute_plan_request_with_metadata")
        and hasattr(client, "_execute")
        and hasattr(proto.Command(), "register_function")
        and hasattr(CommonInlineUserDefinedFunction, "to_plan_udf")
    ):
        raise UDFUnsupportedError(
            "`spark.udf.register` cannot be routed on this connection (name="
            f"{name!r}): this "
            "pyspark build does not expose the request plumbing needed to register a UDF "
            "whose command is built by the version-matched sidecar, and registering it the "
            "normal way would stamp this kernel's Python version and fail late in the job "
            "with PYTHON_VERSION_MISMATCH. Use the DataFrame API instead -- define the "
            "function with `udf(...)` / `pandas_udf(...)` and apply it to a DataFrame."
        )

    plan = CommonInlineUserDefinedFunction(
        function_name=name,
        arguments=[],
        function=udf_obj._python_udf_expression(),
        deterministic=udf_obj.deterministic,
    ).to_plan_udf(client)

    request = client._execute_plan_request_with_metadata()
    request.plan.command.register_function.CopyFrom(plan)
    client._execute(request)


def _routed_register(original: Callable[..., Any]) -> Callable[..., Any]:
    @functools.wraps(original)
    def register(
        self, name: str, f: Any, returnType: Any = None
    ) -> Any:  # noqa: N803 - mirrors pyspark's own name
        from sagemaker_studio.utils.udf.runtime import client_of

        client = client_of(self.sparkSession)
        if client is None:
            registered = original(self, name, f, returnType)
            _stamp_route(registered, *_predict_route())
            return registered
        runtime = resolve_for_client(client)
        if runtime.matches_client():
            # Matched engine: upstream's local build is correct. Untouched --
            # except for describing it on the object handed back, since upstream
            # stamps this client's own version into the command it registers.
            registered = original(self, name, f, returnType)
            _stamp_route(registered, False, client_python_version())
            return registered

        is_udf_object = hasattr(f, "asNondeterministic")
        if is_udf_object and returnType is not None:
            # Upstream raises CANNOT_SPECIFY_RETURN_TYPE_FOR_UDF; let it.
            return original(self, name, f, returnType)
        if is_udf_object and int(getattr(f, "evalType", -1)) not in _REGISTRABLE_EVAL_TYPES:
            # Upstream raises INVALID_UDF_EVAL_TYPE; let it.
            return original(self, name, f, returnType)

        # Match upstream's return identity exactly: given a UDF object, upstream
        # returns THAT object (`spark.udf.register(name, u) is u`), and only the
        # plain-callable branch builds a fresh `_wrapped()`. Returning our own
        # wrapper for the first case would silently change a caller's `is` check
        # -- and lose the caller's object -- the moment the engine mismatched.
        if is_udf_object:
            udf_obj = _sidecar_udf_of(f, name)
            registered = f
            # `f` is the caller's object, not one we built, so it has to be
            # tracked explicitly to describe this registration.
            udf_obj._track_wrapper(registered)
        else:
            udf_obj = SidecarUserDefinedFunction(
                f,
                returnType=StringType() if returnType is None else returnType,
                name=name,
                evalType=PythonEvalType.SQL_BATCHED_UDF,
            )
            registered = udf_obj._wrapped()  # tracks itself

        # Registering goes through `SidecarPythonUDF.to_plan`, so this refreshes
        # `registered`'s route attributes from the sidecar's own answer.
        _register_through_sidecar(client, name, udf_obj)
        logger.info("registered UDF %r through the version-matched sidecar", name)
        return registered

    register._smus_register_routing = True  # type: ignore[attr-defined]
    return register


def install_udf_register_routing() -> bool:
    """Route ``spark.udf.register`` through the sidecar on a mismatched engine.

    Wraps ``pyspark.sql.connect.udf.UDFRegistration.register``, the one UDF entry
    point that does not go through :meth:`SidecarPythonUDF.to_plan` (see this
    module's docstring). Class-level and restorable, like the inline guard;
    resolution is still per connection, so a matched engine is untouched.

    Returns ``True`` if it wrapped something new, ``False`` on a no-op.
    """
    from pyspark.sql.connect.udf import UDFRegistration

    original = UDFRegistration.register
    if getattr(original, "_smus_register_routing", False):
        return False
    _REGISTER_ORIGINALS.append(original)
    UDFRegistration.register = _routed_register(original)
    return True


def uninstall_udf_register_routing() -> None:
    """Restore upstream ``register`` (test helper / clean shutdown)."""
    from pyspark.sql.connect.udf import UDFRegistration

    while _REGISTER_ORIGINALS:
        UDFRegistration.register = _REGISTER_ORIGINALS.pop()


def install_udf_interceptor(namespace: Dict[str, Any], spark: Any) -> Dict[str, Callable]:
    """Install version-routing ``udf`` / ``pandas_udf`` into ``namespace``.

    Notebooks register UDFs with ``from pyspark.sql.functions import udf`` and
    then call ``udf(...)`` -- not ``spark.udf(...)`` -- so the routing lives in
    the notebook namespace, shadowing those names at notebook scope ONLY. No
    pyspark module global is mutated, so the upstream import contract elsewhere
    in the process is untouched.

    ``spark.udf.register`` cannot be covered that way -- it is reached through
    the session object, not through a notebook name -- so
    :func:`install_udf_register_routing` is called from here too. Doing it here
    rather than as a separate kernel-side install keeps the two entry points that
    build a Python UDF from the client in one place, and needs no change on the
    kernel side.

    ``spark`` is registered with the runtime resolver here so a plan built from
    it can resolve its worker runtime. Routing itself is per DataFrame and does
    not depend on this argument.
    """
    from sagemaker_studio.utils.udf.runtime import register_session

    try:
        register_session(spark, getattr(spark, "_session_manager", None))
    except Exception as e:  # never block the install
        logger.debug("could not pre-register the session with the UDF resolver: %s", e)

    installed = {"udf": udf, "pandas_udf": pandas_udf}
    namespace.update(installed)
    logger.info("installed version-routing udf/pandas_udf into the user namespace")

    try:
        if install_udf_register_routing():
            logger.info("installed version-routing spark.udf.register")
    except Exception as e:  # a missing register route must not cost us the udf path
        logger.warning("could not install version-routing spark.udf.register: %s", e)
    return installed
