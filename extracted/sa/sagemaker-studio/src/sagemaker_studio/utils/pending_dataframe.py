"""``PendingDataFrame`` -- the Option A blocking proxy for async SQL result queuing.

When an async SQL cell returns, the SDK binds the DataFrame name in the kernel namespace
**immediately** to a ``PendingDataFrame`` instead of leaving it unbound/``None`` until the
background thread finishes. The proxy holds only ``(var_name, generation)`` and a reference
to the ``_MaterializationRegistry`` -- no data of its own. On the FIRST data access (any
attribute/dunder that reads the frame), it **blocks** on the registry's per-run completion
signal until that generation materializes, caches the real ``pandas.DataFrame``, and
forwards to it. Binding (``x = df``) never blocks; only access does.

Relationship to ``_MaterializationRegistry``: the registry is the producer / source of
truth (the background thread settles a ``(var_name, gen)`` completion Event on it); the
proxy is a thin consumer handle that waits on that signal via ``wait_until_ready`` and
reads the outcome via ``get_result``. Every proxy for the same run points back to the one
registry; the proxy never talks to the background thread directly.

Swap semantics ("swap, don't spoof"): on completion the background thread rebinds
``ip.user_ns["<name>"]`` to the *real* pandas DataFrame (via ``registry.commit``), so
``type(df)`` / ``isinstance(df, pd.DataFrame)`` become genuinely correct afterward. A
reference captured while pending (``x = df``) still works because the proxy self-resolves
on access and delegates. This is a composition proxy -- it does NOT subclass
``pandas.DataFrame`` (subclassing would run pandas' ``__init__`` over data it does not
have and defeat the "not yet a frame" contract).

DuckDB caveat: DuckDB's ``python_scan_all_frames`` replacement scan inspects namespace
objects **by type in the C++ engine**, bypassing ``__getattr__``, so it never triggers the
proxy's blocking. The DuckDB entry point therefore pre-resolves referenced proxies (via
``con.get_table_names`` + ``isinstance`` + ``_resolve``) before handing the statement to
DuckDB. See ``sqlutils._resolve_pending_for_duckdb``.
"""

import logging
import os
import weakref
from typing import Any, Optional

logger = logging.getLogger(__name__)

# Default STALL window (seconds): the maximum time a first access may block on a pending
# materialization WITHOUT PROGRESS before giving up. This is NOT a total-duration cap. The
# wait (registry.wait_until_ready) resets its patience every time the background thread
# writes a page (note_progress), so a healthy-but-large result -- which legitimately takes
# many minutes to rebuffer every row + one S3 PUT per 10k-row page -- is waited on for as
# long as it keeps advancing. Only a genuinely HUNG run (query/network wedged, thread dead)
# with no page written for this window times out. An earlier fixed 300s TOTAL cap was wrong:
# it was justified against the Redshift statement timeout, but that bounds QUERY EXECUTION,
# which finishes before materialization even starts -- so it false-failed healthy large
# results. 300s of NO PROGRESS is generous (a live run writes pages far more often), while
# still bounding a true hang. Introspection probes (see the _PROBE_ATTR fast-path in
# __getattr__) never reach this wait, so an idle-kernel tab-complete cannot hit it. A
# timeout raises TimeoutError from the access site (surfaced to the cell like any error).
# Env-overridable (SAGEMAKER_STUDIO_ASYNC_STALL_TIMEOUT_SECONDS) as an ops escape hatch --
# not a user- or UI-facing setting.
_STALL_TIMEOUT_ENV_VAR = "SAGEMAKER_STUDIO_ASYNC_STALL_TIMEOUT_SECONDS"
_DEFAULT_STALL_TIMEOUT_SECONDS = 300.0


def _parse_stall_timeout_seconds() -> float:
    """Read the stall timeout from the environment, falling back to the default on a
    missing or non-numeric value."""
    try:
        return float(os.environ.get(_STALL_TIMEOUT_ENV_VAR, str(_DEFAULT_STALL_TIMEOUT_SECONDS)))
    except (TypeError, ValueError):
        return _DEFAULT_STALL_TIMEOUT_SECONDS


