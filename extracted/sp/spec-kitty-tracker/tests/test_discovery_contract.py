"""Contract conformance tests for all registered discovery providers.

Validates that every provider's workspace and resource discovery output
conforms to the shared contract: field presence, types, serializability,
and DiscoveryResult envelope shape.

These tests are provider-agnostic -- they do NOT assert provider-specific
field values, only structural conformance.
"""

from __future__ import annotations

import json
from typing import Any
from unittest.mock import patch

import httpx
import pytest
from discovery_helpers import (
    assert_all_metadata_serializable,
    assert_canonical_ids_not_duplicated_in_metadata,
    assert_resource_normalized_keys_typed_when_present,
    assert_valid_resource,
    assert_valid_workspace,
    assert_workspace_context_serializable,
    assert_workspace_normalized_keys_typed_when_present,
    load_provider_fixture,
)

from spec_kitty_tracker.discovery import (
    discover_resources,
    discover_workspaces,
)
from spec_kitty_tracker.discovery.registry import (
    registered_resource_providers,
    registered_workspace_providers,
)
from spec_kitty_tracker.discovery.types import (
    DiscoveredWorkspace,
    DiscoveryResult,
)
from spec_kitty_tracker.nango import NangoConnectionContext

# ---------------------------------------------------------------------------
# Mock transport
# ---------------------------------------------------------------------------


class RoutingMockTransport(httpx.AsyncBaseTransport):
    """Returns canned responses based on URL pattern matching."""

    def __init__(
        self,
        routes: dict[str, tuple[int, Any, dict[str, str] | None]],
    ) -> None:
        self._routes = routes

    async def handle_async_request(self, request: httpx.Request) -> httpx.Response:
        url_str = str(request.url)
        path = request.url.raw_path.decode("ascii")

        for pattern, (status, body, extra_headers) in self._routes.items():
            if pattern in url_str or pattern in path:
                headers: dict[str, str] = {"content-type": "application/json"}
                if extra_headers:
                    headers.update(extra_headers)
                return httpx.Response(
                    status_code=status,
                    content=json.dumps(body).encode(),
                    headers=headers,
                )
        raise ValueError(f"No mock route for {url_str} (path={path})")

    async def aclose(self) -> None:
        pass


# ---------------------------------------------------------------------------
# Per-provider mock route configurations and workspace factories
# ---------------------------------------------------------------------------

# Each entry maps a provider name to:
#   workspace_routes:  mock routes needed for workspace discovery
#   resource_routes:   mock routes needed for resource discovery
#   make_workspace:    callable returning a workspace to feed into resource discovery


def _linear_workspace_routes() -> dict[str, tuple[int, Any, dict[str, str] | None]]:
    body = load_provider_fixture("linear", "workspace")
    return {"/graphql": (200, body, None)}


def _linear_resource_routes() -> dict[str, tuple[int, Any, dict[str, str] | None]]:
    body = load_provider_fixture("linear", "resource")
    return {"/graphql": (200, body, None)}


def _linear_workspace() -> DiscoveredWorkspace:
    return DiscoveredWorkspace(
        id="org-uuid-1",
        name="acme-eng",
        display="Acme Engineering",
        kind="workspace",
        provider="linear",
        provider_context={
            "org_id": "org-uuid-1",
            "url_key": "acme-eng",
            "workspace_handle": "acme-eng",
            "workspace_url": "https://linear.app/acme-eng",
        },
    )


def _jira_workspace_routes() -> dict[str, tuple[int, Any, dict[str, str] | None]]:
    body = load_provider_fixture("jira", "workspace")
    return {"/oauth/token/accessible-resources": (200, body, None)}


def _jira_resource_routes() -> dict[str, tuple[int, Any, dict[str, str] | None]]:
    body = load_provider_fixture("jira", "resource")
    return {"/rest/api/3/project/search": (200, body, None)}


def _jira_workspace() -> DiscoveredWorkspace:
    return DiscoveredWorkspace(
        id="cloud-abc",
        name="My Site",
        display="https://mysite.atlassian.net",
        kind="site",
        provider="jira",
        provider_context={
            "cloud_id": "cloud-abc",
            "site_url": "https://mysite.atlassian.net",
            "workspace_handle": "mysite",
            "workspace_url": "https://mysite.atlassian.net",
        },
    )


def _github_workspace_routes() -> dict[str, tuple[int, Any, dict[str, str] | None]]:
    fixture = load_provider_fixture("github", "workspace")
    return {
        "/user/orgs": (200, fixture["orgs"], None),
        "/user": (200, fixture["user"], None),
    }


def _github_resource_routes() -> dict[str, tuple[int, Any, dict[str, str] | None]]:
    body = load_provider_fixture("github", "resource")
    return {"/orgs/acme/repos": (200, body, None)}


def _github_workspace() -> DiscoveredWorkspace:
    return DiscoveredWorkspace(
        id="100",
        name="acme",
        display="Acme Corp",
        kind="org",
        provider="github",
        provider_context={
            "workspace_type": "org",
            "login": "acme",
            "account_id": "100",
            "workspace_handle": "acme",
            "workspace_url": "https://github.com/acme",
        },
    )


