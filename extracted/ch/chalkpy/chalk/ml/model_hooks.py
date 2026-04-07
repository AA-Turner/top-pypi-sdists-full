from typing import TYPE_CHECKING, Any, Callable, Dict, Optional, Protocol, Tuple, Union, cast

from chalk.ml.utils import ModelClass, ModelEncoding, ModelType
from chalk.utils.environment_parsing import env_var_bool
from chalk.utils.string import resolver_name

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

    def set_name_mappings(
        self,
        input_name_map: Optional[Dict[str, str]] = None,
        output_name_map: Optional[Dict[str, str]] = None,
    ) -> None:
        """Set name mappings for input/output names.

        Default implementation is a no-op.
        Override for models that need to map input/output names (e.g., ONNX).
        """
        pass


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


class XGBoostRankerInference(ModelInference):
    """Model inference for XGBoost rankers."""

    def load_model(self, path: str, resource_hint: Optional["ResourceHint"] = None) -> Any:
        import xgboost  # pyright: ignore[reportMissingImports]

        model = xgboost.XGBRanker()
        model.load_model(path)
        return model

    def predict(self, model: Any, X: Any) -> Any:
        # Returns relevance scores — higher = more relevant, not a class label
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

        array = result.field(field_index if field_index is not None else 0)
        # Convert PyArrow array to Python list for Polars compatibility
        if hasattr(array, "to_pylist"):
            return array.to_pylist()
        return array

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
            # C++ side has already applied output name mapping, so use names as-is
            fields.append(pa.field(name, arrow_array.type))
            arrays.append(arrow_array)

        return pa.StructArray.from_arrays(arrays, fields=fields)

    def _numpy_to_arrow_array(self, arr: Any) -> Any:
        """Convert numpy array to PyArrow array (possibly nested list)."""
        import pyarrow as pa

        # PyArrow can infer the correct nested list type from Python lists
        # Shape (batch, dim1, dim2, ...) -> list[list[...]]
        return pa.array(arr.tolist())


class NativeONNXInference(ModelInference):
    def __init__(self):
        super().__init__()
        # Create fallback to Python ORT for GPU mode or when native is disabled
        self._fallback: ONNXInference = ONNXInference()

        self._use_native = env_var_bool("CHALK_USE_NATIVE_ONNX_INFERENCE", True)
        self._native = False
        self._model = None  # Will hold c++ ONNX Model instance
        self._input_name_map: dict[str, str] = {}  # Maps ONNX input names to struct field names
        self._output_name_map: dict[str, str] = {}  # Maps ONNX output names to struct field names

        if self._use_native:
            try:
                from libchalk.onnx import ONNXModel  # pyright: ignore[reportMissingImports]

                self._native = True
                self._ONNXModel = ONNXModel
            except (ImportError, AttributeError) as e:
                raise ImportError(
                    "CHALK_USE_NATIVE_ONNX_INFERENCE is enabled (default), but native ONNX implementation "
                    + "(libchalk.onnx) is not available. Either disable it via "
                    + "CHALK_USE_NATIVE_ONNX_INFERENCE=false or install libchalk with ONNX support. Error: {e}"
                ) from e

    def set_name_mappings(
        self,
        input_name_map: Optional[dict[str, str]] = None,
        output_name_map: Optional[dict[str, str]] = None,
    ) -> None:
        """Set mappings from ONNX input/output names to struct field names."""
        if input_name_map:
            self._input_name_map = input_name_map
        if output_name_map:
            self._output_name_map = output_name_map

    def load_model(self, path: str, resource_hint: Optional["ResourceHint"] = None) -> Any:
        # Use fallback for GPU mode or if native is disabled
        if not self._use_native or resource_hint == "gpu":
            return self._fallback.load_model(path, resource_hint)

        try:
            self._model = self._ONNXModel(
                model_path=path,
                pool_size=0,
                input_name_map=self._input_name_map if self._input_name_map else None,
                output_name_map=self._output_name_map if self._output_name_map else None,
            )
            return self._model
        except Exception as e:
            raise RuntimeError(f"Failed to load ONNX model with native implementation: {e}") from e

    def prepare_input(self, feature_table: Any) -> Any:
        """Convert PyArrow table to model input format."""
        import pyarrow as pa
        import pyarrow.compute as pc

        # Use fallback if native is disabled
        if not self._use_native:
            return self._fallback.prepare_input(feature_table)

        # Native path: convert to dict[str, Arrow Array]
        # Rename columns according to input_name_map
        input_dict = {}

        # Get the expected input types from the loaded ONNX model
        if self._model and (self._model, "input_schema"):
            schema_name_to_type = {field.name: field.type for field in self._model.input_schema}
        else:
            schema_name_to_type = {}

        for i in range(feature_table.num_columns):
            chalk_name = feature_table.schema[i].name

            onnx_name = self._input_name_map.get(chalk_name, chalk_name)

            col = feature_table.column(i)
            # Combine chunks if needed
            if isinstance(col, pa.ChunkedArray):
                col = col.combine_chunks()

            # Cast to the expected ONNX input type based on model schema
            if schema_name_to_type.get(onnx_name):
                expected_type = schema_name_to_type[onnx_name]
                # Cast the column to the expected type (both list and scalar supported)
                if col.type != expected_type:
                    col = pc.cast(col, expected_type)

            # Convert simple scalar arrays to list arrays
            # The C++ ONNX code expects list arrays, so wrap each scalar in a list
            if not pa.types.is_list(col.type):
                scalar_list = col.to_pylist()
                wrapped_list = [[val] for val in scalar_list]
                col = pa.array(wrapped_list, type=pa.list_(col.type))

            input_dict[onnx_name] = col

        return input_dict

    def predict(self, model: Any, X: Any) -> Any:
        """Run ONNX inference using native C++ or Python fallback."""
        if not self._use_native:
            return self._fallback.predict(model, X)

        output_dict = model.predict_batch(X)

        # Convert dict[onnx_name, Array] to StructArray with chalk field names
        import pyarrow as pa

        fields = []
        arrays = []

        for output_name, output_array in output_dict.items():
            fields.append(pa.field(output_name, output_array.type))
            arrays.append(output_array)

        return pa.StructArray.from_arrays(arrays, fields=fields)

    def extract_output(self, result: Any, output_feature_name: str) -> Any:
        """Extract single field from ONNX struct output."""
        if not self._use_native:
            return self._fallback.extract_output(result, output_feature_name)

        # Native path: result is a StructArray
        import pyarrow as pa

        if not isinstance(result, (pa.StructArray, pa.ChunkedArray)):
            return result

        struct_type = result.type if isinstance(result, pa.StructArray) else result.chunk(0).type

        # Extract just the feature name (without namespace for matching)
        feature_name_only = resolver_name(output_feature_name)

        # Find matching field by ONNX output name
        field_index = None
        for i, field in enumerate(struct_type):
            # Try to match both the full name and just the feature name
            if field.name == output_feature_name or field.name == feature_name_only:
                field_index = i
                break

        if field_index is None:
            # Fallback to first field if name not found
            field_index = 0

        # Extract the field and convert to a format Polars can understand
        extracted = result.field(field_index)

        # Convert ChunkedArray to regular Array if needed
        if isinstance(extracted, pa.ChunkedArray):
            extracted = extracted.combine_chunks()

        # Convert PyArrow Array to Python list for Polars
        return extracted.to_pylist()


