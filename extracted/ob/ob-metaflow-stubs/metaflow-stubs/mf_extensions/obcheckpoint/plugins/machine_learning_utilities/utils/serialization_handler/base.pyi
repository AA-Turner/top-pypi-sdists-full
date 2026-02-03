######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.18.1+obcheckpoint(0.2.10);ob(v1)                                                  #
# Generated on 2026-02-03T01:51:07.295628                                                            #
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

