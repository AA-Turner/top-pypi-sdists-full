"""Comprehensive tests for backend modules - schemas, config, etc."""

import json
import re
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError

# Import backend modules
import sys
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from backend.config import (
    RuntimeConfig,
    AppSettings,
    settings,
    runtime_defaults,
)
from backend.schemas import (
    SchemaBase,
    SAFE_MODEL_ID_PATTERN,
    SAFE_CONVERSATION_ID_PATTERN,
    validate_safe_id,
    ModelVersion,
    ModelRecord,
    RUNTIME_PATTERN,
    DownloadModelReq,
    ImportModelReq,
    LoadModelReq,
    SetActiveVersionReq,
    LARGE_TEXT_THRESHOLD,
    SAFE_FILENAME_PATTERN,
    validate_safe_filename,
    FileAttachment,
)


# =============================================================================
# Tests for RuntimeConfig
# =============================================================================


class TestRuntimeConfig:
    """Tests for RuntimeConfig class."""

    def test_defaults(self):
        """Check default values."""
        config = RuntimeConfig()
        assert config.default_runtime == "llama_cpp"
        assert config.default_threads == 0
        assert config.default_temperature == 0.3
        assert config.default_max_tokens == 512
        assert config.default_top_p == 0.95

    def test_custom_values(self):
        """Create with custom values."""
        config = RuntimeConfig(
            default_runtime="transformers",
            default_threads=8,
            default_temperature=0.7,
            default_max_tokens=1024,
            default_top_p=0.9,
        )
        assert config.default_runtime == "transformers"
        assert config.default_threads == 8
        assert config.default_temperature == 0.7
        assert config.default_max_tokens == 1024
        assert config.default_top_p == 0.9


# =============================================================================
# Tests for AppSettings
# =============================================================================


class TestAppSettings:
    """Tests for AppSettings class."""

    def test_defaults(self):
        """Check default settings."""
        app = AppSettings()
        assert app.host == "0.0.0.0"
        assert app.port == 8090
        assert app.log_level == "INFO"
        assert app.dev_mode is True

    def test_validate_admin_token_dev_mode(self):
        """Admin token not required in dev mode."""
        app = AppSettings(dev_mode=True, admin_token="")
        assert app.validate_admin_token() is True

    def test_validate_admin_token_prod_valid(self):
        """Valid admin token in production."""
        app = AppSettings(dev_mode=False, admin_token="a" * 16)
        assert app.validate_admin_token() is True

    def test_validate_admin_token_prod_invalid(self):
        """Invalid admin token in production."""
        app = AppSettings(dev_mode=False, admin_token="short")
        assert app.validate_admin_token() is False

    def test_is_production_dev(self):
        """is_production in dev mode."""
        app = AppSettings(dev_mode=True)
        assert app.is_production is False

    def test_is_production_prod(self):
        """is_production in production mode."""
        app = AppSettings(dev_mode=False)
        assert app.is_production is True

    def test_cors_origins_default(self):
        """Default CORS origins."""
        app = AppSettings()
        assert len(app.cors_origins) >= 2
        assert any("localhost" in o for o in app.cors_origins)

    def test_cors_origins_parse_json(self):
        """Parse JSON CORS origins."""
        app = AppSettings(cors_origins='["http://a.com", "http://b.com"]')
        assert "http://a.com" in app.cors_origins
        assert "http://b.com" in app.cors_origins

    def test_cors_origins_parse_csv(self):
        """Parse comma-separated CORS origins."""
        app = AppSettings(cors_origins="http://a.com, http://b.com")
        assert "http://a.com" in app.cors_origins
        assert "http://b.com" in app.cors_origins

    def test_cors_origins_empty_string(self):
        """Empty CORS origins string."""
        app = AppSettings(cors_origins="")
        assert app.cors_origins == []

    def test_ensure_dirs(self, tmp_path):
        """ensure_dirs creates directories."""
        models = tmp_path / "models"
        config = tmp_path / "config"
        data = tmp_path / "data"

        app = AppSettings(
            models_dir=models,
            config_dir=config,
            data_dir=data,
        )
        app.ensure_dirs()

        assert models.exists()
        assert config.exists()
        assert data.exists()


