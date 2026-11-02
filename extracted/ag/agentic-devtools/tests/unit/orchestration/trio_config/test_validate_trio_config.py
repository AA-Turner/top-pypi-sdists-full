"""Tests for ``validate_trio_config``."""

import json

import pytest

import agentic_devtools.orchestration.trio_config as trio_module
from agentic_devtools.orchestration.trio_config import TrioConfigValidationError, validate_trio_config
from tests.unit.orchestration.trio_config._samples import document, metadata


@pytest.mark.parametrize(
    ("field", "value", "path"),
    [
        ("schemaVersion", "2.0", "/schemaVersion"),
        ("trioRef", "Bad Ref", "/trioRef"),
        ("unknown", True, "/unknown"),
    ],
)
def test_validate_trio_config_schema_failures_report_json_pointer(field: str, value: object, path: str) -> None:
    doc = document()
    doc[field] = value
    with pytest.raises(TrioConfigValidationError) as raised:
        validate_trio_config(doc)
    assert path in raised.value.paths


def test_validate_trio_config_wraps_schema_and_materialization_errors(monkeypatch: pytest.MonkeyPatch) -> None:
    original_validate_document = trio_module._validate_document
    monkeypatch.setattr(trio_module, "_validate_document", lambda doc: (_ for _ in ()).throw(OSError("schema")))
    with pytest.raises(TrioConfigValidationError) as schema_error:
        validate_trio_config(document())
    assert isinstance(schema_error.value.__cause__, OSError)

    monkeypatch.setattr(trio_module, "_validate_document", lambda doc: None)
    with pytest.raises(TrioConfigValidationError) as materialization_error:
        validate_trio_config({"schemaVersion": "1.0"}, model_metadata={})
    assert isinstance(materialization_error.value.__cause__, KeyError)
    with pytest.raises(TrioConfigValidationError):
        validate_trio_config(document(), model_metadata="invalid")  # type: ignore[arg-type]
    with pytest.raises(TrioConfigValidationError):
        validate_trio_config([])  # type: ignore[arg-type]
    with pytest.raises(TrioConfigValidationError):
        validate_trio_config({})  # type: ignore[arg-type]

    monkeypatch.setattr(trio_module, "_validate_document", original_validate_document)

    heavy_document = document()
    heavy_document["roles"]["heavyweightDuckA"]["tier"] = "tier-1"
    with pytest.raises(TrioConfigValidationError) as heavyweight_error:
        validate_trio_config(heavy_document)
    assert "/roles/heavyweightDuckA/tier" in heavyweight_error.value.paths

    heavyweight_rounds_document = document()
    heavyweight_rounds_document["reviewCap"]["mode"] = "heavyweight_checkpoint"
    heavyweight_rounds_document["reviewCap"]["maxRounds"] = 3
    with pytest.raises(TrioConfigValidationError) as rounds_error:
        validate_trio_config(heavyweight_rounds_document)
    assert "/reviewCap/maxRounds" in rounds_error.value.paths


def test_validate_trio_config_can_materialize_valid_document() -> None:
    doc = json.loads(json.dumps(document()))
    doc["roles"]["duckA"]["fallbackModels"] = ["claude-sonnet-5", "gemini-3.1-pro-preview"]
    assert validate_trio_config(doc).trio_ref == "example-trio"

    compatible_metadata = metadata(
        "mai-code-1.1-flash",
        "gpt-5.6-luna",
        "claude-sonnet-5",
        "gemini-3.1-pro-preview",
        "claude-opus-5",
        "claude-opus-4.8",
        "claude-opus-4.6",
    )
    assert validate_trio_config(document(), model_metadata=compatible_metadata).trio_ref == "example-trio"

    with pytest.raises(TrioConfigValidationError) as missing_model_metadata:
        validate_trio_config(document(), model_metadata={})
    assert "/roles/doer/modelPreference" in missing_model_metadata.value.paths

    incompatible_metadata = json.loads(json.dumps(compatible_metadata))
    incompatible_metadata["mai-code-1.1-flash"]["tier"] = "tier-2"
    with pytest.raises(TrioConfigValidationError) as incompatible_model_metadata:
        validate_trio_config(document(), model_metadata=incompatible_metadata)
    assert "/roles/doer/modelPreference" in incompatible_model_metadata.value.paths


def test_validate_trio_config_rejects_role_tier_mismatch_from_model_metadata() -> None:
    tier_mismatch = document(doer_tier="tier-2")
    tier_mismatch["roles"]["doer"]["modelPreference"] = "mai-code-1.1-flash"
    tier_mismatch["roles"]["doer"]["fallbackModels"] = ["gemini-3.1-pro-preview"]
    with pytest.raises(TrioConfigValidationError) as mismatch_error:
        validate_trio_config(
            tier_mismatch,
            model_metadata=metadata(
                "mai-code-1.1-flash",
                "gpt-5.6-luna",
                "claude-sonnet-5",
                "gemini-3.1-pro-preview",
                "claude-opus-5",
                "claude-opus-4.8",
                "claude-opus-4.6",
            ),
        )
    assert "/roles/doer/modelPreference" in mismatch_error.value.paths
