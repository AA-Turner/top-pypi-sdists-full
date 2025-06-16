from collections import OrderedDict

import pytest

from d8s_lists import (
    cycle,
    deduplicate,
    duplicates,
    flatten,
    has_index,
    iterable_all_items_of_types,
    iterable_count,
    iterable_has_all_items_of_type,
    iterable_has_mixed_types,
    iterable_has_single_item,
    iterable_has_single_type,
    iterable_item_index,
    iterable_item_indexes,
    iterable_item_of_types,
    iterable_replace,
    iterable_sort_by_length,
    iterables_are_same_length,
    iterables_have_same_items,
    longest,
    nontruthy_items,
    run_length_encoding,
    shortest,
    truthy_items,
    types,
)

# from pyannotate_runtime import collect_types

# collect_types.init_types_collection()
# collect_types.start()


@pytest.mark.parametrize("test_input,result_contents", [((None, False, [], 0), ()), ([1, 0, True, False], (1, True))])
def test_truthy_items_1(test_input, result_contents):
    result = tuple(truthy_items(test_input))
    assert result == result_contents


@pytest.mark.parametrize(
    "test_input,result_contents", [((None, False, [], 0), (None, False, [], 0)), ([1, 0, True, False], (0, False))]
)
def test_nontruthy_items_1(test_input, result_contents):
    result = tuple(nontruthy_items(test_input))
    assert result == result_contents


def test_iterable_has_all_items_of_type_1():
    assert not iterable_has_all_items_of_type([1, 'a'], int)
    assert iterable_has_all_items_of_type([1, 2, 3, 4, 5], int)
    assert iterable_has_all_items_of_type([1, 2], int)
    assert not iterable_has_all_items_of_type([1, {2}], int)


def test_iterable_all_items_of_types_1():
    assert not iterable_all_items_of_types([1, 'a'], (int,))
    assert iterable_all_items_of_types([1, 'a'], (int, str))
    assert iterable_all_items_of_types([1, 'a', 3, 4], (int, str))
    assert not iterable_all_items_of_types([1, 'a', 3, {4}], (int, str))


def test_iterable_has_mixed_types_1():
    assert iterable_has_mixed_types([0, 'a'])
    assert iterable_has_mixed_types([0, 'a'])
    assert not iterable_has_mixed_types([0, 1])
    assert not iterable_has_mixed_types([{}, {}])


def test_iterable_has_single_type_1():
    assert not iterable_has_single_type([0, 'a'])
    assert not iterable_has_single_type([0, 'a'])
    assert iterable_has_single_type([0, 1])
    assert iterable_has_single_type([{}, {}])


def test_iterable_has_single_item_1():
    assert not iterable_has_single_item([])
    assert iterable_has_single_item([0])
    assert iterable_has_single_item([0, 0])
    assert not iterable_has_single_item([0, 1])


def test_iterables_have_same_items_docs_1():
    assert iterables_have_same_items([1], [1])
    assert not iterables_have_same_items([1], [2])
    assert not iterables_have_same_items([1], [1, 1])

    assert iterables_have_same_items([2, 1], [1, 2])
    assert not iterables_have_same_items([1], [2, 1])
    assert not iterables_have_same_items([2, 1], [1])
    assert not iterables_have_same_items([2, 2], [1, 2])

    assert iterables_have_same_items([1, 2, 3], [3, 1, 2])
    assert not iterables_have_same_items([1, 2, 3, 4], [3, 1, 2])
    assert not iterables_have_same_items([1, 2, 3], [3, 1, 2, 4])
    assert not iterables_have_same_items([1, 3, 3], [3, 3, 2])


def test_iterables_have_same_items_docs_2():
    assert iterables_have_same_items([1, 2, 3], [3, 2, 1])
    assert iterables_have_same_items([1, 2, 3], [3, 1, 2])
    assert not iterables_have_same_items([1, 2, 3, 3], [1, 2, 2, 3])
    assert not iterables_have_same_items([1], [1, 2])


def test_iterable_item_of_types_1():
    assert iterable_item_of_types([{'a': 1}, 1, 2, 3], (dict,))
    assert not iterable_item_of_types([1, 2, 3], (dict,))


def test_longest_1():
    l = ['a', 'aa', 'aaa']
    result = longest(l)
    assert result == 'aaa'


def test_shortest_1():
    l = ['a', 'aa', 'aaa']
    result = shortest(l)
    assert result == 'a'