# =============================================================================
# Tests for Global Settings
# =============================================================================


class TestGlobalSettings:
    """Tests for global settings instances."""

    def test_settings_exists(self):
        """Global settings instance exists."""
        assert settings is not None
        assert isinstance(settings, AppSettings)

    def test_runtime_defaults_exists(self):
        """Runtime defaults instance exists."""
        assert runtime_defaults is not None
        assert isinstance(runtime_defaults, RuntimeConfig)


# =============================================================================
# Tests for Safe ID Validation
# =============================================================================


class TestSafeIdValidation:
    """Tests for validate_safe_id function."""

    def test_valid_id(self):
        """Accept valid ID."""
        result = validate_safe_id("valid-id-123", "test")
        assert result == "valid-id-123"

    def test_empty_id(self):
        """Reject empty ID."""
        with pytest.raises(ValueError) as exc:
            validate_safe_id("", "test")
        assert "cannot be empty" in str(exc.value)

    def test_path_traversal(self):
        """Reject path traversal."""
        with pytest.raises(ValueError) as exc:
            validate_safe_id("../etc/passwd", "test")
        assert "path traversal" in str(exc.value)

    def test_leading_slash(self):
        """Reject leading slash."""
        with pytest.raises(ValueError) as exc:
            validate_safe_id("/absolute/path", "test")
        assert "path separator" in str(exc.value)

    def test_leading_backslash(self):
        """Reject leading backslash."""
        with pytest.raises(ValueError) as exc:
            validate_safe_id("\\windows\\path", "test")
        assert "path separator" in str(exc.value)

    def test_null_byte(self):
        """Reject null byte."""
        with pytest.raises(ValueError) as exc:
            validate_safe_id("test\x00evil", "test")
        assert "null byte" in str(exc.value)


# =============================================================================
# Tests for Safe Filename Validation
# =============================================================================


class TestSafeFilenameValidation:
    """Tests for validate_safe_filename function."""

    def test_valid_filename(self):
        """Accept valid filename."""
        result = validate_safe_filename("file.txt")
        assert result == "file.txt"

    def test_empty_filename(self):
        """Reject empty filename."""
        with pytest.raises(ValueError) as exc:
            validate_safe_filename("")
        assert "cannot be empty" in str(exc.value)

    def test_path_traversal(self):
        """Reject path traversal."""
        with pytest.raises(ValueError) as exc:
            validate_safe_filename("../etc/passwd")
        assert "path traversal" in str(exc.value)

    def test_extracts_filename_from_path(self):
        """Extract filename from path."""
        result = validate_safe_filename("path/to/file.txt")
        assert result == "file.txt"

    def test_extracts_filename_windows_path(self):
        """Extract filename from Windows path."""
        result = validate_safe_filename("C:\\path\\to\\file.txt")
        assert result == "file.txt"

    def test_null_byte(self):
        """Reject null byte."""
        with pytest.raises(ValueError) as exc:
            validate_safe_filename("file\x00.txt")
        assert "null byte" in str(exc.value)


# =============================================================================
# Tests for ID Patterns
# =============================================================================


class TestIdPatterns:
    """Tests for ID validation patterns."""

    def test_model_id_pattern_valid(self):
        """Valid model IDs match pattern."""
        pattern = re.compile(SAFE_MODEL_ID_PATTERN)
        assert pattern.match("llama-3.3-70b")
        assert pattern.match("gpt-4")
        assert pattern.match("model_v1.0")
        assert pattern.match("a123")

    def test_model_id_pattern_invalid(self):
        """Invalid model IDs don't match pattern."""
        pattern = re.compile(SAFE_MODEL_ID_PATTERN)
        assert not pattern.match("-starts-with-dash")
        assert not pattern.match("_starts_with_underscore")
        assert not pattern.match("")

    def test_conversation_id_pattern_valid(self):
        """Valid conversation IDs match pattern."""
        pattern = re.compile(SAFE_CONVERSATION_ID_PATTERN)
        assert pattern.match("conv-123")
        assert pattern.match("abc_def")
        assert pattern.match("a1b2c3")

    def test_conversation_id_pattern_invalid(self):
        """Invalid conversation IDs don't match pattern."""
        pattern = re.compile(SAFE_CONVERSATION_ID_PATTERN)
        assert not pattern.match("-starts-with-dash")
        assert not pattern.match("")


