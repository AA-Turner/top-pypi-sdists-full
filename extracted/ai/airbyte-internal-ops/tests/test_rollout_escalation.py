"""Tests for connector team oncall routing."""

from __future__ import annotations

import pytest

from airbyte_ops_mcp.connector_ops.rollouts.escalation import (
    OC_APIS_ALIAS,
    OC_DB_DW_ALIAS,
    team_oncall_alias_for_connector,
)
from airbyte_ops_mcp.registry.store import RegistryStore


@pytest.fixture
def store() -> RegistryStore:
    return RegistryStore.parse("coral:dev")


@pytest.mark.parametrize(
    "metadata,expected",
    [
        (
            {"supportLevel": "certified", "connectorType": "destination"},
            OC_DB_DW_ALIAS,
        ),
        (
            {
                "supportLevel": "certified",
                "connectorType": "source",
                "connectorSubtype": "api",
            },
            OC_APIS_ALIAS,
        ),
        (
            {
                "supportLevel": "certified",
                "connectorType": "source",
                "connectorSubtype": "database",
            },
            OC_DB_DW_ALIAS,
        ),
        (
            {
                "supportLevel": "certified",
                "connectorType": "source",
                "connectorSubtype": "file",
            },
            OC_DB_DW_ALIAS,
        ),
        (
            {
                "supportLevel": "community",
                "connectorType": "destination",
                "connectorSubtype": "database",
            },
            None,
        ),
    ],
)
def test_team_oncall_alias_for_connector(
    monkeypatch,
    store: RegistryStore,
    metadata: dict[str, str],
    expected: str | None,
) -> None:
    monkeypatch.setattr(
        "airbyte_ops_mcp.connector_ops.rollouts.escalation.CoralRegistry.get_connector_metadata",
        lambda self, connector_name: {"data": metadata},
    )
    assert team_oncall_alias_for_connector("source-test", store=store) == expected


@pytest.mark.parametrize(
    "metadata",
    [{}, {"data": None}, {"data": {}}, {"data": {"supportLevel": "certified"}}],
)
def test_team_oncall_alias_for_connector_missing_metadata(
    monkeypatch,
    store: RegistryStore,
    metadata: dict,
) -> None:
    monkeypatch.setattr(
        "airbyte_ops_mcp.connector_ops.rollouts.escalation.CoralRegistry.get_connector_metadata",
        lambda self, connector_name: metadata,
    )
    assert team_oncall_alias_for_connector("source-test", store=store) is None


def test_team_oncall_alias_for_connector_handles_exception(monkeypatch, store) -> None:
    def raise_metadata_error(self, connector_name):
        raise RuntimeError("registry unavailable")

    monkeypatch.setattr(
        "airbyte_ops_mcp.connector_ops.rollouts.escalation.CoralRegistry.get_connector_metadata",
        raise_metadata_error,
    )
    assert team_oncall_alias_for_connector("source-test", store=store) is None
