from typing import Optional

from canonmap.utils.logger import setup_logger
from canonmap.config.utils.gcp_validation import validate_service_account_path, validate_bucket_config

logger = setup_logger(__name__)


class CanonMapGCPConfig:
    """
    Base GCP configuration: just service account + troubleshooting flag.
    """
    def __init__(
        self,
        gcp_service_account_json_path: str,
        troubleshooting: bool = False,
    ):
        self.gcp_service_account_json_path = gcp_service_account_json_path
        self.troubleshooting = troubleshooting

    def validate_service_account(self):
        validate_service_account_path(self.gcp_service_account_json_path)


class CanonMapCustomGCSConfig:
    """
    Wraps a base GCP config with bucket-specific options:
      • bucket name (required)
      • prefix, auto-create flags, sync strategy (all optional)
      • inherits troubleshooting default from the base GCP config
    """
    def __init__(
        self,
        gcp_config: CanonMapGCPConfig,
        bucket_name: str,
        bucket_prefix: Optional[str] = None,
        auto_create_bucket: bool = False,
        auto_create_bucket_prefix: bool = False,
        sync_strategy: str = "none",  # "none", "missing", "overwrite", "refresh"
        troubleshooting: Optional[bool] = None,
    ):
        # pull in base service account + default troubleshoot flag
        self.gcp_service_account_json_path = gcp_config.gcp_service_account_json_path
        self.troubleshooting = (
            troubleshooting
            if troubleshooting is not None
            else gcp_config.troubleshooting
        )

        # bucket settings
        self.gcp_bucket_name = bucket_name
        self.gcp_bucket_prefix = bucket_prefix or ""
        self.auto_create_bucket = auto_create_bucket
        self.auto_create_bucket_prefix = auto_create_bucket_prefix
        self.sync_strategy = sync_strategy

    def validate_bucket(self, troubleshooting: bool = False):
        validate_bucket_config(self, troubleshooting or self.troubleshooting)


class CanonMapEmbeddingConfig:
    """
    Embedding model config: 
    • HF name + local path
    • a CustomGCSConfig for where to pull/push model files (optional)
    • optional troubleshooting override
    """
    def __init__(
        self,
        embedding_model_hf_name: str = "sentence-transformers/all-MiniLM-L12-v2",
        embedding_model_local_path: str = "models/sentence-transformers/all-MiniLM-L12-v2",
        gcs_config: Optional[CanonMapCustomGCSConfig] = None,
        troubleshooting: bool = False,
    ):
        self.embedding_model_hf_name = embedding_model_hf_name
        self.embedding_model_local_path = embedding_model_local_path
        self.gcs_config = gcs_config
        self.troubleshooting = troubleshooting

    @property
    def embedding_model_gcp_sync_strategy(self) -> str:
        return self.gcs_config.sync_strategy if self.gcs_config else "none"

    @property
    def embedding_model_gcp_service_account_json_path(self) -> str:
        return self.gcs_config.gcp_service_account_json_path if self.gcs_config else ""

    @property
    def embedding_model_gcp_bucket_name(self) -> str:
        return self.gcs_config.gcp_bucket_name if self.gcs_config else ""

    @property
    def embedding_model_gcp_bucket_prefix(self) -> str:
        return self.gcs_config.gcp_bucket_prefix if self.gcs_config else ""
    
    @property
    def embedding_model_gcp_auto_create_bucket(self) -> bool:
        return self.gcs_config.auto_create_bucket if self.gcs_config else False

    @property
    def embedding_model_gcp_auto_create_bucket_prefix(self) -> bool:
        return self.gcs_config.auto_create_bucket_prefix if self.gcs_config else False


class CanonMapArtifactsConfig:
    """
    Artifacts config:
    • local path
    • a CustomGCSConfig for bucket details (optional)
    • optional troubleshooting override
    """
    def __init__(
        self,
        artifacts_local_path: str,
        gcs_config: Optional[CanonMapCustomGCSConfig] = None,
        troubleshooting: bool = False,
    ):
        self.artifacts_local_path = artifacts_local_path
        self.gcs_config = gcs_config
        self.troubleshooting = troubleshooting

    @property
    def artifacts_gcp_sync_strategy(self) -> str:
        return self.gcs_config.sync_strategy if self.gcs_config else "none"

    @property
    def artifacts_gcp_service_account_json_path(self) -> str:
        return self.gcs_config.gcp_service_account_json_path if self.gcs_config else ""

    @property
    def artifacts_gcp_bucket_name(self) -> str:
        return self.gcs_config.gcp_bucket_name if self.gcs_config else ""

    @property
    def artifacts_gcp_bucket_prefix(self) -> str:
        return self.gcs_config.gcp_bucket_prefix if self.gcs_config else ""

    @property
    def artifacts_gcp_auto_create_bucket(self) -> bool:
        return self.gcs_config.auto_create_bucket if self.gcs_config else False

    @property
    def artifacts_gcp_auto_create_bucket_prefix(self) -> bool:
        return self.gcs_config.auto_create_bucket_prefix if self.gcs_config else False
    
















# from typing import Optional

# from canonmap.logger import setup_logger
# from canonmap.utils.gcp_validation import validate_service_account_path, validate_bucket_config
# from canonmap.utils.artifact_validation import validate_artifacts

# logger = setup_logger(__name__)


