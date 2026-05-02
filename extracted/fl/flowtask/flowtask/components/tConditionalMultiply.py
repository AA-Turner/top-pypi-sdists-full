import asyncio
from collections.abc import Callable
import pandas as pd
import numpy as np
from ..exceptions import ComponentError, ConfigError
from .flow import FlowComponent


class tConditionalMultiply(FlowComponent):
    """
    tConditionalMultiply

        Overview

            The tConditionalMultiply component multiplies specified columns by a weight column, but only
            when a condition is met. This is useful for applying adjustments, weights, or scaling factors
            to specific subsets of data while leaving other rows unchanged.

        :widths: auto

            | condition_column |   Yes    | Column to evaluate the condition on (e.g., "period").                                     |
            | condition_value  |   Yes    | Value that triggers the multiplication (e.g., "pre").                                     |
            | columns_to_multiply |  Yes  | List of column names to multiply when condition is met.                                   |
            | multiplier_column|   Yes    | Column containing the multiplication factor (e.g., "weight").                             |
            | suffix           |   No     | Suffix for new column names. Defaults to "_weighted".                                     |
            | replace_original |   No     | If True, replaces original columns instead of creating new ones. Defaults to False.      |

        Returns

            This component returns the DataFrame with new weighted columns (or modified originals if replace_original=True).
            Rows that don't meet the condition get the original value copied.

        Example:


        This creates `sales_weighted` and `foottraffic_weighted` columns where:
        - If period == "pre": sales_weighted = sales * weight
        - If period != "pre": sales_weighted = sales (unchanged)

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          - tConditionalMultiply:
          condition_column: period
          condition_value: "pre"
          columns_to_multiply:
          - sales
          - foottraffic
          multiplier_column: weight
          suffix: "_weighted"
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
        self.condition_column: str = kwargs.pop("condition_column", None)
        self.condition_value = kwargs.pop("condition_value", None)
        self.columns_to_multiply: list = kwargs.pop("columns_to_multiply", [])
        self.multiplier_column: str = kwargs.pop("multiplier_column", None)
        self.suffix: str = kwargs.pop("suffix", "_weighted")
        self.replace_original: bool = kwargs.pop("replace_original", False)

        if not self.condition_column:
            raise ConfigError("tConditionalMultiply requires 'condition_column' parameter")
        if self.condition_value is None:
            raise ConfigError("tConditionalMultiply requires 'condition_value' parameter")
        if not self.columns_to_multiply:
            raise ConfigError("tConditionalMultiply requires 'columns_to_multiply' parameter")
        if not self.multiplier_column:
            raise ConfigError("tConditionalMultiply requires 'multiplier_column' parameter")

        super(tConditionalMultiply, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found")
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError("Incompatible Pandas Dataframe")

        # Validate columns exist
        if self.condition_column not in self.data.columns:
            raise ComponentError(f"Column '{self.condition_column}' not found in DataFrame")
        if self.multiplier_column not in self.data.columns:
            raise ComponentError(f"Column '{self.multiplier_column}' not found in DataFrame")
        for col in self.columns_to_multiply:
            if col not in self.data.columns:
                raise ComponentError(f"Column '{col}' not found in DataFrame")

        return True

    async def close(self):
        pass

    async def run(self):
        try:
            df = self.data.copy()

            # Create condition mask
            condition_mask = df[self.condition_column] == self.condition_value

            # Apply multiplication for each column
            for col in self.columns_to_multiply:
                if self.replace_original:
                    # Replace original column
                    df[col] = np.where(
                        condition_mask,
                        df[col] * df[self.multiplier_column],
                        df[col]
                    )
                else:
                    # Create new column with suffix
                    new_col = f"{col}{self.suffix}"
                    df[new_col] = np.where(
                        condition_mask,
                        df[col] * df[self.multiplier_column],
                        df[col]
                    )

            # Metrics
            rows_modified = condition_mask.sum()
            self.add_metric("rows_modified", int(rows_modified))
            self.add_metric("rows_unchanged", int((~condition_mask).sum()))
            self.add_metric("columns_created", len(self.columns_to_multiply) if not self.replace_original else 0)

            if self._debug:
                print(f"=== tConditionalMultiply Debug ===")
                print(f"Condition: {self.condition_column} == '{self.condition_value}'")
                print(f"Rows matching condition: {rows_modified}")
                print(f"Columns multiplied: {self.columns_to_multiply}")
                print(f"Multiplier column: {self.multiplier_column}")
                if not self.replace_original:
                    new_cols = [f"{col}{self.suffix}" for col in self.columns_to_multiply]
                    print(f"New columns created: {new_cols}")

            self._result = df
            return df

        except Exception as err:
            raise ComponentError(f"Error in tConditionalMultiply: {err}") from err
