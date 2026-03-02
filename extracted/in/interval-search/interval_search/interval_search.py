import typing

from .binary_search_iterative import binary_search_iterative
from .doubling_search import doubling_search


def interval_search(
    predicate: typing.Callable[[int], bool],
    lower_bound: int=0,
    upper_bound: typing.Optional[int]=None,
) -> typing.Optional[int]:
    """Find the positive integer threshold below which a search criteria is
    never satisfied and above which it is always satisfied.

    Uses either binary search or doubling search, depending on whether upper
    bound is specified.

    Parameters
    ----------
    predicate : callable object
        Returns whether an integer value satisfies the search criteria.
    lower_bound : int
        Lower bound for the binary search, inclusive.
    upper_bound : int
        Upper bound for the binary search, inclusive.

    Returns
    -------
    guess
        The lowest integer value that satisfies the search criteria, and None
        if upper_bound does not satisfy the search criteria or search range is
        empty (i.e., lower_bound > upper_bound).
    """

    return doubling_search(
        predicate,
        lower_bound,
    ) if upper_bound is None else binary_search_iterative(
        predicate,
        lower_bound,
        upper_bound,
    )
