"""Tests for the provider discovery registry."""

from __future__ import annotations

from collections.abc import Iterator

import pytest

from spec_kitty_tracker.discovery.registry import (
    _resource_discoverers,
    _workspace_discoverers,
    get_resource_discoverer,
    get_workspace_discoverer,
    register_resource_discoverer,
    register_workspace_discoverer,
    registered_resource_providers,
    registered_workspace_providers,
)
from spec_kitty_tracker.errors import ConnectorConfigError


@pytest.fixture(autouse=True)
def _clean_registry() -> Iterator[None]:
    """Snapshot, clear, and restore the global registries around each test."""
    saved_workspace = dict(_workspace_discoverers)
    saved_resource = dict(_resource_discoverers)
    _workspace_discoverers.clear()
    _resource_discoverers.clear()
    yield
    _workspace_discoverers.clear()
    _resource_discoverers.clear()
    _workspace_discoverers.update(saved_workspace)
    _resource_discoverers.update(saved_resource)


def _dummy_factory(ctx: object) -> object:
    return object()


def _other_factory(ctx: object) -> object:
    return object()


# ---------------------------------------------------------------------------
# Workspace discoverer registration
# ---------------------------------------------------------------------------


class TestWorkspaceDiscovererRegistration:
    def test_register_and_lookup(self) -> None:
        register_workspace_discoverer("github", _dummy_factory)
        assert get_workspace_discoverer("github") is _dummy_factory

    def test_duplicate_raises(self) -> None:
        register_workspace_discoverer("github", _dummy_factory)
        with pytest.raises(ConnectorConfigError, match="Duplicate workspace discoverer"):
            register_workspace_discoverer("github", _other_factory)

    def test_allow_override(self) -> None:
        register_workspace_discoverer("github", _dummy_factory)
        register_workspace_discoverer("github", _other_factory, _allow_override=True)
        assert get_workspace_discoverer("github") is _other_factory

    def test_unknown_provider_raises(self) -> None:
        with pytest.raises(ConnectorConfigError, match="Unknown provider"):
            get_workspace_discoverer("trello")

    def test_introspection(self) -> None:
        register_workspace_discoverer("github", _dummy_factory)
        register_workspace_discoverer("jira", _dummy_factory)
        assert registered_workspace_providers() == frozenset({"github", "jira"})

    def test_introspection_empty(self) -> None:
        assert registered_workspace_providers() == frozenset()


# ---------------------------------------------------------------------------
# Resource discoverer registration
# ---------------------------------------------------------------------------


class TestResourceDiscovererRegistration:
    def test_register_and_lookup(self) -> None:
        register_resource_discoverer("jira", _dummy_factory)
        assert get_resource_discoverer("jira") is _dummy_factory

    def test_duplicate_raises(self) -> None:
        register_resource_discoverer("jira", _dummy_factory)
        with pytest.raises(ConnectorConfigError, match="Duplicate resource discoverer"):
            register_resource_discoverer("jira", _other_factory)

    def test_allow_override(self) -> None:
        register_resource_discoverer("jira", _dummy_factory)
        register_resource_discoverer("jira", _other_factory, _allow_override=True)
        assert get_resource_discoverer("jira") is _other_factory

    def test_unknown_provider_raises(self) -> None:
        with pytest.raises(ConnectorConfigError, match="Unknown provider"):
            get_resource_discoverer("trello")

    def test_introspection(self) -> None:
        register_resource_discoverer("jira", _dummy_factory)
        register_resource_discoverer("linear", _dummy_factory)
        register_resource_discoverer("gitlab", _dummy_factory)
        assert registered_resource_providers() == frozenset(
            {"jira", "linear", "gitlab"}
        )

    def test_introspection_empty(self) -> None:
        assert registered_resource_providers() == frozenset()


# ---------------------------------------------------------------------------
# Cross-registry isolation
# ---------------------------------------------------------------------------


class TestRegistryIsolation:
    def test_workspace_and_resource_registries_independent(self) -> None:
        register_workspace_discoverer("github", _dummy_factory)
        register_resource_discoverer("jira", _other_factory)

        assert registered_workspace_providers() == frozenset({"github"})
        assert registered_resource_providers() == frozenset({"jira"})

        # Workspace lookup should not find resource providers
        with pytest.raises(ConnectorConfigError):
            get_workspace_discoverer("jira")

        # Resource lookup should not find workspace providers
        with pytest.raises(ConnectorConfigError):
            get_resource_discoverer("github")
