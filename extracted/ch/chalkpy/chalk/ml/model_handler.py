from __future__ import annotations

import importlib
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable, Optional, TypeVar

CHALK_HANDLER_ARTIFACT_PATH = "/app/artifacts"
"""Mount path inside the deployed container where chalkpy attaches the
handler-artifact volume. Single source of truth shared by the image-only
deploy path (which probes for a deterministic-named volume), the
`@model_handler`-injected `artifact_path` field, and the generated
chalk-remote-call shim."""

_MODEL_HANDLER_MARKER = "__chalk_model_handler__"
_MODEL_HANDLER_ENTRYPOINT = "__chalk_handler_entrypoint__"
"""Class attribute recording which method the deployed shim should call:
``"predict"`` (preferred) or ``"handler"`` (legacy). Read by the static shim
and by the image builder (to decide whether to provision ``chalkdf``)."""

_T = TypeVar("_T", bound=type)


def _chalk_default_load_model(self: Any) -> None:
    """Default ``load_model`` injected by :func:`model_handler`.

    Reads the resolved ``MODEL_TYPE`` from the in-container config module and
    uses ``MODEL_SERIALIZERS[model_type].load_fn`` to deserialize the artifact
    volume file into ``self.model``.

    Behavior:
      * Outside the deployed container (no ``_chalk_handler_config`` module
        on ``sys.path``), no-op — the user is testing locally and presumably
        constructed the instance with ``model=`` already set.
      * Inside the container when no model was registered (``MODEL_TYPE`` is
        ``None``), no-op.
      * Inside the container when ``self.model`` is already populated (e.g.
        a user override called ``default_load_model`` then set it again),
        no-op so we don't overwrite.
      * Otherwise, deserialize the pickle on the artifact volume into
        ``self.model``.

    Always exposed as ``self.default_load_model()`` so users who override
    ``load_model`` for custom setup can still get the default behavior:

        @model_handler
        class RFModel:
            def load_model(self):
                self.default_load_model()                  # populates self.model
                self.scaler = joblib.load(self.files["scaler.pkl"])
    """
    try:
        model_type_str = importlib.import_module("_chalk_handler_config").MODEL_TYPE
    except (ImportError, AttributeError):
        return  # running outside the deployed container — leave self.model alone
    if model_type_str is None:
        return  # no model was registered alongside this handler
    if getattr(self, "model", None) is not None:
        return  # already loaded — don't overwrite
    from chalk.client.serialization.model_serialization import MODEL_SERIALIZERS
    from chalk.ml.utils import ModelType

    model_type = ModelType(model_type_str)
    cfg = MODEL_SERIALIZERS[model_type]
    if cfg.load_fn is None:
        return
    self.model = cfg.load_fn(str(self.artifact_path / cfg.filename))


