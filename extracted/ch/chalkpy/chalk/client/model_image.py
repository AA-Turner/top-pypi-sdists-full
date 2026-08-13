from __future__ import annotations

import inspect
import os
import re
import sys
import tempfile
import textwrap
import types
import warnings
from dataclasses import dataclass
from typing import Any, Dict, List, Optional, Tuple

from chalk.ml.model_handler import CHALK_HANDLER_ARTIFACT_PATH
from chalk.ml.utils import ModelEncoding, ModelType, model_encoding_from_proto, model_type_from_proto
from chalk.utils._ast_extract import find_relative_imports, is_module_level_definition
from chalk.utils.collections import FrozenOrderedSet

_DEFAULT_PACKAGES: Dict[ModelType, List[str]] = {
    ModelType.PYTORCH: ["torch"],
    ModelType.SKLEARN: ["scikit-learn", "joblib"],
    ModelType.XGBOOST: ["xgboost"],
    ModelType.ONNX: ["onnxruntime"],
}


def infer_image_from_spec(spec: Any) -> Any:
    """Construct a chalkcompute.Image from a ModelArtifactSpec's model_type and dependencies."""
    try:
        from chalkcompute import Image  # pyright: ignore[reportMissingImports]
    except ImportError:
        raise ImportError("Please install `chalkcompute` to enable model image builds.")

    mt = model_type_from_proto(spec.model_type)

    image = Image.debian_slim()

    packages = list(spec.python_dependencies)
    if not packages:
        packages = _DEFAULT_PACKAGES.get(mt, [])

    if not packages:
        supported = ", ".join(t.name for t in _DEFAULT_PACKAGES)
        raise ValueError(
            f"Image inference is not supported for model type {mt.name}. "
            + f"Supported types: {supported}. "
            + f"Please register your model with an explicit model_image to deploy to a scaling group."
        )

    if "numpy" not in packages:
        packages.append("numpy")
    return image.pip_install(["chalk-remote-call-python"] + packages)


def generate_volume_name(model_name: str, model_version: int) -> str:
    import uuid

    short_id = uuid.uuid4().hex[:8]
    return f"model-{model_name}-v{model_version}-{short_id}"


def _sklearn_load_line(model_path: str) -> str:
    return f"    model = joblib.load({model_path!r})\n"


def _pytorch_load_lines(model_path: str, encoding: ModelEncoding) -> str:
    if encoding == ModelEncoding.SAFETENSOR:
        return f"    model = torch.load({model_path!r}, weights_only=True)\n" + "    model.eval()\n"
    return f"    model = torch.jit.load({model_path!r})\n" + "    model.eval()\n"


_HANDLER_TEMPLATE = (
    "def handler(event, context):\n"
    "    features = np.column_stack([col.to_numpy() for col in event.values()])\n"
    "{predict_block}"
    "    return {{'prediction': preds.tolist()}}\n"
)

_PREDICT_XGBOOST = (
    "    dmatrix = xgb.DMatrix(features, feature_names=list(event.keys()))\n" "    preds = model.predict(dmatrix)\n"
)

_PREDICT_SKLEARN = "    preds = model.predict(features)\n"

_PREDICT_PYTORCH = (
    "    tensor = torch.tensor(features, dtype=torch.float32)\n"
    "    with torch.no_grad():\n"
    "        preds = model(tensor)\n"
    "    preds = preds.numpy()\n"
)

_PREDICT_ONNX = (
    "    features = features.astype(np.float32)\n"
    "    results = session.run(None, {_input_name: features})\n"
    "    preds = np.asarray(results[0]).flatten()\n"
)


def generate_model_handler(
    model_type: ModelType,
    model_encoding: ModelEncoding,
    volume_name: str,
    model_filename: str,
) -> str:
    """Generate a handler shim that loads and serves a serialized model artifact."""
    model_path = f"/volumes/{volume_name}/{model_filename}"

    if model_type == ModelType.XGBOOST:
        source = (
            "import xgboost as xgb\n"
            "import numpy as np\n"
            "\n"
            "model = None\n"
            "\n"
            "def on_startup():\n"
            "    global model\n"
            "    model = xgb.Booster()\n"
            f"    model.load_model({model_path!r})\n"
            "\n"
        ) + _HANDLER_TEMPLATE.format(predict_block=_PREDICT_XGBOOST)
    elif model_type == ModelType.SKLEARN:
        source = (
            (
                "import joblib\n"
                "import numpy as np\n"
                "\n"
                "model = None\n"
                "\n"
                "def on_startup():\n"
                "    global model\n"
            )
            + _sklearn_load_line(model_path)
            + ("\n")
            + _HANDLER_TEMPLATE.format(predict_block=_PREDICT_SKLEARN)
        )
    elif model_type == ModelType.PYTORCH:
        source = (
            (
                "import torch\n"
                "import numpy as np\n"
                "\n"
                "model = None\n"
                "\n"
                "def on_startup():\n"
                "    global model\n"
            )
            + _pytorch_load_lines(model_path, model_encoding)
            + ("\n")
            + _HANDLER_TEMPLATE.format(predict_block=_PREDICT_PYTORCH)
        )
    elif model_type == ModelType.ONNX:
        source = (
            (
                "import onnxruntime as ort\n"
                "import numpy as np\n"
                "\n"
                "session = None\n"
                "_input_name = None\n"
                "\n"
                "def on_startup():\n"
                "    global session, _input_name\n"
            )
            + f"    session = ort.InferenceSession({model_path!r})\n"
            + "    _input_name = session.get_inputs()[0].name\n"
            + ("\n")
            + _HANDLER_TEMPLATE.format(predict_block=_PREDICT_ONNX)
        )
    else:
        raise ValueError(f"No built-in handler for model_type={model_type}. Provide a custom handler.")

    return source


