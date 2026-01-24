import os
import pickle
import tempfile
from typing import Any, Callable, List, Mapping, NamedTuple, Optional, Tuple, Type

from google.protobuf import struct_pb2

from chalk._gen.chalk.models.v1 import model_artifact_pb2 as _model_artifact_pb2
from chalk._gen.chalk.models.v1.model_artifact_pb2 import ModelFile
from chalk._gen.chalk.server.v1.model_registry_pb2 import RunCriterion, RunCriterionDirection
from chalk.ml.model_file_transfer import FileInfo
from chalk.ml.utils import ModelAttributeExtractor, ModelEncoding, ModelRunCriterion, ModelType

ModelSchemaType = List[Tuple[List[int], Any]]


class ModelSerializationConfig(NamedTuple):
    filename: str
    encoding: ModelEncoding
    serialize_fn: Callable[[str, Any], None]
    schema_fn: Optional[Callable[[Any], Tuple[Optional[ModelSchemaType], Optional[ModelSchemaType]]]] = None
    dependency_fn: Optional[Callable[[], Optional[List[str]]]] = None


MODEL_SERIALIZERS = {
    ModelType.PYTORCH: ModelSerializationConfig(
        filename="model.pth",
        encoding=ModelEncoding.PICKLE,
        serialize_fn=lambda model, path: ModelSerializer.with_import(
            "torch",
            lambda torch: torch.jit.save(torch.jit.script(model.eval()), path),
            "Please install PyTorch to save PyTorch models.",
        ),
        schema_fn=lambda model: ModelAttributeExtractor.infer_pytorch_schemas(model),
        dependency_fn=lambda: ModelSerializer.with_import(
            "torch", lambda torch: [f"torch=={torch.__version__}"], "Please install PyTorch to save PyTorch models."
        ),
    ),
    ModelType.SKLEARN: ModelSerializationConfig(
        filename="model.pkl",
        encoding=ModelEncoding.PICKLE,
        serialize_fn=lambda model, path: ModelSerializer.with_import(
            "joblib", lambda joblib: joblib.dump(model, path), "Please install joblib to save sklearn models."
        ),
        schema_fn=lambda model: ModelAttributeExtractor.infer_sklearn_schemas(model),
        dependency_fn=lambda: ModelSerializer.with_import(
            "sklearn",
            lambda sklearn: [f"scikit-learn=={sklearn.__version__}"],
            "Please install sklearn to save sklearn models.",
        ),
    ),
    ModelType.TENSORFLOW: ModelSerializationConfig(
        filename="model.h5", encoding=ModelEncoding.HDF5, serialize_fn=lambda model, path: model.save(path)
    ),
    ModelType.XGBOOST: ModelSerializationConfig(
        filename="model.json",
        encoding=ModelEncoding.JSON,
        serialize_fn=lambda model, path: model.save_model(path),
        schema_fn=lambda model: ModelAttributeExtractor.infer_xgboost_schemas(model),
        dependency_fn=lambda: ModelSerializer.with_import(
            "xgboost",
            lambda xgboost: [f"xgboost=={xgboost.__version__}"],
            "Please install xgboost to save xgboost models.",
        ),
    ),
    ModelType.LIGHTGBM: ModelSerializationConfig(
        filename="model.txt",
        encoding=ModelEncoding.TEXT,
        serialize_fn=lambda model, path: model.save_model(path),
    ),
    ModelType.CATBOOST: ModelSerializationConfig(
        filename="model.cbm",
        encoding=ModelEncoding.CBM,
        serialize_fn=lambda model, path: model.save_model(path),
        schema_fn=lambda model: ModelAttributeExtractor.infer_catboost_schemas(model),
    ),
    ModelType.ONNX: ModelSerializationConfig(
        filename="model.onnx",
        encoding=ModelEncoding.PROTOBUF,
        serialize_fn=lambda model, path: ModelSerializer.with_import(
            "onnx",
            lambda onnx: onnx.save(
                # Unwrap model if it has a _model attribute (e.g., wrapped ONNX models)
                model._model if hasattr(model, "_model") else model,
                path,
            ),
            "Please install onnx to save ONNX models.",
        ),
    ),
}


