import asyncio
from typing import Any, Union
from collections.abc import Callable
import pandas
from pandas import DataFrame
from asyncdb.exceptions import NoDataFound
from ..exceptions import ComponentError, DataNotFound
from .flow import FlowComponent


class tJoin(FlowComponent):
    """
    tJoin

    Overview

        The tJoin class is a component for joining two Pandas DataFrames based on specified join conditions. It supports various join types
        (such as left, right, inner, and outer joins) and handles different scenarios like missing data, custom join conditions, and multi-source joins.

    :widths: auto

        | df1              |   Yes    | The left DataFrame to join.                                                                       |
        | df2              |   Yes    | The right DataFrame to join.                                                                      |
        | type             |   No     | "left"    | The type of join to perform. Supported values are "left", "right", "inner",           |
        |                  |          |           | "outer", and "anti-join". When "anti-join" is used, it returns the difference         |
        |                  |          |           | of B - A, i.e., all rows present in df1 but not in df2.                               |
        | depends          |   Yes    | A list of dependencies defining the sources for the join.                                         |
        | operator         |   No     | The logical operator to use for join conditions, defaults to "and".                               |
        | fk               |   No     | The foreign key or list of keys to use for joining DataFrames.                                    |
        | no_copy          |   No     | A flag indicating if copies of the DataFrames should not be made, defaults to True.               |
        | join_with        |   No     | A list of additional keys to use for join conditions.                                             |

    Return

        The methods in this class manage the joining of two Pandas DataFrames, including initialization, execution, and result handling.
        It ensures proper handling of temporary columns and provides metrics on the joined rows.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tJoin:
          depends:
          - TransformRows_2
          - QueryToPandas_3
          type: left
          fk:
          - store_number
          args:
          validate: many_to_many
        ```
    """
    _version = "1.0.0"
    def __init__(
        self,
        loop: asyncio.AbstractEventLoop = None,
        job: Callable = None,
        stat: Callable = None,
        **kwargs,
    ) -> None:
        """Init Method."""
        self.type: str = "left"
        self.df1: Union[DataFrame, Any] = None
        self.df2: Union[DataFrame, Any] = None
        super(tJoin, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        if not hasattr(self, "depends"):
            raise ComponentError(
                "Missing Dependency (depends) Attribute for declaring Sources."
            )
        if self._multi:
            try:
                self.df1 = self.previous[0].output()
            except IndexError as ex:
                name = self.depends[0]
                raise ComponentError(f"Missing LEFT Dataframe: {name}") from ex
            try:
                self.df2 = self.previous[1].output()
            except IndexError as ex:
                name = self.depends[1]
                raise ComponentError("Missing RIGHT Dataframe") from ex
        elif hasattr(self, "left"):
            # TODO: this not work:
            # think in a persistent structure to save every component after
            # execution, to get later
            # discover the "Left" Table
            try:
                _, num = self.left.split("_")
                left = self.JobTask.getJobByID(int(num) - 1)
                self.df1 = left["component"].output()
            except KeyError as ex:
                raise DataNotFound(f"Failed Left Task name: {self.left}") from ex
        elif hasattr(self, "right"):
            # discover the "Left" Table
            try:
                _, num = self.right.split("_")
                right = self.JobTask.getJobByID(int(num) - 1)
                self.df2 = right["component"].output()
            except KeyError as ex:
                raise DataNotFound(f"Failed Right Task name: {self.right}") from ex
        else:
            raise DataNotFound("Data Was Not Found for Join", status=404)
        return True

    def cleanup_temp_rows(self, df: pandas.DataFrame = None) -> None:
        try:
            self.df1.drop(['_tmp_key_df1'], axis=1, inplace=True)
            self.df2.drop(['_tmp_key_df2'], axis=1, inplace=True)
        except KeyError:
            pass
        if df is not None:
            df.is_copy = None
            # Remember to drop the temporary columns before finalizing the dataframe
            df.drop(
                ['_tmp_key_df1', '_tmp_key_df2'],
                axis=1,
                inplace=True
            )

    async def run(self):
        args = {}
        if self.df1 is None:
            raise DataNotFound("Main data Not Found for Join", status=404)
        if self.df1.empty:
            raise DataNotFound("Data Was Not Found on Dataframe 1", status=404)
        if self.type == "left" and (self.df2 is None or self.df2.empty):
            self._result = self.df1
            return True
        elif self.df2 is None or self.df2.empty:
            raise DataNotFound("Data Was Not Found on Dataframe 2", status=404)
        if hasattr(self, "no_copy"):
            args["copy"] = self.no_copy
        if not self.type:
            self.type = "inner"
            args["left_index"] = True
        if hasattr(self, "args") and isinstance(self.args, dict):
            args = {**args, **self.args}
        if hasattr(self, "operator"):
            operator = self.operator
        else:
            operator = "and"
            if hasattr(self, "fk"):
                args["on"] = self.fk
            else:
                args["left_index"] = True
        # making a Join between 2 dataframes
        # Add a unique identifier to both dataframes before the merge
        self.df1['_tmp_key_df1'] = range(1, len(self.df1) + 1)
        self.df2['_tmp_key_df2'] = range(1, len(self.df2) + 1)
        try:
            if operator == "and":
                if self.type == "anti-join":
                    # Perform a left merge, adding an indicator column to track the merge source
                    df = pandas.merge(
                        self.df1,
                        self.df2,
                        how="left",
                        suffixes=("", "_right"),
                        indicator=True,
                        **args,
                    )

                    # Filter the rows to keep only those that appear exclusively in the left DataFrame (df1)
                    # by selecting rows labeled as 'left_only' in the _merge column, then drop the _merge column
                    df = df[df['_merge'] == 'left_only'].drop(columns=['_merge'])

                    # Remove any columns that were suffixed with '_right', since we only want columns from df1
                    df = df.loc[:, ~df.columns.str.endswith('_right')]

                else:
                    df = pandas.merge(
                        self.df1,
                        self.df2,
                        how=self.type,
                        suffixes=("_left", "_right"),
                        **args,
                    )

            else:
                if hasattr(self, "fk"):
                    args["left_on"] = self.fk
                else:
                    args["left_index"] = True
                ndf = self.df1
                sdf = self.df2.copy()
                merge = []
                for key in self.join_with:
                    d = pandas.merge(
                        ndf,
                        sdf,
                        right_on=key,
                        how=self.type,
                        suffixes=("_left", None),
                        **args,
                    )
                    ndf = d[d[key].isnull()]
                    ndf.drop(
                        ndf.columns[ndf.columns.str.contains("_left")],
                        axis=1,
                        inplace=True,
                    )
                    ddf = d[d[key].notnull()]
                    ddf.drop(
                        ddf.columns[ddf.columns.str.contains("_left")],
                        axis=1,
                        inplace=True,
                    )
                    merge.append(ddf)
                # merge the last (not matched) rows
                merge.append(ndf)
                df = pandas.concat(merge, axis=0)
                df.reset_index(drop=True)
                df.is_copy = None
        except (ValueError, KeyError) as err:
            self.cleanup_temp_rows()
            raise ComponentError(
                f"Cannot Join with missing Column: {err!s}"
            ) from err
        except Exception as err:
            self.cleanup_temp_rows(df)
            raise ComponentError(
                f"Unknown JOIN error {err!s}"
            ) from err
        numrows = len(df.index)
        if numrows == 0:
            raise DataNotFound(
                "Cannot make any JOIN, returns zero coincidences"
            )
        self._variables[f"{self.StepName}_NUMROWS"] = numrows
        print("ON END> ", numrows)
        self.add_metric("TOTAL_ROWS", numrows)
        try:
            # After merge, count matched rows from each dataframe
            matched_rows_df1 = df['_tmp_key_df1'].nunique()
            matched_rows_df2 = df['_tmp_key_df2'].nunique()
            # Log or print the count of matched rows
            print(f"Matched Rows from df1: {matched_rows_df1}")
            print(f"Matched Rows from df2: {matched_rows_df2}")
            _rows = {
                "df1": matched_rows_df1,
                "df2": matched_rows_df2,
            }
            self.add_metric("JOINED_ROWS", _rows)
            if self._debug is True:
                print("::: Printing Column Information === ")
                for column, t in df.dtypes.items():
                    print(column, "->", t, "->", df[column].iloc[0])
        finally:
            # helping some transformations
            self.cleanup_temp_rows(df)
            self._result = df
        return self._result

    async def close(self):
        pass