def _warn_validation_skipped(import_error: ImportError) -> None:
    from rich.console import Console
    from rich.style import Style
    from rich.text import Text

    from chalk._reporting.rich.color import CITRUSY_YELLOW

    module_name = import_error.name or str(import_error)
    Console().print(
        Text(
            f"⚠ Model handler validation skipped: {module_name} not installed locally",
            style=Style(color=CITRUSY_YELLOW, bold=True),
        )
    )


def _build_dummy_event(spec: Any) -> Any:
    """Build a single-row dummy event dict from the spec's input schema.

    Returns dict[str, pa.Array] or None if the schema is unavailable or unsupported.
    """
    try:
        import pyarrow as pa

        from chalk.client.serialization.model_serialization import ModelSerializer
    except ImportError:
        return None

    try:
        schema = ModelSerializer.convert_schema_from_protobuf(spec.model_signature.inputs)
    except Exception:
        return None

    if not isinstance(schema, dict):
        return None

    event: Dict[str, Any] = {}
    for col_name, dtype in schema.items():
        if dtype is float or (isinstance(dtype, pa.DataType) and pa.types.is_floating(dtype)):
            event[col_name] = pa.array([1.0], type=pa.float64())
        elif dtype is int or (isinstance(dtype, pa.DataType) and pa.types.is_integer(dtype)):
            event[col_name] = pa.array([1], type=pa.int64())
        elif dtype is bool or (isinstance(dtype, pa.DataType) and pa.types.is_boolean(dtype)):
            event[col_name] = pa.array([True], type=pa.bool_())
        elif dtype is str or (
            isinstance(dtype, pa.DataType) and (pa.types.is_string(dtype) or pa.types.is_large_string(dtype))
        ):
            event[col_name] = pa.array(["a"], type=pa.string())
        else:
            return None

    return event if event else None


def validate_model_handler(
    model_type: ModelType,
    model_encoding: ModelEncoding,
    volume_name: str,
    model_filename: str,
    local_model_path: str,
    spec: Any = None,
    validate: bool = True,
) -> None:
    """Smoke-test the generated handler's on_startup() and handler() using a local model file.

    Raises ValueError if on_startup() or handler() fails. Prints a warning if the
    required ML framework is not installed locally.
    """
    if not validate:
        return

    handler_source = generate_model_handler(model_type, model_encoding, volume_name, model_filename)

    volume_path = f"/volumes/{volume_name}/{model_filename}"
    volume_path_repr = repr(volume_path)
    if volume_path_repr not in handler_source:
        return

    patched_source = handler_source.replace(volume_path_repr, repr(local_model_path))

    sandbox_mod = types.ModuleType("__chalk_handler_validation__")
    try:
        try:
            exec(patched_source, sandbox_mod.__dict__)  # noqa: S102
        except ImportError as e:
            _warn_validation_skipped(e)
            return
        except Exception as e:
            raise ValueError(
                f"Model handler validation failed during module load: {e}\n"
                + f"The generated handler for model_type={model_type.name}, "
                + f"encoding={model_encoding.name} could not be imported: {e}"
            ) from e

        on_startup = getattr(sandbox_mod, "on_startup", None)
        if on_startup is None:
            return

        try:
            on_startup()
        except ImportError as e:
            _warn_validation_skipped(e)
            return
        except Exception as e:
            raise ValueError(
                f"Model handler validation failed: on_startup() raised {type(e).__name__}: {e}\n"
                + f"The model at '{local_model_path}' could not be loaded as "
                + f"{model_type.name}/{model_encoding.name}. "
                + "Ensure the model artifact format matches the declared model type and encoding."
            ) from e

        handler_fn = getattr(sandbox_mod, "handler", None)
        if handler_fn is None or spec is None:
            return

        dummy_event = _build_dummy_event(spec)
        if dummy_event is None:
            return

        try:
            handler_fn(dummy_event, None)
        except ImportError as e:
            _warn_validation_skipped(e)
            return
        except Exception as e:
            raise ValueError(
                f"Model handler validation failed: handler() raised {type(e).__name__}: {e}\n"
                + "The model loaded successfully but failed on a dummy input. "
                + "Your model may require a custom handler and image."
            ) from e
    finally:
        sys.modules.pop("__chalk_handler_validation__", None)
        del sandbox_mod


