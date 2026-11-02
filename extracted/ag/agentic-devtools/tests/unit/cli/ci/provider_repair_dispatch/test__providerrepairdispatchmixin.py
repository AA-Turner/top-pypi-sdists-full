"""Tests for the repair dispatch provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderRepairDispatchMixin:
    """Tests for the repair dispatch provider capability."""

    def test_dispatch_conflict_repair_default_raises_not_implemented(self) -> None:
        """Base class dispatch_conflict_repair raises NotImplementedError."""
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement dispatch_conflict_repair"):
            provider.dispatch_conflict_repair(
                pr_number=1,
                head_sha="abc",
                base_sha="def",
                base_branch="main",
                head_branch="feat",
            )