# class CanonMapGCPConfig:
#     def __init__(
#         self,
#         gcp_service_account_json_path: str,
#         gcp_bucket_name: str,
#         gcp_bucket_prefix: Optional[str] = None,
#         auto_create_bucket: bool = False,
#         auto_create_bucket_prefix: bool = False,
#         troubleshooting: bool = False,
#     ):
#         self.gcp_service_account_json_path = gcp_service_account_json_path
#         self.gcp_bucket_name = gcp_bucket_name
#         self.gcp_bucket_prefix = gcp_bucket_prefix or ""
#         self.auto_create_bucket = auto_create_bucket
#         self.auto_create_bucket_prefix = auto_create_bucket_prefix
#         self.troubleshooting = troubleshooting

#     def validate_service_account(self):
#         validate_service_account_path(self.gcp_service_account_json_path)

#     def validate_bucket(self, troubleshooting: bool = False):
#         validate_bucket_config(self, troubleshooting)


# class CanonMapEmbeddingConfig:
#     def __init__(
#         self,
#         embedding_model_hf_name: str = "sentence-transformers/all-MiniLM-L12-v2",
#         embedding_model_local_path: str = "models/sentence-transformers/all-MiniLM-L12-v2",
#         embedding_model_gcp_service_account_json_path: str = "",
#         embedding_model_gcp_bucket_name: Optional[str] = "canonmap-models",
#         embedding_model_gcp_bucket_prefix: Optional[str] = "models/sentence-transformers/all-MiniLM-L12-v2",
#         embedding_model_gcp_auto_create_bucket: bool = False,
#         embedding_model_gcp_auto_create_bucket_prefix: bool = False,
#         embedding_model_gcp_sync_strategy: str = "none",  # options: "none", "missing", "overwrite", "refresh"
#         troubleshooting: bool = False,
#     ):
#         self.embedding_model_hf_name = embedding_model_hf_name
#         self.embedding_model_local_path = embedding_model_local_path
#         self.embedding_model_gcp_service_account_json_path = embedding_model_gcp_service_account_json_path
#         self.embedding_model_gcp_bucket_name = embedding_model_gcp_bucket_name
#         self.embedding_model_gcp_bucket_prefix = embedding_model_gcp_bucket_prefix or ""
#         self.embedding_model_gcp_auto_create_bucket = embedding_model_gcp_auto_create_bucket
#         self.embedding_model_gcp_auto_create_bucket_prefix = embedding_model_gcp_auto_create_bucket_prefix
#         self.embedding_model_gcp_sync_strategy = embedding_model_gcp_sync_strategy
#         self.troubleshooting = troubleshooting

#     def upload_local_model_to_gcp(self):
#         # Import here to avoid circular dependency
#         from canonmap.utils.embedding_model_validation import upload_model_to_gcp
#         return upload_model_to_gcp(
#             self.embedding_model_local_path,
#             self.embedding_model_gcp_service_account_json_path,
#             self.embedding_model_gcp_bucket_name,
#             self.embedding_model_gcp_bucket_prefix,
#         )

#     def validate_embedding_model(self, troubleshooting: bool = False):
#         # Import here to avoid circular dependency
#         from canonmap.utils.embedding_model_validation import validate_model
#         return validate_model(
#             self.embedding_model_hf_name,
#             self.embedding_model_local_path,
#             self.embedding_model_gcp_service_account_json_path,
#             self.embedding_model_gcp_bucket_name,
#             self.embedding_model_gcp_bucket_prefix,
#             self.embedding_model_gcp_auto_create_bucket,
#             self.embedding_model_gcp_auto_create_bucket_prefix,
#             self.embedding_model_gcp_sync_strategy,
#             troubleshooting or self.troubleshooting,
#         )
    

# class CanonMapArtifactsConfig:
#     def __init__(
#         self,
#         artifacts_local_path: str,
#         artifacts_gcp_sync_strategy: str = "none",  # options: "none", "missing", "overwrite", "refresh"
#         artifacts_gcp_service_account_json_path: str = "",
#         artifacts_gcp_bucket_name: str = "",
#         artifacts_gcp_bucket_prefix: str = "",
#         artifacts_gcp_auto_create_bucket: bool = False,
#         artifacts_gcp_auto_create_bucket_prefix: bool = False,
#         troubleshooting: bool = False,
#     ):
#         self.artifacts_local_path = artifacts_local_path
#         self.artifacts_gcp_sync_strategy = artifacts_gcp_sync_strategy
#         self.artifacts_gcp_service_account_json_path = artifacts_gcp_service_account_json_path
#         self.artifacts_gcp_bucket_name = artifacts_gcp_bucket_name
#         self.artifacts_gcp_bucket_prefix = artifacts_gcp_bucket_prefix
#         self.artifacts_gcp_auto_create_bucket = artifacts_gcp_auto_create_bucket
#         self.artifacts_gcp_auto_create_bucket_prefix = artifacts_gcp_auto_create_bucket_prefix
#         self.troubleshooting = troubleshooting

#     def validate_artifacts(self, troubleshooting: bool = False):
#         return validate_artifacts(
#             self.artifacts_local_path,
#             self.artifacts_gcp_sync_strategy,
#             self.artifacts_gcp_service_account_json_path,
#             self.artifacts_gcp_bucket_name,
#             self.artifacts_gcp_bucket_prefix,
#             self.artifacts_gcp_auto_create_bucket,
#             self.artifacts_gcp_auto_create_bucket_prefix,
#             troubleshooting or self.troubleshooting,
#         )
    
