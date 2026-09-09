"""Unit tests for plan_provider_configuration."""

from pathlib import Path
from typing import Any
from unittest.mock import patch

import pytest
import yaml

import agentic_devtools.cli.setup.provider_configuration as provider_configuration
from agentic_devtools.cli.setup.provider_configuration import plan_provider_configuration
from agentic_devtools.orchestration.llm.errors import DuplicateNodeMappingError


@pytest.fixture(autouse=True)
def isolate_provider_runtime():
    with patch.object(provider_configuration.ProviderFactory, "preflight", return_value=None):
        yield


def _document(provider_type: str = "copilot", **provider_fields: Any) -> dict:
    provider = {"type": provider_type, "model": "model-a", **provider_fields}
    return {
        "providers": {"copilot_pr_review": provider},
        "workflows": {
            "pr_review": {
                "default_provider": "copilot_pr_review",
                "nodes": {"review_files": {"provider": "copilot_pr_review"}},
            }
        },
    }


def test_plan_provider_configuration_creates_fresh_provider_file(tmp_path: Path) -> None:
    plan = plan_provider_configuration(
        tmp_path,
        available_models=["gemini-3.7-flash"],
        readiness=lambda _document: ("ready", "ready"),
    )

    assert plan.status == "created"
    assert plan.model == "gemini-3.7-flash"
    assert plan.rendered is not None


