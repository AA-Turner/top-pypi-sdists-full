from datetime import datetime
import json
import os
import pathlib
import requests
import sys
import time
from functools import partial
import shlex
from typing import Optional, List, Dict, Any, Tuple, Union
from .utils import TODOException, safe_requests_wrapper, MaximumRetriesExceeded
from .app_config import AppConfig, CAPSULE_DEBUG, AuthType
from . import experimental
from ._state_machine import (
    _capsule_worker_semantic_status,
    _capsule_worker_status_diff,
    CapsuleWorkerSemanticStatus,
    WorkerStatus,
    CapsuleStatus,
    DEPLOYMENT_READY_CONDITIONS,
)


def _format_url_string(url):
    if url is None:
        return None

    if url.startswith("http://") or url.startswith("https://"):
        return url

    return f"https://{url}"


class CapsuleStateMachine:
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
        self._capsule_id = capsule_id
        self._status_trail: List[Dict[str, Any]] = []
        self._current_deployment_instance_version = current_deployment_instance_version

    def get_status_trail(self):
        return self._status_trail

    def add_status(self, status: CapsuleStatus):
        assert type(status) == dict, "TODO: Make this check somewhere else"
        self._status_trail.append({"timestamp": time.time(), "status": status})

    @property
    def current_status(self):
        return self._status_trail[-1].get("status")

    @property
    def out_of_cluster_url(self):
        access_info = self.current_status.get("accessInfo", {}) or {}
        return _format_url_string(access_info.get("outOfClusterURL", None))

    @property
    def in_cluster_url(self):
        access_info = self.current_status.get("accessInfo", {}) or {}
        return _format_url_string(access_info.get("inClusterURL", None))

    @property
    def update_in_progress(self):
        return self.current_status.get("updateInProgress", False)

    @property
    def currently_served_version(self):
        return self.current_status.get("currentlyServedVersion", None)

    @property
    def ready_to_serve_traffic(self):
        if self.current_status.get("readyToServeTraffic", False):
            return any(
                i is not None for i in [self.out_of_cluster_url, self.in_cluster_url]
            )
        return False

    @property
    def available_replicas(self):
        return self.current_status.get("availableReplicas", 0)

    def report_current_status(self, logger):
        pass

    def save_debug_info(self, state_dir: str):
        debug_path = os.path.join(state_dir, f"debug_capsule_{self._capsule_id}.json")
        with open(debug_path, "w") as f:
            json.dump(self._status_trail, f, indent=4)


class CapsuleWorkersStateMachine:
    def __init__(
        self,
        capsule_id: str,
        end_state_capsule_version: str,
        deployment_mode: str = DEPLOYMENT_READY_CONDITIONS.ATLEAST_ONE_RUNNING,
        minimum_replicas: int = 1,
    ):
        self._capsule_id = capsule_id
        self._end_state_capsule_version = end_state_capsule_version
        self._deployment_mode = deployment_mode
        self._minimum_replicas = minimum_replicas
        self._status_trail: List[Dict[str, Union[float, List[WorkerStatus]]]] = []

    def get_status_trail(self):
        return self._status_trail

    def add_status(self, worker_list_response: List[WorkerStatus]):
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
        self._status_trail.append(
            {"timestamp": time.time(), "status": worker_list_response}
        )

    def save_debug_info(self, state_dir: str):
        debug_path = os.path.join(
            state_dir, f"debug_capsule_workers_{self._capsule_id}_trail.json"
        )
        with open(debug_path, "w") as f:
            json.dump(self._status_trail, f, indent=4)

        status_path = os.path.join(
            state_dir, f"debug_capsule_workers_{self._capsule_id}_status.json"
        )
        with open(status_path, "w") as f:
            json.dump(self.current_version_deployment_status(), f, indent=4)

    def report_current_status(self, logger):
        if len(self._status_trail) == 0:
            return
        older_status = None
        if len(self._status_trail) >= 2:
            older_status = _capsule_worker_semantic_status(
                self._status_trail[-2].get("status"),
                self._end_state_capsule_version,
                self._minimum_replicas,
            )
        current_status = self.current_version_deployment_status()
        changes = _capsule_worker_status_diff(current_status, older_status)
        if len(changes) > 0:
            logger(*changes)

    @property
    def current_status(self) -> List[WorkerStatus]:
        return self._status_trail[-1].get("status")  # type: ignore

    def current_version_deployment_status(self) -> CapsuleWorkerSemanticStatus:
        return _capsule_worker_semantic_status(
            self.current_status, self._end_state_capsule_version, self._minimum_replicas
        )

    @property
    def is_crashlooping(self) -> bool:
        status = self.current_version_deployment_status()
        return status["status"]["at_least_one_crashlooping"]


