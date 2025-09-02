import collections
from typing import Any, Callable, Dict, List, Union

from .dicts_temp_utils import copy_first_arg_dict, list_item_types

DictKeyType = Union[str, int, float, complex, tuple, range, frozenset, bytes, memoryview]

python_types_not_allowed_as_dict_keys = (dict, list, set)


def dict_filter_by_values(dictionary: dict, filter_function: Callable) -> dict:
    """."""
    return {k: v for k, v in dictionary.items() if filter_function(v)}


def dict_filter_by_keys(dictionary: dict, filter_function: Callable) -> dict:
    """."""
    return {k: v for k, v in dictionary.items() if filter_function(k)}


def is_dict(possible_dict: Any) -> bool:
    """Return whether or not the possible_dict is a dictionary."""
    # TODO: June 2020: I removed the decorators.map_first_arg decorator b/c a list/tuple/set/mappable type could be one of the inputs to this function and I think it is unintuitive to map over a given list rather than returning False b/c the list is not a dict - feel free to reassess
    return isinstance(possible_dict, dict)


# TODO: improve the return type on the function below (it should be any type that can be a dictionary key)
def dict_keys(dictionary: dict) -> List[Any]:
    """Get the dictionary's keys (as a list)."""
    return list(dictionary.keys())


def is_valid_dict_key(key: Any) -> bool:
    """Return whether or not a dictionary could have the given key."""
    type_is_invalid_key = type(key) in python_types_not_allowed_as_dict_keys
    return not type_is_invalid_key


# TODO: improve the return type on the function below (it should be any type that can be a dictionary value - which may be Any, so the current return type may be correct.. but double check)
def dict_values(dictionary: dict) -> List[Any]:
    """Get the dictionary's values (as a list)."""
    return list(dictionary.values())


# TODO: add a type definition for the `value` parameter
def dict_has_value(dictionary: dict, value) -> bool:
    """Return whether or not the dictionary has the given value (without evaluating the value)."""
    return value in dict_values(dictionary)


# TODO: improve the return type on the function below
def dict_key_types(dictionary: dict) -> list:
    """Return a list with the type of each key in the dictionary."""
    keys = dict_keys(dictionary)
    return list_item_types(keys)


# TODO: improve the return type on the function below
def dict_value_types(dictionary: dict) -> dict:
    """Return a dictionary with the same keys and the type of each value in place of the actual value."""
    types = {}
    for k, v in dictionary.items():
        types[k] = type(v)
    return types


# TODO: add a type definition for the `value` parameter
# TODO: add a return type on the function below (it should be any type that can be a dictionary key)
def dict_keys_with_value(dictionary: dict, value):
    """Find the key(s) in the dictionary which have the given value."""
    keys_with_value = []
    for k, v in dictionary.items():
        if v == value:
            keys_with_value.append(k)
    return keys_with_value


def dict_sort_by_keys(dictionary: dict, **kwargs) -> collections.OrderedDict:
    """Sort the dictionary based on the dictionary's keys."""
    sorted_dict = collections.OrderedDict()
    sorted_keys = sorted(dict_keys(dictionary), **kwargs)

    for key in sorted_keys:
        sorted_dict[key] = dictionary[key]

    return sorted_dict


def dict_sort_by_values(dictionary: dict, **kwargs) -> collections.OrderedDict:
    """Sort the dictionary based on the dictionary's values."""
    dict_items = dictionary.items()

    sorted_list_of_tuples = sorted(dict_items, key=lambda kv: kv[1], **kwargs)
    sorted_dict = collections.OrderedDict({i[0]: i[1] for i in sorted_list_of_tuples})
    return sorted_dict


# TODO: add a type definition for the `key` parameter
# TODO: convert the key argument to a path
def dicts_sort_by_value_at_key(dictionaries: List[Dict[Any, Any]], key, **kwargs) -> List[Dict[Any, Any]]:
    """Sort the given dictionaries (we are assuming that we get a list of dictionaries) based on each dictionary's value at the given key."""
    import more_itertools

    # NOTE: a corollary to this function would be a dicts_sorted_by_key_with_value function... it's not implemented, but can be if needed
    temp_dict = collections.OrderedDict()
    for dictionary in dictionaries:
        # the line below will fail if the key is not present in one of the dictionaries; this is intentional
        value_at_key = dictionary[key]
        # create a dictionary with the value_at_key as the key and the entire dictionary as the value
        temp_dict = dict_add(temp_dict, value_at_key, dictionary)
    sorted_temp_dict = dict_sort_by_keys(temp_dict, **kwargs)

    sorted_dicts = more_itertools.collapse(dict_values(sorted_temp_dict), base_type=dict)
    return sorted_dicts


