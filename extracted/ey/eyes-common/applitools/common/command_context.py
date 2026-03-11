from __future__ import absolute_import, division, print_function

from typing import TYPE_CHECKING

from .marshaller import Marshaller

if TYPE_CHECKING:
    from typing import List, Union

    from .connection import USDKConnection
    from .object_registry import ObjectRegistry


class CommandContext(object):
    def __init__(self, connection, object_registry):
        # type: (USDKConnection, ObjectRegistry) -> None
        self._connection = connection
        self.object_registry = object_registry
        self.key = self.object_registry.next_command_key()
        self.marshaller = Marshaller(self.object_registry)

    @staticmethod
    def commands_or_kind():
        # type: () -> Union[str, List[str]]
        return "webdriver"

    def execute_callback(self, command):
        # type: (dict) -> None
        raise NotImplementedError
