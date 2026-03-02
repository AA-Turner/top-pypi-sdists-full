#!/usr/bin/env python

'''
`pourhomogeneous` tests for `iterpop` package.
'''

import pytest


from iterpop import iterpop as ip

import pandas as pd

def test_pourhomogeneous_homogeneous():
    '''
    pourhomogeneous should pop out homogeneous values.
    '''
    assert ip.pourhomogeneous([0, 0]) == 0
    assert ip.pourhomogeneous(['a']) == 'a'
    assert ip.pourhomogeneous('aaaaaaa') == 'a'
    assert ip.pourhomogeneous((42 for __ in range(10))) == 42
    assert ip.pourhomogeneous({"monty"}) == "monty"

def test_pourhomogeneous_empty():
    '''
    pourhomogeneous should provide default on empty.
    '''
    for container in [], '', set(), range(0), {}, (x for x in range(0)):
        assert ip.pourhomogeneous(container) is None

def test_pourhomogeneous_heterogeneous():
    '''
    pourhomogeneous should pop throw on heterogenous.
    '''
    for container in [1,2], 'ab', {'al','bb'}, range(2), {1:'2', 3:'4'}:
        with pytest.raises(ValueError) as excinfo:
            ip.pourhomogeneous(container)
        assert 'is heterogeneous' in str(excinfo.value)

def test_pourhomogeneous_default():
    '''
    pourhomogeneous default should be configurable.
    '''
    for container in [], '', set(), range(0), {}:
        assert ip.pourhomogeneous(
            container,
            default='Madonna'
        ) == 'Madonna'

def test_pourhomogeneous_pandas():
    '''
    pourhomogeneous should play nice with Pandas.
    '''

    df = pd.DataFrame([
        {'unif' : 0, 'het' : 'x'},
        {'unif' : 0, 'het' : 'x'},
        {'unif' : 0, 'het' : 'y'},
        {'unif' : 0, 'het' : 'z'},
    ])

    # pop out homogeneous values
    assert ip.pourhomogeneous(df['unif']) == 0
    assert ip.pourhomogeneous(df[df['het'] == 'x']['het']) == 'x'
    assert ip.pourhomogeneous(df.iloc[-1]['het']) == 'z'

    # default on empty
    assert ip.pourhomogeneous(df[df['unif'] == 1]['het']) is None
    assert ip.pourhomogeneous(df[df['unif'] == 1]['het'], default='A') == 'A'

    # default on empty
    assert ip.pourhomogeneous(df[df['het'] == 1]['het']) is None
    assert ip.pourhomogeneous(df[df['het'] == 1]['het'], default='A') == 'A'

    # throw on heterogeneous
    with pytest.raises(ValueError) as excinfo:
        ip.pourhomogeneous(df['het'])
    assert 'is heterogeneous' in str(excinfo.value)