def build_inferred_image(
    spec: Any,
    model_files: List[str],
    volume_name: str,
    validate: bool = True,
) -> Tuple[str, str]:
    """Build an inferred image with a generated handler baked in.

    Returns (image_uri, model_filename) — the caller is responsible for
    creating a volume and uploading the model file.
    """
    try:
        from chalkcompute import build_image  # pyright: ignore[reportMissingImports]
    except ImportError:
        raise ImportError("Please install `chalkcompute` to enable model image builds.")

    image = infer_image_from_spec(spec)

    model_filename = os.path.basename(model_files[0])
    mt = model_type_from_proto(spec.model_type)
    me = model_encoding_from_proto(spec.model_encoding)

    validate_model_handler(mt, me, volume_name, model_filename, model_files[0], spec, validate)

    handler_source = generate_model_handler(mt, me, volume_name, model_filename)

    handler_tmp = tempfile.NamedTemporaryFile(suffix=".py", delete=False)
    try:
        handler_tmp.write(handler_source.encode())
        handler_tmp.close()

        image = image.add_local_file(handler_tmp.name, "/app/model_handler.py", strategy="copy")

        image_uri = build_image(image)
    finally:
        os.unlink(handler_tmp.name)

    return image_uri, model_filename


def upload_model_to_volume(
    volume_name: str,
    model_filename: str,
    model_file_path: str,
    chalk_client: Any = None,
) -> None:
    """Upload a model file to a Chalk volume."""
    from chalkcompute import ConnectClient, Volume, VolumeClient  # pyright: ignore[reportMissingImports]

    client = VolumeClient.from_connect(ConnectClient(chalk_client=chalk_client))
    with Volume(volume_name, client=client) as volume:
        volume.put_file_from_path(model_filename, model_file_path)


def model_artifact_volume_name(model_name: str, model_artifact_id: str) -> str:
    """Volume name for model artifacts, derived from the artifact id.

    The name is recorded in ``ModelArtifactSpec.model_volume`` at
    registration time so the deploy path can read it back directly.
    """
    return f"chalk-model-{model_name}-{model_artifact_id}"


def chalk_handler_volume_name(model_name: str, model_version: int) -> str:
    """Legacy deterministic name for handler-artifact volumes.

    Kept for backwards compatibility with model versions registered before
    ``model_volume`` was persisted on the artifact spec. New registrations
    use :func:`model_artifact_volume_name` instead.
    """
    return f"chalk-handler-{model_name}-v{model_version}"


# -----------------------------------------------------------------------------
# @model_handler image-build pipeline.
#
# Architecture:
#   - The user's class is shipped as **code** (source file copy, or
#     AST-extracted view for __main__-defined classes).
#   - Data — an ML object passed via `MyHandler(model=...)` and/or files passed
#     via `MyHandler(files=[...])` — is uploaded to a deterministic-named
#     chalkfs volume and surfaces in the deployed container at
#     CHALK_HANDLER_ARTIFACT_PATH.
#   - A **fixed** chalk-remote-call entrypoint (`chalk/ml/_chalk_handler_shim.py`)
#     reads the user's class location from `_chalk_handler_config.HANDLER_CLASS`
#     — a one-line module also baked into the image. No source codegen.
# -----------------------------------------------------------------------------

# Container paths owned by the chalkpy-generated layout. Kept private to this
# module so they cannot drift.
_USER_HANDLERS_PKG = "_chalk_user_handlers"
_USER_HANDLERS_DIR = f"/app/{_USER_HANDLERS_PKG}"
_MAIN_MODULE_NAME = "__main_class"
_SHIM_DEST = "/app/model_handler.py"
_CONFIG_DEST = "/app/_chalk_handler_config.py"


def _shim_src_path() -> str:
    """Local on-disk path to the static `_chalk_handler_shim.py` shipped with chalkpy."""
    import chalk.ml

    return os.path.join(os.path.dirname(chalk.ml.__file__), "_chalk_handler_shim.py")


class _StagedUserClass:
    """Files chalkpy needs to bake into the image so the user's class is importable.

    `import_path` is the dotted module path the shim resolves at startup via
    `importlib.import_module(...)`. `files_to_bake` is a list of
    `(local_src, container_dest)` pairs to feed to `Image.add_local_file`.
    """

    def __init__(self, import_path: str, files_to_bake: List[Tuple[str, str]]) -> None:
        super().__init__()
        self.import_path = import_path
        self.files_to_bake = files_to_bake


