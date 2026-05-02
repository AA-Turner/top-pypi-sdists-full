import asyncio
from typing import Any
from collections.abc import Callable
import pandas
from pandas import json_normalize
from ..exceptions import ComponentError, DataNotFound
from .flow import FlowComponent


class tExplode(FlowComponent):
    """
    tExplode

        Overview

            The tExplode class is a component for transforming a DataFrame by converting a column of lists or dictionaries
            into multiple rows. It supports options for dropping the original column after exploding, and for expanding
            nested dictionary structures into separate columns.

        :widths: auto

            | column           |   Yes    | The name of the column to explode into multiple rows.                                     |
            | drop_original    |   No     | Boolean indicating if the original column should be dropped after exploding.              |
            | explode_dataset  |   No     | Boolean specifying if nested dictionaries in the column should be expanded as new columns.|
            | advanced_mode    |   No     | Boolean enabling enhanced features: preserve empty lists, propagate parent columns.      |
            | propagate_columns|   No    | List of column names to propagate from parent to child rows (only in advanced_mode).   |

        Returns

            This component returns a DataFrame with the specified column exploded into multiple rows. If `explode_dataset` is
            set to True and the column contains dictionaries, these are expanded into new columns. Metrics on the row count
            after explosion are recorded, and any errors encountered during processing are logged and raised as exceptions.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tExplode:
          column: reviews
          drop_original: false
          advanced_mode: true
          propagate_columns: ["id", "name"]
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
        self.data: Any = None
        # Column to be exploded
        self.column: str = kwargs.pop("column", None)
        self.drop_original: bool = kwargs.pop("drop_original", False)
        # Useful when exploded column is also composed of dictionary, the dictionary
        # is also exploded as columns
        self.explode_dataset: bool = kwargs.pop("explode_dataset", True)
        # Enhanced mode flag for advanced features
        self.advanced_mode: bool = kwargs.pop("advanced_mode", False)
        # List of columns to propagate from parent to child rows (only in advanced_mode)
        self.propagate_columns: list = kwargs.pop("propagate_columns", [])
        super(tExplode, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        # Si lo que llega no es un DataFrame de Pandas se cancela la tarea
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("Data Not Found", status=404)
        if not isinstance(self.data, pandas.DataFrame):
            raise ComponentError("Incompatible Pandas Dataframe", status=404)
        return True

    async def run(self):
        args = {}
        if self.data.empty:
            raise DataNotFound("Data Was Not Found on Dataframe 1")

        try:
            if self.advanced_mode:
                # Enhanced mode with advanced features
                if self.explode_dataset is True:
                    # 1. Add a helper column to track the parent index
                    self.data['_parent_idx'] = self.data.index
                    
                    # 2. Identify rows to explode (non-empty lists)
                    to_explode = self.data[self.data[self.column].apply(lambda x: isinstance(x, list) and len(x) > 0)]

                    # 3. Explode only the rows with non-empty lists
                    exploded_df = to_explode.explode(self.column).reset_index(drop=True)
                    parent_idx_for_child = exploded_df['_parent_idx']
                    
                    # 4. Normalize the exploded column to expand the dictionaries into columns
                    valid_items = exploded_df[self.column].dropna()
                    normalized_df = pandas.json_normalize(valid_items)
                    normalized_df.index = valid_items.index # Align index for update

                    # 5. Build the set of all columns from parent and JSON
                    parent_columns = set(self.data.columns) - {'_parent_idx'}
                    json_columns = set(normalized_df.columns)
                    all_columns = sorted(parent_columns | json_columns)

                    # 6. For each column, assign values explicitly for child rows
                    child_idx = normalized_df.index
                    # Ensure all columns exist in both DataFrames
                    for col in all_columns:
                        if col not in exploded_df.columns:
                            exploded_df[col] = None
                    # Assign values for child rows
                    for col in all_columns:
                        if col in normalized_df.columns:
                            exploded_df.loc[child_idx, col] = normalized_df[col]
                        else:
                            # If propagate_columns is set and col is in it, propagate from parent
                            if self.propagate_columns and col in self.propagate_columns:
                                for idx in child_idx:
                                    parent_row_idx = parent_idx_for_child.loc[idx]
                                    parent_value = self.data.loc[parent_row_idx, col] if col in self.data.columns else None
                                    exploded_df.at[idx, col] = parent_value
                            else:
                                exploded_df.loc[child_idx, col] = None
                    # Assign None for child rows in columns only present in JSON but not in parent
                    for col in json_columns - parent_columns:
                        exploded_df.loc[child_idx, col] = exploded_df.loc[child_idx, col] if col in exploded_df.columns else None

                    # 7. Remove the helper column before returning the result
                    if '_parent_idx' in exploded_df.columns:
                        exploded_df = exploded_df.drop(columns=['_parent_idx'])
                    if '_parent_idx' in self.data.columns:
                        self.data = self.data.drop(columns=['_parent_idx'])

                    # 8. Concatenate the original DataFrame (parents) and the exploded DataFrame (children)
                    df = pandas.concat([self.data, exploded_df], ignore_index=True)

                    if self.drop_original:
                        df = df.drop(columns=[self.column])
                else:
                    df = self.data.explode(self.column).reset_index(drop=True)
            else:
                # Original behavior (default)
                # Step 1: Explode the 'field' column
                exploded_df = self.data.explode(self.column)
                # Reset index to ensure it's unique
                exploded_df = exploded_df.reset_index(drop=True)
                if self.explode_dataset is True:
                    # Step 2: Normalize the JSON data in 'exploded' col
                    # This will create a new DataFrame where each dictionary key becomes a column
                    data_df = json_normalize(exploded_df[self.column])
                    # Step 3: Concatenate with the original DataFrame
                    # Drop the original column from exploded_df and join with data_df
                    if self.drop_original is True:
                        exploded_df.drop(self.column, axis=1)
                    df = pandas.concat([exploded_df, data_df], axis=1)
                else:
                    df = exploded_df

        except Exception as err:
            raise ComponentError(f"Error processing Dataframe in tExplode: {err}") from err
        
        numrows = len(df.index)
        if numrows == 0:
            raise DataNotFound("tExplode: Result is an empty Dataframe")
        
        if hasattr(self, "index"):
            if 'id' in df.columns:
                df[self.index] = df["id"]
                df.drop("id", axis="columns", inplace=True)

        self._variables[f"{self.StepName}_NUMROWS"] = numrows
        self.add_metric("EXPLODE: ", numrows)
        df.is_copy = None
        print(df)
        self._result = df
        if self._debug is True:
            print("::: Printing Column Information === ")
            for column, t in df.dtypes.items():
                print(column, "->", t, "->", df[column].iloc[0])
        return self._result

    async def close(self):
        pass
