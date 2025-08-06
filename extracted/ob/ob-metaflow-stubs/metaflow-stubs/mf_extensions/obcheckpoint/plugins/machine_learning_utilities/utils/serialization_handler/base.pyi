######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.17.0.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-08-05T23:30:10.151855                                                            #
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

