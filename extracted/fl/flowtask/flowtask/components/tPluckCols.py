import asyncio
from typing import List
from collections.abc import Callable
import pandas
from ..exceptions import ComponentError
from .tPandas import tPandas


class tPluckCols(tPandas):
    """
    tPluckCols

        Overview

            The tPluckCols class is a component for selecting a specific subset of columns from a Pandas DataFrame.
            It provides a streamlined way to filter columns, allowing only specified columns to be retained in the output.

        :widths: auto

            | columns     |   Yes    | A list of column names to retain in the DataFrame.                        |

        Returns

            This component returns a Pandas DataFrame containing only the specified columns listed in `columns`.
            If no columns are provided, it raises an error. The resulting DataFrame is a copy to ensure
            any modifications do not affect the original DataFrame.


        Example:

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          tPluckCols:
          depends:
          - TransformRows_11
          columns:
          - location_code
          - ss_market
          - store_id
          - store_number
          - company_id
          - pt_ft
          - is_covered
          - endcap
          - rev_band
          - comparison_store
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
        self.columns: List = None
        super(tPluckCols, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Obtain Pandas Dataframe."""
        await super().start(**kwargs)
        if not self.columns:
            raise ComponentError("Error: need to specify a list of *columns*")
        return True

    async def _run(self):
        return self.data[self.columns].copy()
