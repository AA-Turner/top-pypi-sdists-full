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
"""

from __future__ import annotations

import importlib
from pathlib import Path
from typing import Any

import pyarrow as pa

_CHALK_HANDLER_ARTIFACT_PATH = "/app/artifacts"
"""Mount path for the chalkfs artifact volume. Kept in sync with
`chalk.ml.model_handler.CHALK_HANDLER_ARTIFACT_PATH`."""

_instance: Any = None


def _resolve_handler_class() -> Any:
    handler_class_path = importlib.import_module("_chalk_handler_config").HANDLER_CLASS
    module_path, _, class_name = handler_class_path.partition(":")
    return getattr(importlib.import_module(module_path), class_name)


def on_startup() -> None:
    global _instance
    cls = _resolve_handler_class()
    _instance = cls()
    _instance.artifact_path = Path(_CHALK_HANDLER_ARTIFACT_PATH)
    # Rebind `files` from the construction-time list to a {basename: Path} dict
    # so user code in load_model/handler can do `self.files["scaler.pkl"]`.
    file_basenames = getattr(importlib.import_module("_chalk_handler_config"), "FILES", ())
    _instance.files = {name: _instance.artifact_path / name for name in file_basenames}
    _instance.load_model()


def handler(event: Any, context: Any) -> Any:
    rb = pa.Table.from_pydict(event).combine_chunks().to_batches()[0]
    out = _instance.handler(rb)
    return {name: out.column(i) for i, name in enumerate(out.schema.names)}