def _write_temp(content: str, suffix: str = ".py") -> str:
    """Write `content` to a NamedTemporaryFile and return its path. Caller owns cleanup."""
    fh = tempfile.NamedTemporaryFile(mode="w", suffix=suffix, delete=False)
    try:
        fh.write(content)
    finally:
        fh.close()
    return fh.name


def _extract_main_class_source(src_file: str, class_name: str) -> Optional[str]:
    """Extract the module-level *definitions* from a script — imports, helpers,
    constants, sibling classes, and the target class.

    Used for the ``__main__`` staging path. The deployed container needs the
    user's class to import cleanly, which means we have to ship not just the
    class body but also any names it references at module scope: decorators,
    type annotations, parent classes, module-level helper functions, and
    module-level constants.

    Kept node types:
      * ``Import``, ``ImportFrom`` — module-level imports
      * ``FunctionDef``, ``AsyncFunctionDef`` — module-level helper functions
      * ``ClassDef`` — the target class AND sibling classes (the user may have
        a base class or registry class defined in the same script)
      * ``Assign``, ``AnnAssign`` — module-level constants (only when the RHS
        contains no ``Call``; see ``is_module_level_definition`` for why)

    Dropped: ``If``/``For``/``While``/``Try``/``Expr`` and other side-effect
    statements — so the script's ``main()`` call, training loop, and
    ``ChalkClient()`` instantiation do not run inside the container.
    ``Assign``/``AnnAssign`` whose RHS calls a function (e.g.
    ``rf = RandomForestRegressor()``, ``client = ChalkClient()``,
    ``result = client.register_model_version(...)``) are *also* dropped.
    Notably, ``try: import torch except ImportError: ...`` patterns are
    *also* dropped; a user relying on those should refactor to a real module.

    Returns ``None`` if the file can't be parsed or the target class isn't
    found at module scope; caller falls back to ``inspect.getsource(cls)``.
    """
    import ast

    try:
        with open(src_file) as f:
            src = f.read()
        tree = ast.parse(src)
    except (OSError, SyntaxError):
        return None

    kept: List[ast.stmt] = []
    found_class = False
    for node in tree.body:
        if not is_module_level_definition(node):
            continue
        kept.append(node)
        if isinstance(node, ast.ClassDef) and node.name == class_name:
            found_class = True

    if not found_class:
        return None

    module = ast.Module(body=kept, type_ignores=[])
    try:
        return ast.unparse(module)
    except Exception:
        return None


def _format_relative_import(node: "Any") -> str:
    import ast as _ast

    assert isinstance(node, _ast.ImportFrom)
    dots = "." * (node.level or 0)
    module = node.module or ""
    names = ", ".join(alias.name for alias in node.names)
    return f"from {dots}{module} import {names}"


def _reject_relative_imports(src_file: str, class_name: str) -> None:
    """Raise if `src_file` has any module-level relative imports."""
    import ast as _ast

    try:
        with open(src_file) as f:
            tree = _ast.parse(f.read())
    except (OSError, SyntaxError):
        return  # If we can't parse it, downstream import will surface the error.

    rels = find_relative_imports(tree)
    if not rels:
        return
    formatted = "; ".join(_format_relative_import(n) for n in rels)
    raise ValueError(
        f"@model_handler class {class_name!r} lives in a package that uses relative imports ({formatted}). Chalk ships a single source file into the container, so sibling modules and __init__.py side effects don't run. Define the class in a standalone .py module (no `from .foo import ...`) or in a notebook cell instead."
    )


def _is_trivial_init_statement(node: "Any") -> bool:
    """True if `node` is a statement that's safe to ignore in `__init__.py`.

    Trivial = module docstring, plain imports, or assignments of constant /
    name / tuple / list values (covers `__all__`, `__version__`, simple
    re-exports). Anything else is treated as a runtime side effect.
    """
    import ast as _ast

    if isinstance(node, (_ast.Import, _ast.ImportFrom)):
        return True
    if isinstance(node, _ast.Expr) and isinstance(node.value, _ast.Constant) and isinstance(node.value.value, str):
        return True
    if isinstance(node, (_ast.Assign, _ast.AnnAssign)):
        value = node.value
        return isinstance(value, (_ast.Constant, _ast.Name, _ast.Tuple, _ast.List, _ast.Set, _ast.Dict))
    return False


