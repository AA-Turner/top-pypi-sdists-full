######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.17.1+obcheckpoint(0.2.10);ob(v1)                                                  #
# Generated on 2026-01-22T21:50:04.994120                                                            #
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

