"""Unit tests for load_provider_template."""

from pathlib import Path

import pytest

import agentic_devtools.cli.setup.provider_configuration as provider_configuration


def test_load_provider_template_raises_when_template_path_is_missing(monkeypatch) -> None:
    monkeypatch.setattr(provider_configuration, "resolve_template_path", lambda: None)

    with pytest.raises(FileNotFoundError):
        provider_configuration.load_provider_template()


def test_load_provider_template_rejects_non_mapping_root(monkeypatch) -> None:
    monkeypatch.setattr(provider_configuration, "resolve_template_path", lambda: Path("/tmp/template"))
    monkeypatch.setattr(provider_configuration.Path, "read_text", lambda *_args, **_kwargs: "[]")

    with pytest.raises(ValueError, match="root"):
        provider_configuration.load_provider_template()


def test_load_provider_template_rejects_schema_errors(monkeypatch) -> None:
    monkeypatch.setattr(provider_configuration, "resolve_template_path", lambda: Path("/tmp/template"))
    monkeypatch.setattr(provider_configuration.Path, "read_text", lambda *_args, **_kwargs: "providers: {}")
    monkeypatch.setattr(provider_configuration, "validate_config", lambda _raw: ["bad"])

    with pytest.raises(ValueError, match="validation"):
        provider_configuration.load_provider_template()


def test_load_provider_template_returns_packaged_template() -> None:
    assert provider_configuration.load_provider_template()["providers"]
