from typing import Any
from typing import Dict


def convert_raw_event_destination_to_present(
    hub, configuration_set_name: str, name: str, raw_resource: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Util functions to convert raw resource state to present input format for event destination.
    """
    ret = {
        "name": name,
        "configuration_set_name": configuration_set_name,
        "resource_id": name,
    }
    if "Name" in raw_resource:
        raw_resource.pop("Name")
    ret["event_destination"] = raw_resource.copy()
    return ret
