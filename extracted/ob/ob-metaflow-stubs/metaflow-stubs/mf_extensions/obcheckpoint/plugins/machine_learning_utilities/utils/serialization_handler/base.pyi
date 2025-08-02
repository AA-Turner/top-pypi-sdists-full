######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.16.8.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-01T20:12:28.845243                                                            #
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

