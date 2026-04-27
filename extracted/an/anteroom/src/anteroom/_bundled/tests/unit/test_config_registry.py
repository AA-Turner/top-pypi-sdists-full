"""Tests for config setting registry search and serialization."""

from __future__ import annotations

from anteroom.services.config_editor import _SENSITIVE_FIELDS, list_settable_fields
from anteroom.services.config_registry import (
    attach_current_values,
    list_config_settings,
    search_config_settings,
    setting_to_dict,
)


def test_registry_covers_all_settable_fields() -> None:
    registry_paths = {entry.dot_path for entry in list_config_settings(include_sensitive=True)}
    field_paths = {field.dot_path for field in list_settable_fields(include_sensitive=True)}
    assert field_paths <= registry_paths


def test_search_finds_plain_language_approval_settings() -> None:
    results = search_config_settings("approval permissions")
    paths = [result.entry.dot_path for result in results]
    assert "safety.approval_mode" in paths


def test_registry_excludes_sensitive_by_default() -> None:
    paths = {entry.dot_path for entry in list_config_settings()}
    assert not (paths & set(_SENSITIVE_FIELDS))


def test_current_values_redact_sensitive_fields() -> None:
    entries = [entry for entry in list_config_settings(include_sensitive=True) if entry.dot_path == "ai.api_key"]
    results = attach_current_values(entries, {"ai": {"api_key": "secret"}}, {}, [], redact_sensitive=True)
    payload = setting_to_dict(results[0].entry, current=results[0].current)
    assert payload["sensitive"] is True
    assert payload["current"]["effective_value"] == "***"