DEFAULT_STALL_TIMEOUT_SECONDS: Optional[float] = _parse_stall_timeout_seconds()

# Names that IPython / Jupyter / library duck-typing probe on ANY object, often while the
# kernel is idle (tab-complete, the variable inspector, ``?df``, rich-display negotiation).
# Routing these through _resolve() would BLOCK the idle kernel for up to the resolve timeout
# with no cell running -- a silent freeze. We fast-fail them with AttributeError instead of
# resolving. NOTE: a real pandas DataFrame DOES define some of these (verified: _repr_html_,
# _repr_latex_, _repr_data_resource_, _repr_fits_horizontal_/_vertical_), so fast-failing
# them means a STILL-PENDING proxy renders as plain text rather than rich HTML/LaTeX for the
# brief pending window. That is a deliberate display-only tradeoff: avoiding an idle-kernel
# freeze is worth losing rich display until the background thread swaps in the real frame
# (after which the real _repr_* methods on the class handle rendering normally). We match an
# EXACT set of display/introspection hook names (no ``_repr_`` prefix rule -- a blanket
# prefix over-reaches and reads as if a real DataFrame lacks these, which is false; the set
# below is exhaustive for the display-negotiation hooks Jupyter probes) plus the
# ``_ipython_`` prefix. _repr_html_ and _repr_mimebundle_ are NOT in the set: they are
# RESOLVING methods defined on this class (block-then-delegate so typing ``df`` shows the
# real frame), so __getattr__ never sees them and they must not be listed as fast-fail names.
_PROBE_ATTR_NAMES = frozenset(
    {
        "_ipython_canary_method_should_not_exist_",
        "_ipython_display_",
        "__wrapped__",
        "getdoc",
        "__custom_documentations__",
        # Rich-display negotiation hooks Jupyter probes on an idle kernel. Some exist on a
        # real DataFrame (_repr_latex_, _repr_data_resource_, _repr_fits_horizontal_/
        # _vertical_) and some do not (_repr_json_, _repr_markdown_, _repr_pretty_, ...);
        # while pending we fast-fail ALL of them by name so display negotiation never blocks
        # the idle kernel. NOT listed here: _repr_html_ and _repr_mimebundle_, which are
        # RESOLVING methods defined on this class (they block-then-delegate so typing `df`
        # shows the real frame) -- __getattr__ never sees them, so listing them would be dead.
        "_repr_json_",
        "_repr_latex_",
        "_repr_markdown_",
        "_repr_javascript_",
        "_repr_pdf_",
        "_repr_jpeg_",
        "_repr_png_",
        "_repr_svg_",
        "_repr_pretty_",
        "_repr_data_resource_",
        "_repr_fits_horizontal_",
        "_repr_fits_vertical_",
    }
)


def _is_probe_attr(name: str) -> bool:
    """True for introspection/rich-display probe names that must NOT trigger resolution.
    A pending proxy answers these like a ready frame would (AttributeError -> hasattr False)
    instead of blocking the idle kernel on materialization."""
    return name in _PROBE_ATTR_NAMES or name.startswith("_ipython_")