# =============================================================================
# Tests for ModelVersion
# =============================================================================


class TestModelVersion:
    """Tests for ModelVersion schema."""

    def test_create_minimal(self):
        """Create with required fields."""
        version = ModelVersion(
            version=1,
            file_path="/models/model.gguf",
        )
        assert version.version == 1
        assert version.file_path == "/models/model.gguf"
        assert version.version_tag is None

    def test_create_full(self):
        """Create with all fields."""
        version = ModelVersion(
            version=2,
            version_tag="v1.0.0",
            file_path="/models/model.gguf",
            source_url="https://example.com/model.gguf",
            local_import=False,
            sha256="abc123",
            size_gb=7.5,
            created_at="2024-01-01T00:00:00Z",
        )
        assert version.version_tag == "v1.0.0"
        assert version.source_url == "https://example.com/model.gguf"
        assert version.sha256 == "abc123"
        assert version.size_gb == 7.5


# =============================================================================
# Tests for ModelRecord
# =============================================================================


class TestModelRecord:
    """Tests for ModelRecord schema."""

    def test_create_minimal(self):
        """Create with required fields."""
        record = ModelRecord(
            model_id="test-model",
            runtime="llama_cpp",
        )
        assert record.model_id == "test-model"
        assert record.runtime == "llama_cpp"
        assert record.active_version == 1
        assert record.versions == []

    def test_create_with_versions(self):
        """Create with versions."""
        versions = [
            ModelVersion(version=1, file_path="/v1/model.gguf"),
            ModelVersion(version=2, file_path="/v2/model.gguf"),
        ]
        record = ModelRecord(
            model_id="test-model",
            runtime="llama_cpp",
            versions=versions,
            active_version=2,
        )
        assert len(record.versions) == 2

    def test_active_version(self):
        """Get active version."""
        versions = [
            ModelVersion(version=1, file_path="/v1/model.gguf"),
            ModelVersion(version=2, file_path="/v2/model.gguf"),
        ]
        record = ModelRecord(
            model_id="test-model",
            runtime="llama_cpp",
            versions=versions,
            active_version=2,
        )
        active = record.active()
        assert active.version == 2
        assert active.file_path == "/v2/model.gguf"

    def test_active_version_not_found(self):
        """Active version not found raises."""
        record = ModelRecord(
            model_id="test-model",
            runtime="llama_cpp",
            versions=[],
            active_version=1,
        )
        with pytest.raises(KeyError):
            record.active()

    def test_latest_version_number_empty(self):
        """Latest version with no versions."""
        record = ModelRecord(
            model_id="test-model",
            runtime="llama_cpp",
        )
        assert record.latest_version_number() == 0

    def test_latest_version_number(self):
        """Latest version number."""
        versions = [
            ModelVersion(version=1, file_path="/v1/model.gguf"),
            ModelVersion(version=3, file_path="/v3/model.gguf"),
            ModelVersion(version=2, file_path="/v2/model.gguf"),
        ]
        record = ModelRecord(
            model_id="test-model",
            runtime="llama_cpp",
            versions=versions,
        )
        assert record.latest_version_number() == 3

    def test_all_hashes(self):
        """Get all SHA256 hashes."""
        versions = [
            ModelVersion(version=1, file_path="/v1.gguf", sha256="ABC123"),
            ModelVersion(version=2, file_path="/v2.gguf", sha256="DEF456"),
            ModelVersion(version=3, file_path="/v3.gguf"),  # No hash
        ]
        record = ModelRecord(
            model_id="test-model",
            runtime="llama_cpp",
            versions=versions,
        )
        hashes = record.all_hashes()
        assert "abc123" in hashes  # Lowercased
        assert "def456" in hashes
        assert len(hashes) == 2

    def test_all_tags(self):
        """Get all version tags."""
        versions = [
            ModelVersion(version=1, file_path="/v1.gguf", version_tag="v1.0"),
            ModelVersion(version=2, file_path="/v2.gguf", version_tag="v2.0"),
            ModelVersion(version=3, file_path="/v3.gguf"),  # No tag
        ]
        record = ModelRecord(
            model_id="test-model",
            runtime="llama_cpp",
            versions=versions,
        )
        tags = record.all_tags()
        assert "v1.0" in tags
        assert "v2.0" in tags
        assert len(tags) == 2


