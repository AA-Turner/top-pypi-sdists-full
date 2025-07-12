######################################################################################################
#                                 Auto-generated Metaflow stub file                                  #
# MF version: 2.15.21.1+obcheckpoint(0.2.4);ob(v1)                                                   #
# Generated on 2025-07-11T23:29:18.558966                                                            #
######################################################################################################

from __future__ import annotations

import typing
from typing import TypedDict
if typing.TYPE_CHECKING:
    import metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine


TYPE_CHECKING: bool

class AccessInfo(TypedDict, total=True):
    outOfClusterURL: str
    inClusterURL: str

class CapsuleStatus(TypedDict, total=True):
    availableReplicas: int
    readyToServeTraffic: bool
    accessInfo: AccessInfo
    updateInProgress: bool
    currentlyServedVersion: str

class WorkerStatus(TypedDict, total=True):
    workerId: str
    phase: str
    activity: int
    activityDataAvailable: bool
    version: str

class WorkerInfoDict(TypedDict, total=True):
    pending: typing.Dict[str, typing.List[metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine.WorkerStatus]]
    running: typing.Dict[str, typing.List[metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine.WorkerStatus]]
    crashlooping: typing.Dict[str, typing.List[metaflow.mf_extensions.outerbounds.plugins.apps.core._state_machine.WorkerStatus]]

class CurrentWorkerInfo(TypedDict, total=True):
    pending: int
    running: int
    crashlooping: int

class DEPLOYMENT_READY_CONDITIONS(object, metaclass=type):
    """
    Deployment ready conditions define what is considered a successful completion of the current deployment instance.
    This allows users or platform designers to configure the criteria for deployment readiness.
    
    Why do we need deployment readiness conditions?
    - Deployments might be taking place from a CI/CD esq environment, In these setups, the downstream build triggers might be depending on a specific criteria for deployment completion. Having readiness conditions allows the CI/CD systems to get a signal of when the deployment is ready.
    - Users might be calling the deployment API under different conditions:
        - Some users might want a cluster of workers ready before serving traffic while others might want just one worker ready to start serving traffic.
    
    Some readiness conditions include:
    1) [at_least_one_running] Atleast min(min_replicas, 1) workers of the current deployment instance's version have started running.
        - Usecase: Some endpoints may be deployed ephemerally and are considered ready when at least one instance is running; additional instances are for load management.
    2) [all_running] Atleast min_replicas number of workers are running for the deployment to be considered ready.
        - Usecase: Operators may require that all replicas are available before traffic is routed. Needed when inference endpoints maybe under some SLA or require a larger load
    3) [fully_finished] Atleast min_replicas number of workers are running for the deployment and there are no pending or crashlooping workers from previous versions lying around.
        - Usecase: Ensuring endpoint is fully available and no other versions are running or endpoint has been fully scaled down.
    4) [async] The deployment will be assumed ready as soon as the server responds with a 200.
        - Usecase: Operators may only care that the URL is minted for the deployment or the deployment eventually scales down to 0.
    """
    @classmethod
    def check_failure_condition(cls, capsule_status: CapsuleStatus, worker_semantic_status: CapsuleWorkerSemanticStatus) -> bool:
        """
        Check if the deployment has failed based on the current capsule and worker status.
        """
        ...
    @classmethod
    def check_readiness_condition(cls, capsule_status: CapsuleStatus, worker_semantic_status: CapsuleWorkerSemanticStatus, readiness_condition: str) -> typing.Tuple[bool, bool]:
        """
        Check if the deployment readiness condition is satisfied based on current capsule and worker status.
        
        This method evaluates whether a deployment has reached its desired ready state according to
        the specified readiness condition. Different conditions have different criteria for what
        constitutes a "ready" deployment.
        
        Parameters
        ----------
        capsule_status : CapsuleStatus
            The current status of the capsule deployment, including update progress information.
        worker_semantic_status : CapsuleWorkerSemanticStatus
            Semantic status information about the workers, including counts and states.
        readiness_condition : str
            The readiness condition to evaluate. Must be one of the class constants:
            - ATLEAST_ONE_RUNNING: At least one worker is running and update is not in progress
            - ALL_RUNNING: All required workers are running and update is not in progress
            - FULLY_FINISHED: All workers running with no pending/crashlooping workers and update is not in progress
            - ASYNC: Deployment is ready as soon as the backend responds with a 200 on create and provides a API URL.
        
        Returns
        -------
        Tuple[bool, bool]
            A tuple containing:
            - First element: Boolean indicating if the readiness condition is satisfied
            - Second element: Boolean indicating if additional worker readiness checks
              should be performed (False for ASYNC mode, True for all others)
        
        Raises
        ------
        ValueError
            If an invalid readiness condition is provided.
        """
        ...
    @classmethod
    def docstring(cls):
        ...
    @classmethod
    def enums(cls):
        ...
    ...

class CapsuleWorkerStatusDict(TypedDict, total=True):
    at_least_one_pending: bool
    at_least_one_running: bool
    at_least_one_crashlooping: bool
    all_running: bool
    fully_finished: bool
    none_present: bool
    current_info: CurrentWorkerInfo

class CapsuleWorkerSemanticStatus(TypedDict, total=True):
    final_version: str
    status: CapsuleWorkerStatusDict
    worker_info: WorkerInfoDict

