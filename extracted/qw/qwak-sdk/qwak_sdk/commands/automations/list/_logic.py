from qwak.clients.automation_management.client import AutomationsManagementClient
from tabulate import tabulate

from qwak_sdk.commands._logic.tools import list_of_messages_to_json_str

COLUMNS = ["Id", "Name", "Model id", "Type", "Status", "Last updated", "Updated by"]


def execute_list_automations():
    client = AutomationsManagementClient()
    automations_list = client.list_automations()
    data = []
    for automation in automations_list:
        data.append(
            [
                automation.id,
                automation.name,
                automation.model_id,
                automation.action.__class__.__name__,
                _map_automation_status(automation.is_enabled),
                automation.create_audit.date,
                automation.create_audit.user_id,
            ]
        )

    return tabulate(data, headers=COLUMNS)


def execute_list_json_automations() -> str:
    client = AutomationsManagementClient()
    automations = client.get_list_automations_from_server()
    return list_of_messages_to_json_str(automations)


def _map_automation_status(status: bool) -> str:
    return "Active" if status else "Inactive"
