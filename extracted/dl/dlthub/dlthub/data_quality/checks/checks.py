"""Off-the-shelf data quality checks"""

from __future__ import annotations
from collections.abc import Collection
from typing import Any, Sequence

import sqlglot
from sqlglot import exp as sge

from dlthub.data_quality.checks._base import LazyCheck


__all__ = (
    "is_unique",
    "is_in",
    "is_not_null",
    "is_primary_key",
    "case",
)


def _build_case_from_condition(
    condition: sge.ExpOrStr, *, true_is_success: bool = True
) -> sge.Case:
    return (
        sge.case()
        .when(condition=condition, then=sge.Boolean(this=true_is_success))
        .else_(sge.Boolean(this=not true_is_success))
    )


class is_unique(LazyCheck):
    """Check if value for column `{column}` is unique."""

    version: int = 1

    def __init__(self, column: str):
        self._arguments = dict(column=column)

    # TODO could write expression using `:param` notation or `sqlglot.expressions.Placeholder`
    # to have named parameters in the SQL template to be filled later
    # sqlglot.parse_one("COUNT(*) OVER (PARTITION BY :column) > 1")
    # GT(
    #   this=Window(
    #     this=Count(
    #       this=Star(),
    #       big_int=True),
    #     partition_by=[
    #       Placeholder(this=column)],
    #     over=OVER),
    #   expression=Literal(this=1, is_string=False))
    @property
    def expr(self) -> sge.Expression:
        condition = f"COUNT(*) OVER (PARTITION BY {self.arguments['column']}) > 1"
        return _build_case_from_condition(condition, true_is_success=False)


class is_not_null(LazyCheck):
    """Check if value for column `{column}` is not null."""

    version: int = 1

    def __init__(self, column: str):
        self._arguments = dict(column=column)

    @property
    def expr(self) -> sge.Expression:
        condition = f"{self.arguments['column']} IS NULL"
        return _build_case_from_condition(condition, true_is_success=False)


# NOTE at the column-level, this is pass or fail. It can't be thresholed
class is_primary_key(LazyCheck):
    """Check if `{columns}` constitute a valid primary key.

    To be a valid primary key, one or more columns need to be unique and not null.
    This checks the validity of the primary key, not if it's actually implemented
    as a primary key on the destination.
    """

    version: int = 1

    def __init__(self, columns: str | Sequence[str]) -> None:
        columns = [columns] if isinstance(columns, str) else columns
        self._arguments = dict(columns=columns)

    @property
    def expr(self) -> sge.Expression:
        # TODO parameterize
        sql = """
        CASE
            WHEN value IS NULL OR _dlt_id IS NULL THEN 0
            WHEN COUNT(*) OVER (PARTITION BY value, _dlt_id) > 1 THEN 0
            ELSE 1
        END
        """
        return sqlglot.parse_one(sql.format(**self.arguments))


class is_in(LazyCheck):
    """Check if `{column}` values are IN `{values}`."""

    version: int = 1

    # use more specific type annotation than `Any`
    def __init__(self, column: str, values: Collection[Any], true_is_success: bool = True):
        self._arguments = dict(column=column, values=values, true_is_success=true_is_success)

    @property
    def qualified_name(self) -> str:
        # NOTE it's doesn't make much sense to stack multiple `is_in()` check for the same column
        # therefore, it simplifies namespacing needs
        return f"{self._arguments['column']}__is_in"

    @property
    def expr(self) -> sge.Expression:
        condition = f"{self.arguments['column']} IN {tuple(self.arguments['values'])}"
        return _build_case_from_condition(condition)


class case(LazyCheck):
    """User-defined `CASE` check.

    {condition}
    """

    version: int = 1

    def __init__(self, condition: str, true_is_success: bool = True) -> None:
        self._arguments = dict(condition=condition, true_is_success=true_is_success)

    @property
    def expr(self) -> sge.Expression:
        return _build_case_from_condition(
            self.arguments["condition"],
            true_is_success=self.arguments["true_is_success"],
        )

    @property
    def qualified_name(self) -> str:
        # TODO find solution to generate qualified name; could be user kwarg
        columns = self.expr.find_all(sge.Column)
        condition_type = type(list(self.expr.find_all(sge.If))[0].this).__name__
        return "__".join([str(col) for col in columns]) + f"__case__{condition_type}"
