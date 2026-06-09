# Copyright (c) 2026 Airbyte, Inc., all rights reserved.
"""Tests for connector metadata validation."""

from __future__ import annotations

import pytest
from airbyte_connector_models.metadata.v0.connector_metadata_definition_v0 import (
    ConnectorMetadataDefinitionV0,
)

from airbyte_ops_mcp.metadata_validator import (
    ValidatorOptions,
    validate_version_and_progressive_rollout_configuration,
)


def _metadata_model(
    *,
    docker_image_tag: str,
    enable_progressive_rollout: bool | None,
) -> ConnectorMetadataDefinitionV0:
    metadata: dict[str, object] = {
        "metadataSpecVersion": "1.0",
        "data": {
            "name": "Test Source",
            "definitionId": "f14d5125-dc0d-4f6c-abe5-acde821a2203",
            "connectorType": "source",
            "connectorSubtype": "api",
            "dockerRepository": "airbyte/source-test",
            "dockerImageTag": docker_image_tag,
            "license": "ELv2",
            "documentationUrl": "https://docs.airbyte.com/integrations/sources/test",
            "githubIssueLabel": "source-test",
            "releaseStage": "alpha",
            "supportLevel": "community",
            "tags": ["language:python"],
        },
    }
    if enable_progressive_rollout is not None:
        data = metadata["data"]
        assert isinstance(data, dict)
        data["releases"] = {
            "rolloutConfiguration": {
                "enableProgressiveRollout": enable_progressive_rollout,
            },
        }

    return ConnectorMetadataDefinitionV0.model_validate(metadata)


@pytest.mark.unit
@pytest.mark.parametrize(
    "docker_image_tag,enable_progressive_rollout,expected_valid",
    [
        pytest.param("1.2.3", True, True, id="ga_progressive_rollout_enabled"),
        pytest.param("1.2.3-rc.1", True, True, id="rc_progressive_rollout_enabled"),
        pytest.param("1.2.3-rc.1", None, False, id="rc_requires_rollout_config"),
    ],
)
def test_validate_version_and_progressive_rollout_configuration(
    docker_image_tag: str,
    enable_progressive_rollout: bool | None,
    expected_valid: bool,
) -> None:
    metadata = _metadata_model(
        docker_image_tag=docker_image_tag,
        enable_progressive_rollout=enable_progressive_rollout,
    )

    is_valid, _ = validate_version_and_progressive_rollout_configuration(
        metadata,
        ValidatorOptions(docs_path=""),
    )

    assert is_valid is expected_valid
