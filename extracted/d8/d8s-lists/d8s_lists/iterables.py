import itertools
from collections import Counter
from typing import Any, Dict, Iterable, Iterator, List, Optional, Sequence, Sized, Type

from d8s_dicts import dict_sort_by_values, dict_values

# TODO: consider applying @decorators.listify_first_arg argument to all/most functions in this module


def iterable_sort_by_length(iterable: Iterable[Any], **kwargs) -> List[Any]:
    """."""
    sorted_list = sorted(iterable, key=lambda x: len(x), **kwargs)  # pylint: disable=W0108
    return sorted_list


def longest(iterable: Iterable[Any]) -> Any:
    """."""
    longest_item = max(iterable, key=len)
    return longest_item


def shortest(iterable: Iterable[Any]) -> Any:
    """."""
    shortest_item = min(iterable, key=len)
    return shortest_item


def flatten(iterable: Iterable[Any], level: int = None, **kwargs) -> Iterator[Any]:
    """Flatten all items in the iterable so that they are all items in the same list."""
    import more_itertools

    return more_itertools.collapse(iterable, levels=level, **kwargs)


def has_index(iterable: Sized, index: int) -> bool:
    """."""
    # TODO: would it be faster to simply try to get the item at index and handle exceptions?
    index_int = int(index)

    return 0 <= index_int <= len(iterable) - 1


def types(iterable: Iterable[Any]) -> Iterator[Type]:
    """Return a set containing the types of all items in the list_arg."""
    return map(type, iterable)


def iterable_item_of_types(iterable: Iterable[Any], item_types: Iterable[type]) -> bool:
    """Return True if the iterable has any item that is of the item_types. Otherwise, return False."""
    for i in iterable:
        if type(i) in item_types:
            return True
    return False


def iterable_all_items_of_types(iterable: Iterable[Any], item_types: Iterable[type]) -> bool:
    """Return True if all items in the iterable are of a type given in item_types. Otherwise, return False."""
    for i in iterable:
        if type(i) not in item_types:
            return False
    return True


def iterable_has_all_items_of_type(iterable: Iterable[Any], type_arg: type) -> bool:
    """Return whether or not all iterable in iterable are of the type specified by the type_arg."""
    for i in iterable:
        if type(i) != type_arg:
            return False
    return True


def deduplicate(iterable: Iterable[Any]) -> Iterator[Any]:
    """Deduplicate the iterable."""
    og_iterable, temp_iterable = itertools.tee(iterable)

    if iterable_item_of_types(temp_iterable, (dict, list)):
        deduplicated_list = []
        for i in og_iterable:
            if i not in deduplicated_list:
                deduplicated_list.append(i)
                yield i
    else:
        yield from list(set(og_iterable))


def cycle(iterable: Iterable[Any], length: Optional[int] = None) -> Iterator[Any]:
    """Cycle through the iterable as much as needed."""
    full_cycle = itertools.cycle(iterable)

    if length:
        for index, item in enumerate(full_cycle):
            yield item
            if index == length - 1:
                break
    else:
        return full_cycle


def truthy_items(iterable: Iterable[Any]) -> Iterator[Any]:
    """Return an iterable with only elements of the given iterable which evaluate to True.

    (see https://docs.python.org/3.9/library/stdtypes.html#truth-value-testing)
    """
    return filter(lambda x: x, iterable)


def nontruthy_items(iterable: Iterable[Any]) -> Iterator[Any]:
    """Return an iterable with only elements of the given iterable which evaluate to False.

    (see https://docs.python.org/3.9/library/stdtypes.html#truth-value-testing)
    """
    return filter(lambda x: not x, iterable)


def iterable_has_single_item(iterable: Iterable[Any]) -> bool:
    """Return whether the iterable has a single item in it."""
    iterable = deduplicate(iterable)
    result = len(tuple(iterable)) == 1
    return result


def iterables_are_same_length(a: Sized, b: Sized, *args: Sized, debug_failure: bool = False) -> bool:
    """Return whether or not the given iterables are the same lengths."""
    consolidated_list = [a, b, *args]
    lengths_1, lengths_2 = itertools.tee(map(len, consolidated_list))

    result = iterable_has_single_item(lengths_1)

    if debug_failure and not result:
        list_length_breakdown = iterable_count(lengths_2)
        minority_list_count = min(dict_values(list_length_breakdown))
        for index, arg in enumerate(consolidated_list):
            if list_length_breakdown[len(arg)] == minority_list_count:
                print(f'Argument {index} is not the same length as the majority of the arguments')

    return result


def iterables_have_same_items(a: Sequence, b: Sequence, *args: Sequence) -> bool:  # noqa: CCR001
    """Return whether iterables have identical items (considering both identity and count)."""
    first_list = a
    remaining_lists = [b, *args]

    if iterables_are_same_length(a, *remaining_lists):
        for item in first_list:
            first_list_count = first_list.count(item)
            item_counts = [list_.count(item) for list_ in remaining_lists]
            same_count = item_counts[0] == first_list_count
            if not iterable_has_single_item(item_counts) or not same_count:
                return False
    else:
        return False
    return True


def run_length_encoding(iterable: Iterable[Any]) -> Iterator[str]:
    """Perform run-length encoding on the given array.

    See https://en.wikipedia.org/wiki/Run-length_encoding for more details.
    """
    run_length_encodings = (f'{len(tuple(g))}{k}' for k, g in itertools.groupby(iterable))
    return run_length_encodings


def iterable_count(iterable: Iterable[Any]) -> Dict[Any, int]:
    """Count each item in the iterable."""
    counter: Counter = Counter()
    counter.update(iterable)
    count = dict_sort_by_values(counter)
    return count


def iterable_item_index(iterable: Sequence, item: Any) -> int:
    """Find the given item in the iterable. Return -1 if the item is not found."""
    try:
        return iterable.index(item)
    except ValueError:
        return -1


def iterable_item_indexes(iterable: Iterable[Any], item: Any) -> Iterator[int]:
    """Find the given item in the iterable. Return -1 if the item is not found."""
    indexes = (index for index, value in enumerate(iterable) if value == item)
    return indexes


def duplicates(iterable: Sequence) -> Iterator[Sequence]:
    """Find duplicates in the given iterable."""
    for item in iterable:
        if iterable.count(item) > 1:
            yield item


def iterable_has_mixed_types(iterable: Iterable[Any]) -> bool:
    """Return whether or not the iterable has items with two or more types."""
    return len(tuple(deduplicate(types(iterable)))) >= 2


def iterable_has_single_type(iterable: Iterable[Any]) -> bool:
    """Return whether or not the iterable has items of only one type."""
    return len(tuple(deduplicate(types(iterable)))) == 1


def iterable_replace(iterable: Iterable[Any], old_value: Any, new_value: Any) -> Iterator[Any]:
    """Replace all instances of the old_value with the new_value in the given iterable."""
    for value in iterable:
        if value == old_value:
            yield new_value
        else:
            yield value


# def list_entropy(list_arg):
#     """Find the entropy of the items in the given list."""
#     import math
#     from nlp import frequencyDistribution

#     freqdist = frequencyDistribution(iterable)
#     probs = [freqdist.freq(l) for l in freqdist]
#     return -sum(p * math.log(p, 2) for p in probs)
