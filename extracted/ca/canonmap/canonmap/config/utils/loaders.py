from pathlib import Path
from typing import Optional, Dict
from fnmatch import fnmatch
from typing import TYPE_CHECKING
import os

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

def _find_model_in_cache(hf_model_name: str) -> Optional[Path]:
    """
    Check for the model in the user's home directory cache folders.
    Looks in .huggingface_hub and .sentence_transformers directories.
    """
    home_dir = Path.home()
    
    # Common cache locations
    cache_locations = [
        home_dir / ".huggingface_hub",
        home_dir / ".sentence_transformers",
        home_dir / ".cache" / "huggingface",
        home_dir / ".cache" / "sentence_transformers",
    ]
    
    # Extract model name from HF name (e.g., "sentence-transformers/all-MiniLM-L12-v2" -> "all-MiniLM-L12-v2")
    model_name = hf_model_name.split("/")[-1] if "/" in hf_model_name else hf_model_name
    
    # Create the HuggingFace cache directory name format
    hf_cache_name = f"models--{hf_model_name.replace('/', '--')}"
    
    for cache_dir in cache_locations:
        if not cache_dir.exists():
            continue
            
        # Look for the model in various possible subdirectories
        possible_paths = [
            cache_dir / hf_model_name,
            cache_dir / model_name,
            cache_dir / "models" / hf_model_name,
            cache_dir / "models" / model_name,
            # Handle sentence-transformers specific structure
            cache_dir / "sentence-transformers" / model_name,
            cache_dir / "sentence-transformers" / hf_model_name,
            # Handle HuggingFace cache structure (hub directory)
            cache_dir / "hub" / hf_cache_name,
        ]
        
        for model_path in possible_paths:
            if model_path.exists():
                # For HuggingFace cache, we need to look in the snapshots subdirectory
                if "hub" in str(model_path) and model_path.is_dir():
                    # Look for the latest snapshot
                    snapshots_dir = model_path / "snapshots"
                    if snapshots_dir.exists():
                        # Get the latest snapshot (usually the first one)
                        snapshots = [d for d in snapshots_dir.iterdir() if d.is_dir()]
                        if snapshots:
                            latest_snapshot = snapshots[0]  # Usually the first one is the latest
                            state = _validate_embedding_files(latest_snapshot)
                            if all(state.values()):
                                logger.info(f"Found model in HF cache: {latest_snapshot}")
                                return latest_snapshot
                else:
                    # Validate that it's a complete model
                    state = _validate_embedding_files(model_path)
                    if all(state.values()):
                        logger.info(f"Found model in cache: {model_path}")
                        return model_path
                    else:
                        logger.debug(f"Model found in cache but incomplete: {model_path}")
        
        # Also check for models in subdirectories recursively (for more complex cache structures)
        try:
            for subdir in cache_dir.rglob("*"):
                if subdir.is_dir() and (model_name in subdir.name or hf_model_name.replace("/", "_") in subdir.name):
                    state = _validate_embedding_files(subdir)
                    if all(state.values()):
                        logger.info(f"Found model in cache subdirectory: {subdir}")
                        return subdir
        except (PermissionError, OSError) as e:
            logger.debug(f"Could not search subdirectories in {cache_dir}: {e}")
    
    return None

def get_embedder(
    config: "CanonMapEmbeddingConfig",
    api_mode: bool = False
) -> Optional[Embedder]:
    #0. Check user's home directory cache first (if enabled)
    if config.prioritize_cache:
        logger.info("Checking user's home directory cache for model...")
        cached_model_path = _find_model_in_cache(config.embedding_model_hf_name)
        if cached_model_path:
            try:
                logger.info(f"✅ Using cached model from: {cached_model_path}")
                return Embedder(model_name=str(cached_model_path))
            except Exception as e:
                logger.warning("❌ Embedder load from cache failed: %s", e)

    #1. Local path (if exists)
    logger.info("Checking local path for model...")
    local_dir = Path(config.embedding_model_local_path)
    state = _validate_embedding_files(local_dir) if local_dir.exists() else {}
    if local_dir.exists() and all(state.values()):
        try:
            logger.info(f"✅ Using local model from: {local_dir}")
            return Embedder(model_name=str(local_dir))
        except Exception as e:
            logger.warning("❌ Embedder load from local failed: %s", e)

    #2. GCS sync (only if gcs_config is provided)
    if config.gcs_config:
        logger.info("Checking GCS for model...")
        if not api_mode:
            config.gcs_config.validate_bucket()

        strat = config.embedding_model_gcp_sync_strategy.lower()
        service_account_json_path = config.embedding_model_gcp_service_account_json_path
        bucket = config.embedding_model_gcp_bucket_name
        prefix = config.embedding_model_gcp_bucket_prefix

        ok = False
        if strat == "overwrite":
            logger.info(f"GCS strategy 'overwrite': uploading then downloading from {bucket}/{prefix}")
            upload_to_gcs(service_account_json_path, bucket, prefix, local_dir)
            ok = download_from_gcs(service_account_json_path, bucket, prefix, local_dir) > 0
        elif strat == "refresh":
            logger.info(f"GCS strategy 'refresh': downloading from {bucket}/{prefix}")
            ok = download_from_gcs(service_account_json_path, bucket, prefix, local_dir) > 0
        elif strat == "missing":
            logger.info(f"GCS strategy 'missing': checking {bucket}/{prefix}")
            ok = (download_from_gcs(service_account_json_path, bucket, prefix, local_dir) > 0
                    or upload_to_gcs(service_account_json_path, bucket, prefix, local_dir) > 0)

        if ok:
            try:
                logger.info(f"✅ Using model from GCS: {local_dir}")
                return Embedder(model_name=str(local_dir))
            except Exception as e:
                logger.warning("❌ Embedder load after GCS sync failed: %s", e)
        else:
            logger.warning("❌ GCS sync failed or no files found")
    else:
        logger.info("No GCS config provided, skipping GCS check")

    #3. HF fallback (only if no GCS config or GCS sync failed)
    logger.info("Falling back to HuggingFace download...")
    try:
        logger.info("📥 HF download: %s → %s", config.embedding_model_hf_name, local_dir)
        local_dir.mkdir(parents=True, exist_ok=True)
        model = SentenceTransformer(config.embedding_model_hf_name, cache_folder=str(local_dir))
        model.save(str(local_dir))
        if config.gcs_config and config.embedding_model_gcp_bucket_name:
            logger.info("Uploading downloaded model to GCS...")
            upload_to_gcs(
                config.embedding_model_gcp_service_account_json_path,
                config.embedding_model_gcp_bucket_name,
                config.embedding_model_gcp_bucket_prefix,
                local_dir
            )
        logger.info(f"✅ Using downloaded model from: {local_dir}")
        return Embedder(model_name=str(local_dir))
    except Exception as e:
        logger.error("❌ HF fallback failed: %s", e)
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