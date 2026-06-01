# Copyright (c) 2025 Airbyte, Inc., all rights reserved.
"""Tests for the connector_stubs module.

These tests focus on pure logic that can be tested without mocks:
- ConnectorStub model validation
- find_stub_by_connector matching logic
- Local file operations (using temp directories for round-trip testing)
"""

from pathlib import Path

import pytest

from airbyte_ops_mcp.registry._gcs_util import (
    DEV_METADATA_SERVICE_BUCKET_NAME,
    PROD_METADATA_SERVICE_BUCKET_NAME,
    get_bucket_name,
)
from airbyte_ops_mcp.registry.connector_stubs import (
    CONNECTOR_STUBS_FILE,
    ConnectorStub,
    find_stub_by_connector,
    load_local_stubs,
    save_local_stubs,
)


@pytest.mark.parametrize(
    ("env", "expected_bucket"),
    [
        pytest.param("prod", PROD_METADATA_SERVICE_BUCKET_NAME, id="prod"),
        pytest.param("dev", DEV_METADATA_SERVICE_BUCKET_NAME, id="dev"),
    ],
)
def test_get_bucket_name(env: str, expected_bucket: str) -> None:
    """Test bucket name selection."""
    assert get_bucket_name(env) == expected_bucket


@pytest.mark.parametrize(
    ("stub_data", "expected_id", "expected_optional_none"),
    [
        pytest.param(
            {
                "id": "source-test",
                "name": "Test",
                "url": "https://docs.airbyte.com/test",
                "icon": "https://storage.googleapis.com/test/icon.svg",
            },
            "source-test",
            ["definition_id", "label", "type", "codename"],
            id="required_fields_only",
        ),
        pytest.param(
            {
                "id": "source-oracle-enterprise",
                "name": "Oracle",
                "url": "https://docs.airbyte.com/oracle",
                "icon": "https://storage.googleapis.com/icons/oracle.svg",
                "definition_id": "196a42fc-39f2-473f-88ff-d68b2ea702e9",
                "label": "enterprise",
                "type": "enterprise_source",
                "codename": "oracle-ent",
            },
            "source-oracle-enterprise",
            [],
            id="all_fields",
        ),
    ],
)
def test_connector_stub_model(
    stub_data: dict, expected_id: str, expected_optional_none: list[str]
) -> None:
    """Test ConnectorStub model validation and field handling."""
    stub = ConnectorStub(**stub_data)
    assert stub.id == expected_id
    for field in expected_optional_none:
        assert getattr(stub, field) is None


@pytest.mark.parametrize(
    ("stubs", "connector", "expected_id"),
    [
        pytest.param(
            [{"id": "source-oracle-enterprise", "name": "Oracle"}],
            "source-oracle-enterprise",
            "source-oracle-enterprise",
            id="exact_id_match",
        ),
        pytest.param(
            [{"id": "source-oracle-enterprise", "name": "Oracle"}],
            "source-oracle",
            "source-oracle-enterprise",
            id="enterprise_suffix_match",
        ),
        pytest.param(
            [{"id": "source-sap-hana", "name": "SAP HANA"}],
            "sap-hana",
            "source-sap-hana",
            id="name_match",
        ),
        pytest.param(
            [{"id": "source-oracle-enterprise", "name": "Oracle"}],
            "source-nonexistent",
            None,
            id="no_match",
        ),
    ],
)
def test_find_stub_by_connector(
    stubs: list[dict], connector: str, expected_id: str | None
) -> None:
    """Test stub lookup by various matching strategies."""
    result = find_stub_by_connector(stubs, connector)
    if expected_id is None:
        assert result is None
    else:
        assert result is not None
        assert result["id"] == expected_id


def test_local_stubs_round_trip(tmp_path: Path) -> None:
    """Test saving and loading local stubs (round-trip without mocks)."""
    test_stubs = [
        {
            "id": "source-test-enterprise",
            "name": "Test Connector",
            "url": "https://docs.airbyte.com/test",
            "icon": "https://storage.googleapis.com/test/icon.svg",
            "label": "enterprise",
        },
        {
            "id": "source-another",
            "name": "Another",
            "url": "https://docs.airbyte.com/another",
            "icon": "https://storage.googleapis.com/another/icon.svg",
        },
    ]

    save_local_stubs(tmp_path, test_stubs)
    loaded = load_local_stubs(tmp_path)

    assert loaded == test_stubs
    assert (tmp_path / CONNECTOR_STUBS_FILE).exists()


@pytest.mark.parametrize(
    ("file_content", "expected_error"),
    [
        pytest.param(None, FileNotFoundError, id="file_not_found"),
        pytest.param('{"not": "a list"}', ValueError, id="invalid_json_structure"),
    ],
)
def test_load_local_stubs_errors(
    tmp_path: Path, file_content: str | None, expected_error: type
) -> None:
    """Test error handling when loading local stubs."""
    if file_content is not None:
        (tmp_path / CONNECTOR_STUBS_FILE).write_text(file_content)

    with pytest.raises(expected_error):
        load_local_stubs(tmp_path)
