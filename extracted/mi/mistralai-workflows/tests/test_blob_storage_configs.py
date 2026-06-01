import os
from unittest.mock import patch

from mistralai.extra.workflows.encoding.config import StorageProvider

from mistralai.workflows.core.config.config import WorkerConfig


class TestBlobStorageConfigs:
    def test_parsed_from_env(self):
        with patch.dict(
            os.environ,
            {
                "BLOB_STORAGE_CONFIGS__DOCUMENT__STORAGE_PROVIDER": "gcs",
                "BLOB_STORAGE_CONFIGS__DOCUMENT__BUCKET_ID": "my-bucket",
            },
        ):
            cfg = WorkerConfig()
            assert "document" in cfg.blob_storage_configs
            assert cfg.blob_storage_configs["document"].bucket_id == "my-bucket"
            assert cfg.blob_storage_configs["document"].storage_provider == StorageProvider.GCS

    def test_multiple_configs_are_independent(self):
        with patch.dict(
            os.environ,
            {
                "BLOB_STORAGE_CONFIGS__INVOICES__STORAGE_PROVIDER": "gcs",
                "BLOB_STORAGE_CONFIGS__INVOICES__BUCKET_ID": "invoices-bucket",
                "BLOB_STORAGE_CONFIGS__CONTRACTS__STORAGE_PROVIDER": "s3",
                "BLOB_STORAGE_CONFIGS__CONTRACTS__BUCKET_NAME": "contracts-bucket",
            },
        ):
            cfg = WorkerConfig()
            assert len(cfg.blob_storage_configs) == 2
            assert cfg.blob_storage_configs["invoices"].storage_provider == StorageProvider.GCS
            assert cfg.blob_storage_configs["contracts"].storage_provider == StorageProvider.S3

    def test_defaults_to_empty_dict(self):
        cfg = WorkerConfig()
        assert cfg.blob_storage_configs == {}
