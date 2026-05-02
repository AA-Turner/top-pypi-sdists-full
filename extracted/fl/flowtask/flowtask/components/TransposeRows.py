import asyncio
from collections.abc import Callable
import pandas as pd
import numpy as np
from ..exceptions import ComponentError
from .flow import FlowComponent


class TransposeRows(FlowComponent):
    """
    TransposeRows

     Overview

         The TransposeRows class is a component for transposing specified rows in a DataFrame by converting row values
         into new columns based on pivot settings. This component supports options for preserving the original data,
         handling empty results, and custom column configurations for the transposition.

        :widths: auto

         | pivot            |   Yes    | List of columns to use as the pivot index for transposition.              |
         | columns          |   Yes    | Dictionary mapping row values to their target column names.               |
         | preserve_original|   No     | Boolean indicating if the original rows should be preserved.              |
         | allow_empty      |   No     | Boolean indicating if empty columns should be allowed in the output.      |

     Returns

         This component returns a DataFrame with specified rows transposed into columns according to the provided pivot
         and column configurations. If `preserve_original` is set to False, the original rows used in transposition
         are removed. Any errors in column mapping or pivoting are raised with descriptive error messages.


         Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          TransposeRows:
          column: column_name
          value: data
          pivot:
          - formid
          - form_id
          - orgid
          preserve_original: true
          allow_empty: true
          columns:
          '000_001': ad_hoc
          '000_003': creation_timestamp
          '000_004': user_device
          000_008: geoloc
          000_009: visit_length
          '000_012': store_name
          '000_013': store_id
          '000_023': account_name
          '000_024': store_designation
          '000_026': region_name
          000_029: store_timezone
          '000_037': visitor_username
          000_038: visitor_name
          000_039: visitor_email
          '000_045': visitor_role
          '000_055': updated_timestamp
          '000_065': activity_item_id
          '000_063': time_in
          '000_064': time_out
          '000_066': position_id
          '000_067': position_manager
          '000_070': visit_status
          '194834': retailer
          VisitDateLocal: visit_timestamp
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
        self._pivot: list = kwargs.pop("pivot")
        self.preserve: bool = kwargs.pop("preserve_original", False)
        self.allow_empty: bool = kwargs.pop("allow_empty", False)
        if not self._pivot:
            raise ComponentError("Missing List of Pivot Columns")
        # columns to be transposed:
        # TODO: if not, then all columns not in Pivot list.
        self._columns = kwargs.pop("columns")
        super(TransposeRows, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found", status=404)
        if not isinstance(self.data, pd.DataFrame):
            raise ComponentError("Transpose: Incompatible Pandas Dataframe", status=404)
        if not hasattr(self, "column"):
            raise ComponentError(
                "Transpose: Missing Column name for extracting row values"
            )
        if not hasattr(self, "value"):
            raise ComponentError("Transpose: Missing Column for Values")
        return True

    async def close(self):
        pass

    def row_to_column(self, df: pd.DataFrame, row_to_pivot: str, new_name: str):
        """
        Add a pivoted column to the dataframe based on the given column name.

        Parameters:
        - df: The input dataframe.
        - row_to_pivot: The column name to be pivoted.
        - new_name: The name of the column to be transposed.

        Returns:
        - Dataframe with the new pivoted column.
        """
        # Filter the dataframe to only include rows with the desired column_name
        df_filtered = df[df[self.column] == row_to_pivot]
        if df_filtered.empty is True:
            # there is no data to be filtered:
            if self.allow_empty is True:
                df[new_name] = np.nan
            return df
        # Pivot the filtered dataframe
        df_pivot = df_filtered.pivot_table(
            index=self._pivot,
            columns=self.column,
            values=self.value,
            aggfunc="first",
            dropna=False,  # Preserve NaN values
        ).reset_index()
        df_pivot = df_pivot.rename(columns={row_to_pivot: new_name})
        # Merge the pivoted dataframe with the original dataframe
        df_merged = pd.merge(df, df_pivot, on=self._pivot, how="left")
        if self.preserve is False:
            # Drop the original column_name and value columns for the pivoted rows
            df_merged = df_merged.drop(
                df_merged[(df_merged[self.column] == row_to_pivot)].index
            )
        return df_merged

    async def run(self):
        try:
            df = self.data
            for column, value in self._columns.items():
                try:
                    df_pivot = self.row_to_column(df, column, value)
                except Exception as err:
                    print(err)
                df = df_pivot
            if self._debug is True:
                print("=== TRANSPOSE ===")
                print(" = Data Types: = ")
                print(df.dtypes)
                print("::: Printing Column Information === ")
                for column, t in df.dtypes.items():
                    print(column, "->", t, "->", df[column].iloc[0])
            self._result = df
            return self._result
        except (ValueError, KeyError) as err:
            raise ComponentError(f"Crosstab Error: {err!s}") from err
        except Exception as err:
            raise ComponentError(f"Unknown error {err!s}") from err
