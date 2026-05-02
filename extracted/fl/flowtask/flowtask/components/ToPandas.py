from collections.abc import Callable
import asyncio
from .flow import FlowComponent
from ..exceptions import DataNotFound
from ..interfaces.dataframes import (
    PandasDataframe,
    PolarsDataframe,
    ArrowDataframe,
    DtDataframe
)


class ToPandas(FlowComponent):
    """
    Convert any input into a DataFrame.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          ToPandas:
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
        self._frame = kwargs.get('frame', 'pandas')
        self._type = kwargs.get('type', 'dict')
        self._data_path = kwargs.get('data_path', None)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Initialize the component."""
        if self.previous:
            self.data = self.input
        if self.data is None:
            raise DataNotFound(
                f"No data found for component '{self.name}'."
            )
        # convert into a List.
        if isinstance(self.data, dict):
            if self._data_path:
                self.data = self.data.get(self._data_path, {})
            self.data = [self.data]
        return True

    async def run(self):
        """Run the component."""
        if self._frame == 'pandas':
            self._result = await PandasDataframe().create_dataframe(
                self.data
            )
        elif self._frame == 'polars':
            self._result = await PolarsDataframe().create_dataframe(
                self.data
            )
        elif self._frame == 'arrow':
            self._result = await ArrowDataframe().create_dataframe(
                self.data
            )
        elif self._frame == 'dt':
            self._result = await DtDataframe().create_dataframe(
                self.data
            )
        self._print_data_(self._result)
        return self._result

    async def close(self):
        """Close the component."""
        pass
