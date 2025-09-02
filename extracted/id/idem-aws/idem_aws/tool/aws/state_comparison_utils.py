import inspect
import json
from typing import Any
from typing import Dict
from typing import List

from dict_tools import data


def are_lists_identical(hub, list1: List, list2: List) -> bool:
    """
    Compare two lists and logs the difference.
    :param list1: first list.
    :param list2: second list.
    :return: true if there is no difference between both lists.
    :raises exception if one of the list  is not of type list
    """
    if (list1 is None or len(list1) == 0) and (list2 is None or len(list2) == 0):
        return True
    if list1 is None or len(list1) == 0 or list2 is None or len(list2) == 0:
        return False

    for l in [list1, list2]:
        if not isinstance(l, List):
            raise TypeError(
                f"Expecting lists to compare. This is expected to be of type List: '{l}'"
            )

    diff = [i for i in list1 + list2 if i not in list1 or i not in list2]
    result = len(diff) == 0
    if not result:
        hub.log.debug(f"There are {len(diff)} differences:\n{diff[:5]}")
    return result


def standardise_json(hub, value: str or Dict, sort_keys: bool = True) -> str:
    # Format json string or dictionary
    if value is None or not value or value is inspect._empty:
        return None

    if isinstance(value, str) and len(value) > 0:
        json_dict = json.loads(value)
    elif isinstance(value, Dict):
        json_dict = value
    else:
        raise TypeError(
            f"Expecting string or dictionary. This value has the wrong type: '{value}'"
        )

    return json.dumps(
        _sorting(json_dict) if sort_keys else json_dict,
        separators=(", ", ": "),
        sort_keys=sort_keys,
    )


def _sorting(obj):
    if isinstance(obj, dict):
        return {k: _sorting(v) for k, v in sorted(obj.items())}
    if isinstance(obj, list):
        if all(isinstance(v, str) for v in obj):
            return sorted(obj)
        else:
            return [_sorting(v) for i, v in sorted(enumerate(obj))]
    return obj


def compare_dicts(
    hub, source_dict: Dict[str, Any], target_dict: Dict[str, Any]
) -> bool:
    """Compares two dictionaries.

    Args:
        source_dict(Dict):
            The source dictionary

        target_dict(Dict):
            The target dictionary

    Returns:
        True if the dictionaries are equal, False otherwise
    """

    if source_dict is None and target_dict is None:
        return True

    if source_dict is None or target_dict is None:
        return False

    if len(source_dict) != len(target_dict):
        return False

    for key, value in source_dict.items():
        if key in target_dict:
            if isinstance(source_dict[key], dict) and isinstance(
                target_dict[key], dict
            ):
                if not compare_dicts(hub, source_dict[key], target_dict[key]):
                    return False
            elif isinstance(source_dict[key], list) and isinstance(
                target_dict[key], list
            ):
                if not are_lists_identical(hub, source_dict[key], target_dict[key]):
                    return False
            elif value != target_dict[key]:
                return False
        else:
            return False
    return True


def are_policies_equal(
    hub, expected_policy: str or Dict[str, Any], actual_policy: str or Dict[str, Any]
) -> bool:
    """Compares two AWS policies.

    Args:
        expected_policy(str or Dict):
            The expected policy

        actual_policy(str or Dict):
            The actual policy

    Returns:
        True if the policies are equal, False otherwise
    """
    expected_policy = json.loads(standardise_json(hub, expected_policy))
    actual_policy = json.loads(standardise_json(hub, actual_policy))
    return not data.recursive_diff(actual_policy, expected_policy, ignore_order=True)
