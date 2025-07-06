from pathlib import Path
from typing import Optional, Dict
from fnmatch import fnmatch
from typing import TYPE_CHECKING

from sentence_transformers import SentenceTransformer
from canonmap.utils.logger import setup_logger
from canonmap.config.utils.embedder import Embedder

if TYPE_CHECKING:
    from canonmap.config.validate_configs import (
        CanonMapEmbeddingConfig,
        CanonMapArtifactsConfig,
    )
from canonmap.config.utils.gcs import download_from_gcs, upload_to_gcs

logger = setup_logger(__name__)

# --- Embedding loader -------------------------------------------------------

REQUIRED_EMBEDDING_FILES = [
    "config.json",
    "sentence_bert_config.json",
    "tokenizer.json",
    "vocab.txt",
    "special_tokens_map.json",
    "tokenizer_config.json",
    "modules.json",
    "README.md",
]
EMBED_MODEL_PATTERNS = ["model.safetensors", "pytorch_model.bin"]

def _validate_embedding_files(local_dir: Path) -> Dict[str, bool]:
    status = {name: (local_dir / name).is_file() for name in REQUIRED_EMBEDDING_FILES}
    status["model_file"] = any((local_dir / pat).is_file() for pat in EMBED_MODEL_PATTERNS)
    return status

def get_embedder(
    config: "CanonMapEmbeddingConfig",
    api_mode: bool = False
) -> Optional[Embedder]:
    #1. Local path (if exists)
    local_dir = Path(config.embedding_model_local_path)
    state = _validate_embedding_files(local_dir) if local_dir.exists() else {}
    if local_dir.exists() and all(state.values()):
        try:
            return Embedder(model_name=str(local_dir))
        except Exception as e:
            logger.warning("Embedder load from local failed: %s", e)

    #2. GCS sync (only if gcs_config is provided)
    if config.gcs_config:
        if not api_mode:
            config.gcs_config.validate_bucket()

        strat = config.embedding_model_gcp_sync_strategy.lower()
        service_account_json_path = config.embedding_model_gcp_service_account_json_path
        bucket = config.embedding_model_gcp_bucket_name
        prefix = config.embedding_model_gcp_bucket_prefix

        ok = False
        if strat == "overwrite":
            upload_to_gcs(service_account_json_path, bucket, prefix, local_dir)
            ok = download_from_gcs(service_account_json_path, bucket, prefix, local_dir) > 0
        elif strat == "refresh":
            ok = download_from_gcs(service_account_json_path, bucket, prefix, local_dir) > 0
        elif strat == "missing":
            ok = (download_from_gcs(service_account_json_path, bucket, prefix, local_dir) > 0
                    or upload_to_gcs(service_account_json_path, bucket, prefix, local_dir) > 0)

        if ok:
            try:
                return Embedder(model_name=str(local_dir))
            except Exception as e:
                logger.warning("Embedder load after GCS sync failed: %s", e)

    #3. HF fallback
    try:
        logger.info("📥 HF download: %s → %s", config.embedding_model_hf_name, local_dir)
        local_dir.mkdir(parents=True, exist_ok=True)
        model = SentenceTransformer(config.embedding_model_hf_name, cache_folder=str(local_dir))
        model.save(str(local_dir))
        if config.gcs_config and config.embedding_model_gcp_bucket_name:
            upload_to_gcs(
                config.embedding_model_gcp_service_account_json_path,
                config.embedding_model_gcp_bucket_name,
                config.embedding_model_gcp_bucket_prefix,
                local_dir
            )
        return Embedder(model_name=str(local_dir))
    except Exception as e:
        logger.error("HF fallback failed: %s", e)
        return None


# --- Artifacts loader -------------------------------------------------------

REQUIRED_ARTIFACT_PATTERNS = [
    "*_schema.pkl",
    "*_canonical_entities.pkl",
    "*_canonical_entity_embeddings.npz",
]

def _validate_artifacts(local_dir: Path) -> Dict[str, bool]:
    files = [p.name for p in local_dir.rglob("*") if p.is_file()]
    return {pat: any(fnmatch(name, pat) for name in files)
            for pat in REQUIRED_ARTIFACT_PATTERNS}

def get_artifacts_dir(
    config: "CanonMapArtifactsConfig",
    api_mode: bool = False
) -> Optional[Path]:
    #1. Local path (if exists)
    local_dir = Path(config.artifacts_local_path)
    state = _validate_artifacts(local_dir) if local_dir.exists() else {}
    if local_dir.exists() and all(state.values()):
        return True

    #2. GCS sync (only if gcs_config is provided)
    if config.gcs_config:
        if not api_mode:
            config.gcs_config.validate_bucket()

        strat = config.artifacts_gcp_sync_strategy.lower()
        service_account_json_path = config.artifacts_gcp_service_account_json_path
        bucket = config.artifacts_gcp_bucket_name
        prefix = config.artifacts_gcp_bucket_prefix

        ok = False
        if strat == "overwrite":
            upload_to_gcs(service_account_json_path, bucket, prefix, local_dir)
            ok = download_from_gcs(service_account_json_path, bucket, prefix, local_dir) > 0
        elif strat == "refresh":
            ok = download_from_gcs(service_account_json_path, bucket, prefix, local_dir) > 0
        elif strat == "missing":
            ok = (download_from_gcs(service_account_json_path, bucket, prefix, local_dir) > 0
                    or upload_to_gcs(service_account_json_path, bucket, prefix, local_dir) > 0)

        #3. Return local dir if all artifacts are present
        if ok:
            state = _validate_artifacts(local_dir)
            if all(state.values()):
                return True
            else:
                missing = [p for p, ok in state.items() if not ok]
                logger.warning("After GCS sync, still missing artifacts: %s", missing)

    if config.gcs_config:
        logger.warning("Artifacts directory is incomplete both locally and in GCS, missing patterns: %s", [p for p, ok in state.items() if not ok])
    else:
        logger.warning("Artifacts directory is incomplete locally, missing patterns: %s", [p for p, ok in state.items() if not ok])

    return False