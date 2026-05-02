"""Alternative implementations for functions in `intervals`"""
import itertools

from sprig.intervals import _intersection, _subsets


def _intersecting_subsets_naive(intervals):
    for candidate in _subsets(intervals.items()):
        keys, combination = zip(*candidate)
        left, right = _intersection(combination)
        if left <= right:
            yield frozenset(keys), (left, right)


def intersecting_subsets_naive(intervals):
    return dict(_intersecting_subsets_naive(intervals))


def _intersecting_combinations_naive(intervals, k):
    for candidate in itertools.combinations(intervals.items(), k):
        keys, combination = zip(*candidate)
        left, right = _intersection(combination)
        if left <= right:
            yield frozenset(keys), (left, right)


def intersecting_combinations_naive(intervals, k):
    return dict(_intersecting_combinations_naive(intervals, k))


def _intersecting_products_naive(factors):
    for candidate in itertools.product(*factors):
        keys, combination = zip(*candidate)
        left, right = _intersection(combination)
        if left <= right:
            yield keys, (left, right)


def intersecting_products_naive(factors):
    return dict(_intersecting_products_naive([factor.items() for factor in factors]))


def _intersecting_products_pruning(aggregate, marginal):
    for l_key, (l_first, l_last) in aggregate.items():
        for r_key, (r_first, r_last) in marginal.items():
            first = max(l_first, r_first)
            last = min(l_last, r_last)
            if first < last:
                yield (*l_key, r_key), (first, last)


def intersecting_products_pruning(factors):
    iterator = iter(factors)
    result = {(k,): v for k, v in next(iterator).items()}
    for group in iterator:
        result = dict(_intersecting_products_pruning(result, group))
    return result
