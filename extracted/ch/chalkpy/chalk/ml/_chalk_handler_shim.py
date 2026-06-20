# pyright: reportMissingImports=false
"""chalk-remote-call entrypoint for `@model_handler` classes.

This module is shipped verbatim into the deployed container by chalkpy. The
user's handler class location is read at startup from
`_chalk_handler_config.HANDLER_CLASS` — a one-line module also baked into the
image (format: `"package.module:ClassName"`).

The file deliberately has no static imports from `chalk.*`: it must run inside
a container whose only chalk dependency is `chalk-remote-call-python`. It is
not imported by chalkpy itself — chalkpy only locates its path on disk and
hands it to `chalkcompute.Image.add_local_file`.

Dispatch is backwards compatible. The preferred entrypoint is
``predict(self, df: chalkdf.DataFrame)``; the legacy
``handler(self, input: pa.RecordBatch) -> pa.RecordBatch`` is still supported.
The decorated class is stamped with ``__chalk_handler_entrypoint__`` so this
shim knows which to call. ``chalkdf`` is imported lazily inside the predict
branch only, so legacy ``handler`` deployments take no chalkdf dependency.
"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import pyarrow as pa

_CHALK_HANDLER_ARTIFACT_PATH = "/app/artifacts"
"""Mount path for the chalkfs artifact volume. Kept in sync with
`chalk.ml.model_handler.CHALK_HANDLER_ARTIFACT_PATH`."""

_ENTRYPOINT_ATTR = "__chalk_handler_entrypoint__"
"""Class attribute set by `chalk.ml.model_handler`. Kept as a literal here so
the shim stays free of `chalk.*` imports. Values: "predict" (default) or
"handler"."""

_instance: Any = None


def _resolve_handler_class() -> Any:
    handler_class_path = importlib.import_module("_chalk_handler_config").HANDLER_CLASS
    module_path, _, class_name = handler_class_path.partition(":")
    return getattr(importlib.import_module(module_path), class_name)


def _first_batch(table: pa.Table) -> pa.RecordBatch:
    batches = table.combine_chunks().to_batches()
    if not batches:
        return pa.RecordBatch.from_pylist([], schema=table.schema)
    return batches[0]


def _coerce_to_record_batch(result: Any) -> pa.RecordBatch:
    """Convert a user return value into a ``pa.RecordBatch``.

    Accepted: ``pa.RecordBatch``, ``pa.Table``, anything with a ``to_arrow()``
    method returning ``pa.Table`` (covers ``chalkdf.DataFrame`` and
    ``polars.DataFrame``), ``pandas.DataFrame``, ``numpy.ndarray``
    (1D → single ``"prediction"`` column; 2D → ``col_0``, ``col_1``, …).

    numpy and pandas imports are lazy so users who never return those types
    don't pay for them.
    """
    if isinstance(result, pa.RecordBatch):
        return result
    if isinstance(result, pa.Table):
        return _first_batch(result)
    to_arrow = getattr(result, "to_arrow", None)
    if callable(to_arrow):
        table: Any = to_arrow()
        if not isinstance(table, pa.Table):
            raise TypeError(
                f"predict() returned {type(result).__name__}, whose .to_arrow() "
                + f"yielded {type(table).__name__} (expected pyarrow.Table)."
            )
        return _first_batch(table)
    try:
        import numpy as np
    except ImportError:
        np = None  # pyright: ignore[reportAssignmentType]
    if np is not None and isinstance(result, np.ndarray):
        if result.ndim == 1:
            return pa.RecordBatch.from_arrays([pa.array(result)], names=["prediction"])
        if result.ndim == 2:
            names = [f"col_{i}" for i in range(result.shape[1])]
            arrays = [pa.array(result[:, i]) for i in range(result.shape[1])]
            return pa.RecordBatch.from_arrays(arrays, names=names)
        raise TypeError(f"predict() returned a {result.ndim}D numpy.ndarray; only 1D and 2D are supported.")
    try:
        import pandas as pd
    except ImportError:
        pd = None  # pyright: ignore[reportAssignmentType]
    if pd is not None and isinstance(result, pd.DataFrame):
        return _first_batch(pa.Table.from_pandas(result, preserve_index=False))
    raise TypeError(
        f"predict()/handler() returned unsupported type {type(result).__name__}. "
        + "Supported: pyarrow.RecordBatch, pyarrow.Table, chalkdf.DataFrame, "
        + "pandas.DataFrame, polars.DataFrame, numpy.ndarray."
    )


def _entrypoint() -> str:
    """Which method to call on the user instance: "predict" (default) or "handler"."""
    return getattr(type(_instance), _ENTRYPOINT_ATTR, "predict")


def on_startup() -> None:
    global _instance
    cls = _resolve_handler_class()
    _instance = cls()
    _instance.artifact_path = Path(_CHALK_HANDLER_ARTIFACT_PATH)
    # Rebind `files` from the construction-time list to a {basename: Path} dict
    # so user code in load_model/predict can do `self.files["scaler.pkl"]`.
    file_basenames = getattr(importlib.import_module("_chalk_handler_config"), "FILES", ())
    _instance.files = {name: _instance.artifact_path / name for name in file_basenames}
    _instance.load_model()


def handler(event: Any, context: Any) -> Any:
    rb = pa.Table.from_pydict(event).combine_chunks().to_batches()[0]
    if _entrypoint() == "handler":
        # Legacy path: hand the user a pa.RecordBatch directly. No chalkdf.
        out = _coerce_to_record_batch(_instance.handler(rb))
    else:
        # Preferred path: hand the user a chalkdf.DataFrame. chalkdf is imported
        # lazily here so legacy handler-only deployments never need it.
        from chalkdf import DataFrame as _ChalkdfDataFrame

        df = _ChalkdfDataFrame.from_arrow(rb)
        out = _coerce_to_record_batch(_instance.predict(df))
    return {name: out.column(i) for i, name in enumerate(out.schema.names)}
