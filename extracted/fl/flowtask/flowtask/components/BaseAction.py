import asyncio
from abc import ABC
from typing import List, Dict, Union
from collections.abc import Callable
from ..exceptions import DataNotFound, ComponentError
from .flow import FlowComponent


class BaseAction(FlowComponent, ABC):
    """
    BaseAction Component

        Overview
            Basic component for making RESTful queries to URLs.
            This component serves as a foundation for building more specific action components.
            It allows you to define methods (functions) that can be executed asynchronously.

                :widths: auto

        | loop (optional)       | No       | Event loop to use for asynchronous operations (defaults to the current event loop).                                       |
        | job (optional)        | No       | Reference to a job object for logging and tracking purposes.                                                              |
        | stat (optional)       | No       | Reference to a stat object for custom metrics collection.                                                                 |
        | method (from kwargs)  | Yes      | Name of the method (function) within the component to be executed. Specified as a keyword argument during initialization. |

        **Returns**

        The output data can vary depending on the implemented method. It can be a list, dictionary, or any data structure returned by the executed method.

        **Error Handling**

        - `DataNotFound`: This exception is raised if the executed method doesn't return any data.
        - `ComponentError`: This exception is raised for any other errors encountered during execution.

    |---|---|---|
    | version | No | version of component |


        Example:

        | Name | Required | Summary |
    |---|---|---|
    | version | No | version of component |


        Example:

        ```yaml
          BaseAction:
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
    ) -> None:
        """Init Method."""
        self._result: Union[List, Dict] = None
        self._method: str = kwargs.pop("method", None)
        super().__init__(loop=loop, job=job, stat=stat, **kwargs)
        args = self._attrs.get("args", {})
        keys_to_remove = ["loop", "stat", "debug", "memory", "comment", "Group"]
        self._kwargs = {k: v for k, v in args.items() if k not in keys_to_remove}

    async def start(self, **kwargs):
        if not hasattr(self, self._method):
            raise ComponentError(f"{self.__name__} Error: has no Method {self._method}")
        # Getting the method to be called
        self._fn = getattr(self, self._method)
        await super(BaseAction, self).start(**kwargs)
        # Processing Variables:
        self._kwargs = self.var_replacement(self._kwargs)
        return True

    async def close(self):
        pass

    async def run(self):
        try:
            result, error = await self._fn(**self._kwargs)
            if error:
                self._logger.warning(
                    f"Error {self.__name__}.{self._fn.__name__}: {error}"
                )
                return False
            if result is None:
                raise DataNotFound(
                    f"No data found for {self.__name__}.{self._fn.__name__}"
                )
            self._result = result
            self.add_metric(f"{self.__name__}.{self._fn.__name__}", result)
        except DataNotFound:
            raise
        except Exception as e:
            raise ComponentError(f"Error running {self.__name__}: {e}")
        return self._result