class CapsuleInput:
    @classmethod
    def construct_exec_command(cls, commands: List[str]):
        commands = ["set -eEuo pipefail"] + commands
        command_string = "\n".join(commands)
        # First constuct a base64 encoded string of the quoted command
        # One of the reasons we don't directly pass the command string to the backend with a `\n` join
        # is because the backend controller doesnt play nice when the command can be a multi-line string.
        # So we encode it to a base64 string and then decode it back to a command string at runtime to provide to
        # `bash -c`. The ideal thing to have done is to run "bash -c {shlex.quote(command_string)}" and call it a day
        # but the backend controller yields the following error:
        # `error parsing template: error converting YAML to JSON: yaml: line 111: mapping values are not allowed in this context`
        # So we go to great length to ensure the command is provided in base64 to avoid any issues with the backend controller.
        import base64

        encoded_command = base64.b64encode(command_string.encode()).decode()
        decode_cmd = f"echo {encoded_command} | base64 -d > ./_ob_app_run.sh"
        return (
            f"bash -c '{decode_cmd} && cat ./_ob_app_run.sh && bash ./_ob_app_run.sh'"
        )

    @classmethod
    def _marshal_environment_variables(cls, app_config: AppConfig):
        envs = app_config.get_state("environment", {}).copy()
        _return = []
        for k, v in envs.items():
            _v = v
            if isinstance(v, dict):
                _v = json.dumps(v)
            elif isinstance(v, list):
                _v = json.dumps(v)
            else:
                _v = str(v)
            _return.append(
                {
                    "name": k,
                    "value": _v,
                }
            )
        return _return

    @classmethod
    def from_app_config(cls, app_config: AppConfig):
        ## Replica settings
        replicas = app_config.get_state("replicas", {})
        fixed, _min, _max = (
            replicas.get("fixed"),
            replicas.get("min"),
            replicas.get("max"),
        )
        if fixed is not None:
            _min, _max = fixed, fixed
        gpu_resource = app_config.get_state("resources").get("gpu")
        resources = {}
        shared_memory = app_config.get_state("resources").get("shared_memory")
        if gpu_resource:
            resources["gpu"] = gpu_resource
        if shared_memory:
            resources["sharedMemory"] = shared_memory

        _scheduling_config = {}
        if app_config.get_state("compute_pools", None):
            _scheduling_config["schedulingConfig"] = {
                "computePools": [
                    {"name": x} for x in app_config.get_state("compute_pools")
                ]
            }
        _description = app_config.get_state("description")
        _app_type = app_config.get_state("app_type")
        _final_info = {}
        if _description:
            _final_info["description"] = _description
        if _app_type:
            _final_info["endpointType"] = _app_type
        return {
            "perimeter": app_config.get_state("perimeter"),
            **_final_info,
            "codePackagePath": app_config.get_state("code_package_url"),
            "image": app_config.get_state("image"),
            "resourceIntegrations": [
                {"name": x} for x in app_config.get_state("secrets", [])
            ],
            "resourceConfig": {
                "cpu": str(app_config.get_state("resources").get("cpu")),
                "memory": str(app_config.get_state("resources").get("memory")),
                "ephemeralStorage": str(app_config.get_state("resources").get("disk")),
                **resources,
            },
            "autoscalingConfig": {
                "minReplicas": _min,
                "maxReplicas": _max,
            },
            **_scheduling_config,
            "containerStartupConfig": {
                "entrypoint": cls.construct_exec_command(
                    app_config.get_state("commands")
                )
            },
            "environmentVariables": cls._marshal_environment_variables(app_config),
            # "assets": [{"name": "startup-script.sh"}],
            "authConfig": {
                "authType": app_config.get_state("auth").get("type"),
                "publicToDeployment": app_config.get_state("auth").get("public"),
            },
            "tags": [
                dict(key=k, value=v)
                for tag in app_config.get_state("tags", [])
                for k, v in tag.items()
            ],
            "port": app_config.get_state("port"),
            "displayName": app_config.get_state("name"),
            "forceUpdate": app_config.get_state("force_upgrade", False),
        }


