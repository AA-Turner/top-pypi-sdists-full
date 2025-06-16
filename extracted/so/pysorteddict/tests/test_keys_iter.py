import collections
import gc
import itertools
import platform
import random
import re

import pytest

from pysorteddict import SortedDict

# The PyPy interpreter does not deallocate an object immediately after all
# references to it are dropped. Detect PyPy and force it to collect garbage to
# run any destructors, so that the results are consistent with those of
# CPython.
pypy = platform.python_implementation() == "PyPy"


@pytest.fixture
def sorted_dict(request):
    d = SortedDict()
    for i in range(request.param):
        d[i] = i
    yield d

    if pypy:
        gc.collect()
    d.clear()


@pytest.mark.parametrize("sorted_dict", [0, 1, 10, 100, 1_000, 10_000, 100_000], indirect=True)
@pytest.mark.parametrize("iterators", range(1, 10))
@pytest.mark.parametrize("advance", [0, 1, 2, 4, 8, 16, float("inf")])
def test_modify_with_active_iterators(sorted_dict, iterators, advance):
    sorted_dict_len = len(sorted_dict)
    sorted_dict_keys = sorted_dict.keys()
    sorted_dict_keys_iters = [iter(sorted_dict_keys) for _ in range(iterators)]
    advances = [random.randint(0, min(advance, sorted_dict_len)) for _ in sorted_dict_keys_iters]

    # Advance the iterators by the arbitrary amounts determined above. Record
    # the keys the iterators point to as locked keys.
    keys = [*sorted_dict_keys]
    locked_keys = collections.defaultdict(int)
    for sorted_dict_keys_iter, advance in zip(sorted_dict_keys_iters, advances, strict=True):
        [*itertools.islice(sorted_dict_keys_iter, advance)]
        if advance < sorted_dict_len:
            locked_keys[keys[advance]] += 1

    sorted_dict_copy = sorted_dict.copy()
    for locked_key, known_referrers in locked_keys.items():
        with pytest.raises(
            RuntimeError,
            match=re.escape(f"operation not permitted: key-value pair locked by {known_referrers} iterator(s)"),
        ):
            del sorted_dict[locked_key]
        del sorted_dict_copy[locked_key]
    for unlocked_key in itertools.islice({*keys} - locked_keys.keys(), 100):
        del sorted_dict[unlocked_key]
    if total_known_referrers := sum(locked_keys.values()):
        with pytest.raises(
            RuntimeError,
            match=re.escape(
                f"operation not permitted: sorted dictionary locked by {total_known_referrers} iterator(s)"
            ),
        ):
            sorted_dict.clear()
    sorted_dict_copy.clear()


if __name__ == "__main__":
    pytest.main()
