import typing

from .curried_doubling_search import curried_doubling_search


def doubling_search(
    predicate: typing.Callable[[int], bool],
    lower_bound: int = 0,
    satisfaction_bound: typing.Optional[int] = None,
) -> int:
    """Find the positive integer threshold below which a search criteria is
    never satisfied and above which it is always satisfied.

    Parameters
    ----------
    predicate : callable object
        Returns whether an integer value satisfies the search criteria.
    lower_bound : int, optional
        The initial guess. Should be less than or equal to the first value that
        satsfies the search criteria. Used for recursion. Default is 0.
    satisfaction_bound : int, default None
        Any integer values at or past this value are considered to satisfy the
        search criteria without calling predicate.

    Returns
    -------
    threshold
        The lowest integer value that satisfies the search criteria.
    """
    if satisfaction_bound is not None:
        predicate_ = lambda x: (x >= satisfaction_bound) or predicate(x)
    else:
        predicate_ = predicate
    return curried_doubling_search(predicate_)(lower_bound)