class CapsuleApiException(Exception):
    def __init__(
        self,
        url: str,
        method: str,
        status_code: int,
        text: str,
        message: Optional[str] = None,
    ):
        self.url = url
        self.method = method
        self.status_code = status_code
        self.text = text
        self.message = message

    def __str__(self):
        return (
            f"CapsuleApiException: {self.url} [{self.method}]: Status Code: {self.status_code} \n\n {self.text}"
            + (f"\n\n {self.message}" if self.message else "")
        )


class CapsuleDeploymentException(Exception):
    def __init__(
        self,
        capsule_id: str,
        message: str,
    ):
        self.capsule_id = capsule_id
        self.message = message

    def __str__(self):
        return f"CapsuleDeploymentException: [{self.capsule_id}] :: {self.message}"


class CapsuleApi:
    def __init__(self, base_url: str, perimeter: str, logger_fn=None):
        self._base_url = self._create_base_url(base_url, perimeter)
        from metaflow.metaflow_config import SERVICE_HEADERS

        self._logger_fn = logger_fn
        self._request_headers = {
            **{"Content-Type": "application/json", "Connection": "keep-alive"},
            **(SERVICE_HEADERS or {}),
        }

    @staticmethod
    def _create_base_url(base_url: str, perimeter: str):
        return os.path.join(
            base_url,
            "v1",
            "perimeters",
            perimeter,
            "capsules",
        )

    def _wrapped_api_caller(self, method_func, *args, **kwargs):
        try:
            response = safe_requests_wrapper(
                method_func,
                *args,
                headers=self._request_headers,
                logger_fn=self._logger_fn,
                **kwargs,
            )
        except MaximumRetriesExceeded as e:
            raise CapsuleApiException(
                e.url,
                e.method,
                e.status_code,
                e.text,
                message=f"Maximum retries exceeded for {e.url} [{e.method}]",
            )
        if response.status_code >= 400:
            raise CapsuleApiException(
                args[0],
                method_func.__name__,
                response.status_code,
                response.text,
            )
        return response

    def create(self, capsule_input: dict):
        _data = json.dumps(capsule_input)
        response = self._wrapped_api_caller(
            requests.post,
            self._base_url,
            data=_data,
        )
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise CapsuleApiException(
                self._base_url,
                "post",
                response.status_code,
                response.text,
                message="Capsule JSON decode failed",
            )

    def get(self, capsule_id: str):
        _url = os.path.join(self._base_url, capsule_id)
        response = self._wrapped_api_caller(
            requests.get,
            _url,
            retryable_status_codes=[409, 404],  # todo : verify me
            conn_error_retries=3,
        )
        try:
            return response.json()
        except json.JSONDecodeError as e:
            raise CapsuleApiException(
                _url,
                "get",
                response.status_code,
                response.text,
                message="Capsule JSON decode failed",
            )

    def list(self):
        response = self._wrapped_api_caller(
            requests.get,
            self._base_url,
            retryable_status_codes=[409],  # todo : verify me
            conn_error_retries=3,
        )
        try:
            response_json = response.json()
        except json.JSONDecodeError as e:
            raise CapsuleApiException(
                self._base_url,
                "get",
                response.status_code,
                response.text,
                message="Capsule JSON decode failed",
            )
        if "capsules" not in response_json:
            raise CapsuleApiException(
                self._base_url,
                "get",
                response.status_code,
                response.text,
                message="Capsule JSON decode failed",
            )
        return response_json.get("capsules", []) or []

    def delete(self, capsule_id: str):
        _url = os.path.join(self._base_url, capsule_id)
        response = self._wrapped_api_caller(
            requests.delete,
            _url,
            retryable_status_codes=[409],  # todo : verify me
        )
        if response.status_code >= 400:
            raise CapsuleApiException(
                _url,
                "delete",
                response.status_code,
                response.text,
            )

        if response.status_code == 200:
            return True
        return False

    def get_workers(self, capsule_id: str) -> List[Dict[str, Any]]:
        _url = os.path.join(self._base_url, capsule_id, "workers")
        response = self._wrapped_api_caller(
            requests.get,
            _url,
            retryable_status_codes=[409, 404],  # todo : verify me
            # Adding 404s because sometimes we might even end up getting 404s if
            # the backend cache is not updated yet. So on consistent 404s we should
            # just crash out.
            conn_error_retries=3,
        )
        try:
            return response.json().get("workers", []) or []
        except json.JSONDecodeError as e:
            raise CapsuleApiException(
                _url,
                "get",
                response.status_code,
                response.text,
                message="Capsule JSON decode failed",
            )

    def logs(
        self, capsule_id: str, worker_id: str, previous: bool = False
    ) -> List[str]:
        _url = os.path.join(self._base_url, capsule_id, "workers", worker_id, "logs")
        options = None
        if previous:
            options = {"previous": True}
        response = self._wrapped_api_caller(
            requests.get,
            _url,
            retryable_status_codes=[409],  # todo : verify me
            params=options,
        )
        try:
            return response.json().get("logs", []) or []
        except json.JSONDecodeError as e:
            raise CapsuleApiException(
                _url,
                "get",
                response.status_code,
                response.text,
                message="Capsule JSON decode failed",
            )