def test_plan_provider_configuration_preserves_existing_bytes(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    content = (
        "# user comment\nproviders:\n  custom:\n    type: local_model\n    model: llama3\n"
        "workflows:\n  work_on_issue:\n    default_provider: custom\n"
    )
    path.write_text(content, encoding="utf-8")

    plan = plan_provider_configuration(tmp_path)

    assert plan.status == "skipped"
    assert plan.reason == "workflow_mapping_missing"
    assert path.read_text(encoding="utf-8") == content


def test_plan_provider_configuration_rejects_duplicate_mappings_without_reconfigure(
    tmp_path: Path, monkeypatch
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump(_document()), encoding="utf-8")

    def _raise_duplicate(_document: dict[str, Any]) -> list[str]:
        raise DuplicateNodeMappingError(workflow="pr_review", node_type="review_files")

    monkeypatch.setattr(provider_configuration, "validate_config", _raise_duplicate)

    result = plan_provider_configuration(tmp_path)

    assert result.status == "skipped"
    assert result.reason == "incomplete_configuration"


def test_plan_provider_configuration_handles_invalid_yaml_with_reconfigure(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text("providers: [", encoding="utf-8")

    ordinary = plan_provider_configuration(tmp_path)
    explicit = plan_provider_configuration(tmp_path, reconfigure=True)

    assert ordinary.status == "skipped"
    assert explicit.status == "failed"
    assert path.read_text(encoding="utf-8") == "providers: ["


def test_plan_provider_configuration_custom_mapping_reconfigure_preflights_and_fails_when_unavailable(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    custom = _document("local_model", endpoint="http://localhost")
    custom["workflows"]["pr_review"]["default_provider"] = "custom"
    custom["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "custom"
    custom["providers"]["custom"] = custom["providers"].pop("copilot_pr_review")
    path.write_text(yaml.safe_dump(custom), encoding="utf-8")

    preserved = plan_provider_configuration(
        tmp_path,
        reconfigure=True,
        readiness=lambda _doc: ("unknown", "provider_unavailable"),
    )
    assert preserved.reason == "provider_unavailable"
    assert preserved.status == "failed"


def test_plan_provider_configuration_custom_mapping_reconfigure_fails_on_invalid_mapping(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    custom = _document("local_model", endpoint="http://localhost")
    custom["workflows"]["pr_review"]["default_provider"] = "custom"
    custom["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "custom"
    custom["providers"]["custom"] = custom["providers"].pop("copilot_pr_review")
    custom["providers"].pop("custom")
    path.write_text(yaml.safe_dump(custom), encoding="utf-8")

    preserved = plan_provider_configuration(tmp_path, reconfigure=True)
    assert preserved.status == "failed"
    assert preserved.reason == "provider_missing"


def test_plan_provider_configuration_custom_mapping_reconfigure_fails_without_default_provider(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    custom = _document("local_model", endpoint="http://localhost")
    custom["workflows"]["pr_review"]["default_provider"] = "custom"
    custom["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "custom"
    custom["providers"]["custom"] = custom["providers"].pop("copilot_pr_review")
    custom["workflows"]["pr_review"]["default_provider"] = " "
    path.write_text(yaml.safe_dump(custom), encoding="utf-8")

    preserved = plan_provider_configuration(tmp_path, reconfigure=True)
    assert preserved.status == "failed"
    assert preserved.reason == "default_provider_missing"


def test_plan_provider_configuration_custom_mapping_reconfigure_validates_schema_before_preserving(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    custom = _document("copilot", temperature="0.1")
    custom["workflows"]["pr_review"]["default_provider"] = "custom"
    custom["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "custom"
    custom["providers"]["custom"] = {
        "type": "copilot",
        "model": "model-a",
        "temperature": 0.1,
    }
    custom["providers"].pop("copilot_pr_review")
    path.write_text(yaml.safe_dump(custom), encoding="utf-8")

    preserved = plan_provider_configuration(
        tmp_path,
        reconfigure=True,
        readiness=lambda _doc: ("ready", "ready"),
    )

    assert preserved.status == "failed"
    assert preserved.reason == "configuration_invalid"


def test_plan_provider_configuration_custom_mapping_reconfigure_handles_duplicate_node_mapping(
    tmp_path: Path, monkeypatch
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    custom = _document("local_model", endpoint="http://localhost")
    custom["workflows"]["pr_review"]["default_provider"] = "custom"
    custom["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "custom"
    custom["providers"]["custom"] = custom["providers"].pop("copilot_pr_review")
    path.write_text(yaml.safe_dump(custom), encoding="utf-8")

    def _raise_duplicate(_document: dict[str, Any]) -> list[str]:
        raise DuplicateNodeMappingError(workflow="pr_review", node_type="review_files")

    monkeypatch.setattr(provider_configuration, "validate_config", _raise_duplicate)

    preserved = plan_provider_configuration(tmp_path, reconfigure=True)

    assert preserved.status == "failed"
    assert preserved.reason == "configuration_invalid"


def test_plan_provider_configuration_reconfigure_paths_and_template_validation(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text("providers: {}\n", encoding="utf-8")
    incomplete = plan_provider_configuration(tmp_path)
    assert incomplete.status == "skipped"
    no_model = plan_provider_configuration(tmp_path, reconfigure=True)
    assert no_model.status == "failed"

    path.unlink()
    monkeypatch.setattr(provider_configuration, "load_provider_template", lambda: {"providers": []})
    failed = plan_provider_configuration(
        tmp_path,
        available_models=["m"],
        reconfigure=True,
        readiness=lambda _doc: ("ready", "ready"),
    )
    assert failed.reason == "configuration_invalid"


def test_plan_provider_configuration_reconfigure_does_not_mutate_existing_document(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    original = _document()
    path.write_text(yaml.safe_dump(original), encoding="utf-8")

    plan = plan_provider_configuration(
        tmp_path,
        existing_model="model-b",
        available_models=["model-b"],
        reconfigure=True,
        readiness=lambda _doc: ("ready", "ready"),
    )

    assert plan.status == "updated"
    assert plan.model == "model-b"
    assert yaml.safe_load(path.read_text(encoding="utf-8")) == original


def test_plan_provider_configuration_reconfigure_removes_fields_copilot_forbids(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    original = _document(
        "openai_direct",
        api_key_env="OPENAI_KEY",
        api_key="inline-secret",
        token_environment_variable="COPILOT_TOKEN",
        temperature=0.1,
        max_tokens=256,
        top_p=0.5,
        presence_penalty=0.1,
        frequency_penalty=0.1,
    )
    path.write_text(yaml.safe_dump(original), encoding="utf-8")

    plan = plan_provider_configuration(
        tmp_path,
        existing_model="model-b",
        available_models=["model-b"],
        reconfigure=True,
        readiness=lambda _doc: ("ready", "ready"),
    )

    assert plan.document is not None
    provider = plan.document["providers"]["copilot_pr_review"]
    assert plan.status == "updated"
    assert provider == {
        "type": "copilot",
        "model": "model-b",
        "token_environment_variable": "COPILOT_TOKEN",
    }


def test_plan_provider_configuration_does_not_override_custom_readiness_when_refresh_is_disabled(
    tmp_path: Path, monkeypatch
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    custom = _document("local_model", endpoint="http://localhost")
    custom["workflows"]["pr_review"]["default_provider"] = "custom"
    custom["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "custom"
    custom["providers"]["custom"] = custom["providers"].pop("copilot_pr_review")
    path.write_text(yaml.safe_dump(custom), encoding="utf-8")
    readiness_callbacks = []

    def _ready(_document: dict[str, Any], callback) -> tuple[str, str]:
        readiness_callbacks.append(callback)
        return ("ready", "ready")

    monkeypatch.setattr(provider_configuration, "_run_readiness", _ready)

    result = plan_provider_configuration(
        tmp_path,
        reconfigure=True,
        readiness=lambda _document: ("unknown", "model_not_checked"),
        skip_model_refresh=True,
    )

    assert result.status == "preserved"
    assert readiness_callbacks == [None]


def test_plan_provider_configuration_runs_readiness_for_existing_copilot_configuration(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump(_document()), encoding="utf-8")
    readiness_calls: list[dict[str, Any]] = []

    def _ready(document: dict[str, Any]) -> tuple[str, str]:
        readiness_calls.append(document)
        return ("ready", "ready")

    result = plan_provider_configuration(tmp_path, readiness=_ready)

    assert result.status == "preserved"
    assert result.auth_status == "ready"
    assert result.reason == "preserved_custom_config"
    assert readiness_calls == [_document()]


def test_plan_provider_configuration_handles_readiness_and_dry_run_apply_shape(tmp_path: Path) -> None:
    unavailable = plan_provider_configuration(
        tmp_path, available_models=["m"], readiness=lambda _doc: ("unavailable", "model_unavailable")
    )
    assert unavailable.status == "skipped"

    explicit_unavailable = plan_provider_configuration(
        tmp_path,
        available_models=["m"],
        reconfigure=True,
        readiness=lambda _doc: ("unknown", "provider_unavailable"),
    )
    assert explicit_unavailable.status == "failed"

    dry = plan_provider_configuration(
        tmp_path, available_models=["m"], dry_run=True, readiness=lambda _doc: ("ready", "ready")
    )
    assert dry.status == "created"


def test_plan_provider_configuration_validation_error_branch(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(provider_configuration, "validate_provider_configuration", lambda _doc: ["bad"])
    plan = plan_provider_configuration(
        tmp_path,
        available_models=["m"],
        readiness=lambda _doc: ("ready", "ready"),
    )
    assert plan.status == "failed"
    assert plan.reason == "configuration_invalid"


def test_plan_provider_configuration_reconfigure_reports_no_change_for_same_model(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump(_document()), encoding="utf-8")

    unchanged = plan_provider_configuration(
        tmp_path,
        available_models=["model-a"],
        existing_model="model-a",
        reconfigure=True,
        readiness=lambda _doc: ("ready", "ready"),
    )

    assert unchanged.status == "preserved"
    assert unchanged.reason == "no_change"


def test_plan_provider_configuration_reconfigure_rejects_malformed_existing_documents(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    malformed_documents = [
        {"providers": {"copilot_pr_review": []}, "workflows": {}},
        {"providers": {"copilot_pr_review": {"type": "copilot", "model": "m"}}, "workflows": []},
        {
            "providers": {"copilot_pr_review": {"type": "copilot", "model": "m"}},
            "workflows": {"pr_review": []},
        },
        {
            "providers": {"copilot_pr_review": {"type": "copilot", "model": "m"}},
            "workflows": {"pr_review": {"nodes": []}},
        },
        {
            "providers": {"copilot_pr_review": {"type": "copilot", "model": "m"}},
            "workflows": {"pr_review": {"nodes": {"review_files": []}}},
        },
    ]
    for document in malformed_documents:
        path.write_text(yaml.safe_dump(document), encoding="utf-8")
        result = plan_provider_configuration(
            tmp_path,
            available_models=["m"],
            reconfigure=True,
            readiness=lambda _doc: ("ready", "ready"),
        )
        assert result.reason == "configuration_invalid"