# =============================================================================
# Tests for DownloadModelReq
# =============================================================================


class TestDownloadModelReq:
    """Tests for DownloadModelReq schema."""

    def test_valid_request(self):
        """Create valid download request."""
        req = DownloadModelReq(
            model_id="llama-3-8b",
            source_url="https://example.com/model.gguf",
            runtime="llama_cpp",
        )
        assert req.model_id == "llama-3-8b"
        assert req.runtime == "llama_cpp"

    def test_invalid_model_id_too_short(self):
        """Model ID too short."""
        with pytest.raises(ValidationError):
            DownloadModelReq(
                model_id="a",  # Too short
                source_url="https://example.com/model.gguf",
                runtime="llama_cpp",
            )

    def test_invalid_model_id_path_traversal(self):
        """Model ID with path traversal."""
        with pytest.raises(ValidationError):
            DownloadModelReq(
                model_id="../etc/passwd",
                source_url="https://example.com/model.gguf",
                runtime="llama_cpp",
            )

    def test_invalid_runtime(self):
        """Invalid runtime value."""
        with pytest.raises(ValidationError):
            DownloadModelReq(
                model_id="test-model",
                source_url="https://example.com/model.gguf",
                runtime="invalid_runtime",
            )

    def test_valid_runtimes(self):
        """All valid runtimes work."""
        runtimes = ["llama_cpp", "transformers", "vllm", "onnx", "ollama", "cloud"]
        for runtime in runtimes:
            req = DownloadModelReq(
                model_id="test-model",
                source_url="https://example.com/model.gguf",
                runtime=runtime,
            )
            assert req.runtime == runtime


# =============================================================================
# Tests for ImportModelReq
# =============================================================================


class TestImportModelReq:
    """Tests for ImportModelReq schema."""

    def test_valid_request(self):
        """Create valid import request."""
        req = ImportModelReq(
            model_id="local-model",
            local_path="/path/to/model.gguf",
            runtime="llama_cpp",
        )
        assert req.model_id == "local-model"
        assert req.local_path == "/path/to/model.gguf"

    def test_invalid_runtime(self):
        """Invalid runtime value."""
        with pytest.raises(ValidationError):
            ImportModelReq(
                model_id="test",
                local_path="/path/to/model.gguf",
                runtime="bad_runtime",
            )


# =============================================================================
# Tests for LoadModelReq
# =============================================================================


class TestLoadModelReq:
    """Tests for LoadModelReq schema."""

    def test_minimal(self):
        """Create minimal request."""
        req = LoadModelReq(model_id="test-model")
        assert req.model_id == "test-model"
        assert req.version is None
        assert req.threads is None

    def test_with_version(self):
        """Create with version."""
        req = LoadModelReq(model_id="test-model", version=2)
        assert req.version == 2

    def test_with_threads(self):
        """Create with threads."""
        req = LoadModelReq(model_id="test-model", threads=8)
        assert req.threads == 8

    def test_threads_min(self):
        """Threads must be at least 1."""
        with pytest.raises(ValidationError):
            LoadModelReq(model_id="test-model", threads=0)

    def test_threads_max(self):
        """Threads must be at most 256."""
        with pytest.raises(ValidationError):
            LoadModelReq(model_id="test-model", threads=257)


# =============================================================================
# Tests for SetActiveVersionReq
# =============================================================================


class TestSetActiveVersionReq:
    """Tests for SetActiveVersionReq schema."""

    def test_valid(self):
        """Create valid request."""
        req = SetActiveVersionReq(model_id="test-model", version=2)
        assert req.model_id == "test-model"
        assert req.version == 2

    def test_version_min(self):
        """Version must be at least 1."""
        with pytest.raises(ValidationError):
            SetActiveVersionReq(model_id="test-model", version=0)


