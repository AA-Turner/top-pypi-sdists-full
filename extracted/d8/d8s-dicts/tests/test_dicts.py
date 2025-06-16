# -*- coding: utf-8 -*-

import pytest

from d8s_dicts import (
    is_dict,
    dict_keys,
    dict_values,
    dict_has_value,
    dict_key_types,
    dict_value_types,
    dict_keys_with_value,
    dict_sort_by_keys,
    dict_sort_by_values,
    dicts_sort_by_value_at_key,
    dict_flip,
    dict_delistify_values,
    dict_examples,
    dict_add,
    dicts_diffs,
    dict_copy_value_at_key,
    dict_move_value_at_key,
    dict_key_delete,
    dict_delete_items,
    dict_delete_empty_values,
    dict_filter_by_keys,
    dict_filter_by_values,
    dict_keys_with_max_value,
    dict_keys_with_min_value,
    dict_value_with_max_key,
    dict_value_with_min_key,
)


def test_dict_keys_with_max_value_docs_1():
    d = {'a': 1, 'b': 2, 'c': 3}
    assert dict_keys_with_max_value(d) == ['c']

    d = {'a': 1, 'b': 2, 'c': 3, 'd': 3}
    assert dict_keys_with_max_value(d) == ['c', 'd']


def test_dict_keys_with_min_value_docs_1():
    d = {'a': 1, 'b': 2, 'c': 3}
    assert dict_keys_with_min_value(d) == ['c']

    d = {'a': 1, 'b': 2, 'c': 3, 'd': 3}
    assert dict_keys_with_min_value(d) == ['c', 'd']


def test_dict_value_with_max_key_docs_1():
    d = {'a': 1, 'b': 2, 'c': 3}
    assert dict_value_with_max_key(d) == 3


def test_dict_value_with_min_key_docs_1():
    d = {'a': 1, 'b': 2, 'c': 3}
    assert dict_value_with_min_key(d) == 1


def test_dict_filter_by_values_1():
    result = dict_filter_by_values({1: 'a', 2: 'b'}, lambda x: x > 'a')
    assert result == {2: 'b'}


def test_dict_filter_by_keys_1():
    result = dict_filter_by_keys({1: 'a', 2: 'b'}, lambda x: x > 1)
    assert result == {2: 'b'}


def test_dict_delete_items_1():
    d = {'a': 1}
    result = dict_delete_items(d, values_to_delete=[1, 2])
    assert result == {}
    # test immutability
    assert d == {'a': 1}

    d = {'a': 1}
    result = dict_delete_items(d, values_to_delete=[2, 3])
    assert result == {'a': 1}
    # test immutability
    assert d == {'a': 1}

    d = {'a': 1}
    result = dict_delete_items(d, keys_to_delete=['a', 'b'])
    assert result == {}
    # test immutability
    assert d == {'a': 1}

    d = {'a': 1}
    result = dict_delete_items(d, keys_to_delete=['b', 'c'])
    assert result == {'a': 1}
    # test immutability
    assert d == {'a': 1}

    d = {'a': 1}
    result = dict_delete_items(d, keys_to_delete=['a'], values_to_delete=[2])
    assert result == {}
    # test immutability
    assert d == {'a': 1}


def test_dicts_diffs_1():
    a = {'a': 1}
    b = {'b': 1}
    result = dicts_diffs(a, b)
    assert list(result) == [('add', '', [('b', 1)]), ('remove', '', [('a', 1)])]

    a = {'a': {'b': 2}}
    b = {'a': {'c': 3}}
    result = dicts_diffs(a, b)
    assert list(result) == [('add', 'a', [('c', 3)]), ('remove', 'a', [('b', 2)])]


def test_dict_examples_1():
    result = dict_examples()
    assert len(result) == 10

    result = dict_examples(n=100)
    assert len(result) == 100


def test_dict_keys_with_value_1():
    d = {'a': 1, 'b': 2}
    result = dict_keys_with_value(d, 1)
    assert result == ['a']

    d = {'a': 1, 'b': 2, 'c': 1}
    result = dict_keys_with_value(d, 1)
    assert result == ['a', 'c']

    d = {'a': 1, 'b': 2, 'c': 1}
    result = dict_keys_with_value(d, 0)
    assert result == []


def test_dict_key_types_1():
    result = dict_key_types({'a': 1, 2: 'b', (1, 2, 3): 'bar'})
    assert result == [str, int, tuple]


def test_dict_has_value_1():
    assert dict_has_value({1: 2}, 2)
    assert not dict_has_value({1: 2}, 3)


def test_is_dict_1():
    assert is_dict({})
    assert is_dict({1: 2})


def test_dict_value_types_1():
    d = {
        'a': 1,
        'b': 'b',
        'c': (
            1,
            2,
        ),
        'd': {'a': 1},
    }
    results = dict_value_types(d)
    assert results == {'a': int, 'b': str, 'c': tuple, 'd': dict}


