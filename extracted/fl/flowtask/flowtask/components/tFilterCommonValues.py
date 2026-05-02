import asyncio
from collections.abc import Callable
import pandas as pd
from ..exceptions import ComponentError, ConfigError
from .flow import FlowComponent


class tFilterCommonValues(FlowComponent):
    """
    tFilterCommonValues

        Overview

            The tFilterCommonValues component filters a DataFrame to keep only rows where a specific column's values
            appear in ALL specified groups. This is useful for finding common elements across different categories,
            such as months that exist in both "pre" and "post" periods, or products available in all regions.

        :widths: auto

            | group_column     |   Yes    | Column that defines the groups to compare (e.g., "period").                               |
            | value_column     |   Yes    | Column containing values to check for commonality (e.g., "month").                        |
            | groups           |   Yes    | List of group values to compare (e.g., ["pre", "post"]).                                 |

        Returns

            This component returns a filtered DataFrame containing only rows where the value_column values
            exist in ALL specified groups. Metrics on filtered row counts are recorded.

        Example:


        This will keep only rows where the month appears in both "pre" and "post" periods.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          - tFilterCommonValues:
          group_column: period
          value_column: month
          groups: ["pre", "post"]
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
        self.value_column: str = kwargs.pop("value_column", None)
        self.groups: list = kwargs.pop("groups", [])

        if not self.group_column:
            raise ConfigError("tFilterCommonValues requires 'group_column' parameter")
        if not self.value_column:
            raise ConfigError("tFilterCommonValues requires 'value_column' parameter")
        if not self.groups or len(self.groups) < 2:
            raise ConfigError("tFilterCommonValues requires at least 2 groups to compare")

        super(tFilterCommonValues, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

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
        if self.value_column not in self.data.columns:
            raise ComponentError(f"Column '{self.value_column}' not found in DataFrame")

        return True

    async def close(self):
        pass

    async def run(self):
        try:
            initial_rows = len(self.data)

            # Find unique values for each group
            common_values = None

            for group in self.groups:
                # Get unique values for this group
                group_values = set(
                    self.data[self.data[self.group_column] == group][self.value_column].unique()
                )

                if common_values is None:
                    common_values = group_values
                else:
                    # Intersect with previous groups
                    common_values = common_values.intersection(group_values)

            # Filter dataframe to keep only rows with common values
            df_filtered = self.data[self.data[self.value_column].isin(common_values)].reset_index(drop=True)

            # Metrics
            self.add_metric("initial_rows", initial_rows)
            self.add_metric("filtered_rows", len(df_filtered))
            self.add_metric("common_values_count", len(common_values))
            self.add_metric("removed_rows", initial_rows - len(df_filtered))

            if self._debug:
                print(f"=== tFilterCommonValues Debug ===")
                print(f"Groups compared: {self.groups}")
                print(f"Common {self.value_column} values: {sorted(common_values)}")
                print(f"Rows: {initial_rows} → {len(df_filtered)} (removed {initial_rows - len(df_filtered)})")

            self._result = df_filtered
            return df_filtered

        except Exception as err:
            raise ComponentError(f"Error in tFilterCommonValues: {err}") from err