def _reject_or_warn_init_py(src_file: str, class_name: str) -> None:
    """Inspect the `__init__.py` of the package containing `src_file`.

    Errors if it contains relative imports (those pull in siblings we don't
    ship). Warns if it contains any non-trivial top-level statements
    (function/class definitions, top-level calls, control flow) — chalkpy
    ships only the class's source file, so those setup steps won't run in
    the container and the user might hit subtle bugs at runtime.
    """
    import ast as _ast

    init_py = os.path.join(os.path.dirname(src_file), "__init__.py")
    if not os.path.isfile(init_py):
        return
    try:
        with open(init_py) as f:
            init_src = f.read()
    except OSError:
        return
    if not init_src.strip():
        return
    try:
        tree = _ast.parse(init_src)
    except SyntaxError:
        return  # not our problem to surface

    rels = find_relative_imports(tree)
    if rels:
        formatted = "; ".join(_format_relative_import(n) for n in rels)
        raise ValueError(
            f"@model_handler class {class_name!r} lives in a package whose __init__.py uses relative imports ({formatted}). Chalk ships a single source file into the container, so those sibling modules won't be available. Define the class in a standalone .py module or move the relative imports out of __init__.py."
        )

    non_trivial = [node for node in tree.body if not _is_trivial_init_statement(node)]
    if non_trivial:
        kinds = sorted({type(n).__name__ for n in non_trivial})
        warnings.warn(
            f"@model_handler class {class_name!r} lives in a package whose __init__.py runs non-trivial statements ({', '.join(kinds)}). Chalk ships only the class's source file into the container, so any setup performed in __init__.py (plugin registration, logging config, etc.) will not run. If the class depends on that setup, expect ImportError or surprising runtime behavior in the container.",
            stacklevel=3,
        )


def _stage_user_class(cls: type) -> Tuple[_StagedUserClass, str, List[str]]:
    """Stage a `@model_handler`-decorated class for shipping into the image.

    Three paths, in priority order:
      1. ``cls.__module__`` is a regular module — copy that source file in.
         Rejects files that use relative imports (we'd need to ship siblings).
      2. ``cls.__module__ == "__main__"`` and we're inside a Jupyter notebook
         — reconstruct a self-contained module from cell history via
         ``chalk.utils.notebook.assemble_module_for_class``.
      3. ``cls.__module__ == "__main__"`` and we're in a `.py` script — parse
         the script, keep module-level definitions, drop side-effect statements.
      4. Fallback: ``inspect.getsource(cls)`` (REPL, dynamic class). Helpers
         referenced by the methods are lost; class must be self-contained.

    Returns ``(staged, class_name, owned_tmp_paths)``. The caller adds
    ``staged.files_to_bake`` to the image and passes ``staged.import_path`` +
    ``class_name`` to the shim's config module. ``owned_tmp_paths`` is the set
    of temp files the caller must clean up after the image build.
    """
    from chalk.utils.notebook import assemble_module_for_class, is_notebook

    class_name = cls.__name__
    owned_tmp: List[str] = []

    try:
        init_py = _write_temp("", suffix=".py")
        owned_tmp.append(init_py)

        try:
            src_file = inspect.getsourcefile(cls)
        except (OSError, TypeError):
            src_file = None

        # Path 1: regular module file (not __main__).
        if src_file is not None and cls.__module__ != "__main__":
            module_basename = os.path.basename(src_file)
            if not module_basename.endswith(".py"):
                raise ValueError(f"Cannot ship class {class_name}: its source file {src_file!r} is not a .py file.")
            _reject_relative_imports(src_file, class_name)
            _reject_or_warn_init_py(src_file, class_name)
            module_stem = module_basename[: -len(".py")]
            return (
                _StagedUserClass(
                    import_path=f"{_USER_HANDLERS_PKG}.{module_stem}",
                    files_to_bake=[
                        (init_py, f"{_USER_HANDLERS_DIR}/__init__.py"),
                        (src_file, f"{_USER_HANDLERS_DIR}/{module_basename}"),
                    ],
                ),
                class_name,
                owned_tmp,
            )

        # Path 2: __main__ inside a notebook — reconstruct from cell history.
        class_source: Optional[str] = None
        if is_notebook():
            class_source = assemble_module_for_class(cls)

        # Path 3: __main__ from a .py script — AST-extract module-level defs.
        if class_source is None and src_file is not None:
            class_source = _extract_main_class_source(src_file, class_name)

        # Path 4: fallback — inspect.getsource (REPL, dynamic class).
        if class_source is None:
            try:
                class_source = textwrap.dedent(inspect.getsource(cls))
            except (OSError, TypeError) as e:
                raise ValueError(
                    f"Could not extract source for {class_name}. Define it in a regular Python module or a notebook cell so its source can be located. Original error: {e}"
                ) from e

        class_src_tmp = _write_temp(class_source, suffix=".py")
        owned_tmp.append(class_src_tmp)
        return (
            _StagedUserClass(
                import_path=f"{_USER_HANDLERS_PKG}.{_MAIN_MODULE_NAME}",
                files_to_bake=[
                    (init_py, f"{_USER_HANDLERS_DIR}/__init__.py"),
                    (class_src_tmp, f"{_USER_HANDLERS_DIR}/{_MAIN_MODULE_NAME}.py"),
                ],
            ),
            class_name,
            owned_tmp,
        )
    except Exception:
        for p in owned_tmp:
            try:
                os.unlink(p)
            except OSError:
                pass
        raise


