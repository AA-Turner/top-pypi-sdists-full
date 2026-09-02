"""Tests for CIPlatformProvider.list_supervisor_prs default implementation."""

import pytest


class TestListSupervisorPrsDefault:
    """Tests that the default list_supervisor_prs raises NotImplementedError."""

    def test_raises_not_implemented(self) -> None:
        from tests.unit.cli.ci.provider.test_ciplatformprovider import _ConcreteProvider

        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_supervisor_prs"):
            provider.list_supervisor_prs()
