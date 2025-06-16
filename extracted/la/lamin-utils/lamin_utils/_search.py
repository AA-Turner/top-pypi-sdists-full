from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from pandas import DataFrame, Series


# needed to filter out everything that doesn't contain `string`
def _contains(col: Series, string: str, case_sensitive: bool, fields_convert: dict):
    if col.name not in fields_convert:
        return [False] * len(col)
    if fields_convert[col.name]:
        col = col.astype(str)
    return col.str.contains(string, case=case_sensitive)


# apply ranking based on rules
# `string` - escaped search query,
def _ranks(
    col: Series,
    string: str,
    case_sensitive: bool,
    fields_convert: dict,
):
    if col.name not in fields_convert:
        return [0] * len(col)
    if fields_convert[col.name]:
        col = col.astype(str)
    exact_rank = col.str.fullmatch(string, case=case_sensitive) * 200
    synonym_rank = (
        col.str.match(rf"(?:^|.*\|){string}(?:\|.*|$)", case=case_sensitive) * 200
    )
    sub_rank = (
        col.str.match(
            rf"(?:^|.*[ \|\.,;:]){string}(?:[ \|\.,;:].*|$)", case=case_sensitive
        )
        * 10
    )
    startswith_rank = (
        col.str.match(rf"(?:^|.*\|){string}[^ ]*(?:\|.*|$)", case=case_sensitive) * 8
    )
    right_rank = col.str.match(rf"(?:^|.*[ \|]){string}.*", case=case_sensitive) * 2
    left_rank = col.str.match(rf".*{string}(?:$|[ \|\.,;:].*)", case=case_sensitive) * 2
    contains_rank = col.str.contains(string, case=case_sensitive).astype("int32")
    return (
        exact_rank
        + synonym_rank
        + sub_rank
        + startswith_rank
        + right_rank
        + left_rank
        + contains_rank
    )


def search(
    df: DataFrame,
    string: str,
    *,
    field: str | list[str] | None = None,
    limit: int | None = 20,
    case_sensitive: bool = False,
    _show_rank: bool = False,
) -> DataFrame:
    """Search a given string against a field.

    Args:
        df: The DataFrame to search in.
        string: The input string to match against the field values.
        field: The field or fields to search. Search all fields containing strings by default.
        limit: Maximum amount of top results to return.
        case_sensitive: Whether the match is case sensitive.

    Returns:
        A DataFrame of ranked search results.
        This DataFrame contains the matched rows from the input DataFrame,
        sorted by the match rank in descending order.

    Raises:
        KeyError: If the specified field is not found in the DataFrame.
    """
    import pandas as pd
    from pandas.api.types import is_object_dtype, is_string_dtype

    if len(df) == 0:
        return df

    fields_convert = {}
    if field is None:
        fields = df.columns.to_list()
        for f in fields:
            df_f = df[f]
            if is_object_dtype(df_f):
                fields_convert[f] = True
            elif is_string_dtype(df_f):
                fields_convert[f] = False
    else:
        fields = [field] if isinstance(field, str) else field
        for f in fields:
            fields_convert[f] = not is_string_dtype(df[f])

    string = re.escape(string)

    contains = lambda col: _contains(col, string, case_sensitive, fields_convert)
    df_contains = df.loc[df.apply(contains).any(axis=1)]
    if len(df_contains) == 0:
        return df_contains

    ranks = lambda col: _ranks(col, string, case_sensitive, fields_convert)
    rank = df_contains.apply(ranks).sum(axis=1)

    if _show_rank:
        df_contains = df_contains.copy()
        df_contains.loc[:, "rank"] = rank

    df_result = df_contains.loc[rank.sort_values(ascending=False).index]
    return df_result if limit is None else df_result.head(limit)