def _render_chalk_handler_config(
    import_path: str,
    class_name: str,
    resolved_model_type: Optional[ModelType],
    file_basenames: List[str],
) -> str:
    """Render the `_chalk_handler_config.py` module baked into the image.

    Three module-level constants the static shim reads at container startup:
      * ``HANDLER_CLASS``: ``"package.module:ClassName"`` — what to import.
      * ``MODEL_TYPE``: ``"sklearn"``/``"pytorch"``/... or ``None`` — which
        ``MODEL_SERIALIZERS`` entry the default ``load_model`` should use.
      * ``FILES``: tuple of basenames the user passed via ``files=[...]`` so
        the shim can build the ``self.files`` dict view.
    """
    handler_class = f"{import_path}:{class_name}"
    model_type_value = resolved_model_type.value if resolved_model_type is not None else None
    return (
        f"HANDLER_CLASS = {handler_class!r}\n"
        f"MODEL_TYPE = {model_type_value!r}\n"
        f"FILES = {tuple(file_basenames)!r}\n"
    )


@dataclass
class HandlerArtifacts:
    """Artifact files (serialized model + `files=`) for a `@model_handler`, with inferred schemas."""

    uploads: List[Tuple[str, str]]  # (local_path, container_basename)
    serialized_name: Optional[str]
    owned_tmp_paths: List[str]
    resolved_model_type: Optional[ModelType]
    inferred_input_schema: Optional[Any]
    inferred_output_schema: Optional[Any]


def _collect_chalk_handler_artifacts(
    handler_instance: Any,
    model_type: Optional[ModelType],
) -> HandlerArtifacts:
    """Collect the artifact files that need to land on the runtime volume."""
    uploads: List[Tuple[str, str]] = []
    owned_tmp: List[str] = []
    serialized_name: Optional[str] = None
    resolved_model_type: Optional[ModelType] = None
    inferred_input_schema: Optional[Any] = None
    inferred_output_schema: Optional[Any] = None

    if handler_instance.model is not None:
        from chalk.client.serialization.model_serialization import ModelSerializer

        serializer = ModelSerializer.from_model(handler_instance.model, model_type)
        resolved_model_type = serializer.model_type
        inferred_input_schema, inferred_output_schema = serializer.infer_input_output_schemas(
            handler_instance.model, resolved_model_type
        )
        serialized_path, _encoding = serializer.serialize()
        owned_tmp.append(serialized_path)
        serialized_name = os.path.basename(serialized_path)
        uploads.append((serialized_path, serialized_name))

    seen: set = set()
    if serialized_name is not None:
        seen.add(serialized_name)
    # Source paths come from `_chalk_raw_files` (set by the decorator's
    # __post_init__); `instance.files` itself is now a basename→Path dict
    # for local-test ergonomics.
    raw_files = getattr(handler_instance, "_chalk_raw_files", handler_instance.files)
    for f in raw_files:
        base = os.path.basename(f)
        if base in seen:
            raise ValueError(
                f"Duplicate basename {base!r} in artifact files. The serialized model and every entry in `files=` must have unique basenames since they all mount at {CHALK_HANDLER_ARTIFACT_PATH}."
            )
        seen.add(base)
        uploads.append((f, base))

    return HandlerArtifacts(
        uploads=uploads,
        serialized_name=serialized_name,
        owned_tmp_paths=owned_tmp,
        resolved_model_type=resolved_model_type,
        inferred_input_schema=inferred_input_schema,
        inferred_output_schema=inferred_output_schema,
    )


def upload_chalk_handler_artifacts(
    volume_name: str,
    uploads: List[Tuple[str, str]],
    chalk_client: Any = None,
    mount_path: str = CHALK_HANDLER_ARTIFACT_PATH,
) -> Dict[str, Any]:
    """Upload artifact files to a managed volume the deployed container will mount.

    Each entry in ``uploads`` is ``(local_path, container_basename)``. The
    returned mount uses ``mount_path`` and contains all files in one version.
    """
    try:
        from chalkcompute import ConnectClient, Volume, VolumeClient  # pyright: ignore[reportMissingImports]

        client = VolumeClient.from_connect(ConnectClient(chalk_client=chalk_client))
    except ImportError:
        raise ImportError("Please install `chalkcompute` to upload model artifacts.")

    with Volume(volume_name, client=client) as volume:
        # Batch all files into a single commit (one version) instead of one commit per file.
        with volume.batch_upload() as batch:
            for local_path, basename in uploads:
                batch.put_file(basename, local_path)
        return volume.mount(mount_path).to_spec_dict()


