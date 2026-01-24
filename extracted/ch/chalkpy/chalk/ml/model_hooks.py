from typing import TYPE_CHECKING, Any, Dict, Optional, Protocol, Tuple

from chalk.ml.utils import ModelClass, ModelEncoding, ModelType

if TYPE_CHECKING:
    from chalk.features.resolver import ResourceHint


class ModelInference(Protocol):
    """Abstract base class for model loading and inference."""

    def load_model(self, path: str, resource_hint: Optional["ResourceHint"] = None) -> Any:
        """Load a model from the given path."""
        pass

    def predict(self, model: Any, X: Any) -> Any:
        """Run inference on the model with input X."""
        pass

    def prepare_input(self, feature_table: Any) -> Any:
        """Convert PyArrow table to model input format.

        Default implementation converts to numpy array via __array__().
        Override for model-specific input formats (e.g., ONNX struct arrays).
        """
        return feature_table.__array__()

    def extract_output(self, result: Any, output_feature_name: str) -> Any:
        """Extract single output from model result.

        Default implementation returns result as-is (for single outputs).
        Override for models with structured outputs (e.g., ONNX struct arrays).
        """
        return result


class XGBoostClassifierInference(ModelInference):
    """Model inference for XGBoost classifiers."""

    def load_model(self, path: str, resource_hint: Optional["ResourceHint"] = None) -> Any:
        import xgboost  # pyright: ignore[reportMissingImports]

        model = xgboost.XGBClassifier()
        model.load_model(path)
        return model

    def predict(self, model: Any, X: Any) -> Any:
        return model.predict(X)


class XGBoostRegressorInference(ModelInference):
    """Model inference for XGBoost regressors."""

    def load_model(self, path: str, resource_hint: Optional["ResourceHint"] = None) -> Any:
        import xgboost  # pyright: ignore[reportMissingImports]

        model = xgboost.XGBRegressor()
        model.load_model(path)
        return model

    def predict(self, model: Any, X: Any) -> Any:
        return model.predict(X)


class PyTorchInference(ModelInference):
    """Model inference for PyTorch models."""

    def load_model(self, path: str, resource_hint: Optional["ResourceHint"] = None) -> Any:
        import torch  # pyright: ignore[reportMissingImports]

        torch.set_grad_enabled(False)

        # Load the model
        model = torch.jit.load(path)

        # If resource_hint is "gpu", move model to GPU
        if resource_hint == "gpu" and torch.cuda.is_available():
            device = torch.device("cuda")
            model = model.to(device)
            model.input_to_tensor = lambda X: torch.from_numpy(X).float().to(device)
        else:
            model.input_to_tensor = lambda X: torch.from_numpy(X).float()

        return model

    def predict(self, model: Any, X: Any) -> Any:
        outputs = model(model.input_to_tensor(X))
        result = outputs.detach().cpu().numpy().astype("float64")
        result = result.squeeze()

        # Convert 0-dimensional array to scalar, or ensure we have a proper 1D array
        if result.ndim == 0:
            return result.item()

        return result


class SklearnInference(ModelInference):
    """Model inference for scikit-learn models."""

    def load_model(self, path: str, resource_hint: Optional["ResourceHint"] = None) -> Any:
        import joblib  # pyright: ignore[reportMissingImports]

        return joblib.load(path)

    def predict(self, model: Any, X: Any) -> Any:
        return model.predict(X)


class TensorFlowInference(ModelInference):
    """Model inference for TensorFlow models."""

    def load_model(self, path: str, resource_hint: Optional["ResourceHint"] = None) -> Any:
        import tensorflow  # pyright: ignore[reportMissingImports]

        return tensorflow.keras.models.load_model(path)

    def predict(self, model: Any, X: Any) -> Any:
        return model.predict(X)


class LightGBMInference(ModelInference):
    """Model inference for LightGBM models."""

    def load_model(self, path: str, resource_hint: Optional["ResourceHint"] = None) -> Any:
        import lightgbm  # pyright: ignore[reportMissingImports]

        return lightgbm.Booster(model_file=path)

    def predict(self, model: Any, X: Any) -> Any:
        return model.predict(X)


class CatBoostInference(ModelInference):
    """Model inference for CatBoost models."""

    def load_model(self, path: str, resource_hint: Optional["ResourceHint"] = None) -> Any:
        import catboost  # pyright: ignore[reportMissingImports]

        return catboost.CatBoost().load_model(path)

    def predict(self, model: Any, X: Any) -> Any:
        return model.predict(X)


