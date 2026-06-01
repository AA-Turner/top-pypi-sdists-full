"""Tests for versioning settings."""

import pytest

from csrd.versioning._settings import load_app_name, load_versioning_settings


class TestLoadVersioningSettings:
    def setup_method(self):
        load_versioning_settings.cache_clear()

    def teardown_method(self):
        load_versioning_settings.cache_clear()

    def test_returns_settings_object(self):
        settings = load_versioning_settings()
        assert hasattr(settings, "jwt_secret")
        assert hasattr(settings, "app_name")

    def test_cached(self):
        s1 = load_versioning_settings()
        s2 = load_versioning_settings()
        assert s1 is s2


class TestLoadAppName:
    def setup_method(self):
        load_versioning_settings.cache_clear()

    def teardown_method(self):
        load_versioning_settings.cache_clear()

    def test_override_string(self):
        assert load_app_name("MyApp") == "MyApp"

    def test_override_empty_raises(self):
        with pytest.raises(ValueError, match="non-empty"):
            load_app_name("")

    def test_none_falls_back_to_env_or_default(self):
        result = load_app_name(None)
        # Without APP_NAME env var, should return fallback
        assert isinstance(result, str)
        assert len(result) > 0
