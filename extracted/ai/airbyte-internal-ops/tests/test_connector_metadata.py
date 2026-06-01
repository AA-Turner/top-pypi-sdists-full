# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for connector metadata helpers."""

from __future__ import annotations

import pytest

from airbyte_ops_mcp.connector_metadata import (
    ConnectorMetadataDpathNotFoundError,
    format_metadata_dpath_value,
    get_connector_version_from_metadata,
    get_metadata_dpath_value,
    load_raw_connector_metadata_yaml,
)


@pytest.fixture
def metadata_yaml() -> str:
    return """
data:
  dockerRepository: airbyte/source-test
  dockerImageTag: 1.2.3-rc.1
  supportLevel: certified
  tags:
    - language:python
"""


@pytest.mark.unit
def test_connector_metadata_dpath_helpers(metadata_yaml: str) -> None:
    metadata = load_raw_connector_metadata_yaml(metadata_yaml)

    assert get_metadata_dpath_value(metadata, "data/dockerImageTag") == "1.2.3-rc.1"
    assert (
        load_raw_connector_metadata_yaml(
            metadata_yaml,
            dpath_expression="data/dockerImageTag",
        )
        == "1.2.3-rc.1"
    )
    assert get_connector_version_from_metadata(metadata) == "1.2.3-rc.1"
    assert format_metadata_dpath_value(True) == "true"
    assert format_metadata_dpath_value(None) == "null"
    assert format_metadata_dpath_value({"value": "x"}) == '{\n  "value": "x"\n}'


@pytest.mark.unit
def test_connector_metadata_yaml_helpers_return_raw_metadata(
    metadata_yaml: str,
) -> None:
    metadata = load_raw_connector_metadata_yaml(metadata_yaml)

    assert metadata == {
        "data": {
            "dockerRepository": "airbyte/source-test",
            "dockerImageTag": "1.2.3-rc.1",
            "supportLevel": "certified",
            "tags": ["language:python"],
        }
    }


@pytest.mark.unit
def test_connector_metadata_dpath_missing(metadata_yaml: str) -> None:
    metadata = load_raw_connector_metadata_yaml(metadata_yaml)

    with pytest.raises(ConnectorMetadataDpathNotFoundError):
        get_metadata_dpath_value(metadata, "data/missing")


@pytest.mark.unit
def test_connector_metadata_yaml_parse_failure_raises_value_error() -> None:
    with pytest.raises(ValueError, match="Connector metadata YAML could not be parsed"):
        load_raw_connector_metadata_yaml("data: [")
