import collections.abc
from typing import Any, Dict, List, Mapping


def make_cf_tags(tags: Dict[str, str]) -> List[Dict[str, str]]:
    """
    Converts a dictionary of tags into a list of AWS CloudFormation tag dictionaries.

    Args:
        tags (Dict[str, str]): A dictionary where keys are tag names and values are tag values.

    Returns:
        List[Dict[str, str]]: A list of dictionaries, each with 'Key' and 'Value' fields suitable for CloudFormation resources.
    """
    _tags = []
    for key, value in tags.items():
        _tags.append({"Key": key, "Value": value})
    return _tags


def nested_update(d: Dict[Any, Any], u: Mapping[Any, Any]):
    """
    Recursively updates a dictionary with values from another mapping.

    If a value in the update mapping (`u`) is itself a mapping, the update is performed recursively
    on the corresponding sub-dictionary in `d`. Otherwise, the value is set directly.

    Args:
        d (Dict[Any, Any]): The dictionary to be updated.
        u (Mapping[Any, Any]): The mapping containing updates.

    Returns:
        Dict[Any, Any]: The updated dictionary.
    """
    for key, value in u.items():
        if isinstance(value, collections.abc.Mapping):
            d[key] = nested_update(d.get(key, {}), value)
        else:
            d[key] = value
    return d