def _gitlab_workspace_routes() -> dict[str, tuple[int, Any, dict[str, str] | None]]:
    body = load_provider_fixture("gitlab", "workspace")
    return {"/api/v4/groups": (200, body, None)}


def _gitlab_resource_routes() -> dict[str, tuple[int, Any, dict[str, str] | None]]:
    body = load_provider_fixture("gitlab", "resource")
    return {"/api/v4/groups/42/projects": (200, body, None)}


def _gitlab_workspace() -> DiscoveredWorkspace:
    return DiscoveredWorkspace(
        id="42",
        name="acme/engineering",
        display="Acme / Engineering",
        kind="group",
        provider="gitlab",
        provider_context={
            "group_id": "42",
            "full_path": "acme/engineering",
            "web_url": "https://gitlab.com/groups/acme/engineering",
            "workspace_handle": "acme/engineering",
            "workspace_url": "https://gitlab.com/groups/acme/engineering",
        },
    )


# ---------------------------------------------------------------------------
# Provider config registry
# ---------------------------------------------------------------------------

PROVIDER_CONFIG: dict[
    str,
    dict[str, Any],
] = {
    "linear": {
        "workspace_routes": _linear_workspace_routes,
        "resource_routes": _linear_resource_routes,
        "make_workspace": _linear_workspace,
        "transport_patch_target": (
            "spec_kitty_tracker.discovery.providers.linear.NangoProxyTransport"
        ),
    },
    "jira": {
        "workspace_routes": _jira_workspace_routes,
        "resource_routes": _jira_resource_routes,
        "make_workspace": _jira_workspace,
        "transport_patch_target": "spec_kitty_tracker.discovery.providers.jira.NangoProxyTransport",
    },
    "github": {
        "workspace_routes": _github_workspace_routes,
        "resource_routes": _github_resource_routes,
        "make_workspace": _github_workspace,
        "transport_patch_target": (
            "spec_kitty_tracker.discovery.providers.github.NangoProxyTransport"
        ),
    },
    "gitlab": {
        "workspace_routes": _gitlab_workspace_routes,
        "resource_routes": _gitlab_resource_routes,
        "make_workspace": _gitlab_workspace,
        "transport_patch_target": (
            "spec_kitty_tracker.discovery.providers.gitlab.NangoProxyTransport"
        ),
    },
}

# ---------------------------------------------------------------------------
# Per-provider populated normalized keys (descriptive only, NOT a test gate)
# ---------------------------------------------------------------------------
#
# As of the 006-hosted-discovery-contract-hardening mission, the four current
# in-scope providers happen to populate all four normalized optional keys
# (workspace_handle, workspace_url, display_key, resource_url) because each
# one has cheap meaningful values per research.md §R1. The table below
# records that current state for maintainer reference:
#
#   Provider | workspace_handle | workspace_url | display_key | resource_url
#   ---------|------------------|---------------|-------------|--------------
#   linear   | populated        | populated     | populated   | populated
#   jira     | populated        | populated     | populated   | populated
#   github   | populated        | populated     | populated   | populated
#   gitlab   | populated        | populated     | populated   | populated
#
# The contract test does NOT enforce this table. It enforces type-when-present
# only. A future provider may legitimately omit any of the four normalized
# keys, and that omission is contract-conformant. See data-model.md
# §"Per-provider populated normalized keys (descriptive, not contractually
# required)" and contracts/discovery-contract.md §5.1 C-003/C-004/C-007/C-008.
# ---------------------------------------------------------------------------

ALL_PROVIDERS = list(PROVIDER_CONFIG.keys())


def _make_context(provider: str) -> NangoConnectionContext:
    return NangoConnectionContext(
        connection_id=f"conn-{provider}",
        provider_config_key=f"{provider}-test",
        nango_secret_key="sk-test",
    )


