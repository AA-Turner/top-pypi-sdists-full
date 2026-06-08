"""Comprehensive tests for sage/models/catalog.py - Model Catalog System."""

import json
import time
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock

import pytest

from sage.models.catalog import (
    # Main dataclass
    CatalogModel,
    # Catalog data
    MODEL_CATALOG,
    CATALOG_BY_NAME,
    OLLAMA_CATALOG,
    OLLAMA_BY_NAME,
    # Constants
    GCS_BUCKET,
    DEFAULT_OLLAMA_MODELS,
    BEST_MODELS_RANKED,
    DEFAULT_MODEL_NAME,
    GCS_CATALOG_URL,
    # Alias
    OllamaModel,
    # URL helpers
    _gcs_url,
    _hf_url,
    # Search functions
    search_catalog,
    search_ollama_catalog,
    # Recommendation functions
    get_recommended_models,
    get_recommended_ollama_models,
    get_ollama_models_by_category,
    get_default_models,
    # Remote catalog functions
    _dict_to_model,
    fetch_remote_catalog,
    get_full_catalog,
)


# =============================================================================
# Tests for CatalogModel Dataclass
# =============================================================================


class TestCatalogModel:
    """Tests for CatalogModel dataclass."""

    def test_create_minimal(self):
        """Create with required fields."""
        model = CatalogModel(
            name="test-model",
            display_name="Test Model",
            filename="test.gguf",
            url="https://example.com/test.gguf",
            size_gb=1.0,
            params="1B",
            family="Test",
            description="A test model",
        )
        assert model.name == "test-model"
        assert model.display_name == "Test Model"
        assert model.filename == "test.gguf"
        assert model.size_gb == 1.0

    def test_default_values(self):
        """Check default values."""
        model = CatalogModel(
            name="test",
            display_name="Test",
            filename="test.gguf",
            url="https://example.com",
            size_gb=1.0,
            params="1B",
            family="Test",
            description="Test",
        )
        assert model.backend == "gguf"
        assert model.tags == ()
        assert model.category == "general"
        assert model.default is False

    def test_custom_values(self):
        """Create with custom values."""
        model = CatalogModel(
            name="ollama:test",
            display_name="Test",
            filename="",
            url="",
            size_gb=0,
            params="7b",
            family="Test",
            description="Test",
            backend="ollama",
            tags=("tools", "vision"),
            category="coding",
            default=True,
        )
        assert model.backend == "ollama"
        assert model.tags == ("tools", "vision")
        assert model.category == "coding"
        assert model.default is True

    def test_frozen_dataclass(self):
        """CatalogModel is frozen (immutable)."""
        model = CatalogModel(
            name="test",
            display_name="Test",
            filename="test.gguf",
            url="https://example.com",
            size_gb=1.0,
            params="1B",
            family="Test",
            description="Test",
        )
        with pytest.raises(Exception):  # FrozenInstanceError
            model.name = "new-name"

    def test_ollama_model_alias(self):
        """OllamaModel is an alias for CatalogModel."""
        assert OllamaModel is CatalogModel


# =============================================================================
# Tests for URL Helper Functions
# =============================================================================


class TestUrlHelpers:
    """Tests for URL helper functions."""

    def test_gcs_url(self):
        """_gcs_url generates correct GCS URL."""
        url = _gcs_url("test-model.gguf")
        assert url.startswith(GCS_BUCKET)
        assert url.endswith("test-model.gguf")

    def test_hf_url(self):
        """_hf_url generates correct HuggingFace URL."""
        url = _hf_url("TheBloke/model-GGUF", "model.Q4_K_M.gguf")
        assert "huggingface.co" in url
        assert "TheBloke/model-GGUF" in url
        assert "model.Q4_K_M.gguf" in url


# =============================================================================
# Tests for Catalog Data
# =============================================================================


