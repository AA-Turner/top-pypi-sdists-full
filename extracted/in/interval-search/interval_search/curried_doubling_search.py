import typing

from .binary_search_iterative import binary_search_iterative


def curried_doubling_search(
    predicate: typing.Callable[[int], bool],
    decorate_with: typing.Callable[
        [typing.Callable], typing.Callable
    ] = lambda x: x,
) -> typing.Callable[[typing.Optional[int]], int]:
    """Find the positive integer threshold below which a search criteria is
    never satisfied and above which it is always satisfied.

    Currying allows for recursive calls that don't pass the predicate callable
    as an argument, which is necessary for compatibility with Numba jit
    compilation.

    Parameters
    ----------
    predicate : callable object
        Returns whether an integer value satisfies the search criteria.
    decorate_with : callable, optional
        A decorator that will be applied to the inner search function. Useful
        to enable jit compilation.

    Returns
    -------
    searcher : Callable[[Optional[int]], int]
        The curried search function, which takes an optional integer
        `lower_bound` and returns an integer value that satisfies the search
        criteria. If no lower bound is provided, the default is taken as 0.
    """

    @decorate_with
    def doubling_search(lower_bound: int = 0) -> int:
        """Find the positive integer threshold below which a search criteria is
        never satisfied and above which it is always satisfied.

        Parameters
        ----------
        lower_bound : int, optional
            The initial guess. Should be less than or equal to the first value that
            satsfies the search criteria. Used for recursion. Default is 0.

        Returns
        -------
        threshold : int
            The lowest integer value that satisfies the search criteria.
        """

        assert lower_bound >= 0, lower_bound

        bound = 1
        while not predicate(lower_bound + bound):
            bound <<= 1  # equiv *= 2

        prev_bound = bound >> 1  # equiv // 2
        prev_guess = lower_bound + prev_bound
        return binary_search_iterative(
            predicate, prev_guess, lower_bound + bound
        )

    return doubling_search
