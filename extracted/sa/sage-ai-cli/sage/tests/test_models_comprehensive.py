"""Comprehensive tests for sage/models modules."""

from pathlib import Path
from unittest.mock import MagicMock, patch, Mock
from dataclasses import dataclass

import pytest

# Helper to create catalog model with required fields
def make_catalog_model(name: str, filename: str = "test.gguf", url: str = "http://x"):
    """Create a catalog model with all required fields."""
    from sage.models.catalog import CatalogModel
    return CatalogModel(
        name=name,
        display_name=name,
        filename=filename,
        url=url,
        size_gb=1.0,
        params="1B",
        family="Test",
        description="Test model",
    )


# =============================================================================
# Tests for Model Downloader
# =============================================================================


class TestModelsDir:
    """Tests for models_dir function."""

    def test_creates_directory(self, tmp_path, monkeypatch):
        """Creates directory if not exists."""
        from sage.models import downloader

        models_path = tmp_path / "models"
        monkeypatch.setattr(downloader, "MODELS_DIR", models_path)

        result = downloader.models_dir()
        assert result == models_path
        assert models_path.exists()

    def test_returns_existing_directory(self, tmp_path, monkeypatch):
        """Returns existing directory."""
        from sage.models import downloader

        models_path = tmp_path / "models"
        models_path.mkdir()
        monkeypatch.setattr(downloader, "MODELS_DIR", models_path)

        result = downloader.models_dir()
        assert result == models_path


class TestHttp2Support:
    """Tests for optional HTTP/2 support in downloader."""

    def test_supports_http2_when_h2_installed(self):
        """HTTP/2 should be enabled when h2 is importable."""
        from sage.models import downloader

        with patch("sage.models.downloader.importlib.util.find_spec", return_value=object()):
            assert downloader._supports_http2() is True

    def test_disables_http2_when_h2_missing(self):
        """Downloader should gracefully fall back when h2 is missing."""
        from sage.models import downloader

        with patch("sage.models.downloader.importlib.util.find_spec", return_value=None):
            assert downloader._supports_http2() is False


class TestModelPath:
    """Tests for model_path function."""

    def test_returns_correct_path(self, tmp_path, monkeypatch):
        """Returns correct model path."""
        from sage.models import downloader

        models_path = tmp_path / "models"
        models_path.mkdir()
        monkeypatch.setattr(downloader, "MODELS_DIR", models_path)

        model = make_catalog_model("test-model", filename="test.gguf")

        result = downloader.model_path(model)
        assert result == models_path / "test.gguf"


class TestIsDownloaded:
    """Tests for is_downloaded function."""

    def test_not_downloaded(self, tmp_path, monkeypatch):
        """Returns False if not downloaded."""
        from sage.models import downloader

        models_path = tmp_path / "models"
        models_path.mkdir()
        monkeypatch.setattr(downloader, "MODELS_DIR", models_path)

        model = make_catalog_model("test-model", filename="test.gguf")

        assert downloader.is_downloaded(model) is False

    def test_downloaded(self, tmp_path, monkeypatch):
        """Returns True if downloaded."""
        from sage.models import downloader

        models_path = tmp_path / "models"
        models_path.mkdir()
        (models_path / "test.gguf").write_bytes(b"model data")
        monkeypatch.setattr(downloader, "MODELS_DIR", models_path)

        model = make_catalog_model("test-model", filename="test.gguf")

        assert downloader.is_downloaded(model) is True

    def test_empty_file(self, tmp_path, monkeypatch):
        """Returns False for empty file."""
        from sage.models import downloader

        models_path = tmp_path / "models"
        models_path.mkdir()
        (models_path / "test.gguf").write_bytes(b"")
        monkeypatch.setattr(downloader, "MODELS_DIR", models_path)

        model = make_catalog_model("test-model", filename="test.gguf")

        assert downloader.is_downloaded(model) is False


