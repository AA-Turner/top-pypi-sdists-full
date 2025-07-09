import operator
from functools import reduce
from typing import Any, Iterable

from pandas import DataFrame, Series

OverwriteRule = dict[str, dict[str, str] | dict[str, Any]]


def rule(key: str, operator: str, value: str) -> dict[str, str]:
    return {
        "key": key,
        "operator": operator,
        "value": value,
    }


def overwrite(**overwrites) -> dict[str, Any]:
    return {**overwrites}


def overwrite_rule(key: str, operator: str, value: str, **overwrites) -> OverwriteRule:
    return {
        "rule": rule(key, operator, value),
        "overwrite": overwrite(**overwrites),
    }


def overwrite_row(fields: Iterable[OverwriteRule] | None = None) -> dict[str, list[OverwriteRule]]:
    overwrites_dict = {}

    if fields:
        overwrites_dict["fields"] = [*fields]

    return overwrites_dict


def overwrite_row_df(df: DataFrame, row_cond, fields: Iterable[OverwriteRule]):
    df.loc[row_cond, "_overwrites"] = [{"fields": fields}]


def override_number_to_percent(df: DataFrame, *conditions, filter_operator=operator.or_):
    reduced_conditions = reduce(filter_operator, conditions)

    df.loc[reduced_conditions, "_overwrites"] = [
        {
            "fields": [
                overwrite_rule(
                    key="type",
                    operator="=",
                    value="number",
                    decorators=[{"position": "right", "value": "%"}],
                    precision=1,
                    display_mode="decimal",
                )
            ]
        }
    ] * reduced_conditions.sum()


def override_number_with_currency(df: DataFrame, currency: str, *conditions, filter_operator=operator.or_):
    reduced_conditions = reduce(filter_operator, conditions)

    df.loc[reduced_conditions, "_overwrites"] = [
        {
            "fields": [
                overwrite_rule(
                    key="type",
                    operator="=",
                    value="number",
                    decorators=[{"position": "left", "value": currency}],
                )
            ]
        }
    ] * reduced_conditions.sum()


def override_number_to_x(df: DataFrame, *conditions, filter_operator=operator.or_):
    reduced_conditions = reduce(filter_operator, conditions)

    df.loc[reduced_conditions, "_overwrites"] = [
        {
            "fields": [
                overwrite_rule(
                    key="type",
                    operator="=",
                    value="number",
                    decorators=[{"position": "right", "value": "x"}],
                    precision=1,
                    display_mode="decimal",
                )
            ]
        }
    ] * reduced_conditions.sum()


def override_number_precision(df: DataFrame, precision=2, *conditions, filter_operator=operator.or_):
    reduced_conditions = reduce(filter_operator, conditions)

    df.loc[reduced_conditions, "_overwrites"] = [
        {
            "fields": [
                overwrite_rule(
                    key="type",
                    operator="=",
                    value="number",
                    precision=precision,
                )
            ]
        }
    ] * reduced_conditions.sum()


def override_number_to_decimal(df: DataFrame, *conditions, filter_operator=operator.or_):
    reduced_conditions = reduce(filter_operator, conditions)

    df.loc[reduced_conditions, "_overwrites"] = [
        {
            "fields": [
                overwrite_rule(
                    key="type",
                    operator="=",
                    value="number",
                    precision=0,
                    displayMode="decimal",
                )
            ]
        }
    ] * reduced_conditions.sum()


def override_number_to_integer_without_decorations(df: DataFrame, *conditions, filter_operator=operator.or_):
    reduced_conditions = reduce(filter_operator, conditions)

    df.loc[reduced_conditions, "_overwrites"] = [
        {
            "fields": [
                overwrite_rule(
                    key="type",
                    operator="=",
                    value="number",
                    precision=0,
                    displayMode="decimal",
                    disable_formatting=True,
                )
            ]
        }
    ] * reduced_conditions.sum()


def pct_change_with_negative_values(df: DataFrame, field: str) -> DataFrame:
    """Calculate percentage change with negative values"""
    return df[field].diff() / df[field].abs().shift()


def get_empty_series(df: DataFrame) -> Series:
    """Return empty Series with the same index as the DataFrame"""
    return Series(dtype="float64", index=df.index)


def sanitize_field(df: DataFrame, field: str):
    """Ensure field exists in DataFrame"""
    empty_series = get_empty_series(df)
    df[field] = df.get(field, empty_series)


def sanitize_fields(df: DataFrame, fields: Iterable[str]):
    """Ensure fields exist in DataFrame"""
    for field in fields:
        sanitize_field(df, field)
