import os
from dataclasses import dataclass
from enum import Enum
from functools import cache
from typing import Mapping, Tuple

import chalk._gen.chalk.models.v1.model_artifact_pb2 as pb
import chalk._gen.chalk.models.v1.model_version_pb2 as mv_pb

REGISTRY_METADATA_FILE = os.getenv("CHALK_MODEL_REGISTRY_METADATA_FILENAME", None)
CHALK_MODEL_REGISTRY_ROOT = os.getenv("CHALK_MODEL_REGISTRY_ROOT", "/models")


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
        if REGISTRY_METADATA_FILE is not None:
            with open(REGISTRY_METADATA_FILE, "rb") as f:
                mms.ParseFromString(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(f"Model registry metadata file not found: {REGISTRY_METADATA_FILE}")
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
