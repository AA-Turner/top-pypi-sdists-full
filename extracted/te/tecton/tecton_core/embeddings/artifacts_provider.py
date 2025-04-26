from __future__ import annotations

import copy
import enum
import json
import os
import shutil
from dataclasses import dataclass
from functools import lru_cache
from logging import getLogger
from tempfile import TemporaryDirectory
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from urllib.request import urlretrieve

import boto3
from boto3.s3.transfer import S3Transfer
from boto3.s3.transfer import TransferConfig

from tecton_core import conf
from tecton_core.embeddings.file_utils import hash_file
from tecton_core.embeddings.model_artifacts import ModelArtifactProvider
from tecton_proto.common.id__client_pb2 import Id


S3_BUCKET = "tecton.ai.public"
AWS_REGION = "us-west-2"
ARCHIVE_FN = "model.tar.gz"
METADATA_FN = "metadata.json"

logger = getLogger(__name__)


class InferenceDeviceHardware(str, enum.Enum):
    CPU = "cpu"
    NVIDIA_T4 = "Tesla T4"
    NVIDIA_M60 = "Tesla M60"
    NVIDIA_V100_16GB = "Tesla V100-SXM2-16GB"
    NVIDIA_A10G = "NVIDIA A10G"
    NVIDIA_L4 = "NVIDIA L4"

    def __str__(self):
        return self.value


class TokenBudgetManager:
    def __init__(self, hardware_token_budget_map: Optional[Dict[InferenceDeviceHardware, int]] = None):  # noqa: ANN204
        if hardware_token_budget_map is None:
            hardware_token_budget_map = {}
        for k, v in hardware_token_budget_map.items():
            if not isinstance(k, InferenceDeviceHardware):
                msg = f"Key {k} is not an instance of InferenceDeviceHardware."
                raise ValueError(msg)
            if not isinstance(v, int) or v <= 0:
                msg = f"Value {v} must be an int greater than 0"
                raise ValueError(msg)
        self._hardware_token_budget_map = copy.deepcopy(hardware_token_budget_map)

    def get(self, hardware: InferenceDeviceHardware) -> Optional[int]:
        return self._hardware_token_budget_map.get(hardware)

    def set(self, hardware: InferenceDeviceHardware, token_budget: int) -> None:
        self._hardware_token_budget_map[hardware] = token_budget


CURRENT_ARTIFACTS = {
    "sentence-transformers/all-MiniLM-L6-v2": (
        "s3://tecton.ai.public/models/huggingface/sentence-transformers/all-MiniLM-L6-v2/e4ce987/1711700006",
        TokenBudgetManager(
            {
                InferenceDeviceHardware.CPU: 1000,
                InferenceDeviceHardware.NVIDIA_T4: 68_768,
                InferenceDeviceHardware.NVIDIA_M60: 12_800,
                InferenceDeviceHardware.NVIDIA_V100_16GB: 204_800,
                InferenceDeviceHardware.NVIDIA_A10G: 150_000,
            }
        ),
    ),
    "mixedbread-ai/mxbai-embed-large-v1": (
        "s3://tecton.ai.public/models/huggingface/mixedbread-ai/mxbai-embed-large-v1/456b7cf/1711697884",
        None,
    ),
    "BAAI/bge-large-en-v1.5": (
        "s3://tecton.ai.public/models/huggingface/BAAI/bge-large-en-v1.5/d4aa690/1711698014",
        None,
    ),
    "BAAI/bge-base-en-v1.5": (
        "s3://tecton.ai.public/models/huggingface/BAAI/bge-base-en-v1.5/a5beb1e/1711698489",
        None,
    ),
    "BAAI/bge-small-en-v1.5": (
        "s3://tecton.ai.public/models/huggingface/BAAI/bge-small-en-v1.5/5c38ec7/1711698601",
        None,
    ),
    "thenlper/gte-large": ("s3://tecton.ai.public/models/huggingface/thenlper/gte-large/5857861/1711699451", None),
    "thenlper/gte-base": ("s3://tecton.ai.public/models/huggingface/thenlper/gte-base/5e95d41/1711699488", None),
    "thenlper/gte-small": ("s3://tecton.ai.public/models/huggingface/thenlper/gte-small/50c7dd3/1711699502", None),
    "Snowflake/snowflake-arctic-embed-xs": (
        "s3://tecton.ai.public/models/huggingface/Snowflake/snowflake-arctic-embed-xs/86a0765/1713945940",
        None,
    ),
    "Snowflake/snowflake-arctic-embed-s": (
        " s3://tecton.ai.public/models/huggingface/Snowflake/snowflake-arctic-embed-s/1d03b2d/1713945950",
        None,
    ),
    "Snowflake/snowflake-arctic-embed-m": (
        "s3://tecton.ai.public/models/huggingface/Snowflake/snowflake-arctic-embed-m/2169d31/1713946149",
        None,
    ),
    "Snowflake/snowflake-arctic-embed-l": (
        "s3://tecton.ai.public/models/huggingface/Snowflake/snowflake-arctic-embed-l/c58efbc/1713946326",
        None,
    ),
    "intfloat/e5-large-unsupervised": (
        "s3://tecton.ai.public/models/huggingface/intfloat/e5-large-unsupervised/15af928/1713946911",
        None,
    ),
    "intfloat/e5-small-unsupervised": (
        "s3://tecton.ai.public/models/huggingface/intfloat/e5-small-unsupervised/b1dcdb2/1713947184",
        None,
    ),
    "intfloat/e5-base-unsupervised": (
        "s3://tecton.ai.public/models/huggingface/intfloat/e5-base-unsupervised/6003a5b/1713947222",
        None,
    ),
}


