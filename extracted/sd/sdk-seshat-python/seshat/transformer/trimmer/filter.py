from pandas import DataFrame
from pyspark.sql import functions as F, DataFrame as PySparkDataFrame

from seshat.general.transformer_story.base import (
    BaseTransformerStory,
    TransformerScenario,
)
from seshat.transformer.trimmer import SFrameTrimmer


class FilterTrimmer(SFrameTrimmer):
    def __init__(
        self,
        group_keys=None,
        col=None,
        op=None,
        value=None,
        conditions=None,
        combine_method="and",
    ):
        super().__init__(group_keys)
        self.col = col
        self.op = op
        self.value = value
        self.conditions = conditions if conditions else []
        self.combine_method = combine_method

        if col and op and value is not None:
            self.conditions = [{"col": col, "op": op, "value": value}]

        self.valid_operators = {
            "=": lambda df_col, val: df_col == val,
            "!=": lambda df_col, val: df_col != val,
            ">": lambda df_col, val: df_col > val,
            ">=": lambda df_col, val: df_col >= val,
            "<": lambda df_col, val: df_col < val,
            "<=": lambda df_col, val: df_col <= val,
            "in": lambda df_col, val: df_col.isin(val),
            "not in": lambda df_col, val: ~df_col.isin(val),
            "contains": lambda df_col, val: df_col.str.contains(val, na=False),
            "startswith": lambda df_col, val: df_col.str.startswith(val, na=False),
            "endswith": lambda df_col, val: df_col.str.endswith(val, na=False),
        }

        self.spark_operators = {
            "=": lambda col, val: F.col(col) == val,
            "!=": lambda col, val: F.col(col) != val,
            ">": lambda col, val: F.col(col) > val,
            ">=": lambda col, val: F.col(col) >= val,
            "<": lambda col, val: F.col(col) < val,
            "<=": lambda col, val: F.col(col) <= val,
            "in": lambda col, val: F.col(col).isin(val),
            "not in": lambda col, val: ~F.col(col).isin(val),
            "contains": lambda col, val: F.col(col).contains(val),
            "startswith": lambda col, val: F.col(col).startswith(val),
            "endswith": lambda col, val: F.col(col).endswith(val),
        }

        self._validate_conditions()

    def calculate_complexity(self):
        return 2

    def _validate_conditions(self):
        if not self.conditions:
            return

        valid_operators = list(self.valid_operators.keys())

        for condition in self.conditions:
            if not all(k in condition for k in ["col", "op", "value"]):
                raise ValueError(
                    "Each condition must have 'col', 'op', and 'value' keys"
                )

            if condition["op"] not in valid_operators:
                raise ValueError(f"Operator must be one of {valid_operators}")

            if condition["op"] in ["in", "not in"] and not isinstance(
                condition["value"], (list, tuple)
            ):
                raise ValueError(
                    f"Value for '{condition['op']}' operator must be a list or tuple"
                )

    def _apply_conditions(self, df, operators, is_spark=False):
        if not self.conditions:
            return df

        combined = None
        for condition in self.conditions:
            col = condition["col"]
            op = condition["op"]
            value = condition["value"]

            condition_func = operators[op]
            condition_result = (
                condition_func(df[col], value)
                if not is_spark
                else condition_func(col, value)
            )
            if combined is None:
                combined = condition_result
            elif self.combine_method == "and":
                combined = combined & condition_result
            else:
                combined = combined | condition_result

        if is_spark:
            return df.filter(combined)
        else:
            filtered_df = df[combined]
            filtered_df.reset_index(inplace=True, drop=True)
            return filtered_df

    def trim_df(self, default: DataFrame, *args, **kwargs):
        return {
            "default": self._apply_conditions(
                default, self.valid_operators, is_spark=False
            )
        }

    def trim_spf(self, default: PySparkDataFrame, *args, **kwargs):
        return {
            "default": self._apply_conditions(
                default, self.spark_operators, is_spark=True
            )
        }


class FilterTrimmerStory(BaseTransformerStory):
    transformer = FilterTrimmer
    use_cases = [
        "When we want to filter rows in an SFrame based on specific conditions applied to one or more columns.",
        "To remove rows that do not meet certain criteria (e.g., transactions below a certain amount, addresses not in a specific list).",
    ]
    logic_overview = "Filters SFrame rows based on specified conditions (column, operator, value) combined with 'and' or 'or'."
    steps = [
        "A 'condition' is a rule defined by a column name, an operator (like =, >, <, in), and a value.",
        "Iterate through the list of conditions.",
        "For each condition, create a filter based on the column, operator, and value.",
        "Combine all individual filters using the specified `combine_method` ('and' or 'or').",
        "Apply the combined filter to the SFrame to keep only the rows that match.",
    ]
    tags = ["trimmer", "single-sf-operation"]

    def get_scenarios(self):
        from test.transformer.trimmer.test_filter import FilterTrimmerDFTestCase

        return TransformerScenario.from_testcase(
            FilterTrimmerDFTestCase, transformer=self.transformer
        )
