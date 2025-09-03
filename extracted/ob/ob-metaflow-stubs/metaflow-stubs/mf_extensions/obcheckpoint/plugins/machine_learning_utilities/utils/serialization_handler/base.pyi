######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.1.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-09-02T19:19:25.311806                                                            #
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