def list_and_filter_capsules(
    capsule_api: CapsuleApi, project, branch, name, tags, auth_type, capsule_id
):
    capsules = capsule_api.list()

    def _tags_match(tags, key, value):
        for t in tags:
            if t["key"] == key and t["value"] == value:
                return True
        return False

    def _all_tags_match(tags, tags_to_match):
        return all([_tags_match(tags, t["key"], t["value"]) for t in tags_to_match])

    def _filter_capsules(capsules, project, branch, name, tags, auth_type, capsule_id):
        _filtered_capsules = []
        for capsule in capsules:
            set_tags = capsule.get("spec", {}).get("tags", [])
            display_name = capsule.get("spec", {}).get("displayName", None)
            set_id = capsule.get("id", None)
            set_auth_type = (
                capsule.get("spec", {}).get("authConfig", {}).get("authType", None)
            )

            if auth_type and set_auth_type != auth_type:
                continue
            if project and not _tags_match(set_tags, "project", project):
                continue
            if branch and not _tags_match(set_tags, "branch", branch):
                continue
            if name and display_name != name:
                continue
            if tags and not _all_tags_match(set_tags, tags):
                continue
            if capsule_id and set_id != capsule_id:
                continue

            _filtered_capsules.append(capsule)
        return _filtered_capsules

    return _filter_capsules(
        capsules, project, branch, name, tags, auth_type, capsule_id
    )


from collections import namedtuple

CapsuleInfo = namedtuple("CapsuleInfo", ["info", "workers"])