def model_handler(cls: _T) -> _T:
    """Class decorator: turn a user class into a Chalk model handler.

    The decorated class becomes a :func:`dataclasses.dataclass` with three
    injected fields and is stamped so chalkpy can recognize it at registration
    time:

    * ``model: Any = None`` — optional Python ML object. chalkpy serializes
      this via the existing ``ModelSerializer`` pipeline at registration time
      and uploads it to the artifact volume. In the deployed container, the
      default ``load_model`` deserializes the file back into ``self.model``
      so user code sees the same attribute on both sides.
    * ``files: Any = []`` — optional list of local file paths uploaded as-is to
      the artifact volume. **At runtime in the container, chalkpy rebinds this
      to a ``{basename: Path}`` mapping** so user code can do
      ``self.files["scaler.pkl"]`` and get back a ``Path`` pointing into
      ``self.artifact_path``. Construction-time it's still a list; the dict
      view only exists in the deployed container.
    * ``artifact_path: Path`` — injected by chalkpy on the in-container
      instance before ``load_model()`` runs. Points at the mounted artifact
      volume.

    The class **must** define ``predict(self, df: chalkdf.DataFrame)`` (the
    preferred entrypoint) or, for backwards compatibility, the legacy
    ``handler(self, input: pa.RecordBatch) -> pa.RecordBatch``. If both are
    defined, ``predict`` wins. From ``predict`` the return value may be any of:
    ``pa.RecordBatch``, ``pa.Table``, ``chalkdf.DataFrame``,
    ``pandas.DataFrame``, ``polars.DataFrame``, or ``numpy.ndarray`` (1D
    becomes a single ``"prediction"`` column; 2D becomes ``col_0``, ``col_1``,
    … columns).

    The Arrow ↔ chalkdf conversion and the return-type coercion live in the
    static shim (``chalk/ml/_chalk_handler_shim.py``) so the deployed runtime
    owns the wire format; the decorated class stays pure user code with just a
    ``predict`` (or legacy ``handler``) method. The shim only imports
    ``chalkdf`` when the entrypoint is ``predict``, so legacy ``handler``
    deployments take no chalkdf dependency.

    ``load_model`` is optional — if absent, chalkpy injects a default that
    deserializes ``self.model`` for the registered framework. Override
    ``load_model`` for custom setup (e.g., loading auxiliary files); call
    ``self.default_load_model()`` inside the override if you also want the
    default behavior.

    Example
    -------
    >>> import pandas as pd
    >>> from chalk.ml import model_handler
    >>>
    >>> @model_handler
    ... class RFModel:
    ...     def predict(self, df):
    ...         preds = self.model.predict(df.to_pandas())
    ...         return pd.DataFrame({"prediction": preds})
    ...
    >>> client.register_model_version(
    ...     name="rf",
    ...     model=RFModel(model=trained_rf, files=["./scaler.pkl"]),
    ... )
    """
    if not isinstance(cls, type):  # pyright: ignore[reportUnnecessaryIsInstance]
        raise TypeError(f"@model_handler must decorate a class, got {type(cls).__name__}.")
    # `predict(self, df)` is the preferred entrypoint; `handler(self, input)` is
    # still supported for backwards compatibility. Prefer `predict` when both
    # exist. The chosen entrypoint is stamped on the class so the static shim
    # and the image builder dispatch (and provision chalkdf) accordingly.
    predict_attr = cls.__dict__.get("predict") or getattr(cls, "predict", None)
    handler_attr = cls.__dict__.get("handler") or getattr(cls, "handler", None)
    if callable(predict_attr):
        entrypoint = "predict"
    elif callable(handler_attr):
        entrypoint = "handler"
    else:
        raise TypeError(
            f"@model_handler class {cls.__name__!r} must define predict(self, df) "
            + "(preferred) or the legacy handler(self, input). Neither is defined or callable."
        )

    annotations = dict(getattr(cls, "__annotations__", {}))
    for name, type_str in (
        ("model", "Any"),
        ("files", "Any"),
        ("artifact_path", "Path"),
    ):
        annotations.setdefault(name, type_str)
    cls.__annotations__ = annotations

    if "model" not in cls.__dict__:
        cls.model = None
    if "files" not in cls.__dict__:
        cls.files = field(default_factory=list)
    if "artifact_path" not in cls.__dict__:
        cls.artifact_path = field(default_factory=lambda: Path(CHALK_HANDLER_ARTIFACT_PATH))

    # Inject the default load_model when the user didn't define one. The
    # default is always exposed under `default_load_model` so an overriding
    # user can call it for "default + extras" patterns.
    if "load_model" not in cls.__dict__:
        cls.load_model = _chalk_default_load_model
    cls.default_load_model = _chalk_default_load_model

    # Inject __post_init__ that rebinds `self.files` from List[str] to
    # `Dict[str, Path]` at construction time — pointing at the user's local
    # paths — so local tests can do `instance.files["scaler.pkl"]` and
    # `instance.predict(df)` without any container plumbing. The shim
    # overwrites these values in the container with paths under
    # /app/artifacts/. Wraps any existing user __post_init__.
    user_post_init: Optional[Callable[..., None]] = cls.__dict__.get("__post_init__")
    cls.__post_init__ = _make_chalk_post_init(user_post_init)

    wrapped = dataclass(cls)
    setattr(wrapped, _MODEL_HANDLER_MARKER, True)
    setattr(wrapped, _MODEL_HANDLER_ENTRYPOINT, entrypoint)
    return wrapped


def _make_chalk_post_init(user_post_init: Optional[Callable[..., None]]) -> Callable[[Any], None]:
    def _chalk_post_init(self: Any) -> None:
        files = getattr(self, "files", None)
        if isinstance(files, list):
            raw_paths = list(files)
            self._chalk_raw_files = raw_paths
            self.files = {os.path.basename(p): Path(p) for p in raw_paths}
        else:
            # Dict already (e.g., shim rebound during cls() in container, or user
            # passed a dict directly). Leave alone; nothing to upload.
            self._chalk_raw_files = []
        if user_post_init is not None:
            user_post_init(self)

    return _chalk_post_init


def is_model_handler(obj: Any) -> bool:
    """True if `obj` is an instance (or class) wrapped with :func:`model_handler`."""
    target = obj if isinstance(obj, type) else type(obj)
    return getattr(target, _MODEL_HANDLER_MARKER, False) is True


def model_handler_entrypoint(obj: Any) -> str:
    """Return the deployed dispatch entrypoint for a decorated class/instance.

    ``"predict"`` (preferred) or ``"handler"`` (legacy). Defaults to
    ``"predict"`` for anything not stamped by :func:`model_handler`.
    """
    target = obj if isinstance(obj, type) else type(obj)
    return getattr(target, _MODEL_HANDLER_ENTRYPOINT, "predict")
