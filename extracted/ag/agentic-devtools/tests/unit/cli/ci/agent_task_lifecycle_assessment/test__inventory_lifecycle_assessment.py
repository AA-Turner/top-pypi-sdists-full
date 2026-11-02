from agentic_devtools.cli.ci.agent_task_lifecycle_assessment import _inventory_lifecycle_assessment
from agentic_devtools.cli.ci.models import AgentTaskInventory


def test_preserves_partial_inventory_diagnostics() -> None:
    inventory = AgentTaskInventory((), complete=False, incomplete_reasons=("page-limit",))
    result = _inventory_lifecycle_assessment(None, False, None, "incomplete-inventory", inventory=inventory)
    assert result.inventory_availability == inventory.availability