def test_dict_copy_value_at_key_1():
    d = {'a': 1, 'b': 2}
    assert dict_copy_value_at_key(d, 'a', 'c') == {'a': 1, 'b': 2, 'c': 1}

    # test immutability
    assert d == {'a': 1, 'b': 2}


def test_dict_delistify_values_1():
    d = {'a': [1], 'b': [1, 2], 'c': [1, 2, 3], 'd': ['foo']}

    assert dict_delistify_values(d) == {'a': 1, 'b': [1, 2], 'c': [1, 2, 3], 'd': 'foo'}


def test_dict_delistify_values_immutability():
    d = {'a': [1], 'b': [1, 2], 'c': [1, 2, 3], 'd': ['foo']}

    assert dict_delistify_values(d) == {'a': 1, 'b': [1, 2], 'c': [1, 2, 3], 'd': 'foo'}

    # test immutability
    assert d == {'a': [1], 'b': [1, 2], 'c': [1, 2, 3], 'd': ['foo']}


def test_dict_sort_by_keys_1():
    d = {'b': 1, 'a': 2}
    assert dict_sort_by_keys(d) == {'a': 2, 'b': 1}


def test_dicts_sort_by_value_at_key_1():
    l = [{'a': 2, 'b': 1}, {'a': 1, 'b': 2}]
    results = dicts_sort_by_value_at_key(l, 'a')
    assert list(results) == [{'a': 1, 'b': 2}, {'a': 2, 'b': 1}]
    # test immutability
    assert l == [{'a': 2, 'b': 1}, {'a': 1, 'b': 2}]

    l = [{'a': 2, 'b': 'foo'}, {'a': 1, 'b': 'z'}, {'a': 2, 'b': 'bar'}]
    results = dicts_sort_by_value_at_key(l, 'a')
    assert list(results) == [{'a': 1, 'b': 'z'}, {'a': 2, 'b': 'foo'}, {'a': 2, 'b': 'bar'}]
    # test immutability
    assert l == [{'a': 2, 'b': 'foo'}, {'a': 1, 'b': 'z'}, {'a': 2, 'b': 'bar'}]

    # if we are trying to sort a dict by a value at a key that doesn't exist, raise a KeyError
    with pytest.raises(KeyError):
        l = [{'a': 2, 'b': 'foo'}, {'b': 'z'}]
        results = dicts_sort_by_value_at_key(l, 'a')


def test_dict_flip_1():
    d = {'a': 1, 'b': 2}
    assert dict_flip(d) == {1: ['a'], 2: ['b']}
    # test immutability
    assert d == {'a': 1, 'b': 2}

    d = {'a': 1, 'b': 1}
    assert dict_flip(d) == {1: ['a', 'b']}
    # test immutability
    assert d == {'a': 1, 'b': 1}

    d = {'a': [1, 2, 3], 'b': [1, 2, 4]}
    assert dict_flip(d) == {}
    # test immutability
    assert d == {'a': [1, 2, 3], 'b': [1, 2, 4]}

    d = {'a': [[1, 2], [3]]}
    assert dict_flip(d) == {}
    # test immutability
    assert d == {'a': [[1, 2], [3]]}

    d = {'a': {'b': 2}}
    assert dict_flip(d) == {}
    # test immutability
    assert d == {'a': {'b': 2}}


def test_dict_flip_flatten_values():
    d = {'a': 1, 'b': 2}
    assert dict_flip(d, flatten_values=True) == {1: 'a', 2: 'b'}
    # test immutability
    assert d == {'a': 1, 'b': 2}

    d = {'a': 1, 'b': 1}
    assert dict_flip(d, flatten_values=True) == {1: ['a', 'b']}
    # test immutability
    assert d == {'a': 1, 'b': 1}

    d = {'a': [1, 2, 3], 'b': [1, 2, 4]}
    assert dict_flip(d, flatten_values=True) == {}
    # test immutability
    assert d == {'a': [1, 2, 3], 'b': [1, 2, 4]}

    d = {'a': [[1, 2], [3]]}
    assert dict_flip(d, flatten_values=True) == {}
    # test immutability
    assert d == {'a': [[1, 2], [3]]}


