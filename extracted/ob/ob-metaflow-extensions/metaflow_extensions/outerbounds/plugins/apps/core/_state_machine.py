import sys
from typing import TYPE_CHECKING, Dict, List, Tuple, Union


# on 3.8+ use the stdlib TypedDict;
# in TYPE_CHECKING blocks mypy/pyright still pick it up on older Pythons
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    if TYPE_CHECKING:
        # for the benefit of type-checkers
        from typing import TypedDict  # noqa: F401
    # runtime no-op TypedDict shim
    class _TypedDictMeta(type):
        def __new__(cls, name, bases, namespace, total=True):
            # ignore total at runtime
            return super().__new__(cls, name, bases, namespace)

    class TypedDict(dict, metaclass=_TypedDictMeta):
        # Runtime stand-in for typing.TypedDict on <3.8.
        pass


class _dagNode:
    def __init__(self, name: str):
        self.name = name
        self.incoming_nodes: List["_dagNode"] = []
        self.outgoing_nodes: List["_dagNode"] = []

    def goto(self, *nodes: "_dagNode"):
        for node in nodes:
            self.outgoing_nodes.append(node)
            node.incoming_nodes.append(self)
        return self

    def arrives_from(self, *nodes: "_dagNode"):
        for node in nodes:
            node.outgoing_nodes.append(self)
            self.incoming_nodes.append(node)
        return self

    def __repr__(self):
        return self.name

    def __str__(self):
        return self.name


class _capsuleDeployerStateMachine:
    def __init__(self):
        # -- (your existing setup) --
        start_state = _dagNode("start")
        fail_state = _dagNode("fail")
        success_state = _dagNode("success")
        upgrade_state = _dagNode("upgrade")
        first_time_create_state = _dagNode("first_time_create")
        end_state = _dagNode("end")

        capsule_deploy_api_call = _dagNode("capsule_deploy_api_call")
        capsule_deploy_api_call_rejected = _dagNode("capsule_deploy_api_call_rejected")
        capsule_worker_pending = _dagNode("capsule_worker_pending")

        capsule_single_worker_ready = _dagNode("capsule_single_worker_ready")
        capsule_multiple_workers_ready = _dagNode("capsule_all_workers_ready")
        current_deployment_deployed_worker_crashed = _dagNode(
            "current_deployment_deployed_worker_crashed"
        )
        current_deployment_workers_pending_beyond_timeout = _dagNode(
            "current_deployment_workers_pending_beyond_timeout"
        )

        start_state.goto(first_time_create_state, upgrade_state)

        capsule_deploy_api_call.arrives_from(
            first_time_create_state, upgrade_state
        ).goto(capsule_deploy_api_call_rejected, capsule_worker_pending)

        capsule_worker_pending.goto(
            capsule_single_worker_ready,
            capsule_multiple_workers_ready,
            current_deployment_deployed_worker_crashed,
            current_deployment_workers_pending_beyond_timeout,
        )
        success_state.arrives_from(
            capsule_single_worker_ready, capsule_multiple_workers_ready
        ).goto(end_state)
        fail_state.arrives_from(
            capsule_deploy_api_call_rejected,
            current_deployment_deployed_worker_crashed,
            current_deployment_workers_pending_beyond_timeout,
        ).goto(end_state)

        self._states = [
            start_state,
            fail_state,
            success_state,
            upgrade_state,
            first_time_create_state,
            end_state,
            capsule_single_worker_ready,
            capsule_multiple_workers_ready,
            current_deployment_deployed_worker_crashed,
            current_deployment_workers_pending_beyond_timeout,
            capsule_deploy_api_call,
            capsule_deploy_api_call_rejected,
            capsule_worker_pending,
        ]

    def get_edges(self) -> List[Tuple["_dagNode", "_dagNode"]]:
        """
        Returns a list of (src_node, dst_node) tuples for all transitions.
        """
        edges = []
        for node in self._states:
            for out in node.outgoing_nodes:
                edges.append((node, out))
        return edges

    def to_dot(self, graph_name="StateMachine"):
        """
        Emit a Graphviz DOT description of the state machine.
        """
        lines = [f"digraph {graph_name} {{"]
        # optional: rankdir=LR for left-to-right layout
        lines.append("    rankdir=LR;")
        for src, dst in self.get_edges():
            lines.append(f'    "{src}" -> "{dst}";')
        lines.append("}")
        return "\n".join(lines)

    def adjacency_list(self):
        """
        Returns a dict mapping each node to list of its outgoing nodes.
        """
        return {node: list(node.outgoing_nodes) for node in self._states}

    def __str__(self):
        # Default to DOT format; you could swap this out for something else
        return self.to_dot()

    def to_diagraph(self):
        from graphviz import Digraph  # type: ignore

        # Create a new Digraph
        dot = Digraph(name="StateMachine", format="png")
        dot.attr(rankdir="LR")  # left-to-right layout

        # Add one edge per transition in your SM
        for src, dst in self.get_edges():
            # src and dst are _dagNode instances; use their .name (or str(src))
            dot.edge(src.name, dst.name)

        # Render to file (e.g. "state_machine.png") and optionally view it:
        dot.render("state_machine", view=False)