class ONNXInference(ModelInference):
    """Model inference for ONNX models with struct input/output support."""

    def load_model(self, path: str, resource_hint: Optional["ResourceHint"] = None) -> Any:
        import onnxruntime  # pyright: ignore[reportMissingImports]

        # Conditionally add CUDAExecutionProvider based on resource_hint
        providers = (
            ["CUDAExecutionProvider", "CPUExecutionProvider"] if resource_hint == "gpu" else ["CPUExecutionProvider"]
        )
        return onnxruntime.InferenceSession(path, providers=providers)

    def prepare_input(self, feature_table: Any) -> Any:
        """Convert PyArrow table to struct array for ONNX models."""
        import pyarrow as pa

        # Get arrays for each column, combining chunks if necessary
        arrays = []
        for i in range(feature_table.num_columns):
            col = feature_table.column(i)
            if isinstance(col, pa.ChunkedArray):
                arrays.append(col.combine_chunks())
            else:
                arrays.append(col)

        # Create fields from schema, preserving original field names
        # Field names should match ONNX input names exactly
        fields = []
        for field in feature_table.schema:
            fields.append(pa.field(field.name, field.type))

        # Create struct array where each row is a struct with named fields
        return pa.StructArray.from_arrays(arrays, fields=fields)

    def extract_output(self, result: Any, output_feature_name: str) -> Any:
        """Extract single field from ONNX struct output."""
        import pyarrow as pa

        if not isinstance(result, (pa.StructArray, pa.ChunkedArray)):
            return result

        struct_type = result.type if isinstance(result, pa.StructArray) else result.chunk(0).type

        # Find matching field by name, or use first field
        field_index = None
        for i, field in enumerate(struct_type):
            if field.name == output_feature_name:
                field_index = i
                break

        return result.field(field_index if field_index is not None else 0)

    def predict(self, model: Any, X: Any) -> Any:
        """Run ONNX inference with struct input/output."""
        # Get ONNX model input/output names
        input_names = [inp.name for inp in model.get_inputs()]
        output_names = [out.name for out in model.get_outputs()]

        # Convert struct input to ONNX input dict
        input_dict = self._struct_to_inputs(X, input_names)

        # Run ONNX inference
        outputs = model.run(output_names, input_dict)

        # Always return outputs as struct array
        return self._outputs_to_struct(output_names, outputs)

    def _struct_to_inputs(self, struct_array: Any, input_names: list) -> dict:
        """Extract ONNX inputs from struct array by matching field names.

        Struct field names must match ONNX input names (supports list/Tensor types).
        If ONNX expects a single input but struct has multiple scalar fields,
        stack them into a 2D array.
        """
        import numpy as np
        import pyarrow as pa

        if isinstance(struct_array, pa.ChunkedArray):
            struct_array = struct_array.combine_chunks()

        input_dict = {}
        struct_fields = {field.name: i for i, field in enumerate(struct_array.type)}

        # Check if struct field names match ONNX input names
        fields_match = all(input_name in struct_fields for input_name in input_names)

        if not fields_match:
            # Special case 1: ONNX expects single input and struct has single field
            # Use that field regardless of name mismatch
            if len(input_names) == 1 and len(struct_fields) == 1:
                field_data = struct_array.field(0)
                input_dict[input_names[0]] = self._arrow_to_numpy(field_data)
                return input_dict

            # Special case 2: ONNX expects single input, but struct has multiple scalar fields
            # Stack them into a 2D array [batch_size, num_fields]
            if len(input_names) == 1 and len(struct_fields) > 1:
                # Check if all fields are scalar (not nested lists)
                all_scalar = all(
                    not pa.types.is_list(struct_array.type[i].type)
                    and not pa.types.is_large_list(struct_array.type[i].type)
                    for i in range(len(struct_array.type))
                )

                if all_scalar:
                    # Stack all fields into a single 2D array
                    columns = []
                    for i in range(len(struct_array.type)):
                        field_data = struct_array.field(i)
                        col_array = self._arrow_to_numpy(field_data)
                        columns.append(col_array)

                    # Stack columns horizontally to create [batch_size, num_features]
                    stacked = np.column_stack(columns)
                    input_dict[input_names[0]] = stacked
                    return input_dict

            raise ValueError(
                f"ONNX inputs {input_names} not found in struct fields {list(struct_fields.keys())}. "
                + "Struct field names must match ONNX input names."
            )

        # Direct mapping: struct fields match ONNX inputs (for Tensor/list types or named inputs)
        for input_name in input_names:
            field_data = struct_array.field(struct_fields[input_name])
            input_dict[input_name] = self._arrow_to_numpy(field_data)

        return input_dict

    def _arrow_to_numpy(self, arrow_array: Any) -> Any:
        """Convert Arrow array (including nested lists) to dense numpy array."""
        import numpy as np
        import pyarrow as pa

        if isinstance(arrow_array, pa.ChunkedArray):
            arrow_array = arrow_array.combine_chunks()

        # Convert to Python list, then numpy - handles all cases (nested lists, flat arrays, etc.)
        return np.array(arrow_array.to_pylist(), dtype=np.float32)

    def _outputs_to_struct(self, output_names: list, outputs: list) -> Any:
        """Convert ONNX outputs to PyArrow struct array."""
        import pyarrow as pa

        if not outputs:
            raise ValueError("ONNX model returned no outputs")

        # Convert each output to Arrow array with proper type
        fields = []
        arrays = []

        for name, output_array in zip(output_names, outputs):
            arrow_array = self._numpy_to_arrow_array(output_array)
            fields.append(pa.field(name, arrow_array.type))
            arrays.append(arrow_array)

        return pa.StructArray.from_arrays(arrays, fields=fields)

    def _numpy_to_arrow_array(self, arr: Any) -> Any:
        """Convert numpy array to PyArrow array (possibly nested list)."""
        import pyarrow as pa

        # PyArrow can infer the correct nested list type from Python lists
        # Shape (batch, dim1, dim2, ...) -> list[list[...]]
        return pa.array(arr.tolist())


