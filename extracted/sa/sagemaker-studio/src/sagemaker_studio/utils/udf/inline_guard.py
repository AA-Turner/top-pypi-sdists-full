"""Fail fast, and clearly, for the deferred inline-UDF family.

``mapInPandas``, ``mapInArrow``, ``applyInPandas``, ``foreach``,
``foreachBatch``, Python UDTFs and Python Data Sources build their
``UserDefinedFunction`` INTERNALLY on the DataFrame / GroupedData object, so the
routing factories never see them. On a version-mismatched engine they would fail
at execution time with a bare ``PYTHON_VERSION_MISMATCH`` -- exactly the "fails
late and confusingly" outcome the design rules out.

This installs a thin guard on the relevant Connect classes. On a MATCHED
connection it delegates straight to upstream, so nothing changes for Glue 5. On
a MISMATCHED one it raises :class:`UDFUnsupportedError` naming the method, the
versions involved, and the supported alternative.

``foreachBatch`` is listed above as part of the same deferred-build family, but
it lives on ``DataStreamWriter``, not ``DataFrame``/``GroupedData``, so it is
NOT wrapped by this module -- it is documented as unsupported (README, Task 16)
rather than guarded. A reader of this module alone should not conclude
``foreachBatch`` is covered; see :data:`INLINE_ONLY_METHODS` for what actually
is.

This is the one place we touch an upstream class, and it only ever wraps -- the
originals are kept and restorable via :func:`uninstall_inline_guard`.
"""

from __future__ import annotations

import functools
import logging
from typing import Any, Dict, List, Tuple

from sagemaker_studio.utils.udf.errors import UDFUnsupportedError
from sagemaker_studio.utils.udf.registry import client_python_version
from sagemaker_studio.utils.udf.runtime import client_of, resolve_for_client

logger = logging.getLogger("SparkConnect")

INLINE_ONLY_METHODS: Dict[str, Tuple[str, ...]] = {
    "DataFrame": ("mapInPandas", "mapInArrow", "foreach", "foreachPartition"),
    "GroupedData": ("applyInPandas", "applyInArrow", "applyInPandasWithState"),
}

_ORIGINALS: List[Tuple[Any, str, Any]] = []


def _unsupported(method_name: str, runtime) -> UDFUnsupportedError:
    if runtime.is_mismatched_unknown:
        worker = (
            "a Python version this kernel could not determine (the engine reported a "
            f"version mismatch, detected via {runtime.source})"
        )
    else:
        worker = f"Python {runtime.python_version} (detected via {runtime.source})"
    return UDFUnsupportedError(
        f"`{method_name}` is not supported on this connection. Its Spark workers run "
        f"{worker} while this kernel runs Python {client_python_version()}, and "
        f"`{method_name}` builds its Python function internally, so it cannot be routed "
        "through the version-matched UDF sidecar. Supported on this engine: scalar `udf` "
        "and `pandas_udf`, plus all DataFrame/SQL expressions and Java/Scala UDFs. "
        "Rewrite this step as a scalar `udf`/`pandas_udf`, or run it against an engine "
        "whose Python matches this kernel."
    )


def _raw_attr(obj: Any, name: str) -> Any:
    """``obj.name`` without going through ``__getattr__``, or ``None``.

    Connect's ``DataFrame.__getattr__`` resolves COLUMN names -- it evaluates
    ``self.columns``, a server round trip -- so a plain
    ``getattr(df, "_session", None)`` on a DataFrame that happens not to carry
    ``_session`` does network I/O (and on a half-built one, recurses). Both
    ``_session`` and ``_df`` are ordinary instance attributes on the real
    classes, so reading them raw is both correct and free.
    """
    try:
        return object.__getattribute__(obj, name)
    except AttributeError:
        return None


def _client_for(obj: Any) -> Any:
    """The ``SparkConnectClient`` behind a Connect ``DataFrame`` or ``GroupedData``.

    A Connect ``DataFrame`` holds its session as ``_session``; a Connect
    ``GroupedData`` does NOT -- it holds the DataFrame it was grouped from as
    ``_df`` and reaches the session through ``self._df._session`` (see
    ``pyspark/sql/connect/group.py``, which never touches ``self._session``).
    Reading only ``_session`` therefore made every grouped entry point --
    ``applyInPandas``, ``applyInArrow``, ``applyInPandasWithState`` -- silently
    fall through to upstream and fail late on the worker, which is the precise
    outcome this guard exists to prevent. Both shapes are resolved here.

    Returns ``None`` when neither shape yields a client, which the caller treats
    as "not our object, delegate".
    """
    session = _raw_attr(obj, "_session")
    if session is None:
        df = _raw_attr(obj, "_df")
        if df is not None:
            session = _raw_attr(df, "_session")
    if session is None:
        return None
    return client_of(session)


def _guard(owner: Any, method_name: str) -> bool:
    """Wrap one method. Returns True if it wrapped something new, False on a no-op."""
    original = getattr(owner, method_name, None)
    if original is None or getattr(original, "_smus_inline_guard", False):
        return False

    @functools.wraps(original)
    def guarded(self, *args, **kwargs):
        # Narrow to AttributeError deliberately. A bare `except Exception` around
        # the guard's own plumbing is what hid the GroupedData bug above: the
        # AttributeError from reading a field that does not exist was swallowed
        # and the call delegated straight to upstream, so the guard never fired
        # and the failure resurfaced late on the worker. Anything other than a
        # missing attribute is a real bug and must be visible.
        try:
            client = _client_for(self)
        except AttributeError as e:
            logger.debug("inline guard could not resolve a client for %r: %s", type(self), e)
            return original(self, *args, **kwargs)
        if client is None:
            return original(self, *args, **kwargs)
        runtime = resolve_for_client(client)
        if not runtime.matches_client():
            raise _unsupported(method_name, runtime)
        return original(self, *args, **kwargs)

    guarded._smus_inline_guard = True  # type: ignore[attr-defined]
    _ORIGINALS.append((owner, method_name, original))
    setattr(owner, method_name, guarded)
    return True


def install_inline_guard(spark: Any = None) -> None:
    """Wrap the inline-family methods on the Connect DataFrame/GroupedData classes.

    ``spark`` is accepted for symmetry with ``install_udf_interceptor`` and to
    register the session with the resolver; the guard itself is class-level and
    resolves per call.
    """
    if spark is not None:
        try:
            from sagemaker_studio.utils.udf.runtime import register_session

            register_session(spark, getattr(spark, "_session_manager", None))
        except Exception as e:
            logger.debug("could not register the session while installing the guard: %s", e)

    from pyspark.sql.connect.dataframe import DataFrame as ConnectDataFrame
    from pyspark.sql.connect.group import GroupedData as ConnectGroupedData

    wrapped_any = False
    for method_name in INLINE_ONLY_METHODS["DataFrame"]:
        wrapped_any = _guard(ConnectDataFrame, method_name) or wrapped_any
    for method_name in INLINE_ONLY_METHODS["GroupedData"]:
        wrapped_any = _guard(ConnectGroupedData, method_name) or wrapped_any
    if wrapped_any:
        logger.info("installed the inline-family UDF guard")


def uninstall_inline_guard() -> None:
    """Restore every method the guard replaced (test helper / clean shutdown)."""
    while _ORIGINALS:
        owner, method_name, original = _ORIGINALS.pop()
        setattr(owner, method_name, original)