class AccessInfo(TypedDict):
    outOfClusterURL: str
    inClusterURL: str


class CapsuleStatus(TypedDict):
    availableReplicas: int
    readyToServeTraffic: bool
    accessInfo: AccessInfo
    updateInProgress: bool
    currentlyServedVersion: str


class WorkerStatus(TypedDict):
    workerId: str
    phase: str
    activity: int
    activityDataAvailable: bool
    version: str


class WorkerInfoDict(TypedDict):
    # TODO : Check if we need to account for the `Terminating` state
    pending: Dict[str, List[WorkerStatus]]
    running: Dict[str, List[WorkerStatus]]
    crashlooping: Dict[str, List[WorkerStatus]]
    failed: Dict[str, List[WorkerStatus]]


class CurrentWorkerInfo(TypedDict):
    # TODO : Check if we need to account for the `Terminating` state
    pending: int
    running: int
    crashlooping: int


class LogLine(TypedDict):
    message: str


class DEPLOYMENT_READY_CONDITIONS:
    """
    Deployment ready conditions define what is considered a successful completion of the current deployment instance.
    This allows users or platform designers to configure the criteria for deployment readiness.

    Why do we need deployment readiness conditions?
        - Deployments might be taking place from a CI/CD-esque environment, In these setups, the downstream build triggers might be depending on a specific criteria for deployment completion. Having readiness conditions allows the CI/CD systems to get a signal of when the deployment is ready.
    - Users might be calling the deployment API under different conditions:
        - Some users might want a cluster of workers ready before serving traffic while others might want just one worker ready to start serving traffic.

    Some readiness conditions include:
            1) [at_least_one_running] At least min(min_replicas, 1) workers of the current deployment instance's version have started running.
        - Usecase: Some endpoints may be deployed ephemerally and are considered ready when at least one instance is running; additional instances are for load management.
        2) [all_running] At least min_replicas number of workers are running for the deployment to be considered ready.
        - Usecase: Operators may require that all replicas are available before traffic is routed. Needed when inference endpoints maybe under some SLA or require a larger load
        3) [fully_finished] At least min_replicas number of workers are running for the deployment and there are no pending or crashlooping workers from previous versions lying around.
        - Usecase: Ensuring endpoint is fully available and no other versions are running or endpoint has been fully scaled down.
    4) [async] The deployment will be assumed ready as soon as the server responds with a 200.
        - Usecase: Operators may only care that the URL is minted for the deployment or the deployment eventually scales down to 0.
    """

    # `ATLEAST_ONE_RUNNING` implies that at least one worker of the current deployment instance's version has started running.
    ATLEAST_ONE_RUNNING = "at_least_one_running"

    # `ALL_RUNNING` implies that all workers of the current deployment instance's version have started running (i.e. all workers aligning to the minimum number of replicas).
    # It doesn't imply that all the workers relating to other deployments have been torn down.
    ALL_RUNNING = "all_running"

    # `FULLY_FINISHED` implies at least min_replicas number of workers are running for the deployment and there are no pending or crashlooping workers from previous versions lying around.
    FULLY_FINISHED = "fully_finished"

    # `ASYNC` implies that the deployment will be assumed ready after the URL is minted and the worker statuses are not checked.
    ASYNC = "async"

    @classmethod
    def check_failure_condition(
        cls,
        capsule_status: CapsuleStatus,
        worker_semantic_status: "CapsuleWorkerSemanticStatus",
    ) -> bool:
        """
        Check if the deployment has failed based on the current capsule and worker status.
        """
        return worker_semantic_status["status"]["at_least_one_crashlooping"]

    @classmethod
    def check_readiness_condition(
        cls,
        capsule_status: CapsuleStatus,
        worker_semantic_status: "CapsuleWorkerSemanticStatus",
        readiness_condition: str,
    ) -> Tuple[bool, bool]:
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
        _worker_readiness_check = True
        _readiness_condition_satisfied = False
        if readiness_condition == cls.ATLEAST_ONE_RUNNING:
            _readiness_condition_satisfied = (
                worker_semantic_status["status"]["at_least_one_running"]
                and not capsule_status["updateInProgress"]
            )
        elif readiness_condition == cls.ALL_RUNNING:
            _readiness_condition_satisfied = (
                worker_semantic_status["status"]["all_running"]
                and not capsule_status["updateInProgress"]
            )
        elif readiness_condition == cls.FULLY_FINISHED:
            # We dont wait for updateInProgress in this condition since
            # UpdateInProgress can switch to false when users scale all replicas down to 0.
            # So for this condition to satisfy we will only rely on the worker semantic status.
            # ie. the thing actually tracking what is running and what is not.
            _readiness_condition_satisfied = worker_semantic_status["status"][
                "fully_finished"
            ]
        elif readiness_condition == cls.ASYNC:
            # The async readiness condition is satisfied immediately after the server responds
            # with the URL.
            _readiness_condition_satisfied = True
            _worker_readiness_check = False
        else:
            raise ValueError(f"Invalid readiness condition: {readiness_condition}")

        return _readiness_condition_satisfied, _worker_readiness_check

    @classmethod
    def docstring(cls):
        return cls.__doc__

    @classmethod
    def enums(cls):
        return [
            cls.ATLEAST_ONE_RUNNING,
            cls.ALL_RUNNING,
            cls.FULLY_FINISHED,
            cls.ASYNC,
        ]


