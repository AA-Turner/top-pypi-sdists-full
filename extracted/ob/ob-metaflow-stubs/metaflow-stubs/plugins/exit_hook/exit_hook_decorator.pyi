######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.39.1+obcheckpoint(0.2.14);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-09-30T13:33:32.397781                                                            #
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

