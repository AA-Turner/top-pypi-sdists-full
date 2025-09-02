from typing import Any
from typing import Dict


def merge_arguments(hub, desire_state: Dict[str, Any], current_state: Dict[str, Any]):
    """
    Assign current_state parameter value to desire_state parameter if desire_state parameter value is None
    or parameter key is missing in desire_state.
    """
    if isinstance(current_state, dict):
        for key, value in current_state.items():
            if key in desire_state:
                desire_value = desire_state.get(key)
                if desire_value is None:
                    desire_state[key] = value
                elif isinstance(desire_value, dict):
                    desire_state[key] = hub.tool.aws.state_utils.merge_arguments(
                        desire_value, value
                    )
            else:
                desire_state[key] = value

    return desire_state