class CapsuleWorkerStatusDict(TypedDict):
    at_least_one_pending: bool
    at_least_one_running: bool
    at_least_one_crashlooping: bool
    all_running: bool
    fully_finished: bool
    none_present: bool
    current_info: CurrentWorkerInfo


class CapsuleWorkerSemanticStatus(TypedDict):
    final_version: str
    status: CapsuleWorkerStatusDict
    worker_info: WorkerInfoDict


def _capsule_worker_status_diff(
    current_status: CapsuleWorkerSemanticStatus,
    previous_status: Union[CapsuleWorkerSemanticStatus, None],
) -> List[str]:
    """
    The goal of this function is to return a status string that will be used to update the user the
    change in status of the different capsules.
    """
    if previous_status is None:
        # Check if the current status has pending workers or crashlooping workers
        curr = current_status["status"]["current_info"]
        version = current_status["final_version"]
        changes = []

        if curr["pending"] > 0:
            changes.append(f"⏳ {curr['pending']} worker(s) pending")

        if curr["running"] > 0:
            changes.append(f"🚀 {curr['running']} worker(s) currently running")

        if curr["crashlooping"] > 0:
            changes.append(f"💥 {curr['crashlooping']} worker(s) currently crashlooping")

        return changes

    curr = current_status["status"]["current_info"]
    prev = previous_status["status"]["current_info"]
    version = current_status["final_version"]

    changes = []

    # Track worker count changes for the target version
    pending_diff = curr["pending"] - prev["pending"]
    running_diff = curr["running"] - prev["running"]
    crash_diff = curr["crashlooping"] - prev["crashlooping"]

    # Worker count changes
    if pending_diff > 0:
        changes.append(
            f"⏳ {pending_diff} new worker(s) pending. Total pending ({curr['pending']})"
        )

    if running_diff > 0:
        changes.append(
            f"🚀 {running_diff} worker(s) started running. Total running ({curr['running']})"
        )
    elif running_diff < 0:
        changes.append(
            f"🛑 {abs(running_diff)} worker(s) stopped running. Total running ({curr['running']})"
        )

    if crash_diff > 0:
        changes.append(
            f"💥 {crash_diff} worker(s) started crashlooping. Total crashlooping ({curr['crashlooping']})"
        )
    elif crash_diff < 0:
        changes.append(f"🔧 {abs(crash_diff)} worker(s) recovered from crashlooping")

    # Significant state transitions
    if (
        not previous_status["status"]["at_least_one_running"]
        and current_status["status"]["at_least_one_running"]
    ):
        changes.append(f"✅ First worker came online")

    if (
        not previous_status["status"]["all_running"]
        and current_status["status"]["all_running"]
    ):
        changes.append(f"🎉 All workers are now running")

    if (
        not previous_status["status"]["at_least_one_crashlooping"]
        and current_status["status"]["at_least_one_crashlooping"]
    ):
        changes.append(f"⚠️  Worker crash detected")

    # Current state summary

    return changes