class TestCatalogData:
    """Tests for catalog data structures."""

    def test_model_catalog_not_empty(self):
        """MODEL_CATALOG has models."""
        assert len(MODEL_CATALOG) >= 100

    def test_catalog_has_gguf_models(self):
        """Catalog has GGUF models."""
        gguf_models = [m for m in MODEL_CATALOG if m.backend == "gguf"]
        assert len(gguf_models) >= 10

    def test_catalog_has_ollama_models(self):
        """Catalog has Ollama models."""
        ollama_models = [m for m in MODEL_CATALOG if m.backend == "ollama"]
        assert len(ollama_models) >= 50

    def test_catalog_by_name_lookup(self):
        """CATALOG_BY_NAME allows lookup by name."""
        assert len(CATALOG_BY_NAME) == len(MODEL_CATALOG)
        for model in MODEL_CATALOG:
            assert CATALOG_BY_NAME[model.name] is model

    def test_unique_model_names(self):
        """All model names are unique."""
        names = [m.name for m in MODEL_CATALOG]
        assert len(names) == len(set(names))

    def test_ollama_catalog(self):
        """OLLAMA_CATALOG filters Ollama models."""
        assert len(OLLAMA_CATALOG) >= 50
        for model in OLLAMA_CATALOG:
            assert model.backend == "ollama"

    def test_ollama_by_name_with_prefix(self):
        """OLLAMA_BY_NAME supports prefix lookup."""
        for model in OLLAMA_CATALOG:
            assert model.name in OLLAMA_BY_NAME
            # Also supports without prefix
            stripped = model.name.removeprefix("ollama:")
            assert stripped in OLLAMA_BY_NAME

    def test_gguf_models_have_valid_urls(self):
        """GGUF models have valid download URLs."""
        gguf_models = [m for m in MODEL_CATALOG if m.backend == "gguf"]
        for model in gguf_models:
            assert model.url.startswith("https://")

    def test_gguf_models_have_gguf_extension(self):
        """GGUF models have .gguf filename."""
        gguf_models = [m for m in MODEL_CATALOG if m.backend == "gguf"]
        for model in gguf_models:
            assert model.filename.endswith(".gguf")

    def test_ollama_models_have_prefix(self):
        """Ollama models have ollama: prefix."""
        for model in OLLAMA_CATALOG:
            assert model.name.startswith("ollama:")


# =============================================================================
# Tests for Constants
# =============================================================================


class TestConstants:
    """Tests for module constants."""

    def test_gcs_bucket(self):
        """GCS_BUCKET is valid URL."""
        assert GCS_BUCKET.startswith("https://")
        assert "storage.googleapis.com" in GCS_BUCKET

    def test_default_ollama_models(self):
        """DEFAULT_OLLAMA_MODELS has entries."""
        assert len(DEFAULT_OLLAMA_MODELS) >= 5

    def test_best_models_ranked(self):
        """BEST_MODELS_RANKED has entries."""
        assert len(BEST_MODELS_RANKED) >= 10

    def test_default_model_name(self):
        """DEFAULT_MODEL_NAME is valid."""
        assert DEFAULT_MODEL_NAME
        assert DEFAULT_MODEL_NAME in CATALOG_BY_NAME

    def test_gcs_catalog_url(self):
        """GCS_CATALOG_URL is valid."""
        assert GCS_CATALOG_URL.startswith("https://")
        assert "catalog.json" in GCS_CATALOG_URL


# =============================================================================
# Tests for Search Functions
# =============================================================================


class TestSearchCatalog:
    """Tests for search_catalog function."""

    def test_search_by_name(self):
        """Search by model name."""
        results = search_catalog("llama")
        assert len(results) >= 1
        for model in results:
            assert (
                "llama" in model.name.lower()
                or "llama" in model.family.lower()
                or "llama" in model.display_name.lower()
                or "llama" in model.description.lower()
            )

    def test_search_by_family(self):
        """Search by family name."""
        results = search_catalog("Qwen")
        assert len(results) >= 3

    def test_search_by_description(self):
        """Search by description keyword."""
        results = search_catalog("coding")
        assert len(results) >= 1

    def test_search_case_insensitive(self):
        """Search is case insensitive."""
        upper = search_catalog("GEMMA")
        lower = search_catalog("gemma")
        assert len(upper) == len(lower)

    def test_search_no_results(self):
        """Search with no matches returns empty list."""
        results = search_catalog("nonexistent_xyz_model_abc123")
        assert results == []


class TestSearchOllamaCatalog:
    """Tests for search_ollama_catalog function."""

    def test_search_ollama_by_name(self):
        """Search Ollama catalog by name."""
        results = search_ollama_catalog("llama")
        assert len(results) >= 1
        for model in results:
            assert model.backend == "ollama"

    def test_search_ollama_by_category(self):
        """Search Ollama catalog by category."""
        results = search_ollama_catalog("coding")
        assert len(results) >= 1

    def test_search_ollama_no_results(self):
        """Search Ollama with no matches returns empty."""
        results = search_ollama_catalog("nonexistent_xyz_model")
        assert results == []


# =============================================================================
# Tests for Recommendation Functions
# =============================================================================


