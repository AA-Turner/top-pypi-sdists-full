######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.2+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-16T21:13:36.416304                                                            #
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

