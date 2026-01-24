import os
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Literal, Mapping, Optional, Tuple

import pyarrow as pa

import chalk._gen.chalk.models.v1.model_artifact_pb2 as pb
import chalk._gen.chalk.models.v1.model_version_pb2 as mv_pb


def get_registry_metadata_file() -> Optional[str]:
    branch_root = os.getenv("CHALK_MODEL_REGISTRY_BRANCH_METADATA_ROOT", None)
    if os.getenv("IS_BRANCH", None) is not None and branch_root is not None:
        return os.path.join(branch_root, os.getenv("CHALK_DEPLOYMENT_ID", "") + ".bin")
    return os.getenv("CHALK_MODEL_REGISTRY_METADATA_FILENAME", None)


CHALK_MODEL_REGISTRY_ROOT = os.getenv("CHALK_MODEL_REGISTRY_ROOT", "/models")

MODEL_METADATA_PREFIX = "__chalk_model__"

MODEL_TRAIN_METADATA_RUN_NAME = f"{MODEL_METADATA_PREFIX}run_name__"
MODEL_TRAIN_RUN_NAME_ENV_VAR = "CHALK_MODEL_TRAIN_RUN_NAME"

MODEL_TRAIN_METADATA_RUN_ID = f"{MODEL_METADATA_PREFIX}run_id__"


def get_model_metadata_run_name_from_env():
    return os.getenv(MODEL_TRAIN_RUN_NAME_ENV_VAR, "")


class ModelType(str, Enum):
    PYTORCH = "MODEL_TYPE_PYTORCH"
    SKLEARN = "MODEL_TYPE_SKLEARN"
    TENSORFLOW = "MODEL_TYPE_TENSORFLOW"
    XGBOOST = "MODEL_TYPE_XGBOOST"
    LIGHTGBM = "MODEL_TYPE_LIGHTGBM"
    CATBOOST = "MODEL_TYPE_CATBOOST"
    ONNX = "MODEL_TYPE_ONNX"


class ModelEncoding(str, Enum):
    PICKLE = "MODEL_ENCODING_PICKLE"
    JOBLIB = "MODEL_ENCODING_JOBLIB"
    JSON = "MODEL_ENCODING_JSON"
    TEXT = "MODEL_ENCODING_TEXT"
    HDF5 = "MODEL_ENCODING_HDF5"
    PROTOBUF = "MODEL_ENCODING_PROTOBUF"
    CBM = "MODEL_ENCODING_CBM"
    SAFETENSOR = "MODEL_ENCODING_SAFETENSORS"


class ModelClass(str, Enum):
    CLASSIFICATION = "classification"
    REGRESSION = "regression"
    CLUSTERING = "clustering"
    DIMENSIONALITY_REDUCTION = "dimensionality_reduction"
    EMBEDDING = "embedding"


@dataclass
class ModelRunCriterion:
    direction: Literal["max", "min"]
    metric: str


@dataclass
class LoadedModel:
    spec: pb.ModelArtifactSpec
    model_path: str


def get_model_path(spec: mv_pb.MountedVersionSpecs) -> str:
    if len(spec.spec.model_files) == 0:
        raise ValueError(f"Invalid model spec for {spec.model_name}: has no model files.")
    return os.path.join(CHALK_MODEL_REGISTRY_ROOT, spec.model_artifact_filename, spec.spec.model_files[0].name)


@cache
def load_model_map() -> Mapping[Tuple[str, str], LoadedModel]:
    mms = mv_pb.MountedModelsSpecs()
    model_map: dict[Tuple[str, str], LoadedModel] = {}

    try:
        registry_metadata_file = get_registry_metadata_file()
        if registry_metadata_file is not None:
            with open(registry_metadata_file, "rb") as f:
                mms.ParseFromString(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"Model registry metadata file not found: {registry_metadata_file}")
    except Exception as e:
        raise RuntimeError(f"Failed to load model map: {e}")

    for spec in mms.specs:
        for identifier in spec.identifiers:
            model_map[(spec.model_name, f"version_{identifier.version}")] = LoadedModel(
                spec=spec.spec, model_path=get_model_path(spec)
            )

            if identifier.alias != "":
                model_map[(spec.model_name, f"alias_{identifier.alias}")] = LoadedModel(
                    spec=spec.spec, model_path=get_model_path(spec)
                )

            if identifier.as_of.seconds != 0:
                model_map[(spec.model_name, f"asof_{identifier.as_of.seconds}")] = LoadedModel(
                    spec=spec.spec, model_path=get_model_path(spec)
                )
    return model_map


def get_model_spec(model_name: str, identifier: str) -> LoadedModel:
    mms = load_model_map()
    if (spec := mms.get((model_name, identifier), None)) is None:
        raise ValueError(f"Model '{model_name}, {identifier}' not found in mounted models.")
    return spec