# ---------------------------------------------------------------------------
# T036: Parametrized contract conformance tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("provider", ALL_PROVIDERS)
class TestWorkspaceContractConformance:
    """Validate workspace discovery contract across all providers."""

    async def test_workspace_discovery_returns_valid_workspaces(self, provider: str) -> None:
        config = PROVIDER_CONFIG[provider]
        routes = config["workspace_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_workspaces(provider, ctx)

        assert len(result.items) >= 1, f"{provider}: expected at least 1 workspace"
        for ws in result.items:
            assert_valid_workspace(ws)

    async def test_workspace_provider_context_serializable(self, provider: str) -> None:
        config = PROVIDER_CONFIG[provider]
        routes = config["workspace_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_workspaces(provider, ctx)

        for ws in result.items:
            assert_workspace_context_serializable(ws)

    async def test_workspace_normalized_keys_typed_when_present(self, provider: str) -> None:
        """For each present normalized workspace key, value is str | None.
        Absent keys are contractually allowed and produce no assertion."""
        config = PROVIDER_CONFIG[provider]
        routes = config["workspace_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_workspaces(provider, ctx)

        assert result.items, f"{provider}: expected at least one workspace"
        for ws in result.items:
            assert_workspace_normalized_keys_typed_when_present(ws)

    async def test_workspace_canonical_ids_not_duplicated_in_metadata(self, provider: str) -> None:
        """workspace.id must not equal provider_context['workspace_handle']
        when the latter is present. Skips silently when handle is absent."""
        config = PROVIDER_CONFIG[provider]
        routes = config["workspace_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_workspaces(provider, ctx)

        for ws in result.items:
            assert_canonical_ids_not_duplicated_in_metadata(ws=ws)


@pytest.mark.parametrize("provider", ALL_PROVIDERS)
class TestResourceContractConformance:
    """Validate resource discovery contract across all providers."""

    async def test_resource_discovery_returns_valid_resources(self, provider: str) -> None:
        config = PROVIDER_CONFIG[provider]
        routes = config["resource_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)
        workspace = config["make_workspace"]()

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_resources(provider, workspace, ctx)

        assert len(result.items) >= 1, f"{provider}: expected at least 1 resource"
        for res in result.items:
            assert_valid_resource(res)

    async def test_resource_metadata_serializable(self, provider: str) -> None:
        config = PROVIDER_CONFIG[provider]
        routes = config["resource_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)
        workspace = config["make_workspace"]()

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_resources(provider, workspace, ctx)

        for res in result.items:
            assert_all_metadata_serializable(res)

    async def test_resource_normalized_keys_typed_when_present(self, provider: str) -> None:
        """For each present normalized resource key, value is str | None.
        Absent keys are contractually allowed and produce no assertion."""
        config = PROVIDER_CONFIG[provider]
        routes = config["resource_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)
        workspace = config["make_workspace"]()

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_resources(provider, workspace, ctx)

        assert result.items, f"{provider}: expected at least one resource"
        for res in result.items:
            assert_resource_normalized_keys_typed_when_present(res)

    async def test_resource_canonical_ids_not_duplicated_in_metadata(self, provider: str) -> None:
        """resource.stable_ref must not equal routing_metadata['display_key']
        when the latter is present. Skips silently when display_key is absent."""
        config = PROVIDER_CONFIG[provider]
        routes = config["resource_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)
        workspace = config["make_workspace"]()

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_resources(provider, workspace, ctx)

        for res in result.items:
            assert_canonical_ids_not_duplicated_in_metadata(res=res)


# ---------------------------------------------------------------------------
# T037: Verify DiscoveryResult shape
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("provider", ALL_PROVIDERS)
class TestDiscoveryResultShape:
    """Validate the DiscoveryResult envelope shape for all providers."""

    async def test_workspace_result_is_discovery_result(self, provider: str) -> None:
        config = PROVIDER_CONFIG[provider]
        routes = config["workspace_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_workspaces(provider, ctx)

        assert isinstance(result, DiscoveryResult)
        assert isinstance(result.items, list)
        assert isinstance(result.truncated, bool)

    async def test_resource_result_is_discovery_result(self, provider: str) -> None:
        config = PROVIDER_CONFIG[provider]
        routes = config["resource_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)
        workspace = config["make_workspace"]()

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_resources(provider, workspace, ctx)

        assert isinstance(result, DiscoveryResult)
        assert isinstance(result.items, list)
        assert isinstance(result.truncated, bool)

    async def test_workspace_not_truncated_with_small_result(self, provider: str) -> None:
        """When fewer results than page limit, truncated should be False."""
        config = PROVIDER_CONFIG[provider]
        routes = config["workspace_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_workspaces(provider, ctx)

        # Our mock data returns a small number of items, well below any page limit
        assert result.truncated is False

    async def test_resource_not_truncated_with_small_result(self, provider: str) -> None:
        """When fewer results than page limit, truncated should be False."""
        config = PROVIDER_CONFIG[provider]
        routes = config["resource_routes"]()
        mock = RoutingMockTransport(routes)
        ctx = _make_context(provider)
        workspace = config["make_workspace"]()

        with patch(config["transport_patch_target"], return_value=mock):
            result = await discover_resources(provider, workspace, ctx)

        assert result.truncated is False


# ---------------------------------------------------------------------------
# T038: Registry completeness
# ---------------------------------------------------------------------------


class TestRegistryCompleteness:
    """Verify all 4 providers are registered in both registries."""

    def test_all_providers_registered_for_workspaces(self) -> None:
        ws_providers = registered_workspace_providers()
        expected = {"linear", "jira", "github", "gitlab"}
        assert ws_providers >= expected, f"Missing workspace providers: {expected - ws_providers}"

    def test_all_providers_registered_for_resources(self) -> None:
        rs_providers = registered_resource_providers()
        expected = {"linear", "jira", "github", "gitlab"}
        assert rs_providers >= expected, f"Missing resource providers: {expected - rs_providers}"

    def test_workspace_and_resource_providers_match(self) -> None:
        """Every workspace provider should also have a resource provider."""
        ws_providers = registered_workspace_providers()
        rs_providers = registered_resource_providers()
        expected = {"linear", "jira", "github", "gitlab"}
        for provider in expected:
            assert provider in ws_providers, f"{provider} missing from workspace registry"
            assert provider in rs_providers, f"{provider} missing from resource registry"
