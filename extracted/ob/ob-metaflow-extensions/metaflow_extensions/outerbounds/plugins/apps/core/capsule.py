from datetime import datetime
import json
import os
import pathlib
import requests
import sys
import time
from functools import partial
import shlex
from typing import Optional, List, Dict, Any, Tuple, Union, Callable
from urllib.parse import urlparse
from .utils import TODOException, safe_requests_wrapper, MaximumRetriesExceeded
from .app_config import AppConfig, CAPSULE_DEBUG, AuthType
from .config.unified_config import UNASSIGNED_PROJECT_BRANCH, CapsuleType
from . import experimental
from ._state_machine import (
    _capsule_worker_semantic_status,
    _capsule_worker_status_diff,
    CapsuleWorkerSemanticStatus,
    WorkerStatus,
    CapsuleStatus,
    DEPLOYMENT_READY_CONDITIONS,
    LogLine,
)
from .exceptions import (
    CapsuleApiException,
    CapsuleConcurrentUpgradeException,
    CapsuleCrashLoopException,
    CapsuleDeletedDuringDeploymentException,
    CapsuleDeploymentException,
    CapsuleReadinessException,
    OuterboundsBackendUnhealthyException,
    OuterboundsForbiddenException,
)

STATE_REFRESH_FREQUENCY = 1  # in seconds

# The port a `proxy.service_url` without an explicit one is served on. Mirrors the
# schemes `ProxyConfig.SERVICE_URL_REGEX` admits.
SCHEME_DEFAULT_PORTS = {"http": 80, "https": 443}