@dataclass
class ArtifactMetadata:
    model_id: str
    commit_hash: str
    created_at: str
    files: List[str]
    content_hashes: Dict[str, str]
    model_scan_results: Dict[str, Any]

    @staticmethod
    def from_json_file(metadata_file: str) -> ArtifactMetadata:
        with open(metadata_file, "r") as f:
            metadata = json.load(f)
            return ArtifactMetadata(
                model_id=metadata["model_id"],
                commit_hash=metadata["commit_hash"],
                created_at=metadata["created_at"],
                files=metadata["files"],
                content_hashes=metadata["content_hashes"],
                model_scan_results=metadata["model_scan_results"],
            )


class EmbeddingModelInfo:
    def __init__(
        self,
        hf_repo_id: str,
        s3_path: str,
        s3_bucket: str = S3_BUCKET,
        region: str = AWS_REGION,
        token_budget_manager: Optional[TokenBudgetManager] = None,
    ) -> None:
        self.hf_repo_id = hf_repo_id
        self.s3_path = s3_path
        self.s3_bucket = s3_bucket
        self.region = region
        self.__artifact_dir = s3_path.split(S3_BUCKET, 1)[-1]
        self.__http_url_base = f"https://s3.{AWS_REGION}.amazonaws.com/{S3_BUCKET}{self.__artifact_dir}"
        self.metadata_uri = f"{self.s3_path}/{METADATA_FN}"
        self.metadata_object_key = self.object_key_from_uri(self.metadata_uri)
        self.metadata_public_url = f"{self.__http_url_base}/{METADATA_FN}"
        self.model_uri = f"{self.s3_path}/{ARCHIVE_FN}"
        self.model_object_key = self.object_key_from_uri(self.model_uri)
        self.model_public_url = f"{self.__http_url_base}/{ARCHIVE_FN}"
        self.token_budget_manager = token_budget_manager or TokenBudgetManager()

    def get_token_budget(self, device: InferenceDeviceHardware) -> Optional[int]:
        return self.token_budget_manager.get(device)

    def set_token_budget(self, device: InferenceDeviceHardware, token_budget: int) -> None:
        self.token_budget_manager.set(device, token_budget)

    @staticmethod
    def object_key_from_uri(uri: str) -> str:
        return uri.split(S3_BUCKET, 1)[-1][1:]


class ArtifactsProvider:
    def __init__(self, artifact_s3_map: Optional[Dict[str, Tuple[str, TokenBudgetManager]]] = None):  # noqa: ANN204
        artifact_s3_map = CURRENT_ARTIFACTS if artifact_s3_map is None else artifact_s3_map
        self.artifacts = {
            k: EmbeddingModelInfo(k, s3_path, token_budget_manager=token_budget_manager)
            for k, (s3_path, token_budget_manager) in artifact_s3_map.items()
        }

    def get_model_info(self, hf_repo_id: str) -> Optional[EmbeddingModelInfo]:
        return self.artifacts.get(hf_repo_id)


