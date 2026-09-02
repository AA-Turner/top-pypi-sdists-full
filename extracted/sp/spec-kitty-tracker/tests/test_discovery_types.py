"""Tests for discovery types: construction, immutability, and serializability."""

from __future__ import annotations

import json
from dataclasses import FrozenInstanceError

import pytest

from spec_kitty_tracker.discovery.types import (
    DiscoveredResource,
    DiscoveredWorkspace,
    DiscoveryResult,
)

# ---------------------------------------------------------------------------
# DiscoveredWorkspace
# ---------------------------------------------------------------------------


class TestDiscoveredWorkspace:
    def test_construction_all_fields(self) -> None:
        ctx = {"cloud_id": "abc-123", "region": "us-east-1"}
        ws = DiscoveredWorkspace(
            id="ws-1",
            name="my-site",
            display="My Site",
            kind="site",
            provider="jira",
            provider_context=ctx,
        )
        assert ws.id == "ws-1"
        assert ws.name == "my-site"
        assert ws.display == "My Site"
        assert ws.kind == "site"
        assert ws.provider == "jira"
        assert ws.provider_context == ctx

    def test_provider_context_defaults_to_none(self) -> None:
        ws = DiscoveredWorkspace(
            id="1", name="slug", display="Display", kind="org", provider="github"
        )
        assert ws.provider_context is None

    def test_frozen(self) -> None:
        ws = DiscoveredWorkspace(
            id="1", name="slug", display="Display", kind="org", provider="github"
        )
        with pytest.raises(FrozenInstanceError):
            ws.id = "2"  # type: ignore[misc]

    def test_provider_context_accepts_none(self) -> None:
        ws = DiscoveredWorkspace(
            id="1",
            name="x",
            display="X",
            kind="org",
            provider="github",
            provider_context=None,
        )
        assert ws.provider_context is None

    def test_provider_context_json_round_trip(self) -> None:
        ctx = {"cloud_id": "abc", "nested": {"key": [1, 2, 3]}}
        ws = DiscoveredWorkspace(
            id="1",
            name="x",
            display="X",
            kind="site",
            provider="jira",
            provider_context=ctx,
        )
        serialized = json.dumps(ws.provider_context)
        assert json.loads(serialized) == ctx


# ---------------------------------------------------------------------------
# DiscoveredResource
# ---------------------------------------------------------------------------


class TestDiscoveredResource:
    def test_construction_all_fields(self) -> None:
        res = DiscoveredResource(
            provider="jira",
            parent_workspace_id="ws-1",
            resource_type="project",
            stable_ref="PROJ",
            display_name="My Project",
            connector_params={"cloud_id": "abc", "project_key": "PROJ"},
            routing_metadata={"region": "us-east-1"},
        )
        assert res.provider == "jira"
        assert res.parent_workspace_id == "ws-1"
        assert res.resource_type == "project"
        assert res.stable_ref == "PROJ"
        assert res.display_name == "My Project"
        assert res.connector_params == {"cloud_id": "abc", "project_key": "PROJ"}
        assert res.routing_metadata == {"region": "us-east-1"}

    def test_frozen(self) -> None:
        res = DiscoveredResource(
            provider="jira",
            parent_workspace_id="ws-1",
            resource_type="project",
            stable_ref="PROJ",
            display_name="My Project",
            connector_params={},
            routing_metadata={},
        )
        with pytest.raises(FrozenInstanceError):
            res.provider = "github"  # type: ignore[misc]

    def test_nested_dict_and_list_values(self) -> None:
        params = {
            "cloud_id": "abc",
            "tags": ["a", "b"],
            "nested": {"deep": True, "count": 42},
        }
        res = DiscoveredResource(
            provider="jira",
            parent_workspace_id="ws-1",
            resource_type="project",
            stable_ref="PROJ",
            display_name="My Project",
            connector_params=params,
            routing_metadata={"items": [1, 2, 3]},
        )
        assert res.connector_params["tags"] == ["a", "b"]
        assert res.routing_metadata["items"] == [1, 2, 3]

    def test_connector_params_json_round_trip(self) -> None:
        params = {"key": "val", "nested": {"a": [1, None, True]}}
        res = DiscoveredResource(
            provider="linear",
            parent_workspace_id="ws-2",
            resource_type="team",
            stable_ref="TEAM-1",
            display_name="Team Alpha",
            connector_params=params,
            routing_metadata={},
        )
        serialized = json.dumps(res.connector_params)
        assert json.loads(serialized) == params


# ---------------------------------------------------------------------------
# DiscoveryResult
# ---------------------------------------------------------------------------


class TestDiscoveryResult:
    def test_construction(self) -> None:
        ws = DiscoveredWorkspace(
            id="1", name="slug", display="Display", kind="org", provider="github"
        )
        result = DiscoveryResult(items=[ws], truncated=False)
        assert len(result.items) == 1
        assert result.items[0] is ws
        assert result.truncated is False

    def test_truncated_flag(self) -> None:
        result: DiscoveryResult[DiscoveredWorkspace] = DiscoveryResult(items=[], truncated=True)
        assert result.truncated is True

    def test_frozen(self) -> None:
        result = DiscoveryResult(items=[], truncated=False)
        with pytest.raises(FrozenInstanceError):
            result.truncated = True  # type: ignore[misc]

    def test_generic_with_resources(self) -> None:
        res = DiscoveredResource(
            provider="gitlab",
            parent_workspace_id="ws-3",
            resource_type="project",
            stable_ref="42",
            display_name="My Repo",
            connector_params={"group_id": "10"},
            routing_metadata={},
        )
        result: DiscoveryResult[DiscoveredResource] = DiscoveryResult(items=[res], truncated=False)
        assert len(result.items) == 1
        assert result.items[0].stable_ref == "42"

    def test_empty_result(self) -> None:
        result = DiscoveryResult(items=[], truncated=False)
        assert result.items == []
        assert result.truncated is False
