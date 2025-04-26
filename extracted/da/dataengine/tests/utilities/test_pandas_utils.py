import pandas as pd
from dataengine.utilities import pandas_utils


def test_get_null_columns_no_null():
    df = pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': ['a', 'b', 'c']})
    result = pandas_utils.get_null_columns(df)
    assert result == []


def test_get_null_columns_all_null():
    df = pd.DataFrame({
        'col1': [None, None, None],
        'col2': [None, None, None]})
    result = pandas_utils.get_null_columns(df)
    assert result == ['col1', 'col2']


def test_get_null_columns_mixed():
    df = pd.DataFrame({
        'col1': [1, None, None],
        'col2': [None, None, None],
        'col3': ['a', 'b', 'c']})
    result = pandas_utils.get_null_columns(df)
    assert result == ['col2']


def test_get_non_null_columns_no_null():
    df = pd.DataFrame({
        'col1': [1, 2, 3],
        'col2': ['a', 'b', 'c']})
    result = pandas_utils.get_non_null_columns(df)
    assert result == ['col1', 'col2']


def test_get_non_null_columns_all_have_null():
    df = pd.DataFrame({
        'col1': [1, None, None],
        'col2': ['a', None, 'c']})
    result = pandas_utils.get_non_null_columns(df)
    assert result == ['col1', 'col2']


def test_get_non_null_columns_mixed():
    df = pd.DataFrame({
        'col1': [1, None, 3],
        'col2': [None, None, None],
        'col3': ['a', 'b', 'c']})
    result = pandas_utils.get_non_null_columns(df)
    assert result == ['col1', 'col3']


def test_collapse_dataframe_columns_empty():
    df = pd.DataFrame()
    result = pandas_utils.collapse_dataframe_columns(df)
    assert result == []


def test_collapse_dataframe_columns_all_null():
    df = pd.DataFrame({'col1': [None, None], 'col2': [None, None]})
    result = pandas_utils.collapse_dataframe_columns(df)
    assert result == []


def test_collapse_dataframe_columns_some_null():
    df = pd.DataFrame({
        'col1': [1, None],
        'col2': ['a', 'b']})
    result = sorted(pandas_utils.collapse_dataframe_columns(df), key=str)
    assert result == [1, 'a', 'b']


def test_collapse_dataframe_columns_no_null():
    df = pd.DataFrame({
        'col1': [1, 2],
        'col2': ['a', 'b']})
    result = sorted(pandas_utils.collapse_dataframe_columns(df), key=str)
    assert result == [1, 2, 'a', 'b']


def test_collapse_dataframe_columns_duplicates():
    df = pd.DataFrame({
        'col1': [1, 1, 2],
        'col2': ['a', 'a', 'b']})
    result = sorted(pandas_utils.collapse_dataframe_columns(df), key=str)
    assert result == [1, 2, 'a', 'b']


def test_filter_dataframe_exact():
    df = pd.DataFrame({
        'col1': [1, 2],
        'col2': ['a', 'b'],
        'col3': [True, False]})
    result = pandas_utils.filter_dataframe(df, ['col1', 'col3'])
    assert result.columns.tolist() == ['col1', 'col3']


def test_filter_dataframe_filter_out_exact():
    df = pd.DataFrame({
        'col1': [1, 2],
        'col2': ['a', 'b'],
        'col3': [True, False]})
    result = pandas_utils.filter_dataframe(df, ['col1', 'col3'], filter_out=True)
    assert result.columns.tolist() == ['col2']


def test_filter_dataframe_substring():
    df = pd.DataFrame({
        'col1': [1, 2],
        'col2': ['a', 'b'],
        'col3': [True, False],
        'data1': ['x', 'y']})
    result = pandas_utils.filter_dataframe(df, ['col'], use_substring=True)
    assert result.columns.tolist() == ['col1', 'col2', 'col3']


def test_filter_dataframe_startswith():
    df = pd.DataFrame({
        'col1': [1, 2],
        'col2': ['a', 'b'],
        'col3': [True, False],
        'data1': ['x', 'y']})
    result = pandas_utils.filter_dataframe(df, ['col'], use_startswith=True)
    assert result.columns.tolist() == ['col1', 'col2', 'col3']


def test_filter_dataframe_empty_df():
    df = pd.DataFrame()
    result = pandas_utils.filter_dataframe(df, ['col1', 'col3'])
    assert result.columns.tolist() == []
