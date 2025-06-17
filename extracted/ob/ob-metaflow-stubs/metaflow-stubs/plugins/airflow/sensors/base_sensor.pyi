######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.999691                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.decorators

from ..exception import AirflowException as AirflowException
from ..airflow_utils import AirflowTask as AirflowTask
from ..airflow_utils import id_creator as id_creator

TASK_ID_HASH_LEN: int

class AirflowSensorDecorator(metaflow.decorators.FlowDecorator, metaclass=type):
    """
    Base class for all Airflow sensor decorators.
    """
    def __init__(self, *args, **kwargs):
        ...
    def serialize_operator_args(self):
        """
        Subclasses will parse the decorator arguments to
        Airflow task serializable arguments.
        """
        ...
    def create_task(self):
        ...
    def validate(self, flow):
        """
        Validate if the arguments for the sensor are correct.
        """
        ...
    def flow_init(self, flow, graph, environment, flow_datastore, metadata, logger, echo, options):
        ...
    ...