# =============================================================================
# Tests for FileAttachment
# =============================================================================


class TestFileAttachment:
    """Tests for FileAttachment schema."""

    def test_minimal(self):
        """Create with required fields."""
        attachment = FileAttachment(
            file_id="file-123",
            filename="test.txt",
        )
        assert attachment.file_id == "file-123"
        assert attachment.filename == "test.txt"
        assert attachment.mime_type == "application/octet-stream"
        assert attachment.size_bytes == 0

    def test_full(self):
        """Create with all fields."""
        attachment = FileAttachment(
            file_id="file-123",
            filename="document.pdf",
            mime_type="application/pdf",
            size_bytes=1024,
            url="https://example.com/file.pdf",
            content_preview="PDF document...",
        )
        assert attachment.mime_type == "application/pdf"
        assert attachment.size_bytes == 1024
        assert attachment.url == "https://example.com/file.pdf"

    def test_size_non_negative(self):
        """Size must be non-negative."""
        with pytest.raises(ValidationError):
            FileAttachment(
                file_id="file-123",
                filename="test.txt",
                size_bytes=-1,
            )


# =============================================================================
# Tests for Constants
# =============================================================================


class TestConstants:
    """Tests for schema constants."""

    def test_large_text_threshold(self):
        """Large text threshold is 100KB."""
        assert LARGE_TEXT_THRESHOLD == 100 * 1024

    def test_runtime_pattern_valid(self):
        """Runtime pattern matches valid runtimes."""
        pattern = re.compile(RUNTIME_PATTERN)
        valid = ["llama_cpp", "transformers", "vllm", "onnx", "ollama", "cloud"]
        for runtime in valid:
            assert pattern.match(runtime)

    def test_safe_filename_pattern(self):
        """Safe filename pattern."""
        pattern = re.compile(SAFE_FILENAME_PATTERN)
        assert pattern.match("file.txt")
        assert pattern.match("model-v1.0.gguf")
        assert not pattern.match(".hidden")
        assert not pattern.match("-starts-with-dash")


# =============================================================================
# Integration Tests
# =============================================================================


class TestBackendIntegration:
    """Integration tests for backend modules."""

    def test_model_lifecycle(self):
        """Test model record lifecycle."""
        # Create model record
        record = ModelRecord(
            model_id="llama-3-8b",
            runtime="llama_cpp",
            license="MIT",
        )

        # Add first version
        v1 = ModelVersion(
            version=1,
            file_path="/models/llama-3-8b-v1.gguf",
            sha256="abc123",
        )
        record.versions.append(v1)

        # Add second version
        v2 = ModelVersion(
            version=2,
            file_path="/models/llama-3-8b-v2.gguf",
            sha256="def456",
            version_tag="v2.0.0",
        )
        record.versions.append(v2)

        # Set active version
        record.active_version = 2

        # Verify
        assert record.active().version == 2
        assert record.latest_version_number() == 2
        assert len(record.all_hashes()) == 2
        assert "v2.0.0" in record.all_tags()

    def test_settings_validation(self):
        """Test settings validation flow."""
        # Dev mode allows empty token
        dev = AppSettings(dev_mode=True, admin_token="")
        assert dev.validate_admin_token()

        # Production requires proper token
        prod = AppSettings(dev_mode=False, admin_token="secure_token_16_ch")
        assert prod.validate_admin_token()

    def test_request_validation_flow(self):
        """Test request validation flow."""
        # Valid download request
        download = DownloadModelReq(
            model_id="llama-3-8b",
            source_url="https://huggingface.co/model.gguf",
            runtime="llama_cpp",
            license="Meta Llama 3",
            size_gb=4.5,
        )
        assert download.model_id == "llama-3-8b"

        # Valid import request
        import_req = ImportModelReq(
            model_id="local-model",
            local_path="/home/user/models/model.gguf",
            runtime="llama_cpp",
        )
        assert import_req.local_path == "/home/user/models/model.gguf"

        # Valid load request
        load = LoadModelReq(
            model_id="llama-3-8b",
            version=1,
            threads=8,
        )
        assert load.threads == 8
