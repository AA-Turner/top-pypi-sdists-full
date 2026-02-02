from collections.abc import Callable
from queue import Queue
from typing import get_type_hints

from theutilitybelt.functional.predicate import always_true


def get_type_args_for_function(fn: Callable) -> dict[str, type]:
    """
    Get the type arguments for a given function.

    Args:
        fn (Callable): The function for which to retrieve the type arguments.

    Returns:
        dict[str, type]: A dictionary mapping the argument names to their corresponding types.
    """
    return {k: v for k, v in get_type_hints(fn).items() if k != "return"}


def get_subclasses(cls: type, *, filter: Callable[[type], bool] = always_true):
    """
    Retrieves all subclasses of a given class.

    Args:
        cls (type): The class to retrieve subclasses from.
        filter (Callable[[type], bool], optional): A filter function to apply to each subclass. Defaults to always_true.

    Returns:
        list: A list of subclasses that pass the filter.

    """
    queue = Queue()
    queue.put(cls)
    items = []
    while not queue.empty():
        t = queue.get_nowait()

        for sub in t.__subclasses__():
            queue.put(sub)

            if filter(sub):
                items.append(sub)

    return items