class ModelInferenceRegistry:
    """Registry for model inference implementations."""

    def __init__(self):
        super().__init__()
        self._registry: Dict[
            Tuple[ModelType, ModelEncoding, Optional[ModelClass]], Union[ModelInference, Callable[[], ModelInference]]
        ] = {}

    def register(
        self,
        model_type: ModelType,
        encoding: ModelEncoding,
        model_class: Optional[ModelClass],
        inference: Union[ModelInference, Callable[[], ModelInference]],
    ) -> None:
        """Register a model inference implementation."""
        self._registry[(model_type, encoding, model_class)] = inference

    def register_for_all_classes(
        self,
        model_type: ModelType,
        encoding: ModelEncoding,
        inference: Union[ModelInference, Callable[[], ModelInference]],
    ) -> None:
        """Register inference for all ModelClass variants."""
        self.register(model_type, encoding, None, inference)
        self.register(model_type, encoding, ModelClass.CLASSIFICATION, inference)
        self.register(model_type, encoding, ModelClass.REGRESSION, inference)
        self.register(model_type, encoding, ModelClass.RANKING, inference)

    def get(
        self,
        model_type: ModelType,
        encoding: ModelEncoding,
        model_class: Optional[ModelClass] = None,
    ) -> Optional[ModelInference]:
        """Get a model inference implementation from the registry."""
        value = self._registry.get((model_type, encoding, model_class), None)

        # If it's a callable (factory/lambda), instantiate and cache the result
        if callable(value) and not isinstance(value, type):
            instance = value()
            self._registry[(model_type, encoding, model_class)] = instance
            return instance

        return cast(Optional[ModelInference], value)

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
MODEL_REGISTRY.register_for_all_classes(ModelType.SKLEARN, ModelEncoding.JOBLIB, SklearnInference())
MODEL_REGISTRY.register_for_all_classes(ModelType.TENSORFLOW, ModelEncoding.HDF5, TensorFlowInference())
MODEL_REGISTRY.register_for_all_classes(ModelType.LIGHTGBM, ModelEncoding.TEXT, LightGBMInference())
MODEL_REGISTRY.register_for_all_classes(ModelType.CATBOOST, ModelEncoding.CBM, CatBoostInference())
MODEL_REGISTRY.register_for_all_classes(ModelType.ONNX, ModelEncoding.PROTOBUF, lambda: NativeONNXInference())

# XGBoost requires different implementations for task types; defaults to regression
MODEL_REGISTRY.register(ModelType.XGBOOST, ModelEncoding.JSON, None, XGBoostRegressorInference())
MODEL_REGISTRY.register(ModelType.XGBOOST, ModelEncoding.JSON, ModelClass.CLASSIFICATION, XGBoostClassifierInference())
MODEL_REGISTRY.register(ModelType.XGBOOST, ModelEncoding.JSON, ModelClass.REGRESSION, XGBoostRegressorInference())
MODEL_REGISTRY.register(ModelType.XGBOOST, ModelEncoding.JSON, ModelClass.RANKING, XGBoostRankerInference())
