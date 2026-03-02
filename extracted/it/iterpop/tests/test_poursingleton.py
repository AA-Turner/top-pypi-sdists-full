#!/usr/bin/env python

'''
`poursingleton` tests for `iterpop` package.
'''

import pytest


from iterpop import iterpop as ip

import pandas as pd

def test_poursingleton_singleton():
    '''
    poursingleton should pop singletons.
    '''
    assert ip.poursingleton([0]) == 0
    assert ip.poursingleton(['a']) == 'a'
    assert ip.poursingleton('a') == 'a'
    assert ip.poursingleton(range(1)) == 0
    assert ip.poursingleton({"monty"}) == "monty"

def test_poursingleton_empty():
    '''
    poursingleton should provide default on empty.
    '''
    for container in [], '', set(), range(0), {}:
        assert ip.poursingleton(container) is None

def test_poursingleton_overfull():
    '''
    poursingleton should throw on overfull.
    '''
    for container in [1,2], 'ab', {'al','bb'}, range(2), {1:'2', 3:'4'}:
        with pytest.raises(ValueError) as excinfo:
            ip.poursingleton(container)
        assert 'is overfull' in str(excinfo.value)

def test_poursingleton_default():
    '''
    poursingleton default should be configurable.
    '''
    for container in [], '', set(), range(0), {}:
        assert ip.poursingleton(
            container,
            default='Madonna'
        ) == 'Madonna'

def test_poursingleton_pandas():
    '''
    poursingleton should play nice with pandas.
    '''

    df = pd.DataFrame([
        {'unif' : 0, 'het' : 'x'},
        {'unif' : 0, 'het' : 'x'},
        {'unif' : 0, 'het' : 'y'},
        {'unif' : 0, 'het' : 'z'},
    ])

    # pop out homogeneous values
    assert ip.poursingleton(df['unif'].unique()) == 0
    assert ip.poursingleton(df[df['het'] == 'y']['het']) == 'y'
    assert ip.poursingleton(df.iloc[-1]['het']) == 'z'

    # default on empty
    assert ip.poursingleton(df[df['unif'] == 1]['het']) is None
    assert ip.poursingleton(df[df['unif'] == 1]['het'], default='A') == 'A'

    # throw on empty
    assert ip.poursingleton(df[df['unif'] == 1]['unif']) is None
    assert ip.poursingleton(df[df['unif'] == 1]['unif'], default='A') == 'A'

    # throw on overfull
    with pytest.raises(ValueError) as excinfo:
        ip.poursingleton(df['het'])
    assert 'is overfull' in str(excinfo.value)

    # throw on overfull
    with pytest.raises(ValueError) as excinfo:
        ip.poursingleton(df['unif'])
    assert 'is overfull' in str(excinfo.value)
