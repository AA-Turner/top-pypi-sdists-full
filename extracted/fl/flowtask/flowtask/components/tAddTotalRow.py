import asyncio
from collections.abc import Callable
import pandas as pd
from ..exceptions import ComponentError, ConfigError
from .flow import FlowComponent


class tAddTotalRow(FlowComponent):
    """
    tAddTotalRow

    Overview
        Adds a 'Total' row to a DataFrame by:
        1. Summing all numeric columns
        2. Calculating weighted averages for specified columns
        3. Setting a label column to 'Total'

    Properties:
        label_column (str, required): Column to set as 'Total' (e.g., 'account_name')
        weighted_avg_columns (list, optional): Columns to calculate weighted average instead of sum
        weight_column (str, optional): Column to use as weight for weighted averages

    Example:
        - tAddTotalRow:
            label_column: account_name
            weighted_avg_columns:
              - pre_conversion
              - post_conversion
              - lift_perc
            weight_column: sales_weighted_sum_pre

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tAddTotalRow:
          # attributes here
        ```
    """
    _version = "1.0.0"

    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ):
        """Init Method."""
        self.label_column = kwargs.pop("label_column", None)
        self.weighted_avg_columns = kwargs.pop("weighted_avg_columns", [])
        self.weight_column = kwargs.pop("weight_column", None)

        if not self.label_column:
            raise ConfigError("label_column is required")

        if self.weighted_avg_columns and not self.weight_column:
            raise ConfigError("weight_column is required when using weighted_avg_columns")

        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found")
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError("Incompatible Pandas Dataframe")
        return True

    async def close(self):
        pass

    async def run(self):
        try:
            df = self.data.copy()

            # Calculate sum of all numeric columns
            tot_row = pd.DataFrame(df.sum(numeric_only=True)).T

            # Calculate weighted averages for specified columns
            if self.weighted_avg_columns and self.weight_column:
                for col in self.weighted_avg_columns:
                    if col in df.columns and self.weight_column in df.columns:
                        # Weighted average: sum(col * weight) / sum(weight)
                        weighted_sum = (df[col] * df[self.weight_column]).sum()
                        weight_sum = df[self.weight_column].sum()
                        tot_row[col] = weighted_sum / weight_sum if weight_sum != 0 else 0

            # Set label column to 'Total'
            tot_row[self.label_column] = 'Total'

            # Concatenate total row to dataframe
            result = pd.concat([df, tot_row], ignore_index=True)

            if self._debug:
                print("=== tAddTotalRow Debug ===")
                print(f"Label column: {self.label_column}")
                print(f"Weighted avg columns: {self.weighted_avg_columns}")
                print(f"Weight column: {self.weight_column}")
                print(f"Total row:\n{tot_row}")
                print(f"Result shape: {df.shape} → {result.shape}")

            self._result = result
            return self._result

        except Exception as err:
            raise ComponentError(f"Error in tAddTotalRow: {err}") from err
