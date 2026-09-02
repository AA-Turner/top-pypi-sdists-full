from typing import Any
from abc import ABC, abstractmethod
from ...interfaces import LogSupport, MaskSupport, LocaleSupport


class AbstractAction(MaskSupport, LogSupport, LocaleSupport, ABC):
    """AbstractAction.

    Action can be used to perform operations when a Hook is called.
    """

    def __init__(self, *args, **kwargs) -> None:
        self._name_ = self.__class__.__name__
        super().__init__(*args, **kwargs)
        # program
        self._program = kwargs.pop("program", "navigator")
        # attributes (root-level of component arguments):
        self._attributes: dict = kwargs.pop("attributes", {})
        # arguments (root-level of component arguments):
        self.arguments: dict = kwargs.pop("arguments", {})
        # Arguments of actions::
        try:
            self.arguments = {**self.arguments, **kwargs}
        except (TypeError, ValueError):
            pass
        # set the attributes of Action:
        for arg, val in self.arguments.items():
            if arg in self._attributes:
                val = self._attributes[arg]
            try:
                setattr(self, arg, val)
            except (AttributeError, TypeError) as err:
                self._logger.warning(
                    f"Wrong Attribute: {arg}={val}"
                )
                self._logger.error(err)
        # You can define any initialization logic here, such as
        # storing parameters that control the behavior of the action.
        self._args = args
        self._kwargs = kwargs

    def __repr__(self) -> str:
        return f"<Action.{self._name_}>"

    @abstractmethod
    async def open(self) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass

    @abstractmethod
    async def run(self, hook, *args, **kwargs) -> Any:
        # This is where you define the behavior of the action.
        # Since this method is asynchronous, you should use the "await"
        # keyword to call other asynchronous functions or coroutines.
        pass

    async def __aenter__(self) -> "AbstractAction":
        await self.open()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        # clean up anything you need to clean up
        return await self.close()