class PendingDataFrame:
    """A namespace-bound handle to an async DataFrame still materializing.

    First data access blocks until the run completes, then transparently delegates to the
    real ``pandas.DataFrame``. See module docstring for the full contract.
    """

    # All real state lives under these names; every OTHER attribute access is treated as a
    # data access and routed through _resolve(). Keep this list in sync with __init__.
    # "__weakref__" is REQUIRED so weakref.finalize can register a GC callback that releases
    # the registry consumer even when the proxy is never resolved (the normal success path:
    # commit rebinds the namespace to the real frame and the proxy is dropped untouched).
    __slots__ = (
        "_var_name",
        "_generation",
        "_registry",
        "_timeout",
        "_real",
        "_terminal_error",
        "_finalizer",
        "__weakref__",
    )

    def __init__(
        self,
        var_name: str,
        generation: int,
        registry: Any,
        timeout: Optional[float] = DEFAULT_STALL_TIMEOUT_SECONDS,
    ) -> None:
        # Use object.__setattr__ so setting internal state does not route through
        # __setattr__ (which forwards to the resolved frame).
        object.__setattr__(self, "_var_name", var_name)
        object.__setattr__(self, "_generation", generation)
        object.__setattr__(self, "_registry", registry)
        object.__setattr__(self, "_timeout", timeout)
        object.__setattr__(self, "_real", None)
        object.__setattr__(self, "_terminal_error", None)
        object.__setattr__(self, "_finalizer", None)
        # Register as a live consumer of this run's result so the registry can drop the
        # retained frame once every proxy bound to it has resolved (see _resolve /
        # registry.release_consumer). Best-effort: a registry without the method (older
        # code / a test double) is tolerated.
        retain = getattr(registry, "retain", None)
        if retain is not None:
            retain(var_name, generation)
            # Release-on-GC backstop: the normal success path never calls _resolve() (the
            # background thread commits the real frame into the namespace and this proxy is
            # dropped untouched), so release_consumer would never run and reap would keep
            # the full frame for the kernel's life. finalize fires release_consumer when the
            # proxy is garbage-collected regardless of whether it was ever resolved. It binds
            # the registry's bound method + plain (var_name, gen) -- NOT self -- so it does
            # not keep the proxy alive. Each proxy must release EXACTLY once: _resolve()
            # detaches this finalizer after its own release, so a proxy that resolves does
            # not also release on GC. Without the detach, a proxy would release twice
            # (resolve + GC), and with multiple proxies sharing one (var_name, gen) -- the
            # per-index df_i AND the consolidated-list element -- the shared
            # count would over-decrement and pop _result early, KeyError-ing a sibling's
            # later resolve.
            release = getattr(registry, "release_consumer", None)
            if release is not None:
                object.__setattr__(
                    self, "_finalizer", weakref.finalize(self, release, var_name, generation)
                )

    # --- Core resolution ---

    def _resolve(self) -> Any:
        """Block until this run's generation completes, cache and return the real frame.

        Idempotent: after the first resolve the cached frame is returned instantly. Raises
        ``TimeoutError`` if the wait exceeds ``_timeout``, or the background run's terminal
        error (materialization failed / superseded) for a non-success outcome.
        """
        real = object.__getattribute__(self, "_real")
        if real is not None:
            return real
        # Symmetric with the _real success cache: once a run settled non-success, its
        # terminal error is cached and re-raised on every later access, so repeated access
        # is idempotent. Without this, a second _resolve() would re-enter consume_result on
        # an already-released consumer whose slot may be gone -> a confusing KeyError (and a
        # double-decrement of the shared count) instead of the original terminal error.
        cached_error = object.__getattribute__(self, "_terminal_error")
        if cached_error is not None:
            raise cached_error
        registry = object.__getattribute__(self, "_registry")
        var_name = object.__getattribute__(self, "_var_name")
        gen = object.__getattribute__(self, "_generation")
        timeout = object.__getattribute__(self, "_timeout")

        if not registry.wait_until_ready(var_name, gen, timeout):
            raise TimeoutError(
                f"Async DataFrame '{var_name}' stalled: no materialization progress for "
                f"{timeout}s (the background run appears hung). This bounds a stuck run, "
                f"not a large one -- a result that keeps streaming pages is waited on."
            )
        # consume_result atomically reads the frame AND releases this consumer under one
        # registry lock (memory release + the concurrent-resolve race fix): two threads
        # resolving the same proxy can't have one drop _result between the other's read and
        # release. It raises the recorded terminal error for a failed/superseded run -- and
        # releases the consumer BEFORE raising, so the finalizer must be detached on the
        # error path too (hence try/finally): this proxy has released exactly once here and
        # must not release again on GC. A double-release would over-decrement the shared
        # (var_name, gen) count and pop _result early, breaking a sibling proxy's resolve
        # (the per-index proxy and the consolidated-list element share one key). The detach
        # is scoped to AFTER wait_until_ready succeeds: a wait TIMEOUT above released
        # nothing, so its proxy keeps the finalizer armed to release on GC.
        try:
            try:
                consume = getattr(registry, "consume_result", None)
                if consume is not None:
                    real = consume(var_name, gen)
                else:
                    # Back-compat for a registry without consume_result (older code / test
                    # double): fall back to the two-call form.
                    real = registry.get_result(var_name, gen)
                    release = getattr(registry, "release_consumer", None)
                    if release is not None:
                        release(var_name, gen)
            except BaseException as exc:
                # The run settled non-success (failed / superseded). consume_result already
                # released this consumer before raising, so cache the error and re-raise it
                # on every later access instead of re-entering consume_result (which could
                # then KeyError on an already-dropped slot and double-decrement the count).
                object.__setattr__(self, "_terminal_error", exc)
                raise
        finally:
            finalizer = object.__getattribute__(self, "_finalizer")
            if finalizer is not None:
                finalizer.detach()
        # A settled run always hands over a real frame; None would mean a mis-settled
        # cancel/superseded run leaked through as a success. Guard so we never cache None
        # (which would make every later access re-wait and re-release, driving the consumer
        # count negative). Treat it as a failed materialization.
        if real is None:
            from sagemaker_studio.utils.sqlutils_async import _AsyncMaterializationFailed

            err = _AsyncMaterializationFailed(var_name)
            object.__setattr__(self, "_terminal_error", err)
            raise err
        object.__setattr__(self, "_real", real)
        return real

    def resolve(self) -> Any:
        """Public alias for forcing resolution (returns the real DataFrame). Useful for a
        caller that wants to convert a proxy to a concrete frame explicitly (e.g. the
        DuckDB pre-resolve pass)."""
        return self._resolve()

    @property
    def is_resolved(self) -> bool:
        """True if the real frame is already cached (no access will block)."""
        return object.__getattribute__(self, "_real") is not None

    # --- Transparent forwarding ---

    def __getattr__(self, name: str) -> Any:
        # __getattr__ is only called when normal lookup fails; since real data attributes
        # (.head, .shape, .columns, ...) are not on the proxy, they all land here and
        # trigger resolution + delegation.
        #
        # Fast-fail introspection/rich-display probes WITHOUT resolving: IPython, the
        # variable inspector and library duck-typing hit names like
        # _ipython_canary_method_should_not_exist_, _repr_json_, getdoc, __wrapped__ on an
        # idle kernel. Resolving on those would block the kernel for up to the resolve
        # timeout with no cell running. A ready DataFrame lacks these too, so raising
        # AttributeError here is faithful (hasattr() -> False, same as a real frame).
        if _is_probe_attr(name):
            raise AttributeError(name)
        return getattr(self._resolve(), name)

    def __setattr__(self, name: str, value: Any) -> None:
        # Internal slots are set via object.__setattr__ in __init__; any other attribute
        # set is a mutation of the underlying frame.
        if name in PendingDataFrame.__slots__:
            object.__setattr__(self, name, value)
        else:
            setattr(self._resolve(), name, value)

    # --- "Use" dunders: Python does NOT route implicit dunder calls through __getattr__
    # for new-style classes (it looks them up on the type), so each data-access dunder we
    # want to be transparent must be defined explicitly to force resolution. ---

    def __repr__(self) -> str:
        return repr(self._resolve())

    def __str__(self) -> str:
        return str(self._resolve())

    def __len__(self) -> int:
        return len(self._resolve())

    def __iter__(self):
        return iter(self._resolve())

    def __getitem__(self, key: Any) -> Any:
        return self._resolve()[key]

    def __setitem__(self, key: Any, value: Any) -> None:
        self._resolve()[key] = value

    def __contains__(self, item: Any) -> bool:
        return item in self._resolve()

    def __eq__(self, other: Any) -> Any:
        return self._resolve() == other

    def __ne__(self, other: Any) -> Any:
        return self._resolve() != other

    def __hash__(self) -> int:  # DataFrames are unhashable; delegate (will raise like pandas)
        return hash(self._resolve())

    # Rich display in Jupyter: forcing resolution here means typing `df` in a cell blocks
    # until ready then shows the real frame (matching the "df behaves as if ready" goal).
    def _repr_html_(self) -> Any:
        real = self._resolve()
        fn = getattr(real, "_repr_html_", None)
        return fn() if fn is not None else repr(real)

    def _repr_mimebundle_(self, include=None, exclude=None) -> Any:
        real = self._resolve()
        fn = getattr(real, "_repr_mimebundle_", None)
        if fn is not None:
            return fn(include=include, exclude=exclude)
        return {"text/plain": repr(real)}

    # Pickling: resolve then pickle the real frame, so a pending proxy is never serialized.
    def __reduce__(self):
        real = self._resolve()
        return (_identity, (real,))

    # --- NumPy protocol dunders (cannot use the generic forwarding loop below) ---
    # np.asarray(df) and numpy ufuncs (np.log(df), ...) look these up on the type and
    # bypass __getattr__, like every operator. __array_ufunc__ can't be forwarded verbatim
    # because it must substitute the resolved frame for `self` inside `inputs`.

    def __array__(self, *args, **kwargs) -> Any:
        return self._resolve().__array__(*args, **kwargs)

    def __array_ufunc__(self, ufunc, method, *inputs, **kwargs) -> Any:
        real = self._resolve()
        resolved_inputs = tuple(real if x is self else x for x in inputs)
        return getattr(ufunc, method)(*resolved_inputs, **kwargs)