def test_iterable_sort_by_length_1():
    l = ['a', 'aa', 'aaa']
    result = iterable_sort_by_length(l)
    assert result == ['a', 'aa', 'aaa']

    l = ['a', 'aa', 'aaa']
    result = iterable_sort_by_length(l, reverse=True)
    assert result == ['aaa', 'aa', 'a']

    l = ('a', 'aa', 'aaa')
    result = iterable_sort_by_length(l, reverse=True)
    assert result == ['aaa', 'aa', 'a']


def test_iterable_item_indexes_1():
    assert tuple(iterable_item_indexes([1, 2, 1, 2], 1)) == (0, 2)
    assert tuple(iterable_item_indexes([1, 2, 1, 2], 2)) == (1, 3)
    assert tuple(iterable_item_indexes([1, 2], 3)) == ()


def test_flatten_1():
    assert tuple(flatten([1, 2, 3])) == (1, 2, 3)
    assert tuple(flatten([1, [2], 3])) == (1, 2, 3)
    assert tuple(flatten([1, [2, 3]])) == (1, 2, 3)
    assert tuple(flatten([(1, 2), ([3, 4], [[5], [6]])])) == (1, 2, 3, 4, 5, 6)
    assert tuple(flatten([(1, 2), ([3, 4], [[5], [6]])], level=1)) == (1, 2, [3, 4], [[5], [6]])


def test_has_index_1():
    assert not has_index(['a', 'b', 'c'], -1)
    assert has_index(['a', 'b', 'c'], 0)
    assert has_index(['a', 'b', 'c'], 1)
    assert has_index(['a', 'b', 'c'], 2)
    assert not has_index(['a', 'b', 'c'], 3)
    assert not has_index(['a', 'b', 'c'], 4)
    assert not has_index(['a', 'b', 'c'], 4000)


def test_iterables_are_same_length_1():
    l1 = ['a']
    l2 = ['b']
    l3 = ['a']
    l4 = ['a', 'b']
    l5 = []

    assert iterables_are_same_length(l1, l2)
    assert iterables_are_same_length(l1, l2, l3)
    assert not iterables_are_same_length(l1, l2, l3, l4)
    assert not iterables_are_same_length(l1, l2, l3, l4, l5)
    assert iterables_are_same_length(l1, l3)
    assert not iterables_are_same_length(l1, l4)
    assert not iterables_are_same_length(l4, l5)
    assert not iterables_are_same_length(l1, l5)

    assert not iterables_are_same_length(l1, l4, debug_failure=True)
    assert not iterables_are_same_length(l1, l2, l3, l4, l5, debug_failure=True)


def test_types_1():
    assert tuple(types([1, 2, 3])) == (int, int, int)
    assert tuple(types(['a', 'b', 'c'])) == (str, str, str)


def test_iterable_replace_docs_1():
    old_list = [1, 2, 3]
    new_list = tuple(iterable_replace(old_list, 1, 4))
    assert new_list == (4, 2, 3)
    # test immutability
    assert old_list == [1, 2, 3]

    old_list = [1, 2, 3]
    new_list = tuple(iterable_replace(old_list, 5, 3))
    assert new_list == (1, 2, 3)
    # test immutability
    assert old_list == [1, 2, 3]

    old_list = [1, 1, 1]
    new_list = tuple(iterable_replace(old_list, 1, 0))
    assert new_list == (0, 0, 0)
    # test immutability
    assert old_list == [1, 1, 1]

    old_list = [1, 2, 3]
    new_list = tuple(iterable_replace(old_list, 1, 4))
    assert new_list == (4, 2, 3)
    # test immutability
    assert old_list == [1, 2, 3]

    old_list = [[1], [2, 2], [3, 3, 3]]
    new_list = tuple(iterable_replace(old_list, [1], [4, 4, 4, 4]))
    assert new_list == ([4, 4, 4, 4], [2, 2], [3, 3, 3])
    # test immutability
    assert old_list == [[1], [2, 2], [3, 3, 3]]

    old_list = [[{'a': 1}], [{'b': 2}], [{'c': 3}]]
    new_list = tuple(iterable_replace(old_list, [{'a': 1}], [{'e': 1}]))
    assert new_list == ([{'e': 1}], [{'b': 2}], [{'c': 3}])
    # test immutability
    assert old_list == [[{'a': 1}], [{'b': 2}], [{'c': 3}]]