ARTIFACT_PROVIDER = ArtifactsProvider()


def _verify_hashes(metadata: ArtifactMetadata, archive_dir: str) -> None:
    """
    Verify the hash of the model archive.
    """
    for file in metadata.files:
        fp = os.path.join(archive_dir, file)
        if not os.path.exists(fp):
            msg = f"File '{fp}' not found in model directory."
            raise FileNotFoundError(msg)
        actual_hash = hash_file(fp)
        if actual_hash != metadata.content_hashes[file]:
            msg = f"Hash of '{file}' does not match the expected hash."
            raise ValueError(msg)


@lru_cache()
def _get_s3_client():
    return boto3.client("s3")


# Currently `model_file_path` is only used for Custom Models
# TODO(EMBED-103): Consolidate the data model for open source and custom models
def _initialize_model_cache_dir(
    model_name: str, model_file_path: Optional[str] = None, force_overwrite: bool = False
) -> Tuple[str, bool]:
    model_cache_dir = os.path.join(conf.get_or_raise("MODEL_CACHE_DIRECTORY"), model_name)
    if not force_overwrite and (
        os.path.exists(os.path.join(model_cache_dir, METADATA_FN))
        or (model_file_path and os.path.exists(os.path.join(model_cache_dir, model_file_path)))
    ):
        logger.info("Model already exists in cache. Skipping download.")
        return model_cache_dir, True
    os.makedirs(model_cache_dir, exist_ok=True)
    return model_cache_dir, False


def retrieve_open_source_model_artifacts(model_name: str, use_http: bool = False) -> str:
    py_model_info = ARTIFACT_PROVIDER.get_model_info(model_name)
    if py_model_info is None:
        msg = f"Model '{model_name}' not found in the artifact provider."
        raise ValueError(msg)

    model_cache_dir, exist = _initialize_model_cache_dir(model_name)
    if exist:
        return model_cache_dir
    with TemporaryDirectory() as temp_dir:
        metadata_path = os.path.join(temp_dir, METADATA_FN)
        archive_path = os.path.join(temp_dir, ARCHIVE_FN)
        if use_http:
            urlretrieve(py_model_info.metadata_public_url, metadata_path)
            urlretrieve(py_model_info.model_public_url, archive_path)
        else:
            transfer_manager = S3Transfer(
                _get_s3_client(),
                config=TransferConfig(),
            )
            transfer_manager.download_file(py_model_info.s3_bucket, py_model_info.model_object_key, archive_path)
            transfer_manager.download_file(py_model_info.s3_bucket, py_model_info.metadata_object_key, metadata_path)
        metadata = ArtifactMetadata.from_json_file(metadata_path)
        shutil.unpack_archive(archive_path, temp_dir, format="gztar")
        _verify_hashes(metadata, temp_dir)
        for file in metadata.files:
            shutil.move(os.path.join(temp_dir, file), os.path.join(model_cache_dir, file))
        shutil.move(metadata_path, model_cache_dir)
    logger.info(f"Model '{model_name}': {os.listdir(model_cache_dir)} downloaded to '{model_cache_dir}'.")
    return model_cache_dir


def retrieve_custom_model_artifacts(
    model_name: str,
    model_artifact_id: Id,
    s3_path: str,
    model_file_path: str,
    model_artifact_provider: ModelArtifactProvider,
) -> str:
    model_cache_dir, exist = _initialize_model_cache_dir(model_name, model_file_path)
    if exist:
        return model_cache_dir
    with TemporaryDirectory() as temp_dir:
        temp_archive_file = os.path.join(temp_dir, ARCHIVE_FN)
        url = model_artifact_provider.get_presigned_url(s3_path=s3_path, model_artifact_id=model_artifact_id)
        urlretrieve(url, temp_archive_file)
        temp_model_dir = os.path.join(temp_dir, model_name)
        shutil.unpack_archive(temp_archive_file, temp_model_dir, format="gztar")
        for item in os.listdir(temp_model_dir):
            shutil.move(os.path.join(temp_model_dir, item), os.path.join(model_cache_dir, item))
    logger.info(f"Model '{model_name}': {os.listdir(model_cache_dir)} downloaded to '{model_cache_dir}'.")
    return model_cache_dir
