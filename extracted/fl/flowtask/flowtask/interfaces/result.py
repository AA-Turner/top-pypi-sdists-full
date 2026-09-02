from abc import ABC
from typing import Optional, ParamSpec, Any
from collections.abc import Iterable
from asyncdb import AsyncDB
from asyncdb.drivers.base import BaseDriver
from ..conf import MEMCACHE_HOST, MEMCACHE_PORT

P = ParamSpec("P")

class ResultSupport(ABC):
    """Support for manipulating the results of Components."""

    _memory: Optional[BaseDriver] = None

    def __init__(
        self,
        *args: P.args,
        **kwargs: P.kwargs
    ):
        self.use_memory: bool = kwargs.pop('use_memory', False)
        # collection of results:
        self._result: Optional[Any] = None
        self.data: Optional[Any] = None
        # previous Component
        self._component: Optional[Iterable] = None
        # can pass a previous data as Argument:
        self._input_result = kwargs.pop('input_result', None)
        super(ResultSupport, self).__init__(*args, **kwargs)
        # memcache connector
        if self.use_memory is True:
            self.get_memcached()

    def get_memcached(self):
        params = {"host": MEMCACHE_HOST, "port": MEMCACHE_PORT}
        try:
            self._memory = AsyncDB("memcache", params=params)
        except Exception as err:
            self.logger.exception(err)

    def output(self):
        return self._result

    @property
    def result(self):
        return self._result

    @result.setter
    def result(self, value):
        self._result = value

    @property
    def input(self):
        if isinstance(self._component, list):
            # TODO: get an array the results from different components
            result = []
            for component in self._component:
                if component:
                    result.append(component.output())
            if len(result) == 1:
                return result[0]
            else:
                return result
        elif self._component:
            if self._input_result is not None:
                return self._input_result
            return self._component.output()
        else:
            return self._input_result

    @input.setter
    def input(self, value: Any):
        self._input_result = value

    @property
    def previous(self):
        if self._component is not None:
            return self._component
        elif self._input_result is not None:
            return self  # result data is already on component
        else:
            return None

    async def close(self):
        try:
            await self._memory.close()
        except Exception:  # pylint: disable=W0718
            pass