def model_type_from_proto(mt: pb.ModelType) -> ModelType:
    mapping = {
        pb.ModelType.MODEL_TYPE_PYTORCH: ModelType.PYTORCH,
        pb.ModelType.MODEL_TYPE_SKLEARN: ModelType.SKLEARN,
        pb.ModelType.MODEL_TYPE_TENSORFLOW: ModelType.TENSORFLOW,
        pb.ModelType.MODEL_TYPE_XGBOOST: ModelType.XGBOOST,
        pb.ModelType.MODEL_TYPE_LIGHTGBM: ModelType.LIGHTGBM,
        pb.ModelType.MODEL_TYPE_CATBOOST: ModelType.CATBOOST,
        pb.ModelType.MODEL_TYPE_ONNX: ModelType.ONNX,
    }
    _mt = mapping.get(mt, None)
    if _mt is None:
        raise ValueError(f"Unsupported model type: {mt}")
    return _mt


def model_encoding_from_proto(me: pb.ModelEncoding) -> ModelEncoding:
    mapping = {
        pb.ModelEncoding.MODEL_ENCODING_PICKLE: ModelEncoding.PICKLE,
        pb.ModelEncoding.MODEL_ENCODING_JOBLIB: ModelEncoding.JOBLIB,
        pb.ModelEncoding.MODEL_ENCODING_JSON: ModelEncoding.JSON,
        pb.ModelEncoding.MODEL_ENCODING_TEXT: ModelEncoding.TEXT,
        pb.ModelEncoding.MODEL_ENCODING_HDF5: ModelEncoding.HDF5,
        pb.ModelEncoding.MODEL_ENCODING_PROTOBUF: ModelEncoding.PROTOBUF,
        pb.ModelEncoding.MODEL_ENCODING_CBM: ModelEncoding.CBM,
        pb.ModelEncoding.MODEL_ENCODING_SAFETENSORS: ModelEncoding.SAFETENSOR,
    }
    _me = mapping.get(me, None)
    if _me is None:
        raise ValueError(f"Unsupported model encoding: {me}")
    return _me


from typing import Any, List, Optional, Tuple