def test_dict_flip_flip_lists_and_sets():
    d = {'a': [1, 2, 3], 'b': [1, 2, 4]}
    assert dict_flip(d, flip_lists_and_sets=True) == {1: ['a', 'b'], 2: ['a', 'b'], 3: ['a'], 4: ['b']}
    assert dict_flip(d, flatten_values=True, flip_lists_and_sets=True) == {1: ['a', 'b'], 2: ['a', 'b'], 3: 'a', 4: 'b'}
    # test immutability
    assert d == {'a': [1, 2, 3], 'b': [1, 2, 4]}

    d = {'a': [1, 2, 3], 'b': {1, 2, 4}}
    assert dict_flip(d, flip_lists_and_sets=True) == {1: ['a', 'b'], 2: ['a', 'b'], 3: ['a'], 4: ['b']}
    assert dict_flip(d, flatten_values=True, flip_lists_and_sets=True) == {1: ['a', 'b'], 2: ['a', 'b'], 3: 'a', 4: 'b'}
    # test immutability
    assert d == {'a': [1, 2, 3], 'b': {1, 2, 4}}

    d = {'a': [[1, 2], [3]]}
    with pytest.raises(TypeError) as e:
        dict_flip(d, flip_lists_and_sets=True)
        assert (
            'Unable to flip <<[[1, 2], [3]]>> because it contains items of a type which cannot be the keys for dictionaries.'
            in e
        )
    # test immutability
    assert d == {'a': [[1, 2], [3]]}


def test_dict_delete_empty_values_1():
    d = {'a': 1, 'b': '', 'c': 0, 'd': None, 'e': [], 'f': False}
    results = dict_delete_empty_values(d)
    assert results == {'a': 1}
    # test immutability
    assert d == {'a': 1, 'b': '', 'c': 0, 'd': None, 'e': [], 'f': False}

    d = {'a': 1, 'b': ' foo', 'c': 0, 'd': None, 'e': [1, 2]}
    results = dict_delete_empty_values(d)
    assert results == {'a': 1, 'b': ' foo', 'e': [1, 2]}
    # test immutability
    assert d == {'a': 1, 'b': ' foo', 'c': 0, 'd': None, 'e': [1, 2]}


def test_dict_sort_by_values_1():
    d = {'c': 'cc', 'a': 'aa', 'b': 'bb'}
    assert dict_sort_by_values(d) == {'a': 'aa', 'b': 'bb', 'c': 'cc'}
    # test immutability
    assert d == {'c': 'cc', 'a': 'aa', 'b': 'bb'}


def test_dict_sort_by_values_number_keys():
    d = {'2': 'cc', '3': 'aa', '1': 'bb'}
    assert dict_sort_by_values(d) == {'3': 'aa', '1': 'bb', '2': 'cc'}
    # test immutability
    assert d == {'2': 'cc', '3': 'aa', '1': 'bb'}


def test_dict_sort_by_values_number_values():
    d = {'2': 2, '3': 3, '1': 1}
    assert dict_sort_by_values(d) == {'1': 1, '2': 2, '3': 3}
    # test immutability
    assert d == {'2': 2, '3': 3, '1': 1}

    d = {'c': 2, 'a': 3, 'b': 1}
    assert dict_sort_by_values(d) == {'b': 1, 'c': 2, 'a': 3}
    # test immutability
    assert d == {'c': 2, 'a': 3, 'b': 1}


def test_dict_add_1():
    d = {}
    # add an item
    d = dict_add(d, 'test', 1)
    assert d == {'test': [1]}

    # add an existing item
    d = dict_add(d, 'test', 1)
    assert d == {'test': [1, 1]}

    # add an item with a new key
    d = dict_add(d, 'foo', 1)
    assert d == {'test': [1, 1], 'foo': [1]}

    # add an existing item (again)
    d = dict_add(d, 'test', 1)
    assert d == {'test': [1, 1, 1], 'foo': [1]}

    with pytest.raises(TypeError) as e:
        dict_add({'a': 1}, 'a', 2)
        assert 'The value at the "a" key' in e


def test_dict_add_immutability():
    a = {}
    # make sure the dict returned by the dict_add function is a copy of the given dict and does not modify the given dict
    b = dict_add(a, 'test', 1)
    assert a == {}
    assert b == {'test': [1]}


def test_dict_key_delete_1():
    assert dict_key_delete({1: 2}, 1) == {}
    assert dict_key_delete({}, 'a') == {}
    assert dict_key_delete({'a': 'baafds'}, 'a') == {}
    assert dict_key_delete({'a': 'b', 'c': 'd'}, 'a') == {'c': 'd'}
    assert dict_key_delete({'a': 'b', 'c': 'd'}, 'foo') == {'a': 'b', 'c': 'd'}


def test_dict_key_delete_immutability():
    d = {1: 2}
    assert dict_key_delete(d, 1) == {}
    assert d == {1: 2}


def test_dict_key_delete_2():
    d = {'a': 1, 'b': 2}
    assert dict_key_delete(d, 'a') == {'b': 2}
    assert d == {'a': 1, 'b': 2}


def test_dict_move_value_at_key_1():
    assert dict_move_value_at_key({'a': 1}, 'a', 'b') == {'b': 1}


def test_dict_move_value_at_key_immutability():
    d = {'a': 1}
    assert dict_move_value_at_key(d, 'a', 'b') == {'b': 1}
    assert d == {'a': 1}
