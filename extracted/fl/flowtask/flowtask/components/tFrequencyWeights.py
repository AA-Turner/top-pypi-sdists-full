import asyncio
from collections.abc import Callable
import pandas as pd
from ..exceptions import ComponentError, ConfigError
from .flow import FlowComponent


class tFrequencyWeights(FlowComponent):
    """
    tFrequencyWeights

        Overview

            The tFrequencyWeights component calculates frequency-based weights for values in a specific column
            within a specified group. This is useful for seasonality adjustments, where you want to weight
            values based on how frequently they occur in a reference period.

        :widths: auto

            | group_column     |   Yes    | Column that defines the group to analyze (e.g., "period").                                |
            | group_value      |   Yes    | Value of the group to calculate frequencies from (e.g., "post").                          |
            | weight_by        |   Yes    | Column to calculate frequencies for (e.g., "month").                                      |
            | weight_column    |   No     | Name of the output weight column. Defaults to "weight".                                   |
            | year_column      |   No     | Optional year column to account for same values in different years.                       |

        Returns

            This component returns the DataFrame with a new weight column added. Each row gets a weight
            indicating how many times its weight_by value appears in the specified group.

        Example:


        If March appears 3 times in the "post" period, all rows with month=3 will get weight=3.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          - tFrequencyWeights:
          group_column: period
          group_value: "post"
          weight_by: month
          weight_column: weight
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
        self.group_column: str = kwargs.pop("group_column", None)
        self.group_value: str = kwargs.pop("group_value", None)
        self.weight_by: str = kwargs.pop("weight_by", None)
        self.weight_column: str = kwargs.pop("weight_column", "weight")
        self.year_column: str = kwargs.pop("year_column", None)

        if not self.group_column:
            raise ConfigError("tFrequencyWeights requires 'group_column' parameter")
        if not self.group_value:
            raise ConfigError("tFrequencyWeights requires 'group_value' parameter")
        if not self.weight_by:
            raise ConfigError("tFrequencyWeights requires 'weight_by' parameter")

        super(tFrequencyWeights, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found")
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError("Incompatible Pandas Dataframe")

        # Validate columns exist
        if self.group_column not in self.data.columns:
            raise ComponentError(f"Column '{self.group_column}' not found in DataFrame")
        if self.weight_by not in self.data.columns:
            raise ComponentError(f"Column '{self.weight_by}' not found in DataFrame")
        if self.year_column and self.year_column not in self.data.columns:
            raise ComponentError(f"Column '{self.year_column}' not found in DataFrame")

        return True

    async def close(self):
        pass

    async def run(self):
        try:
            # Filter data to the specified group
            group_data = self.data[self.data[self.group_column] == self.group_value].copy()

            if len(group_data) == 0:
                raise ComponentError(
                    f"No rows found for {self.group_column}='{self.group_value}'"
                )

            # Calculate frequencies
            if self.year_column:
                # Count occurrences of weight_by value per year, then count how many years
                # Example: March appears in 2024 and 2025, so it has frequency 2
                freq_by_year = (
                    group_data.groupby([self.year_column, self.weight_by])
                    .size()
                    .reset_index(name='_tmp_count')
                )
                frequencies = (
                    freq_by_year.groupby(self.weight_by)
                    .size()
                    .reset_index(name=self.weight_column)
                )
            else:
                # Simple frequency count
                frequencies = (
                    group_data.groupby(self.weight_by)
                    .size()
                    .reset_index(name=self.weight_column)
                )

            # Merge weights back to original dataframe
            df_result = self.data.merge(frequencies, on=self.weight_by, how='left')

            # Fill NaN weights with 1 (for values that don't appear in the group)
            df_result[self.weight_column] = df_result[self.weight_column].fillna(1).astype('Int64')

            # Metrics
            self.add_metric("unique_values", len(frequencies))
            self.add_metric("weight_column", self.weight_column)

            if self._debug:
                print(f"=== tFrequencyWeights Debug ===")
                print(f"Group: {self.group_column}='{self.group_value}'")
                print(f"Calculating frequencies for: {self.weight_by}")
                print(f"\nFrequency distribution:")
                print(frequencies.to_string())

            self._result = df_result
            return df_result

        except Exception as err:
            raise ComponentError(f"Error in tFrequencyWeights: {err}") from err
