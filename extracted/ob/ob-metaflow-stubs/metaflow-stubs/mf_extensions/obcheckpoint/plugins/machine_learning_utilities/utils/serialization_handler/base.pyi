######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.2+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-16T21:13:36.472258                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import typing


class SerializationHandler(object, metaclass=type):
    def serialze(self, *args, **kwargs) -> typing.Union[str, bytes]:
        ...
    def deserialize(self, *args, **kwargs) -> typing.Any:
        ...
    ...

