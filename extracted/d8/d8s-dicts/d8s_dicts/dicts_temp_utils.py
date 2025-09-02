import functools
from typing import List


def copy_first_arg_dict(func):
    """If the first arg is a dictionary, pass a copy of the dictionary into func."""
    import copy

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        first_arg_dict = args[0]
        other_args = args[1:]

        if isinstance(first_arg_dict, dict):
            first_arg_dict_copy = copy.deepcopy(first_arg_dict)
            return func(first_arg_dict_copy, *other_args, **kwargs)
        else:
            return func(*args, **kwargs)

    return wrapper


def list_item_types(list_arg: list) -> List[str]:
    """Return a set containing the types of all items in the list_arg."""
    # TODO: I don't like the fact that this function returns types as a string (see also the dict_key_types function)
    types = [type(item) for item in list_arg]
    return types