_CHALKPY_DEV_PLACEHOLDER_VERSION = "0.0.0"


def _chalkpy_dep_spec(user_dependencies: List[str]) -> Optional[str]:
    """Return the pip requirement spec for chalkpy to bake into the container.

    Pins to the locally-installed chalkpy version so the container's
    ``from chalk.ml import model_handler`` resolves to the same version that
    decorated the user's class. Returns ``None`` (skipping auto-injection) if
    the user already supplied a chalkpy requirement in ``dependencies=``.

    On a dev checkout (``chalk._version.__version__ == "0.0.0"``) the version
    isn't a real PyPI release, so we fall back to unpinned ``"chalkpy"`` and
    emit a ``UserWarning`` telling the user to release first or override.
    """
    for dep in user_dependencies:
        head = dep.strip().split()[0] if dep.strip() else ""
        head = (
            head.split("==")[0].split(">=")[0].split("<=")[0].split("~=")[0].split("!=")[0].split(">")[0].split("<")[0]
        )
        if head.lower() == "chalkpy":
            return None

    from chalk._version import __version__ as chalkpy_version

    if chalkpy_version == _CHALKPY_DEV_PLACEHOLDER_VERSION:
        warnings.warn(
            f'Auto-installing `chalkpy` unpinned in the @model_handler container image because the local chalkpy version is the dev placeholder ({_CHALKPY_DEV_PLACEHOLDER_VERSION!r}). The container will install whatever PyPI considers latest, which may not match this checkout. Release chalkpy first or pass dependencies=["chalkpy==<version>"] to pin explicitly.',
            stacklevel=3,
        )
        return "chalkpy"
    return f"chalkpy=={chalkpy_version}"


_APT_INSTALL_LIBGOMP = (
    "apt-get update && apt-get install -y --no-install-recommends libgomp1 " "&& rm -rf /var/lib/apt/lists/*"
)

# Wheels that dlopen the system OpenMP runtime (libgomp.so.1) instead of
# vendoring their own. scikit-learn / scipy / torch / tensorflow all bundle a
# private, auditwheel-renamed libgomp with matching RPATH, so they DON'T need
# it — only these do.
_LIBGOMP_PACKAGES = FrozenOrderedSet(("lightgbm", "xgboost"))


def _needs_system_libgomp(dependencies: List[str]) -> bool:
    for dep in dependencies:
        # strip extras/markers/version specifiers -> bare package name
        name = re.split(r"[<>=!~;\[ ]", dep.strip(), maxsplit=1)[0].lower()
        if name in _LIBGOMP_PACKAGES:
            return True
    return False


@dataclass
class StagedModelHandlerImage:
    """A staged (not yet built) `@model_handler` image plus its artifacts and inferred schemas."""

    image: Any  # unbuilt chalkcompute.Image
    artifact_uploads: List[Tuple[str, str]]  # (local_path, container_basename)
    serialized_name: Optional[str]
    owned_tmp_paths: List[str]
    inferred_input_schema: Optional[Any]
    inferred_output_schema: Optional[Any]