class CapsuleDeployer:

    status: CapsuleStateMachine

    identifier = None

    # TODO: Current default timeout is very large of 5 minutes. Ideally we should have finished the deployed in less than 1 minutes.
    def __init__(
        self,
        app_config: AppConfig,
        base_url: str,
        create_timeout: int = 60 * 5,
        debug_dir: Optional[str] = None,
        success_terminal_state_condition: str = DEPLOYMENT_READY_CONDITIONS.ATLEAST_ONE_RUNNING,
        readiness_wait_time: int = 20,
        logger_fn=None,
    ):
        self._app_config = app_config
        self._capsule_api = CapsuleApi(
            base_url,
            app_config.get_state("perimeter"),
            logger_fn=logger_fn or partial(print, file=sys.stderr),
        )
        self._create_timeout = create_timeout
        self._logger_fn = logger_fn
        self._debug_dir = debug_dir
        self._capsule_deploy_response = None
        self._success_terminal_state_condition = success_terminal_state_condition
        self._readiness_wait_time = readiness_wait_time

    @property
    def url(self):
        return _format_url_string(
            ({} or self._capsule_deploy_response).get("outOfClusterUrl", None)
        )

    @property
    def capsule_api(self):
        return self._capsule_api

    @property
    def capsule_type(self):
        auth_type = self._app_config.get_state("auth", {}).get("type", AuthType.default)
        if auth_type == AuthType.BROWSER:
            return "App"
        elif auth_type == AuthType.API:
            return "Endpoint"
        else:
            raise TODOException(f"Unknown auth type: {auth_type}")

    @property
    def name(self):
        return self._app_config.get_state("name")

    def create_input(self):
        return experimental.capsule_input_overrides(
            self._app_config, CapsuleInput.from_app_config(self._app_config)
        )

    @property
    def current_deployment_instance_version(self):
        """
        The backend `create` call returns a version of the object that will be
        """
        if self._capsule_deploy_response is None:
            return None
        return self._capsule_deploy_response.get("version", None)

    def create(self):
        capsule_response = self._capsule_api.create(self.create_input())
        self.identifier = capsule_response.get("id")
        self._capsule_deploy_response = capsule_response
        return self.identifier

    def get(self):
        return self._capsule_api.get(self.identifier)

    def get_workers(self):
        return self._capsule_api.get_workers(self.identifier)

    def _backend_version_mismatch_check(
        self, capsule_response: dict, current_deployment_instance_version: str
    ):
        """
        - `capsule_response.version` contains the version of the object present in the database
        - `current_deployment_instance_version` contains the version of the object that was deployed by this instance of the deployer.
        In the situtation that the versions of the objects become a mismatch then it means that current deployment process is not giving the user the
        output that they desire.
        """
        if capsule_response.get("version", None) != current_deployment_instance_version:
            raise CapsuleDeploymentException(
                self.identifier,  # type: ignore
                f"A capsule upgrade was triggered outside current deployment instance. Current deployment version was discarded. Current deployment version: {current_deployment_instance_version} and new version: {capsule_response.get('version', None)}",
            )

    def _monitor_worker_readiness(
        self,
        workers_sm: "CapsuleWorkersStateMachine",
    ):
        """returns True if the worker is crashlooping, False otherwise"""
        logger = self._logger_fn or partial(print, file=sys.stderr)
        for i in range(self._readiness_wait_time):
            time.sleep(1)
            workers_response = self.get_workers()
            workers_sm.add_status(workers_response)
            workers_sm.report_current_status(logger)
            if workers_sm.is_crashlooping:
                return True
        return False

    def _extract_logs_from_crashlooping_worker(
        self, workers_sm: "CapsuleWorkersStateMachine"
    ):
        def _extract_worker_id_of_crashlooping_worker(
            workers_status: List[WorkerStatus],
        ):
            for worker in workers_status:
                if worker["phase"] == "CrashLoopBackOff":
                    return worker["workerId"]
            return None

        worker_id = _extract_worker_id_of_crashlooping_worker(workers_sm.current_status)
        if worker_id is None:
            return None, None
        logs = self.capsule_api.logs(self.identifier, worker_id, previous=True)
        return logs, worker_id

    def _get_min_replicas(self):
        replicas = self._app_config.get_state("replicas", {})
        fixed, _min, _ = replicas.get("fixed"), replicas.get("min"), replicas.get("max")
        if fixed is not None:
            return fixed
        return _min

    def wait_for_terminal_state(
        self,
    ):
        """ """
        logger = self._logger_fn or partial(print, file=sys.stderr)
        state_machine = CapsuleStateMachine(
            self.identifier, self.current_deployment_instance_version
        )
        # min_replicas will always be present
        min_replicas = self._get_min_replicas()
        workers_state_machine = CapsuleWorkersStateMachine(
            self.identifier,
            self.current_deployment_instance_version,
            deployment_mode=self._success_terminal_state_condition,
            minimum_replicas=min_replicas,
        )
        self.status = state_machine
        for i in range(self._create_timeout):
            time.sleep(1)
            capsule_response = self.get()
            workers_response = self.get_workers()

            # We first need to check if someone has not upgraded the capsule under the hood and
            # the current deployment instance is invalid.
            self._backend_version_mismatch_check(
                capsule_response, self.current_deployment_instance_version  # type: ignore
            )
            state_machine.add_status(capsule_response.get("status", {}))  # type: ignore
            workers_state_machine.add_status(workers_response)
            state_machine.report_current_status(logger)

            workers_state_machine.report_current_status(logger)
            # Deployment readiness checks will determine what is the terminal state
            # of the workerstate machine. If we detect a terminal state in the workers,
            # then even if the capsule upgrade is still in progress we will end up crashing
            # the deployment.
            (
                capsule_ready,
                further_check_worker_readiness,
            ) = DEPLOYMENT_READY_CONDITIONS.check_readiness_condition(
                state_machine.current_status,
                workers_state_machine.current_version_deployment_status(),
                self._success_terminal_state_condition,
            )

            failure_condition_satisfied = (
                DEPLOYMENT_READY_CONDITIONS.check_failure_condition(
                    state_machine.current_status,
                    workers_state_machine.current_version_deployment_status(),
                )
            )
            if capsule_ready or failure_condition_satisfied:
                logger(
                    "💊 %s deployment status: %s | worker states: [success :%s | failure :%s ] "
                    % (
                        self.capsule_type.title(),
                        "in progress"
                        if state_machine.update_in_progress
                        else "completed",
                        capsule_ready,
                        failure_condition_satisfied,
                    )
                )
                _further_readiness_check_failed = False
                if further_check_worker_readiness:
                    # HACK : monitor the workers for N seconds to make sure they are healthy
                    # this is a hack. Ideally we should implment a healtcheck as a first class citizen
                    # but it will take some time to do that so in the meanwhile a timeout set on the cli
                    # side will be really helpful.
                    logger(
                        "💊 running last minute readiness check for %s..."
                        % self.identifier
                    )
                    _further_readiness_check_failed = self._monitor_worker_readiness(
                        workers_state_machine
                    )

                if CAPSULE_DEBUG:
                    logger(
                        f"[debug] 💊 {self.capsule_type} {self.identifier}: further_check_worker_readiness {_further_readiness_check_failed} | failure_condition_satisfied {failure_condition_satisfied}"
                    )

                # We should still check for failure state and crash if we detect something in the readiness check
                if failure_condition_satisfied or _further_readiness_check_failed:
                    # hit the logs endpoint for the worker and get the logs
                    # Print those logs out on the terminal
                    # raise an exception that should be caught gracefully by the cli
                    logs, worker_id = self._extract_logs_from_crashlooping_worker(
                        workers_state_machine
                    )
                    if logs is not None:
                        # todo: It would be really odd if the logs are not present and we discover something is crashlooping.
                        # Handle that condition later
                        logger(
                            *(
                                [
                                    f"💥 Worker ID ({worker_id}) is crashlooping. Please check the following logs for more information: "
                                ]
                                + ["\t" + l["message"] for l in logs]
                            )
                        )
                        raise CapsuleDeploymentException(
                            self.identifier,
                            f"Worker ID ({worker_id}) is crashlooping. Please check the logs for more information.",
                        )

                if state_machine.ready_to_serve_traffic:
                    logger(
                        "💊 %s %s is ready to serve traffic on the URL: %s"
                        % (
                            self.capsule_type,
                            self.identifier,
                            state_machine.out_of_cluster_url,
                        ),
                    )

                break

            if CAPSULE_DEBUG and self._debug_dir:
                state_machine.save_debug_info(self._debug_dir)
                workers_state_machine.save_debug_info(self._debug_dir)
                if i % 3 == 0:  # Every 3 seconds report the status
                    logger(
                        f"[debug] 💊 {self.capsule_type} {self.identifier} deployment status: {state_machine.current_status} | worker states: {workers_state_machine.current_status}"
                    )

        # We will only check ready_to_serve_traffic under the following conditions:
        # If the readiness condition is not Async and min_replicas in this deployment
        # instance is < 0
        _is_async_readiness = (
            self._success_terminal_state_condition == DEPLOYMENT_READY_CONDITIONS.ASYNC
        )
        if (
            min_replicas > 0
            and not _is_async_readiness
            and not self.status.ready_to_serve_traffic
        ):
            raise CapsuleDeploymentException(
                self.identifier,
                f"Capsule {self.identifier} failed to be ready to serve traffic",
            )

        if CAPSULE_DEBUG and self._debug_dir:
            state_machine.save_debug_info(self._debug_dir)
            workers_state_machine.save_debug_info(self._debug_dir)
            logger(
                f"[debug] 💊 {self.capsule_type} {self.identifier} deployment status [on return]: {state_machine.current_status} | worker states: {workers_state_machine.current_status}"
            )

        return dict(
            id=self.identifier,
            auth_type=self.capsule_type,
            public_url=self.url,
            available_replicas=self.status.available_replicas,
            name=self.name,
            deployed_version=self.current_deployment_instance_version,
            deployed_at=datetime.now().isoformat(),
        )
