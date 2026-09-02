from typing import Any, Union, ParamSpec
from abc import ABC, abstractmethod
from navconfig.logging import logging


P = ParamSpec("P")


class BaseDataframe(ABC):

    @abstractmethod
    async def create_dataframe(
        self, result: Union[dict, bytes, Any], *args: P.args, **kwargs: P.kwargs
    ) -> Any:
        """
        Converts any result into a DataFrame.

        :param result: The result data to be converted into a DataFrame.
        :return: A DataFrame containing the result data.
        """
        pass
