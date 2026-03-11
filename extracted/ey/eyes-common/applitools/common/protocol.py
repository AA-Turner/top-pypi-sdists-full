from __future__ import absolute_import, division, print_function

from typing import TYPE_CHECKING

from .__version__ import __version__
from .command_context import CommandContext
from .object_registry import ObjectRegistry

if TYPE_CHECKING:
    from typing import List, Optional, Union

    from .connection import USDKConnection


class USDKProtocol(object):
    _CommandContext = CommandContext
    _ObjectRegistry = ObjectRegistry
    SDK_INFO = "eyes-common", __version__

    @classmethod
    def object_registry(cls):
        return cls._ObjectRegistry()

    @classmethod
    def context(cls, connection, object_registry=None):
        # type: (USDKConnection, Optional[ObjectRegistry]) -> CommandContext
        return cls._CommandContext(connection, object_registry or cls.object_registry())

    @classmethod
    def commands_or_kind(cls):
        # type: () -> Union[str, List[str]]
        return cls._CommandContext.commands_or_kind()