class TestListDownloaded:
    """Tests for list_downloaded function."""

    def test_empty(self, tmp_path, monkeypatch):
        """Returns empty list when no models."""
        from sage.models import downloader
        from sage import config

        # Mock config
        mock_config = MagicMock()
        mock_config.models = {}

        with patch.object(downloader, "load_config", return_value=mock_config):
            result = downloader.list_downloaded()
            assert result == []

    def test_with_models(self, tmp_path, monkeypatch):
        """Returns list of downloaded models."""
        from sage.models import downloader

        # Create a model file
        model_path = tmp_path / "test.gguf"
        model_path.write_bytes(b"model data")

        mock_config = MagicMock()
        mock_config.models = {
            "test-model": {"path": str(model_path), "provider": "llama_cpp"}
        }

        with patch.object(downloader, "load_config", return_value=mock_config):
            result = downloader.list_downloaded()
            assert len(result) == 1
            assert result[0][0] == "test-model"
            assert result[0][1] == model_path

    def test_missing_file(self, tmp_path, monkeypatch):
        """Excludes models with missing files."""
        from sage.models import downloader

        mock_config = MagicMock()
        mock_config.models = {
            "missing-model": {"path": "/nonexistent/path.gguf", "provider": "llama_cpp"}
        }

        with patch.object(downloader, "load_config", return_value=mock_config):
            result = downloader.list_downloaded()
            assert result == []


class TestDeleteModel:
    """Tests for delete_model function."""

    def test_delete_existing(self, tmp_path):
        """Delete existing model."""
        from sage.models import downloader

        model_path = tmp_path / "test.gguf"
        model_path.write_bytes(b"model data")

        mock_config = MagicMock()
        mock_config.models = {
            "test-model": {"path": str(model_path), "provider": "llama_cpp"}
        }
        mock_config.default_model = "other"

        with patch.object(downloader, "load_config", return_value=mock_config):
            with patch.object(downloader, "unregister_model") as mock_unreg:
                result = downloader.delete_model("test-model")
                assert result is True
                assert not model_path.exists()
                mock_unreg.assert_called_once_with("test-model")

    def test_delete_missing(self):
        """Delete non-existent model."""
        from sage.models import downloader

        mock_config = MagicMock()
        mock_config.models = {}

        with patch.object(downloader, "load_config", return_value=mock_config):
            result = downloader.delete_model("nonexistent")
            assert result is False


class TestRegisterModel:
    """Tests for register_model function."""

    def test_register(self, tmp_path, monkeypatch):
        """Register a model."""
        from sage.models import downloader
        from sage.config import SageConfig

        models_path = tmp_path / "models"
        models_path.mkdir()
        monkeypatch.setattr(downloader, "MODELS_DIR", models_path)

        model = make_catalog_model("test-model", filename="test.gguf")

        mock_config = MagicMock()
        mock_config.models = {}
        mock_config.default_model = SageConfig.default_model

        with patch.object(downloader, "load_config", return_value=mock_config):
            with patch.object(downloader, "save_config") as mock_save:
                downloader.register_model(model)
                mock_save.assert_called_once()
                assert "test-model" in mock_config.models


class TestRegisterModelsBatch:
    """Tests for register_models_batch function."""

    def test_empty_list(self):
        """Empty list does nothing."""
        from sage.models import downloader

        with patch.object(downloader, "load_config") as mock_load:
            with patch.object(downloader, "save_config") as mock_save:
                downloader.register_models_batch([])
                mock_load.assert_not_called()
                mock_save.assert_not_called()

    def test_batch_register(self, tmp_path, monkeypatch):
        """Register multiple models."""
        from sage.models import downloader
        from sage.config import SageConfig

        models_path = tmp_path / "models"
        models_path.mkdir()
        monkeypatch.setattr(downloader, "MODELS_DIR", models_path)

        models = [
            make_catalog_model("m1", filename="m1.gguf", url="http://x"),
            make_catalog_model("m2", filename="m2.gguf", url="http://y"),
        ]

        mock_config = MagicMock()
        mock_config.models = {}
        mock_config.default_model = SageConfig.default_model

        with patch.object(downloader, "load_config", return_value=mock_config):
            with patch.object(downloader, "save_config") as mock_save:
                downloader.register_models_batch(models)
                mock_save.assert_called_once()
                assert "m1" in mock_config.models
                assert "m2" in mock_config.models


