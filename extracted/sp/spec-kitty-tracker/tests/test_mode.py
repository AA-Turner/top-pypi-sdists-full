"""Tests for the hosted-vs-local mode taxonomy (mission tracker-readiness-alignment-01KS7PZ7).

WS5 of Priivacy-ai/spec-kitty#1091, tracking spec-kitty-tracker#18.
"""

from __future__ import annotations

import pytest

from spec_kitty_tracker import (
    ALL_KNOWN_PROVIDERS,
    HOSTED_PROVIDERS,
    LOCAL_PROVIDERS,
    HostedAuthRequiredError,
    TrackerMode,
    is_hosted_provider,
    is_local_provider,
    provider_mode,
)
from spec_kitty_tracker.errors import (
    ConnectorRequestError,
    FailureClass,
    SpecKittyTrackerError,
)

# ---------------------------------------------------------------------------
# TrackerMode enum
# ---------------------------------------------------------------------------


def test_tracker_mode_has_exactly_two_members() -> None:
    """Adding a third TrackerMode value is a spec-level change.

    Every consumer with an exhaustive ``match`` statement would silently
    fall through to the default branch.  This test exists to make any
    future addition impossible-to-miss in CI.
    """
    assert {m.value for m in TrackerMode} == {"hosted", "local"}


def test_tracker_mode_is_str_enum() -> None:
    """TrackerMode is a StrEnum so comparisons against plain strings work."""
    assert TrackerMode.HOSTED == "hosted"
    assert TrackerMode.LOCAL == "local"


# ---------------------------------------------------------------------------
# Provider taxonomy frozensets
# ---------------------------------------------------------------------------


def test_hosted_and_local_sets_are_disjoint() -> None:
    """No provider may belong to both modes."""
    assert HOSTED_PROVIDERS.isdisjoint(LOCAL_PROVIDERS)


def test_all_known_providers_is_union() -> None:
    """ALL_KNOWN_PROVIDERS is the union of hosted + local."""
    assert ALL_KNOWN_PROVIDERS == HOSTED_PROVIDERS | LOCAL_PROVIDERS


def test_hosted_providers_contains_canonical_four() -> None:
    """linear / jira / github / gitlab are SaaS-hosted."""
    assert HOSTED_PROVIDERS == frozenset({"linear", "jira", "github", "gitlab"})


def test_local_providers_contains_canonical_two() -> None:
    """beads / fp are local-only."""
    assert LOCAL_PROVIDERS == frozenset({"beads", "fp"})


def test_frozensets_are_immutable() -> None:
    """The taxonomy is read-only."""
    assert isinstance(HOSTED_PROVIDERS, frozenset)
    assert isinstance(LOCAL_PROVIDERS, frozenset)
    assert isinstance(ALL_KNOWN_PROVIDERS, frozenset)


# ---------------------------------------------------------------------------
# provider_mode lookup
# ---------------------------------------------------------------------------


@pytest.mark.parametrize("provider", sorted(HOSTED_PROVIDERS))
def test_provider_mode_returns_hosted_for_hosted_slugs(provider: str) -> None:
    assert provider_mode(provider) is TrackerMode.HOSTED


@pytest.mark.parametrize("provider", sorted(LOCAL_PROVIDERS))
def test_provider_mode_returns_local_for_local_slugs(provider: str) -> None:
    assert provider_mode(provider) is TrackerMode.LOCAL


def test_provider_mode_is_case_insensitive() -> None:
    """Case-insensitive lookup matches the normalization the CLI does."""
    assert provider_mode("LINEAR") is TrackerMode.HOSTED
    assert provider_mode("Linear") is TrackerMode.HOSTED
    assert provider_mode("BEADS") is TrackerMode.LOCAL


def test_provider_mode_strips_whitespace() -> None:
    """Surrounding whitespace is stripped before classification."""
    assert provider_mode("  github  ") is TrackerMode.HOSTED


def test_provider_mode_rejects_empty_string() -> None:
    """Empty or whitespace-only slugs raise ValueError."""
    with pytest.raises(ValueError, match="empty"):
        provider_mode("")
    with pytest.raises(ValueError, match="empty"):
        provider_mode("   ")