class ModelAttributeExtractor:
    @staticmethod
    def infer_pytorch_schemas(
        model: Any,
    ) -> Tuple[Optional[List[Tuple[List[int], Any]]], Optional[List[Tuple[List[int], Any]]]]:
        input_schema: Optional[List[Tuple[List[int], Any]]] = None
        output_schema: Optional[List[Tuple[List[int], Any]]] = None

        if hasattr(model, "modules"):
            try:
                first_layer = None
                last_layer = None

                for module in model.modules():
                    if hasattr(module, "in_features") or hasattr(module, "in_channels"):
                        if first_layer is None:
                            first_layer = module
                        last_layer = module

                if first_layer is not None:
                    input_shape: List[int] = []
                    if hasattr(first_layer, "in_features"):
                        input_shape = [first_layer.in_features]
                    elif hasattr(first_layer, "in_channels"):
                        input_shape = [first_layer.in_channels, 224, 224]

                    input_schema = [(input_shape, pa.float64())]

                if last_layer is not None:
                    output_shape: List[int] = []
                    if hasattr(last_layer, "out_features"):
                        output_shape = [last_layer.out_features]
                    elif hasattr(last_layer, "out_channels"):
                        output_shape = [last_layer.out_channels, 1, 1]

                    output_schema = [(output_shape, pa.float64())]
            except Exception:
                pass

        return input_schema, output_schema

    @staticmethod
    def infer_xgboost_schemas(
        model: Any,
    ) -> Tuple[Optional[List[Tuple[List[int], Any]]], Optional[List[Tuple[List[int], Any]]]]:
        input_schema: Optional[List[Tuple[List[int], Any]]] = None
        output_schema: Optional[List[Tuple[List[int], Any]]] = None

        try:
            n_features = None

            if hasattr(model, "n_features_in_"):
                n_features = model.n_features_in_
            elif hasattr(model, "feature_names_in_") and model.feature_names_in_ is not None:
                n_features = len(model.feature_names_in_)
            elif hasattr(model, "get_booster"):
                booster = model.get_booster()
                if hasattr(booster, "num_features"):
                    n_features = booster.num_features()
                elif hasattr(booster, "feature_names") and booster.feature_names:
                    n_features = len(booster.feature_names)

            if n_features is not None:
                input_schema = [([n_features], pa.float64())]

            if hasattr(model, "_estimator_type"):
                if model._estimator_type == "classifier":
                    n_classes = None
                    if hasattr(model, "n_classes_"):
                        n_classes = model.n_classes_
                    elif hasattr(model, "classes_") and model.classes_ is not None:
                        n_classes = len(model.classes_)

                    if n_classes is not None:
                        if n_classes == 2:
                            output_schema = [([1], pa.float64())]
                        else:
                            output_schema = [([n_classes], pa.float64())]
                    else:
                        output_schema = [([1], pa.float64())]

                elif model._estimator_type == "regressor":
                    n_outputs = 1
                    if hasattr(model, "n_outputs_"):
                        n_outputs = model.n_outputs_
                    output_schema = [([n_outputs], pa.float64())]

            else:
                output_schema = [([1], pa.float64())]

        except Exception:
            pass

        return input_schema, output_schema

    @staticmethod
    def infer_sklearn_schemas(
        model: Any,
    ) -> Tuple[Optional[List[Tuple[List[int], Any]]], Optional[List[Tuple[List[int], Any]]]]:
        input_schema: Optional[List[Tuple[List[int], Any]]] = None
        output_schema: Optional[List[Tuple[List[int], Any]]] = None

        try:
            n_features = None

            if hasattr(model, "n_features_in_"):
                n_features = model.n_features_in_
            elif hasattr(model, "feature_names_in_") and model.feature_names_in_ is not None:
                n_features = len(model.feature_names_in_)
            elif hasattr(model, "coef_") and model.coef_ is not None:
                if model.coef_.ndim == 1:
                    n_features = len(model.coef_)
                elif model.coef_.ndim == 2:
                    n_features = model.coef_.shape[1]
            elif hasattr(model, "support_vectors_") and model.support_vectors_ is not None:
                n_features = model.support_vectors_.shape[1]
            elif hasattr(model, "tree_") and hasattr(model.tree_, "n_features"):
                n_features = model.tree_.n_features
            elif hasattr(model, "estimators_") and model.estimators_ is not None and len(model.estimators_) > 0:
                first_estimator = model.estimators_[0]
                if hasattr(first_estimator, "n_features_in_"):
                    n_features = first_estimator.n_features_in_
                elif hasattr(first_estimator, "tree_") and hasattr(first_estimator.tree_, "n_features"):
                    n_features = first_estimator.tree_.n_features

            if n_features is not None:
                input_schema = [([n_features], pa.float64())]

            if hasattr(model, "_estimator_type"):
                if model._estimator_type == "classifier":
                    n_classes = None
                    if hasattr(model, "classes_") and model.classes_ is not None:
                        n_classes = len(model.classes_)
                    elif hasattr(model, "n_classes_"):
                        n_classes = model.n_classes_

                    if n_classes is not None:
                        if n_classes == 2:
                            output_schema = [([1], pa.float64())]
                        else:
                            output_schema = [([n_classes], pa.float64())]
                    else:
                        output_schema = [([1], pa.float64())]

                elif model._estimator_type == "regressor":
                    n_outputs = 1
                    if hasattr(model, "n_outputs_"):
                        n_outputs = model.n_outputs_
                    elif hasattr(model, "coef_") and model.coef_ is not None:
                        if model.coef_.ndim == 2:
                            n_outputs = model.coef_.shape[0]

                    output_schema = [([n_outputs], pa.float64())]

                elif model._estimator_type == "clusterer":
                    output_schema = [([1], pa.int64())]

                elif model._estimator_type == "transformer":
                    pass

            else:
                if hasattr(model, "predict_proba"):
                    output_schema = [([1], pa.float64())]
                elif hasattr(model, "predict"):
                    output_schema = [([1], pa.float64())]
                elif hasattr(model, "transform"):
                    pass

        except Exception:
            pass

        return input_schema, output_schema

    @staticmethod
    def infer_catboost_schemas(
        model: Any,
    ) -> Tuple[Optional[List[Tuple[List[int], Any]]], Optional[List[Tuple[List[int], Any]]]]:
        input_schema: Optional[List[Tuple[List[int], Any]]] = None
        output_schema: Optional[List[Tuple[List[int], Any]]] = None

        try:
            n_features = None

            # CatBoost uses feature_names_ or can query from get_feature_importance
            if hasattr(model, "feature_names_") and model.feature_names_ is not None:
                n_features = len(model.feature_names_)
            elif hasattr(model, "n_features_in_"):
                n_features = model.n_features_in_
            elif hasattr(model, "get_feature_importance"):
                # Try to get feature count from the model's tree structure
                try:
                    feature_importances = model.get_feature_importance()
                    if feature_importances is not None:
                        n_features = len(feature_importances)
                except Exception:
                    pass

            if n_features is not None:
                input_schema = [([n_features], pa.float64())]

            # Determine output schema based on model type
            # CatBoost has is_fitted() and can check the model type
            if hasattr(model, "_estimator_type"):
                if model._estimator_type == "classifier":
                    n_classes = None
                    if hasattr(model, "classes_") and model.classes_ is not None:
                        n_classes = len(model.classes_)

                    if n_classes is not None:
                        if n_classes == 2:
                            output_schema = [([1], pa.float64())]
                        else:
                            output_schema = [([n_classes], pa.float64())]
                    else:
                        output_schema = [([1], pa.float64())]

                elif model._estimator_type == "regressor":
                    output_schema = [([1], pa.float64())]
            else:
                # Check class name as fallback
                class_name = model.__class__.__name__
                if "Classifier" in class_name:
                    n_classes = None
                    if hasattr(model, "classes_") and model.classes_ is not None:
                        n_classes = len(model.classes_)

                    if n_classes is not None:
                        if n_classes == 2:
                            output_schema = [([1], pa.float64())]
                        else:
                            output_schema = [([n_classes], pa.float64())]
                    else:
                        output_schema = [([1], pa.float64())]
                elif "Regressor" in class_name:
                    output_schema = [([1], pa.float64())]
                else:
                    # Default to single output
                    output_schema = [([1], pa.float64())]

        except Exception:
            pass

        return input_schema, output_schema

    @staticmethod
    def infer_model_type(model: Any) -> Tuple[Optional[ModelType], Optional[ModelClass]]:
        # ONNX - check early since ONNX models are commonly wrapped
        try:
            import onnx  # pyright: ignore[reportMissingImports]

            if isinstance(model, onnx.ModelProto):
                return ModelType.ONNX, None
            # Check if model has a wrapped ONNX ModelProto (e.g., model._model)
            if hasattr(model, "_model") and isinstance(model._model, onnx.ModelProto):
                return ModelType.ONNX, None
        except ImportError:
            pass

        try:
            import onnxruntime  # pyright: ignore[reportMissingImports]

            if isinstance(model, onnxruntime.InferenceSession):
                return ModelType.ONNX, None
        except ImportError:
            pass

        # PYTORCH
        try:
            import torch.nn as nn  # pyright: ignore[reportMissingImports]

            if isinstance(model, nn.Module):
                return ModelType.PYTORCH, None
        except ImportError:
            pass

        # XGBOOST
        try:
            import xgboost as xgb  # pyright: ignore[reportMissingImports]

            if isinstance(model, xgb.XGBClassifier):
                return ModelType.XGBOOST, ModelClass.CLASSIFICATION
            if isinstance(model, xgb.XGBRegressor):
                return ModelType.XGBOOST, ModelClass.REGRESSION

            if isinstance(model, (xgb.XGBModel, xgb.Booster)):
                return ModelType.XGBOOST, None
            # Also check for XGBoost sklearn API
            if hasattr(model, "__class__") and "xgboost" in model.__class__.__module__:
                return ModelType.XGBOOST, None
        except ImportError:
            pass

        # LIGHTGBM
        try:
            import lightgbm as lgb  # pyright: ignore[reportMissingImports]

            if isinstance(model, (lgb.LGBMModel, lgb.Booster)):
                return ModelType.LIGHTGBM, None
            if hasattr(model, "__class__") and "lightgbm" in model.__class__.__module__:
                return ModelType.LIGHTGBM, None
        except ImportError:
            pass

        # CATBOOST
        try:
            import catboost as cb  # pyright: ignore[reportMissingImports]

            # Common CatBoost classes - check specific types first
            try:
                if isinstance(model, cb.CatBoostClassifier):
                    return ModelType.CATBOOST, ModelClass.CLASSIFICATION
                if isinstance(model, cb.CatBoostRegressor):
                    return ModelType.CATBOOST, ModelClass.REGRESSION

                if isinstance(model, (cb.CatBoost)):
                    return ModelType.CATBOOST, None
            except (AttributeError, NameError):
                pass
            # CatBoost has various model classes - generic fallback
            if hasattr(model, "__class__") and "catboost" in model.__class__.__module__:
                return ModelType.CATBOOST, None
        except ImportError:
            pass

        # SKLEARN
        try:
            import sklearn.base  # pyright: ignore[reportMissingImports]

            if isinstance(model, sklearn.base.BaseEstimator):
                return ModelType.SKLEARN, None

            if hasattr(model, "__class__") and "sklearn" in model.__class__.__module__:
                return ModelType.SKLEARN, None
        except ImportError:
            pass

        # TENSORFLOW
        try:
            import tensorflow as tf  # pyright: ignore[reportMissingImports]

            if isinstance(model, tf.keras.Model):
                return ModelType.TENSORFLOW, None
            if hasattr(model, "__class__") and "tensorflow" in model.__class__.__module__:
                return ModelType.TENSORFLOW, None
        except ImportError:
            pass

        return None, None
