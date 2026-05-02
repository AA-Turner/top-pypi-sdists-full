from typing import Union
import importlib
import asyncio
import logging
from collections.abc import Callable, Awaitable
from ..exceptions import ComponentError
from settings.settings import TASK_STORAGES
from .flow import FlowComponent


def getFunction(program, function):
    """getFunction.

        Example:

        ```yaml
        UserFunc:
          function: scheduling_visits
          args:
            max_distance: 400
            max_stores: 5
            year: 2024
            month: 11
        ```

    """
    ## TODO: detect TaskStorage of the task
    storage = TASK_STORAGES["default"]
    fn_path = storage.path.joinpath(program, "functions", f"{function}.py")
    try:
        spec = importlib.util.spec_from_file_location(function, fn_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        obj = getattr(module, function)
        return obj
    except ImportError as e:
        logging.error(f"UserFunc: No Function {function} was Found")
        raise ComponentError(
            f"UserFunc: No Python Function {function} was Found on {fn_path}"
        ) from e


class UserFunc(FlowComponent):
    """
    UserFunc.

       Overview

       Run a arbitrary user function and return result

       :widths: auto


    |  function    |   Yes    | Name function                                                     |
    |  params      |   Yes    | Allows you to set parameters                                      |
    |  foo         |   Yes    | Variable name                                                     |
    |  api_keys    |   Yes    | Api password to query                                             |

    Return the list of arbitrary days

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          UserFunc:
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
        """Init Method."""
        self._fn: Union[Callable, Awaitable] = None
        self.data = None
        self.params = None
        self.function: Callable = None
        self._kwargs = kwargs.get('args', {})
        super(UserFunc, self).__init__(loop=loop, job=job, stat=stat, **kwargs)

    async def start(self, **kwargs):
        """Obtain Previous data."""
        if self.previous:
            self.data = self.input
        try:
            self._fn = getFunction(self._program, self.function)
        except ComponentError as err:
            raise ComponentError(
                f"UserFunc: Error getting Function from {self.function}"
            ) from err

    async def close(self):
        """Close Method."""

    async def run(self):
        """Run Method."""
        self._result = None
        params = {"data": self.data, "variables": self._variables, **self._kwargs}
        if self.params:
            params = {**params, **self.params}
        try:
            if asyncio.iscoroutinefunction(self._fn):
                result = await self._fn(
                    self, loop=self._loop, env=self._environment, **params
                )
            else:
                result = self._fn(
                    self, loop=self._loop, env=self._environment, **params
                )
            self._result = result
            self.add_metric("UDF", f"{self._fn!s}")
            return self._result
        except ComponentError as err:
            raise ComponentError(f"UserFunc: Error calling {self._fn}: {err}") from err
