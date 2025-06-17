######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.947070                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.utils.serialization_handler.base

from ..tar_utils import create_tarball_in_memory as create_tarball_in_memory
from ..tar_utils import create_tarball_on_disk as create_tarball_on_disk
from ..tar_utils import extract_tarball as extract_tarball
from .base import SerializationHandler as SerializationHandler

class TarHandler(metaflow.mf_extensions.obcheckpoint.plugins.machine_learning_utilities.utils.serialization_handler.base.SerializationHandler, metaclass=type):
    def serialize(self, path_to_compress, path_to_save = None, in_memory = False, strict = False) -> typing.Union[str, bytes]:
        ...
    def deserialize(self, path_or_bytes, target_directory) -> str:
        ...
    ...

