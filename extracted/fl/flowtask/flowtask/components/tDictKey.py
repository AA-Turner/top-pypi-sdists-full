import asyncio
from collections.abc import Callable
from typing import Any
import pandas as pd
from ..exceptions import ComponentError, DataNotFound
from ..interfaces.flow import FlowComponent


class tDictKey(FlowComponent):
    """
    tDictKey

        Overview

            Extracts a single value from a dictionary produced by the previous
            component and forwards it as this component's result.

            Several components return a mapping of named results rather than a
            bare object (e.g. ``CensusData`` returns
            ``{"data": DataFrame, "variables": DataFrame}``). ``tDictKey`` selects
            one of those keys (``key: "data"``) so that downstream DataFrame
            components such as ``tMap`` or ``tFilter`` receive the DataFrame they
            expect instead of the whole dictionary.

        .. table:: Properties
           :widths: auto

            +-----------+----------+-----------------------------------------------------------+
            | Name      | Required | Summary                                                   |
            +===========+==========+===========================================================+
            | key       |   Yes    | Key to extract from the incoming dictionary.              |
            +-----------+----------+-----------------------------------------------------------+
            | default   |   No     | Value to return when ``key`` is missing. When omitted, a  |
            |           |          | missing key raises a ``ComponentError``.                  |
            +-----------+----------+-----------------------------------------------------------+

        Returns

            The value stored under ``key`` in the incoming dictionary (commonly a
            Pandas DataFrame). When the extracted value is a DataFrame, row/column
            metrics are recorded.

        Example:

        ```yaml
          - CensusData:
              year: 2024
              table: DP05
              geography: county
              state_filter: "06"
          - tDictKey:
              key: data
          - tMap:
              # ... now receives the DataFrame instead of the dict
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
        self.key: str = kwargs.pop("key", None)
        # Sentinel so that ``default: null`` is honoured as a real default.
        self._has_default: bool = "default" in kwargs
        self.default: Any = kwargs.pop("default", None)
        super(tDictKey, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Obtain the dictionary produced by the previous component."""
        if not self.key:
            raise ComponentError(
                "tDictKey: a 'key' attribute is required."
            )
        if self.previous:
            self.data = self.input
        else:
            raise DataNotFound(
                "tDictKey: No input data found.", status=404
            )
        if not isinstance(self.data, dict):
            raise ComponentError(
                f"tDictKey: expected a dict as input, got "
                f"{type(self.data).__name__}."
            )
        return True

    async def close(self):
        pass

    async def run(self):
        if self.key in self.data:
            self._result = self.data[self.key]
        elif self._has_default:
            self.logger.warning(
                f"tDictKey: key '{self.key}' not found; using default."
            )
            self._result = self.default
        else:
            raise ComponentError(
                f"tDictKey: key '{self.key}' not found in input dict. "
                f"Available keys: {list(self.data.keys())}"
            )
        if isinstance(self._result, pd.DataFrame):
            self.add_metric("NUM_ROWS", self._result.shape[0])
            self.add_metric("NUM_COLUMNS", self._result.shape[1])
            if self._debug:
                print(f"Debugging: {self.__name__} (key='{self.key}') ===")
                print(self._result)
        self.add_metric("EXTRACTED_KEY", self.key)
        return self._result