def _make_forward(method_name: str):
    """Build a proxy method that blocks on ``_resolve()`` then forwards ``method_name`` to
    the real frame. Used to generate the operator/dunder methods below: Python looks
    implicit dunders up on the TYPE (bypassing ``__getattr__``), so each must exist as a
    named slot on the class -- but they all share this one body. ``method_name`` is bound
    per-call (not captured by reference), so each generated method forwards its own dunder.
    """

    def _forward(self, *args, **kwargs):
        return getattr(self._resolve(), method_name)(*args, **kwargs)

    _forward.__name__ = method_name
    _forward.__qualname__ = f"PendingDataFrame.{method_name}"
    return _forward


# Every dunder a pandas.DataFrame supports that must trigger resolution while the proxy is
# still pending. __getattr__ already covers named attribute access (.head, .loc, ...); this
# list covers the implicit operator/protocol dunders it cannot. __bool__ is the important
# one: without it, ``if df:`` uses default object truthiness (always True) instead of
# raising pandas' ambiguous-truth ValueError -- a silent wrong result. The rest fail loudly
# on the proxy today; forwarding makes them block-then-delegate. (__eq__/__ne__/__len__/
# __iter__/__getitem__/__setitem__/__contains__/__hash__ are defined explicitly above.)
_FORWARDED_DUNDERS = (
    "__bool__",
    # ordering comparisons
    "__lt__",
    "__le__",
    "__gt__",
    "__ge__",
    # arithmetic (binary, reflected, in-place)
    "__add__",
    "__radd__",
    "__iadd__",
    "__sub__",
    "__rsub__",
    "__isub__",
    "__mul__",
    "__rmul__",
    "__imul__",
    "__truediv__",
    "__rtruediv__",
    "__itruediv__",
    "__floordiv__",
    "__rfloordiv__",
    "__ifloordiv__",
    "__mod__",
    "__rmod__",
    "__imod__",
    "__pow__",
    "__rpow__",
    "__ipow__",
    "__matmul__",
    "__rmatmul__",
    # bitwise (pandas boolean masks: df & mask, ~df, ...)
    "__and__",
    "__rand__",
    "__or__",
    "__ror__",
    "__xor__",
    "__rxor__",
    "__invert__",
    # unary math
    "__neg__",
    "__pos__",
    "__abs__",
    # deletion
    "__delitem__",
)

for _dunder in _FORWARDED_DUNDERS:
    setattr(PendingDataFrame, _dunder, _make_forward(_dunder))


def _identity(obj: Any) -> Any:
    """Unpickle helper: a PendingDataFrame pickles as its resolved frame (see __reduce__)."""
    return obj