class TestGetRecommendedModels:
    """Tests for get_recommended_models function."""

    def test_returns_models(self):
        """Returns a list of models."""
        models = get_recommended_models()
        assert len(models) >= 3

    def test_all_in_catalog(self):
        """All recommended models are in catalog."""
        models = get_recommended_models()
        for model in models:
            assert model.name in CATALOG_BY_NAME


class TestGetRecommendedOllamaModels:
    """Tests for get_recommended_ollama_models function."""

    def test_returns_models(self):
        """Returns a list of Ollama models."""
        models = get_recommended_ollama_models()
        assert len(models) >= 3

    def test_all_ollama_backend(self):
        """All recommended are Ollama backend."""
        models = get_recommended_ollama_models()
        for model in models:
            assert model.backend == "ollama"


class TestGetOllamaModelsByCategory:
    """Tests for get_ollama_models_by_category function."""

    def test_coding_category(self):
        """Get coding category models."""
        models = get_ollama_models_by_category("coding")
        assert len(models) >= 1
        for model in models:
            assert model.category == "coding"

    def test_general_category(self):
        """Get general category models."""
        models = get_ollama_models_by_category("general")
        assert len(models) >= 1

    def test_unknown_category_empty(self):
        """Unknown category returns empty."""
        models = get_ollama_models_by_category("nonexistent_category")
        assert models == []


class TestGetDefaultModels:
    """Tests for get_default_models function."""

    def test_returns_gguf_models(self):
        """Returns GGUF models."""
        models = get_default_models()
        for model in models:
            assert model.backend == "gguf"

    def test_all_marked_default(self):
        """All returned models have default=True."""
        models = get_default_models()
        for model in models:
            assert model.default is True


# =============================================================================
# Tests for _dict_to_model Function
# =============================================================================


class TestDictToModel:
    """Tests for _dict_to_model function."""

    def test_convert_minimal(self):
        """Convert minimal dict."""
        d = {
            "name": "test-model",
        }
        model = _dict_to_model(d)
        assert model.name == "test-model"
        assert model.display_name == "test-model"  # Defaults to name
        assert model.filename == ""
        assert model.url == ""

    def test_convert_full(self):
        """Convert full dict."""
        d = {
            "name": "test-model",
            "display_name": "Test Model",
            "filename": "test.gguf",
            "url": "https://example.com/test.gguf",
            "size_gb": 2.5,
            "params": "3B",
            "family": "TestFamily",
            "description": "A test model",
            "backend": "gguf",
            "tags": ["tools", "vision"],
            "category": "coding",
            "default": True,
        }
        model = _dict_to_model(d)
        assert model.name == "test-model"
        assert model.display_name == "Test Model"
        assert model.size_gb == 2.5
        assert model.tags == ("tools", "vision")
        assert model.category == "coding"
        assert model.default is True

    def test_convert_with_defaults(self):
        """Convert with default values filled."""
        d = {"name": "minimal"}
        model = _dict_to_model(d)
        assert model.backend == "gguf"
        assert model.tags == ()
        assert model.category == "general"
        assert model.default is False


# =============================================================================
# Tests for Remote Catalog Functions
# =============================================================================


class TestFetchRemoteCatalog:
    """Tests for fetch_remote_catalog function."""

    def test_fetch_success(self, tmp_path):
        """Fetch remote catalog successfully."""
        import httpx
        # Mock the response
        mock_response = MagicMock()
        mock_response.json.return_value = {
            "models": [
                {
                    "name": "remote-model",
                    "display_name": "Remote Model",
                    "filename": "remote.gguf",
                    "url": "https://example.com/remote.gguf",
                    "size_gb": 1.0,
                    "params": "1B",
                    "family": "Remote",
                    "description": "Remote model",
                }
            ]
        }
        mock_response.raise_for_status = MagicMock()

        # Patch cache location and httpx.get
        with patch("sage.models.catalog._CACHE_DIR", tmp_path):
            with patch("sage.models.catalog._CACHE_FILE", tmp_path / "catalog.json"):
                with patch.object(httpx, "get", return_value=mock_response):
                    result = fetch_remote_catalog(force=True)

        assert result is not None
        assert len(result) == 1
        assert result[0].name == "remote-model"

    def test_fetch_network_error(self, tmp_path):
        """Network error falls back gracefully."""
        import httpx

        with patch("sage.models.catalog._CACHE_DIR", tmp_path):
            with patch("sage.models.catalog._CACHE_FILE", tmp_path / "catalog.json"):
                with patch.object(httpx, "get", side_effect=Exception("Network error")):
                    result = fetch_remote_catalog(force=True)

        assert result is None  # Falls back to hardcoded

    def test_fetch_uses_cache(self, tmp_path):
        """Fetch uses cached data."""
        cache_file = tmp_path / "catalog.json"
        cache_data = {
            "models": [
                {
                    "name": "cached-model",
                    "display_name": "Cached",
                    "filename": "",
                    "url": "",
                    "size_gb": 0,
                    "params": "",
                    "family": "",
                    "description": "",
                }
            ]
        }
        cache_file.write_text(json.dumps(cache_data))
        # Set modification time to now (fresh cache)
        cache_file.touch()

        with patch("sage.models.catalog._CACHE_DIR", tmp_path):
            with patch("sage.models.catalog._CACHE_FILE", cache_file):
                result = fetch_remote_catalog(force=False)

        assert result is not None
        assert len(result) == 1
        assert result[0].name == "cached-model"


