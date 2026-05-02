import asyncio
from collections.abc import Callable

# logging system
import numpy as np
import pandas
from querysource.types.dt import filters as qsffunctions
from . import functions as dffunctions
from ..flow import FlowComponent
from ...utils.functions import check_empty
from ...exceptions import ComponentError, DataNotFound


class FilterRows(FlowComponent):
    """
    FilterRows

    Overview

        The FilterRows class is a component for removing or cleaning rows in a Pandas DataFrame based on specified criteria.
        It supports various cleaning and filtering operations and allows for the saving of rejected rows to a file.

    :widths: auto

        | fields           |   Yes    | A dictionary defining the fields and corresponding filtering conditions to be applied.           |
        | filter_conditions|   Yes    | A dictionary defining the filter conditions for transformations.                                 |
        | _applied         |   No     | A list to store the applied filters.                                                             |
        | multi            |   No     | A flag indicating if multiple DataFrame transformations are supported, defaults to False.        |

    Return

        The methods in this class manage the filtering of rows in a Pandas DataFrame, including initialization, execution,
        and result handling.



        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          FilterRows:
          filter_conditions:
          clean_empty:
          columns:
          - updated
          drop_columns:
          columns:
          - legal_street_address_1
          - legal_street_address_2
          - work_location_address_1
          - work_location_address_2
          - birth_date
          suppress:
          columns:
          - payroll_id
          - reports_to_payroll_id
          pattern: (\.0)
          drop_empty: true
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
        self.fields: dict = {}
        self.filter_conditions: dict = {}
        self._applied: list = []
        self.multi = bool(kwargs.pop("multi", False))
        if self.multi:
            self.fields = {}
        if self.multi is False:
            if "fields" in kwargs:
                self.fields = kwargs.pop('fields', {})
        else:
            self.fields = {}
        super(FilterRows, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        if self.previous:
            self.data = self.input
        else:
            raise ComponentError("a Previous Component was not found.")
        if check_empty(self.data):
            raise DataNotFound("No data was found")

    async def run(self):
        if self.data is None:
            return False
        if isinstance(self.data, pandas.DataFrame):
            # add first metrics
            self.add_metric("started_rows", self.data.shape[0])
            self.add_metric("started_columns", self.data.shape[1])

            # start filtering
            if hasattr(self, "clean_strings"):
                u = self.data.select_dtypes(include=["object", "string"])
                self.data[u.columns] = self.data[u.columns].fillna("")
            if hasattr(self, "clean_numbers"):
                u = self.data.select_dtypes(include=["Int64"])
                # self.data[u.columns] = self.data[u.columns].fillna('')
                self.data[u.columns] = self.data[u.columns].replace(
                    ["nan", np.nan], 0, regex=True
                )
                u = self.data.select_dtypes(include=["float64"])
                self.data[u.columns] = self.data[u.columns].replace(
                    ["nan", np.nan], 0, regex=True
                )
            if hasattr(self, "clean_dates"):
                u = self.data.select_dtypes(include=["datetime64[ns]"])
                self.data[u.columns] = self.data[u.columns].replace({np.nan: None})
                # df[u.columns] = df[u.columns].astype('datetime64[ns]')
            if hasattr(self, "drop_empty"):
                # First filter out those rows which
                # does not contain any data
                self.data.dropna(how="all")
                # removing empty cols
                self.data.is_copy = None
                self.data.dropna(axis=1, how="all")
                self.data.dropna(axis=0, how="all")
            if hasattr(self, "dropna"):
                self.data.dropna(subset=self.dropna, how="all")
            # iterate over all filtering conditions:
            df = self.data
            it = df.copy()
            for ft, args in self.filter_conditions.items():
                self._applied.append(f"Filter: {ft!s} args: {args}")
                # TODO: create an expression builder
                # condition = dataframe[(dataframe[column].empty) & (dataframe[column]=='')].index
                # check if is a function
                try:
                    try:
                        func = getattr(dffunctions, ft)
                    except AttributeError:
                        func = getattr(qsffunctions, ft)
                    except AttributeError:
                        func = globals()[ft]
                    if callable(func):
                        it = func(it, **args)
                except Exception as err:
                    print(f"Error on {ft}: {err}")
            else:
                df = it
            if df is None or df.empty:
                raise DataNotFound("No Data was Found after Filtering.")
            self._result = df
            passed = len(self._result.index)
            rejected = len(self.data.index) - len(self._result.index)
            # avoid threat the Dataframe as a Copy
            self._result.is_copy = None
            self.add_metric("ended_rows", df.shape[0])
            self.add_metric("ended_columns", df.shape[1])
            self.add_metric("PASSED", passed)
            self.add_metric("REJECTED", rejected)
            self.add_metric("FILTERS", self._applied)
            self._variables[f"{self.StepName}_PASSED"] = passed
            self._variables[f"{self.StepName}_REJECTED"] = rejected
            if hasattr(self, 'save_rejected'):
                if self.save_rejected:
                    # Identify the indices of the rows that were removed
                    removed_indices = set(self.data.index) - set(self._result.index)
                    # Select these rows from the original DataFrame
                    rejected = self.data.loc[list(removed_indices)]
                    filename = self.save_rejected.get("filename", "rejected_rows.csv")
                    try:
                        rejected.to_csv(filename, sep="|")
                    except IOError:
                        self._logger.warning(
                            f"Error writing Rejectd File: {filename}"
                        )
                    self.add_metric(
                        "rejected_file", filename
                    )
            if self._debug:
                self._logger.verbose(
                    f"PASSED: {passed}, REJECTED: {rejected}",
                )
                print("FILTERED ===")
                print(df)
                print("::: Printing Column Information === ")
                for column, t in df.dtypes.items():
                    print(column, "->", t, "->", df[column].iloc[0])
            return self._result
        else:
            return self._result

    def close(self):
        pass
