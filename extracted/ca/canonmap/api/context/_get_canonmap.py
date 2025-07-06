from canonmap import (
    CanonMap,
    CanonMapEmbeddingConfig,
    CanonMapArtifactsConfig,
    CanonMapGCPConfig,
    CanonMapCustomGCSConfig,
)

def get_canonmap():
    # 1) base GCP key + global troubleshooting flag
    base_gcp = CanonMapGCPConfig(
        gcp_service_account_json_path="dev_service_account.json",
        troubleshooting=True,
    )
    
    # 2) one CustomGCSConfig per bucket use
    artifacts_gcs = CanonMapCustomGCSConfig(
        gcp_config=base_gcp,
        bucket_name="keenai-test-bucket",
        bucket_prefix="artifacts",
        auto_create_bucket=True,
        auto_create_bucket_prefix=True,
        sync_strategy="refresh",
    )

    embedding_gcs = CanonMapCustomGCSConfig(
        gcp_config=base_gcp,
        bucket_name="keenai-test-bucket",
        bucket_prefix="models/sentence-transformers/all-MiniLM-L12-v2",
        auto_create_bucket=True,
        auto_create_bucket_prefix=True,
        sync_strategy="refresh",
    )

    # 3) application-specific configs
    artifacts_config = CanonMapArtifactsConfig(
        artifacts_local_path="artifacts",
        gcs_config=artifacts_gcs,
    )

    embedding_config = CanonMapEmbeddingConfig(
        embedding_model_hf_name="sentence-transformers/all-MiniLM-L12-v2",
        embedding_model_local_path="models/sentence-transformers/all-MiniLM-L12-v2",
        gcs_config=embedding_gcs,
    )

    # 4) build your CanonMap
    canonmap = CanonMap(
        artifacts_config=artifacts_config,
        embedding_config=embedding_config,
        verbose=True,
        api_mode=True,
    )

    return canonmap