class TestGetFullCatalog:
    """Tests for get_full_catalog function."""

    @patch("sage.models.catalog.fetch_remote_catalog")
    def test_uses_remote_if_available(self, mock_fetch):
        """Uses remote catalog if available."""
        remote_models = [
            CatalogModel(
                name="remote",
                display_name="Remote",
                filename="",
                url="",
                size_gb=0,
                params="",
                family="",
                description="",
            )
        ]
        mock_fetch.return_value = remote_models

        result = get_full_catalog()
        assert result == remote_models

    @patch("sage.models.catalog.fetch_remote_catalog")
    def test_falls_back_to_hardcoded(self, mock_fetch):
        """Falls back to MODEL_CATALOG if remote fails."""
        mock_fetch.return_value = None

        result = get_full_catalog()
        assert result == MODEL_CATALOG

    @patch("sage.models.catalog.fetch_remote_catalog")
    def test_falls_back_on_empty_remote(self, mock_fetch):
        """Falls back if remote returns empty."""
        mock_fetch.return_value = []

        result = get_full_catalog()
        assert result == MODEL_CATALOG


# =============================================================================
# Integration Tests
# =============================================================================


class TestCatalogIntegration:
    """Integration tests for catalog module."""

    def test_model_families(self):
        """Catalog has multiple model families."""
        families = {m.family for m in MODEL_CATALOG}
        assert len(families) >= 5  # At least 5 different families

    def test_model_categories(self):
        """Catalog has multiple categories."""
        categories = {m.category for m in MODEL_CATALOG}
        assert "general" in categories
        assert "coding" in categories

    def test_default_model_exists(self):
        """Default model exists and is valid."""
        model = CATALOG_BY_NAME.get(DEFAULT_MODEL_NAME)
        assert model is not None
        assert model.backend == "gguf"

    def test_recommended_models_are_quality(self):
        """Recommended models have proper metadata."""
        models = get_recommended_models()
        for model in models:
            assert model.name
            assert model.display_name
            assert model.family
            assert model.description

    def test_search_and_filter_consistency(self):
        """Search results are consistent with catalog data."""
        # Search for "coder" finds models with coder in name/description
        search_results = search_catalog("coder")
        assert len(search_results) >= 1

        # All search results should have "coder" somewhere
        for model in search_results:
            has_match = (
                "coder" in model.name.lower()
                or "coder" in model.display_name.lower()
                or "coder" in model.family.lower()
                or "coder" in model.description.lower()
            )
            assert has_match, f"Model {model.name} doesn't match 'coder'"

        # Category filter returns exactly coding category
        category_results = get_ollama_models_by_category("coding")
        for model in category_results:
            assert model.category == "coding"

    def test_ollama_prefix_handling(self):
        """Ollama prefix is handled correctly."""
        # Pick an Ollama model
        if OLLAMA_CATALOG:
            model = OLLAMA_CATALOG[0]
            # Can look up with prefix
            assert model.name in OLLAMA_BY_NAME
            # Can look up without prefix
            stripped = model.name.removeprefix("ollama:")
            assert stripped in OLLAMA_BY_NAME

    def test_gguf_vs_ollama_separation(self):
        """GGUF and Ollama models are properly separated."""
        gguf_count = sum(1 for m in MODEL_CATALOG if m.backend == "gguf")
        ollama_count = sum(1 for m in MODEL_CATALOG if m.backend == "ollama")

        assert len(OLLAMA_CATALOG) == ollama_count
        assert gguf_count + ollama_count == len(MODEL_CATALOG)
