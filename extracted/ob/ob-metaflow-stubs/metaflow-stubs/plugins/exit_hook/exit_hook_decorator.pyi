######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.19.37.3+obcheckpoint(0.2.10);<unk>(<unk>);ob(v1)                                     #
# Generated on 2026-09-04T19:03:46.154530                                                            #
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

