#!/usr/bin/env python

'''
`pophomogeneous` tests for `iterpop` package.
'''

import pytest


from iterpop import iterpop as ip

import pandas as pd

def test_pophomogeneous_homogeneous():
    '''
    pophomogeneous should pop out homogeneous values.
    '''
    assert ip.pophomogeneous([0, 0]) == 0
    assert ip.pophomogeneous(['a']) == 'a'
    assert ip.pophomogeneous('aaaaaaa') == 'a'
    assert ip.pophomogeneous((42 for __ in range(10))) == 42
    assert ip.pophomogeneous({"monty"}) == "monty"

def test_pophomogeneous_empty():
    '''
    pophomogeneous should pop throw or provide default on empty.
    '''
    for container in [], '', set(), range(0), {}:
        with pytest.raises(ValueError) as excinfo:
            ip.pophomogeneous(container)
        assert 'is empty' in str(excinfo.value)

    for container in [], '', set(), range(0), {}:
        assert ip.pophomogeneous(container, catch_empty=True) == None

def test_pophomogeneous_heterogeneous():
    '''
    pophomogeneous should pop throw or provide default on heterogenous.
    '''
    for container in [1,2], 'ab', {'al','bb'}, range(2), {1:'2', 3:'4'}:
        with pytest.raises(ValueError) as excinfo:
            ip.pophomogeneous(container)
        assert 'is heterogeneous' in str(excinfo.value)

    for container in [1,2], 'ab', {'al','bb'}, range(2), {1:'2', 3:'4'}:
        assert ip.pophomogeneous(container, catch_heterogeneous=True) == None

def test_pophomogeneous_default():
    '''
    pophomogeneous default should be configurable.
    '''
    for container in [], '', set(), range(0), {}:
        assert ip.pophomogeneous(
            container,
            catch_empty=True,
            default='Madonna'
        ) == 'Madonna'

    for container in [1,2], 'ab', {'al','bb'}, range(2), {1:'2', 3:'4'}:
        assert ip.pophomogeneous(
            container,
            catch_heterogeneous=True,
            default='Cher',
        ) == 'Cher'

def test_pophomogeneous_pandas():
    '''
    pophomogeneous should play nice with Pandas.
    '''

    df = pd.DataFrame([
        {'unif' : 0, 'het' : 'x'},
        {'unif' : 0, 'het' : 'x'},
        {'unif' : 0, 'het' : 'y'},
        {'unif' : 0, 'het' : 'z'},
    ])

    # pop out homogeneous values
    assert ip.pophomogeneous(df['unif']) == 0
    assert ip.pophomogeneous(df[df['het'] == 'x']['het']) == 'x'
    assert ip.pophomogeneous(df.iloc[-1]['het']) == 'z'

    # throw on empty
    with pytest.raises(ValueError) as excinfo:
        ip.pophomogeneous(df[df['unif'] == 1]['het'])
    assert 'is empty' in str(excinfo.value)

    # throw on empty
    with pytest.raises(ValueError) as excinfo:
        ip.pophomogeneous(df[df['unif'] == 1]['unif'])
    assert 'is empty' in str(excinfo.value)

    # throw on heterogeneous
    with pytest.raises(ValueError) as excinfo:
        ip.pophomogeneous(df['het'])
    assert 'is heterogeneous' in str(excinfo.value)