def test_deduplicate_1():
    assert tuple(deduplicate([1, 2, 3, 3, 3, 4, 2])) == (1, 2, 3, 4)


def test_deduplicate_dicts():
    assert tuple(deduplicate([{'a': 1}, 1, {'b': 2}])) == ({'a': 1}, 1, {'b': 2})
    assert tuple(deduplicate([{'a': 1}, {'a': 1}, {'b': 2}])) == ({'a': 1}, {'b': 2})


def test_duplicates():
    assert tuple(duplicates([1, 2, 3, 3, 2])) == (2, 3, 3, 2)
    assert tuple(duplicates([1, 2])) == ()
    assert tuple(duplicates([1, 2, 2])) == (2, 2)

    assert tuple(duplicates([1, 2, 3, 3, 2])) == (2, 3, 3, 2)
    assert tuple(duplicates([1, 2, 2, 2, 2, 3])) == (2, 2, 2, 2)
    assert tuple(duplicates([1, 2, 1, 2])) == (1, 2, 1, 2)


def test_run_length_encoding_1():
    assert tuple(run_length_encoding('foobar')) == (
        '1f',
        '2o',
        '1b',
        '1a',
        '1r',
    )
    assert tuple(run_length_encoding(list('foobar'))) == (
        '1f',
        '2o',
        '1b',
        '1a',
        '1r',
    )

    assert tuple(run_length_encoding(['a'])) == ('1a',)
    assert tuple(run_length_encoding(['a', 'a'])) == ('2a',)
    assert tuple(run_length_encoding(['a', 'b'])) == (
        '1a',
        '1b',
    )
    assert tuple(run_length_encoding(['a', 'a', 'b'])) == (
        '2a',
        '1b',
    )
    assert tuple(run_length_encoding(['a', 'b', 'b'])) == (
        '1a',
        '2b',
    )
    assert tuple(run_length_encoding(['a', 'b', 'a'])) == (
        '1a',
        '1b',
        '1a',
    )


def test_run_length_encoding_2():
    assert tuple(run_length_encoding(['aa'])) == ('1aa',)
    assert tuple(run_length_encoding(['aa', 'aa'])) == ('2aa',)
    assert tuple(run_length_encoding(['aa', 'bbb'])) == (
        '1aa',
        '1bbb',
    )
    assert tuple(run_length_encoding(['aa', 'aa', 'bbb'])) == (
        '2aa',
        '1bbb',
    )
    assert tuple(run_length_encoding(['aa', 'bbb', 'bbb'])) == (
        '1aa',
        '2bbb',
    )
    assert tuple(run_length_encoding(['aa', 'bbb', 'aa'])) == (
        '1aa',
        '1bbb',
        '1aa',
    )
    assert tuple(run_length_encoding('WWWWWWWWWWWWBWWWWWWWWWWWWBBBWWWWWWWWWWWWWWWWWWWWWWWWBWWWWWWWWWWWWWW')) == (
        '12W',
        '1B',
        '12W',
        '3B',
        '24W',
        '1B',
        '14W',
    )


def test_multiple_duplicates():
    assert tuple(duplicates([1, 2, 3, 3, 2, 1, 3, 4, 5])) == (1, 2, 3, 3, 2, 1, 3)


def test_iterable_count_1():
    assert iterable_count([1, 2, 3, 2, 3]) == OrderedDict([(1, 1), (2, 2), (3, 2)])
    assert iterable_count(['bob', 'bob', 'frank', 'bob', 'john', 'frank', 'tim', 'tim']) == OrderedDict(
        [('john', 1), ('frank', 2), ('tim', 2), ('bob', 3)]
    )


def test_iterable_item_index_1():
    assert iterable_item_index(['a', 'b'], 'a') == 0
    assert iterable_item_index(['a', 'b'], 'b') == 1
    assert iterable_item_index(['a', 'b'], 'c') == -1


def test_cycle_1():
    l = tuple(cycle([1, 2, 3], length=42))
    assert len(l) == 42
    assert l[0] == 1
    assert l[1] == 2
    assert l[2] == 3
    assert l[3] == 1
    # collect_types.stop()
    # collect_types.dump_stats('type_info.json')


# TODO: write test for `remove_nonexistent_items` that test the following cases:
# ('', [], 0, False, None)