def test_provider_mode_rejects_non_string() -> None:
    """Non-string slugs raise ValueError with a typed message."""
    with pytest.raises(ValueError, match="string"):
        provider_mode(None)  # type: ignore[arg-type]
    with pytest.raises(ValueError, match="string"):
        provider_mode(123)  # type: ignore[arg-type]


def test_provider_mode_rejects_unknown_provider() -> None:
    """Unknown providers raise ValueError listing known slugs (no silent default)."""
    with pytest.raises(ValueError) as exc:
        provider_mode("clickup")
    assert "clickup" in str(exc.value)
    assert "linear" in str(exc.value)  # known providers listed


def test_provider_mode_rejects_removed_azure_devops() -> None:
    """``azure_devops`` was removed; it must NOT silently classify as hosted."""
    with pytest.raises(ValueError):
        provider_mode("azure_devops")


# ---------------------------------------------------------------------------
# Convenience boolean helpers
# ---------------------------------------------------------------------------


def test_is_hosted_provider_matches_provider_mode() -> None:
    for slug in HOSTED_PROVIDERS:
        assert is_hosted_provider(slug) is True
    for slug in LOCAL_PROVIDERS:
        assert is_hosted_provider(slug) is False


def test_is_local_provider_matches_provider_mode() -> None:
    for slug in LOCAL_PROVIDERS:
        assert is_local_provider(slug) is True
    for slug in HOSTED_PROVIDERS:
        assert is_local_provider(slug) is False


def test_is_hosted_provider_rejects_unknown() -> None:
    """No silent ``False`` fallback for unknown providers."""
    with pytest.raises(ValueError):
        is_hosted_provider("clickup")


def test_is_local_provider_rejects_unknown() -> None:
    """No silent ``False`` fallback for unknown providers."""
    with pytest.raises(ValueError):
        is_local_provider("clickup")


# ---------------------------------------------------------------------------
# HostedAuthRequiredError
# ---------------------------------------------------------------------------


def test_hosted_auth_required_error_is_connector_request_error() -> None:
    """The CLI catches ConnectorRequestError; HostedAuthRequiredError must inherit."""
    assert issubclass(HostedAuthRequiredError, ConnectorRequestError)
    assert issubclass(HostedAuthRequiredError, SpecKittyTrackerError)


def test_hosted_auth_required_error_default_envelope() -> None:
    """The default failure_class is AUTHENTICATION; default status_code is 401."""
    exc = HostedAuthRequiredError()
    assert exc.failure_class is FailureClass.AUTHENTICATION
    assert exc.status_code == 401
    assert not exc.is_retryable
    assert "authentication" in str(exc).lower() or "auth" in str(exc).lower()


def test_hosted_auth_required_error_carries_provider() -> None:
    """Provider field is preserved on the typed envelope."""
    exc = HostedAuthRequiredError(provider="linear")
    assert exc.provider == "linear"


def test_hosted_auth_required_error_forces_authentication_failure_class() -> None:
    """``failure_class`` is always AUTHENTICATION regardless of status_code.

    A 403 from the SaaS control plane (token present but lacks team scope)
    is still an auth problem from the CLI's perspective and MUST render
    the shared ``spec-kitty auth login`` remediation.
    """
    exc = HostedAuthRequiredError("Token lacks team scope", status_code=403)
    assert exc.failure_class is FailureClass.AUTHENTICATION
    assert exc.status_code == 403


def test_hosted_auth_required_error_custom_message() -> None:
    exc = HostedAuthRequiredError("Custom message")
    assert str(exc) == "Custom message"


# ---------------------------------------------------------------------------
# Public surface availability
# ---------------------------------------------------------------------------


def test_public_surface_exports_taxonomy() -> None:
    """All taxonomy symbols are exported from the top-level package."""
    import spec_kitty_tracker as sdk

    for name in (
        "TrackerMode",
        "HOSTED_PROVIDERS",
        "LOCAL_PROVIDERS",
        "ALL_KNOWN_PROVIDERS",
        "provider_mode",
        "is_hosted_provider",
        "is_local_provider",
        "HostedAuthRequiredError",
    ):
        assert hasattr(sdk, name), f"public surface missing {name!r}"
        assert name in sdk.__all__, f"{name!r} present on module but missing from __all__"