class ModelInferenceRegistry:
    """Registry for model inference implementations."""

    def __init__(self):
        super().__init__()
        self._registry: Dict[Tuple[ModelType, ModelEncoding, Optional[ModelClass]], ModelInference] = {}

    def register(
        self,
        model_type: ModelType,
        encoding: ModelEncoding,
        model_class: Optional[ModelClass],
        inference: ModelInference,
    ) -> None:
        """Register a model inference implementation."""
        self._registry[(model_type, encoding, model_class)] = inference

    def register_for_all_classes(
        self,
        model_type: ModelType,
        encoding: ModelEncoding,
        inference: ModelInference,
    ) -> None:
        """Register inference for None, CLASSIFICATION, and REGRESSION variants."""
        self.register(model_type, encoding, None, inference)
        self.register(model_type, encoding, ModelClass.CLASSIFICATION, inference)
        self.register(model_type, encoding, ModelClass.REGRESSION, inference)

    def get(
        self,
        model_type: ModelType,
        encoding: ModelEncoding,
        model_class: Optional[ModelClass] = None,
    ) -> Optional[ModelInference]:
        """Get a model inference implementation from the registry."""
        return self._registry.get((model_type, encoding, model_class), None)

    def get_loader(
        self,
        model_type: ModelType,
        encoding: ModelEncoding,
        model_class: Optional[ModelClass] = None,
    ):
        """Get the load_model function for a given configuration."""
        inference = self.get(model_type, encoding, model_class)
        return inference.load_model if inference else None

    def get_predictor(
        self,
        model_type: ModelType,
        encoding: ModelEncoding,
        model_class: Optional[ModelClass] = None,
    ):
        """Get the predict function for a given configuration."""
        inference = self.get(model_type, encoding, model_class)
        return inference.predict if inference else None


# Global registry instance
MODEL_REGISTRY = ModelInferenceRegistry()

# Register all model types
MODEL_REGISTRY.register_for_all_classes(ModelType.PYTORCH, ModelEncoding.PICKLE, PyTorchInference())
MODEL_REGISTRY.register_for_all_classes(ModelType.SKLEARN, ModelEncoding.PICKLE, SklearnInference())
MODEL_REGISTRY.register_for_all_classes(ModelType.TENSORFLOW, ModelEncoding.HDF5, TensorFlowInference())
MODEL_REGISTRY.register_for_all_classes(ModelType.LIGHTGBM, ModelEncoding.TEXT, LightGBMInference())
MODEL_REGISTRY.register_for_all_classes(ModelType.CATBOOST, ModelEncoding.CBM, CatBoostInference())
MODEL_REGISTRY.register_for_all_classes(ModelType.ONNX, ModelEncoding.PROTOBUF, ONNXInference())

# XGBoost requires different implementations for classification vs regression
MODEL_REGISTRY.register(ModelType.XGBOOST, ModelEncoding.JSON, None, XGBoostRegressorInference())
MODEL_REGISTRY.register(ModelType.XGBOOST, ModelEncoding.JSON, ModelClass.CLASSIFICATION, XGBoostClassifierInference())
MODEL_REGISTRY.register(ModelType.XGBOOST, ModelEncoding.JSON, ModelClass.REGRESSION, XGBoostRegressorInference())
