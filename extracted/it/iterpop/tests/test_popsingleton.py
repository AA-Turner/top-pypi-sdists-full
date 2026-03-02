#!/usr/bin/env python

'''
`popsingleton` tests for `iterpop` package.
'''

import pytest


from iterpop import iterpop as ip

import pandas as pd

def test_popsingleton_singleton():
    '''
    popsingleton should pop singletons.
    '''
    assert ip.popsingleton([0]) == 0
    assert ip.popsingleton(['a']) == 'a'
    assert ip.popsingleton('a') == 'a'
    assert ip.popsingleton(range(1)) == 0
    assert ip.popsingleton({"monty"}) == "monty"

def test_popsingleton_empty():
    '''
    popsingleton should pop throw or provide default on empty.
    '''
    for container in [], '', set(), range(0), {}:
        with pytest.raises(ValueError) as excinfo:
            ip.popsingleton(container)
        assert 'is empty' in str(excinfo.value)

    for container in [], '', set(), range(0), {}:
        assert ip.popsingleton(container, catch_empty=True) == None

def test_popsingleton_overfull():
    '''
    popsingleton should pop throw or provide default on overfull.
    '''
    for container in [1,2], 'ab', {'al','bb'}, range(2), {1:'2', 3:'4'}:
        with pytest.raises(ValueError) as excinfo:
            ip.popsingleton(container)
        assert 'is overfull' in str(excinfo.value)

    for container in [1,2], 'ab', {'al','bb'}, range(2), {1:'2', 3:'4'}:
        assert ip.popsingleton(container, catch_overfull=True) == None

def test_popsingleton_default():
    '''
    popsingleton default should be configurable.
    '''
    for container in [], '', set(), range(0), {}:
        assert ip.popsingleton(
            container,
            catch_empty=True,
            default='Madonna'
        ) == 'Madonna'

    for container in [1,2], 'ab', {'al','bb'}, range(2), {1:'2', 3:'4'}:
        assert ip.popsingleton(
            container,
            catch_overfull=True,
            default='Cher',
        ) == 'Cher'

def test_popsingleton_pandas():
    '''
    popsingleton should play nice with pandas.
    '''

    df = pd.DataFrame([
        {'unif' : 0, 'het' : 'x'},
        {'unif' : 0, 'het' : 'x'},
        {'unif' : 0, 'het' : 'y'},
        {'unif' : 0, 'het' : 'z'},
    ])

    # pop out homogeneous values
    assert ip.popsingleton(df['unif'].unique()) == 0
    assert ip.popsingleton(df[df['het'] == 'y']['het']) == 'y'
    assert ip.popsingleton(df.iloc[-1]['het']) == 'z'

    # throw on empty
    with pytest.raises(ValueError) as excinfo:
        ip.popsingleton(df[df['unif'] == 1]['het'])
    assert 'is empty' in str(excinfo.value)

    # throw on empty
    with pytest.raises(ValueError) as excinfo:
        ip.popsingleton(df[df['unif'] == 1]['unif'])
    assert 'is empty' in str(excinfo.value)

    # throw on overfull
    with pytest.raises(ValueError) as excinfo:
        ip.popsingleton(df['het'])
    assert 'is overfull' in str(excinfo.value)

    # throw on overfull
    with pytest.raises(ValueError) as excinfo:
        ip.popsingleton(df['unif'])
    assert 'is overfull' in str(excinfo.value)
