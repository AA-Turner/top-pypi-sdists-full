"""Tests for CIPlatformProvider.list_open_copilot_pr_briefs default implementation."""

import pytest


class TestListOpenCopilotPrBriefsDefault:
    """The default list_open_copilot_pr_briefs raises NotImplementedError."""

    def test_raises_not_implemented(self) -> None:
        from tests.unit.cli.ci.provider.test_ciplatformprovider import _ConcreteProvider

        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_open_copilot_pr_briefs"):
            provider.list_open_copilot_pr_briefs()
