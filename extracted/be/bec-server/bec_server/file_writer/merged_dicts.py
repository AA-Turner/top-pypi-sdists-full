import collections
from functools import reduce


def get_merged_flat_dicts(input_dicts: list[dict]):
    """merge dicts into a single flat dict"""
    res = collections.defaultdict(list)
    for input_dict in input_dicts:
        for key, value in flatten_dict(input_dict).items():
            res[key].append(value)
    return dict(res)


def flatten_dict(target: dict, base: str = ""):
    """convert a nested dict into a flat dict"""
    res = {}
    for key, value in target.items():
        if isinstance(value, dict):
            res.update(flatten_dict(value, base=base + "/" + key))
        else:
            res[base + "/" + key] = value
    return res


def nested_update(target: dict, update: dict):
    """
    update a nested dictionary
    similar to dict.update() but without overwriting nested structures
    """
    for key, value in update.items():
        if isinstance(value, collections.abc.Mapping):
            target[key] = nested_update(target.get(key, {}), value)
            continue
        target[key] = value
    return target


def merge_dicts(input_dicts: list[dict]) -> dict:
    """Merge dicts of the same structure into a single dict with values as list

    Args:
        input_dicts (list[dict]): List of input dicts

    Returns:
        dict: Merged dict
    """

    merged_dict = {}
    for key, val in get_merged_flat_dicts(input_dicts).items():
        keys = key.split("/")[1:]
        nested_update(merged_dict, reduce(lambda k, v: {v: k}, reversed(keys), val))
    return merged_dict
