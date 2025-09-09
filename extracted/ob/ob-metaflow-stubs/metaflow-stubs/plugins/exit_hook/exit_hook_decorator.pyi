######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.2.1+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-09-08T21:00:14.420339                                                            #
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