class TestUnregisterModel:
    """Tests for unregister_model function."""

    def test_unregister(self):
        """Unregister a model."""
        from sage.models import downloader
        from sage.config import SageConfig

        mock_config = MagicMock()
        mock_config.models = {"test-model": {"path": "/path", "provider": "llama_cpp"}}
        mock_config.default_model = "other"

        with patch.object(downloader, "load_config", return_value=mock_config):
            with patch.object(downloader, "save_config") as mock_save:
                downloader.unregister_model("test-model")
                mock_save.assert_called_once()
                assert "test-model" not in mock_config.models

    def test_unregister_default_model(self):
        """Unregister default model resets default."""
        from sage.models import downloader
        from sage.config import SageConfig

        mock_config = MagicMock()
        mock_config.models = {"test-model": {"path": "/path", "provider": "llama_cpp"}}
        mock_config.default_model = "llama_cpp:test-model"

        with patch.object(downloader, "load_config", return_value=mock_config):
            with patch.object(downloader, "save_config") as mock_save:
                downloader.unregister_model("test-model")
                assert mock_config.default_model == SageConfig.default_model


class TestUnregisterModelsBatch:
    """Tests for unregister_models_batch function."""

    def test_empty_list(self):
        """Empty list does nothing."""
        from sage.models import downloader

        with patch.object(downloader, "load_config") as mock_load:
            with patch.object(downloader, "save_config") as mock_save:
                downloader.unregister_models_batch([])
                mock_load.assert_not_called()
                mock_save.assert_not_called()

    def test_batch_unregister(self):
        """Unregister multiple models."""
        from sage.models import downloader
        from sage.config import SageConfig

        mock_config = MagicMock()
        mock_config.models = {
            "m1": {"path": "/p1"},
            "m2": {"path": "/p2"},
            "m3": {"path": "/p3"},
        }
        mock_config.default_model = "other"

        with patch.object(downloader, "load_config", return_value=mock_config):
            with patch.object(downloader, "save_config") as mock_save:
                downloader.unregister_models_batch(["m1", "m2"])
                mock_save.assert_called_once()
                assert "m1" not in mock_config.models
                assert "m2" not in mock_config.models
                assert "m3" in mock_config.models


# =============================================================================
# Tests for GCS Manager
# =============================================================================


class TestGCSManager:
    """Tests for GCS Manager module."""

    def test_import(self):
        """Module can be imported."""
        from sage.models import gcs_manager
        assert gcs_manager is not None


# =============================================================================
# Tests for Model Catalog
# =============================================================================


class TestCatalogModel:
    """Tests for CatalogModel dataclass."""

    def test_create(self):
        """Create a catalog model."""
        from sage.models.catalog import CatalogModel

        model = CatalogModel(
            name="llama-2-7b",
            display_name="Llama 2 7B",
            filename="llama-2-7b.gguf",
            url="https://gcs.com/model.gguf",
            size_gb=4.0,
            params="7B",
            family="Llama",
            description="Test model",
        )
        assert model.name == "llama-2-7b"
        assert model.size_gb == 4.0

    def test_with_optional_fields(self):
        """Create model with optional fields."""
        from sage.models.catalog import CatalogModel

        model = CatalogModel(
            name="test",
            display_name="Test Model",
            filename="test.gguf",
            url="https://example.com",
            size_gb=1.0,
            params="1B",
            family="Test",
            description="A test model",
            backend="gguf",
            tags=("coding", "tools"),
            category="coding",
            default=True,
        )
        assert model.description == "A test model"
        assert model.backend == "gguf"
        assert model.tags == ("coding", "tools")
        assert model.category == "coding"
        assert model.default is True


class TestGCSBucket:
    """Tests for GCS bucket constant."""

    def test_bucket_defined(self):
        """GCS bucket is defined."""
        from sage.models.catalog import GCS_BUCKET

        assert GCS_BUCKET is not None
        assert isinstance(GCS_BUCKET, str)


