"""Tests for CIPlatformProvider.list_eligible_prs default implementation."""

import pytest

from agentic_devtools.cli.ci.scheduler import EligiblePR


class TestListEligiblePrsDefault:
    """Tests that the default list_eligible_prs raises NotImplementedError."""

    def test_raises_not_implemented(self) -> None:
        # Create a minimal concrete subclass that only implements abstract methods
        from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider

        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_eligible_prs"):
            provider.list_eligible_prs()

    def test_retry_liveness_defaults_to_false(self) -> None:
        from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider

        class EligibleProvider(_ConcreteProvider):
            def list_eligible_prs(self, max_prs: int | None = None) -> list[EligiblePR]:
                return []

        assert EligibleProvider().list_eligible_prs_with_retry_liveness() == ([], False)
