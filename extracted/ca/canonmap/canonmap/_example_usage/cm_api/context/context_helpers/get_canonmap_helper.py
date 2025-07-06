from canonmap import CanonMap, CanonMapEmbeddingConfig, CanonMapArtifactsConfig

from canonmap._example_usage.cm_api.utils.api_logger import setup_logger
from canonmap._example_usage.cm_api.context.context_helpers.gcp_gcs_configs import artifacts_gcs, embedding_gcs

logger = setup_logger(__name__)

def get_canonmap():

    artifacts_config = CanonMapArtifactsConfig(
        artifacts_local_path="artifacts",
        # gcs_config=artifacts_gcs,
    )

    embedding_config = CanonMapEmbeddingConfig(
        embedding_model_hf_name="sentence-transformers/all-MiniLM-L12-v2",
        embedding_model_local_path="models",
        # gcs_config=embedding_gcs,
    )

    canonmap = CanonMap(
        artifacts_config=artifacts_config,
        embedding_config=embedding_config,
        verbose=True,
        api_mode=True,
    )


    logger.success("✅ CanonMap successfully initialized...")
    return canonmap