######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.18.3.2+obcheckpoint(0.2.4);ob(v1)                                                    #
# Generated on 2025-09-09T09:20:35.603330                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators


class ScheduleDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    """
    Specifies the times when the flow should be run when running on a
    production scheduler.
    
    Parameters
    ----------
    hourly : bool, default False
        Run the workflow hourly.
    daily : bool, default True
        Run the workflow daily.
    weekly : bool, default False
        Run the workflow weekly.
    cron : str, optional, default None
        Run the workflow at [a custom Cron schedule](https://docs.aws.amazon.com/eventbridge/latest/userguide/scheduled-events.html#cron-expressions)
        specified by this expression.
    timezone : str, optional, default None
        Timezone on which the schedule runs (default: None). Currently supported only for Argo workflows,
        which accepts timezones in [IANA format](https://nodatime.org/TimeZones).
    """
    def flow_init(self, flow, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    ...

