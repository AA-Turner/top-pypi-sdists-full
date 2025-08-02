from typing import List, Tuple

from qwak.clients.alerts_registry import AlertingRegistryClient
from qwak.clients.alerts_registry.channel import Channel
from tabulate import tabulate

from qwak_sdk.commands._logic.tools import list_of_messages_to_json_str


def execute_list_channels():
    alerts_client = AlertingRegistryClient()
    channels: List[Tuple[str, Channel]] = alerts_client.list_alerting_channel()
    columns = ["id", "Name", "Type", "repr"]
    data = []
    for c_id, c in channels:
        data.append([c_id, c.name, type(c.channel_conf).__name__, c.__dict__])
    return tabulate(data, headers=columns)


def execute_json_format_list_channels():
    alerts_client = AlertingRegistryClient()
    channels = alerts_client.list_alerting_channel_from_client().description
    return list_of_messages_to_json_str(channels)
