"""Tests for the scheduler provider capability."""

import pytest

from tests.unit.cli.ci.provider._fixtures import _ConcreteProvider


class TestProviderSchedulerMixin:
    """Tests for the scheduler provider capability."""

    def test_list_workflow_runs_default_raises_not_implemented(self) -> None:
        """Default list_workflow_runs raises NotImplementedError."""
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement list_workflow_runs"):
            provider.list_workflow_runs(workflow_id="ci.yml")

    def test_rerun_workflow_default_raises_not_implemented(self) -> None:
        """Default rerun_workflow raises NotImplementedError."""
        provider = _ConcreteProvider()
        with pytest.raises(NotImplementedError, match="does not implement rerun_workflow"):
            provider.rerun_workflow(run_id=12345)
