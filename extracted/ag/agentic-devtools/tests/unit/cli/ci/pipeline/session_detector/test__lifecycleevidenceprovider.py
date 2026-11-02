from unittest.mock import MagicMock

from agentic_devtools.cli.ci.models import AgentTaskInventory
from agentic_devtools.cli.ci.pipeline.session_detector import _LifecycleEvidenceProvider


def test_reuses_inventory_without_repeating_provider_lookup() -> None:
    provider = MagicMock()
    inventory = AgentTaskInventory(())
    cached = _LifecycleEvidenceProvider(provider, inventory)
    assert cached.list_pr_agent_task_lifecycles(7) is inventory
    assert cached.list_correlated_cloud_writer_runs is provider.list_correlated_cloud_writer_runs
    provider.list_pr_agent_task_lifecycles.assert_not_called()
