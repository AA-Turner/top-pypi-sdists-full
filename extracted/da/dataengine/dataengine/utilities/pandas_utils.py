"""
Pandas Utility methods.
"""
import itertools


def get_null_columns(pandas_df):
    """
    This function will get null columns.

    Args:
        pandas_df (pandas.core.frame.DataFrame): pandas DataFrame

    Returns:
        list of non null columns
    """
    return [
        column_header
        for column_header, is_null in pandas_df.isnull().all().items()
        if is_null]


def get_non_null_columns(pandas_df):
    """
    This function will get non null columns.

    Args:
        pandas_df (pandas.core.frame.DataFrame): pandas DataFrame

    Returns:
        list of non null columns
    """
    return [
        column_header
        for column_header, is_null in pandas_df.isnull().all().items()
        if not is_null]


def collapse_dataframe_columns(pandas_df):
    """
    This method will collapse DataFrame column values into a list.

    Args:
        pandas_df (pandas.DataFrame): pandas DataFrame

    Returns:
        list of unique column values
    """
    return list(set(itertools.chain.from_iterable([
        pandas_df[~pandas_df[col].isnull()][col].values.tolist()
        for col in pandas_df.columns])))


def filter_dataframe(
        pandas_df, cols, filter_out=False, use_substring=False,
        use_startswith=False):
    """
    This method will filter a DataFrame by a list of columns.

    Args:
        pandas_df (pandas.DataFrame): pandas DataFrame
        cols (list): list of desired columns
        filter_out (bool): switch to filter columns out of DataFrame
        use_substring (bool): switch to use substring logic
        use_startswith (bool): switch to use startswith logic

    Returns:
        filtered DataFrame
    """
    # Create condition lambda function
    if use_substring:
        column_filter = lambda c: any(
            str(substring) in c for substring in cols)
    elif use_startswith:
        column_filter = lambda c: any(
            c.startswith(substring) for substring in cols)
    else:
        column_filter = lambda c: c in cols
    # Return DataFrame with filtered columns
    if filter_out:
        return pandas_df.loc[
            :, [c for c in pandas_df.columns if not column_filter(c)]]

    return pandas_df.loc[
        :, [c for c in pandas_df.columns if column_filter(c)]]
