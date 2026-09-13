"""Unit tests for check_provider_configuration."""

from pathlib import Path

import yaml

import agentic_devtools.cli.setup.provider_configuration as provider_configuration
from agentic_devtools.cli.setup.provider_configuration import check_provider_configuration
from agentic_devtools.orchestration.llm.errors import DuplicateNodeMappingError


def _document(provider_type: str = "copilot", **provider_fields: str) -> dict:
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


def _document_with_distinct_review_providers(default_provider: dict, review_provider: dict) -> dict:
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


def test_check_provider_configuration_handles_missing_file(tmp_path: Path) -> None:
    checked = check_provider_configuration(tmp_path)

    assert not checked.found
    assert checked.reason == "missing_file"


def test_check_provider_configuration_handles_unreadable_path(monkeypatch) -> None:
    def _raise(_self):
        raise OSError("permission denied")

    monkeypatch.setattr(Path, "exists", _raise)
    result = check_provider_configuration(Path("/tmp/repository"))

    assert not result.found
    assert result.reason == "missing_file"


def test_check_provider_configuration_covers_provider_validation_paths(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    documents = [
        _document("unsupported"),
        _document("copilot", api_key_env="SECRET"),
        _document("openai_direct"),
        _document("openai_direct", api_key_env="MISSING"),
        _document("azure_openai", api_key_env="MISSING"),
        _document("azure_openai", api_key_env="KEY", endpoint="bad"),
        _document("local_model"),
        _document("local_model", endpoint="bad"),
        _document("local_model", endpoint="http://localhost"),
    ]
    expected = [
        "provider_type_invalid",
        "copilot_api_key_env_forbidden",
        "credential_reference_missing",
        "credential_missing",
        "credential_missing",
        "credential_missing",
        "provider_unavailable",
        "endpoint_invalid",
        "provider_unavailable",
    ]
    for document, reason in zip(documents, expected, strict=True):
        path.write_text(yaml.safe_dump(document), encoding="utf-8")
        result = check_provider_configuration(tmp_path, readiness=lambda _doc: ("unknown", "provider_unavailable"))
        assert result.reason == reason

    path.write_text(yaml.safe_dump(_document("openai_direct", api_key_env="KEY")), encoding="utf-8")
    monkeypatch.setenv("KEY", "present")
    result = check_provider_configuration(tmp_path, readiness=lambda _doc: ("ready", "ready"))
    assert result.valid
    assert result.report_details()["status"] == "preserved"


def test_check_provider_configuration_reports_invalid_yaml(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text("providers: [", encoding="utf-8")

    assert check_provider_configuration(tmp_path).reason == "invalid_yaml"


def test_check_provider_configuration_handles_duplicate_mappings(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump(_document()), encoding="utf-8")

    def _raise_duplicate(_document: dict) -> list[str]:
        raise DuplicateNodeMappingError(workflow="pr_review", node_type="review_files")

    monkeypatch.setattr(provider_configuration, "validate_config", _raise_duplicate)

    result = check_provider_configuration(tmp_path)

    assert result.valid is False
    assert result.reason == "duplicate_node_mapping"


def test_check_provider_configuration_reports_specific_mapping_errors(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)

    path.write_text("workflows: {}\n", encoding="utf-8")
    assert check_provider_configuration(tmp_path).reason == "workflow_mapping_missing"

    default_missing = _document()
    default_missing["workflows"]["pr_review"]["default_provider"] = " "
    path.write_text(yaml.safe_dump(default_missing), encoding="utf-8")
    assert check_provider_configuration(tmp_path).reason == "default_provider_missing"

    missing_node = _document()
    missing_node["workflows"]["pr_review"]["nodes"] = {}
    path.write_text(yaml.safe_dump(missing_node), encoding="utf-8")
    assert check_provider_configuration(tmp_path).reason == "review_files_mapping_missing"

    missing_model = _document()
    missing_model["providers"]["copilot_pr_review"].pop("model")
    path.write_text(yaml.safe_dump(missing_model), encoding="utf-8")
    assert check_provider_configuration(tmp_path).reason == "model_missing"


def test_check_provider_configuration_does_not_mask_mapping_error_with_default_provider_error(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document_with_distinct_review_providers(
        {"type": "openai_direct", "model": "gpt-4.1", "api_key_env": "MISSING"},
        {"type": "copilot", "model": "gemini-3.7-flash"},
    )
    document["workflows"]["pr_review"]["nodes"] = {}
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    result = check_provider_configuration(tmp_path)

    assert result.valid is False
    assert result.reason == "review_files_mapping_missing"


def test_check_provider_configuration_reports_malformed_endpoint(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    monkeypatch.setenv("KEY", "present")
    path.write_text(
        yaml.safe_dump(_document("azure_openai", api_key_env="KEY", endpoint="http://[")),
        encoding="utf-8",
    )

    assert check_provider_configuration(tmp_path).reason == "endpoint_invalid"


def test_check_provider_configuration_validates_default_provider_reference_independently(tmp_path: Path) -> None:
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

    result = check_provider_configuration(tmp_path, readiness=lambda _doc: ("ready", "ready"))

    assert result.reason == "credential_missing"
    assert result.provider_id == "default"
    assert result.provider_type == "openai_direct"


def test_check_provider_configuration_preflights_default_and_review_provider_separately(tmp_path: Path) -> None:
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

    def _ready(document: dict) -> tuple[str, str]:
        review = document["workflows"]["pr_review"]
        seen_provider_ids.append((review["default_provider"], review["nodes"]["review_files"]["provider"]))
        return ("ready", "ready")

    result = check_provider_configuration(tmp_path, readiness=_ready)

    assert result.valid is True
    assert result.provider_id == "review"
    assert seen_provider_ids == [("default", "default"), ("review", "review")]


def test_check_provider_configuration_reports_effective_override_model_on_review_failure(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    document = _document()
    document["providers"]["copilot_pr_review"]["type"] = "local_model"
    document["providers"]["copilot_pr_review"]["endpoint"] = "http://localhost"
    document["workflows"]["pr_review"]["nodes"]["review_files"]["model"] = "override-model"
    path.write_text(yaml.safe_dump(document), encoding="utf-8")

    def _ready(candidate: dict) -> tuple[str, str]:
        model = candidate["workflows"]["pr_review"]["nodes"]["review_files"].get("model")
        if model == "override-model":
            return ("unavailable", "model_unavailable")
        return ("ready", "ready")

    result = check_provider_configuration(tmp_path, readiness=_ready)

    assert result.valid is False
    assert result.reason == "model_unavailable"
    assert result.provider_id == "copilot_pr_review"
    assert result.provider_type == "local_model"
    assert result.model == "override-model"


def test_check_provider_configuration_validates_selected_provider_reference_independently(tmp_path: Path) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(
        yaml.safe_dump(
            _document_with_distinct_review_providers(
                {"type": "local_model", "model": "default-model", "endpoint": "http://localhost"},
                {"type": "local_model", "model": "review-model"},
            )
        ),
        encoding="utf-8",
    )

    result = check_provider_configuration(tmp_path, readiness=lambda _doc: ("ready", "ready"))

    assert result.reason == "ready"
    assert result.provider_id == "review"
    assert result.provider_type == "local_model"
    assert result.valid is True


def test_check_provider_configuration_reports_selected_provider_validation_error(tmp_path: Path) -> None:
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

    result = check_provider_configuration(tmp_path, readiness=lambda _doc: ("ready", "ready"))

    assert result.valid is False
    assert result.reason == "endpoint_invalid"
    assert result.provider_id == "review"
    assert result.provider_type == "local_model"


def test_check_provider_configuration_defensively_handles_unresolved_provider_ids(tmp_path: Path, monkeypatch) -> None:
    path = tmp_path / ".agdt" / "config" / "llm-providers.yml"
    path.parent.mkdir(parents=True)
    path.write_text(yaml.safe_dump(_document()), encoding="utf-8")
    monkeypatch.setattr(provider_configuration, "validate_config", lambda _document: [])
    monkeypatch.setattr(
        provider_configuration,
        "_resolve_review_providers",
        lambda _document: (None, None, None, None, None),
    )
    monkeypatch.setattr(provider_configuration, "_validate_provider_mapping", lambda _provider: None)

    result = check_provider_configuration(tmp_path, readiness=lambda _doc: ("ready", "ready"))

    assert result.valid is False
    assert result.reason == "provider_missing"