def _capsule_worker_semantic_status(
    workers: List[WorkerStatus], version: str, min_replicas: int
) -> CapsuleWorkerSemanticStatus:
    def _filter_workers_by_phase(
        workers: List[WorkerStatus], phase: str
    ) -> List[WorkerStatus]:
        return [w for w in workers if w.get("phase") == phase]

    def _make_version_dict(
        _workers: List[WorkerStatus], phase: str
    ) -> Dict[str, List[WorkerStatus]]:
        xx: Dict[str, List[WorkerStatus]] = {}
        for w in _workers:
            if w.get("phase") != phase:
                continue
            worker_version = w.get("version")
            if worker_version is not None:
                if worker_version not in xx:
                    xx[worker_version] = []
                xx[worker_version].append(w)
        return xx

    # phases can be Pending, Running, Succeeded, Failed, Unknown, CrashLoopBackOff
    pending_workers = _make_version_dict(workers, "Pending")
    running_workers = _make_version_dict(workers, "Running")
    crashlooping_workers = _make_version_dict(workers, "CrashLoopBackOff")
    failed_workers = _make_version_dict(workers, "Failed")

    # current_status (formulated basis):
    # - at least one pods are pending for `_end_state_capsule_version`
    # - at least one pod is in Running state for `_end_state_capsule_version` (maybe terminal) [Might require health-check thing here]
    # - at least one pod is crashlooping for `_end_state_capsule_version` (maybe terminal)
    # - all pods are running for `_end_state_capsule_version` that match the minimum number of replicas
    # - all pods are running for `_end_state_capsule_version` that match the maximum number of replicas and no other pods of older versions are running
    # - no pods relating to `_end_state_capsule_version` are pending/running/crashlooping

    # Helper to count pods for the final version in each state
    def count_for_version(workers_dict):
        return len(workers_dict.get(version, []))

    status_dict: CapsuleWorkerStatusDict = {
        "at_least_one_pending": count_for_version(pending_workers) > 0,
        # if min_replicas is 0, the at_least_one_running should be true for running worker count = 0
        "at_least_one_running": (
            count_for_version(running_workers) >= min(min_replicas, 1)
        ),
        "at_least_one_crashlooping": count_for_version(crashlooping_workers) > 0
        or count_for_version(failed_workers) > 0,
        "none_present": (
            count_for_version(running_workers) == 0
            and count_for_version(pending_workers) == 0
            and count_for_version(crashlooping_workers) == 0
        ),
        "all_running": count_for_version(running_workers) >= min_replicas,
        "fully_finished": (
            count_for_version(running_workers) >= min_replicas
            # count the workers of different versions that are runnning
            # and ensure that only the current version's workers are running.
            and count_for_version(running_workers)
            == len(_filter_workers_by_phase(workers, "Running"))
            and len(_filter_workers_by_phase(workers, "Pending")) == 0
            and len(_filter_workers_by_phase(workers, "CrashLoopBackOff")) == 0
        ),
        "current_info": {
            "pending": count_for_version(pending_workers),
            "running": count_for_version(running_workers),
            "crashlooping": count_for_version(crashlooping_workers),
            "failed": count_for_version(failed_workers),
        },
    }

    worker_info: WorkerInfoDict = {
        "pending": pending_workers,
        "running": running_workers,
        "crashlooping": crashlooping_workers,
        "failed": failed_workers,
    }

    return {
        "final_version": version,
        "status": status_dict,
        "worker_info": worker_info,
    }
