"""DiscoveryContractError raise tests for all four providers.

For each provider, this file exercises the validator's rule branches by
constructing dataclasses with deliberately malformed metadata sourced from
tests/fixtures/discovery/<provider>/malformed/*.json. Each test asserts
that DiscoveryContractError is raised with the expected reason code, kind,
and field_path.

These tests bypass the per-provider HTTP adapters intentionally — the
validator's job is to catch contract violations regardless of where the
bad value came from. We construct DiscoveredWorkspace / DiscoveredResource
directly and feed them to validate_workspace_result / validate_resource_result.

See kitty-specs/006-hosted-discovery-contract-hardening/contracts/
discovery-contract.md §5.2 for the full conformance obligations.
"""

from __future__ import annotations

import pytest
from discovery_helpers import load_provider_fixture

from spec_kitty_tracker import (
    DiscoveredResource,
    DiscoveredWorkspace,
    DiscoveryContractError,
    DiscoveryResult,
    SpecKittyTrackerError,
)
from spec_kitty_tracker.discovery._validation import (
    validate_resource_result,
    validate_workspace_result,
)

ALL_PROVIDERS = ["linear", "jira", "github", "gitlab"]


def _make_workspace(provider: str, provider_context: object) -> DiscoveredWorkspace:
    """Construct a DiscoveredWorkspace with a deliberately bad provider_context.

    The dataclass itself does not validate, so this construction succeeds
    even though the validator will reject it.
    """
    return DiscoveredWorkspace(
        id="test-id",
        name="test-name",
        display="Test Display",
        kind="workspace",
        provider=provider,
        provider_context=provider_context,  # type: ignore[arg-type]
    )


def _make_resource(provider: str, routing_metadata: object) -> DiscoveredResource:
    """Construct a DiscoveredResource with a deliberately bad routing_metadata."""
    return DiscoveredResource(
        provider=provider,
        parent_workspace_id="test-ws-id",
        resource_type="test-type",
        stable_ref="test-stable-ref",
        display_name="Test Display",
        connector_params={"k": "v"},
        routing_metadata=routing_metadata,  # type: ignore[arg-type]
    )


# ---------------------------------------------------------------------------
# Workspace error tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("provider", ALL_PROVIDERS)
class TestWorkspaceContractErrors:
    """Verify DiscoveryContractError raises with correct attribution
    for each provider's malformed workspace fixtures."""

    def test_provider_context_not_dict_raises_ws_006(self, provider: str) -> None:
        fixture = load_provider_fixture(provider, "malformed/workspace_provider_context_not_dict")
        bad_ctx = fixture["_inject_provider_context"]
        ws = _make_workspace(provider, bad_ctx)
        result: DiscoveryResult[DiscoveredWorkspace] = DiscoveryResult(items=[ws], truncated=False)

        with pytest.raises(DiscoveryContractError) as exc_info:
            validate_workspace_result(result)

        exc = exc_info.value
        assert exc.reason == "WS-006", f"{provider}: expected reason WS-006, got {exc.reason!r}"
        assert exc.kind == "workspace"
        assert exc.provider == provider
        assert "provider_context" in (exc.field_path or "")
        assert isinstance(exc, SpecKittyTrackerError)

    def test_workspace_handle_wrong_type_raises_ws_008(self, provider: str) -> None:
        fixture = load_provider_fixture(provider, "malformed/workspace_handle_wrong_type")
        bad_ctx = fixture["_inject_provider_context"]
        ws = _make_workspace(provider, bad_ctx)
        result: DiscoveryResult[DiscoveredWorkspace] = DiscoveryResult(items=[ws], truncated=False)

        with pytest.raises(DiscoveryContractError) as exc_info:
            validate_workspace_result(result)

        exc = exc_info.value
        assert exc.reason == "WS-008", f"{provider}: expected reason WS-008, got {exc.reason!r}"
        assert exc.kind == "workspace"
        assert exc.provider == provider
        assert "workspace_handle" in (exc.field_path or "")
        assert isinstance(exc, SpecKittyTrackerError)


# ---------------------------------------------------------------------------
# Resource error tests
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("provider", ALL_PROVIDERS)
class TestResourceContractErrors:
    """Verify DiscoveryContractError raises with correct attribution
    for each provider's malformed resource fixtures."""

    def test_routing_metadata_not_dict_raises_rs_009(self, provider: str) -> None:
        fixture = load_provider_fixture(provider, "malformed/resource_routing_metadata_not_dict")
        bad_rm = fixture["_inject_routing_metadata"]
        res = _make_resource(provider, bad_rm)
        result: DiscoveryResult[DiscoveredResource] = DiscoveryResult(items=[res], truncated=False)

        with pytest.raises(DiscoveryContractError) as exc_info:
            validate_resource_result(result)

        exc = exc_info.value
        assert exc.reason == "RS-009", f"{provider}: expected reason RS-009, got {exc.reason!r}"
        assert exc.kind == "resource"
        assert exc.provider == provider
        assert "routing_metadata" in (exc.field_path or "")
        assert isinstance(exc, SpecKittyTrackerError)

    def test_display_key_wrong_type_raises_rs_011(self, provider: str) -> None:
        fixture = load_provider_fixture(provider, "malformed/resource_display_key_wrong_type")
        bad_rm = fixture["_inject_routing_metadata"]
        res = _make_resource(provider, bad_rm)
        result: DiscoveryResult[DiscoveredResource] = DiscoveryResult(items=[res], truncated=False)

        with pytest.raises(DiscoveryContractError) as exc_info:
            validate_resource_result(result)

        exc = exc_info.value
        assert exc.reason == "RS-011", f"{provider}: expected reason RS-011, got {exc.reason!r}"
        assert exc.kind == "resource"
        assert exc.provider == provider
        assert "display_key" in (exc.field_path or "")
        assert isinstance(exc, SpecKittyTrackerError)