def _format_url_string(url, is_https=True):
    if url is None:
        return None

    if url.startswith("http://") or url.startswith("https://"):
        return url
    if is_https:
        return f"https://{url}"

    return f"http://{url}"


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
                - (interleaved) Poll the worker endpoints to check their status
                    - showcase how many workers are coming up if things are on the cli side.
                - If the user has set some flag like `--dont-wait-to-fully-finish` then we check the `status.currentlyServedVersion` to see if even one replica is ready to
                serve traffic.
            - once the status.updateInProgress is set to False, it means that the replicas are ready
        - Upgrade:
            - wait for status.updateInProgress to be set to False
                - (interleaved) Poll the worker endpoints to check their status and signal the user the number replicas coming up
                - If the user has set some flag like `--dont-wait-to-fully-finish` then we check the `status.currentlyServedVersion` to see if even one replica is ready to
                serve traffic.
    - Unhappy Path:
        - First time Create :
            - wait for status.updateInProgress to be set to False,
                - (interleaved) Poll the workers to check their status.
                    - If the worker pertaining the current deployment instance version is crashlooping then crash the deployment process with the error messages and logs.
        - Upgrade:
            - wait for status.updateInProgress to be set to False,
                - (interleaved) Poll the workers to check their status.
                    - If the worker pertaining the current deployment instance version is crashlooping then crash the deployment process with the error messages and logs.

    """

    def __init__(self, capsule_id: str, current_deployment_instance_version: str):
        self._capsule_id = capsule_id
        self._status_trail: List[Dict[str, Any]] = []
        self._current_deployment_instance_version = current_deployment_instance_version

    def get_status_trail(self):
        return self._status_trail

    def add_status(self, status: CapsuleStatus):
        self._status_trail.append({"timestamp": time.time(), "status": status})

    @property
    def current_status(self):
        return self._status_trail[-1].get("status")

    @property
    def out_of_cluster_url(self):
        access_info = self.current_status.get("accessInfo", {}) or {}
        return _format_url_string(access_info.get("outOfClusterURL", None), True)

    @property
    def in_cluster_url(self):
        access_info = self.current_status.get("accessInfo", {}) or {}
        return _format_url_string(access_info.get("inClusterURL", None), True)

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
        debug_path = os.path.join(
            state_dir, f"debug_capsule_sm_{self._capsule_id}.json"
        )
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
        # First construct a base64 encoded string of the quoted command
        # One of the reasons we don't directly pass the command string to the backend with a `\n` join
        # is because the backend controller doesn't play nice when the command can be a multi-line string.
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
    def _marshal_proxy_settings(cls, app_config: AppConfig):
        proxy = app_config.get_state("proxy", {}) or {}
        _settings = {}
        if proxy.get("namespace"):
            _settings["namespace"] = proxy["namespace"]
        if proxy.get("selector_labels"):
            _settings["selectorLabels"] = dict(proxy["selector_labels"])
        if proxy.get("service_url"):
            _settings["serviceURL"] = proxy["service_url"]
        return _settings

    @classmethod
    def _port_from_service_url(cls, service_url):
        """The port a `proxy.service_url` points at, or None if it has none.

        `service_url` is `[scheme://]host[:port][/path]`, so the port lives in the
        URL and the config does not make the user set `port` separately in that
        mode. The payload still carries a port, so read it back out here.
        """
        if not service_url:
            return None
        # urlparse reads `my-svc:8080` as scheme `my-svc`, so give it a scheme.
        _url = service_url if "://" in service_url else "http://%s" % service_url
        try:
            _parsed = urlparse(_url)
            _port = _parsed.port
        except ValueError:
            # A port outside 0-65535; config validation reports it properly.
            return None
        if _port is not None:
            return _port
        return SCHEME_DEFAULT_PORTS.get(_parsed.scheme)

    @classmethod
    def _marshal_port(cls, app_config: AppConfig):
        _port = app_config.get_state("port", None)
        if _port is not None:
            return _port
        # The only way to get here is a Proxy capsule fronting an existing
        # service, whose port `port_required` lets the user leave unset.
        proxy = app_config.get_state("proxy", {}) or {}
        return cls._port_from_service_url(proxy.get("service_url"))

    @classmethod
    def from_app_config(cls, app_config: AppConfig):
        ## Replica settings
        replicas = app_config.get_state("replicas", {})
        fixed, _min, _max = (
            replicas.get("fixed"),
            replicas.get("min"),
            replicas.get("max"),
        )
        rpm = replicas.get("scaling_policy", {}).get("rpm", None)
        autoscaling_config = {}
        if rpm:
            autoscaling_config = {
                "requestRateBasedAutoscalingConfig": {"targetRequestsPerMinute": rpm}
            }
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

        # A Proxy capsule runs nothing but the platform's proxy, so there is no user
        # container to hand code or a startup command to.
        _capsule_type = app_config.get_state("capsule_type", None)
        _is_proxy = _capsule_type == CapsuleType.PROXY

        _capsule_type_config = {}
        if _capsule_type is not None:
            _capsule_type_config["capsuleType"] = _capsule_type
        _proxy_settings = cls._marshal_proxy_settings(app_config)
        if _proxy_settings:
            _capsule_type_config["proxySettings"] = _proxy_settings

        # Conditionally include codePackagePath if not skipping code packaging
        _code_package_config = {}
        if not _is_proxy and not app_config.get_state("skip_code_package", False):
            _code_package_config["codePackagePath"] = app_config.get_state(
                "code_package_url"
            )

        # Conditionally include containerStartupConfig if not using base image command
        _startup_config = {}
        if not _is_proxy and not app_config.get_state("use_base_image_command", False):
            _startup_config["containerStartupConfig"] = {
                "entrypoint": cls.construct_exec_command(
                    app_config.get_state("commands")
                )
            }

        _project = app_config.get_state("project", UNASSIGNED_PROJECT_BRANCH)
        _branch = app_config.get_state("branch", UNASSIGNED_PROJECT_BRANCH)

        _tags = [
            dict(key=k, value=v)
            for tag in app_config.get_state("tags", [])
            for k, v in tag.items()
        ]
        if _project != UNASSIGNED_PROJECT_BRANCH:
            _tags.append(dict(key="project", value=_project))
        if _branch != UNASSIGNED_PROJECT_BRANCH:
            _tags.append(dict(key="branch", value=_branch))

        return {
            "perimeter": app_config.get_state("perimeter"),
            "project": _project,
            "branch": _branch,
            **_final_info,
            **_capsule_type_config,
            **_code_package_config,
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
                **autoscaling_config,
            },
            **_scheduling_config,
            **_startup_config,
            "environmentVariables": cls._marshal_environment_variables(app_config),
            "authConfig": {
                "authType": app_config.get_state("auth").get("type"),
                "publicToDeployment": app_config.get_state("auth").get("public"),
            },
            "tags": _tags,
            "port": cls._marshal_port(app_config),
            "displayName": app_config.get_state("name"),
            "forceUpdate": app_config.get_state("force_upgrade", False),
        }

    @classmethod
    def from_backend_spec(cls, spec: dict, patch: dict = None) -> dict:
        """
        Transform a backend spec into a valid create payload.

        The backend returns specs with computed/runtime fields that should
        not be sent back to the create endpoint.

        Parameters
        ----------
        spec : dict
            The spec from backend (via capsule_api.get())
        patch : dict, optional
            Fields to update/merge into the spec

        Returns
        -------
        dict
            A spec ready for the create endpoint
        """
        result = json.loads(json.dumps(spec))
        # We have this if statement only because if the backend
        # gets a `none` persistence it farts out.
        if result.get("persistence") and spec.get("persistence") == "none":
            result.pop("persistence")

        # Apply patch with deep merge for nested dicts
        if patch:
            for key, value in patch.items():
                if (
                    key in result
                    and isinstance(result[key], dict)
                    and isinstance(value, dict)
                ):
                    result[key] = {**result[key], **value}
                else:
                    result[key] = value

        return result


class CapsuleApi:
    def __init__(self, base_url: str, perimeter: str, logger_fn=None, retry_500s=False):
        self._base_url = self._create_base_url(base_url, perimeter)
        from metaflow.metaflow_config import SERVICE_HEADERS

        self._retry_500s = retry_500s
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
        # The CapsuleApi wraps every API call happening to the capsule
        # API. We do this so that we can raise exceptions in a way that make
        # it clearer to the end-user and the operator. since the safe_requests_wrapper
        # can already retry 5xx errors too we should ensure that any time we hit max
        # retries or if we hit 5xx without retries, we should raise a "special" exception
        # and not the CapsuleApiException to notify the operator that the
        # backend is not working right RN and thier application crashes. We can lift the
        # exception to top level to make it importable so operators can deal with that condition
        # how they like.
        except MaximumRetriesExceeded as e:
            if e.status_code >= 500:
                raise OuterboundsBackendUnhealthyException(
                    e.url,
                    e.method,
                    e.status_code,
                    e.text,
                )
            raise CapsuleApiException(
                e.url,
                e.method,
                e.status_code,
                e.text,
                message=f"Maximum retries exceeded for {e.url} [{e.method}]",
            )
        except requests.exceptions.ConnectionError as e:
            # Network connectivity issues after retries exhausted
            raise OuterboundsBackendUnhealthyException(
                url=args[0] if args else "unknown",
                method=method_func.__name__,
                message=(
                    f"Unable to reach Outerbounds backend at {args[0] if args else 'unknown'}. "
                    "This could be due to network connectivity issues, DNS resolution failures, "
                    "or the service being temporarily unavailable. "
                    "Please check your network connection and retry. "
                    "If the issue persists, contact Outerbounds support."
                ),
            ) from e

        if response.status_code >= 500:
            raise OuterboundsBackendUnhealthyException(
                args[0],
                method_func.__name__,
                response.status_code,
                response.text,
                message=(
                    f"Outerbounds backend returned an error (HTTP {response.status_code}). "
                    "This is a server-side issue, not a problem with your configuration. "
                    "Please retry your request. If the issue persists, contact Outerbounds support."
                ),
            )

        elif response.status_code == 403:
            raise OuterboundsForbiddenException(
                args[0],
                method_func.__name__,
                response.text,
            )

        elif response.status_code >= 400:
            raise CapsuleApiException(
                args[0],
                method_func.__name__,
                response.status_code,
                response.text,
            )
        return response

    def _retry_parameters(
        self,
        status_codes,
        retries,
    ):
        """
        All functions calling the wrapped_api_caller use this function
        set the number of retries for the apis calls. It sets status codes
        that are allowed to N retries (total including connection retries).
        If no status codes are passed we should still always pass connnection
        retries > 0 since DNS can be flaky in-frequently and we dont want to
        trip up there.
        """
        kwargs = {}
        if self._retry_500s:
            kwargs = dict(
                retryable_status_codes=status_codes
                + [500, 502, 503, 504],  # todo : verify me
                conn_error_retries=max(
                    3, retries
                ),  # connection retries + any other retries.
            )
        else:
            kwargs = dict(
                retryable_status_codes=status_codes,
                conn_error_retries=retries,  # connection retries + any other retries.
            )
        return kwargs

    def create(self, capsule_input: dict):
        _data = json.dumps(capsule_input)
        response = self._wrapped_api_caller(
            requests.post, self._base_url, data=_data, **self._retry_parameters([], 3)
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

    def get(self, capsule_id: str) -> Dict[str, Any]:
        _url = os.path.join(self._base_url, capsule_id)
        response = self._wrapped_api_caller(
            requests.get, _url, **self._retry_parameters([409, 404], 3)
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

    def list(self, project=None, branch=None, name=None):
        params = {}
        if project:
            params["project"] = project
        if branch:
            params["branch"] = branch
        if name:
            params["displayName"] = name
        response = self._wrapped_api_caller(
            requests.get,
            self._base_url,
            params=params,
            **self._retry_parameters([409], 3),
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
            requests.delete, _url, **self._retry_parameters([409], 3)
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
            # Adding 404s because sometimes we might even end up getting 404s if
            # the backend cache is not updated yet. So on consistent 404s we should
            # just crash out.
            **self._retry_parameters([409, 404], 3),
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
    ) -> List[LogLine]:
        _url = os.path.join(self._base_url, capsule_id, "workers", worker_id, "logs")
        options = None
        if previous:
            options = {"previous": True}
        response = self._wrapped_api_caller(
            requests.get, _url, params=options, **self._retry_parameters([409], 3)
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

    def patch(self, capsule_id: str, patch_input: dict):
        capsule_response = self.get(capsule_id)
        if "spec" not in capsule_response or len(capsule_response.get("spec", {})) == 0:
            raise CapsuleApiException(
                self._base_url,
                "patch",
                403,
                "Capsule response of incorrect format",
            )

        spec = CapsuleInput.from_backend_spec(
            capsule_response.get("spec"), patch=patch_input
        )
        return self.create(spec)


def list_and_filter_capsules(
    capsule_api: CapsuleApi, project, branch, name, tags, auth_type, capsule_id
):
    capsules = capsule_api.list(project=project, branch=branch, name=name)

    def _tags_match(tags, key, value):
        for t in tags:
            if t["key"] == key and t["value"] == value:
                return True
        return False

    def _all_tags_match(tags, tags_to_match):
        return all([_tags_match(tags, t["key"], t["value"]) for t in tags_to_match])

    def _filter_capsules(capsules, tags, auth_type, capsule_id):
        _filtered_capsules = []
        for capsule in capsules:
            set_tags = capsule.get("spec", {}).get("tags", [])
            set_id = capsule.get("id", None)
            set_auth_type = (
                capsule.get("spec", {}).get("authConfig", {}).get("authType", None)
            )

            if auth_type and set_auth_type != auth_type:
                continue
            if tags and not _all_tags_match(set_tags, tags):
                continue
            if capsule_id and set_id != capsule_id:
                continue

            _filtered_capsules.append(capsule)
        return _filtered_capsules

    return _filter_capsules(capsules, tags, auth_type, capsule_id)


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
            retry_500s=True
            # retry for 5xx because during the capsule deployer might even be used
            # programmatically so any intermittent breakage shouldnt break the overall
            # control flow unless the breakage is severe (maybe over 20s of complete outage)
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
            ({} or self._capsule_deploy_response).get("outOfClusterUrl", None), True
        )

    @property
    def capsule_api(self):
        return self._capsule_api

    @property
    def capsule_type(self):
        auth_type = self._app_config.get_state("auth", {}).get("type", AuthType.default)
        if auth_type == AuthType.BROWSER:
            return "App"
        elif auth_type == AuthType.API or auth_type == AuthType.BROWSER_AND_API:
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
        In the situation that the versions of the objects become a mismatch then it means that current deployment process is not giving the user the
        output that they desire.
        """
        if capsule_response.get("version", None) != current_deployment_instance_version:
            metadata = capsule_response.get("metadata", {}) or {}
            raise CapsuleConcurrentUpgradeException(
                self.identifier,  # type: ignore
                expected_version=current_deployment_instance_version,
                actual_version=capsule_response.get("version", None),
                modified_by=metadata.get("lastModifiedBy"),
                modified_at=metadata.get("lastModifiedAt"),
            )

    def _update_capsule_and_worker_sm(
        self,
        capsule_sm: "CapsuleStateMachine",
        workers_sm: "CapsuleWorkersStateMachine",
        logger: Callable[[str], None],
    ) -> Tuple[Dict[str, Any], List[Dict[str, Any]]]:
        try:
            capsule_response = self.get()
        except CapsuleApiException as e:
            # At this point when the code is executing
            # the CapsuleDeployer would already have created
            # the capsule since this function is called within
            # wait_for_terminal_state. Because of that if there
            # is now a 404 then it means someone deleted the
            # deployment WHILE this deployment instance is running
            # We shoud notify the user that something funky has
            # happened over here. We need to do this since Apps can
            # now be programmatically created / deleted, we need to
            # ensure that if some-one has done something concurrent-unsafe
            # (foo deleting bar's deployment while bar is deploying)
            # then for that circumstance we should raise an exception here
            # that something funky has happened. Otherwise if the
            # CapsuleApiException leaks out then it should be fine.
            if e.status_code == 404:
                raise CapsuleDeletedDuringDeploymentException(self.identifier) from e
            raise
        capsule_sm.add_status(capsule_response.get("status", {}))  # type: ignore

        # We need to check if someone has not upgraded the capsule under the hood and
        # the current deployment instance is invalid.
        self._backend_version_mismatch_check(
            capsule_response, self.current_deployment_instance_version  # type: ignore
        )
        workers_response = self.get_workers()
        capsule_sm.report_current_status(logger)
        workers_sm.add_status(workers_response)
        workers_sm.report_current_status(logger)
        return capsule_response, workers_response

    def _publish_capsule_debug_info(
        self,
        capsule_sm: "CapsuleStateMachine",
        workers_sm: "CapsuleWorkersStateMachine",
        capsule_response: Dict[str, Any],
    ):
        if CAPSULE_DEBUG and self._debug_dir:
            capsule_sm.save_debug_info(self._debug_dir)
            workers_sm.save_debug_info(self._debug_dir)
            debug_path = os.path.join(
                self._debug_dir, f"debug_capsule_{self.identifier}.json"
            )
            with open(debug_path, "w") as f:
                f.write(json.dumps(capsule_response, indent=4))

    def _monitor_worker_readiness(
        self,
        workers_sm: "CapsuleWorkersStateMachine",
        capsule_sm: "CapsuleStateMachine",
    ):
        """returns True if the worker is crashlooping, False otherwise"""
        logger = self._logger_fn or partial(print, file=sys.stderr)
        for i in range(self._readiness_wait_time):
            time.sleep(STATE_REFRESH_FREQUENCY)
            self._update_capsule_and_worker_sm(
                capsule_sm, workers_sm, logger
            )  # [2 API calls]
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
                if worker["phase"] == "CrashLoopBackOff" or worker["phase"] == "Failed":
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

        # This loop will check all the conditions that help verify the terminal state.
        # How it works is by extracting the statuses of the capsule and workers and
        # then adding them as a part of a state-machine that helps track transitions and
        # helps derive terminal states.
        # We will first keep checking for terminal conditions or outright failure conditions
        # If we reach a terminal condition like described in `DEPLOYMENT_READY_CONDITIONS`, then
        # we will further check for readiness conditions.
        # The readiness conditions in DEPLOYMENT_READY_CONDITIONS also account for
        # readyToServeTraffic from the backend, so there is no separate phase for
        # waiting on traffic readiness.
        _timed_out = False
        _logged_waiting_for_traffic = False
        for i in range(self._create_timeout):
            time.sleep(STATE_REFRESH_FREQUENCY)
            capsule_response, _ = self._update_capsule_and_worker_sm(  # [2 API calls]
                state_machine, workers_state_machine, logger
            )

            # Check worker readiness and failure conditions.
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
                    "💊 %s deployment status: %s "
                    % (
                        self.capsule_type.title(),
                        (
                            "in progress"
                            if state_machine.update_in_progress
                            else "completed"
                        ),
                    )
                )
                _further_readiness_check_failed = False
                if further_check_worker_readiness:
                    # HACK : monitor the workers for N seconds to make sure they are healthy
                    # this is a hack. Ideally we should implement a healthcheck as a first class citizen
                    # but it will take some time to do that so in the meanwhile a timeout set on the cli
                    # side will be really helpful.
                    logger(
                        "💊 Running last minute readiness check for %s..."
                        % self.identifier
                    )
                    _further_readiness_check_failed = self._monitor_worker_readiness(
                        workers_state_machine,
                        state_machine,
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
                        raise CapsuleCrashLoopException(
                            self.identifier,
                            worker_id=worker_id,
                            logs=logs,
                        )

                # capsule_ready includes readyToServeTraffic check,
                # so we can break directly.
                logger(
                    "💊 %s %s is ready to serve traffic on the URL: %s"
                    % (
                        self.capsule_type,
                        self.identifier,
                        state_machine.out_of_cluster_url,
                    ),
                )
                break

            # Log once when workers are running but capsule is not yet ready
            # to serve traffic (e.g. health checks, routing propagation).
            worker_status = workers_state_machine.current_version_deployment_status()
            if (
                not _logged_waiting_for_traffic
                and worker_status["status"]["at_least_one_running"]
                and not state_machine.ready_to_serve_traffic
            ):
                logger(
                    "💊 Workers are running. Waiting for %s to be ready to serve traffic..."
                    % self.capsule_type.lower()
                )
                _logged_waiting_for_traffic = True

            self._publish_capsule_debug_info(
                state_machine, workers_state_machine, capsule_response
            )

            if CAPSULE_DEBUG and i % 3 == 0:  # Every 3 seconds report the status
                logger(
                    f"[debug] 💊 {self.capsule_type} {self.identifier} deployment status: {state_machine.current_status} | worker states: {workers_state_machine.current_status} | capsule_ready : {capsule_ready} | further_check_worker_readiness {further_check_worker_readiness}"
                )
        else:
            _timed_out = True

        self._publish_capsule_debug_info(
            state_machine, workers_state_machine, capsule_response
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
            raise CapsuleReadinessException(
                self.identifier,
                capsule_status=state_machine.current_status,
                worker_semantic_status=workers_state_machine.current_version_deployment_status(),
                readiness_condition=self._success_terminal_state_condition,
                min_replicas=min_replicas,
                max_wait_time=self._create_timeout,
                timed_out=_timed_out,
            )
        auth_type = self._app_config.get_state("auth", {}).get("type", AuthType.default)
        return dict(
            id=self.identifier,
            auth_type=auth_type,
            public_url=self.url,
            available_replicas=self.status.available_replicas,
            name=self.name,
            deployed_version=self.current_deployment_instance_version,
            deployed_at=datetime.now().isoformat(),
        )
