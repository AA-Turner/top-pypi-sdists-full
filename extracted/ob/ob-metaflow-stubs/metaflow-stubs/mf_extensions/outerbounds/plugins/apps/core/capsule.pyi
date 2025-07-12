######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.561256                                                            #
######################################################################################################

from __future__ import annotations

import typing
if typing.TYPE_CHECKING:
    import typing
    import metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.app_config
    import metaflow.mf_extensions.outerbounds.plugins.apps.core.capsule

from .utils import TODOException as TODOException
from .utils import safe_requests_wrapper as safe_requests_wrapper
from .utils import MaximumRetriesExceeded as MaximumRetriesExceeded
from .app_config import AppConfig as AppConfig
from .app_config import AuthType as AuthType
from . import experimental as experimental
from ._state_machine import CapsuleWorkerSemanticStatus as CapsuleWorkerSemanticStatus
from ._state_machine import WorkerStatus as WorkerStatus
from ._state_machine import CapsuleStatus as CapsuleStatus
from ._state_machine import DEPLOYMENT_READY_CONDITIONS as DEPLOYMENT_READY_CONDITIONS

CAPSULE_DEBUG: bool

class CapsuleStateMachine(object, metaclass=type):
    """
    - Every capsule create call will return a `identifier` and a `version` of the object.
    - Each update call will return a new version.
    - The status.currentlyServedVersion will be the version that is currently serving traffic.
    - The status.updateInProgress will be True if an upgrade is in progress.
    
    CapsuleState Transition:
    - Every capsule create call will return a `identifier` and a `version` of the object.
    - Happy Path:
        - First time Create :
            - wait for status.updateInProgress to be set to False
                - (interleved) Poll the worker endpoints to check their status
                    - showcase how many workers are coming up if things are on the cli side.
                - If the user has set some flag like `--dont-wait-to-fully-finish` then we check the `status.currentlyServedVersion` to see if even one replica is ready to
                serve traffic.
            - once the status.updateInProgress is set to False, it means that the replicas are ready
        - Upgrade:
            - wait for status.updateInProgress to be set to False
                - (interleved) Poll the worker endpoints to check their status and signal the user the number replicas coming up
                - If the user has set some flag like `--dont-wait-to-fully-finish` then we check the `status.currentlyServedVersion` to see if even one replica is ready to
                serve traffic.
    - Unhappy Path:
        - First time Create :
            - wait for status.updateInProgress to be set to False,
                - (interleved) Poll the workers to check their status.
                    - If the worker pertaining the current deployment instance version is crashlooping then crash the deployment process with the error messages and logs.
        - Upgrade:
            - wait for status.updateInProgress to be set to False,
                - (interleved) Poll the workers to check their status.
                    - If the worker pertaining the current deployment instance version is crashlooping then crash the deployment process with the error messages and logs.
    """
    def __init__(self, capsule_id: str, current_deployment_instance_version: str):
        ...
    def get_status_trail(self):
        ...
    def add_status(self, status: metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine.CapsuleStatus):
        ...
    @property
    def current_status(self):
        ...
    @property
    def out_of_cluster_url(self):
        ...
    @property
    def in_cluster_url(self):
        ...
    @property
    def update_in_progress(self):
        ...
    @property
    def currently_served_version(self):
        ...
    @property
    def ready_to_serve_traffic(self):
        ...
    @property
    def available_replicas(self):
        ...
    def report_current_status(self, logger):
        ...
    def save_debug_info(self, state_dir: str):
        ...
    ...

class CapsuleWorkersStateMachine(object, metaclass=type):
    def __init__(self, capsule_id: str, end_state_capsule_version: str, deployment_mode: str = 'at_least_one_running', minimum_replicas: int = 1):
        ...
    def get_status_trail(self):
        ...
    def add_status(self, worker_list_response: typing.List[metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine.WorkerStatus]):
        """
        worker_list_response: List[Dict[str, Any]]
            [
                {
                    "workerId": "c-4pqikm-659dd9ccdc-5hcwz",
                    "phase": "Running",
                    "activity": 0,
                    "activityDataAvailable": false,
                    "version": "0xhgaewiqb"
                },
                {
                    "workerId": "c-4pqikm-b8559688b-xk2jh",
                    "phase": "Pending",
                    "activity": 0,
                    "activityDataAvailable": false,
                    "version": "421h48qh95"
                }
            ]
        """
        ...
    def save_debug_info(self, state_dir: str):
        ...
    def report_current_status(self, logger):
        ...
    @property
    def current_status(self) -> typing.List[metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine.WorkerStatus]:
        ...
    def current_version_deployment_status(self) -> metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine.CapsuleWorkerSemanticStatus:
        ...
    @property
    def is_crashlooping(self) -> bool:
        ...
    ...

class CapsuleInput(object, metaclass=type):
    @classmethod
    def construct_exec_command(cls, commands: typing.List[str]):
        ...
    @classmethod
    def from_app_config(cls, app_config: metaflow.mf_extensions.outerbounds.plugins.apps.core.app_config.AppConfig):
        ...
    ...

class CapsuleApiException(Exception, metaclass=type):
    def __init__(self, url: str, method: str, status_code: int, text: str, message: typing.Optional[str] = None):
        ...
    def __str__(self):
        ...
    ...

class CapsuleDeploymentException(Exception, metaclass=type):
    def __init__(self, capsule_id: str, message: str):
        ...
    def __str__(self):
        ...
    ...

class CapsuleApi(object, metaclass=type):
    def __init__(self, base_url: str, perimeter: str, logger_fn = None):
        ...
    def create(self, capsule_input: dict):
        ...
    def get(self, capsule_id: str):
        ...
    def list(self):
        ...
    def delete(self, capsule_id: str):
        ...
    def get_workers(self, capsule_id: str) -> typing.List[typing.Dict[str, typing.Any]]:
        ...
    def logs(self, capsule_id: str, worker_id: str, previous: bool = False) -> typing.List[str]:
        ...
    ...

def list_and_filter_capsules(capsule_api: CapsuleApi, project, branch, name, tags, auth_type, capsule_id):
    ...

class CapsuleInfo(tuple, metaclass=type):
    """
    CapsuleInfo(info, workers)
    """
    @staticmethod
    def __new__(_cls, info, workers):
        """
        Create new instance of CapsuleInfo(info, workers)
        """
        ...
    def __repr__(self):
        """
        Return a nicely formatted representation string
        """
        ...
    def __getnewargs__(self):
        """
        Return self as a plain tuple.  Used by copy and pickle.
        """
        ...
    ...

class CapsuleDeployer(object, metaclass=type):
    def __init__(self, app_config: metaflow.mf_extensions.outerbounds.plugins.apps.core.app_config.AppConfig, base_url: str, create_timeout: int = 300, debug_dir: typing.Optional[str] = None, success_terminal_state_condition: str = 'at_least_one_running', readiness_wait_time: int = 20, logger_fn = None):
        ...
    @property
    def url(self):
        ...
    @property
    def capsule_api(self):
        ...
    @property
    def capsule_type(self):
        ...
    @property
    def name(self):
        ...
    def create_input(self):
        ...
    @property
    def current_deployment_instance_version(self):
        """
        The backend `create` call returns a version of the object that will be
        """
        ...
    def create(self):
        ...
    def get(self):
        ...
    def get_workers(self):
        ...
    def wait_for_terminal_state(self):
        """
        """
        ...
    ...