class TestModelCatalog:
    """Tests for MODEL_CATALOG constant."""

    def test_catalog_exists(self):
        """Model catalog exists."""
        from sage.models.catalog import MODEL_CATALOG

        assert MODEL_CATALOG is not None
        assert isinstance(MODEL_CATALOG, list)

    def test_catalog_has_models(self):
        """Catalog contains models."""
        from sage.models.catalog import MODEL_CATALOG, CatalogModel

        assert len(MODEL_CATALOG) > 0
        assert all(isinstance(m, CatalogModel) for m in MODEL_CATALOG)


class TestCatalogByName:
    """Tests for CATALOG_BY_NAME lookup."""

    def test_get_existing(self):
        """Get existing model from catalog by name."""
        from sage.models.catalog import CATALOG_BY_NAME, MODEL_CATALOG

        if MODEL_CATALOG:
            first_name = MODEL_CATALOG[0].name
            model = CATALOG_BY_NAME.get(first_name)
            assert model is not None
            assert model.name == first_name

    def test_get_nonexistent(self):
        """Get non-existent model returns None."""
        from sage.models.catalog import CATALOG_BY_NAME

        model = CATALOG_BY_NAME.get("nonexistent-model-xyz")
        assert model is None


class TestGetRecommendedModels:
    """Tests for get_recommended_models function."""

    def test_returns_list(self):
        """Returns list of recommended models."""
        from sage.models.catalog import get_recommended_models, CatalogModel

        models = get_recommended_models()
        assert isinstance(models, list)
        for m in models:
            assert isinstance(m, CatalogModel)


class TestSearchCatalog:
    """Tests for search_catalog function."""

    def test_search_by_name(self):
        """Search by name."""
        from sage.models.catalog import search_catalog, MODEL_CATALOG

        if MODEL_CATALOG:
            # Use partial name of first model
            partial_name = MODEL_CATALOG[0].name[:4]
            models = search_catalog(partial_name)
            assert len(models) >= 1

    def test_search_by_family(self):
        """Search by family."""
        from sage.models.catalog import search_catalog, MODEL_CATALOG

        if MODEL_CATALOG:
            family = MODEL_CATALOG[0].family[:4].lower()
            models = search_catalog(family)
            assert len(models) >= 1

    def test_search_no_results(self):
        """Search with no results."""
        from sage.models.catalog import search_catalog

        models = search_catalog("xyz123nonexistent")
        assert models == []


class TestOllamaCatalog:
    """Tests for Ollama catalog helpers."""

    def test_ollama_catalog_exists(self):
        """OLLAMA_CATALOG exists."""
        from sage.models.catalog import OLLAMA_CATALOG

        assert isinstance(OLLAMA_CATALOG, list)

    def test_ollama_models_have_ollama_backend(self):
        """All Ollama models have backend='ollama'."""
        from sage.models.catalog import OLLAMA_CATALOG

        for m in OLLAMA_CATALOG:
            assert m.backend == "ollama"

    def test_search_ollama_catalog(self):
        """Search Ollama catalog."""
        from sage.models.catalog import search_ollama_catalog

        # Just verify function works
        results = search_ollama_catalog("llama")
        assert isinstance(results, list)


class TestGetDefaultModels:
    """Tests for get_default_models function."""

    def test_returns_list(self):
        """Returns list of default models."""
        from sage.models.catalog import get_default_models, CatalogModel

        models = get_default_models()
        assert isinstance(models, list)
        for m in models:
            assert isinstance(m, CatalogModel)


# =============================================================================
# Tests for Downloader Constants
# =============================================================================


class TestDownloaderConstants:
    """Tests for downloader constants."""

    def test_chunk_size(self):
        """Chunk size is defined."""
        from sage.models.downloader import CHUNK_SIZE

        assert CHUNK_SIZE > 0
        assert CHUNK_SIZE == 1024 * 1024  # 1MB

    def test_write_buffer_size(self):
        """Write buffer size is defined."""
        from sage.models.downloader import WRITE_BUFFER_SIZE

        assert WRITE_BUFFER_SIZE > 0
        assert WRITE_BUFFER_SIZE == 8 * 1024 * 1024  # 8MB
