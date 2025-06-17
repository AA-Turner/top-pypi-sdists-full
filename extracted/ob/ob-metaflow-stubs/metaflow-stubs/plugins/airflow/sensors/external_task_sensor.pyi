######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:03.000134                                                            #
######################################################################################################

from __future__ import annotations

import metaflow
import typing
if typing.TYPE_CHECKING:
    import metaflow.plugins.airflow.sensors.base_sensor

from .base_sensor import AirflowSensorDecorator as AirflowSensorDecorator
from ..airflow_utils import SensorNames as SensorNames
from ..exception import AirflowException as AirflowException

AIRFLOW_STATES: dict

class ExternalTaskSensorDecorator(metaflow.plugins.airflow.sensors.base_sensor.AirflowSensorDecorator, metaclass=type):
    """
    The `@airflow_external_task_sensor` decorator attaches a Airflow [ExternalTaskSensor](https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/sensors/external_task/index.html#airflow.sensors.external_task.ExternalTaskSensor) before the start step of the flow.
    This decorator only works when a flow is scheduled on Airflow and is compiled using `airflow create`. More than one `@airflow_external_task_sensor` can be added as a flow decorators. Adding more than one decorator will ensure that `start` step starts only after all sensors finish.
    
    Parameters
    ----------
    timeout : int
        Time, in seconds before the task times out and fails. (Default: 3600)
    poke_interval : int
        Time in seconds that the job should wait in between each try. (Default: 60)
    mode : str
        How the sensor operates. Options are: { poke | reschedule }. (Default: "poke")
    exponential_backoff : bool
        allow progressive longer waits between pokes by using exponential backoff algorithm. (Default: True)
    pool : str
        the slot pool this task should run in,
        slot pools are a way to limit concurrency for certain tasks. (Default:None)
    soft_fail : bool
        Set to true to mark the task as SKIPPED on failure. (Default: False)
    name : str
        Name of the sensor on Airflow
    description : str
        Description of sensor in the Airflow UI
    external_dag_id : str
        The dag_id that contains the task you want to wait for.
    external_task_ids : List[str]
        The list of task_ids that you want to wait for.
        If None (default value) the sensor waits for the DAG. (Default: None)
    allowed_states : List[str]
        Iterable of allowed states, (Default: ['success'])
    failed_states : List[str]
        Iterable of failed or dis-allowed states. (Default: None)
    execution_delta : datetime.timedelta
        time difference with the previous execution to look at,
        the default is the same logical date as the current task or DAG. (Default: None)
    check_existence: bool
        Set to True to check if the external task exists or check if
        the DAG to wait for exists. (Default: True)
    """
    def serialize_operator_args(self):
        ...
    def validate(self, flow):
        ...
    ...

