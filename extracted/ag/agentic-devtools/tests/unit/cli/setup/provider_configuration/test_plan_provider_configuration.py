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


def _document_with_distinct_review_providers(default_provider: dict[str, Any], review_provider: dict[str, Any]) -> dict:
    return {
        "providers": {
            "default": default_provider,
            "review": review_provider,
        },
        "workflows": {
            "pr_review": {
                "default_provider": "default",
                "nodes": {"review_files": {"provider": "review"}},
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


def test_plan_provider_configuration_custom_mapping_reconfigure_repairs_blank_default_mapping(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    custom = _document("local_model", endpoint="http://localhost")
    custom["workflows"]["pr_review"]["default_provider"] = "custom"
    custom["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "custom"
    custom["providers"]["custom"] = custom["providers"].pop("copilot_pr_review")
    custom["workflows"]["pr_review"]["default_provider"] = " "
    path.write_text(yaml.safe_dump(custom), encoding="utf-8")

    plan = plan_provider_configuration(
        tmp_path,
        reconfigure=True,
        available_models=["model-b"],
        existing_model="model-b",
        readiness=lambda _doc: ("ready", "ready"),
    )
    assert plan.status == "updated"
    assert plan.document is not None
    review = plan.document["workflows"]["pr_review"]
    assert review["default_provider"] == "copilot_pr_review"
    assert review["nodes"]["review_files"]["provider"] == "custom"


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


def test_plan_provider_configuration_reconfigure_normalizes_managed_copilot_provider(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    original = _document()
    provider = original["providers"]["copilot_pr_review"]
    provider.update(
        {
            "api_key_env": "OPENAI_KEY",
            "api_key": "inline-secret",
            "endpoint": "******example.invalid/v1?sig=secret",
            "timeout_seconds": 90,
            "token_environment_variable": "COPILOT_TOKEN",
            "temperature": 0.1,
            "max_tokens": 256,
            "top_p": 0.5,
            "presence_penalty": 0.1,
            "frequency_penalty": 0.1,
            "headers": {"Authorization": "******"},
        }
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
        "timeout_seconds": 90,
    }


def test_plan_provider_configuration_reconfigure_updates_managed_review_mapping_with_custom_default(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document("local_model", endpoint="http://localhost")
    document["providers"]["custom"] = document["providers"].pop("copilot_pr_review")
    document["workflows"]["pr_review"]["default_provider"] = "custom"
    document["providers"]["copilot_pr_review"] = {"type": "copilot", "model": "model-a"}
    document["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "copilot_pr_review"
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    result = plan_provider_configuration(
        tmp_path,
        existing_model="model-b",
        available_models=["model-b"],
        reconfigure=True,
        readiness=lambda _doc: ("ready", "ready"),
    )

    assert result.status == "updated"
    assert result.document is not None
    review = result.document["workflows"]["pr_review"]
    assert review["default_provider"] == "custom"
    assert review["nodes"]["review_files"]["provider"] == "copilot_pr_review"
    assert result.document["providers"]["copilot_pr_review"]["model"] == "model-b"


def test_plan_provider_configuration_reconfigure_updates_managed_default_mapping_with_custom_review(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document("copilot")
    document["providers"]["custom"] = {"type": "local_model", "model": "model-a", "endpoint": "http://localhost"}
    document["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "custom"
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    result = plan_provider_configuration(
        tmp_path,
        existing_model="model-b",
        available_models=["model-b"],
        reconfigure=True,
        readiness=lambda _doc: ("ready", "ready"),
    )

    assert result.status == "updated"
    assert result.document is not None
    review = result.document["workflows"]["pr_review"]
    assert review["default_provider"] == "copilot_pr_review"
    assert review["nodes"]["review_files"]["provider"] == "custom"
    assert result.document["providers"]["copilot_pr_review"]["model"] == "model-b"


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


def test_plan_provider_configuration_applies_no_refresh_readiness_per_provider(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(
        yaml.safe_dump(
            _document_with_distinct_review_providers(
                {"type": "local_model", "model": "default-model", "endpoint": "http://localhost"},
                {"type": "copilot", "model": "gemini-3.7-flash"},
            )
        ),
        encoding="utf-8",
    )
    readiness_callbacks: list[Any] = []

    def expected_readiness(_document: dict[str, Any]) -> tuple[str, str]:
        return ("unknown", "model_not_checked")

    def _ready(_document: dict[str, Any], callback) -> tuple[str, str]:
        readiness_callbacks.append(callback)
        return ("ready", "ready")

    monkeypatch.setattr(provider_configuration, "_run_readiness", _ready)

    result = plan_provider_configuration(
        tmp_path,
        reconfigure=True,
        readiness=expected_readiness,
        skip_model_refresh=True,
    )

    assert result.status == "preserved"
    assert readiness_callbacks == [None, expected_readiness]


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


def test_plan_provider_configuration_validates_default_provider_before_reporting_preserved_status(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(
        yaml.safe_dump(
            _document_with_distinct_review_providers(
                {"type": "openai_direct", "model": "gpt-4.1", "api_key_env": "MISSING"},
                {"type": "copilot", "model": "gemini-3.7-flash"},
            )
        ),
        encoding="utf-8",
    )

    result = plan_provider_configuration(tmp_path, readiness=lambda _document: ("ready", "ready"))

    assert result.status == "skipped"
    assert result.reason == "credential_missing"
    assert result.credential_status == "missing"
    assert result.provider_id == "default"


def test_plan_provider_configuration_preflights_distinct_default_and_review_providers(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(
        yaml.safe_dump(
            _document_with_distinct_review_providers(
                {"type": "local_model", "model": "default-model", "endpoint": "http://localhost"},
                {"type": "local_model", "model": "review-model", "endpoint": "http://localhost"},
            )
        ),
        encoding="utf-8",
    )
    seen_provider_ids: list[tuple[str, str]] = []

    def _ready(document: dict[str, Any]) -> tuple[str, str]:
        review = document["workflows"]["pr_review"]
        seen_provider_ids.append((review["default_provider"], review["nodes"]["review_files"]["provider"]))
        return ("ready", "ready")

    result = plan_provider_configuration(tmp_path, readiness=_ready)

    assert result.status == "preserved"
    assert result.provider_id == "review"
    assert seen_provider_ids == [("default", "default"), ("review", "review")]


def test_plan_provider_configuration_reports_selected_provider_validation_failure(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(
        yaml.safe_dump(
            _document_with_distinct_review_providers(
                {"type": "local_model", "model": "default-model", "endpoint": "http://localhost"},
                {"type": "local_model", "model": "review-model", "endpoint": "bad"},
            )
        ),
        encoding="utf-8",
    )

    result = plan_provider_configuration(tmp_path, readiness=lambda _document: ("ready", "ready"))

    assert result.status == "skipped"
    assert result.reason == "endpoint_invalid"
    assert result.provider_id == "review"


def test_plan_provider_configuration_reports_default_provider_readiness_failure(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(
        yaml.safe_dump(
            _document_with_distinct_review_providers(
                {"type": "local_model", "model": "default-model", "endpoint": "http://localhost"},
                {"type": "local_model", "model": "review-model", "endpoint": "http://localhost"},
            )
        ),
        encoding="utf-8",
    )

    def _ready(document: dict[str, Any]) -> tuple[str, str]:
        provider_id = document["workflows"]["pr_review"]["default_provider"]
        if provider_id == "default":
            return ("unavailable", "authentication_unavailable")
        return ("ready", "ready")

    result = plan_provider_configuration(tmp_path, readiness=_ready)

    assert result.status == "preserved"
    assert result.reason == "authentication_unavailable"
    assert result.provider_id == "default"


def test_plan_provider_configuration_reports_effective_override_model_on_review_failure(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document("local_model", endpoint="http://localhost")
    document["workflows"]["pr_review"]["nodes"]["review_files"]["model"] = "override-model"
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    def _ready(candidate: dict[str, Any]) -> tuple[str, str]:
        model = candidate["workflows"]["pr_review"]["nodes"]["review_files"].get("model")
        if model == "override-model":
            return ("unavailable", "model_unavailable")
        return ("ready", "ready")

    result = plan_provider_configuration(tmp_path, readiness=_ready)

    assert result.status == "preserved"
    assert result.reason == "model_unavailable"
    assert result.provider_id == "copilot_pr_review"
    assert result.provider_type == "local_model"
    assert result.model == "override-model"


def test_plan_provider_configuration_reports_workflow_override_model_on_default_failure(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document("local_model", endpoint="http://localhost")
    document["workflows"]["pr_review"]["model"] = "workflow-override"
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    def _ready(candidate: dict[str, Any]) -> tuple[str, str]:
        review = candidate["workflows"]["pr_review"]
        if review["default_provider"] == "copilot_pr_review":
            return ("unavailable", "model_unavailable")
        return ("ready", "ready")

    result = plan_provider_configuration(tmp_path, readiness=_ready)

    assert result.status == "preserved"
    assert result.reason == "model_unavailable"
    assert result.provider_id == "copilot_pr_review"
    assert result.provider_type == "local_model"
    assert result.model == "workflow-override"


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
    monkeypatch.setattr(provider_configuration, "validate_config", lambda _doc: ["bad"])
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


def test_plan_provider_configuration_reconfigure_preserves_readiness_failure_for_same_yaml(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump(_document()), encoding="utf-8")

    unchanged = plan_provider_configuration(
        tmp_path,
        available_models=["model-a"],
        existing_model="model-a",
        reconfigure=True,
        readiness=lambda _doc: ("unavailable", "authentication_unavailable"),
    )

    assert unchanged.status == "failed"
    assert unchanged.reason == "authentication_unavailable"


def test_plan_provider_configuration_rejects_invalid_template_provider_shape(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.setattr(
        provider_configuration,
        "load_provider_template",
        lambda: {"providers": {"copilot_pr_review": []}, "workflows": {}},
    )

    failed = plan_provider_configuration(
        tmp_path,
        available_models=["m"],
        readiness=lambda _doc: ("ready", "ready"),
    )

    assert failed.status == "failed"
    assert failed.reason == "configuration_invalid"


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


def test_plan_provider_configuration_custom_mapping_reconfigure_validates_default_provider_reference(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document_with_distinct_review_providers(
        {"type": "local_model", "model": "default-model"},
        {"type": "local_model", "model": "review-model", "endpoint": "http://localhost"},
    )
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    result = plan_provider_configuration(tmp_path, reconfigure=True, readiness=lambda _doc: ("ready", "ready"))

    assert result.status == "preserved"
    assert result.reason == "preserved_custom_mapping"
    assert result.provider_id == "review"


def test_plan_provider_configuration_custom_mapping_reconfigure_reports_missing_credentials(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document_with_distinct_review_providers(
        {"type": "openai_direct", "model": "default-model", "api_key_env": "MISSING"},
        {"type": "copilot", "model": "review-model"},
    )
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    result = plan_provider_configuration(tmp_path, reconfigure=True, readiness=lambda _doc: ("ready", "ready"))

    assert result.status == "failed"
    assert result.reason == "credential_missing"
    assert result.credential_status == "missing"
    assert result.provider_id == "default"


def test_plan_provider_configuration_custom_mapping_reconfigure_validates_selected_provider_reference(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document_with_distinct_review_providers(
        {"type": "local_model", "model": "default-model", "endpoint": "http://localhost"},
        {"type": "local_model", "model": "review-model", "endpoint": "bad"},
    )
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    result = plan_provider_configuration(tmp_path, reconfigure=True, readiness=lambda _doc: ("ready", "ready"))

    assert result.status == "failed"
    assert result.reason == "endpoint_invalid"
    assert result.provider_id == "review"


def test_plan_provider_configuration_reconfigure_handles_duplicate_mapping_validation_error(
    tmp_path: Path, monkeypatch
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump(_document()), encoding="utf-8")

    def _raise_duplicate(_document: dict[str, Any]) -> list[str]:
        raise DuplicateNodeMappingError(workflow="pr_review", node_type="review_files")

    monkeypatch.setattr(provider_configuration, "validate_config", _raise_duplicate)

    result = plan_provider_configuration(
        tmp_path,
        reconfigure=True,
        existing_model="model-b",
        available_models=["model-b"],
        readiness=lambda _doc: ("ready", "ready"),
    )

    assert result.status == "failed"
    assert result.reason == "configuration_invalid"


def test_plan_provider_configuration_reconfigure_handles_post_merge_mapping_error(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump(_document()), encoding="utf-8")
    monkeypatch.setattr(provider_configuration, "validate_config", lambda _document: [])
    monkeypatch.setattr(
        provider_configuration,
        "_resolve_review_providers",
        lambda _document: ("workflow_mapping_missing", None, None, None, None),
    )

    result = plan_provider_configuration(
        tmp_path,
        reconfigure=True,
        existing_model="model-b",
        available_models=["model-b"],
        readiness=lambda _doc: ("ready", "ready"),
    )

    assert result.status == "failed"
    assert result.reason == "configuration_invalid"


def test_plan_provider_configuration_reconfigure_reports_default_provider_error_for_mixed_mapping(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document()
    document["providers"]["default"] = {
        "type": "openai_direct",
        "model": "default-model",
        "api_key_env": "MISSING",
    }
    document["workflows"]["pr_review"]["default_provider"] = "default"
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    result = plan_provider_configuration(
        tmp_path,
        reconfigure=True,
        existing_model="model-b",
        available_models=["model-b"],
        readiness=lambda _doc: ("ready", "ready"),
    )

    assert result.status == "failed"
    assert result.reason == "credential_missing"
    assert result.credential_status == "missing"
    assert result.provider_id == "default"
    assert result.provider_type == "openai_direct"
    assert result.model == "default-model"


def test_plan_provider_configuration_reconfigure_reports_review_provider_error_for_mixed_mapping(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document()
    document["providers"]["review"] = {
        "type": "local_model",
        "model": "review-model",
        "endpoint": "bad",
    }
    document["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "review"
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    result = plan_provider_configuration(
        tmp_path,
        reconfigure=True,
        existing_model="model-b",
        available_models=["model-b"],
        readiness=lambda _doc: ("ready", "ready"),
    )

    assert result.status == "failed"
    assert result.reason == "endpoint_invalid"
    assert result.provider_id == "review"
    assert result.provider_type == "local_model"
    assert result.model == "review-model"


def test_plan_provider_configuration_reconfigure_reports_default_provider_readiness_for_mixed_mapping(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document()
    document["providers"]["default"] = {
        "type": "local_model",
        "model": "default-model",
        "endpoint": "http://localhost",
    }
    document["workflows"]["pr_review"]["default_provider"] = "default"
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    def _ready(candidate: dict[str, Any]) -> tuple[str, str]:
        provider_id = candidate["workflows"]["pr_review"]["nodes"]["review_files"]["provider"]
        if provider_id == "default":
            return ("unavailable", "authentication_unavailable")
        return ("ready", "ready")

    result = plan_provider_configuration(
        tmp_path,
        reconfigure=True,
        existing_model="model-b",
        available_models=["model-b"],
        readiness=_ready,
    )

    assert result.status == "failed"
    assert result.reason == "authentication_unavailable"
    assert result.provider_id == "default"
    assert result.provider_type == "local_model"
    assert result.model == "default-model"
    assert result.credential_status == "unknown"


def test_plan_provider_configuration_reconfigure_reports_managed_default_provider_readiness_for_mixed_mapping(
    tmp_path: Path,
) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document()
    document["providers"]["review"] = {
        "type": "local_model",
        "model": "review-model",
        "endpoint": "http://localhost",
    }
    document["workflows"]["pr_review"]["nodes"]["review_files"]["provider"] = "review"
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    def _ready(candidate: dict[str, Any]) -> tuple[str, str]:
        provider_id = candidate["workflows"]["pr_review"]["nodes"]["review_files"]["provider"]
        if provider_id == "copilot_pr_review":
            return ("unavailable", "authentication_unavailable")
        return ("ready", "ready")

    result = plan_provider_configuration(
        tmp_path,
        reconfigure=True,
        existing_model="model-b",
        available_models=["model-b"],
        readiness=_ready,
    )

    assert result.status == "failed"
    assert result.reason == "authentication_unavailable"
    assert result.provider_id == "copilot_pr_review"
    assert result.provider_type == "copilot"
    assert result.model == "model-b"
    assert result.credential_status == "not_required"
