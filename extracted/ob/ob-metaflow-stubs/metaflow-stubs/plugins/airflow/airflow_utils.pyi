######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.17.1+obcheckpoint(0.2.1);ob(v1)                                                   #
# Generated on 2025-06-16T20:11:02.932104                                                            #
######################################################################################################

from __future__ import annotations



TASK_ID_XCOM_KEY: str

FOREACH_CARDINALITY_XCOM_KEY: str

FOREACH_XCOM_KEY: str

RUN_HASH_ID_LEN: int

TASK_ID_HASH_LEN: int

RUN_ID_PREFIX: str

AIRFLOW_FOREACH_SUPPORT_VERSION: str

AIRFLOW_MIN_SUPPORT_VERSION: str

KUBERNETES_PROVIDER_FOREACH_VERSION: str

class KubernetesProviderNotFound(Exception, metaclass=type):
    ...

class ForeachIncompatibleException(Exception, metaclass=type):
    ...

class IncompatibleVersionException(Exception, metaclass=type):
    def __init__(self, version_number):
        ...
    ...

class IncompatibleKubernetesProviderVersionException(Exception, metaclass=type):
    ...

class AirflowSensorNotFound(Exception, metaclass=type):
    ...

def create_absolute_version_number(version):
    ...

def get_kubernetes_provider_version():
    ...

def datetimeparse(isotimestamp):
    ...

def get_xcom_arg_class():
    ...

class AIRFLOW_MACROS(object, metaclass=type):
    @classmethod
    def create_task_id(cls, is_foreach):
        ...
    @classmethod
    def pathspec(cls, flowname, is_foreach = False):
        ...
    ...

class SensorNames(object, metaclass=type):
    @classmethod
    def get_supported_sensors(cls):
        ...
    ...

def run_id_creator(val):
    ...

def task_id_creator(val):
    ...

def id_creator(val, hash_len):
    ...

def json_dump(val):
    ...

class AirflowDAGArgs(object, metaclass=type):
    def __init__(self, **kwargs):
        ...
    @property
    def arguments(self):
        ...
    def serialize(self):
        ...
    @classmethod
    def deserialize(cls, data_dict):
        ...
    ...

def get_metaflow_kubernetes_operator():
    ...

class AirflowTask(object, metaclass=type):
    def __init__(self, name, operator_type = 'kubernetes', flow_name = None, is_mapper_node = False, flow_contains_foreach = False):
        ...
    @property
    def is_mapper_node(self):
        ...
    def set_operator_args(self, **kwargs):
        ...
    def to_dict(self):
        ...
    @classmethod
    def from_dict(cls, task_dict, flow_name = None, flow_contains_foreach = False):
        ...
    def to_task(self):
        ...
    ...

class Workflow(object, metaclass=type):
    def __init__(self, file_path = None, graph_structure = None, metadata = None, **kwargs):
        ...
    def set_parameters(self, params):
        ...
    def add_state(self, state):
        ...
    def to_dict(self):
        ...
    def to_json(self):
        ...
    @classmethod
    def from_dict(cls, data_dict):
        ...
    @classmethod
    def from_json(cls, json_string):
        ...
    def compile(self):
        ...
    ...