def stage_chalk_model_handler_image(
    handler_instance: Any,
    model_type: Optional[ModelType],
    dependencies: List[str],
) -> StagedModelHandlerImage:
    """Stage (but do not build) the deployable image for a `@model_handler` instance."""
    try:
        from chalkcompute import Image  # pyright: ignore[reportMissingImports]
    except ImportError:
        raise ImportError("Please install `chalkcompute` to enable @model_handler image builds.")

    # Collect artifacts first so basename collisions abort before image work.
    artifacts = _collect_chalk_handler_artifacts(handler_instance, model_type)
    artifact_uploads = artifacts.uploads
    serialized_name = artifacts.serialized_name
    owned_tmp_paths = artifacts.owned_tmp_paths
    resolved_model_type = artifacts.resolved_model_type

    # Container deps: chalk-remote-call-python is the entrypoint; pyarrow is
    # used by the static shim; chalkpy provides `chalk.ml.model_handler` for
    # the staged user module's `from chalk.ml import model_handler` import.
    chalkpy_spec = _chalkpy_dep_spec(list(dependencies))
    deps = ["chalk-remote-call-python", "pyarrow"]
    if chalkpy_spec is not None:
        deps.append(chalkpy_spec)
    deps.extend(dependencies)

    # The preferred `predict(self, df)` path hands user code a
    # `chalkdf.DataFrame`, so the runtime needs chalkdf — and chalkdf requires
    # Python `<3.13`, so pin 3.12 (chalkcompute's default is 3.13+, which makes
    # chalkdf unresolvable at build). The legacy `handler(self, input)` path
    # takes no chalkdf dependency and keeps the unpinned default interpreter.
    from chalk.ml.model_handler import model_handler_entrypoint

    if model_handler_entrypoint(handler_instance) == "predict":
        if not any(d.strip().lower().split("==")[0].split(">")[0].split("<")[0] == "chalkdf" for d in deps):
            deps.append("chalkdf")
        img = Image.debian_slim("3.12")
    else:
        img = Image.debian_slim()
    # debian_slim ships without the OpenMP runtime (libgomp.so.1). LightGBM and
    # XGBoost dlopen it by soname at import and don't vendor their own copy, so
    # install it into the image when either is a dependency. Other OpenMP users
    # (scikit-learn, scipy, torch, ...) bundle a private auditwheel-renamed copy
    # and don't need the system library.
    if _needs_system_libgomp(deps):
        img = img.run_commands(_APT_INSTALL_LIBGOMP)
    img = img.pip_install(deps)

    code_tmp_paths: List[str] = []
    try:
        # 1. Ship the user's class as source.
        staged, class_name, staging_tmps = _stage_user_class(type(handler_instance))
        code_tmp_paths.extend(staging_tmps)
        for local, dest in staged.files_to_bake:
            img = img.add_local_file(local, dest, strategy="copy")

        # 2. Bake the **static** chalk-remote-call shim shipped with chalkpy.
        #    The shim resolves the user's class via a tiny config module — no
        #    source codegen, no string-template churn.
        img = img.add_local_file(_shim_src_path(), _SHIM_DEST, strategy="copy")

        # File basenames the user passed via files=[...], minus the auto-
        # serialized model file. The shim uses this to build self.files.
        file_basenames = [base for _local, base in artifact_uploads if base != serialized_name]
        config_path = _write_temp(
            _render_chalk_handler_config(staged.import_path, class_name, resolved_model_type, file_basenames)
        )
        code_tmp_paths.append(config_path)
        img = img.add_local_file(config_path, _CONFIG_DEST, strategy="copy")

        return StagedModelHandlerImage(
            image=img,
            artifact_uploads=artifact_uploads,
            serialized_name=serialized_name,
            owned_tmp_paths=owned_tmp_paths,
            inferred_input_schema=artifacts.inferred_input_schema,
            inferred_output_schema=artifacts.inferred_output_schema,
        )
    except Exception:
        for p in owned_tmp_paths:
            try:
                os.unlink(p)
            except OSError:
                pass
        raise
    finally:
        for p in code_tmp_paths:
            try:
                os.unlink(p)
            except OSError:
                pass


def serialize_image_spec(image: Any) -> bytes:
    """Serialize an ``Image`` to ``ImageSpec`` bytes (excludes strategy='volume' files)."""
    return image.to_proto().SerializeToString()


def image_local_files(image: Any) -> List[Tuple[str, str, Optional[int]]]:
    """Return the image's strategy='volume' files as ``(src, dest, mode)`` triples."""
    return [(lf.src, lf.dest, lf.mode) for lf in getattr(image, "lazy_local_files", []) or []]


def image_spec_bakes_handler_shim(data: bytes) -> bool:
    """True if an ImageSpec bakes the chalk handler shim — i.e. a handler/inferred serving image."""
    from chalkcompute._gen.chalk.sandbox.v1 import service_pb2 as _sandbox  # pyright: ignore[reportMissingImports]

    spec = _sandbox.ImageSpec()
    spec.ParseFromString(data)
    return any(s.HasField("add_file") and s.add_file.destination == _SHIM_DEST for s in spec.steps)


def build_image_from_spec_bytes(data: bytes, chalk_client: Any = None) -> str:
    """Rebuild the image from persisted ``ImageSpec`` bytes and return its URI."""
    try:
        from chalkcompute import Image, build_image  # pyright: ignore[reportMissingImports]
    except ImportError:
        raise ImportError("Please install `chalkcompute` to enable @model_handler image builds.")
    return build_image(Image.from_proto_bytes(data), chalk_client=chalk_client)


def build_image_from_spec_with_files(
    data: bytes,
    local_files: List[Tuple[str, str, Optional[int]]],
    chalk_client: Any = None,
) -> Tuple[str, List[Dict[str, Any]]]:
    """Rebuild from ``ImageSpec`` bytes + ``(src, dest, mode)`` files; return (uri, volume_mounts)."""
    try:
        from chalkcompute import Image, build_image_with_volumes  # pyright: ignore[reportMissingImports]
    except ImportError:
        raise ImportError("Please install `chalkcompute` to enable @model_handler image builds.")
    img = Image.from_proto_bytes(data)
    for src, dest, mode in local_files:
        img = img.add_local_file(src, dest, mode=mode, strategy="volume")
    uri, volumes = build_image_with_volumes(img, chalk_client=chalk_client)
    return uri, [v.to_spec_dict() for v in volumes]