def dict_flip(dictionary: dict, *, flatten_values: bool = False, flip_lists_and_sets: bool = False) -> dict:
    """Flip the dictionary's keys and values; all of the values become keys and keys become values."""
    import copy

    new_dict = {}

    for key, value in dictionary.items():
        if not is_valid_dict_key(value):
            if flip_lists_and_sets and isinstance(value, (list, set)):
                temp_dict = copy.deepcopy(new_dict)
                for i in value:
                    try:
                        temp_dict = dict_add(temp_dict, i, key)
                    except TypeError as e:
                        message = f'Unable to flip <<{value}>> because it contains items of a type which cannot be the keys for dictionaries.'
                        raise TypeError(message)
                else:
                    new_dict.update(temp_dict)
        else:
            new_dict = dict_add(new_dict, value, key)

    if flatten_values:
        new_dict = dict_delistify_values(new_dict)

    return new_dict


@copy_first_arg_dict
def dict_delistify_values(dictionary: dict) -> dict:
    """For all values in the given dictionary that are lists whose lengths are one, replace the list of length one with the value in the list."""
    # TODO: it would be nice to be able to do this iteratively throughout a dict... currently it only goes through the first level of values - adding a recursive option would be nice... would this principle apply to other functions in this library?
    for k, v in dictionary.items():
        if isinstance(v, list) and len(v) == 1:
            dictionary[k] = v[0]
    return dictionary


def dict_examples(n: int = 10, **kwargs) -> List[Dict[Any, Any]]:
    """Create n dictionary examples."""
    from hypothesis import strategies as st

    key_strategies = [st.integers(), st.none(), st.text(), st.floats()]
    keys = st.one_of(*key_strategies)

    list_strategy = st.lists(st.one_of(*key_strategies), max_size=2)
    values = st.one_of(*key_strategies, list_strategy)

    from d8s_hypothesis import hypothesis_get_strategy_results

    results = hypothesis_get_strategy_results(st.dictionaries, keys, values, n=n, **kwargs)
    return results


# TODO: update the type definition for the `key` parameter
# TODO: update the type definition for the `value` parameter
@copy_first_arg_dict
def dict_add(dictionary: Dict[Any, List[Any]], key: Any, value: Any) -> Dict[Any, List[Any]]:
    """Add the given value to the dictionary at the given key. This function expects that all values of the dictionary parameter are lists."""
    if key in dictionary:
        if not isinstance(dictionary[key], list):
            message = f'The value at the "{key}" key in the dictionary is not a list and the dict_add function requires all values to be a list.'
            raise TypeError(message)
        dictionary[key].append(value)
    else:
        dictionary[key] = [value]
    return dictionary


# TODO: update the type annotation for the return type
def dicts_diffs(dictionary_a: dict, dictionary_b: dict) -> list:
    """."""
    import dictdiffer

    result = dictdiffer.diff(dictionary_a, dictionary_b)
    return result


# TODO: update the type definition for the `key` and `new_key` parameters
@copy_first_arg_dict
def dict_copy_value_at_key(dictionary: dict, key: Any, new_key: Any) -> dict:
    """Copy the value at the given key into the new key."""
    dictionary.update({new_key: dictionary.get(key)})
    return dictionary


# TODO: update the type definition for the `key` and `new_key` parameters
@copy_first_arg_dict
def dict_move_value_at_key(dictionary: dict, old_key: Any, new_key: Any) -> dict:
    """Move the given key and its values into the new key."""
    dictionary = dict_copy_value_at_key(dictionary, old_key, new_key)
    dictionary = dict_key_delete(dictionary, old_key)
    return dictionary


# TODO: update the type definition for the `key` parameter
@copy_first_arg_dict
def dict_key_delete(dictionary: dict, key: Any) -> dict:
    """Delete the given key from the given dictionary."""
    if key in dictionary:
        del dictionary[key]
    return dictionary


def dict_delete_items(dictionary: dict, values_to_delete: List[Any] = None, keys_to_delete: List[Any] = None) -> dict:
    """Delete all items from the dictionary if the item's value is in values_to_delete or the item's key is in keys_to_delete."""
    # TODO: write a decorator to do this
    if values_to_delete is None:
        values_to_delete = []
    if keys_to_delete is None:
        keys_to_delete = []

    new_dict = {k: v for k, v in dictionary.items() if v not in values_to_delete and k not in keys_to_delete}
    return new_dict


def dict_delete_empty_values(dictionary: dict) -> dict:
    """Delete all key-values pairs from the dictionary if the value is an empty strings, empty list, zero, False or None."""
    empty_values = ('', [], 0, False, None)
    return dict_delete_items(dictionary, values_to_delete=empty_values)


# TODO: write function to find the number of items in the values (counting each item in the list)


def dict_keys_with_max_value(dictionary: dict) -> List[DictKeyType]:
    """."""
    max_value = max(dict_values(dictionary))
    keys = [key for key in dict_keys(dictionary) if dictionary[key] == max_value]
    return keys


def dict_keys_with_min_value(dictionary: dict) -> List[DictKeyType]:
    """."""
    max_value = max(dict_values(dictionary))
    keys = [key for key in dict_keys(dictionary) if dictionary[key] == max_value]
    return keys


def dict_value_with_max_key(dictionary: dict) -> Any:
    """."""
    max_key = max(dict_keys(dictionary))
    return dictionary[max_key]


def dict_value_with_min_key(dictionary: dict) -> Any:
    """."""
    min_key = min(dict_keys(dictionary))
    return dictionary[min_key]
