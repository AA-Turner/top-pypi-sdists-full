from __future__ import annotations

import os
import sys
import tempfile
import types
from typing import Any, Dict, List, Tuple

from chalk.ml.utils import ModelEncoding, ModelType, model_encoding_from_proto, model_type_from_proto

_DEFAULT_PACKAGES: Dict[ModelType, List[str]] = {
    ModelType.PYTORCH: ["torch"],
    ModelType.SKLEARN: ["scikit-learn", "joblib"],
    ModelType.XGBOOST: ["xgboost"],
}


def infer_image_from_spec(spec: Any) -> Any:
    """Construct a chalkcompute.Image from a ModelArtifactSpec's model_type and dependencies."""
    try:
        from chalkcompute import Image  # pyright: ignore[reportMissingImports]
    except ImportError:
        raise ImportError("Please install `chalkcompute` to enable model image builds.")

    mt = model_type_from_proto(spec.model_type)

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
    return Image.debian_slim().pip_install(["chalk-remote-call-python"] + packages)


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
    "        dmatrix = xgb.DMatrix(features, feature_names=list(event.keys()))\n"
    "        preds = model.predict(dmatrix)\n"
)

_PREDICT_SKLEARN = "        preds = model.predict(features)\n"

_PREDICT_PYTORCH = (
    "        tensor = torch.tensor(features, dtype=torch.float32)\n"
    "        with torch.no_grad():\n"
    "            preds = model(tensor)\n"
    "        preds = preds.numpy()\n"
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
) -> None:
    """Upload a model file to a chalkfs volume."""
    try:
        from chalkcompute import ConnectClient, VolumeClient  # pyright: ignore[reportMissingImports]
    except ImportError:
        raise ImportError("Please install `chalkcompute` to enable model image builds.")

    vol_client = VolumeClient.from_connect(ConnectClient())
    vol = vol_client.create(volume_name)
    vol.put_file_from_path(model_filename, model_file_path)
