from canonmap import CanonMapGCPConfig, CanonMapCustomGCSConfig

base_gcp = CanonMapGCPConfig(
    gcp_service_account_json_path="<path_to_service_account.json>",
    troubleshooting=True,
)

artifacts_gcs = CanonMapCustomGCSConfig(
    gcp_config=base_gcp,
    bucket_name="<bucket_name>",
    bucket_prefix="<bucket_prefix>",
    auto_create_bucket=True,
    auto_create_bucket_prefix=True,
    sync_strategy="refresh",
)

embedding_gcs = CanonMapCustomGCSConfig(
    gcp_config=base_gcp,
    bucket_name="<bucket_name>",
    bucket_prefix="<bucket_prefix>",
    auto_create_bucket=True,
    auto_create_bucket_prefix=True,
    sync_strategy="refresh",
)