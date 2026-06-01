"""Tests for versioning core: normalize, resolve, map."""

from enum import Enum

import pytest

from csrd.versioning._core import (
    map_version_path,
    normalize_prefix,
    normalize_version,
    resolve_version,
    validate_version_mapping_keys,
)


class Versions(Enum):
    Unversioned = "Unversioned"
    V1 = "2024-01-01"
    V2 = "2025-06-20"


# ── normalize_version ───────────────────────────────────────────────────


class TestNormalizeVersion:
    def test_none(self):
        assert normalize_version(None) == "unv"

    def test_empty_string(self):
        assert normalize_version("") == "unv"

    def test_whitespace(self):
        assert normalize_version("   ") == "unv"

    def test_unversioned_aliases(self):
        for alias in ("null", "unv", "none", "unversioned", "UNVERSIONED", "Null"):
            assert normalize_version(alias) == "unv"

    def test_date_string(self):
        assert normalize_version("2025-06-20") == "2025-06-20"

    def test_enum_value(self):
        assert normalize_version(Versions.V1) == "2024-01-01"
        assert normalize_version(Versions.Unversioned) == "unv"

    def test_integer(self):
        assert normalize_version(3) == "3"

    def test_mixed_case_preserved_lowered(self):
        assert normalize_version("V2-Beta") == "v2-beta"


# ── normalize_prefix ────────────────────────────────────────────────────


class TestNormalizePrefix:
    def test_adds_leading_slash(self):
        assert normalize_prefix("api") == "/api"

    def test_strips_trailing_slash(self):
        assert normalize_prefix("/api/") == "/api"

    def test_root_preserved(self):
        assert normalize_prefix("/") == "/"

    def test_empty_raises(self):
        with pytest.raises(ValueError, match="must not be empty"):
            normalize_prefix("")


# ── validate_version_mapping_keys ────────────────────────────────────────


class TestValidateVersionMappingKeys:
    def test_no_collision(self):
        validate_version_mapping_keys({Versions.V1: "app1", Versions.V2: "app2"})

    def test_collision_raises(self):
        with pytest.raises(ValueError, match="Duplicate version keys"):
            validate_version_mapping_keys({None: "a", "unversioned": "b"})


# ── resolve_version ──────────────────────────────────────────────────────


class TestResolveVersion:
    def test_no_mapping_none_request(self):
        assert resolve_version(requested_version=None) == "unv"

    def test_no_mapping_with_value(self):
        assert resolve_version(requested_version="2025-06-20") == "2025-06-20"

    def test_exact_match(self):
        mapping = {Versions.V1: "app1", Versions.V2: "app2"}
        result = resolve_version(requested_version="2025-06-20", version_mapping=mapping)
        assert result == "2025-06-20"

    def test_missing_falls_back_to_unv(self):
        mapping = {Versions.Unversioned: "app0", Versions.V1: "app1"}
        result = resolve_version(requested_version=None, version_mapping=mapping)
        assert result == "unv"

    def test_unknown_version_fallback(self):
        mapping = {Versions.V1: "app1", Versions.V2: "app2"}
        result = resolve_version(requested_version="9999-01-01", version_mapping=mapping)
        # Should fall back to latest
        assert result == "2025-06-20"

    def test_strict_mode_rejects_unknown(self):
        mapping = {Versions.V1: "app1"}
        with pytest.raises(ValueError, match="not available"):
            resolve_version(requested_version="9999-01-01", version_mapping=mapping, strict=True)

    def test_strict_mode_allows_none(self):
        mapping = {Versions.V1: "app1", Versions.Unversioned: "app0"}
        result = resolve_version(requested_version=None, version_mapping=mapping, strict=True)
        assert result == "unv"

    def test_default_version(self):
        mapping = {Versions.V1: "app1", Versions.V2: "app2"}
        result = resolve_version(
            requested_version=None,
            version_mapping=mapping,
            default_version=Versions.V1,
        )
        assert result == "2024-01-01"

    def test_default_version_not_in_mapping_ignored(self):
        mapping = {Versions.V1: "app1"}
        result = resolve_version(
            requested_version=None,
            version_mapping=mapping,
            default_version="nonexistent",
        )
        assert result == "2024-01-01"  # falls back to latest


# ── map_version_path ─────────────────────────────────────────────────────


class TestMapVersionPath:
    def test_basic_rewrite(self):
        result = map_version_path("/api/users", version="2025-06-20", prefix="/api")
        assert result == "/api/2025-06-20/users"

    def test_unversioned(self):
        result = map_version_path("/api/health", version="unv", prefix="/api")
        assert result == "/api/unv/health"

    def test_root_prefix(self):
        result = map_version_path("/users/1", version="v1", prefix="/")
        assert result == "/v1/users/1"

    def test_prefix_only(self):
        result = map_version_path("/api", version="v1", prefix="/api")
        assert result == "/api/v1"

    def test_already_versioned_path_is_unchanged(self):
        result = map_version_path("/api/unv/items", version="unv", prefix="/api")
        assert result == "/api/unv/items"

    def test_already_versioned_root_prefix_path_is_unchanged(self):
        result = map_version_path("/unv/api/items", version="unv", prefix="/")
        assert result == "/unv/api/items"

    def test_trailing_slash_normalized(self):
        result = map_version_path("/api/", version="v1", prefix="/api")
        assert result == "/api/v1"

    def test_wrong_prefix_raises(self):
        with pytest.raises(ValueError, match="does not start with prefix"):
            map_version_path("/other/path", version="v1", prefix="/api")