class ModelSerializer:
    def __init__(self, model: Any, model_type: Optional[ModelType]):
        self._temp_files: List[str] = []
        self.model = model
        if model_type is not None:
            self.model_type = model_type
            self.model_class = None
        else:
            model_type, model_class = ModelAttributeExtractor.infer_model_type(model)
            self.model_type = model_type
            self.model_class = model_class

        if self.model_type is None:
            raise ValueError("Unable to infer model type from object and no type given.")

        super().__init__()

    @classmethod
    def from_model(cls, model: Any, model_type: Optional[ModelType] = None) -> "ModelSerializer":
        return cls(model=model, model_type=model_type)

    def __enter__(self) -> "ModelSerializer":
        return self

    def __exit__(
        self, exc_type: Optional[Type[BaseException]], exc_val: Optional[BaseException], exc_tb: Optional[object]
    ) -> bool:
        self.cleanup()
        return False

    def serialize(self) -> Tuple[str, ModelEncoding]:
        assert self.model_type is not None, "Could not determine model type. Please set parameter: model_type."
        return self.serialize_model(self.model, self.model_type)

    def serialize_model(self, model: Any, model_type: ModelType) -> tuple[str, ModelEncoding]:
        if model_type not in MODEL_SERIALIZERS:
            raise NotImplementedError(f"Unsupported model type: {model_type}")

        tmp_dir = tempfile.mkdtemp()
        serializer_config = MODEL_SERIALIZERS[model_type]

        file_name = serializer_config.filename

        model_path = os.path.join(tmp_dir, file_name)

        serializer_config.serialize_fn(model, model_path)

        self._temp_files.append(model_path)
        return model_path, serializer_config.encoding

    def serialize_to_path(self, path: str, cleanup: bool = True) -> Tuple[str, ModelEncoding]:
        assert self.model_type is not None, "Could not determine model type. Please set parameter: model_type."
        return self.serialize_model_to_path(self.model, self.model_type, path, cleanup)

    def serialize_model_to_path(
        self,
        model: Any,
        model_type: ModelType,
        path: str,
        cleanup: bool = True,
    ) -> tuple[str, ModelEncoding]:
        if model_type not in MODEL_SERIALIZERS:
            raise NotImplementedError(f"Unsupported model type: {model_type}")
        dir = path

        serializer_config = MODEL_SERIALIZERS[model_type]

        file_name = serializer_config.filename

        model_path = os.path.join(dir, file_name)

        serializer_config.serialize_fn(model, model_path)
        if cleanup:
            self._temp_files.append(model_path)
        return model_path, serializer_config.encoding

    @staticmethod
    def with_import(module_name: str, func: Callable[[Any], Any], error_msg: str) -> Any:
        try:
            module = __import__(module_name)
            return func(module)
        except ImportError:
            raise ImportError(error_msg)

    def get_dependencies(self) -> Optional[List[str]]:
        assert self.model_type is not None, "Could not determine model type. Please set parameter: model_type."
        return (MODEL_SERIALIZERS[self.model_type].dependency_fn or (lambda: None))()

    def cleanup(self):
        import shutil

        for temp_path in self._temp_files:
            try:
                if os.path.isfile(temp_path):
                    os.remove(temp_path)
                elif os.path.isdir(temp_path):
                    shutil.rmtree(temp_path)
                temp_dir = os.path.dirname(temp_path)
                if temp_dir and os.path.exists(temp_dir) and temp_dir.startswith(tempfile.gettempdir()):
                    shutil.rmtree(temp_dir)
            except Exception:
                pass
        self._temp_files.clear()

    @staticmethod
    def fileinfo_to_protobuf(file_info: FileInfo) -> ModelFile:
        return ModelFile(name=file_info.name, size_kb=file_info.size_kb, file_hash=file_info.file_hash)

    @staticmethod
    def protobuf_to_fileinfo(model_file: ModelFile) -> FileInfo:
        return FileInfo(name=model_file.name, size_kb=model_file.size_kb, file_hash=model_file.file_hash)

    @staticmethod
    def convert_metadata_to_protobuf(metadata: Optional[Mapping[str, Any]]) -> Optional[Mapping[str, struct_pb2.Value]]:
        metadata_converted: Mapping[str, struct_pb2.Value] = {}
        if metadata is not None:
            for k, v in metadata.items():
                converted_v = struct_pb2.Value()
                if isinstance(v, str):
                    converted_v.string_value = v
                elif isinstance(v, (int, float)):
                    converted_v.number_value = v
                elif isinstance(v, bool):
                    converted_v.bool_value = v
                else:
                    raise ValueError(
                        f"Unable to parse metadata field: `{k}:{v}`. "
                        + f"{type(v).__name__} is not currently supported."
                    )
                metadata_converted[k] = converted_v
        return metadata_converted

    def infer_input_output_schemas(
        self, model: Optional[Any] = None, model_type: Optional[ModelType] = None
    ) -> Tuple[Optional[ModelSchemaType], Optional[ModelSchemaType]]:
        if model is None:
            model = self.model

        if model_type is None:
            assert self.model_type is not None, "Could not determine model type. Please set parameter: model_type."
            model_type = self.model_type

        serializer_config = MODEL_SERIALIZERS[model_type]
        if serializer_config.schema_fn:
            return serializer_config.schema_fn(model)
        else:
            return None, None

    def pickle_object(self, object: Any, object_name: str) -> str:
        tmp_dir = tempfile.mkdtemp()
        tmp_file_path = os.path.join(tmp_dir, f"{object_name}.pkl")

        with open(tmp_file_path, "wb") as file:
            pickle.dump(object, file)

        self._temp_files.append(tmp_file_path)

        return tmp_file_path

    @staticmethod
    def build_tabular_schema(column_dtypes: Mapping[str, Any]) -> _model_artifact_pb2.TabularSchema:
        import pyarrow as pa

        from chalk.features._encoding.converter import PrimitiveFeatureConverter

        tabular_schema = _model_artifact_pb2.TabularSchema()

        for col_name, dtype in column_dtypes.items():
            if not isinstance(dtype, pa.DataType):
                if dtype == str:
                    pa_dtype = pa.string()
                elif dtype == int:
                    pa_dtype = pa.int64()
                elif dtype == float:
                    pa_dtype = pa.float64()
                elif dtype == bool:
                    pa_dtype = pa.bool_()
                else:
                    raise ValueError(f"Unsupported dtype {dtype} for column {col_name}")
            else:
                pa_dtype = dtype

            proto_arrow_type = PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(pa_dtype)

            column_spec = _model_artifact_pb2.TabularSpec(name=col_name, dtype=proto_arrow_type)

            tabular_schema.columns.append(column_spec)

        return tabular_schema

    @staticmethod
    def build_tensor_schema(tensor_specs: ModelSchemaType) -> _model_artifact_pb2.TensorSchema:
        import pyarrow as pa

        from chalk.features._encoding.converter import PrimitiveFeatureConverter

        tensor_schema = _model_artifact_pb2.TensorSchema()

        for shape, dtype in tensor_specs:
            # Handle Chalk Tensor types
            if hasattr(dtype, "__mro__") and any("Tensor" in base.__name__ for base in dtype.__mro__):
                # Extract shape and dtype from Tensor type
                if hasattr(dtype, "shape") and hasattr(dtype, "dtype"):
                    shape = dtype.shape
                    pa_dtype = dtype.dtype
                else:
                    raise ValueError(f"Tensor type is missing shape or dtype attributes")
            elif not isinstance(dtype, pa.DataType):
                if dtype == str:
                    pa_dtype = pa.string()
                elif dtype == int:
                    pa_dtype = pa.int64()
                elif dtype == float:
                    pa_dtype = pa.float64()
                elif dtype == bool:
                    pa_dtype = pa.bool_()
                else:
                    raise ValueError(f"Unsupported dtype {dtype} for tensor")
            else:
                pa_dtype = dtype

            proto_arrow_type = PrimitiveFeatureConverter.convert_pa_dtype_to_proto_dtype(pa_dtype)

            tensor_spec = _model_artifact_pb2.TensorSpec(
                dtype=proto_arrow_type, shape=[_model_artifact_pb2.TensorDimension(fixed=dim) for dim in shape]
            )

            tensor_schema.tensors.append(tensor_spec)

        return tensor_schema

    @staticmethod
    def convert_onnx_list_schema_to_dict(schema: Any, model: Any, is_input: bool = True) -> Any:
        """Convert list-based schema to dict-based schema for ONNX models.

        Args:
            schema: The schema (list or dict)
            model: The ONNX model (ModelProto or wrapped)
            is_input: True for input schema, False for output schema

        Returns:
            Dict-based schema with field names from ONNX model
        """
        if not isinstance(schema, list):
            return schema

        try:
            import onnx  # type: ignore[reportMissingImports]
        except ImportError:
            raise ValueError("onnx package is required to convert list schemas for ONNX models")

        # Unwrap model if needed
        onnx_model = model._model if hasattr(model, "_model") else model

        if not isinstance(onnx_model, onnx.ModelProto):
            raise ValueError(
                f"ONNX models must be registered with tabular schema (dict format). "
                + f"Use dict format like {{'input': Tensor[...]}} instead of list format."
            )

        # Get input/output names from ONNX model
        if is_input:
            names = [inp.name for inp in onnx_model.graph.input]
            schema_type = "input"
        else:
            names = [out.name for out in onnx_model.graph.output]
            schema_type = "output"

        if len(names) != len(schema):
            raise ValueError(f"ONNX model has {len(names)} {schema_type}s but schema has {len(schema)} entries")

        # Convert to dict format
        return {name: spec for name, spec in zip(names, schema)}

    @staticmethod
    def convert_schema(schema: Any) -> Optional[_model_artifact_pb2.ModelSchema]:
        model_schema = _model_artifact_pb2.ModelSchema()
        if schema is not None:
            if isinstance(schema, dict):
                # Convert Tensor/Vector types to their PyArrow types for tabular schema
                converted_schema = {}
                for col_name, dtype in schema.items():
                    if hasattr(dtype, "__mro__") and any("Tensor" in base.__name__ for base in dtype.__mro__):
                        # Use Tensor's to_pyarrow_dtype() method to convert to Arrow type
                        if hasattr(dtype, "to_pyarrow_dtype"):
                            converted_schema[col_name] = dtype.to_pyarrow_dtype()
                        else:
                            raise ValueError(f"Tensor type for '{col_name}' is missing to_pyarrow_dtype method")
                    elif hasattr(dtype, "__mro__") and any("Vector" in base.__name__ for base in dtype.__mro__):
                        # Vector already has a .dtype attribute that's a PyArrow type
                        if hasattr(dtype, "dtype"):
                            converted_schema[col_name] = dtype.dtype
                        else:
                            raise ValueError(f"Vector type for '{col_name}' is missing dtype attribute")
                    else:
                        converted_schema[col_name] = dtype

                model_schema.tabular.CopyFrom(ModelSerializer.build_tabular_schema(converted_schema))
            elif isinstance(schema, list):
                model_schema.tensor.CopyFrom(ModelSerializer.build_tensor_schema(schema))
            else:
                raise ValueError(f"Invalid schema: {schema}")
        else:
            raise ValueError(f"Invalid empty schema.")

        return model_schema

    @staticmethod
    def convert_run_criterion_to_proto(
        run_id: Optional[str] = None, run_name: Optional[str] = None, criterion: Optional[ModelRunCriterion] = None
    ) -> Optional[RunCriterion]:
        if run_id is None and run_name is None:
            raise ValueError("Please specify either run_id or run_name.")

        if criterion is None:
            return RunCriterion(run_id=run_id, run_name=run_name)

        if criterion.direction == "max":
            return RunCriterion(
                run_id=run_id,
                run_name=run_name,
                metric=criterion.metric,
                direction=RunCriterionDirection.RUN_CRITERION_DIRECTION_MAX,
            )
        elif criterion.direction == "min":
            return RunCriterion(
                run_id=run_id,
                run_name=run_name,
                metric=criterion.metric,
                direction=RunCriterionDirection.RUN_CRITERION_DIRECTION_MIN,
            )
        else:
            raise ValueError(
                f"Unable to create model training run criterion. Unrecognized direction: {criterion.direction}."
            )
