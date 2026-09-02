"""Tests for CIPlatformProvider.list_eligible_prs default implementation."""

import pytest


class TestListEligiblePrsDefault:
    """Tests that the default list_eligible_prs raises NotImplementedError."""

    def test_raises_not_implemented(self) -> None:
        # Create a minimal concrete subclass that only implements abstract methods
        from tests.unit.cli.ci.provider.test_ciplatformprovider import _ConcreteProvider

        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_eligible_prs"):
            provider.list_eligible_prs()
