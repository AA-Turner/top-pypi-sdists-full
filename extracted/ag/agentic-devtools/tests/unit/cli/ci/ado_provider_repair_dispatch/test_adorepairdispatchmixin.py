"""Tests for the Azure DevOps repair dispatch mixin."""

import pytest

from agentic_devtools.cli.ci.ado_provider import AzureDevOpsProvider
from agentic_devtools.cli.ci.ado_provider_repair_dispatch import _AdoRepairDispatchMixin
from agentic_devtools.cli.ci.provider import CIPlatformProvider


def test_dispatch_repair_uses_mixin_and_accepts_optional_prompt() -> None:
    """The provider resolves the ADO mixin before the abstract contract."""
    mro = AzureDevOpsProvider.mro()
    assert mro.index(_AdoRepairDispatchMixin) < mro.index(CIPlatformProvider)
    assert AzureDevOpsProvider.dispatch_repair.__qualname__ == "_AdoRepairDispatchMixin.dispatch_repair"

    provider = AzureDevOpsProvider()
    with pytest.raises(
        NotImplementedError,
        match="AzureDevOpsProvider.dispatch_repair\\(\\) not yet implemented",
    ):
        provider.dispatch_repair(
            pr_number=1,
            head_sha="sha",
            repair_type="review",
            failed_checks=[],
            review_comments=[],
            agent_task_prompt="Repair the finding.",
        )
