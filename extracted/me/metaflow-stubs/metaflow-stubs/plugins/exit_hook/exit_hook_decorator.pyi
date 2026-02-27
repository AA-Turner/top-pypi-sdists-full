######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.20                                                                                #
# Generated on 2026-02-26T21:59:51.325033                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ...exception import MetaflowException as MetaflowException

class ExitHookDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    def flow_init(self, flow, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    ...

