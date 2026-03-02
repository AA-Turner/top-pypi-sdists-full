import pytest

from downstream._auxlib._indexable_range import indexable_range


def test_contains_true_and_false():
    r = indexable_range(0, 10, 2)  # [0,2,4,6,8]
    assert 4 in r
    assert 5 not in r
    assert 0 in r
    assert 9 not in r


def test_empty_range_behavior():
    r = indexable_range(5, 5)
    assert len(r) == 0
    assert list(r) == []
    assert 0 not in r
    # slicing an empty range gives empty
    s = r[0:10]
    assert isinstance(s, indexable_range)
    assert list(s) == []


def test_slice_with_step_arg():
    r = indexable_range(0, 10, 2)  # [0,2,4,6,8]
    s = r[1:5:2]
    # picks r[1]=2 and r[3]=6
    assert isinstance(s, indexable_range)
    assert list(s) == [2, 6]


def test_slice_negative_step_on_forward_range():
    r = indexable_range(0, 10, 2)  # [0,2,4,6,8]
    s = r[4:1:-1]
    # elements at indices 4,3,2 => [8,6,4]
    assert list(s) == [8, 6, 4]


def test_slice_out_of_bound_indices():
    r = indexable_range(5)  # [0,1,2,3,4]
    assert list(r[10:20]) == []
    assert list(r[-10:3]) == [0, 1, 2]


def test_index_method_and_value_error():
    r = indexable_range(0, 10, 3)  # [0,3,6,9]
    assert r.index(6) == 2
    with pytest.raises(ValueError):
        r.index(5)


def test_sequence_equality_and_comparison_to_list():
    r1 = indexable_range(5)
    r2 = indexable_range(0, 5, 1)
    assert r1 == r2
    assert list(r1) == [0, 1, 2, 3, 4]
    assert r1 != indexable_range(5, 10)
    # reversed equality
    rev = reversed(r1)
    assert rev == rev
    assert rev != r1
    assert list(rev) == [4, 3, 2, 1, 0]


def test_negative_step_full_range():
    r = indexable_range(5, 0, -1)  # [5,4,3,2,1]
    assert len(r) == 5
    assert list(r) == [5, 4, 3, 2, 1]
    assert 3 in r
    assert 0 not in r


def test_iteration_and_for_loop():
    r = indexable_range(3)
    acc = []
    for x in r:
        acc.append(x * 2)
    assert acc == [0, 2, 4]


def test_invalid_step_slice_zero():
    r = indexable_range(0, 5, 1)
    with pytest.raises(ValueError):
        # slicing with a zero stride should fail
        _ = r[1:4:0]
